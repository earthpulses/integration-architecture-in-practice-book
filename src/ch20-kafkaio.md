# Kafka as an Integration Backbone

Chapters {{ref ch:kafka1}} and {{ref ch:kafka2}} explained how Kafka works. This chapter answers the question an architect actually faces: *given a source system and a target system, how should each connect to Kafka?* The answer is never "use Kafka." A design is a *pair*: which way in for this source, and which way out for that target. A CRM-to-warehouse flow is change data capture in and a warehouse sink out. A SaaS-webhook-to-ERP flow is an HTTP gateway in and a consumer application out. Naming both ends on the diagram is the first sign of a real design.

There are many ways in and many ways out, and the right choice depends mainly on one question, *who initiates?*, because that decides where retries, backpressure, and failures live. This chapter maps them all, then covers how consumers can share a stream, how clusters can be combined across sites, how integration platforms plug in, and how to choose between Kafka and its alternatives.

!!! goals "In this chapter"
    * Explain the push-and-pull asymmetry of Kafka and what it means for failure handling
    * Choose among twelve ways of getting data into Kafka and eleven ways of getting it out
    * Apply fan-out, competing, broadcast, replay, and bootstrap consumption strategies
    * Compare active-passive, active-active, aggregate, and stretch-cluster topologies
    * Describe how integration platforms consume from Kafka, and what to check in their connectors
    * Compare Kafka with its alternatives and pick a way in and out for a given flow

## Settling the Push-versus-Pull Confusion

People say "Kafka pushes to my application" or "my application pulls from Kafka" interchangeably, and the confusion leads to wrong designs. The facts are simple. Kafka is **push on the write side and pull on the read side**. Producers push records to brokers. Consumers *pull* records from brokers with long-polling fetch requests; the broker never pushes to a consumer. Anything that looks like "Kafka pushes to my REST API" is a *separate process*, a sink connector or a bridge, that pulls from Kafka and then pushes to the target. {{ref fig:kafkaio-who-initiates-in-kafka-integrations}} shows who opens each connection.

{{fig kafkaio-who-initiates-in-kafka-integrations | Read the arrows as "who opens the request". The connectors are the bridge between systems that cannot speak the Kafka protocol.}}

{{tbl initiators | Who initiates, and what that means for design}}

| Path | Who initiates | Direction | Consequence for design |
|---|---|---|---|
| Producer to broker | The producer (push) | In | The producer owns retries, batching, and ordering via the key; failures surface as delivery errors |
| Broker to consumer | The consumer (pull) | Out | The consumer controls the pace, so backpressure is natural: slow down or pause |
| Source connector to an external system | The connector (pull, or tailing a log) | In | Polling frequency and source load are yours to tune; CDC avoids query load |
| Source system to an HTTP gateway | The source (push) | In | You need an endpoint that verifies, produces, and acknowledges quickly |
| Sink connector to an external target | The connector (pulls from Kafka, pushes to the target) | Out | The target's rate limits and errors become your problem: retries, dead letters, idempotent writes |
| A consumer pushing to a REST API | Your code (pull, then push) | Out | You must pause consumption when the target throttles |

The practical lesson is in the last row. Because the consumer controls the pace, a consumer that writes to a rate-limited API can simply *stop pulling* when the API says 429, and the records wait safely in the log. Kafka's pull model is what gives it natural backpressure, and it is the reason a Kafka-based integration degrades gracefully when its target fails.

## Ways In

{{ref fig:kafkaio-ways-into-kafka}} shows six of the common entrances, and {{ref tbl:waysin}} lists twelve in all. Many estates use four or five of them at once.

{{fig kafkaio-ways-into-kafka | Six common entrances. Many estates use four or five of them at once.}}

{{tbl waysin | Ways of getting data into Kafka}}

| # | Way in | Initiator | Best for | Watch out for |
|---|---|---|---|---|
| 1 | Native producer client (Java, Python, Go, .NET, JavaScript, C/C++) | Your application pushes | New services; lowest latency; full control of keys, headers, schemas | Delivery callbacks and flush; idempotence defaults differ by client; the dual-write problem |
| 2 | Connect source: log-based CDC (Debezium) | The connector tails the database log | Legacy databases; no application change; complete history | Replication slots filling disks; schema changes; the physical schema becomes your public contract |
| 3 | Connect source: query-based (JDBC source) | The connector polls with `SELECT` | Simple tables with reliable update columns; quick wins | Misses deletes and same-timestamp rows; adds query load; latency equals the poll interval |
| 4 | REST proxy or HTTP ingest gateway | The sender pushes over HTTP | Applications and SaaS webhooks that cannot use a Kafka client | Per-request overhead; verify signatures; answer 429 or 503 when Kafka is slow instead of buffering without bound |
| 5 | File ingestion connectors (spool directory, SFTP, object storage) | The connector polls folders | Legacy batch extracts; partner files | Partial files; duplicates; large files; use manifests |
| 6 | MQ or JMS bridge (IBM MQ, ActiveMQ, TIBCO EMS) | The connector subscribes | Migrating from queues; mainframe offload | Ordering and transaction semantics differ; header mapping; poison messages |
| 7 | MQTT or IoT bridge | The bridge subscribes | Devices; factory and fleet telemetry | QoS mapping; topic-name mapping; device identity; bursts |
| 8 | SaaS event feeds through connectors or an integration platform | The platform subscribes or polls, then produces | SaaS sources without a Kafka-native path | Vendor API limits; replay identifiers; vendor-side retention |
| 9 | Stream processor output (Kafka Streams, Flink, ksqlDB) | The processor pushes derived topics | Enriched, filtered, aggregated streams | State size and recovery; late data; exactly-once boundaries |
| 10 | Outbox relay (Debezium outbox router or a polling relay) | The relay reads the outbox table | Atomic "state change plus event" from a service with its own database | Cleaning the outbox; ordering per aggregate |
| 11 | Cluster replication (MirrorMaker 2, cluster linking) | The replicator pulls, then pushes | Disaster recovery; geo-replication; edge to core | Offset translation; topic prefixes; loops in active-active |
| 12 | Bulk loaders (Spark or Flink batch jobs) | The job pushes | Backfills and migrations | Throttle so live traffic is not starved; keep keys consistent with live data |

Three of these merit extra advice.

**HTTP ingest gateways** (row 4) are how SaaS webhooks get into Kafka. The gateway must do everything the webhook receiver of Chapter {{ref ch:time}} does: verify the signature, produce to Kafka, and answer quickly. Crucially, when Kafka is slow or the producer's buffer is full, answer `429` or `503` so that the sender retries, instead of accepting the request and buffering unboundedly in memory. A REST proxy call looks like this, with the details depending on the product and version:

```bash
curl -X POST https://rest-proxy.example.com:8082/topics/orders.events.v1 \
  -H "Content-Type: application/vnd.kafka.json.v2+json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"records":[{"key":"order-42",
        "value":{"id":"evt-9f2","status":"SHIPPED"}}]}'
```

**Query-based JDBC sources** (row 3) are a quick win and a quiet hazard. They poll with a `SELECT` using a timestamp or incrementing column, so they miss deletes and rows that share a timestamp, and they add query load to the source. Prefer log-based CDC when the database permits; fall back to the query-based connector when it does not.

**The outbox relay** (row 10) is the right way in whenever your own service writes to its own database *and* must publish an event: write both in one transaction and let a relay publish, as Chapter {{ref ch:patterns2}} explained.

## Ways Out

Every exit starts with a pull from Kafka. What differs is what happens next and who owns the target's failures. {{ref fig:kafkaio-ways-out-of-kafka}} and {{ref tbl:waysout}} show the exits.

{{fig kafkaio-ways-out-of-kafka | Every exit starts with a pull from Kafka. What differs is what happens next and who owns the target's failures.}}

{{tbl waysout | Ways of getting data out of Kafka}}

| # | Way out | Pattern | Best for | Watch out for |
|---|---|---|---|---|
| 1 | Consumer application (poll loop) | Pull, process, commit | Custom logic, API calls, complex routing | Lag; rebalances; idempotent processing; poison messages |
| 2 | Connect sink connectors (JDBC, object storage, warehouses, search) | Pull, then write | Configuration-only replication into stores | Upsert versus insert; schema mapping; error tolerance with a dead letter topic |
| 3 | HTTP sink or webhook relay | Pull, then push to REST | Delivering events to SaaS and partner endpoints | Target rate limits; retries; ordering; idempotency keys; treat 4xx as poison; batch size |
| 4 | Stream processing with queryable state | Pull, compute, serve | Real-time views and aggregates | State rebuild time; where queries are routed |
| 5 | Serverless triggers (event-source mappings, Kafka triggers) | The platform polls for you and invokes a function | Scale-to-zero glue; light transformations | Concurrency is bounded by partitions; retry loops on poison; cost at high volume |
| 6 | Integration-platform listeners | The platform consumes; a flow processes | Low-code delivery into SaaS and ERP | Acknowledgment mode; batch size; parallel consumers versus partitions |
| 7 | SSE or WebSocket gateway | Pull, fan out to clients | Live UIs and notifications | Per-user filtering; resume with the last event; slow clients |
| 8 | Share-group workers (newer Kafka releases) | Competing consumers with per-record acknowledgment | Task-style work where ordered streaming is not needed | A newer feature with different semantics; check client support and ordering expectations |
| 9 | Analytics and warehouse streaming ingest | Pull, micro-batch load | Near-real-time analytics | The cost of tiny batches; schema drift |
| 10 | Request-reply over Kafka | A reply topic plus a correlation ID | RPC-style calls over an event backbone | Timeouts; orphaned replies; consider HTTP for true RPC |
| 11 | Archive and compliance sinks (columnar files in object storage) | Pull, write files | Long-term retention outside Kafka | The small-file problem; partitioning scheme; legal holds |

Two of the exits cause most of the surprises. A **consumer or HTTP sink writing to a rate-limited API** inherits the API's behavior: when the target throttles, the consumer must *pause* rather than discard, and its writes must be idempotent. And **serverless triggers** are convenient but bounded: the number of concurrent function instances cannot usefully exceed the number of partitions, and a poison message can cause a retry loop that burns money until someone notices.

## Consumption Strategies

The same topic can be consumed in several ways, depending on how consumer groups are used. {{ref fig:kafkaio-fan-out-one-group-per-consumer-team}} illustrates six common strategies.

{{figgrid kafkaio-fan-out-one-group-per-consumer-team kafkaio-competing-consumers-one-group-many-instances kafkaio-broadcast-unique-group-per-instance kafkaio-replay-backfill-new-group-or-offset-reset kafkaio-bootstrap-from-compacted-topic kafkaio-request-reply-over-kafka | Six consumption strategies on one platform.}}

**Fan-out** (a): each consuming team uses its own group ID, and each group receives every record. This is the way to feed many independent downstream systems from one event stream. **Competing consumers** (b): one group with many instances, among which Kafka divides the partitions; this scales a single processing job. **Broadcast** (c): every instance has its own unique group, so each sees all records; use it for in-memory caches that must all know every change. **Replay and backfill** (d): a new group, or a reset of offsets to a timestamp, fixes bugs, rebuilds projections, and onboards a new consumer from history. **Bootstrap from state** (e): a new service reads a *compacted* topic from the beginning and obtains the current state of every key without history. **Request-reply** (f): a request topic, a reply topic, and a correlation ID header give RPC-like behavior; use it sparingly, since HTTP is simpler for true RPC.

Three more are worth knowing. **Priority** is not supported per record, so use separate topics per priority and let the consumer poll the high-priority topic first. **Delayed retry** uses retry topics with the consumer pausing until the due time. **Tenant partitioning** uses the tenant ID as the key, or a topic per tenant for strong isolation, although beware growth in the number of topics.

## Multi-Cluster and Multi-Region Topologies

When one cluster is not enough, four topologies recur. {{ref fig:kafkaio-active-passive}} shows them together.

{{figgrid kafkaio-active-passive kafkaio-active-active kafkaio-aggregate kafkaio-stretch-cluster | Four multi-cluster topologies.}}

{{tbl multicluster | Multi-cluster topologies compared}}

| Topology | Mechanism | Benefit | Risk |
|---|---|---|---|
| Active-passive (a) | MirrorMaker 2 or cluster linking replicates to a standby | Simple disaster recovery | Failover needs offset translation and client reconfiguration; some data may not have replicated |
| Active-active (b) | Bidirectional replication with prefixed topics | Local latency in both regions | Conflict resolution; duplicates; loops if topics are not prefixed |
| Aggregate or hub (c) | Many edge clusters replicate to a central cluster | Stores and factories keep working offline | Central cluster sizing; schema management across sites |
| Stretch cluster (d) | One cluster across three sites with rack awareness and synchronous replication | No data loss on a site failure | Needs low-latency links; a quorum of sites must stay up |

Pick by recovery objectives: how much data you can afford to lose, and how long you can afford to be down. Chapter {{ref ch:recovery}} turns these into numbers.

## Kafka Meets the Integration Platforms

Integration platforms consume from and produce to Kafka through connectors, and their behavior has details that decide correctness. The MuleSoft Kafka connector, for example, offers a *message listener* that receives records one at a time and a *batch message listener* that receives them in groups, and supports several acknowledgment modes (automatic, manual, duplicates-allowed, and immediate), which differ in when the offset is committed relative to the flow's success. Other platforms have analogous settings. Three questions apply to any of them:

* **When is the offset committed?** After the flow succeeds, or before? This decides loss versus duplication.
* **How many consumers run, relative to partitions?** More consumers than partitions leaves some idle; fewer limits throughput.
* **What happens on an error?** Does the flow's error handler decide whether the record is retried, committed, or dead-lettered, and does the *default* match what you want?

Platform behavior changes with versions, so read the current connector documentation, and test the failure cases (a failing record, a restart mid-batch) rather than assuming.

## Kafka Versus the Alternatives

Kafka is not the only streaming platform, and some alternatives fit some situations better. {{ref tbl:alternatives}} offers a short orientation, and every claim should be verified against current documentation before it is relied upon.

{{tbl alternatives | Kafka and its alternatives}}

| Platform | In brief | Consider when |
|---|---|---|
| Apache Kafka (and managed services) | The reference log-based platform with the largest ecosystem | You need the ecosystem of connectors, stream processing, and skills |
| Redpanda and other Kafka-API-compatible platforms | Implement the Kafka protocol with a different engine | You want Kafka's clients with a different operational profile |
| Apache Pulsar | Separates serving from storage; built-in multi-tenancy and geo-replication | Multi-tenancy and tiered storage are central |
| Azure Event Hubs | A managed streaming service, including a Kafka-compatible endpoint | You are Azure-native and want fewer operational duties |
| Amazon Kinesis and MSK | Kinesis is AWS's native stream; MSK is managed Kafka | You are AWS-native; choose Kinesis for simplicity, MSK for Kafka compatibility |
| RabbitMQ (queues, streams) | A classic broker with flexible routing, and a log-like streams feature | Rich routing and task queues dominate |
| NATS JetStream | A lightweight messaging system with persistence | Small footprint and simplicity matter |

## Choosing a Way In and a Way Out

Return to the decision trees of Chapter {{ref ch:decide}}. The "which way in" tree asks where the data enters: from your own application, use a producer (with an outbox if it also writes a database); from a database, use change data capture, or a JDBC poll if the need is simple; from SaaS webhooks, use an HTTP gateway or an integration platform; from legacy MQ, files, or MQTT, use a source connector or a bridge. The "which way out" tree asks where the data leaves: to a store or warehouse, a sink connector; to a rate-limited API, a consumer or HTTP sink that pauses on 429 and uses idempotency keys; to serverless, an event-source trigger with an idempotent handler; to browsers, a server-push gateway; to a SaaS application through flows, an integration-platform listener.

!!! example "Larkspur Outdoor: both ends named"
    Larkspur's analytics feed pairs a *change-data-capture source* on the ERP's database (way in 2) with a *warehouse sink connector* (way out 2), keyed by order ID. Its shop-to-ERP orders use an *application producer with an outbox* (way in 1 and 10) feeding a *consumer application* (way out 1) that calls the ERP with a lookup-before-retry safeguard. Each diagram names the way in and the way out; neither says merely "Kafka."

## Summary

Kafka is push on the write side and pull on the read side; connectors bridge to systems that cannot speak its protocol, and the consumer's control of pace gives natural backpressure toward a throttled target. There are about a dozen ways in (producers, CDC, JDBC polling, HTTP gateways, files, MQ and MQTT bridges, SaaS feeds, stream processors, outbox relays, replication, and bulk loaders) and about a dozen out (consumer applications, sink connectors, HTTP sinks, queryable state, serverless triggers, platform listeners, server push, share groups, warehouse ingest, request-reply, and archives), and a design names one of each.

Consumer groups give fan-out, competing consumption, broadcast, replay, and bootstrap from compacted state. Four multi-cluster topologies trade simplicity, latency, and data-loss risk, chosen by recovery objectives. Integration-platform connectors differ in when offsets commit, how many consumers run, and how errors are handled: verify each, and test failure cases. Alternatives to Kafka exist, and the choice follows from ecosystem, operational model, and cloud alignment.

## Exercises

1. **Name both ends.** For three integrations in your estate that involve Kafka, write the way in and the way out. Is any described only as "via Kafka"?
2. **Handle the throttle.** A consumer writes to an API with a limit of 5 calls per second. Describe exactly what it does when it receives 429, and what happens to the records that arrive meanwhile.
3. **Choose a multi-cluster topology.** A company has two regions and may lose at most 30 seconds of data, with failover in under 10 minutes. Which topology would you propose, and which would you reject?
4. **Interrogate a connector.** For an integration-platform Kafka connector you use, answer the three questions: when does it commit, how many consumers run, and what happens on error?
