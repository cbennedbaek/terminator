# Term-Inator evaluations

These 21 cases check terminology, contextual ambiguity, requested explanations,
factual fidelity, uncertainty, and output constraints. Topics include software,
business, cooking, and literary analysis. Some cases require already-correct
text to remain unchanged.

- `cases.json` contains prompts, acceptance criteria, and scoring guidance.
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

Generation makes 21 model calls; grading makes another 21. Your normal model
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

## Check without model calls

```sh
python evals/eval.py check
python -m unittest discover -s evals
```

The first command checks the published results. The second tests the runner with
synthetic responses, including malformed JSON, changed instructions, failed
commands, and incomplete reviews. Neither generates new model evidence.

## Recorded run

All 21 cases passed the recorded review.

The response generator received the skill and prompts without grading criteria
or earlier results. A separate reviewer received prompts, criteria, and responses,
without the skill or earlier outcomes. Cases shared a batch context; they were
not independent trials. Model and reasoning settings were inherited from the
harness; the exact backend model identifier and sampling settings were not captured.
Shared host instructions and available skill metadata may have influenced responses.

These are behavioral smoke tests with model-assisted grading. They do not test
automatic activation, long conversations, multilingual use, or cross-model
consistency. There is no no-skill control, so the results cannot establish the
skill's causal effect on quality, productivity, or token use.
