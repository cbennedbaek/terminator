<p align="center">
  <img src="assets/terminator.png" alt="Term-Inator cyborg platypus logo" width="180" />
</p>

<h1 align="center">Term-Inator</h1>

<p align="center"><strong>Precise technical language for Codex.</strong></p>

Term-Inator makes software explanations specific: **name the thing, describe
what happens, and keep the context that makes it understandable.**

## Before / after

**Before**

> I'll clean up the email logic in `OrderService`.

**After**

> I'll inject `IEmailSender` into `OrderService` through its constructor, so
> unit tests can use a fake sender without sending real confirmation emails.

**Before**

> I'll improve the error handling.

**After**

> I'll map a `null` result from `GetOrderAsync` to `404 Not Found` in the order
> endpoint, instead of returning `200 OK` with a null body.

These illustrate chosen changes, not patterns to apply automatically. The same
approach applies to UI work, reviews, refactoring, and debugging.

## What it avoids

No invented details, jargon for its own sake, automatic acronym expansion,
unnecessary abstractions, or tool-by-tool narration. KISS, DRY, SOLID, and DDD
support an explanation when relevant; they do not replace it. Code-only stays
code-only. Already precise text stays short.

Replies start with the answer, finding, correction, or action, not "You're
right," "Good catch," or the same filler reworded. Mistakes are acknowledged
specifically and corrected; factual confirmation and evidence-based disagreement
remain intact.

## Install for Codex

From the repository root (the folder containing `SKILL.md`), choose your shell.
These commands install the skill for your user. They stop if that destination
already exists; compare an existing installation before updating it.

PowerShell:

```powershell
$skillDestination = Join-Path $HOME '.agents/skills/term-inator'
if (Test-Path -LiteralPath $skillDestination) { throw "Already exists: $skillDestination" }
New-Item -ItemType Directory -Path $skillDestination -Force -ErrorAction Stop | Out-Null
Copy-Item -LiteralPath 'SKILL.md', 'LICENSE', 'agents', 'assets' -Destination $skillDestination -Recurse -ErrorAction Stop
```

Bash (macOS, Linux, or the environment where you run Codex; WSL uses a separate
home from native Windows):

```bash
(
  set -eu
  skill_destination="$HOME/.agents/skills/term-inator"
  if [ -e "$skill_destination" ] || [ -L "$skill_destination" ]; then
    printf 'Already exists: %s\n' "$skill_destination" >&2
    exit 1
  fi
  mkdir -p "$skill_destination"
  cp -R SKILL.md LICENSE agents assets "$skill_destination/"
)
```

For project-only use, copy those same files and folders into
`.agents/skills/term-inator/` at your repository root instead. Choose one
location to avoid duplicate entries. These are the documented
[Codex skill locations](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills).
The installed folder is named `term-inator`, even though the repository is
named `terminator`. Codex detects skill changes automatically; restart it if
the skill does not appear.

## Make it the default

The bundled `agents/openai.yaml` permits
[automatic skill selection](https://learn.chatgpt.com/docs/build-skills#optional-metadata);
it does not force the skill to load on every turn.

Add this once to `~/.codex/AGENTS.md` using Codex's
[persistent instructions](https://learn.chatgpt.com/docs/agent-configuration/agents-md):

```markdown
## Communication

Use the installed term-inator skill by default for software explanations.
```

Append to the existing file; do not replace other instructions. Use
`$CODEX_HOME/AGENTS.md` for a custom Codex home, or your repository's `AGENTS.md`
for project-only defaults. An `AGENTS.override.md` at the same scope takes
precedence; add the preference there instead when that override is intentional.
Start a new Codex session. Project instructions and explicit requests can still
override the default. No repeated session prompt is needed for this setup.

For an individual task, explicit invocation also works:

```text
$term-inator Review this refactor.
```

## With Ponytail and Caveman

Use [Ponytail](https://github.com/DietrichGebert/ponytail) for implementation
simplicity and Term-Inator for precise explanations. With
[Caveman](https://github.com/juliusbrussee/caveman), trim filler without dropping
names, material context, or uncertainty. Explicit preferences for terse wording
still apply; Term-Inator does not require full sentences or extra explanation.
Neither companion is required.

## License

[MIT](LICENSE).
