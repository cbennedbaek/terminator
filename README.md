<p align="center">
  <img src="assets/terminator.png" alt="Term-Inator cyborg platypus logo" width="180" />
</p>

<h1 align="center">Term-Inator</h1>

<p align="center">A communication skill for AI assistants</p>

Term-Inator helps AI assistants use the right terms for the subject you're
working on and keep the context that makes an answer useful. The idea is simple: name the
concept, describe what's happening, and make the important details clear.

We all know some subjects better than others. Using the correct term gives you
something to recognize, look up, or ask about. You choose when you'd like an
explanation; Term-Inator keeps those on request.

## Examples

**Concurrency:** Two tasks each hold a lock the other needs; neither releases it.

> The tasks are deadlocked.

**Project planning:** A team has 40 hours available this week and 55 hours assigned.

> The team is overallocated by 15 hours this week.

**Quantitative reporting:** Conversion rate rises from 8% to 10%.

> Conversion rate rose by 2 percentage points, a 25% relative increase.

**Deferred work:** Payment is captured before an order is created. If order
creation fails, the customer may be charged without an order. The team has
deferred choosing how to recover.

> Deferred: decide how to recover if order creation fails after payment is
> captured, leaving the customer charged without an order.

## What to expect

The goal is to make answers easier to work with. They use the vocabulary of your
subject or project, say what's known, and keep relevant uncertainty clear.
Your requested language, tone, length, and format still guide the response.
Answers omit redundant disclaimers and repetition while retaining details needed
to understand the outcome.

In a summary, that means keeping the findings and open decisions someone needs
to continue the work. In a recommendation, it means explaining what the evidence
supports and reconsidering when new information arrives. When a term could mean
different things, a focused question helps establish the right context.

## Always-on setup

Codex is the primary setup documented here. The communication instructions can
also be used with other models and compatible agent hosts; loading and activation
depend on the host.

These two steps make Term-Inator part of your usual Codex setup, so you can
ask questions normally in each new session.

### 1. Install the skill

From the repository root (the folder containing `SKILL.md`), choose your shell.
These commands install the skill for your user. If you already have it installed,
compare the existing files before updating; the commands preserve that installation.

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

At session startup, read the installed term-inator SKILL.md and apply it across
assistant replies. Respect requested formats, authored voice, and explicit
requests to disable it for the session.
```

Replace older Term-Inator guidance if present; keep unrelated instructions. Use
`$CODEX_HOME/AGENTS.md` for a custom Codex home, or your repository's `AGENTS.md`
for project-only defaults. An `AGENTS.override.md` at the same scope takes
precedence; add the preference there instead when that override is intentional.
Start a new Codex session and ask it to confirm which communication instructions
it loaded. After that, just ask normally. You can change the default through
project instructions or an explicit request.

## Everyday use

Use it with the questions and tasks you already bring to your assistant:

```text
Review this incident summary.
Summarize these survey results.
Explain bottlenecks.
```

When you'd like to explore a term, ask for an explanation. A little context
helps with acronyms that have several meanings. For occasional use, you can
also invoke the installed skill with `$term-inator`.

## Token-Evaporator-Inator Architecture

Term-Inator works on its own. For development work, you can also pair it with
RTK, Ponytail, and Caveman. Each has a different job:

| Component | Responsibility |
| --- | --- |
| [RTK](https://github.com/rtk-ai/rtk) | Filter supported command output before the agent reads it. |
| [Ponytail](https://github.com/DietrichGebert/ponytail) | Keep implementation simple while preserving required behavior. |
| [Caveman Full](https://github.com/juliusbrussee/caveman) | Shorten phrasing while retaining useful content. |
| Term-Inator | Use correct domain terms and preserve relationships, conditions, and uncertainty. |

Keep the original command output available for details you need to revisit,
and check implementation changes against the requirements.

To use them together, install the companions through their linked documentation,
then add this alongside the Term-Inator
instruction in your `AGENTS.md`:

```markdown
At the start of each session, read and apply the installed Ponytail and Caveman
skills. Use Ponytail for implementation decisions and Caveman Full for concise
replies. Use RTK for supported shell commands. Retain Term-Inator's correct terms,
relationships, conditions, and uncertainty. Honor explicit mode changes.
```

## Evaluation

The evaluation suite gives you concrete examples to inspect and try yourself.
**37 of 37 cases passed** the recorded model-assisted review, covering terminology,
requested explanations, uncertainty, handoffs, deferred decisions, and output
formats, relevant non-actions, and material side effects. These smoke tests check
specific communication behaviors; a separate
reviewer grades responses against criteria hidden from the response generator.

The separate [response-relevance comparison](evals/comparisons/response-relevance/README.md)
records 144 replies across six domains: 66/72 passes for v1.3.1 and 69/72 for the
wording adopted in v1.3.2. Both variants preserved material information in all
36 applicable replies. The gain was concentrated in two cases; exact inputs,
responses, grades, and batch-context limits are included.

The [evaluation guide](evals/README.md) provides commands to generate and grade
your own responses, plus the published cases, results, and methodology. To check
the saved results without making model calls:

```sh
python evals/eval.py check
```

## Project notes

For the thinking behind the skill, read the [rationale](docs/RATIONALE.md): how it
started, which ideas shaped it, and the supporting research. The
[lexicon](docs/LEXICON.md) explains the terms used in those discussions. The
[changelog](docs/CHANGELOG.md) records what's changed, and the
[roadmap](docs/ROADMAP.md) describes what we'd like to explore next.

## License

[MIT](LICENSE).
