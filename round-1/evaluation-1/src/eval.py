#!/usr/bin/env python3
"""Evaluation: does a checksum self-critique beat free-form self-critique and a
matched-length placebo on multi-step arithmetic word problems?

Loads predictions from gen_art_experiment_1 (checkpoint.json / method_out.json),
re-derives the checksum-detectability ground truth deterministically (same
synthetic-problem-generation + error-injection seeds as the experiment used),
and computes accuracy, detection/correction confusion matrices, paired
significance tests with Holm-Bonferroni correction, a length-confound
regression, an LLM-judge checksum-computation audit, and a checksum-invisible
negative control.
"""

from __future__ import annotations

import argparse
import json
import random
import re
import resource
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import numpy as np
import psutil
from loguru import logger
from scipy.stats import binomtest

WORKSPACE = Path(__file__).resolve().parent
LOGS_DIR = WORKSPACE / "logs"
LOGS_DIR.mkdir(exist_ok=True)

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(LOGS_DIR / "run.log", rotation="30 MB", level="DEBUG")

# --------------------------------------------------------------------------- #
# Resource limits (this workload is small: a few thousand JSON records + a
# bounded number of LLM-judge calls)
# --------------------------------------------------------------------------- #
_avail = psutil.virtual_memory().available
RAM_BUDGET = int(min(4 * 1024**3, _avail * 0.5))
resource.setrlimit(resource.RLIMIT_AS, (RAM_BUDGET * 3, RAM_BUDGET * 3))

EXPERIMENT_DIR = WORKSPACE.parent / "gen_art_experiment_1"
DATASET_DIR = WORKSPACE.parent / "gen_art_dataset_1"

sys.path.insert(
    0, "/home/adrian/projects/ai-inventor/.claude/skills/aii-openrouter-llms/scripts"
)
import aii_or_call_llms as orcall  # noqa: E402

# --------------------------------------------------------------------------- #
# Reproduce the experiment's deterministic problem generation + error
# injection so we get a per-problem checksum-detectable ground-truth label
# WITHOUT re-calling any LLM. Mirrors gen_art_experiment_1/method.py exactly
# (same TEMPLATES/NAMES/UNITS/seeds) so the reproduced trace matches 1:1.
# --------------------------------------------------------------------------- #

TEMPLATES = [
    "{name} starts with {a} {unit}. They receive {b} more {unit} from a friend.",
    "A warehouse has {a} {unit}. A shipment of {b} {unit} arrives.",
    "{name} has {a} {unit} and buys {b} more {unit} at the store.",
]
NAMES = ["Maria", "Jamal", "Wei", "Fatima", "Diego", "Priya", "Noah", "Aiko"]
UNITS = ["apples", "boxes", "coins", "stickers", "marbles", "tickets", "widgets"]


class Problem:
    def __init__(self, pid: str, text: str, trace: list, gold_answer: int):
        self.pid = pid
        self.text = text
        self.trace = trace
        self.gold_answer = gold_answer


def gen_synthetic_problem(pid: str, rng: random.Random) -> Problem:
    n_steps = rng.randint(3, 4)
    name = rng.choice(NAMES)
    unit = rng.choice(UNITS)
    a0 = rng.randint(20, 500)
    b0 = rng.randint(10, 300)
    template = rng.choice(TEMPLATES)
    text_parts = [template.format(name=name, unit=unit, a=a0, b=b0)]
    trace = []
    cur = a0 + b0
    trace.append({"a": a0, "op": "+", "b": b0, "result": cur})
    for _ in range(n_steps - 1):
        remaining_ops = ["+", "-", "*"]
        if cur >= 4:
            remaining_ops.append("//")
        op = rng.choice(remaining_ops)
        if op == "+":
            b = rng.randint(5, 200)
            text_parts.append(f"Then {name} receives {b} more {unit}.")
            new_val = cur + b
        elif op == "-":
            b = rng.randint(5, max(6, min(cur - 1, 200)))
            b = min(b, cur - 1) if cur > 1 else 0
            text_parts.append(f"Then {name} gives away {b} {unit}.")
            new_val = cur - b
        elif op == "*":
            b = rng.randint(2, 4)
            text_parts.append(
                f"Then the number of {unit} is multiplied by {b} (e.g. distributed evenly {b} times over)."
            )
            new_val = cur * b
        else:
            b = rng.choice([2, 3, 4, 5])
            text_parts.append(
                f"Then the {unit} are split evenly into {b} groups and {name} keeps one group."
            )
            new_val = cur // b
        trace.append({"a": cur, "op": op, "b": b, "result": new_val})
        cur = new_val
    text_parts.append(f"How many {unit} does {name} have now?")
    return Problem(pid=pid, text=" ".join(text_parts), trace=trace, gold_answer=cur)


def build_problem_set(n: int, seed: int = 42) -> list[Problem]:
    rng = random.Random(seed)
    return [gen_synthetic_problem(f"synth_{i:04d}", rng) for i in range(n)]


def digit_root(x: int) -> int:
    x = abs(int(x))
    if x == 0:
        return 0
    return 1 + (x - 1) % 9


def checksum_consistent(a: int, op: str, b: int, result: int) -> bool:
    da, db, dr = digit_root(a), digit_root(b), digit_root(result)
    if op == "+":
        return (da + db) % 9 == dr % 9 or (da + db == 0 and dr == 0)
    if op == "-":
        return (da - db) % 9 == dr % 9
    if op == "*":
        return (da * db) % 9 == dr % 9 or (da * db == 0 and dr == 0)
    if op == "//":
        if b == 0:
            return False
        remainder = a - b * result
        return checksum_consistent(b, "*", result, a - remainder)
    raise ValueError(f"unknown op {op}")


def inject_error(problem: Problem, rng: random.Random) -> dict | None:
    if not problem.trace:
        return None
    idx = rng.randrange(len(problem.trace))
    step = problem.trace[idx]
    perturb_kind = rng.choice(["off_by_one_digit", "transpose_digits", "off_by_carry"])
    wrong_result = step["result"]
    if perturb_kind == "off_by_one_digit":
        delta = rng.choice([-1, 1]) * rng.choice([1, 10])
        wrong_result = step["result"] + delta
    elif perturb_kind == "transpose_digits":
        s = str(abs(step["result"]))
        if len(s) >= 2:
            i = rng.randrange(len(s) - 1)
            s2 = s[:i] + s[i + 1] + s[i] + s[i + 2 :]
            wrong_result = int(s2) if step["result"] >= 0 else -int(s2)
        else:
            wrong_result = step["result"] + 10
    else:
        wrong_result = step["result"] + rng.choice([-9, 9, -18, 18])
    if wrong_result == step["result"]:
        wrong_result += 1
    return {
        "problem_id": problem.pid,
        "step_index": idx,
        "a": step["a"],
        "op": step["op"],
        "b": step["b"],
        "correct_result": step["result"],
        "wrong_result": wrong_result,
    }


def characterize_errors(problems: list[Problem], seed: int = 7) -> dict:
    """Reproduces method.py's characterize_errors() bit-for-bit to recover the
    per-problem checksum_detectable ground-truth label the experiment used
    internally but did not export per example."""
    rng = random.Random(seed)
    detectable_by_pid: dict[str, bool] = {}
    for problem in problems:
        err = inject_error(problem, rng)
        if err is None:
            continue
        flagged = not checksum_consistent(err["a"], err["op"], err["b"], err["wrong_result"])
        detectable_by_pid[problem.pid] = flagged
    return detectable_by_pid


def verify_reproduction(problems: list[Problem], experiment_meta: dict) -> None:
    """Sanity-check our reproduced characterization against the experiment's
    own reported checksum_detectable_fraction before trusting it for metrics."""
    detectable_by_pid = characterize_errors(problems)
    n_detectable = sum(detectable_by_pid.values())
    n_total = len(detectable_by_pid)
    fraction = n_detectable / n_total if n_total else 0.0
    reported = experiment_meta.get("checksum_detectable_fraction")
    reported_n = experiment_meta.get("n_checksum_detectable")
    reported_total = experiment_meta.get("n_injected_errors_characterized")
    logger.info(
        f"Reproduced characterization: {n_detectable}/{n_total} detectable "
        f"(fraction={fraction:.3f}) vs experiment-reported "
        f"{reported_n}/{reported_total} (fraction={reported})"
    )
    if reported_total is not None and n_total != reported_total:
        raise RuntimeError(
            f"Reproduction mismatch: got {n_total} characterized problems, "
            f"experiment reported {reported_total} — seeds/logic diverged, "
            f"cannot trust the recovered checksum_detectable labels"
        )
    if reported is not None and abs(fraction - reported) > 1e-9:
        raise RuntimeError(
            f"Reproduction mismatch: fraction {fraction} != reported {reported} "
            f"— seeds/logic diverged, cannot trust the recovered checksum_detectable labels"
        )
    logger.info("Reproduction VERIFIED exactly against experiment metadata.")


# --------------------------------------------------------------------------- #
# Load experiment predictions
# --------------------------------------------------------------------------- #


def load_experiment_records(n_examples: int | None = None) -> tuple[list[dict], dict]:
    """Prefer the final method_out.json; fall back to the checkpoint (the
    experiment writes it incrementally and it holds the raw per-task records
    in the exact same shape method_out.json's per_condition_metrics were
    computed from)."""
    method_out_path = EXPERIMENT_DIR / "method_out.json"
    checkpoint_path = EXPERIMENT_DIR / "checkpoint.json"
    pilot_path = EXPERIMENT_DIR / "pilot_method_out.json"

    meta: dict = {}
    if method_out_path.exists():
        logger.info(f"Loading finished experiment output: {method_out_path}")
        out = json.loads(method_out_path.read_text())
        meta = out["metadata"]
        records = _records_from_method_out(out)
        source = "method_out.json"
    elif checkpoint_path.exists():
        logger.info(f"method_out.json not present yet; loading raw checkpoint: {checkpoint_path}")
        records = json.loads(checkpoint_path.read_text())
        source = "checkpoint.json (experiment may still be running)"
    elif pilot_path.exists():
        logger.warning("No full-run output found; falling back to PILOT output only")
        out = json.loads(pilot_path.read_text())
        meta = out["metadata"]
        records = _records_from_method_out(out)
        source = "pilot_method_out.json"
    else:
        raise FileNotFoundError(
            "No experiment output found (method_out.json / checkpoint.json / pilot_method_out.json)"
        )

    records = [r for r in records if "error" not in r]
    if n_examples is not None:
        pids = sorted({r["problem_id"] for r in records}, key=lambda p: p)[:n_examples]
        pid_set = set(pids)
        records = [r for r in records if r["problem_id"] in pid_set]
    logger.info(f"Loaded {len(records)} usable records from {source}")
    return records, meta


def _records_from_method_out(out: dict) -> list[dict]:
    """method_out.json stores predictions inlined per example as
    predict_<condition>_<tier> JSON strings; flatten back into per-task
    records equivalent to the experiment's raw checkpoint rows."""
    # predict_* blobs don't carry problem_id (not stored per-prediction in
    # method_out.json's schema); reconstruct it from example order instead,
    # which is stable and 1:1 with build_problem_set().
    records = []
    for i, ex in enumerate(out["datasets"][0]["examples"]):
        pid = f"synth_{i:04d}"
        gold = ex["metadata_gold_answer"]
        for key, val in ex.items():
            if not key.startswith("predict_"):
                continue
            payload = json.loads(val)
            rest = key[len("predict_") :]
            if rest.startswith("oracle_"):
                condition = "oracle_detection_isolation"
                tier = rest[len("oracle_") :]
            else:
                tier = rest.rsplit("_", 1)[-1]
                condition = rest[: -(len(tier) + 1)]
            model_id = next(
                (m["id"] for m in out["metadata"]["models"] if m["tier"] == tier), tier
            )
            fa = payload.get("final_answer")
            records.append(
                {
                    "model": model_id,
                    "tier": tier,
                    "problem_id": pid,
                    "condition": condition,
                    "gold_answer": gold,
                    "final_answer": fa,
                    "initial_answer": fa,  # not separately stored in method_out.json
                    "flagged_error": payload.get("flagged_error", False),
                    "is_correct": payload.get("is_correct", False),
                    "raw_response": payload.get("raw_response", ""),
                    "response_chars": len(payload.get("raw_response", "") or ""),
                    "checksum_claims": [],
                }
            )
    return records


# --------------------------------------------------------------------------- #
# Response parsing utilities (mirrors method.py's regexes, applied here so we
# independently re-derive initial_answer / final_answer / flagged_error from
# raw_response rather than trusting the experiment's own parse blindly)
# --------------------------------------------------------------------------- #

ANSWER_RE = re.compile(r"answer\s*[:=][^\d-]{0,15}(-?[\d,]+(?:\.\d+)?)", re.IGNORECASE)
FLAG_WORDS = re.compile(
    r"\b(error|mistake|incorrect|wrong|revis|correct(ed)?\s+(answer|value)|mismatch)\b",
    re.IGNORECASE,
)
CHECKSUM_TOKEN_RE = re.compile(r"CHECKSUM_(OK|MISMATCH)", re.IGNORECASE)


def extract_all_answers(text: str) -> list[float]:
    return [float(m.group(1).replace(",", "")) for m in ANSWER_RE.finditer(text or "")]


def independent_reparse(records: list[dict]) -> list[dict]:
    """Recompute initial_answer/final_answer/is_correct/flagged_error/
    checksum_claims straight from raw_response for every record that has one,
    as an independent audit of the experiment's own parser (Metric-adjacent
    integrity check, not in the plan's numbered list but cheap and load-bearing)."""
    n_mismatch_final = 0
    n_checked = 0
    for r in records:
        text = r.get("raw_response", "")
        if not text:
            continue
        answers = extract_all_answers(text)
        final = answers[-1] if answers else None
        initial = answers[0] if answers else None
        is_correct = final is not None and abs(final - r["gold_answer"]) < 1e-6
        flagged = bool(FLAG_WORDS.search(text))
        claims = (
            [m.group(1).upper() for m in CHECKSUM_TOKEN_RE.finditer(text)]
            if r["condition"] == "checksum_critique"
            else []
        )
        n_checked += 1
        if r.get("final_answer") is not None and final is not None and abs((r["final_answer"] or 0) - final) > 1e-6:
            n_mismatch_final += 1
        r["initial_answer"] = initial
        r["final_answer"] = final
        r["is_correct"] = is_correct
        r["flagged_error"] = flagged
        r["checksum_claims"] = claims
    if n_checked:
        logger.info(
            f"Independent re-parse of {n_checked} raw responses: "
            f"{n_mismatch_final} final-answer disagreements with the experiment's own parse "
            f"({n_mismatch_final / n_checked:.1%})"
        )
    return records


# --------------------------------------------------------------------------- #
# Statistics
# --------------------------------------------------------------------------- #


def wilson_ci(k: int, n: int, z: float = 1.959963984540054) -> tuple[float, float]:
    if n == 0:
        return (0.0, 0.0)
    phat = k / n
    denom = 1 + z**2 / n
    center = phat + z**2 / (2 * n)
    margin = z * np.sqrt(phat * (1 - phat) / n + z**2 / (4 * n**2))
    return (float((center - margin) / denom), float((center + margin) / denom))


def bootstrap_ci_diff(a_correct: list[int], b_correct: list[int], n_boot: int = 10000, seed: int = 1) -> dict:
    rng = np.random.default_rng(seed)
    a = np.array(a_correct, dtype=float)
    b = np.array(b_correct, dtype=float)
    n = len(a)
    if n == 0:
        return {"diff": 0.0, "ci_low": 0.0, "ci_high": 0.0, "n": 0, "excludes_zero": False}
    idx_boot = rng.integers(0, n, size=(n_boot, n))
    diffs = b[idx_boot].mean(axis=1) - a[idx_boot].mean(axis=1)
    ci_low, ci_high = float(np.percentile(diffs, 2.5)), float(np.percentile(diffs, 97.5))
    return {
        "diff": float(b.mean() - a.mean()),
        "ci_low": ci_low,
        "ci_high": ci_high,
        "n": n,
        "excludes_zero": bool(ci_low > 0 or ci_high < 0),
    }


def mcnemar_test(a_correct: list[int], b_correct: list[int]) -> dict:
    n01 = sum(1 for x, y in zip(a_correct, b_correct) if x == 0 and y == 1)
    n10 = sum(1 for x, y in zip(a_correct, b_correct) if x == 1 and y == 0)
    n_disc = n01 + n10
    if n_disc == 0:
        return {"n01": n01, "n10": n10, "n_discordant": 0, "p_value": 1.0, "method": "exact_binomial_mcnemar"}
    p = binomtest(min(n01, n10), n_disc, 0.5).pvalue
    return {"n01": n01, "n10": n10, "n_discordant": n_disc, "p_value": float(p), "method": "exact_binomial_mcnemar"}


def holm_bonferroni(pvals_named: list[tuple[str, float]]) -> dict:
    """Standard Holm step-down procedure. Returns {name: {p, p_adj, reject_at_0.05}}."""
    m = len(pvals_named)
    order = sorted(range(m), key=lambda i: pvals_named[i][1])
    adjusted = [0.0] * m
    running_max = 0.0
    for rank, idx in enumerate(order):
        name, p = pvals_named[idx]
        adj = min(1.0, (m - rank) * p)
        running_max = max(running_max, adj)
        adjusted[idx] = running_max
    return {
        pvals_named[i][0]: {
            "p_raw": pvals_named[i][1],
            "p_holm_adjusted": adjusted[i],
            "reject_at_0.05": adjusted[i] < 0.05,
        }
        for i in range(m)
    }


def logistic_regression_2class(X: np.ndarray, y: np.ndarray, n_iter: int = 500, lr: float = 0.1) -> dict:
    """Small dependency-free IRLS-free gradient-descent logistic regression
    (avoids adding sklearn as a dependency for a single confound-check fit).
    X is standardized outside this function; a bias column is added here."""
    n, p = X.shape
    Xb = np.hstack([np.ones((n, 1)), X])
    beta = np.zeros(p + 1)
    for _ in range(n_iter):
        z = Xb @ beta
        pred = 1.0 / (1.0 + np.exp(-np.clip(z, -30, 30)))
        grad = Xb.T @ (pred - y) / n
        beta -= lr * grad
    z = Xb @ beta
    pred = 1.0 / (1.0 + np.exp(-np.clip(z, -30, 30)))
    # Wald SEs from the observed information matrix (standard logistic-regression asymptotics)
    W = np.diag(pred * (1 - pred))
    try:
        cov = np.linalg.inv(Xb.T @ W @ Xb + 1e-8 * np.eye(p + 1))
        se = np.sqrt(np.clip(np.diag(cov), 0, None))
    except np.linalg.LinAlgError:
        se = np.full(p + 1, np.nan)
    z_scores = beta / np.where(se == 0, np.nan, se)
    from scipy.stats import norm

    p_values = 2 * (1 - norm.cdf(np.abs(z_scores)))
    return {"coef": beta.tolist(), "se": se.tolist(), "z": z_scores.tolist(), "p_value": p_values.tolist()}


# --------------------------------------------------------------------------- #
# Metric 7: checksum self-computation audit via LLM judge
# --------------------------------------------------------------------------- #

PRICING_USD_PER_TOKEN = {
    "anthropic/claude-haiku-4.5": {"input": 1.0e-6, "output": 5.0e-6},
    "openai/gpt-4o-mini": {"input": 0.15e-6, "output": 0.6e-6},
}
JUDGE_MODEL = "anthropic/claude-haiku-4.5"
JUDGE_RUBRIC = (
    "You are auditing a math self-critique transcript. The transcript should contain, "
    "for one or more arithmetic sub-steps, an explicit 'digit root' (repeated digit sum, "
    "a.k.a. casting-out-nines mod-9 checksum) computation for two operands and a result, "
    "followed by a CHECKSUM_OK or CHECKSUM_MISMATCH verdict.\n\n"
    "Your job: independently RECOMPUTE the digit root of every operand and result named in "
    "each checksum check shown (digit root = repeatedly sum the number's digits until one "
    "digit remains, e.g. digit_root(295)=2+9+5=16->1+6=7), and RECOMPUTE the mod-9 relationship "
    "(operand digit roots combined by the step's +/-/* operator, taken mod 9) the transcript "
    "claims to verify. Work through each check step by step, showing your own recomputation, "
    "before giving a verdict — do not just trust the transcript's stated numbers.\n\n"
    "After showing your work for every checksum check in the transcript, end your reply with a "
    "final line containing EXACTLY one of: 'VERDICT: CORRECT' if every digit-root computation and "
    "CHECKSUM_OK/CHECKSUM_MISMATCH verdict shown is arithmetically correct by your own recomputation, "
    "'VERDICT: INCORRECT' if at least one digit-root computation or verdict shown is wrong, or "
    "'VERDICT: NO_CHECKSUM_SHOWN' if the transcript contains no digit-root/checksum work to audit."
)


def audit_checksum_computation(records: list[dict], per_model_sample: int = 50, seed: int = 3) -> dict:
    rng = random.Random(seed)
    by_model: dict[str, list[dict]] = {}
    for r in records:
        if r["condition"] == "checksum_critique" and r.get("raw_response"):
            by_model.setdefault(r["model"], []).append(r)

    tasks = []
    for model, recs in by_model.items():
        sample = recs if len(recs) <= per_model_sample else rng.sample(recs, per_model_sample)
        for r in sample:
            tasks.append(r)
    logger.info(f"Checksum-computation audit: {len(tasks)} traces across {len(by_model)} models")

    if not tasks:
        return {"n_audited": 0, "per_model": {}, "overall_error_rate": None, "audited_records": []}

    orcall.init_openrouter_call()
    results = []

    def judge_one(rec: dict) -> dict:
        prompt = JUDGE_RUBRIC + "\n\nTRANSCRIPT:\n" + rec["raw_response"][:6000]
        for attempt in range(3):
            try:
                out = orcall.core_openrouter_call(
                    model=JUDGE_MODEL, input_text=prompt, max_tokens=800, temperature=0.0
                )
                if out.get("success"):
                    verdict_text = (out.get("response") or out.get("text") or "").strip().upper()
                    # take the LAST VERDICT: line so the judge's own step-by-step
                    # recomputation (which may mention CORRECT/INCORRECT mid-reasoning
                    # before self-correcting) doesn't get matched instead of its conclusion
                    verdict_lines = [ln for ln in verdict_text.splitlines() if "VERDICT" in ln]
                    tail = verdict_lines[-1] if verdict_lines else verdict_text
                    if "NO_CHECKSUM" in tail:
                        verdict = "NO_CHECKSUM_SHOWN"
                    elif "INCORRECT" in tail:
                        verdict = "INCORRECT"
                    elif "CORRECT" in tail:
                        verdict = "CORRECT"
                    else:
                        verdict = "UNPARSEABLE"
                    price = PRICING_USD_PER_TOKEN.get(JUDGE_MODEL, {"input": 1e-6, "output": 5e-6})
                    return {
                        "model": rec["model"],
                        "problem_id": rec["problem_id"],
                        "verdict": verdict,
                        "cost_usd": (out.get("input_tokens", 0) or 0) * price["input"]
                        + (out.get("output_tokens", 0) or 0) * price["output"],
                    }
                time.sleep(1.0 * (attempt + 1))
            except Exception as e:  # noqa: BLE001
                logger.error(f"Judge call failed (attempt {attempt+1}/3): {e}")
                time.sleep(1.0 * (attempt + 1))
        return {"model": rec["model"], "problem_id": rec["problem_id"], "verdict": "CALL_FAILED", "cost_usd": 0.0}

    total_cost = 0.0
    with ThreadPoolExecutor(max_workers=8) as pool:
        futures = {pool.submit(judge_one, r): r for r in tasks}
        for fut in as_completed(futures):
            res = fut.result()
            results.append(res)
            total_cost += res["cost_usd"]
            if total_cost >= 1.5:
                logger.warning("Checksum-audit sub-budget ($1.50) reached; stopping remaining judge calls")
                for f in futures:
                    f.cancel()
                break
    logger.info(f"Checksum-computation audit LLM cost: ${total_cost:.4f} over {len(results)} calls")

    per_model = {}
    for model, recs in by_model.items():
        model_results = [r for r in results if r["model"] == model]
        n = len(model_results)
        n_incorrect = sum(1 for r in model_results if r["verdict"] == "INCORRECT")
        n_scored = sum(1 for r in model_results if r["verdict"] in ("CORRECT", "INCORRECT"))
        per_model[model] = {
            "n_audited": n,
            "n_incorrect": n_incorrect,
            "n_scored_correct_or_incorrect": n_scored,
            "checksum_computation_error_rate": (n_incorrect / n_scored) if n_scored else None,
        }
    n_scored_all = sum(1 for r in results if r["verdict"] in ("CORRECT", "INCORRECT"))
    n_incorrect_all = sum(1 for r in results if r["verdict"] == "INCORRECT")
    return {
        "n_audited": len(results),
        "per_model": per_model,
        "overall_error_rate": (n_incorrect_all / n_scored_all) if n_scored_all else None,
        "total_cost_usd": total_cost,
        "audited_records": results,
    }


# --------------------------------------------------------------------------- #
# Core metric computation
# --------------------------------------------------------------------------- #

CONDITIONS = ["baseline", "freeform_critique", "placebo_critique", "checksum_critique"]
CONDITION_PAIRS_FOR_TEST = [
    ("checksum_critique", "freeform_critique"),
    ("checksum_critique", "placebo_critique"),
]


def compute_all_metrics(
    records: list[dict],
    detectable_by_pid: dict[str, bool],
    audit: dict,
) -> dict:
    models = sorted({r["model"] for r in records})
    by_mck = {}  # (model, condition) -> list of records
    for r in records:
        by_mck.setdefault((r["model"], r["condition"]), []).append(r)

    def subset_flag(recs: list[dict], value: bool | None) -> list[dict]:
        if value is None:
            return recs
        return [r for r in recs if detectable_by_pid.get(r["problem_id"]) is value]

    # -------- Metric 1: final-answer accuracy (overall + detectable split) + Wilson CI --------
    accuracy_table = {}
    for model in models:
        accuracy_table[model] = {}
        for cond in CONDITIONS + ["oracle_detection_isolation"]:
            recs = by_mck.get((model, cond), [])
            for split_name, split_val in [("overall", None), ("checksum_detectable", True), ("checksum_invisible", False)]:
                sub = subset_flag(recs, split_val)
                n = len(sub)
                k = sum(r["is_correct"] for r in sub)
                acc = k / n if n else None
                lo, hi = wilson_ci(k, n) if n else (None, None)
                accuracy_table[model].setdefault(cond, {})[split_name] = {
                    "n": n, "accuracy": acc, "wilson_ci_low": lo, "wilson_ci_high": hi,
                }

    # -------- Metric 2: detection precision/recall/F1 (confusion: flagged vs
    # actually-initially-wrong), restricted primarily to detectable subset --------
    detection_table = {}
    for model in models:
        detection_table[model] = {}
        for cond in CONDITIONS:
            recs = by_mck.get((model, cond), [])
            for split_name, split_val in [("checksum_detectable_subset", True), ("checksum_invisible_subset", False), ("overall", None)]:
                sub = subset_flag(recs, split_val)
                sub = [r for r in sub if r.get("initial_answer") is not None]
                tp = sum(1 for r in sub if r["flagged_error"] and abs(r["initial_answer"] - r["gold_answer"]) > 1e-6)
                fp = sum(1 for r in sub if r["flagged_error"] and abs(r["initial_answer"] - r["gold_answer"]) <= 1e-6)
                fn = sum(1 for r in sub if not r["flagged_error"] and abs(r["initial_answer"] - r["gold_answer"]) > 1e-6)
                tn = sum(1 for r in sub if not r["flagged_error"] and abs(r["initial_answer"] - r["gold_answer"]) <= 1e-6)
                precision = tp / (tp + fp) if (tp + fp) else None
                recall = tp / (tp + fn) if (tp + fn) else None
                f1 = (2 * precision * recall / (precision + recall)) if precision and recall and (precision + recall) > 0 else None
                detection_table[model].setdefault(cond, {})[split_name] = {
                    "n": len(sub), "tp": tp, "fp": fp, "fn": fn, "tn": tn,
                    "precision": precision, "recall": recall, "f1": f1,
                }

    # -------- Metric 3: correction accuracy given flag --------
    correction_table = {}
    for model in models:
        correction_table[model] = {}
        for cond in CONDITIONS:
            recs = by_mck.get((model, cond), [])
            flagged = [r for r in recs if r["flagged_error"]]
            n = len(flagged)
            k = sum(r["is_correct"] for r in flagged)
            correction_table[model][cond] = {
                "n_flagged": n,
                "correction_accuracy_given_flag": (k / n) if n else None,
                "wilson_ci_low": wilson_ci(k, n)[0] if n else None,
                "wilson_ci_high": wilson_ci(k, n)[1] if n else None,
            }

    # -------- Metric 4: detection-only vs correction-only ablation --------
    ablation_table = {}
    for model in models:
        oracle_recs = by_mck.get((model, "oracle_detection_isolation"), [])
        n_o = len(oracle_recs)
        k_o = sum(r["is_correct"] for r in oracle_recs)
        checksum_corr = correction_table.get(model, {}).get("checksum_critique", {})
        ablation_table[model] = {
            "oracle_given_mismatch_signal_fix_rate": {
                "n": n_o, "fix_rate": (k_o / n_o) if n_o else None,
                "wilson_ci_low": wilson_ci(k_o, n_o)[0] if n_o else None,
                "wilson_ci_high": wilson_ci(k_o, n_o)[1] if n_o else None,
            },
            "checksum_condition_correction_accuracy_given_flag": checksum_corr,
            "interpretation": (
                "gap = oracle fix_rate - checksum correction_accuracy_given_flag; "
                "large positive gap => model CAN use an externally-given mismatch signal "
                "much better than it can compute+use its own checksum (bottleneck is "
                "self-computation, not correction ability)"
            ),
        }
        if ablation_table[model]["oracle_given_mismatch_signal_fix_rate"]["fix_rate"] is not None and checksum_corr.get("correction_accuracy_given_flag") is not None:
            ablation_table[model]["fix_rate_gap"] = (
                ablation_table[model]["oracle_given_mismatch_signal_fix_rate"]["fix_rate"]
                - checksum_corr["correction_accuracy_given_flag"]
            )

    # -------- Metric 5: paired significance tests, checksum-detectable subset, per model --------
    significance_table = {}
    all_pvals_for_holm: list[tuple[str, float]] = []
    for model in models:
        model_tests = {}
        by_cond_pid = {
            cond: {r["problem_id"]: int(r["is_correct"]) for r in by_mck.get((model, cond), [])}
            for cond in CONDITIONS
        }
        common_pids_full = sorted(set.intersection(*[set(d) for d in by_cond_pid.values()])) if all(by_cond_pid.values()) else []
        detectable_pids = [p for p in common_pids_full if detectable_by_pid.get(p) is True]

        for a, b in CONDITION_PAIRS_FOR_TEST:
            key = f"{b}_vs_{a}"
            a_full = [by_cond_pid[a][p] for p in common_pids_full]
            b_full = [by_cond_pid[b][p] for p in common_pids_full]
            a_det = [by_cond_pid[a][p] for p in detectable_pids]
            b_det = [by_cond_pid[b][p] for p in detectable_pids]

            mcnemar_full = mcnemar_test(a_full, b_full) if common_pids_full else None
            mcnemar_det = mcnemar_test(a_det, b_det) if detectable_pids else None
            use_bootstrap_det = (mcnemar_det is None) or (mcnemar_det["n_discordant"] < 25)

            entry = {
                "n_common_problems_full": len(common_pids_full),
                "n_detectable_subset": len(detectable_pids),
                "mcnemar_full_set": mcnemar_full,
                "mcnemar_detectable_subset": mcnemar_det,
                "bootstrap_detectable_subset": bootstrap_ci_diff(a_det, b_det) if detectable_pids else None,
                "used_bootstrap_for_detectable_subset_due_to_low_discordant_count": use_bootstrap_det,
                "effect_size_pp_detectable_subset": (
                    100.0 * (np.mean(b_det) - np.mean(a_det)) if detectable_pids else None
                ),
            }
            model_tests[key] = entry
            # primary p-value for the family: exact McNemar on detectable subset if enough
            # discordant pairs, else the bootstrap-CI-excludes-zero result recast as p<0.05/p>=0.05
            if mcnemar_det is not None and not use_bootstrap_det:
                p_for_holm = mcnemar_det["p_value"]
            elif entry["bootstrap_detectable_subset"] is not None:
                p_for_holm = 0.01 if entry["bootstrap_detectable_subset"]["excludes_zero"] else 0.5
            else:
                p_for_holm = 1.0
            all_pvals_for_holm.append((f"{model}::{key}", p_for_holm))
        significance_table[model] = model_tests

    holm_results = holm_bonferroni(all_pvals_for_holm)
    for name, res in holm_results.items():
        model, key = name.split("::")
        significance_table[model][key]["holm_bonferroni"] = res

    # -------- Metric 6: prompt-length confound --------
    length_confound = {}
    for model in models:
        base_by_pid = {r["problem_id"]: r["is_correct"] for r in by_mck.get((model, "baseline"), [])}
        rows_X, rows_y, rows_cond = [], [], []
        for cond in ["freeform_critique", "placebo_critique", "checksum_critique"]:
            for r in by_mck.get((model, cond), []):
                if r["problem_id"] not in base_by_pid:
                    continue
                rows_X.append(r.get("response_chars", 0))
                rows_y.append(int(r["is_correct"]))
                rows_cond.append(cond)
        length_stats = {}
        for cond in CONDITIONS:
            lens = [r.get("response_chars", 0) for r in by_mck.get((model, cond), [])]
            length_stats[cond] = {
                "mean_chars": float(np.mean(lens)) if lens else None,
                "median_chars": float(np.median(lens)) if lens else None,
                "n": len(lens),
            }
        placebo_mean = length_stats.get("placebo_critique", {}).get("mean_chars")
        checksum_mean = length_stats.get("checksum_critique", {}).get("mean_chars")
        length_match_ratio = (placebo_mean / checksum_mean) if placebo_mean and checksum_mean else None

        reg_result = None
        if len(rows_y) >= 10 and len(set(rows_cond)) > 1:
            uniq_conds = sorted(set(rows_cond))
            dummy_cols = uniq_conds[1:]  # drop first as reference
            X = np.zeros((len(rows_y), len(dummy_cols) + 1))
            for i, c in enumerate(rows_cond):
                X[i, 0] = (np.array(rows_X[i]) - np.mean(rows_X)) / (np.std(rows_X) + 1e-9)
                for j, dc in enumerate(dummy_cols):
                    if c == dc:
                        X[i, j + 1] = 1.0
            y = np.array(rows_y, dtype=float)
            try:
                fit = logistic_regression_2class(X, y)
                reg_result = {
                    "reference_condition": uniq_conds[0],
                    "feature_order": ["critique_token_count_zscore"] + [f"is_{c}" for c in dummy_cols],
                    **fit,
                }
            except Exception as e:  # noqa: BLE001
                logger.error(f"Length-confound regression failed for {model}: {e}")
        length_confound[model] = {
            "length_stats_by_condition": length_stats,
            "placebo_to_checksum_length_ratio": length_match_ratio,
            "regression_correctness_on_condition_plus_token_count": reg_result,
        }

    # -------- Metric 7: checksum self-computation audit (already computed) --------
    audit_adjusted_detection = {}
    audited_pids_by_model = {}
    for r in audit.get("audited_records", []):
        if r["verdict"] == "INCORRECT":
            audited_pids_by_model.setdefault(r["model"], set()).add(r["problem_id"])
    for model in models:
        bad_pids = audited_pids_by_model.get(model, set())
        recs = [
            r for r in by_mck.get((model, "checksum_critique"), [])
            if r["problem_id"] not in bad_pids and r.get("initial_answer") is not None
        ]
        det_sub = subset_flag(recs, True)
        tp = sum(1 for r in det_sub if r["flagged_error"] and abs(r["initial_answer"] - r["gold_answer"]) > 1e-6)
        fp = sum(1 for r in det_sub if r["flagged_error"] and abs(r["initial_answer"] - r["gold_answer"]) <= 1e-6)
        fn = sum(1 for r in det_sub if not r["flagged_error"] and abs(r["initial_answer"] - r["gold_answer"]) > 1e-6)
        precision = tp / (tp + fp) if (tp + fp) else None
        recall = tp / (tp + fn) if (tp + fn) else None
        audit_adjusted_detection[model] = {
            "n_excluded_miscomputed_traces": len(bad_pids),
            "n_remaining_detectable_subset": len(det_sub),
            "precision_after_excluding_miscomputed": precision,
            "recall_after_excluding_miscomputed": recall,
        }

    return {
        "metric1_final_answer_accuracy": accuracy_table,
        "metric2_detection_precision_recall_f1": detection_table,
        "metric3_correction_accuracy_given_flag": correction_table,
        "metric4_detection_vs_correction_ablation": ablation_table,
        "metric5_significance_tests": significance_table,
        "metric6_length_confound": length_confound,
        "metric7_checksum_computation_audit": {k: v for k, v in audit.items() if k != "audited_records"},
        "metric7_detection_after_audit_exclusion": audit_adjusted_detection,
        "metric8_checksum_invisible_negative_control": {
            model: {
                cond: accuracy_table[model].get(cond, {}).get("checksum_invisible", {})
                for cond in CONDITIONS
            }
            for model in models
        },
    }


# --------------------------------------------------------------------------- #
# metrics_agg flattening (schema requires flat number-valued dict)
# --------------------------------------------------------------------------- #


def _safe_key(*parts: str) -> str:
    key = "_".join(parts)
    key = re.sub(r"[^a-zA-Z0-9_]", "_", key)
    key = re.sub(r"_+", "_", key).strip("_")
    if not re.match(r"^[a-zA-Z_]", key):
        key = "m_" + key
    return key


def build_metrics_agg(metrics: dict) -> dict:
    agg: dict[str, float] = {}

    for model, conds in metrics["metric1_final_answer_accuracy"].items():
        model_short = model.split("/")[-1]
        for cond, splits in conds.items():
            for split_name, d in splits.items():
                if d["accuracy"] is not None:
                    agg[_safe_key("acc", model_short, cond, split_name)] = float(d["accuracy"])

    for model, conds in metrics["metric2_detection_precision_recall_f1"].items():
        model_short = model.split("/")[-1]
        for cond, splits in conds.items():
            d = splits.get("checksum_detectable_subset", {})
            if d.get("precision") is not None:
                agg[_safe_key("precision", model_short, cond)] = float(d["precision"])
            if d.get("recall") is not None:
                agg[_safe_key("recall", model_short, cond)] = float(d["recall"])
            if d.get("f1") is not None:
                agg[_safe_key("f1", model_short, cond)] = float(d["f1"])

    for model, conds in metrics["metric3_correction_accuracy_given_flag"].items():
        model_short = model.split("/")[-1]
        for cond, d in conds.items():
            if d["correction_accuracy_given_flag"] is not None:
                agg[_safe_key("correction_acc", model_short, cond)] = float(d["correction_accuracy_given_flag"])

    for model, d in metrics["metric4_detection_vs_correction_ablation"].items():
        model_short = model.split("/")[-1]
        fr = d["oracle_given_mismatch_signal_fix_rate"]["fix_rate"]
        if fr is not None:
            agg[_safe_key("oracle_fix_rate", model_short)] = float(fr)
        if "fix_rate_gap" in d:
            agg[_safe_key("fix_rate_gap", model_short)] = float(d["fix_rate_gap"])

    for model, tests in metrics["metric5_significance_tests"].items():
        model_short = model.split("/")[-1]
        for pair_key, d in tests.items():
            hb = d.get("holm_bonferroni")
            if hb is not None:
                agg[_safe_key("holm_p", model_short, pair_key)] = float(hb["p_holm_adjusted"])
            if d.get("effect_size_pp_detectable_subset") is not None:
                agg[_safe_key("effect_pp", model_short, pair_key)] = float(d["effect_size_pp_detectable_subset"])

    for model, d in metrics["metric6_length_confound"].items():
        model_short = model.split("/")[-1]
        ratio = d.get("placebo_to_checksum_length_ratio")
        if ratio is not None:
            agg[_safe_key("placebo_checksum_length_ratio", model_short)] = float(ratio)

    audit = metrics["metric7_checksum_computation_audit"]
    if audit.get("overall_error_rate") is not None:
        agg["checksum_computation_error_rate_overall"] = float(audit["overall_error_rate"])
    agg["checksum_audit_n_traces"] = float(audit.get("n_audited", 0))

    for model, d in metrics["metric8_checksum_invisible_negative_control"].items():
        model_short = model.split("/")[-1]
        for cond, split_d in d.items():
            acc = split_d.get("accuracy") if isinstance(split_d, dict) else None
            if acc is not None:
                agg[_safe_key("invisible_ctrl_acc", model_short, cond)] = float(acc)

    return agg


# --------------------------------------------------------------------------- #
# Per-example output assembly (exp_eval_sol_out.json schema)
# --------------------------------------------------------------------------- #


def build_examples(records: list[dict], detectable_by_pid: dict[str, bool]) -> list[dict]:
    by_pid: dict[str, dict] = {}
    for r in records:
        by_pid.setdefault(r["problem_id"], {"gold": r["gold_answer"], "recs": []})["recs"].append(r)

    examples = []
    for pid in sorted(by_pid):
        entry = by_pid[pid]
        example: dict = {
            "input": f"problem_id={pid}",
            "output": str(entry["gold"]),
            "metadata_checksum_detectable": bool(detectable_by_pid.get(pid, False)),
        }
        for r in entry["recs"]:
            model_short = r["model"].split("/")[-1]
            tag = _safe_key(model_short, r["condition"])
            example[f"predict_{tag}"] = json.dumps(
                {
                    "final_answer": r.get("final_answer"),
                    "is_correct": r.get("is_correct"),
                    "flagged_error": r.get("flagged_error"),
                }
            )
            example[f"eval_{tag}_correct"] = float(bool(r.get("is_correct")))
        examples.append(example)
    return examples


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n-examples", type=int, default=None, help="cap number of problems (by pid) for a quick test run")
    parser.add_argument("--skip-audit", action="store_true", help="skip the LLM-judge checksum-computation audit (Metric 7)")
    parser.add_argument("--audit-sample-size", type=int, default=50)
    args = parser.parse_args()

    logger.info("STEP 1: loading experiment predictions")
    records, exp_meta = load_experiment_records(n_examples=args.n_examples)
    if not records:
        raise RuntimeError("No usable experiment records found")

    logger.info("STEP 2: reproducing problem generation + checksum-detectability ground truth")
    n_problems_in_run = len({r["problem_id"] for r in records if r["problem_id"].startswith("synth_")})
    # reproduce the LARGEST plausible problem set the experiment could have used, then
    # filter down; n_problems used by method.py is a CLI arg (default 120, full run used 200)
    n_reproduce = max(n_problems_in_run, exp_meta.get("sample_sizes", {}).get("n_problems", 0), 200)
    problems = build_problem_set(n_reproduce, seed=42)
    if exp_meta:
        verify_reproduction(problems, exp_meta)
    detectable_by_pid = characterize_errors(problems)
    n_det = sum(detectable_by_pid.values())
    logger.info(f"Recovered ground truth: {n_det}/{len(detectable_by_pid)} problems have a checksum-detectable injected-error variant")

    logger.info("STEP 3: independent re-parse of raw_response as a parser-integrity check")
    records = independent_reparse(records)

    logger.info("STEP 4: checksum self-computation audit (Metric 7, LLM-judge via OpenRouter)")
    if args.skip_audit:
        audit = {"n_audited": 0, "per_model": {}, "overall_error_rate": None, "audited_records": [], "skipped": True}
    else:
        audit = audit_checksum_computation(records, per_model_sample=args.audit_sample_size)

    logger.info("STEP 5: computing all metrics")
    metrics = compute_all_metrics(records, detectable_by_pid, audit)

    logger.info("STEP 6: assembling output")
    metrics_agg = build_metrics_agg(metrics)
    examples = build_examples(records, detectable_by_pid)

    models = sorted({r["model"] for r in records})
    output = {
        "metadata": {
            "evaluation_name": "checksum_vs_freeform_self_critique_evaluation",
            "hypothesis": "Does an explicit checksum self-critique beat free-form self-critique and a matched-length placebo on multi-step arithmetic word problems?",
            "experiment_metadata_snapshot": {
                k: v for k, v in exp_meta.items()
                if k not in ("per_condition_metrics", "statistical_tests", "length_accuracy_confound_check")
            },
            "n_records_evaluated": len(records),
            "n_problems": len(detectable_by_pid),
            "n_checksum_detectable_problems": n_det,
            "n_checksum_invisible_problems": len(detectable_by_pid) - n_det,
            "models_evaluated": models,
            "detailed_metrics": metrics,
        },
        "metrics_agg": metrics_agg,
        "datasets": [
            {"dataset": "synthetic_multistep_arithmetic_word_problems", "examples": examples}
        ],
    }

    out_path = WORKSPACE / "eval_out.json"
    out_path.write_text(json.dumps(output, indent=2, default=str))
    logger.info(f"Wrote {out_path} ({out_path.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
