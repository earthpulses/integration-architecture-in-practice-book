# The Architect's Mindset

Two engineers are handed the same task: connect the web shop to the ERP. The first opens the ERP's API documentation, finds the "create sales order" endpoint, writes a script that calls it for every new order, and demonstrates it to the team that afternoon. It works. The second engineer spends the afternoon asking questions. How many orders arrive on the busiest hour of the busiest day? What happens to an order if the ERP is in its maintenance window? Who decides the price when the shop and the ERP disagree? Who gets called at 3 a.m. when orders stop flowing?

By Friday the first engineer has a demo and the second has a list of questions, and the first looks faster. Three months later the first engineer's script has lost 400 orders during a weekend outage, has no alerting, and cannot be run twice without creating duplicates. The second engineer's integration is still running, because the hard decisions were made when they were cheap.

The difference is not intelligence or tooling. It is a way of thinking, and it is what this chapter teaches. The integration architect's job is not to be the best coder on the project. It is to **shrink the gap between the demo and the messy reality** before the messy reality arrives. That gap is where integrations fail.

!!! goals "In this chapter"
    * Recognize the ten defaults experienced architects assume about every integration
    * Ask the three questions that sit behind every design
    * Describe the full lifecycle an architect is accountable for, and the artifact each phase produces
    * Name the thirteen skill domains of the role and assess your own profile
    * Use the ten technology-independent ideas that every platform renames
    * Argue the six trade-offs that never go away, and record decisions in an architecture decision record

## Ten Defaults to Assume Before You Read a Single Document

Experienced architects begin every project with a list of assumptions about how integrations fail. They write them on the whiteboard in the first workshop and then design as though they were already true. Each one is cheap to design for on the first day and expensive to discover on the ninetieth.

{{tbl defaults | Ten defaults, their design consequence, and the symptom when ignored}}

| Default assumption | What it means for design | Symptom if ignored |
|---|---|---|
| The API will rate-limit you | Build backoff and a request budget from the start | The nightly sync works in test, then fails at 02:14 in production with HTTP 429 |
| The API will return partial failures | Check per-item results, not only the HTTP status | HTTP 200 with 40 of 5,000 records rejected inside the body |
| Clocks are not synchronized | Use overlap windows and server-issued watermarks, never "last run time" from your own clock | Records changed during the sync are skipped forever |
| IDs are not stable across systems | Store the source ID on the target, and the target ID on the source where possible | A rename in the source creates a duplicate in the target |
| Documentation is wrong somewhere | Probe every endpoint with `curl` before you design around it | The documentation says the field is `caller`; the API returns `caller_id` |
| The sandbox is not production | Ask for production-sized data and production authentication settings early | It works against 200 rows and times out against 2 million |
| Credentials will be rotated | Keep secrets in a vault; handle 401 with exactly one re-authentication | The integration dies on a Sunday when a service-account password expires |
| A firewall sits in the way | Identify the network path and who can open ports in week one | Everything works from the consultant's laptop and nothing from the server |
| Somebody will run it twice | Make every write idempotent | Duplicate tickets; double-counted measures |
| Nobody owns it after you leave | Treat the runbook, alerting, and a named owner as deliverables | The integration is quietly broken for a quarter before anyone notices |

It is worth dwelling on a few of these, because each hides a story that repeats on almost every project.

**"Clocks are not synchronized"** is the most underestimated. Suppose your sync job records "I last ran at 10:00:00" and next time asks the source for everything changed since 10:00:00. A record the source modified at 09:59:58 but committed to its database at 10:00:03 will never be returned by that query, because its timestamp is older than your bookmark. The record is skipped forever, with no error anywhere. Chapter {{ref ch:python}} shows the fix: use the *source's* timestamps, and always re-read a short overlap window, relying on idempotency to make the repeats harmless.

**"The sandbox is not production"** deserves a place on every risk list. Vendor sandboxes typically differ from production in rate limits, data volume, enabled features, and authentication settings. An integration validated against a sandbox with 200 rows tells you very little about how it behaves against 2 million. Chapter {{ref ch:delivery}} shows how to close that gap with a shadow run in a production-like environment.

**"Nobody owns it after you leave"** is the quietest failure. Integrations rarely crash loudly. They stall: a token expires, a schedule is disabled during a migration, a field is renamed, and the data simply stops moving. If no alert fires and no person owns the flow, the first sign of trouble is a business user asking why a report is wrong, often weeks later.

!!! why "Why this matters"
    Integration projects rarely fail on the happy path. They fail on the third day of production, on the one record with an emoji in the name, or when the source team ships a "minor" API change. Writing these defaults down at the start turns vague unease into a checklist that the whole team can design against.

## The Three Questions Behind Every Integration

Beneath the ten defaults sit three questions. If you can answer them for an integration, the design usually becomes obvious. If you cannot, you are not ready to design.

**Where does the truth live?** For every entity and every field, exactly one system should be authoritative. The shop owns the customer's shipping address as typed at checkout; the ERP owns the stock level and the invoice number. When two systems both edit the same field, you have a conflict-resolution problem, which is the most expensive kind of integration to build and to operate. Part of an architect's craft is steering a project toward *clean authority splits* so that conflicts never arise. Chapter {{ref ch:patterns2}} develops this idea.

**How fast must change travel?** Seconds, minutes, hours, or next day. This one answer eliminates most of the pattern catalog, and it drives cost more than any other requirement. "Real time" is expensive, and it is often requested out of habit rather than need. When a business owner says "real time," ask what decision is made with the data and how long that decision can wait. Frequently the honest answer is "within a few minutes," which opens up far cheaper designs.

**What happens when it breaks?** Who is told, what is retried, what is parked for a human, and how do we reconcile afterward? A design without an answer here is a prototype, however polished the diagrams.

## The Lifecycle You Own

A common mistake is to think of the architect as the person who draws the boxes at the start. In practice, the architect is accountable for the whole arc, from the first conversation to the retirement of the integration years later. {{ref fig:skills-integration-lifecycle}} shows the seven phases.

{{fig skills-integration-lifecycle | An architect is accountable for the whole arc, not only the design phase. Each phase produces something concrete and ends with a sign-off.}}

Each phase has a characteristic output and a characteristic way of failing when it is skipped.

{{tbl lifecycle | The seven phases, their outputs, and the failure when skipped}}

| Phase | You produce | Typical failure if skipped | Who signs off |
|---|---|---|---|
| Discover | Integration brief, authority matrix, the four numbers, risk list | Right solution to the wrong problem | Business owner |
| Design | Pattern choice with rejected alternatives, contracts, network and security design, decision records | Late discovery of firewall, authentication, or volume limits | Architecture board, security |
| Build | Flows or code, mappings as configuration, infrastructure as code | Click-built flows nobody can reproduce | Technical lead |
| Test | Contract tests, failure injection, volume test, reconciliation report | Acceptance by demo | Quality assurance and business |
| Release | Go-live checklist, backfill plan, rollback plan, communications | The initial load corrupts the target | Change board |
| Operate | Alerts, runbook, dashboards, reconciliation schedule, on-call rota | Silent breakage for weeks | Operations owner |
| Evolve | Versioning policy, deprecation notices, retirement plan | Zombie integrations nobody dares touch | Product owner |

The discover phase introduces **the four numbers**, which you should leave every first workshop with: how many records exist now; how many you expect in three years; the peak number of changes per hour; and the maximum acceptable staleness. With those four numbers you can size an API budget, choose between polling and streaming, and estimate cost, all before writing a line of code. Chapter {{ref ch:discovery}} shows how to get them.

## Thirteen Skill Domains

The role of an integration architect draws on thirteen skill domains. You will not be equally strong in all of them, and you do not need to be. What matters is knowing where you are weak, so that you can learn, or involve a specialist, before the weakness hurts a project. {{ref tbl:skills}} summarizes each domain, what "good" looks like, and the artifact that proves it.

{{tbl skills | The thirteen skill domains of an integration architect}}

| Domain | What good looks like | Artifact you can show |
|---|---|---|
| Discovery and requirements | You leave every workshop with an authority matrix, the four numbers, and a named owner | One-page integration brief |
| Systems thinking | You can say what breaks, for whom, and how long it takes to notice when any component dies | Failure-mode table |
| Data and semantics | You settle matching, deletes, and field ownership before code is written | Authority matrix and field mapping |
| Interface and contract design | You write the OpenAPI or AsyncAPI contract first, with idempotency, pagination, and errors defined | API and event specifications |
| Security and identity | Every integration has a dedicated identity, a rotation plan, and a data classification | Security review pack |
| Networking and hybrid connectivity | You can spot the proxy that will break TLS in week three | Network path diagram |
| Platform literacy | You can translate a design between platforms ("an SQS queue here, a Service Bus queue there") | Platform mapping table |
| Reliability and performance | Every flow has a timeout, retry policy, duplicate strategy, and volume test | Failure-injection results |
| Observability and operations | The business hears about an outage from your alert, not from a user | Runbook and alert catalog |
| Delivery and engineering practice | Flows and configuration are versioned, promoted, and reproducible | Pipeline and infrastructure code |
| Governance, cost, and vendor judgment | You can defend a platform choice with numbers and record why alternatives were rejected | Decision records |
| Communication and leadership | An executive and an engineer can both act on the same one-page design | Executive one-pager |
| Testing and quality engineering | You prove correctness with reconciliation reports, not demos | Test plan and reconciliation report |

To assess yourself, rate each domain from 1 (new to it) to 5 (could teach it to a colleague). Be honest; nobody will see the result but you. Then circle your three lowest scores and read the chapters that teach them first. Chapter {{ref ch:career}} turns the same list into a twelve-month learning plan.

!!! tip "The most common gap"
    In our experience of reviewing architects' profiles, networking and operations are the two domains rated lowest, and they cause a disproportionate share of production incidents. If you are strong on design and weak on these, you are not unusual, and you now know where to invest.

## Mental Models That Do Not Change with the Technology

Technologies come and go every few years; the underlying ideas do not. A platform vendor will tell you that their product has "message groups," "sessions," "key-based partitioning," or "sequential processing flags." They are all answers to the same question: does the order of messages matter? Learn the question once and you can read any vendor's documentation.

{{tbl ideas | Ten ideas that every platform renames}}

| Idea | The question it answers | On premises (MQ, ESB) | Cloud native | Integration platform | In your own code |
|---|---|---|---|---|---|
| Idempotency | What if this runs twice? | Duplicate detection on message ID | FIFO queue dedupe ID; API idempotency keys | Upsert by key; data-store check | A deduplication table |
| Retry | What if the target is briefly down? | Backout count and requeue | Workflow retry policies | Retry scopes; until-successful | Backoff with jitter |
| Dead letters | Where do poison messages go? | Backout queue | Dead-letter queues | Error queues; failed-record batches | Quarantine table or topic |
| Ordering | Does sequence matter? | One consumer per queue; message groups | FIFO queues; sessions; partitions | Sequential processing flags | Key-based partitioning |
| Backpressure | What if the producer is faster? | Queue depth limits | Autoscaling; throttling | Concurrency limits | Bounded queues; pause and resume |
| Contracts | What may consumers rely on? | WSDL and XSD | OpenAPI; AsyncAPI; schema registry | API specs in a design catalog | Typed models; contract tests |
| Identity | Who is calling? | Service accounts; certificates | Managed identity; IAM roles; OAuth | Connection credentials | Vault client; workload identity |
| Time | Whose clock, what zone? | Batch calendars | UTC; event time versus processing time | Scheduler time zones | Timezone-aware datetimes |
| Consistency | How wrong may data be, for how long? | Two-phase commit | Sagas; eventual consistency | Compensating flows | Outbox; reconciliation |
| Ownership | Who fixes it at 3 a.m.? | Operations team | Platform plus product team | Center of excellence | The service owner |

The table repays study. If you can fill in the fourth column for a technology you know well, you understand it; if you can fill in the fifth for one you do not, you can learn it quickly.

## Trade-offs You Will Argue for the Rest of Your Career

Architecture is the art of choosing which problem to have. Six trade-offs recur in almost every design review, and a good architect can argue either side of each, depending on the context.

**Freshness, reliability, and cost.** You can usually afford two of the three. Real-time and reliable is expensive, because it needs streaming infrastructure, replay, and on-call staff. Cheap and real-time tends to drop events when something fails. Cheap and reliable is batch: late, but dependable.

**Coupling versus simplicity.** Direct calls between systems are simple until the fifth system joins, at which point the number of links explodes. Events decouple producers from consumers at the price of invisibility. Choose by asking how many consumers there will be in two years, not how many there are today.

**Consistency versus availability.** Transactions that span systems rarely exist in practice. Decide which side may be stale, for how long, and how you repair it. The tools are sagas, outboxes, and reconciliation, which Part II and Chapter {{ref ch:sync}} explain.

**Build versus buy.** Custom code wins on control and loses on long-term maintenance. Integration platforms win on speed and available connectors and lose on cost curve and lock-in. Neither is right in general; Chapter {{ref ch:platforms}} gives a method for choosing.

**Central versus federated.** A central integration team guarantees standards and tends to become a queue that everyone waits in. Federated teams move faster and drift apart. The usual compromise, and the one Chapter {{ref ch:governance}} recommends, is a platform team that provides a well-lit "paved road" while domain teams build on it.

**Canonical versus bounded models.** A shared data model across all systems removes translation sprawl and creates a committee to maintain it. Use canonical models only for a small number of stable, widely shared entities such as customer and product.

## Recording Decisions

A decision that is not written down gets re-argued every six months by whoever was not in the room. The standard remedy is the **architecture decision record**, or ADR: a half-page document that captures what was decided, why, and under what conditions the decision should be revisited.

```text
ADR-014: Use polling with a watermark instead of webhooks for ticket sync
Status:    Accepted (2026-11-23)         Deciders: <names>
Context:   The source offers webhooks without replay; the network is
           outbound-only; the freshness target is 5 minutes.
Options:   (A) webhooks plus a queue
           (B) polling with a modified-since filter
           (C) change data capture on the source database
Decision:  B, with a nightly ID-list reconciliation to detect deletes.
Because:   It meets the 5-minute target, needs no inbound firewall rule,
           and is replayable by resetting the watermark.
Consequences: Up to 2 minutes of overlap is re-read (idempotent upsert);
           no sub-minute latency; deletes are detected up to 24 h late.
Revisit when: The freshness target drops below 1 minute, or the API
           rate limit is lowered.
```

The most valuable lines in an ADR are the last two. "Consequences" forces you to state what you gave up, and "Revisit when" turns a permanent verdict into a conditional one with a trigger. Both make it easier for a successor to trust or challenge the decision intelligently.

!!! example "Larkspur Outdoor: the first three decisions"
    Larkspur's integration team recorded three ADRs in its first fortnight. ADR-001 chose webhooks plus a queue plus a 15-minute reconciliation pull for orders arriving from the shop. ADR-002 chose to create orders in the ERP through its API with a lookup-before-retry safeguard, because the create call was not idempotent. ADR-003 chose code-first services on the company's existing container platform rather than buying an integration platform, with a stated revisit trigger of five or more shop-to-ERP flows. Chapter {{ref ch:capstone}} follows these decisions to production.

## A Design Review Checklist

Before any integration design is approved, a reviewer should be able to answer the following questions from the design document. Use them to review your own work, and encourage others to use them on yours.

**Functional**

* Who is authoritative for each field?
* How are records matched across systems?
* How are deletes and renames handled?
* What is the freshness target, expressed as a number?
* What is the backfill plan for the initial load?

**Non-functional**

* What happens on timeout, duplicate, partial failure, and bad data?
* What is the request budget against each API?
* How is drift detected and repaired?
* Who is alerted, and what do they do?
* How are secrets rotated without downtime?

If a question cannot be answered, that is not a reason to stop; it is a reason to add the question to the open-items list with an owner and a date. Gates, which Chapter {{ref ch:journey}} introduces, are how a project makes sure open items are closed before they become incidents.

## Summary

An integration architect's job is to shrink the gap between the demo and the messy reality. They start from ten defaults, such as rate limits, partial failures, unsynchronized clocks, and rotating credentials, and design as if those were already happening. Three questions, where the truth lives, how fast change must travel, and what happens when it breaks, make most designs obvious.

The role covers a seven-phase lifecycle from discovery to retirement, and thirteen skill domains; being honest about which are your weak ones tells you what to learn next. Ten technology-independent ideas, from idempotency to ownership, reappear under different names on every platform. Six trade-offs, freshness against cost, coupling against simplicity, consistency against availability, build against buy, central against federated, and canonical against bounded, will be argued in every design review. Architecture decision records preserve what was chosen, why, and when to revisit it.

## Exercises

1. **Run the defaults on a real project.** Take an integration you work with and mark each of the ten defaults as *handled*, *partly handled*, or *ignored*. For each one marked *ignored*, write the symptom you would expect and how long it would take to notice.
2. **Rate yourself.** Score the thirteen skill domains from 1 to 5. Circle the three lowest and name one concrete action for each within the next month.
3. **Write an ADR.** Pick a past integration decision, perhaps one you disagreed with, and write it up in the template above. Add a "Revisit when" line that you would add today.
4. **Find the four numbers.** For an integration you know, estimate the current record count, the three-year count, the peak hourly change rate, and the acceptable staleness. If you cannot estimate one, whom would you ask?
