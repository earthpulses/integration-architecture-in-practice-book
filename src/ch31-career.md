# Becoming an Integration Architect

You have now read the whole of a field. Knowledge, however, is not the same as skill. A reader who has absorbed every chapter can explain idempotency and still build a job that duplicates records, because skill comes from doing the work, seeing it fail, and correcting it. This final chapter turns the book into a path: five levels, each ending in artifacts you can show a manager or a client, and the habits that compound over years.

It closes with the question every practitioner eventually faces: how do you *prove* it? Interviews, design reviews, and client workshops all test the same abilities, and the final sections explain what assessors listen for and how to answer.

!!! goals "In this chapter"
    * Follow a five-level learning path from newcomer to principal, with an artifact for each milestone
    * Build habits that compound: reconnaissance, incident reviews, pattern logs, plain explanations, and reading changelogs
    * Choose books and certifications that support the path
    * Understand how interviewers and clients assess an integration architect
    * Answer design questions with a repeatable structure

## The Learning Path

{{ref fig:learning-zero-to-hero-levels}} shows the five levels. Each ends in artifacts you can show, not courses you attended.

{{fig learning-zero-to-hero-levels | Five levels from newcomer to principal. Each level ends with artifacts you can show.}}

Expect about a year from level 0 to level 3 with steady practice alongside real work. Level 4 is a career stage rather than a course.

### Level 0: Newcomer (Weeks 1 to 4)

You are learning the vocabulary and making your first calls. The milestones are to read Chapters {{ref ch:basics}} and {{ref ch:mindset}} and explain synchronous versus asynchronous communication in your own words; to call three public APIs with `curl` and read the status codes, headers, and bodies; to read an OpenAPI specification and list its authentication, pagination, and error model; to write a Python script with timeouts that handles 200, 404, and 429 differently; and to answer the foundation-level questions in Appendix {{ref app:interviewbank}}.

### Level 1: Practitioner (Months 2 to 3)

You are building components that work. The milestones are to build a watermark poller with pagination, retries with jitter, and a checkpoint (Chapter {{ref ch:python}}); to implement OAuth 2.0 client credentials with a cached, refreshed token (Chapter {{ref ch:auth}}); to write a mapping specification and golden-file tests for one entity (Chapter {{ref ch:formats}}); to build a webhook receiver that verifies signatures and deduplicates events; and to write a reconnaissance sheet for one real API (Chapter {{ref ch:readdocs}}).

### Level 2: Integration Engineer (Months 4 to 6)

You are building systems, with streams and pipelines. The milestones are to run Kafka locally, produce keyed events, and watch consumer groups rebalance (Chapter {{ref ch:kafka1}}); to capture changes from a PostgreSQL database with Debezium into Kafka and sink them to a second database; to automate the failure-injection matrix for one integration (Chapter {{ref ch:testing}}); to put an integration through a delivery pipeline with contract tests (Chapter {{ref ch:delivery}}); and to write a reconciliation job and a run summary with alerts (Chapter {{ref ch:reliability}}).

### Level 3: Solution Architect (Months 6 to 12)

You are leading designs. The milestones are to lead a discovery workshop with the question bank and reach the design gate (Chapters {{ref ch:journey}} and {{ref ch:discovery}}); to produce a brief, an authority matrix, decision records, and a threat model for a real project; to run the decision method and defend the choice against the runner-up (Chapter {{ref ch:decide}}); to estimate with stated assumptions and plan cutover and recovery (Chapter {{ref ch:recovery}}); and to pass the senior questions and two whiteboard exercises in Appendix {{ref app:interviewbank}}.

### Level 4: Principal (Year 2 and Beyond)

You are shaping a practice. The milestones are to write or refresh the standards catalog (Chapter {{ref ch:governance}}); to run a platform proof of concept with failure injection and a three-year cost model (Chapter {{ref ch:platforms}}); to set up an integration inventory and estate indicators; to mentor two engineers through levels 1 and 2; and to explain an integration program to an executive in five minutes with one diagram.

!!! tip "Tick a milestone only when you have the artifact"
    The test of a milestone is a file, a repository, or a document that someone else could read. "I understand it" is not an artifact; "here is the poller, and here is the test that kills it mid-run" is. The artifacts also form your portfolio.

## Habits That Compound

Five habits produce growth beyond what any course gives.

* **Read one vendor API reference a week** and fill a reconnaissance sheet. Patterns in API design become obvious quickly, and you begin to recognize good and bad choices at a glance.
* **Write a short post-incident review for every problem you meet,** even small ones. Writing forces you to separate the cause from the symptom.
* **Keep a pattern log:** for each project, which patterns you used, what went wrong, and what you would change. After ten projects it is your own book.
* **Explain a design to a non-engineer every month.** If they cannot follow, simplify; the skill transfers directly to sponsors and executives.
* **Read the changelogs** of the platforms you depend on. Most surprises are announced somewhere weeks before they arrive.

## Reading and Certifications

The books below deepen the topics of this one. Appendix {{ref app:reading}} gives fuller details.

{{tbl books | Books that deepen the path}}

| Book | Authors | Why |
|---|---|---|
| *Enterprise Integration Patterns* | Gregor Hohpe and Bobby Woolf | The vocabulary of messaging patterns still used by every platform |
| *Designing Data-Intensive Applications* | Martin Kleppmann | Replication, consistency, logs, and streams explained properly |
| *Kafka: The Definitive Guide* | Gwen Shapira and co-authors | Kafka internals and operations |
| *Building Event-Driven Microservices* | Adam Bellemare | Event design and stream-based architecture |
| *Release It!* | Michael Nygard | Stability patterns: timeouts, circuit breakers, bulkheads |
| *Fundamentals of Software Architecture* | Mark Richards and Neal Ford | Architecture characteristics and trade-off thinking |
| *API Design Patterns* | JJ Geewax | Designing APIs others can integrate with |
| *Site Reliability Engineering* | Google (Beyer and co-editors) | Objectives, error budgets, incident practice |
| *Team Topologies* | Matthew Skelton and Manuel Pais | Platform teams and operating models |

Certifications are useful signals but not substitutes for delivered integrations. Common choices are vendor tracks for the platforms you use (for example, MuleSoft developer and integration architect certifications, Confluent's Kafka developer and administrator certifications, the solution architect certifications of AWS, Azure, and Google Cloud) and general architecture frameworks such as TOGAF. Catalogs change often, so check the vendors' current lists before planning.

## How You Will Be Assessed

Hiring managers, sponsors, and clients probe an integration architect in four ways: *fundamentals* (do you understand the ideas?), *depth* (have you operated this?), *judgment* (what would you do when constraints conflict?), and *communication* (can you explain it to a non-engineer?). The signals they listen for are consistent across all four.

{{tbl assess | What assessors listen for}}

| They listen for | A strong signal | A weak signal |
|---|---|---|
| Trade-offs | "It depends on freshness, volume, and network direction; here is how I would decide." | A product name or favorite pattern with no conditions |
| Failure thinking | Unprompted mention of retries, idempotency, duplicates, reconciliation, and monitoring | Describes only the happy path |
| Questions before answers | Clarifies authority, volume, freshness, network, and ownership before drawing | Starts drawing immediately |
| Numbers | Back-of-envelope arithmetic for throughput, limits, and cost | "It should scale" |
| Operations | Runbooks, alerts, ownership, rotation, recovery | Stops at "deployed" |
| Communication | One diagram, plain words, the decision needed | Protocol vocabulary for a non-technical audience |

### A Reusable Answer Structure

For a design question ("design an integration between our CRM and ERP") use a seven-step structure that mirrors the book.

1. **Clarify.** Ask about the outcome, the four numbers, authority, network, and ownership. Say what you are assuming.
2. **Constraints first.** State which constraints rule options out.
3. **Choose a pattern family and a pattern,** and name the runner-up and why you rejected it.
4. **Sketch the flow,** one diagram, with the failure points marked.
5. **Handle failure:** idempotency, retries, quarantine, reconciliation, and what is monitored.
6. **Cover security and operations:** identities, secrets, alerts, owner, runbook.
7. **State the trade-offs and the conditions to revisit the decision.**

The structure shows an assessor, in order, the habits they are looking for. It also keeps you from the commonest failure of a nervous candidate: drawing boxes for ten minutes before asking a single question. Appendix {{ref app:interviewbank}} contains over 150 questions with model answers, what each tests, and the red-flag answer to avoid. Practice them aloud, then mark yourself honestly; the discipline of explaining out loud exposes gaps that silent reading hides.

## Final Words

Integration is, at bottom, the craft of making independent things cooperate despite their differences and failures. The technologies will keep changing, with new platforms, new protocols, and new fashions, but the problems the book has described, meaning, time, and failure, will not. The architect who asks the five questions of Chapter {{ref ch:basics}}, who finds the authority split, who designs for the retry and the duplicate and the outage, who writes the runbook before go-live, and who measures what matters, will be useful on any technology, in any company, for as long as systems need to talk to each other. Which is likely to be a long time.

## Summary

Knowledge becomes skill through deliberate practice with artifacts. Five levels, newcomer, practitioner, integration engineer, solution architect, and principal, each end in things you can show, and five habits compound: reading API references, writing incident reviews, keeping a pattern log, explaining designs plainly, and following changelogs. Books and certifications support the path but do not replace delivered work. Assessors listen for trade-offs, failure thinking, questions before answers, numbers, operations, and clear communication, and a seven-step answer structure presents those signals in order.

## Exercises

1. **Place yourself.** Which level are you on? List the milestones you have *artifacts* for, and the three you will complete next.
2. **Start a pattern log.** Create a document, and enter the last integration you worked on: patterns used, what went wrong, what you would change.
3. **Practice aloud.** Pick five questions from Appendix {{ref app:interviewbank}}, answer them aloud without notes, and then compare with the model answers. Which category is weakest?
4. **Explain it in five minutes.** Explain one integration to a non-engineer using one diagram. Ask them to tell you what they understood.
