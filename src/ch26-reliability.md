# Reliability and Observability

An integration that works is not the same as an integration you can rely on. The first is a statement about a moment; the second is a statement about months of operation, through outages, deployments, expired certificates, and upstream changes. Reliability is the discipline of designing for the unreliable world in which integrations actually live, and observability is the discipline of *knowing* what is happening, so that you hear about a problem from your own alert and not from a customer.

This chapter assembles the reliability toolkit that earlier chapters introduced piece by piece, and adds what they did not cover: how to follow one transaction across queues and systems with traces, how to define service-level indicators and objectives for an integration, how to design alerts that people act on, and how to write the runbook that makes the difference between a three-minute and a three-hour incident.

!!! goals "In this chapter"
    * Combine timeouts, retries, idempotency, circuit breakers, bulkheads, backpressure, dead letters, and reconciliation into a reliability design
    * Instrument an integration with logs, metrics, and traces, and propagate trace context across asynchronous hops
    * Define service-level indicators and objectives for freshness, completeness, correctness, and headroom
    * Design alerts that are symptom-based, owned, and actionable
    * Write a runbook that someone other than the author can execute

## The Reliability Toolkit

Reliability for integrations comes from a small set of mechanisms, each answering a specific failure. {{ref tbl:toolkit}} collects them, with where each is described in this book.

{{tbl toolkit | The reliability toolkit}}

| Mechanism | The failure it answers | Where described |
|---|---|---|
| Timeouts | A call that hangs forever | Chapter {{ref ch:python}} |
| Bounded retries with backoff and jitter | Transient errors; retry storms | Chapter {{ref ch:python}} |
| Idempotency | Duplicates from retries and redelivery | Chapters {{ref ch:basics}}, {{ref ch:python}}, {{ref ch:sync}} |
| Circuit breaker | A failing dependency that is hammered | Chapter {{ref ch:time}} |
| Bulkhead | One slow dependency exhausting shared resources | This chapter |
| Backpressure | A producer faster than a consumer | Chapters {{ref ch:kafka1}} and {{ref ch:kafkaio}} |
| Dead letter queue and quarantine | Poison messages and bad records | Chapters {{ref ch:patterns2}} and {{ref ch:kafka2}} |
| Checkpoints | Crashes mid-run | Chapter {{ref ch:python}} |
| Reconciliation | Drift from every cause | Chapter {{ref ch:sync}} |
| Replay | A bug that corrupted data | Chapters {{ref ch:kafka1}} and {{ref ch:recovery}} |

Two are new to this chapter, or deserve a fuller treatment.

**Bulkheads.** A ship's bulkheads keep a leak in one compartment from sinking the whole vessel. In software, the idea is to give each dependency its own *limited* pool of resources, such as threads, connections, and queue capacity, so that when one slows down it exhausts only its own pool. Without bulkheads, a slow ERP can consume every worker thread, and the integration that has nothing to do with the ERP stops too. In practice: separate worker pools or queues per target system, and a cap on concurrent calls to each.

**Backpressure.** When a producer can outrun a consumer, something must give. Either the producer is slowed (backpressure), or the data accumulates somewhere (a queue or log, which is a deliberate buffer), or it is dropped (data loss). Good designs choose the first two on purpose: a pull-based consumer simply stops pulling; a webhook receiver answers 429 or 503 so the sender slows down; and queues are sized and monitored so that "the buffer is filling" is an alert, not a surprise.

!!! why "Why this matters"
    Reliability mechanisms work in *combination* and fail in combination. A retry without backoff hammers a target; backoff without a circuit breaker still wastes threads; a circuit breaker without a dead letter path discards messages; a dead letter queue without an owner is data loss with extra steps. Review a design by asking, for each failure in the table, which mechanism answers it, and who watches that mechanism.

## Observability: Knowing What Is Happening

An integration is almost always invisible when it works. **Observability** is the practice of making its behavior knowable through three kinds of evidence: *logs* (what happened), *metrics* (how much and how fast), and *traces* (how one transaction moved through the system).

### Logs

Logs should be *structured*, with every line a set of named fields, as Chapter {{ref ch:python}} showed, so they can be searched and counted. Every line carries a run ID, a trace ID, and the entity ID; outcome and reason are fields rather than prose; and no line carries a secret or unmasked personal data.

### Metrics

Metrics are numbers over time, cheap to store and fast to alert on. For an integration, the essential ones are throughput (records per minute in and out), error counts by class, latency of calls to each dependency, queue depth or consumer lag, the age of the oldest unprocessed item, quarantine counts, and the time since the last successful run.

### Traces

Logs tell you what one component did; a **trace** tells you what happened to one business transaction across all of them. Integrations break traces at every queue and topic, because the receiving side has no idea which transaction a message belongs to, unless the context travels *with* the message. The W3C Trace Context standard defines a `traceparent` header (for example `00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01`, holding a version, a trace ID, a parent span ID, and flags), and OpenTelemetry propagates it over HTTP and, with a few lines of code, over message headers. {{ref fig:obs-trace-context-across-asynchronous-hops}} shows the idea.

{{fig obs-trace-context-across-asynchronous-hops | Inject the trace context when you send; extract it when you receive. The result is one trace from the webhook to the analytics consumer.}}

The webhook arrives at the receiver (step 1), which starts a span and puts the event on a queue with the trace context in the message headers (step 2). The worker takes the message and *extracts* the context (step 3), so its span continues the same trace; it passes the context in its call to SAP (step 4) and in the event it publishes to Kafka (step 5). The analytics consumer extracts it again (step 6), and a trace backend assembles all the spans into one trace from the first webhook to the last consumer (step 7).

The code is small. This sketch uses OpenTelemetry's propagation functions with a Kafka producer and consumer; it needs the OpenTelemetry packages and a configured exporter, so it is a template rather than part of the companion tests.

```python
from opentelemetry import trace
from opentelemetry.propagate import inject, extract

tracer = trace.get_tracer("orders-sync")

def publish(producer, topic, key, value):
    with tracer.start_as_current_span(f"{topic} publish"):
        carrier = {}
        inject(carrier)              # adds traceparent for the current span
        producer.produce(topic, key=key, value=value,
                         headers=list(carrier.items()))

def handle(msg):
    carrier = {k: v.decode() for k, v in (msg.headers() or [])}
    ctx = extract(carrier)           # continue the producer's trace
    with tracer.start_as_current_span("orders process", context=ctx):
        process(msg)
# A batch consumer starts one span per batch and adds a span *link*
# to each message's context instead of a single parent.
```

## Service-Level Indicators and Objectives

An integration needs measurable goals, or "reliable" means whatever the loudest stakeholder says it means. A **service-level indicator** (SLI) is a measurement; a **service-level objective** (SLO) is a target for it. {{ref tbl:slis}} lists the indicators that suit integrations.

{{tbl slis | Service-level indicators and example objectives for an integration}}

| Indicator | Definition | Example objective |
|---|---|---|
| Freshness | The age of the newest change visible in the target, or the time from a source change to the target | 95% of changes within 5 minutes |
| Completeness | The share of source records present in the target after reconciliation | 100% daily; any non-zero drift alerts |
| Correctness | The share of sampled records whose fields match after mapping | 99.9% on a daily sample |
| Availability | The share of time the receiver or API accepts requests | 99.9% monthly |
| Throughput headroom | Peak load as a share of the tightest limit (an API quota, worker capacity) | Below 70% at peak |
| Reject rate | Quarantined records as a share of those processed | Below 1%; every reject triaged within a day |

An **error budget** turns an objective into a decision rule. If the freshness objective permits 5 percent of changes to be late, then over a month the team has a *budget* of lateness. When the budget is spent, reliability work takes priority over new features in the backlog; when plenty remains, the team can ship changes with less caution. It replaces arguments about whether reliability matters with a shared number.

## Designing Alerts

An alert is a request for a human to act, and every unnecessary one reduces the chance that the next, necessary, one is heeded. Four principles guide good alerts.

**Alert on symptoms, not causes.** "Freshness exceeds 15 minutes" tells you the business is affected, whatever the cause. "CPU on worker 3 is 85 percent" tells you very little. Use cause-level signals for diagnosis on a dashboard, and symptom-level signals for paging.

**Every alert has an owner and a first action.** A page that says "something is wrong" is a burden; one that says "freshness is breached; check the queue depth dashboard; runbook section 5" is a lead. Each alert links to its runbook entry.

**Alert on the absence of success.** Many integration failures are silent: the job did not run, the receiver is down, the schedule was disabled. A *heartbeat* alert, which fires when an expected event (a run summary, a successful poll) does *not* occur, catches what error-based alerts cannot.

**Match urgency to impact.** Pages are for conditions that need a human within minutes (the freshness SLO is being burned fast). Tickets are for conditions that need a human within days (the quarantine rate is creeping up). Distinguish them, or everything becomes a page and nothing is heard.

### A Dashboard That Answers the First Five Questions

An operator facing an alert asks five questions in order, and the dashboard should answer them top to bottom:

1. **Is it running?** The last successful run or heartbeat per component.
2. **Is it fresh?** Freshness against its objective.
3. **Is it complete and correct?** Reconciliation drift and sampled mismatches.
4. **Is it healthy?** Error rate by class, retries, queue or consumer lag, dead letter depth.
5. **Is it safe for peak?** Quota use and worker utilization against their limits.

## The Runbook

The runbook is a deliverable, not an afterthought, and its quality is tested only in an incident, when its reader is tired, stressed, and possibly not its author. Keep it in the repository with the code, and structure it so that the answer to "what do I do now?" is a few lines away.

```text
1. Purpose and business impact (one paragraph; tier; objectives)
2. Architecture and data flow; systems, owners, contacts
3. How to: run manually, rerun a period, backfill, pause (kill switch),
   resume
4. Where to look: logs (with example queries), dashboards, quarantine,
   dead letters, run summaries
5. Alerts: each alert, what it means, the first three actions
6. Known failure modes and fixes (the top ten)
7. Secrets and certificates: where they live, rotation steps, expiry dates
8. Replay and reprocessing procedure, with safety checks
9. Recovery and disaster recovery: failover steps, state to restore,
   verification
10. Escalation: source owner, target owner, vendor support, on call
```

Sections 5 and 6 carry the most value. Each alert entry should say what it means, how to confirm it, and the first three actions, written so that someone who has never seen the integration can follow them. The "known failure modes" section grows after every incident: the most reliable runbooks are the ones that have been corrected by real use. Test the runbook by asking someone who did not write it to execute a drill, an expired token, a stopped queue, a quarantined batch, and fix every place they hesitate.

## Post-Incident Reviews

Incidents are the cheapest education an organization gets. Run a short, blameless review for each significant one: the summary and the impact; a timeline in UTC from the first signal to recovery, including how and when it was detected; the root cause, covering both the technical cause and *why it was possible* (a missing test, a missing alert, an unreviewed change); what went well and what did not; and actions, each with an owner, a due date, and a type (prevent, detect, or recover). Then follow through: add the test, update the runbook, change the standard. A review that produces no changes is a story, not a review.

## Summary

Reliability for integrations combines timeouts, bounded retries with backoff, idempotency, circuit breakers, bulkheads, backpressure, dead letters with owners, checkpoints, reconciliation, and replay, and the mechanisms must be reviewed together because each depends on the others. Observability adds structured logs, metrics, and traces; propagating trace context in message headers lets one trace follow a transaction across queues and topics.

Service-level indicators for freshness, completeness, correctness, availability, headroom, and reject rate, with objectives and an error budget, make "reliable" measurable. Alerts should be symptom-based, owned, and actionable, with heartbeat alerts for silent failures and a clear distinction between pages and tickets. A dashboard answers five questions in order; a runbook, tested by someone who did not write it, turns an incident from a crisis into a procedure; and blameless post-incident reviews turn incidents into improvements.

## Exercises

1. **Audit the toolkit.** For one integration, fill in the table: for each failure mode, which mechanism answers it, and who watches that mechanism? Where is the gap?
2. **Define the indicators.** Write the freshness, completeness, and reject-rate indicators for an integration you run, with numeric objectives. How would you measure each today?
3. **Add a heartbeat.** Describe a heartbeat alert for a scheduled job that runs every 15 minutes. What is its threshold, and what does it page?
4. **Run a drill.** Ask a colleague to follow your runbook to handle a simulated expired token. Note every place they hesitated.
