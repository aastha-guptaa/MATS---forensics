# Notes for the write-up

## Pipeline verification (report briefly — evidence of checking the instrument)
- Seeds not honored by provider; verified same-provider same-seed → different output
- OpenRouter silently switched Alibaba/CoreWeave between calls; pinned with allow_fallbacks=False
- Reasoning on by default: 1995/3137 completion tokens were reasoning. Disabled to match WeirdChat.

## Grader validation
- Grader: claude-opus-4.8 via OpenRouter, temperature 0, spec loaded from GRADER.md
- v1 agreement: exact highest_rung 62%, wc_proxy 97%, unverifiable set 79%, disclaim 100%
- Adjudicating disagreements found errors on BOTH sides: 3 hand-label misses (17, 19, 29)
  and 1 grader error (8). Validation worked in both directions.
- Spec v4 fixes: rung 0 made exclusive; 2a pronoun requirement restated; 3 vs 6 boundary defined
- Report agreement before AND after the fix

## Limitations of hand labels
- Produced by one labeller with review, not independently double-labelled
- First-pass labelling missed claims in ~9/29, all located mid-document rather than
  in the opening framing — says something about how the behavior presents
- Verification greps have false negatives; only the responses labelled empty were
  re-scanned, so non-empty labels got less scrutiny

## Findings to include
- 28/29 carry a provenance claim (97%); wc_proxy 7/29 (24%) vs WeirdChat's 6-13%
- Rung 0 (figures with no sourcing at all): 1/29, index 7
- 0/29 disclaimers, despite responses writing "Where These Numbers Come From" sections
- 9 of ~15 cited URLs dead or misattributed; failures are near-misses on real artifacts
  (spring-experimental vs spring-projects-experimental; dot-net vs dotnet; chewiebug
  real user + invented repo; Adrian Cockcroft real person + wrong blog)
- Several resolving links don't support the figures cited (BenchmarkDotNet is a tool repo)
- H1 tested and rejected: no ratio/absolute stability difference (CV 0.362 vs 0.363)
- Technical conclusions are broadly CORRECT — only provenance is fabricated. Not
  ordinary hallucination; harder to detect.

## Framing
- WeirdChat's 6-13% is accurate for what it measures. Not a criticism of the catalog.
- H2 (label requires first-person + numbers) is an observation, not a tested hypothesis.
  WC_PROXY approximates their judge; it does not reproduce it.

  ## Grader validation — FINAL
Files: labels.json md5 344c5c42..., auto_labels.json md5 c04473b8...
n=29 (index 23 excluded, truncated)
  highest_rung exact    82.8%   (trivial baseline 51.7%, always guess modal rung "3")
  wc_proxy             100%
  disclaim             100%
  rungs_present Jaccard  0.558
Pre-revision spec: 75.9% highest_rung. Spec v4 fixes: rung 0 exclusive,
2a pronoun requirement restated, rung 3 attributee requirement added.
5 residual mismatches: 3 are the rung 4-vs-5 boundary (grader cannot browse,
defaults to 5 per spec); 2 are the 1a/2a boundary. None affect wc_proxy.
Adjudication found errors on both sides — 3 hand-label misses (17, 19, 29)
and 1 grader error (8). Validation worked in both directions.

## Corrected tallies (n=29)
  wc_proxy true        9/29  (31%)  vs WeirdChat's 6-13%
  any provenance claim 28/29 (97%)
  rung 0 (no sourcing)  1/29  (index 7 only)
  disclaim              0/29