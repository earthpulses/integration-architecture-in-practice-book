# Behavior in Time: The Hard Cases

Static diagrams show structure. They show which boxes exist and which arrows connect them. Integrations, however, fail in *time*: a retry arrives twice, a consumer crashes before it saves its position, a token expires between two calls, a sender gives up waiting for an answer that was in fact sent. None of these can be seen in a box-and-arrow picture, and all of them decide whether an integration is reliable.

This chapter walks through ten of the hard cases as sequence diagrams. A sequence diagram has one vertical line per participant, and time flows downward; each arrow is a message, numbered in order. Where a failure usually strikes, a red lettered circle explains it below the figure. Read each diagram slowly, tracing the numbers, and ask at every step: *what if the process died right here?* That question is the single most useful habit in this book.

!!! goals "In this chapter"
    * Trace ten failure-prone interactions step by step, and say what happens at each possible crash point
    * Explain why a watermark must advance only after a batch succeeds
    * Show how a receiver acknowledges quickly and still processes exactly once
    * Distinguish transient from permanent failure, and describe the circuit breaker's three states
    * Describe how an outbox, a saga, and a consumer group behave when something goes wrong

## Refreshing a Token and Surviving a Surprise 401

Almost every integration begins with authentication, and a surprising share of production outages end there too. {{ref fig:seq-oauth2-client-credentials-with-refresh-and-a}} shows the standard flow for an unattended job, including what to do when a token stops working early.

{{fig seq-oauth2-client-credentials-with-refresh-and-a | OAuth 2.0 client credentials with refresh and a surprise 401.}}

The integration job asks a **token cache** for a token (step 1). The cache has none, or the one it holds is close to expiry (step 2), so it contacts the authorization server with the client's identity and secret (step 3) and receives an access token and its lifetime (step 4). The cache keeps the token until about 80 percent of its lifetime has passed, so that no request is ever sent with a token that expires in flight. The job then calls the target API with the token as a bearer credential (step 5) and receives a normal answer (step 6).

Now the surprise. Between two calls, the token is revoked, perhaps because an administrator rotated the secret, or it expires earlier than the server said it would. The next call (step 7) is answered with `401 Unauthorized` (step 8, failure point A). The correct behavior is exactly one repair: discard the cached token, fetch a new one (step 9), and retry the call once (step 10). If the retry also fails with 401, stop and alert. A loop that retries forever on 401 not only wastes effort; it can lock the account.

Three design rules follow. Use **one shared token provider** with a lock, so that twenty parallel workers that all see an expired token do not make twenty token requests. Allow **one re-authentication per failure**, never more. And **never log the token**, not even in debug output. Chapter {{ref ch:auth}} builds this provider, and Appendix {{ref app:codelab}} contains a tested version.

## Polling with a Watermark, and a Crash in the Middle

The polling pattern of Chapter {{ref ch:patterns1}} looks simple, and its correctness depends on one detail: *when* the bookmark moves. {{ref fig:seq-polling-with-a-watermark-and-a-crash-in-the}} follows a run that crashes halfway.

{{fig seq-polling-with-a-watermark-and-a-crash-in-the | Polling with a watermark, and a crash in the middle.}}

A scheduler wakes the poller every five minutes (step 1). The poller reads the **watermark** from its store (steps 2 and 3): call it T0, the newest change time it has seen so far. It then asks the source for everything modified since T0 minus two minutes (step 4). The deliberate two-minute **overlap** guards against rows that were committed late. The source returns the first page of results with a cursor (step 5), and the poller upserts the page into the target (step 6). It requests the second page (step 7), receives the last page (step 8), and upserts it (step 9).

At failure point A, something goes wrong: the process is killed, or the target rejects a write. What matters is what has *not* happened. The watermark has not advanced, because the poller moves it only after the whole run succeeds. So the next run starts from T0 again, re-reads pages one and two, and repeats the upserts. Because upserts are idempotent, repeating them changes nothing.

Two rules produce reliability. **Move the watermark last**, after every record has been written, and write it atomically (to a temporary file, then rename) so that a crash cannot leave it half-written. And **make the writes idempotent**, so that the overlap and the re-reads, which are certain to occur, are harmless. Together they convert "at least once" delivery into "effectively once" results. The companion code in Appendix {{ref app:codelab}} implements precisely this sequence, and its tests kill the poller mid-batch to prove it.

## A Webhook Receiver That Survives Duplicates

A webhook sender has one worry, whether you received the event, and one tool, retrying. The receiver must therefore expect duplicates. {{ref fig:seq-webhook-receiver-with-a-queue-and-duplicate}} shows a receiver built for them.

{{fig seq-webhook-receiver-with-a-queue-and-duplicate | A webhook receiver with a queue and duplicate protection.}}

The source posts a signed event, e1 (step 1). The receiver verifies the signature and timestamp, then puts the event on a queue (step 2) and immediately answers `200` within milliseconds (step 3). It does *not* process the event; doing so would keep the sender waiting and risk a timeout. Later, a worker takes the event from the queue (step 4) and asks a **dedupe ledger**, "have I seen e1?" (step 5). The answer is no (step 6), so the worker applies the change to the target (step 7) and records e1 in the ledger (step 8).

Now the retry. The sender did not see the `200` in time, perhaps because a network device dropped it, so it sends event e1 again (step 9, failure point A). The receiver again verifies and enqueues it (step 10), and the worker again takes it (step 11). This time the ledger answers yes (steps 12 and 13), and the worker skips it. One event, delivered twice, applied once.

The sequence embodies four rules: **acknowledge fast, process later, deduplicate by event ID, and reconcile on a schedule**. The last one is needed because some senders never retry for long, and none replay events you missed while you were down. A periodic pull of "everything changed since X" repairs the gaps. The verification and ledger code is in Appendix {{ref app:codelab}}.

## Asynchronous Request-Reply

Long-running work, such as a bulk import, should not hold a connection open. {{ref fig:seq-asynchronous-request-reply-202-and-polling}} shows the standard dance.

{{fig seq-asynchronous-request-reply-202-and-polling | Asynchronous request-reply: 202 and polling.}}

The client submits a job with an idempotency key (step 1). The API places it on a queue (step 2) and replies at once with `202 Accepted` and a `Location` header naming a status URL (step 3). A worker takes the job (step 4) and marks it running (step 5). Meanwhile the client polls the status URL (step 6) and is told the job is still running, with a suggestion to wait five seconds (step 7). Later, the worker finishes and records the result (step 8). The next poll (step 9) is answered with `303 See Other`, redirecting to the result (step 10).

At failure point A the result is only retained for a limited time: collect it within the retention window, or it vanishes. Make the submission idempotent, so that a retry after a lost `202` does not start the job twice, honor the suggested polling interval, and set an overall timeout so that a stuck job does not make the client wait forever.

## A Saga with a Failing Step

When a business transaction spans systems, each step must be undoable. {{ref fig:seq-saga-with-a-failing-step-and-compensation}} shows an orchestrated saga that fails at the third step.

{{fig seq-saga-with-a-failing-step-and-compensation | A saga with a failing step and compensation.}}

The orchestrator creates the order in a pending state (steps 1 and 2) and asks the inventory service to reserve stock (steps 3 and 4). It then asks the payment service to charge the card (step 5), and the card is declined (step 6, failure point A). The saga now *compensates in reverse order*: it releases the reserved stock (step 7) and cancels the order (step 8). The customer sees a clear failure, and no stock is stuck in a reservation nobody will claim.

Two facts make this work. The orchestrator **persists the saga's state before each step**, so that if it crashes mid-way it can resume or compensate after a restart. And **every step and every compensation is idempotent and retryable**, because the orchestrator itself may retry them. A compensation that cannot be repeated safely is a defect waiting for its first outage.

## The Outbox, Followed by Change Data Capture

The outbox pattern solves the dual-write problem, and its failure behavior is subtle enough to deserve a sequence. {{ref fig:seq-transactional-outbox-with-cdc}} shows it with a change-data-capture relay.

{{fig seq-transactional-outbox-with-cdc | The transactional outbox with change data capture.}}

The service writes the order and its outbox row in *one transaction* (step 1), and the database confirms (step 2). A CDC connector, tailing the database's transaction log (step 3), sees the new outbox row (step 4) and publishes an event to Kafka with the order ID as the key (step 5). A consumer polls (step 6), receives the event (step 7), and applies it idempotently before committing its position (step 8).

The weak spot is at failure point A. If the connector restarts after publishing the event but before saving its own position, it will read the same log entry again and publish the event a second time. The outbox cannot prevent that: it guarantees that the state change and the event are never *separated*, not that the event is delivered only once. So consumers must deduplicate, by event ID or by a version number on the entity. The sequence also reminds us of an important truth about this class of tools: "exactly once" holds within a boundary, and the moment data crosses to something outside it, you are back to at least once.

## Kafka: Produce, Consume, Crash, Redeliver

Kafka's consumer model is easy to describe and easy to misunderstand. {{ref fig:seq-kafka-produce-consume-crash-redelivery}} follows one batch through a crash.

{{fig seq-kafka-produce-consume-crash-redelivery | Kafka: produce, consume, crash, redelivery.}}

A producer sends with `acks=all` (step 1), meaning it waits until every in-sync replica has the record. The partition leader replicates to a follower (step 2), the follower acknowledges (step 3), and the producer receives an acknowledgment carrying the offset, 98 (step 4). A consumer whose last committed offset is 95 fetches from offset 95 (step 5) and receives records 95 to 98 (step 6). It processes them against the target (step 7).

Then it crashes *before committing its offset*. The committed offset is still 95. When the consumer restarts, or another member of the group takes over the partition, it fetches from 95 again (step 8), receives records 95 to 98 again (step 9), and reprocesses them (step 10). Only then does it commit offset 99 (step 11).

This is correct behavior, and it is **at-least-once delivery** in action. The consumer chose to commit *after* processing, which means a crash causes repeats but never losses. The alternative, committing before processing, would mean a crash causes losses but never repeats. For integrations, repeats you can handle are almost always preferable to losses you cannot see, so the rule is: process, then commit, and make processing idempotent. Chapter {{ref ch:kafka1}} explains offsets and commits in depth.

## Backoff, the Circuit Breaker, and the Dead Letter Queue

When a target fails, how a consumer reacts determines whether the outage stays small. {{ref fig:seq-backoff-circuit-breaker-and-dead-letter}} shows three mechanisms working together.

{{fig seq-backoff-circuit-breaker-and-dead-letter | Backoff, circuit breaker, and dead letter.}}

The consumer calls the target through a **circuit breaker** (steps 1 and 2) and receives `503` (step 3), so the breaker reports an error (step 4, failure point A). The consumer waits using **exponential backoff with full jitter**, honoring `Retry-After` if the server sent one, and tries again (steps 5 to 7). After the failures reach a threshold, the breaker *opens*: the consumer's next call fails immediately, without even reaching the target (steps 8 and 9). This protects the struggling target from being hammered, and it protects the consumer from wasting threads on doomed calls. The right response at this point is to *pause consumption* rather than to discard messages.

After a cool-down, the breaker goes *half-open* and lets a single probe through (step 10). If it succeeds (step 11), the breaker closes and normal consumption resumes (step 12). A breaker has three states: closed (normal), open (failing fast), and half-open (testing recovery).

Later in the diagram, a different record produces a **permanent** error: a malformed message that the target rejects with `400` (failure point B). Retrying will never help. The consumer parks it, with the reason, in the **dead letter queue** and moves on. The ability to tell transient failures from permanent ones is what separates a resilient consumer from one that either loses data or blocks forever. Chapter {{ref ch:python}} implements the retry decision, and Chapter {{ref ch:kafka2}} shows how Kafka-based consumers do the same with retry topics.

## Bidirectional Sync Without an Echo

The authority split avoids bidirectional synchronization when it can, but sometimes both systems must edit. {{ref fig:seq-bidirectional-sync-without-an-echo-loop}} shows how to prevent the most notorious failure, the echo loop.

{{fig seq-bidirectional-sync-without-an-echo-loop | Bidirectional sync without an echo loop.}}

The sync service asks System A for changes since its checkpoint (step 1) and finds an edit by a person, Alice, at 10:00:03 (step 2). It asks System B for changes since *its* checkpoint (step 3) and finds no new human edits (step 4). It takes a lock on the record, a lease of 60 seconds so that a crashed service does not hold it forever (step 5), applies Alice's change to System B, stamping the change with its origin, A (step 6), releases the lock (step 7), and advances the checkpoint for System A (step 8).

On the next cycle, the service asks System B for changes (step 9) and finds one: an edit made at 10:00:10 by the integration's own user (step 10, failure point A). This is the echo, the change the service itself just made. If it were treated as a new edit, it would be copied back to System A, which would then show a change that the service would copy to System B, and so on forever. The defense is to **ignore changes made by the integration's own identity**, which is why the integration needs a dedicated service account, and to stamp changes with their origin as a second safeguard.

## A Consumer Group Rebalance

When members join or leave a Kafka consumer group, the partitions are redistributed. {{ref fig:seq-consumer-group-rebalance-classic-versus-incr}} contrasts the older eager protocol with the newer incremental ones.

{{fig seq-consumer-group-rebalance-classic-versus-incr | A consumer group rebalance: classic versus incremental.}}

Consumer A joins the group (step 1) and is assigned all three partitions, P0 to P2 (step 2), and starts consuming. Consumer B then joins using the classic *eager* protocol (step 3). The coordinator tells Consumer A to **revoke all** its partitions (step 4); Consumer A rejoins (step 5), and the coordinator assigns P0 and P1 to A (step 6) and P2 to B (step 7). During this exchange, *nobody consumes anything*: a stop-the-world pause that grows with the size of the group.

With incremental protocols (cooperative rebalancing, and the newer consumer protocol described in Chapter {{ref ch:kafka2}}), only the partitions that must move are interrupted: P2 is handed from A to B while A keeps consuming P0 and P1. Static group membership further avoids needless rebalances when a consumer restarts quickly. For integrations, the practical consequence is that rebalances cause duplicates, because uncommitted work on a revoked partition is redone by the new owner. This is one more reason that idempotency, not luck, is the foundation of a streaming consumer.

## Reading Sequence Diagrams in Design Reviews

You can apply what these ten sequences teach to any design review. Draw the sequence for the integration under review, and at every arrow ask three questions.

1. **What if this message is lost?** Does the sender know? Will it retry? What stops the retry from causing harm?
2. **What if this step runs twice?** Is it idempotent? What is the key that makes it so?
3. **What if the process dies between this step and the next?** What state survives? Where does the process resume?

If you ask these questions at every arrow, you will find most of the defects that would otherwise appear in production. Most architects find, after a few reviews, that the habit becomes automatic.

## Summary

Integrations fail in time, and sequence diagrams make time visible. A token provider refreshes once per failure and alerts on a second 401. A poller advances its watermark only after the batch succeeds, and re-reads an overlap that idempotent writes make harmless. A webhook receiver acknowledges fast, processes later, and deduplicates by event ID. Asynchronous request-reply separates submission from collection and needs idempotent submits and result retention. A saga undoes its steps in reverse with idempotent compensations.

The outbox guarantees state and event are never separated but not that events are delivered once. A Kafka consumer that commits after processing repeats work rather than losing it. A circuit breaker stops hammering a failing target, and a dead letter queue holds permanent failures. Bidirectional sync ignores its own edits, and group rebalances cause duplicates. Three questions asked at every arrow, what if it is lost, what if it runs twice, what if the process dies here, find most design defects early.

## Exercises

1. **Trace a crash.** Take the polling sequence and, for each of the nine numbered steps, write what state exists if the process dies immediately afterward, and what the next run does.
2. **Draw your own.** Choose an integration you know and draw its sequence diagram with participants as columns. Apply the three questions at every arrow. Which arrow is the weakest?
3. **Retry or park?** List ten error responses an API can return (for example 400, 401, 404, 409, 429, 500, 502, 503, 504, a connection reset). Classify each as transient or permanent, and state what your consumer should do.
4. **Break the poller.** Using the companion code, run the poller test that kills a batch midway, and then change the code to advance the watermark after each page instead of at the end. What does the test now report, and why?
