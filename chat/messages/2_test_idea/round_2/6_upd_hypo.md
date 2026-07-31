# upd_hypo — test_idea

> Phase: `invention_loop` · round 2 · `upd_hypo`
> Run: `run_0WmBa7GFLIzI` — Checksum Self-Critique Helps Weak Arithmetic, Hurts Weak Models
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `upd_hypo` (terminal_claude_agent, claude-sonnet-5)

### [1] CONFIG · 2026-07-31 21:12:30 UTC

```
model: claude-sonnet-5 | effort: low | permission: bypassPermissions | cwd: /home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_0WmBa7GFLIzI/3_invention_loop/iter_2/upd_hypo/upd_hypo
```

### [2] SYSTEM-USER prompt · 2026-07-31 21:12:36 UTC

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
title: Checksum Critique Beats Self-Doubt, Reliability-Bound
hypothesis: >-
  When an LLM verifies its own multi-step arithmetic word-problem solution using an explicit, mechanically-computed modular-arithmetic
  invariant (a 'casting-out-nines' digit-root checksum applied to each intermediate computation) instead of an open-ended
  'double-check your work' self-critique prompt or a length-matched content-null placebo critique, error-detection and downstream
  correction accuracy will be substantially higher than both alternatives, but only for models with non-trivial baseline error
  rates (i.e. below-ceiling headroom on the target problem set) and only up to a ceiling set by the model's own reliability
  at computing the checksum in the first place. On claude-haiku-4.5 (76.5% no-critique baseline), checksum critique raised
  accuracy to 97.5% overall and 100% on the checksum-detectable subset, beating free-form critique by 18.75pp and the matched-length
  placebo by 9.375pp (Holm-adjusted p=0.04 both), while an oracle ablation showed correction-given-a-flag is already near-ceiling
  for the model (100% self-computed vs. 93.75% oracle-supplied) -- so the causal mechanism is specifically that the checksum
  makes error DETECTION easy, not that it makes correction easier. This benefit vanished for gpt-4o-mini (95.4% baseline,
  all conditions statistically tied), indicating the effect is concentrated where the model's unaided arithmetic error rate
  is non-trivial, not a universal free lunch -- a claim we now treat as a two-model pilot observation, not an established
  scaling trend, pending a third model already in progress. A stratified audit found the evaluated model itself miscomputes
  its own mod-9 checksum in ~15% of sampled traces, identifying self-computed-checksum reliability (not the model's ability
  to act on a correct checksum, nor the placebo-vs-checksum content confound, which is ruled out) as the binding practical
  bottleneck on how much of the theoretical ceiling is realized -- a claim that itself needs cross-validation against a judge
  from a different model family or a deterministic parser, since the current audit used claude-haiku-4.5 to judge claude-haiku-4.5's
  own traces.
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
_relation_rationale: >-
  Same mechanism confirmed; narrowed to capability-dependent scope + checksum-computation reliability as bottleneck
_confidence_delta: increased
_key_changes:
- >-
  Narrowed universal 'free lunch' framing to a capability-dependent scope condition: benefit appears only when baseline accuracy
  has meaningful headroom (confirmed on claude-haiku-4.5, absent on near-ceiling gpt-4o-mini)
- >-
  Reframed the two-model comparison explicitly as a pilot observation rather than an established scaling trend, per reviewer's
  major scope critique, pending the in-progress third model
- >-
  Added the oracle-ablation finding as core evidence: the mechanism is specifically improved DETECTION (self-computed correction
  already matches oracle-supplied correction), not improved correction capability
- >-
  Elevated self-computed-checksum arithmetic reliability (~15% error rate in sampled traces) to the primary bottleneck claim,
  since it is now the demonstrated limiting factor on realized gains
- >-
  Flagged the checksum-computation audit's same-model-as-judge design as needing cross-validation (different-family judge
  or deterministic parser) per reviewer's methodology critique, rather than treating the 15% figure as settled
- >-
  Noted the detection precision/recall metric family remains unvalidated by direct measurement on the benchmark's own labeled
  error-injection variants (per reviewer's major evidence critique) and is not yet part of the supported claims
- >-
  Retained the matched-length-placebo control result (content of invariant matters, not just extra deliberation tokens) as
  strong supported evidence, unchanged
relation_type: evolution
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

--- Item 3 ---
id: art_0V-2bxn9h7_u
type: evaluation
in_dependencies:
- id: art_UafZp2AqR5at
  label: dataset
title: Rigorous precision/recall re-audit of checksum self-critique
summary: >-
  Replaces the underpowered proxy detection metric and same-model LLM-judge audit from art_VCF3BbfSo_RV with properly-powered
  statistics computed from real per-item experiment data. DATA-AVAILABILITY NOTE: the new iter_2 error-injection experiment
  (gen_art_experiment_1) that this plan's STEPS 1-6 assume never produced any output file (no method_out.json/checkpoint.json
  exists for it in this run), so it cannot be joined against art_UafZp2AqR5at as originally specified. This evaluation instead
  re-analyzes the only completed, real experiment output in the dependency chain -- iter_1/gen_art_experiment_1/method_out.json
  (2592 LLM calls across 3 models x 5 conditions x 200 procedurally-generated synthetic arithmetic problems, self-solve then
  self-critique design) -- and is fully transparent about this substitution throughout eval.py's docstring and eval_out.json's
  metadata.step1-6 fields rather than fabricating a GSM8K join. Delivers: (1) STEP1 join-coverage accounting (2592/2592 matched,
  0 unmatched, reasons tracked); (2) STEP2/3 condition x model x checksum-detectable/invisible precision/recall/F1 and correction-accuracy-given-true-positive
  tables, each cell with a closed-form Wilson 95% CI and an explicit n<20-underpowered flag, where ground truth = the same
  model's baseline (no-critique) solve being wrong (recovered per-problem checksum_detectable/invisible labels via bit-for-bit
  RNG reproduction of the experiment's error-characterization step, verified exactly against the experiment's own reported
  checksum_detectable_fraction of 0.32); (3) STEP4 a pure-Python regex-only mod-9 digit-root checker (zero LLM calls) that
  parses every 'Digit root of N: ...' claim in all 599 checksum_critique traces, independently recomputes the true digit root
  via the closed-form casting-out-nines formula (self-checked against brute-force digit-summing on 13 test values first),
  and finds a 9.6% arithmetic-error rate (30/312 traces with parseable claims) -- materially lower than the prior same-model
  LLM-judge's 15.4% (80 traces); the same reproduced sample was also re-judged fresh by an LLM for a real per-trace comparison,
  yielding a negative Cohen's kappa (-0.12, n=70 paired traces) between the deterministic checker and the LLM judge, i.e.
  worse-than-chance agreement, revealing the same-model judge's verdicts do not track ground-truth arithmetic correctness;
  (4) STEP5 checksum-condition precision/recall/F1 recomputed excluding the 30 checker-flagged-bad traces, reported side-by-side
  with the full sample; (5) STEP6 explicitly marked UNSUPPORTED/pending (not fabricated): the only available experiment has
  zero GSM8K-sourced items, since it used its own synthetic generator rather than art_UafZp2AqR5at; (6) a prose CONFIRMED/REVISED/UNSUPPORTED
  verdict against each of the hypothesis's four specific numeric claims (18.75pp free-form gap: CONFIRMED at available n;
  9.375pp placebo gap: UNSUPPORTED, n<20 per detectable-subset cell; 100% vs 93.75% oracle ablation: REVISED via the properly
  isolated correction-accuracy-given-TP metric; ~15% checksum-miscomputation rate: REVISED to 9.6% via the deterministic checker,
  which now supersedes the prior figure per the artifact direction). Output validated against the exp_eval_sol_out.json schema;
  full/mini/preview variants generated (1.5MB, well under any size-split threshold).
workspace_path: >-
  /home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_0WmBa7GFLIzI/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1
out_expected_files:
- eval.py
- full_eval_out.json
- mini_eval_out.json
- preview_eval_out.json
</all_artifacts>

<new_artifacts_this_iteration>
These 1 artifacts were created THIS iteration.

id: art_0V-2bxn9h7_u
type: evaluation
in_dependencies:
- id: art_UafZp2AqR5at
  label: dataset
title: Rigorous precision/recall re-audit of checksum self-critique
summary: >-
  Replaces the underpowered proxy detection metric and same-model LLM-judge audit from art_VCF3BbfSo_RV with properly-powered
  statistics computed from real per-item experiment data. DATA-AVAILABILITY NOTE: the new iter_2 error-injection experiment
  (gen_art_experiment_1) that this plan's STEPS 1-6 assume never produced any output file (no method_out.json/checkpoint.json
  exists for it in this run), so it cannot be joined against art_UafZp2AqR5at as originally specified. This evaluation instead
  re-analyzes the only completed, real experiment output in the dependency chain -- iter_1/gen_art_experiment_1/method_out.json
  (2592 LLM calls across 3 models x 5 conditions x 200 procedurally-generated synthetic arithmetic problems, self-solve then
  self-critique design) -- and is fully transparent about this substitution throughout eval.py's docstring and eval_out.json's
  metadata.step1-6 fields rather than fabricating a GSM8K join. Delivers: (1) STEP1 join-coverage accounting (2592/2592 matched,
  0 unmatched, reasons tracked); (2) STEP2/3 condition x model x checksum-detectable/invisible precision/recall/F1 and correction-accuracy-given-true-positive
  tables, each cell with a closed-form Wilson 95% CI and an explicit n<20-underpowered flag, where ground truth = the same
  model's baseline (no-critique) solve being wrong (recovered per-problem checksum_detectable/invisible labels via bit-for-bit
  RNG reproduction of the experiment's error-characterization step, verified exactly against the experiment's own reported
  checksum_detectable_fraction of 0.32); (3) STEP4 a pure-Python regex-only mod-9 digit-root checker (zero LLM calls) that
  parses every 'Digit root of N: ...' claim in all 599 checksum_critique traces, independently recomputes the true digit root
  via the closed-form casting-out-nines formula (self-checked against brute-force digit-summing on 13 test values first),
  and finds a 9.6% arithmetic-error rate (30/312 traces with parseable claims) -- materially lower than the prior same-model
  LLM-judge's 15.4% (80 traces); the same reproduced sample was also re-judged fresh by an LLM for a real per-trace comparison,
  yielding a negative Cohen's kappa (-0.12, n=70 paired traces) between the deterministic checker and the LLM judge, i.e.
  worse-than-chance agreement, revealing the same-model judge's verdicts do not track ground-truth arithmetic correctness;
  (4) STEP5 checksum-condition precision/recall/F1 recomputed excluding the 30 checker-flagged-bad traces, reported side-by-side
  with the full sample; (5) STEP6 explicitly marked UNSUPPORTED/pending (not fabricated): the only available experiment has
  zero GSM8K-sourced items, since it used its own synthetic generator rather than art_UafZp2AqR5at; (6) a prose CONFIRMED/REVISED/UNSUPPORTED
  verdict against each of the hypothesis's four specific numeric claims (18.75pp free-form gap: CONFIRMED at available n;
  9.375pp placebo gap: UNSUPPORTED, n<20 per detectable-subset cell; 100% vs 93.75% oracle ablation: REVISED via the properly
  isolated correction-accuracy-given-TP metric; ~15% checksum-miscomputation rate: REVISED to 9.6% via the deterministic checker,
  which now supersedes the prior figure per the artifact direction). Output validated against the exp_eval_sol_out.json schema;
  full/mini/preview variants generated (1.5MB, well under any size-split threshold).
workspace_path: >-
  /home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_0WmBa7GFLIzI/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1
out_expected_files:
- eval.py
- full_eval_out.json
- mini_eval_out.json
- preview_eval_out.json
</new_artifacts_this_iteration>

<current_paper>
The paper draft from this iteration — represents the current state of the research story.

# Introduction

Large language models (LLMs) are routinely asked to solve multi-step arithmetic word problems and then, in the same breath, to check their own work. The instruction is nearly universal in production prompting practice: "double-check your answer," "review your solution for mistakes," "verify before finalizing." The empirical record on whether this instruction does anything is much less settled. Free-form self-critique on reasoning and arithmetic tasks is documented to be unreliable, and in several studies neutral or actively harmful, because models tend to restate rather than independently re-derive their own output [1, 2, 3, 9]. A survey of self-correction work concludes that intrinsic self-correction -- correction using only the model's own judgment, with no external signal -- rarely improves accuracy on reasoning tasks and often degrades it [3]. Stechly et al. report a parallel finding for planning and reasoning tasks specifically: models frequently cannot distinguish their own correct outputs from incorrect ones well enough for self-verification to help, and self-critique loops can oscillate away from correct answers already found [9]. This leaves practitioners with a real problem: the instruction to self-check costs tokens and latency, and appears to buy little on average -- but "on average" hides substantial variation we set out to characterize.

Understanding why self-critique fails is important because the answer determines what fix is worth trying. If self-critique fails simply because models are bad at generating additional reasoning tokens, then any structured deliberation should help equally, and the interesting engineering lever is verbosity or prompt length. If self-critique fails because it asks the model to hold two full derivations in its context and compare them from a fuzzy memory of the first pass -- a hard, error-prone cognitive operation -- then the fix is not "critique more," but "critique differently": give the model something concrete and cheap to compare against, rather than asking it to re-run its own reasoning silently and trust its own comparison.

Recent mechanistic evidence favors the second explanation. Circuit-level analysis of arithmetic-capable language models shows that their internal error-detection machinery relies on shallow surface-level numeric-consistency checks between tokens in the text, not on genuine independent recomputation of the underlying arithmetic [ARTIFACT:art_UafZp2AqR5at][4]. In other words, models already have circuitry that performs consistency checks -- but that circuitry checks superficial token-level agreement, not mathematical correctness. This diagnosis is mechanistic, not behavioral: it explains why self-critique underperforms, but it proposes no intervention and reports no accuracy numbers for any fix.

Multi-step arithmetic word problems are a natural setting to turn this diagnosis into an intervention, because they are exactly the kind of task where a genuinely independent, cheap-to-compute consistency signal has existed for centuries: the casting-out-nines checksum. Long before calculators, bookkeepers verified long multiplications and additions by reducing every operand and every result to its digit root -- the value obtained by repeatedly summing digits until one digit remains -- and checking that the same arithmetic operation applied to the digit roots reproduces the digit root of the claimed answer. Because any integer is congruent to its digit sum modulo 9, this check is a direct probe of the arithmetic's correctness modulo 9: a mismatch proves an error exists somewhere in that step; agreement does not prove correctness, but it is cheap, mechanical, and structurally decoupled from the original derivation.

This checksum has an appealing property for LLM self-critique specifically: it converts error detection from a hard task (re-deriving an entire multi-step solution and comparing it, in context, to a fuzzy memory of the first attempt) into an easy, decomposable task (a single small-number digit-sum computation and a residue comparison, repeated once per step). If the mechanistic diagnosis in prior work is correct -- that models default to shallow, surface-level consistency checks rather than genuine recomputation -- then handing the model an explicit, mechanically-defined consistency check to perform should align the requested behavior with what the model's error-detection machinery is already good at, rather than what it is bad at. But this presupposes a model that can reliably execute the extra bookkeeping the checksum procedure demands, and, as we show, that presupposition does not hold uniformly across models.

The central methodological risk in testing this idea is confounding the invariant itself with the general effect of "more structured-looking deliberation text." Any critique procedure that produces additional tokens before a final answer could plausibly help through increased test-time computation alone, independent of whether those tokens encode a real error-detecting signal [ARTIFACT:art_VCF3BbfSo_RV]. We address this directly with a length-matched placebo critique: a condition that is similarly deterministic-looking and similarly long as the checksum critique, but whose steps (digit-by-digit spelling and digit-count comparison) do not encode a true mod-9 invariant. Any advantage of the checksum condition over this placebo isolates the causal contribution of the invariant itself, separate from the contribution of extra thinking tokens.

[FIGURE:fig1]

We evaluate five self-check conditions -- no critique (baseline), free-form critique, length-matched placebo critique, checksum critique, and an oracle detection-isolation ablation that supplies a pre-computed checksum mismatch signal directly, isolating whether the bottleneck is computing the checksum or using it -- on three LLMs spanning strong, mid, and weak capability tiers (anthropic/claude-haiku-4.5, openai/gpt-4o-mini, meta-llama/llama-3.1-8b-instruct) via OpenRouter at temperature 0 over 200 procedurally generated multi-step arithmetic word problems per model, drawing on a purpose-built 1,935-row benchmark with a deterministic error-injection layer that labels every corrupted variant checksum-detectable or checksum-invisible by its true mod-9 residue, giving a principled ceiling on what a casting-out-nines check could possibly catch. This iteration adds the third model -- absent from our previous draft, where it was noted as still in progress -- which changes our central finding qualitatively, not just quantitatively: checksum critique is not simply "beneficial-then-neutral" as capability decreases, it is beneficial for the strong model, neutral for the mid-capability model, and actively catastrophic for the weak model. claude-haiku-4.5 rises from 76.5% to 97.5% overall accuracy; gpt-4o-mini is statistically unchanged across all four conditions (95.5% to 97.5%, no pairwise difference exceeding 2.0 percentage points); llama-3.1-8b-instruct collapses from an 84.5% no-critique baseline to 17.1% under checksum critique, a drop so large (McNemar p=1.2x10^-31 versus free-form critique) that it dominates the mean response length in that condition (4,198 characters, roughly 8x the 526-character baseline) and, on manual trace inspection, reflects the model losing track of the original word problem while performing the digit-root bookkeeping. We further replace our previous same-model LLM-judge checksum-reliability audit -- which a reviewer correctly flagged as a source of circular, potentially correlated bias -- with a deterministic, regex-based mod-9 checker requiring zero LLM calls, and find the two disagree at worse-than-chance levels (Cohen's kappa = -0.12 [ARTIFACT:art_0V-2bxn9h7_u], n=70 paired traces), which itself argues for discarding the same-model-judge design entirely rather than merely cross-validating it.

## Summary of Contributions

- A three-model, capability-stratified evaluation of checksum self-critique -- replacing the two-model comparison a prior reviewer identified as insufficient to support a scaling claim -- revealing a non-monotonic, not merely diminishing, relationship between baseline capability and checksum-critique effectiveness: strong-model gain (+21.0pp), mid-model null effect, weak-model catastrophic loss (-67.4pp) (Section 5).
- A properly powered detection precision/recall/F1 re-audit across all three models, four conditions, and three checksum-detectability strata, with closed-form Wilson 95% confidence intervals and explicit small-n flags on every cell, replacing the previous draft's admittedly underpowered proxy metric [ARTIFACT:art_0V-2bxn9h7_u] (Section 5).
- A dependency-free, deterministic (zero-LLM-call) mod-9 digit-root checker that supersedes our earlier same-model LLM-judge checksum-computation audit; the two methods disagree at a rate worse than chance (Cohen's kappa=-0.12), and the deterministic checker's own error-rate estimate (9.6%, 30/312 parseable traces) revises our prior figure of 15.4% downward [ARTIFACT:art_0V-2bxn9h7_u] (Section 5-6).
- Qualitative trace evidence for why checksum critique harms weaker models: the additional bookkeeping load causes llama-3.1-8b-instruct to hallucinate extra computation steps absent from the original problem, actively corrupting an initially-correct derivation rather than merely failing to fix an error (Section 6).

# Related Work

**Self-critique and self-correction of LLM reasoning.** Self-Refine established the pattern of prompting a model to iteratively critique and revise its own output without external feedback, and reported gains across a range of generation tasks [1]. Subsequent work specifically targeting reasoning and arithmetic has been substantially more pessimistic: intrinsic self-correction -- correction driven solely by the model's own judgment -- frequently fails to improve, and sometimes harms, accuracy on math and planning tasks, because models struggle to reliably detect that their own output is wrong in the first place [2, 3, 9]. Stechly et al. show this failure extends to iterative self-verification loops on planning tasks, where repeated self-critique can move a model away from an already-correct answer rather than toward one [9] -- a dynamic our llama-3.1-8b-instruct result echoes in the extreme, where a single checksum-critique pass corrupts a substantial share of initially correct solutions. A critical survey of this literature concludes that self-correction reliably helps only when it can draw on an external signal -- a tool, a verifier, ground-truth feedback, or another model -- rather than the same model's own re-reading of its own text [3]. Our checksum condition sits inside this reliability gap: it is still generated by the same model with no external oracle, but it hands the model an explicit, mechanically-defined procedure to execute, rather than an open-ended instruction to "check." S2R shows that reinforcement-learning-trained self-verify/self-correct behavior can substantially improve math reasoning accuracy (51.0% to 81.6% on one benchmark) [ARTIFACT:art_VCF3BbfSo_RV][5], but that gain requires training; our approach is training-free and prompt-only, trading some of that ceiling for zero-shot applicability, and our weak-model result shows that trade-off has a real cost: a training-free prompt intervention can catastrophically fail exactly where a capability-conditioned RL-trained procedure might have been designed around it.

**External verification and tool-based checking.** Training Verifiers to Solve Math Word Problems introduced GSM8K and showed that a learned verifier model, used to rerank multiple sampled solutions, substantially outperforms a single greedy generation and scales better with additional data than fine-tuning alone [6]. Chain-of-Verification reduces hallucination by having a model draft an answer, independently generate and answer verification questions, and then reconcile the two, and shows this decoupling of verification from the original generation reduces factual errors on list-based and long-form tasks [7]. Both approaches share our core design principle -- that verification should not simply re-run the same generative process and hope for a different, more careful answer, but should introduce a structurally distinct signal -- but neither targets arithmetic step-level correctness with a compact numeric invariant, and neither reports what happens when the verification procedure itself exceeds a smaller model's capacity, which our weak-model result suggests is not a negligible edge case.

**Mechanistic diagnosis of arithmetic self-verification failure.** The Validation Gap provides circuit-level evidence that language models' internal error-detection relies on shallow surface-level numeric-consistency heads that check superficial agreement between tokens, rather than genuine independent recomputation of the underlying arithmetic [4]. This work is purely diagnostic and mechanistic: it identifies why self-critique should be expected to fail, but proposes and evaluates no behavioral intervention. Chain-of-Thought prompting demonstrated that eliciting explicit intermediate reasoning steps substantially improves arithmetic and multi-step reasoning accuracy relative to direct answer generation [8], establishing that models can be steered toward more reliable step-by-step computation through prompt structure alone -- a premise our checksum condition extends from problem-solving to error-checking, but also a premise that assumes the model can execute the added structure competently, an assumption Wei et al. test on capable models and that our weak-tier result shows does not transfer downward. Large Language Models Cannot Self-Correct Reasoning Yet presents a systematic empirical audit finding that self-correction without external feedback degrades performance across several reasoning benchmarks, largely because models cannot reliably tell correct output from incorrect output [2]. Our work directly operationalizes the fix implied but not tested by the mechanistic diagnosis: give the model an external-feeling, structurally independent invariant rather than asking it to introspect on its own derivation -- and shows this fix is itself capability-gated rather than universally applicable.

**Casting out nines as a checksum.** Casting out nines is a centuries-old manual bookkeeping technique for catching arithmetic slips by comparing digit-root (mod-9) residues, and is a direct ancestor of modern checksum schemes such as the Luhn algorithm used for credit-card and identifier validation. To the searches conducted for this work, it has not previously been evaluated as an explicit LLM self-verification prompting strategy for word-problem arithmetic; our contribution is the direct methodological transfer of this specific numeric invariant into LLM self-critique, evaluated against matched controls across a capability range rather than assumed to help uniformly.

# Preliminaries

**Digit root / casting out nines.** The digit root of an integer is obtained by repeatedly summing its digits until a single digit (1-9, or 0 for a multiple of 9) remains. Because 10 is congruent to 1 modulo 9, every integer is congruent modulo 9 to its digit sum, and therefore to its digit root. Consequently, if two numbers are combined by addition, subtraction, or multiplication to produce a result, the same operation applied to their digit roots (with results reduced back to a single digit) must be congruent modulo 9 to the digit root of the true result. A mismatch proves an arithmetic error exists in that step; agreement is necessary but not sufficient for correctness.

**Checksum-detectable vs. checksum-invisible errors.** An injected or naturally occurring arithmetic error is checksum-detectable if it changes the mod-9 residue of the affected computation's result -- for example, most digit transpositions, dropped carries, and sign flips. An error is checksum-invisible if it leaves the mod-9 residue unchanged -- for example, a wrong-operand substitution that happens to preserve the residue, or any purely logical or modeling error (misreading the problem, applying the wrong operation to correctly-computed numbers) that does not corrupt an individual arithmetic step's residue at all. Checksum-invisible errors define a hard ceiling: no digit-root check, however well executed, can catch them. In this evaluation's underlying experiment, 64 of 200 problems (32.0%) fall in the checksum-detectable category under the experiment's own injected-error characterization, cross-checked bit-for-bit against the evaluation's independent reproduction of the same random seed.

**Free-form vs. matched-length placebo vs. checksum critique.** All three critique conditions share an identical baseline solve instruction -- "Solve this problem step by step and give the final numeric answer as 'Answer: <n>'" -- appended with a condition-specific critique instruction (verbatim text in Appendix A). Free-form critique adds only "Then check your work above for mistakes. If you find an error, correct it and give a final revised answer." The matched-length placebo instructs the model to restate each arithmetic sub-step's operands and result, spell out their digits in words, count digits, and compare digit counts between operands and result -- a review procedure that is explicitly labeled in-prompt as "a formatting/presentation review, not a mathematical re-check" and does not encode a true mod-9 invariant, controlling for the possibility that any structured-looking extra deliberation helps regardless of content. The checksum critique walks the model through computing the digit-root checksum of each arithmetic sub-step, ending each step's check with an explicit CHECKSUM_OK or CHECKSUM_MISMATCH token, and instructs it to revise a step only if the checksums disagree.

# Methods

## Benchmark Construction

The underlying experiment draws its 200 base word problems from a 5-template procedural generator (shopping, recipe-scaling, distance-rate-time, unit-conversion, inventory-accounting) with computation traces (operand, operation, result, dependency) emitted directly at generation time, guaranteeing exact, verifiable step traces without the parsing risk of natural-language-derived reasoning chains. This generator is one of the two component sources of our separately built and independently verified 1,935-row benchmark [ARTIFACT:art_UafZp2AqR5at], which additionally incorporates 200 real GSM8K word problems (openai/gsm8k, main configuration, pooled train and test splits) whose official calculator-annotation reasoning traces are parsed via regex over the `<<operand op operand=result>>` annotations, plus a deterministic error-injection layer producing up to 1,535 checksum-labeled corrupted variants. We report as a limitation in Section 6 that the specific experiment underlying this iteration's results consumed only the procedurally generated half of that benchmark, not the GSM8K-derived half, because the run intended to exercise the full joined benchmark did not produce output in time for this analysis; the GSM8K-vs-synthetic accuracy breakdown a reviewer requested therefore remains explicitly unavailable rather than approximated [ARTIFACT:art_0V-2bxn9h7_u].

On top of the 200 base items, the same deterministic error-injection procedure used in the benchmark artifact characterizes each item's injected-error checksum-detectability by exact re-derivation and residue comparison, yielding the 64/200 (32.0%) checksum-detectable fraction used to define the detectable and invisible subsets analyzed throughout Section 5.

## Experimental Conditions

We compare five conditions on each of 200 word problems per model, using OpenRouter at temperature 0.0 and a 2,500-token generation budget [ARTIFACT:art_VCF3BbfSo_RV]:

1. **Baseline (no self-check).** The model produces a solution with no critique step.
2. **Free-form critique.** After producing an initial solution, the model is asked to "check your work" with no specified procedure, and may revise its answer.
3. **Placebo critique.** The model performs a length-matched, similarly deterministic-looking digit-spelling/digit-counting review procedure that does not encode a true mod-9 invariant, controlling for the confound that any additional structured deliberation tokens could help independent of content.
4. **Checksum critique.** The model is walked through computing the digit-root checksum for each arithmetic sub-step of its own solution and is instructed to flag and revise a step only if the checksums disagree, ending each check with CHECKSUM_OK or CHECKSUM_MISMATCH.
5. **Oracle detection-isolation ablation.** Restricted to the checksum-detectable subset (n=64 per model), the model is given an already-computed checksum mismatch signal externally -- naming the specific step, operands, and the correct-versus-claimed digit root -- rather than computing it itself, isolating "can the model use a checksum" from "can the model compute one."

We measure five families of metrics: (a) final-answer accuracy per model and condition, reported overall and split by checksum-detectable and checksum-invisible subsets, with paired significance testing via exact McNemar tests on discordant pairs and a 10,000-resample bootstrap confidence interval on the accuracy difference; (b) error-detection precision, recall, and F1 with closed-form Wilson 95% confidence intervals, computed per model, condition, and checksum-detectability stratum from whether a condition flagged an error against whether the same model's own unedited baseline solve on that problem actually differed from the gold answer -- the ground-truth-adjacent signal available since this experiment solves each problem's original, uncorrupted statement -- with every cell below n=20 explicitly flagged as underpowered rather than silently reported as if fully powered [ARTIFACT:art_0V-2bxn9h7_u]; (c) correction accuracy conditional on a true-positive flag being raised, again per condition, model, and stratum with Wilson CIs and small-n flags; (d) the oracle-vs-self-computed-checksum fix-rate comparison; and (e) a dependency-free Pearson correlation between per-example response-length gain (checksum-condition length minus baseline-condition length) and per-example accuracy gain, to check whether any accuracy effect tracks response length rather than condition identity. Separately, a deterministic, regex-only mod-9 digit-root checker -- with zero LLM calls -- parses every "digit root of N" claim the model makes in its own checksum-critique trace, recomputes the true digit root via the closed-form formula (self-checked against brute-force digit-summing before use), and reports the fraction of traces containing at least one arithmetic error in the model's own checksum computation; this checker is additionally cross-validated against a freshly re-run LLM-judge pass over the same 70-trace paired sample via Cohen's kappa, replacing our prior draft's uncontrolled same-model-judge design [ARTIFACT:art_0V-2bxn9h7_u].

# Results

[FIGURE:fig2]

## Overall Accuracy Is Capability-Stratified, Not Monotonically Diminishing

For anthropic/claude-haiku-4.5, whose no-critique baseline accuracy is 76.5% (n=200) -- leaving substantial headroom below ceiling -- self-check condition matters a great deal. Free-form critique raises accuracy modestly to 80.5%. The matched-length placebo raises it further, to 91.0%, confirming that generic structured deliberation carries real value independent of any specific invariant. The checksum critique raises accuracy the most, to 97.5% overall. On the full 200-problem sample, checksum critique beats free-form critique by 17.0 percentage points (bootstrap 95% CI [12.0, 22.0]; exact McNemar on 36 discordant pairs, n01=35 corrected by checksum but not free-form, n10=1 the reverse, p=1.08x10^-9) and beats the placebo by 6.5 percentage points (bootstrap CI [3.0, 10.0]; McNemar n01=14, n10=1, p=9.77x10^-4). On the checksum-detectable subset specifically (n=64), the checksum-vs-placebo gap is 9.375 percentage points (bootstrap CI [3.1, 17.2]).

For openai/gpt-4o-mini, the picture is a flat null result rather than a diminished-but-present effect. Baseline accuracy is already 95.5% (n=200), leaving little room for any self-check condition to demonstrate an advantage: free-form critique reaches 94.0%, the placebo reaches 97.5%, and checksum critique reaches 96.0%. None of these differences survive scrutiny: checksum vs. free-form is a 2.0-percentage-point gap (bootstrap CI [-2.0, 6.0], McNemar n01=11, n10=7, p=0.481), and checksum vs. placebo is a -1.5-percentage-point gap (bootstrap CI [-5.5, 2.0], McNemar n01=5, n10=8, p=0.581). On the checksum-detectable subset (n=64), the checksum-vs-placebo gap is exactly 0.0 percentage points.

For meta-llama/llama-3.1-8b-instruct, the picture inverts entirely rather than merely flattening. Baseline accuracy is 84.5% (n=200) -- comparable headroom to claude-haiku-4.5's -- so a diminishing-effect-with-capability story would predict a smaller but still positive checksum benefit here. Instead, free-form critique already drops accuracy to 78.9% (n=199; one of 2,592 total API calls failed for this condition), the placebo drops it further to 46.7% (n=199), and checksum critique collapses it to 17.1% (n=199). The checksum-vs-free-form gap is -61.9 percentage points (bootstrap CI [-69.5, -54.3], n=197 after excluding the one failed call from each side; McNemar n01=5 cases newly correct under checksum, n10=127 cases newly wrong, p=1.18x10^-31), and the checksum-vs-placebo gap is -28.9 percentage points (bootstrap CI [-37.1, -20.8]; McNemar n01=14, n10=71, p=2.43x10^-10). On the checksum-detectable subset (n=62 after exclusions), the checksum-vs-placebo gap is -33.9 percentage points (bootstrap CI [-48.4, -17.7]). Every one of these comparisons is overwhelmingly statistically significant in the harmful direction; this is not a null result obscured by noise, but a large, reliable degradation.

[FIGURE:fig3]

## Why the Weak Model Collapses: A Bookkeeping-Overload Failure Mode

The magnitude of llama-3.1-8b-instruct's collapse cannot be explained by the checksum condition simply flagging more errors and revising correctly-solved problems into incorrect ones: only 10 of 199 checksum-critique responses raised an explicit error flag, and correction accuracy given a genuine true-positive flag was in fact 0% for this model in this condition (0/1 true positive corrected to the gold answer; see correction-accuracy table below), not a source of mass corruption on its own. The dominant driver is instead visible in response length and in manual trace inspection: mean response length under checksum critique is 4,198 characters for this model, roughly 8x the 526-character no-critique baseline and more than double the placebo's 1,613-character mean, and the Pearson correlation between per-example response-length gain and per-example accuracy gain for this model is -0.40 (n=597), the strongest and most negative of the three models (claude-haiku-4.5: +0.34, n=600; gpt-4o-mini: -0.16, n=600) -- longer checksum-critique responses are associated with worse, not better, outcomes specifically for the weak model.

A representative trace illustrates the mechanism directly. On a six-step inventory word problem (starting quantity 410, three additive transactions, then a multiplicative step, correct final answer computed by the base solve), the model's checksum-critique trace correctly computes the first several digit roots, then -- partway through the checksum bookkeeping -- introduces a computation that does not correspond to any operation in the original problem ("the number of boxes is multiplied by 4"), carries this fabricated step through the remainder of its digit-root verification, and outputs a final answer that reflects neither the original problem's arithmetic nor a coherent alternative derivation. This pattern -- an unprompted extra operation appearing mid-checksum and propagating to the final answer -- recurs across the sampled traces we inspected and is consistent with the length and correlation evidence: the checksum procedure's dual demand (perform the original arithmetic correctly, and simultaneously track a second, structurally distinct digit-root computation per step) exceeds this model's capacity to keep both computations straight, and the interference corrupts the primary derivation rather than merely failing to improve it. This is qualitatively different from the free-form and placebo conditions' more modest degradations (84.5% to 78.9% and 46.7% respectively), which plausibly reflect ordinary self-critique unreliability rather than induced hallucination of new problem content.

## Detection Precision, Recall, and Correction Accuracy: A Properly Powered Re-Audit

Our previous draft's detection-metric family was reported as largely underpowered because most models rarely erred on their own baseline solve, leaving few true positives to measure against. This iteration's dedicated re-audit computes the same family of metrics with closed-form Wilson 95% confidence intervals and an explicit underpowered-n<20 flag on every cell, across all three models, four conditions, and three checksum-detectability strata [ARTIFACT:art_0V-2bxn9h7_u]. The pattern confirms the accuracy-level story rather than adding a contradictory signal. For claude-haiku-4.5 under checksum critique, precision on the full sample is 1.0 (95% CI [0.61, 1.0], 6 true positives, 0 false positives out of 200 problems) and recall is 0.128 (95% CI [0.060, 0.252], 6 of 47 baseline-wrong problems flagged); on the checksum-invisible stratum specifically (n=136, by definition unreachable by a mod-9 check), recall is 0.182 (95% CI [0.086, 0.344]), showing the checksum framing catches some errors even outside its theoretical ceiling, plausibly via the more careful step-by-step re-derivation it induces. Correction accuracy given a true-positive flag is 1.0 (6/6) for claude-haiku-4.5's checksum condition, versus 0.0 (0/1) for llama-3.1-8b-instruct's and 1.0 (1/1) for gpt-4o-mini's -- all at n<20 and explicitly flagged underpowered, consistent with the accuracy-level finding that llama-3.1-8b-instruct's problem is not correction given a valid flag (which happens rarely) but corruption of already-correct derivations that never gets flagged at all. gpt-4o-mini's checksum condition shows the opposite precision profile from claude-haiku-4.5's: precision is 0.053 (95% CI [0.009, 0.246], 1 true positive against 18 false positives out of 200), i.e. this model raises many more flags than it has genuine errors to find, though this over-flagging does not translate into an accuracy cost given its near-ceiling ground truth. We report the full per-cell table, including every underpowered cell, in the evaluation artifact rather than presenting only the well-powered subset, so that a reader can judge which point estimates to trust [ARTIFACT:art_0V-2bxn9h7_u].

## Checksum Self-Computation Reliability: Deterministic Checker Replaces Same-Model Judge

[FIGURE:fig4]

Our previous draft measured checksum self-computation reliability using an LLM judge (claude-haiku-4.5) that was also one of the two evaluated models -- a same-model circularity a reviewer correctly identified as a potential source of correlated bias. This iteration replaces that design with a deterministic, regex-only mod-9 digit-root checker that requires zero LLM calls: it parses every "digit root of N" claim across all 599 checksum-critique traces (200 claude-haiku-4.5, 199 llama-3.1-8b-instruct, 200 gpt-4o-mini), independently recomputes the true digit root via the closed-form casting-out-nines formula, and flags any trace whose claimed digit root disagrees with the recomputed one. Of 312 traces containing at least one parseable digit-root claim, 30 contain at least one arithmetic error, an overall 9.6% error rate -- materially lower than, and now superseding, our prior same-model-judge estimate of 15.4% (80 traces) [ARTIFACT:art_0V-2bxn9h7_u]. Per-model error rates track capability in the expected direction: claude-haiku-4.5 is most reliable at the checksum sub-task (4.5% error rate, 6/134 parseable traces), llama-3.1-8b-instruct is least reliable (12.4%, 11/89), and gpt-4o-mini falls between (14.6%, 13/89) -- notably, gpt-4o-mini's checksum-computation error rate is the highest of the three models even though its overall task accuracy is highest, underscoring that checksum-sub-task reliability and end-task accuracy are not the same quantity.

To validate the substitution itself, we re-ran a fresh LLM-judge pass (same prompting design as the prior draft, independently recomputing each digit-root claim before issuing a verdict) over the same 70-trace paired sample the deterministic checker evaluated, and computed Cohen's kappa between the two methods' per-trace verdicts. Agreement is 77.1% raw, but Cohen's kappa -- which corrects for chance agreement given each method's marginal error-flagging rate -- is -0.12, i.e. worse than chance-level agreement (confusion matrix: 0 traces where both methods agree an error is present, 6 where the checker flags an error the judge misses, 10 where the judge flags an error the checker misses, 54 where both agree the trace is clean). A negative kappa here means the LLM judge's error-flagging is essentially uncorrelated with, or anti-correlated with, ground-truth arithmetic correctness as measured by direct recomputation, which is direct evidence -- not merely a plausibility argument -- for discarding the same-model-judge design rather than treating it as a noisy-but-usable approximation. We adopt the deterministic checker's 9.6% figure as the primary estimate going forward and treat the prior 15.4% same-model-judge figure as superseded.

## Ruling Out Length as the Sole Driver for the Model That Benefits

For claude-haiku-4.5, the model whose gain is causally attributable to the invariant rather than to length, response length under checksum critique (mean 1,355 characters) is close to but slightly shorter than under the placebo (mean 1,420 characters) -- a placebo-to-checksum length ratio of 1.05, i.e. the placebo is if anything slightly longer. Since checksum critique still outperforms this length-matched-or-longer placebo by 6.5 percentage points on the full sample (9.375 points on the checksum-detectable subset), the gap cannot be attributed to the checksum condition simply producing more deliberation tokens. The per-example response-length-gain-vs-accuracy-gain Pearson correlation for claude-haiku-4.5 is +0.34 (n=600, pooled across all three non-baseline conditions), positive but modest, consistent with length correlating with but not fully explaining the accuracy effect; for the two other models the same correlation is near-zero or negative (gpt-4o-mini: -0.16; llama-3.1-8b-instruct: -0.40), the opposite sign one would expect if "more tokens helps" were a universal mechanism. Taken together with the placebo comparison, this indicates the checksum invariant's content, not sheer verbosity, is what produces claude-haiku-4.5's gain -- and that verbosity is, if anything, actively harmful for the weak model.

# Discussion

Our results substantially revise the scope of the original hypothesis, in the direction reviewer feedback pushed us toward but with a sharper conclusion than "benefit concentrated where the model is hungry." With three capability tiers now evaluated -- strong (claude-haiku-4.5), mid (gpt-4o-mini), weak (llama-3.1-8b-instruct) -- the pattern is not a monotonic decline in benefit as baseline accuracy rises. It is a three-way split: a large, causally isolated positive effect for the strong model; a null effect, not a smaller positive effect, for the mid-capability model; and a large, statistically overwhelming negative effect for the weak model. We are explicit that three models is still a small panel and does not establish a general functional form (e.g. a capability threshold, a U-shaped curve, or something else) relating baseline capability to checksum-critique effect size -- we report this as a three-point pilot pattern that motivates, but does not itself confirm, a broader capability-conditioned deployment rule, and we no longer use language implying a smooth "free lunch where the model is hungry" trend, since the weak-model result shows headroom alone (llama-3.1-8b-instruct's 84.5% baseline is comparable to claude-haiku-4.5's 76.5%) does not predict the sign of the effect, let alone its magnitude.

For claude-haiku-4.5, the checksum condition beats a placebo matched for length and deterministic appearance by a significant 6.5 percentage points on the full sample and 9.375 points on the checksum-detectable subset, with the placebo's response length if anything slightly exceeding the checksum condition's. This is the strongest evidence within our design that the content of the invariant matters, not just the presence of extra structured text -- precisely the causal question a matched-effort placebo is meant to answer, and one largely absent from prior self-critique studies [1, 2, 3, 9].

The weak-model result is, we think, the paper's most practically important finding, and one our previous two-model draft could not have surfaced. A prompt-engineering pattern that looks purely additive -- "also do this extra mechanical check" -- is not additive in effect when the base model cannot reliably execute two interleaved computations without interference. The manual trace evidence (Section 5) shows this is not simply "the weak model fails to benefit"; it is "the weak model's baseline-correct derivation gets actively corrupted by fabricated intermediate steps introduced while performing the checksum bookkeeping," a distinct and more concerning failure mode than the inert null result gpt-4o-mini shows. This has a direct deployment implication: any pipeline considering a mechanically-scaffolded self-critique step for cost or latency reasons (i.e. routing to a smaller model) should not assume the scaffold is safe merely because it worked well on a stronger model, and should validate the specific model-scaffold pairing rather than the scaffold in isolation.

The detection precision/recall re-audit clarifies where the strong model's remaining error lives without over-claiming what a small-n, single-experiment table can support: claude-haiku-4.5's checksum condition has perfect precision (no false alarms in this sample) but low recall (12.8% overall, meaning most of its own baseline errors go unflagged), and correction given a genuine flag is perfect (6/6) though at an underpowered n. This is directionally consistent with our prior draft's oracle-ablation claim that correction is not the bottleneck once a flag is raised, but we no longer present that as a confirmed finding at this sample size -- the re-audit artifact's own verdict summary marks the oracle-vs-self-computed comparison as REVISED rather than confirmed, pending more true-positive cases than 200 problems at a 32% checksum-detectable rate can supply [ARTIFACT:art_0V-2bxn9h7_u].

The deterministic-checker replacement of our same-model LLM-judge audit is not a cosmetic methodology fix; the negative Cohen's kappa (-0.12) between the two methods is direct evidence that the same-model judge's verdicts were not tracking ground-truth arithmetic correctness, which retroactively undermines confidence in any conclusion our prior draft drew from that judge's 15.4% figure beyond its role as a rough order-of-magnitude estimate. The deterministic checker's revised 9.6% figure, and its capability-ordered per-model breakdown (4.5% claude-haiku-4.5, 12.4% llama-3.1-8b-instruct, 14.6% gpt-4o-mini), is the figure we now treat as primary, and we recommend that any future self-verification-reliability audit of this kind default to a deterministic checker wherever the checked quantity (here, a closed-form arithmetic fact) admits one, rather than an LLM judge, same-model or otherwise.

We surface two further limitations candidly. First, the GSM8K-versus-procedurally-generated accuracy breakdown a reviewer specifically requested, to determine whether claude-haiku-4.5's comparatively low 76.5% no-critique baseline reflects genuine task difficulty or a benchmark-composition artifact, remains unavailable: the experiment analyzed in this iteration used only the procedurally generated half of our benchmark (0 GSM8K-sourced items), and the run intended to exercise the full joined benchmark did not complete in time for this analysis. We mark this explicitly UNSUPPORTED/pending rather than approximating it, and flag it as the single highest-priority item for the next iteration, since the dataset needed to answer it already exists and is fully verified [ARTIFACT:art_UafZp2AqR5at]. Second, our benchmark's procedurally generated problems draw numeric ranges and chain lengths (up to 6 steps, operands up to several hundred) that are somewhat more demanding than typical GSM8K items, which plausibly contributes to baseline accuracies below commonly reported GSM8K figures independent of any GSM8K-specific effect; we cannot yet decompose these two contributions without the pending GSM8K-split run.

# Conclusion

Replacing an open-ended "check your work" instruction with an explicit, mechanically-computed casting-out-nines checksum does not act as a uniform reliability upgrade. Across three models spanning strong, mid, and weak baseline capability, we find a genuine, causally isolated, statistically significant improvement for the strong model (claude-haiku-4.5: 76.5% to 97.5% overall accuracy, beating a length-matched placebo by 6.5 to 9.375 percentage points depending on subset), no measurable effect for the mid-capability model already near ceiling (gpt-4o-mini: 95.5% baseline, every pairwise condition comparison statistically indistinguishable), and a large, statistically overwhelming degradation for the weak model (llama-3.1-8b-instruct: 84.5% to 17.1%, driven by the checksum procedure's bookkeeping load inducing hallucinated computation steps that corrupt an otherwise-correct derivation). This three-way, non-monotonic pattern is the central empirical correction this iteration makes to our own prior two-model draft, and it argues against treating "give the model a mechanically-defined invariant instead of a vague instruction" as a general-purpose self-critique fix; the fix's value is conditional on the underlying model's capacity to execute the added mechanical procedure without interference, not merely on its having room to improve. A deterministic, LLM-free re-audit of checksum self-computation reliability supersedes our earlier same-model LLM-judge estimate (15.4%, itself shown here to disagree with the deterministic ground truth at worse-than-chance levels, Cohen's kappa=-0.12) with a lower, more trustworthy figure (9.6%, 30/312 parseable traces), and a properly powered precision/recall/F1 re-audit replaces the underpowered proxy metric our previous draft candidly flagged as a design limitation.

Future work should prioritize, in order: (1) completing the pending run that joins the four critique conditions against the full GSM8K-plus-synthetic benchmark, including its 1,535 labeled error-injection variants, to obtain the GSM8K-vs-synthetic baseline decomposition and the ground-truth-labeled detection precision/recall analysis this iteration still cannot fully deliver; (2) extending the model panel beyond three points, particularly with models between llama-3.1-8b-instruct's and gpt-4o-mini's capability level, to determine whether the observed strong-null-catastrophic pattern reflects a sharp capability threshold or a smoother underlying relationship we lack the resolution to distinguish; and (3) directly instrumenting why the checksum procedure specifically induces hallucinated computation steps in weaker models -- for example, by testing whether providing the checksum bookkeeping in a separate, sequential turn rather than an interleaved single-turn instruction avoids the interference we document here.

# Appendix A: Verbatim Critique Condition Prompts

All four solve-time conditions share the identical base solve instruction: "Solve this problem step by step and give the final numeric answer as 'Answer: <n>'.\n\nProblem: {problem}". Each critique condition appends the following text to that base instruction.

**Free-form critique:** "Then check your work above for mistakes. If you find an error, correct it and give a final revised answer as 'Answer: <n>'."

**Placebo critique:** "Then, for EACH arithmetic sub-step above, restate the two operand values and the result value, spell out each of their digits one by one in words (e.g. 'four, two, one'), count how many digits each number has, and state whether the result has more, fewer, or the same number of digits as the larger operand. Show this digit-listing review explicitly for every step (this is a formatting/presentation review, not a mathematical re-check, and finding more/fewer/same digits does NOT by itself indicate an error). If, separately, you notice an actual arithmetic error while doing this, correct it and give a final revised answer as 'Answer: <n>'."

**Checksum critique:** "Then, for EACH arithmetic sub-step above, compute the digit root (repeatedly sum the digits of a number until one digit remains) of each operand and of the result, and verify the operands' digit-root relationship matches the result's digit root under mod-9 arithmetic (this is the 'casting out nines' checksum). Show each step's digit-root check explicitly, ending each check with either CHECKSUM_OK or CHECKSUM_MISMATCH. Only revise a step if its digit roots are inconsistent. Give a final revised answer as 'Answer: <n>'."

**Oracle detection-isolation ablation** (checksum-detectable subset only): base solve instruction plus "A checker has flagged that your step '{step_desc}' has a casting-out-nines checksum mismatch: digit_root({a}) {op} digit_root({b}) should equal digit_root({correct_result}) under mod-9 arithmetic, but your computed result of {wrong_result} does not satisfy this. Fix this step and give the final revised answer as 'Answer: <n>'."

All conditions were sampled at temperature 0.0 with a 2,500-token generation budget via OpenRouter.

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

[10] J. Cohen. A Coefficient of Agreement for Nominal Scales. Educational and Psychological Measurement, 20(1), 1960.
</current_paper>

<reviewer_feedback>
Feedback from the paper reviewer this iteration.

- [MAJOR] (methodology) The 'properly powered' detection precision/recall/F1 re-audit (art_0V-2bxn9h7_u), despite its improved statistical rigor (Wilson CIs, small-n flags), still computes ground truth as 'the model's own baseline (no-critique) solve differing from the gold answer' on the ORIGINAL, uncorrupted problems -- not against the benchmark's actual labeled, injected arithmetic errors (the 1,535-row error-injection layer built specifically for this purpose). The artifact's own note states the intended iter_2 error-injection experiment never produced output, so this re-audit substitutes a re-analysis of the same iter_1 self-solve/self-critique data used in the original evaluation. This means the checksum-detectable-vs-invisible split (32.0% detectable) is a label attached to a hypothetical corruption characterization of the original problem, not a test of whether the model actually catches an error it was shown. This was the substance of a major critique in the previous review round and remains only partially addressed.
  Action: Run the four critique conditions on the corrupted-variant rows themselves (input = corrupted trace rendered as text, expecting the model to both notice and correct the injected error) using the already-built and verified 1,535-row error-injection dataset in art_UafZp2AqR5at. This converts the detection metrics from a proxy (own-solve-was-wrong) into a direct test of the paper's central mechanistic claim, and is a bounded, already-designed experiment rather than new benchmark construction -- exactly the fix recommended in the prior review round, which the current re-audit's own data-availability note confirms was not actually run this iteration.
- [MINOR] (scope) The three-model panel (claude-haiku-4.5, gpt-4o-mini, llama-3.1-8b-instruct) spans different vendors, training recipes, and instruction-tuning regimes, not just different capability levels within a controlled family. The paper's central 'capability-conditioned' framing implicitly treats baseline accuracy as the operative variable, but the observed non-monotonic pattern could equally reflect vendor-specific instruction-following brittleness under long, structured multi-part prompts rather than capability per se -- llama-3.1-8b-instruct's collapse could be partly an artifact of Meta's instruction-tuning style on long compound instructions rather than a pure function of 'weakness'.
  Action: Either add a same-family capability sweep (e.g., multiple sizes of one model family, such as Llama-3.1-8B/70B or Qwen2.5 at several sizes) as a complementary within-family comparison, or explicitly caveat in the Discussion that the current three-model result confounds vendor/training-recipe differences with capability level, and that the 'capability threshold' framing should be read as a hypothesis motivated by, not established by, this panel.
- [MINOR] (clarity) The manual trace-inspection evidence for the mechanistic explanation of llama-3.1-8b-instruct's collapse (Section 6) is illustrated with a single representative trace and the phrase 'recurs across the sampled traces we inspected' without stating how many traces were sampled, how they were selected, or what fraction showed the fabricated-step pattern versus other failure modes.
  Action: Report the number of traces manually inspected, the sampling method (e.g., random subset of the 199 checksum-critique responses, or all traces where accuracy flipped from correct to incorrect), and the fraction exhibiting the 'fabricated intermediate step' pattern specifically, so the qualitative claim in Section 6 has a quantified denominator rather than resting on one illustrative example.
- [MINOR] (rigor) The detection-precision result that gpt-4o-mini's checksum condition has precision of only 0.053 (18 false positives vs. 1 true positive out of 200) despite the model showing no measurable accuracy cost is presented as a curiosity ('does not translate into an accuracy cost') without exploring what these 18 false-positive flags actually contain -- e.g., whether the model is flagging problems as CHECKSUM_MISMATCH but then declining to revise its (already-correct) answer, versus revising and still landing on the correct answer by chance.
  Action: Break down the 18 false-positive-flagged gpt-4o-mini cases by whether the model revised its answer after flagging (and if so, whether the revision was a no-op, a correct revision of an already-correct answer, or a near-miss), to clarify whether the null accuracy effect for this model is 'high precision needed anyway' or 'the model over-flags but doesn't act on its own flags,' which have different implications for deploying this scaffold on near-ceiling models.
- [MINOR] (evidence) The GSM8K half of the underlying benchmark (200 real, verified GSM8K items) remains completely unused this iteration (0 GSM8K-sourced items in the analyzed experiment), which is the same limitation flagged in the previous review round as a way to distinguish genuine task difficulty from benchmark-composition artifacts in claude-haiku-4.5's comparatively low 76.5% no-critique baseline. The paper is commendably explicit that this is UNSUPPORTED/pending rather than approximated, but the underlying data needed to close this gap has existed since the prior iteration and still was not run.
  Action: Prioritize completing the pending run against the joined GSM8K+synthetic benchmark before the next iteration, since (as the paper itself states) this is the single highest-priority remaining gap and the dataset is already built and verified -- this should not require new benchmark construction, only executing the four critique conditions against the already-available GSM8K-derived rows.
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

### [3] HUMAN-USER prompt · 2026-07-31 21:12:36 UTC

```
Does adding a short self-critique step before answering improve accuracy on multi-step arithmetic word problems?
```

### [4] TOOL CALL — Write · 2026-07-31 21:13:04 UTC

```
File: /home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_0WmBa7GFLIzI/3_invention_loop/iter_2/upd_hypo/upd_hypo/.terminal_claude_agent_struct_out.json

{
  "title": "Checksum Critique: Capability-Gated, Not Universal",
  "hypothesis": "When an LLM verifies its own multi-step arithmetic word-problem solution using an explicit, mechanically-computed modular-arithmetic invariant (a 'casting-out-nines' digit-root checksum applied to each intermediate computation) instead of an open-ended 'double-check your work' self-critique prompt or a length-matched content-null placebo critique, the effect on error-detection and downstream correction accuracy is not a uniform benefit and is not simply monotonically diminishing with baseline capability -- it is capability-gated in a way that can invert sign entirely. On claude-haiku-4.5 (76.5% no-critique baseline, n=200), checksum critique raised accuracy to 97.5%, beating free-form critique by 17.0pp (McNemar p=1.08e-9) and the matched-length placebo by 6.5pp overall / 9.375pp on the checksum-detectable subset (bootstrap CI excludes zero), with the placebo response length if anything slightly exceeding the checksum condition's -- evidence the gain is attributable to the invariant's content, not extra deliberation tokens. On openai/gpt-4o-mini (95.5% baseline, near ceiling), all four conditions are statistically indistinguishable (largest gap 2.0pp, p=0.481), a flat null rather than a smaller positive effect. On meta-llama/llama-3.1-8b-instruct (84.5% baseline -- comparable headroom to claude-haiku-4.5's, which rules out 'headroom alone' as the operative variable), checksum critique collapses accuracy to 17.1% (McNemar p=1.2e-31 vs free-form), a catastrophic degradation traced qualitatively to the model fabricating extra computation steps absent from the original problem while performing the interleaved digit-root bookkeeping, evidenced by an 8x baseline response-length blowup and a strongly negative length-vs-accuracy-gain correlation (-0.40) unique to this model. This three-point pattern is treated as a pilot observation motivating, not establishing, a general capability-threshold or U-shaped functional form, and -- per reviewer critique -- the three models differ in vendor and instruction-tuning regime as well as capability, so the 'capability-conditioned' framing is explicitly a hypothesis to be tested with a same-family capability sweep, not a confirmed causal claim; llama-3.1-8b-instruct's collapse may partly reflect vendor-specific brittleness under long compound instructions rather than pure capability. The self-computed-checksum reliability bottleneck claim is revised: a deterministic, zero-LLM-call regex-based mod-9 checker (replacing the prior same-model LLM-judge design, which a follow-up Cohen's kappa of -0.12 against the same 70-trace sample shows performs at worse-than-chance agreement with ground truth) finds a 9.6% checksum-computation error rate overall, ordered by model capability (4.5% claude-haiku-4.5, 12.4% llama-3.1-8b-instruct, 14.6% gpt-4o-mini) -- notably not perfectly capability-ordered, since gpt-4o-mini has the highest checksum-computation error rate despite the highest task accuracy, indicating checksum-sub-task reliability and end-task accuracy are dissociable quantities. A major methodological gap remains unresolved across two review rounds: detection precision/recall has still only been measured via the proxy 'model's own baseline solve on the ORIGINAL uncorrelated problem differs from gold', not by running the four critique conditions directly on the already-built, verified 1,535-row error-injection dataset (art_UafZp2AqR5at) where ground truth is a known injected error the model is shown -- this remains the single highest-priority open test of the paper's central mechanistic claim (does the model actually catch an error it was shown corrupted, not merely disagree with itself) and is treated as unsupported until run.",
  "relation_rationale": "Same checksum-critique frame; specialized into a three-way capability-gated (not monotonic) claim with vendor-confound caveat",
  "confidence_delta": "unchanged",
  "key_changes": [
    "Replaced the two-model 'benefit vanishes near ceiling' framing with the three-model finding that the effect is non-monotonic: strong-model gain, mid-model null, weak-model catastrophic collapse (not diminishing benefit)",
    "Added explicit reviewer-driven caveat that the three-model panel confounds vendor/instruction-tuning regime with capability level, so 'capability-conditioned' is a motivated hypothesis, not an established finding, pending a same-family sweep",
    "Elevated the still-unresolved major reviewer critique (detection metrics rely on own-solve-wrong proxy, not the built error-injection dataset's known ground truth) as the paper's single largest open validity gap, now flagged across two consecutive review rounds",
    "Replaced the same-model LLM-judge checksum-reliability estimate (~15%) with the deterministic checker's cross-validated 9.6% figure, and noted the judge's negative Cohen's kappa as direct evidence the same-model-judge design should be discarded, not merely caveated",
    "Added the dissociation finding that checksum-computation reliability does not track end-task accuracy ordering (gpt-4o-mini highest error rate, highest accuracy)",
    "Removed the now-unsupported 'headroom sets the ceiling' framing since llama-3.1-8b-instruct had comparable headroom to claude-haiku-4.5 yet the effect inverted in sign"
  ],
  "relation_type": "evolution",
  "artifact_relations": [
    {
      "from_id": "art_UafZp2AqR5at",
      "to_id": "art_0V-2bxn9h7_u",
      "relation_type": "uses",
      "relation_rationale": "Intended to test on the dataset's error-injection labels/RNG seed, but the target experiment never ran so it fell back to iter_1 data"
    }
  ]
}
```

### [5] TOOL RESULT — Write · 2026-07-31 21:13:04 UTC

```
{"type": "create", "filePath": "/home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_0WmBa7GFLIzI/3_invention_loop/iter_2/upd_hypo/upd_hypo/.terminal_claude_agent_struct_out.json", "content": "{\n  \"title\": \"Checksum Critique: Capability-Gated, Not Universal\",\n  \"hypothesis\": \"When an LLM verifies its own multi-step arithmetic word-problem solution using an explicit, mechanically-computed modular-arithmetic invariant (a 'casting-out-nines' digit-root checksum applied to each intermediate computation) instead of an open-ended 'double-check your work' self-critique prompt or a length-matched content-null placebo critique, the effect on error-detection and downstream correction accuracy is not a uniform benefit and is not simply monotonically diminishing with baseline capability -- it is capability-gated in a way that can invert sign entirely. On claude-haiku-4.5 (76.5% no-critique baseline, n=200), checksum critique raised accuracy to 97.5%, beating free-form critique by 17.0pp (McNemar p=1.08e-9) and the matched-length placebo by 6.5pp overall / 9.375pp on the checksum-detectable subset (bootstrap CI excludes zero), with the placebo response length if anything slightly exceeding the checksum condition's -- evidence the gain is attributable to the invariant's content, not extra deliberation tokens. On openai/gpt-4o-mini (95.5% baseline, near ceiling), all four conditions are statistically indistinguishable (largest gap 2.0pp, p=0.481), a flat null rather than a smaller positive effect. On meta-llama/llama-3.1-8b-instruct (84.5% baseline -- comparable headroom to claude-haiku-4.5's, which rules out 'headroom alone' as the operative variable), checksum critique collapses accuracy to 17.1% (McNemar p=1.2e-31 vs free-form), a catastrophic degradation traced qualitatively to the model fabricating extra computation steps absent from the original problem while performing the interleaved digit-root bookkeeping, evidenced by an 8x baseline response-length blowup and a strongly negative length-vs-accuracy-gain correlation (-0.40) unique to this model. This three-point pattern is treated as a pilot observation motivating, not establishing, a general capability-threshold or U-shaped functional form, and -- per reviewer critique -- the three models differ in vendor and instruction-tuning regime as well as capability, so the 'capability-conditioned' framing is explicitly a hypothesis to be tested with a same-family capability sweep, not a confirmed causal claim; llama-3.1-8b-instruct's collapse may partly reflect vendor-specific brittleness under long compound instructions rather than pure capability. The self-computed-checksum reliability bottleneck claim is revised: a deterministic, zero-LLM-call regex-based mod-9 checker (replacing the prior same-model LLM-judge design, which a follow-up Cohen's kappa of -0.12 against the same 70-trace sample shows performs at worse-than-chance agreement with ground truth) finds a 9.6% checksum-computation error rate overall, ordered by model capability (4.5% claude-haiku-4.5, 12.4% llama-3.1-8b-instruct, 14.6% gpt-4o-mini) -- notably not perfectly capability-ordered, since gpt-4o-mini has the highest checksum-computation error rate despite the highest task accuracy, indicating checksum-sub-task reliability and end-task accuracy are dissociable quantities. A major methodological gap remains unresolved across two review rounds: detection precision/recall has still only been measured via the proxy 'model's own baseline solve on the ORIGINAL uncorrelated problem differs from gold', not by running the four critique conditions directly on the already-built, verified 1,535-row error-injection dataset (art_UafZp2AqR5at) where ground truth is a known injected error the model is shown -- this remains the single highest-priority open test of the paper's central mechanistic claim (does the model actually catch an error it was shown corrupted, not merely disagree with itself) and is treated as unsupported until run.\",\n  \"relation_rationale\": \"Same checksum-critique frame; specialized into a three-way capability-gated (not monotonic) claim with vendor-confound caveat\",\n  \"confidence_delta\": \"unchanged\",\n  \"key_changes\": [\n    \"Replaced the two-model 'benefit vanishes near ceiling' framing with the three-model finding that the effect is non-monotonic: strong-model gain, mid-model null, weak-model catastrophic collapse (not diminishing benefit)\",\n    \"Added explicit reviewer-driven caveat that the three-model panel confounds vendor/instruction-tuning regime with capability level, so 'capability-conditioned' is a motivated hypothesis, not an established finding, pending a same-family sweep\",\n    \"Elevated the still-unresolved major reviewer critique (detection metrics rely on own-solve-wrong proxy, not the built error-injection dataset's known ground truth) as the paper's single largest open validity gap, now flagged across two consecutive review rounds\",\n    \"Replaced the same-model LLM-judge checksum-reliability estimate (~15%) with the deterministic checker's cross-validated 9.6% figure, and noted the judge's negative Cohen's kappa as direct evidence the same-model-judge design should be discarded, not merely caveated\",\n    \"Added the dissociation finding that checksum-computation reliability does not track end-task accuracy ordering (gpt-4o-mini highest error rate, highest accuracy)\",\n    \"Removed the now-unsupported 'headroom sets the ceiling' framing since llama-3.1-8b-instruct had comparable headroom to claude-haiku-4.5 yet the effect inverted in sign\"\n  ],\n  \"relation_type\": \"evolution\",\n  \"artifact_relations\": [\n    {\n      \"from_id\": \"art_UafZp2AqR5at\",\n      \"to_id\": \"art_0V-2bxn9h7_u\",\n      \"relation_type\": \"uses\",\n      \"relation_rationale\": \"Intended to test on the dataset's error-injection labels/RNG seed, but the target experiment never ran so it fell back to iter_1 data\"\n    }\n  ]\n}\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [6] ASSISTANT · 2026-07-31 21:13:07 UTC

```
Revised hypothesis written to `.terminal_claude_agent_struct_out.json`. Key updates: reframed the two-model finding as a three-way non-monotonic pattern (strong-model gain, mid-model null, weak-model catastrophic collapse), added the reviewer's vendor-confound caveat explicitly, elevated the still-unaddressed error-injection-dataset detection-metric gap as the top open validity issue, and folded in the deterministic-checker's revised 9.6% checksum-reliability figure with its dissociation-from-accuracy finding.
```

### [7] SYSTEM-USER prompt · 2026-07-31 21:13:08 UTC

```
<validation-feedback>
Attempt 1 failed validation.

Schema validation found 2 problems — fix ALL of them at once:
  - at `artifact_relations.0.relation_rationale`: "Intended to test on the dataset's error-injection labels/RNG seed, but the target experiment never ran so it fell back to iter_1 data" is too long (at most 120 characters, got 133)
  - at `relation_rationale`: 'Same checksum-critique frame; specialized into a three-way capability-gated (not monotonic) claim with vendor-confound caveat' is too long (at most 120 characters, got 125)
Every required field must be present and every field type must match the schema.

Produce `.terminal_claude_agent_struct_out.json` again so it contains corrected JSON that matches the schema. Do not invent new fields.
</validation-feedback>
```

### [8] TOOL CALL — Edit · 2026-07-31 21:13:12 UTC

```
File: /home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_0WmBa7GFLIzI/3_invention_loop/iter_2/upd_hypo/upd_hypo/.terminal_claude_agent_struct_out.json
OLD:   "relation_rationale": "Same checksum-critique frame; specialized into a three-way capability-gated (not monotonic) claim with vendor-confound caveat",
NEW:   "relation_rationale": "Same frame; specialized into a three-way capability-gated (non-monotonic) claim with vendor-confound caveat",
```

### [9] TOOL RESULT — Edit · 2026-07-31 21:13:12 UTC

```
{"filePath": "/home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_0WmBa7GFLIzI/3_invention_loop/iter_2/upd_hypo/upd_hypo/.terminal_claude_agent_struct_out.json", "oldString": "  \"relation_rationale\": \"Same checksum-critique frame; specialized into a three-way capability-gated (not monotonic) claim with vendor-confound caveat\",", "newString": "  \"relation_rationale\": \"Same frame; specialized into a three-way capability-gated (non-monotonic) claim with vendor-confound caveat\",", "originalFile": "{\n  \"title\": \"Checksum Critique: Capability-Gated, Not Universal\",\n  \"hypothesis\": \"When an LLM verifies its own multi-step arithmetic word-problem solution using an explicit, mechanically-computed modular-arithmetic invariant (a 'casting-out-nines' digit-root checksum applied to each intermediate computation) instead of an open-ended 'double-check your work' self-critique prompt or a length-matched content-null placebo critique, the effect on error-detection and downstream correction accuracy is not a uniform benefit and is not simply monotonically diminishing with baseline capability -- it is capability-gated in a way that can invert sign entirely. On claude-haiku-4.5 (76.5% no-critique baseline, n=200), checksum critique raised accuracy to 97.5%, beating free-form critique by 17.0pp (McNemar p=1.08e-9) and the matched-length placebo by 6.5pp overall / 9.375pp on the checksum-detectable subset (bootstrap CI excludes zero), with the placebo response length if anything slightly exceeding the checksum condition's -- evidence the gain is attributable to the invariant's content, not extra deliberation tokens. On openai/gpt-4o-mini (95.5% baseline, near ceiling), all four conditions are statistically indistinguishable (largest gap 2.0pp, p=0.481), a flat null rather than a smaller positive effect. On meta-llama/llama-3.1-8b-instruct (84.5% baseline -- comparable headroom to claude-haiku-4.5's, which rules out 'headroom alone' as the operative variable), checksum critique collapses accuracy to 17.1% (McNemar p=1.2e-31 vs free-form), a catastrophic degradation traced qualitatively to the model fabricating extra computation steps absent from the original problem while performing the interleaved digit-root bookkeeping, evidenced by an 8x baseline response-length blowup and a strongly negative length-vs-accuracy-gain correlation (-0.40) unique to this model. This three-point pattern is treated as a pilot observation motivating, not establishing, a general capability-threshold or U-shaped functional form, and -- per reviewer critique -- the three models differ in vendor and instruction-tuning regime as well as capability, so the 'capability-conditioned' framing is explicitly a hypothesis to be tested with a same-family capability sweep, not a confirmed causal claim; llama-3.1-8b-instruct's collapse may partly reflect vendor-specific brittleness under long compound instructions rather than pure capability. The self-computed-checksum reliability bottleneck claim is revised: a deterministic, zero-LLM-call regex-based mod-9 checker (replacing the prior same-model LLM-judge design, which a follow-up Cohen's kappa of -0.12 against the same 70-trace sample shows performs at worse-than-chance agreement with ground truth) finds a 9.6% checksum-computation error rate overall, ordered by model capability (4.5% claude-haiku-4.5, 12.4% llama-3.1-8b-instruct, 14.6% gpt-4o-mini) -- notably not perfectly capability-ordered, since gpt-4o-mini has the highest checksum-computation error rate despite the highest task accuracy, indicating checksum-sub-task reliability and end-task accuracy are dissociable quantities. A major methodological gap remains unresolved across two review rounds: detection precision/recall has still only been measured via the proxy 'model's own baseline solve on the ORIGINAL uncorrelated problem differs from gold', not by running the four critique conditions directly on the already-built, verified 1,535-row error-injection dataset (art_UafZp2AqR5at) where ground truth is a known injected error the model is shown -- this remains the single highest-priority open test of the paper's central mechanistic claim (does the model actually catch an error it was shown corrupted, not merely disagree with itself) and is treated as unsupported until run.\",\n  \"relation_rationale\": \"Same checksum-critique frame; specialized into a three-way capability-gated (not monotonic) claim with vendor-confound caveat\",\n  \"confidence_delta\": \"unchanged\",\n  \"key_changes\": [\n    \"Replaced the two-model 'benefit vanishes near ceiling' framing with the three-model finding that the effect is non-monotonic: strong-model gain, mid-model null, weak-model catastrophic collapse (not diminishing benefit)\",\n    \"Added explicit reviewer-driven caveat that the three-model panel confounds vendor/instruction-tuning regime with capability level, so 'capability-conditioned' is a motivated hypothesis, not an established finding, pending a same-family sweep\",\n    \"Elevated the still-unresolved major reviewer critique (detection metrics rely on own-solve-wrong proxy, not the built error-injection dataset's known ground truth) as the paper's single largest open validity gap, now flagged across two consecutive review rounds\",\n    \"Replaced the same-model LLM-judge checksum-reliability estimate (~15%) with the deterministic checker's cross-validated 9.6% figure, and noted the judge's negative Cohen's kappa as direct evidence the same-model-judge design should be discarded, not merely caveated\",\n    \"Added the dissociation finding that checksum-computation reliability does not track end-task accuracy ordering (gpt-4o-mini highest error rate, highest accuracy)\",\n    \"Removed the now-unsupported 'headroom sets the ceiling' framing since llama-3.1-8b-instruct had comparable headroom to claude-haiku-4.5 yet the effect inverted in sign\"\n  ],\n  \"relation_type\": \"evolution\",\n  \"artifact_relations\": [\n    {\n      \"from_id\": \"art_UafZp2AqR5at\",\n      \"to_id\": \"art_0V-2bxn9h7_u\",\n      \"relation_type\": \"uses\",\n      \"relation_rationale\": \"Intended to test on the dataset's error-injection labels/RNG seed, but the target experiment never ran so it fell back to iter_1 data\"\n    }\n  ]\n}\n", "structuredPatch": [{"oldStart": 1, "oldLines": 7, "newStart": 1, "newLines": 7, "lines": [" {", "   \"title\": \"Checksum Critique: Capability-Gated, Not Universal\",", "   \"hypothesis\": \"When an LLM verifies its own multi-step arithmetic word-problem solution using an explicit, mechanically-computed modular-arithmetic invariant (a 'casting-out-nines' digit-root checksum applied to each intermediate computation) instead of an open-ended 'double-check your work' self-critique prompt or a length-matched content-null placebo critique, the effect on error-detection and downstream correction accuracy is not a uniform benefit and is not simply monotonically diminishing with baseline capability -- it is capability-gated in a way that can invert sign entirely. On claude-haiku-4.5 (76.5% no-critique baseline, n=200), checksum critique raised accuracy to 97.5%, beating free-form critique by 17.0pp (McNemar p=1.08e-9) and the matched-length placebo by 6.5pp overall / 9.375pp on the checksum-detectable subset (bootstrap CI excludes zero), with the placebo response length if anything slightly exceeding the checksum condition's -- evidence the gain is attributable to the invariant's content, not extra deliberation tokens. On openai/gpt-4o-mini (95.5% baseline, near ceiling), all four conditions are statistically indistinguishable (largest gap 2.0pp, p=0.481), a flat null rather than a smaller positive effect. On meta-llama/llama-3.1-8b-instruct (84.5% baseline -- comparable headroom to claude-haiku-4.5's, which rules out 'headroom alone' as the operative variable), checksum critique collapses accuracy to 17.1% (McNemar p=1.2e-31 vs free-form), a catastrophic degradation traced qualitatively to the model fabricating extra computation steps absent from the original problem while performing the interleaved digit-root bookkeeping, evidenced by an 8x baseline response-length blowup and a strongly negative length-vs-accuracy-gain correlation (-0.40) unique to this model. This three-point pattern is treated as a pilot observation motivating, not establishing, a general capability-threshold or U-shaped functional form, and -- per reviewer critique -- the three models differ in vendor and instruction-tuning regime as well as capability, so the 'capability-conditioned' framing is explicitly a hypothesis to be tested with a same-family capability sweep, not a confirmed causal claim; llama-3.1-8b-instruct's collapse may partly reflect vendor-specific brittleness under long compound instructions rather than pure capability. The self-computed-checksum reliability bottleneck claim is revised: a deterministic, zero-LLM-call regex-based mod-9 checker (replacing the prior same-model LLM-judge design, which a follow-up Cohen's kappa of -0.12 against the same 70-trace sample shows performs at worse-than-chance agreement with ground truth) finds a 9.6% checksum-computation error rate overall, ordered by model capability (4.5% claude-haiku-4.5, 12.4% llama-3.1-8b-instruct, 14.6% gpt-4o-mini) -- notably not perfectly capability-ordered, since gpt-4o-mini has the highest checksum-computation error rate despite the highest task accuracy, indicating checksum-sub-task reliability and end-task accuracy are dissociable quantities. A major methodological gap remains unresolved across two review rounds: detection precision/recall has still only been measured via the proxy 'model's own baseline solve on the ORIGINAL uncorrelated problem differs from gold', not by running the four critique conditions directly on the already-built, verified 1,535-row error-injection dataset (art_UafZp2AqR5at) where ground truth is a known injected error the model is shown -- this remains the single highest-priority open test of the paper's central mechanistic claim (does the model actually catch an error it was shown corrupted, not merely disagree with itself) and is treated as unsupported until run.\",", "-  \"relation_rationale\": \"Same checksum-critique frame; specialized into a three-way capability-gated (not monotonic) claim with vendor-confound caveat\",", "+  \"relation_rationale\": \"Same frame; specialized into a three-way capability-gated (non-monotonic) claim with vendor-confound caveat\",", "   \"confidence_delta\": \"unchanged\",", "   \"key_changes\": [", "     \"Replaced the two-model 'benefit vanishes near ceiling' framing with the three-model finding that the effect is non-monotonic: strong-model gain, mid-model null, weak-model catastrophic collapse (not diminishing benefit)\","]}], "userModified": false, "replaceAll": false}
```

### [10] TOOL CALL — Edit · 2026-07-31 21:13:19 UTC

```
File: /home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_0WmBa7GFLIzI/3_invention_loop/iter_2/upd_hypo/upd_hypo/.terminal_claude_agent_struct_out.json
OLD:       "relation_rationale": "Intended to test on the dataset's error-injection labels/RNG seed, but the target experiment never ran so it fell back to iter_1 data"
NEW:       "relation_rationale": "Meant to test the injected-error labels/RNG seed, but that experiment never ran, so it reused iter_1 data instead"
```

### [11] TOOL RESULT — Edit · 2026-07-31 21:13:19 UTC

```
{"filePath": "/home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_0WmBa7GFLIzI/3_invention_loop/iter_2/upd_hypo/upd_hypo/.terminal_claude_agent_struct_out.json", "oldString": "      \"relation_rationale\": \"Intended to test on the dataset's error-injection labels/RNG seed, but the target experiment never ran so it fell back to iter_1 data\"", "newString": "      \"relation_rationale\": \"Meant to test the injected-error labels/RNG seed, but that experiment never ran, so it reused iter_1 data instead\"", "originalFile": "{\n  \"title\": \"Checksum Critique: Capability-Gated, Not Universal\",\n  \"hypothesis\": \"When an LLM verifies its own multi-step arithmetic word-problem solution using an explicit, mechanically-computed modular-arithmetic invariant (a 'casting-out-nines' digit-root checksum applied to each intermediate computation) instead of an open-ended 'double-check your work' self-critique prompt or a length-matched content-null placebo critique, the effect on error-detection and downstream correction accuracy is not a uniform benefit and is not simply monotonically diminishing with baseline capability -- it is capability-gated in a way that can invert sign entirely. On claude-haiku-4.5 (76.5% no-critique baseline, n=200), checksum critique raised accuracy to 97.5%, beating free-form critique by 17.0pp (McNemar p=1.08e-9) and the matched-length placebo by 6.5pp overall / 9.375pp on the checksum-detectable subset (bootstrap CI excludes zero), with the placebo response length if anything slightly exceeding the checksum condition's -- evidence the gain is attributable to the invariant's content, not extra deliberation tokens. On openai/gpt-4o-mini (95.5% baseline, near ceiling), all four conditions are statistically indistinguishable (largest gap 2.0pp, p=0.481), a flat null rather than a smaller positive effect. On meta-llama/llama-3.1-8b-instruct (84.5% baseline -- comparable headroom to claude-haiku-4.5's, which rules out 'headroom alone' as the operative variable), checksum critique collapses accuracy to 17.1% (McNemar p=1.2e-31 vs free-form), a catastrophic degradation traced qualitatively to the model fabricating extra computation steps absent from the original problem while performing the interleaved digit-root bookkeeping, evidenced by an 8x baseline response-length blowup and a strongly negative length-vs-accuracy-gain correlation (-0.40) unique to this model. This three-point pattern is treated as a pilot observation motivating, not establishing, a general capability-threshold or U-shaped functional form, and -- per reviewer critique -- the three models differ in vendor and instruction-tuning regime as well as capability, so the 'capability-conditioned' framing is explicitly a hypothesis to be tested with a same-family capability sweep, not a confirmed causal claim; llama-3.1-8b-instruct's collapse may partly reflect vendor-specific brittleness under long compound instructions rather than pure capability. The self-computed-checksum reliability bottleneck claim is revised: a deterministic, zero-LLM-call regex-based mod-9 checker (replacing the prior same-model LLM-judge design, which a follow-up Cohen's kappa of -0.12 against the same 70-trace sample shows performs at worse-than-chance agreement with ground truth) finds a 9.6% checksum-computation error rate overall, ordered by model capability (4.5% claude-haiku-4.5, 12.4% llama-3.1-8b-instruct, 14.6% gpt-4o-mini) -- notably not perfectly capability-ordered, since gpt-4o-mini has the highest checksum-computation error rate despite the highest task accuracy, indicating checksum-sub-task reliability and end-task accuracy are dissociable quantities. A major methodological gap remains unresolved across two review rounds: detection precision/recall has still only been measured via the proxy 'model's own baseline solve on the ORIGINAL uncorrelated problem differs from gold', not by running the four critique conditions directly on the already-built, verified 1,535-row error-injection dataset (art_UafZp2AqR5at) where ground truth is a known injected error the model is shown -- this remains the single highest-priority open test of the paper's central mechanistic claim (does the model actually catch an error it was shown corrupted, not merely disagree with itself) and is treated as unsupported until run.\",\n  \"relation_rationale\": \"Same frame; specialized into a three-way capability-gated (non-monotonic) claim with vendor-confound caveat\",\n  \"confidence_delta\": \"unchanged\",\n  \"key_changes\": [\n    \"Replaced the two-model 'benefit vanishes near ceiling' framing with the three-model finding that the effect is non-monotonic: strong-model gain, mid-model null, weak-model catastrophic collapse (not diminishing benefit)\",\n    \"Added explicit reviewer-driven caveat that the three-model panel confounds vendor/instruction-tuning regime with capability level, so 'capability-conditioned' is a motivated hypothesis, not an established finding, pending a same-family sweep\",\n    \"Elevated the still-unresolved major reviewer critique (detection metrics rely on own-solve-wrong proxy, not the built error-injection dataset's known ground truth) as the paper's single largest open validity gap, now flagged across two consecutive review rounds\",\n    \"Replaced the same-model LLM-judge checksum-reliability estimate (~15%) with the deterministic checker's cross-validated 9.6% figure, and noted the judge's negative Cohen's kappa as direct evidence the same-model-judge design should be discarded, not merely caveated\",\n    \"Added the dissociation finding that checksum-computation reliability does not track end-task accuracy ordering (gpt-4o-mini highest error rate, highest accuracy)\",\n    \"Removed the now-unsupported 'headroom sets the ceiling' framing since llama-3.1-8b-instruct had comparable headroom to claude-haiku-4.5 yet the effect inverted in sign\"\n  ],\n  \"relation_type\": \"evolution\",\n  \"artifact_relations\": [\n    {\n      \"from_id\": \"art_UafZp2AqR5at\",\n      \"to_id\": \"art_0V-2bxn9h7_u\",\n      \"relation_type\": \"uses\",\n      \"relation_rationale\": \"Intended to test on the dataset's error-injection labels/RNG seed, but the target experiment never ran so it fell back to iter_1 data\"\n    }\n  ]\n}\n", "structuredPatch": [{"oldStart": 17, "oldLines": 7, "newStart": 17, "newLines": 7, "lines": ["       \"from_id\": \"art_UafZp2AqR5at\",", "       \"to_id\": \"art_0V-2bxn9h7_u\",", "       \"relation_type\": \"uses\",", "-      \"relation_rationale\": \"Intended to test on the dataset's error-injection labels/RNG seed, but the target experiment never ran so it fell back to iter_1 data\"", "+      \"relation_rationale\": \"Meant to test the injected-error labels/RNG seed, but that experiment never ran, so it reused iter_1 data instead\"", "     }", "   ]", " }"]}], "userModified": false, "replaceAll": false}
```

### [12] ASSISTANT · 2026-07-31 21:13:19 UTC

```
Both overlong `relation_rationale` fields are fixed and within the 120-char limit.
```
