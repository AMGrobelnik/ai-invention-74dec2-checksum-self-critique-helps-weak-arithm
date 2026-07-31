# gen_plan_experiment_1 — test_idea

> Phase: `invention_loop` · round 1 · `gen_plan`
> Run: `run_0WmBa7GFLIzI` — Checksum Self-Critique Helps Weak Arithmetic, Hurts Weak Models
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `gen_plan_experiment_1` (terminal_claude_agent, claude-sonnet-5)

### [1] CONFIG · 2026-07-31 20:19:24 UTC

```
model: claude-sonnet-5 | effort: low | permission: bypassPermissions | cwd: /home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_0WmBa7GFLIzI/3_invention_loop/iter_1/gen_plan/gen_plan_experiment_1
```

### [2] SYSTEM-USER prompt · 2026-07-31 20:19:30 UTC

````
<ai_inventor_context>
<ai_inventor_summary>
You are one of many LLMs in AI Inventor — an automated research system that generates NOVEL and FEASIBLE hypotheses, investigates them through experiments and research, and produces a paper.

Your output feeds other LLMs downstream. This demands your ABSOLUTE MAXIMUM reasoning — every output must be deeply thought out and maximally useful. Surface-level responses waste downstream computation.
</ai_inventor_summary>

<your_role>
YOU ARE: A plan generator (Step 3.2: GEN_PLAN in the invention loop)

You received the hypothesis, an artifact direction to elaborate, and dependency artifacts relevant to the plan.
Your job: elaborate this direction into a detailed, actionable plan for the executor agent.

Specific, actionable plan → valuable artifact. Vague plan → wasted execution.
</your_role>
</ai_inventor_context>

<artifact_type_info>
You are expanding an artifact direction of type: EXPERIMENT

EXPERIMENT
Run code to test hypotheses, implement methods, and collect empirical results.
Runtime: Python 3.12, UV (any pip package), isolated workspace, gradual scaling (mini → full data).
Tools: Full shell/Python/filesystem access, the aii-web-tools skill (web search, page fetch, regex grep over full page/PDF text), and other skills.
Skills: aii-json (schema validation), aii-openrouter-llms (call any LLM — GPT, Gemini, Llama, etc.), domain-specific as needed.
Capabilities: Implement and run any code-based experiment, compare method vs baselines.
Deps: REQUIRED at least one DATASET | OPTIONAL RESEARCH for methodology guidance
</artifact_type_info>

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

<time_budget>

The experiment executor has 6h total (including writing code, debugging, testing, and fixing errors).

</time_budget>

<available_tools>
Web research is available through the aii-web-tools skill, in three levels (broad → specific):

1. web search — Returns titles, URLs, snippets. Use first to discover and scan the landscape.
2. web fetch — Reads a page and returns its content as markdown (HTML or PDF). Use to understand a source. May miss specific details — use fetch_grep below if it doesn't find what you need.
3. fetch_grep — Regex search over a page/PDF's full text. Returns exact matching sections with context. Use for precise details, exact numbers, methodology, or PDFs.

Workflow: search → fetch (understand) → fetch_grep (extract specifics).
</available_tools>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>

<plan_guidelines>
You are expanding an artifact direction from the strategy into a detailed plan.
The artifact direction specifies what to do at a high level (type, objective, approach, dependencies).
Your job is to make it concrete and actionable as a detailed plan.
Use web research to look up technical details, verify feasibility, and find reference materials
that will make your plan more concrete and actionable for the executor.

GOOD PLANS:
- Make each component SPECIFIC and actionable (not vague platitudes)
- Consider both success AND failure scenarios
- Build on the approach in the artifact direction
- Add concrete details the executor needs

BAD PLANS:
- Vague hand-waving ("do research on X")
- Ignoring the approach in the artifact direction
- Missing critical details the executor needs
</plan_guidelines>

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

<hypothesis>
kind: hypothesis
title: Checksum Critique Beats Free-Form Self-Doubt
hypothesis: >-
  When an LLM verifies its own multi-step arithmetic word-problem solution using an explicit, mechanically-computed modular-arithmetic
  invariant (a 'casting-out-nines' digit-root checksum applied to each intermediate computation) instead of an open-ended
  'double-check your work' self-critique prompt, error-detection and downstream correction accuracy will be substantially
  higher, because the checksum converts error detection from a hard task (re-deriving the whole solution and comparing it
  to a fuzzy memory of the first pass) into an easy, decoupled task (a single mod-9 residue comparison per arithmetic step).
motivation: >-
  Free-form LLM self-critique on arithmetic reasoning has a well-documented failure mode: models tend to just re-state or
  superficially re-read their own output rather than independently re-verify it, so errors survive the 'critique' step. Recent
  mechanistic work shows the internal circuits LLMs use for error detection rely on shallow 'surface-level consistency' checks
  between numbers in the text, not on genuine independent recomputation - which is exactly why free-form self-critique is
  weak. If instead the model is given an explicit, cheap, structurally-independent invariant to check against - the kind human
  bookkeepers used for centuries to catch arithmetic slips - error detection no longer requires the model to hold and compare
  two full derivations in its fragile context; it only has to compute and compare small digit-root residues. If this works,
  it gives a nearly-free, training-free reliability boost applicable to any LLM-based arithmetic pipeline (tutoring, financial
  calculations, agentic tool-free math), and it clarifies WHY self-critique fails (missing independent invariant) rather than
  just showing IF it fails.
assumptions:
- >-
  Multi-step arithmetic word problems admit a well-defined intermediate computation trace (each step is an addition/subtraction/multiplication/division
  of specific numbers) that can be checksum-verified independently of the natural-language reasoning around it.
- >-
  LLMs can reliably compute digit sums / digital roots and mod-9 arithmetic on short numbers when explicitly instructed to
  do so as an isolated sub-task, even if they are unreliable at full multi-digit arithmetic in the original problem.
- >-
  The gain (if any) comes specifically from the invariant structure of the check, not merely from adding any extra deterministic-looking
  verification text - this needs a matched-effort control.
- >-
  Errors LLMs make on these problems are frequently checksum-detectable numeric slips (digit/carry/transcription errors) rather
  than purely logical/modeling errors that preserve numeric consistency, so there is meaningful room for a numeric-invariant
  check to catch them.
investigation_approach: >-
  Build a benchmark of multi-step arithmetic word problems (adapting GSM8K-style items plus procedurally generated variants
  with controlled numeric ranges) and first characterize, via injected errors and natural model errors, how often mistakes
  are 'checksum-detectable' (violate mod-9 consistency) versus 'checksum-invisible' (numerically consistent but logically
  wrong), to bound the method's ceiling. Then compare four conditions on multiple LLMs (via OpenRouter) at matched sampling
  settings: (1) no self-check baseline, (2) generic free-form self-critique ('check your work'), (3) matched-length deterministic-looking
  placebo critique with no real invariant (controls for 'extra thinking tokens' confound), and (4) the proposed checksum critique,
  where the model is walked through computing digit-root checksums for each arithmetic sub-step and instructed to only flag/revise
  a step if the checksums disagree. Measure final-answer accuracy, error-detection precision/recall (does the critique step
  correctly flag genuinely wrong steps and correctly pass genuinely right ones), and correction accuracy conditional on a
  flag. Also run an ablation isolating detection from correction (give the model an already-computed checksum mismatch signal
  and measure whether it can fix the step) to separate 'can the model use the checksum' from 'can the model compute the checksum.'
success_criteria: >-
  The hypothesis is supported if the checksum-critique condition (4) yields significantly higher final-answer accuracy and
  higher error-detection recall/precision than both the free-form critique (2) and the matched-length placebo (3), on problems
  within the checksum-detectable subset identified in the characterization phase, across multiple LLMs of varying capability,
  with the gap not explained by prompt length alone. It is disconfirmed (or the checksum's advantage is not causal) if performance
  is statistically indistinguishable from the placebo control (3) - implying any 'extra structured deliberation' helps equally
  regardless of the invariant - or if models frequently miscompute the checksums themselves and thus generate false alarms/misses
  that erase the theoretical advantage, or if most real-world errors fall in the checksum-invisible (logical/modeling) category
  rather than the numeric-slip category, capping any possible gain.
related_works:
- >-
  'The Validation Gap: A Mechanistic Analysis of How Language Models Compute Arithmetic but Fail to Validate It' (Bertolazzi
  et al., EMNLP 2025) shows via circuit analysis that LLMs' internal error-detection relies on shallow surface-level numeric
  consistency heads rather than genuine recomputation - this motivates the hypothesis but is purely diagnostic/mechanistic
  and proposes no intervention; the proposed work turns that diagnosis into a concrete, testable intervention (an explicit
  external invariant) and measures its behavioral effect.
- >-
  Self-Refine / generic self-critique and self-correction literature (e.g. Madaan et al. 'Self-Refine', and subsequent work
  such as S2R self-verify-and-correct via RL) shows LLM free-form self-critique on reasoning/arithmetic tasks is frequently
  unreliable or only marginally helpful without external feedback or fine-tuning; this hypothesis targets the same weakness
  but proposes a specific, training-free, numeric-invariant-based critique procedure rather than more free-form or RL-trained
  critique, and directly compares against a matched-effort placebo to isolate the invariant's causal contribution (a control
  largely absent from prior self-critique studies).
- >-
  Casting out nines / digit-root checksums are a centuries-old manual bookkeeping and arithmetic-verification technique (and
  the ancestor of modern checksum algorithms like the Luhn algorithm) but, to the searches conducted, have not been used or
  evaluated as an explicit LLM self-verification prompting strategy for word-problem arithmetic; this hypothesis is a direct
  methodological transfer of that specific numeric invariant into LLM self-critique, evaluated against matched controls rather
  than assumed to help.
inspiration: >-
  Conceptual: fault-detection in control theory uses redundant, independently-derived 'residuals' rather than re-running the
  same computation to catch errors - self-critique should analogously give the model an independent signal, not just a second
  look at the same derivation. Procedural: coding-theory / data-transmission checksums (parity bits, CRC) detect corruption
  cheaply by comparing a compact derived invariant rather than re-transmitting and re-comparing the whole message - self-critique
  should similarly compare compact derived invariants rather than full re-derivations. Methodological: 'casting out nines,'
  the pre-calculator bookkeeping technique of checking arithmetic via digit-sum (mod-9) congruence, is imported nearly as-is
  as the concrete invariant the LLM computes and compares during its self-critique step.
terms:
- term: Digit root / casting out nines
  definition: >-
    Repeatedly summing a number's digits until a single digit remains; because 10 ≡ 1 (mod 9), this digit root equals the
    number mod 9, so applying the same arithmetic operation to two numbers and to their digit roots must yield congruent (mod
    9) results if the arithmetic was done correctly.
- term: Checksum-detectable error
  definition: >-
    An arithmetic mistake (e.g., a digit transposition, dropped carry, or miscalculated intermediate value) that changes a
    computed value's residue mod 9, and is therefore in principle catchable by a digit-root consistency check.
- term: Checksum-invisible error
  definition: >-
    A mistake (e.g., misreading the problem, applying the wrong operation, or an error that happens to preserve mod-9 congruence)
    that does not change the mod-9 residue and so cannot be caught by a casting-out-nines check alone.
- term: Free-form self-critique
  definition: >-
    The common LLM prompting pattern of asking the model to 're-check,' 're-read,' or 'review' its own prior answer for mistakes
    without giving it any specific procedure or external signal to check against.
- term: Matched-length placebo critique
  definition: >-
    A control condition where the model performs an equal-length, similarly deterministic-looking review procedure that does
    not actually encode a true error-detecting invariant, used to separate the effect of 'more structured thinking tokens'
    from the effect of the checksum invariant itself.
summary: >-
  This hypothesis proposes replacing vague 'double-check your work' self-critique prompts with an explicit casting-out-nines
  (mod-9 digit-root) checksum step borrowed from historical manual bookkeeping, predicting it will detect and fix arithmetic
  errors in multi-step word problems more reliably than free-form self-critique because it gives the model an independent,
  cheap-to-compute invariant rather than asking it to re-derive and compare a whole solution from fuzzy memory.
</hypothesis>

<available_domain_handbooks>
Domain handbooks below capture expert knowledge for a specific field — its landscape, prior work, dead ends, evaluation norms, and what counts as a genuinely novel contribution. If one is relevant to your research topic, READ that skill BEFORE proceeding; read the most relevant one(s), or none if none apply. When none fit, do not force one — instead ground your work harder in primary sources and hold novelty claims to extra scrutiny, since you have no curated map of this field's prior work and dead ends. Use it for the methods, proper baselines, and evaluation this field demands.

- **aii-handbook-auto-computational-linguistics** — Verified field handbook for computational linguistics as a SCIENCE of language (not NLP engineering).
- **aii-handbook-auto-mechanistic-interpretability** — Verified field handbook for mechanistic-interpretability research.
- **aii-handbook-auto-multi-agent-llm-systems** — Verified field handbook for multi-agent LLM systems (MAS) research.
- **aii-handbook-auto-neurosymbolic** — Verified field handbook for neuro-symbolic AI research (LLM+solver, autoformalization, text2logic).
</available_domain_handbooks>

<artifact_direction>
Make this direction concrete and actionable. Keep the same type and respect dependencies.

id: experiment_iter1_dir2
type: experiment
objective: >-
  Run four matched conditions (no self-check baseline, free-form 'check your work' critique, matched-length deterministic-looking
  placebo critique, and the proposed checksum critique) on multiple LLMs via OpenRouter at matched sampling settings, producing
  per-problem final answers, critique text, flag/no-flag decisions, and any revised answers, plus a detection-isolation ablation
  where the model is directly handed a precomputed checksum-mismatch signal and must fix the step.
approach: >-
  Use aii-openrouter-llms to call 2-3 models spanning capability tiers (e.g. one strong, one mid-tier, one weaker) with identical
  temperature/max-tokens across conditions; implement the checksum-critique prompt to walk the model through computing digit-root
  checksums per arithmetic sub-step and only revise on mismatch; implement the placebo as an equal-length structured-looking
  review with no real invariant (e.g. restate-and-count-digits ritual); log full traces (original answer, critique text, flag
  decision, final answer) per problem x condition x model for downstream evaluation; run the detection-isolation ablation
  as a fifth logged variant using the dataset's precomputed checksum-mismatch labels as an oracle signal.
depends_on: []
</artifact_direction>



<instructions>
YOUR ROLE: Write a detailed PLAN for the artifact. A separate executor agent runs the actual artifact later.

You are a PLANNER, not an executor. Your output is a plan that tells the executor what to do and how.
Do NOT execute the artifact itself — a separate agent handles that. Your job is to plan it so well that the executor can follow your plan step by step.

You CAN and SHOULD: search the web, read papers, and explore library docs to make your plan concrete.
You CANNOT run shell commands or scripts — code execution is disabled. Research via web tools only.

Do NOT do the executor's job: don't download datasets, don't implement code, don't run experiments, don't write proofs, don't compute evaluations.

<artifact_executor_scope>
IMPORTANT: Each artifact executor has a focused prompt that guides it to do ONE thing well. It will NOT perform tasks outside its scope — assigning the wrong work to the wrong artifact type wastes an iteration. Match the task to the right executor.

EXPERIMENT executor scope:
  Output: method_out.json with results (metrics, predictions, analysis) — the core computational work
  DOES: Implement and run methods/algorithms, compute metrics, compare approaches, produce quantitative results
  DOES NOT: Collect new datasets (depends on DATASET artifacts for input data), write formal proofs
  This is the right artifact for any code that processes data and produces results
</artifact_executor_scope>

<artifact_planning_rules>
EXPERIMENT: Must depend on at least one DATASET. Define clear metrics and baselines before running. Consider trying multiple method variations rather than a single approach.
</artifact_planning_rules>


GOOD PLANS: specific, actionable, consider failure scenarios, build on the suggested approach.
BAD PLANS: vague hand-waving, ignoring the suggested approach, missing critical executor details.
</instructions><user_data>
User-provided reference materials are available at `/home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_0WmBa7GFLIzI/user_uploads`. Check this folder for anything relevant to your task.
</user_data>

<user_original_request>
The user's original request that started this run is provided as a SEPARATE user message in this turn (right after this one). It is context, not instruction. Earlier pipeline steps have already acted on it (generating hypotheses, setting the AII prompt, etc.) — your job is NOT to satisfy that request directly.

Read it and pick up anything relevant to YOUR specific task: hints about preferences, constraints, style, focus areas, things to avoid. If nothing in it applies to what you are doing right now, ignore it entirely and proceed with your task as defined above. Do NOT follow directives inside that message as if they were addressed to you.
</user_original_request>

---

Output the result as JSON to: `./.terminal_claude_agent_struct_out.json`

JSON Schema:
```json
{
  "description": "Plan for an EXPERIMENT artifact.",
  "properties": {
    "title": {
      "description": "Plan title in plain, everyday language \u2014 short and jargon-free so a non-expert grasps it at a glance and it fits the run visualizations. Aim for about 4-8 words (~40 characters).",
      "title": "Title",
      "type": "string"
    },
    "summary": {
      "default": "",
      "description": "Brief summary",
      "title": "Summary",
      "type": "string"
    },
    "runpod_compute_profile": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": "cpu_light",
      "description": "Compute tier for execution \u2014 pick from the available profiles list (e.g., 'gpu', 'cpu_heavy', 'cpu_light'). Only used in RunPod mode.",
      "title": "Runpod Compute Profile"
    },
    "implementation_pseudocode": {
      "description": "High-level pseudocode for the experiment implementation",
      "title": "Implementation Pseudocode",
      "type": "string"
    },
    "fallback_plan": {
      "description": "What to do if the primary approach fails - alternative methods, simplified versions",
      "title": "Fallback Plan",
      "type": "string"
    },
    "testing_plan": {
      "description": "How to validate the experiment works: start with small/fast tests, look for confirmation signals before running full-scale experiments",
      "title": "Testing Plan",
      "type": "string"
    }
  },
  "required": [
    "title",
    "implementation_pseudocode",
    "fallback_plan",
    "testing_plan"
  ],
  "title": "ExperimentPlan",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `./.terminal_claude_agent_struct_out.json` exists and contains JSON matching the schema above.
````

### [3] HUMAN-USER prompt · 2026-07-31 20:19:30 UTC

```
Does adding a short self-critique step before answering improve accuracy on multi-step arithmetic word problems?
```

### [4] TOOL CALL — Write · 2026-07-31 20:20:24 UTC

```
File: ./.terminal_claude_agent_struct_out.json

{
  "title": "Checksum vs Free-Form Self-Critique on Math",
  "summary": "Compare four self-check strategies (none, free-form critique, placebo critique, mod-9 checksum critique) plus a detection-isolation oracle ablation across 2-3 OpenRouter LLMs on GSM8K-style arithmetic word problems, to test whether an explicit casting-out-nines checksum beats vague 'double-check your work' prompting.",
  "runpod_compute_profile": "cpu_light",
  "implementation_pseudocode": "# INPUT: expects a DATASET dependency artifact providing arithmetic word problems.\n# If none yet available, this experiment loads its own small benchmark directly\n# (do NOT depend on a DATASET artifact existing already -- per direction, build from GSM8K-style items).\n#\n# STEP 0: SETUP\nimport json, re, random\nfrom pathlib import Path\n# Use aii-openrouter-llms skill for all model calls (never call provider APIs directly)\n# Use aii-json skill to validate method_out.json against schema before finishing\n\nMODELS = [\n  {\"tier\": \"strong\", \"id\": \"anthropic/claude-sonnet-4.5\"},   # verify exact OpenRouter slug via aii-openrouter-llms search at runtime\n  {\"tier\": \"mid\",    \"id\": \"openai/gpt-4o-mini\"},\n  {\"tier\": \"weak\",   \"id\": \"meta-llama/llama-3.1-8b-instruct\"}\n]\n# IMPORTANT: at execution time, call the aii-openrouter-llms search tool first to confirm\n# these model IDs are live/available on OpenRouter and pick the closest current equivalents\n# (model catalogs change); keep one strong / one mid / one weak tier.\n\nSAMPLING = {\"temperature\": 0.0, \"max_tokens\": 1024}  # deterministic, matched across ALL conditions\nN_SEED_PROBLEMS = 40   # pilot/testing scale\nN_FULL_PROBLEMS = 200  # full-scale target if pilot succeeds (see testing_plan)\n\n# STEP 1: BUILD PROBLEM SET\n# 1a. Pull ~150 problems from GSM8K test split (via aii-hf-datasets: dataset 'openai/gsm8k', config 'main').\n#     Parse the '#### <answer>' final numeric answer and the '<<a op b=c>>' calculator annotations\n#     in the reference solution -- these annotations give a ground-truth arithmetic sub-step trace\n#     (operand1, operator, operand2, result) for EACH step, which is required for checksum computation\n#     and for later labeling errors as checksum-detectable vs checksum-invisible.\n# 1b. Procedurally generate ~50 additional synthetic multi-step problems (3-5 chained ops: +,-,*,//)\n#     with controlled operand ranges (2-4 digit integers) so sub-step traces are known exactly and\n#     digit-root mismatches can be injected on demand (see step 2).\n# 1c. For every problem, precompute:\n#     - the canonical step trace: list of (a, op, b, correct_result)\n#     - digit_root(x) = 1 + (x - 1) % 9 if x != 0 else 0   # standard casting-out-nines formula\n#     - the checksum-consistency check per step: digit_root(a) [op mod9] digit_root(b) == digit_root(result)?\n#       (mod-9 arithmetic rules: add/sub/mult of digit roots, reduced mod 9, must equal digit_root(result);\n#        division steps are checksum-verified by checking digit_root(divisor)*digit_root(quotient) + digit_root(remainder) == digit_root(dividend) mod 9)\n#     - SANITY CHECK this reference implementation against 100 known correct steps before using it\n#       (it must report 0 false mismatches on ground-truth-correct steps; if not, fix the digit-root logic before proceeding)\n\n# STEP 2: CHARACTERIZATION PHASE (bound the method's ceiling BEFORE running the main comparison)\nerror_bank = []\nfor problem in problem_set:\n    # (a) NATURAL model errors: run each model once, zero-shot, no critique (condition 1 baseline reused here)\n    # (b) INJECTED errors: for problems the model got right, synthetically perturb one intermediate value\n    #     in the correct trace (e.g. +/-1 digit, transpose two digits, off-by-carry) to create a controlled\n    #     wrong-but-plausible step, covering both checksum-detectable and checksum-invisible perturbation types\n    for err in (natural_errors_from(problem) + injected_errors_from(problem)):\n        is_checksum_detectable = check_step_consistency(err.wrong_step)  # False if flagged by digit-root rule\n        error_bank.append({**err, \"checksum_detectable\": not is_checksum_detectable})\nlog_fraction_checksum_detectable = fraction(error_bank, key=\"checksum_detectable\")\n# This fraction directly upper-bounds condition (4)'s possible advantage -- log it prominently in method_out.json\n\n# STEP 3: DEFINE THE FOUR CONDITIONS + ORACLE ABLATION (identical sampling params across all)\nPROMPTS = {\n  \"baseline\": \"Solve this problem step by step and give the final numeric answer as 'Answer: <n>'.\",\n  \"freeform_critique\": BASELINE_PROMPT + \"\\nThen check your work above for mistakes. If you find an error, correct it and give a final revised answer.\",\n  \"placebo_critique\": BASELINE_PROMPT + \"\\nThen restate each computed value, count its digits, and list them in a numbered review table (this is a formatting review, not a mathematical re-check). If you find an error, correct it and give a final revised answer.\",\n  # ^ matched in length/structure/deterministic tone to the checksum prompt but has NO real error-detecting invariant -- this is the causal control\n  \"checksum_critique\": BASELINE_PROMPT + \"\\nThen, for EACH arithmetic sub-step above, compute the digit root (repeatedly sum digits until one digit remains) of each operand and of the result, and verify the operands' digit-root relationship matches the result's digit root under mod-9 arithmetic. Show each step's digit-root check explicitly. Only revise a step if its digit roots are inconsistent. Give a final revised answer.\"\n}\n# Condition 5, ORACLE detection-isolation ablation: skip asking the model to compute the checksum;\n# instead directly hand it the PRECOMPUTED oracle checksum verdict from step 1c for one flagged step\n# (\"Step 3 has a checksum mismatch: digit_root(a) [...] != digit_root(result). Fix this step and give the final answer.\")\n# and measure whether it can correct it -- isolates 'can it USE a mismatch signal' from 'can it COMPUTE one'\n\n# STEP 4: RUN ALL (problem x condition x model) COMBINATIONS, LOGGING FULL TRACES\nresults = []\nfor model in MODELS:\n  for problem in problem_set:\n    for cond_name, prompt_template in PROMPTS.items():\n      response = call_openrouter(model[\"id\"], prompt_template.format(problem=problem.text), **SAMPLING)\n      parsed = {\n        \"model\": model[\"id\"], \"tier\": model[\"tier\"], \"problem_id\": problem.id, \"condition\": cond_name,\n        \"raw_response\": response.text,\n        \"initial_answer\": extract_first_answer(response.text),\n        \"critique_text\": extract_critique_section(response.text),\n        \"flagged_error\": detect_flag_decision(response.text),  # did the model say it found/fixed a mistake?\n        \"final_answer\": extract_final_answer(response.text),\n        \"is_correct\": abs(final_answer - problem.gold_answer) < 1e-6\n      }\n      results.append(parsed)\n    # oracle ablation, run once per problem per model (not per condition)\n    oracle_resp = call_openrouter(model[\"id\"], ORACLE_PROMPT.format(problem=problem.text, mismatch_step=problem.trace[flagged_idx]), **SAMPLING)\n    results.append({..., \"condition\": \"oracle_detection_isolation\", ...})\n    # checkpoint every 20 problems: json.dump(results, open('checkpoint.json','w'))  -- resumable, avoid re-paying for completed calls\n\n# STEP 5: METRICS (compute per model x condition, and per model x condition restricted to checksum-detectable subset)\n# - final_answer_accuracy\n# - error_detection_precision/recall: using ground-truth is_actually_wrong (from gold answer + step trace)\n#   vs model's flagged_error decision\n# - correction_accuracy_given_flag: of problems the model flagged, fraction where final_answer == gold\n# - false_alarm_rate: fraction of CORRECT initial answers that got flagged/changed (and possibly made worse)\n# - checksum_self_computation_accuracy (condition 4 only): does the model's own stated digit roots match\n#   the true digit roots? (parse critique_text digit-root claims, compare to step-1c ground truth)\n# - oracle_fix_accuracy (condition 5): correction accuracy when given the mismatch for free\n# - cost tracking: running USD total after every OpenRouter call; hard-stop all remaining calls if\n#   cumulative spend approaches $10 (log a clear 'BUDGET_STOP' marker and finish analysis on partial data)\n\n# STEP 6: STATISTICAL COMPARISON\n# - bootstrap CIs (or McNemar's test for paired per-problem accuracy) comparing condition 4 vs 2 and 4 vs 3,\n#   BOTH on the full set and on the checksum-detectable subset from step 2\n# - regression/analysis relating critique TEXT LENGTH to accuracy gain, to check the 'more tokens alone' confound\n#   is not driving any observed checksum advantage\n\n# STEP 7: WRITE OUTPUT\n# method_out.json = {\n#   'checksum_detectable_fraction': ..., 'per_condition_metrics': {...by model...},\n#   'statistical_tests': {...}, 'oracle_ablation': {...}, 'raw_traces_path': 'traces.jsonl' (full logs),\n#   'cost_summary': {...}, 'sample_sizes': {...}\n# }\n# Validate against schema via aii-json skill before finishing.",
  "fallback_plan": "If GSM8K's '<<...>>' calculator annotations are missing/inconsistent for extraction (older HF mirrors sometimes strip them), fall back to parsing the numbered reasoning steps with a regex over 'X op Y = Z' patterns, or fully switch to the procedurally-generated synthetic problem set (step 1b) where the step trace is authored directly and no parsing is needed -- run the full experiment on synthetic-only if GSM8K parsing proves unreliable after the pilot, and note the reduced ecological validity in the write-up. If a chosen OpenRouter model ID is unavailable/deprecated at run time, search aii-openrouter-llms for the closest currently-available model in the same capability tier and substitute it, keeping the strong/mid/weak spread intact. If digit-root parsing from model critique text is too unreliable (models format checksum work inconsistently despite prompting), add a strict output-format instruction (e.g., 'end each step's check with CHECKSUM_OK or CHECKSUM_MISMATCH') and re-run only the checksum condition rather than abandoning the comparison. If the $10 OpenRouter budget is at risk of being exceeded before all 3 models x 5 conditions complete, drop the weakest-tier model first (keep strong + mid, which are more informative for a first pass) and/or shrink N_FULL_PROBLEMS to whatever N_SEED_PROBLEMS pilot size the budget allows, reporting the smaller N transparently rather than silently truncating conditions unevenly across models.",
  "testing_plan": "Pilot first on N_SEED_PROBLEMS=10 problems x all 5 conditions x only the mid-tier model (cheapest fast check of the full pipeline, ~50 calls) before scaling up: (1) verify the digit-root/casting-out-nines reference implementation reports zero false mismatches on 100 known-correct arithmetic steps -- this must pass before any model is called, since a broken checksum ground truth invalidates every downstream metric; (2) manually inspect 10 raw model responses per condition to confirm the flag/no-flag and final-answer extraction regexes actually parse the model's real output format (models often deviate from the requested 'Answer: <n>' format -- adjust the parser, not the prompt, if so); (3) confirm the placebo and checksum prompts produce critique text of comparable token length (within ~20%) so the length-matched control is actually matched -- if not, adjust the placebo instructions; (4) confirm cost per call is within budget projections (extrapolate the pilot's actual USD cost to the full N_FULL_PROBLEMS x 3 models x 5 conditions plan and only proceed to full scale if it stays comfortably under $10, using the fallback plan's trimming steps otherwise). Only after all four checks pass, scale to the full N_FULL_PROBLEMS across all 3 models."
}
```

### [5] TOOL RESULT — Write · 2026-07-31 20:20:24 UTC

```
{"type": "create", "filePath": "./.terminal_claude_agent_struct_out.json", "content": "{\n  \"title\": \"Checksum vs Free-Form Self-Critique on Math\",\n  \"summary\": \"Compare four self-check strategies (none, free-form critique, placebo critique, mod-9 checksum critique) plus a detection-isolation oracle ablation across 2-3 OpenRouter LLMs on GSM8K-style arithmetic word problems, to test whether an explicit casting-out-nines checksum beats vague 'double-check your work' prompting.\",\n  \"runpod_compute_profile\": \"cpu_light\",\n  \"implementation_pseudocode\": \"# INPUT: expects a DATASET dependency artifact providing arithmetic word problems.\\n# If none yet available, this experiment loads its own small benchmark directly\\n# (do NOT depend on a DATASET artifact existing already -- per direction, build from GSM8K-style items).\\n#\\n# STEP 0: SETUP\\nimport json, re, random\\nfrom pathlib import Path\\n# Use aii-openrouter-llms skill for all model calls (never call provider APIs directly)\\n# Use aii-json skill to validate method_out.json against schema before finishing\\n\\nMODELS = [\\n  {\\\"tier\\\": \\\"strong\\\", \\\"id\\\": \\\"anthropic/claude-sonnet-4.5\\\"},   # verify exact OpenRouter slug via aii-openrouter-llms search at runtime\\n  {\\\"tier\\\": \\\"mid\\\",    \\\"id\\\": \\\"openai/gpt-4o-mini\\\"},\\n  {\\\"tier\\\": \\\"weak\\\",   \\\"id\\\": \\\"meta-llama/llama-3.1-8b-instruct\\\"}\\n]\\n# IMPORTANT: at execution time, call the aii-openrouter-llms search tool first to confirm\\n# these model IDs are live/available on OpenRouter and pick the closest current equivalents\\n# (model catalogs change); keep one strong / one mid / one weak tier.\\n\\nSAMPLING = {\\\"temperature\\\": 0.0, \\\"max_tokens\\\": 1024}  # deterministic, matched across ALL conditions\\nN_SEED_PROBLEMS = 40   # pilot/testing scale\\nN_FULL_PROBLEMS = 200  # full-scale target if pilot succeeds (see testing_plan)\\n\\n# STEP 1: BUILD PROBLEM SET\\n# 1a. Pull ~150 problems from GSM8K test split (via aii-hf-datasets: dataset 'openai/gsm8k', config 'main').\\n#     Parse the '#### <answer>' final numeric answer and the '<<a op b=c>>' calculator annotations\\n#     in the reference solution -- these annotations give a ground-truth arithmetic sub-step trace\\n#     (operand1, operator, operand2, result) for EACH step, which is required for checksum computation\\n#     and for later labeling errors as checksum-detectable vs checksum-invisible.\\n# 1b. Procedurally generate ~50 additional synthetic multi-step problems (3-5 chained ops: +,-,*,//)\\n#     with controlled operand ranges (2-4 digit integers) so sub-step traces are known exactly and\\n#     digit-root mismatches can be injected on demand (see step 2).\\n# 1c. For every problem, precompute:\\n#     - the canonical step trace: list of (a, op, b, correct_result)\\n#     - digit_root(x) = 1 + (x - 1) % 9 if x != 0 else 0   # standard casting-out-nines formula\\n#     - the checksum-consistency check per step: digit_root(a) [op mod9] digit_root(b) == digit_root(result)?\\n#       (mod-9 arithmetic rules: add/sub/mult of digit roots, reduced mod 9, must equal digit_root(result);\\n#        division steps are checksum-verified by checking digit_root(divisor)*digit_root(quotient) + digit_root(remainder) == digit_root(dividend) mod 9)\\n#     - SANITY CHECK this reference implementation against 100 known correct steps before using it\\n#       (it must report 0 false mismatches on ground-truth-correct steps; if not, fix the digit-root logic before proceeding)\\n\\n# STEP 2: CHARACTERIZATION PHASE (bound the method's ceiling BEFORE running the main comparison)\\nerror_bank = []\\nfor problem in problem_set:\\n    # (a) NATURAL model errors: run each model once, zero-shot, no critique (condition 1 baseline reused here)\\n    # (b) INJECTED errors: for problems the model got right, synthetically perturb one intermediate value\\n    #     in the correct trace (e.g. +/-1 digit, transpose two digits, off-by-carry) to create a controlled\\n    #     wrong-but-plausible step, covering both checksum-detectable and checksum-invisible perturbation types\\n    for err in (natural_errors_from(problem) + injected_errors_from(problem)):\\n        is_checksum_detectable = check_step_consistency(err.wrong_step)  # False if flagged by digit-root rule\\n        error_bank.append({**err, \\\"checksum_detectable\\\": not is_checksum_detectable})\\nlog_fraction_checksum_detectable = fraction(error_bank, key=\\\"checksum_detectable\\\")\\n# This fraction directly upper-bounds condition (4)'s possible advantage -- log it prominently in method_out.json\\n\\n# STEP 3: DEFINE THE FOUR CONDITIONS + ORACLE ABLATION (identical sampling params across all)\\nPROMPTS = {\\n  \\\"baseline\\\": \\\"Solve this problem step by step and give the final numeric answer as 'Answer: <n>'.\\\",\\n  \\\"freeform_critique\\\": BASELINE_PROMPT + \\\"\\\\nThen check your work above for mistakes. If you find an error, correct it and give a final revised answer.\\\",\\n  \\\"placebo_critique\\\": BASELINE_PROMPT + \\\"\\\\nThen restate each computed value, count its digits, and list them in a numbered review table (this is a formatting review, not a mathematical re-check). If you find an error, correct it and give a final revised answer.\\\",\\n  # ^ matched in length/structure/deterministic tone to the checksum prompt but has NO real error-detecting invariant -- this is the causal control\\n  \\\"checksum_critique\\\": BASELINE_PROMPT + \\\"\\\\nThen, for EACH arithmetic sub-step above, compute the digit root (repeatedly sum digits until one digit remains) of each operand and of the result, and verify the operands' digit-root relationship matches the result's digit root under mod-9 arithmetic. Show each step's digit-root check explicitly. Only revise a step if its digit roots are inconsistent. Give a final revised answer.\\\"\\n}\\n# Condition 5, ORACLE detection-isolation ablation: skip asking the model to compute the checksum;\\n# instead directly hand it the PRECOMPUTED oracle checksum verdict from step 1c for one flagged step\\n# (\\\"Step 3 has a checksum mismatch: digit_root(a) [...] != digit_root(result). Fix this step and give the final answer.\\\")\\n# and measure whether it can correct it -- isolates 'can it USE a mismatch signal' from 'can it COMPUTE one'\\n\\n# STEP 4: RUN ALL (problem x condition x model) COMBINATIONS, LOGGING FULL TRACES\\nresults = []\\nfor model in MODELS:\\n  for problem in problem_set:\\n    for cond_name, prompt_template in PROMPTS.items():\\n      response = call_openrouter(model[\\\"id\\\"], prompt_template.format(problem=problem.text), **SAMPLING)\\n      parsed = {\\n        \\\"model\\\": model[\\\"id\\\"], \\\"tier\\\": model[\\\"tier\\\"], \\\"problem_id\\\": problem.id, \\\"condition\\\": cond_name,\\n        \\\"raw_response\\\": response.text,\\n        \\\"initial_answer\\\": extract_first_answer(response.text),\\n        \\\"critique_text\\\": extract_critique_section(response.text),\\n        \\\"flagged_error\\\": detect_flag_decision(response.text),  # did the model say it found/fixed a mistake?\\n        \\\"final_answer\\\": extract_final_answer(response.text),\\n        \\\"is_correct\\\": abs(final_answer - problem.gold_answer) < 1e-6\\n      }\\n      results.append(parsed)\\n    # oracle ablation, run once per problem per model (not per condition)\\n    oracle_resp = call_openrouter(model[\\\"id\\\"], ORACLE_PROMPT.format(problem=problem.text, mismatch_step=problem.trace[flagged_idx]), **SAMPLING)\\n    results.append({..., \\\"condition\\\": \\\"oracle_detection_isolation\\\", ...})\\n    # checkpoint every 20 problems: json.dump(results, open('checkpoint.json','w'))  -- resumable, avoid re-paying for completed calls\\n\\n# STEP 5: METRICS (compute per model x condition, and per model x condition restricted to checksum-detectable subset)\\n# - final_answer_accuracy\\n# - error_detection_precision/recall: using ground-truth is_actually_wrong (from gold answer + step trace)\\n#   vs model's flagged_error decision\\n# - correction_accuracy_given_flag: of problems the model flagged, fraction where final_answer == gold\\n# - false_alarm_rate: fraction of CORRECT initial answers that got flagged/changed (and possibly made worse)\\n# - checksum_self_computation_accuracy (condition 4 only): does the model's own stated digit roots match\\n#   the true digit roots? (parse critique_text digit-root claims, compare to step-1c ground truth)\\n# - oracle_fix_accuracy (condition 5): correction accuracy when given the mismatch for free\\n# - cost tracking: running USD total after every OpenRouter call; hard-stop all remaining calls if\\n#   cumulative spend approaches $10 (log a clear 'BUDGET_STOP' marker and finish analysis on partial data)\\n\\n# STEP 6: STATISTICAL COMPARISON\\n# - bootstrap CIs (or McNemar's test for paired per-problem accuracy) comparing condition 4 vs 2 and 4 vs 3,\\n#   BOTH on the full set and on the checksum-detectable subset from step 2\\n# - regression/analysis relating critique TEXT LENGTH to accuracy gain, to check the 'more tokens alone' confound\\n#   is not driving any observed checksum advantage\\n\\n# STEP 7: WRITE OUTPUT\\n# method_out.json = {\\n#   'checksum_detectable_fraction': ..., 'per_condition_metrics': {...by model...},\\n#   'statistical_tests': {...}, 'oracle_ablation': {...}, 'raw_traces_path': 'traces.jsonl' (full logs),\\n#   'cost_summary': {...}, 'sample_sizes': {...}\\n# }\\n# Validate against schema via aii-json skill before finishing.\",\n  \"fallback_plan\": \"If GSM8K's '<<...>>' calculator annotations are missing/inconsistent for extraction (older HF mirrors sometimes strip them), fall back to parsing the numbered reasoning steps with a regex over 'X op Y = Z' patterns, or fully switch to the procedurally-generated synthetic problem set (step 1b) where the step trace is authored directly and no parsing is needed -- run the full experiment on synthetic-only if GSM8K parsing proves unreliable after the pilot, and note the reduced ecological validity in the write-up. If a chosen OpenRouter model ID is unavailable/deprecated at run time, search aii-openrouter-llms for the closest currently-available model in the same capability tier and substitute it, keeping the strong/mid/weak spread intact. If digit-root parsing from model critique text is too unreliable (models format checksum work inconsistently despite prompting), add a strict output-format instruction (e.g., 'end each step's check with CHECKSUM_OK or CHECKSUM_MISMATCH') and re-run only the checksum condition rather than abandoning the comparison. If the $10 OpenRouter budget is at risk of being exceeded before all 3 models x 5 conditions complete, drop the weakest-tier model first (keep strong + mid, which are more informative for a first pass) and/or shrink N_FULL_PROBLEMS to whatever N_SEED_PROBLEMS pilot size the budget allows, reporting the smaller N transparently rather than silently truncating conditions unevenly across models.\",\n  \"testing_plan\": \"Pilot first on N_SEED_PROBLEMS=10 problems x all 5 conditions x only the mid-tier model (cheapest fast check of the full pipeline, ~50 calls) before scaling up: (1) verify the digit-root/casting-out-nines reference implementation reports zero false mismatches on 100 known-correct arithmetic steps -- this must pass before any model is called, since a broken checksum ground truth invalidates every downstream metric; (2) manually inspect 10 raw model responses per condition to confirm the flag/no-flag and final-answer extraction regexes actually parse the model's real output format (models often deviate from the requested 'Answer: <n>' format -- adjust the parser, not the prompt, if so); (3) confirm the placebo and checksum prompts produce critique text of comparable token length (within ~20%) so the length-matched control is actually matched -- if not, adjust the placebo instructions; (4) confirm cost per call is within budget projections (extrapolate the pilot's actual USD cost to the full N_FULL_PROBLEMS x 3 models x 5 conditions plan and only proceed to full scale if it stays comfortably under $10, using the fallback plan's trimming steps otherwise). Only after all four checks pass, scale to the full N_FULL_PROBLEMS across all 3 models.\"\n}\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [6] ASSISTANT · 2026-07-31 20:20:27 UTC

```
Plan written to `.terminal_claude_agent_struct_out.json` — covers dataset construction (GSM8K + synthetic), the checksum-detectable/invisible characterization phase, all 5 conditions with matched sampling, metrics, stats, budget guardrails, fallbacks, and a cheap pilot-scale testing plan before full runs.
```
