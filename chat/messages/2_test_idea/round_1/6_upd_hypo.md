# upd_hypo — test_idea

> Phase: `invention_loop` · round 1 · `upd_hypo`
> Run: `run_0WmBa7GFLIzI` — Checksum Self-Critique Helps Weak Arithmetic, Hurts Weak Models
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `upd_hypo` (terminal_claude_agent, claude-sonnet-5)

### [1] CONFIG · 2026-07-31 20:49:15 UTC

```
model: claude-sonnet-5 | effort: low | permission: bypassPermissions | cwd: /home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_0WmBa7GFLIzI/3_invention_loop/iter_1/upd_hypo/upd_hypo
```

### [2] SYSTEM-USER prompt · 2026-07-31 20:49:22 UTC

````
<ai_inventor_context>
<ai_inventor_summary>
You are one of many LLMs in AI Inventor — an automated research system that generates NOVEL and FEASIBLE hypotheses, investigates them through experiments and research, and produces a paper.

Your output feeds other LLMs downstream. This demands your ABSOLUTE MAXIMUM reasoning — every output must be deeply thought out and maximally useful. Surface-level responses waste downstream computation.
</ai_inventor_summary>

<your_role>
YOU ARE: A hypothesis reviser (Step 3.6: UPD_HYPO in the invention loop)

You received the current hypothesis, all artifacts, and the paper draft.
Revise the hypothesis based on what the evidence supports.

Honest revision → focused research. Inflated confidence → wasted iteration.
</your_role>
</ai_inventor_context>

You are revising a research hypothesis based on empirical evidence gathered
during an iterative invention loop. Your role is internal reflection — honest
assessment of what the evidence supports.

SCOPE: Your ONLY output is the revised hypothesis text. You do NOT run code,
produce artifacts, fix bugs, or otherwise act on the evidence yourself — the
next iteration of the invention loop will spawn fresh artifacts based on your
revised hypothesis. Reflect on the evidence and rewrite the hypothesis;
nothing else.

PRINCIPLES:
- Ground every revision in specific artifacts and results
- Treat negative and null results as valuable contributions. If the original
  approach failed, the null result IS often the contribution — frame it as
  such (e.g. "X does not improve Y under conditions Z"). Only pivot to a
  different positive claim when the evidence actually supports one; never
  fabricate a positive narrative to mask a failed approach.
- Increase specificity as evidence accumulates
- Don't inflate confidence without strong evidence
- Preserve the core AII prompt unless evidence clearly contradicts it
- Revise hypothesis text only — never attempt to address feedback by running
  code, proposing fixes, or producing artifacts; the next loop iteration
  handles all artifact generation

<current_hypothesis>
The hypothesis as it stands. Revise it based on the evidence below.

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
</current_hypothesis>

<all_artifacts>
Complete set of research artifacts across all iterations.

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
These 2 artifacts were created THIS iteration.

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
</new_artifacts_this_iteration>

<current_paper>
The paper draft from this iteration — represents the current state of the research story.


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

</current_paper>

<reviewer_feedback>
Feedback from the paper reviewer this iteration.

- [MAJOR] (scope) The paper's central scaling claim ('benefit concentrated where the model is hungry') is drawn from exactly two models, and the paper explicitly states the underlying experiment 'was still executing toward a third model and a larger budget when this evaluation was generated.' A two-point comparison cannot establish a trend, and submitting with an admittedly incomplete run undermines confidence in the paper's readiness.
  Action: Either wait for the third model's run to complete and include it before submission, or rewrite the abstract/contributions/discussion to explicitly frame the finding as a two-model pilot observation, not a general capability-dependent trend, removing language like 'the free lunch is available primarily where the model is hungry' until backed by more than two data points.
- [MAJOR] (evidence) The paper's own detection precision/recall/F1 metric — one of the five metric families promised in Methods — is reported to have produced 'undefined or trivially zero' values for most conditions because the experiment ran on uncorrupted problems rather than the benchmark's labeled error-injection variants. This means a core piece of the promised evaluation is essentially non-functional in the current draft, despite a benchmark built specifically to support it.
  Action: Re-run the four critique conditions directly on the 1,535 labeled error-injection variants (already built and verified in the dataset artifact) before submission — this is a bounded, already-designed experiment, not new benchmark construction, and would convert an admitted weakness into one of the paper's strongest pieces of evidence.
- [MAJOR] (methodology) The checksum self-computation reliability audit — the paper's proposed explanation for the practical bottleneck — uses claude-haiku-4.5 as the judge model, which is also one of the two evaluated models. Using a model to audit its own arithmetic reliability (even on different traces) is a potential source of correlated bias (shared blind spots, consistent misjudgment of the same error types) that the paper does not discuss or control for.
  Action: Cross-validate the audit with a judge from a different model family (e.g., GPT-4o or a lightweight deterministic parser, since digit-root checks are fully mechanical and can be verified with a regex/arithmetic script rather than an LLM judge at all), and report agreement between the LLM-judge and the deterministic checker.
- [MINOR] (evidence) claude-haiku-4.5's no-critique baseline accuracy of 76.5% on this benchmark (a mix of real GSM8K and procedurally generated problems) is notably lower than commonly reported GSM8K accuracies for comparable current-generation models, which are often well above 90%. The paper does not discuss why baseline accuracy is this low, leaving open whether the drop is driven by the harder procedurally-generated half of the benchmark, an answer-parsing artifact, or something else.
  Action: Report baseline accuracy separately for the real-GSM8K-derived items vs. the procedurally generated items, so a reader can judge whether the low baseline reflects genuine task difficulty (procedural problems being harder) or a benchmark/parsing artifact that could also be inflating the apparent checksum benefit.
- [MINOR] (rigor) Two different effect sizes on the checksum-detectable subset for claude-haiku-4.5 (18.75pp vs free-form, 9.375pp vs placebo) are both reported at exactly the same Holm-adjusted p-value (p=0.04), which is a coincidence worth explaining rather than leaving unaddressed, since it can otherwise read as a reporting or computation error.
  Action: Report the pre-correction p-values and the exact test statistic (McNemar discordant-pair counts or bootstrap CI bounds) for each comparison in a supplementary table so readers can verify the two corrected p-values are independently derived rather than duplicated.
- [MINOR] (clarity) The exact prompt wording for the free-form, placebo, and checksum critique conditions is never shown in the paper, making it impossible for a reader to independently judge whether the placebo condition is genuinely 'similarly deterministic-looking' but content-null, which is the paper's key methodological claim.
  Action: Add an appendix (or supplementary artifact reference) with the verbatim prompt template for all three critique conditions, ideally with one annotated example transcript per condition.
- [MINOR] (clarity) Reference [9] (Stechly, Valmeekam, Kambhampati, ICLR 2024) appears in the reference list but is never cited anywhere in the body text, which is easy for a copy-editing pass or reviewer to flag as an unused/orphan citation.
  Action: Either cite [9] where relevant (it is directly on-topic for the Related Work self-verification-limitations discussion and could strengthen the pessimistic-prior-work framing alongside [2] and [3]) or remove it from the reference list.
- [MINOR] (methodology) gpt-4o-mini's baseline is reported over n=195 rather than the stated 200 problems, with no explanation given for the missing 5 items; this kind of unexplained sample attrition, if it recurs across conditions, could subtly bias the reported CIs and accuracy deltas if the dropped items are not a random subset (e.g., API failures, parsing failures, or timeouts correlated with problem difficulty).
  Action: State explicitly why 5 of 200 gpt-4o-mini items are missing from the baseline count (API error, refusal, parse failure) and confirm the same 195/200 set is used consistently across all conditions and analyses for that model.
</reviewer_feedback>



<available_domain_handbooks>
Domain handbooks below capture expert knowledge for a specific field — its landscape, prior work, dead ends, evaluation norms, and what counts as a genuinely novel contribution. If one is relevant to your research topic, READ that skill BEFORE proceeding; read the most relevant one(s), or none if none apply. When none fit, do not force one — instead ground your work harder in primary sources and hold novelty claims to extra scrutiny, since you have no curated map of this field's prior work and dead ends. Use it for the field's landscape, prior work, crowded lanes, and the novelty bar — consult it while revising so the updated hypothesis stays genuinely novel and well-positioned.

- **aii-handbook-auto-computational-linguistics** — Verified field handbook for computational linguistics as a SCIENCE of language (not NLP engineering).
- **aii-handbook-auto-mechanistic-interpretability** — Verified field handbook for mechanistic-interpretability research.
- **aii-handbook-auto-multi-agent-llm-systems** — Verified field handbook for multi-agent LLM systems (MAS) research.
- **aii-handbook-auto-neurosymbolic** — Verified field handbook for neuro-symbolic AI research (LLM+solver, autoformalization, text2logic).
</available_domain_handbooks>

<task>
IMPORTANT: Your ONLY output is the revised hypothesis text. Do NOT run code, produce artifacts,
fix bugs, or attempt to address the evidence yourself — the next iteration of the invention loop
will generate fresh artifacts based on your revised hypothesis. Reflect and rewrite; nothing else.

Do NOT generate a completely new hypothesis. Take the current hypothesis and REVISE it
to incorporate new evidence. Keep the core idea — refine, narrow, or strengthen it.

1. Does the evidence support the hypothesis? Narrow or broaden scope as needed.
2. Which claims now have strong evidence? Which are still unsupported?
3. Should the hypothesis become more specific based on what we've learned?
4. If reviewer feedback is provided, address the critiques directly.

STABILITY IS OK: If progress is good and evidence supports the current direction, keep the
hypothesis similar or identical. Only make substantive changes when evidence clearly calls for
them — e.g., contradictory results, fundamental reviewer critiques, or findings that refine scope.

You must also classify two kinds of edges in the research trace:

(A) The H↔H edge — how does this revised hypothesis relate to the previous one?
    Set `relation_type` (Moulines's structuralist typology) to one of:
    - "evolution": refining specialised claims, same conceptual frame
    - "embedding": previous hypothesis is now a special case of a broader frame
    - "replacement": rejecting the previous frame entirely (Kuhnian shift)
    Set `relation_rationale` to a brief justification (≤120 chars).

(B) The A↔A edges — for each artifact created THIS iteration, classify each of its
    `in_dependencies` (predecessor → dependent) using MultiCite's citation-function
    typology (Lauscher et al., NAACL 2022) — emit one entry in `artifact_relations`
    per (predecessor, dependent) pair. Predecessors are ALWAYS artifacts from EARLIER
    iterations — artifacts within one iteration run in parallel and cannot depend on
    each other, so never emit a relation between two same-iteration artifacts (it
    will be dropped):
    - "background": predecessor is treated as background context
    - "motivation": predecessor motivated this artifact's research
    - "uses": this artifact uses the predecessor's data, method, or output
    - "extends": this artifact extends the predecessor
    - "similarities": this artifact's results agree with the predecessor's
    - "differences": this artifact's results disagree with the predecessor's
    Each `relation_rationale` must be ≤120 characters.

Output the COMPLETE revised hypothesis (with the H↔H relation fields) AND the full
list of A↔A `artifact_relations` for this iteration's new artifacts.
</task><user_data>
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
    "ArtifactRelation": {
      "description": "One typed A\u2194A edge between a dependent artifact and one of its in_dependencies.\n\nMultiCite citation-function typology (Lauscher et al., NAACL 2022),\nreduced to 6 plain-English types.",
      "properties": {
        "from_id": {
          "description": "ID of the predecessor artifact (the one being depended on)",
          "title": "From Id",
          "type": "string"
        },
        "to_id": {
          "description": "ID of the dependent artifact (the new artifact this iteration)",
          "title": "To Id",
          "type": "string"
        },
        "relation_type": {
          "description": "MultiCite citation-function type for the predecessor\u2192dependent edge: 'background' \u2014 predecessor is treated as background context; 'motivation' \u2014 predecessor motivated this artifact's research; 'uses' \u2014 this artifact uses the predecessor's data, method, or output; 'extends' \u2014 this artifact extends the predecessor; 'similarities' \u2014 this artifact's results agree with the predecessor's; 'differences' \u2014 this artifact's results disagree with the predecessor's.",
          "enum": [
            "background",
            "motivation",
            "uses",
            "extends",
            "similarities",
            "differences"
          ],
          "title": "Relation Type",
          "type": "string"
        },
        "relation_rationale": {
          "description": "Brief rationale for this relation type (one short line, max 120 characters).",
          "maxLength": 120,
          "title": "Relation Rationale",
          "type": "string"
        }
      },
      "required": [
        "from_id",
        "to_id",
        "relation_type",
        "relation_rationale"
      ],
      "title": "ArtifactRelation",
      "type": "object"
    }
  },
  "description": "Revised hypothesis after reviewing iteration results.\n\nOutput matches the hypothesis dict structure so it can replace the\noriginal hypothesis in subsequent iterations.",
  "properties": {
    "title": {
      "description": "Revised hypothesis title in plain, everyday language \u2014 short and jargon-free so a non-expert grasps it at a glance and it fits the run visualizations. Aim for about 4-8 words (~40 characters); may be unchanged if still accurate.",
      "title": "Title",
      "type": "string"
    },
    "hypothesis": {
      "description": "Revised hypothesis statement \u2014 what we now believe based on evidence",
      "title": "Hypothesis",
      "type": "string"
    },
    "relation_rationale": {
      "description": "Brief rationale for the H\u2194H revision type (one short line, max 120 characters).",
      "maxLength": 120,
      "title": "Relation Rationale",
      "type": "string"
    },
    "confidence_delta": {
      "description": "How confidence changed: 'increased', 'decreased', or 'unchanged'",
      "title": "Confidence Delta",
      "type": "string"
    },
    "key_changes": {
      "description": "Bullet list of specific changes made to the hypothesis",
      "items": {
        "type": "string"
      },
      "title": "Key Changes",
      "type": "array"
    },
    "relation_type": {
      "description": "Moulines's structuralist typology of this hypothesis revision: 'evolution' \u2014 refining specialised claims while keeping the same conceptual frame; 'embedding' \u2014 the previous hypothesis is now a special case of a broader frame; 'replacement' \u2014 rejecting the previous frame entirely (incommensurable, Kuhnian revolution).",
      "enum": [
        "evolution",
        "embedding",
        "replacement"
      ],
      "title": "Relation Type",
      "type": "string"
    },
    "artifact_relations": {
      "description": "Typed A\u2194A edges for this iteration's new artifacts. Emit one entry per (predecessor \u2192 dependent) edge for every in_dependency on each artifact produced this iteration.",
      "items": {
        "$ref": "#/$defs/ArtifactRelation"
      },
      "title": "Artifact Relations",
      "type": "array"
    }
  },
  "required": [
    "title",
    "hypothesis",
    "relation_rationale",
    "confidence_delta",
    "key_changes",
    "relation_type"
  ],
  "title": "RevisedHypothesis",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `./.terminal_claude_agent_struct_out.json` exists and contains JSON matching the schema above.
````

### [3] HUMAN-USER prompt · 2026-07-31 20:49:22 UTC

```
Does adding a short self-critique step before answering improve accuracy on multi-step arithmetic word problems?
```

### [4] TOOL CALL — Write · 2026-07-31 20:49:58 UTC

```
File: /home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_0WmBa7GFLIzI/3_invention_loop/iter_1/upd_hypo/upd_hypo/.terminal_claude_agent_struct_out.json

{
  "title": "Checksum Critique Beats Self-Doubt, Reliability-Bound",
  "hypothesis": "When an LLM verifies its own multi-step arithmetic word-problem solution using an explicit, mechanically-computed modular-arithmetic invariant (a 'casting-out-nines' digit-root checksum applied to each intermediate computation) instead of an open-ended 'double-check your work' self-critique prompt or a length-matched content-null placebo critique, error-detection and downstream correction accuracy will be substantially higher than both alternatives, but only for models with non-trivial baseline error rates (i.e. below-ceiling headroom on the target problem set) and only up to a ceiling set by the model's own reliability at computing the checksum in the first place. On claude-haiku-4.5 (76.5% no-critique baseline), checksum critique raised accuracy to 97.5% overall and 100% on the checksum-detectable subset, beating free-form critique by 18.75pp and the matched-length placebo by 9.375pp (Holm-adjusted p=0.04 both), while an oracle ablation showed correction-given-a-flag is already near-ceiling for the model (100% self-computed vs. 93.75% oracle-supplied) -- so the causal mechanism is specifically that the checksum makes error DETECTION easy, not that it makes correction easier. This benefit vanished for gpt-4o-mini (95.4% baseline, all conditions statistically tied), indicating the effect is concentrated where the model's unaided arithmetic error rate is non-trivial, not a universal free lunch -- a claim we now treat as a two-model pilot observation, not an established scaling trend, pending a third model already in progress. A stratified audit found the evaluated model itself miscomputes its own mod-9 checksum in ~15% of sampled traces, identifying self-computed-checksum reliability (not the model's ability to act on a correct checksum, nor the placebo-vs-checksum content confound, which is ruled out) as the binding practical bottleneck on how much of the theoretical ceiling is realized -- a claim that itself needs cross-validation against a judge from a different model family or a deterministic parser, since the current audit used claude-haiku-4.5 to judge claude-haiku-4.5's own traces.",
  "relation_rationale": "Same core mechanism confirmed; narrowed to capability-dependent scope + computation-reliability bottleneck as binding constraint",
  "confidence_delta": "increased",
  "key_changes": [
    "Narrowed universal 'free lunch' framing to a capability-dependent scope condition: benefit appears only when baseline accuracy has meaningful headroom (confirmed on claude-haiku-4.5, absent on near-ceiling gpt-4o-mini)",
    "Reframed the two-model comparison explicitly as a pilot observation rather than an established scaling trend, per reviewer's major scope critique, pending the in-progress third model",
    "Added the oracle-ablation finding as core evidence: the mechanism is specifically improved DETECTION (self-computed correction already matches oracle-supplied correction), not improved correction capability",
    "Elevated self-computed-checksum arithmetic reliability (~15% error rate in sampled traces) to the primary bottleneck claim, since it is now the demonstrated limiting factor on realized gains",
    "Flagged the checksum-computation audit's same-model-as-judge design as needing cross-validation (different-family judge or deterministic parser) per reviewer's methodology critique, rather than treating the 15% figure as settled",
    "Noted the detection precision/recall metric family remains unvalidated by direct measurement on the benchmark's own labeled error-injection variants (per reviewer's major evidence critique) and is not yet part of the supported claims",
    "Retained the matched-length-placebo control result (content of invariant matters, not just extra deliberation tokens) as strong supported evidence, unchanged"
  ],
  "relation_type": "evolution",
  "artifact_relations": []
}
```

### [5] TOOL RESULT — Write · 2026-07-31 20:49:58 UTC

```
{"type": "create", "filePath": "/home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_0WmBa7GFLIzI/3_invention_loop/iter_1/upd_hypo/upd_hypo/.terminal_claude_agent_struct_out.json", "content": "{\n  \"title\": \"Checksum Critique Beats Self-Doubt, Reliability-Bound\",\n  \"hypothesis\": \"When an LLM verifies its own multi-step arithmetic word-problem solution using an explicit, mechanically-computed modular-arithmetic invariant (a 'casting-out-nines' digit-root checksum applied to each intermediate computation) instead of an open-ended 'double-check your work' self-critique prompt or a length-matched content-null placebo critique, error-detection and downstream correction accuracy will be substantially higher than both alternatives, but only for models with non-trivial baseline error rates (i.e. below-ceiling headroom on the target problem set) and only up to a ceiling set by the model's own reliability at computing the checksum in the first place. On claude-haiku-4.5 (76.5% no-critique baseline), checksum critique raised accuracy to 97.5% overall and 100% on the checksum-detectable subset, beating free-form critique by 18.75pp and the matched-length placebo by 9.375pp (Holm-adjusted p=0.04 both), while an oracle ablation showed correction-given-a-flag is already near-ceiling for the model (100% self-computed vs. 93.75% oracle-supplied) -- so the causal mechanism is specifically that the checksum makes error DETECTION easy, not that it makes correction easier. This benefit vanished for gpt-4o-mini (95.4% baseline, all conditions statistically tied), indicating the effect is concentrated where the model's unaided arithmetic error rate is non-trivial, not a universal free lunch -- a claim we now treat as a two-model pilot observation, not an established scaling trend, pending a third model already in progress. A stratified audit found the evaluated model itself miscomputes its own mod-9 checksum in ~15% of sampled traces, identifying self-computed-checksum reliability (not the model's ability to act on a correct checksum, nor the placebo-vs-checksum content confound, which is ruled out) as the binding practical bottleneck on how much of the theoretical ceiling is realized -- a claim that itself needs cross-validation against a judge from a different model family or a deterministic parser, since the current audit used claude-haiku-4.5 to judge claude-haiku-4.5's own traces.\",\n  \"relation_rationale\": \"Same core mechanism confirmed; narrowed to capability-dependent scope + computation-reliability bottleneck as binding constraint\",\n  \"confidence_delta\": \"increased\",\n  \"key_changes\": [\n    \"Narrowed universal 'free lunch' framing to a capability-dependent scope condition: benefit appears only when baseline accuracy has meaningful headroom (confirmed on claude-haiku-4.5, absent on near-ceiling gpt-4o-mini)\",\n    \"Reframed the two-model comparison explicitly as a pilot observation rather than an established scaling trend, per reviewer's major scope critique, pending the in-progress third model\",\n    \"Added the oracle-ablation finding as core evidence: the mechanism is specifically improved DETECTION (self-computed correction already matches oracle-supplied correction), not improved correction capability\",\n    \"Elevated self-computed-checksum arithmetic reliability (~15% error rate in sampled traces) to the primary bottleneck claim, since it is now the demonstrated limiting factor on realized gains\",\n    \"Flagged the checksum-computation audit's same-model-as-judge design as needing cross-validation (different-family judge or deterministic parser) per reviewer's methodology critique, rather than treating the 15% figure as settled\",\n    \"Noted the detection precision/recall metric family remains unvalidated by direct measurement on the benchmark's own labeled error-injection variants (per reviewer's major evidence critique) and is not yet part of the supported claims\",\n    \"Retained the matched-length-placebo control result (content of invariant matters, not just extra deliberation tokens) as strong supported evidence, unchanged\"\n  ],\n  \"relation_type\": \"evolution\",\n  \"artifact_relations\": []\n}\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [6] ASSISTANT · 2026-07-31 20:50:01 UTC

```
Done — revised hypothesis written to `.terminal_claude_agent_struct_out.json`. It narrows the claim to a capability-dependent effect (confirmed on claude-haiku-4.5, absent on near-ceiling gpt-4o-mini, treated as pilot not trend), elevates self-computed-checksum reliability (~15% error rate) as the binding bottleneck, and flags the same-model judge-audit and unvalidated detection-precision metrics as open issues per reviewer feedback.
```

### [7] SYSTEM-USER prompt · 2026-07-31 20:50:04 UTC

```
<validation-feedback>
Attempt 1 failed validation.

Schema validation found 1 problem — fix ALL of them at once:
  - at `relation_rationale`: 'Same core mechanism confirmed; narrowed to capability-dependent scope + computation-reliability bottleneck as binding constraint' is too long (at most 120 characters, got 128)
Every required field must be present and every field type must match the schema.

Produce `.terminal_claude_agent_struct_out.json` again so it contains corrected JSON that matches the schema. Do not invent new fields.
</validation-feedback>
```

### [8] TOOL CALL — Edit · 2026-07-31 20:50:08 UTC

```
File: /home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_0WmBa7GFLIzI/3_invention_loop/iter_1/upd_hypo/upd_hypo/.terminal_claude_agent_struct_out.json
OLD:   "relation_rationale": "Same core mechanism confirmed; narrowed to capability-dependent scope + computation-reliability bottleneck as binding constraint",
NEW:   "relation_rationale": "Same mechanism confirmed; narrowed to capability-dependent scope + checksum-computation reliability as bottleneck",
```

### [9] TOOL RESULT — Edit · 2026-07-31 20:50:08 UTC

```
{"filePath": "/home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_0WmBa7GFLIzI/3_invention_loop/iter_1/upd_hypo/upd_hypo/.terminal_claude_agent_struct_out.json", "oldString": "  \"relation_rationale\": \"Same core mechanism confirmed; narrowed to capability-dependent scope + computation-reliability bottleneck as binding constraint\",", "newString": "  \"relation_rationale\": \"Same mechanism confirmed; narrowed to capability-dependent scope + checksum-computation reliability as bottleneck\",", "originalFile": "{\n  \"title\": \"Checksum Critique Beats Self-Doubt, Reliability-Bound\",\n  \"hypothesis\": \"When an LLM verifies its own multi-step arithmetic word-problem solution using an explicit, mechanically-computed modular-arithmetic invariant (a 'casting-out-nines' digit-root checksum applied to each intermediate computation) instead of an open-ended 'double-check your work' self-critique prompt or a length-matched content-null placebo critique, error-detection and downstream correction accuracy will be substantially higher than both alternatives, but only for models with non-trivial baseline error rates (i.e. below-ceiling headroom on the target problem set) and only up to a ceiling set by the model's own reliability at computing the checksum in the first place. On claude-haiku-4.5 (76.5% no-critique baseline), checksum critique raised accuracy to 97.5% overall and 100% on the checksum-detectable subset, beating free-form critique by 18.75pp and the matched-length placebo by 9.375pp (Holm-adjusted p=0.04 both), while an oracle ablation showed correction-given-a-flag is already near-ceiling for the model (100% self-computed vs. 93.75% oracle-supplied) -- so the causal mechanism is specifically that the checksum makes error DETECTION easy, not that it makes correction easier. This benefit vanished for gpt-4o-mini (95.4% baseline, all conditions statistically tied), indicating the effect is concentrated where the model's unaided arithmetic error rate is non-trivial, not a universal free lunch -- a claim we now treat as a two-model pilot observation, not an established scaling trend, pending a third model already in progress. A stratified audit found the evaluated model itself miscomputes its own mod-9 checksum in ~15% of sampled traces, identifying self-computed-checksum reliability (not the model's ability to act on a correct checksum, nor the placebo-vs-checksum content confound, which is ruled out) as the binding practical bottleneck on how much of the theoretical ceiling is realized -- a claim that itself needs cross-validation against a judge from a different model family or a deterministic parser, since the current audit used claude-haiku-4.5 to judge claude-haiku-4.5's own traces.\",\n  \"relation_rationale\": \"Same core mechanism confirmed; narrowed to capability-dependent scope + computation-reliability bottleneck as binding constraint\",\n  \"confidence_delta\": \"increased\",\n  \"key_changes\": [\n    \"Narrowed universal 'free lunch' framing to a capability-dependent scope condition: benefit appears only when baseline accuracy has meaningful headroom (confirmed on claude-haiku-4.5, absent on near-ceiling gpt-4o-mini)\",\n    \"Reframed the two-model comparison explicitly as a pilot observation rather than an established scaling trend, per reviewer's major scope critique, pending the in-progress third model\",\n    \"Added the oracle-ablation finding as core evidence: the mechanism is specifically improved DETECTION (self-computed correction already matches oracle-supplied correction), not improved correction capability\",\n    \"Elevated self-computed-checksum arithmetic reliability (~15% error rate in sampled traces) to the primary bottleneck claim, since it is now the demonstrated limiting factor on realized gains\",\n    \"Flagged the checksum-computation audit's same-model-as-judge design as needing cross-validation (different-family judge or deterministic parser) per reviewer's methodology critique, rather than treating the 15% figure as settled\",\n    \"Noted the detection precision/recall metric family remains unvalidated by direct measurement on the benchmark's own labeled error-injection variants (per reviewer's major evidence critique) and is not yet part of the supported claims\",\n    \"Retained the matched-length-placebo control result (content of invariant matters, not just extra deliberation tokens) as strong supported evidence, unchanged\"\n  ],\n  \"relation_type\": \"evolution\",\n  \"artifact_relations\": []\n}\n", "structuredPatch": [{"oldStart": 1, "oldLines": 7, "newStart": 1, "newLines": 7, "lines": [" {", "   \"title\": \"Checksum Critique Beats Self-Doubt, Reliability-Bound\",", "   \"hypothesis\": \"When an LLM verifies its own multi-step arithmetic word-problem solution using an explicit, mechanically-computed modular-arithmetic invariant (a 'casting-out-nines' digit-root checksum applied to each intermediate computation) instead of an open-ended 'double-check your work' self-critique prompt or a length-matched content-null placebo critique, error-detection and downstream correction accuracy will be substantially higher than both alternatives, but only for models with non-trivial baseline error rates (i.e. below-ceiling headroom on the target problem set) and only up to a ceiling set by the model's own reliability at computing the checksum in the first place. On claude-haiku-4.5 (76.5% no-critique baseline), checksum critique raised accuracy to 97.5% overall and 100% on the checksum-detectable subset, beating free-form critique by 18.75pp and the matched-length placebo by 9.375pp (Holm-adjusted p=0.04 both), while an oracle ablation showed correction-given-a-flag is already near-ceiling for the model (100% self-computed vs. 93.75% oracle-supplied) -- so the causal mechanism is specifically that the checksum makes error DETECTION easy, not that it makes correction easier. This benefit vanished for gpt-4o-mini (95.4% baseline, all conditions statistically tied), indicating the effect is concentrated where the model's unaided arithmetic error rate is non-trivial, not a universal free lunch -- a claim we now treat as a two-model pilot observation, not an established scaling trend, pending a third model already in progress. A stratified audit found the evaluated model itself miscomputes its own mod-9 checksum in ~15% of sampled traces, identifying self-computed-checksum reliability (not the model's ability to act on a correct checksum, nor the placebo-vs-checksum content confound, which is ruled out) as the binding practical bottleneck on how much of the theoretical ceiling is realized -- a claim that itself needs cross-validation against a judge from a different model family or a deterministic parser, since the current audit used claude-haiku-4.5 to judge claude-haiku-4.5's own traces.\",", "-  \"relation_rationale\": \"Same core mechanism confirmed; narrowed to capability-dependent scope + computation-reliability bottleneck as binding constraint\",", "+  \"relation_rationale\": \"Same mechanism confirmed; narrowed to capability-dependent scope + checksum-computation reliability as bottleneck\",", "   \"confidence_delta\": \"increased\",", "   \"key_changes\": [", "     \"Narrowed universal 'free lunch' framing to a capability-dependent scope condition: benefit appears only when baseline accuracy has meaningful headroom (confirmed on claude-haiku-4.5, absent on near-ceiling gpt-4o-mini)\","]}], "userModified": false, "replaceAll": false}
```

### [10] ASSISTANT · 2026-07-31 20:50:13 UTC

```
Fixed — the rationale is now 116 characters, under the 120 limit.
```
