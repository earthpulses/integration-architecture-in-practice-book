# Kafka in Production

Understanding Kafka's model is the beginning. Running integrations on it is a matter of a few dozen decisions that look minor and are not: how many partitions, what retention, which key, which schema rules, how errors are handled, who may read what, and what you watch. Each is easy to get roughly right and costly to correct once other teams depend on it, because a topic, unlike a private function, is a shared interface with a long memory.

This chapter covers topic design, event design, Kafka Connect and change data capture, schemas and their evolution, stream processing, error handling with retry topics and dead letter queues, security, and operations, including capacity arithmetic and multi-region options. It closes with a troubleshooting matrix and the questions to ask a client before any Kafka design begins.

!!! goals "In this chapter"
    * Size partitions from throughput, choose keys that avoid hot partitions, and pick retention or compaction
    * Design events as business facts with an envelope, a version, and both event time and processing time
    * Configure source and sink connectors, including a change-data-capture source and a sink with a dead letter queue
    * Evolve schemas safely using a registry and a compatibility mode
    * Handle failure with non-blocking retries and a dead letter topic
    * Secure a cluster with TLS, authenticated principals, and least-privilege ACLs
    * Estimate storage and monitor the signals that predict trouble

## Topic Design

### How Many Partitions?

Partitions cap consumer parallelism: a group can have at most one active consumer per partition. A practical method is to take the larger of two quotients, the target throughput divided by what one partition can *produce*, and the target divided by what one partition's consumer can *process*:

```text
partitions >= max( target / producer_throughput_per_partition,
                   target / consumer_throughput_per_partition )

Example: target 60 MB/s; one partition handles about 10 MB/s of
producing and 5 MB/s of consuming:
   max(60/10, 60/5) = max(6, 12) = 12 partitions
Add headroom for growth: choose 18 or 24.
```

Both extremes cause trouble. *Too few* partitions mean consumers cannot scale out, one slow partition blocks a whole range of keys, and migration later is painful, because adding partitions changes the key-to-partition mapping and so breaks per-key ordering across the change. *Far too many* mean more file handles, longer leader elections and recovery, more memory in consumers, and added end-to-end latency; thousands of partitions per broker need care. Choose generously at creation, but with a reason.

### Keys and Hot Partitions

Choose the key that defines the *ordering boundary*: all events about one order, one customer, one asset share a key. A badly distributed key creates a **hot partition**. If one enormous customer produces half your events and the customer ID is the key, one partition, and so one consumer, carries half the load while the others sit idle. A constant or null key is the extreme case. A null key distributes records round-robin, which is excellent for throughput and gives no ordering guarantee at all. Check key distribution in design and in monitoring.

### Retention or Compaction

Each topic has a cleanup policy, and the choice reflects what the topic *means*.

{{tbl retention | Retention policies and their uses}}

| Policy | Behavior | Use for | Notes |
|---|---|---|---|
| `delete` (by time or size) | Old segments are removed after the retention period | Event streams, logs, telemetry | Set retention longer than your worst-case outage plus replay needs |
| `compact` | Keeps only the latest record per key; a null value (a *tombstone*) deletes the key | Current-state topics, reference data, changelogs | A new consumer sees the latest state per key, not the full history |
| `compact,delete` | Both | State with bounded age | Tombstones are retained for `delete.retention.ms`; consumers offline longer miss deletes |

The retention-period rule contains a sentence worth underlining: *longer than your worst-case outage plus replay needs*. If the consumer team might be down for a long weekend, and might need to reprocess a week of data after a bug, seven days is the minimum, not the generous option.

### A Sane Default

For a business-event topic, this creation command is a reasonable starting point:

```bash
kafka-topics.sh --bootstrap-server broker1:9093 \
  --command-config client.properties --create \
  --topic sales.order.events.v1 --partitions 12 --replication-factor 3 \
  --config min.insync.replicas=2 \
  --config retention.ms=604800000 \
  --config compression.type=producer \
  --config max.message.bytes=1048576
```

It sets twelve partitions, three replicas, a minimum of two in-sync replicas (so that `acks=all` means two copies), seven days of retention (604,800,000 milliseconds), and a one-megabyte record limit. Keep events small and link to large payloads using the claim-check pattern of Chapter {{ref ch:patterns2}}.

### Naming and Versioning

Adopt a naming pattern and enforce it. A common one is `<domain>.<entity>.<kind>.v<major>`, giving names such as `sales.order.events.v1`, `sales.order.state.v1` (a compacted topic), and `sales.order.events.dlq.v1`. Increase the major version in the name only for *breaking* changes; compatible changes use schema evolution. Isolate environments by cluster, not by name suffix, wherever possible; if tenants must share a cluster, encode tenant and environment in the name and apply quotas and ACLs per tenant.

## Event Design on Kafka

Chapter {{ref ch:apidesign}} set out the principles for events as a provider. On Kafka, the styles available are worth comparing.

{{tbl evstyles | Event styles on Kafka}}

| Style | Payload | Strength | Weakness |
|---|---|---|---|
| Notification | Just "order 42 changed", with an ID | Small; always current after you fetch | Consumers call back to the source; coupling and load |
| Event-carried state transfer | The full new state of the entity | Consumers need no callback; easy to rebuild state | Larger; the schema is a public contract |
| Domain event | What happened (`OrderShipped`) with the fields that matter | Business meaning is explicit | Harder to reconstruct the current state |
| CDC row event | Before and after images of a database row | Complete, with no application changes | Leaks the physical schema; consumers depend on table structure |

A widely supported envelope is **CloudEvents**, a standard from the Cloud Native Computing Foundation. A typical event looks like this:

```json
{
  "specversion": "1.0",
  "id": "7d1e0f4c-8f3b-4a0f-9c0e-0e3d1f2a9b11",
  "type": "com.example.sales.order.updated.v1",
  "source": "/erp/orders",
  "subject": "order/10492",
  "time": "2026-11-23T09:14:07.311Z",
  "datacontenttype": "application/json",
  "data": {"orderId": 10492, "status": "SHIPPED", "version": 17,
           "total": {"amount": "129.90", "currency": "EUR"}}
}
```

The `id` is unique per event and is the consumer's deduplication key. The `subject` identifies the entity and is also the natural Kafka key. The `time` is *event time*, when the thing happened, in UTC. Carry both event time and processing time (when your system handled it), because late events are normal. And include a per-entity `version` so that consumers can discard stale or reordered events, since Kafka orders only within a partition. Notice that the monetary amount is a string, to avoid the floating-point trap of Chapter {{ref ch:formats}}.

## Kafka Connect and Change Data Capture

**Kafka Connect** is a runtime for moving data between Kafka and other systems through *configuration*, not code. *Source connectors* read from external systems into topics, and *sink connectors* write from topics to external systems. Connect runs as a cluster of **workers** that execute connector **tasks**, stores connector offsets in internal topics, and exposes a REST API for managing connectors. Using Connect means that you inherit solved problems (retries, offset tracking, scaling out, error handling) instead of rewriting them.

### A Change-Data-Capture Source

The most important source connector for integrations is a **change-data-capture** connector such as Debezium, which reads a database's transaction log and publishes each row change as an event. This configuration reads two tables from a PostgreSQL database:

```json
{
  "name": "pg-orders-cdc",
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "database.hostname": "prod-db.internal",
    "database.port": "5432",
    "database.user": "cdc_reader",
    "database.password": "${file:/secrets/db.properties:password}",
    "database.dbname": "production_db",
    "topic.prefix": "pg",
    "table.include.list": "public.orders,public.order_items",
    "plugin.name": "pgoutput",
    "slot.name": "debezium_orders",
    "snapshot.mode": "initial",
    "heartbeat.interval.ms": "10000",
    "key.converter": "io.confluent.connect.avro.AvroConverter",
    "value.converter": "io.confluent.connect.avro.AvroConverter",
    "key.converter.schema.registry.url": "https://sr.internal:8081",
    "value.converter.schema.registry.url": "https://sr.internal:8081",
    "transforms": "unwrap",
    "transforms.unwrap.type":
        "io.debezium.transforms.ExtractNewRecordState",
    "transforms.unwrap.delete.handling.mode": "rewrite"
  }
}
```

Several properties encode decisions. The `topic.prefix` makes the topics `pg.public.orders` and `pg.public.order_items`. The `database.password` is a *reference* to a file, not a literal, as Chapter {{ref ch:auth}} insists. The `slot.name` names a PostgreSQL *replication slot*, which keeps the database from discarding log segments the connector has not yet read. That is essential for correctness, and also the connector's main hazard: an idle or stopped connector leaves the slot holding log data, which can fill the source database's disk. Monitor the slot's lag. The `heartbeat.interval.ms` makes the connector advance the slot even when the captured tables are quiet, so that unrelated database activity does not accumulate log. The `snapshot.mode` of `initial` takes a full snapshot first and then streams changes. And the *unwrap* transformation flattens Debezium's envelope into a simple record, with deletes kept visible as a flag.

### A Sink with a Dead Letter Queue

A sink connector writes topic data to a target. This configuration upserts into a warehouse through JDBC and routes bad records to a dead letter topic:

```json
{
  "name": "orders-to-warehouse",
  "config": {
    "connector.class": "io.confluent.connect.jdbc.JdbcSinkConnector",
    "topics": "pg.public.orders",
    "insert.mode": "upsert",
    "pk.mode": "record_key",
    "pk.fields": "id",
    "errors.tolerance": "all",
    "errors.deadletterqueue.topic.name": "dlq.orders-to-warehouse",
    "errors.deadletterqueue.context.headers.enable": "true",
    "errors.retry.timeout": "600000",
    "errors.retry.delay.max.ms": "30000",
    "errors.log.enable": "true"
  }
}
```

The `insert.mode` of `upsert` with the record key as the primary key makes the sink idempotent: replays and duplicates overwrite instead of multiplying. The `errors.tolerance` of `all` means one bad record does not kill the task; instead the record is written to the dead letter topic, with headers explaining *why* it failed. Transient failures are retried for up to ten minutes with a delay that grows to thirty seconds. Leaving `errors.tolerance` at its default `none` makes a single malformed record stop the connector, which is sometimes right (it fails loudly) and sometimes disastrous, so choose deliberately.

### Operating Connect

Three REST calls cover most operations:

```bash
# list connectors with their configuration and status in one call
curl -s "http://connect:8083/connectors?expand=info&expand=status" | jq 'keys'

# restart only the failed tasks, after fixing the cause
curl -s -X POST "http://connect:8083/connectors/pg-orders-cdc/restart\
?includeTasks=true&onlyFailed=true"

# pause during maintenance
curl -s -X PUT "http://connect:8083/connectors/pg-orders-cdc/pause"
```

{{tbl cdc | Change-data-capture hazards and mitigations}}

| Hazard | Why it happens | Mitigation |
|---|---|---|
| The source disk fills up | The replication slot retains log data while the connector is down or slow | Alert on slot lag and disk; use heartbeats; drop the slot deliberately when decommissioning |
| Schema change breaks consumers | CDC exposes the physical table | Use an outbox or a view as the contract; use schema compatibility rules |
| The initial snapshot is slow or locks tables | A large table is read in one pass | Use incremental snapshots; run during low traffic |
| Deletes are lost | Consumers ignore tombstones or compaction removes them | Keep the delete flag; set `delete.retention.ms` above the longest consumer outage |
| Out-of-order updates | Multiple partitions or reprocessing | Key by primary key; carry the source's log position or a version |

## Schemas and Their Evolution

Records without schemas are strings, and strings drift. A **schema registry** stores the schema of each topic's records, assigns each version an identifier, and checks new versions against a **compatibility mode** before they are accepted. Producers embed the schema identifier in each record (a few bytes), and consumers fetch the schema by identifier to decode it. The registry therefore acts as an enforcement point: a producer that tries to publish a breaking change is refused.

{{tbl compat | Schema compatibility modes}}

| Mode | Allowed change | Who must upgrade first |
|---|---|---|
| Backward | New schema can read data written with the old one (for example, delete a field or add one with a default) | Consumers, then producers |
| Forward | Old consumers can read data written with the new schema (for example, add a field) | Producers, then consumers |
| Full | Both directions | Either order |
| None | Anything goes | Nobody is protected |

Three rules cover most evolution. **Add optional fields with defaults**; this is compatible in the common modes. **Never change a field's type or meaning**, because even a compatible-looking change corrupts consumers that rely on the old meaning. And, for Protobuf, **never reuse a field number**. The formats, Avro, Protobuf, and JSON Schema, differ in details, but the discipline is the same: evolve additively, validate in the build before anything is produced, and choose the strictest compatibility mode your producers can live with. Enforce the mode in the pipeline (Chapter {{ref ch:delivery}}), so a pull request that would break consumers fails before deployment.

## Stream Processing: When to Transform Inside Kafka

Some transformations belong inside the streaming platform: filtering, enriching with reference data, joining two streams, aggregating over time windows. **Stateful stream processing** (Chapter {{ref ch:patterns2}}) keeps state between events and handles *late* and *out-of-order* data using event time and windows. Kafka Streams, Apache Flink, and ksqlDB are the common tools. Use them when the result is itself a stream that other consumers need, or when the computation requires continuity over time that a request-based job cannot provide. Do *not* use them to perform ordinary business integration, such as calling an ERP: that is the job of a consumer with an idempotent sink. The honest costs to weigh are the state's size and recovery time, the handling of late data, and the skill the team needs.

## Errors, Retries, and Dead Letter Topics

A consumer that fails on a record has two bad options: stop, and block everything behind it, or skip, and lose data. Retry topics and a dead letter topic give a third. {{ref fig:kafka-retry-topics-and-dead-letter-queue-flow}} shows a **non-blocking retry** design.

{{fig kafka-retry-topics-and-dead-letter-queue-flow | Non-blocking retries. A failed record moves to a delay topic so the main partition keeps flowing. After the last attempt it moves to the dead letter topic for a human.}}

When the main consumer fails to process a record because of a *transient* error, it publishes the record to a **retry topic** with a delay, instead of retrying in place. The main partition keeps flowing, so one troublesome record does not stall thousands of healthy ones. A retry consumer processes the delayed record after the delay, and, if it still fails, may pass it on to a longer-delay topic. After the final attempt, or immediately for a *permanent* error such as a malformed message, the record goes to the **dead letter topic**, with the failure reason in its headers.

The trade-off is ordering: a retried record arrives after later records for the same key, so the consumer must tolerate out-of-order arrival, using the per-entity version to ignore stale events. If strict order matters, the alternative is to *pause* the partition and retry in place, accepting the stall. Either way, the dead letter topic needs an owner, an alert on its depth, and a tool to inspect and replay its records once the cause is fixed. Chapter {{ref ch:reliability}} returns to this operational discipline.

## Security

A Kafka cluster shared by many applications is a high-value target, and its security has four layers.

**Encryption in transit.** Use TLS between clients and brokers and between brokers. **Authentication.** Every client authenticates as a distinct principal: mutual TLS, SASL/SCRAM with per-application credentials, or SASL/OAUTHBEARER for token-based identity. Never share one credential among applications. **Authorization.** Use access control lists to grant each principal only what it needs: write to *its* topics, read from *its* input topics, and use *its* consumer group. Prefixed ACLs (such as `sales.order.*`) keep this manageable. **Protection of data.** Do not publish personal data to broadly readable topics; tokenize or encrypt sensitive fields, and remember that retention keeps data for days or weeks, so a deletion request must account for the log. Apply quotas so that one runaway producer cannot starve the rest.

!!! warning "A topic is a shared interface"
    Anyone who can read a topic can read all of it, including history. Classify topics by sensitivity, separate the sensitive ones, and review who holds read permission as carefully as you would for a database table.

## Operations

### Capacity Arithmetic

Estimate storage before the cluster exists. The formula is *ingest rate × retention × replication factor*. A topic carrying 20 MB/s retained for 7 days needs 20 × 86,400 seconds × 7 days = about 12.1 TB for one copy, and with a replication factor of three, about 36 TB. Add headroom of at least 30 percent. Network follows a similar rule: with replication, each byte produced is written to the network several times, and each consumer group multiplies the read traffic.

### What to Monitor

Four groups of signals predict trouble. *Replication health:* under-replicated partitions and offline partitions should both be zero, and a shrinking in-sync replica set means a struggling broker. *Resources:* disk use, network throughput, and request latency. *Consumers:* lag in records and in time, per group, and rebalance frequency. *Connect:* the status of every connector and task, and the dead letter topic's depth. For CDC, add the replication slot's retained size.

### Multi-Region Options

Spanning regions is a trade between simplicity and recovery. **Active-passive** replication (using MirrorMaker 2, or a vendor's cluster-linking feature) copies topics from a primary region to a standby: simple, suitable for disaster recovery, with the cost that failover requires translating consumer offsets and accepting a small window of loss. **Active-active** runs producers and consumers in both regions with topics replicated each way, which demands care to avoid loops and conflicts. A **stretch cluster** spans three sites in one cluster, rack-aware, with synchronous replication: it offers very low loss but needs low-latency links. Chapter {{ref ch:kafkaio}} shows each in a diagram, and Chapter {{ref ch:recovery}} connects them to recovery objectives.

## Kafka and the Data Catalog

A governed estate wants to know which topics exist, who owns them, which schemas they carry, and where the data goes. Catalogs can harvest topic and schema metadata from the registry. *Lineage* across topics can be derived from connector configurations (this source feeds that topic, this sink reads it) or emitted as **OpenLineage** events by stream processors and orchestrators, the open specification for run, job, and dataset lineage. Linking topics to owners, classifications, and data contracts (Chapter {{ref ch:governance}}) turns the streaming platform from a black box into a governed asset.

## A Troubleshooting Matrix

{{tbl kafkatrouble | Kafka symptoms, causes, and fixes}}

| Symptom | Likely cause | Fix |
|---|---|---|
| Lag grows steadily | The consumer is slower than the producer; a hot partition; a slow target | Scale consumers up to the partition count; fix key skew; apply backpressure to the target; check the sink's rate limit |
| Duplicates in the target | At-least-once delivery after a rebalance or restart | Make the sink idempotent (upsert by key or event ID) |
| Frequent rebalances | Processing exceeds `max.poll.interval.ms`; flapping autoscaler; rolling deploys | Raise the interval or shrink batches; use static membership and cooperative assignment |
| Records missing | Auto-commit before processing; a producer that never flushed; retention expired | Commit after processing; check delivery reports and flush; lengthen retention |
| Producer timeouts | Broker unreachable; `acks=all` with too few in-sync replicas | Check the network, ACLs, and `min.insync.replicas` against the replica count |
| A connector shows FAILED | A bad record with `errors.tolerance=none`; a credentials change; a schema error | Read the task's trace; fix the cause; restart only the failed tasks |
| The CDC source disk fills | An idle replication slot | Restore the connector or drop the slot; add slot-lag alerts |
| Schema registry rejects a change | The change violates the compatibility mode | Make the change compatible, or create a new versioned topic for a breaking one |
| Ordering looks wrong | A null or random key; the retry topic path | Key by entity; carry a version and ignore stale events |

## Questions to Ask Before Any Kafka Design

* Who are the producers and consumers, today and in two years?
* What is the throughput at peak, in records and in megabytes per second?
* How long must data be retained, and who may need to replay it?
* What defines the ordering boundary, and is there a natural key?
* What schemas exist, who owns them, and what compatibility rules apply?
* Who runs the cluster, and what happens when they are unavailable?
* What are the security and data-protection requirements for each topic?
* How are failures handled, who owns the dead letter topics, and how are messages replayed?
* What are the recovery objectives across regions?

## Summary

Partitions are sized from throughput divided by per-partition rates, keys are chosen to define the ordering boundary and avoid hot partitions, and retention or compaction reflects what the topic means. Events carry an envelope, a unique ID, a per-entity version, and both event time and processing time. Kafka Connect supplies the integration plumbing: a change-data-capture source reads database logs, with a replication slot to monitor, and a sink with upsert semantics and a dead letter topic is idempotent and tolerant of bad records.

A schema registry with a compatibility mode, enforced in the pipeline, makes evolution safe: add optional fields with defaults, never change meaning, and never reuse Protobuf field numbers. Non-blocking retries keep partitions flowing, and the dead letter topic needs an owner, an alert, and a replay tool. Security means encrypted transport, distinct authenticated principals, least-privilege ACLs, and care with sensitive data. Capacity is ingest × retention × replication, and the signals worth watching are replication health, resources, consumer lag, and connector status.

## Exercises

1. **Size a topic.** A topic must carry 45 MB/s at peak with seven days of retention and replication factor three. How many partitions (one consumer handles 5 MB/s), and how much disk?
2. **Review a connector.** Take a sink connector configuration from your estate. What happens to a single malformed record? What does `errors.tolerance` say? Where would the record go?
3. **Plan an evolution.** You must add a mandatory field to an event with fifty consumers. Describe the steps and the compatibility mode that make it safe.
4. **Design the retry path.** For a consumer that writes to an API with a rate limit, define the retry topics and delays, the number of attempts, the conditions for the dead letter topic, and who is alerted.
