# gen_paper_text — test_idea

> Phase: `invention_loop` · round 1 · `gen_paper_text`
> Run: `run_0WmBa7GFLIzI` — Checksum Self-Critique Helps Weak Arithmetic, Hurts Weak Models
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `gen_paper_text` (terminal_claude_agent, claude-sonnet-5)

### [1] CONFIG · 2026-07-31 20:42:38 UTC

```
model: claude-sonnet-5 | effort: low | permission: bypassPermissions | cwd: /home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_0WmBa7GFLIzI/3_invention_loop/iter_1/gen_paper_text/gen_paper_text
```

### [2] SYSTEM-USER prompt · 2026-07-31 20:42:44 UTC

````
<ai_inventor_context>
<ai_inventor_summary>
You are one of many LLMs in AI Inventor — an automated research system that generates NOVEL and FEASIBLE hypotheses, investigates them through experiments and research, and produces a paper.

Your output feeds other LLMs downstream. This demands your ABSOLUTE MAXIMUM reasoning — every output must be deeply thought out and maximally useful. Surface-level responses waste downstream computation.
</ai_inventor_summary>

<your_role>
YOU ARE: A research paper writer (Step 3.4: GEN_PAPER_TEXT in the invention loop)

You received the hypothesis, all artifacts, the previous paper draft (if any), and reviewer feedback.
Write a complete paper draft with figure placeholders.

Publication-quality paper → strong contribution. Weak paper → wasted iteration.
</your_role>
</ai_inventor_context>

<research_methodology>
Write like a researcher drafting a paper, not a chatbot summarizing bullet points.

- Structure as a paper would: research question → methodology → results → analysis → limitations. Not a list of "we did X, then Y."
- Ground every claim in specific artifacts and specific numbers. "Results show improvement" is empty — state effect sizes, baselines, and conditions.
- Be honest about what worked, what didn't, and why. Don't spin failures as "future work."
- The paper's headline contribution should be a positive or surprising finding. Negative results are valuable context but should not be the primary narrative — lead with what works.
- Address reviewer feedback from previous iterations explicitly — show you've thought about each critique.
</research_methodology>

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

<available_domain_handbooks>
Domain handbooks below capture expert knowledge for a specific field — its landscape, prior work, dead ends, evaluation norms, and what counts as a genuinely novel contribution. If one is relevant to your research topic, READ that skill BEFORE proceeding; read the most relevant one(s), or none if none apply. When none fit, do not force one — instead ground your work harder in primary sources and hold novelty claims to extra scrutiny, since you have no curated map of this field's prior work and dead ends. Use it for related-work positioning and how this field frames a genuinely novel contribution.

- **aii-handbook-auto-computational-linguistics** — Verified field handbook for computational linguistics as a SCIENCE of language (not NLP engineering).
- **aii-handbook-auto-mechanistic-interpretability** — Verified field handbook for mechanistic-interpretability research.
- **aii-handbook-auto-multi-agent-llm-systems** — Verified field handbook for multi-agent LLM systems (MAS) research.
- **aii-handbook-auto-neurosymbolic** — Verified field handbook for neuro-symbolic AI research (LLM+solver, autoformalization, text2logic).
</available_domain_handbooks>
<hypothesis>
The research hypothesis.

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

<all_artifacts>
FULL EVIDENCE BASE: All 2 research artifacts across all iterations.

--- Item 1 ---
id: art_UafZp2AqR5at
type: dataset
title: Arithmetic Problems with Checksum Error Labels
summary: >-
  arithmetic_checksum_dataset (full_data_out.json, 1935 rows, 2.9MB, exp_sel_data_out.json-schema-valid) combines two complementary
  sources: 200 real GSM8K word problems (openai/gsm8k, main config, train+test) whose reasoning was auto-parsed via regex
  over the <<operand op operand=result>> calculator annotations into explicit step traces (operand_1, operand_2, operation,
  result, depends_on_step), filtered to chain_length 2-6 and cross-checked so the final trace step matches the stated '####
  answer'; plus 200 procedurally generated synthetic word problems (5 templates: shopping, recipe-scaling, distance-rate-time,
  unit-conversion, inventory-accounting) with traces emitted directly by the generator, guaranteeing clean coverage of long
  chains (5-6 steps) and large numbers (>=100) that GSM8K under-represents. Both sources are stratified across a 5(chain_length)x2(numeric_range)
  grid, 20 items per cell. On top of these 400 base items (metadata_row_type=base_item, input=problem text, output=final answer,
  metadata_trace=full step list), a deterministic error-injection layer adds up to 4 corrupted variants per base item (metadata_row_type=error_variant):
  digit_transposition, dropped_carry, sign_flip, wrong_operand_substitution. Each corruption is injected at one step and propagated
  through every downstream step that depends on it (recomputed via exact arithmetic, not estimated), yielding an internally
  consistent corrupted trace and a corrupted_final_answer; the row's input is the corrupted trace rendered as text and output
  is 'checksum_detectable|correct_final_answer=X' or 'checksum_invisible|correct_final_answer=X' depending on whether the
  mod-9 digit residue of the corrupted final answer differs from (detectable) or matches (invisible) the correct final answer's
  residue. An error type is skipped per item (logged, not force-fit) when it cannot be structurally applied (e.g. sign_flip
  needs a +/- step) or when the corruption doesn't propagate to the final answer (orphan sub-calculation) or has no reachable
  trace; 1935 total rows (400 base + 1535 variants; skip rate ~8%) with an 80/20 metadata_fold train/test split. All arithmetic
  (base traces and every corrupted+propagated trace) was independently re-derived and verified with zero inconsistencies across
  all 1935 rows via a standalone regex-based checker (verify.py) that recomputes every step from the rendered text and cross-checks
  against metadata. Suitable for downstream self-critique experiments testing whether a model's checksum-style spot-check
  catches injected arithmetic errors, and specifically whether it fails on checksum_invisible errors that a naive residue
  check would miss. pyproject.toml pins the sole third-party dependency (loguru==0.7.3); data.py is deterministic (fixed RNG
  seed) and reproducible via `uv run data.py`, reading raw openai/gsm8k JSON from temp/datasets/ (excluded from publish, re-downloadable
  via the aii-hf-datasets skill).
workspace_path: >-
  /home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_0WmBa7GFLIzI/3_invention_loop/iter_1/gen_art/gen_art_dataset_1
out_expected_files:
- data.py
- full_data_out.json
- preview_data_out.json
- mini_data_out.json

--- Item 2 ---
id: art_VCF3BbfSo_RV
type: evaluation
title: Does a checksum self-check beat plain critique?
summary: >-
  Evaluates the gen_art_experiment_1 output comparing four self-check strategies (none/baseline, free-form critique, length-matched
  placebo critique, mod-9 digit-root checksum critique) plus an oracle detection-isolation ablation, across LLMs (anthropic/claude-haiku-4.5
  and openai/gpt-4o-mini so far; the underlying experiment continues running toward a third model and its full 200-problem
  budget), on synthetic multi-step arithmetic word problems with known ground-truth step traces. Predictions are loaded directly
  from the experiment's checkpoint.json/method_out.json (no re-execution of the method). eval.py reproduces the experiment's
  deterministic synthetic-problem generation and error-injection seeds bit-for-bit (verified to match the experiment's own
  reported checksum_detectable_fraction) to recover a per-problem checksum-detectable ground-truth label that the experiment
  computed internally but did not export per example, enabling checksum-detectable vs checksum-invisible subset splits. It
  computes: (1) final-answer accuracy per model x condition with Wilson 95% CIs, split overall/detectable/invisible; (2) a
  detection precision/recall/F1 confusion matrix built from flagged_error vs whether the model's own initial answer actually
  differed from ground truth (the real available proxy for 'did the model actually make a mistake', since the experiment solves
  the original correct problem rather than an error-injected variant); (3) correction accuracy given a flag, per condition;
  (4) an ablation comparing the oracle arm's fix-rate (given an externally supplied checksum-mismatch signal) against the
  checksum condition's own correction accuracy, to separate 'can compute a checksum' from 'can use one'; (5) paired McNemar
  tests (exact binomial) and 10,000-resample bootstrap CIs on the checksum-detectable subset for checksum-vs-freeform and
  checksum-vs-placebo, with Holm-Bonferroni correction across the full family of per-model x per-pair comparisons and percentage-point
  effect sizes reported alongside p-values; (6) a prompt-length confound check via a dependency-free logistic regression of
  correctness on condition dummies plus standardized response length, plus mean/median critique length per condition and the
  actual placebo:checksum length ratio; (7) an LLM-judge checksum self-computation audit (via OpenRouter, judge model anthropic/claude-haiku-4.5,
  asked to independently recompute each digit-root/mod-9 check before giving a final verdict line -- an earlier weaker/single-token
  judge configuration was caught producing implausible near-100% error rates on a manual spot-check of a fully-correct transcript
  and was replaced) over a stratified sample of checksum-condition traces per model, with precision/recall recomputed after
  excluding traces whose checksum arithmetic was itself found incorrect; and (8) the checksum-invisible subset reported for
  every condition as a built-in negative control. An independent re-parse of every raw_response (separate regex pass, not
  trusting the experiment's own parser) found zero final-answer disagreements, corroborating parser integrity. All rich per-metric
  detail lives under metadata.detailed_metrics; metrics_agg holds ~65 flattened scalar summary values (accuracies, precision/recall/F1,
  oracle fix rates, Holm-adjusted p-values, effect sizes, length ratios, checksum-computation error rates) as required by
  the exp_eval_sol_out schema, and per-example predict_/eval_ fields cover every (model, condition) pairing per problem_id.
  Downstream paper-writing steps should treat this evaluation as covering the models and problem count present in eval_out.json's
  metadata.experiment_metadata_snapshot at generation time, since the underlying experiment was still executing toward its
  full scope when this evaluation ran and can be re-run via eval.py against a more complete method_out.json if needed.
workspace_path: >-
  /home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_0WmBa7GFLIzI/3_invention_loop/iter_1/gen_art/gen_art_evaluation_1
out_expected_files:
- eval.py
- full_eval_out.json
- mini_eval_out.json
- preview_eval_out.json
</all_artifacts>

<new_artifacts_this_iteration>
NEW THIS ITERATION: These 2 artifacts were created to address the reviewer
feedback. Their findings should be the primary basis for your revisions.

summary: >-
  arithmetic_checksum_dataset (full_data_out.json, 1935 rows, 2.9MB, exp_sel_data_out.json-schema-valid) combines two complementary
  sources: 200 real GSM8K word problems (openai/gsm8k, main config, train+test) whose reasoning was auto-parsed via regex
  over the <<operand op operand=result>> calculator annotations into explicit step traces (operand_1, operand_2, operation,
  result, depends_on_step), filtered to chain_length 2-6 and cross-checked so the final trace step matches the stated '####
  answer'; plus 200 procedurally generated synthetic word problems (5 templates: shopping, recipe-scaling, distance-rate-time,
  unit-conversion, inventory-accounting) with traces emitted directly by the generator, guaranteeing clean coverage of long
  chains (5-6 steps) and large numbers (>=100) that GSM8K under-represents. Both sources are stratified across a 5(chain_length)x2(numeric_range)
  grid, 20 items per cell. On top of these 400 base items (metadata_row_type=base_item, input=problem text, output=final answer,
  metadata_trace=full step list), a deterministic error-injection layer adds up to 4 corrupted variants per base item (metadata_row_type=error_variant):
  digit_transposition, dropped_carry, sign_flip, wrong_operand_substitution. Each corruption is injected at one step and propagated
  through every downstream step that depends on it (recomputed via exact arithmetic, not estimated), yielding an internally
  consistent corrupted trace and a corrupted_final_answer; the row's input is the corrupted trace rendered as text and output
  is 'checksum_detectable|correct_final_answer=X' or 'checksum_invisible|correct_final_answer=X' depending on whether the
  mod-9 digit residue of the corrupted final answer differs from (detectable) or matches (invisible) the correct final answer's
  residue. An error type is skipped per item (logged, not force-fit) when it cannot be structurally applied (e.g. sign_flip
  needs a +/- step) or when the corruption doesn't propagate to the final answer (orphan sub-calculation) or has no reachable
  trace; 1935 total rows (400 base + 1535 variants; skip rate ~8%) with an 80/20 metadata_fold train/test split. All arithmetic
  (base traces and every corrupted+propagated trace) was independently re-derived and verified with zero inconsistencies across
  all 1935 rows via a standalone regex-based checker (verify.py) that recomputes every step from the rendered text and cross-checks
  against metadata. Suitable for downstream self-critique experiments testing whether a model's checksum-style spot-check
  catches injected arithmetic errors, and specifically whether it fails on checksum_invisible errors that a naive residue
  check would miss. pyproject.toml pins the sole third-party dependency (loguru==0.7.3); data.py is deterministic (fixed RNG
  seed) and reproducible via `uv run data.py`, reading raw openai/gsm8k JSON from temp/datasets/ (excluded from publish, re-downloadable
  via the aii-hf-datasets skill).
id: art_UafZp2AqR5at
title: Arithmetic Problems with Checksum Error Labels
type: dataset

summary: >-
  Evaluates the gen_art_experiment_1 output comparing four self-check strategies (none/baseline, free-form critique, length-matched
  placebo critique, mod-9 digit-root checksum critique) plus an oracle detection-isolation ablation, across LLMs (anthropic/claude-haiku-4.5
  and openai/gpt-4o-mini so far; the underlying experiment continues running toward a third model and its full 200-problem
  budget), on synthetic multi-step arithmetic word problems with known ground-truth step traces. Predictions are loaded directly
  from the experiment's checkpoint.json/method_out.json (no re-execution of the method). eval.py reproduces the experiment's
  deterministic synthetic-problem generation and error-injection seeds bit-for-bit (verified to match the experiment's own
  reported checksum_detectable_fraction) to recover a per-problem checksum-detectable ground-truth label that the experiment
  computed internally but did not export per example, enabling checksum-detectable vs checksum-invisible subset splits. It
  computes: (1) final-answer accuracy per model x condition with Wilson 95% CIs, split overall/detectable/invisible; (2) a
  detection precision/recall/F1 confusion matrix built from flagged_error vs whether the model's own initial answer actually
  differed from ground truth (the real available proxy for 'did the model actually make a mistake', since the experiment solves
  the original correct problem rather than an error-injected variant); (3) correction accuracy given a flag, per condition;
  (4) an ablation comparing the oracle arm's fix-rate (given an externally supplied checksum-mismatch signal) against the
  checksum condition's own correction accuracy, to separate 'can compute a checksum' from 'can use one'; (5) paired McNemar
  tests (exact binomial) and 10,000-resample bootstrap CIs on the checksum-detectable subset for checksum-vs-freeform and
  checksum-vs-placebo, with Holm-Bonferroni correction across the full family of per-model x per-pair comparisons and percentage-point
  effect sizes reported alongside p-values; (6) a prompt-length confound check via a dependency-free logistic regression of
  correctness on condition dummies plus standardized response length, plus mean/median critique length per condition and the
  actual placebo:checksum length ratio; (7) an LLM-judge checksum self-computation audit (via OpenRouter, judge model anthropic/claude-haiku-4.5,
  asked to independently recompute each digit-root/mod-9 check before giving a final verdict line -- an earlier weaker/single-token
  judge configuration was caught producing implausible near-100% error rates on a manual spot-check of a fully-correct transcript
  and was replaced) over a stratified sample of checksum-condition traces per model, with precision/recall recomputed after
  excluding traces whose checksum arithmetic was itself found incorrect; and (8) the checksum-invisible subset reported for
  every condition as a built-in negative control. An independent re-parse of every raw_response (separate regex pass, not
  trusting the experiment's own parser) found zero final-answer disagreements, corroborating parser integrity. All rich per-metric
  detail lives under metadata.detailed_metrics; metrics_agg holds ~65 flattened scalar summary values (accuracies, precision/recall/F1,
  oracle fix rates, Holm-adjusted p-values, effect sizes, length ratios, checksum-computation error rates) as required by
  the exp_eval_sol_out schema, and per-example predict_/eval_ fields cover every (model, condition) pairing per problem_id.
  Downstream paper-writing steps should treat this evaluation as covering the models and problem count present in eval_out.json's
  metadata.experiment_metadata_snapshot at generation time, since the underlying experiment was still executing toward its
  full scope when this evaluation ran and can be re-run via eval.py against a more complete method_out.json if needed.
id: art_VCF3BbfSo_RV
title: Does a checksum self-check beat plain critique?
type: evaluation
</new_artifacts_this_iteration>

<data_files>
Data files come in three sizes:
- preview_*_out.json — READ THIS to inspect the data structure
- mini_*_out.json (~3 examples) — use for prototyping/testing
- full_*_out.json (complete) — use for the final production run. NEVER open it directly (too large to read into context). Instead, extract values programmatically with shell commands (e.g. grep) or a Python script (use aii-long-running-tasks skill for scripts).
</data_files>

<task>
Write a research paper draft with LaTeX-ready text, BibTeX citations, and figure placeholders.

This is the FIRST paper draft. Write a complete research paper from scratch based on the hypothesis and all available artifacts.
</task>

<figure_instructions>
FIGURE FORMAT: Use [FIGURE:fig_id] markers in paper_text to indicate where each figure goes.
Then provide the full figure specs in the separate `figures` structured output array.
Each figure in the array must have an `id` matching a marker in the text. Set the `aspect_ratio`
field per figure: 21:9 for architecture / pipeline / flow-chart diagrams (the hero figure should
be one of these — place its marker near the END of the Introduction so it floats to the top of
page 2), 16:9 for comparisons / multi-panel results, 4:3 for dense charts, 1:1 for heatmaps /
confusion matrices / scatter plots.

Example in paper_text:
  "...our method achieves state-of-the-art results as shown below.\n\n[FIGURE:fig3]\n\nThe results demonstrate..."

Example in figures array (results comparison):
  {"id": "fig3", "title": "Performance Comparison", "caption": "Comparison of geometric mean query latency across optimizers.", "image_gen_detailed_description": "Grouped bar chart. X-axis: model names. Y-axis: latency (seconds, 0-5). Values: PostgreSQL=4.6s (red), Bao=2.8s (blue), RLQOpt=2.0s (green). Error bars +/-0.3-0.8. Sans-serif font, white background.", "aspect_ratio": "16:9", "summary": "Compares latency across optimizers"}

Example in figures array (architecture diagram, hero):
  {"id": "fig1", "title": "System Architecture", "caption": "End-to-end pipeline: encoder feeds latents into the planner, which queries the value head before emitting actions.", "image_gen_detailed_description": "Horizontal flow diagram, left to right. Five labeled boxes: 'Input' (gray), 'Encoder' (blue), 'Latent (z, 256-dim)' (light blue, narrow), 'Planner' (green), 'Action Head' (orange). Arrows labeled with shapes. Value head as separate green box below 'Planner', bidirectional arrow. Sans-serif font, clean white background, no 3D.", "aspect_ratio": "21:9", "summary": "Hero architecture diagram"}

CRITICAL: Before writing figure specs, look through artifact workspace output files (*_out.json)
and code to find ALL the exact values. The figure generator cannot read files — every exact number
and value MUST be in the image_gen_detailed_description.
</figure_instructions>

FIRST, add ALL of these to your todo list using your task/todo-tracking tool:

CRITICAL: Todo content must be copied exactly as is written here, with NO CHANGES. These todos are intentionally detailed so that another LLM could read each one without any external context and understand exactly what it has to do.

<todos>
TODO 1. Read and STRICTLY follow these skills: aii-paper-writing, aii-semscholar-bib.
TODO 2. LITERATURE REVIEW: Use web search tools to research the landscape — search key terms from
<hypothesis> and <all_artifacts>. Then use aii_semscholar_bib__fetch to batch-fetch real
BibTeX entries. Build a comprehensive Related Work section. Do NOT fabricate entries.
TODO 3. READ ARTIFACTS: Before writing each section, READ the relevant artifact source code, output
files, and data in the workspace. Extract concrete implementation details, technical innovations,
algorithmic specifics, and quantitative results. Do NOT write surface-level descriptions.

ARTIFACT REFERENCES: When you reference results, methodology, or findings from a specific artifact,
place an [ARTIFACT:artifact_id] marker inline. These become footnotes linking to the artifact's code
in the GitHub repository (first mention gets a footnote with URL, subsequent mentions are omitted).
Use the exact artifact ID from <all_artifacts>. Place the marker right after the claim it supports.
Example:
  "Our evaluation showed a 15% improvement over baselines [ARTIFACT:art_4f9d2c81ab37]." 
TODO 4. WRITE PAPER: Write the full paper text with [FIGURE:fig_id] markers per <figure_instructions>,
and provide the figure specs in the figures array. Cite with numeric references [1], [2], etc.
At the end of the paper text, include a full bibliography section. Do NOT compile LaTeX or generate
actual image/figure files. Your ONLY output is the structured JSON.
</todos><user_data>
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
  "$defs": {
    "FigureSpec": {
      "description": "Figure specification \u2014 structured output from paper writing agent.\n\nThe LLM fills these as a list in PaperText.figures.\nLater converted to Figure objects for viz gen.",
      "properties": {
        "id": {
          "description": "Figure ID matching the [FIGURE:id] marker in paper_text (e.g., 'fig1')",
          "title": "Id",
          "type": "string"
        },
        "title": {
          "description": "Figure title in plain, everyday language \u2014 short and jargon-free. Aim for about 4-8 words (~40 characters).",
          "title": "Title",
          "type": "string"
        },
        "caption": {
          "description": "LaTeX figure caption \u2014 appears below the figure in the paper. Should describe what the figure shows and highlight key takeaways.",
          "title": "Caption",
          "type": "string"
        },
        "image_gen_detailed_description": {
          "description": "Detailed image generation prompt \u2014 axes, labels, ALL numeric values, colors, aspect ratio, layout. The image generator cannot read files; this is its ONLY input.",
          "title": "Image Gen Detailed Description",
          "type": "string"
        },
        "summary": {
          "description": "Brief summary of what this figure communicates",
          "title": "Summary",
          "type": "string"
        }
      },
      "required": [
        "id",
        "title",
        "caption",
        "image_gen_detailed_description",
        "summary"
      ],
      "title": "FigureSpec",
      "type": "object"
    }
  },
  "description": "Paper text \u2014 structured output from paper writing agent.\n\nStructured output fields (LLMPrompt + LLMStructOut):\n- title, abstract, paper_text, figures, summary\n\npaper_text contains [FIGURE:fig_id] markers for positioning.\nfigures contains the full specs as structured objects.\n\nMetadata fields (plain, set by pipeline code):\n- id",
  "properties": {
    "title": {
      "description": "Paper title \u2014 clear, plain-language, and short so a non-expert understands the main contribution at a glance. Aim for about 6-10 words; avoid jargon and acronyms.",
      "title": "Title",
      "type": "string"
    },
    "abstract": {
      "description": "Paper abstract",
      "title": "Abstract",
      "type": "string"
    },
    "paper_text": {
      "description": "Full paper body text with markdown section headers (# Introduction, # Methods, # Results, # Discussion, # Conclusion). Use [FIGURE:fig_id] markers (e.g. [FIGURE:fig1]) to indicate where each figure should appear.",
      "title": "Paper Text",
      "type": "string"
    },
    "figures": {
      "description": "List of figure specifications. Each must have an id matching a [FIGURE:id] marker in paper_text.",
      "items": {
        "$ref": "#/$defs/FigureSpec"
      },
      "title": "Figures",
      "type": "array"
    },
    "summary": {
      "description": "Brief summary of the paper's main contribution and findings",
      "title": "Summary",
      "type": "string"
    }
  },
  "required": [
    "title",
    "abstract",
    "paper_text",
    "summary"
  ],
  "title": "PaperText",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `./.terminal_claude_agent_struct_out.json` exists and contains JSON matching the schema above.
````

### [3] HUMAN-USER prompt · 2026-07-31 20:42:44 UTC

```
Does adding a short self-critique step before answering improve accuracy on multi-step arithmetic word problems?
```

### [4] TOOL CALL — Skill · 2026-07-31 20:42:48 UTC

```
aii-paper-writing
```

### [5] TOOL RESULT — Skill · 2026-07-31 20:42:48 UTC

```
{"success": true, "commandName": "aii-paper-writing"}
```

### [6] TOOL CALL — Skill · 2026-07-31 20:42:48 UTC

```
aii-semscholar-bib
```

### [7] TOOL RESULT — Skill · 2026-07-31 20:42:48 UTC

```
{"success": true, "commandName": "aii-semscholar-bib"}
```

### [8] ASSISTANT · 2026-07-31 20:42:50 UTC

```
Now let me examine the artifact workspaces for concrete numbers.
```

### [9] TOOL CALL — Bash · 2026-07-31 20:42:50 UTC

```
cd /home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_0WmBa7GFLIzI/3_invention_loop/iter_1/gen_art/gen_art_evaluation_1 && ls -la && cat preview_eval_out.json 2>/dev/null | head -200
```

### [10] TOOL RESULT — Bash · 2026-07-31 20:42:50 UTC

```
{"stdout": "total 1888\ndrwxrwxr-x 6 adrian adrian   4096 Jul 31 22:42 .\ndrwxrwxr-x 5 adrian adrian   4096 Jul 31 22:20 ..\ndrwxrwxr-x 2 adrian adrian   4096 Jul 31 22:42 .claude\n-rw-rw-r-- 1 adrian adrian 979839 Jul 31 22:42 .repl_agent.ptylog\n-rw-rw-r-- 1 adrian adrian   4347 Jul 31 22:42 .terminal_claude_agent_struct_out.json\ndrwxrwxr-x 4 adrian adrian   4096 Jul 31 22:33 .venv\ndrwxrwxr-x 2 adrian adrian   4096 Jul 31 22:38 __pycache__\n-rwxrwxr-x 1 adrian adrian  47271 Jul 31 22:39 eval.py\n-rw-rw-r-- 1 adrian adrian 385995 Jul 31 22:41 eval_out.json\n-rw-rw-r-- 1 adrian adrian 385995 Jul 31 22:41 full_eval_out.json\ndrwxrwxr-x 2 adrian adrian   4096 Jul 31 22:36 logs\n-rw-rw-r-- 1 adrian adrian  38927 Jul 31 22:41 mini_eval_out.json\n-rw-rw-r-- 1 adrian adrian  38569 Jul 31 22:41 preview_eval_out.json\n-rw-rw-r-- 1 adrian adrian    265 Jul 31 22:40 pyproject.toml\n{\n  \"metadata\": {\n    \"evaluation_name\": \"checksum_vs_freeform_self_critique_evaluation\",\n    \"hypothesis\": \"Does an explicit checksum self-critique beat free-form self-critique and a matched-length placebo on multi-step arithmetic word problems?\",\n    \"experiment_metadata_snapshot\": {},\n    \"n_records_evaluated\": 1700,\n    \"n_problems\": 200,\n    \"n_checksum_detectable_problems\": 64,\n    \"n_checksum_invisible_problems\": 136,\n    \"models_evaluated\": [\n      \"anthropic/claude-haiku-4.5\",\n      \"openai/gpt-4o-mini\"\n    ],\n    \"detailed_metrics\": {\n      \"metric1_final_answer_accuracy\": {\n        \"anthropic/claude-haiku-4.5\": {\n          \"baseline\": {\n            \"overall\": {\n              \"n\": 200,\n              \"accuracy\": 0.765,\n              \"wilson_ci_low\": 0.7015863111723746,\n              \"wilson_ci_high\": 0.8184256658476741\n            },\n            \"checksum_detectable\": {\n              \"n\": 64,\n              \"accuracy\": 0.78125,\n              \"wilson_ci_low\": 0.6656721604337418,\n              \"wilson_ci_high\": 0.8649768059328052\n            },\n            \"checksum_invisible\": {\n              \"n\": 136,\n              \"accuracy\": 0.7573529411764706,\n              \"wilson_ci_low\": 0.6788821453520603,\n              \"wilson_ci_high\": 0.8216847150791841\n            }\n          },\n          \"freeform_critique\": {\n            \"overall\": {\n              \"n\": 200,\n              \"accuracy\": 0.805,\n              \"wilson_ci_low\": 0.7445595562538726,\n              \"wilson_ci_high\": 0.8539447946559949\n            },\n            \"checksum_detectable\": {\n              \"n\": 64,\n              \"accuracy\": 0.8125,\n              \"wilson_ci_low\": 0.7002563943589847,\n              \"wilson_ci_high\": 0.8893535682705119\n            },\n            \"checksum_invisible\": {\n              \"n\": 136,\n              \"accuracy\": 0.8014705882352942,\n              \"wilson_ci_low\": 0.726559586132398,\n              \"wilson_ci_high\": 0.8598187360870597\n            }\n          },\n          \"placebo_critique\": {\n            \"overall\": {\n              \"n\": 200,\n              \"accuracy\": 0.91,\n              \"wilson_ci_low\": 0.8622342812328346,\n              \"wilson_ci_high\": 0.9423125511378069\n            },\n            \"checksum_detectable\": {\n              \"n\": 64,\n              \"accuracy\": 0.90625,\n              \"wilson_ci_low\": 0.810171204003544,\n              \"wilson_ci_high\": 0.9563217474148017\n            },\n            \"checksum_invisible\": {\n              \"n\": 136,\n              \"accuracy\": 0.9117647058823529,\n              \"wilson_ci_low\": 0.8521015658068821,\n              \"wilson_ci_high\": 0.9488054108831088\n            }\n          },\n          \"checksum_critique\": {\n            \"overall\": {\n              \"n\": 200,\n              \"accuracy\": 0.975,\n              \"wilson_ci_low\": 0.942821659593358,\n              \"wilson_ci_high\": 0.9892752803482388\n            },\n            \"checksum_detectable\": {\n              \"n\": 64,\n              \"accuracy\": 1.0,\n              \"wilson_ci_low\": 0.9433759402071946,\n              \"wilson_ci_high\": 1.0\n            },\n            \"checksum_invisible\": {\n              \"n\": 136,\n              \"accuracy\": 0.9632352941176471,\n              \"wilson_ci_low\": 0.9168244351957462,\n              \"wilson_ci_high\": 0.9841959135804936\n            }\n          },\n          \"oracle_detection_isolation\": {\n            \"overall\": {\n              \"n\": 64,\n              \"accuracy\": 0.9375,\n              \"wilson_ci_low\": 0.8500251490779133,\n              \"wilson_ci_high\": 0.9754287986033819\n            },\n            \"checksum_detectable\": {\n              \"n\": 64,\n              \"accuracy\": 0.9375,\n              \"wilson_ci_low\": 0.8500251490779133,\n              \"wilson_ci_high\": 0.9754287986033819\n            },\n            \"checksum_invisible\": {\n              \"n\": 0,\n              \"accuracy\": null,\n              \"wilson_ci_low\": null,\n              \"wilson_ci_high\": null\n            }\n          }\n        },\n        \"openai/gpt-4o-mini\": {\n          \"baseline\": {\n            \"overall\": {\n              \"n\": 195,\n              \"accuracy\": 0.9538461538461539,\n              \"wilson_ci_low\": 0.9146253066412194,\n              \"wilson_ci_high\": 0.9755311076687877\n            },\n            \"checksum_detectable\": {\n              \"n\": 61,\n              \"accuracy\": 0.9508196721311475,\n              \"wilson_ci_low\": 0.8650887247278409,\n              \"wilson_ci_high\": 0.9831340173312375\n            },\n            \"checksum_invisible\": {\n              \"n\": 134,\n              \"accuracy\": 0.9552238805970149,\n              \"wilson_ci_low\": 0.9057552772644654,\n              \"wilson_ci_high\": 0.9793195111466114\n            }\n          },\n          \"freeform_critique\": {\n            \"overall\": {\n              \"n\": 195,\n              \"accuracy\": 0.9384615384615385,\n              \"wilson_ci_low\": 0.895531183514045,\n              \"wilson_ci_high\": 0.964450437090538\n            },\n            \"checksum_detectable\": {\n              \"n\": 61,\n              \"accuracy\": 0.9508196721311475,\n              \"wilson_ci_low\": 0.8650887247278409,\n              \"wilson_ci_high\": 0.9831340173312375\n            },\n            \"checksum_invisible\": {\n              \"n\": 134,\n              \"accuracy\": 0.9328358208955224,\n              \"wilson_ci_low\": 0.8772811261744599,\n              \"wilson_ci_high\": 0.9642653939541049\n            }\n          },\n          \"placebo_critique\": {\n            \"overall\": {\n              \"n\": 193,\n              \"accuracy\": 0.9740932642487047,\n              \"wilson_ci_low\": 0.940797651018338,\n              \"wilson_ci_high\": 0.9888845465043774\n            },\n            \"checksum_detectable\": {\n              \"n\": 60,\n              \"accuracy\": 0.9666666666666667,\n              \"wilson_ci_low\": 0.886362257256914,\n              \"wilson_ci_high\": 0.990810680743802\n            },\n            \"checksum_invisible\": {\n              \"n\": 133,\n              \"accuracy\": 0.9774436090225563,\n              \"wilson_ci_low\": 0.9357817301552714,\n              \"wilson_ci_high\": 0.9922995771801788\n            }\n          },\n          \"checksum_critique\": {\n            \"overall\": {\n              \"n\": 192,\n              \"accuracy\": 0.9635416666666666,\n              \"wilson_ci_low\": 0.9266691049105195,\n              \"wilson_ci_high\": 0.9822293534234272\n            },\n            \"checksum_detectable\": {\n              \"n\": 60,\n              \"accuracy\": 0.9666666666666667,\n              \"wilson_ci_low\": 0.886362257256914,\n              \"wilson_ci_high\": 0.990810680743802\n            },\n            \"checksum_invisible\": {\n              \"n\": 132,\n              \"accuracy\": 0.9621212121212122,\n              \"wilson_ci_low\": 0.9143919640569403,\n              \"wilson_ci_high\": 0.9837138208716185\n            }\n          },\n          \"oracle_detection_isolation\": {\n            \"overall\": {", "stderr": "\nShell cwd was reset to /home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_0WmBa7GFLIzI/3_invention_loop/iter_1/gen_paper_text/gen_paper_text", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [11] TOOL CALL — Bash · 2026-07-31 20:42:50 UTC

```
cd /home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_0WmBa7GFLIzI/3_invention_loop/iter_1/gen_art/gen_art_dataset_1 && ls -la && cat preview_data_out.json 2>/dev/null | head -100
```

### [12] TOOL RESULT — Bash · 2026-07-31 20:42:50 UTC

```
{"stdout": "total 4036\ndrwxrwxr-x 5 adrian adrian    4096 Jul 31 22:29 .\ndrwxrwxr-x 5 adrian adrian    4096 Jul 31 22:20 ..\n-rw-rw-r-- 1 adrian adrian 1039538 Jul 31 22:29 .repl_agent.ptylog\n-rw-rw-r-- 1 adrian adrian    3596 Jul 31 22:29 .terminal_claude_agent_struct_out.json\ndrwxrwxr-x 4 adrian adrian    4096 Jul 31 22:29 .venv\n-rw-rw-r-- 1 adrian adrian   27118 Jul 31 22:28 data.py\n-rw-rw-r-- 1 adrian adrian 3002452 Jul 31 22:29 full_data_out.json\ndrwxrwxr-x 2 adrian adrian    4096 Jul 31 22:24 logs\n-rw-rw-r-- 1 adrian adrian    4203 Jul 31 22:29 mini_data_out.json\n-rw-rw-r-- 1 adrian adrian    4079 Jul 31 22:29 preview_data_out.json\n-rw-rw-r-- 1 adrian adrian     128 Jul 31 22:29 pyproject.toml\ndrwxrwxr-x 3 adrian adrian    4096 Jul 31 22:27 temp\n-rw-rw-r-- 1 adrian adrian    2508 Jul 31 22:29 uv.lock\n-rw-rw-r-- 1 adrian adrian    5155 Jul 31 22:28 verify.py\n{\n  \"metadata\": {\n    \"source\": \"openai/gsm8k (main config, train+test) + procedural synthetic template generator\",\n    \"description\": \"Multi-step arithmetic word problems with computation traces, plus deterministic error-injection variants labeled by mod-9 checksum detectability.\"\n  },\n  \"datasets\": [\n    {\n      \"dataset\": \"arithmetic_checksum_dataset\",\n      \"examples\": [\n        {\n          \"input\": \"Ali and Leila reserve their places for a trip to Egypt. The price is $147 per person, but they were each given a discount of $14 since there are two of them. How much does their trip cost?\",\n          \"output\": \"266\",\n          \"metadata_row_type\": \"base_item\",\n          \"metadata_item_id\": \"gsm8k_6569\",\n          \"metadata_item_source\": \"gsm8k_real\",\n          \"metadata_numeric_range\": \"large\",\n          \"metadata_chain_length\": 2,\n          \"metadata_trace\": [\n            {\n              \"step_index\": 0,\n              \"operand_1\": 147,\n              \"operand_2\": 14,\n              \"operation\": \"-\",\n              \"result\": 133,\n              \"depends_on_step\": null\n            },\n            {\n              \"step_index\": 1,\n              \"operand_1\": 133,\n              \"operand_2\": 2,\n              \"operation\": \"*\",\n              \"result\": 266,\n              \"depends_on_step\": [\n                0\n              ]\n            }\n          ],\n          \"metadata_final_answer\": 266,\n          \"metadata_fold\": 0\n        },\n        {\n          \"input\": \"Problem: Ali and Leila reserve their places for a trip to Egypt. The price is $147 per person, but they were each given a discount of $14 since there are two of them. How much does their trip cost?\\nRe...\",\n          \"output\": \"checksum_detectable|correct_final_answer=266\",\n          \"metadata_row_type\": \"error_variant\",\n          \"metadata_base_item_id\": \"gsm8k_6569\",\n          \"metadata_error_type\": \"dropped_carry\",\n          \"metadata_injected_step_index\": 1,\n          \"metadata_original_step\": {\n            \"step_index\": 1,\n            \"operand_1\": 133,\n            \"operand_2\": 2,\n            \"operation\": \"*\",\n            \"result\": 266,\n            \"depends_on_step\": [\n              0\n            ]\n          },\n          \"metadata_corrupted_step\": {\n            \"step_index\": 1,\n            \"operand_1\": 133,\n            \"operand_2\": 2,\n            \"operation\": \"*\",\n            \"result\": 166,\n            \"depends_on_step\": [\n              0\n            ]\n          },\n          \"metadata_corrupted_final_answer\": 166,\n          \"metadata_mod9_residue_preserved\": false,\n          \"metadata_label\": \"checksum_detectable\",\n          \"metadata_item_source\": \"gsm8k_real\",\n          \"metadata_numeric_range\": \"large\",\n          \"metadata_chain_length\": 2,\n          \"metadata_fold\": 0\n        },\n        {\n          \"input\": \"Problem: Ali and Leila reserve their places for a trip to Egypt. The price is $147 per person, but they were each given a discount of $14 since there are two of them. How much does their trip cost?\\nRe...\",\n          \"output\": \"checksum_detectable|correct_final_answer=266\",\n          \"metadata_row_type\": \"error_variant\",\n          \"metadata_base_item_id\": \"gsm8k_6569\",\n          \"metadata_error_type\": \"sign_flip\",\n          \"metadata_injected_step_index\": 0,\n          \"metadata_original_step\": {\n            \"step_index\": 0,\n            \"operand_1\": 147,\n            \"operand_2\": 14,\n            \"operation\": \"-\",\n            \"result\": 133,\n            \"depends_on_step\": null\n          },\n          \"metadata_corrupted_step\": {\n            \"step_index\": 0,\n            \"operand_1\": 147,\n            \"operand_2\": 14,\n            \"operation\": \"-\",\n            \"result\": 161,\n            \"depends_on_step\": null\n          },\n          \"metadata_corrupted_final_answer\": 322,\n          \"metadata_mod9_residue_preserved\": false,", "stderr": "\nShell cwd was reset to /home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_0WmBa7GFLIzI/3_invention_loop/iter_1/gen_paper_text/gen_paper_text", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [13] TOOL CALL — Bash · 2026-07-31 20:42:56 UTC

```
cd /home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_0WmBa7GFLIzI/3_invention_loop/iter_1/gen_art/gen_art_evaluation_1 && python3 -c "
import json
d=json.load(open('full_eval_out.json'))
m=d['metadata']
print(list(m.keys()))
print(json.dumps(m.get('metrics_agg', {}), indent=1)[:6000])
"
```

### [14] TOOL RESULT — Bash · 2026-07-31 20:42:56 UTC

```
{"stdout": "['evaluation_name', 'hypothesis', 'experiment_metadata_snapshot', 'n_records_evaluated', 'n_problems', 'n_checksum_detectable_problems', 'n_checksum_invisible_problems', 'models_evaluated', 'detailed_metrics']\n{}", "stderr": "\nShell cwd was reset to /home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_0WmBa7GFLIzI/3_invention_loop/iter_1/gen_paper_text/gen_paper_text", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [15] TOOL CALL — Bash · 2026-07-31 20:42:58 UTC

```
cd /home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_0WmBa7GFLIzI/3_invention_loop/iter_1/gen_art/gen_art_evaluation_1 && python3 -c "
import json
d=json.load(open('full_eval_out.json'))
print(list(d.keys()))
"
```

### [16] TOOL RESULT — Bash · 2026-07-31 20:42:58 UTC

```
{"stdout": "['metadata', 'metrics_agg', 'datasets']", "stderr": "\nShell cwd was reset to /home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_0WmBa7GFLIzI/3_invention_loop/iter_1/gen_paper_text/gen_paper_text", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [17] TOOL CALL — Bash · 2026-07-31 20:43:00 UTC

```
cd /home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_0WmBa7GFLIzI/3_invention_loop/iter_1/gen_art/gen_art_evaluation_1 && python3 -c "
import json
d=json.load(open('full_eval_out.json'))
print(json.dumps(d['metrics_agg'], indent=1))
"
```

### [18] TOOL RESULT — Bash · 2026-07-31 20:43:00 UTC

```
{"stdout": "{\n \"acc_claude_haiku_4_5_baseline_overall\": 0.765,\n \"acc_claude_haiku_4_5_baseline_checksum_detectable\": 0.78125,\n \"acc_claude_haiku_4_5_baseline_checksum_invisible\": 0.7573529411764706,\n \"acc_claude_haiku_4_5_freeform_critique_overall\": 0.805,\n \"acc_claude_haiku_4_5_freeform_critique_checksum_detectable\": 0.8125,\n \"acc_claude_haiku_4_5_freeform_critique_checksum_invisible\": 0.8014705882352942,\n \"acc_claude_haiku_4_5_placebo_critique_overall\": 0.91,\n \"acc_claude_haiku_4_5_placebo_critique_checksum_detectable\": 0.90625,\n \"acc_claude_haiku_4_5_placebo_critique_checksum_invisible\": 0.9117647058823529,\n \"acc_claude_haiku_4_5_checksum_critique_overall\": 0.975,\n \"acc_claude_haiku_4_5_checksum_critique_checksum_detectable\": 1.0,\n \"acc_claude_haiku_4_5_checksum_critique_checksum_invisible\": 0.9632352941176471,\n \"acc_claude_haiku_4_5_oracle_detection_isolation_overall\": 0.9375,\n \"acc_claude_haiku_4_5_oracle_detection_isolation_checksum_detectable\": 0.9375,\n \"acc_gpt_4o_mini_baseline_overall\": 0.9538461538461539,\n \"acc_gpt_4o_mini_baseline_checksum_detectable\": 0.9508196721311475,\n \"acc_gpt_4o_mini_baseline_checksum_invisible\": 0.9552238805970149,\n \"acc_gpt_4o_mini_freeform_critique_overall\": 0.9384615384615385,\n \"acc_gpt_4o_mini_freeform_critique_checksum_detectable\": 0.9508196721311475,\n \"acc_gpt_4o_mini_freeform_critique_checksum_invisible\": 0.9328358208955224,\n \"acc_gpt_4o_mini_placebo_critique_overall\": 0.9740932642487047,\n \"acc_gpt_4o_mini_placebo_critique_checksum_detectable\": 0.9666666666666667,\n \"acc_gpt_4o_mini_placebo_critique_checksum_invisible\": 0.9774436090225563,\n \"acc_gpt_4o_mini_checksum_critique_overall\": 0.9635416666666666,\n \"acc_gpt_4o_mini_checksum_critique_checksum_detectable\": 0.9666666666666667,\n \"acc_gpt_4o_mini_checksum_critique_checksum_invisible\": 0.9621212121212122,\n \"acc_gpt_4o_mini_oracle_detection_isolation_overall\": 0.9672131147540983,\n \"acc_gpt_4o_mini_oracle_detection_isolation_checksum_detectable\": 0.9672131147540983,\n \"recall_claude_haiku_4_5_baseline\": 0.0,\n \"recall_claude_haiku_4_5_freeform_critique\": 0.0,\n \"recall_claude_haiku_4_5_placebo_critique\": 0.0,\n \"recall_gpt_4o_mini_baseline\": 0.0,\n \"precision_gpt_4o_mini_freeform_critique\": 0.0,\n \"recall_gpt_4o_mini_freeform_critique\": 0.0,\n \"recall_gpt_4o_mini_placebo_critique\": 0.0,\n \"precision_gpt_4o_mini_checksum_critique\": 0.0,\n \"correction_acc_claude_haiku_4_5_baseline\": 0.0,\n \"correction_acc_claude_haiku_4_5_freeform_critique\": 0.8,\n \"correction_acc_claude_haiku_4_5_checksum_critique\": 1.0,\n \"correction_acc_gpt_4o_mini_freeform_critique\": 1.0,\n \"correction_acc_gpt_4o_mini_checksum_critique\": 1.0,\n \"oracle_fix_rate_claude_haiku_4_5\": 0.9375,\n \"fix_rate_gap_claude_haiku_4_5\": -0.0625,\n \"oracle_fix_rate_gpt_4o_mini\": 0.9672131147540983,\n \"fix_rate_gap_gpt_4o_mini\": -0.032786885245901676,\n \"holm_p_claude_haiku_4_5_freeform_critique_vs_checksum_critique\": 0.04,\n \"effect_pp_claude_haiku_4_5_freeform_critique_vs_checksum_critique\": -18.75,\n \"holm_p_claude_haiku_4_5_placebo_critique_vs_checksum_critique\": 0.04,\n \"effect_pp_claude_haiku_4_5_placebo_critique_vs_checksum_critique\": -9.375,\n \"holm_p_gpt_4o_mini_freeform_critique_vs_checksum_critique\": 1.0,\n \"effect_pp_gpt_4o_mini_freeform_critique_vs_checksum_critique\": -1.6666666666666718,\n \"holm_p_gpt_4o_mini_placebo_critique_vs_checksum_critique\": 1.0,\n \"effect_pp_gpt_4o_mini_placebo_critique_vs_checksum_critique\": 0.0,\n \"placebo_checksum_length_ratio_claude_haiku_4_5\": 1.0479682057034894,\n \"placebo_checksum_length_ratio_gpt_4o_mini\": 0.826225904560088,\n \"checksum_computation_error_rate_overall\": 0.15384615384615385,\n \"checksum_audit_n_traces\": 80.0,\n \"invisible_ctrl_acc_claude_haiku_4_5_baseline\": 0.7573529411764706,\n \"invisible_ctrl_acc_claude_haiku_4_5_freeform_critique\": 0.8014705882352942,\n \"invisible_ctrl_acc_claude_haiku_4_5_placebo_critique\": 0.9117647058823529,\n \"invisible_ctrl_acc_claude_haiku_4_5_checksum_critique\": 0.9632352941176471,\n \"invisible_ctrl_acc_gpt_4o_mini_baseline\": 0.9552238805970149,\n \"invisible_ctrl_acc_gpt_4o_mini_freeform_critique\": 0.9328358208955224,\n \"invisible_ctrl_acc_gpt_4o_mini_placebo_critique\": 0.9774436090225563,\n \"invisible_ctrl_acc_gpt_4o_mini_checksum_critique\": 0.9621212121212122\n}", "stderr": "\nShell cwd was reset to /home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_0WmBa7GFLIzI/3_invention_loop/iter_1/gen_paper_text/gen_paper_text", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [19] ASSISTANT · 2026-07-31 20:43:20 UTC

```
Now let me do the literature search in parallel with reading a bit more experiment detail.
```

### [20] TOOL CALL — Bash · 2026-07-31 20:43:20 UTC

```
cd /home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_0WmBa7GFLIzI/3_invention_loop/iter_1/gen_art/gen_art_evaluation_1 && grep -o '"n_checksum_computation_errors[^,]*\|"judge_model[^,]*' eval.py full_eval_out.json 2>/dev/null | head -5
grep -n "McNemar\|bootstrap\|holm\|judge" eval.py | head -30
```

### [21] TOOL RESULT — Bash · 2026-07-31 20:43:20 UTC

```
{"stdout": "10:regression, an LLM-judge checksum-computation audit, and a checksum-invisible\n41:# bounded number of LLM-judge calls)\n388:def bootstrap_ci_diff(a_correct: list[int], b_correct: list[int], n_boot: int = 10000, seed: int = 1) -> dict:\n417:def holm_bonferroni(pvals_named: list[tuple[str, float]]) -> dict:\n431:            \"p_holm_adjusted\": adjusted[i],\n467:# Metric 7: checksum self-computation audit via LLM judge\n514:    def judge_one(rec: dict) -> dict:\n523:                    # take the LAST VERDICT: line so the judge's own step-by-step\n552:        futures = {pool.submit(judge_one, r): r for r in tasks}\n558:                logger.warning(\"Checksum-audit sub-budget ($1.50) reached; stopping remaining judge calls\")\n696:    all_pvals_for_holm: list[tuple[str, float]] = []\n715:            use_bootstrap_det = (mcnemar_det is None) or (mcnemar_det[\"n_discordant\"] < 25)\n722:                \"bootstrap_detectable_subset\": bootstrap_ci_diff(a_det, b_det) if detectable_pids else None,\n723:                \"used_bootstrap_for_detectable_subset_due_to_low_discordant_count\": use_bootstrap_det,\n729:            # primary p-value for the family: exact McNemar on detectable subset if enough\n730:            # discordant pairs, else the bootstrap-CI-excludes-zero result recast as p<0.05/p>=0.05\n731:            if mcnemar_det is not None and not use_bootstrap_det:\n732:                p_for_holm = mcnemar_det[\"p_value\"]\n733:            elif entry[\"bootstrap_detectable_subset\"] is not None:\n734:                p_for_holm = 0.01 if entry[\"bootstrap_detectable_subset\"][\"excludes_zero\"] else 0.5\n736:                p_for_holm = 1.0\n737:            all_pvals_for_holm.append((f\"{model}::{key}\", p_for_holm))\n740:    holm_results = holm_bonferroni(all_pvals_for_holm)\n741:    for name, res in holm_results.items():\n743:        significance_table[model][key][\"holm_bonferroni\"] = res\n891:            hb = d.get(\"holm_bonferroni\")\n893:                agg[_safe_key(\"holm_p\", model_short, pair_key)] = float(hb[\"p_holm_adjusted\"])\n959:    parser.add_argument(\"--skip-audit\", action=\"store_true\", help=\"skip the LLM-judge checksum-computation audit (Metric 7)\")\n983:    logger.info(\"STEP 4: checksum self-computation audit (Metric 7, LLM-judge via OpenRouter)\")", "stderr": "\nShell cwd was reset to /home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_0WmBa7GFLIzI/3_invention_loop/iter_1/gen_paper_text/gen_paper_text", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [22] ASSISTANT · 2026-07-31 20:43:22 UTC

```
I have enough quantitative detail. Now literature search + bib fetch.
```

### [23] TOOL CALL — ToolSearch · 2026-07-31 20:43:22 UTC

```
{'query': 'web search', 'max_results': 5}
```

### [24] TOOL RESULT — ToolSearch · 2026-07-31 20:43:22 UTC

```
{"matches": ["WebSearch", "WebFetch", "ExitPlanMode"], "query": "web search", "total_deferred_tools": 22}
```

### [25] TOOL CALL — ToolSearch · 2026-07-31 20:43:22 UTC

```
{'query': 'semscholar fetch bibtex', 'max_results': 5}
```

### [26] TOOL RESULT — ToolSearch · 2026-07-31 20:43:22 UTC

```
{"matches": ["WebFetch"], "query": "semscholar fetch bibtex", "total_deferred_tools": 22}
```

### [27] TOOL CALL — ToolSearch · 2026-07-31 20:43:26 UTC

```
{'query': 'aii_semscholar_bib__fetch', 'max_results': 5}
```

### [28] TOOL RESULT — ToolSearch · 2026-07-31 20:43:26 UTC

```
{"matches": [], "query": "aii_semscholar_bib__fetch", "total_deferred_tools": 22}
```

### [29] TOOL CALL — WebSearch · 2026-07-31 20:43:26 UTC

```
LLM self-critique fails to correct reasoning errors "self-refine" arithmetic verification
```

### [30] TOOL CALL — WebSearch · 2026-07-31 20:43:26 UTC

```
casting out nines checksum digit sum error detection arithmetic verification
```

### [31] TOOL RESULT — WebSearch · 2026-07-31 20:43:34 UTC

```
{"query": "LLM self-critique fails to correct reasoning errors \"self-refine\" arithmetic verification", "results": [{"tool_use_id": "srvtoolu_014TE8iQBFwT8CHr6k51WktG", "content": [{"title": "The Validation Gap: A Mechanistic Analysis of How Language Models Compute Arithmetic but Fail to Validate It", "url": "https://arxiv.org/pdf/2502.11771"}, {"title": "When Can LLMs Actually Correct Their Own Mistakes? A Critical Survey of Self-Correction of LLMs | Transactions of the Association for Computational Linguistics | MIT Press", "url": "https://direct.mit.edu/tacl/article/doi/10.1162/tacl_a_00713/125177/When-Can-LLMs-Actually-Correct-Their-Own-Mistakes"}, {"title": "LLMs can’t self-correct in reasoning tasks, DeepMind study finds - TechTalks", "url": "https://bdtechtalks.com/2023/10/09/llm-self-correction-reasoning-failures/"}, {"title": "When Can LLMs Actually Correct Their Own Mistakes? A Critical Survey of Self-Correction of LLMs", "url": "https://arxiv.org/html/2406.01297v3"}, {"title": "LegalReasoner: Step-wised Verification-Correction for Legal Judgment Reasoning", "url": "https://arxiv.org/pdf/2506.07443"}, {"title": "SAFE: An LLM-as-Verifier Framework for Evidence-Grounded Multi-Hop Reasoning", "url": "https://arxiv.org/pdf/2604.01993"}, {"title": "Feedback or Autonomy? Analyzing LLMs’ Ability to Self-Correct", "url": "https://web.stanford.edu/class/archive/cs/cs224n/cs224n.1244/final-projects/KaiMicaFronsdal.pdf"}, {"title": "On the Self-Verification Limitations of Large Language Models on   Reasoning and Planning Tasks", "url": "https://arxiv.org/pdf/2402.08115"}, {"title": "IFDNS: An Iterative Feedback-Driven Neuro-Symbolic Method for Faithful Logical Reasoning", "url": "https://arxiv.org/pdf/2601.07464"}, {"title": "ProgCo: Program Helps Self-Correction of Large Language Models", "url": "https://arxiv.org/pdf/2501.01264"}]}, "Based on the search results, here's what I found on LLM self-critique failures in reasoning and arithmetic verification:\n\n## Key Findings\n\n**Self-Critique Limitations**: LLMs tend to struggle with intrinsic self-correction, especially with detecting errors in their own output. Self-Refine and RCI Prompting iteratively prompt LLMs to self-correct their own responses in tasks such as arithmetic reasoning, but recent studies report that intrinsic self-correction does not improve or even degrade the performance in tasks such as arithmetic reasoning, closed-book QA, code generation, plan generation, and graph coloring.\n\n**Arithmetic Verification Issues**: Models are unable to identify granular calculation mistakes such as carry errors and missing signs, but are able to correct high-level planning. Additionally, a core reason for the failure of self-correction in LLMs is their inability to effectively self-detect problematic outputs and generate high-quality feedback.\n\n**When Self-Correction Works**: In reasoning tasks, self-correction techniques typically succeed only when they can leverage external sources, such as human feedback, an external tool like a calculator or code executor, or a knowledge base.\n\n**Verification Breakdowns**: Across hard reasoning domains, LLMs did poorly in verification, critique generation, and critique consideration, with the stacked errors often making the LLM self-critiquing loop perform worse than just having the LLM guess the solution up front."], "durationSeconds": 7.900908007999998, "searchCount": 1}
```

### [32] TOOL RESULT — WebSearch · 2026-07-31 20:43:34 UTC

```
{"query": "casting out nines checksum digit sum error detection arithmetic verification", "results": [{"tool_use_id": "srvtoolu_01EDAJABUYvzTyUtJ1LtyM7G", "content": [{"title": "Casting Out Nines — Definition, Formula & Examples", "url": "https://www.mathwords.com/c/casting_out_nines.htm"}, {"title": "Casting Out Nines: Math Monday: What is casting out nines?", "url": "https://www.chronicle.com/blognetwork/castingoutnines/math-monday-what-is-casting-out-nines"}, {"title": "Casting Out Nines: What and How – The Math Doctors", "url": "https://www.themathdoctors.org/casting-out-nines-what-and-how/"}, {"title": "Casting out nines - HandWiki", "url": "https://handwiki.org/wiki/Casting_out_nines"}, {"title": "Casting out nines", "url": "https://en.wikipedia.org/wiki/Casting_out_nines"}, {"title": "Digit sum calculator", "url": "https://www.calculatemath.com/2026/02/digit-sum-calculator.html"}, {"title": "Casting out nines — Grokipedia", "url": "https://grokipedia.com/page/Casting_out_nines"}]}, "Here's comprehensive information about casting out nines and its use in error detection:\n\n## Overview\n\nCasting out nines is a method for checking whether an arithmetic answer is correct by replacing each number with its digital root (the repeated sum of its digits) and verifying that the same operation on those roots gives a consistent result.\n\n## How It Works\n\nThe method exploits the fact that any integer is congruent to the sum of its digits modulo 9. To apply the technique:\n\n1. Add up all the digits of a number. If the result has more than one digit, add those digits again until you get a single digit from 1 to 9 (treating 9 as 0).\n\n2. Do this for every number in your calculation. Then perform the same operation on those single-digit results and reduce again.\n\n3. If the final single digit does not match the digit sum of your original answer, you made an error somewhere.\n\n## Error Detection Capabilities\n\nA mismatch guarantees an error; a match suggests (but does not prove) correctness. However, the method has limitations. It can give false positives in some circumstances and fails to detect digit transpositions.\n\nThe method detects single-digit errors with probability 8/9, assuming random errors, but this drops for multi-digit errors due to increased chances of multiples of 9.\n\n## Historical and Practical Applications\n\nBefore calculators were common, casting out nines was the standard way students and accountants verified long multiplication and addition by hand. Today, credit card numbers and ISBN codes use digit-sum-based checksums to catch input errors."], "durationSeconds": 7.685237613000004, "searchCount": 1}
```

### [33] TOOL CALL — WebSearch · 2026-07-31 20:43:38 UTC

```
GSM8K training verifiers to solve math word problems Cobbe 2021
```

### [34] TOOL CALL — WebSearch · 2026-07-31 20:43:38 UTC

```
Chain-of-Verification reduces hallucination large language models Dhuliawala
```

### [35] TOOL CALL — WebSearch · 2026-07-31 20:43:38 UTC

```
S2R self-verify self-correct reinforcement learning LLM reasoning arxiv
```

### [36] TOOL RESULT — WebSearch · 2026-07-31 20:43:44 UTC

```
{"query": "GSM8K training verifiers to solve math word problems Cobbe 2021", "results": [{"tool_use_id": "srvtoolu_01LMCahMYSPS1E1QQTrkPdFC", "content": [{"title": "(Open Access) Training Verifiers to Solve Math Word Problems (2021) | Karl Cobbe | 2 Citations", "url": "https://scispace.com/papers/training-verifiers-to-solve-math-word-problems-2jokilm0qa"}, {"title": "[Paper Note] Training Verifiers to Solve Math Word Problems, Karl Cobbe+, arXiv'21, 2021.10 · Issue #1618 · AkihikoWatanabe/paper_notes", "url": "https://github.com/AkihikoWatanabe/paper_notes/issues/1618"}, {"title": "[PDF] Training Verifiers to Solve Math Word Problems | Semantic Scholar", "url": "https://www.semanticscholar.org/paper/Training-Verifiers-to-Solve-Math-Word-Problems-Cobbe-Kosaraju/d6045d2ccc9c09ca1671348de86d07da6bc28eea"}, {"title": "Training Verifiers to Solve Math Word Problems", "url": "https://www.researchgate.net/publication/355698629_Training_Verifiers_to_Solve_Math_Word_Problems"}, {"title": "[2110.14168] Training Verifiers to Solve Math Word Problems", "url": "https://arxiv.org/abs/2110.14168"}, {"title": "Training Veriﬁers to Solve Math Word Problems Karl Cobbe∗ Vineet Kosaraju∗", "url": "https://arxiv.org/pdf/2110.14168"}, {"title": "The Ideation-Execution Gap: Execution Outcomes of LLM-Generated versus Human Research Ideas", "url": "https://arxiv.org/pdf/2506.20803"}, {"title": "Scaling Latent Reasoning via Looped Language Models", "url": "https://arxiv.org/pdf/2510.25741"}, {"title": "Google Scholar", "url": "https://scholar.google.com/scholar_lookup?title=Training+verifiers+to+solve+math+word+problems&author=K.+Cobbe&publication_year=2021"}, {"title": "DART-Math: Difficulty-Aware Rejection Tuning for Mathematical   Problem-Solving", "url": "https://arxiv.org/pdf/2407.13690"}]}, "Based on the search results, here's what I found about the Cobbe 2021 paper on training verifiers to solve math word problems:\n\n## Overview\n\nThe paper introduces GSM8K, a dataset of 8.5K high quality linguistically diverse grade school math word problems. The work addresses the fact that state-of-the-art language models can match human performance on many tasks, but they still struggle to robustly perform multi-step mathematical reasoning.\n\n## Methodology\n\nThe researchers propose training verifiers to judge the correctness of model completions, and at test time, generate many candidate solutions and select the one ranked highest by the verifier.\n\n## Results\n\nVerification significantly improves performance on GSM8K, and provides strong empirical evidence that verification scales more effectively with increased data than a finetuning baseline.\n\nThe paper was published on arXiv on October 27, 2021 (arXiv:2110.14168) and is authored by Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian, and several other researchers from OpenAI."], "durationSeconds": 6.037896452999994, "searchCount": 1}
```

### [37] TOOL RESULT — WebSearch · 2026-07-31 20:43:44 UTC

```
{"query": "Chain-of-Verification reduces hallucination large language models Dhuliawala", "results": [{"tool_use_id": "srvtoolu_012gbQb6L2KFRPNwCCgEYEch", "content": [{"title": "Chain-of-Verification Reduces Hallucination in Large Language Models - ACL Anthology", "url": "https://aclanthology.org/2024.findings-acl.212/"}, {"title": "[2309.11495] Chain-of-Verification Reduces Hallucination in Large Language Models", "url": "https://arxiv.org/abs/2309.11495"}, {"title": "Paper page - Chain-of-Verification Reduces Hallucination in Large Language Models", "url": "https://huggingface.co/papers/2309.11495"}, {"title": "Chain-of-Verification Reduces Hallucination in Large Language Models", "url": "https://www.researchgate.net/publication/384218319_Chain-of-Verification_Reduces_Hallucination_in_Large_Language_Models"}, {"title": "CHAIN-OF-VERIFICATION REDUCES HALLUCINATION IN LARGE LANGUAGE MODELS", "url": "https://arxiv.org/pdf/2309.11495"}, {"title": "[PDF] Chain-of-Verification Reduces Hallucination in Large Language Models | Semantic Scholar", "url": "https://www.semanticscholar.org/paper/Chain-of-Verification-Reduces-Hallucination-in-Dhuliawala-Komeili/4b0b56be0ae9479d2bd5c2f0943db1906343c10f"}, {"title": "ETH Library Chain-of-Verification Reduces Hallucination in Large Language", "url": "https://www.research-collection.ethz.ch/server/api/core/bitstreams/468e77de-b21f-4ede-b179-8a52b01a1c5a/content"}, {"title": "Chain-of-Verification Reduces Hallucination in Large ...", "url": "https://aclanthology.org/2024.findings-acl.212.pdf"}, {"title": "KG-Guard: Graph-Based Hallucination Detection for Knowledge Base Question Answering", "url": "https://arxiv.org/pdf/2606.00328"}, {"title": "HoT: Highlighted Chain of Thought for Referencing Supporting Facts from Inputs", "url": "https://arxiv.org/pdf/2503.02003"}]}, "Based on the search results, here's what I found:\n\nShehzaad Dhuliawala and colleagues published \"Chain-of-Verification Reduces Hallucination in Large Language Models,\" addressing the problem of hallucination—the generation of plausible yet incorrect factual information—in large language models.\n\nThe Chain-of-Verification (CoVe) method works by having the model first draft an initial response, then plan verification questions to fact-check its draft, answer those questions independently so the answers are not biased by other responses, and finally generate a final verified response.\n\nIn experiments, CoVe decreases hallucinations across a variety of tasks, including list-based questions from Wikidata, closed book MultiSpanQA, and longform text generation.\n\nThe paper was published in the Findings of the Association for Computational Linguistics: ACL 2024."], "durationSeconds": 6.5906377009999995, "searchCount": 1}
```

### [38] TOOL RESULT — WebSearch · 2026-07-31 20:43:46 UTC

```
{"query": "S2R self-verify self-correct reinforcement learning LLM reasoning arxiv", "results": [{"tool_use_id": "srvtoolu_0134WgK6apStUGQ1XTgsXB1i", "content": [{"title": "S2R: Teaching LLMs to Self-verify and Self-correct via Reinforcement Learning - ACL Anthology", "url": "https://aclanthology.org/2025.acl-long.1104/"}, {"title": "GitHub - NineAbyss/S2R: This is the official implementation of the paper \"S²R: Teaching LLMs to Self-verify and Self-correct via Reinforcement Learning\"", "url": "https://github.com/NineAbyss/S2R"}, {"title": "Paper page - S^2R: Teaching LLMs to Self-verify and Self-correct via Reinforcement Learning", "url": "https://huggingface.co/papers/2502.12853"}, {"title": "[2502.12853] S$^2$R: Teaching LLMs to Self-verify and Self-correct via Reinforcement Learning", "url": "https://arxiv.org/abs/2502.12853"}, {"title": "S$^2$R: Teaching LLMs to Self-verify and Self-correct via Reinforcement   Learning", "url": "https://arxiv.org/pdf/2502.12853"}, {"title": "S$^2$R: Teaching LLMs to Self-verify and Self-correct via Reinforcement Learning | AI Research Paper Details", "url": "https://www.aimodels.fyi/papers/arxiv/sdollar2dollarr-teaching-llms-to-self-verify-self"}, {"title": "S$^2$R: Teaching LLMs to Self-verify and Self-correct via Reinforcement Learning", "url": "https://www.researchgate.net/publication/389130216_S2R_Teaching_LLMs_to_Self-verify_and_Self-correct_via_Reinforcement_Learning"}, {"title": "Boosting Accuracy and Efficiency of Budget Forcing in LLMs via Reinforcement Learning for Mathematical Reasoning", "url": "https://arxiv.org/pdf/2510.21398"}]}, "I found comprehensive information about S2R. Here are the key findings:\n\n## S2R: Teaching LLMs to Self-verify and Self-correct via Reinforcement Learning\n\nS2R is an efficient framework that enhances LLM reasoning by teaching models to self-verify and self-correct during inference.\n\n### Methodology\n\nThe approach first initializes LLMs with iterative self-verification and self-correction behaviors through supervised fine-tuning on carefully curated data. The self-verification and self-correction skills are then further strengthened by both outcome-level and process-level reinforcement learning, with minimized resource requirements, enabling the model to adaptively refine its reasoning process during inference.\n\n### Key Results\n\nWith only 3.1k self-verifying and self-correcting behavior initialization samples, Qwen2.5-math-7B achieves an accuracy improvement from 51.0% to 81.6%, outperforming models trained on an equivalent amount of long-CoT distilled data.\n\nExtensive experiments and analysis based on three base models across both in-domain and out-of-domain benchmarks validate the effectiveness of S2R.\n\n### Publication Details\n\nThe paper was published on arXiv as arXiv:2502.12853 in 2025 by authors including Ruotian Ma, Peisong Wang, Cheng Liu, Xingyan Liu, Jiaqi Chen, Bang Zhang, Xin Zhou, Nan Du, and Jia Li. Code and data are available at https://github.com/NineAbyss/S2R."], "durationSeconds": 8.327518357000008, "searchCount": 1}
```

### [39] ASSISTANT · 2026-07-31 20:43:50 UTC

```
Now let me fetch BibTeX entries for the core citation set.
```

### [40] TOOL CALL — ToolSearch · 2026-07-31 20:43:50 UTC

```
{'query': 'semscholar', 'max_results': 10}
```

### [41] TOOL RESULT — ToolSearch · 2026-07-31 20:43:50 UTC

```
{"matches": [], "query": "semscholar", "total_deferred_tools": 22}
```

### [42] TOOL CALL — Bash · 2026-07-31 20:43:58 UTC

```
SKILL_DIR="$(git -C /home/adrian/projects/ai-inventor rev-parse --show-toplevel 2>/dev/null)/.claude/skills/aii-semscholar-bib"
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_semscholar_bib__fetch.py --refs '[
  {"arxiv": "2502.11771", "author": "Bertolazzi", "year": 2025},
  {"arxiv": "2303.17651", "author": "Madaan", "year": 2023},
  {"arxiv": "2502.12853", "author": "Ma", "year": 2025},
  {"arxiv": "2110.14168", "author": "Cobbe", "year": 2021},
  {"arxiv": "2309.11495", "author": "Dhuliawala", "year": 2023},
  {"arxiv": "2402.08115", "author": "Stechly", "year": 2024},
  {"arxiv": "2406.01297", "author": "Kamoi", "year": 2024},
  {"arxiv": "2310.01798", "author": "Huang", "year": 2023},
  {"title": "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models", "author": "Wei", "year": 2022}
]' 2>&1 | tail -100
```

### [43] TOOL RESULT — Bash · 2026-07-31 20:43:58 UTC

```
{"stdout": "Found 9/9 references\n\n@inproceedings{Bertolazzi2025,\n author = {Leonardo Bertolazzi and Philipp Mondorf and Barbara Plank and Raffaella Bernardi},\n booktitle = {Conference on Empirical Methods in Natural Language Processing},\n journal = {ArXiv},\n title = {The Validation Gap: A Mechanistic Analysis of How Language Models Compute Arithmetic but Fail to Validate It},\n volume = {abs/2502.11771},\n year = {2025},\n  doi = {10.48550/arXiv.2502.11771}\n}\n\n@inproceedings{Madaan2023,\n author = {Aman Madaan and Niket Tandon and Prakhar Gupta and Skyler Hallinan and Luyu Gao and Sarah Wiegreffe and Uri Alon and Nouha Dziri and Shrimai Prabhumoye and Yiming Yang and S. Welleck and Bodhisattwa Prasad Majumder and Shashank Gupta and A. Yazdanbakhsh and Peter Clark},\n booktitle = {Neural Information Processing Systems},\n journal = {ArXiv},\n title = {Self-Refine: Iterative Refinement with Self-Feedback},\n volume = {abs/2303.17651},\n year = {2023},\n  doi = {10.48550/arXiv.2303.17651}\n}\n\n@inproceedings{Ma2025,\n author = {Ruotian Ma and Peisong Wang and Cheng Liu and Xingyan Liu and Jiaqi Chen and Bang Zhang and Xin Zhou and Nan Du and Jia Li},\n booktitle = {Annual Meeting of the Association for Computational Linguistics},\n journal = {ArXiv},\n title = {S2R: Teaching LLMs to Self-verify and Self-correct via Reinforcement Learning},\n volume = {abs/2502.12853},\n year = {2025},\n  doi = {10.48550/arXiv.2502.12853}\n}\n\n@article{Cobbe2021,\n author = {K. Cobbe and Vineet Kosaraju and Mo Bavarian and Mark Chen and Heewoo Jun and Lukasz Kaiser and Matthias Plappert and Jerry Tworek and Jacob Hilton and Reiichiro Nakano and Christopher Hesse and John Schulman},\n booktitle = {arXiv.org},\n journal = {ArXiv},\n title = {Training Verifiers to Solve Math Word Problems},\n volume = {abs/2110.14168},\n year = {2021}\n}\n\n@inproceedings{Dhuliawala2023,\n author = {S. Dhuliawala and M. Komeili and Jing Xu and R. Raileanu and Xian Li and Asli Celikyilmaz and Jason Weston},\n booktitle = {Annual Meeting of the Association for Computational Linguistics},\n pages = {3563-3578},\n title = {Chain-of-Verification Reduces Hallucination in Large Language Models},\n year = {2023},\n  doi = {10.48550/arXiv.2309.11495}\n}\n\n@inproceedings{Stechly2024,\n author = {Kaya Stechly and Karthik Valmeekam and Subbarao Kambhampati},\n booktitle = {International Conference on Learning Representations},\n journal = {ArXiv},\n title = {On the Self-Verification Limitations of Large Language Models on Reasoning and Planning Tasks},\n volume = {abs/2402.08115},\n year = {2024},\n  doi = {10.48550/arXiv.2402.08115}\n}\n\n@inproceedings{Kamoi2024,\n author = {Ryo Kamoi and Yusen Zhang and Nan Zhang and Jiawei Han and Rui Zhang},\n booktitle = {Transactions of the Association for Computational Linguistics},\n journal = {Transactions of the Association for Computational Linguistics},\n pages = {1417-1440},\n title = {When Can LLMs Actually Correct Their Own Mistakes? A Critical Survey of Self-Correction of LLMs},\n volume = {12},\n year = {2024},\n  doi = {10.1162/tacl_a_00713}\n}\n\n@inproceedings{Huang2023,\n author = {Jie Huang and Xinyun Chen and Swaroop Mishra and Huaixiu Steven Zheng and Adams Wei Yu and Xinying Song and Denny Zhou},\n booktitle = {International Conference on Learning Representations},\n journal = {ArXiv},\n title = {Large Language Models Cannot Self-Correct Reasoning Yet},\n volume = {abs/2310.01798},\n year = {2023},\n  doi = {10.48550/arXiv.2310.01798}\n}\n\n@inproceedings{Wei2022,\n author = {Jason Wei and Xuezhi Wang and Dale Schuurmans and Maarten Bosma and Ed H. Chi and F. Xia and Quoc Le and Denny Zhou},\n booktitle = {Neural Information Processing Systems},\n journal = {ArXiv},\n title = {Chain of Thought Prompting Elicits Reasoning in Large Language Models},\n volume = {abs/2201.11903},\n year = {2022},\n  doi = {10.52202/068431-1800}\n}", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [44] ASSISTANT · 2026-07-31 20:44:16 UTC

```
All 9 references found. Now writing the paper and figures with concrete numbers, then producing structured JSON output.
```

### [45] TOOL CALL — Write · 2026-07-31 20:44:16 UTC

```
File: /home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_0WmBa7GFLIzI/3_invention_loop/iter_1/gen_paper_text/gen_paper_text/references.bib

@inproceedings{Bertolazzi2025,
 author = {Leonardo Bertolazzi and Philipp Mondorf and Barbara Plank and Raffaella Bernardi},
 booktitle = {Conference on Empirical Methods in Natural Language Processing},
 journal = {ArXiv},
 title = {The Validation Gap: A Mechanistic Analysis of How Language Models Compute Arithmetic but Fail to Validate It},
 volume = {abs/2502.11771},
 year = {2025},
  doi = {10.48550/arXiv.2502.11771}
}

@inproceedings{Madaan2023,
 author = {Aman Madaan and Niket Tandon and Prakhar Gupta and Skyler Hallinan and Luyu Gao and Sarah Wiegreffe and Uri Alon and Nouha Dziri and Shrimai Prabhumoye and Yiming Yang and S. Welleck and Bodhisattwa Prasad Majumder and Shashank Gupta and A. Yazdanbakhsh and Peter Clark},
 booktitle = {Neural Information Processing Systems},
 journal = {ArXiv},
 title = {Self-Refine: Iterative Refinement with Self-Feedback},
 volume = {abs/2303.17651},
 year = {2023},
  doi = {10.48550/arXiv.2303.17651}
}

@inproceedings{Ma2025,
 author = {Ruotian Ma and Peisong Wang and Cheng Liu and Xingyan Liu and Jiaqi Chen and Bang Zhang and Xin Zhou and Nan Du and Jia Li},
 booktitle = {Annual Meeting of the Association for Computational Linguistics},
 journal = {ArXiv},
 title = {S2R: Teaching LLMs to Self-verify and Self-correct via Reinforcement Learning},
 volume = {abs/2502.12853},
 year = {2025},
  doi = {10.48550/arXiv.2502.12853}
}

@article{Cobbe2021,
 author = {K. Cobbe and Vineet Kosaraju and Mo Bavarian and Mark Chen and Heewoo Jun and Lukasz Kaiser and Matthias Plappert and Jerry Tworek and Jacob Hilton and Reiichiro Nakano and Christopher Hesse and John Schulman},
 booktitle = {arXiv.org},
 journal = {ArXiv},
 title = {Training Verifiers to Solve Math Word Problems},
 volume = {abs/2110.14168},
 year = {2021}
}

@inproceedings{Dhuliawala2023,
 author = {S. Dhuliawala and M. Komeili and Jing Xu and R. Raileanu and Xian Li and Asli Celikyilmaz and Jason Weston},
 booktitle = {Annual Meeting of the Association for Computational Linguistics},
 pages = {3563-3578},
 title = {Chain-of-Verification Reduces Hallucination in Large Language Models},
 year = {2023},
  doi = {10.48550/arXiv.2309.11495}
}

@inproceedings{Stechly2024,
 author = {Kaya Stechly and Karthik Valmeekam and Subbarao Kambhampati},
 booktitle = {International Conference on Learning Representations},
 journal = {ArXiv},
 title = {On the Self-Verification Limitations of Large Language Models on Reasoning and Planning Tasks},
 volume = {abs/2402.08115},
 year = {2024},
  doi = {10.48550/arXiv.2402.08115}
}

@inproceedings{Kamoi2024,
 author = {Ryo Kamoi and Yusen Zhang and Nan Zhang and Jiawei Han and Rui Zhang},
 booktitle = {Transactions of the Association for Computational Linguistics},
 journal = {Transactions of the Association for Computational Linguistics},
 pages = {1417-1440},
 title = {When Can LLMs Actually Correct Their Own Mistakes? A Critical Survey of Self-Correction of LLMs},
 volume = {12},
 year = {2024},
  doi = {10.1162/tacl_a_00713}
}

@inproceedings{Huang2023,
 author = {Jie Huang and Xinyun Chen and Swaroop Mishra and Huaixiu Steven Zheng and Adams Wei Yu and Xinying Song and Denny Zhou},
 booktitle = {International Conference on Learning Representations},
 journal = {ArXiv},
 title = {Large Language Models Cannot Self-Correct Reasoning Yet},
 volume = {abs/2310.01798},
 year = {2023},
  doi = {10.48550/arXiv.2310.01798}
}

@inproceedings{Wei2022,
 author = {Jason Wei and Xuezhi Wang and Dale Schuurmans and Maarten Bosma and Ed H. Chi and F. Xia and Quoc Le and Denny Zhou},
 booktitle = {Neural Information Processing Systems},
 journal = {ArXiv},
 title = {Chain of Thought Prompting Elicits Reasoning in Large Language Models},
 volume = {abs/2201.11903},
 year = {2022},
  doi = {10.52202/068431-1800}
}
```

### [46] TOOL RESULT — Write · 2026-07-31 20:44:16 UTC

```
{"type": "create", "filePath": "/home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_0WmBa7GFLIzI/3_invention_loop/iter_1/gen_paper_text/gen_paper_text/references.bib", "content": "@inproceedings{Bertolazzi2025,\n author = {Leonardo Bertolazzi and Philipp Mondorf and Barbara Plank and Raffaella Bernardi},\n booktitle = {Conference on Empirical Methods in Natural Language Processing},\n journal = {ArXiv},\n title = {The Validation Gap: A Mechanistic Analysis of How Language Models Compute Arithmetic but Fail to Validate It},\n volume = {abs/2502.11771},\n year = {2025},\n  doi = {10.48550/arXiv.2502.11771}\n}\n\n@inproceedings{Madaan2023,\n author = {Aman Madaan and Niket Tandon and Prakhar Gupta and Skyler Hallinan and Luyu Gao and Sarah Wiegreffe and Uri Alon and Nouha Dziri and Shrimai Prabhumoye and Yiming Yang and S. Welleck and Bodhisattwa Prasad Majumder and Shashank Gupta and A. Yazdanbakhsh and Peter Clark},\n booktitle = {Neural Information Processing Systems},\n journal = {ArXiv},\n title = {Self-Refine: Iterative Refinement with Self-Feedback},\n volume = {abs/2303.17651},\n year = {2023},\n  doi = {10.48550/arXiv.2303.17651}\n}\n\n@inproceedings{Ma2025,\n author = {Ruotian Ma and Peisong Wang and Cheng Liu and Xingyan Liu and Jiaqi Chen and Bang Zhang and Xin Zhou and Nan Du and Jia Li},\n booktitle = {Annual Meeting of the Association for Computational Linguistics},\n journal = {ArXiv},\n title = {S2R: Teaching LLMs to Self-verify and Self-correct via Reinforcement Learning},\n volume = {abs/2502.12853},\n year = {2025},\n  doi = {10.48550/arXiv.2502.12853}\n}\n\n@article{Cobbe2021,\n author = {K. Cobbe and Vineet Kosaraju and Mo Bavarian and Mark Chen and Heewoo Jun and Lukasz Kaiser and Matthias Plappert and Jerry Tworek and Jacob Hilton and Reiichiro Nakano and Christopher Hesse and John Schulman},\n booktitle = {arXiv.org},\n journal = {ArXiv},\n title = {Training Verifiers to Solve Math Word Problems},\n volume = {abs/2110.14168},\n year = {2021}\n}\n\n@inproceedings{Dhuliawala2023,\n author = {S. Dhuliawala and M. Komeili and Jing Xu and R. Raileanu and Xian Li and Asli Celikyilmaz and Jason Weston},\n booktitle = {Annual Meeting of the Association for Computational Linguistics},\n pages = {3563-3578},\n title = {Chain-of-Verification Reduces Hallucination in Large Language Models},\n year = {2023},\n  doi = {10.48550/arXiv.2309.11495}\n}\n\n@inproceedings{Stechly2024,\n author = {Kaya Stechly and Karthik Valmeekam and Subbarao Kambhampati},\n booktitle = {International Conference on Learning Representations},\n journal = {ArXiv},\n title = {On the Self-Verification Limitations of Large Language Models on Reasoning and Planning Tasks},\n volume = {abs/2402.08115},\n year = {2024},\n  doi = {10.48550/arXiv.2402.08115}\n}\n\n@inproceedings{Kamoi2024,\n author = {Ryo Kamoi and Yusen Zhang and Nan Zhang and Jiawei Han and Rui Zhang},\n booktitle = {Transactions of the Association for Computational Linguistics},\n journal = {Transactions of the Association for Computational Linguistics},\n pages = {1417-1440},\n title = {When Can LLMs Actually Correct Their Own Mistakes? A Critical Survey of Self-Correction of LLMs},\n volume = {12},\n year = {2024},\n  doi = {10.1162/tacl_a_00713}\n}\n\n@inproceedings{Huang2023,\n author = {Jie Huang and Xinyun Chen and Swaroop Mishra and Huaixiu Steven Zheng and Adams Wei Yu and Xinying Song and Denny Zhou},\n booktitle = {International Conference on Learning Representations},\n journal = {ArXiv},\n title = {Large Language Models Cannot Self-Correct Reasoning Yet},\n volume = {abs/2310.01798},\n year = {2023},\n  doi = {10.48550/arXiv.2310.01798}\n}\n\n@inproceedings{Wei2022,\n author = {Jason Wei and Xuezhi Wang and Dale Schuurmans and Maarten Bosma and Ed H. Chi and F. Xia and Quoc Le and Denny Zhou},\n booktitle = {Neural Information Processing Systems},\n journal = {ArXiv},\n title = {Chain of Thought Prompting Elicits Reasoning in Large Language Models},\n volume = {abs/2201.11903},\n year = {2022},\n  doi = {10.52202/068431-1800}\n}\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [47] TOOL CALL — Write · 2026-07-31 20:44:56 UTC

```
File: /home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_0WmBa7GFLIzI/3_invention_loop/iter_1/gen_paper_text/gen_paper_text/paper_draft.md

(scratch copy of paper text and figures — see .terminal_claude_agent_struct_out.json for the actual structured output)
```

### [48] TOOL RESULT — Write · 2026-07-31 20:44:56 UTC

```
{"type": "create", "filePath": "/home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_0WmBa7GFLIzI/3_invention_loop/iter_1/gen_paper_text/gen_paper_text/paper_draft.md", "content": "(scratch copy of paper text and figures — see .terminal_claude_agent_struct_out.json for the actual structured output)\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [49] TOOL CALL — Bash · 2026-07-31 20:47:39 UTC

```
cat > /tmp/build_paper.py << 'PYEOF'
import json

title = "Checksum Critique Beats Free-Form Self-Doubt: Casting Out Nines for LLM Arithmetic Self-Correction"

abstract = (
"Large language models asked to double-check arithmetic word-problem solutions typically re-read rather than "
"re-derive their own work, so free-form self-critique catches few genuine errors. We test whether replacing "
"vague \"check your work\" prompts with an explicit, mechanically-computed invariant -- a casting-out-nines "
"(mod-9 digit-root) checksum applied to each intermediate computation step -- improves error detection and "
"final-answer accuracy more than free-form critique, and more than a matched-length placebo critique that adds "
"equally deterministic-looking text without a real invariant. We build a 1,935-row benchmark of 400 multi-step "
"arithmetic word problems (200 real GSM8K items, 200 procedurally generated items spanning 2-6 step chains and "
"controlled numeric ranges) with deterministic error-injection variants labeled checksum-detectable or "
"checksum-invisible by mod-9 residue. We then compare four self-check conditions -- no critique, free-form "
"critique, length-matched placebo critique, and checksum critique -- plus an oracle detection-isolation ablation, "
"on two LLMs via OpenRouter (anthropic/claude-haiku-4.5, openai/gpt-4o-mini) over 200 problems per model. On "
"claude-haiku-4.5, whose 76.5% no-critique baseline leaves substantial room for improvement, the checksum "
"condition reaches 97.5% overall accuracy (100% on the checksum-detectable subset), significantly outperforming "
"both free-form critique (+18.75 percentage points, Holm-adjusted p=0.04) and the matched-length placebo "
"(+9.375 percentage points, Holm-adjusted p=0.04). On gpt-4o-mini, which is already near ceiling at 95.4% "
"baseline accuracy, the four conditions are statistically indistinguishable (Holm-adjusted p=1.0 for both "
"checksum comparisons), and the placebo nominally edges out the checksum by 1 point. A stratified LLM-judge audit "
"finds models miscompute their own mod-9 checksum in 15.4% of sampled checksum-critique traces, and an oracle "
"ablation shows the model's own correction accuracy given its self-computed checksum mismatch (100% on "
"claude-haiku-4.5) already matches or exceeds the oracle-signal condition (93.75%), indicating the bottleneck is "
"not correction but reliable checksum computation and having enough baseline error margin to show a benefit at "
"all. These results support the hypothesis conditionally: an explicit numeric invariant provides a real, "
"causally isolated benefit over generic structured deliberation, but only for models with meaningful headroom "
"above ceiling; near-ceiling models gain nothing measurable from any critique strategy, including the checksum."
)

paper_text = r"""
# Introduction

Large language models (LLMs) are routinely asked to solve multi-step arithmetic word problems and then, in the same breath, to check their own work. The instruction is nearly universal in production prompting practice: "double-check your answer," "review your solution for mistakes," "verify before finalizing." The empirical record on whether this instruction does anything is much less settled. Free-form self-critique on reasoning and arithmetic tasks is documented to be unreliable, and in several studies neutral or actively harmful, because models tend to restate rather than independently re-derive their own output [1, 2, 3]. A survey of self-correction work concludes that intrinsic self-correction -- correction using only the model's own judgment, with no external signal -- rarely improves accuracy on reasoning tasks and often degrades it [3]. This leaves practitioners with a real problem: the instruction to self-check costs tokens and latency, and appears to buy little.

Understanding why self-critique fails is important because the answer determines what fix is worth trying. If self-critique fails simply because models are bad at generating additional reasoning tokens, then any structured deliberation should help equally, and the interesting engineering lever is verbosity or prompt length. If self-critique fails because it asks the model to hold two full derivations in its context and compare them from a fuzzy memory of the first pass -- a hard, error-prone cognitive operation -- then the fix is not "critique more," but "critique differently": give the model something concrete and cheap to compare against, rather than asking it to re-run its own reasoning silently and trust its own comparison.

Recent mechanistic evidence favors the second explanation. Circuit-level analysis of arithmetic-capable language models shows that their internal error-detection machinery relies on shallow surface-level numeric-consistency checks between tokens in the text, not on genuine independent recomputation of the underlying arithmetic [ARTIFACT:art_UafZp2AqR5at][4]. In other words, models already have circuitry that performs consistency checks -- but that circuitry checks superficial token-level agreement, not mathematical correctness. This diagnosis is mechanistic, not behavioral: it explains why self-critique underperforms, but it proposes no intervention and reports no accuracy numbers for any fix.

Multi-step arithmetic word problems are a natural setting to turn this diagnosis into an intervention, because they are exactly the kind of task where a genuinely independent, cheap-to-compute consistency signal has existed for centuries: the casting-out-nines checksum. Long before calculators, bookkeepers verified long multiplications and additions by reducing every operand and every result to its digit root -- the value obtained by repeatedly summing digits until one digit remains -- and checking that the same arithmetic operation applied to the digit roots reproduces the digit root of the claimed answer. Because any integer is congruent to its digit sum modulo 9, this check is a direct probe of the arithmetic's correctness modulo 9: a mismatch proves an error exists somewhere in that step; a match does not prove correctness, but it is cheap, mechanical, and structurally decoupled from the original derivation.

This checksum has an appealing property for LLM self-critique specifically: it converts error detection from a hard task (re-deriving an entire multi-step solution and comparing it, in context, to a fuzzy memory of the first attempt) into an easy, decomposable task (a single small-number digit-sum computation and a residue comparison, repeated once per step). If the mechanistic diagnosis in prior work is correct -- that models default to shallow, surface-level consistency checks rather than genuine recomputation -- then handing the model an explicit, mechanically-defined consistency check to perform should align the requested behavior with what the model's error-detection machinery is already good at, rather than what it is bad at.

The central methodological risk in testing this idea is confounding the invariant itself with the general effect of "more structured-looking deliberation text." Any critique procedure that produces additional tokens before a final answer could plausibly help through increased test-time computation alone, independent of whether those tokens encode a real error-detecting signal [ARTIFACT:art_VCF3BbfSo_RV]. We address this directly with a length-matched placebo critique: a condition that is equally long and equally deterministic-looking as the checksum critique, but whose steps do not encode a true mod-9 invariant. Any advantage of the checksum condition over this placebo isolates the causal contribution of the invariant itself, separate from the contribution of extra thinking tokens.

[FIGURE:fig1]

We evaluate four self-check conditions -- no critique (baseline), free-form critique, length-matched placebo critique, and checksum critique -- plus an oracle detection-isolation ablation that supplies a pre-computed checksum mismatch signal directly, isolating whether the bottleneck is computing the checksum or using it. We build a purpose-made 1,935-row benchmark combining 200 real GSM8K word problems with 200 procedurally generated problems and a deterministic error-injection layer that labels every corrupted variant as checksum-detectable or checksum-invisible by its true mod-9 residue, giving us a principled ceiling on what a casting-out-nines check could possibly catch. We run all four conditions on two LLMs of different baseline capability (anthropic/claude-haiku-4.5 and openai/gpt-4o-mini) via OpenRouter over 200 problems each. Our central finding is that checksum critique gives a large, statistically significant, placebo-robust improvement for the model with baseline headroom (claude-haiku-4.5: 76.5% to 97.5% overall accuracy), but no measurable benefit for the model already near ceiling (gpt-4o-mini: 95.4% baseline, all conditions statistically tied). A stratified audit further shows that even the winning condition is capped by the model's own checksum arithmetic reliability, not by its ability to act on a correct checksum once computed.

## Summary of Contributions

- A benchmark of 1,935 multi-step arithmetic word problems (400 base items: 200 real GSM8K, 200 procedurally generated) with deterministic, exactly-propagated error injections labeled checksum-detectable or checksum-invisible by ground-truth mod-9 residue, enabling a principled ceiling analysis for any digit-root-based self-check (Section 3).
- A four-condition, matched-effort experimental design -- no critique, free-form critique, length-matched placebo critique, checksum critique -- plus an oracle detection-isolation ablation, that isolates the causal contribution of the invariant itself from the confound of extra deliberation tokens (Section 4).
- Evidence that checksum critique yields a statistically significant, Holm-corrected improvement over both free-form critique (+18.75 percentage points) and the matched-length placebo (+9.375 percentage points) for a model with baseline headroom, reaching 100% accuracy on the checksum-detectable subset (Section 5).
- Evidence that this advantage disappears for a model already near ceiling, and a stratified LLM-judge audit showing the checksum condition's own internal arithmetic is unreliable in 15.4% of sampled traces, which we identify as the practical bottleneck rather than the model's ability to act on a correctly computed checksum (Section 5-6).

# Related Work

**Self-critique and self-correction of LLM reasoning.** Self-Refine established the pattern of prompting a model to iteratively critique and revise its own output without external feedback, and reported gains across a range of generation tasks [1]. Subsequent work specifically targeting reasoning and arithmetic has been substantially more pessimistic: intrinsic self-correction -- correction driven solely by the model's own judgment -- frequently fails to improve, and sometimes harms, accuracy on math and planning tasks, because models struggle to reliably detect that their own output is wrong in the first place [2, 3]. A critical survey of this literature concludes that self-correction reliably helps only when it can draw on an external signal -- a tool, a verifier, ground-truth feedback, or another model -- rather than the same model's own re-reading of its own text [3]. Our checksum condition sits inside this reliability gap: it is still generated by the same model with no external oracle, but it hands the model an explicit, mechanically-defined procedure to execute, rather than an open-ended instruction to "check." S2R shows that reinforcement-learning-trained self-verify/self-correct behavior can substantially improve math reasoning accuracy (51.0% to 81.6% on one benchmark) [ARTIFACT:art_VCF3BbfSo_RV][5], but that gain requires training; our approach is training-free and prompt-only, trading some of that ceiling for zero-shot applicability to any model accessible through an inference API.

**External verification and tool-based checking.** Training Verifiers to Solve Math Word Problems introduced GSM8K and showed that a learned verifier model, used to rerank multiple sampled solutions, substantially outperforms a single greedy generation and scales better with additional data than fine-tuning alone [6]. Chain-of-Verification reduces hallucination by having a model draft an answer, independently generate and answer verification questions, and then reconcile the two, and shows this decoupling of verification from the original generation reduces factual errors on list-based and long-form tasks [7]. Both approaches share our core design principle -- that verification should not simply re-run the same generative process and hope for a different, more careful answer, but should introduce a structurally distinct signal -- but neither targets arithmetic step-level correctness with a compact numeric invariant, and neither includes a matched-effort placebo to separate the contribution of the specific mechanism from the contribution of generating extra text.

**Mechanistic diagnosis of arithmetic self-verification failure.** The Validation Gap provides circuit-level evidence that language models' internal error-detection relies on shallow surface-level numeric-consistency heads that check superficial agreement between tokens, rather than genuine independent recomputation of the underlying arithmetic [4]. This work is purely diagnostic and mechanistic: it identifies why self-critique should be expected to fail, but proposes and evaluates no behavioral intervention. Chain-of-Thought prompting demonstrated that eliciting explicit intermediate reasoning steps substantially improves arithmetic and multi-step reasoning accuracy relative to direct answer generation [8], establishing that models can be steered toward more reliable step-by-step computation through prompt structure alone -- a premise our checksum condition extends from problem-solving to error-checking. Large Language Models Cannot Self-Correct Reasoning Yet presents a systematic empirical audit finding that self-correction without external feedback degrades performance across several reasoning benchmarks, largely because models cannot reliably tell correct output from incorrect output [2]. Our work directly operationalizes the fix implied but not tested by the mechanistic diagnosis: give the model an external-feeling, structurally independent invariant rather than asking it to introspect on its own derivation.

**Casting out nines as a checksum.** Casting out nines is a centuries-old manual bookkeeping technique for catching arithmetic slips by comparing digit-root (mod-9) residues, and is a direct ancestor of modern checksum schemes such as the Luhn algorithm used for credit-card and identifier validation. To the searches conducted for this work, it has not previously been evaluated as an explicit LLM self-verification prompting strategy for word-problem arithmetic; our contribution is the direct methodological transfer of this specific numeric invariant into LLM self-critique, evaluated against matched controls rather than assumed to help.

# Preliminaries

**Digit root / casting out nines.** The digit root of an integer is obtained by repeatedly summing its digits until a single digit (1-9, or 0 for a multiple of 9) remains. Because 10 is congruent to 1 modulo 9, every integer is congruent modulo 9 to its digit sum, and therefore to its digit root. Consequently, if two numbers are combined by addition, subtraction, or multiplication to produce a result, the same operation applied to their digit roots (with results reduced back to a single digit) must be congruent modulo 9 to the digit root of the true result. A mismatch proves an arithmetic error exists in that step; agreement is necessary but not sufficient for correctness.

**Checksum-detectable vs. checksum-invisible errors.** An injected or naturally occurring arithmetic error is checksum-detectable if it changes the mod-9 residue of the affected computation's result -- for example, most digit transpositions, dropped carries, and sign flips. An error is checksum-invisible if it leaves the mod-9 residue unchanged -- for example, a wrong-operand substitution that happens to preserve the residue, or any purely logical or modeling error (misreading the problem, applying the wrong operation to correctly-computed numbers) that does not corrupt an individual arithmetic step's residue at all. Checksum-invisible errors define a hard ceiling: no digit-root check, however well executed, can catch them.

**Free-form vs. matched-length placebo vs. checksum critique.** Free-form critique instructs the model to "re-check," "re-read," or "review" its own answer with no specified procedure. The matched-length placebo instructs the model to perform an equally long, similarly deterministic-looking review procedure that does not encode a true mod-9 invariant, controlling for the possibility that any structured-looking extra deliberation helps regardless of content. The checksum critique walks the model through computing the digit-root checksum of each arithmetic sub-step and instructs it to flag and revise a step only if the checksums disagree.

# Methods

## Benchmark Construction

We construct a benchmark of multi-step arithmetic word problems from two complementary sources [ARTIFACT:art_UafZp2AqR5at]. The first source is 200 real GSM8K word problems (openai/gsm8k, main configuration, pooled train and test splits), whose official calculator-annotation reasoning traces are parsed via regex over the `<<operand op operand=result>>` annotations into explicit step traces (operand_1, operand_2, operation, result, depends_on_step), filtered to chain lengths of 2-6 steps and cross-checked so that the final trace step matches the problem's stated `#### answer`. The second source is 200 procedurally generated synthetic word problems drawn from five templates (shopping, recipe-scaling, distance-rate-time, unit-conversion, inventory-accounting) with computation traces emitted directly by the generator, which guarantees clean coverage of long chains (5-6 steps) and large numbers (greater than or equal to 100) that GSM8K under-represents. Both sources are stratified across a 5 (chain length) by 2 (numeric range) grid with 20 items per cell, for 400 base items.

On top of these 400 base items, a deterministic error-injection layer adds up to four corrupted variants per base item, drawn from digit transposition, dropped carry, sign flip, and wrong-operand substitution. Each corruption is injected at a single step and propagated through every downstream step that depends on it via exact re-derivation (not estimation), producing an internally consistent corrupted trace and a corrupted final answer. Each variant is labeled checksum-detectable or checksum-invisible according to whether the mod-9 residue of the corrupted final answer differs from or matches the correct final answer's residue. An error type is skipped for a given item, and logged rather than force-fit, when it cannot be structurally applied (for example, sign flip requires an addition/subtraction step) or when the corruption does not propagate to the final answer. This yields 1,935 total rows -- 400 base items plus 1,535 corrupted variants, an approximately 8% skip rate -- split 80/20 into train and test folds. All arithmetic in the dataset, both original and corrupted-and-propagated, was independently re-derived and verified with zero inconsistencies across all 1,935 rows by a standalone regex-based checker that recomputes every step from the rendered problem text and cross-checks it against the recorded metadata.

## Experimental Conditions

We compare five conditions on each of 200 (uncorrupted) word problems per model, using OpenRouter to query each LLM at matched sampling settings [ARTIFACT:art_VCF3BbfSo_RV]:

1. **Baseline (no self-check).** The model produces a solution with no critique step.
2. **Free-form critique.** After producing an initial solution, the model is asked to "check your work" with no specified procedure, and may revise its answer.
3. **Placebo critique.** The model performs a length-matched, similarly deterministic-looking review procedure that does not encode a true mod-9 invariant, controlling for the confound that any additional structured deliberation tokens could help independent of content.
4. **Checksum critique.** The model is walked through computing the digit-root checksum for each arithmetic sub-step of its own solution and is instructed to flag and revise a step only if the checksums disagree.
5. **Oracle detection-isolation ablation.** Restricted to the checksum-detectable subset, the model is given an already-computed checksum mismatch signal externally (rather than computing it itself) and asked whether it can use that signal to fix the flagged step, isolating "can the model use a checksum" from "can the model compute one."

We measure five families of metrics: (a) final-answer accuracy per model and condition, with Wilson 95% confidence intervals, reported overall and split by checksum-detectable and checksum-invisible subsets; (b) error-detection precision, recall, and F1, built from whether a condition flagged an error against whether the model's own unedited initial answer actually differed from the ground-truth answer; (c) correction accuracy conditional on a flag being raised; (d) the oracle-vs-self-computed-checksum fix-rate gap; and (e) paired significance testing -- exact McNemar tests where the number of discordant pairs is sufficient, otherwise a 10,000-resample bootstrap confidence interval on the accuracy difference -- on the checksum-detectable subset for checksum-vs-freeform and checksum-vs-placebo, with Holm-Bonferroni correction applied across the full family of per-model, per-pair comparisons. We additionally regress correctness on condition dummies plus standardized response length in a dependency-free logistic regression to check whether any accuracy gap is explained by prompt length alone, and report the placebo-to-checksum response-length ratio directly. Finally, an LLM-judge audit (judge model anthropic/claude-haiku-4.5, prompted to independently recompute each digit-root check before issuing a verdict) is run over a stratified sample of checksum-condition traces per model to measure how often the evaluated model's own checksum arithmetic is itself incorrect, since a checksum the model cannot reliably compute cannot deliver its theoretical benefit regardless of how well the model uses a correctly computed one.

# Results

[FIGURE:fig2]

For anthropic/claude-haiku-4.5, whose no-critique baseline accuracy is 76.5% (n=200, 95% Wilson CI [70.2%, 81.8%]) -- leaving substantial headroom below ceiling -- self-check condition matters a great deal. Free-form critique raises accuracy modestly to 80.5% ([74.5%, 85.4%]). The matched-length placebo raises it further, to 91.0% ([86.2%, 94.2%]), confirming that generic structured deliberation carries real value independent of any specific invariant. The checksum critique raises accuracy the most, to 97.5% overall ([94.3%, 98.9%]), and reaches 100% (n=64, [94.3%, 100%]) on the checksum-detectable subset -- every injected-error-equivalent case that a mod-9 residue check could in principle catch is resolved. On the checksum-invisible subset (n=136), checksum critique still reaches 96.3% ([91.7%, 98.4%]), ahead of the placebo's 91.2% and the baseline's 75.7% on that same subset, even though checksum-invisible errors are by construction not catchable by a mod-9 check -- indicating the checksum framing carries some benefit beyond pure invariant-catching, plausibly by inducing a more careful, decomposed re-derivation of each step even where the residue check itself cannot flag an error.

These claude-haiku-4.5 gaps are statistically robust after correction for multiple comparisons. On the checksum-detectable subset, checksum critique beats free-form critique by 18.75 percentage points (Holm-adjusted p=0.04) and beats the placebo by 9.375 percentage points (Holm-adjusted p=0.04). Correction accuracy conditional on a flag being raised is 100% for the checksum condition versus 80% for free-form critique, indicating that once claude-haiku-4.5 flags a step via checksum mismatch, it reliably repairs it.

[FIGURE:fig3]

For openai/gpt-4o-mini, the picture inverts. Baseline accuracy is already 95.4% (n=195, [91.5%, 97.6%]), leaving little room for any self-check condition to demonstrate an advantage. Free-form critique is nominally slightly worse, at 93.8% ([89.6%, 96.4%]). The placebo reaches the highest accuracy of any condition, 97.4% ([94.1%, 98.9%]), and the checksum condition reaches 96.4% ([92.7%, 98.2%]) -- essentially tied with the placebo and statistically indistinguishable from both free-form critique (Holm-adjusted p=1.0, effect -1.67 percentage points) and the placebo (Holm-adjusted p=1.0, effect 0.0 percentage points). On the checksum-detectable subset specifically, placebo and checksum are exactly tied at 96.7% (n=60). Correction accuracy conditional on a flag is 100% for both free-form and checksum critique on this model.

## Oracle Detection-Isolation Ablation

We separate "can the model compute a checksum" from "can the model use one" by comparing the checksum condition's own correction accuracy against an oracle condition in which the checksum mismatch is supplied externally rather than self-computed, on the checksum-detectable subset. For claude-haiku-4.5, the oracle condition's fix rate is 93.75% (n=64), while the checksum condition's own correction accuracy given its self-detected flag is 100% -- a fix-rate gap of -6.25 percentage points, meaning claude-haiku-4.5's self-computed checksum condition is if anything more effective than the externally-supplied-signal condition on this subset, not less. For gpt-4o-mini, the oracle fix rate is 96.7%, versus the checksum condition's own correction accuracy of 100% (fix-rate gap -3.3 percentage points), the same qualitative pattern. This indicates that, for both models, correction given a genuine flag is not the bottleneck: once either model has a correctly detected mismatch in hand -- whether self-computed or externally supplied -- it can act on it reliably.

## Checksum Self-Computation Reliability and the Length Confound

[FIGURE:fig4]

If correction is not the bottleneck, the natural remaining bottleneck is the reliability of the checksum computation itself. A stratified LLM-judge audit over 80 sampled checksum-condition traces, in which the judge independently recomputes each digit-root check before issuing a verdict, finds that models miscompute their own mod-9 checksum in 15.4% of sampled traces. This means roughly one in six or seven checksum-critique episodes contains an arithmetic error in the check itself, which can produce a false pass (a real error survives because the checksum was miscalculated to agree) or a false alarm (a correct step is needlessly revised because the checksum was miscalculated to disagree). This computation-reliability ceiling is a direct, practical limit on how much of the checksum method's theoretical advantage is realized in practice, and helps explain why claude-haiku-4.5's checksum-detectable accuracy, while reaching 100% in this sample, is not guaranteed to hold at larger scale or on harder problems where checksum arithmetic itself is more error-prone.

We also rule out response length as the sole driver of claude-haiku-4.5's checksum-vs-placebo gap. The placebo-to-checksum response-length ratio is 1.048 for claude-haiku-4.5 (the placebo is, if anything, slightly longer than the checksum critique) and 0.826 for gpt-4o-mini (the placebo is shorter). Since claude-haiku-4.5's checksum condition outperforms its length-matched-or-longer placebo by 9.375 percentage points on the checksum-detectable subset, this gap cannot be attributed to the checksum condition simply producing more deliberation tokens; the placebo already matches or exceeds it in length. The dependency-free logistic regression of correctness on condition dummies plus standardized response length is consistent with this: condition membership, not response length, is the dominant predictor of correctness for claude-haiku-4.5.

## Detection Precision and Recall: A Design Limitation

We designed error-detection precision and recall to be computed from whether a condition's flag agreed with whether the model's own unedited initial answer actually differed from the correct answer -- the only ground-truth-adjacent signal available, since this experiment solves each problem's original, uncorrupted statement rather than an error-injected variant. In practice, initial-answer errors were rare for both models (most acutely for gpt-4o-mini, whose 95.4% baseline leaves few true-positive cases at all), which left most computed recall and precision values undefined or trivially zero across conditions. We report this candidly as a design limitation rather than obscuring it: a properly powered detection precision/recall analysis requires running the critique conditions directly on the error-injection variants in the benchmark [ARTIFACT:art_UafZp2AqR5at], where ground-truth error status is known by construction, rather than inferring it indirectly from whether an uncorrupted problem happened to be solved incorrectly on the first pass. We flag this as the highest-priority extension for follow-up work rather than presenting an underpowered detection metric as if it were conclusive.

# Discussion

Our results support the core hypothesis, but conditionally rather than unconditionally: an explicit, mechanically-computed invariant is not merely "more thinking" dressed up as a specific procedure. For claude-haiku-4.5, the checksum condition beats a placebo matched for length and deterministic appearance by a statistically significant 9.375 percentage points on the checksum-detectable subset, after Holm-Bonferroni correction, with the placebo's response length if anything slightly exceeding the checksum condition's. This is the strongest possible evidence within our design that the content of the invariant matters, not just the presence of extra structured text -- precisely the causal question a matched-effort placebo is meant to answer, and one largely absent from prior self-critique studies [1, 2, 3].

At the same time, the second model tested shows no such benefit. gpt-4o-mini's 95.4% no-critique baseline leaves at most 4.6 percentage points of headroom to demonstrate any improvement, and none of the three critique conditions distinguish themselves from baseline or from each other at a level surviving multiple-comparison correction. This is not evidence against the mechanism -- a checksum cannot improve on answers that are already correct -- but it is an important scope condition: the benefit of checksum critique, as measured here, appears concentrated in the regime where a model's unaided arithmetic error rate is non-trivial. Practitioners deploying a stronger, already highly accurate model should not expect the same gains reported here for a weaker one, and any claim of a "free-lunch" reliability boost applicable to "any LLM-based arithmetic pipeline," as originally motivated, needs this caveat: the free lunch is available primarily where the model is hungry.

The oracle ablation clarifies where remaining error lives. Because self-computed correction accuracy already matches or exceeds the externally-supplied-signal oracle condition for both models, the bottleneck is not "can the model act on a checksum mismatch" -- both models are already excellent at that -- but "can the model compute the checksum correctly in the first place." The 15.4% checksum self-computation error rate found by the independent LLM-judge audit is therefore the most actionable lever for future work: even a training-free intervention that improved checksum-arithmetic reliability (for example, restricting digit-root computation to very short numeric strings, or externally validating the checksum computation with a lightweight parser before letting the model act on it) could plausibly push the checksum condition's advantage further, since correction given a valid signal is essentially solved already.

We surface two further limitations candidly rather than minimizing them. First, the detection precision/recall analysis was underpowered by design, because the experiment solved uncorrupted problems rather than the benchmark's own error-injection variants; a direct evaluation of detection on the labeled checksum-detectable/checksum-invisible variants is a natural and higher-priority next step than anything reported here. Second, our evaluation covers two models over 200 problems each at the time of writing; the underlying experiment was still executing toward a third model and a larger budget when this evaluation was generated [ARTIFACT:art_VCF3BbfSo_RV], and the two-model comparison, while internally consistent and individually well-powered per model (Wilson CIs on the order of five to ten percentage points), should not be read as establishing a general capability-dependent trend across the full space of LLMs without further replication.

# Conclusion

Replacing an open-ended "check your work" instruction with an explicit, mechanically-computed casting-out-nines checksum produces a large, causally isolated, statistically significant improvement in multi-step arithmetic accuracy for a model with meaningful baseline error margin -- claude-haiku-4.5 rises from 76.5% to 97.5% overall accuracy, and to a perfect 100% on the subset of errors the checksum can in principle catch, beating both free-form critique and a length-matched placebo after multiple-comparison correction. This same intervention shows no measurable benefit for a model already near ceiling, and an oracle ablation combined with an independent computation audit locates the practical limiting factor not in the model's ability to use a checksum, but in its ability to compute one reliably: models miscompute their own mod-9 check in roughly one of every six to seven checksum-critique episodes. The mechanistic diagnosis that motivated this work -- that LLM self-critique defaults to shallow surface-level consistency checks rather than genuine recomputation [4] -- is therefore only half the story for building a practical fix: giving the model a genuinely independent, structurally decoupled invariant to check helps substantially where there is room to help, but the reliability of computing that invariant, not merely its structural independence, ultimately bounds how much of its promise is realized.

Future work should prioritize, in order: (1) running the four critique conditions directly on this benchmark's error-injection variants, where ground-truth error and checksum-detectability labels are known by construction, to obtain a properly powered detection precision/recall analysis rather than the underpowered proxy used here; (2) extending the model panel to the additional third model already in progress at the time of this evaluation and to models spanning a wider capability and baseline-error-rate range, to map how the checksum advantage scales with a model's unaided error rate; and (3) testing whether externally validating (rather than trusting) the model's self-computed checksum -- for example with a lightweight parser -- closes the 15.4% checksum-computation error rate and further widens the observed advantage.

# References

[1] A. Madaan, N. Tandon, P. Gupta, et al. Self-Refine: Iterative Refinement with Self-Feedback. NeurIPS, 2023.

[2] J. Huang, X. Chen, S. Mishra, H. S. Zheng, A. W. Yu, X. Song, D. Zhou. Large Language Models Cannot Self-Correct Reasoning Yet. ICLR, 2023.

[3] R. Kamoi, Y. Zhang, N. Zhang, J. Han, R. Zhang. When Can LLMs Actually Correct Their Own Mistakes? A Critical Survey of Self-Correction of LLMs. Transactions of the Association for Computational Linguistics, 12, 2024.

[4] L. Bertolazzi, P. Mondorf, B. Plank, R. Bernardi. The Validation Gap: A Mechanistic Analysis of How Language Models Compute Arithmetic but Fail to Validate It. EMNLP, 2025.

[5] R. Ma, P. Wang, C. Liu, et al. S2R: Teaching LLMs to Self-verify and Self-correct via Reinforcement Learning. ACL, 2025.

[6] K. Cobbe, V. Kosaraju, M. Bavarian, et al. Training Verifiers to Solve Math Word Problems. arXiv:2110.14168, 2021.

[7] S. Dhuliawala, M. Komeili, J. Xu, R. Raileanu, X. Li, A. Celikyilmaz, J. Weston. Chain-of-Verification Reduces Hallucination in Large Language Models. ACL Findings, 2023.

[8] J. Wei, X. Wang, D. Schuurmans, M. Bosma, E. H. Chi, F. Xia, Q. Le, D. Zhou. Chain of Thought Prompting Elicits Reasoning in Large Language Models. NeurIPS, 2022.

[9] K. Stechly, K. Valmeekam, S. Kambhampati. On the Self-Verification Limitations of Large Language Models on Reasoning and Planning Tasks. ICLR, 2024.
"""

figures = [
{
 "id": "fig1",
 "title": "Four Self-Check Conditions Pipeline",
 "caption": "End-to-end experimental pipeline: an initial solution is produced for each of the 200 word problems per model, then routed through one of four self-check conditions (no critique, free-form critique, length-matched placebo critique, checksum critique) plus a separate oracle detection-isolation branch that supplies a pre-computed checksum mismatch signal externally on the checksum-detectable subset.",
 "image_gen_detailed_description": "Horizontal flow diagram, left to right, aspect ratio 21:9, clean white background, sans-serif font, no 3D effects. Start box: 'Word Problem' (gray) with subtext '200 problems x 2 models'. Arrow to box 'Initial Solution' (blue). From 'Initial Solution', four parallel arrows fan out downward to four labeled boxes in a row: 'Baseline: No Critique' (gray), 'Free-form Critique: check your work' (orange), 'Placebo Critique: length-matched, no real invariant' (purple), 'Checksum Critique: mod-9 digit-root check per step' (green, highlighted with thicker border). Each of these four boxes has an arrow flowing right into a shared box labeled 'Final Answer'. Below the 'Checksum Critique' box, a dashed arrow branches down to a fifth box labeled 'Oracle Ablation: externally-supplied checksum mismatch signal (checksum-detectable subset only, n=64 claude-haiku-4.5 / n=60 gpt-4o-mini)' (teal, dashed border) which also flows into 'Final Answer'. Small annotation near the checksum critique box: 'digit root = repeated digit sum; mod 9 residue comparison per arithmetic step'. Overall style: clean rectangular boxes, rounded corners, thin black arrows, minimal color palette (gray, blue, orange, purple, green, teal).",
 "summary": "Shows the five experimental branches (baseline, free-form, placebo, checksum, oracle) all evaluated against the same 200 word problems per model."
},
{
 "id": "fig2",
 "title": "Accuracy Gains on claude-haiku-4.5",
 "caption": "Final-answer accuracy for anthropic/claude-haiku-4.5 across the four self-check conditions, split overall and by checksum-detectable / checksum-invisible subsets. Checksum critique reaches 100% on the checksum-detectable subset and significantly outperforms both free-form critique (+18.75pp, Holm-adjusted p=0.04) and the length-matched placebo (+9.375pp, Holm-adjusted p=0.04) on that subset.",
 "image_gen_detailed_description": "Grouped bar chart, aspect ratio 16:9, white background, sans-serif font. Title: 'claude-haiku-4.5: Final-Answer Accuracy by Condition'. X-axis has 3 groups: 'Overall (n=200)', 'Checksum-Detectable (n=64)', 'Checksum-Invisible (n=136)'. Within each group, 4 bars in this order and these colors: 'Baseline' (gray) , 'Free-form Critique' (orange), 'Placebo Critique' (purple), 'Checksum Critique' (green, slightly thicker outline to highlight). Y-axis: 'Final-Answer Accuracy (%)', range 0 to 100, gridlines every 10. Exact bar values: Overall group: Baseline=76.5, Free-form=80.5, Placebo=91.0, Checksum=97.5. Checksum-Detectable group: Baseline=78.1, Free-form=81.25, Placebo=90.6, Checksum=100.0. Checksum-Invisible group: Baseline=75.7, Free-form=80.1, Placebo=91.2, Checksum=96.3. Add thin black 95% Wilson CI error bars: Overall Baseline [70.2,81.8], Free-form [74.5,85.4], Placebo [86.2,94.2], Checksum [94.3,98.9]; Checksum-Detectable Baseline [66.6,86.5], Free-form [70.0,88.9], Placebo [81.0,95.6], Checksum [94.3,100]; Checksum-Invisible Baseline [67.9,82.2], Free-form [72.7,86.0], Placebo [85.2,94.9], Checksum [91.7,98.4]. Legend in top-right showing the 4 condition colors.",
 "summary": "Checksum critique dominates all other conditions for claude-haiku-4.5, reaching 100% on checksum-detectable errors."
},
{
 "id": "fig3",
 "title": "No Advantage on Near-Ceiling gpt-4o-mini",
 "caption": "Final-answer accuracy for openai/gpt-4o-mini across the four self-check conditions. With a 95.4% baseline, all conditions are statistically indistinguishable (Holm-adjusted p=1.0 for checksum-vs-freeform and checksum-vs-placebo), illustrating a ceiling effect that caps any observable benefit from either the checksum or the placebo.",
 "image_gen_detailed_description": "Grouped bar chart, aspect ratio 16:9, white background, sans-serif font. Title: 'gpt-4o-mini: Final-Answer Accuracy by Condition'. X-axis has 3 groups: 'Overall (n=195)', 'Checksum-Detectable (n=61)', 'Checksum-Invisible (n=134)'. Within each group, 4 bars in this order and colors: 'Baseline' (gray), 'Free-form Critique' (orange), 'Placebo Critique' (purple), 'Checksum Critique' (green). Y-axis: 'Final-Answer Accuracy (%)', range 85 to 100 (zoomed in to show small differences), gridlines every 2.5. Exact bar values: Overall group: Baseline=95.4, Free-form=93.8, Placebo=97.4, Checksum=96.4. Checksum-Detectable group (n=61 baseline/freeform, n=60 placebo/checksum): Baseline=95.1, Free-form=95.1, Placebo=96.7, Checksum=96.7. Checksum-Invisible group (n=134 baseline, n=133 placebo, n=132 checksum): Baseline=95.5, Free-form=93.3, Placebo=97.7, Checksum=96.2. Add thin black 95% Wilson CI error bars: Overall Baseline [91.5,97.6], Free-form [89.6,96.4], Placebo [94.1,98.9], Checksum [92.7,98.2]. Legend in top-right showing the 4 condition colors. Add a small annotation text box: 'All pairwise checksum comparisons: Holm-adjusted p = 1.0'.",
 "summary": "All four conditions cluster tightly around 94-97% for gpt-4o-mini, showing no significant checksum advantage when baseline accuracy is already near ceiling."
},
{
 "id": "fig4",
 "title": "What Limits the Checksum Advantage",
 "caption": "Three-panel diagnostic: (a) checksum self-computation error rate audited by an independent LLM judge, (b) response-length ratio between the placebo and checksum conditions per model (ruling out a pure length confound), and (c) Holm-adjusted statistical significance and percentage-point effect sizes for checksum vs. free-form and checksum vs. placebo, per model.",
 "image_gen_detailed_description": "Three-panel dense chart, aspect ratio 4:3, white background, sans-serif font, panels stacked vertically or in an L-shape, each panel clearly labeled (a), (b), (c). Panel (a) 'Checksum Self-Computation Error Rate': single horizontal bar chart with one bar labeled 'Audited checksum traces (n=80, stratified across both models)' at value 15.4%, red/orange color, x-axis 0-30%, with annotation 'models miscompute their own mod-9 check in ~1 of every 6-7 traces'. Panel (b) 'Placebo:Checksum Response-Length Ratio': grouped bar chart, x-axis two models 'claude-haiku-4.5' and 'gpt-4o-mini', y-axis 'Length Ratio (placebo / checksum)' range 0 to 1.2 with a horizontal dashed reference line at 1.0 labeled 'equal length'. Bar values: claude-haiku-4.5 = 1.048 (blue bar, placebo slightly longer), gpt-4o-mini = 0.826 (blue bar, placebo shorter). Panel (c) 'Holm-Adjusted Significance and Effect Size (checksum-detectable subset)': grouped bar chart, x-axis 4 comparisons: 'claude-haiku-4.5: freeform vs checksum', 'claude-haiku-4.5: placebo vs checksum', 'gpt-4o-mini: freeform vs checksum', 'gpt-4o-mini: placebo vs checksum'. Two bars per group: 'Effect size (percentage points, checksum advantage)' (green bar) and 'Holm-adjusted p-value x100 for scale' (gray bar). Values: claude-haiku-4.5 freeform-vs-checksum: effect=18.75, p=0.04 (starred, significant, annotate with asterisk); claude-haiku-4.5 placebo-vs-checksum: effect=9.375, p=0.04 (starred, significant); gpt-4o-mini freeform-vs-checksum: effect=1.67, p=1.0 (not significant); gpt-4o-mini placebo-vs-checksum: effect=0.0, p=1.0 (not significant). Use green for significant comparisons and gray for non-significant ones.",
 "summary": "Shows the checksum condition's own arithmetic reliability (84.6% correct) as the practical ceiling, confirms the claude-haiku-4.5 advantage is not a length artifact, and summarizes which comparisons survive multiple-comparison correction."
}
]

summary = (
"We tested whether an explicit casting-out-nines (mod-9 digit-root) checksum beats free-form self-critique for "
"catching LLM arithmetic errors, using a matched-length placebo to isolate the invariant's causal contribution "
"from generic extra deliberation. On claude-haiku-4.5 (76.5% baseline), checksum critique reached 97.5% overall "
"(100% on checksum-detectable errors), significantly beating both free-form critique (+18.75pp, p=0.04) and the "
"placebo (+9.375pp, p=0.04) after Holm correction. On the near-ceiling gpt-4o-mini (95.4% baseline), all "
"conditions were statistically indistinguishable. An oracle ablation and independent audit show correction is "
"not the bottleneck (near-100% fix rates once a mismatch is flagged) but the model's own checksum computation is "
"unreliable in 15.4% of traces -- support for the hypothesis is real but conditional on the model having "
"baseline error margin to close."
)

out = {
    "title": title,
    "abstract": abstract,
    "paper_text": paper_text,
    "figures": figures,
    "summary": summary,
}

with open("./.terminal_claude_agent_struct_out.json", "w") as f:
    json.dump(out, f, indent=2, ensure_ascii=False)

print("wrote", len(paper_text), "chars of paper_text")
print("figures:", [f["id"] for f in figures])
PYEOF
cd /home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_0WmBa7GFLIzI/3_invention_loop/iter_1/gen_paper_text/gen_paper_text
python3 /tmp/build_paper.py
```

### [50] TOOL RESULT — Bash · 2026-07-31 20:47:39 UTC

```
{"stdout": "wrote 34160 chars of paper_text\nfigures: ['fig1', 'fig2', 'fig3', 'fig4']", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [51] ASSISTANT · 2026-07-31 20:47:43 UTC

```
Now let me verify the JSON output is valid and clean up the scratch file.
```

### [52] TOOL CALL — Bash · 2026-07-31 20:47:43 UTC

```
cd /home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_0WmBa7GFLIzI/3_invention_loop/iter_1/gen_paper_text/gen_paper_text
python3 -c "
import json
d = json.load(open('./.terminal_claude_agent_struct_out.json'))
print('keys:', list(d.keys()))
print('title:', d['title'])
import re
markers = set(re.findall(r'\[FIGURE:(\w+)\]', d['paper_text']))
fig_ids = set(f['id'] for f in d['figures'])
print('markers:', markers)
print('fig ids:', fig_ids)
print('match:', markers == fig_ids)
"
rm -f /home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_0WmBa7GFLIzI/3_invention_loop/iter_1/gen_paper_text/gen_paper_text/paper_draft.md
```

### [53] TOOL RESULT — Bash · 2026-07-31 20:47:43 UTC

```
{"stdout": "keys: ['title', 'abstract', 'paper_text', 'figures', 'summary']\ntitle: Checksum Critique Beats Free-Form Self-Doubt: Casting Out Nines for LLM Arithmetic Self-Correction\nmarkers: {'fig2', 'fig1', 'fig3', 'fig4'}\nfig ids: {'fig2', 'fig1', 'fig3', 'fig4'}\nmatch: True", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [54] ASSISTANT · 2026-07-31 20:47:48 UTC

```
The paper draft is complete and validated. Summary of what was produced:

- **`.terminal_claude_agent_struct_out.json`** — full structured output with title, abstract, paper body (Intro/Related Work/Preliminaries/Methods/Results/Discussion/Conclusion/References), 4 figure specs, and summary.
- **`references.bib`** — 9 real BibTeX entries fetched from Semantic Scholar (Self-Refine, Validation Gap, S2R, GSM8K, Chain-of-Verification, Chain-of-Thought, two self-correction surveys).

Key finding reported honestly, not spun: the checksum critique gives a large, statistically significant, placebo-robust win on claude-haiku-4.5 (76.5%→97.5%, 100% on checksum-detectable errors, p=0.04 after Holm correction vs. both baselines), but no measurable benefit on the near-ceiling gpt-4o-mini (95.4% baseline). The oracle ablation and LLM-judge audit pinpoint the real bottleneck as the model's own 15.4% checksum-computation error rate, not its ability to act on a correct checksum — and the detection precision/recall design limitation (few true-positive cases in the uncorrupted-problem setup) is flagged explicitly as future work rather than glossed over.
```
