# Why Term-Inator exists

An answer can sound helpful and still leave you asking what it actually means.
“Improve error handling” leaves out the operation, the failure, and the
consequence. “Tests pass” leaves you wondering which tests ran. “Recovery
decisions” gives you a label where you needed an explanation.

Term-Inator grew out of that frustration. It is a communication skill for AI
assistants, across topics, designed to **reduce avoidable interpretation work**.
The aim is to keep the terms and context you need to understand an answer, even
when the reply is short.

The intended benefit is more attention for deciding whether the answer makes
sense and what to do next. The research in this document informs the design;
the examples and evaluations help turn that intention into specific behaviors
we can inspect.

## How the idea developed

The first version focused on software commentary: describe the actual change,
use the correct term, and leave out conversational filler.

The scope expanded because expertise is uneven. An experienced backend developer
can be unfamiliar with a business concept. Someone who knows the business may
not recognize the software pattern behind it. The right term gives both a useful
reference for a follow-up question, a search, or a conversation with a colleague.
It does not require every answer to become a lesson.

The 1.2.0 work made another distinction explicit: **correct nouns alone do not
preserve meaning**. This illustrative checkout example shows what was missing.

**Before**

> Recovery decisions.

**After**

> **Deferred:** decide how to recover if order creation fails after payment is
> captured, leaving the customer charged without an order.

The second version preserves the event order, the possible failure, its
consequence, and the decision that remains open. It neither assigns an owner nor
chooses a recovery procedure. Those extra words answer questions the label
leaves behind.

## What a communication skill adds

A skill packages reusable instructions and, when needed, supporting resources.
An instruction-only skill like Term-Inator guides the model through the context
it receives rather than requiring model retraining. This is **specialization at
inference time**: supplying task-relevant guidance when the agent works.[^skills][^specification]

The practical distinction is simple: **the task prompt describes what you need
now; the skill carries expectations you want to reuse**. You can ask “summarize
the remaining work” without restating how to handle terminology, uncertainty,
and deferred decisions each time the skill is in use.

| Benefit | What it gives you |
| --- | --- |
| Reusable expectations | One maintained instruction instead of repeated requests to clarify the same kinds of answer. |
| Shared conventions | A written standard collaborators can discuss for terminology, evidence, and handoffs. |
| Reviewable changes | A way to connect each instruction revision to a concrete requirement or observed failure. |
| Testable behavior | Specific expectations to evaluate, beyond whether the answer sounds more polished. |

The shared format makes a skill portable across compatible hosts. That makes
reuse easier; checking the actual model, host, and companion instructions is
still part of adopting it.[^specification]

Research gives a reason to take this approach seriously. Version 1 of the 2026
*SkillsBench* preprint reports an average **16.2-percentage-point increase in
pass rate** with curated skills across its tested configurations, with varying
results and regressions on some tasks. The study evaluates procedural task
packages, including supporting resources. Its contribution here is evidence
that carefully chosen guidance can help, alongside a clear reason to compare
configurations rather than assume every skill adds value.[^skillsbench]

For Term-Inator, the relevant question is more specific: can a reader understand
the intended meaning with fewer avoidable clarifications?

## Engineering ideas behind the design

**Separation of concerns** keeps communication guidance apart from tool
permissions, implementation decisions, and teaching methods. The **single
responsibility principle** offers a related design influence: separate
responsibilities that change for different reasons. Here, it helps explain why
Term-Inator stays focused on communication. It is an analogy for organizing
instructions, not a formal property of a Markdown file.[^srp]

**Ubiquitous language**, from domain-driven design, provides a useful precedent
for respecting the vocabulary shared by a team and its domain experts. If a
project distinguishes an account from a member, a prose cleanup should preserve
that distinction. This influence does not require adopting a DDD architecture.[^ubiquitous]

Several other terms help describe the design when their meanings stay concrete:

| Term | Meaning for Term-Inator |
| --- | --- |
| Semantic fidelity | Preserve task-relevant meaning when wording changes. “Order creation can fail after payment” must not become “payment failed.” |
| Referential clarity | Make it clear which object a name or pronoun identifies. “Order creation failed” removes ambiguity that “it failed” can leave when both payment and order creation are discussed. |
| Behavioral specification | State observable expectations and exceptions: what a response should preserve, omit, or leave unchanged. This gives constraint-based prompting something concrete to constrain. |
| Composability | Keep instructions compatible when skills operate together. A brevity preference can change phrasing without changing an identifier or required output format. |
| Information density | Include useful meaning without unnecessary text. Here, this is an editorial aim rather than a numerical score. |
| Prompt bloat | Duplicated, irrelevant, or needlessly elaborate instructions. Length alone does not make a prompt wasteful. |

Google's guidance on consistent terminology and clear pronoun references
supports the writing choices behind referential clarity.[^words][^pronouns]

These terms describe what we are trying to preserve. Semantic fidelity is an
editorial objective, for example, rather than a claim of mathematically lossless
compression. The skill remains an instruction-level guardrail: useful behavior
is specified, then checked against actual responses.

## Cognitive load and reading effort

**Cognitive load** concerns demands on human working memory. Cognitive load
theory distinguishes **intrinsic cognitive load**, which depends on both the
material and the reader's existing knowledge, from **extraneous cognitive load**,
which arises from presentation and instructional demands. This distinction
comes from learning research and provides a useful lens for examining assistant
responses.[^cognitive]

Term-Inator targets the effort spent reconstructing an answer: resolving
inconsistent names, reconnecting a claim with a distant qualification, or
guessing what “done” covers. In an illustrative status report, “the build passed;
integration is untested” gives a verification boundary that “looks good” leaves
unstated.

The goal is not to remove the effort of thinking about the work. Understanding
a failure, comparing alternatives, and deciding whether a check is sufficient
still require attention. The opportunity is to spend less of that attention
decoding the explanation.

### Correct terms still need usable context

Shorter text can move work onto the reader. A compressed label may leave them to
infer the sequence that makes it important. An unfamiliar term may also require
more context for one reader than another. Audience-aware writing starts with
what the reader needs to understand, rather than assuming either universal
expertise or universal unfamiliarity.[^audience]

The preference is to avoid automatic definitions, not to withhold necessary
meaning. Describing how a customer can be charged without an order is part of
answering the question; it is not an unsolicited lesson about payment
systems. Clarifying the relevant relationship or consequence keeps the answer
usable. Definitions remain on request; unfamiliarity or stated inexperience
alone does not trigger an explanation.

Requested explanations, comparisons, and plain-language rewrites remain normal
tasks. When the surrounding context already explains the term, repeating the
explanation may add nothing.

The intended benefit is **less effort interpreting the answer while retaining
the effort needed to assess it**. Comprehension, errors, clarification requests,
and reader-reported effort are more informative measures than length alone.

## Context limits and information loss

Human reading effort and model context are related concerns in the workflow,
but they are different things. “Context exhaustion” is too broad to identify a
problem on its own.

| Term | What it describes |
| --- | --- |
| Context-window limit | The token capacity available to a model request. Instructions, history, tool results, and allowances for generation consume capacity according to the model and host. |
| Long-context performance degradation | Relevant information is present but is not used reliably. |
| Compaction loss | A summary or replacement history leaves out a detail that becomes important later. |
| Context pollution | An informal label here for irrelevant material, redundant instructions, or obsolete claims presented as current. It concerns relevance and organization, not a separate capacity limit. |

The context-window limit is a capacity constraint.[^context-window] *Lost in the
Middle* found that performance on its retrieval and question-answering tasks
varied with the position of relevant information, illustrating that fitting
information into a window and using it reliably are separate concerns.[^lost-middle]
Anthropic's context-engineering guidance describes compaction as a way to
continue longer tasks while warning that overly aggressive summarization can
discard important details.[^context-engineering]

Term-Inator contributes at the communication layer: preserve current findings,
uncertainty, constraints, and deferred choices in replies and handoffs. Clearly
separate a superseded diagnosis from the current one. Omit the repetitive story
of failed attempts while retaining what those attempts established.

Retrieval and compaction provide complementary support. A precise summary can
preserve available evidence; missing evidence must be retrieved or its absence
made clear. Wording alone cannot reconstruct it.

When replies become part of later context, unnecessary prose also becomes part
of that history. Reducing it may help, but the loaded skill has its own context
cost. Evaluate the complete exchange, including instructions and extra tool use,
rather than treating a short final reply as the whole saving.

## Evidence over agreement

**Sycophancy** includes favoring agreement with the user's beliefs over accuracy.
Sharma and colleagues observed this behavior across several assistants and tasks
and investigated how human preference judgments can encourage it.[^sycophancy]

For Term-Inator, the concern goes beyond phrases such as “you're right” or
“good catch.” A response can remove those words and still endorse a proposal
without examining the assumption it depends on. The useful replacement is a
substantive assessment: what is supported, what remains uncertain, and what
could change the decision.

This works in both directions. Correct a material false premise, and update the
assessment when new evidence supports the user's position. A passed build is
different from tested integration; a feasible approach is different from a
justified recommendation. Any stated review requirements should survive a
shortened reply.

### Support discernment without taking over judgment

Consider an illustrative exchange where a build has passed but integration has
not been tested. “So we're ready?” should not turn that limited result into
approval. A useful answer keeps the boundary visible:

> The build passed. Integration remains untested; readiness depends on the
> required checks and review.

The purpose is not to make the assistant habitually skeptical. It is to make
confidence track the evidence and to leave the reader able to examine the
recommendation. Clearer wording supports that work; testing, independent
reasoning, and mentorship provide the checks and learning opportunities around it.

## Writing a skill from a real failure

The checkout example gives a practical way to develop a skill. Start with an
answer that failed the reader, then identify what was lost before adding rules.

### 1. Describe the failure precisely

“Too vague” is a useful first observation. The actionable diagnosis is that the
reply omitted the captured payment, possible subsequent order-creation failure,
customer charge without an order, and deferred recovery choice.

Keep the facts separate from the preferred wording. Payment can be captured
while no order exists; choosing a recovery procedure is deferred.
The response must preserve that meaning without inventing an owner, remedy, or
new implementation task.

### 2. Specify the replacement behavior

A candidate instruction could say:

> When summarizing deferred work, preserve the condition that makes a decision
> necessary, its consequence, and what remains undecided. Do not invent an
> owner or a chosen remedy.

This targets the failure rather than a particular phrase. Banning “recovery
decisions” would still allow another vague label, such as “failure handling.”
OpenAI's prompting guidance similarly recommends specifying what to do instead
of relying only on prohibitions.[^prompting]

The lesson is not that negative instructions never work. A clear boundary can
be useful. Pair it with an observable replacement behavior so the agent has
something specific to do.

### 3. Test meaning rather than a preferred sentence

The regression case should accept different wording, including clear Caveman
Full fragments, when the state, failure sequence, consequence, and deferred
choice survive.

Test related cases as well: a similar scenario with different names, a case
where recovery has already been chosen, and an already-clear answer that needs
no change. Include a strict-format request to check that the skill preserves
the requested structure.

These contrasts distinguish a general behavior from a memorized answer. Keep
reference responses and grading criteria in the reviewer's context, separate
from the facts and prompt given to the answering agent.

### 4. Change the smallest relevant instruction

First check whether an existing rule already covers the failure. The problem
may be unclear wording, competing instructions, or a missing evaluation case.
Another paragraph is not automatically the right fix.

Compare the current skill, the candidate revision, and a no-skill baseline in
fresh sessions. Keep the model, settings, input evidence, and companion skills
fixed. Check that persistent instructions have not quietly put the skill into
the baseline. Record improvements, ties, regressions, and overhead. This follows
the paired-comparison approach in the Agent Skills evaluation guidance.[^evaluation]

A small set of revealing cases is a useful starting point. Expand it when actual
responses expose another failure mode, rather than trying to anticipate every
possible conversation in the runtime instructions.

## Testable instructions and regression checks

**Regression testing** checks whether a revision breaks behavior that previously
worked. Some expectations can be checked mechanically: exact text, JSON
structure, required fields, or a stated word limit. **Invariant checks** test
properties that must remain true in the saved response.

These checks detect violations. Used as acceptance gates, they can reject an
unsuitable result; they do not prevent the model from generating it. Meaning
preservation still needs a judgment about the relationship between the source
and the answer.

The public evaluation runner separates response generation, model-assisted
review, and validation of saved results. The generation step receives the skill
and prompt without the grading criteria. Review receives the response and its
criteria. The final check inspects selected structural properties and recorded
judgments.[^runner]

**LLM-as-a-judge** means using a model to assess those responses. It supports a
repeatable review process, but the judgment itself can vary. Research identifies
biases including preferences linked to answer position and verbosity. Human
inspection and contrasting cases help examine results that a mechanical check
alone cannot distinguish.[^judges]

Keep each reported result with its tested revision, prompt, actual response,
criteria, outcome, and relevant settings. Rechecking a saved result and
collecting a fresh model response are different activities. A useful test suite
explains failures and preserves evidence, not just a growing pass count.

## A focused role in the combined workflow

The **Token-Evaporator-Inator Architecture** names an optional workflow with
complementary responsibilities:

| Component | Role |
| --- | --- |
| RTK | Filter and compress supported command output before the agent reads it.[^rtk] |
| Ponytail | Guide simpler implementations that meet the requirements.[^ponytail] |
| Caveman Full | Shorten ordinary reply phrasing, including clear fragments.[^caveman] |
| Term-Inator | Preserve correct terms, relevant relationships, limits, and uncertainty in the explanation. |

These roles overlap; they are not successive stages of a deterministic pipeline.
Caveman already includes meaning-preservation rules. The useful question is
whether Term-Inator improves the combined behavior in the setup being used.[^caveman]

The responsibility split is practical: keep evidence retrievable, verify
implementation changes, and preserve the meaning of the explanation. A filtered
result may need its original output inspected. A simplification may need tests
against the requirements. Term-Inator protects how the agent communicates those
findings and their limits.

An optional coordinator belongs around that workflow rather than
inside the communication skill. Required acknowledgments, task identifiers, and
structured messages should remain intact; coordination protocols are not
conversational filler. Integration belongs in its own guide and tests.

## Keep the runtime small and the reasoning available

**Progressive disclosure** means loading detail when needed. Skill systems can
expose a name and description first, then read full instructions and supporting
resources when a task calls for them.[^skills][^skill-design]

Term-Inator's documented always-on setup requests the core instructions each
session. Keeping this rationale, project history, and evaluation material outside
the required runtime makes them available to readers without making them
prerequisites for ordinary use.

For an author, the distinction is useful: `SKILL.md` explains what the agent
should do and when. The rationale explains why. Evaluation cases describe how
to recognize useful behavior and catch regressions. More explanation for a
reader does not have to mean more instructions in every task.

## What improvement should look like

The next comparisons should examine the work the reader actually needs to do:

| Question | What to inspect |
| --- | --- |
| Is the answer understood? | Can the reader identify the relevant object, condition, consequence, and open decision? |
| Does meaning survive compression? | Do identifiers, negation, scope, sequence, and uncertainty remain accurate? |
| Does a handoff preserve useful state? | Can the next reader distinguish current findings from superseded claims and unresolved work? |
| Does the skill add avoidable work? | Are there needless definitions, repeated qualifications, extra questions, or unnecessary tool calls? |
| Is the tradeoff worthwhile? | Compare comprehension and errors alongside reader effort, time, and available usage measurements. |

Behavioral tests establish how responses handle particular cases. Reader studies
and workflow comparisons address the broader goals: easier interpretation,
better-informed decisions, and efficient use of context. Each kind of evidence
answers a different question.

A useful communication skill gives expectations a maintained home, so they can
be reused, challenged, and tested. For Term-Inator, the goal remains the one that
started the project: understand the answer without having to reconstruct the
important parts yourself.

## References

[^skills]: OpenAI, [Build skills](https://learn.chatgpt.com/docs/build-skills).
[^specification]: Agent Skills, [Specification](https://agentskills.io/specification).
[^skillsbench]: *SkillsBench: Benchmarking How Well Agent Skills Work Across Diverse Tasks* (2026), [version 1](https://arxiv.org/html/2602.12670v1). Preprint; the cited result concerns the study's tested procedural-task configurations.
[^srp]: Robert C. Martin (2014), [The Single Responsibility Principle](https://blog.cleancoder.com/uncle-bob/2014/05/08/SingleReponsibilityPrinciple.html).
[^ubiquitous]: Martin Fowler (2006), [Ubiquitous Language](https://martinfowler.com/bliki/UbiquitousLanguage.html).
[^words]: Google, [Words](https://developers.google.com/tech-writing/one/words).
[^pronouns]: Google, [Pronouns](https://developers.google.com/style/pronouns).
[^cognitive]: Sweller, van Merriënboer, and Paas (2019), [Cognitive Architecture and Instructional Design: 20 Years Later](https://link.springer.com/article/10.1007/s10648-019-09465-5).
[^audience]: Google, [Audience](https://developers.google.com/tech-writing/one/audience).
[^context-window]: OpenAI, [Conversation state](https://developers.openai.com/api/docs/guides/conversation-state).
[^lost-middle]: Liu et al. (2024), [Lost in the Middle: How Language Models Use Long Contexts](https://aclanthology.org/2024.tacl-1.9/).
[^context-engineering]: Anthropic (2025), [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents).
[^sycophancy]: Sharma et al. (2023), [Towards Understanding Sycophancy in Language Models](https://arxiv.org/abs/2310.13548).
[^prompting]: OpenAI, [Best practices for prompt engineering with the OpenAI API](https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-the-openai-api).
[^evaluation]: Agent Skills, [Evaluating skill output quality](https://agentskills.io/skill-creation/evaluating-skills).
[^runner]: Term-Inator, [evaluation runner](../evals/eval.py) and [evaluation guide](../evals/README.md). These describe generation, grading, and saved-result checks; individual run claims belong with their recorded artifacts.
[^judges]: Zheng et al. (2023), [Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena](https://arxiv.org/abs/2306.05685).
[^rtk]: RTK, [project documentation](https://github.com/rtk-ai/rtk).
[^ponytail]: Ponytail, [skill instructions](https://github.com/DietrichGebert/ponytail/blob/main/skills/ponytail/SKILL.md).
[^caveman]: Caveman, [skill instructions](https://github.com/JuliusBrussee/caveman/blob/main/skills/caveman/SKILL.md).
[^skill-design]: Anthropic (2025), [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills).
