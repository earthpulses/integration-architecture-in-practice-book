# Testing Integrations

Integrations fail at the boundaries. A field changes type. A partner retries. A token expires between two calls. A page of results arrives out of order. A record contains a character nobody expected. Demonstration-driven acceptance, in which someone clicks through a happy path in front of the business owner and everyone nods, finds none of these. It tests that the integration works when nothing goes wrong, which is the one situation that does not need testing.

This chapter gives you a test strategy that finds the failures that matter, with the tools and code to run it in a delivery pipeline. It extends the classic test pyramid with the layers that integrations specifically need, introduces a failure-injection checklist you can apply to any integration, and shows how to turn "it works" into numbers a business owner can sign.

!!! goals "In this chapter"
    * Extend the test pyramid with contract tests, failure injection, and production checks
    * Apply the twelve-row failure-injection matrix to any integration
    * Build a harness that runs the real integration against a mock API behind a fault proxy
    * Write tests for retry behavior, idempotency, and crash recovery, using the companion code as models
    * Use contract tests as a consumer and as a provider
    * Create realistic test data and state acceptance criteria as numbers

## The Integration Test Pyramid

The traditional pyramid has many fast unit tests at the bottom and a few slow end-to-end tests at the top. Integrations need the same shape with three additions, shown in {{ref fig:testing-integration-test-pyramid}}.

{{fig testing-integration-test-pyramid | The test pyramid for integrations. Many fast tests at the bottom, a few slow end-to-end tests at the top, and checks that keep running in production.}}

Contract tests sit in the middle, to catch interface changes before they reach production. Non-functional tests, including failure injection, check how the integration behaves when things go wrong. And a layer of production checks continues the testing after go-live.

{{tbl layers | The layers of integration testing}}

| Layer | What it proves | Tools | Runs |
|---|---|---|---|
| Unit | Mappings, validation, code lists, retry decisions, watermark logic | pytest, JUnit; MUnit for MuleSoft flows | Every commit |
| Contract | Your client still matches the provider's API, and your API still matches what consumers rely on | Schema validation against OpenAPI or AsyncAPI; consumer-driven contracts (Pact); schema-registry compatibility checks | Every commit |
| Integration | Real protocols, real serialization, real databases and brokers | Testcontainers; vendor sandboxes; mock servers generated from OpenAPI (Prism, WireMock) | Every merge |
| Non-functional | Volume, latency, failure behavior, security | k6, JMeter, Gatling; Toxiproxy or similar fault proxies; OWASP ZAP; dependency scanners | Nightly and before release |
| End to end | The business flow works across real systems | Scripted scenarios in a test environment | Before release |
| Production checks | It keeps working: no drift, no silent stops | Reconciliation jobs; synthetic transactions; freshness measurements; run summaries | Continuously |

The unit layer should be the largest by far, and for integrations it is richer than it sounds. The mapping rules, the retry decisions, the watermark arithmetic, and the deduplication logic are all *pure* logic that can be tested without any network at all, in milliseconds. Teams that push everything into slow end-to-end tests end up with a suite that runs for hours and is therefore run rarely.

## The Failure-Injection Matrix

Every integration should pass the twelve checks in {{ref tbl:failinj}} before go-live. Each row is a test you can automate. They are the most valuable testing an integration will receive, because each one corresponds to something that *will* happen in production.

{{tbl failinj | The failure-injection matrix}}

| Inject | Expected behavior | Assert |
|---|---|---|
| Kill the process mid-run | Restart resumes from the checkpoint | No loss and no duplicates in the target |
| Run the same input twice | The second run changes nothing | Target row count and checksums unchanged |
| 429 responses with `Retry-After` | Backs off as told, then succeeds | Request timing and eventual success |
| 503 for ten minutes | Retries with backoff, the breaker opens, alerts fire | No hammering; alert raised; recovery afterward |
| Token expires mid-run | One re-authentication, then continues | No more than one extra token request |
| A malformed record | Quarantined with a reason; the run continues | Reject count and quarantine contents |
| Duplicate webhook or message | Ignored by the deduplication ledger | A single change in the target |
| Out-of-order updates | The stale update is ignored by a version check | Final state equals the latest version |
| Slow network (latency, resets) | Timeouts fire; retries are safe | No hung threads; bounded duration |
| Source schema adds a field or changes a type | An additive change is ignored; a breaking change is quarantined with a clear error | The contract test fails in the build before production |
| Clock skew of minutes | The overlap window absorbs it | No skipped records |
| Production-sized volume | Completes within the window and within limits | Duration, memory, and API calls used |

Some of these need infrastructure. Most do not. The first nine can be tested with the lab server and a few lines of code, which is what the companion test suite does. Here are two real examples from it. The first checks that the client honors the server's `Retry-After`:

```python
def test_retry_after_is_honored(server):
    labserver.CFG.update(rate_limit=3)
    waits = []
    s = client.build_session()
    try:
        for _ in range(8):
            client.request(s, "GET", server + "/orders",
                           params={"limit": 1},
                           sleep=lambda w: (waits.append(w), time.sleep(w)))
    finally:
        labserver.CFG.update(rate_limit=0)
    assert waits and all(w == 1.0 for w in waits)   # the server said 1 s
```

The test configures the server to answer 429 after three requests per second, sends eight requests, records every wait the client chooses, and asserts that each one equals the one second the server demanded. The second checks crash recovery, the first row of the matrix:

```python
def test_watermark_poller_resumes_without_loss(server, tmp_path):
    ...
    before = poller.load_watermark(state)
    requests.post(server + "/admin/touch/A1010")      # a change arrives
    def boom(rec):
        raise RuntimeError("crash")
    with pytest.raises(RuntimeError):
        poller.run_once(s, server, state, boom)       # crash mid-batch
    assert poller.load_watermark(state) == before     # nothing moved
    poller.run_once(s, server, state, upsert)         # next run recovers
    assert got["A1010"]["updatedAt"] > before         # and loses nothing
```

A crash in the middle of a batch leaves the watermark where it was, and the next run delivers the change. Both tests read like specifications of behavior, which is the point: when someone later "improves" the poller by advancing the watermark after each page, the test fails and explains why.

## A Harness That Makes Failures Cheap

Some failures are hard to cause on demand: slow networks, connection resets, a broker that disappears. For these, build a harness in which the integration runs for real against controllable dependencies. {{ref fig:testing-failure-injection-test-harness}} shows the arrangement.

{{fig testing-failure-injection-test-harness | A failure-injection test harness. The real integration runs against a mock API behind a fault proxy, a real Kafka in a container, and a real database in a container. The test asserts the end state.}}

A test runner starts the integration under test (step 1). Its HTTP calls pass through a **fault proxy** that can add latency, drop connections, or reset them (step 2) on their way to a **mock API** generated from the provider's OpenAPI contract (step 3). The integration also produces to and consumes from a real Kafka running in a container (step 4), and writes to a real database in a container (step 5). The test runner then reads the database directly and asserts the end state (step 6). The key idea is that the *integration is real*; only its dependencies are controlled.

Tools exist for each part. A mock server such as Stoplight Prism can be started from an OpenAPI file with one command, `npx @stoplight/prism-cli mock openapi.yaml`, and answers with examples from the contract. Toxiproxy and similar tools sit between client and server and inject latency, bandwidth limits, and resets. Testcontainers starts disposable Kafka brokers and databases from a test, and removes them afterward. The following sketch shows the Kafka part; it needs Docker and is not part of the companion test suite, so treat it as a template to adapt.

```python
from testcontainers.kafka import KafkaContainer
from confluent_kafka import Producer, Consumer

def test_event_roundtrip():
    with KafkaContainer() as kafka:
        bootstrap = kafka.get_bootstrap_server()
        p = Producer({"bootstrap.servers": bootstrap,
                      "enable.idempotence": True, "acks": "all"})
        p.produce("orders.events.v1", key="order-42",
                  value=b'{"status":"SHIPPED","version":3}')
        assert p.flush(10) == 0                  # nothing left undelivered
        c = Consumer({"bootstrap.servers": bootstrap, "group.id": "t",
                      "auto.offset.reset": "earliest"})
        c.subscribe(["orders.events.v1"])
        msg = c.poll(15)
        assert msg is not None and msg.key() == b"order-42"
        c.close()
```

## Contract Testing

A **contract test** checks that two parties still agree on the interface. It is the cheapest way to catch the failure that causes the most production incidents: a change on the other side that nobody told you about.

As the **consumer** of someone else's API, validate every recorded or sandbox response against the provider's OpenAPI document in your build. Keep a *consumer contract*, a small file listing the interactions and fields you rely on (tools such as Pact generate and verify these), and share it with the provider. And fail your build when the provider's published specification changes in a way that breaks you.

As the **provider** of an API or events, lint your contract against your style guide. Verify the consumers' contracts before every release. For events, enforce schema compatibility in the registry and in the build, before anything is produced. The effect is that the provider learns it is about to break a consumer *while the change is still a pull request*, not after it is deployed.

## Test Data

Test data deserves attention, because an integration tested with tidy data is untested. Aim for data that is **realistic but not real**: production-shaped, with personal fields masked or synthesized. Include the ugly cases deliberately: emoji, very long names, leading zeros, every status value, missing optional fields, a record with four hundred lines. Keep **golden files**, pairs of anonymized source records and their expected target output, versioned with the mapping, and run them on every build (Chapter {{ref ch:formats}}). Make the environments **resettable**: a script that puts the sandbox into a known state before each run, so that tests do not depend on what the previous run left behind. And have a **volume generator** that produces production-sized data for load tests; the best time to learn that the job takes nine hours is before go-live.

## Acceptance by Numbers

The business owner signs off acceptance, and a signature on "it works" means little. State the criteria as numbers, agree them in the brief (Chapter {{ref ch:discovery}}), and produce evidence for each.

{{tbl accept | Acceptance criteria stated as numbers}}

| Criterion | Example target | Evidence |
|---|---|---|
| Completeness | 100% of source records present in the target after reconciliation | Reconciliation report |
| Correctness | Zero field mismatches on a random sample of 1,000 records | Sample comparison |
| Freshness | 95% of changes visible within 5 minutes | Freshness metric over a week |
| Resilience | All failure-injection rows pass | Test report |
| Volume | The peak day processed within the window, using under 70% of the API budget | Load-test report |
| Operability | The support team executes the runbook unaided | Signed handover |

The last row connects testing to the gates of Chapter {{ref ch:journey}}: gate three requires this evidence, and gate four requires that the operations team has actually used the runbook. An integration that passes its numbers and has a rehearsed runbook is ready. One that "looked fine in the demo" is a hope.

## Summary

Integrations fail at boundaries, and acceptance by demonstration tests only the happy path. Extend the test pyramid with contract tests in the middle, failure injection beside it, and production checks above it. The unit layer, covering mappings, retry decisions, and watermark logic, is the largest and fastest, and tests pure logic without a network.

Apply the twelve-row failure-injection matrix to every integration: kill it mid-run, run it twice, throttle it, take the target down, expire the token, send bad records, duplicate messages, reorder updates, slow the network, change the schema, skew the clock, and load it to production volume. A harness with a mock API, a fault proxy, and containerized dependencies lets you do so repeatably. Use contract tests as both consumer and provider so interface changes are caught in the pull request. Use realistic, ugly test data and golden files, and state acceptance as numbers backed by evidence.

## Exercises

1. **Run the matrix.** Pick an integration you maintain and run the first nine rows of the failure-injection matrix against it. Which row fails first?
2. **Write the missing test.** Using the companion tests as a model, write a test proving that a duplicate webhook is processed once.
3. **Break a contract.** Take an OpenAPI file, rename a response field, and show how a validation step in your build detects it. Where would the check run?
4. **Define the numbers.** For a real integration, write the six acceptance criteria with numeric targets. Which would the business owner challenge?
