#!/usr/bin/env python3
"""Independent exhaustive verification of full_data_out.json.

Re-derives, from scratch (no reuse of data.py's internal helpers), whether
every row is internally consistent: base-item traces compute to their stated
output, error-variant corrupted traces are consistent with their rendered
input text, and mod9 checksum labels are correct.
"""

import json
import re
import sys
from pathlib import Path

from loguru import logger

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")

EPS = 1e-6
STEP_RE = re.compile(r"Step (\d+): (-?[\d.]+) ([+\-*/]) (-?[\d.]+) = (-?[\d.]+)")


def apply_op(a, op, b):
    return {"+": a + b, "-": a - b, "*": a * b, "/": round(a / b, 6) if b else None}[op]


def mod9_residue(n):
    n = abs(round(n))
    return 0 if n == 0 else (9 if n % 9 == 0 else n % 9)


def verify_base_row(row):
    trace = row["metadata_trace"]
    for i, s in enumerate(trace):
        expect = apply_op(s["operand_1"], s["operation"], s["operand_2"])
        if expect is None or abs(expect - s["result"]) > max(EPS, abs(expect) * 1e-4):
            return f"step {i} arithmetic mismatch: {s['operand_1']}{s['operation']}{s['operand_2']} != {s['result']}"
    if abs(trace[-1]["result"] - float(row["output"])) > max(EPS, abs(trace[-1]["result"]) * 1e-4):
        return f"final trace result {trace[-1]['result']} != declared output {row['output']}"
    return None


def verify_variant_row(row):
    parsed_steps = [(int(i), float(o1), op, float(o2), float(r)) for i, o1, op, o2, r in STEP_RE.findall(row["input"])]
    if not parsed_steps:
        return "could not parse any Step lines from rendered input"

    injected_idx = row["metadata_injected_step_index"]
    for idx, o1, op, o2, r in parsed_steps:
        expect = apply_op(o1, op, o2)
        matches = expect is not None and abs(expect - r) <= max(EPS, abs(expect) * 1e-4)
        if idx == injected_idx:
            if matches:
                return f"injected step {idx} is arithmetically CORRECT ({o1}{op}{o2}={r}) — not actually a corruption"
        else:
            if not matches:
                return f"non-injected step {idx} arithmetic mismatch: {o1}{op}{o2} != {r} (expected {expect}) — corruption should only affect step {injected_idx} and its downstream propagation, not break arithmetic elsewhere"

    rendered_final = parsed_steps[-1][4]
    corrupted_final = row["metadata_corrupted_final_answer"]
    if abs(rendered_final - corrupted_final) > max(EPS, abs(rendered_final) * 1e-4):
        return f"rendered final step result {rendered_final} != metadata_corrupted_final_answer {corrupted_final}"

    label = row["metadata_label"]
    correct_final_str = row["output"].split("correct_final_answer=")[-1]
    correct_final = float(correct_final_str)
    residue_correct = mod9_residue(correct_final)
    residue_corrupted = mod9_residue(corrupted_final)
    preserved = residue_correct == residue_corrupted
    expected_label = "checksum_invisible" if preserved else "checksum_detectable"
    if label != expected_label:
        return f"label {label} != recomputed {expected_label} (residues {residue_correct} vs {residue_corrupted})"
    if row["metadata_mod9_residue_preserved"] != preserved:
        return "metadata_mod9_residue_preserved disagrees with recomputed residue check"
    if abs(corrupted_final - rendered_final) > EPS:
        return "corrupted_final_answer doesn't match trace"
    if abs(corrupted_final - correct_final) < EPS:
        return "corrupted_final_answer equals correct_final_answer (no-op corruption)"
    return None


def main():
    data = json.loads(Path("full_data_out.json").read_text())
    total, failures = 0, []
    by_source: dict[str, list] = {}
    for row in data["datasets"][0]["examples"]:
        by_source.setdefault(row["metadata_item_source"], []).append(row)
    groups = [{"dataset": src, "examples": rows} for src, rows in by_source.items()]
    for group in groups:
        n_base = n_variant = n_base_fail = n_variant_fail = 0
        for row in group["examples"]:
            total += 1
            if row["metadata_row_type"] == "base_item":
                n_base += 1
                err = verify_base_row(row)
                if err:
                    n_base_fail += 1
                    failures.append((group["dataset"], row.get("metadata_item_id"), "base", err))
            else:
                n_variant += 1
                err = verify_variant_row(row)
                if err:
                    n_variant_fail += 1
                    failures.append((group["dataset"], row.get("metadata_base_item_id"), row.get("metadata_error_type"), err))
        logger.info(f"[{group['dataset']}] base: {n_base} checked, {n_base_fail} failed | variants: {n_variant} checked, {n_variant_fail} failed")

    logger.info(f"TOTAL rows checked: {total}, TOTAL failures: {len(failures)}")
    for f in failures[:30]:
        logger.error(f"FAIL: {f}")
    if failures:
        raise SystemExit(f"{len(failures)} verification failures")
    logger.info("ALL ROWS VERIFIED CONSISTENT")


if __name__ == "__main__":
    main()
