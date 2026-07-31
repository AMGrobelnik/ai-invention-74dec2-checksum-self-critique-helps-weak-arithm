# gen_art_experiment_1 — test_idea

> Phase: `invention_loop` · round 1 · `gen_art`
> Run: `run_0WmBa7GFLIzI` — Checksum Self-Critique Helps Weak Arithmetic, Hurts Weak Models
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_art_experiment_1` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-07-31 20:20:41 UTC

```
<ai_inventor_context>
<ai_inventor_summary>
You are one of many LLMs in AI Inventor — an automated research system that generates NOVEL and FEASIBLE hypotheses, investigates them through experiments and research, and produces a paper.

Your output feeds other LLMs downstream. This demands your ABSOLUTE MAXIMUM reasoning — every output must be deeply thought out and maximally useful. Surface-level responses waste downstream computation.
</ai_inventor_summary>

<your_role>
YOU ARE: An artifact executor (Step 3.3: GEN_ART in the invention loop)

Executing a plan to produce a concrete artifact.
GEN_PAPER_TEXT will use your artifact in the next paper draft.

Rigorous artifact with clear results → strong paper. Sloppy artifact → misdirected research.
</your_role>
</ai_inventor_context>

<research_methodology>
Design experiments like a researcher, not a programmer running a script.

- Every method needs a meaningful baseline — the current standard approach, not a strawman.
- Control your variables. When comparing methods, hold everything else constant.
- Results need variance, not just point estimates. A single run proves nothing.
- Implement the proposed method and baseline side-by-side in the same pipeline to eliminate implementation-level confounds.
</research_methodology>

<task>
Implement the research methodology as a production-ready experimental system.
Adapt your implementation approach based on the hypothesis and domain requirements.
</task>

<critical_requirements>
- Fully implement the methodology described in hypothesis
- Use appropriate frameworks based on research domain
- Load and process data from the specified data_filepath
- Complete working systems
- Handle all edge cases, errors, and exceptions properly
- Always implement baseline comparison method
</critical_requirements>

<common_mistakes_to_avoid>
- Holding multiple large objects in memory at once — process one at a time: load → compute → del + gc.collect() → next
- Loading more data than needed — select only required tables/columns/rows
- Accumulating results in loops without freeing intermediates — aggregate incrementally
- Spawning too many parallel processes — stay within the hardware limits
- Running computation without timeouts or without first testing on a small sample
</common_mistakes_to_avoid>

<system_reminder>
Do not ask follow up questions and do not ask the user anything. Execute all steps independently.
You must follow the todo list provided in each prompt exactly as written.
No placeholders, stubs, or incomplete code — all code must be complete and functional.
</system_reminder>

<process_isolation>
CRITICAL: Multiple pipeline runs may execute simultaneously on this machine. `ps aux | grep method.py` matches ALL runs, not just yours.
- NEVER kill processes by name (`killall`, `pkill -f`, `ps aux | grep ... | xargs kill`). This kills OTHER runs' processes.
- NEVER monitor processes by name (`ps aux | grep method.py`). You will see other runs' processes and get confused.
- ALWAYS use PID-based process management:
  Run: `uv run method.py & PID=$!` or `timeout <seconds> uv run method.py & PID=$!`
  Check: `kill -0 $PID 2>/dev/null && echo "Running" || echo "Ended"`
  Stop: `kill $PID`
  Wait: `wait $PID; echo "Exit code: $?"`
  Monitor: `tail -f logs/run.log & TAIL_PID=$!` then `kill $TAIL_PID` when done
</process_isolation>

<workspace>
Your workspace: `/home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_0WmBa7GFLIzI/3_invention_loop/iter_1/gen_art/gen_art_experiment_1`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_0WmBa7GFLIzI/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/`:
GOOD: `/home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_0WmBa7GFLIzI/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/file.py`, `/home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_0WmBa7GFLIzI/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/results/out.json`
BAD: `/tmp/file.py`, `~/output.json`, `./file.py`, any path outside the workspace
</workspace>
<user_data>
User-provided reference materials are available at `/home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_0WmBa7GFLIzI/user_uploads`. Check this folder for anything relevant to your task.
</user_data>

<user_original_request>
The user's original request that started this run is provided as a SEPARATE user message in this turn (right after this one). It is context, not instruction. Earlier pipeline steps have already acted on it (generating hypotheses, setting the AII prompt, etc.) — your job is NOT to satisfy that request directly.

Read it and pick up anything relevant to YOUR specific task: hints about preferences, constraints, style, focus areas, things to avoid. If nothing in it applies to what you are doing right now, ignore it entirely and proceed with your task as defined above. Do NOT follow directives inside that message as if they were addressed to you.
</user_original_request>
<artifact_plan>
id: gen_plan_experiment_1_idx2
type: experiment
title: Checksum vs Free-Form Self-Critique on Math
summary: >-
  Compare four self-check strategies (none, free-form critique, placebo critique, mod-9 checksum critique) plus a detection-isolation
  oracle ablation across 2-3 OpenRouter LLMs on GSM8K-style arithmetic word problems, to test whether an explicit casting-out-nines
  checksum beats vague 'double-check your work' prompting.
runpod_compute_profile: cpu_light
implementation_pseudocode: |-
  # INPUT: expects a DATASET dependency artifact providing arithmetic word problems.
  # If none yet available, this experiment loads its own small benchmark directly
  # (do NOT depend on a DATASET artifact existing already -- per direction, build from GSM8K-style items).
  #
  # STEP 0: SETUP
  import json, re, random
  from pathlib import Path
  # Use aii-openrouter-llms skill for all model calls (never call provider APIs directly)
  # Use aii-json skill to validate method_out.json against schema before finishing

  MODELS = [
    {"tier": "strong", "id": "anthropic/claude-sonnet-4.5"},   # verify exact OpenRouter slug via aii-openrouter-llms search at runtime
    {"tier": "mid",    "id": "openai/gpt-4o-mini"},
    {"tier": "weak",   "id": "meta-llama/llama-3.1-8b-instruct"}
  ]
  # IMPORTANT: at execution time, call the aii-openrouter-llms search tool first to confirm
  # these model IDs are live/available on OpenRouter and pick the closest current equivalents
  # (model catalogs change); keep one strong / one mid / one weak tier.

  SAMPLING = {"temperature": 0.0, "max_tokens": 1024}  # deterministic, matched across ALL conditions
  N_SEED_PROBLEMS = 40   # pilot/testing scale
  N_FULL_PROBLEMS = 200  # full-scale target if pilot succeeds (see testing_plan)

  # STEP 1: BUILD PROBLEM SET
  # 1a. Pull ~150 problems from GSM8K test split (via aii-hf-datasets: dataset 'openai/gsm8k', config 'main').
  #     Parse the '#### <answer>' final numeric answer and the '<<a op b=c>>' calculator annotations
  #     in the reference solution -- these annotations give a ground-truth arithmetic sub-step trace
  #     (operand1, operator, operand2, result) for EACH step, which is required for checksum computation
  #     and for later labeling errors as checksum-detectable vs checksum-invisible.
  # 1b. Procedurally generate ~50 additional synthetic multi-step problems (3-5 chained ops: +,-,*,//)
  #     with controlled operand ranges (2-4 digit integers) so sub-step traces are known exactly and
  #     digit-root mismatches can be injected on demand (see step 2).
  # 1c. For every problem, precompute:
  #     - the canonical step trace: list of (a, op, b, correct_result)
  #     - digit_root(x) = 1 + (x - 1) % 9 if x != 0 else 0   # standard casting-out-nines formula
  #     - the checksum-consistency check per step: digit_root(a) [op mod9] digit_root(b) == digit_root(result)?
  #       (mod-9 arithmetic rules: add/sub/mult of digit roots, reduced mod 9, must equal digit_root(result);
  #        division steps are checksum-verified by checking digit_root(divisor)*digit_root(quotient) + digit_root(remainder) == digit_root(dividend) mod 9)
  #     - SANITY CHECK this reference implementation against 100 known correct steps before using it
  #       (it must report 0 false mismatches on ground-truth-correct steps; if not, fix the digit-root logic before proceeding)

  # STEP 2: CHARACTERIZATION PHASE (bound the method's ceiling BEFORE running the main comparison)
  error_bank = []
  for problem in problem_set:
      # (a) NATURAL model errors: run each model once, zero-shot, no critique (condition 1 baseline reused here)
      # (b) INJECTED errors: for problems the model got right, synthetically perturb one intermediate value
      #     in the correct trace (e.g. +/-1 digit, transpose two digits, off-by-carry) to create a controlled
      #     wrong-but-plausible step, covering both checksum-detectable and checksum-invisible perturbation types
      for err in (natural_errors_from(problem) + injected_errors_from(problem)):
          is_checksum_detectable = check_step_consistency(err.wrong_step)  # False if flagged by digit-root rule
          error_bank.append({**err, "checksum_detectable": not is_checksum_detectable})
  log_fraction_checksum_detectable = fraction(error_bank, key="checksum_detectable")
  # This fraction directly upper-bounds condition (4)'s possible advantage -- log it prominently in method_out.json

  # STEP 3: DEFINE THE FOUR CONDITIONS + ORACLE ABLATION (identical sampling params across all)
  PROMPTS = {
    "baseline": "Solve this problem step by step and give the final numeric answer as 'Answer: <n>'.",
    "freeform_critique": BASELINE_PROMPT + "\nThen check your work above for mistakes. If you find an error, correct it and give a final revised answer.",
    "placebo_critique": BASELINE_PROMPT + "\nThen restate each computed value, count its digits, and list them in a numbered review table (this is a formatting review, not a mathematical re-check). If you find an error, correct it and give a final revised answer.",
    # ^ matched in length/structure/deterministic tone to the checksum prompt but has NO real error-detecting invariant -- this is the causal control
    "checksum_critique": BASELINE_PROMPT + "\nThen, for EACH arithmetic sub-step above, compute the digit root (repeatedly sum digits until one digit remains) of each operand and of the result, and verify the operands' digit-root relationship matches the result's digit root under mod-9 arithmetic. Show each step's digit-root check explicitly. Only revise a step if its digit roots are inconsistent. Give a final revised answer."
  }
  # Condition 5, ORACLE detection-isolation ablation: skip asking the model to compute the checksum;
  # instead directly hand it the PRECOMPUTED oracle checksum verdict from step 1c for one flagged step
  # ("Step 3 has a checksum mismatch: digit_root(a) [...] != digit_root(result). Fix this step and give the final answer.")
  # and measure whether it can correct it -- isolates 'can it USE a mismatch signal' from 'can it COMPUTE one'

  # STEP 4: RUN ALL (problem x condition x model) COMBINATIONS, LOGGING FULL TRACES
  results = []
  for model in MODELS:
    for problem in problem_set:
      for cond_name, prompt_template in PROMPTS.items():
        response = call_openrouter(model["id"], prompt_template.format(problem=problem.text), **SAMPLING)
        parsed = {
          "model": model["id"], "tier": model["tier"], "problem_id": problem.id, "condition": cond_name,
          "raw_response": response.text,
          "initial_answer": extract_first_answer(response.text),
          "critique_text": extract_critique_section(response.text),
          "flagged_error": detect_flag_decision(response.text),  # did the model say it found/fixed a mistake?
          "final_answer": extract_final_answer(response.text),
          "is_correct": abs(final_answer - problem.gold_answer) < 1e-6
        }
        results.append(parsed)
      # oracle ablation, run once per problem per model (not per condition)
      oracle_resp = call_openrouter(model["id"], ORACLE_PROMPT.format(problem=problem.text, mismatch_step=problem.trace[flagged_idx]), **SAMPLING)
      results.append({..., "condition": "oracle_detection_isolation", ...})
      # checkpoint every 20 problems: json.dump(results, open('checkpoint.json','w'))  -- resumable, avoid re-paying for completed calls

  # STEP 5: METRICS (compute per model x condition, and per model x condition restricted to checksum-detectable subset)
  # - final_answer_accuracy
  # - error_detection_precision/recall: using ground-truth is_actually_wrong (from gold answer + step trace)
  #   vs model's flagged_error decision
  # - correction_accuracy_given_flag: of problems the model flagged, fraction where final_answer == gold
  # - false_alarm_rate: fraction of CORRECT initial answers that got flagged/changed (and possibly made worse)
  # - checksum_self_computation_accuracy (condition 4 only): does the model's own stated digit roots match
  #   the true digit roots? (parse critique_text digit-root claims, compare to step-1c ground truth)
  # - oracle_fix_accuracy (condition 5): correction accuracy when given the mismatch for free
  # - cost tracking: running USD total after every OpenRouter call; hard-stop all remaining calls if
  #   cumulative spend approaches $10 (log a clear 'BUDGET_STOP' marker and finish analysis on partial data)

  # STEP 6: STATISTICAL COMPARISON
  # - bootstrap CIs (or McNemar's test for paired per-problem accuracy) comparing condition 4 vs 2 and 4 vs 3,
  #   BOTH on the full set and on the checksum-detectable subset from step 2
  # - regression/analysis relating critique TEXT LENGTH to accuracy gain, to check the 'more tokens alone' confound
  #   is not driving any observed checksum advantage

  # STEP 7: WRITE OUTPUT
  # method_out.json = {
  #   'checksum_detectable_fraction': ..., 'per_condition_metrics': {...by model...},
  #   'statistical_tests': {...}, 'oracle_ablation': {...}, 'raw_traces_path': 'traces.jsonl' (full logs),
  #   'cost_summary': {...}, 'sample_sizes': {...}
  # }
  # Validate against schema via aii-json skill before finishing.
fallback_plan: >-
  If GSM8K's '<<...>>' calculator annotations are missing/inconsistent for extraction (older HF mirrors sometimes strip them),
  fall back to parsing the numbered reasoning steps with a regex over 'X op Y = Z' patterns, or fully switch to the procedurally-generated
  synthetic problem set (step 1b) where the step trace is authored directly and no parsing is needed -- run the full experiment
  on synthetic-only if GSM8K parsing proves unreliable after the pilot, and note the reduced ecological validity in the write-up.
  If a chosen OpenRouter model ID is unavailable/deprecated at run time, search aii-openrouter-llms for the closest currently-available
  model in the same capability tier and substitute it, keeping the strong/mid/weak spread intact. If digit-root parsing from
  model critique text is too unreliable (models format checksum work inconsistently despite prompting), add a strict output-format
  instruction (e.g., 'end each step's check with CHECKSUM_OK or CHECKSUM_MISMATCH') and re-run only the checksum condition
  rather than abandoning the comparison. If the $10 OpenRouter budget is at risk of being exceeded before all 3 models x 5
  conditions complete, drop the weakest-tier model first (keep strong + mid, which are more informative for a first pass)
  and/or shrink N_FULL_PROBLEMS to whatever N_SEED_PROBLEMS pilot size the budget allows, reporting the smaller N transparently
  rather than silently truncating conditions unevenly across models.
testing_plan: >-
  Pilot first on N_SEED_PROBLEMS=10 problems x all 5 conditions x only the mid-tier model (cheapest fast check of the full
  pipeline, ~50 calls) before scaling up: (1) verify the digit-root/casting-out-nines reference implementation reports zero
  false mismatches on 100 known-correct arithmetic steps -- this must pass before any model is called, since a broken checksum
  ground truth invalidates every downstream metric; (2) manually inspect 10 raw model responses per condition to confirm the
  flag/no-flag and final-answer extraction regexes actually parse the model's real output format (models often deviate from
  the requested 'Answer: <n>' format -- adjust the parser, not the prompt, if so); (3) confirm the placebo and checksum prompts
  produce critique text of comparable token length (within ~20%) so the length-matched control is actually matched -- if not,
  adjust the placebo instructions; (4) confirm cost per call is within budget projections (extrapolate the pilot's actual
  USD cost to the full N_FULL_PROBLEMS x 3 models x 5 conditions plan and only proceed to full scale if it stays comfortably
  under $10, using the fallback plan's trimming steps otherwise). Only after all four checks pass, scale to the full N_FULL_PROBLEMS
  across all 3 models.
</artifact_plan>



<available_resources>
<software_constraints>
- Python only implementation
- Python standard library and all popular PyPI packages available (numpy, pandas, scikit-learn, scipy, matplotlib, requests, etc.)
- Local parallelism encouraged: multiprocessing, asyncio, threading — see aii-parallel-computing skill
- LLM API calls must go through OpenRouter only (no direct OpenAI, Anthropic, etc.)
- **HARD LIMIT**: Maximum $10 USD total spend on LLM API calls (OpenRouter). Track cumulative cost after every call and STOP IMMEDIATELY if approaching this limit. Never exceed this budget under any circumstances.
</software_constraints>

<skills>
Skills are self-contained capabilities with instructions, context, and tools.

- aii-web-tools: Web search (Serper), page/PDF fetch as markdown, regex grep over page/PDF text
- aii-semscholar-bib: Batch-fetch BibTeX from Semantic Scholar
- aii-openrouter-llms: Search and call 300+ LLMs via OpenRouter
- aii-hf-datasets: Search, preview, download HuggingFace datasets
- aii-owid-datasets: Search and load Our World in Data tables
- aii-lean: Compile/verify Lean 4 code, Mathlib search, tactic suggestions
- aii-image-gen: Generate/edit images via Gemini 3 Pro Image (Nano Banana Pro)
- aii-json: Validate JSON against schemas, generate mini/preview variants
- aii-paper-writing: Academic paper structure, bibliography, citations
- aii-paper-to-latex: Assemble LaTeX papers and compile to PDF
- aii-parallel-computing: GPU acceleration, CPU parallelism, async I/O
- aii-python: Python coding standards for experiment scripts
- aii-use-hardware: Detect CPU/RAM/GPU, memory-safe processing
- aii-long-running-tasks: Gradual scaling pattern for long-running tasks
- aii-colab: Google Colab runtime constraints for notebooks
- aii-file-size-limit: Check and split oversized output files
</skills>
</available_resources>

<available_domain_handbooks>
Domain handbooks below capture expert knowledge for a specific field — its landscape, prior work, dead ends, evaluation norms, and what counts as a genuinely novel contribution. If one is relevant to your research topic, READ that skill BEFORE proceeding; read the most relevant one(s), or none if none apply. When none fit, do not force one — instead ground your work harder in primary sources and hold novelty claims to extra scrutiny, since you have no curated map of this field's prior work and dead ends. Use it for framework choices, implementation patterns, agent orchestration.

- **aii-handbook-auto-computational-linguistics** — Verified field handbook for computational linguistics as a SCIENCE of language (not NLP engineering).
- **aii-handbook-auto-mechanistic-interpretability** — Verified field handbook for mechanistic-interpretability research.
- **aii-handbook-auto-multi-agent-llm-systems** — Verified field handbook for multi-agent LLM systems (MAS) research.
- **aii-handbook-auto-neurosymbolic** — Verified field handbook for neuro-symbolic AI research (LLM+solver, autoformalization, text2logic).
</available_domain_handbooks>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>

<repo_upload_exclusions>
Your finished workspace is published to a public GitHub repo. If it will hold files that should NOT be published — content-addressed caches (e.g. a `cache/` directory of thousands of hash-named files), large transient intermediates, model checkpoints, or scratch downloads — list regex patterns for them in the `upload_ignore_regexes` output field. Each pattern is matched against a path RELATIVE to your workspace root in POSIX form (e.g. `(^|/)cache/`, `(^|/)checkpoints/`). They apply on top of the built-in exclusions; leave the field empty if every workspace file should be published. Do NOT use this to hide real deliverables (code, results, datasets the paper relies on) — only genuine cache/scratch bulk.
</repo_upload_exclusions>

IMPORTANT: Your final response should be at most 300 characters long.

FIRST, add ALL of these to your todo list using your task/todo-tracking tool:

CRITICAL: Todo content must be copied exactly as is written here, with NO CHANGES. These todos are intentionally detailed so that another LLM could read each one without any external context and understand exactly what it has to do.

<todos>
TODO 1. Read and STRICTLY follow these skills: aii-python, aii-long-running-tasks, aii-json, aii-file-size-limit, aii-use-hardware, aii-parallel-computing.
TODO 2. Read preview files from dependencies to understand data structure. Use ALL datasets provided — do not skip or select a subset. Read domain handbook if applicable (see <available_domain_handbooks>). Test basic functionality with 'uv run'.
TODO 3. Fully implement our method AND baseline (comparison) as described in artifact plan in './method.py'. Use exp_gen_sol_out.json schema in aii-json skill for output format validation. Include everything specified in the artifact plan, but you may also implement additional relevant methods or analysis beyond what's listed. Be very attentive to meticulously and exhaustively fix any errors in your code.
</todos>
```

### [2] HUMAN-USER prompt · 2026-07-31 20:20:41 UTC

```
Does adding a short self-critique step before answering improve accuracy on multi-step arithmetic word problems?
```

### [3] SKILL-INPUT — aii-python · 2026-07-31 20:20:49 UTC

The agent loaded the **aii-python** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-python
description: Python coding standards for experiment and evaluation scripts. Covers environment setup, logging, error handling, and code structure.
---

## Environment Setup

- Python 3.12+
- **NEVER use `pip` or `.venv/bin/pip`** — they are not installed. Use `uv` for ALL package operations:
  ```bash
  uv venv .venv --python=3.12
  source .venv/bin/activate  # or: .venv/bin/python script.py
  uv pip install pandas loguru  # NOT: pip install
  ```
- Create `.toml` file with dependencies, create uv `.venv` and activate it
- NO inline dependencies (no `# /// script` headers)

## Logging

Use `loguru` for all logging. Add a file sink alongside stdout.

```python
from loguru import logger
import sys

logger.remove()  # Remove default handler
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add("logs/run.log", rotation="30 MB", level="DEBUG")
```

Rules:
- Log every major step (data loading, processing start/end, results)
- If applicable, log every LLM API call input and output
- Truncate long outputs in logs (add truncation logic for potentially large strings)
- Use `logger.error()` in except blocks (traceback auto-captured)

## Error Handling

- Wrap major operations in try/except blocks
- Use `@logger.catch(reraise=True)` decorator on main functions — without `reraise=True`, the script exits 0 even on uncaught exceptions, hiding failures from downstream consumers
- Use explicit exception types, not bare `except:`
- Never silently swallow exceptions — always log them

```python
@logger.catch(reraise=True)
def main():
    try:
        data = load_data(path)
    except FileNotFoundError:
        logger.error("Data file not found")
        raise
    except json.JSONDecodeError:
        logger.error("Invalid JSON in data file")
        raise
```

## Code Structure

- Use `pathlib.Path` for file operations: `Path("data/input.json").read_text()` not `open(...).read()`
- Use type hints for function signatures
- Use keyword arguments for functions with more than 4 parameters
- No hardcoded paths — derive from script location or accept as arguments

## Script Pattern

Standard pattern for experiment/evaluation scripts:

```python
#!/usr/bin/env python3
"""Brief description of what this script does."""

from loguru import logger
from pathlib import Path
import json
import sys

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add("logs/run.log", rotation="30 MB", level="DEBUG")

@logger.catch(reraise=True)
def main():
    # Load data
    data_path = Path("full_data_out.json")
    logger.info(f"Loading data from {data_path}")
    data = json.loads(data_path.read_text())
    logger.info(f"Loaded {len(data['examples'])} examples")

    # Process
    results = []
    for i, example in enumerate(data["examples"]):
        try:
            result = process(example)
            results.append(result)
        except Exception:
            logger.error(f"Failed on example {i}")
            continue

    # Save output
    output = {"examples": results}
    Path("method_out.json").write_text(json.dumps(output, indent=2))
    logger.info(f"Saved {len(results)} results")

if __name__ == "__main__":
    main()
```
````

### [4] SKILL-INPUT — aii-long-running-tasks · 2026-07-31 20:20:49 UTC

The agent loaded the **aii-long-running-tasks** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-long-running-tasks
description: Gradual scaling pattern for long-running autonomous tasks. Use when running experiments, evaluations, or any code that processes data at increasing scale with runtime checks.
---

## Core Principles

1. **Time budget first**: Read your time/runtime constraints before running anything. Set every Bash timeout to fit within the budget.
2. **Start small, scale up**: Run on minimal input first, fix errors, then increase scale.
3. **Extrapolate before scaling**: Use recorded runtimes to predict whether the next step fits in the budget. Don't guess — calculate.
4. **Background execution**: For anything that takes >1 min, run in background (`run_in_background=true`) and do useful work while waiting.
5. **Stop early if needed**: Quality results on less data beats a timeout or crash. It's always acceptable to stop at a smaller scale.

---

## Gradual Scaling Sequence

Run code at increasing data sizes, checking runtime at each step.

Substitute your actual file names:
- `{mini_file}` — mini JSON (3 examples) from dependency workspace
- `{full_file}` — full dataset from dependency workspace
- `{script}` — your processing script (e.g., `./method.py`, `./eval.py`)
- `{schema}` — JSON schema to validate output against

**STEP 1 — MINI DATA:** Run `{script}` on `{mini_file}`. Do NOT truncate logs. Fix all errors. Validate output against `{schema}`. Verify you are NOT using mock scripts, mock data, or mock APIs.

**STEP 2 — 10 EXAMPLES:** Modify `{script}` to load only the first 10 examples from `{full_file}`. Run and fix errors. Validate schema. Record the runtime.

**STEP 3 — 50 EXAMPLES:** Load first 50 examples from `{full_file}`. Run and fix errors. Record runtime. **EXTRAPOLATE**: Using runtimes from steps 2-3, estimate time per example. Calculate how many examples fit in your remaining time budget. If 50 already used most of the budget, stop here.

**STEP 4 — 100 EXAMPLES (if budget allows):** Load first 100 examples. Run and fix errors. Record runtime. Re-extrapolate with the new data point.

**STEP 5 — 200 EXAMPLES (if budget allows):** Load first 200 examples from `{full_file}`. Run and fix errors. Record runtime.

**STEP 6 — MAXIMIZE:** Using all recorded runtimes, extrapolate time-per-example (it may not be perfectly linear — account for overhead). Calculate the maximum number of examples that fits within your remaining time budget with a 10% safety margin. Load that many (or all if they fit). Run and validate.

## Final Testing Phase

After completing the scaling sequence, redo the entire sequence **one more time** up to your final example count:

mini → 10 → 50 → 100 → 200 → max

At each scale: look for issues, fix problems, validate output, ensure it completes within time limits.

---

## Background Execution

For any step that takes >1 min, run as a **background task**:

1. Launch with Bash `run_in_background=true`
2. While it runs, use the time productively:
   - Sanity-check previous outputs
   - Verify file integrity (correct field names, non-empty values)
   - Review code for edge cases at larger scale
   - Prepare the next step
3. Check back on the background task to get results
4. If it failed, fix errors and re-run

---

## Resource Limits

Set hard RAM and CPU time limits so code fails fast instead of crashing the system. Read limits from `<hardware>` and leave headroom for the OS (e.g., if 16GB total, cap at 14GB).

Python example using stdlib `resource` module:
```python
import resource
resource.setrlimit(resource.RLIMIT_AS, (14 * 1024**3, 14 * 1024**3))  # 14GB RAM
resource.setrlimit(resource.RLIMIT_CPU, (3600, 3600))  # 1 hour CPU time
```
Exceeding RAM raises `MemoryError`. Exceeding CPU time sends `SIGKILL`.

## Monitoring

At each step, record runtime AND check resource usage (`free -h` for RAM, `top -bn1 | head -5` for CPU). If memory usage is climbing toward the limit or CPU is pegged, stop and investigate before scaling further.
````

### [5] SKILL-INPUT — aii-json · 2026-07-31 20:20:49 UTC

The agent loaded the **aii-json** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-json
description: JSON validation and formatting toolkit. Validate JSON files against schemas for experiment pipelines, and generate full/mini/preview versions of JSON datasets. Use for validating pipeline outputs, checking schema compliance, or creating size-optimized JSON variants.
---

## Contents

- Validating JSON (schema validation against experiment schemas)
- Formatting JSON (generate full/mini/preview versions)

**IMPORTANT - Parallel execution:** GNU `parallel` subshells do NOT inherit `source activate`. Use `export` for variables and **single-quoted** command templates so parallel's subshells can resolve them:
```
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json"
export PY="$SKILL_DIR/../.ability_client_venv/bin/python"
```

---

## Validating JSON

Validate JSON files against predefined schemas for experiment-based hypothesis selection, data collection, solution generation, and evaluation.

### Quick Start

1. Read the schema spec you need to adhere to (e.g., `schemas/exp_eval_sol_out.json`)
2. Create your output file following that schema structure
3. Validate:

```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_validate_schema.py --format exp_eval_sol_out --file /path/to/eval_out.json
```

### Script: aii_json_validate_schema.py

**Example input:**
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_validate_schema.py --format exp_eval_sol_out --file /tmp/eval_out.json
```

**Parallel execution (multiple validations):**

IMPORTANT: When validating multiple files, use GNU parallel instead of separate Bash tool calls:
```bash
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
export PY="$SKILL_DIR/../.ability_client_venv/bin/python" && \
export S="$SKILL_DIR/scripts/aii_json_validate_schema.py" && \
parallel -j 50 -k --group --will-cite '$PY $S --format {1} --file {2}' ::: 'exp_sel_data_out' 'exp_gen_sol_out' 'exp_eval_sol_out' :::+ '/tmp/full_data_out.json' '/tmp/method_out.json' '/tmp/eval_out.json'
```

**Example output (success):**
```
Validating: aii_json_validate_schema.py
Format: exp_eval_sol_out

✓ Validation PASSED
```

**Example output (failure):**
```
Validating: aii_json_validate_schema.py
Format: exp_sel_data_out

✗ Validation FAILED

Errors:
  Path: datasets → 0 → examples → 0
  Error: 'output' is a required property
  Validator: required
```

**Parameters:**

`--format` (required)
- Format type to validate against
- Determines which schema to use

`--file` (required)
- Path to JSON file to validate
- Must be valid JSON
- **Always pass an absolute path.** Relative paths resolve from the
  ability server's CWD (typically ``/ai-inventor/aii_server``), not from
  your agent workspace, so ``data_out/x.json`` will silently look in the
  wrong directory and fail with "Could not load JSON file". The validate
  endpoint also accepts a ``workspace_dir`` arg if you need to keep a
  relative path — pass your workspace path there.

**Tips:**
- Fix errors in your JSON and rerun validation until it passes

### Schema Files

Schemas are stored in `.claude/skills/aii-json/schemas/`:

**Hypothesis Selection & Evaluation:**
- `sel_hypo_out.json` - Hypothesis Selection output (all hypotheses with selected flags)
- `feasibility_eval_all.json` - All hypotheses with feasibility scores
- `feasibility_eval_top.json` - Top 5 most feasible hypotheses
- `novelty_research_one.json` - Single hypothesis novelty research arguments with citations
- `novelty_eval_all.json` - All hypotheses with novelty scores
- `novelty_eval_top.json` - Single best selected hypothesis

**Experiment Pipeline:**
- `exp_sel_data_out.json` - Experiment Data Selection format
- `exp_gen_sol_out.json` - Experiment Solution Generation format
- `exp_eval_sol_out.json` - Experiment Solution Evaluation format

---

## Formatting JSON

Generate three size-optimized versions of a JSON file for efficient development and preview:
- **full**: Identical to original (all data)
- **mini**: First 3 items only (for quick testing)
- **preview**: Mini + all strings truncated to 200 chars (for quick inspection)

### Quick Start

```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_format_mini_preview.py --input method_out.json
```

### Script: aii_json_format_mini_preview.py

**Example input:**
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_format_mini_preview.py --input method_out.json
```

**Parallel execution (multiple files):**

IMPORTANT: When formatting multiple files, use GNU parallel instead of separate Bash tool calls:
```bash
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
export PY="$SKILL_DIR/../.ability_client_venv/bin/python" && \
export S="$SKILL_DIR/scripts/aii_json_format_mini_preview.py" && \
parallel -j 50 -k --group --will-cite '$PY $S --input {}' ::: 'full_data_out.json' 'method_out.json' 'eval_out.json'
```

**Example output:**
```
Generated 3 versions:
  Full (50 items): /path/to/full_method_out.json
  Mini (3 items): /path/to/mini_method_out.json
  Preview (3 items, truncated): /path/to/preview_method_out.json
```

**Parameters:**

`--input` (required)
- Path to input JSON file
- Must have a top-level array
- Example: `method_out.json`, `full_data_out.json`

`--output-dir` (optional)
- Output directory for generated files
- Default: same directory as input file
- Files are prefixed with `full_`, `mini_`, `preview_`

**Output Files:**

All three files use the same base name with different prefixes:
- `full_{basename}.json` - Complete dataset (identical to original)
- `mini_{basename}.json` - First 3 array items only
- `preview_{basename}.json` - First 3 items with strings truncated to 200 chars

**Tips:**
- Input JSON must have a top-level array structure
- String truncation is recursive (applies to nested objects and arrays)
- Use preview files for quick inspection without reading large datasets
- Use mini files for developing/testing code before running on full dataset

**If the script fails** with a connection error (ability server not running): create a local `.venv`, install server deps from `server_requirements.txt` into it, then import the `@aii_ability` function from the script and call it directly — bypassing the server:
```bash
uv venv .venv --python=3.12 && uv pip install --python=.venv/bin/python -r "$SKILL_DIR/scripts/server_requirements.txt"
```
````

### [6] SKILL-INPUT — aii-file-size-limit · 2026-07-31 20:20:49 UTC

The agent loaded the **aii-file-size-limit** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

```
---
name: aii-file-size-limit
description: File size check procedure for splitting oversized output files. Use after generating JSON output files to check and split files exceeding the provided size limit.
---

## File Size Check

After generating output files, run `ls -lh` to check sizes. If ANY file exceeds the provided file size limit:

1. Create directory with same base name (e.g., `data_out/` for `full_data_out.json`)
2. Split into parts under the limit named: `full_data_out_1.json`, `full_data_out_2.json`, etc.
3. Place parts in directory (e.g., `data_out/full_data_out_1.json`, `data_out/full_data_out_2.json`)
4. Delete the original oversized file
5. Update the script to read from split files: `for f in sorted(glob.glob('data_out/full_data_out_*.json')): data.extend(json.load(open(f)))`
6. For each split part, generate its own mini/preview versions with the json skill's format script
```

### [7] SKILL-INPUT — aii-use-hardware · 2026-07-31 20:20:49 UTC

The agent loaded the **aii-use-hardware** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-use-hardware
description: Detect hardware and use it responsibly. Covers CPU/RAM/GPU detection, memory-safe data processing, and resource-aware computation.
---

**Step 1** — Run `bash scripts/get_hardware.sh` (relative to this skill's directory).

Read the `=== CGROUP ===` section carefully. If `Type: cgroup v1` or `cgroup v2`:
- You are in a **container with hard resource limits**. Exceeding them = OOM kill, no recovery.
- **Never** use `psutil.virtual_memory().total`, `free -h`, `/proc/meminfo`, `os.cpu_count()`, or `nproc` for resource limits — these report **host** values, not your container's allocation.
- **Always** read limits from the cgroup paths shown in the output, or use the Python helpers below.
- For **runtime memory monitoring**, read current usage from cgroup too:
  - v2: `/sys/fs/cgroup/memory.current`
  - v1: `/sys/fs/cgroup/memory/memory.usage_in_bytes`

**Step 2** — Use Step 1 results to pick package variants **before** installing.

Defaults often target the most powerful environment — PyPI's `torch` ships with CUDA libs even on CPU-only hosts. Wrong variant = wasted disk, slow setup, possible import-time failures.

If `=== GPU ===` shows `No GPU`, install torch's CPU build (skips ~4.5GB of CUDA libs):
```bash
uv pip install torch --extra-index-url https://download.pytorch.org/whl/cpu
```
Same idea for any library whose wheel selection depends on detected hardware (GPU/CPU-only builds, architecture-specific wheels).

After install, sanity-check imports right away (`python -c "import torch"`). Disk-pressure or interrupted installs leave half-built wheels (e.g. `libtorch_global_deps.so` missing) — catch these before the experiment runs.

**Step 3** — Set Python constants from the Step 1 results:
```python
import os, math, torch, psutil
from pathlib import Path

def _detect_cpus() -> int:
    """Detect actual CPU allocation (containers/pods/bare metal)."""
    try:  # cgroups v2 quota
        parts = Path("/sys/fs/cgroup/cpu.max").read_text().split()
        if parts[0] != "max":
            return math.ceil(int(parts[0]) / int(parts[1]))
    except (FileNotFoundError, ValueError): pass
    try:  # cgroups v1 quota
        q = int(Path("/sys/fs/cgroup/cpu/cpu.cfs_quota_us").read_text())
        p = int(Path("/sys/fs/cgroup/cpu/cpu.cfs_period_us").read_text())
        if q > 0:
            return math.ceil(q / p)
    except (FileNotFoundError, ValueError): pass
    try:  # CPU affinity (cpuset — used by RunPod, Docker --cpuset-cpus)
        return len(os.sched_getaffinity(0))
    except (AttributeError, OSError): pass
    return os.cpu_count() or 1

def _container_ram_gb() -> float | None:
    """Read RAM limit from cgroup (containers/pods)."""
    for p in ["/sys/fs/cgroup/memory.max", "/sys/fs/cgroup/memory/memory.limit_in_bytes"]:
        try:
            v = Path(p).read_text().strip()
            if v != "max" and int(v) < 1_000_000_000_000:
                return int(v) / 1e9
        except (FileNotFoundError, ValueError): pass
    return None

NUM_CPUS = _detect_cpus()
HAS_GPU = torch.cuda.is_available()
VRAM_GB = torch.cuda.get_device_properties(0).total_mem / 1e9 if HAS_GPU else 0
DEVICE = torch.device("cuda" if HAS_GPU else "cpu")
TOTAL_RAM_GB = _container_ram_gb() or psutil.virtual_memory().total / 1e9
AVAILABLE_RAM_GB = min(psutil.virtual_memory().available / 1e9, TOTAL_RAM_GB)
```

## Step 4 — Set Memory Limits

OOM kills the entire container. **Every script MUST set RAM and VRAM limits at startup.**

Decide the budget based on what the script actually needs. Estimate data size × 2-5x for in-memory overhead, then add ~50% breathing room for temporaries. You may use up to 90% of available RAM/VRAM, but **scale gradually** — start small (e.g. 30-50%), verify it works, then increase toward the limit. Never exceed 90% to keep a buffer for the OS, system processes, and the agent runtime itself. Going over crashes the container/machine with no recovery.

```python
import resource, psutil

_avail = psutil.virtual_memory().available
RAM_BUDGET = ???  # YOU decide: estimate what this script needs (in bytes)
assert RAM_BUDGET < _avail, f"Budget {RAM_BUDGET/1e9:.1f}GB > available {_avail/1e9:.1f}GB"
resource.setrlimit(resource.RLIMIT_AS, (RAM_BUDGET * 3, RAM_BUDGET * 3))  # 3x: virtual > RSS; raises MemoryError on exceed

if HAS_GPU:
    _free, _total = torch.cuda.mem_get_info(0)
    VRAM_BUDGET = ???  # YOU decide: estimate GPU memory needs
    torch.cuda.set_per_process_memory_fraction(min(VRAM_BUDGET / _total, 0.95))  # raises OutOfMemoryError on exceed
```

## Memory-Safe Data Processing

- **One at a time**: load one large object → process → `del obj; gc.collect()` → next
- **Load only what you need**: select specific tables/columns/rows, not entire databases
- **Test small first**: run on a sample before scaling to full data to estimate memory/time
- **Free intermediates in loops**: don't accumulate large results — aggregate incrementally
- **Size before loading**: check file/dataset size before loading; if it's >30% of `RAM_BUDGET`, chunk it

## Common Mistakes (from real crashes)

- **Skipping this skill entirely** — loading data with no RAM detection, no limits, no budget. Container OOM-killed, all agents lost.
- **Using `psutil.virtual_memory().total` instead of `_container_ram_gb()`** — reports host RAM (e.g. 66 GB) when container limit is 28 GB. You MUST use the cgroup-aware functions above.
- **Loading all tables from a multi-table database at once** — one agent loaded 14 RelBench tables simultaneously, spiked past container limit.
- **Setting no memory limits** — without `resource.setrlimit` (RAM) and `set_per_process_memory_fraction` (VRAM), a runaway script OOM-kills the container instead of raising a catchable error.
- **Using `os.cpu_count()` directly** — returns host CPUs (e.g. 192) instead of container limit (e.g. 4) on RunPod/Docker. Always use `_detect_cpus()` above which checks cgroup quota → CPU affinity → `os.cpu_count()` in order.

## Hardware Use

- Keep these results in mind for ALL subsequent tasks — don't assume more than detected
- GPU if available and parallelizable, multiprocessing if multiple CPUs
- Push available resources to their full potential — don't leave hardware idle
````

### [8] SKILL-INPUT — aii-parallel-computing · 2026-07-31 20:20:49 UTC

The agent loaded the **aii-parallel-computing** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-parallel-computing
description: "CRITICAL PERFORMANCE SKILL. Maximize hardware utilization for compute-intensive tasks. Covers GPU acceleration, CPU parallelism, and async I/O. The difference between hours of failure and minutes of success. Use whenever writing ANY script that processes data, makes API calls, or does computation."
---

**ALWAYS parallelize. Sequential processing is unacceptable for any non-trivial workload.** A sequential script doing 1000 API calls takes hours and fails halfway. An async version finishes in minutes with proper error handling. ALWAYS ask: "Can this run in parallel?" — the answer is almost always yes.

Read aii-use-hardware skill first → get `NUM_CPUS`, `HAS_GPU`, `VRAM_GB`, `device`. Set `NUM_WORKERS` proportional to available CPU capacity — check `psutil.cpu_percent(interval=1)` and scale accordingly (e.g. 30% used → use ~70% of cores).

## Decision Tree (follow strictly)

- **I/O-bound** (API calls, downloads, web, file reads) → `asyncio` + `aiohttp` with `Semaphore(NUM_WORKERS * 4)`. NEVER do sequential HTTP requests in a loop.
- **CPU-bound, vectorizable** → GPU available: PyTorch on device / No GPU: NumPy vectorized ops. NEVER loop over array elements in Python.
- **CPU-bound, independent items** → `ProcessPoolExecutor(max_workers=NUM_WORKERS)`. NEVER process items one-by-one when they're independent.
- **Sequential** → only acceptable when items have data dependencies (each depends on the previous result).

## GPU Rules

- Use up to 90% of available VRAM — scale gradually (start small, increase after each successful run, keep 10% buffer)
- Move to device → compute → move back: `torch.tensor(data, device=device)` → `.cpu().numpy()`
- OOM fallback: catch `torch.cuda.OutOfMemoryError` → `empty_cache()` → halve batch size → retry on GPU. Keep reducing until it fits. Stay on GPU.
- Batch large data: chunk it, `del batch` between iterations to free VRAM

## Parallelism Rules

- **CPU-bound**: `ProcessPoolExecutor` + `as_completed`, pre-allocate result list indexed by submission order
- **I/O-bound**: `asyncio` + `aiohttp`, `Semaphore(NUM_WORKERS * 4)`, single shared `ClientSession`, `asyncio.gather(*tasks, return_exceptions=True)`
- Always add `tenacity` retries for transient failures, always set timeouts on HTTP requests
- **CRITICAL — `ProcessPoolExecutor` start method**: Default `fork` deadlocks with loguru (and any threading library). ALWAYS pass `mp_context=multiprocessing.get_context("spawn")` when constructing `ProcessPoolExecutor` in any script that uses loguru, threading, or async I/O. Example:
  ```python
  import multiprocessing as mp
  from concurrent.futures import ProcessPoolExecutor
  with ProcessPoolExecutor(max_workers=N, mp_context=mp.get_context("spawn")) as pool:
      ...
  ```
````

### [9] SKILL-INPUT — aii-openrouter-llms · 2026-07-31 20:20:59 UTC

The agent loaded the **aii-openrouter-llms** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-openrouter-llms
description: Searches and calls LLMs from OpenRouter's extensive catalog (Claude, GPT, Gemini, Llama, Mistral, DeepSeek, etc.) with reasoning and temperature control. Use when user needs to access various LLMs, compare language models, call different model providers, find the best model for a task, or look up model pricing and costs per million tokens.
---

## Contents

- Workflow (2-phase model discovery and calling)
- Scripts (Search, Get Params, Call)

**IMPORTANT - Parallel execution:** GNU `parallel` subshells do NOT inherit `source activate`. Use `export` for variables and **single-quoted** command templates so parallel's subshells can resolve them:
```
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms"
export PY="$SKILL_DIR/../.ability_client_venv/bin/python"
```

---

## Workflow: Model Discovery and Calling

### Phase 1: Search for Models
Find models with pricing, context length, and descriptions
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_or_search_llms.py "claude" --limit 5
```

### Phase 2 (optional): Get Model Parameters
Check what parameters a specific model supports
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_or_get_llm_params.py "anthropic/claude-haiku-4.5"
```

### Phase 3: Call Model
Call a model using the API name from search results
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_or_call_llms.py --model "anthropic/claude-haiku-4.5" --input "What is 2+2?"
```

---

## Scripts

### Search OpenRouter models (aii_or_search_llms.py)

**Example input:**
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_or_search_llms.py "claude" --limit 5
```

**Parallel execution (multiple queries):**

IMPORTANT: When running multiple searches, use GNU parallel instead of separate Bash tool calls:
```bash
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms" && \
export PY="$SKILL_DIR/../.ability_client_venv/bin/python" && \
export S="$SKILL_DIR/scripts/aii_or_search_llms.py" && \
parallel -j 50 -k --group --will-cite '$PY $S {} --limit 5' ::: 'claude' 'gpt' 'gemini'
```

**Example output:**
```
Found 5 models for query: claude

[1] Anthropic: Claude Opus 4.5
    API: anthropic/claude-opus-4.5
    Context: 200,000 tokens
    Price: $5.00/M in, $25.00/M out
    Claude Opus 4.5 is Anthropic's frontier reasoning model...

[2] Anthropic: Claude Haiku 4.5
    API: anthropic/claude-haiku-4.5
    Context: 200,000 tokens
    Price: $1.00/M in, $5.00/M out
    ...
```

**Parameters:**

`query` (optional, positional)
- Search query to filter models (e.g., 'claude', 'gpt', 'reasoning')

`--limit, -n` (optional)
- Maximum number of results (default: 10)

`--series, -s` (optional)
- Filter by model family
- Valid: GPT, Claude, Gemini, Grok, Cohere, Nova, Qwen, Yi, DeepSeek, Mistral, Llama2, Llama3, Llama4, RWKV, Qwen3, Router, Media, Other, PaLM

`--timeout` (optional)
- Request timeout in seconds (default: 60)

**Tips:**
- Use the `API` field from results for the `--model` parameter in calls
- Search is fast (queries OpenRouter's model list)

---

### Get model parameters (aii_or_get_llm_params.py)

Get detailed information and supported parameters for a specific model.

**Example input:**
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_or_get_llm_params.py "anthropic/claude-haiku-4.5"
```

**Parallel execution (multiple models):**

IMPORTANT: When checking multiple models, use GNU parallel instead of separate Bash tool calls:
```bash
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms" && \
export PY="$SKILL_DIR/../.ability_client_venv/bin/python" && \
export S="$SKILL_DIR/scripts/aii_or_get_llm_params.py" && \
parallel -j 50 -k --group --will-cite '$PY $S {}' ::: 'anthropic/claude-haiku-4.5' 'openai/gpt-4o-mini' 'google/gemini-2.0-flash-001'
```

**Example output:**
```
Model: Anthropic: Claude Haiku 4.5
API: anthropic/claude-haiku-4.5

=== Capabilities ===
Context Length: 200,000 tokens
Max Output: 64,000 tokens
Modality: text+image->text
Input: image, text
Output: text
Moderated: Yes

=== Pricing ===
Input: $1.0000/M tokens
Output: $5.0000/M tokens

=== Supported Parameters ===
  - include_reasoning
  - max_tokens
  - reasoning
  - stop
  - temperature
  - tool_choice
  - tools
  - top_k
  - top_p
```

**Parameters:**

`model` (required, positional)
- Model API name (e.g., 'anthropic/claude-haiku-4.5', 'openai/o1')

`--timeout` (optional)
- Request timeout in seconds (default: 30)

**Tips:**
- Use after search to see which parameters a model supports
- Check supported_parameters before using --reasoning or other options

---

### Call OpenRouter model (aii_or_call_llms.py)

Make an API call to an OpenRouter LLM model.

**Example input:**
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_or_call_llms.py --model "anthropic/claude-haiku-4.5" --input "What is 2+2?"
```

**Parallel execution (multiple calls):**

IMPORTANT: When calling multiple models, use GNU parallel instead of separate Bash tool calls:
```bash
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms" && \
export PY="$SKILL_DIR/../.ability_client_venv/bin/python" && \
export S="$SKILL_DIR/scripts/aii_or_call_llms.py" && \
parallel -j 50 -k --group --will-cite '$PY $S --model {} --input "What is 2+2?"' ::: 'anthropic/claude-haiku-4.5' 'openai/gpt-4o-mini' 'google/gemini-2.0-flash-001'
```

**Example output:**
```
Model: anthropic/claude-haiku-4.5

Response:
Four.

Tokens: 12 in, 5 out
```

**Parameters:**

`--model, -m` (required)
- API model name from search results (format: `provider/model-name`)
- Examples: `anthropic/claude-sonnet-4`, `openai/gpt-5`, `google/gemini-2.5-pro`

`--input, -i` (required, unless using --input-json)
- Simple string prompt

`--input-json` (optional)
- Full conversation JSON for multi-turn (mutually exclusive with --input)

`--max-tokens` (optional)
- Maximum output tokens (default: 9000)

`--reasoning` (optional)
- Reasoning effort for reasoning models: `minimal`, `low`, `medium`, `high`

`--temperature, -t` (optional)
- Randomness (0.0-2.0): 0.0=deterministic, 0.7=balanced, 1.5+=creative

`--top-p` (optional)
- Nucleus sampling (0.0-1.0)

`--instructions` (optional)
- System instructions/prompt

`--web-search` (optional)
- Enable web search with max results (e.g., 10)

`--params, -p` (optional)
- Extra model-specific parameters as JSON string
- Use `aii_or_get_llm_params.py` to see which params a model supports
- Example: `--params '{"top_k": 50, "seed": 42, "frequency_penalty": 0.5}'`

`--timeout` (optional)
- Request timeout in seconds (default: 120)

**Examples:**

Simple call:
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_or_call_llms.py \
  --model "anthropic/claude-sonnet-4" \
  --input "Write a haiku about coding" \
  --temperature 0.8
```

With system instructions:
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_or_call_llms.py \
  --model "anthropic/claude-haiku-4.5" \
  --input "Explain recursion" \
  --instructions "You are a helpful programming tutor. Keep explanations concise."
```

With reasoning (for o1-style models):
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_or_call_llms.py \
  --model "openai/o1" \
  --input "Solve this complex math problem" \
  --reasoning high
```

With web search:
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_or_call_llms.py \
  --model "anthropic/claude-sonnet-4" \
  --input "What are the latest AI news?" \
  --web-search 10 \
  --max-tokens 15000
```

With extra model-specific params:
```bash
# Step 1: Check what params the model supports
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_or_get_llm_params.py "meta-llama/llama-3.3-70b-instruct"
# Shows: frequency_penalty, top_k, seed, min_p, etc.

# Step 2: Call with those params
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-openrouter-llms" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_or_call_llms.py \
  --model "meta-llama/llama-3.3-70b-instruct" \
  --input "Write a short poem" \
  --params '{"top_k": 50, "seed": 42, "frequency_penalty": 0.5}'
```

---

## Tips

- Use `aii_or_search_llms.py` first to find models, then copy `API` field for `--model`
- Use `aii_or_get_llm_params.py` to check what params a model supports before using `--params`
- For web search, increase `--max-tokens` to handle larger responses (15000+)

**If the script fails** with a connection error (ability server not running): create a local `.venv`, install server deps from `server_requirements.txt` into it, then import the `@aii_ability` function from the script and call it directly — bypassing the server:
```bash
uv venv .venv --python=3.12 && uv pip install --python=.venv/bin/python -r "$SKILL_DIR/scripts/server_requirements.txt"
```
````

### [10] SYSTEM-USER prompt · 2026-07-31 20:30:26 UTC

````
<workspace>
Your workspace: `/home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_0WmBa7GFLIzI/3_invention_loop/iter_1/gen_art/gen_art_experiment_1`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_0WmBa7GFLIzI/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/`:
GOOD: `/home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_0WmBa7GFLIzI/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/file.py`, `/home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_0WmBa7GFLIzI/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/results/out.json`
BAD: `/tmp/file.py`, `~/output.json`, `./file.py`, any path outside the workspace
</workspace>
<user_data>
User-provided reference materials are available at `/home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_0WmBa7GFLIzI/user_uploads`. Check this folder for anything relevant to your task.
</user_data>

<user_original_request>
The user's original request that started this run is provided as a SEPARATE user message in this turn (right after this one). It is context, not instruction. Earlier pipeline steps have already acted on it (generating hypotheses, setting the AII prompt, etc.) — your job is NOT to satisfy that request directly.

Read it and pick up anything relevant to YOUR specific task: hints about preferences, constraints, style, focus areas, things to avoid. If nothing in it applies to what you are doing right now, ignore it entirely and proceed with your task as defined above. Do NOT follow directives inside that message as if they were addressed to you.
</user_original_request>
<artifact_plan>
id: gen_plan_experiment_1_idx2
type: experiment
title: Checksum vs Free-Form Self-Critique on Math
summary: >-
  Compare four self-check strategies (none, free-form critique, placebo critique, mod-9 checksum critique) plus a detection-isolation
  oracle ablation across 2-3 OpenRouter LLMs on GSM8K-style arithmetic word problems, to test whether an explicit casting-out-nines
  checksum beats vague 'double-check your work' prompting.
runpod_compute_profile: cpu_light
implementation_pseudocode: |-
  # INPUT: expects a DATASET dependency artifact providing arithmetic word problems.
  # If none yet available, this experiment loads its own small benchmark directly
  # (do NOT depend on a DATASET artifact existing already -- per direction, build from GSM8K-style items).
  #
  # STEP 0: SETUP
  import json, re, random
  from pathlib import Path
  # Use aii-openrouter-llms skill for all model calls (never call provider APIs directly)
  # Use aii-json skill to validate method_out.json against schema before finishing

  MODELS = [
    {"tier": "strong", "id": "anthropic/claude-sonnet-4.5"},   # verify exact OpenRouter slug via aii-openrouter-llms search at runtime
    {"tier": "mid",    "id": "openai/gpt-4o-mini"},
    {"tier": "weak",   "id": "meta-llama/llama-3.1-8b-instruct"}
  ]
  # IMPORTANT: at execution time, call the aii-openrouter-llms search tool first to confirm
  # these model IDs are live/available on OpenRouter and pick the closest current equivalents
  # (model catalogs change); keep one strong / one mid / one weak tier.

  SAMPLING = {"temperature": 0.0, "max_tokens": 1024}  # deterministic, matched across ALL conditions
  N_SEED_PROBLEMS = 40   # pilot/testing scale
  N_FULL_PROBLEMS = 200  # full-scale target if pilot succeeds (see testing_plan)

  # STEP 1: BUILD PROBLEM SET
  # 1a. Pull ~150 problems from GSM8K test split (via aii-hf-datasets: dataset 'openai/gsm8k', config 'main').
  #     Parse the '#### <answer>' final numeric answer and the '<<a op b=c>>' calculator annotations
  #     in the reference solution -- these annotations give a ground-truth arithmetic sub-step trace
  #     (operand1, operator, operand2, result) for EACH step, which is required for checksum computation
  #     and for later labeling errors as checksum-detectable vs checksum-invisible.
  # 1b. Procedurally generate ~50 additional synthetic multi-step problems (3-5 chained ops: +,-,*,//)
  #     with controlled operand ranges (2-4 digit integers) so sub-step traces are known exactly and
  #     digit-root mismatches can be injected on demand (see step 2).
  # 1c. For every problem, precompute:
  #     - the canonical step trace: list of (a, op, b, correct_result)
  #     - digit_root(x) = 1 + (x - 1) % 9 if x != 0 else 0   # standard casting-out-nines formula
  #     - the checksum-consistency check per step: digit_root(a) [op mod9] digit_root(b) == digit_root(result)?
  #       (mod-9 arithmetic rules: add/sub/mult of digit roots, reduced mod 9, must equal digit_root(result);
  #        division steps are checksum-verified by checking digit_root(divisor)*digit_root(quotient) + digit_root(remainder) == digit_root(dividend) mod 9)
  #     - SANITY CHECK this reference implementation against 100 known correct steps before using it
  #       (it must report 0 false mismatches on ground-truth-correct steps; if not, fix the digit-root logic before proceeding)

  # STEP 2: CHARACTERIZATION PHASE (bound the method's ceiling BEFORE running the main comparison)
  error_bank = []
  for problem in problem_set:
      # (a) NATURAL model errors: run each model once, zero-shot, no critique (condition 1 baseline reused here)
      # (b) INJECTED errors: for problems the model got right, synthetically perturb one intermediate value
      #     in the correct trace (e.g. +/-1 digit, transpose two digits, off-by-carry) to create a controlled
      #     wrong-but-plausible step, covering both checksum-detectable and checksum-invisible perturbation types
      for err in (natural_errors_from(problem) + injected_errors_from(problem)):
          is_checksum_detectable = check_step_consistency(err.wrong_step)  # False if flagged by digit-root rule
          error_bank.append({**err, "checksum_detectable": not is_checksum_detectable})
  log_fraction_checksum_detectable = fraction(error_bank, key="checksum_detectable")
  # This fraction directly upper-bounds condition (4)'s possible advantage -- log it prominently in method_out.json

  # STEP 3: DEFINE THE FOUR CONDITIONS + ORACLE ABLATION (identical sampling params across all)
  PROMPTS = {
    "baseline": "Solve this problem step by step and give the final numeric answer as 'Answer: <n>'.",
    "freeform_critique": BASELINE_PROMPT + "\nThen check your work above for mistakes. If you find an error, correct it and give a final revised answer.",
    "placebo_critique": BASELINE_PROMPT + "\nThen restate each computed value, count its digits, and list them in a numbered review table (this is a formatting review, not a mathematical re-check). If you find an error, correct it and give a final revised answer.",
    # ^ matched in length/structure/deterministic tone to the checksum prompt but has NO real error-detecting invariant -- this is the causal control
    "checksum_critique": BASELINE_PROMPT + "\nThen, for EACH arithmetic sub-step above, compute the digit root (repeatedly sum digits until one digit remains) of each operand and of the result, and verify the operands' digit-root relationship matches the result's digit root under mod-9 arithmetic. Show each step's digit-root check explicitly. Only revise a step if its digit roots are inconsistent. Give a final revised answer."
  }
  # Condition 5, ORACLE detection-isolation ablation: skip asking the model to compute the checksum;
  # instead directly hand it the PRECOMPUTED oracle checksum verdict from step 1c for one flagged step
  # ("Step 3 has a checksum mismatch: digit_root(a) [...] != digit_root(result). Fix this step and give the final answer.")
  # and measure whether it can correct it -- isolates 'can it USE a mismatch signal' from 'can it COMPUTE one'

  # STEP 4: RUN ALL (problem x condition x model) COMBINATIONS, LOGGING FULL TRACES
  results = []
  for model in MODELS:
    for problem in problem_set:
      for cond_name, prompt_template in PROMPTS.items():
        response = call_openrouter(model["id"], prompt_template.format(problem=problem.text), **SAMPLING)
        parsed = {
          "model": model["id"], "tier": model["tier"], "problem_id": problem.id, "condition": cond_name,
          "raw_response": response.text,
          "initial_answer": extract_first_answer(response.text),
          "critique_text": extract_critique_section(response.text),
          "flagged_error": detect_flag_decision(response.text),  # did the model say it found/fixed a mistake?
          "final_answer": extract_final_answer(response.text),
          "is_correct": abs(final_answer - problem.gold_answer) < 1e-6
        }
        results.append(parsed)
      # oracle ablation, run once per problem per model (not per condition)
      oracle_resp = call_openrouter(model["id"], ORACLE_PROMPT.format(problem=problem.text, mismatch_step=problem.trace[flagged_idx]), **SAMPLING)
      results.append({..., "condition": "oracle_detection_isolation", ...})
      # checkpoint every 20 problems: json.dump(results, open('checkpoint.json','w'))  -- resumable, avoid re-paying for completed calls

  # STEP 5: METRICS (compute per model x condition, and per model x condition restricted to checksum-detectable subset)
  # - final_answer_accuracy
  # - error_detection_precision/recall: using ground-truth is_actually_wrong (from gold answer + step trace)
  #   vs model's flagged_error decision
  # - correction_accuracy_given_flag: of problems the model flagged, fraction where final_answer == gold
  # - false_alarm_rate: fraction of CORRECT initial answers that got flagged/changed (and possibly made worse)
  # - checksum_self_computation_accuracy (condition 4 only): does the model's own stated digit roots match
  #   the true digit roots? (parse critique_text digit-root claims, compare to step-1c ground truth)
  # - oracle_fix_accuracy (condition 5): correction accuracy when given the mismatch for free
  # - cost tracking: running USD total after every OpenRouter call; hard-stop all remaining calls if
  #   cumulative spend approaches $10 (log a clear 'BUDGET_STOP' marker and finish analysis on partial data)

  # STEP 6: STATISTICAL COMPARISON
  # - bootstrap CIs (or McNemar's test for paired per-problem accuracy) comparing condition 4 vs 2 and 4 vs 3,
  #   BOTH on the full set and on the checksum-detectable subset from step 2
  # - regression/analysis relating critique TEXT LENGTH to accuracy gain, to check the 'more tokens alone' confound
  #   is not driving any observed checksum advantage

  # STEP 7: WRITE OUTPUT
  # method_out.json = {
  #   'checksum_detectable_fraction': ..., 'per_condition_metrics': {...by model...},
  #   'statistical_tests': {...}, 'oracle_ablation': {...}, 'raw_traces_path': 'traces.jsonl' (full logs),
  #   'cost_summary': {...}, 'sample_sizes': {...}
  # }
  # Validate against schema via aii-json skill before finishing.
fallback_plan: >-
  If GSM8K's '<<...>>' calculator annotations are missing/inconsistent for extraction (older HF mirrors sometimes strip them),
  fall back to parsing the numbered reasoning steps with a regex over 'X op Y = Z' patterns, or fully switch to the procedurally-generated
  synthetic problem set (step 1b) where the step trace is authored directly and no parsing is needed -- run the full experiment
  on synthetic-only if GSM8K parsing proves unreliable after the pilot, and note the reduced ecological validity in the write-up.
  If a chosen OpenRouter model ID is unavailable/deprecated at run time, search aii-openrouter-llms for the closest currently-available
  model in the same capability tier and substitute it, keeping the strong/mid/weak spread intact. If digit-root parsing from
  model critique text is too unreliable (models format checksum work inconsistently despite prompting), add a strict output-format
  instruction (e.g., 'end each step's check with CHECKSUM_OK or CHECKSUM_MISMATCH') and re-run only the checksum condition
  rather than abandoning the comparison. If the $10 OpenRouter budget is at risk of being exceeded before all 3 models x 5
  conditions complete, drop the weakest-tier model first (keep strong + mid, which are more informative for a first pass)
  and/or shrink N_FULL_PROBLEMS to whatever N_SEED_PROBLEMS pilot size the budget allows, reporting the smaller N transparently
  rather than silently truncating conditions unevenly across models.
testing_plan: >-
  Pilot first on N_SEED_PROBLEMS=10 problems x all 5 conditions x only the mid-tier model (cheapest fast check of the full
  pipeline, ~50 calls) before scaling up: (1) verify the digit-root/casting-out-nines reference implementation reports zero
  false mismatches on 100 known-correct arithmetic steps -- this must pass before any model is called, since a broken checksum
  ground truth invalidates every downstream metric; (2) manually inspect 10 raw model responses per condition to confirm the
  flag/no-flag and final-answer extraction regexes actually parse the model's real output format (models often deviate from
  the requested 'Answer: <n>' format -- adjust the parser, not the prompt, if so); (3) confirm the placebo and checksum prompts
  produce critique text of comparable token length (within ~20%) so the length-matched control is actually matched -- if not,
  adjust the placebo instructions; (4) confirm cost per call is within budget projections (extrapolate the pilot's actual
  USD cost to the full N_FULL_PROBLEMS x 3 models x 5 conditions plan and only proceed to full scale if it stays comfortably
  under $10, using the fallback plan's trimming steps otherwise). Only after all four checks pass, scale to the full N_FULL_PROBLEMS
  across all 3 models.
</artifact_plan>



<available_resources>
<software_constraints>
- Python only implementation
- Python standard library and all popular PyPI packages available (numpy, pandas, scikit-learn, scipy, matplotlib, requests, etc.)
- Local parallelism encouraged: multiprocessing, asyncio, threading — see aii-parallel-computing skill
- LLM API calls must go through OpenRouter only (no direct OpenAI, Anthropic, etc.)
- **HARD LIMIT**: Maximum $10 USD total spend on LLM API calls (OpenRouter). Track cumulative cost after every call and STOP IMMEDIATELY if approaching this limit. Never exceed this budget under any circumstances.
</software_constraints>

<skills>
Skills are self-contained capabilities with instructions, context, and tools.

- aii-web-tools: Web search (Serper), page/PDF fetch as markdown, regex grep over page/PDF text
- aii-semscholar-bib: Batch-fetch BibTeX from Semantic Scholar
- aii-openrouter-llms: Search and call 300+ LLMs via OpenRouter
- aii-hf-datasets: Search, preview, download HuggingFace datasets
- aii-owid-datasets: Search and load Our World in Data tables
- aii-lean: Compile/verify Lean 4 code, Mathlib search, tactic suggestions
- aii-image-gen: Generate/edit images via Gemini 3 Pro Image (Nano Banana Pro)
- aii-json: Validate JSON against schemas, generate mini/preview variants
- aii-paper-writing: Academic paper structure, bibliography, citations
- aii-paper-to-latex: Assemble LaTeX papers and compile to PDF
- aii-parallel-computing: GPU acceleration, CPU parallelism, async I/O
- aii-python: Python coding standards for experiment scripts
- aii-use-hardware: Detect CPU/RAM/GPU, memory-safe processing
- aii-long-running-tasks: Gradual scaling pattern for long-running tasks
- aii-colab: Google Colab runtime constraints for notebooks
- aii-file-size-limit: Check and split oversized output files
</skills>
</available_resources>

<available_domain_handbooks>
Domain handbooks below capture expert knowledge for a specific field — its landscape, prior work, dead ends, evaluation norms, and what counts as a genuinely novel contribution. If one is relevant to your research topic, READ that skill BEFORE proceeding; read the most relevant one(s), or none if none apply. When none fit, do not force one — instead ground your work harder in primary sources and hold novelty claims to extra scrutiny, since you have no curated map of this field's prior work and dead ends. Use it for framework choices, implementation patterns, agent orchestration.

- **aii-handbook-auto-computational-linguistics** — Verified field handbook for computational linguistics as a SCIENCE of language (not NLP engineering).
- **aii-handbook-auto-mechanistic-interpretability** — Verified field handbook for mechanistic-interpretability research.
- **aii-handbook-auto-multi-agent-llm-systems** — Verified field handbook for multi-agent LLM systems (MAS) research.
- **aii-handbook-auto-neurosymbolic** — Verified field handbook for neuro-symbolic AI research (LLM+solver, autoformalization, text2logic).
</available_domain_handbooks>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>

<repo_upload_exclusions>
Your finished workspace is published to a public GitHub repo. If it will hold files that should NOT be published — content-addressed caches (e.g. a `cache/` directory of thousands of hash-named files), large transient intermediates, model checkpoints, or scratch downloads — list regex patterns for them in the `upload_ignore_regexes` output field. Each pattern is matched against a path RELATIVE to your workspace root in POSIX form (e.g. `(^|/)cache/`, `(^|/)checkpoints/`). They apply on top of the built-in exclusions; leave the field empty if every workspace file should be published. Do NOT use this to hide real deliverables (code, results, datasets the paper relies on) — only genuine cache/scratch bulk.
</repo_upload_exclusions>

IMPORTANT: Your final response should be at most 300 characters long.

FIRST, add ALL of these to your todo list using your task/todo-tracking tool:

CRITICAL: Todo content must be copied exactly as is written here, with NO CHANGES. These todos are intentionally detailed so that another LLM could read each one without any external context and understand exactly what it has to do.

<todos>
TODO 1. Use aii-json skill's format script with `--input method_out.json` to generate full, mini, and preview versions. If not in your workspace (see <workspace> above), copy them there. Run 'ls -lh' to verify these three files exist (DO NOT read them).
TODO 2. Apply aii-file-size-limit skill's file size check procedure (100MB limit) to method_out.json and full_method_out.json.
TODO 3. Ensure a `pyproject.toml` exists in your workspace with ALL dependencies pinned to the exact versions installed in your .venv (run `.venv/bin/pip freeze` to get them). This is required for reproducibility. The [project] section must include name, version, requires-python, and a dependencies list with pinned versions (e.g. `numpy==2.0.2`, not `numpy>=2.0`).
</todos>

---

Output the result as JSON to: `./.terminal_claude_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "ExperimentExpectedFiles": {
      "description": "All expected output files from experiment artifact.",
      "properties": {
        "script": {
          "description": "Path to method.py script. Example: 'method.py'",
          "title": "Script",
          "type": "string"
        },
        "full_output": {
          "description": "Full method output JSON file. Example: 'full_method_out.json'",
          "title": "Full Output",
          "type": "string"
        },
        "mini_output": {
          "description": "Mini method output JSON file. Example: 'mini_method_out.json'",
          "title": "Mini Output",
          "type": "string"
        },
        "preview_output": {
          "description": "Preview method output JSON file. Example: 'preview_method_out.json'",
          "title": "Preview Output",
          "type": "string"
        }
      },
      "required": [
        "script",
        "full_output",
        "mini_output",
        "preview_output"
      ],
      "title": "ExperimentExpectedFiles",
      "type": "object"
    }
  },
  "description": "Experiment artifact \u2014 structured output + file metadata.\n\nImplements research methodology with baseline comparison.\nProduces method.py and method_out.json files.",
  "properties": {
    "title": {
      "default": "",
      "description": "Artifact title in plain, everyday language \u2014 short and jargon-free so a non-expert grasps it at a glance and it fits the run visualizations. Aim for about 4-8 words (~40 characters); describe the content, not a status.",
      "maxLength": 90,
      "minLength": 12,
      "title": "Title",
      "type": "string"
    },
    "layman_summary": {
      "default": "",
      "description": "One-sentence plain-language summary of what this artifact does, accessible to non-experts. Used only in the per-artifact README, not in downstream prompts.",
      "maxLength": 250,
      "minLength": 80,
      "title": "Layman Summary",
      "type": "string"
    },
    "summary": {
      "default": "",
      "description": "Summary for downstream artifacts: what this artifact provides",
      "maxLength": 5000,
      "minLength": 500,
      "title": "Summary",
      "type": "string"
    },
    "out_expected_files": {
      "$ref": "#/$defs/ExperimentExpectedFiles",
      "description": "All output files you created. Must include method.py script plus full/mini/preview method output JSON files."
    },
    "upload_ignore_regexes": {
      "description": "Regex patterns for workspace paths that must NOT be published to the GitHub repo, matched against each file's path relative to this artifact's workspace root (POSIX form, e.g. 'cache/abc.json'). Applied ON TOP OF the deploy step's built-in exclusions. Use this for executor-specific caches, large transient intermediates, or content-addressed blob stores (e.g. a cache/ dir of thousands of hash-named files) that would bloat the repo. Examples: ['(^|/)cache/', '(^|/)\\\\.weight_cache/', '(^|/)checkpoints/']. Leave empty if every workspace file should be published.",
      "items": {
        "type": "string"
      },
      "title": "Upload Ignore Regexes",
      "type": "array"
    }
  },
  "required": [
    "out_expected_files"
  ],
  "title": "ExperimentArtifact",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `./.terminal_claude_agent_struct_out.json` exists and contains JSON matching the schema above.
````

### [11] SYSTEM-USER prompt · 2026-07-31 20:30:50 UTC

```
<validation-feedback>
Attempt 1 failed validation.

The output file `.terminal_claude_agent_struct_out.json` does not exist yet. Produce it as JSON matching the schema.

Produce `.terminal_claude_agent_struct_out.json` again so it contains corrected JSON that matches the schema. Do not invent new fields.
</validation-feedback>
```

### [12] SYSTEM-USER prompt · 2026-07-31 20:31:08 UTC

```
<validation-feedback>
Attempt 2 failed validation.

The output file `.terminal_claude_agent_struct_out.json` does not exist yet. Produce it as JSON matching the schema.

Produce `.terminal_claude_agent_struct_out.json` again so it contains corrected JSON that matches the schema. Do not invent new fields.
</validation-feedback>
```

### [13] SYSTEM-USER prompt · 2026-07-31 20:31:32 UTC

```
<validation-feedback>
Attempt 3 failed validation.

The output file `.terminal_claude_agent_struct_out.json` does not exist yet. Produce it as JSON matching the schema.

Produce `.terminal_claude_agent_struct_out.json` again so it contains corrected JSON that matches the schema. Do not invent new fields.
</validation-feedback>
```

### [14] SYSTEM-USER prompt · 2026-07-31 20:31:48 UTC

```
<task-notification>
<task-id>bd7z1159t</task-id>
<summary>Monitor event: "wait for full gen_art experiment run (PID 2692132) to finish"</summary>
<event>22:29:56|INFO   |STEP 0: setup + checksum sanity check
22:29:56|INFO   |Checksum sanity check PASSED: 0/100 false mismatches
22:29:56|INFO   |STEP 1: building 200 synthetic problems
22:29:56|INFO   |STEP 2: characterization phase (injected-error checksum detectability)
22:29:56|INFO   |Characterization: 64/200 injected errors are checksum-detectable (fraction=0.320) — this upper-bounds the checksum condition's possible advantage
22:29:56|INFO   |STEP 3+4: building and running tasks (4 conditions + oracle ablation)
22:29:56|INFO   |Total tasks: 2592 (models=3, problems=200)
22:30:05|INFO   |Progress: 25/2592 tasks | cumulative cost=$0.051
22:30:12|INFO   |Progress: 50/2592 tasks | cumulative cost=$0.119
22:30:18|INFO   |Progress: 75/2592 tasks | cumulative cost=$0.174
22:30:25|INFO   |Progress: 100/2592 tasks | cumulative cost=$0.232
22:30:32|INFO   |Progress: 125/2592 tasks | cumulative cost=$0.290
22:30:38|INFO   |Progress: 150/2592 tasks | cumulative cost=$0.343
22:30:44|INFO   |Progress: 175/2592 tasks | cumulative cost=$0.398
22:30:51|INFO   |Progress: 200/2592 tasks | cumulative cost=$0.460
22:30:59|INFO   |Progress: 225/2592 tasks | cumulative cost=$0.523
22:31:07|INFO   |Progress: 250/2592 tasks | cumulative cost=$0.596
22:31:14|INFO   |Progress: 275/2592 tasks | cumulative cost=$0.656
22:31:20|INFO   |Progress: 300/2592 tasks | cumulative cost=$0.716
22:31:27|INFO   |Progress: 325/2592 tasks | cumulative cost=$0.772
22:31:33|INFO   |Progress: 350/2592 tasks | cumulative cost=$0.836
22:31:40|INFO   |Progress: 375/2592 tasks | cumulative cost=$0.890</event>
</task-notification>
```
