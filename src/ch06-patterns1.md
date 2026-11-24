# Patterns for Requests and Data Movement

A pattern is a named solution to a problem that keeps recurring. Architects use patterns the way carpenters use joints: not because they are clever, but because everyone who sees the name knows what is meant, what it is good for, and where it tends to fail. When a colleague says "we'll use a transactional outbox," you do not need a whiteboard. The vocabulary is the point.

This chapter and the next catalog forty-one integration patterns in six families, each with a diagram, a plain description of how it works, when to use it, and what goes wrong. They are not a menu from which you pick one; real integrations combine three or four. Chapter {{ref ch:patterns2}} closes with recipes that show typical combinations, and Chapter {{ref ch:decide}} gives you a method for choosing.

Here, we cover the first two families: **request-based patterns**, where one system calls another and waits, and **data-movement patterns**, where information is copied or exposed in bulk. Together they cover most of the volume in a typical enterprise.

!!! goals "In this chapter"
    * Read a pattern diagram and its three characteristics: initiator, timing, and coupling
    * Use four questions to narrow a requirement to a pattern family
    * Explain why hubs and event backbones exist, using the arithmetic of links
    * Describe eight request-based patterns and nine data-movement patterns, with when to use each and what to watch for
    * Recognize the patterns hidden inside the tools your organization already runs

## How to Read the Pattern Diagrams

Every pattern in this book has a diagram in the same visual language, so you can learn it once. The key is in {{ref fig:legend-conventions}}.

{{fig legend-conventions | The visual language of the diagrams. Arrow styles show how information travels; numbered circles give the order of steps; lettered red circles mark where a design usually fails.}}

Three characteristics describe every pattern, and they appear in the descriptions that follow. The **initiator** says who starts the exchange: the consumer *pulls*, the producer *pushes*, or both are possible. The **timing** says how long the exchange takes: *synchronous* (the caller waits), *asynchronous* (it does not), *batch* (data moves in bulk on a schedule), or *streaming* (data flows continuously). The **coupling** says how much one side must know about, and depend on, the other: *tight*, *moderate*, or *loose*. Tight coupling is simple and fragile; loose coupling is resilient and harder to follow.

## Start with the Family

With forty-one patterns, a newcomer needs a way in. {{ref fig:pattern-pattern-family-decision-tree}} shows four questions that narrow almost any requirement to a family.

{{fig pattern-pattern-family-decision-tree | Four questions narrow almost any requirement to a pattern family. Chapter 9 turns this into a fuller method.}}

The first question is whether the consumer needs an *answer right now* (a request-based pattern) or merely needs to *be told* when something happens (messaging and events). The second is whether the work is about *moving large amounts of data*, in which case data-movement patterns apply, or about individual business events. The third asks whether more than one system may change the same data, which sends you to the authority patterns of Chapter {{ref ch:patterns2}}. The fourth asks about special circumstances: partners, edge sites, legacy interfaces, or streaming computation. The tree is a starting point; the decision method in Chapter {{ref ch:decide}} refines it.

## Why Hubs and Backbones Exist

Before the patterns themselves, one piece of arithmetic explains an entire family of them. If every system talks directly to every other, the number of links grows with the square of the number of systems. {{ref fig:pattern-point-to-point-spaghetti-versus-hub}} shows the difference.

{{fig pattern-point-to-point-spaghetti-versus-hub | Links grow as N times (N minus 1), divided by 2, when every system talks to every other. A hub or event backbone makes the growth linear, at the price of a shared component to govern.}}

With five systems, full point-to-point connectivity needs 10 links. With ten systems it needs 45, and with twenty, 190. Each link has its own mapping, its own credentials, its own failure modes, and its own owner. Through a hub, twenty systems need 20 connections: one each. The price is a shared component that must be governed and kept available. This is the whole argument behind enterprise service buses, API gateways, and event backbones, and it is also the argument against them: a hub that becomes a bottleneck and a bureaucracy has traded one problem for another. Keep this arithmetic in mind as you read the patterns that follow.

## Request-Based Patterns

In request-based patterns, the caller asks and waits, or at least asks and receives an immediate acknowledgment. They are simple to reason about and tightly coupled in time: both sides must be available at the same moment.

### Point-to-Point API Call

{{fig pattern-point-to-point-api-call}}

One system calls another system's API and waits for the answer. The consumer sends a request (step 1) and the provider returns a response (step 2). This is the pattern everyone starts with, and for good reason: it is the simplest thing that can possibly work. When the shop asks the ERP whether a product is in stock before showing the page, that is a point-to-point call.

Use it for lookups, validations, and simple create-and-update flows between a handful of systems. The weaknesses are *temporal coupling* (both must be up), cascading failures (if the ERP is slow, the shop is slow), versioning pain when the provider changes, and the link explosion described above as the estate grows. Typical technologies are REST described with OpenAPI, gRPC, SOAP, and GraphQL. Whatever the technology, always set a timeout, and wrap the call in a circuit breaker, as Chapter {{ref ch:python}} shows.

### API Gateway or Facade

{{fig pattern-api-gateway-facade}}

Clients call one managed entry point, which authenticates them, enforces quotas, routes the call, and sometimes transforms it. The clients, whether web, mobile, or partners, send HTTPS requests to the gateway (step 1), which forwards them to the right back-end service (steps 2 and 3).

Use it to expose internal or partner APIs, to apply security and rate limiting in one place, and to gather usage analytics. The danger is that the gateway becomes a single choke point, and, more subtly, that *logic creeps into it*. A gateway that starts to contain business rules and data transformations becomes an unmaintainable miniature enterprise service bus. Keep its policies declarative: authentication, quotas, routing, and header rules. Products include Kong, Apigee, Azure API Management, Amazon API Gateway, MuleSoft's gateway offerings, WSO2, and Axway.

### API-Led Connectivity

{{fig pattern-api-led-connectivity}}

API-led connectivity, a term popularized by MuleSoft, layers APIs by role. *System APIs* unlock back-end systems once: one clean interface to the ERP, one to the CRM, one to the warehouse system. *Process APIs* compose them into business logic, such as "place an order," which touches all three. *Experience APIs* tailor the data to a channel, such as the web shop or the mobile app. In the diagram, two experience APIs call one process API (steps 1 and 2), which calls three system APIs (steps 3 to 5).

Use it in large estates with many consumers, where reuse and clear ownership per layer matter. Beware layers for their own sake: three tiers add latency, teams, and meetings, and a small estate rarely needs them. The pattern is a way of organizing reuse, not a rule that every call must pass through three hops.

### Orchestration

{{fig pattern-orchestration}}

A central coordinator calls the steps of a business process in order, owns its state, and decides what to do on failure. In the diagram, an orchestrator, a workflow engine, calls "reserve stock" (step 1), "charge payment" (step 2), and "create shipment" (step 3), and persists its state after each (step 4).

Use it for business processes with a clear sequence, timeouts, and human approval steps, especially where auditability matters. The risk is that the orchestrator becomes a "god service" that knows too much about everyone. It needs durable state, timeouts, and compensation logic for steps that must be undone. Typical technologies are workflow engines such as Camunda, Flowable, and Temporal, cloud workflow services such as AWS Step Functions and Azure Logic Apps, and the flow designers of integration platforms.

### Scatter-Gather

{{fig pattern-scatter-gather}}

The caller sends a request to an aggregator (step 1), which fans it out to several providers in parallel (steps 2 to 4) and merges the answers. It is the pattern behind a "customer 360" screen that gathers data from five systems, or a price comparison across suppliers.

The slowest provider sets the latency, so decide up front what happens on a timeout: return partial results, or fail? Decide also how to present a result that is missing a source. Integration platforms provide scatter-gather scopes, and the pattern is straightforward in code with asynchronous calls, provided you set a deadline.

### Adapter or Anti-Corruption Layer

{{fig pattern-adapter-anti-corruption-layer}}

An adapter sits in front of a legacy or awkward system and translates between its model and a clean one, so that the legacy model does not spread into modern services. Modern services speak the clean model to the adapter (step 1), which speaks the legacy model to the old system (step 2). The idea of an "anti-corruption layer" comes from domain-driven design: it protects the new world from being "corrupted" by the old.

Use it for mainframes, old ERPs, SOAP services, and partners with peculiar data models. Its cost is one more component to run, and its discipline is to remain a *dumb translator*. The moment business rules enter the adapter, you have hidden logic in the least visible place. In integration platforms the adapter is often called a system API.

### Strangler Fig

{{fig pattern-strangler-fig}}

The name, coined by Martin Fowler, comes from a vine that grows around a tree until the tree is gone. Clients call a routing proxy (step 1), which sends some functionality to the legacy monolith (step 2, being phased out) and some to new services (step 3, being phased in). Over time, more routes point at the new services, until the legacy system can be retired.

Use it to replace a legacy platform without a big-bang cutover. The hard part is data: while both systems are alive, they must stay synchronized, which brings in the patterns of Chapter {{ref ch:sync}}. Define the retirement criteria early, or the legacy system will live forever on the strength of "just one more route."

### Asynchronous Request-Reply

{{fig pattern-asynchronous-request-reply}}

Some operations take too long to hold a connection open: a bulk import, a report, a large export. In asynchronous request-reply, the client submits a job (step 1) and receives `202 Accepted` with a status URL, then polls that URL (step 2) or is called back when it finishes. Behind the scenes, the API enqueues the job (step 3), a worker takes it (step 4) and updates the status (step 5).

Use it for bulk operations and long-running tasks on vendor APIs; many platforms offer job APIs of exactly this form, such as Salesforce's Bulk API 2.0. Watch for job expiry (results that disappear after a day), idempotent submission (so a retried submit does not start a second job), sensible polling intervals, and what happens to a result nobody collects.

{{tbl req | Request-based patterns at a glance}}

| Pattern | Initiator | Timing | Coupling | Use it for |
|---|---|---|---|---|
| Point-to-point API call | Pull | Sync | Tight | Lookups and simple writes |
| API gateway | Pull | Sync | Tight | One managed front door |
| API-led connectivity | Pull | Sync | Moderate | Reuse in large estates |
| Orchestration | Pull | Sync | Tight | Sequenced business processes |
| Scatter-gather | Pull | Sync | Tight | Combining several sources |
| Adapter | Pull | Sync | Moderate | Isolating a legacy model |
| Strangler fig | Pull | Sync | Moderate | Gradual replacement |
| Asynchronous request-reply | Pull | Async | Moderate | Long-running operations |

## Data-Movement Patterns

Data-movement patterns copy or expose information in bulk rather than per transaction. They carry most of the volume in an enterprise, and most of its reconciliation pain, because "the same data in two places" inevitably drifts.

### Scheduled Batch ETL or ELT

{{fig pattern-scheduled-batch-etl-elt}}

On a schedule, a job extracts data from sources (steps 1 and 2), transforms it, and loads it into a target (step 3). In classic ETL the transformation happens before loading; in ELT, the data is loaded first and transformed inside the warehouse, which is the common approach on modern platforms because warehouses are good at it.

Use it for analytics feeds, reference data, and anything where hours of latency are acceptable. The traps are batch windows that grow until they collide, data that arrives late, reruns that double-count, and silent failures. A job that fails without raising an alarm is the integration equivalent of a stopped clock: give every batch a heartbeat alert that fires when it does *not* run. Tools include the data-integration suites (Informatica, Talend), cloud services (Azure Data Factory, AWS Glue), orchestrators (Airflow with dbt), and managed ELT tools (Fivetran, Airbyte).

### Managed File Transfer

{{fig pattern-managed-file-transfer}}

The source drops files on an SFTP server, an AS2 endpoint, or object storage (step 1), and a loader polls, fetches, validates, and ingests them (step 2). It is the oldest pattern here and still the best for large volumes, legacy systems, partners, and strict audit trails.

Files fail in characteristic ways: partial files picked up before the writer finished, encoding and delimiter surprises, schema drift, and duplicate delivery. Defend against them with a **manifest** (a small file listing expected names, sizes, and checksums), by having the writer upload under a temporary name and rename it atomically when done, and by archiving every file after processing. Products include Axway, IBM Sterling, GoAnywhere, Cleo, and the managed transfer services of the clouds.

### Polling with a Watermark

{{fig pattern-polling-with-a-watermark}}

The workhorse of SaaS integration. A scheduler repeatedly asks the source for "changes since the last watermark" (step 1), receives the changed rows (step 2), upserts them into the target (step 3), and saves the largest timestamp it saw as the new watermark (step 4).

It needs only outbound connections, which is a large part of its appeal. It is the right pattern whenever the source offers a modified-since filter. Its weaknesses are that it misses deletes, depends on honest timestamps, and can miss rows committed late. The standard defenses are an *overlap window* (re-read the last few minutes each time and let idempotent upserts absorb the repeats) and a periodic reconciliation. Chapter {{ref ch:python}} implements the pattern, and Chapter {{ref ch:sync}} examines its edge cases.

### Full Snapshot and Diff

{{fig pattern-full-snapshot-and-diff}}

When the source offers no way to ask what changed, read all of it. A diff engine pulls the complete source state (step 1) and the current target state (step 2), computes the difference, and applies it (step 3): create what is new, update what changed, delete what vanished.

It suits small and medium datasets, sources with no change tracking, reference data that should heal itself, and, importantly, **delete detection**, which many other patterns lack. Its cost grows with data size. Add a safety threshold, for example "refuse to delete more than 5 percent of the target in one run," so that a bad read from the source cannot wipe out the target.

### Change Data Capture

{{fig pattern-change-data-capture}}

Instead of asking the application what changed, read the database's transaction log, where every committed change is already recorded. A connector reads the log (step 1) and publishes each row change as an event (step 2) to a topic, from which targets consume (step 3).

Log-based change data capture, or CDC, is powerful because it does not touch the application, captures every change including deletes, and preserves order. It underpins replication, event feeds from legacy systems, near-real-time warehouse loads, and the outbox pattern of Chapter {{ref ch:patterns2}}. Its dangers are that it exposes the *physical* schema (renaming a column breaks consumers) and, with some databases, that an idle replication slot makes the source's disk fill up. Tools include Debezium, Qlik Replicate, Oracle GoldenGate, AWS DMS, and Striim.

### Read-Model Replication

{{fig pattern-read-model-replication}}

Keep a copy of data shaped for *reading*, such as a search index, a cache, or an operational data store, updated from events or CDC. The system of record emits changes (step 1), which a feed distributes (steps 2 and 3) to the read models.

Use it when search, dashboards, or APIs must stay fast and independent of the system of record. It is eventually consistent by nature, so decide how stale the copy may be. And design a *rebuild strategy* up front: sooner or later the read model will need to be regenerated from scratch, and "we can replay the topic" is a better answer than "we cannot."

### Reverse ETL

{{fig pattern-reverse-etl}}

Analytics produces valuable results, such as churn scores and customer segments, that are useless in a warehouse when the people who need them work in the CRM or the marketing tool. Reverse ETL queries the warehouse (step 1) and pushes the results into operational applications through their APIs (steps 2 and 3).

Watch for SaaS API rate limits, identity resolution (matching a warehouse customer to a CRM contact), loops with the original source, and above all *ownership*: who owns the field that the sync overwrites? Tools include Hightouch and Census, and custom jobs.

### Data Virtualization

{{fig pattern-data-virtualization}}

Query across sources at read time through a virtual layer, without copying the data first. The consumer sends SQL to the virtualization layer (step 1), which pushes parts of the query down to each source (steps 2 and 3) and combines the results.

It is attractive for exploration, for regulated data that cannot be copied, for rapid prototypes, and for "logical data warehouses." The performance is that of the slowest source, and production queries land on operational systems, so test with realistic loads. Security delegation, who is allowed to see what through the layer, needs deliberate design. Examples are Denodo, Trino and Starburst, and Dremio.

### Zero-Copy Data Sharing

{{fig pattern-zero-copy-data-sharing}}

A provider grants governed read access to a dataset (step 1), and consumers query it in place (steps 2 and 3) instead of receiving a copy. Because there is only one copy, there is nothing to reconcile.

Use it for data products shared across teams or companies on the same platform family. Its limits are platform affinity (it generally works only between users of the same technology), cross-region cost, and the semantics of revoking access. Governance still has to define who may see what. Examples include Snowflake Secure Data Sharing, Delta Sharing, and BigQuery Analytics Hub.

{{tbl data | Data-movement patterns at a glance}}

| Pattern | Initiator | Timing | Coupling | Use it for |
|---|---|---|---|---|
| Scheduled batch ETL or ELT | Pull | Batch | Loose | Analytics feeds, reference data |
| Managed file transfer | Push | Batch | Loose | Legacy systems, partners, large volumes |
| Polling with a watermark | Pull | Batch | Loose | SaaS sources with a modified-since filter |
| Full snapshot and diff | Pull | Batch | Loose | Small datasets, delete detection |
| Change data capture | Both | Stream | Loose | Replication, event feeds |
| Read-model replication | Push | Async | Loose | Search, caches, fast reads |
| Reverse ETL | Push | Batch | Loose | Analytics results back to applications |
| Data virtualization | Pull | Sync | Tight | Exploration, uncopyable data |
| Zero-copy data sharing | Pull | Sync | Loose | Cross-team data products |

!!! example "Larkspur Outdoor: which patterns were already there"
    Larkspur's nightly CSV is a *managed file transfer* with a *scheduled batch* loader, and the manual fix-up of rejected rows is a human acting as the *dead letter queue* (Chapter {{ref ch:patterns2}}). Its stock check is a *point-to-point API call*. Naming the patterns already in use made the discussion concrete: the team was not proposing to "add integration"; it was proposing to replace one batch pattern with polling and webhooks, and to keep the file as the safety net.

## Summary

A pattern is a named, reusable solution; its value lies in shared vocabulary. Three characteristics describe each: who initiates (pull or push), the timing (synchronous, asynchronous, batch, or streaming), and the coupling (tight, moderate, or loose). Four questions narrow a requirement to a family, and the arithmetic of links, N times N minus 1 over 2, explains why hubs and backbones exist.

Request-based patterns are simple but tightly coupled in time: the point-to-point call, the API gateway, API-led layers, orchestration, scatter-gather, the adapter, the strangler fig for gradual replacement, and asynchronous request-reply for long operations. Data-movement patterns carry the volume: scheduled batch, managed file transfer, polling with a watermark, snapshot and diff, change data capture, read-model replication, reverse ETL, virtualization, and zero-copy sharing. Each trades latency and effort differently, and each has a characteristic way of failing.

## Exercises

1. **Name what you run.** List five data flows in your organization and name the pattern each uses. Which uses a pattern that does not match its freshness requirement?
2. **Count your links.** Count the systems in one business domain and the direct integrations between them. Compare with the N times (N minus 1) over 2 maximum. How close are you to the "spaghetti" limit?
3. **Choose a family.** For each requirement, name the pattern family and one specific pattern: (a) show live stock levels on the product page; (b) load yesterday's sales into the warehouse; (c) replace the legacy billing system without a big bang; (d) import 2 million customer records overnight.
4. **Design a safety threshold.** For a snapshot-and-diff job, write the rule that would stop it from deleting too much. What percentage would you choose, and why?
