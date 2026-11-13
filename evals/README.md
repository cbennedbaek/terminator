# Term-Inator evaluations

These 37 cases check terminology, contextual ambiguity, requested explanations,
factual fidelity, uncertainty, handoffs, deferred decisions, and output constraints.
They also check whether recommendations change with evidence rather than pressure.
Topics include software, business, cooking, and literary analysis. Some cases
require already-correct text to remain unchanged.
The final four cases check irrelevant non-actions, blocked deployment, requested
negative findings, and disclosure of accidental data loss.

- `cases.json` contains prompts, acceptance criteria, and scoring guidance.
  The suite name `term-inator-1.3.0` identifies the shared cases; versions 1.3.0,
  1.3.1, and 1.3.2 use the same suite for comparison.
- `results.json` contains actual responses and independent model-assisted judgments.
  Hashes identify the tested skill and cases, with CRLF normalized to LF.
- `eval.py` generates responses, collects separate reviewer judgments, and checks
  saved results. `test_eval.py` tests the runner offline.

## Run the cases

Requires Python 3.9+ and an authenticated model CLI. No Python packages required.
From the repository root, these commands work with the
[Codex CLI](https://learn.chatgpt.com/docs/non-interactive-mode):

```sh
python evals/eval.py run --output evals/local-responses.json --settings "Codex configured model and reasoning; existing user instructions" -- codex exec --ephemeral --skip-git-repo-check --sandbox read-only -
python evals/eval.py grade --input evals/local-responses.json --output evals/local-results.json --settings "Codex configured reviewer and reasoning; existing user instructions" -- codex exec --ephemeral --skip-git-repo-check --sandbox read-only -
python evals/eval.py check --input evals/local-results.json
```

Generation makes 37 model calls; grading makes another 37. Your normal model
usage applies. For reproducible comparisons, select a model and reasoning
settings in the CLI arguments and replace `--settings` with their actual values.
That label records settings; it does not configure the model.

Each call uses a fresh process and temporary working directory. Generation gets
the skill and one prompt, without criteria. Grading gets one response, its prompt,
criteria, and scoring guidance, without the skill or previous judgments. The
runner supplies a request to avoid tools. Host instructions and configured tools
can still affect behavior; temporary directories do not isolate your user profile.

You can replace the command after `--` with any CLI that reads a UTF-8 prompt
from stdin and returns only its final answer on stdout. It must start a fresh
conversation, without resuming history. Diagnostics belong on stderr. Use an
executable on PATH and absolute paths for any wrapper files: calls run outside
the repository. Shell aliases are not resolved. On Windows, use `codex.exe` when
available; for an npm command shim, use `cmd /d /c codex.cmd exec ...` after `--`.
Trailing transport newlines are removed from responses; other
whitespace is preserved. Grader output must be a JSON object containing a boolean
`pass` and a nonempty `reason`.

Output files are never overwritten. Completed cases are saved as the run proceeds;
a failed command stops the run and leaves partial evidence. Rerun to a new filename
after resolving the failure. `local*.json` files are ignored by Git. No timestamps,
command arguments, working directories, or diagnostic logs are written into results.
Keep settings labels free of private information; inspect responses before publishing.

The final check requires complete coverage, matching skill and case hashes, valid
review judgments, exact-text controls, selected word limits, and the required JSON
structure. It exits nonzero for failures or missing reviews. Semantic correctness
still depends on the reviewer; a recorded pass is not independently proven by Python.

## Compare instruction files

Add `--skill previous-SKILL.md` to all three commands to evaluate another version
against the same cases. The file can also contain a short communication preference
or be empty for a control with no supplied skill. Use separate output filenames
for each run. Grading and checking require the same instruction file used for
generation; its content hash is recorded, but its path is not.

Keep the model, reasoning settings, host instructions, and case set fixed across
runs. An empty file removes only the supplied skill; disable any always-on
Term-Inator preference separately when testing without it. Review individual
answers as well as pass counts, and repeat trials before drawing conclusions.

## Check without model calls

```sh
python evals/eval.py check
python -m unittest discover -s evals
```

The first command checks the published results. The second tests the runner with
synthetic responses, including malformed JSON, changed instructions, failed
commands, and incomplete reviews. Neither generates new model evidence.

## Recorded run

All 37 cases passed the recorded review.

All responses were freshly generated for v1.3.2 using the unchanged 37-case
suite. A separate reviewer graded them against the acceptance criteria. The
earlier v1.3.0 and v1.3.1 release tags preserve their own responses and judgments.

The response generator received the skill and prompts without grading criteria
or earlier results. A separate reviewer received prompts, criteria, and responses,
without the skill, version label, or earlier judgments.

Generation and review used batch contexts, unlike the per-case CLI workflow
above. Model and reasoning settings were inherited from the harness; the exact
backend model identifier and sampling settings were not captured. Shared host
instructions and available skill metadata may have influenced responses.

These behavioral smoke tests check adherence in the supplied cases. They do not
measure productivity or token savings, or establish behavior across models,
languages, or long conversations. Automatic activation is not tested.

## Varied response-relevance comparison

The [comparison archive](comparisons/response-relevance/README.md) contains a
separate 24-case study across six domains and three batch runs per variant.
v1.3.1 passed 66/72 replies; the candidate adopted in v1.3.2 passed 69/72.
Both passed all 36 material-information replies. Gains were concentrated in
two cases; three irrelevant-detail failures remained for the candidate.

This study used six generator batch contexts, not 144 independent trials.
Its exact inputs, criteria, responses, and per-criterion grades are preserved.
The candidate file retains the metadata used during that experiment; the archive
explains its relationship to the later v1.3.2 release. The main regression
checker above validates the separate 37-case release record, not this archive.
