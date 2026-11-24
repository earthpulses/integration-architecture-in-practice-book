# What Integration Really Is

It is Monday morning at Larkspur Outdoor, a mid-sized company that sells camping gear online in six countries. The warehouse manager is staring at a spreadsheet. Over the weekend the web shop took 3,100 orders. The company's ERP system, the system that actually reserves stock, prints pick lists, and issues invoices, knows about none of them yet. Each night an export job writes a CSV file from the shop, and each morning someone opens that file, fixes the rows that the import rejected, and uploads it by hand. This morning the file has 214 rejected rows, and customers are already emailing to ask why their tents have not shipped.

Nothing here is broken in the way engineers usually mean it. The shop works. The ERP works. The export job runs. What is missing is the connection between them, and that connection has to answer questions that neither system was built to answer. How quickly should an order reach the ERP? What should happen when the ERP is down for maintenance? What if the same order arrives twice? Who is allowed to change a price? Who finds out when something goes wrong, and how?

That is integration. It is the work of making independently built systems behave, from the business's point of view, like one system. This chapter gives you the vocabulary and the mental models for the rest of the book. By the end of it you will have read a raw HTTP exchange, written a small client, and met the one idea, idempotency, that explains more integration failures than any other.

!!! goals "In this chapter"
    * Define integration in terms of meaning, time, and failure rather than technology
    * Distinguish the four basic ways systems exchange information, and know when each fits
    * Read an HTTP request and response, including the status codes and headers that matter
    * Explain idempotency and why safe retries depend on it
    * Build and run a first integration against a local test API

## Integration Is About Meaning, Time, and Failure

The simplest definition of integration is "moving data from one system to another." It is also the least useful, because it hides everything that makes the work hard. A better definition is that an integration is a *contract between systems that were not built together*. The contract covers three things.

**Meaning.** The shop calls a customer record `customer`, with a `fullName` field and an email address. The ERP calls it a *business partner*, splits the name into first and last parts, and requires a tax region the shop never collects. Moving the fields is easy. Deciding what a "customer" is, who owns the definition, and what to do when the two systems disagree is the real work. Chapter {{ref ch:formats}} covers mapping in depth.

**Time.** The shop wants to take an order at any hour. The ERP has a nightly batch window during which it refuses connections. The shop's marketing team changes prices on Black Friday at 06:00; the ERP's price list changes on the first of the month. Systems live on different clocks, and an integration must say what "up to date" means: seconds, minutes, or tomorrow. That promise, usually called *freshness*, shapes the whole design.

**Failure.** Networks drop connections. Servers restart. A vendor's API starts returning errors at 02:14 and recovers at 02:31. A deployment changes a field name. An integration spends most of its life in the narrow gap between "everything works" and "everything is down", where some requests succeeded, some failed, and nobody is sure which. Good integrations are designed around the gap.

Every integration you will ever meet answers the same five questions, whether or not the people building it noticed they were asking them:

1. **What** moves, and what does it mean in each system?
2. **When** does it move, and how fresh must the result be?
3. **Which direction** does it flow, and which system wins when both change the same thing?
4. **Who** is allowed to read and write, and how do they prove it?
5. **What happens when something fails**, and who finds out?

The rest of this book is a long answer to those five questions. Part II teaches you to ask them before anything is built. Parts III through IV teach you to answer them well. Part VI teaches you to keep the answers true after go-live.

!!! why "Why this matters"
    Teams that treat integration as "plumbing" tend to build the happy path and discover the other four questions in production. The typical symptom is an integration that works in the demo, then loses orders on the third day because nobody decided what should happen when the target system returned an error. Asking the five questions early costs an afternoon. Answering them late costs weeks.

## Four Ways Systems Talk

Underneath every integration technology, from a 1990s message broker to a modern streaming platform, there are only four basic ways for systems to exchange information. Learning them first gives you a map that stays useful as products come and go. {{ref fig:basics-phone-call-synchronous-request}} shows them side by side, each with an everyday analogy.

{{figgrid basics-phone-call-synchronous-request basics-letter-in-a-mailbox-queue basics-noticeboard-publish-subscribe basics-shared-filing-cabinet-files-and-databases | The four basic interaction styles. Solid arrows are calls that wait; dashed arrows are messages that do not. Each style trades simplicity for independence in a different way.}}

### The Phone Call: Synchronous Request

In a synchronous request, one system calls another and waits for the answer. REST APIs, GraphQL, gRPC, and SOAP services all work this way. The shop asks the ERP "is SKU TENT-2P in stock?" and does not show the product page until the ERP replies.

The strength of the phone call is simplicity and immediacy: you get an answer, and you know whether the call worked. The weakness is *coupling in time*. Both systems must be up at the same moment, and the caller is only as fast and as reliable as the slowest thing it depends on. If the ERP takes five seconds to answer, the product page takes five seconds to load. If the ERP is down, the page is down.

### The Letter: Queue

In a queue, the sender drops a message into a mailbox and carries on. A worker picks the message up whenever it is ready. Message brokers such as IBM MQ, RabbitMQ, Amazon SQS, and Azure Service Bus work this way. The shop writes "order A1043 was placed" to a queue; the ERP's worker reads it a few seconds, or a few hours, later.

A queue decouples the sender from the receiver *in time*: the receiver can be down, slow, or busy, and messages wait. It also smooths out spikes, because the queue absorbs a burst of orders that the receiver then works through at its own pace. The trade-off is that each message typically goes to *one* reader, the sender does not get an immediate answer, and you now have a new thing to operate and monitor.

### The Noticeboard: Publish and Subscribe

In publish and subscribe, a publisher pins a message to a board, and any number of interested readers see it. Apache Kafka topics, Amazon SNS, Google Pub/Sub, and Azure Event Grid are examples. The shop publishes "order A1043 was placed" once. The ERP, the analytics platform, the fraud-detection service, and the email system each read it independently, and the shop does not know or care how many there are.

The noticeboard decouples the publisher from the *number and identity* of its consumers. That is a powerful property, and it is why event-driven designs dominate large estates. Its cost is reduced visibility: when anyone can subscribe, it becomes difficult to answer "who depends on this message?" before you change it. Chapters {{ref ch:kafka1}} through {{ref ch:kafkaio}} cover the most important platform of this kind in depth.

### The Filing Cabinet: Shared Storage

In shared storage, one system writes files or rows to a place that another system reads. A CSV dropped on an SFTP server, a Parquet file in a cloud storage bucket, or a database table the other side queries are all variations. This is the oldest style and, for large volumes, often still the best. Moving ten million rows as a file is far more efficient than moving them as ten million API calls.

Shared storage is simple and cheap, but it reacts slowly, because nobody tells the reader a new file has arrived unless you add a notification. It also invites arguments about format, timing, and who cleans up. Larkspur's nightly CSV is a filing cabinet, and its problems are typical: late, brittle, and fixed by hand.

{{tbl styles | The four interaction styles compared}}

| Style | Everyday analogy | Typical technology | Strength | Weakness |
|---|---|---|---|---|
| Synchronous request | Phone call | REST, GraphQL, gRPC, SOAP | Immediate answer, simple mental model | Both sides must be up; latency adds up |
| Queue | Letter | IBM MQ, RabbitMQ, SQS, Service Bus | Independent pace; absorbs spikes | One reader per message; no replay |
| Publish and subscribe | Noticeboard | Kafka, SNS, Pub/Sub, Event Grid | Many readers; publisher unaware of them | Hard to see who depends on what |
| Shared storage | Filing cabinet | SFTP, object storage, shared tables | Efficient for volume; simple | Slow to react; format disputes |

No style is better in general. Real integrations combine them: a synchronous call for the instant answer the customer sees, an event for everything that follows, and a nightly file as the safety net that catches whatever the first two missed. Chapters {{ref ch:patterns1}} and {{ref ch:patterns2}} catalog the patterns that arise from these combinations.

## Anatomy of an API Call

Most integrations you will build touch at least one HTTP API, so it pays to be able to read one fluently. An HTTP exchange has two halves, a request and a response, and each has the same three parts: a first line, a set of headers, and an optional body. {{ref fig:basics-anatomy-of-an-http-request-and-response}} shows a request that creates an order and the response that confirms it.

{{fig basics-anatomy-of-an-http-request-and-response | Anatomy of an HTTP exchange. The request line carries the method and path; headers carry identity, format, and retry safety; the body carries the data. The response begins with a status code.}}

### The Request

The first line holds the **method** and the **path**. `POST /v2/orders` means "create something in the orders collection." The five methods you will use constantly are listed in {{ref tbl:methods}}.

{{tbl methods | HTTP methods and their guarantees}}

| Method | Typical meaning | Safe? | Idempotent? |
|---|---|---|---|
| GET | Read a resource or list | Yes | Yes |
| POST | Create, or trigger an action | No | **No** |
| PUT | Replace a resource entirely | No | Yes |
| PATCH | Change part of a resource | No | Depends on the API |
| DELETE | Remove a resource | No | Yes |

"Safe" means the call does not change anything on the server, so repeating it is harmless. "Idempotent" means that doing it twice has the same effect as doing it once. We return to that word shortly, because it matters more than any other in this book.

The **headers** are name and value pairs that describe the request. Five appear in nearly every integration:

* `Authorization` carries your credential, usually `Bearer` followed by a token. Chapter {{ref ch:auth}} covers how to obtain and protect it.
* `Content-Type` says what format the body is in, for example `application/json`.
* `Accept` says what format you want back.
* `Idempotency-Key` is a unique value you generate so that the server can recognize a retried request. Not every API supports it, but those that create money or orders should.
* `X-Request-ID` or `traceparent` carry identifiers that let you follow one request through several systems. Chapter {{ref ch:reliability}} explains why you should always send one.

The **body** carries the data, most often as JSON. Requests that only read, such as `GET`, usually have no body; the details travel in the URL as *query parameters*, for example `GET /v2/orders?updatedSince=2026-11-01T00:00:00Z&limit=100`.

### The Response

The response begins with a **status code**, a three-digit number that tells you, before you read anything else, whether the call worked and whose problem it is. The first digit is the class, and the class tells you what to do next.

{{tbl status | What each status family means for an integration}}

| Family | Meaning | What your integration should do |
|---|---|---|
| 2xx (200, 201, 202, 204) | Success. 202 means "accepted, still processing" | Continue. For 202, poll the status URL. For bulk calls, still check per-item results inside the body |
| 3xx | Look elsewhere (redirect) | Follow carefully; rare in APIs |
| 4xx (400, 401, 403, 404, 409, 422, 429) | Your request has a problem | Fix the request. For 401, re-authenticate once. For 429, slow down. Never blindly retry 400 or 422 |
| 5xx (500, 502, 503, 504) | The server has a problem | Retry with backoff, up to a limit, and alert if it persists |

Three details save hours of debugging. First, a **200 does not always mean success**: many bulk APIs return 200 with a body saying "40 of 5,000 records rejected." Always read the body. Second, **409 Conflict** and **422 Unprocessable Content** are the server telling you your data is wrong or collides with something; retrying the same request will fail the same way. Third, **429 Too Many Requests** usually arrives with a `Retry-After` header telling you how long to wait. Honor it.

!!! warning "A 200 can hide failures"
    Treat the HTTP status as the first of two checks. For any endpoint that accepts batches, parse the response body for per-item errors and count them. An integration that checks only the status code will report a perfect run while silently dropping records.

The response also has headers. `Location` tells you where a newly created resource lives. `Retry-After` tells you how long to wait. `ETag` identifies a version of a resource, which later lets you update safely. Rate-limit headers such as `X-RateLimit-Remaining` tell you how much budget you have left. And the body carries the answer, or, for a failure, an error description. Chapter {{ref ch:apidesign}} shows the standard format APIs should use for errors.

## Idempotency: The Idea That Holds the Book Together

Imagine the shop sends "create order A1043" to the ERP. The ERP creates the order and sends back a confirmation, but the network drops that confirmation. From the shop's side, the request simply timed out. Did the order get created or not? The shop cannot tell. It has two choices, and both are bad:

* **Do not retry.** If the ERP never received the request, the order is lost, and a customer waits for a tent that nobody will ship.
* **Retry.** If the ERP did create the order, the retry creates a second one, and the customer receives two tents and two invoices.

This is the oldest problem in distributed systems, and there is no way to detect the difference from the outside. The only way out is to make the operation **idempotent**: designed so that doing it twice is the same as doing it once. Then the shop can retry freely.

There are three common ways to achieve this, and you will use all of them:

1. **Natural idempotency.** Some operations are idempotent by their nature. "Set the order status to SHIPPED" can be repeated forever. A `PUT` that replaces a resource at a known address is the classic example. Whenever you can express a change as "make it so," prefer that over "add one more."
2. **An idempotency key.** The client generates a unique key for each logical operation and sends it with the request. The server remembers the key, and if the same key arrives again it returns the original result instead of repeating the work. This is how well-designed payment and order APIs make `POST` safe to retry.
3. **Lookup before retry.** When the API offers no idempotency support, the client first asks the server whether the earlier attempt succeeded, for example by searching for an order with the customer's purchase-order number, and only creates the order if the search finds nothing.

!!! example "Larkspur Outdoor: the duplicate that cost a weekend"
    In the nightly-file process, a rejected row was fixed by hand and re-uploaded, and nobody checked whether the rejected row had also been partly imported. Each month a handful of customers received a second shipment. The fix was not better typing. It was giving every order a unique business key, the shop's order number, and making the import an *upsert*: insert if the key is new, update if it exists. Doing it twice became harmless.

Keep this idea in your pocket. Almost every pattern in Part II, and most of the failure handling in Parts III and VI, is a way of making repeated or reordered messages harmless.

## Your First Integration

Reading about requests is no substitute for making them. The book's companion code includes a small order API, `labserver.py`, that you will use in several chapters. It runs on your own machine, needs only Python 3.9 or later and no packages, and can be told to misbehave on purpose. Appendix {{ref app:codelab}} lists the code.

Start the server in a terminal. It seeds 250 orders and listens on port 8080:

```bash
python3 labserver.py --port 8080 --no-auth
```

In a second terminal, make your first call with `curl`. The `-i` option includes the response headers, which is where much of the interesting information lives:

```bash
curl -i "http://127.0.0.1:8080/orders?limit=2"
```

You should see a status line of `HTTP/1.1 200 OK`, a few headers, and a JSON body containing two orders and a `nextCursor` value. The cursor is the server's way of saying "there is more; hand this value back to get the next page." Pagination gets a full treatment in Chapter {{ref ch:readdocs}}.

Now try the failure cases deliberately. Ask for an order that does not exist, then try to create one without an idempotency key:

```bash
curl -i http://127.0.0.1:8080/orders/NOPE
curl -i -X POST http://127.0.0.1:8080/orders -d '{"sku":"TENT-2P"}'
```

The first returns `404 Not Found`. The second returns `400 Bad Request` with a message explaining that the key is required, which is the server insisting on idempotency. Now supply a key, and send the same request twice:

```bash
curl -i -X POST http://127.0.0.1:8080/orders \
     -H "Idempotency-Key: demo-001" \
     -d '{"sku":"TENT-2P","qty":1}'
```

Run it a second time with the identical key. The second response carries the *same order*, and a header `Idempotent-Replay: true`. The server recognized the key and returned the original result instead of creating a duplicate. That header is the whole idea of the previous section, made visible.

Finally, the same exchange in Python. Install the one dependency with `pip install requests`, then run this script:

```python
import requests

BASE = "http://127.0.0.1:8080"

r = requests.get(BASE + "/orders", params={"limit": 3}, timeout=(5, 20))
if r.status_code == 200:
    body = r.json()
    for order in body["results"]:
        print(order["id"], order["sku"], order["updatedAt"])
    print("more pages:", body["nextCursor"] is not None)
elif r.status_code == 429:
    print("rate limited; retry after", r.headers.get("Retry-After"))
else:
    print("unexpected", r.status_code, r.text[:200])
```

Three habits are already visible in these few lines. The call sets a **timeout**: `requests` has no default timeout, so a call without one can hang a worker forever. The code **branches on the status code** instead of assuming success. And it treats the rate-limit case as a normal outcome, because in production it will be. Chapter {{ref ch:python}} turns these habits into a reusable client.

!!! tip "Make the server misbehave"
    Restart the lab server with `--rate-limit 3 --flaky 0.2` and rerun your script a few times. You will see 429 and 503 responses within minutes. Writing code that survives them is the subject of Chapter {{ref ch:python}}, and you now have a reproducible way to test it.

## Data Formats in One Page

Whatever style systems use to talk, they must agree on how to write the data down. Five formats cover almost everything:

* **JSON** (JavaScript Object Notation) dominates modern APIs. It is human-readable, but has no native type for decimals or dates, which causes subtle bugs.
* **XML** appears in SOAP services, B2B exchanges, and many enterprise suites. It is verbose but strongly typed through schemas.
* **CSV** and fixed-width files carry batch exports. They are compact, but carry no schema, and quoting, encoding, and locale-specific number formats cause endless trouble.
* **Avro and Protobuf** are compact binary formats, usually paired with a registered schema. They dominate event streaming.
* **Parquet** is a columnar format used for analytics.

A **schema** is the formal description of what a valid message looks like: OpenAPI and JSON Schema for JSON APIs, XSD for XML, Avro or Protobuf definitions for events. A schema is a contract you can test automatically, which makes it one of the most valuable artifacts an integration can have. Chapter {{ref ch:formats}} covers formats, mapping, and the traps hidden in dates, decimals, and text encodings.

## The Vocabulary You Will Need

{{ref tbl:vocab}} lists the terms used throughout the book, with the chapter where each is treated in depth. Appendix {{ref app:glossary}} contains the full glossary.

{{tbl vocab | Twenty terms you need before Chapter 2}}

| Term | Plain meaning | Chapter |
|---|---|---|
| API | A defined way for one program to ask another for data or an action | {{ref ch:readdocs}} |
| Endpoint | One address in an API, such as `/orders/{id}` | {{ref ch:readdocs}} |
| Authentication and authorization | Proving who you are, and what you are allowed to do | {{ref ch:auth}} |
| Token | A short-lived credential sent with each request | {{ref ch:auth}} |
| Payload | The data carried in a request, response, or message | {{ref ch:formats}} |
| Schema | The rules a valid payload must follow | {{ref ch:formats}} |
| Mapping | The rules that turn a source record into a target record | {{ref ch:formats}} |
| Pagination | Reading a large result in pages | {{ref ch:readdocs}} |
| Rate limit | How many calls you may make in a period | {{ref ch:python}} |
| Idempotent | Safe to do twice; the second time changes nothing | {{ref ch:python}} |
| Watermark | A bookmark recording how far you have read | {{ref ch:sync}} |
| Webhook | The source calls you when something changes | {{ref ch:patterns2}} |
| Queue and topic | Buffers for messages: one reader, or many readers | {{ref ch:kafka1}} |
| Event | A record that something happened | {{ref ch:apidesign}} |
| Change data capture | Reading every change from a database's log | {{ref ch:kafkaio}} |
| Upsert | Insert if new, update if it exists | {{ref ch:sync}} |
| Reconciliation | Comparing two systems to find drift | {{ref ch:sync}} |
| Dead letter queue | Where unprocessable messages wait for a human | {{ref ch:kafka2}} |
| iPaaS | A cloud platform for building integrations with connectors | {{ref ch:platforms}} |
| System of record | The system whose value wins for a given field | {{ref ch:patterns2}} |

## Ten Things That Go Wrong

Experienced integrators carry a mental list of failures, because the same ones recur on every project regardless of technology. Read this list now as a preview; every item has a chapter that handles it.

1. The same record is sent twice and duplicates appear. (Idempotency; Chapters {{ref ch:python}} and {{ref ch:sync}}.)
2. Changes are skipped because clocks disagree. (Watermarks with overlap; Chapter {{ref ch:python}}.)
3. The API starts refusing calls. (Rate limits and backoff; Chapter {{ref ch:python}}.)
4. A token expires halfway through a run. (Chapter {{ref ch:auth}}.)
5. Deleted records never disappear from the target. (Chapter {{ref ch:sync}}.)
6. A source field changes format and the mapping breaks. (Chapters {{ref ch:formats}} and {{ref ch:testing}}.)
7. A firewall or proxy blocks production but not your laptop. (Chapters {{ref ch:topologies}} and {{ref ch:security}}.)
8. The integration stops and nobody notices for weeks. (Chapter {{ref ch:reliability}}.)
9. Two systems keep overwriting each other's changes. (Chapter {{ref ch:sync}}.)
10. Nobody owns it after go-live. (Chapters {{ref ch:journey}} and {{ref ch:governance}}.)

## Summary

An integration is a contract between systems that were not built together, and it must settle three things: the *meaning* of the data, the *timing* of its movement, and the *behavior on failure*. Five questions, what, when, direction, who, and what if it fails, apply to every integration on every technology.

Systems exchange information in four basic ways: the synchronous request, the queue, publish and subscribe, and shared storage. Each trades simplicity against independence differently, and real designs combine them. An HTTP call has a method, a path, headers, and a body; the response begins with a status code whose first digit tells you whose problem it is and what to do next. And because networks fail between sending a request and seeing its answer, safe retries depend on **idempotency**, which you achieve through naturally repeatable operations, idempotency keys, or looking up before retrying.

## Exercises

1. **Read a real exchange.** Run `curl -i https://api.github.com/repos/apache/kafka` and label the status line, three headers, and the body. Find the rate-limit headers and calculate how many requests you have left in the current window.
2. **Break the lab server.** Start it with `--rate-limit 2`, then send five quick requests in a loop. Record which status codes appear and what `Retry-After` says. How would your script behave if it ignored that header?
3. **Prove idempotency.** Send the same `POST /orders` request with the same key three times, then with three different keys. Count the orders created each time by listing `GET /orders?limit=500` and comparing the total.
4. **Classify your own estate.** Choose two systems you work with that exchange data. For each flow, name which of the four interaction styles it uses, and answer the five questions. Which answers do you not know?
