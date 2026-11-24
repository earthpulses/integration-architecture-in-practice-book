# Patterns for Messages, Routing, and Authority

The previous chapter covered patterns in which a caller asks and waits, and patterns that move data in bulk. This chapter covers the rest: the patterns of *asynchronous messaging*, where producers and consumers are decoupled in time; the *routing and transformation* toolbox that every integration platform provides; the patterns of *authority, master data, and identity*, which decide who owns which truth; and a final family of *specialized* patterns for boundaries such as partners, edge sites, legacy screens, and AI agents.

Messaging is where integrations gain resilience and fan-out, and also where most of the subtle bugs live. Messages arrive twice. They arrive out of order. They arrive when nobody is listening, or in such numbers that someone drowns. The patterns in this chapter are, to a large extent, the accumulated answers to those problems, and several of them (the transactional outbox, the idempotent receiver, the dead letter queue) will recur in every chapter that follows.

!!! goals "In this chapter"
    * Describe thirteen messaging and event patterns, including the three that make asynchronous systems safe: the outbox, the idempotent receiver, and the dead letter queue
    * Use the routing and transformation toolbox, and judge when a hub is worth its cost
    * Choose among bidirectional sync, master data management, and identity provisioning
    * Recognize the specialized patterns for agents, partners, legacy screens, streaming computation, and AI tools
    * Combine patterns into recipes, and spot the anti-patterns that undo them
    * Apply the authority split, the most valuable simplification in this book

## Messaging and Event Patterns

In messaging patterns, producers and consumers are decoupled in time. You gain resilience and fan-out. You pay with ordering problems, duplicates, and the need to trace flows across components that no longer call each other directly.

### Message Queue

{{fig pattern-message-queue}}

Producers put messages on a queue, and each message is processed by exactly one of several competing workers. The producer sends (step 1); each worker receives a message and acknowledges it when finished (steps 2 and 3). If a worker crashes before acknowledging, the queue offers the message to another worker.

That last sentence contains the most important property of queues: **delivery is at least once**. A message may be delivered more than once, because the queue cannot know whether the worker finished its work before it died. Consumers must therefore be idempotent, which is the subject of a pattern later in this chapter.

Use queues to distribute tasks, to level load, and to protect a slow downstream system from bursts: the shop's Black Friday spike goes into the queue, and the ERP's workers drain it at the pace the ERP can sustain. Classic queues keep no history and cannot be replayed, and ordering is limited. Technologies include IBM MQ, RabbitMQ, ActiveMQ, Amazon SQS, Azure Service Bus, and, in recent versions, Kafka's share groups, which add queue semantics to a log.

### Publish and Subscribe

{{fig pattern-publish-subscribe}}

A publisher emits an event to a topic (step 1), and every interested subscriber receives its own copy (steps 2 to 4). The publisher does not know how many subscribers exist or who they are. The shop publishes "order placed" once; the ERP, the analytics platform, and the fraud check each receive it.

Use it to broadcast business events to an unknown or changing set of consumers. The cost is invisibility: when anyone may subscribe, it becomes hard to answer "who depends on this event?" before you change it. Keep an **event catalog** listing every topic, its owner, its schema, and its known subscribers. Expect duplicates and out-of-order delivery as normal conditions. Technologies include Amazon SNS and EventBridge, Google Pub/Sub, Azure Event Grid and Service Bus topics, RabbitMQ exchanges, and Solace.

### Event-Carried State Transfer

{{fig pattern-event-carried-state-transfer}}

There are two ways to design the content of an event. A *notification* event says only that something happened ("customer 42 changed") and forces consumers to call back for the details. An *event-carried state transfer* event carries the full new state of the entity, so consumers keep a local copy and never call back. The customer service publishes the full state to a compacted topic (step 1), and the billing and support services each maintain their own copy (steps 2 and 3).

The pattern reduces runtime coupling, because billing no longer needs the customer service to be up in order to work. It also makes it easy to bootstrap a new consumer: read the compacted topic from the beginning and you have the current state of every customer. The costs are that the event's schema becomes a public contract that is hard to change, payloads are larger, and a consumer that misses events can drift from the truth. Pair it with a reconciliation.

### Event Streaming

{{fig pattern-event-streaming}}

Events are appended to a partitioned, retained log. Producers write to it (steps 1 and 2); consumer groups read from it at their own pace and can *replay* by moving their position (steps 3 and 4). Unlike a queue, reading does not remove anything; the log is a record, and each group keeps its own bookmark.

Choose streaming for high volume, many independent consumers, the need to replay after a bug, stream processing, and change-data-capture backbones. The costs are real: operational weight, the need for schema discipline, ordering only within a partition, and the need to watch **consumer lag**, the distance between the newest event and the consumer's position. Chapters {{ref ch:kafka1}} to {{ref ch:kafkaio}} are devoted to the most widely used platform of this kind, Apache Kafka. Alternatives include Redpanda, Apache Pulsar, Azure Event Hubs, and Amazon Kinesis.

### Request-Reply over Messaging

{{fig pattern-request-reply-over-messaging}}

Sometimes you need a conversation, not just a notification, but the systems share a broker rather than an HTTP path. In request-reply over messaging, the requester sends a message to a request queue with a *correlation ID* (step 1). The responder takes it (step 2), does its work, and sends a reply with the same ID to a reply queue (step 3), where the requester matches it (step 4).

The pattern suits legacy message-queue estates and decoupled remote calls. Watch for timeouts (how long does the requester wait?), orphaned replies for requesters that have gone away, and the temptation to rebuild HTTP on top of a broker. If the requester needs an answer within a second, an API is usually simpler.

### Webhook

{{fig pattern-webhook}}

The source sends an HTTP POST to your endpoint when something changes (step 1). A well-built receiver does only three things on the request path: it verifies the signature, persists the event by putting it on a queue (step 2), and acknowledges. A worker takes events from the queue and processes them later (step 3). The rule is: *answer in milliseconds; process later*.

Webhooks give near-real-time notification without polling. They require a publicly reachable endpoint, which brings the security work of signature verification and replay protection (Chapter {{ref ch:security}}), and the source typically retries, so you must deduplicate. Most importantly, **if you were down when the event was sent, you may never receive it**; many providers do not replay. The standard remedy is to pair the webhook with a slower *reconciliation pull*, so that the fast path provides speed and the slow path repairs whatever the fast path missed. Chapter {{ref ch:capstone}} builds exactly this combination.

### Event Mesh

{{fig pattern-event-mesh}}

An event mesh is a network of interconnected brokers, spread across sites and clouds, that routes events dynamically to wherever subscribers exist. A publisher at one site connects to its local broker, and the mesh carries the event across to subscribers at other sites and clouds (steps 1 to 4).

It fits retail stores, factories, and multi-cloud estates that exchange events with each other and with the core. The tooling matters less than the discipline: a clear topic taxonomy and governance are decisive, and latency and cost across the links need watching. Commercial meshes such as Solace and SAP Advanced Event Mesh pursue this goal, as do Kafka's MirrorMaker 2 and cluster-linking features.

### Choreography

{{fig pattern-choreography}}

In choreography, services react to each other's events with no central coordinator. The order service publishes "order placed" (step 1); payment and inventory services each react (steps 2 and 3); payment publishes "payment taken" (step 4), which others react to in turn. Each team owns its own reaction.

It suits loosely coupled domains where autonomy matters. The cost is that *the end-to-end flow is no longer written down anywhere*. To understand what happens when an order is placed, you must read the code of five services. Compensate with correlation IDs on every event, distributed tracing (Chapter {{ref ch:reliability}}), and an event catalog that documents the flow. If the process is long, has deadlines, or needs a human step, an orchestrator is usually clearer.

### Saga

{{fig pattern-saga}}

Transactions that span several systems cannot rely on a database to roll everything back. A **saga**, a term from a 1987 paper by Hector Garcia-Molina and Kenneth Salem, replaces the one big transaction with a chain of local transactions, each with a *compensating action* that undoes it. In the diagram, the saga creates the order, reserves stock, charges payment, and ships (steps 1 to 3). If shipping fails, the saga compensates in reverse: it refunds the payment, releases the stock, and cancels the order (steps 4 to 6).

The crucial insight is that a compensation is *business logic*, not a technical rollback. You cannot "un-send" an email or "un-ship" a parcel; you can send an apology or arrange a return. Design every step to be idempotent, expect partial failure, and decide what each compensation means to the business. Sagas can be orchestrated by a workflow engine (Temporal, Step Functions, Camunda) or choreographed through events.

### Transactional Outbox

{{fig pattern-transactional-outbox}}

Consider a service that must update its database *and* publish an event. If it writes the database and then publishes, a crash in between leaves the data changed and the event never sent. If it publishes first, a crash leaves an event for a change that never happened. This is the **dual-write problem**, and it cannot be solved by ordering the two steps carefully, because there is no transaction that spans a database and a broker.

The outbox pattern removes the problem by making only one write. The service writes the state change *and* the event to an outbox table in the same database transaction (step 1). A separate relay, either a poller or a change-data-capture connector, reads the outbox (step 2) and publishes to the broker (step 3). Either both rows are committed or neither is, and the relay takes care of delivery.

Delivery from the relay is at least once, because the relay may publish and then crash before marking the row as sent, so consumers must deduplicate. Watch for relay operations, outbox cleanup, and ordering per aggregate. Chapter {{ref ch:time}} walks through exactly this sequence, and Appendix {{ref app:codelab}} includes a tested implementation that demonstrates the duplicate and its fix. Debezium provides an outbox event router; polling relays are simple to write.

### Claim Check

{{fig pattern-claim-check}}

Message brokers limit message size, and moving large payloads through them is wasteful. In a claim check, the producer stores the large payload in blob storage (step 1) and sends a small message containing only a reference (step 2). The consumer takes the message (step 3) and fetches the payload by reference (step 4), as one hands in a coat and receives a ticket.

Use it for documents, images, and large JSON. Take care of the stored payload's lifecycle (who deletes it, and when?), of access control on the reference (anyone holding the reference should not automatically get the data), and of consistency between the message and the blob: store the payload *before* sending the message, never after.

### Retry and Dead Letter Queue

{{fig pattern-retry-and-dead-letter-queue}}

Failures come in two kinds. *Transient* failures, such as a timeout or a brief outage, succeed if tried again. *Permanent* failures, such as a malformed message or a business rule violation, will fail forever. A retry and dead letter design treats them differently. The consumer processes a message from the main queue (steps 1 and 2); on success, it writes to the target (step 3). On a transient failure it sends the message to a retry queue with a delay (steps 4 and 5), which returns it to the main queue later. On a permanent failure, or after too many attempts, it parks the message with context in a **dead letter queue** (step 6) for a human.

Every asynchronous consumer in production needs this. And a dead letter queue nobody watches is data loss with extra steps: assign an owner, alert on its depth, and build a tool to inspect and replay its messages once the cause is fixed. Brokers provide native dead letter queues; Kafka implementations use retry topics and connector error handling (Chapter {{ref ch:kafka2}}).

### Idempotent Receiver

{{fig pattern-idempotent-receiver}}

Since queues, webhooks, retries, and streams all deliver at least once, a receiver that processes the same message twice will do the work twice unless it is built not to. An idempotent receiver records the identifier of each message it processes. When a message arrives (step 1), the receiver checks the ledger (step 2): "seen this ID?" If not, it applies the business write once (step 3) and records the ID.

Two details matter. The ledger entry and the business write must commit *in the same transaction*; otherwise a crash between them re-creates the duplicate. And the ledger must remember IDs for longer than the longest retry window, or an old duplicate slips through. Where possible, prefer *natural* idempotency (an upsert by business key) to a ledger, because it needs no extra state.

{{tbl msg | Messaging and event patterns at a glance}}

| Pattern | Initiator | Timing | Coupling | Use it for |
|---|---|---|---|---|
| Message queue | Push | Async | Loose | Task distribution, load leveling |
| Publish and subscribe | Push | Async | Loose | Broadcasting events |
| Event-carried state transfer | Push | Async | Loose | Local copies without callbacks |
| Event streaming | Both | Stream | Loose | High volume, replay, many consumers |
| Request-reply over messaging | Push | Async | Moderate | Decoupled remote calls |
| Webhook | Push | Async | Loose | SaaS notifications |
| Event mesh | Push | Async | Loose | Multi-site and multi-cloud events |
| Choreography | Push | Async | Loose | Autonomous reactions |
| Saga | Both | Async | Moderate | Multi-system business transactions |
| Transactional outbox | Push | Async | Loose | State change plus event, atomically |
| Claim check | Push | Async | Loose | Large payloads |
| Retry and dead letter queue | Both | Async | Loose | Every asynchronous consumer |
| Idempotent receiver | Both | Async | Loose | Every at-least-once channel |

## Routing and Transformation

Every integration platform provides a set of building blocks for shaping and steering messages. They were cataloged in the 2003 book *Enterprise Integration Patterns* by Gregor Hohpe and Bobby Woolf, and their names form the shared vocabulary of the field. {{ref fig:pattern-content-based-router}} shows six of the most useful.

{{figgrid pattern-content-based-router pattern-splitter pattern-aggregator pattern-message-translator pattern-content-enricher pattern-message-filter | Six routing and transformation building blocks.}}

A **content-based router** inspects a message and sends it to one of several destinations: orders for Europe to one queue, orders for North America to another. A **splitter** breaks one message into many, for example a file of 10,000 orders into 10,000 order messages. An **aggregator** does the reverse, collecting related messages and combining them, such as gathering all the lines of an order. A **message translator** converts one format into another: an XML purchase order into the JSON the ERP expects. A **content enricher** adds data the message lacks by looking it up elsewhere, for instance adding a customer's region from a reference table. A **message filter** discards messages that do not meet a condition, such as ignoring test orders.

These blocks appear, under different names, in Apache Camel, MuleSoft, Boomi, Spring Integration, IBM App Connect, and every other platform. The danger is hidden complexity: an estate with a hundred tiny flows, each combining three of these blocks, can become impossible to understand. Name every flow, document its purpose, and test it.

### Hub-and-Spoke and the Canonical Model

{{fig pattern-hub-and-spoke-esb-with-canonical-model}}

In a hub-and-spoke design, every system connects once to a central hub, which translates between each system's format and a shared **canonical model** and routes messages. The ERP and CRM send to the hub (steps 1 and 2), and the hub forwards to the warehouse system and the web shop (steps 3 and 4). With a canonical model, adding a new system requires one new translation, to and from the canonical form, instead of one translation per existing system.

This is the classic enterprise service bus, and it delivered on its promise in estates with many systems and few changes. It also gave rise to its own failure modes: the hub becomes a bottleneck and a governance bureaucracy, and a canonical model for *everything* tends to become a lowest-common-denominator committee product. A pragmatic modern approach is to adopt a canonical model only for the few entities that are truly shared and stable, such as customer and product, and to leave everything else bounded to its own domain. Technologies include MuleSoft, IBM App Connect, TIBCO BusinessWorks, webMethods, WSO2, and Apache Camel.

## Authority, Master Data, and Identity

A different family of patterns concerns who owns which truth, and how copies of it stay honest.

### Bidirectional Sync with Per-Field Authority

{{fig pattern-bidirectional-sync-with-per-field-authority}}

Sometimes two systems legitimately both change the same entity: a ticket in a service desk and a matching issue in a project tool, each edited by different teams who will not give up their own application. A synchronization service watches both sides (steps 1 and 4) and applies changes each way (steps 2 and 3), under an **authority map** that says, field by field, which side wins.

Bidirectional synchronization is the hardest mode to get right. The failure modes are *echo loops* (a change written to B triggers a change event, which is written back to A, forever), ordering problems, and concurrent edits. The defenses are a loop guard (ignore changes made by the integration's own user, or stamp changes with their origin), a per-record lock, and explicit conflict rules. Better still, apply the authority split described at the end of this chapter, which usually turns one bidirectional flow into two simple one-way flows. Chapter {{ref ch:sync}} treats the topic in depth.

### Master Data Management Hub

{{fig pattern-master-data-management-hub}}

When the same customer, product, or supplier exists in a dozen systems with different spellings, identifiers, and levels of completeness, someone must decide which record is "the customer." A **master data management** hub receives records from each source (steps 1 to 3), *matches* those that describe the same real-world entity, *merges* them into a golden record using survivorship rules, and publishes the result to consumers (step 4). Four classic styles differ in how much authority the hub takes: *registry* (the hub only holds an index of which records match), *consolidation* (the hub builds the golden record for reporting), *coexistence* (the golden record is synchronized back to the sources), and *centralized* (the hub is the only place the entity is edited).

Match rules and survivorship, such as "the CRM's phone number wins unless it is older than the billing system's," are *business* decisions, not technical ones. Without data stewards who own and tune them, the hub decays. Products include Informatica MDM, Boomi DataHub, Reltio, Profisee, Stibo for products, and SAP MDG.

### Identity Provisioning

{{fig pattern-identity-provisioning}}

The employee lifecycle is an integration problem in disguise. The HR system is the source of truth for who works at the company. When someone joins, changes role, or leaves (the "joiner, mover, leaver" events, step 1), an identity provider such as Entra ID or Okta provisions, updates, or removes accounts and roles in each application (steps 2 and 3), typically through the SCIM standard.

The hardest problems are not technical: rehires who return with new identifiers, leavers whose access must end within hours rather than days, attribute mappings that differ per application, and approval workflows for sensitive roles. Products include Workday and SuccessFactors as sources, Entra ID and Okta as providers, and SailPoint for governance.

## Specialized and Boundary Patterns

The last family covers boundaries and special circumstances.

### Stateful Stream Processing

{{fig pattern-stateful-stream-processing}}

Some questions can be answered only by computing continuously over a stream: "how many failed payments has this card had in the last ten minutes?" A stream processor reads input topics (step 1), filters, joins, and aggregates over *windows* of time, keeps state between events (step 3), and emits derived events (step 2).

Use it for real-time aggregates, fraud signals, and enrichment of events with reference data. Pitfalls include late and out-of-order events, the size of the state, recovery time after a crash, and the boundaries within which processing is exactly once. Tools include Kafka Streams, Apache Flink, ksqlDB, and Spark Structured Streaming.

### Server Push to Clients

{{fig pattern-server-push-to-clients}}

Browsers and mobile apps that must show live updates can poll, or the server can keep a connection open and push. A gateway holds Server-Sent Events or WebSocket connections to clients (steps 2 and 3) and relays events from the broker behind it (step 1). Watch for reconnect and resume (clients should send the last event ID they saw), fan-out at scale, and proxies that close idle connections. Services include Azure SignalR and AWS AppSync subscriptions, along with mobile push notification systems.

### Hybrid Agent

{{fig pattern-hybrid-agent}}

Chapter {{ref ch:topologies}} introduced the agent topology; here it appears as a pattern. A lightweight agent inside the private network reaches the local systems (step 1), and holds an outbound TLS connection to a cloud control plane (step 2), from which it reaches SaaS applications (step 3). No inbound ports are needed. Watch for agent patching, high availability, and the question of where the logic actually executes.

### B2B and EDI Exchange

{{fig pattern-b2b-edi-exchange}}

Retail, manufacturing, logistics, and healthcare supply chains exchange standard documents, such as purchase orders and invoices in the X12 or EDIFACT formats, over AS2, SFTP, or a value-added network. A partner sends a purchase order (step 1) through the transport (step 2); an EDI translator maps it to an ERP document such as an IDoc (step 3) and returns a functional acknowledgment, such as an X12 997 (step 4), to confirm receipt. The "standard" has partner-specific variations, so onboarding each partner is real work. Products include Boomi B2B, IBM Sterling B2B Integrator, OpenText, SPS Commerce, and Cleo.

### UI Automation as a Last Resort

{{fig pattern-ui-automation-last-resort}}

A bot drives a legacy application's screens because the application has no API (step 1), and feeds the result to a target through an API or a file (step 2). Robotic process automation tools such as UiPath, Power Automate Desktop, and Blue Prism, or browser automation libraries like Playwright, do this. It is a legitimate bridge while a proper integration is built, and a poor foundation for anything else: it breaks when the screen changes, has no contract, and is hard to monitor. Treat it as technical debt with an exit date.

### AI Agent Access via Tools

{{fig pattern-ai-agent-access-via-tools}}

An AI agent, a program built on a large language model that decides which actions to take, can call tools exposed to it, often through the Model Context Protocol (MCP) or through function calling. An MCP server wraps your existing APIs (steps 2 and 3) with a catalog of tools and scoped credentials, and the agent discovers and calls them (step 1). Natural-language access to a CRM, a service desk, or a data catalog becomes possible without a new integration for each.

The risks are new and serious. *Prompt injection* means text returned by a tool, such as a customer's note, can try to instruct the agent. Over-broad scopes let a mistaken agent do real damage. Non-idempotent writes may be repeated. Auditing is easily forgotten. Apply the same discipline as to any integration, and more: scope credentials to the minimum, require human approval for writes, log every call, and treat tool output as untrusted input (Chapter {{ref ch:security}}).

## Pattern Recipes: How Real Integrations Combine Them

Real integrations use three or four patterns at once. {{ref tbl:recipes}} lists recipes that recur so often they deserve names.

{{tbl recipes | Common recipes and why they work}}

| Situation | Recipe | Why it works |
|---|---|---|
| Reliable SaaS notifications | Webhook, queue, idempotent receiver, polling reconciliation | The fast path gives speed; the slow path repairs what the fast path missed |
| Legacy database to analytics | Change data capture, stream, sink, snapshot diff | Continuous freshness with a periodic audit |
| Atomic state change plus event | Outbox, CDC relay, schema registry | No dual-write drift |
| Governed API program | Gateway, API-led layers, OAuth 2.0, asynchronous request-reply for bulk | Central policy, reusable blocks, safe long-running calls |
| On premises to cloud platform | Outbound agent, queue buffer, circuit breaker | No inbound ports; survives cloud outages |
| Partner supply chain | EDI over managed file transfer, canonical order model, acknowledgments | Standard exchange with partner variations isolated at the edge |
| Replacing a monolith | Strangler fig, anti-corruption layer, CDC sync during transition | Gradual and reversible migration |
| Operational analytics | ELT, reverse ETL, governed lineage | Insights flow back into the tools people use |

## Anti-Patterns to Challenge

Anti-patterns are designs that look reasonable and fail in predictable ways. Challenge them when you meet them in design reviews, including your own.

{{tbl anti | Anti-patterns, why they hurt, and what to do instead}}

| Anti-pattern | Why it hurts | Better |
|---|---|---|
| Shared database integration (two applications read and write the same tables) | Hidden coupling; a schema change breaks everyone; no clear owner | An API or events; CDC if you must read tables |
| Distributed monolith (long chains of synchronous calls) | Availability multiplies down; latency stacks | Asynchronous events, caching, fewer hops |
| Dual write (write the database, then publish, and hope both succeed) | State and events diverge | Outbox or CDC |
| God ESB (all logic centralized in the bus) | A bottleneck team; untestable flows | Smart endpoints, dumb pipes; declarative policies in gateways |
| Canonical model for everything | Committees; lowest-common-denominator data | A canonical model for a few shared entities; bounded contexts elsewhere |
| Unbounded retries | Retry storms hammer a recovering system | Backoff with jitter, caps, circuit breakers |
| Silent drops (errors swallowed; zero rows treated as success) | Quiet data loss | Run summaries, reject counts, heartbeat alerts |
| Integration by spreadsheet or inbox rule | Unowned shadow integrations | Inventory shadow flows; move critical ones to a governed platform |
| Screen scraping as the plan | Brittle and unsupported | Treat it as a bridge with an exit date |

## The Authority Split: The Most Valuable Simplification

Conflict resolution is the most expensive machinery in integration: timestamps, version vectors, locks, merge rules, and human review queues. The most valuable simplification in this book is to design it *out*.

When each field has exactly one owner, you do not need conflict resolution at all. You need only a clean one-way flow per field. Two one-way flows beat one bidirectional merge in almost every case, because a one-way flow has a source of truth, a direction, and no possibility of an echo. The authority matrix of Chapter {{ref ch:discovery}} is the tool that finds the split.

{{tbl authsplit | The authority split applied to a ticketing integration}}

| Entity or field | Authoritative system | Direction | Conflict rule needed? |
|---|---|---|---|
| Business object definition | Governance catalog | Catalog to process tool | No |
| Process steps and documentation | Process tool | Process tool to catalog | No |
| Incident status | Service desk | Service desk to catalog | No |
| Issue description | Catalog | Catalog to service desk | No |
| Comments (both sides can write) | Neither | Both | Yes: append-only, tagged with origin |

Notice that the table needs a conflict rule in only one row, and that row has a simple rule: comments are *appended*, never edited, and each carries a tag naming where it originated. A design review that finds a bidirectional merge should ask first: "can we split the authority instead?" The answer is yes more often than people expect, and each time it removes a whole class of bugs from the project.

## Summary

Messaging patterns trade the simplicity of a call for resilience and fan-out. Queues share work and deliver at least once; publish and subscribe broadcasts; event-carried state transfer replaces callbacks with local copies; streaming keeps a replayable log. The webhook gives speed and must be paired with reconciliation. Choreography and sagas coordinate business processes without a global transaction, and the outbox, the idempotent receiver, and the dead letter queue make asynchronous systems safe.

The routing toolbox, router, splitter, aggregator, translator, enricher, and filter, provides the building blocks of every platform, and hubs trade link growth for governance cost. Authority patterns decide who owns which truth, and the specialized patterns cover agents, partners, stream computation, legacy screens, and AI tools. Real integrations combine patterns into recipes, and the authority split, one owner per field and one-way flows, is the most effective way of avoiding conflict machinery altogether.

## Exercises

1. **Find the dual write.** Look in a service you know for a place where code writes to a database and then publishes a message, or calls another service, in two separate steps. What happens if the process crashes between them? Sketch the outbox version.
2. **Design the dead letter process.** For an asynchronous consumer you know, write down: what counts as a permanent failure, who owns the dead letter queue, what alert fires, and how a message is replayed.
3. **Split the authority.** Take a bidirectional integration you know and build its authority matrix. How many fields truly need both directions? Could the rest become one-way flows?
4. **Pick a recipe.** Choose three requirements from your own work and match each to one of the recipes in {{ref tbl:recipes}}. Where would you adapt it?
