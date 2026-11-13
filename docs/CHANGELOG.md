# Changelog

User-visible changes by version. Git commits and release tags retain the detailed
history and timing.

## 1.3.1

- Name irrelevant reporting explicitly and keep responses relevant and concise.
- Report non-actions and unchanged properties only when they answer the request
  or materially clarify completion, side effects, or verification.
- Record 37/37 passing cases in the shared comparison suite; retain the 1.3.0
  result under its own tag.

## 1.3.0

- Omit defensive qualifications, redundant disclaimers, and immaterial caveats.
- Remove repeated points and low-value closing sentences while preserving meaning.
- Expand the suite from 33 to 37 cases to check relevant negative findings and
  material side effects. Record 36/37 passes; T34 retains irrelevant non-actions.
- Let the runner's unit tests verify recorded failures as well as passing results.

## 1.2.0

- Preserve deferred decisions and their consequences without inventing owners
  or choosing procedures.
- Distinguish current conclusions from superseded claims; retain useful findings
  from unsuccessful attempts in handoffs.
- Keep qualifications near claims, distinguish feasibility from supported
  recommendations, and update assessments when evidence resolves concerns.
- Clarify that a user's stated inexperience does not itself request definitions.
- Expand the behavioral suite from 21 to 33 cases; add `--skill` so users can
  evaluate other instruction files against the same cases.
- Add rationale, a context-engineering lexicon, roadmap, and version history
  under `docs/`.

## 1.1.0

- Broaden terminology guidance from software work to communication across domains.
- Make explanations user-directed rather than automatically defining unfamiliar
  terms; preserve explicit requests for explanations and plain language.
- Strengthen ambiguity handling, evidence distinctions, and response to corrections.
- Add broad examples, always-on setup instructions, and a runnable 21-case
  evaluation suite with recorded responses and separate model-assisted grading.
- Document the optional Token-Evaporator-Inator workflow.

## 1.0.0

- Introduce the software-focused communication skill: concrete names, observable
  behavior, useful context, and evidence-aligned claims.
- Preserve requested formats and implementation scope while removing filler.
- Package the skill with Codex interface metadata and artwork.
