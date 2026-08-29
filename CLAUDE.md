# Project
Model forensics: investigating why [model] exhibits [behavior].
Model: Qwen3.6-9B via nnsight. GPU pod, persistent ipython in tmux.

## Kernel discipline
- Load model/data in dedicated top-level cells. NEVER restart the kernel without asking.
- Save all plots to figures/ as PNG in addition to displaying.
- Long jobs: background scripts with logs, not kernel cells.

## Research discipline — important
- You execute experiments. I design them. Do not propose a new
  experimental direction without asking; do flag if an experiment
  doesn't test the stated hypothesis.
- Every result goes to experiments/eNN/results.json as raw numbers.
  Never report a summary statistic without writing the raw data.
- When an experiment "works", say so as a hypothesis, not a finding.
  List the two most likely ways it could be an artifact.
- Never fabricate or interpolate a number. If a run failed, say it failed.
- Always include the trivial baseline (random vector / random choice /
  just ask the model) in any comparison.