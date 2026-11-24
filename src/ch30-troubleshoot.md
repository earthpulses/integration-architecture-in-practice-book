# A Troubleshooting Field Guide

When an integration fails, the person on the other end of the pager is rarely the person who built it. They are tired, they have a business user waiting, and they need a way to narrow a very large space of possible causes to the one that matters. This chapter is for that person. It gives a method first, because a method works on problems nobody has seen before, then a set of symptom tables for the failures that recur, and finally a short list of the evidence to gather before asking a vendor or another team for help.

The tables collect, in one place, material from earlier chapters, with pointers to the chapter that explains each fix. Use them as an index into the book.

!!! goals "In this chapter"
    * Apply a five-question method that narrows any failure to its layer
    * Bisect a data path to find where records stop
    * Recognize the common symptoms of connectivity, authentication, data, synchronization, messaging, performance, and delivery failures
    * Collect the evidence that lets a vendor or colleague help you quickly

## The Five-Question Method

Most integration failures yield to five questions, asked in order. They are cheap, and skipping them to chase a clever theory is the most common way to lose an afternoon.

**1. What changed?** Almost every failure follows a change: a deployment, a configuration edit, a credential rotation, a vendor release, a certificate expiry, a network change, a new data pattern, a volume spike. Ask for the change log of *every* party, not just yours. If nothing changed in your system, ask the other side; if nothing changed anywhere, look at time (a certificate that reached its expiry date is a change nobody made).

**2. Where does the flow stop?** *Bisect the path.* A record travels from source through several stages to the target. Check the middle: is it in the queue? Is it in the log? Did the worker see it? The answer halves the search. Trace identifiers (Chapter {{ref ch:reliability}}) make this a search, not an investigation; without them, pick a record and follow it by hand.

**3. Is it the connection, the credential, the data, or the capacity?** These four categories cover most failures. A connection failure shows as timeouts, resets, and DNS errors; a credential failure as 401 and 403; a data failure as 400 and 422, or as a quarantine; a capacity failure as 429, slowness, and growing lag.

**4. Can I reproduce it by hand?** A `curl` call from the runtime's own host, with the same credentials, removes your code from the equation. If `curl` fails, the problem is not your code; if it works, the problem is in it.

**5. What does the evidence say?** Read the actual error body, the actual log line, the actual response headers. The most expensive mistake in troubleshooting is the theory formed before looking.

!!! tip "The first ten minutes"
    Check the dashboard's five questions (Chapter {{ref ch:reliability}}): running, fresh, complete and correct, healthy, safe for peak. Then the change log. Then bisect. Most incidents are located within ten minutes by following that order, and the remainder are the ones that deserve a fresh look.

## Connectivity and Network

{{tbl tconn | Connectivity and network symptoms}}

| Symptom | Likely cause | Fix |
|---|---|---|
| Works from a laptop, fails from the server | A firewall or proxy; egress addresses not allowlisted; DNS differs | Trace the path from the server; check proxy settings; compare DNS answers |
| TLS handshake errors | TLS inspection with a private authority; an expired certificate; wrong trust store | Add the authority to the runtime's trust store; check expiry; never disable verification |
| Intermittent resets on long requests | An idle timeout on a load balancer or firewall | Set client keepalives and timeouts below the shortest idle timeout |
| Timeouts only at certain hours | A batch window or maintenance on the target; a shared link saturated | Check the target's calendar; measure link use; move the schedule |
| Large payloads fail, small ones work | MTU or fragmentation; a gateway size limit | Check path MTU; raise gateway limits; use a claim check |

## Authentication

Chapter {{ref ch:auth}} contains a full table; the most common patterns are repeated here as pointers. A 401 immediately after obtaining a token usually means the wrong audience or scope. A 401 after exactly N minutes means the token expired and nothing refreshed it. A 403 on some endpoints only means a missing scope or role. Intermittent 401s with parallel workers usually mean each worker is refreshing its own token and invalidating the others', so share one token provider.

## Data and Mapping

{{tbl tdata | Data and mapping symptoms}}

| Symptom | Likely cause | Fix |
|---|---|---|
| Garbled characters (for example "Ã©" instead of "é") | UTF-8 read as Latin-1, or the reverse | Declare and enforce UTF-8 at every hop; test with accented characters |
| Totals off by a cent | Floating-point money or inconsistent rounding | Decimals end to end; one rounding rule in the mapping |
| Identifiers lose leading zeros | Identifiers parsed as numbers, often by spreadsheets | Treat identifiers as strings in schemas and code |
| Records rejected for a missing field that the source documents | The field is optional in some conditions, or renamed | Compare real responses with the contract; update the mapping |
| A status value rejected or skipped | No entry in the mapping table | Add the mapping; the integration should log and skip, not guess |
| Fewer fields returned than documented | Field-level security or role permissions on the integration user | Test with the integration user's real permissions |

## Synchronization and State

{{tbl tsync | Synchronization symptoms}}

| Symptom | Likely cause | Fix |
|---|---|---|
| Records missing around a clock change | Local-time watermarks | UTC and timezone-aware datetimes; overlap windows; a test for daylight-saving transitions |
| Duplicates after a rerun | Non-idempotent writes; wrong match key | Upsert by a stored foreign ID; deduplication ledger |
| Deleted records still in the target | No delete detection | Soft-delete mapping or a periodic ID comparison, with a deletion guard |
| Two systems keep overwriting each other | No authority split; echo loop | Per-field authority; ignore the integration's own edits |
| Imports create duplicates instead of updates | The wrong coalesce or external-ID field in the import mapping | Fix the key; deduplicate; add an idempotency test |
| Counts differ after an incident | Missed window with no repair path | Run the reconciliation; extend it to run after incidents |

## Messaging and Kafka

Chapter {{ref ch:kafka2}} contains the full Kafka matrix. The most common patterns: lag that grows steadily means a slow consumer, a hot partition, or a throttled target; duplicates in the target mean at-least-once delivery meeting a non-idempotent sink; frequent rebalances mean processing that outlasts `max.poll.interval.ms` or an autoscaler that flaps; and a trace that stops at a queue means the trace context is not carried in message headers.

## Performance

{{tbl tperf | Performance symptoms}}

| Symptom | Likely cause | Fix |
|---|---|---|
| Works in test, times out in production | Sandbox data volume or limits differ | Test at production volume; list sandbox differences |
| The job gets slower each run | Offset pagination that deepens; an unbounded state | Cursor paging; bound state; check for growth |
| 429 responses under parallel load | The concurrency exceeds the shared limit | A token bucket; bounded workers; ask for a larger allocation |
| One slow dependency stalls everything | No bulkheads | Separate pools or queues per target |
| Memory grows without bound | Loading a whole collection instead of streaming | Generators and bounded batches |

## Delivery and Environments

{{tbl tdeliv | Delivery symptoms}}

| Symptom | Likely cause | Fix |
|---|---|---|
| Duplicates after a blue-green release | Old and new consumers both processing | Hand over consumption deliberately; idempotent processing |
| Works in test, not in production, with the same code | Configuration differences; sandbox differences | Diff configuration; run a shadow run in pre-production |
| A flow behaves differently after a platform upgrade | A changed default | Read the release notes; add regression tests for defaults you rely on |
| Change notifications stopped silently | An expired subscription | Renew on a schedule; reconcile with a delta query |
| Documents stuck in an error status | Unmonitored error queue or status in a target system | Assign an owner; alert on the status; reprocess after fixing the data |

## Before You Escalate

When the cause lies with a vendor or another team, you will get help faster with evidence than with adjectives. Gather the following before you raise the ticket.

* **A minimal reproduction:** the smallest request or action that fails, ideally as a `curl` command that anyone can run.
* **Exact timestamps in UTC,** with the time zone stated, and the request or correlation IDs.
* **The full error response,** body and headers, not a paraphrase.
* **What changed,** and when, on your side.
* **What you have ruled out,** so nobody re-checks it.
* **The business impact and urgency,** in one sentence.

A ticket with these six things is often resolved in one reply. A ticket that says "your API is broken" begins a long conversation.

## Summary

Troubleshooting is a method before it is a list. Five questions, what changed, where does the flow stop, is it the connection, credential, data, or capacity, can I reproduce it by hand, and what does the evidence say, locate most failures in ten minutes. Symptom tables for connectivity, authentication, data, synchronization, messaging, performance, and delivery serve as an index into the book's earlier chapters. And when you must escalate, a minimal reproduction, exact timestamps, the full error, the change history, what you have ruled out, and the business impact turn a vendor ticket from a conversation into a fix.

## Exercises

1. **Bisect a path.** Draw the path of one record through an integration you operate. At which three points could you check it? How would you check each?
2. **Reproduce by hand.** Take a call your integration makes and reproduce it with `curl` from the integration's own host. What differs from your code's behavior, if anything?
3. **Add to the tables.** Write three symptom rows from your own incidents, with cause and fix.
4. **Write a ticket.** Rewrite a vendor ticket you once sent, using the six pieces of evidence. What was missing?
