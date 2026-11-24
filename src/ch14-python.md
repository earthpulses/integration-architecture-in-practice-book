# Python Clients That Survive Production

Python with the `requests` library is the most common way to build REST integrations, and for good reasons: it is quick to write, easy to read, and every team has someone who knows it. The difference between a *script* and an *integration* is a handful of habits. A script runs once on a developer's laptop, against a healthy API, and its author watches it finish. An integration runs unattended at 03:00, against an API that is occasionally slow, occasionally down, and sometimes returns surprises, and nobody watches it at all until something goes wrong.

This chapter teaches the habits that make the difference, and shows them in working code from the book's companion repository: a hardened HTTP client, a paginating reader, a watermark poller with atomic checkpoints, a rate limiter, and a run loop that quarantines bad data. Every listing here is exercised by automated tests, including tests that kill the process halfway through a run, so you can trust the behavior and adapt the code to your own work.

!!! goals "In this chapter"
    * Apply seven habits that distinguish an integration from a script
    * Build an HTTP client with timeouts, bounded retries, exponential backoff with full jitter, and `Retry-After` support
    * Explain why only some requests may be retried, and how an idempotency key changes that
    * Read large collections with generators and cursors, and checkpoint progress safely
    * Implement an incremental sync with a watermark, an overlap window, and an atomic checkpoint
    * Stay within an API's rate limit with a token bucket, and run work with bounded concurrency
    * Quarantine bad records, report run summaries, and structure a project that others can maintain

## The Seven Habits

Each of the seven habits below corresponds to a failure that happens, sooner or later, in every production integration. Learn them as a set.

**1. Always set timeouts.** The `requests` library has no default timeout. A connection that hangs, because a firewall silently dropped it or a server stopped answering mid-response, will hang your job forever, and nothing will be logged because nothing has happened yet. Always pass a `(connect, read)` tuple, for example `(5, 30)`: five seconds to establish a connection and thirty to wait for data.

**2. Retry only what is safe.** Retry on 429, 500, 502, 503, 504, and network errors, because these are usually transient. Do not blindly retry a `POST` that creates something, unless it carries an idempotency key, because you may create it twice.

**3. Back off with jitter.** Retrying immediately, or at fixed intervals, hammers a struggling server and synchronizes every client into waves. Wait exponentially longer after each failure, and add randomness.

**4. Page with generators.** Stream results lazily, so memory stays flat however large the collection, and keep the cursor so you can resume.

**5. Make writes idempotent.** Upsert by external ID. A rerun must produce the same end state as a single run, because reruns *will* happen.

**6. Log with correlation.** Every log line should carry the run ID, the entity ID, and the endpoint, so one search finds the whole story. Never log secrets, or payloads containing personal data.

**7. Fail loudly, park gently.** One bad record must not stop a run of a million; it goes to a quarantine with its reason, and the run summary reports the count. But a systemic failure, such as a target that is down or a bug in your own code, must stop the run and raise an alarm rather than being swallowed.

## A Hardened HTTP Client

The client below puts habits 1 to 3 into about eighty lines. It is a module of the companion code, and we will walk through it in pieces.

{{code client.py}}

### What Gets Retried, and What Does Not

The first design decision is in two constants at the top. `RETRY_STATUS` lists the status codes that usually mean "try again later": 429 (too many requests) and the 5xx server errors. `SAFE_METHODS` lists the HTTP methods that are idempotent: `GET`, `HEAD`, `PUT`, `DELETE`, and `OPTIONS`. In `request`, a call is `retryable` only if its method is in that list *or* the caller supplied an `Idempotency-Key` header. A plain `POST` is therefore never retried, which is the correct default: a failure leaves you not knowing whether the order was created, and the safe action is to look rather than to repeat. The companion tests prove it: a `POST` against a server that always fails is attempted exactly once, while the same request with an idempotency key is retried and replayed safely.

Network errors, such as a connection reset or a timeout, follow the same rule. If the method is not retryable, the exception propagates immediately; if it is, the client waits and tries again, up to `max_attempts`.

### Backoff with Full Jitter

When a retry is warranted, how long should the client wait? Waiting a fixed second is better than nothing, and waiting longer after each failure is better still: that is **exponential backoff**, in which the delay doubles each time up to a cap. But exponential backoff alone has a flaw. If a hundred clients all hit an outage at the same moment, they all retry at the same moments, in synchronized waves, which can keep a recovering server down. {{ref fig:backoff-jitter}} shows the effect.

{{fig backoff-jitter}}

The fix is **jitter**: randomness. The function `backoff_delay` implements the "full jitter" strategy, which waits a random time between zero and the exponential ceiling: `random.uniform(0, min(cap, base * 2 ** attempt))`. The load spreads out, and the server sees a trickle instead of a wave. With `base=0.5` and `cap=30`, the ceilings are 0.5, 1, 2, 4, 8, 16, and then 30 seconds.

### Honoring Retry-After

Backoff is a guess; `Retry-After` is the server telling you the answer. When a 429 or 503 response carries that header, the client uses it instead of its own computation. The header comes in two forms, a number of seconds (`Retry-After: 3`) or an HTTP date, and `parse_retry_after` handles both, returning `None` for anything it cannot understand, in which case the client falls back to backoff. The companion test points the client at a server limited to three requests per second and verifies that every wait the client chooses equals the one second the server demanded.

### One Re-Authentication

The `refreshed` flag implements the rule from Chapter {{ref ch:time}}: on a 401, discard the cached token, fetch a new one, and retry *once*. A second 401 is raised as an error. Without the flag, a revoked credential would produce an endless loop of token requests, and a loop of failed logins can lock the account.

### Raising Meaningful Errors

Finally, any status of 400 or above that is not retried becomes an `ApiError` carrying the status, the first 200 characters of the body, and the URL. That small convenience matters at 03:00: the log line says "422 from https://…/orders: field quantity must be between 1 and 99," and the cause is visible without a debugger.

## Reading Large Collections with Generators

The `iter_records` function at the bottom of `client.py` reads a cursor-paginated collection as a stream. A *generator* produces one record at a time and pauses between requests, so memory use stays flat whether the collection holds a hundred records or a hundred million. Three details deserve attention. After the first page, the parameters become only `cursor` and `limit`, because, as Chapter {{ref ch:readdocs}} warned, many APIs reject a request that mixes a cursor with other filters. The loop is bounded by `max_pages`, so a server bug that returns the same cursor forever causes an error instead of an infinite loop. And because the function is a generator, the caller can stop early and resume later by saving the cursor.

```python
for order in iter_records(session, BASE + "/orders", limit=200):
    handle(order)          # one record at a time; memory stays flat
```

## Watermarks and Checkpoints

The most common synchronization job reads "everything that changed since last time." Two ideas make it reliable: a **watermark** that records how far you have read, and an **overlap** that guards against late-committed rows. {{ref fig:watermark-overlap-timeline}} shows the failure that overlap prevents.

{{fig watermark-overlap-timeline}}

A row can be *modified* at 09:59:58 but only become *visible* to queries at 10:00:03, because its transaction committed late. If the job's first run ended at 10:00:00 and stored that as the watermark, the second run asks for changes since 10:00:00, and the row, whose timestamp is earlier, is never returned. It is missed forever, with no error anywhere. The remedy is to reach back: each run asks for changes since the watermark *minus a safety margin*, here two minutes. Re-reading a few rows is harmless if the writes are idempotent, and the late row is caught.

{{code poller.py}}

The module implements the whole discipline in about thirty lines. `run_once` loads the watermark, subtracts the overlap, reads every changed record through the paginating generator, upserts each (the callback `upsert` must be idempotent, because the overlap repeats rows), and tracks the newest `updatedAt` it saw. Only after the loop completes does it save the new watermark, with `save_watermark`.

That function is worth reading closely. It writes the value to a temporary file in the same directory, flushes it, forces it to disk with `fsync`, and then calls `os.replace`, which atomically swaps the new file in. A crash at any instant leaves either the old watermark or the new one, never a half-written file. And because the watermark is saved *last*, a crash in the middle of a batch leaves it unchanged: the next run starts from the same point, re-reads the same records, and the upserts make the repetition harmless. The companion test proves exactly this. It makes the upsert callback raise an error halfway through, asserts that the watermark did not move, and then verifies that a following run captures every change.

!!! why "Why this matters"
    The two rules, *move the watermark last* and *make the writes idempotent*, convert "at least once" processing into "effectively once" results. The overlap and the re-reads are not a defect to be eliminated; they are the price of safety, and idempotency is how you pay it.

Use the **source's timestamps**, never your own clock, to compute the watermark. Your clock and the server's differ by seconds or minutes, and any difference in the wrong direction skips rows. Store the watermark in UTC, with the precision the source provides.

## Staying Within the Rate Limit

An integration that reads or writes fast enough will meet the API's rate limit. Backoff on 429 is the safety net, but a well-behaved client avoids hitting the limit in the first place by *pacing itself*. Start with arithmetic. If the API allows 300 requests per minute, that is five per second; plan for four, which leaves 20 percent headroom for other integrations sharing the same limit. A job that must make 36,000 calls therefore needs at least 9,000 seconds, two and a half hours, and no amount of parallelism will change that. If the window is shorter, look for bulk endpoints.

The standard pacing tool is the **token bucket**. Imagine a bucket that holds up to `burst` tokens and is refilled at `rate` tokens per second. Each request takes one token; if the bucket is empty, the caller waits until a token arrives.

{{code ratelimit.py}}

The `acquire` method computes how many tokens have accumulated since the last call, takes one if available, and otherwise sleeps for exactly the time needed, *outside* the lock so that other threads are not blocked. Injecting the clock and sleep function, as the constructor does, lets the test run in virtual time: with a rate of two per second and a burst of two, six acquisitions complete after exactly two seconds of waiting.

### Bounded Concurrency

Concurrency can speed up an integration that waits on the network, but only within limits. Use a small, fixed pool of workers, such as four, with a *shared* token bucket so that the pool as a whole respects the API's budget, and a shared token provider (Chapter {{ref ch:auth}}) so that they do not each refresh credentials. A pool of 50 threads hitting a vendor with a limit of five per second does not finish sooner; it produces 429s, retries, and a lot of heat. Concurrency is also a risk to *ordering*: if two records for the same entity are processed in parallel, the older update may land last. Partition the work by entity key so that each key is handled by one worker at a time.

## Quarantine Instead of Crash

Habit seven is about proportion. A single malformed record should not stop a million good ones, and a systemic failure should not be mistaken for a bad record. The run loop below makes the distinction explicit.

{{code runloop.py}}

The convention is simple. If processing a record raises `ValueError`, the *data* is at fault, so the record is written to a quarantine file with its reason and the run continues. Any other exception, such as a network failure after retries or a bug in the mapping, propagates and stops the run, because continuing would hide the problem. At the end, the loop logs a **run summary**: records read, written, and quarantined, keyed by a run ID. That summary is the most useful single line an integration emits. Alert if the quarantine count rises above a threshold, such as one percent, and alert if a scheduled run produces no summary at all, a *heartbeat* check that catches the integration that silently stopped.

## Logging You Can Use at 3 A.M.

When an integration fails, the log is the only witness. Structured logs, in which every line is a set of named fields rather than a sentence, can be searched and counted.

```json
{"ts":"2026-11-23T09:14:07.311Z","level":"WARN","service":"orders-sync",
 "run_id":"r-20261123-0905","entity":"order","entity_id":"A1043",
 "action":"create","target":"erp","outcome":"quarantined",
 "reason":"unmapped sku TENT-9X","duration_ms":182}
```

Every line carries a run ID, so one search retrieves a whole run; an entity ID, so one search retrieves one order's history; and an outcome and reason as fields, so a dashboard can count them. It carries no payloads containing personal data, and never a token or a secret. Chapter {{ref ch:reliability}} extends the idea to traces that follow a transaction across systems.

## A Project Layout Others Can Maintain

An integration lives for years and is maintained by people who did not write it. A conventional layout makes it easy to enter.

```text
orders-sync/
  README.md              what it does, how to run it, who owns it
  pyproject.toml         dependencies pinned; Python version stated
  src/orders_sync/
    client.py            the hardened HTTP client
    tokens.py            the token provider
    mapping.py           typed models and the mapping rules
    poller.py            the incremental sync
    runloop.py           quarantine and run summaries
    config.py            reads settings from the environment; fails fast
  tests/
    test_client.py       retry, backoff, Retry-After behavior
    test_mapping.py      golden-file tests
    golden/              real, anonymized records with expected outputs
  deploy/                container definition and deployment scripts
  runbook.md             alerts, symptoms, first actions, contacts
```

Three conventions repay the effort. **Configuration comes from the environment**, and the program validates it at start-up and fails fast with a clear message if something is missing. **Dependencies are pinned**, so that a build in six months produces the same behavior. And **the runbook lives with the code**, so that it changes in the same review as the behavior it describes.

## Proving It

Claims such as "it handles restarts" are opinions. Tests make them facts, and the companion test suite for this chapter's code checks, among other things, that a poller killed mid-batch does not advance its watermark and loses nothing on the next run; that the client honors the server's `Retry-After` exactly; that a `POST` without an idempotency key is attempted once; that a flaky server returning 503 half the time still yields every record; that a revoked token triggers exactly one refresh; and that a run containing bad records quarantines them and finishes. Chapter {{ref ch:testing}} explains how to build such a suite for your own integrations, including a failure-injection checklist.

## Summary

The difference between a script and an integration is seven habits: always set timeouts, retry only what is safe, back off with jitter, page with generators, make writes idempotent, log with correlation, and fail loudly while parking bad records gently. A hardened client retries only idempotent methods or requests with an idempotency key, honors `Retry-After` before computing its own full-jitter backoff, refreshes a rejected token exactly once, and raises errors that say what failed.

Incremental sync depends on a watermark that moves only after the whole batch succeeds, written atomically, plus an overlap window that guards against late-committed rows and idempotent upserts that make the repetition harmless. A token bucket paces requests below the API's limit, concurrency stays bounded and partitioned by key, and a run loop quarantines bad data, stops on systemic errors, and emits a run summary. A conventional project layout with environment configuration, pinned dependencies, and an in-repository runbook makes the whole thing maintainable by someone else.

## Exercises

1. **Watch the retries.** Start the lab server with `--flaky 0.3`, run the client against it, and print each wait the client chooses. Do the waits grow? Do they ever exceed the cap?
2. **Prove atomicity.** Modify `save_watermark` to write the file directly instead of using a temporary file and `os.replace`. Describe a crash timing that would corrupt it, and why the original cannot be corrupted that way.
3. **Size a job.** An API allows 600 requests per minute, shared among three integrations. Your job must update 90,000 records, one call each. How long will it take at a fair share of the budget, and what would you ask the vendor for?
4. **Add a metric.** Extend `process` to count records that took more than one second, and include that count in the run summary. What alert would you attach to it?
