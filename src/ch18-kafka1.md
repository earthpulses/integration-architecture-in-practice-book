# Kafka Fundamentals

Apache Kafka is a distributed, durable, replayable commit log. It is not a queue, although it can behave like one. It is not a database, although it stores data. And it is not magic, although the way people talk about it sometimes suggests otherwise. Understood correctly, it is one of the most useful tools an integration architect can have: a shared, ordered, retained record of events that many systems can read independently, at their own pace, and replay when something goes wrong.

Understood incorrectly, it is an expensive way to move two hundred messages a day. This chapter takes you from the mental model to the settings that decide whether a pipeline loses data, duplicates it, or runs without incident. It begins with the question that most Kafka projects skip, whether you should use it at all, then explains the model, notes what changed in the 4.x releases, and covers producers and consumers in enough depth to write correct ones. Chapter {{ref ch:kafka2}} then covers topic design, Kafka Connect, schemas, security, and operations, and Chapter {{ref ch:kafkaio}} the many ways data enters and leaves.

!!! goals "In this chapter"
    * Decide whether Kafka is the right tool, using the criteria that justify its operational cost
    * Explain topics, partitions, offsets, brokers, replication, and consumer groups
    * Describe what changed in the 4.x releases and why an architect cares
    * Configure a producer so that it does not lose or duplicate data
    * Compare delivery semantics, and explain why "exactly once" ends at Kafka's boundary
    * Write a consumer that commits after processing, handles bad records, and survives rebalances
    * Monitor consumer lag, the one metric most worth alerting on

## Should You Use Kafka at All?

The most common Kafka mistake in enterprise projects is adopting it for a flow of 200 events a day. Kafka earns its place through a specific set of strengths, and if your requirement does not need them, a simpler tool serves better. {{ref tbl:kafkaneed}} compares Kafka with polling, webhooks, and message queues across the needs that usually decide the matter.

{{tbl kafkaneed | When Kafka is, and is not, the right tool}}

| Need | REST polling | Webhooks | Message queue | Kafka |
|---|---|---|---|---|
| Freshness of minutes is fine | Best fit | Acceptable | Overkill | Overkill |
| Seconds or sub-second latency | Poor | Good | Good | Good |
| Many independent consumers of the same data | Each polls the source | The source must fan out | Needs a topic or exchange | Native strength |
| Replay history (reprocess the last seven days) | Only if the source keeps history | No | Usually no | Native strength |
| Very high throughput (100,000 or more events per second) | No | No | Limited | Native strength |
| Strict per-key ordering | By sorting | Not guaranteed | Per queue | Per partition (choose the key well) |
| Simple task distribution (each job once, competing workers) | Acceptable | Acceptable | Best fit | Share groups (newer releases) |
| Small team, low volume | Best fit | Good | Acceptable | Operational weight probably too high |

Three strengths, *replay*, *fan-out to many independent consumers*, and *throughput*, justify Kafka's weight. If none of them applies, poll or use a queue. If the client has no Kafka platform team and no existing cluster, say so plainly and put the operational cost into the recommendation: running a cluster, upgrading it, securing it, and watching it is a standing commitment, not a one-time purchase. Managed services reduce the burden without removing the need to understand the model.

## The Mental Model

{{ref fig:kafka-kafka-architecture-producers-brokers-with-pa}} shows the pieces. We take them in turn.

{{fig kafka-kafka-architecture-producers-brokers-with-pa | Topics are split into partitions; partitions are replicated across brokers; consumer groups share partitions.}}

### Topics, Partitions, and Offsets

A **topic** is a named stream of records, such as `orders.events.v1`. To scale, each topic is split into **partitions**, and each partition is an ordered, append-only sequence of records, a *log*. Every record in a partition has a number, its **offset**, which never changes: the first record is offset 0, the next 1, and so on. {{ref fig:kafka-partition-log}} shows one partition.

{{fig kafka-partition-log}}

Producers append records at the end of the log. Consumers read from a position they choose, and, crucially, **reading does not remove anything**. The record stays until the topic's *retention* expires, which might be seven days, or a size limit, or forever. This is the difference between a log and a queue, and it is what makes replay possible: a consumer that needs to reprocess last week's events simply moves its position back.

### Keys and Ordering

A record has an optional **key**, and the key decides which partition the record goes to: records with the same key always go to the same partition. Because a partition is an ordered log, records with the same key are therefore *ordered relative to each other*. {{ref fig:kafka-key-to-partition}} shows three orders, each in its own partition, with their events in sequence.

{{fig kafka-key-to-partition}}

Kafka guarantees order *within a partition*, and nothing about order *across* partitions. This leads to the single most important design rule about keys: **use the business entity's identifier** (the order ID, the customer ID) as the key, so that all events about one entity are ordered, and never use a random or missing key if order matters. A topic whose records have no key is spread across partitions with no ordering relationship at all.

### Brokers and Replication

A Kafka cluster consists of **brokers**, the servers that store the partitions. Each partition is *replicated* across several brokers: one is the **leader**, which handles all reads and writes for that partition, and the others are **followers**, which copy the leader's data. If a leader fails, one of the followers that is *in sync* is promoted. A replication factor of three is the usual production choice: the data exists on three brokers, and the cluster survives the loss of one without losing data or availability.

### Consumer Groups

Consumers read in **groups**. Within one group, each partition is assigned to exactly one consumer, so the group as a whole reads each record once, and the work is divided among its members. Two partitions and two consumers means one partition each; with six partitions, up to six consumers can work in parallel, and a seventh would sit idle. *Different* groups are fully independent: the billing group and the search group each read the entire topic, each with their own position. A new consumer team gets its own group, and no coordination with existing consumers is needed. This is the fan-out strength that distinguishes Kafka from a queue.

When a consumer joins or leaves, the group **rebalances**: the partitions are redistributed among the remaining members. Section "Rebalances" below explains why this matters.

## What Changed in Kafka 4.x

Kafka has changed significantly in recent releases, and a design that assumes older behavior may be wrong. {{ref tbl:kafka4}} summarizes the changes that matter to architects.

{{tbl kafka4 | Kafka 4.x changes and why an architect cares}}

| Change | Why it matters |
|---|---|
| **ZooKeeper removed.** Kafka 4.0 removed it entirely; every 4.x release runs in KRaft mode only | Older clusters must migrate to KRaft before upgrading; plan the upgrade path |
| **New consumer rebalance protocol** (KIP-848), generally available in 4.0; consumers opt in with `group.protocol=consumer` | Far fewer stop-the-world rebalances in large groups; check client-library support before enabling |
| **Queues for Kafka / share groups** (KIP-932): early access in 4.0, production-ready in 4.2 | Competing-consumer, per-record acknowledgment semantics for task-style workloads; use when you want queue behavior, not an ordered stream |
| **Java baseline:** brokers, Connect, and tools need Java 17; clients and Kafka Streams need Java 11 | Check base images and deployment platforms |
| **Old client protocol versions removed** | Very old clients fail against new brokers; inventory client versions early |
| **Duration-based offset reset** (KIP-1106) | A new consumer group can start "from 24 hours ago", not only from earliest or latest |

These points were verified against Apache Kafka's release announcements and upgrade notes in November 2026. Versions move quickly, so confirm what the client's cluster actually runs, whether self-managed or a managed service, before you promise a feature.

## Producers: Where Data Loss Begins

A producer sends records to the cluster, and most data loss in Kafka pipelines begins here, through settings that favor speed over safety. {{ref tbl:producer}} lists the settings that matter for integrations, with the values to prefer.

{{tbl producer | Producer settings for integrations}}

| Setting | What it does | Recommended for integrations |
|---|---|---|
| `acks` | 0 means fire and forget; 1 means the leader only; `all` means every in-sync replica | `all` for anything you cannot lose |
| `enable.idempotence` | The broker deduplicates retries per producer session and partition | `true`. It is the default in the Java client since 3.0, but librdkafka-based clients (Python, Go, .NET, Node.js) must set it explicitly |
| `retries`, `delivery.timeout.ms` | How long the producer keeps retrying a send | Leave retries high; bound the total with `delivery.timeout.ms` (for example 120,000) |
| `linger.ms`, `batch.size` | Wait briefly to batch records; larger batches mean higher throughput | 5 to 50 ms and 64 to 256 KB for throughput flows; 0 to 5 ms for latency flows |
| `compression.type` | Compress batches | `zstd` or `lz4` for most uses; a large win for JSON |
| `max.in.flight.requests.per.connection` | Parallel unacknowledged requests | 5 or fewer with idempotence keeps ordering |
| `transactional.id` | Atomic writes across partitions and consume-transform-produce exactly-once | Only when you truly need atomic multi-topic output |
| The record key | Hashed to choose the partition | The business entity ID, never random |

Three of these deserve explanation. `acks=all` makes the producer wait until *all in-sync replicas* have the record, so the loss of the leader cannot lose acknowledged data; together with the topic setting `min.insync.replicas=2`, it means an acknowledged record lives on at least two brokers. **Idempotence** makes the producer's own retries safe: each producer has an identity and numbers its records per partition, so if a retry sends a record that the broker already stored, the broker recognizes the sequence number and discards the duplicate. Without it, a network blip during an acknowledgment causes a duplicate. And **linger and batch** settings trade a little latency for a lot of throughput, because sending records in batches is far more efficient than sending them one by one.

The following sketch shows a producer with safe settings, using the `confluent-kafka` Python client. It requires a running cluster, so it is not part of the companion test suite; treat it as a template.

```python
from confluent_kafka import Producer
import json, uuid, datetime as dt, logging
log = logging.getLogger("producer")

p = Producer({
    "bootstrap.servers": "broker1:9093,broker2:9093",
    "security.protocol": "SASL_SSL", "sasl.mechanism": "SCRAM-SHA-512",
    "sasl.username": "svc-orders", "sasl.password": "<from the vault>",
    "acks": "all", "enable.idempotence": True,
    "compression.type": "zstd", "linger.ms": 20, "batch.size": 131072,
    "delivery.timeout.ms": 120000,
})

def on_delivery(err, msg):
    if err:
        log.error("delivery failed key=%s: %s", msg.key(), err)  # alert!

def publish(order):
    event = {"id": str(uuid.uuid4()), "type": "order.updated.v1",
             "time": dt.datetime.now(dt.timezone.utc).isoformat(),
             "data": order}
    p.produce("orders.events.v1", key=str(order["id"]),
              value=json.dumps(event),
              headers={"event-type": "order.updated.v1"},
              on_delivery=on_delivery)
    p.poll(0)                       # serve delivery callbacks

# On shutdown, never exit without:  p.flush(30)
```

!!! warning "produce() only queues the message"
    The call places the record in a local buffer; it does not mean the record reached Kafka. Without a delivery callback and a final `flush()`, a job can exit "successfully" having sent nothing. Check every delivery report, and fail the run, or alert, if any reports an error.

## Consumers, Groups, and Offsets

A consumer reads records, processes them, and *commits its offset* to record how far it has got. When it restarts, it resumes from the committed offset. *When* it commits relative to processing determines what happens when something fails.

### Delivery Semantics

{{tbl semantics | Delivery semantics and when to use each}}

| Semantics | How you get it | Outcome on failure | Use for |
|---|---|---|---|
| At most once | Commit the offset *before* processing | Messages can be lost | Metrics where loss is tolerable |
| At least once | Process, *then* commit | Messages can be repeated | The normal choice; pair with idempotent processing |
| Exactly once (within Kafka) | Idempotent producer plus transactions, `isolation.level=read_committed` | Neither lost nor duplicated inside Kafka topics | Kafka-to-Kafka stream processing |
| Effectively once (end to end) | At least once plus an idempotent sink (upsert by key, deduplication table) | Duplicates arrive but have no effect | Kafka to a database, API, or other system |

"Exactly once" is a precise claim with a boundary: it holds *within Kafka*, for records that are read from Kafka topics and written to Kafka topics in a transaction. The moment your consumer calls a REST API or writes to a database, you are outside the boundary and back to at-least-once, and your safety comes from idempotent writes. Design the sink first. For nearly every integration, the right answer is "at least once, with an idempotent sink," which delivers *effectively once* results, as Chapter {{ref ch:time}} showed in sequence.

### A Consumer That Behaves

The consumer sketch below embodies the rules. It disables auto-commit, because the default commits on a timer regardless of whether processing succeeded; it commits only after a batch has been handled; it distinguishes permanent failures, which go to a dead letter queue, from transient ones, which stop the batch so that it is redelivered; and it closes cleanly so that its partitions are released promptly.

```python
from confluent_kafka import Consumer, KafkaError

c = Consumer({
    "bootstrap.servers": "broker1:9093", "group.id": "erp-sync-v1",
    "enable.auto.commit": False,         # we commit after processing
    "auto.offset.reset": "earliest",     # only when no committed offset
    "isolation.level": "read_committed",
    "max.poll.interval.ms": 300000,      # must exceed the slowest batch
    "session.timeout.ms": 45000,
    "partition.assignment.strategy": "cooperative-sticky",
})
c.subscribe(["orders.events.v1"])
try:
    while True:
        batch = c.consume(num_messages=200, timeout=1.0)
        for m in batch:
            if m.error():
                if m.error().code() != KafkaError._PARTITION_EOF:
                    log.error(m.error())
                continue
            try:
                handle(m)              # idempotent upsert by event ID or key
            except PermanentError as e:
                send_to_dlq(m, reason=str(e))   # park it and go on
            # a TransientError propagates: no commit, batch is redelivered
        if batch:
            c.commit(asynchronous=False)
finally:
    c.close()                          # leave the group cleanly
```

The newer consumer protocol described above changes the configuration: set `group.protocol` to `consumer` (which requires brokers at 4.0 or later and a client library that supports it), and *remove* the client-side assignment strategy and heartbeat settings, which that protocol does not use.

### Rebalances: The Hidden Cost

Whenever consumers join, leave, or are considered dead, the partitions are reassigned. With the classic *eager* protocol, every consumer in the group stops, gives up all its partitions, and waits for a new assignment, which causes lag spikes and duplicate processing as uncommitted work is redone by the new owner. **Cooperative-sticky** assignment moves only the partitions that must move, and the newer protocol moves coordination to the broker and removes the global stop.

The common triggers deserve a place in every troubleshooting checklist: processing that takes longer than `max.poll.interval.ms`, so the consumer is declared dead; rolling deployments that restart consumers one by one; autoscalers that add and remove consumers repeatedly; and long garbage-collection pauses. **Static membership**, a `group.instance.id` per consumer, lets a restarted instance rejoin without causing a rebalance within the session timeout, which is a useful remedy for rolling deployments.

### Consumer Lag: The One Metric to Alert On

**Lag** is the difference between the newest record in a partition and the group's committed position. It is the single most informative measure of a consumer's health, and the command-line tool reports it:

```text
kafka-consumer-groups.sh --bootstrap-server broker1:9093 \
  --command-config client.properties --describe --group erp-sync-v1

GROUP        TOPIC             PARTITION CURRENT  LOG-END  LAG
erp-sync-v1  orders.events.v1  0         98121    98130    9
erp-sync-v1  orders.events.v1  1         97004    131552   34548  <- stuck
```

Alert on *growing* lag, as a trend, not on a fixed number. A steady lag of nine records is healthy; lag that grows for ten minutes is an incident. Also alert on **time lag**, the age of the oldest unprocessed record, because it maps directly to the business's freshness target: "orders must be in the ERP within five minutes" translates into "time lag must stay below five minutes."

## Partitions: How Many?

A final design decision arrives early and is hard to reverse: the number of partitions. Too few limits parallelism, since a group can use at most as many consumers as there are partitions. Too many adds overhead and lengthens recovery. A workable method is to start from throughput. If a single consumer can process 2 MB/s and the topic must carry 20 MB/s at peak, you need at least ten partitions; add headroom for growth, so perhaps 24. Partitions can be added later, but doing so changes which partition a key maps to, breaking ordering guarantees for existing keys. Choose generously at creation, and avoid thousands per topic without a reason.

## Summary

Kafka is a replayable, partitioned, replicated log, and it earns its operational weight only for replay, fan-out to many independent consumers, or very high throughput; for small flows, a poll or a queue is better. A topic is split into partitions, each an ordered log of numbered records; keys place related records in one partition, which preserves their order; brokers replicate partitions for durability; consumer groups divide a topic's partitions among their members while remaining independent of other groups.

Kafka 4.x runs without ZooKeeper, offers a new consumer protocol, and adds share groups for queue-like work. A producer that cannot lose data uses `acks=all`, idempotence, bounded delivery timeouts, and a business key, and always checks delivery reports and flushes. A consumer commits after processing, parks permanent failures in a dead letter queue, and treats at-least-once delivery with idempotent sinks as "effectively once." Rebalances cause duplicates and pauses, and growing consumer lag, in records and in time, is the most useful alert.

## Exercises

1. **Justify Kafka.** For a flow you work with, score it against the table: how many of the three strengths (replay, fan-out, throughput) does it need? Would a queue or polling serve?
2. **Choose keys.** For orders, payments, and shipments, state the key each topic should use. What ordering guarantee does each key give? What breaks if the key is random?
3. **Find the default.** Check the idempotence setting in the Kafka client you use. Is it on by default? Where would you set it explicitly?
4. **Size a topic.** A topic must carry 30 MB/s at peak, and one consumer handles 3 MB/s. How many partitions would you create, and why that many?
