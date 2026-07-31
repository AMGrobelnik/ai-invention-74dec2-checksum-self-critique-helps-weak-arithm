#!/usr/bin/env python3
"""Build arithmetic-word-problem dataset with checksum (mod-9) error-detection labels.

Two candidate dataset groups are produced (both consumed downstream, this
script keeps them separate for schema/quality comparison):
  - gsm8k_real:        traces auto-extracted from openai/gsm8k <<...>> annotations
  - synthetic_template: procedurally generated word problems with exact traces

For each base item (correct trace) we also emit up to 4 corrupted variants
(one per error type), each labeled checksum_detectable / checksum_invisible
based on whether the mod-9 digit-residue of the corrupted final answer
differs from the correct final answer.
"""

import json
import random
import re
import resource
import sys
from fractions import Fraction
from pathlib import Path

from loguru import logger

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
Path("logs").mkdir(exist_ok=True)
logger.add("logs/run.log", rotation="30 MB", level="DEBUG")

# ---- resource limits (tiny dataset, generous budget) ----
RAM_BUDGET = 2 * 1024**3  # 2GB is far more than this workload needs
resource.setrlimit(resource.RLIMIT_AS, (RAM_BUDGET * 3, RAM_BUDGET * 3))

WORKSPACE = Path(__file__).parent
GSM8K_TRAIN = WORKSPACE / "temp/datasets/full_openai_gsm8k_main_train.json"
GSM8K_TEST = WORKSPACE / "temp/datasets/full_openai_gsm8k_main_test.json"
OUT_PATH = WORKSPACE / "full_data_out.json"

RNG = random.Random(20260731)

CALC_RE = re.compile(r"<<([^=<>]+)=(-?[\d,]*\.?\d+)>>")
OP_RE = re.compile(r"^\s*(-?[\d.]+)\s*([+\-*/])\s*(-?[\d.]+)\s*$")
FINAL_RE = re.compile(r"####\s*(-?[\d,]*\.?\d+)")

EPS = 1e-6


def to_num(s: str):
    s = s.replace(",", "")
    f = float(s)
    i = int(f)
    return i if abs(f - i) < EPS else f


def mod9_residue(n) -> int:
    """Digit root of |n| via mod-9, mapping 0 residue to 9 (except n==0 -> 0)."""
    n = abs(round(n)) if isinstance(n, float) else abs(n)
    if n == 0:
        return 0
    r = n % 9
    return 9 if r == 0 else r


# =====================================================================
# 1) GSM8K real-item trace extraction
# =====================================================================


def extract_gsm8k_steps(answer_text: str):
    """Parse <<op1 OP op2=result>> annotations into an ordered step list.

    Returns None if any annotation fails to parse as a clean binary op,
    or if the final #### answer doesn't match the last extracted step.
    """
    matches = CALC_RE.findall(answer_text)
    if not matches:
        return None

    steps = []
    for step_idx, (expr, result_str) in enumerate(matches):
        m = OP_RE.match(expr)
        if not m:
            return None  # non-binary or malformed annotation -> discard item
        op1_str, op, op2_str = m.groups()
        try:
            op1, op2, result = to_num(op1_str), to_num(op2_str), to_num(result_str)
        except ValueError:
            return None

        depends_on = []
        for prior_idx, prior_step in enumerate(steps):
            for candidate in (op1, op2):
                if abs(candidate - prior_step["result"]) < EPS:
                    depends_on.append(prior_idx)
                    break
        steps.append(
            {
                "step_index": step_idx,
                "operand_1": op1,
                "operand_2": op2,
                "operation": op,
                "result": result,
                "depends_on_step": sorted(set(depends_on)) or None,
            }
        )

    final_match = FINAL_RE.search(answer_text)
    if not final_match:
        return None
    try:
        final_answer = to_num(final_match.group(1))
    except ValueError:
        return None
    if abs(final_answer - steps[-1]["result"]) > max(EPS, abs(final_answer) * 1e-4):
        return None  # trace doesn't lead to the stated final answer -> discard

    return steps, final_answer


def numeric_range_of(steps) -> str:
    for s in steps:
        for v in (s["operand_1"], s["operand_2"], s["result"]):
            if abs(v) >= 100:
                return "large"
    return "small"


def load_gsm8k_base_items(max_per_cell: int = 20):
    raw = json.loads(GSM8K_TRAIN.read_text()) + json.loads(GSM8K_TEST.read_text())
    logger.info(f"Loaded {len(raw)} raw GSM8K rows (train+test combined)")

    by_cell: dict[tuple[int, str], list[dict]] = {}
    n_discarded = 0
    for row_idx, row in enumerate(raw):
        parsed = extract_gsm8k_steps(row["answer"])
        if parsed is None:
            n_discarded += 1
            continue
        steps, final_answer = parsed
        chain_length = len(steps)
        if not (2 <= chain_length <= 6):
            n_discarded += 1
            continue
        nrange = numeric_range_of(steps)
        item = {
            "item_id": f"gsm8k_{row_idx}",
            "problem_text": row["question"],
            "final_answer": final_answer,
            "trace": steps,
            "item_source": "gsm8k_real",
            "numeric_range": nrange,
            "chain_length": chain_length,
        }
        by_cell.setdefault((chain_length, nrange), []).append(item)

    logger.info(
        f"GSM8K: {sum(len(v) for v in by_cell.values())} clean-parsed items, "
        f"{n_discarded} discarded (unparseable / bad chain_length / trace mismatch)"
    )

    selected = []
    for cell, items in sorted(by_cell.items()):
        RNG.shuffle(items)
        take = items[:max_per_cell]
        selected.extend(take)
        logger.info(f"  cell chain_length={cell[0]} numeric_range={cell[1]}: {len(take)}/{len(items)} taken")
    return selected


# =====================================================================
# 2) Synthetic template generator (fills gaps GSM8K under-represents:
#    large numbers, long chains)
# =====================================================================


def gen_shopping(chain_length: int, nrange: str, item_id: str):
    """Buy N items at unit price, apply repeated discounts/additions."""
    lo, hi = (2, 40) if nrange == "small" else (120, 900)
    price = RNG.randint(lo, hi)
    qty = RNG.randint(2, 9)
    steps = []
    result = price * qty
    steps.append({"step_index": 0, "operand_1": price, "operand_2": qty, "operation": "*", "result": result, "depends_on_step": None})
    text_parts = [f"An item costs ${price} and a shopper buys {qty} of them."]
    for i in range(1, chain_length):
        if i % 2 == 1:
            extra = RNG.randint(1, max(1, hi // 4))
            new_result = result + extra
            text_parts.append(f"Then the shopper adds ${extra} in shipping/extra fees.")
            steps.append({"step_index": i, "operand_1": result, "operand_2": extra, "operation": "+", "result": new_result, "depends_on_step": [i - 1]})
        else:
            frac = RNG.choice([2, 4, 5])
            discount = result // frac
            new_result = result - discount
            text_parts.append(f"Then a discount of one-{frac}th of the running total is applied.")
            steps.append({"step_index": i, "operand_1": result, "operand_2": discount, "operation": "-", "result": new_result, "depends_on_step": [i - 1]})
        result = new_result
    text_parts.append("What is the final total?")
    return " ".join(text_parts), steps, result


def gen_recipe_scaling(chain_length: int, nrange: str, item_id: str):
    """Scale ingredient amounts across a multi-step recipe conversion chain."""
    lo, hi = (2, 20) if nrange == "small" else (110, 800)
    base_amount = RNG.randint(lo, hi)
    scale = RNG.randint(2, 6)
    steps = []
    result = base_amount * scale
    steps.append({"step_index": 0, "operand_1": base_amount, "operand_2": scale, "operation": "*", "result": result, "depends_on_step": None})
    text_parts = [f"A recipe uses {base_amount} grams of an ingredient per batch, and a baker scales it up to {scale} batches."]
    for i in range(1, chain_length):
        if i % 2 == 1:
            waste = RNG.randint(1, max(1, hi // 5))
            new_result = result - waste
            text_parts.append(f"{waste} grams are lost to spillage during mixing.")
            steps.append({"step_index": i, "operand_1": result, "operand_2": waste, "operation": "-", "result": new_result, "depends_on_step": [i - 1]})
        else:
            portions = pick_exact_divisor(result, [2, 3, 4])
            if portions is None:
                bonus = RNG.randint(1, max(1, hi // 5))
                new_result = result + bonus
                text_parts.append(f"An extra {bonus} grams are added from a backup batch.")
                steps.append({"step_index": i, "operand_1": result, "operand_2": bonus, "operation": "+", "result": new_result, "depends_on_step": [i - 1]})
            else:
                new_result = result // portions
                text_parts.append(f"The batter is then split evenly into {portions} equal portions and only one portion is kept.")
                steps.append({"step_index": i, "operand_1": result, "operand_2": portions, "operation": "/", "result": new_result, "depends_on_step": [i - 1]})
        result = new_result
    text_parts.append("How many grams remain in the kept portion?")
    return " ".join(text_parts), steps, result


def gen_distance_rate_time(chain_length: int, nrange: str, item_id: str):
    """Multi-leg trip: distance = rate * time, then combine legs."""
    lo_rate, hi_rate = (3, 15) if nrange == "small" else (60, 200)
    rate = RNG.randint(lo_rate, hi_rate)
    time_ = RNG.randint(2, 8)
    steps = []
    result = rate * time_
    steps.append({"step_index": 0, "operand_1": rate, "operand_2": time_, "operation": "*", "result": result, "depends_on_step": None})
    text_parts = [f"A traveler moves at {rate} units per hour for {time_} hours on the first leg of a trip."]
    for i in range(1, chain_length):
        if i % 2 == 1:
            leg_rate = RNG.randint(lo_rate, hi_rate)
            leg_time = RNG.randint(1, 6)
            leg_dist = leg_rate * leg_time
            new_result = result + leg_dist
            text_parts.append(f"On the next leg they travel {leg_time} more hours at {leg_rate} units per hour.")
            steps.append({"step_index": i, "operand_1": result, "operand_2": leg_dist, "operation": "+", "result": new_result, "depends_on_step": [i - 1]})
        else:
            backtrack = RNG.randint(1, max(1, hi_rate // 2))
            new_result = result - backtrack
            text_parts.append(f"They then backtrack {backtrack} units to retrieve a dropped item.")
            steps.append({"step_index": i, "operand_1": result, "operand_2": backtrack, "operation": "-", "result": new_result, "depends_on_step": [i - 1]})
        result = new_result
    text_parts.append("What is the total distance covered?")
    return " ".join(text_parts), steps, result


def gen_unit_conversion(chain_length: int, nrange: str, item_id: str):
    """Chain of unit conversions (e.g. minutes -> hours-equivalent tallies)."""
    lo, hi = (5, 90) if nrange == "small" else (150, 999)
    amount = RNG.randint(lo, hi)
    factor = RNG.choice([2, 3, 4, 5])
    steps = []
    result = amount * factor
    steps.append({"step_index": 0, "operand_1": amount, "operand_2": factor, "operation": "*", "result": result, "depends_on_step": None})
    text_parts = [f"A worker logs {amount} units of work and a supervisor multiplies it by a conversion factor of {factor}."]
    for i in range(1, chain_length):
        if i % 2 == 1:
            bonus = RNG.randint(1, max(1, hi // 3))
            new_result = result + bonus
            text_parts.append(f"A bonus of {bonus} converted units is added.")
            steps.append({"step_index": i, "operand_1": result, "operand_2": bonus, "operation": "+", "result": new_result, "depends_on_step": [i - 1]})
        else:
            div = pick_exact_divisor(result, [2, 3])
            if div is None:
                bonus = RNG.randint(1, max(1, hi // 4))
                new_result = result + bonus
                text_parts.append(f"An extra {bonus} converted units are credited.")
                steps.append({"step_index": i, "operand_1": result, "operand_2": bonus, "operation": "+", "result": new_result, "depends_on_step": [i - 1]})
            else:
                new_result = result // div
                text_parts.append(f"The total is then divided evenly among {div} teams and one team's share is reported.")
                steps.append({"step_index": i, "operand_1": result, "operand_2": div, "operation": "/", "result": new_result, "depends_on_step": [i - 1]})
        result = new_result
    text_parts.append("What is the final converted amount for that team?")
    return " ".join(text_parts), steps, result


def gen_inventory_accounting(chain_length: int, nrange: str, item_id: str):
    """Multi-step stock in/out ledger."""
    lo, hi = (10, 60) if nrange == "small" else (200, 950)
    stock = RNG.randint(lo, hi)
    restock = RNG.randint(lo // 2 or 1, hi // 2)
    steps = []
    result = stock + restock
    steps.append({"step_index": 0, "operand_1": stock, "operand_2": restock, "operation": "+", "result": result, "depends_on_step": None})
    text_parts = [f"A warehouse starts with {stock} units in stock and receives a restock of {restock} units."]
    for i in range(1, chain_length):
        if i % 2 == 1:
            sold = RNG.randint(1, max(1, result // 3))
            new_result = result - sold
            text_parts.append(f"Then {sold} units are sold.")
            steps.append({"step_index": i, "operand_1": result, "operand_2": sold, "operation": "-", "result": new_result, "depends_on_step": [i - 1]})
        else:
            crates = pick_exact_divisor(result, [2, 3, 4])
            if crates is None:
                sold = RNG.randint(1, max(1, result // 4))
                new_result = result - sold
                text_parts.append(f"Then {sold} more units are sold before repacking.")
                steps.append({"step_index": i, "operand_1": result, "operand_2": sold, "operation": "-", "result": new_result, "depends_on_step": [i - 1]})
            else:
                new_result = result // crates
                text_parts.append(f"The remaining stock is repacked into {crates} equal-sized crates and one crate is shipped out for audit.")
                steps.append({"step_index": i, "operand_1": result, "operand_2": crates, "operation": "/", "result": new_result, "depends_on_step": [i - 1]})
        result = new_result
    text_parts.append("How many units are in the audited crate?")
    return " ".join(text_parts), steps, result


def pick_exact_divisor(value: int, candidates: list[int]):
    """Return a candidate divisor that evenly divides value, or None."""
    options = [c for c in candidates if c > 0 and value % c == 0]
    return RNG.choice(options) if options else None


TEMPLATES = [gen_shopping, gen_recipe_scaling, gen_distance_rate_time, gen_unit_conversion, gen_inventory_accounting]


def generate_synthetic_items(per_cell: int = 20):
    items = []
    idx = 0
    for chain_length in range(2, 7):
        for nrange in ("small", "large"):
            for _ in range(per_cell):
                template = TEMPLATES[idx % len(TEMPLATES)]
                item_id = f"synthetic_{idx}"
                text, steps, final_answer = template(chain_length, nrange, item_id)
                # verify constructed trace actually reduces to final_answer
                assert abs(steps[-1]["result"] - final_answer) < EPS, "generator internal trace mismatch"
                items.append(
                    {
                        "item_id": item_id,
                        "problem_text": text,
                        "final_answer": final_answer,
                        "trace": steps,
                        "item_source": "synthetic_template",
                        "numeric_range": numeric_range_of(steps),
                        "chain_length": chain_length,
                    }
                )
                idx += 1
    logger.info(f"Synthetic: generated {len(items)} template items across chain_length 2-6 x {{small,large}}")
    return items


# =====================================================================
# 3) Error injection (deterministic, pure arithmetic)
# =====================================================================


def apply_op(op1, op, op2):
    if op == "+":
        return op1 + op2
    if op == "-":
        return op1 - op2
    if op == "*":
        return op1 * op2
    if op == "/":
        if op2 == 0:
            return None
        val = op1 / op2
        return round(val, 6)
    raise ValueError(op)


def recompute_full_trace(steps, changed_idx, new_result):
    """Given steps[changed_idx].result replaced by new_result, recompute every
    downstream step whose operand(s) referenced the (now-changed) upstream
    result, propagating through the rest of the chain. Returns a list of
    per-step dicts {operand_1, operand_2, result} for the FULL corrupted
    trace (all steps, not just downstream ones), or None if recomputation
    hits an invalid operation (e.g. division by a corrupted zero)."""
    orig_results = [s["result"] for s in steps]
    corrupted = [dict(operand_1=s["operand_1"], operand_2=s["operand_2"], result=s["result"]) for s in steps]
    corrupted[changed_idx]["result"] = new_result

    for i in range(changed_idx + 1, len(steps)):
        s = steps[i]
        op1, op2 = s["operand_1"], s["operand_2"]
        changed = False
        # any operand that equals a prior step's ORIGINAL result gets swapped
        # for that prior step's CORRUPTED result if it differs
        for j in range(i):
            if abs(orig_results[j] - corrupted[j]["result"]) < EPS:
                continue  # that upstream step wasn't altered, nothing to propagate
            if abs(op1 - orig_results[j]) < EPS:
                op1 = corrupted[j]["result"]
                changed = True
            if abs(op2 - orig_results[j]) < EPS:
                op2 = corrupted[j]["result"]
                changed = True
        if not changed:
            continue
        new_val = apply_op(op1, s["operation"], op2)
        if new_val is None:
            return None
        corrupted[i] = dict(operand_1=op1, operand_2=op2, result=new_val)
    return corrupted


def recompute_downstream(steps, changed_idx, new_result):
    """Final corrupted answer after propagating a corruption at changed_idx."""
    full_trace = recompute_full_trace(steps, changed_idx, new_result)
    if full_trace is None:
        return None
    return full_trace[-1]["result"]


def err_digit_transposition(steps, step_idx):
    s = steps[step_idx]
    result_int = int(round(s["result"]))
    digits = list(str(abs(result_int)))
    if len(digits) < 2:
        return None
    pos = RNG.randrange(len(digits) - 1)
    digits[pos], digits[pos + 1] = digits[pos + 1], digits[pos]
    corrupted = int("".join(digits))
    if result_int < 0:
        corrupted = -corrupted
    if corrupted == result_int:
        return None
    return corrupted


def err_dropped_carry(steps, step_idx):
    s = steps[step_idx]
    result_int = int(round(s["result"]))
    if abs(result_int) < 10:
        return None
    power = 10 ** RNG.randint(1, max(1, len(str(abs(result_int))) - 1))
    corrupted = result_int - power
    if corrupted == result_int:
        return None
    return corrupted


def err_sign_flip(steps, step_idx):
    s = steps[step_idx]
    if s["operation"] not in ("+", "-"):
        return None
    flipped_op = "-" if s["operation"] == "+" else "+"
    corrupted = apply_op(s["operand_1"], flipped_op, s["operand_2"])
    if corrupted is None or abs(corrupted - s["result"]) < EPS:
        return None
    return corrupted


def err_wrong_operand(steps, step_idx):
    s = steps[step_idx]
    other_vals = [st["result"] for j, st in enumerate(steps) if j != step_idx]
    other_vals += [st["operand_1"] for j, st in enumerate(steps) if j != step_idx]
    other_vals = [v for v in other_vals if abs(v - s["operand_1"]) > EPS and abs(v - s["operand_2"]) > EPS]
    if not other_vals:
        return None
    wrong_op2 = RNG.choice(other_vals)
    corrupted = apply_op(s["operand_1"], s["operation"], wrong_op2)
    if corrupted is None or abs(corrupted - s["result"]) < EPS:
        return None
    return corrupted


ERROR_FUNCS = {
    "digit_transposition": err_digit_transposition,
    "dropped_carry": err_dropped_carry,
    "sign_flip": err_sign_flip,
    "wrong_operand_substitution": err_wrong_operand,
}


def render_corrupted_trace(problem_text, steps, full_corrupted_trace):
    lines = [f"Problem: {problem_text}", "Reasoning trace:"]
    for i, s in enumerate(steps):
        c = full_corrupted_trace[i]
        lines.append(f"  Step {i}: {c['operand_1']} {s['operation']} {c['operand_2']} = {c['result']}")
    return "\n".join(lines)


def make_error_variants(item, skip_log):
    variants = []
    steps = item["trace"]
    for error_type, fn in ERROR_FUNCS.items():
        candidate_order = list(range(len(steps)))
        RNG.shuffle(candidate_order)

        step_idx = corrupted_result = full_corrupted_trace = corrupted_final = None
        for alt_idx in candidate_order:
            alt_result = fn(steps, alt_idx)
            if alt_result is None:
                continue
            alt_trace = recompute_full_trace(steps, alt_idx, alt_result)
            if alt_trace is None:
                continue
            alt_final = alt_trace[-1]["result"]
            if abs(alt_final - item["final_answer"]) < EPS:
                continue  # orphan/parallel sub-calc: corruption doesn't reach the final answer
            step_idx, corrupted_result, full_corrupted_trace, corrupted_final = alt_idx, alt_result, alt_trace, alt_final
            break

        if step_idx is None:
            skip_log.append((item["item_id"], error_type))
            continue

        residue_correct = mod9_residue(item["final_answer"])
        residue_corrupted = mod9_residue(corrupted_final)
        preserved = residue_correct == residue_corrupted
        label = "checksum_invisible" if preserved else "checksum_detectable"

        variants.append(
            {
                "base_item_id": item["item_id"],
                "error_type": error_type,
                "injected_step_index": step_idx,
                "original_step": dict(steps[step_idx]),
                "corrupted_step": {**steps[step_idx], **full_corrupted_trace[step_idx]},
                "full_corrupted_trace": full_corrupted_trace,
                "corrupted_final_answer": corrupted_final,
                "mod9_residue_preserved": preserved,
                "label": label,
                "problem_text": item["problem_text"],
                "trace": steps,
                "item_source": item["item_source"],
                "numeric_range": item["numeric_range"],
                "chain_length": item["chain_length"],
            }
        )
    return variants


# =====================================================================
# 4) Row rendering (exp_sel_data_out.json schema)
# =====================================================================


def base_item_to_row(item, fold: int):
    return {
        "input": item["problem_text"],
        "output": str(item["final_answer"]),
        "metadata_row_type": "base_item",
        "metadata_item_id": item["item_id"],
        "metadata_item_source": item["item_source"],
        "metadata_numeric_range": item["numeric_range"],
        "metadata_chain_length": item["chain_length"],
        "metadata_trace": item["trace"],
        "metadata_final_answer": item["final_answer"],
        "metadata_fold": fold,
    }


def variant_to_row(variant, fold: int):
    return {
        "input": render_corrupted_trace(variant["problem_text"], variant["trace"], variant["full_corrupted_trace"]),
        "output": f"{variant['label']}|correct_final_answer={variant['trace'][-1]['result']}",
        "metadata_row_type": "error_variant",
        "metadata_base_item_id": variant["base_item_id"],
        "metadata_error_type": variant["error_type"],
        "metadata_injected_step_index": variant["injected_step_index"],
        "metadata_original_step": variant["original_step"],
        "metadata_corrupted_step": variant["corrupted_step"],
        "metadata_corrupted_final_answer": variant["corrupted_final_answer"],
        "metadata_mod9_residue_preserved": variant["mod9_residue_preserved"],
        "metadata_label": variant["label"],
        "metadata_item_source": variant["item_source"],
        "metadata_numeric_range": variant["numeric_range"],
        "metadata_chain_length": variant["chain_length"],
        "metadata_fold": fold,
    }


def assign_fold(rng: random.Random) -> int:
    """80/20 split encoded as fold 0 (train) / 1 (test)."""
    return 1 if rng.random() < 0.2 else 0


def build_dataset_group(name: str, base_items: list[dict]):
    rows = []
    skip_log: list[tuple[str, str]] = []
    for item in base_items:
        fold = assign_fold(RNG)
        rows.append(base_item_to_row(item, fold))
        for variant in make_error_variants(item, skip_log):
            rows.append(variant_to_row(variant, fold))
    if skip_log:
        logger.info(f"[{name}] {len(skip_log)} error-injection skips (structurally inapplicable): sample={skip_log[:5]}")
    n_base = sum(1 for r in rows if r["metadata_row_type"] == "base_item")
    n_variant = sum(1 for r in rows if r["metadata_row_type"] == "error_variant")
    logger.info(f"[{name}] {n_base} base rows + {n_variant} error-variant rows = {len(rows)} total")
    return rows


def main():
    logger.info("Loading & extracting GSM8K real base items")
    gsm8k_items = load_gsm8k_base_items(max_per_cell=20)

    logger.info("Generating synthetic template base items")
    synthetic_items = generate_synthetic_items(per_cell=20)

    logger.info("Building gsm8k_real rows (base + error variants)")
    gsm8k_rows = build_dataset_group("gsm8k_real", gsm8k_items)

    logger.info("Building synthetic_template rows (base + error variants)")
    synthetic_rows = build_dataset_group("synthetic_template", synthetic_items)

    # Single combined dataset per the artifact plan (target_num_datasets: 1):
    # gsm8k_real + synthetic_template are complementary components of one
    # arithmetic-checksum benchmark, not separate candidate datasets.
    all_rows = gsm8k_rows + synthetic_rows
    out = {
        "metadata": {
            "source": "openai/gsm8k (main config, train+test) + procedural synthetic template generator",
            "description": "Multi-step arithmetic word problems with computation traces, plus deterministic error-injection variants labeled by mod-9 checksum detectability.",
        },
        "datasets": [
            {"dataset": "arithmetic_checksum_dataset", "examples": all_rows},
        ],
    }
    OUT_PATH.write_text(json.dumps(out, indent=2))
    logger.info(f"Wrote {OUT_PATH} ({OUT_PATH.stat().st_size / 1e6:.2f} MB), {len(all_rows)} total rows")


if __name__ == "__main__":
    main()
