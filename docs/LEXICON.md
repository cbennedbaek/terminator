# Context engineering lexicon

“The answer is too short” can mean several things: an identifier is missing, a
condition disappeared, or a conclusion sounds more certain than its evidence.
Having words for those differences makes it easier to explain what needs fixing.

This lexicon covers the ideas behind Term-Inator and the wider workflow around
it. The entries connect each term to a practical question about writing,
reviewing, or using a communication skill. Informal phrases and project-specific
uses are identified where they appear.

Read it alongside [the rationale](RATIONALE.md): the rationale explains the design choices;
this document explains the vocabulary. Both are optional reference material,
separate from the runtime instructions. Examples illustrate the distinctions;
they are not reports of measured improvements.

## Context and memory

### Context engineering

Selecting, organizing, and maintaining the information a model receives:
instructions, conversation history, retrieved material, and tool results.
**Prompt engineering** focuses more narrowly on how the instructions and
examples are written within that context.[^context-engineering]

The practical question is: *What information does the agent need for this step?*
Term-Inator contributes communication instructions and guides the replies that
may become part of later context. The host controls which material is loaded,
retained, or replaced.

### Context window and token budget

The **context window** is the token capacity available for a model request.
A **token budget** allocates capacity within the relevant model or application
limits. Instructions, retained messages, and tool results occupy space;
allowances for generated output and reasoning depend on the model and host.[^conversation-state]

**Context exhaustion** is informal shorthand for reaching a context limit.
Depending on the system, reaching the limit may lead to request rejection,
truncation, or compaction. Describe the actual event when diagnosing it:
“the request exceeded the context limit” is more specific than “the model ran
out of memory.”

### Long-context performance degradation

Relevant information can be present in the context without being used reliably.
*Lost in the Middle* found that performance on its retrieval and
question-answering tasks depended on where the relevant information appeared.
The observed effect belongs to the models and tasks studied.[^lost-middle]

For a missed requirement, ask two separate questions: was the requirement
available, and did the response account for it? More capacity can help when
relevant material was excluded for lack of space; missing material may instead
need retrieval. Reliable use of available information addresses the second question.

### Context pollution

An informal label for irrelevant, misleading, stale, or unresolved contradictory
material accumulating in the supplied context. It describes a relevance problem,
not simply a large amount of text.

A ruled-out diagnosis may still be worth retaining if it prevents repeated
investigation. Label it as superseded, and distinguish it from the current
finding. The useful cleanup preserves what earlier work established while
removing repetition and confusion about what still applies.

### Compaction

Replacing accumulated context with a shorter representation so work can continue
within the available capacity. A useful summary preserves the decisions,
conditions, and unresolved issues needed for the next step. **Compaction loss**
occurs when that representation leaves out something needed later.[^context-engineering]

In the checkout example, “recovery deferred” loses why recovery matters.
Keeping the captured payment and possible order-creation failure makes the
handoff more informative. Term-Inator guides that wording when its instructions
apply; the host determines when and how compaction runs.

### Progressive disclosure

Making detail available when it becomes relevant. In skill systems, the host can
start with a name and description, then load the full instructions and supporting
resources as needed.[^skills][^agent-skills]

Term-Inator's documented always-on setup asks for its core instructions each
session. This lexicon, the rationale, and the evaluation material remain
optional reading. That distinction lets the project explain its design without
making every explanation part of every task prompt.

## Language and human effort

### Cognitive load

Demands on human working memory. Cognitive load theory distinguishes
**intrinsic cognitive load**, which depends on the material and the reader's
existing knowledge, from **extraneous cognitive load**, which arises from how
information is presented and what the instructional procedure requires.[^cognitive-load]

For Term-Inator, this is a way to examine avoidable interpretation work. The
reader still needs to assess the underlying problem; inconsistent names or a
missing condition add another task before that assessment can begin.

**Context fatigue** is an informal description of a person's experience during
a demanding conversation. Repeated rereading, missed conditions, and reported
effort are useful things to examine. Keep that human experience separate from
a model's context capacity or retrieval performance.

### Information density

Useful meaning relative to the amount of text. Here, it is an editorial goal,
not a defined numerical score. A short label earns its place only if it carries
what the reader needs.

“Recovery decisions” is compact but leaves the failure and open decision
unexplained. This illustrative checkout example makes both explicit:

> **Deferred:** decide how to recover if order creation fails after payment is
> captured, leaving the customer charged without an order.

The extra words preserve the sequence, consequence, and deferred choice. Judge
the note by what a reader can understand from it, alongside its length.

### Semantic fidelity

Preserving task-relevant meaning when wording changes. This is the project's
editorial use of the term: the response should retain the distinctions that make
the source accurate and useful.

In the checkout example, **can fail** preserves possibility rather than
reporting an event, **after** preserves the sequence, and **deferred** preserves
the decision's status. Keeping the term “payment capture” while losing those
relationships would retain terminology but change or obscure the meaning.

Evaluate fidelity against the supplied facts and the task, rather than requiring
the response to repeat one reference sentence.

### Referential clarity

Making it clear which object a name or pronoun refers to. “It failed” can be
ambiguous when a sentence mentions payment processing and order creation.
“Order creation failed” identifies the operation.

Consistent terminology and clear pronoun references help readers follow an
explanation. Repeat the noun when it resolves ambiguity; use the pronoun when
its reference is already clear.[^clear-language]

This complements semantic fidelity: the relationship can be correct while the
reader is still left guessing which object participates in it.

### Ubiquitous language

A shared vocabulary grounded in a domain model and developed with domain
experts, as used in domain-driven design. It provides a precedent for preserving
the distinctions a team relies on.[^ubiquitous-language]

An account and a member may be separate concepts in one project, even if another
system uses tenant and user. Follow the meaning established in the current
domain rather than rotating familiar words for variety. A terminology cleanup
should preserve deliberate distinctions, not silently rename the domain.

### Epistemic humility

Acknowledging the limits of what is known. In Term-Inator, that means stating
material uncertainty specifically and accepting supported conclusions when the
evidence resolves it.

“The build passed; integration remains untested” identifies the boundary more
clearly than a generic “I might be wrong.” Ask for missing context when different
interpretations would materially change the answer.

**Bounded epistemic humility** is shorthand from the design discussions, not a
separate formal method. Keep real gaps visible without treating every established
fact as doubtful or adding objections after the relevant evidence is supplied.

### Sycophancy

Favoring agreement with the user's beliefs over accuracy. Research has observed
assistants endorsing users' views and changing answers in ways that prioritize
agreement over correctness.[^sycophancy]

The response can be sycophantic without saying “you're right.” A confident
recommendation that merely accepts an unsupported premise has the same problem.
Term-Inator asks for a substantive assessment: identify what is supported,
correct material errors, and revise when new evidence warrants it.

Courtesy, a valid correction, and warranted agreement remain useful. The target
is unsupported endorsement, not agreement itself.

## Instructions and evaluation

### Behavioral specification

A description of observable expectations and exceptions. For a communication
skill, it explains what a reply should preserve, clarify, omit, or leave
unchanged. It turns “be precise” into behavior that a reviewer can inspect.

For example:

> When summarizing deferred work, preserve the failure condition, its
> consequence, and the decision that remains open. Do not invent an owner or
> a chosen recovery procedure.

**Constraint-based prompting** uses explicit requirements to guide the response.
Pairing an important prohibition with the desired alternative gives the agent
more direction than a list of banned phrases.[^prompt-guidance]

This is a natural-language specification. Evaluation checks how well responses
follow it; the instructions are not an executable enforcement layer.

### Prompt bloat

Informal shorthand for instructions that add little value through duplication,
irrelevant detail, or conflicting requirements. Length alone is a poor test: an
example or qualification may be exactly what makes a rule useful.

For each instruction, ask what failure it addresses and whether it earns its
place in comparisons. Keep the explanation of the design in documentation when
the agent only needs the rule. A small runtime and a detailed rationale serve
different readers.

### Constraints and assertions

These terms describe related but distinct parts of a testable instruction:

| Term | Meaning | Example |
| --- | --- | --- |
| Constraint | A requirement on the response. | Return valid JSON with the required fields. |
| Negative constraint | A prohibition. | Add no prose outside the JSON value. |
| Invariant | A property expected to remain true within a defined scope. | In an exact-text task, preserve the supplied identifier unchanged. |
| Assertion | A check of a stated condition. | Parse the saved response and check that the required fields exist. |

A Python check can detect a changed identifier or malformed structure. A word
blacklist cannot determine whether a paraphrase preserves the failure sequence.
Use mechanical checks for properties they can inspect and semantic review for
the meaning of the answer.

### Regression testing

Repeating checks after a change to detect behavior that previously worked and
now fails. In Term-Inator, that includes both structural requirements and
meaning-preservation cases.

The checkout regression accepts different wording when it preserves the
state, possible failure, consequence, and deferred choice. A useful additional
case would cover recovery that has already been chosen, to catch a rule that
labels every recovery decision as deferred.

Compare revisions on the same inputs in fresh contexts, keeping other settings
fixed. Include a no-skill baseline when measuring the skill's contribution.[^skill-evaluation]
Rechecking a saved response inspects recorded output; collecting fresh responses
examines model behavior and its variability.

### LLM-as-a-judge

Using a language model to assess a response against supplied criteria. It lets
the same criteria be applied across many responses, while introducing another
source of error.
Research identifies biases including preferences related to response position
and verbosity.[^model-judges]

Term-Inator's evaluation runner separates response generation, reviewer
judgments, and checks of saved results. Grading criteria belong with the reviewer,
not in the answering agent's input.[^project-evaluations]

Keep the actual response, criteria, and judgment available for inspection. A
reviewer can be wrong, and a long answer can still omit the one condition that
matters. Human inspection and contrasting cases help reveal those mistakes.

### Separation of concerns

Organizing a system so distinct responsibilities can be understood and changed
with less coupling. The related **single responsibility principle** groups work
around the reasons it changes.[^single-responsibility]

For the combined workflow, communication, implementation simplicity, phrasing
density, and tool-output filtering have different jobs. Term-Inator protects
the explanation; implementation checks and evidence retrieval provide
complementary support. This is a design influence for organizing instructions,
not a claim that a Markdown prompt implements a software architecture.

### Composability

How well components or instructions work together without undermining each
other's requirements. In this project, it means checking the combined behavior,
not merely installing several skills.

Caveman Full can shorten a reply into clear fragments while Term-Inator preserves
relevant identifiers, conditions, and uncertainty. Required protocol messages,
quoted strings, and structured fields still need to keep their intended form.

Test ordinary replies and format-sensitive cases together. A style preference
that breaks a coordination message is a compatibility problem, not successful
compression.

### Agent loop and human-in-the-loop

An **agent loop** repeatedly selects an action, observes its result, and decides
what to do next. **Human-in-the-loop** means human input, review, or decisions
form part of that process.

Clear findings and pending decisions help a person steer the work. “The build
passed; integration is untested” gives a reviewer a more specific starting point
than “done.” A handoff should retain any stated approval requirement rather than
turning a successful check into permission to proceed.

These terms describe participation in a workflow. They do not prescribe a tone,
response length, or speed target.

### Evidence provenance and status

**Provenance** identifies where information came from. **Status** identifies what
kind of claim is being made: an observation, hypothesis, proposal, completed
action, or verified result.

For an illustrative status report:

> The build log reports exit code `0`; integration of the proposed fix remains
> untested.

The log supplies provenance. The successful build and outstanding integration
check establish the scope of the report. Verification remains tied to what was
actually checked.

**Telemetry** is operational data, such as logs and metrics. It can supply
evidence; distinguishing a proposal from an observation is a communication
responsibility, whether that evidence comes from telemetry or another source.

## Model behavior and reasoning

### Attention

A model mechanism that relates information through queries, keys, and values.
For a query, compatibility with the keys determines weights used to combine the
associated value vectors. In **self-attention**, those queries, keys, and values
come from representations of the same sequence.[^attention]

This is different from a person's attention while reading. Headings and clear
instruction structure organize the prompt; evaluate their usefulness through
responses. Claims about specific changes to internal attention weights require
analysis of the model, rather than inference from the formatting alone.

### Chain-of-thought prompting

Prompting with intermediate reasoning steps, including demonstrations that show
how to reach an answer. Wei and colleagues found improvements on particular
arithmetic, commonsense, and symbolic reasoning tasks in the models they studied.[^chain-of-thought]

Conversational introductions, praise, and repeated acknowledgments are not
reasoning steps simply because they appear before an answer. Likewise, final
response length describes the text the reader receives, not all the computation
used to produce it. Term-Inator focuses on the explanation the task requires.

### Inference-time compute

Computation used when producing an answer, also called **test-time compute**.
It can include generating candidates, searching, revising, or verifying them.
Research on allocating this compute finds that the useful strategy depends on
the task and its difficulty.[^test-time-compute]

**High-compute reasoning** is a broad description, not a specification of
particular hardware or a prerequisite for Term-Inator. Examine the work performed
and available usage measurements separately from how concise the final reply is.

### Persona prompting

Asking a model to adopt a role, perspective, or voice. A role can express useful
context, such as reviewing a change for its intended audience. Observable
requirements make that role easier to evaluate.

“Act as a world-class expert” gives a status description. “Identify the material
assumption, explain its consequence, and retain unresolved checks” describes
work a reviewer can inspect. Term-Inator favors those concrete expectations
while preserving the voice requested for an authored artifact.

## Informal phrases from the design discussions

These labels can be memorable. The table preserves their intended use while
pointing to more concrete wording when discussing behavior or measurements.

| Phrase | Practical meaning here |
| --- | --- |
| Context architecture | How instructions, history, retrieved evidence, and tool results are organized. Describe the actual loading and retention policy rather than implying a deterministic memory stack. |
| Token evaporation | The Token-Evaporator-Inator workflow's metaphor for removing low-value text while preserving useful meaning. Assess savings across the exchange, including instructions and tool use. |
| Negative space architecture | An informal name for defining boundaries around unwanted behavior. Pair important boundaries with positive instructions and examples; **behavioral specification** is the more direct description. |
| Attention steering / attention dilution | Use **instruction organization** or **context-use performance** for observable changes. Claims about internal attention weights belong to model analysis. |
| Probability disruption | Use **wording constraints** for instructions to avoid certain expressions. Describe a change to sampling only when the sampling mechanism is actually part of the evidence. |
| Entropy generation | Use **stylistic variation** for varied sentence structure. Statistical entropy requires a defined probability distribution and measurement. |
| Stereotype drift | Informal shorthand here for a persona becoming clichéd. Identify the repeated wording or unwanted behavior rather than relying on the label. |
| Telemetry separation | Use **evidence provenance and status** when distinguishing observations, proposals, and results in prose. Reserve telemetry for the operational data itself. |
| Sycophancy drift | Use **sycophancy** for unsupported agreement. Describe and test any change across turns separately. |

The vocabulary is useful when it helps explain a real difference: what meaning
was lost, what an instruction asks for, or what a test establishes. Keep those
connections visible, and the terms become tools for improving the skill rather
than another layer the reader has to decode.

## References

[^context-engineering]: Anthropic. [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents). Guidance on selecting context, targeted retrieval, and compaction.

[^conversation-state]: OpenAI. [Conversation state: managing the context window](https://developers.openai.com/api/docs/guides/conversation-state). Request capacity and context management.

[^lost-middle]: Liu et al. [Lost in the Middle: How Language Models Use Long Contexts](https://aclanthology.org/2024.tacl-1.9/). Research on information position and performance in long contexts.

[^skills]: OpenAI. [Build skills](https://learn.chatgpt.com/docs/build-skills). Skill discovery, progressive disclosure, and runtime instructions.

[^agent-skills]: Anthropic. [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills). Packaging reusable instructions and resources.

[^cognitive-load]: Sweller, van Merriënboer, and Paas. [Cognitive Architecture and Instructional Design: 20 Years Later](https://link.springer.com/article/10.1007/s10648-019-09465-5). Cognitive load, reader knowledge, and presentation demands.

[^clear-language]: Google. [Words — Technical Writing One](https://developers.google.com/tech-writing/one/words) and [Pronouns](https://developers.google.com/style/pronouns). Consistent terminology and clear pronoun references.

[^ubiquitous-language]: Martin Fowler. [Ubiquitous Language](https://martinfowler.com/bliki/UbiquitousLanguage.html). Shared domain vocabulary developed with domain experts.

[^sycophancy]: Sharma et al. [Towards Understanding Sycophancy in Language Models](https://arxiv.org/abs/2310.13548). Agreement with user beliefs at the expense of accuracy.

[^prompt-guidance]: OpenAI. [Best practices for prompt engineering with the OpenAI API](https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-the-openai-api). Specific requirements and positive alternatives to prohibited behavior.

[^skill-evaluation]: Agent Skills. [Evaluating skill output quality](https://agentskills.io/skill-creation/evaluating-skills). Baselines, fresh contexts, assertions, and comparison of outcomes and overhead.

[^model-judges]: Zheng et al. [Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena](https://arxiv.org/abs/2306.05685). Model-based review and documented grading biases.

[^project-evaluations]: Term-Inator. [Evaluation guide](../evals/README.md). Project response generation, separate review, and validation of saved results. Individual runs identify the tested revision.

[^single-responsibility]: Robert C. Martin. [The Single Responsibility Principle](https://blog.cleancoder.com/uncle-bob/2014/05/08/SingleReponsibilityPrinciple.html). Responsibility, reasons to change, and separation of concerns.

[^attention]: Vaswani et al. [Attention Is All You Need](https://arxiv.org/html/1706.03762v7). Query-key-value attention and self-attention.

[^chain-of-thought]: Wei et al. [Chain-of-Thought Prompting Elicits Reasoning in Large Language Models](https://arxiv.org/abs/2201.11903). Intermediate reasoning demonstrations and task performance.

[^test-time-compute]: Snell et al. [Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters](https://arxiv.org/abs/2408.03314). Allocation of inference-time computation.
