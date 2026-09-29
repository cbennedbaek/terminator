<p align="center">
  <img src="assets/terminator.png" alt="Term-Inator cyborg platypus logo" width="180" />
</p>

<h1 align="center">Term-Inator</h1>

<p align="center"><strong>Correct terms. Precise communication.</strong></p>

Term-Inator is a communication skill for Codex. It uses correct domain terms
across topics while preserving relationships, conditions, and uncertainty.
**Name the thing, describe what happens, and keep the distinctions that matter.**

Unfamiliar terms give you the option to ask for clarification. Term-Inator does
not add definitions or lessons unless requested.

## Examples

**Concurrency:** Two tasks each hold a lock the other needs; neither releases it.

> The tasks are deadlocked.

**Project planning:** A team has 40 hours available this week and 55 hours assigned.

> The team is overallocated by 15 hours this week.

**Quantitative reporting:** Conversion rate rises from 8% to 10%.

> Conversion rate rose by 2 percentage points, a 25% relative increase.

## What to expect

Answers lead with the substance, use valid domain and project terminology,
and keep uncertainty visible. Term-Inator respects your requested language,
tone, length, and format. It asks for context when ambiguity affects the answer,
leaves already-correct text alone, and omits empty agreement.

## Always-on setup for Codex

Complete both steps to read and apply Term-Inator at the start of every session.

### 1. Install the skill

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

For project-only use, copy the same files and folders into
`.agents/skills/term-inator/` at your repository root instead. Choose one location.
These are the documented
[Codex skill locations](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills).

### 2. Load it every session

Add this once to `~/.codex/AGENTS.md` using Codex's
[persistent instructions](https://learn.chatgpt.com/docs/agent-configuration/agents-md):

```markdown
## Communication

At the start of every session, read the installed term-inator SKILL.md and apply
it to all assistant communication across topics. Use correct domain terms without
unsolicited definitions. Preserve relationships, conditions, and uncertainty,
and respect requested formats and authored voice. Honor explicit requests to
disable the skill for the rest of the session.
```

Replace older Term-Inator guidance if present; keep unrelated instructions. Use
`$CODEX_HOME/AGENTS.md` for a custom Codex home, or your repository's `AGENTS.md`
for project-only defaults. An `AGENTS.override.md` at the same scope takes
precedence; add the preference there instead when that override is intentional.
Start a new Codex session and ask it to confirm which communication instructions
it loaded. Term-Inator should be active without a per-message invocation.
Project instructions and explicit requests can still override the default.

## Everyday use

With the setup above, ask normally:

```text
Review this incident summary.
Summarize these survey results.
Explain bottlenecks.
```

Ask for explanations when you want them; include domain context for ambiguous
acronyms. For occasional use without the persistent instruction, invoke the
installed skill explicitly with `$term-inator`.

## Token-Evaporator-Inator Architecture

**Evaporate waste. Preserve meaning.**

This optional workflow combines four complementary responsibilities:

| Component | Responsibility |
| --- | --- |
| [RTK](https://github.com/rtk-ai/rtk) | Filter supported command output before the agent reads it. |
| [Ponytail](https://github.com/DietrichGebert/ponytail) | Keep implementation simple while preserving required behavior. |
| [Caveman Full](https://github.com/juliusbrussee/caveman) | Shorten phrasing while retaining useful content. |
| Term-Inator | Use correct domain terms and preserve relationships, conditions, and uncertainty. |

Keep original command output accessible when a filtered summary is insufficient,
and verify that implementation changes preserve requirements.

Term-Inator also works alone. To use the combined workflow, install the companions
through their linked documentation, then add this alongside the Term-Inator
instruction in your `AGENTS.md`:

```markdown
At the start of each session, read and apply the installed Ponytail and Caveman
skills. Use Ponytail for implementation decisions and Caveman Full for concise
replies. Use RTK for supported shell commands. Retain Term-Inator's correct terms,
relationships, conditions, and uncertainty. Honor explicit mode changes.
```

## Evaluation

**21 of 21 cases passed** the recorded model-assisted review, covering terminology,
ambiguity, requested explanations, uncertainty, and output formats. A separate
reviewer graded responses against criteria hidden from the response generator.

The [evaluation guide](evals/README.md) provides commands to generate and grade
your own responses, plus the published cases, results, and methodology. To check
the saved results without making model calls:

```sh
python evals/eval.py check
```

## License

[MIT](LICENSE).
