# Response-relevance comparison

This comparison informed the wording adopted in Term-Inator 1.3.2. It compares
v1.3.1 with a candidate that changes one bullet about non-actions and unchanged
properties.

| Measure | v1.3.1 | Candidate |
| --- | --- | --- |
| Overall | 66/72 | 69/72 |
| Omit irrelevant details | 30/36 | 33/36 |
| Preserve material information | 36/36 | 36/36 |

The candidate gained one passing reply in each of three runs. Gains were
concentrated in two of 24 cases: scheduling recommendations (V13) and a practice
failover checklist handoff (V22). The remaining 22 cases tied. There were three
candidate-only passes, no baseline-only passes, 66 shared passes, and three
shared failures. The candidate still reported irrelevant unrun integration
tests and an unperformed live failover in some replies.

## Files

- `cases.json`: 24 prompts and acceptance criteria across six domains.
- `results.json`: all 144 replies, per-criterion grades, summaries, and provenance.
- `v1.3.1-SKILL.md`: exact baseline instructions supplied to generators.
- `candidate-SKILL.md`: exact candidate instructions supplied to generators.

The candidate input retains its original `1.3.1` metadata. The adopted v1.3.2
instruction body is identical; only release-version metadata changed afterward.
Input hashes identify the evaluated files rather than relabeling the experiment
as a run against the later release file.

In `results.json`, `alpha` is v1.3.1 and `beta` is the candidate. Sample IDs were
shuffled before grading; reviewers did not receive this mapping. The independent
case designer did not see either instruction variant. A pre-run rubric audit
made incidental reporting optional and included realistic validation disclaimers.
Cases and criteria were frozen before generation.

## Method and interpretation

Each variant used three fresh native executor agent contexts, with 24 cases in
each batch. The prompt order was shuffled identically for both variants within
each run. Three separate native critic agents each graded one matched run's
48 replies without version labels, skills, or earlier judgments.

This is a modest observed gain on synthetic reporting tasks. The study used six
generator contexts, not 144 independent trials; replies within each batch share
context. Backend routing and sampling settings were not captured. It does not
establish execution accuracy or effectiveness across models and hosts.

The main 37-case release regression suite is separate. Its results are recorded
in `../../results.json`; these comparison replies have not been substituted for
fresh release-regression results.
