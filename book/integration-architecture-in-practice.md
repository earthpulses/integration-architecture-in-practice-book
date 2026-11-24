# Integration Architecture in Practice

*Designing, Building, and Running Enterprise Integrations from REST to Kafka*

**Author:** Stefan Živanović, Solution Architect, Prague, Czech Republic  
**Edition:** First Edition, November 2026  
**Copyright:** © 2026 Stefan Živanović. All rights reserved.  
**AI statement:** Generated with AI assistance (Claude, by Anthropic), under the author's direction. See the section "How This Book Was Made".

Reference copy of the manuscript (Markdown). Figures appear as bracketed captions; see the PDF for diagrams. Companion code is in the `code` folder of the build workspace.



# Preface

Every company that has more than one system has an integration problem. The sales system must tell the warehouse what to ship. The warehouse must tell the finance system what to invoice. The human-resources system must tell everything else who still works here. The data platform must learn about all of it. Each connection is small; together they decide whether a company's information is trustworthy, and they decide it in ways that executives rarely see until something goes wrong.

This book is about doing that work well. It is for the people who design, build, and run those connections, from the developer writing a first client to the architect deciding how a hundred integrations fit together. It assumes you can read code and understand what a database and a web service are. It does not assume you have built an integration before, and it will not bore you if you have, because it concentrates on the part that experience teaches slowly: *how integrations fail, and how to design so that failure is survivable*.

## Who This Book Is For

You will get the most from this book if you are one of the following:

* **A developer or analyst moving into integration**, who has called an API but not yet had to keep one running for a year.
* **An integration engineer becoming an architect**, who builds well and now has to decide what to build, with whom, and why.
* **A solution architect on enterprise projects**, who needs a repeatable method for discovery, design, and review, and a vocabulary to use with clients.
* **A technical lead or principal** shaping an integration practice, who needs standards, an operating model, and a way to measure health.
* **Someone preparing for an interview or a design review**, who wants the questions and the answers in one place.

## What You Will Learn

By the end, you will be able to run a discovery workshop and turn its answers into a signed brief. You will choose between patterns and platforms using a method that others can inspect. You will read an unfamiliar API like an architect, design your own, and write clients that survive timeouts, retries, duplicates, and rate limits. You will understand Kafka well enough to know when not to use it and how to use it correctly when you should. You will design for failure, test for it, observe it, secure against it, and recover from it. And you will be able to estimate the work and explain the design to an executive in five minutes.

## How This Book Is Organized

The book has seven parts and thirty-one chapters.

**Part I, Foundations,** builds the vocabulary: how systems talk, how HTTP works, why idempotency matters, and how an architect thinks. **Part II, Discover and Decide,** covers the journey of an integration project, the discovery questions, the places integrations run, forty-one patterns, ten sequence diagrams of the hard cases, and a method for deciding. **Part III, Design and Build,** is the practical core: reading and designing APIs, formats and mapping, authentication, Python clients, synchronization, testing, and delivery. **Part IV, Messaging and Streaming,** covers Kafka from first principles to production, the many ways to connect to it, the interfaces beyond REST, and the large SaaS platforms. **Part V, Platforms and Practice,** surveys integration platforms, presents nine case studies, and follows one project from the first meeting to the first incident. **Part VI, Operate, Secure, Govern,** covers reliability and observability, security and threat modeling, recovery and estimation, governance, and troubleshooting. **Part VII, Growing as an Architect,** gives a learning path and a way to prove your skill.

Seven appendices follow: the full discovery question bank, interview and knowledge-check questions with model answers, workshop scenario cards, templates, the companion code, a glossary, and further reading.

You do not have to read straight through. Parts I and II are best read in order. Parts III to V can be read by need. Part VI belongs before your first go-live, and Part VII after a few months of practice.

## A Running Example

Most chapters return to **Larkspur Outdoor**, a fictional company that sells camping gear online and needs its web shop connected to its ERP. The example gives the book continuity: you meet the company's problem in the first chapter, answer its discovery questions in the fourth, see its design decisions at points along the way, and follow its project to production in Chapter 25. Larkspur and the other organizations in the case studies are composites. No real company or person is described.

## Conventions Used in This Book

The following typographical conventions are used:

*Italic* indicates new terms, emphasis, and the titles of books. `Constant width` indicates code, commands, file names, and parameters. Shaded boxes carry additional material: a *Why this matters* box explains the reasoning behind a practice, a *Warning* box flags a common failure, a *Tip* box offers a shortcut, an *Example* box returns to the running example, and an *In this chapter* box opens each chapter with its learning goals.

Diagrams use a consistent visual language, described in Chapter 6: solid arrows wait for an answer, dashed arrows do not, numbered circles give the order of steps, and lettered red circles mark where a design usually fails.

## Using the Code Examples

The companion code is a set of small, tested Python modules: a local lab API server, a hardened HTTP client, a token provider, an incremental poller, a webhook verifier, an outbox, a rate limiter, a run loop with quarantine, a reconciliation module, an OpenAPI analyzer, and a mapping module with its tests. Appendix E lists them. The code is distributed with the book as a zip archive and is licensed under the MIT License.

Listings marked as sketches, such as the Kafka producer and consumer, the Testcontainers test, the OpenTelemetry example, and the platform flow, are illustrative and need external services to run; they are not part of the automated tests. Product names, product features, limits, and prices change often. Where the book states a fact about a vendor's product, it is a fact as of the writing date, and you should confirm it against current documentation before you rely on it.

## How to Contact the Author

Comments, questions, and corrections are welcome and will be considered for later editions of this book.

## A Note on Authorship

This book was produced with the help of an AI assistant, under the author's direction. The section that follows, "How This Book Was Made," says what the AI did, what the author did, and how the result was checked. Please read it before you rely on any statement about a product or a version.



# How This Book Was Made

This book was produced with the help of artificial intelligence, and you should know exactly how.

**What the AI did.** The prose of the Preface, the thirty-one chapters and the seven appendices; the diagrams (drawn programmatically as vector graphics); the companion code and its automated tests; the index; the cover; and the page layout were generated by Claude, an AI assistant made by Anthropic, in a long series of working sessions. Several versions of the model took part. The text is original to this work; it was not intentionally copied from other books or from the proprietary documentation of any vendor.

**What the author did.** Stefan Živanović, a Solution Architect in Prague, set the subject, the audience, the structure, and the quality bar; commissioned and directed the earlier working guides on which this book builds; directed each stage of the work; and decided what the book would and would not contain. He is the author of record and is responsible for the published content.

**What was checked, and how.** Every listing in the companion code was run, and its eighteen automated tests pass; the few listings marked as sketches need external services and were not run. The diagrams were checked by script for layout problems and for step numbers that the text cites. Statements about products, versions, and standards were checked against public sources in November 2026 where the text says so. The book has not had a professional copyedit or an independent technical review, and readers who find errors are asked to report them to the author.

**What to keep in mind.** AI systems can state wrong things fluently. Vendor products, versions, limits, and standards change; verify them before you rely on them for contracts, security reviews, or compliance decisions. Larkspur Outdoor and the other organizations in the case studies are fictional composites, and no real company or person is described. The companion code is provided as is, under the MIT License.



---

# Part I. Foundations

How systems talk to each other, how an architect thinks, and the vocabulary you need before anything else.



# Chapter 1. What Integration Really Is

It is Monday morning at Larkspur Outdoor, a mid-sized company that sells camping gear online in six countries. The warehouse manager is staring at a spreadsheet. Over the weekend the web shop took 3,100 orders. The company's ERP system, the system that actually reserves stock, prints pick lists, and issues invoices, knows about none of them yet. Each night an export job writes a CSV file from the shop, and each morning someone opens that file, fixes the rows that the import rejected, and uploads it by hand. This morning the file has 214 rejected rows, and customers are already emailing to ask why their tents have not shipped.

Nothing here is broken in the way engineers usually mean it. The shop works. The ERP works. The export job runs. What is missing is the connection between them, and that connection has to answer questions that neither system was built to answer. How quickly should an order reach the ERP? What should happen when the ERP is down for maintenance? What if the same order arrives twice? Who is allowed to change a price? Who finds out when something goes wrong, and how?

That is integration. It is the work of making independently built systems behave, from the business's point of view, like one system. This chapter gives you the vocabulary and the mental models for the rest of the book. By the end of it you will have read a raw HTTP exchange, written a small client, and met the one idea, idempotency, that explains more integration failures than any other.

> **In this chapter**
    * Define integration in terms of meaning, time, and failure rather than technology
    * Distinguish the four basic ways systems exchange information, and know when each fits
    * Read an HTTP request and response, including the status codes and headers that matter
    * Explain idempotency and why safe retries depend on it
    * Build and run a first integration against a local test API

## Integration Is About Meaning, Time, and Failure

The simplest definition of integration is "moving data from one system to another." It is also the least useful, because it hides everything that makes the work hard. A better definition is that an integration is a *contract between systems that were not built together*. The contract covers three things.

**Meaning.** The shop calls a customer record `customer`, with a `fullName` field and an email address. The ERP calls it a *business partner*, splits the name into first and last parts, and requires a tax region the shop never collects. Moving the fields is easy. Deciding what a "customer" is, who owns the definition, and what to do when the two systems disagree is the real work. Chapter 12 covers mapping in depth.

**Time.** The shop wants to take an order at any hour. The ERP has a nightly batch window during which it refuses connections. The shop's marketing team changes prices on Black Friday at 06:00; the ERP's price list changes on the first of the month. Systems live on different clocks, and an integration must say what "up to date" means: seconds, minutes, or tomorrow. That promise, usually called *freshness*, shapes the whole design.

**Failure.** Networks drop connections. Servers restart. A vendor's API starts returning errors at 02:14 and recovers at 02:31. A deployment changes a field name. An integration spends most of its life in the narrow gap between "everything works" and "everything is down", where some requests succeeded, some failed, and nobody is sure which. Good integrations are designed around the gap.

Every integration you will ever meet answers the same five questions, whether or not the people building it noticed they were asking them:

1. **What** moves, and what does it mean in each system?
2. **When** does it move, and how fresh must the result be?
3. **Which direction** does it flow, and which system wins when both change the same thing?
4. **Who** is allowed to read and write, and how do they prove it?
5. **What happens when something fails**, and who finds out?

The rest of this book is a long answer to those five questions. Part II teaches you to ask them before anything is built. Parts III through IV teach you to answer them well. Part VI teaches you to keep the answers true after go-live.

> **Why this matters**
    Teams that treat integration as "plumbing" tend to build the happy path and discover the other four questions in production. The typical symptom is an integration that works in the demo, then loses orders on the third day because nobody decided what should happen when the target system returned an error. Asking the five questions early costs an afternoon. Answering them late costs weeks.

## Four Ways Systems Talk

Underneath every integration technology, from a 1990s message broker to a modern streaming platform, there are only four basic ways for systems to exchange information. Learning them first gives you a map that stays useful as products come and go. the figure shows them side by side, each with an everyday analogy.

*[Figure grid: The four basic interaction styles. Solid arrows are calls that wait; dashed arrows are messages that do not. Each style trades simplicity for independence in a different way.]*
### The Phone Call: Synchronous Request

In a synchronous request, one system calls another and waits for the answer. REST APIs, GraphQL, gRPC, and SOAP services all work this way. The shop asks the ERP "is SKU TENT-2P in stock?" and does not show the product page until the ERP replies.

The strength of the phone call is simplicity and immediacy: you get an answer, and you know whether the call worked. The weakness is *coupling in time*. Both systems must be up at the same moment, and the caller is only as fast and as reliable as the slowest thing it depends on. If the ERP takes five seconds to answer, the product page takes five seconds to load. If the ERP is down, the page is down.

### The Letter: Queue

In a queue, the sender drops a message into a mailbox and carries on. A worker picks the message up whenever it is ready. Message brokers such as IBM MQ, RabbitMQ, Amazon SQS, and Azure Service Bus work this way. The shop writes "order A1043 was placed" to a queue; the ERP's worker reads it a few seconds, or a few hours, later.

A queue decouples the sender from the receiver *in time*: the receiver can be down, slow, or busy, and messages wait. It also smooths out spikes, because the queue absorbs a burst of orders that the receiver then works through at its own pace. The trade-off is that each message typically goes to *one* reader, the sender does not get an immediate answer, and you now have a new thing to operate and monitor.

### The Noticeboard: Publish and Subscribe

In publish and subscribe, a publisher pins a message to a board, and any number of interested readers see it. Apache Kafka topics, Amazon SNS, Google Pub/Sub, and Azure Event Grid are examples. The shop publishes "order A1043 was placed" once. The ERP, the analytics platform, the fraud-detection service, and the email system each read it independently, and the shop does not know or care how many there are.

The noticeboard decouples the publisher from the *number and identity* of its consumers. That is a powerful property, and it is why event-driven designs dominate large estates. Its cost is reduced visibility: when anyone can subscribe, it becomes difficult to answer "who depends on this message?" before you change it. Chapters 18 through 20 cover the most important platform of this kind in depth.

### The Filing Cabinet: Shared Storage

In shared storage, one system writes files or rows to a place that another system reads. A CSV dropped on an SFTP server, a Parquet file in a cloud storage bucket, or a database table the other side queries are all variations. This is the oldest style and, for large volumes, often still the best. Moving ten million rows as a file is far more efficient than moving them as ten million API calls.

Shared storage is simple and cheap, but it reacts slowly, because nobody tells the reader a new file has arrived unless you add a notification. It also invites arguments about format, timing, and who cleans up. Larkspur's nightly CSV is a filing cabinet, and its problems are typical: late, brittle, and fixed by hand.

**Table: The four interaction styles compared**
| Style | Everyday analogy | Typical technology | Strength | Weakness |
|---|---|---|---|---|
| Synchronous request | Phone call | REST, GraphQL, gRPC, SOAP | Immediate answer, simple mental model | Both sides must be up; latency adds up |
| Queue | Letter | IBM MQ, RabbitMQ, SQS, Service Bus | Independent pace; absorbs spikes | One reader per message; no replay |
| Publish and subscribe | Noticeboard | Kafka, SNS, Pub/Sub, Event Grid | Many readers; publisher unaware of them | Hard to see who depends on what |
| Shared storage | Filing cabinet | SFTP, object storage, shared tables | Efficient for volume; simple | Slow to react; format disputes |

No style is better in general. Real integrations combine them: a synchronous call for the instant answer the customer sees, an event for everything that follows, and a nightly file as the safety net that catches whatever the first two missed. Chapters 6 and 7 catalog the patterns that arise from these combinations.

## Anatomy of an API Call

Most integrations you will build touch at least one HTTP API, so it pays to be able to read one fluently. An HTTP exchange has two halves, a request and a response, and each has the same three parts: a first line, a set of headers, and an optional body. the figure shows a request that creates an order and the response that confirms it.

*[Figure: Anatomy of an HTTP exchange. The request line carries the method and path; headers carry identity, format, and retry safety; the body carries the data. The response begins with a status code.]*
### The Request

The first line holds the **method** and the **path**. `POST /v2/orders` means "create something in the orders collection." The five methods you will use constantly are listed in the table.

**Table: HTTP methods and their guarantees**
| Method | Typical meaning | Safe? | Idempotent? |
|---|---|---|---|
| GET | Read a resource or list | Yes | Yes |
| POST | Create, or trigger an action | No | **No** |
| PUT | Replace a resource entirely | No | Yes |
| PATCH | Change part of a resource | No | Depends on the API |
| DELETE | Remove a resource | No | Yes |

"Safe" means the call does not change anything on the server, so repeating it is harmless. "Idempotent" means that doing it twice has the same effect as doing it once. We return to that word shortly, because it matters more than any other in this book.

The **headers** are name and value pairs that describe the request. Five appear in nearly every integration:

* `Authorization` carries your credential, usually `Bearer` followed by a token. Chapter 13 covers how to obtain and protect it.
* `Content-Type` says what format the body is in, for example `application/json`.
* `Accept` says what format you want back.
* `Idempotency-Key` is a unique value you generate so that the server can recognize a retried request. Not every API supports it, but those that create money or orders should.
* `X-Request-ID` or `traceparent` carry identifiers that let you follow one request through several systems. Chapter 26 explains why you should always send one.

The **body** carries the data, most often as JSON. Requests that only read, such as `GET`, usually have no body; the details travel in the URL as *query parameters*, for example `GET /v2/orders?updatedSince=2026-11-01T00:00:00Z&limit=100`.

### The Response

The response begins with a **status code**, a three-digit number that tells you, before you read anything else, whether the call worked and whose problem it is. The first digit is the class, and the class tells you what to do next.

**Table: What each status family means for an integration**
| Family | Meaning | What your integration should do |
|---|---|---|
| 2xx (200, 201, 202, 204) | Success. 202 means "accepted, still processing" | Continue. For 202, poll the status URL. For bulk calls, still check per-item results inside the body |
| 3xx | Look elsewhere (redirect) | Follow carefully; rare in APIs |
| 4xx (400, 401, 403, 404, 409, 422, 429) | Your request has a problem | Fix the request. For 401, re-authenticate once. For 429, slow down. Never blindly retry 400 or 422 |
| 5xx (500, 502, 503, 504) | The server has a problem | Retry with backoff, up to a limit, and alert if it persists |

Three details save hours of debugging. First, a **200 does not always mean success**: many bulk APIs return 200 with a body saying "40 of 5,000 records rejected." Always read the body. Second, **409 Conflict** and **422 Unprocessable Content** are the server telling you your data is wrong or collides with something; retrying the same request will fail the same way. Third, **429 Too Many Requests** usually arrives with a `Retry-After` header telling you how long to wait. Honor it.

> **A 200 can hide failures**
    Treat the HTTP status as the first of two checks. For any endpoint that accepts batches, parse the response body for per-item errors and count them. An integration that checks only the status code will report a perfect run while silently dropping records.

The response also has headers. `Location` tells you where a newly created resource lives. `Retry-After` tells you how long to wait. `ETag` identifies a version of a resource, which later lets you update safely. Rate-limit headers such as `X-RateLimit-Remaining` tell you how much budget you have left. And the body carries the answer, or, for a failure, an error description. Chapter 11 shows the standard format APIs should use for errors.

## Idempotency: The Idea That Holds the Book Together

Imagine the shop sends "create order A1043" to the ERP. The ERP creates the order and sends back a confirmation, but the network drops that confirmation. From the shop's side, the request simply timed out. Did the order get created or not? The shop cannot tell. It has two choices, and both are bad:

* **Do not retry.** If the ERP never received the request, the order is lost, and a customer waits for a tent that nobody will ship.
* **Retry.** If the ERP did create the order, the retry creates a second one, and the customer receives two tents and two invoices.

This is the oldest problem in distributed systems, and there is no way to detect the difference from the outside. The only way out is to make the operation **idempotent**: designed so that doing it twice is the same as doing it once. Then the shop can retry freely.

There are three common ways to achieve this, and you will use all of them:

1. **Natural idempotency.** Some operations are idempotent by their nature. "Set the order status to SHIPPED" can be repeated forever. A `PUT` that replaces a resource at a known address is the classic example. Whenever you can express a change as "make it so," prefer that over "add one more."
2. **An idempotency key.** The client generates a unique key for each logical operation and sends it with the request. The server remembers the key, and if the same key arrives again it returns the original result instead of repeating the work. This is how well-designed payment and order APIs make `POST` safe to retry.
3. **Lookup before retry.** When the API offers no idempotency support, the client first asks the server whether the earlier attempt succeeded, for example by searching for an order with the customer's purchase-order number, and only creates the order if the search finds nothing.

> **Larkspur Outdoor: the duplicate that cost a weekend**
    In the nightly-file process, a rejected row was fixed by hand and re-uploaded, and nobody checked whether the rejected row had also been partly imported. Each month a handful of customers received a second shipment. The fix was not better typing. It was giving every order a unique business key, the shop's order number, and making the import an *upsert*: insert if the key is new, update if it exists. Doing it twice became harmless.

Keep this idea in your pocket. Almost every pattern in Part II, and most of the failure handling in Parts III and VI, is a way of making repeated or reordered messages harmless.

## Your First Integration

Reading about requests is no substitute for making them. The book's companion code includes a small order API, `labserver.py`, that you will use in several chapters. It runs on your own machine, needs only Python 3.9 or later and no packages, and can be told to misbehave on purpose. Appendix E lists the code.

Start the server in a terminal. It seeds 250 orders and listens on port 8080:

```bash
python3 labserver.py --port 8080 --no-auth
```

In a second terminal, make your first call with `curl`. The `-i` option includes the response headers, which is where much of the interesting information lives:

```bash
curl -i "http://127.0.0.1:8080/orders?limit=2"
```

You should see a status line of `HTTP/1.1 200 OK`, a few headers, and a JSON body containing two orders and a `nextCursor` value. The cursor is the server's way of saying "there is more; hand this value back to get the next page." Pagination gets a full treatment in Chapter 10.

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

Three habits are already visible in these few lines. The call sets a **timeout**: `requests` has no default timeout, so a call without one can hang a worker forever. The code **branches on the status code** instead of assuming success. And it treats the rate-limit case as a normal outcome, because in production it will be. Chapter 14 turns these habits into a reusable client.

> **Make the server misbehave**
    Restart the lab server with `--rate-limit 3 --flaky 0.2` and rerun your script a few times. You will see 429 and 503 responses within minutes. Writing code that survives them is the subject of Chapter 14, and you now have a reproducible way to test it.

## Data Formats in One Page

Whatever style systems use to talk, they must agree on how to write the data down. Five formats cover almost everything:

* **JSON** (JavaScript Object Notation) dominates modern APIs. It is human-readable, but has no native type for decimals or dates, which causes subtle bugs.
* **XML** appears in SOAP services, B2B exchanges, and many enterprise suites. It is verbose but strongly typed through schemas.
* **CSV** and fixed-width files carry batch exports. They are compact, but carry no schema, and quoting, encoding, and locale-specific number formats cause endless trouble.
* **Avro and Protobuf** are compact binary formats, usually paired with a registered schema. They dominate event streaming.
* **Parquet** is a columnar format used for analytics.

A **schema** is the formal description of what a valid message looks like: OpenAPI and JSON Schema for JSON APIs, XSD for XML, Avro or Protobuf definitions for events. A schema is a contract you can test automatically, which makes it one of the most valuable artifacts an integration can have. Chapter 12 covers formats, mapping, and the traps hidden in dates, decimals, and text encodings.

## The Vocabulary You Will Need

the table lists the terms used throughout the book, with the chapter where each is treated in depth. Appendix F contains the full glossary.

**Table: Twenty terms you need before Chapter 2**
| Term | Plain meaning | Chapter |
|---|---|---|
| API | A defined way for one program to ask another for data or an action | 10 |
| Endpoint | One address in an API, such as `/orders/{id}` | 10 |
| Authentication and authorization | Proving who you are, and what you are allowed to do | 13 |
| Token | A short-lived credential sent with each request | 13 |
| Payload | The data carried in a request, response, or message | 12 |
| Schema | The rules a valid payload must follow | 12 |
| Mapping | The rules that turn a source record into a target record | 12 |
| Pagination | Reading a large result in pages | 10 |
| Rate limit | How many calls you may make in a period | 14 |
| Idempotent | Safe to do twice; the second time changes nothing | 14 |
| Watermark | A bookmark recording how far you have read | 15 |
| Webhook | The source calls you when something changes | 7 |
| Queue and topic | Buffers for messages: one reader, or many readers | 18 |
| Event | A record that something happened | 11 |
| Change data capture | Reading every change from a database's log | 20 |
| Upsert | Insert if new, update if it exists | 15 |
| Reconciliation | Comparing two systems to find drift | 15 |
| Dead letter queue | Where unprocessable messages wait for a human | 19 |
| iPaaS | A cloud platform for building integrations with connectors | 23 |
| System of record | The system whose value wins for a given field | 7 |

## Ten Things That Go Wrong

Experienced integrators carry a mental list of failures, because the same ones recur on every project regardless of technology. Read this list now as a preview; every item has a chapter that handles it.

1. The same record is sent twice and duplicates appear. (Idempotency; Chapters 14 and 15.)
2. Changes are skipped because clocks disagree. (Watermarks with overlap; Chapter 14.)
3. The API starts refusing calls. (Rate limits and backoff; Chapter 14.)
4. A token expires halfway through a run. (Chapter 13.)
5. Deleted records never disappear from the target. (Chapter 15.)
6. A source field changes format and the mapping breaks. (Chapters 12 and 16.)
7. A firewall or proxy blocks production but not your laptop. (Chapters 5 and 27.)
8. The integration stops and nobody notices for weeks. (Chapter 26.)
9. Two systems keep overwriting each other's changes. (Chapter 15.)
10. Nobody owns it after go-live. (Chapters 3 and 29.)

## Summary

An integration is a contract between systems that were not built together, and it must settle three things: the *meaning* of the data, the *timing* of its movement, and the *behavior on failure*. Five questions, what, when, direction, who, and what if it fails, apply to every integration on every technology.

Systems exchange information in four basic ways: the synchronous request, the queue, publish and subscribe, and shared storage. Each trades simplicity against independence differently, and real designs combine them. An HTTP call has a method, a path, headers, and a body; the response begins with a status code whose first digit tells you whose problem it is and what to do next. And because networks fail between sending a request and seeing its answer, safe retries depend on **idempotency**, which you achieve through naturally repeatable operations, idempotency keys, or looking up before retrying.

## Exercises

1. **Read a real exchange.** Run `curl -i https://api.github.com/repos/apache/kafka` and label the status line, three headers, and the body. Find the rate-limit headers and calculate how many requests you have left in the current window.
2. **Break the lab server.** Start it with `--rate-limit 2`, then send five quick requests in a loop. Record which status codes appear and what `Retry-After` says. How would your script behave if it ignored that header?
3. **Prove idempotency.** Send the same `POST /orders` request with the same key three times, then with three different keys. Count the orders created each time by listing `GET /orders?limit=500` and comparing the total.
4. **Classify your own estate.** Choose two systems you work with that exchange data. For each flow, name which of the four interaction styles it uses, and answer the five questions. Which answers do you not know?



# Chapter 2. The Architect's Mindset

Two engineers are handed the same task: connect the web shop to the ERP. The first opens the ERP's API documentation, finds the "create sales order" endpoint, writes a script that calls it for every new order, and demonstrates it to the team that afternoon. It works. The second engineer spends the afternoon asking questions. How many orders arrive on the busiest hour of the busiest day? What happens to an order if the ERP is in its maintenance window? Who decides the price when the shop and the ERP disagree? Who gets called at 3 a.m. when orders stop flowing?

By Friday the first engineer has a demo and the second has a list of questions, and the first looks faster. Three months later the first engineer's script has lost 400 orders during a weekend outage, has no alerting, and cannot be run twice without creating duplicates. The second engineer's integration is still running, because the hard decisions were made when they were cheap.

The difference is not intelligence or tooling. It is a way of thinking, and it is what this chapter teaches. The integration architect's job is not to be the best coder on the project. It is to **shrink the gap between the demo and the messy reality** before the messy reality arrives. That gap is where integrations fail.

> **In this chapter**
    * Recognize the ten defaults experienced architects assume about every integration
    * Ask the three questions that sit behind every design
    * Describe the full lifecycle an architect is accountable for, and the artifact each phase produces
    * Name the thirteen skill domains of the role and assess your own profile
    * Use the ten technology-independent ideas that every platform renames
    * Argue the six trade-offs that never go away, and record decisions in an architecture decision record

## Ten Defaults to Assume Before You Read a Single Document

Experienced architects begin every project with a list of assumptions about how integrations fail. They write them on the whiteboard in the first workshop and then design as though they were already true. Each one is cheap to design for on the first day and expensive to discover on the ninetieth.

**Table: Ten defaults, their design consequence, and the symptom when ignored**
| Default assumption | What it means for design | Symptom if ignored |
|---|---|---|
| The API will rate-limit you | Build backoff and a request budget from the start | The nightly sync works in test, then fails at 02:14 in production with HTTP 429 |
| The API will return partial failures | Check per-item results, not only the HTTP status | HTTP 200 with 40 of 5,000 records rejected inside the body |
| Clocks are not synchronized | Use overlap windows and server-issued watermarks, never "last run time" from your own clock | Records changed during the sync are skipped forever |
| IDs are not stable across systems | Store the source ID on the target, and the target ID on the source where possible | A rename in the source creates a duplicate in the target |
| Documentation is wrong somewhere | Probe every endpoint with `curl` before you design around it | The documentation says the field is `caller`; the API returns `caller_id` |
| The sandbox is not production | Ask for production-sized data and production authentication settings early | It works against 200 rows and times out against 2 million |
| Credentials will be rotated | Keep secrets in a vault; handle 401 with exactly one re-authentication | The integration dies on a Sunday when a service-account password expires |
| A firewall sits in the way | Identify the network path and who can open ports in week one | Everything works from the consultant's laptop and nothing from the server |
| Somebody will run it twice | Make every write idempotent | Duplicate tickets; double-counted measures |
| Nobody owns it after you leave | Treat the runbook, alerting, and a named owner as deliverables | The integration is quietly broken for a quarter before anyone notices |

It is worth dwelling on a few of these, because each hides a story that repeats on almost every project.

**"Clocks are not synchronized"** is the most underestimated. Suppose your sync job records "I last ran at 10:00:00" and next time asks the source for everything changed since 10:00:00. A record the source modified at 09:59:58 but committed to its database at 10:00:03 will never be returned by that query, because its timestamp is older than your bookmark. The record is skipped forever, with no error anywhere. Chapter 14 shows the fix: use the *source's* timestamps, and always re-read a short overlap window, relying on idempotency to make the repeats harmless.

**"The sandbox is not production"** deserves a place on every risk list. Vendor sandboxes typically differ from production in rate limits, data volume, enabled features, and authentication settings. An integration validated against a sandbox with 200 rows tells you very little about how it behaves against 2 million. Chapter 17 shows how to close that gap with a shadow run in a production-like environment.

**"Nobody owns it after you leave"** is the quietest failure. Integrations rarely crash loudly. They stall: a token expires, a schedule is disabled during a migration, a field is renamed, and the data simply stops moving. If no alert fires and no person owns the flow, the first sign of trouble is a business user asking why a report is wrong, often weeks later.

> **Why this matters**
    Integration projects rarely fail on the happy path. They fail on the third day of production, on the one record with an emoji in the name, or when the source team ships a "minor" API change. Writing these defaults down at the start turns vague unease into a checklist that the whole team can design against.

## The Three Questions Behind Every Integration

Beneath the ten defaults sit three questions. If you can answer them for an integration, the design usually becomes obvious. If you cannot, you are not ready to design.

**Where does the truth live?** For every entity and every field, exactly one system should be authoritative. The shop owns the customer's shipping address as typed at checkout; the ERP owns the stock level and the invoice number. When two systems both edit the same field, you have a conflict-resolution problem, which is the most expensive kind of integration to build and to operate. Part of an architect's craft is steering a project toward *clean authority splits* so that conflicts never arise. Chapter 7 develops this idea.

**How fast must change travel?** Seconds, minutes, hours, or next day. This one answer eliminates most of the pattern catalog, and it drives cost more than any other requirement. "Real time" is expensive, and it is often requested out of habit rather than need. When a business owner says "real time," ask what decision is made with the data and how long that decision can wait. Frequently the honest answer is "within a few minutes," which opens up far cheaper designs.

**What happens when it breaks?** Who is told, what is retried, what is parked for a human, and how do we reconcile afterward? A design without an answer here is a prototype, however polished the diagrams.

## The Lifecycle You Own

A common mistake is to think of the architect as the person who draws the boxes at the start. In practice, the architect is accountable for the whole arc, from the first conversation to the retirement of the integration years later. the figure shows the seven phases.

*[Figure: An architect is accountable for the whole arc, not only the design phase. Each phase produces something concrete and ends with a sign-off.]*
Each phase has a characteristic output and a characteristic way of failing when it is skipped.

**Table: The seven phases, their outputs, and the failure when skipped**
| Phase | You produce | Typical failure if skipped | Who signs off |
|---|---|---|---|
| Discover | Integration brief, authority matrix, the four numbers, risk list | Right solution to the wrong problem | Business owner |
| Design | Pattern choice with rejected alternatives, contracts, network and security design, decision records | Late discovery of firewall, authentication, or volume limits | Architecture board, security |
| Build | Flows or code, mappings as configuration, infrastructure as code | Click-built flows nobody can reproduce | Technical lead |
| Test | Contract tests, failure injection, volume test, reconciliation report | Acceptance by demo | Quality assurance and business |
| Release | Go-live checklist, backfill plan, rollback plan, communications | The initial load corrupts the target | Change board |
| Operate | Alerts, runbook, dashboards, reconciliation schedule, on-call rota | Silent breakage for weeks | Operations owner |
| Evolve | Versioning policy, deprecation notices, retirement plan | Zombie integrations nobody dares touch | Product owner |

The discover phase introduces **the four numbers**, which you should leave every first workshop with: how many records exist now; how many you expect in three years; the peak number of changes per hour; and the maximum acceptable staleness. With those four numbers you can size an API budget, choose between polling and streaming, and estimate cost, all before writing a line of code. Chapter 4 shows how to get them.

## Thirteen Skill Domains

The role of an integration architect draws on thirteen skill domains. You will not be equally strong in all of them, and you do not need to be. What matters is knowing where you are weak, so that you can learn, or involve a specialist, before the weakness hurts a project. the table summarizes each domain, what "good" looks like, and the artifact that proves it.

**Table: The thirteen skill domains of an integration architect**
| Domain | What good looks like | Artifact you can show |
|---|---|---|
| Discovery and requirements | You leave every workshop with an authority matrix, the four numbers, and a named owner | One-page integration brief |
| Systems thinking | You can say what breaks, for whom, and how long it takes to notice when any component dies | Failure-mode table |
| Data and semantics | You settle matching, deletes, and field ownership before code is written | Authority matrix and field mapping |
| Interface and contract design | You write the OpenAPI or AsyncAPI contract first, with idempotency, pagination, and errors defined | API and event specifications |
| Security and identity | Every integration has a dedicated identity, a rotation plan, and a data classification | Security review pack |
| Networking and hybrid connectivity | You can spot the proxy that will break TLS in week three | Network path diagram |
| Platform literacy | You can translate a design between platforms ("an SQS queue here, a Service Bus queue there") | Platform mapping table |
| Reliability and performance | Every flow has a timeout, retry policy, duplicate strategy, and volume test | Failure-injection results |
| Observability and operations | The business hears about an outage from your alert, not from a user | Runbook and alert catalog |
| Delivery and engineering practice | Flows and configuration are versioned, promoted, and reproducible | Pipeline and infrastructure code |
| Governance, cost, and vendor judgment | You can defend a platform choice with numbers and record why alternatives were rejected | Decision records |
| Communication and leadership | An executive and an engineer can both act on the same one-page design | Executive one-pager |
| Testing and quality engineering | You prove correctness with reconciliation reports, not demos | Test plan and reconciliation report |

To assess yourself, rate each domain from 1 (new to it) to 5 (could teach it to a colleague). Be honest; nobody will see the result but you. Then circle your three lowest scores and read the chapters that teach them first. Chapter 31 turns the same list into a twelve-month learning plan.

> **The most common gap**
    In our experience of reviewing architects' profiles, networking and operations are the two domains rated lowest, and they cause a disproportionate share of production incidents. If you are strong on design and weak on these, you are not unusual, and you now know where to invest.

## Mental Models That Do Not Change with the Technology

Technologies come and go every few years; the underlying ideas do not. A platform vendor will tell you that their product has "message groups," "sessions," "key-based partitioning," or "sequential processing flags." They are all answers to the same question: does the order of messages matter? Learn the question once and you can read any vendor's documentation.

**Table: Ten ideas that every platform renames**
| Idea | The question it answers | On premises (MQ, ESB) | Cloud native | Integration platform | In your own code |
|---|---|---|---|---|---|
| Idempotency | What if this runs twice? | Duplicate detection on message ID | FIFO queue dedupe ID; API idempotency keys | Upsert by key; data-store check | A deduplication table |
| Retry | What if the target is briefly down? | Backout count and requeue | Workflow retry policies | Retry scopes; until-successful | Backoff with jitter |
| Dead letters | Where do poison messages go? | Backout queue | Dead-letter queues | Error queues; failed-record batches | Quarantine table or topic |
| Ordering | Does sequence matter? | One consumer per queue; message groups | FIFO queues; sessions; partitions | Sequential processing flags | Key-based partitioning |
| Backpressure | What if the producer is faster? | Queue depth limits | Autoscaling; throttling | Concurrency limits | Bounded queues; pause and resume |
| Contracts | What may consumers rely on? | WSDL and XSD | OpenAPI; AsyncAPI; schema registry | API specs in a design catalog | Typed models; contract tests |
| Identity | Who is calling? | Service accounts; certificates | Managed identity; IAM roles; OAuth | Connection credentials | Vault client; workload identity |
| Time | Whose clock, what zone? | Batch calendars | UTC; event time versus processing time | Scheduler time zones | Timezone-aware datetimes |
| Consistency | How wrong may data be, for how long? | Two-phase commit | Sagas; eventual consistency | Compensating flows | Outbox; reconciliation |
| Ownership | Who fixes it at 3 a.m.? | Operations team | Platform plus product team | Center of excellence | The service owner |

The table repays study. If you can fill in the fourth column for a technology you know well, you understand it; if you can fill in the fifth for one you do not, you can learn it quickly.

## Trade-offs You Will Argue for the Rest of Your Career

Architecture is the art of choosing which problem to have. Six trade-offs recur in almost every design review, and a good architect can argue either side of each, depending on the context.

**Freshness, reliability, and cost.** You can usually afford two of the three. Real-time and reliable is expensive, because it needs streaming infrastructure, replay, and on-call staff. Cheap and real-time tends to drop events when something fails. Cheap and reliable is batch: late, but dependable.

**Coupling versus simplicity.** Direct calls between systems are simple until the fifth system joins, at which point the number of links explodes. Events decouple producers from consumers at the price of invisibility. Choose by asking how many consumers there will be in two years, not how many there are today.

**Consistency versus availability.** Transactions that span systems rarely exist in practice. Decide which side may be stale, for how long, and how you repair it. The tools are sagas, outboxes, and reconciliation, which Part II and Chapter 15 explain.

**Build versus buy.** Custom code wins on control and loses on long-term maintenance. Integration platforms win on speed and available connectors and lose on cost curve and lock-in. Neither is right in general; Chapter 23 gives a method for choosing.

**Central versus federated.** A central integration team guarantees standards and tends to become a queue that everyone waits in. Federated teams move faster and drift apart. The usual compromise, and the one Chapter 29 recommends, is a platform team that provides a well-lit "paved road" while domain teams build on it.

**Canonical versus bounded models.** A shared data model across all systems removes translation sprawl and creates a committee to maintain it. Use canonical models only for a small number of stable, widely shared entities such as customer and product.

## Recording Decisions

A decision that is not written down gets re-argued every six months by whoever was not in the room. The standard remedy is the **architecture decision record**, or ADR: a half-page document that captures what was decided, why, and under what conditions the decision should be revisited.

```text
ADR-014: Use polling with a watermark instead of webhooks for ticket sync
Status:    Accepted (2026-11-23)         Deciders: <names>
Context:   The source offers webhooks without replay; the network is
           outbound-only; the freshness target is 5 minutes.
Options:   (A) webhooks plus a queue
           (B) polling with a modified-since filter
           (C) change data capture on the source database
Decision:  B, with a nightly ID-list reconciliation to detect deletes.
Because:   It meets the 5-minute target, needs no inbound firewall rule,
           and is replayable by resetting the watermark.
Consequences: Up to 2 minutes of overlap is re-read (idempotent upsert);
           no sub-minute latency; deletes are detected up to 24 h late.
Revisit when: The freshness target drops below 1 minute, or the API
           rate limit is lowered.
```

The most valuable lines in an ADR are the last two. "Consequences" forces you to state what you gave up, and "Revisit when" turns a permanent verdict into a conditional one with a trigger. Both make it easier for a successor to trust or challenge the decision intelligently.

> **Larkspur Outdoor: the first three decisions**
    Larkspur's integration team recorded three ADRs in its first fortnight. ADR-001 chose webhooks plus a queue plus a 15-minute reconciliation pull for orders arriving from the shop. ADR-002 chose to create orders in the ERP through its API with a lookup-before-retry safeguard, because the create call was not idempotent. ADR-003 chose code-first services on the company's existing container platform rather than buying an integration platform, with a stated revisit trigger of five or more shop-to-ERP flows. Chapter 25 follows these decisions to production.

## A Design Review Checklist

Before any integration design is approved, a reviewer should be able to answer the following questions from the design document. Use them to review your own work, and encourage others to use them on yours.

**Functional**

* Who is authoritative for each field?
* How are records matched across systems?
* How are deletes and renames handled?
* What is the freshness target, expressed as a number?
* What is the backfill plan for the initial load?

**Non-functional**

* What happens on timeout, duplicate, partial failure, and bad data?
* What is the request budget against each API?
* How is drift detected and repaired?
* Who is alerted, and what do they do?
* How are secrets rotated without downtime?

If a question cannot be answered, that is not a reason to stop; it is a reason to add the question to the open-items list with an owner and a date. Gates, which Chapter 3 introduces, are how a project makes sure open items are closed before they become incidents.

## Summary

An integration architect's job is to shrink the gap between the demo and the messy reality. They start from ten defaults, such as rate limits, partial failures, unsynchronized clocks, and rotating credentials, and design as if those were already happening. Three questions, where the truth lives, how fast change must travel, and what happens when it breaks, make most designs obvious.

The role covers a seven-phase lifecycle from discovery to retirement, and thirteen skill domains; being honest about which are your weak ones tells you what to learn next. Ten technology-independent ideas, from idempotency to ownership, reappear under different names on every platform. Six trade-offs, freshness against cost, coupling against simplicity, consistency against availability, build against buy, central against federated, and canonical against bounded, will be argued in every design review. Architecture decision records preserve what was chosen, why, and when to revisit it.

## Exercises

1. **Run the defaults on a real project.** Take an integration you work with and mark each of the ten defaults as *handled*, *partly handled*, or *ignored*. For each one marked *ignored*, write the symptom you would expect and how long it would take to notice.
2. **Rate yourself.** Score the thirteen skill domains from 1 to 5. Circle the three lowest and name one concrete action for each within the next month.
3. **Write an ADR.** Pick a past integration decision, perhaps one you disagreed with, and write it up in the template above. Add a "Revisit when" line that you would add today.
4. **Find the four numbers.** For an integration you know, estimate the current record count, the three-year count, the peak hourly change rate, and the acceptable staleness. If you cannot estimate one, whom would you ask?



---

# Part II. Discover and Decide

The questions to ask before anything is built, the landscapes your integrations live in, the patterns that solve recurring problems, and a method for choosing between them.



# Chapter 3. The Integration Journey

Larkspur Outdoor's first attempt to fix the nightly CSV problem took one week. A contractor wrote a script that read new orders from the shop's database and called the ERP's order API for each one. It worked on the contractor's laptop and in a demo. It went live on a Tuesday.

By week three, security discovered that the script used a personal ERP login and ordered it disabled. By week five, the ERP team revealed that the order API allowed 60 calls per minute, which was fewer than the shop produced at peak. By week eight, the shop's database administrator found the script's queries were slowing checkout and asked for it to be switched off. By week nine, nobody could say who was responsible for any of it, because the contractor had left.

None of these problems was exotic, and every one of them could have been found in the first two weeks by asking someone. The project did not lack skill. It lacked a *journey*: a sequence of stages, each ending with a decision, each decision backed by evidence, each piece of evidence owned by a person. This chapter describes that journey, and the four gates that keep a project honest.

> **In this chapter**
    * Explain what a gate is, and what separates a real gate from a rubber stamp
    * Describe the four gates of an integration project and the evidence each requires
    * Turn discovery answers into an architecture in the right order: constraints, pattern family, delivery vehicle
    * Assign roles with a RACI chart, and know who is usually missing from the room
    * Plan the first two weeks of a project so that long-lead items start on day one
    * Define "ready to build" and "done" so that both can be checked

## Why Projects Need Gates

A **gate** is a decision point at the end of a stage. The project does not proceed to the next stage until a named person agrees, on the basis of stated evidence, that the criteria for the stage have been met. That is all a gate is. It is not necessarily a meeting, it is not a bureaucratic ritual, and it is not a delay. It is the point at which the team stops and asks, "do we actually know what we think we know?"

Gates exist because integration projects carry a distinctive risk profile. The expensive surprises are rarely about code. They are about things outside the team's immediate control: a security review that takes six weeks, a firewall rule that needs a change board, an API limit nobody mentioned, a data owner who disagrees about who owns a field. These surprises cost the same whether they are discovered in week one or week eight, with one crucial difference. In week one you can plan around them. In week eight you are already committed.

The failure mode of gates is the rubber stamp. A gate review where the criteria are vague ("design is reasonable"), the evidence is a slide deck, and the approver has not read the material does not reduce risk. It manufactures false confidence. The cure is to define each gate with *testable criteria* and *named evidence*, which the rest of this chapter does.

> **Why this matters**
    Skipping a gate does not save time. It moves the discovery to production, where it is a lot more expensive. A useful test when someone proposes skipping a gate is to ask, "which of the things this gate checks do we already know for certain?" Usually the answer is "some of them," and the right response is to pass quickly on those and spend the time on the rest.

## The Journey with Four Gates

Every integration, on every technology, passes through the same sequence of stages. the figure shows them with the four gates that separate them.

*[Figure: The integration journey. Each of the four gates has criteria, an owner, and a list of evidence. A fifth, optional gate at the very start asks whether the integration should be built at all.]*
**Table: The gates, the question each answers, and the evidence that passes it**
| Gate | The question it answers | Passes when | Evidence | Failure if skipped |
|---|---|---|---|---|
| G0 (optional): Worth doing? | Should this be built at all? | Business outcome, owner, and a cheaper alternative have been considered | One-page case | Building integrations nobody needs |
| G1: Brief signed | Do we understand the problem? | At least 90% of critical discovery questions are answered; authority matrix agreed; the four numbers are known | Integration brief; question checklist; named owners | The right solution to the wrong problem |
| G2: Design approved | Is the design safe, feasible, and approvable? | Pattern chosen with rejected alternatives; contracts, authentication, and network path defined; security review done; decisions recorded | Design document; security approval; network diagram; ADRs | Firewall and review surprises in week eight |
| G3: Ready to release | Will it behave in production? | Contract, failure, and volume tests pass; reconciliation is clean; runbook accepted; rollback rehearsed | Test report; runbook; go-live checklist | Acceptance by demo |
| G4: Handover accepted | Can someone else run it? | The operations owner confirms; alerts reach them; hypercare exit criteria are met | Signed handover; alert test | Nobody owns it after you leave |

### G0: Is It Worth Doing?

Gate zero is optional because many integrations arrive pre-approved by someone senior. Even so, it pays to ask for a one-page case. State the business outcome, name the owner, and, most importantly, record the cheaper alternative you considered. Sometimes the cheaper alternative is "fix the nightly CSV so it rejects fewer rows," and sometimes it is "let the warehouse team query the ERP report directly." If nobody can describe an alternative, nobody has thought about the problem hard enough.

### G1: The Brief Is Signed

Gate one proves that you understand the problem. Its evidence is the **integration brief**, a document of one or two pages that Chapter 4 teaches you to write. It states the outcome, the systems and entities, the direction of flow, the authority for each field, and the four numbers: records now, records in three years, peak changes per hour, and acceptable staleness. The gate passes when at least 90 percent of the critical discovery questions have answers, and the remainder are on a risk register with an owner and a date.

The business owner signs this gate, not the architect. The reason is that the brief is, in effect, a promise: "this is what we will deliver, to this standard, for these people." If the business owner has not agreed to that promise, the project will be re-scoped halfway through.

### G2: The Design Is Approved

Gate two proves the design can actually be built and operated. The evidence is the design document, together with approvals from the people who can say no: security, network, and the owners of both systems. The document names the chosen pattern, and, just as importantly, names the alternatives that were rejected and why. It defines the contracts (what each API call looks like), the authentication method, and the network path, and it contains the decision records.

This is the gate teams skip most often, because it feels like paperwork. It is also the gate that would have saved Larkspur's contractor, because a network-and-security review in week one would have found the personal login, the rate limit, and the load on the shop's database before a line of code was written.

### G3: Ready to Release

Gate three proves the integration will behave in production, not merely in a demo. The evidence is test results, including the failure-injection tests that Chapter 16 describes. It includes a reconciliation report showing that source and target agree, a runbook that someone other than the author has actually executed, and a rollback plan that has been rehearsed.

The most commonly missed criterion is the rollback rehearsal. Teams write a rollback plan, never test it, and discover during an incident that it assumed a database backup that nobody had taken. Rehearse it once in a test environment, and the plan stops being fiction.

### G4: Handover Accepted

Gate four proves that someone else can run what you built. A typical project ends with a few weeks of **hypercare**, a period of intensified monitoring during which the build team remains on call. The gate passes when the exit criteria for hypercare are met (for example, three weeks without a severity-one incident), the operations owner confirms they can run the integration from the runbook, and a test alert has demonstrably reached them.

Without this gate the integration ends the way Larkspur's first attempt did: with a service nobody owns, running on a contractor's account, until the day it breaks.

## From Answers to Architecture

Discovery produces answers. Architecture is what you do with them. The order in which you use the answers matters more than most people expect, and the figure shows the correct order.

*[Figure: Constraints come first and rule options out. Only then do you choose a pattern family, and only after that a delivery vehicle. Unknowns are carried forward as risks, never silently assumed.]*
**Constraints come first.** Some answers eliminate options outright. If the network allows only outbound connections from the customer's data center, then any design that needs the source to call you (a webhook) needs an extra component or is out. If the target allows 60 requests per minute and you need 200, one-call-per-record is out. If the data is regulated and may not leave a region, some vendor clouds are out. Constraints are not preferences; you cannot negotiate with them, so apply them before anything else.

**Then the pattern family.** With the constraints applied, you choose among the families that remain: request-based, data-movement, messaging, routing and hub, authority and identity, or specialized. Chapters 6 and 7 describe forty-one patterns across these families. Narrowing to a family first prevents you from comparing a webhook with a nightly batch as though they answered the same question.

**Last, the delivery vehicle.** Only now do you ask whether to build the integration as code, on an integration platform, with cloud-native services, or on a streaming platform. The reason this comes last is that the vehicle should be chosen to *carry* the pattern, not to dictate it. Teams that pick the tool first spend the rest of the project arguing with it.

**Unknowns are risks.** If a critical question has no answer yet, the design must not silently assume a favorable one. Record the unknown as a risk with an owner and a date, and design so that either answer is survivable if you can. If you cannot, the gate stays closed.

Chapter 9 turns this order into a repeatable method with decision trees.

## Who Must Be Involved, and When

Integration projects span organizational boundaries, and one of the most reliable predictors of trouble is a missing voice. The usual absentees are security, network, and operations, who are also the people who can block a go-live. the table lists the roles that should be involved in each activity, using the standard RACI notation: **R**esponsible (does the work), **A**ccountable (answers for the outcome; exactly one per activity), **C**onsulted (is asked before the decision), and **I**nformed (is told after).

**Table: A RACI chart for an integration project**
| Activity | Business owner | Architect | Source owner | Target owner | Security | Network | Developers | QA | Operations |
|---|---|---|---|---|---|---|---|---|---|
| Define outcome and scope | A | R | C | C | I | I | I | I | I |
| Authority matrix and mappings | C | A | R | R | I | | C | I | I |
| Pattern and platform choice | C | A/R | C | C | C | C | C | | C |
| Security review and credentials | I | R | C | C | A | C | C | | I |
| Network path and firewall changes | I | R | C | C | C | A | C | | C |
| Build | I | C | C | C | I | I | A/R | C | C |
| Test and acceptance | A | C | C | C | I | | R | R | C |
| Cutover and backfill | A | R | C | C | I | C | R | R | R |
| Runbook, alerts, handover | I | C | I | I | I | | R | C | A |

Names will differ from project to project; the roles will not. Three points are worth drawing out. First, the architect is accountable for the authority matrix and the pattern choice, but is only *responsible* (not accountable) for security and network work: those belong to the people who own the decision. Second, the **operations** role is accountable for the handover, which is why they must be named before build starts, not at the end. Third, the **source owner** and **target owner** are responsible for the mapping, because only they know what their fields really mean.

## The First Two Weeks

A good project start looks unremarkable and saves months. The overriding principle is that **long-lead items start on day one**. Service accounts, sandbox access, firewall changes, and security reviews all depend on other people's calendars, and most of them take longer than you expect. the table shows a typical plan.

**Table: A plan for the first two weeks**
| Days | Activity | Output |
|---|---|---|
| 1 to 2 | Kick off with the business owner and both system owners. File every long-lead request now: service accounts, sandbox access, firewall and security review. | Named contacts; requests filed with dates |
| 2 to 4 | Run the discovery workshops using the question bank. Draw the current-state flow, including the manual steps. | Answered and open question lists; current-state diagram |
| 4 to 6 | Explore both APIs with `curl` against the sandbox (Chapter 10). Record limits, pagination, errors, and authentication in a reconnaissance sheet. | Two reconnaissance sheets based on observed behavior |
| 6 to 8 | Hold the authority and mapping workshop. Agree identity, deletes, and ordering. | Signed authority matrix |
| 8 to 10 | Apply the decision method (Chapter 9), compare the top two patterns, write the decision records, and estimate (Chapter 28). | Draft design and an estimate range |

Notice what is *absent* from this plan: no coding. The first technical activity is exploring the real APIs with `curl`, because documentation is wrong somewhere and you want to learn where before you design around it. Chapter 10 shows how.

> **Larkspur Outdoor: the second attempt**
    When Larkspur restarted the project with a proper journey, the first two days produced five requests that would have taken the contractor's project eight weeks to discover: a service account for the ERP, a sandbox for the shop, a firewall review for the private link, a security review slot, and a calendar hold with the ERP team's DBA. The fastest of the five took nine working days to complete. Because they were filed on day one, none of them delayed the build.

## Definitions of Ready and Done

Two short checklists prevent most arguments about whether work is ready to start or finished. Write them down at the start and agree them with the business owner.

**Ready to start building** means the following are all true:

* Gate G2 has passed: security and network approvals are in hand.
* Credentials and sandboxes exist for every environment.
* The authority matrix and mapping table are signed.
* Acceptance criteria are written as numbers.
* An operations owner is named.

**Done** means these are all true:

* The integration is idempotent and restart-safe, *proved by killing it mid-run*.
* Failure handling, quarantine, and dead letter handling are in place.
* Alerts, a dashboard, and a run summary are live.
* The runbook is accepted and has been rehearsed.
* The reconciliation report shows agreement and the backfill is complete.

The phrase "proved by killing it mid-run" is deliberate. Statements such as "it handles restarts" are opinions; a test that kills the process halfway through a batch and then verifies that the target has no gaps and no duplicates is evidence.

## Running a Gate Review

A gate review does not need to be long, but it does need to be real. A format that works for most projects:

1. **Circulate the evidence 48 hours ahead.** The approver reads it before the meeting, not during it.
2. **Spend the meeting on the weakest evidence,** not the strongest. The team should say, "here is what we are least sure of," and the approver should push on exactly those points.
3. **Record one of three outcomes:** *pass*, *pass with conditions* (each condition has an owner and a date), or *fail* (with the specific missing evidence).
4. **Publish the outcome** where the whole project can see it.

The third outcome, "pass with conditions," is the most useful and the most abused. A condition must be concrete ("security approval for the ERP service account, due by the 14th") and must be checked at the next gate. A condition such as "monitor security risks" is a way of not deciding.

## Gates in Agile Delivery

Teams that work in short iterations sometimes feel that gates belong to a slower world. They do not have to. The idea of a gate is *criteria checked before proceeding*, and agile teams already use the concept under other names: a "definition of ready" for stories, a "definition of done," a release checklist. The adaptation is to apply the integration-specific gates to the *whole integration* while the team still delivers in thin slices.

In practice that means three things. Run discovery and design for the whole integration up front, in the first one or two weeks, so that the expensive surprises surface early. Build in vertical slices (one entity, end to end, through to a test environment) so that each slice proves the network path, the authentication, and the failure handling on a small scale. And treat G3 and G4 as release-level criteria that apply to the first production slice and are inherited, with only the changes re-checked, by later ones.

## Handover and Hypercare

The final stage is where good projects distinguish themselves. **Hypercare** is a defined period, typically two to four weeks, in which the build team stays on call, the alert thresholds are tuned on real traffic, and the operations owner shadows and then takes over incident response. Define its exit criteria up front, as numbers: no severity-one incidents for fourteen consecutive days; alert noise below an agreed level; reconciliation clean for seven consecutive days; the operations owner has resolved at least one real incident using the runbook alone.

Hypercare is also when the runbook is corrected. No runbook survives contact with production unchanged. Every question the operations team asks during hypercare is a gap in the document, and every gap should be closed before the gate. Chapter 26 describes what a good runbook contains.

## Summary

An integration project needs a journey: stages that end in decisions, decisions that rest on evidence, evidence that someone owns. Four gates give the journey its shape. G1 proves you understand the problem, G2 that the design is safe and feasible, G3 that it will behave in production, and G4 that someone else can run it. An optional G0 asks whether to build it at all.

Discovery answers become architecture in a fixed order: constraints rule options out, then you choose a pattern family, and only then a delivery vehicle. Unknowns are recorded as risks, never assumed away. A RACI chart makes sure that security, network, and operations are in the room, and the first two weeks put long-lead requests in motion before any code is written. Definitions of ready and done turn opinions into checks, and a gate review, held honestly, replaces a rubber stamp with a decision.

## Exercises

1. **Gate your current project.** Take an integration you are working on and evaluate it against G1 to G4. For each gate, list the criteria you cannot yet prove. Which would you close first?
2. **Find the missing role.** Fill in the RACI chart for a real project. Which column has no named person? What would happen if that person learned about the project in week eight?
3. **Write the long-lead list.** List every request on your project that depends on someone else's calendar (accounts, access, reviews, network changes). Estimate the elapsed time of each, and work out which one sets the earliest date you can go live.
4. **Define your own hypercare exit.** For a real or imagined integration, write five numeric exit criteria for hypercare.



# Chapter 4. Discovery: Asking the Right Questions

Larkspur's second attempt began with a workshop, and the first ten minutes were uncomfortable. The business owner, Head of E-commerce, described the goal as "getting orders into the ERP faster." The ERP product owner said that was already happening, because the nightly import worked. The warehouse manager disagreed, loudly, and mentioned the 214 rejected rows. The finance lead pointed out that order totals in the shop and the ERP differed by small amounts after discounts and nobody knew why. The architect wrote four numbers on the whiteboard and asked for each of them, and nobody in the room knew more than two.

By the end of ninety minutes the room had agreed on something precise: *99 percent of orders in the ERP within five minutes; shipping status back on the shop within thirty minutes of dispatch; the shop owns the order and the customer's address; the ERP owns price confirmation, stock, and invoices.* That sentence took ninety minutes and replaced three weeks of misaligned assumptions.

Discovery is the discipline of getting to that sentence on purpose. It is the cheapest phase of an integration project and the one most often cut. This chapter teaches you to run it: the seven dimensions to cover, the four numbers to leave with, how to run a workshop that produces answers instead of opinions, and how to turn the answers into a brief the business will sign.

> **In this chapter**
    * Cover the seven dimensions of integration discovery and recognize red-flag answers
    * Turn a vague request into a precise brief, and read the design consequences hidden in it
    * Obtain the four numbers that let you size almost any design
    * Plan and run a ninety-minute discovery workshop, and the follow-up sessions
    * Build an authority matrix that makes ownership explicit
    * Handle unanswered questions as risks rather than assumptions

## The Seven Dimensions

Before choosing REST or Kafka, run discovery across seven dimensions. They are deliberately broader than "technical requirements," because most of the facts that decide an integration are not technical. the table lists each dimension with the questions to ask, what a good answer looks like, and the red-flag answer that should make you probe harder.

**Table: The seven dimensions of discovery**
| Dimension | Questions to ask | A good answer looks like | Red flag |
|---|---|---|---|
| Business | Why does this integration exist? Who is the business owner? What decision or process depends on it? What does a day of downtime cost? | "Stewards must see incident status inside the catalog to close audit findings" | "We just want the systems connected" |
| Data | Which entities and fields? Volume today and in three years? Rate of change? Which system is authoritative per field? Any personal or regulated data? | A field-level authority matrix, row counts, peak change rate | "Everything," or "we are not sure who owns it" |
| Interface | What does the source expose: REST, SOAP, database access, files, events? Is there an OpenAPI specification? A versioning policy? A sandbox? | A specification in hand, sandbox access granted, a contact on the API team | "Our developer will send the docs" |
| Timing | What freshness is required? Is there a batch window? Does order matter? Is real time needed or merely desired? | "Within fifteen minutes; order matters per ticket only" | "Real time," with no number attached |
| Non-functional | Availability target, throughput, latency, retention, audit trail, disaster recovery | Numbers, not adjectives | No service-level discussion at all |
| Security and network | Which authentication method? Where does the integration run? Which firewalls and proxies? Who approves a service account? Data residency? | A network diagram, a named security approver, a service-account process | "We will sort security later" |
| Operations | Who runs it, monitors it, is paged? What is the release process? How are secrets rotated? What is the support model? | A named team and an accepted runbook | "The vendor will maintain it" (said by everyone) |

Two observations about this table matter more than any single row. First, **the red flags are all vague.** A good answer has a number, a name, or a document attached. When an answer is an adjective or a promise, you have not received an answer; you have received a placeholder. Second, **the dimensions interact.** A "real time" timing answer combined with an "outbound-only" network answer already tells you something important: webhooks will need an extra component, and polling must be fast. Good discovery notices these interactions while the room is still full.

## From Vague to Precise

The core skill of discovery is converting a sentence of intent into a statement that can be tested. The conversion usually surfaces decisions nobody knew they were making.

> **A vague request and its precise brief**
    **Vague.** "Integrate the ticketing system with the data catalog so incidents show up."

    **Precise.** Data-quality issues of type *Critical* in the catalog create an incident in the ticketing system when their status moves to *Accepted*. Status, assignee, and comments synchronize in both directions within five minutes. The ticketing system is authoritative for incident state; the catalog is authoritative for the issue description. About 300 issues per month, peaking at 40 per hour. The integration runs on a company virtual machine with outbound HTTPS only.

The second version implies a surprising amount of design. Polling at short intervals is acceptable, so no streaming platform is needed. A status-mapping table is required, because the two systems use different status vocabularies. A loop-prevention strategy is required, because both systems write to each other. A service account is needed on each side. And the monthly volume of 300 issues, with a peak of 40 per hour, tells you that rate limits are unlikely to matter and that the cheapest design that meets the five-minute target is the right one. That is what discovery buys: *each precise sentence removes a branch of the design tree*.

## The Four Numbers

Leave every discovery session with four numbers, and keep asking until you have them.

1. **Records now.** How many of each entity exist today?
2. **Records in three years.** Growth is usually underestimated. Ask for the plan, not the hope.
3. **Peak changes per hour.** The busiest hour of the busiest day, not the average. Black Friday, month-end close, the Monday-morning surge.
4. **Acceptable staleness, in minutes.** How old may the data be at the target before someone makes a wrong decision?

With these four numbers you can size an API budget, decide between polling and streaming, estimate cost, and judge whether a platform's limits will hold. Without them, every later conversation about design is a conversation about adjectives.

> **Getting a number out of someone who does not have one**
    When a stakeholder says "I don't know how many," do not accept it, and do not guess for them. Ask a bracketing question: "Is it closer to a thousand, a hundred thousand, or ten million?" Almost everyone can answer that, and one order of magnitude is enough for design. Then ask who *could* give an exact figure, and record that person's name.

### Estimating Volume in Your Head

You will often need to turn a business statement into a request rate on the spot. The arithmetic is simple, and doing it aloud in the workshop builds credibility. Larkspur's shop takes 4,000 orders per day, with a peak hour carrying about 1,200. Each order has three lines on average. Creating one order in the ERP takes one API call. At the peak that is 1,200 calls per hour, or one call every three seconds, about 0.33 calls per second. Even allowing growth of 30 percent a year for three years, you need roughly 0.7 calls per second: well under the ERP's limit of one per second. That single paragraph of arithmetic tells you *one call per order is feasible, and no batching is required*.

Now change one number. If the ERP's limit were 0.2 calls per second, the same arithmetic would say the design is infeasible, and you would need a bulk endpoint or an import job. The calculation took thirty seconds and saved a failed design.

## The Authority Matrix

Of all the artifacts discovery produces, the most valuable is the **authority matrix**: a table that lists each entity and field and names the one system that is authoritative for it. It is the document that prevents the most expensive kind of integration problem, two systems both editing the same data.

**Table: An authority matrix for the shop-to-ERP integration**
| Entity and field | Authoritative system | Other systems | Direction of change | Notes |
|---|---|---|---|---|
| Order: lines, quantities | Shop | ERP (read-only copy) | Shop to ERP | Frozen once the ERP confirms |
| Order: confirmed price | ERP | Shop (read-only) | ERP to shop | Shop price kept for comparison only |
| Order: shipping status | ERP | Shop | ERP to shop | Events from the warehouse system |
| Customer: shipping address | Shop | ERP | Shop to ERP | Customer edits at checkout and in the account page |
| Customer: credit limit | ERP | Shop | None | The shop never needs it |
| Product: stock level | ERP | Shop (cache) | ERP to shop | Refresh every five minutes |

The matrix does two jobs. It tells the build team which flows exist and which direction each runs. More valuably, it forces a conversation. The first time Larkspur filled in the row for "customer shipping address," the shop team and the ERP team each assumed they owned it. The resolution, shop-owned with the ERP receiving a copy, was reached in five minutes and eliminated a whole class of overwrite bugs. When you genuinely cannot assign a single owner to a field, you have found a problem that needs a business decision, not a technical one. Chapter 7 covers what to do when two systems must both edit.

## Running the First Workshop

Discovery is a conversation, and conversations need structure. A ninety-minute first workshop with the business owner, both system owners, and the architect covers six topics.

**Table: A ninety-minute first-workshop agenda**
| Minutes | Topic | Output |
|---|---|---|
| 10 | Business outcome and owner | One sentence of purpose; the accountable name |
| 15 | Current-state data flow, drawn on a whiteboard, including manual steps | A diagram of what happens today |
| 20 | Entity and field authority | A first authority matrix |
| 15 | Freshness, volume, and failure tolerance | The four numbers |
| 20 | Interfaces on each side, authentication, network path | A list of interfaces and unknowns |
| 10 | Operations, ownership, and what "done" means | A named operations owner; acceptance criteria |

A few techniques make the session productive.

**Draw the current state, including the people.** Ask someone to walk through how an order gets from the shop to the ERP *today*. Draw every step, including "Maria opens the CSV and fixes the rejected rows." Manual steps are where the hidden rules live: Maria knows that rows with a missing postcode go to a different queue, and nobody has written that down. If the integration automates the file but not Maria's knowledge, it will fail in the same way the file did.

**Walk the data.** Ask to see a real record, ideally the largest and the ugliest. Real records contain the surprises that schemas do not: the 4,000-character comment, the customer name with an emoji, the order with 400 lines.

**Separate what from how.** Stakeholders often arrive with a solution ("use a message queue"). Acknowledge it, write it down, and steer back to the need ("what must be true when it is done?"). The solution may be right, but it should be chosen from the facts rather than imported from the first meeting.

**Send each group their questions a day ahead.** Do not read a list aloud to a room of five groups. Send business, data, interface, security, and operations stakeholders the questions that concern them, and run a short session per group. Appendix A contains the full bank of 125 questions, grouped by who can answer them, with the design consequence of each.

### Red-Flag Questions

When something feels off, these questions reliably surface the truth. Ask them politely, and listen to the pause before the answer.

* "Has anyone actually called this API in production?" Many internal APIs have never been called by anyone outside the team that wrote them.
* "What happened the last time the source team changed this interface?"
* "Can I see the largest record or file you have?"
* "Which fields are free text, and who types into them?"
* "If this integration stopped for a week, who would notice first?"

The last question is the most revealing. If the answer is "nobody," the integration may not be needed. If the answer is "the CFO," you have just identified your real business owner.

## Reading the Design Consequences

Every discovery question exists because its answer changes the design. Making that link explicit helps you decide which questions to press and which to let go. the table shows ten examples from the question bank.

**Table: Ten questions and what their answers change**
| Question | If the answer is unfavorable | The design changes by |
|---|---|---|
| What does an hour of downtime cost? | "Orders stop and we lose revenue" | Setting a higher availability tier, alerting, and replay |
| Which system is authoritative for each field? | "Both can edit" | Adding conflict rules, loop prevention, and locking |
| Does the source offer a modified-since filter? | "No" | Using snapshot and diff, or change data capture, instead of polling |
| Are the source's modified timestamps reliable? | "We are not sure" | Adding an overlap window and a nightly reconciliation |
| How does the source signal deletes? | "It doesn't" | Scheduling a periodic full comparison |
| Are target writes idempotent? | "No, create-only" | Adding lookup-before-retry or a deduplication table |
| Which connections may be opened? | "Outbound only" | Preferring polling or an outbound agent; ruling out plain webhooks |
| What are the API rate limits, and are they shared with other integrations? | "60 per minute, shared" | Modeling a request budget; using bulk endpoints; throttling |
| Is the data personal or regulated? | "Yes" | Adding masking, residency constraints, and a security review |
| Who is on call after go-live? | "Nobody yet" | Holding the go-live gate until an owner is named |

Reading answers this way also protects you from a subtle trap: collecting facts without using them. A question whose answer changes nothing is not worth the stakeholder's time. When you are short of time, prioritize the **critical questions**, the 50 of the 125 in the question bank whose unfavorable answers change the architecture.

## Handling the Unknown

You will not get every answer, and that is acceptable if you handle the gaps honestly. For each critical question that remains open, create an entry on the **risk register** with three fields: *what we do not know*, *the person who could tell us*, and *the date by which we need it*. Then ask what the design would look like under each possible answer. If both answers lead to the same design, the unknown is harmless. If they lead to different designs, the risk is serious, and the gate should stay closed until the answer arrives.

The unforgivable move is to assume. "We assumed the API supported idempotency keys" is the opening line of many incident reports. An assumption that has been written down as an assumption, with an owner who will verify it, is a risk. An assumption nobody noticed making is a defect.

## The Integration Brief

Discovery ends with the **integration brief**, a one- or two-page document the business owner signs to pass the first gate. A good brief is brief: its purpose is to be read and agreed, not to be a specification.

```text
INTEGRATION BRIEF  -  Orders: shop to ERP                      v1.0
Outcome:    99% of orders in the ERP within 5 minutes; shipping status
            on the shop within 30 minutes of dispatch.
Owner:      Head of E-commerce (accountable); ERP product owner.
Systems:    Web shop (SaaS, REST + webhooks)  ->  ERP (OData, events).
Entities:   Orders, order status, customer crosswalk.
Authority:  Shop owns order capture and address; ERP owns confirmed
            price, stock, shipping status. (Matrix attached.)
Numbers:    4,000 orders/day now; 9,000 in three years; peak 1,200/hour
            (2,000 in three years); staleness target 5 minutes.
Network:    ERP in company data center; cloud runtime over private link.
Security:   Personal data; dedicated service accounts; review lead time
            four weeks (filed on day one).
Failure:    Replay after outage; quarantine bad orders; alert to the
            e-commerce platform team; reconciliation every 15 minutes.
Out of scope: Returns; invoicing.
Open risks: (1) ERP order API not idempotent (owner: ERP team, due 14th).
            (2) Webhook replay unsupported by the shop (owner: vendor).
Acceptance: Reconciliation shows 100% of sampled orders correct;
            peak-hour load test passes within 70% of the API budget.
```

Read the brief again with the design in mind. The two open risks are the ones that will shape the architecture: a non-idempotent create call and a webhook feed with no replay. Chapter 25 shows how Larkspur's design answered both.

## Summary

Discovery is the cheapest and most skipped phase of an integration project. It covers seven dimensions, business, data, interface, timing, non-functional, security and network, and operations, and a good answer in any of them has a number, a name, or a document attached. Vague answers are placeholders, not answers.

Four numbers (records now, records in three years, peak changes per hour, acceptable staleness) let you size almost any design, and simple arithmetic on them decides feasibility in seconds. The authority matrix assigns every field to exactly one system and surfaces ownership disputes early. A ninety-minute workshop, run with drawings of the real current state, real records, and a separation of needs from solutions, produces the answers. Unknowns become risks with owners and dates, never silent assumptions, and the whole exercise ends in a signed one-page brief.

## Exercises

1. **Convert a vague request.** Take a one-sentence integration request from your own work and rewrite it as a precise brief of five or six sentences. List the design decisions that the precise version implies.
2. **Do the arithmetic.** For an integration you know, estimate the four numbers. Compute the average and the peak request rate per second. Does the target system's rate limit allow it?
3. **Build an authority matrix.** Choose two systems and ten fields they share. For each, name the authoritative system. For which fields did you hesitate? Whom would you ask?
4. **Run the red-flag questions.** Ask the five red-flag questions about an integration in your organization. Write down the most surprising answer.



# Chapter 5. Where Integrations Run

Before patterns come places. Two integrations that use exactly the same pattern, say "poll the source every five minutes and upsert into the target," can be trivial or painful depending on one question: *where do the systems live, and who may open a connection to whom?* A poller between two cloud applications is an afternoon's work. The same poller between a mainframe in a locked-down data center and a SaaS product can take six weeks, because the work is no longer the polling; it is the firewall change, the certificate, the proxy, and the approval chain.

For that reason, experienced architects draw the network before they draw the data flow. This chapter describes the seven topologies that cover almost every engagement, with the tools you will meet in each and the failure modes to look for. It then compares the places an integration runtime can live, translates the vocabulary of the three major clouds into one another, and ends with a checklist of network facts to establish in week one.

> **In this chapter**
    * Recognize the seven integration topologies and the one question that distinguishes them
    * Explain why an outbound agent is the approach security teams approve fastest
    * Choose where an integration runtime should live, and what each choice costs
    * Translate a design between AWS, Azure, Google Cloud, and on-premises equivalents
    * Run a network fluency check that finds firewall, proxy, and certificate problems before go-live

## The Question That Decides Everything: Who Opens the Connection?

Every topology in this chapter is, at bottom, an answer to one question: **which side is allowed to initiate a connection?** In a modern cloud, any service can call any other over the internet, so the question barely arises. Inside a corporate network, the default is the opposite. Firewalls block inbound traffic from outside, and outbound traffic is allowed only through approved proxies to approved destinations. Security teams are conservative about inbound rules for good reason: each one is a door that attackers can try.

This asymmetry explains most of the patterns you will see. An agent that opens a connection *outward* needs no inbound rule, which is why it is approved quickly. A webhook, which requires the source to call *you*, needs an inbound path and often a long review. Polling needs only outbound access, and that, as much as technical preference, is why it remains the workhorse of enterprise integration. When you read the topologies below, notice in each one which arrow crosses a firewall, and in which direction.

## Topology 1: SaaS to SaaS

The simplest topology connects cloud applications to each other. Larkspur's marketing platform needs customers from the shop; the support tool needs orders from the ERP's cloud edition. Everything is reachable over the internet, authentication is OAuth, and rate limits are the main constraint. the figure shows the shape.

*[Figure: SaaS to SaaS. Everything is reachable over the internet. A cloud integration platform or serverless glue is usually the fastest answer. Webhooks and polling both work; REST calls write to the targets.]*
The runtime sits in a vendor's or your own cloud account. One SaaS application sends webhooks to the platform, or the platform polls it (arrow 1), and the platform writes to the other two applications through REST calls (arrows 2 and 3). Typical tools are cloud integration platforms such as Workato, Boomi, Celigo, or MuleSoft's cloud runtime, lightweight automation services such as Zapier and Power Automate for simple flows, and serverless functions for custom glue.

**Watch for:** vendor API rate limits shared with other integrations on the same tenant; the reliability of webhooks, especially whether the vendor can *replay* missed events; the question of whose user identity the integration runs as (a flow built on an employee's OAuth grant breaks the day the employee leaves); and task-based pricing that grows with volume.

## Topology 2: On Premises to the Cloud Through an Agent

Often one of the systems lives inside the company network: the ERP in the data center, a database, a file share. The cloud integration platform cannot reach it, and nobody will open an inbound firewall rule for it. The standard answer is the **agent**: a small piece of software installed inside the network that opens a connection *outward* to the cloud platform and keeps it open. the figure shows the arrangement.

*[Figure: On premises to the cloud through an outbound agent. The agent opens the connection outward, so no inbound firewall rule is required. That is why security teams approve it fastest.]*
Inside the customer data center, the agent reads the ERP, the database, and the file shares locally (using protocols such as JDBC and SMB). It holds an outbound TLS connection to the platform's cloud control plane, where the flows are designed and monitored, and it reaches SaaS applications over HTTPS. Because every connection starts inside and goes out, the firewall needs only the rules that already allow outbound web traffic.

Products with this shape include Boomi's Atom, Workato's on-premises agent, SnapLogic's Groundplex, Microsoft's self-hosted integration runtime and on-premises data gateway, and customer-hosted runtimes of MuleSoft. The details differ in a way that matters: in some products the agent *runs* the business logic locally and only reports to the cloud, in others the agent merely provides access while the logic executes in the vendor's cloud. That changes where your data is processed, which matters to privacy and residency reviews. Ask the question explicitly rather than assuming.

**Watch for:** where logic and data actually execute; agent high availability (a single agent is a single point of failure, so use clustered agents); who patches the agent; and whether it supports your corporate proxy, including authenticated proxies.

## Topology 3: Hybrid with Private Connectivity

When volumes are high, latency matters, or policy forbids sending data across the public internet, companies join their data center to a cloud network with a private link. the figure shows the arrangement.

*[Figure: Hybrid with private connectivity. A private link joins the data center to a cloud network. Platform services are reached through private endpoints, never over the public internet.]*
On the left, the data center holds the on-premises applications and message queues behind a firewall and proxy. A private link (a site-to-site VPN, or a dedicated circuit such as AWS Direct Connect, Azure ExpressRoute, or Google Cloud Interconnect) carries traffic to the cloud network on the right. There the integration runtime, perhaps on virtual machines or a Kubernetes cluster, calls the cloud's managed services through *private endpoints* that never expose them to the internet.

The technology is mature, and the difficulty is almost entirely organizational. **Lead time** is the first surprise: a dedicated circuit takes weeks to provision, so order it before you finish the design. Next, **overlapping IP ranges**: two companies that merged often both use the same private address space, and no routing trick fully hides that. Then **DNS across the boundary**: a name that resolves one way inside the data center and another way inside the cloud will produce failures that look like application bugs. Add MTU and fragmentation issues for large payloads, and the cost of data leaving the cloud.

## Topology 4: Multi-Cloud with an Event Backbone

Large companies rarely live in one place. Applications run in two clouds and a data center, a data platform consumes from all of them, and partners connect through an integration layer. Point-to-point links between all these locations multiply quickly. The answer is an **event backbone**: a streaming platform, such as Kafka, or an event mesh that all locations publish to and subscribe from. the figure shows it.

*[Figure: Multi-cloud with an event backbone. Applications in each cloud and in the data center publish to and subscribe from a shared backbone, which also feeds the data platform and, through connectors and an integration platform, SaaS applications and partners.]*
Applications in a first cloud, a second cloud, and the data center all publish and consume events through the backbone at the center. The backbone feeds the data platform (a lakehouse, through sink connectors) and reaches SaaS applications and partners through an integration platform. No application knows the location of any other; each knows only the backbone. Tools include Kafka with cluster linking or MirrorMaker 2, commercial event meshes such as Solace or SAP Advanced Event Mesh, and cloud-native buses bridged by connectors. Chapters 18 to 20 cover this in depth.

**Watch for:** data egress charges between clouds, which can dominate the bill; topic governance, since a backbone that anyone can write to becomes a swamp; schema ownership; and the temptation to make a single cluster the single point of failure for the whole company.

## Topology 5: Mainframe and Legacy Offload

Core systems of record, often mainframes, hold the most valuable data in a company and are the systems everyone is most afraid to touch. The pattern here is to **leave the core alone** and take data from the edges of it. the figure shows two ways.

*[Figure: Mainframe and legacy offload. The core system is left untouched. Messages are taken from its message queue, or changes are captured from its database log, and published outward.]*
The mainframe runs its transaction monitor, its COBOL programs, and its Db2 database. Many of its applications already write messages to IBM MQ, and an MQ-to-Kafka bridge or connector can publish them outward without any change to the applications. Alternatively, a change data capture tool reads Db2's log and publishes every row change. Both approaches avoid adding queries to the core, which matters because mainframe capacity is often billed by usage.

**Watch for:** EBCDIC text encoding and packed-decimal numbers, which need conversion; batch windows in which the system is busy; per-query cost; change-freeze calendars that block deployments for months; and, above all, the small number of people who still understand the system. Find them early.

## Topology 6: Partner and B2B Connectivity

When external parties connect, such as suppliers sending invoices or retailers sending orders, the security posture changes. Partners are outside your control, and anything exposed to them is exposed to the internet. the figure shows the standard shape.

*[Figure: Partner and B2B connectivity. Partners enter through a hardened component in the demilitarized zone, a web application firewall and API gateway for APIs, or a managed file transfer server for files. Nothing from the internet touches internal systems directly.]*
A partner reaches either a web application firewall and API gateway (for API calls) or a managed file transfer server (for AS2 or SFTP exchanges), both located in a demilitarized zone, or DMZ, a network segment between the internet and the internal network. Messages pass from there to an integration layer, which validates and translates them before anything reaches the ERP and core systems. At no point does a partner's traffic reach an internal system directly.

Typical tools are API gateways with web application firewalls, managed file transfer products such as Axway, IBM Sterling, GoAnywhere, and Cleo, AS2 and value-added-network gateways, and EDI translators. **Watch for:** partner certificates and their rotation, IP allowlists that partners insist on, acknowledgment and non-repudiation requirements, and the onboarding effort per partner, which is usually the real bottleneck.

## Topology 7: Edge, Factory, and Store Sites

The last topology is the one where the network is least reliable. Factories, warehouses, ships, and retail stores must keep operating when the wide-area link fails. the figure shows how.

*[Figure: Edge, factory, and store sites. Local devices connect through an edge gateway to a local broker that buffers and forwards when the wide-area link returns. The cloud side receives the messages through an IoT hub and passes them to Kafka and the lake.]*
At the site, sensors and programmable logic controllers speak industrial protocols such as OPC UA and Modbus. An edge gateway converts them to a common messaging protocol and passes them to a **site broker**, often an MQTT broker. The broker stores messages while the wide-area link is down and forwards them when it returns. In the cloud, an IoT hub receives the messages and bridges them to Kafka and the data lake.

**Watch for:** intermittent connectivity and what "store and forward" does to message ordering; the management of device identities and certificates across thousands of devices; time synchronization, because a sensor with a wrong clock produces wrong data; and the data volume, which can be enormous.

> **Why this matters**
    A design that is correct for a data center is often wrong for a store. A store may lose connectivity for hours and must keep selling. If your integration treats "the ERP is unreachable" as an error that stops the checkout, you have designed for the data center. Ask of every site: "what happens when the link drops for an hour?"

## Where Should the Integration Runtime Live?

Having drawn the topology, you must decide where the integration code actually runs. the table compares the main options.

**Table: Where an integration runtime can live**
| Option | Best when | Control | Operational burden | Main risk |
|---|---|---|---|---|
| Vendor-hosted cloud runtime | All endpoints are SaaS or internet-reachable | Low | Low | Data residency and cost curve |
| Customer-hosted runtime (VM, container, Kubernetes) | Data must stay in your network or region; high volume | High | High | You own patching and scaling |
| Agent plus cloud control plane | You want cloud tooling but have on-premises sources | Medium | Medium | Unclear where processing happens |
| Serverless functions | Small event-driven glue | Medium | Low | Time limits, cold starts, hidden coupling |
| Containers on Kubernetes | Many small integrations and a platform team | High | High | Cluster expertise required |
| A scheduled job on a virtual machine | Few integrations; simple schedules; outbound only | High | Medium | Becomes a snowflake without delivery pipelines and monitoring |

The last row deserves a comment, because it is how many integrations begin. A Python script on a virtual machine is cheap, understandable, and a reasonable start. It becomes dangerous when it is the *only* copy, nobody has the deployment steps, and its monitoring is "someone would notice." Chapter 17 describes how to turn such a script into a maintainable service, and Chapter 23 describes when a platform is a better choice.

## The Cloud-Service Translation Table

An architect who knows one cloud can read the others if they know the equivalents. the table lists the equivalent service for each common integration capability. Treat it as a map, not an equivalence: services with similar names differ in limits, semantics, and pricing, so verify the details before you rely on a mapping.

**Table: Equivalent services across clouds and on premises**
| Capability | AWS | Azure | Google Cloud | On premises or neutral |
|---|---|---|---|---|
| Queue | SQS, Amazon MQ | Service Bus queues, Storage queues | Pub/Sub (pull subscription), Cloud Tasks | IBM MQ, RabbitMQ, ActiveMQ Artemis |
| Topic (pub/sub) | SNS, EventBridge | Service Bus topics, Event Grid | Pub/Sub, Eventarc | RabbitMQ exchanges, Solace |
| Streaming log | Kinesis, MSK | Event Hubs (with Kafka endpoint) | Pub/Sub, managed Kafka | Kafka, Redpanda, Pulsar |
| API management | API Gateway | API Management | Apigee, API Gateway | Kong, WSO2, Axway, MuleSoft |
| Workflow | Step Functions | Logic Apps, Durable Functions | Workflows, Application Integration | Camunda, Temporal, Airflow |
| Serverless compute | Lambda | Functions | Cloud Functions, Cloud Run | Knative, OpenFaaS |
| File transfer | Transfer Family, S3 | Blob Storage SFTP, Data Factory | Storage Transfer Service | Axway, Sterling, GoAnywhere |
| Data pipelines | Glue, DMS, AppFlow | Data Factory, Synapse pipelines | Dataflow, Datastream, Data Fusion | Informatica, Talend, NiFi, Airflow |
| SaaS connectors | AppFlow, EventBridge API destinations | Logic Apps connectors, Power Automate | Application Integration connectors | iPaaS connector libraries |

## Network Fluency: What to Establish in Week One

Many integration incidents are network incidents wearing an application costume. The following facts, collected in the first week, prevent most of them. Treat them as questions for the network and security teams, and record the answers in the design.

**The path.** Trace a request from the integration runtime to each system, naming every hop: proxy, firewall, load balancer, gateway. Every hop is a place a request can be blocked, rewritten, or delayed. If you cannot draw the path, you do not know it.

**The proxy.** Does outbound traffic go through a proxy? Does it require authentication? Does it inspect TLS, replacing the server's certificate with the company's own? TLS inspection is a frequent cause of "it works on my laptop, but not on the server": the runtime does not trust the company's certificate authority. Fix it by installing the corporate certificate authority into the runtime's trust store, never by disabling certificate verification.

**Egress addresses.** Vendors often allow API access only from approved IP addresses. Find out what address your runtime's traffic leaves from. A cloud runtime may use a pool of addresses that change; request a fixed one (a NAT gateway with a static address) if the vendor needs an allowlist.

**DNS.** Does the name of the target resolve to the same address from the runtime as from your laptop? Private endpoints and split-horizon DNS make this a common cause of confusing failures.

**Certificates and expiry.** List every certificate in the path: server certificates, client certificates for mutual TLS, partner certificates. Record the expiry dates in the inventory and alert sixty days ahead. Certificate expiry is among the most predictable outages and still among the most common.

**Idle timeouts.** Load balancers, firewalls, and NAT devices close idle connections after a period, often 60 to 350 seconds. A long-running request, or a pooled connection reused after sitting idle, can fail with a reset. Set client-side keepalives and timeouts below the shortest idle timeout on the path.

**Time.** Make sure the runtime's clock is synchronized (NTP). Signed requests, token validity, and replay protection all assume clocks agree to within a few minutes, and so do your watermarks.

**Latency and bandwidth.** Estimate the round-trip time between the runtime and each system and multiply it by the number of sequential calls. One hundred sequential calls at 80 milliseconds each is eight seconds; across a continent it can be much more. This arithmetic decides whether a design should batch or run calls in parallel.

## Summary

Before patterns come places. The question that distinguishes topologies is *who may open the connection*: inbound rules are scarce and slow to obtain, outbound access is easy, and that asymmetry explains the popularity of polling and agents. Seven topologies cover most work: SaaS to SaaS; on premises to cloud through an outbound agent; hybrid with private connectivity; multi-cloud with an event backbone; mainframe offload; partner connectivity through a DMZ; and edge sites that must survive a lost link.

Where the runtime lives is a separate choice, trading control against operational burden. A cloud translation table helps read designs across providers. A short network checklist covering the path, proxy, egress addresses, DNS, certificates, idle timeouts, time, and latency converts the most common production surprises into week-one facts.

## Exercises

1. **Draw your network.** Draw the path of a request from an integration runtime to one system you integrate with, naming every hop. Mark every place a connection must be opened inbound. Which of those has the longest approval time?
2. **Classify your estate.** Choose three integrations in your organization and label each with one of the seven topologies. Do any fit none of them cleanly?
3. **Certificates.** List every certificate your most critical integration depends on, with expiry dates. Which expires first, and who gets the alert?
4. **Latency arithmetic.** An integration makes 250 sequential API calls across a link with 120 ms round-trip time. How long does one run take? How would you change the design to bring it under 30 seconds?



# Chapter 6. Patterns for Requests and Data Movement

A pattern is a named solution to a problem that keeps recurring. Architects use patterns the way carpenters use joints: not because they are clever, but because everyone who sees the name knows what is meant, what it is good for, and where it tends to fail. When a colleague says "we'll use a transactional outbox," you do not need a whiteboard. The vocabulary is the point.

This chapter and the next catalog forty-one integration patterns in six families, each with a diagram, a plain description of how it works, when to use it, and what goes wrong. They are not a menu from which you pick one; real integrations combine three or four. Chapter 7 closes with recipes that show typical combinations, and Chapter 9 gives you a method for choosing.

Here, we cover the first two families: **request-based patterns**, where one system calls another and waits, and **data-movement patterns**, where information is copied or exposed in bulk. Together they cover most of the volume in a typical enterprise.

> **In this chapter**
    * Read a pattern diagram and its three characteristics: initiator, timing, and coupling
    * Use four questions to narrow a requirement to a pattern family
    * Explain why hubs and event backbones exist, using the arithmetic of links
    * Describe eight request-based patterns and nine data-movement patterns, with when to use each and what to watch for
    * Recognize the patterns hidden inside the tools your organization already runs

## How to Read the Pattern Diagrams

Every pattern in this book has a diagram in the same visual language, so you can learn it once. The key is in the figure.

*[Figure: The visual language of the diagrams. Arrow styles show how information travels; numbered circles give the order of steps; lettered red circles mark where a design usually fails.]*
Three characteristics describe every pattern, and they appear in the descriptions that follow. The **initiator** says who starts the exchange: the consumer *pulls*, the producer *pushes*, or both are possible. The **timing** says how long the exchange takes: *synchronous* (the caller waits), *asynchronous* (it does not), *batch* (data moves in bulk on a schedule), or *streaming* (data flows continuously). The **coupling** says how much one side must know about, and depend on, the other: *tight*, *moderate*, or *loose*. Tight coupling is simple and fragile; loose coupling is resilient and harder to follow.

## Start with the Family

With forty-one patterns, a newcomer needs a way in. the figure shows four questions that narrow almost any requirement to a family.

*[Figure: Four questions narrow almost any requirement to a pattern family. Chapter 9 turns this into a fuller method.]*
The first question is whether the consumer needs an *answer right now* (a request-based pattern) or merely needs to *be told* when something happens (messaging and events). The second is whether the work is about *moving large amounts of data*, in which case data-movement patterns apply, or about individual business events. The third asks whether more than one system may change the same data, which sends you to the authority patterns of Chapter 7. The fourth asks about special circumstances: partners, edge sites, legacy interfaces, or streaming computation. The tree is a starting point; the decision method in Chapter 9 refines it.

## Why Hubs and Backbones Exist

Before the patterns themselves, one piece of arithmetic explains an entire family of them. If every system talks directly to every other, the number of links grows with the square of the number of systems. the figure shows the difference.

*[Figure: Links grow as N times (N minus 1), divided by 2, when every system talks to every other. A hub or event backbone makes the growth linear, at the price of a shared component to govern.]*
With five systems, full point-to-point connectivity needs 10 links. With ten systems it needs 45, and with twenty, 190. Each link has its own mapping, its own credentials, its own failure modes, and its own owner. Through a hub, twenty systems need 20 connections: one each. The price is a shared component that must be governed and kept available. This is the whole argument behind enterprise service buses, API gateways, and event backbones, and it is also the argument against them: a hub that becomes a bottleneck and a bureaucracy has traded one problem for another. Keep this arithmetic in mind as you read the patterns that follow.

## Request-Based Patterns

In request-based patterns, the caller asks and waits, or at least asks and receives an immediate acknowledgment. They are simple to reason about and tightly coupled in time: both sides must be available at the same moment.

### Point-to-Point API Call

*[Figure: pattern-point-to-point-api-call]*
One system calls another system's API and waits for the answer. The consumer sends a request (step 1) and the provider returns a response (step 2). This is the pattern everyone starts with, and for good reason: it is the simplest thing that can possibly work. When the shop asks the ERP whether a product is in stock before showing the page, that is a point-to-point call.

Use it for lookups, validations, and simple create-and-update flows between a handful of systems. The weaknesses are *temporal coupling* (both must be up), cascading failures (if the ERP is slow, the shop is slow), versioning pain when the provider changes, and the link explosion described above as the estate grows. Typical technologies are REST described with OpenAPI, gRPC, SOAP, and GraphQL. Whatever the technology, always set a timeout, and wrap the call in a circuit breaker, as Chapter 14 shows.

### API Gateway or Facade

*[Figure: pattern-api-gateway-facade]*
Clients call one managed entry point, which authenticates them, enforces quotas, routes the call, and sometimes transforms it. The clients, whether web, mobile, or partners, send HTTPS requests to the gateway (step 1), which forwards them to the right back-end service (steps 2 and 3).

Use it to expose internal or partner APIs, to apply security and rate limiting in one place, and to gather usage analytics. The danger is that the gateway becomes a single choke point, and, more subtly, that *logic creeps into it*. A gateway that starts to contain business rules and data transformations becomes an unmaintainable miniature enterprise service bus. Keep its policies declarative: authentication, quotas, routing, and header rules. Products include Kong, Apigee, Azure API Management, Amazon API Gateway, MuleSoft's gateway offerings, WSO2, and Axway.

### API-Led Connectivity

*[Figure: pattern-api-led-connectivity]*
API-led connectivity, a term popularized by MuleSoft, layers APIs by role. *System APIs* unlock back-end systems once: one clean interface to the ERP, one to the CRM, one to the warehouse system. *Process APIs* compose them into business logic, such as "place an order," which touches all three. *Experience APIs* tailor the data to a channel, such as the web shop or the mobile app. In the diagram, two experience APIs call one process API (steps 1 and 2), which calls three system APIs (steps 3 to 5).

Use it in large estates with many consumers, where reuse and clear ownership per layer matter. Beware layers for their own sake: three tiers add latency, teams, and meetings, and a small estate rarely needs them. The pattern is a way of organizing reuse, not a rule that every call must pass through three hops.

### Orchestration

*[Figure: pattern-orchestration]*
A central coordinator calls the steps of a business process in order, owns its state, and decides what to do on failure. In the diagram, an orchestrator, a workflow engine, calls "reserve stock" (step 1), "charge payment" (step 2), and "create shipment" (step 3), and persists its state after each (step 4).

Use it for business processes with a clear sequence, timeouts, and human approval steps, especially where auditability matters. The risk is that the orchestrator becomes a "god service" that knows too much about everyone. It needs durable state, timeouts, and compensation logic for steps that must be undone. Typical technologies are workflow engines such as Camunda, Flowable, and Temporal, cloud workflow services such as AWS Step Functions and Azure Logic Apps, and the flow designers of integration platforms.

### Scatter-Gather

*[Figure: pattern-scatter-gather]*
The caller sends a request to an aggregator (step 1), which fans it out to several providers in parallel (steps 2 to 4) and merges the answers. It is the pattern behind a "customer 360" screen that gathers data from five systems, or a price comparison across suppliers.

The slowest provider sets the latency, so decide up front what happens on a timeout: return partial results, or fail? Decide also how to present a result that is missing a source. Integration platforms provide scatter-gather scopes, and the pattern is straightforward in code with asynchronous calls, provided you set a deadline.

### Adapter or Anti-Corruption Layer

*[Figure: pattern-adapter-anti-corruption-layer]*
An adapter sits in front of a legacy or awkward system and translates between its model and a clean one, so that the legacy model does not spread into modern services. Modern services speak the clean model to the adapter (step 1), which speaks the legacy model to the old system (step 2). The idea of an "anti-corruption layer" comes from domain-driven design: it protects the new world from being "corrupted" by the old.

Use it for mainframes, old ERPs, SOAP services, and partners with peculiar data models. Its cost is one more component to run, and its discipline is to remain a *dumb translator*. The moment business rules enter the adapter, you have hidden logic in the least visible place. In integration platforms the adapter is often called a system API.

### Strangler Fig

*[Figure: pattern-strangler-fig]*
The name, coined by Martin Fowler, comes from a vine that grows around a tree until the tree is gone. Clients call a routing proxy (step 1), which sends some functionality to the legacy monolith (step 2, being phased out) and some to new services (step 3, being phased in). Over time, more routes point at the new services, until the legacy system can be retired.

Use it to replace a legacy platform without a big-bang cutover. The hard part is data: while both systems are alive, they must stay synchronized, which brings in the patterns of Chapter 15. Define the retirement criteria early, or the legacy system will live forever on the strength of "just one more route."

### Asynchronous Request-Reply

*[Figure: pattern-asynchronous-request-reply]*
Some operations take too long to hold a connection open: a bulk import, a report, a large export. In asynchronous request-reply, the client submits a job (step 1) and receives `202 Accepted` with a status URL, then polls that URL (step 2) or is called back when it finishes. Behind the scenes, the API enqueues the job (step 3), a worker takes it (step 4) and updates the status (step 5).

Use it for bulk operations and long-running tasks on vendor APIs; many platforms offer job APIs of exactly this form, such as Salesforce's Bulk API 2.0. Watch for job expiry (results that disappear after a day), idempotent submission (so a retried submit does not start a second job), sensible polling intervals, and what happens to a result nobody collects.

**Table: Request-based patterns at a glance**
| Pattern | Initiator | Timing | Coupling | Use it for |
|---|---|---|---|---|
| Point-to-point API call | Pull | Sync | Tight | Lookups and simple writes |
| API gateway | Pull | Sync | Tight | One managed front door |
| API-led connectivity | Pull | Sync | Moderate | Reuse in large estates |
| Orchestration | Pull | Sync | Tight | Sequenced business processes |
| Scatter-gather | Pull | Sync | Tight | Combining several sources |
| Adapter | Pull | Sync | Moderate | Isolating a legacy model |
| Strangler fig | Pull | Sync | Moderate | Gradual replacement |
| Asynchronous request-reply | Pull | Async | Moderate | Long-running operations |

## Data-Movement Patterns

Data-movement patterns copy or expose information in bulk rather than per transaction. They carry most of the volume in an enterprise, and most of its reconciliation pain, because "the same data in two places" inevitably drifts.

### Scheduled Batch ETL or ELT

*[Figure: pattern-scheduled-batch-etl-elt]*
On a schedule, a job extracts data from sources (steps 1 and 2), transforms it, and loads it into a target (step 3). In classic ETL the transformation happens before loading; in ELT, the data is loaded first and transformed inside the warehouse, which is the common approach on modern platforms because warehouses are good at it.

Use it for analytics feeds, reference data, and anything where hours of latency are acceptable. The traps are batch windows that grow until they collide, data that arrives late, reruns that double-count, and silent failures. A job that fails without raising an alarm is the integration equivalent of a stopped clock: give every batch a heartbeat alert that fires when it does *not* run. Tools include the data-integration suites (Informatica, Talend), cloud services (Azure Data Factory, AWS Glue), orchestrators (Airflow with dbt), and managed ELT tools (Fivetran, Airbyte).

### Managed File Transfer

*[Figure: pattern-managed-file-transfer]*
The source drops files on an SFTP server, an AS2 endpoint, or object storage (step 1), and a loader polls, fetches, validates, and ingests them (step 2). It is the oldest pattern here and still the best for large volumes, legacy systems, partners, and strict audit trails.

Files fail in characteristic ways: partial files picked up before the writer finished, encoding and delimiter surprises, schema drift, and duplicate delivery. Defend against them with a **manifest** (a small file listing expected names, sizes, and checksums), by having the writer upload under a temporary name and rename it atomically when done, and by archiving every file after processing. Products include Axway, IBM Sterling, GoAnywhere, Cleo, and the managed transfer services of the clouds.

### Polling with a Watermark

*[Figure: pattern-polling-with-a-watermark]*
The workhorse of SaaS integration. A scheduler repeatedly asks the source for "changes since the last watermark" (step 1), receives the changed rows (step 2), upserts them into the target (step 3), and saves the largest timestamp it saw as the new watermark (step 4).

It needs only outbound connections, which is a large part of its appeal. It is the right pattern whenever the source offers a modified-since filter. Its weaknesses are that it misses deletes, depends on honest timestamps, and can miss rows committed late. The standard defenses are an *overlap window* (re-read the last few minutes each time and let idempotent upserts absorb the repeats) and a periodic reconciliation. Chapter 14 implements the pattern, and Chapter 15 examines its edge cases.

### Full Snapshot and Diff

*[Figure: pattern-full-snapshot-and-diff]*
When the source offers no way to ask what changed, read all of it. A diff engine pulls the complete source state (step 1) and the current target state (step 2), computes the difference, and applies it (step 3): create what is new, update what changed, delete what vanished.

It suits small and medium datasets, sources with no change tracking, reference data that should heal itself, and, importantly, **delete detection**, which many other patterns lack. Its cost grows with data size. Add a safety threshold, for example "refuse to delete more than 5 percent of the target in one run," so that a bad read from the source cannot wipe out the target.

### Change Data Capture

*[Figure: pattern-change-data-capture]*
Instead of asking the application what changed, read the database's transaction log, where every committed change is already recorded. A connector reads the log (step 1) and publishes each row change as an event (step 2) to a topic, from which targets consume (step 3).

Log-based change data capture, or CDC, is powerful because it does not touch the application, captures every change including deletes, and preserves order. It underpins replication, event feeds from legacy systems, near-real-time warehouse loads, and the outbox pattern of Chapter 7. Its dangers are that it exposes the *physical* schema (renaming a column breaks consumers) and, with some databases, that an idle replication slot makes the source's disk fill up. Tools include Debezium, Qlik Replicate, Oracle GoldenGate, AWS DMS, and Striim.

### Read-Model Replication

*[Figure: pattern-read-model-replication]*
Keep a copy of data shaped for *reading*, such as a search index, a cache, or an operational data store, updated from events or CDC. The system of record emits changes (step 1), which a feed distributes (steps 2 and 3) to the read models.

Use it when search, dashboards, or APIs must stay fast and independent of the system of record. It is eventually consistent by nature, so decide how stale the copy may be. And design a *rebuild strategy* up front: sooner or later the read model will need to be regenerated from scratch, and "we can replay the topic" is a better answer than "we cannot."

### Reverse ETL

*[Figure: pattern-reverse-etl]*
Analytics produces valuable results, such as churn scores and customer segments, that are useless in a warehouse when the people who need them work in the CRM or the marketing tool. Reverse ETL queries the warehouse (step 1) and pushes the results into operational applications through their APIs (steps 2 and 3).

Watch for SaaS API rate limits, identity resolution (matching a warehouse customer to a CRM contact), loops with the original source, and above all *ownership*: who owns the field that the sync overwrites? Tools include Hightouch and Census, and custom jobs.

### Data Virtualization

*[Figure: pattern-data-virtualization]*
Query across sources at read time through a virtual layer, without copying the data first. The consumer sends SQL to the virtualization layer (step 1), which pushes parts of the query down to each source (steps 2 and 3) and combines the results.

It is attractive for exploration, for regulated data that cannot be copied, for rapid prototypes, and for "logical data warehouses." The performance is that of the slowest source, and production queries land on operational systems, so test with realistic loads. Security delegation, who is allowed to see what through the layer, needs deliberate design. Examples are Denodo, Trino and Starburst, and Dremio.

### Zero-Copy Data Sharing

*[Figure: pattern-zero-copy-data-sharing]*
A provider grants governed read access to a dataset (step 1), and consumers query it in place (steps 2 and 3) instead of receiving a copy. Because there is only one copy, there is nothing to reconcile.

Use it for data products shared across teams or companies on the same platform family. Its limits are platform affinity (it generally works only between users of the same technology), cross-region cost, and the semantics of revoking access. Governance still has to define who may see what. Examples include Snowflake Secure Data Sharing, Delta Sharing, and BigQuery Analytics Hub.

**Table: Data-movement patterns at a glance**
| Pattern | Initiator | Timing | Coupling | Use it for |
|---|---|---|---|---|
| Scheduled batch ETL or ELT | Pull | Batch | Loose | Analytics feeds, reference data |
| Managed file transfer | Push | Batch | Loose | Legacy systems, partners, large volumes |
| Polling with a watermark | Pull | Batch | Loose | SaaS sources with a modified-since filter |
| Full snapshot and diff | Pull | Batch | Loose | Small datasets, delete detection |
| Change data capture | Both | Stream | Loose | Replication, event feeds |
| Read-model replication | Push | Async | Loose | Search, caches, fast reads |
| Reverse ETL | Push | Batch | Loose | Analytics results back to applications |
| Data virtualization | Pull | Sync | Tight | Exploration, uncopyable data |
| Zero-copy data sharing | Pull | Sync | Loose | Cross-team data products |

> **Larkspur Outdoor: which patterns were already there**
    Larkspur's nightly CSV is a *managed file transfer* with a *scheduled batch* loader, and the manual fix-up of rejected rows is a human acting as the *dead letter queue* (Chapter 7). Its stock check is a *point-to-point API call*. Naming the patterns already in use made the discussion concrete: the team was not proposing to "add integration"; it was proposing to replace one batch pattern with polling and webhooks, and to keep the file as the safety net.

## Summary

A pattern is a named, reusable solution; its value lies in shared vocabulary. Three characteristics describe each: who initiates (pull or push), the timing (synchronous, asynchronous, batch, or streaming), and the coupling (tight, moderate, or loose). Four questions narrow a requirement to a family, and the arithmetic of links, N times N minus 1 over 2, explains why hubs and backbones exist.

Request-based patterns are simple but tightly coupled in time: the point-to-point call, the API gateway, API-led layers, orchestration, scatter-gather, the adapter, the strangler fig for gradual replacement, and asynchronous request-reply for long operations. Data-movement patterns carry the volume: scheduled batch, managed file transfer, polling with a watermark, snapshot and diff, change data capture, read-model replication, reverse ETL, virtualization, and zero-copy sharing. Each trades latency and effort differently, and each has a characteristic way of failing.

## Exercises

1. **Name what you run.** List five data flows in your organization and name the pattern each uses. Which uses a pattern that does not match its freshness requirement?
2. **Count your links.** Count the systems in one business domain and the direct integrations between them. Compare with the N times (N minus 1) over 2 maximum. How close are you to the "spaghetti" limit?
3. **Choose a family.** For each requirement, name the pattern family and one specific pattern: (a) show live stock levels on the product page; (b) load yesterday's sales into the warehouse; (c) replace the legacy billing system without a big bang; (d) import 2 million customer records overnight.
4. **Design a safety threshold.** For a snapshot-and-diff job, write the rule that would stop it from deleting too much. What percentage would you choose, and why?



# Chapter 7. Patterns for Messages, Routing, and Authority

The previous chapter covered patterns in which a caller asks and waits, and patterns that move data in bulk. This chapter covers the rest: the patterns of *asynchronous messaging*, where producers and consumers are decoupled in time; the *routing and transformation* toolbox that every integration platform provides; the patterns of *authority, master data, and identity*, which decide who owns which truth; and a final family of *specialized* patterns for boundaries such as partners, edge sites, legacy screens, and AI agents.

Messaging is where integrations gain resilience and fan-out, and also where most of the subtle bugs live. Messages arrive twice. They arrive out of order. They arrive when nobody is listening, or in such numbers that someone drowns. The patterns in this chapter are, to a large extent, the accumulated answers to those problems, and several of them (the transactional outbox, the idempotent receiver, the dead letter queue) will recur in every chapter that follows.

> **In this chapter**
    * Describe thirteen messaging and event patterns, including the three that make asynchronous systems safe: the outbox, the idempotent receiver, and the dead letter queue
    * Use the routing and transformation toolbox, and judge when a hub is worth its cost
    * Choose among bidirectional sync, master data management, and identity provisioning
    * Recognize the specialized patterns for agents, partners, legacy screens, streaming computation, and AI tools
    * Combine patterns into recipes, and spot the anti-patterns that undo them
    * Apply the authority split, the most valuable simplification in this book

## Messaging and Event Patterns

In messaging patterns, producers and consumers are decoupled in time. You gain resilience and fan-out. You pay with ordering problems, duplicates, and the need to trace flows across components that no longer call each other directly.

### Message Queue

*[Figure: pattern-message-queue]*
Producers put messages on a queue, and each message is processed by exactly one of several competing workers. The producer sends (step 1); each worker receives a message and acknowledges it when finished (steps 2 and 3). If a worker crashes before acknowledging, the queue offers the message to another worker.

That last sentence contains the most important property of queues: **delivery is at least once**. A message may be delivered more than once, because the queue cannot know whether the worker finished its work before it died. Consumers must therefore be idempotent, which is the subject of a pattern later in this chapter.

Use queues to distribute tasks, to level load, and to protect a slow downstream system from bursts: the shop's Black Friday spike goes into the queue, and the ERP's workers drain it at the pace the ERP can sustain. Classic queues keep no history and cannot be replayed, and ordering is limited. Technologies include IBM MQ, RabbitMQ, ActiveMQ, Amazon SQS, Azure Service Bus, and, in recent versions, Kafka's share groups, which add queue semantics to a log.

### Publish and Subscribe

*[Figure: pattern-publish-subscribe]*
A publisher emits an event to a topic (step 1), and every interested subscriber receives its own copy (steps 2 to 4). The publisher does not know how many subscribers exist or who they are. The shop publishes "order placed" once; the ERP, the analytics platform, and the fraud check each receive it.

Use it to broadcast business events to an unknown or changing set of consumers. The cost is invisibility: when anyone may subscribe, it becomes hard to answer "who depends on this event?" before you change it. Keep an **event catalog** listing every topic, its owner, its schema, and its known subscribers. Expect duplicates and out-of-order delivery as normal conditions. Technologies include Amazon SNS and EventBridge, Google Pub/Sub, Azure Event Grid and Service Bus topics, RabbitMQ exchanges, and Solace.

### Event-Carried State Transfer

*[Figure: pattern-event-carried-state-transfer]*
There are two ways to design the content of an event. A *notification* event says only that something happened ("customer 42 changed") and forces consumers to call back for the details. An *event-carried state transfer* event carries the full new state of the entity, so consumers keep a local copy and never call back. The customer service publishes the full state to a compacted topic (step 1), and the billing and support services each maintain their own copy (steps 2 and 3).

The pattern reduces runtime coupling, because billing no longer needs the customer service to be up in order to work. It also makes it easy to bootstrap a new consumer: read the compacted topic from the beginning and you have the current state of every customer. The costs are that the event's schema becomes a public contract that is hard to change, payloads are larger, and a consumer that misses events can drift from the truth. Pair it with a reconciliation.

### Event Streaming

*[Figure: pattern-event-streaming]*
Events are appended to a partitioned, retained log. Producers write to it (steps 1 and 2); consumer groups read from it at their own pace and can *replay* by moving their position (steps 3 and 4). Unlike a queue, reading does not remove anything; the log is a record, and each group keeps its own bookmark.

Choose streaming for high volume, many independent consumers, the need to replay after a bug, stream processing, and change-data-capture backbones. The costs are real: operational weight, the need for schema discipline, ordering only within a partition, and the need to watch **consumer lag**, the distance between the newest event and the consumer's position. Chapters 18 to 20 are devoted to the most widely used platform of this kind, Apache Kafka. Alternatives include Redpanda, Apache Pulsar, Azure Event Hubs, and Amazon Kinesis.

### Request-Reply over Messaging

*[Figure: pattern-request-reply-over-messaging]*
Sometimes you need a conversation, not just a notification, but the systems share a broker rather than an HTTP path. In request-reply over messaging, the requester sends a message to a request queue with a *correlation ID* (step 1). The responder takes it (step 2), does its work, and sends a reply with the same ID to a reply queue (step 3), where the requester matches it (step 4).

The pattern suits legacy message-queue estates and decoupled remote calls. Watch for timeouts (how long does the requester wait?), orphaned replies for requesters that have gone away, and the temptation to rebuild HTTP on top of a broker. If the requester needs an answer within a second, an API is usually simpler.

### Webhook

*[Figure: pattern-webhook]*
The source sends an HTTP POST to your endpoint when something changes (step 1). A well-built receiver does only three things on the request path: it verifies the signature, persists the event by putting it on a queue (step 2), and acknowledges. A worker takes events from the queue and processes them later (step 3). The rule is: *answer in milliseconds; process later*.

Webhooks give near-real-time notification without polling. They require a publicly reachable endpoint, which brings the security work of signature verification and replay protection (Chapter 27), and the source typically retries, so you must deduplicate. Most importantly, **if you were down when the event was sent, you may never receive it**; many providers do not replay. The standard remedy is to pair the webhook with a slower *reconciliation pull*, so that the fast path provides speed and the slow path repairs whatever the fast path missed. Chapter 25 builds exactly this combination.

### Event Mesh

*[Figure: pattern-event-mesh]*
An event mesh is a network of interconnected brokers, spread across sites and clouds, that routes events dynamically to wherever subscribers exist. A publisher at one site connects to its local broker, and the mesh carries the event across to subscribers at other sites and clouds (steps 1 to 4).

It fits retail stores, factories, and multi-cloud estates that exchange events with each other and with the core. The tooling matters less than the discipline: a clear topic taxonomy and governance are decisive, and latency and cost across the links need watching. Commercial meshes such as Solace and SAP Advanced Event Mesh pursue this goal, as do Kafka's MirrorMaker 2 and cluster-linking features.

### Choreography

*[Figure: pattern-choreography]*
In choreography, services react to each other's events with no central coordinator. The order service publishes "order placed" (step 1); payment and inventory services each react (steps 2 and 3); payment publishes "payment taken" (step 4), which others react to in turn. Each team owns its own reaction.

It suits loosely coupled domains where autonomy matters. The cost is that *the end-to-end flow is no longer written down anywhere*. To understand what happens when an order is placed, you must read the code of five services. Compensate with correlation IDs on every event, distributed tracing (Chapter 26), and an event catalog that documents the flow. If the process is long, has deadlines, or needs a human step, an orchestrator is usually clearer.

### Saga

*[Figure: pattern-saga]*
Transactions that span several systems cannot rely on a database to roll everything back. A **saga**, a term from a 1987 paper by Hector Garcia-Molina and Kenneth Salem, replaces the one big transaction with a chain of local transactions, each with a *compensating action* that undoes it. In the diagram, the saga creates the order, reserves stock, charges payment, and ships (steps 1 to 3). If shipping fails, the saga compensates in reverse: it refunds the payment, releases the stock, and cancels the order (steps 4 to 6).

The crucial insight is that a compensation is *business logic*, not a technical rollback. You cannot "un-send" an email or "un-ship" a parcel; you can send an apology or arrange a return. Design every step to be idempotent, expect partial failure, and decide what each compensation means to the business. Sagas can be orchestrated by a workflow engine (Temporal, Step Functions, Camunda) or choreographed through events.

### Transactional Outbox

*[Figure: pattern-transactional-outbox]*
Consider a service that must update its database *and* publish an event. If it writes the database and then publishes, a crash in between leaves the data changed and the event never sent. If it publishes first, a crash leaves an event for a change that never happened. This is the **dual-write problem**, and it cannot be solved by ordering the two steps carefully, because there is no transaction that spans a database and a broker.

The outbox pattern removes the problem by making only one write. The service writes the state change *and* the event to an outbox table in the same database transaction (step 1). A separate relay, either a poller or a change-data-capture connector, reads the outbox (step 2) and publishes to the broker (step 3). Either both rows are committed or neither is, and the relay takes care of delivery.

Delivery from the relay is at least once, because the relay may publish and then crash before marking the row as sent, so consumers must deduplicate. Watch for relay operations, outbox cleanup, and ordering per aggregate. Chapter 8 walks through exactly this sequence, and Appendix E includes a tested implementation that demonstrates the duplicate and its fix. Debezium provides an outbox event router; polling relays are simple to write.

### Claim Check

*[Figure: pattern-claim-check]*
Message brokers limit message size, and moving large payloads through them is wasteful. In a claim check, the producer stores the large payload in blob storage (step 1) and sends a small message containing only a reference (step 2). The consumer takes the message (step 3) and fetches the payload by reference (step 4), as one hands in a coat and receives a ticket.

Use it for documents, images, and large JSON. Take care of the stored payload's lifecycle (who deletes it, and when?), of access control on the reference (anyone holding the reference should not automatically get the data), and of consistency between the message and the blob: store the payload *before* sending the message, never after.

### Retry and Dead Letter Queue

*[Figure: pattern-retry-and-dead-letter-queue]*
Failures come in two kinds. *Transient* failures, such as a timeout or a brief outage, succeed if tried again. *Permanent* failures, such as a malformed message or a business rule violation, will fail forever. A retry and dead letter design treats them differently. The consumer processes a message from the main queue (steps 1 and 2); on success, it writes to the target (step 3). On a transient failure it sends the message to a retry queue with a delay (steps 4 and 5), which returns it to the main queue later. On a permanent failure, or after too many attempts, it parks the message with context in a **dead letter queue** (step 6) for a human.

Every asynchronous consumer in production needs this. And a dead letter queue nobody watches is data loss with extra steps: assign an owner, alert on its depth, and build a tool to inspect and replay its messages once the cause is fixed. Brokers provide native dead letter queues; Kafka implementations use retry topics and connector error handling (Chapter 19).

### Idempotent Receiver

*[Figure: pattern-idempotent-receiver]*
Since queues, webhooks, retries, and streams all deliver at least once, a receiver that processes the same message twice will do the work twice unless it is built not to. An idempotent receiver records the identifier of each message it processes. When a message arrives (step 1), the receiver checks the ledger (step 2): "seen this ID?" If not, it applies the business write once (step 3) and records the ID.

Two details matter. The ledger entry and the business write must commit *in the same transaction*; otherwise a crash between them re-creates the duplicate. And the ledger must remember IDs for longer than the longest retry window, or an old duplicate slips through. Where possible, prefer *natural* idempotency (an upsert by business key) to a ledger, because it needs no extra state.

**Table: Messaging and event patterns at a glance**
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

Every integration platform provides a set of building blocks for shaping and steering messages. They were cataloged in the 2003 book *Enterprise Integration Patterns* by Gregor Hohpe and Bobby Woolf, and their names form the shared vocabulary of the field. the figure shows six of the most useful.

*[Figure grid: Six routing and transformation building blocks.]*
A **content-based router** inspects a message and sends it to one of several destinations: orders for Europe to one queue, orders for North America to another. A **splitter** breaks one message into many, for example a file of 10,000 orders into 10,000 order messages. An **aggregator** does the reverse, collecting related messages and combining them, such as gathering all the lines of an order. A **message translator** converts one format into another: an XML purchase order into the JSON the ERP expects. A **content enricher** adds data the message lacks by looking it up elsewhere, for instance adding a customer's region from a reference table. A **message filter** discards messages that do not meet a condition, such as ignoring test orders.

These blocks appear, under different names, in Apache Camel, MuleSoft, Boomi, Spring Integration, IBM App Connect, and every other platform. The danger is hidden complexity: an estate with a hundred tiny flows, each combining three of these blocks, can become impossible to understand. Name every flow, document its purpose, and test it.

### Hub-and-Spoke and the Canonical Model

*[Figure: pattern-hub-and-spoke-esb-with-canonical-model]*
In a hub-and-spoke design, every system connects once to a central hub, which translates between each system's format and a shared **canonical model** and routes messages. The ERP and CRM send to the hub (steps 1 and 2), and the hub forwards to the warehouse system and the web shop (steps 3 and 4). With a canonical model, adding a new system requires one new translation, to and from the canonical form, instead of one translation per existing system.

This is the classic enterprise service bus, and it delivered on its promise in estates with many systems and few changes. It also gave rise to its own failure modes: the hub becomes a bottleneck and a governance bureaucracy, and a canonical model for *everything* tends to become a lowest-common-denominator committee product. A pragmatic modern approach is to adopt a canonical model only for the few entities that are truly shared and stable, such as customer and product, and to leave everything else bounded to its own domain. Technologies include MuleSoft, IBM App Connect, TIBCO BusinessWorks, webMethods, WSO2, and Apache Camel.

## Authority, Master Data, and Identity

A different family of patterns concerns who owns which truth, and how copies of it stay honest.

### Bidirectional Sync with Per-Field Authority

*[Figure: pattern-bidirectional-sync-with-per-field-authority]*
Sometimes two systems legitimately both change the same entity: a ticket in a service desk and a matching issue in a project tool, each edited by different teams who will not give up their own application. A synchronization service watches both sides (steps 1 and 4) and applies changes each way (steps 2 and 3), under an **authority map** that says, field by field, which side wins.

Bidirectional synchronization is the hardest mode to get right. The failure modes are *echo loops* (a change written to B triggers a change event, which is written back to A, forever), ordering problems, and concurrent edits. The defenses are a loop guard (ignore changes made by the integration's own user, or stamp changes with their origin), a per-record lock, and explicit conflict rules. Better still, apply the authority split described at the end of this chapter, which usually turns one bidirectional flow into two simple one-way flows. Chapter 15 treats the topic in depth.

### Master Data Management Hub

*[Figure: pattern-master-data-management-hub]*
When the same customer, product, or supplier exists in a dozen systems with different spellings, identifiers, and levels of completeness, someone must decide which record is "the customer." A **master data management** hub receives records from each source (steps 1 to 3), *matches* those that describe the same real-world entity, *merges* them into a golden record using survivorship rules, and publishes the result to consumers (step 4). Four classic styles differ in how much authority the hub takes: *registry* (the hub only holds an index of which records match), *consolidation* (the hub builds the golden record for reporting), *coexistence* (the golden record is synchronized back to the sources), and *centralized* (the hub is the only place the entity is edited).

Match rules and survivorship, such as "the CRM's phone number wins unless it is older than the billing system's," are *business* decisions, not technical ones. Without data stewards who own and tune them, the hub decays. Products include Informatica MDM, Boomi DataHub, Reltio, Profisee, Stibo for products, and SAP MDG.

### Identity Provisioning

*[Figure: pattern-identity-provisioning]*
The employee lifecycle is an integration problem in disguise. The HR system is the source of truth for who works at the company. When someone joins, changes role, or leaves (the "joiner, mover, leaver" events, step 1), an identity provider such as Entra ID or Okta provisions, updates, or removes accounts and roles in each application (steps 2 and 3), typically through the SCIM standard.

The hardest problems are not technical: rehires who return with new identifiers, leavers whose access must end within hours rather than days, attribute mappings that differ per application, and approval workflows for sensitive roles. Products include Workday and SuccessFactors as sources, Entra ID and Okta as providers, and SailPoint for governance.

## Specialized and Boundary Patterns

The last family covers boundaries and special circumstances.

### Stateful Stream Processing

*[Figure: pattern-stateful-stream-processing]*
Some questions can be answered only by computing continuously over a stream: "how many failed payments has this card had in the last ten minutes?" A stream processor reads input topics (step 1), filters, joins, and aggregates over *windows* of time, keeps state between events (step 3), and emits derived events (step 2).

Use it for real-time aggregates, fraud signals, and enrichment of events with reference data. Pitfalls include late and out-of-order events, the size of the state, recovery time after a crash, and the boundaries within which processing is exactly once. Tools include Kafka Streams, Apache Flink, ksqlDB, and Spark Structured Streaming.

### Server Push to Clients

*[Figure: pattern-server-push-to-clients]*
Browsers and mobile apps that must show live updates can poll, or the server can keep a connection open and push. A gateway holds Server-Sent Events or WebSocket connections to clients (steps 2 and 3) and relays events from the broker behind it (step 1). Watch for reconnect and resume (clients should send the last event ID they saw), fan-out at scale, and proxies that close idle connections. Services include Azure SignalR and AWS AppSync subscriptions, along with mobile push notification systems.

### Hybrid Agent

*[Figure: pattern-hybrid-agent]*
Chapter 5 introduced the agent topology; here it appears as a pattern. A lightweight agent inside the private network reaches the local systems (step 1), and holds an outbound TLS connection to a cloud control plane (step 2), from which it reaches SaaS applications (step 3). No inbound ports are needed. Watch for agent patching, high availability, and the question of where the logic actually executes.

### B2B and EDI Exchange

*[Figure: pattern-b2b-edi-exchange]*
Retail, manufacturing, logistics, and healthcare supply chains exchange standard documents, such as purchase orders and invoices in the X12 or EDIFACT formats, over AS2, SFTP, or a value-added network. A partner sends a purchase order (step 1) through the transport (step 2); an EDI translator maps it to an ERP document such as an IDoc (step 3) and returns a functional acknowledgment, such as an X12 997 (step 4), to confirm receipt. The "standard" has partner-specific variations, so onboarding each partner is real work. Products include Boomi B2B, IBM Sterling B2B Integrator, OpenText, SPS Commerce, and Cleo.

### UI Automation as a Last Resort

*[Figure: pattern-ui-automation-last-resort]*
A bot drives a legacy application's screens because the application has no API (step 1), and feeds the result to a target through an API or a file (step 2). Robotic process automation tools such as UiPath, Power Automate Desktop, and Blue Prism, or browser automation libraries like Playwright, do this. It is a legitimate bridge while a proper integration is built, and a poor foundation for anything else: it breaks when the screen changes, has no contract, and is hard to monitor. Treat it as technical debt with an exit date.

### AI Agent Access via Tools

*[Figure: pattern-ai-agent-access-via-tools]*
An AI agent, a program built on a large language model that decides which actions to take, can call tools exposed to it, often through the Model Context Protocol (MCP) or through function calling. An MCP server wraps your existing APIs (steps 2 and 3) with a catalog of tools and scoped credentials, and the agent discovers and calls them (step 1). Natural-language access to a CRM, a service desk, or a data catalog becomes possible without a new integration for each.

The risks are new and serious. *Prompt injection* means text returned by a tool, such as a customer's note, can try to instruct the agent. Over-broad scopes let a mistaken agent do real damage. Non-idempotent writes may be repeated. Auditing is easily forgotten. Apply the same discipline as to any integration, and more: scope credentials to the minimum, require human approval for writes, log every call, and treat tool output as untrusted input (Chapter 27).

## Pattern Recipes: How Real Integrations Combine Them

Real integrations use three or four patterns at once. the table lists recipes that recur so often they deserve names.

**Table: Common recipes and why they work**
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

**Table: Anti-patterns, why they hurt, and what to do instead**
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

When each field has exactly one owner, you do not need conflict resolution at all. You need only a clean one-way flow per field. Two one-way flows beat one bidirectional merge in almost every case, because a one-way flow has a source of truth, a direction, and no possibility of an echo. The authority matrix of Chapter 4 is the tool that finds the split.

**Table: The authority split applied to a ticketing integration**
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
4. **Pick a recipe.** Choose three requirements from your own work and match each to one of the recipes in the table. Where would you adapt it?



# Chapter 8. Behavior in Time: The Hard Cases

Static diagrams show structure. They show which boxes exist and which arrows connect them. Integrations, however, fail in *time*: a retry arrives twice, a consumer crashes before it saves its position, a token expires between two calls, a sender gives up waiting for an answer that was in fact sent. None of these can be seen in a box-and-arrow picture, and all of them decide whether an integration is reliable.

This chapter walks through ten of the hard cases as sequence diagrams. A sequence diagram has one vertical line per participant, and time flows downward; each arrow is a message, numbered in order. Where a failure usually strikes, a red lettered circle explains it below the figure. Read each diagram slowly, tracing the numbers, and ask at every step: *what if the process died right here?* That question is the single most useful habit in this book.

> **In this chapter**
    * Trace ten failure-prone interactions step by step, and say what happens at each possible crash point
    * Explain why a watermark must advance only after a batch succeeds
    * Show how a receiver acknowledges quickly and still processes exactly once
    * Distinguish transient from permanent failure, and describe the circuit breaker's three states
    * Describe how an outbox, a saga, and a consumer group behave when something goes wrong

## Refreshing a Token and Surviving a Surprise 401

Almost every integration begins with authentication, and a surprising share of production outages end there too. the figure shows the standard flow for an unattended job, including what to do when a token stops working early.

*[Figure: OAuth 2.0 client credentials with refresh and a surprise 401.]*
The integration job asks a **token cache** for a token (step 1). The cache has none, or the one it holds is close to expiry (step 2), so it contacts the authorization server with the client's identity and secret (step 3) and receives an access token and its lifetime (step 4). The cache keeps the token until about 80 percent of its lifetime has passed, so that no request is ever sent with a token that expires in flight. The job then calls the target API with the token as a bearer credential (step 5) and receives a normal answer (step 6).

Now the surprise. Between two calls, the token is revoked, perhaps because an administrator rotated the secret, or it expires earlier than the server said it would. The next call (step 7) is answered with `401 Unauthorized` (step 8, failure point A). The correct behavior is exactly one repair: discard the cached token, fetch a new one (step 9), and retry the call once (step 10). If the retry also fails with 401, stop and alert. A loop that retries forever on 401 not only wastes effort; it can lock the account.

Three design rules follow. Use **one shared token provider** with a lock, so that twenty parallel workers that all see an expired token do not make twenty token requests. Allow **one re-authentication per failure**, never more. And **never log the token**, not even in debug output. Chapter 13 builds this provider, and Appendix E contains a tested version.

## Polling with a Watermark, and a Crash in the Middle

The polling pattern of Chapter 6 looks simple, and its correctness depends on one detail: *when* the bookmark moves. the figure follows a run that crashes halfway.

*[Figure: Polling with a watermark, and a crash in the middle.]*
A scheduler wakes the poller every five minutes (step 1). The poller reads the **watermark** from its store (steps 2 and 3): call it T0, the newest change time it has seen so far. It then asks the source for everything modified since T0 minus two minutes (step 4). The deliberate two-minute **overlap** guards against rows that were committed late. The source returns the first page of results with a cursor (step 5), and the poller upserts the page into the target (step 6). It requests the second page (step 7), receives the last page (step 8), and upserts it (step 9).

At failure point A, something goes wrong: the process is killed, or the target rejects a write. What matters is what has *not* happened. The watermark has not advanced, because the poller moves it only after the whole run succeeds. So the next run starts from T0 again, re-reads pages one and two, and repeats the upserts. Because upserts are idempotent, repeating them changes nothing.

Two rules produce reliability. **Move the watermark last**, after every record has been written, and write it atomically (to a temporary file, then rename) so that a crash cannot leave it half-written. And **make the writes idempotent**, so that the overlap and the re-reads, which are certain to occur, are harmless. Together they convert "at least once" delivery into "effectively once" results. The companion code in Appendix E implements precisely this sequence, and its tests kill the poller mid-batch to prove it.

## A Webhook Receiver That Survives Duplicates

A webhook sender has one worry, whether you received the event, and one tool, retrying. The receiver must therefore expect duplicates. the figure shows a receiver built for them.

*[Figure: A webhook receiver with a queue and duplicate protection.]*
The source posts a signed event, e1 (step 1). The receiver verifies the signature and timestamp, then puts the event on a queue (step 2) and immediately answers `200` within milliseconds (step 3). It does *not* process the event; doing so would keep the sender waiting and risk a timeout. Later, a worker takes the event from the queue (step 4) and asks a **dedupe ledger**, "have I seen e1?" (step 5). The answer is no (step 6), so the worker applies the change to the target (step 7) and records e1 in the ledger (step 8).

Now the retry. The sender did not see the `200` in time, perhaps because a network device dropped it, so it sends event e1 again (step 9, failure point A). The receiver again verifies and enqueues it (step 10), and the worker again takes it (step 11). This time the ledger answers yes (steps 12 and 13), and the worker skips it. One event, delivered twice, applied once.

The sequence embodies four rules: **acknowledge fast, process later, deduplicate by event ID, and reconcile on a schedule**. The last one is needed because some senders never retry for long, and none replay events you missed while you were down. A periodic pull of "everything changed since X" repairs the gaps. The verification and ledger code is in Appendix E.

## Asynchronous Request-Reply

Long-running work, such as a bulk import, should not hold a connection open. the figure shows the standard dance.

*[Figure: Asynchronous request-reply: 202 and polling.]*
The client submits a job with an idempotency key (step 1). The API places it on a queue (step 2) and replies at once with `202 Accepted` and a `Location` header naming a status URL (step 3). A worker takes the job (step 4) and marks it running (step 5). Meanwhile the client polls the status URL (step 6) and is told the job is still running, with a suggestion to wait five seconds (step 7). Later, the worker finishes and records the result (step 8). The next poll (step 9) is answered with `303 See Other`, redirecting to the result (step 10).

At failure point A the result is only retained for a limited time: collect it within the retention window, or it vanishes. Make the submission idempotent, so that a retry after a lost `202` does not start the job twice, honor the suggested polling interval, and set an overall timeout so that a stuck job does not make the client wait forever.

## A Saga with a Failing Step

When a business transaction spans systems, each step must be undoable. the figure shows an orchestrated saga that fails at the third step.

*[Figure: A saga with a failing step and compensation.]*
The orchestrator creates the order in a pending state (steps 1 and 2) and asks the inventory service to reserve stock (steps 3 and 4). It then asks the payment service to charge the card (step 5), and the card is declined (step 6, failure point A). The saga now *compensates in reverse order*: it releases the reserved stock (step 7) and cancels the order (step 8). The customer sees a clear failure, and no stock is stuck in a reservation nobody will claim.

Two facts make this work. The orchestrator **persists the saga's state before each step**, so that if it crashes mid-way it can resume or compensate after a restart. And **every step and every compensation is idempotent and retryable**, because the orchestrator itself may retry them. A compensation that cannot be repeated safely is a defect waiting for its first outage.

## The Outbox, Followed by Change Data Capture

The outbox pattern solves the dual-write problem, and its failure behavior is subtle enough to deserve a sequence. the figure shows it with a change-data-capture relay.

*[Figure: The transactional outbox with change data capture.]*
The service writes the order and its outbox row in *one transaction* (step 1), and the database confirms (step 2). A CDC connector, tailing the database's transaction log (step 3), sees the new outbox row (step 4) and publishes an event to Kafka with the order ID as the key (step 5). A consumer polls (step 6), receives the event (step 7), and applies it idempotently before committing its position (step 8).

The weak spot is at failure point A. If the connector restarts after publishing the event but before saving its own position, it will read the same log entry again and publish the event a second time. The outbox cannot prevent that: it guarantees that the state change and the event are never *separated*, not that the event is delivered only once. So consumers must deduplicate, by event ID or by a version number on the entity. The sequence also reminds us of an important truth about this class of tools: "exactly once" holds within a boundary, and the moment data crosses to something outside it, you are back to at least once.

## Kafka: Produce, Consume, Crash, Redeliver

Kafka's consumer model is easy to describe and easy to misunderstand. the figure follows one batch through a crash.

*[Figure: Kafka: produce, consume, crash, redelivery.]*
A producer sends with `acks=all` (step 1), meaning it waits until every in-sync replica has the record. The partition leader replicates to a follower (step 2), the follower acknowledges (step 3), and the producer receives an acknowledgment carrying the offset, 98 (step 4). A consumer whose last committed offset is 95 fetches from offset 95 (step 5) and receives records 95 to 98 (step 6). It processes them against the target (step 7).

Then it crashes *before committing its offset*. The committed offset is still 95. When the consumer restarts, or another member of the group takes over the partition, it fetches from 95 again (step 8), receives records 95 to 98 again (step 9), and reprocesses them (step 10). Only then does it commit offset 99 (step 11).

This is correct behavior, and it is **at-least-once delivery** in action. The consumer chose to commit *after* processing, which means a crash causes repeats but never losses. The alternative, committing before processing, would mean a crash causes losses but never repeats. For integrations, repeats you can handle are almost always preferable to losses you cannot see, so the rule is: process, then commit, and make processing idempotent. Chapter 18 explains offsets and commits in depth.

## Backoff, the Circuit Breaker, and the Dead Letter Queue

When a target fails, how a consumer reacts determines whether the outage stays small. the figure shows three mechanisms working together.

*[Figure: Backoff, circuit breaker, and dead letter.]*
The consumer calls the target through a **circuit breaker** (steps 1 and 2) and receives `503` (step 3), so the breaker reports an error (step 4, failure point A). The consumer waits using **exponential backoff with full jitter**, honoring `Retry-After` if the server sent one, and tries again (steps 5 to 7). After the failures reach a threshold, the breaker *opens*: the consumer's next call fails immediately, without even reaching the target (steps 8 and 9). This protects the struggling target from being hammered, and it protects the consumer from wasting threads on doomed calls. The right response at this point is to *pause consumption* rather than to discard messages.

After a cool-down, the breaker goes *half-open* and lets a single probe through (step 10). If it succeeds (step 11), the breaker closes and normal consumption resumes (step 12). A breaker has three states: closed (normal), open (failing fast), and half-open (testing recovery).

Later in the diagram, a different record produces a **permanent** error: a malformed message that the target rejects with `400` (failure point B). Retrying will never help. The consumer parks it, with the reason, in the **dead letter queue** and moves on. The ability to tell transient failures from permanent ones is what separates a resilient consumer from one that either loses data or blocks forever. Chapter 14 implements the retry decision, and Chapter 19 shows how Kafka-based consumers do the same with retry topics.

## Bidirectional Sync Without an Echo

The authority split avoids bidirectional synchronization when it can, but sometimes both systems must edit. the figure shows how to prevent the most notorious failure, the echo loop.

*[Figure: Bidirectional sync without an echo loop.]*
The sync service asks System A for changes since its checkpoint (step 1) and finds an edit by a person, Alice, at 10:00:03 (step 2). It asks System B for changes since *its* checkpoint (step 3) and finds no new human edits (step 4). It takes a lock on the record, a lease of 60 seconds so that a crashed service does not hold it forever (step 5), applies Alice's change to System B, stamping the change with its origin, A (step 6), releases the lock (step 7), and advances the checkpoint for System A (step 8).

On the next cycle, the service asks System B for changes (step 9) and finds one: an edit made at 10:00:10 by the integration's own user (step 10, failure point A). This is the echo, the change the service itself just made. If it were treated as a new edit, it would be copied back to System A, which would then show a change that the service would copy to System B, and so on forever. The defense is to **ignore changes made by the integration's own identity**, which is why the integration needs a dedicated service account, and to stamp changes with their origin as a second safeguard.

## A Consumer Group Rebalance

When members join or leave a Kafka consumer group, the partitions are redistributed. the figure contrasts the older eager protocol with the newer incremental ones.

*[Figure: A consumer group rebalance: classic versus incremental.]*
Consumer A joins the group (step 1) and is assigned all three partitions, P0 to P2 (step 2), and starts consuming. Consumer B then joins using the classic *eager* protocol (step 3). The coordinator tells Consumer A to **revoke all** its partitions (step 4); Consumer A rejoins (step 5), and the coordinator assigns P0 and P1 to A (step 6) and P2 to B (step 7). During this exchange, *nobody consumes anything*: a stop-the-world pause that grows with the size of the group.

With incremental protocols (cooperative rebalancing, and the newer consumer protocol described in Chapter 19), only the partitions that must move are interrupted: P2 is handed from A to B while A keeps consuming P0 and P1. Static group membership further avoids needless rebalances when a consumer restarts quickly. For integrations, the practical consequence is that rebalances cause duplicates, because uncommitted work on a revoked partition is redone by the new owner. This is one more reason that idempotency, not luck, is the foundation of a streaming consumer.

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



# Chapter 9. Making the Decision

Discovery produces answers. Patterns offer options. The step between them, deciding, is where many architects improvise, and where an explicit method pays for itself. Improvised decisions have two weaknesses: they favor whatever the decider knows best, and they leave no trail, so nobody can later tell whether the choice was reasoned or merely habitual.

This chapter gives you a method with two parts. The first is a set of **seven decision trees** for the choices that recur in every project: how to get data out of the source, how to write to the target, where the runtime should live, which authentication to use, whether to use Kafka and how to feed it, how to take data out of it, and which class of technology to build on. The second is a **scorecard** that combines your answers into a ranked recommendation, with a worked example. Neither replaces judgment. Both make it visible, which is what allows a colleague to challenge it.

> **In this chapter**
    * Use seven decision trees to make the recurring technical choices in an integration
    * Explain why each tree ends in a mechanism or a class, never in a product name
    * Score candidate patterns against discovery answers, and interpret a close second place
    * Combine two near-tied patterns into one design, such as webhook plus reconciliation poll
    * Record the decision, the rejected alternatives, and the conditions for revisiting them

## Seven Decision Trees

Read each tree from the left. Diamonds are questions you can answer from discovery; rounded boxes are outcomes. Every tree ends in a *mechanism* or a *class*, not in a product. That is deliberate: products change, mechanisms last. After the tree tells you "use log-based change data capture," choosing between Debezium and a commercial tool is a separate, later question.

### How to Get Data Out of the Source

Start with what the source really offers, because that, more than your preferences, decides the extraction mechanism. the figure shows the tree.

*[Figure: How to get data out of the source.]*
If the source exposes an API, the first question is whether it supports a modified-since filter or a change feed. If so, **poll with a watermark and reconcile**. If not, ask whether it sends webhooks or events; if so, use a **webhook with a queue and a reconciliation poll**. If neither exists, ask whether listing everything is feasible; for small and medium datasets, use **snapshot and diff**. If listing is infeasible, ask the vendor for a change feed, or, failing that, read the underlying database's log.

If the source offers no API, ask whether direct database access is allowed. If you may read the transaction log, use **log-based change data capture**; if not, a **JDBC query poll** against a replica using a timestamp column. If there is no database access, look for files (**a file drop with a manifest**), a message queue (**a bridge or subscription**), or, failing everything, UI automation as a stopgap while you push for a real interface.

### How to Write to the Target

The target's write semantics decide how safely you can retry, so this tree is about idempotency. the figure shows it.

*[Figure: How to write to the target.]*
If the target supports an **idempotent upsert by key**, everything is easy: for more than about 100,000 records per run, use a bulk import API in batches; for fewer, upsert per record behind a rate limiter. If it does not, check whether it accepts an **idempotency-key header**: if yes, create with the key and keep a deduplication ledger. If not, ask whether you can read the target to check for existence; if yes, *look up before you write*, store the foreign ID, and allow only one writer per key. If you cannot even read, you are left with a single-writer queue plus reconciliation, and you should ask the vendor for an upsert. A strict rate limit on the target adds a queue and a throttle in front of any of these.

### Where the Runtime Should Live

Data-processing boundaries and network direction decide hosting before preferences do. the figure shows the tree.

*[Figure: Where the runtime should live.]*
If payloads may not leave your network or region, use a customer-hosted runtime if the platform offers one (and check its capacity); otherwise run containers or virtual machines with your own code or a self-hosted runtime. If payloads may leave, ask whether the endpoints are reachable from the internet. If yes, a vendor-cloud integration platform or serverless functions is usually fastest. If not, ask whether an outbound-only agent is allowed: if so, use an **agent plus cloud control plane**, and verify where the logic actually runs; if not, you need a private link or VPN to a cloud or on-premises runtime.

### Which Authentication

Machine identity first; human flows only for humans. the figure shows the tree.

*[Figure: Which authentication to use.]*
Ask first who or what is calling. For **a person**, use single sign-on with an authorization-code flow and PKCE. For **a job**, prefer OAuth 2.0 client credentials with short-lived tokens and secrets in a vault. If those are not offered, look for a JWT bearer grant or mutual TLS (and alert on certificate expiry), then an API key (in a header, scoped, and rotated), and as a last resort basic authentication over TLS with a single service account and a vault. For **a webhook**, authenticate by an HMAC signature with a timestamp, and deduplicate by event ID. Chapter 13 covers each of these.

### Do You Need Kafka, and Which Way In

Kafka earns its place through replay, fan-out, or throughput. the figure shows the tree.

*[Figure: Do you need Kafka, and which way in.]*
If you need none of the three, do not use Kafka; poll, use a webhook with a queue, or use an integration platform. If you do, choose the entrance that matches the source. Your own **application** produces events directly, with an outbox for atomicity. A **database** feeds through change data capture, or a JDBC poll if the need is simple. **SaaS webhooks** are published by an HTTP gateway or an integration platform. **Legacy** sources, such as MQ, files, and MQTT, use a source connector or a bridge.

### Which Way Out of Kafka

Every exit starts with a pull from Kafka; the target decides what happens next. the figure shows the tree.

*[Figure: Which way out of Kafka.]*
A **store or warehouse** takes a sink connector. A **REST API with limits** takes a consumer or an HTTP sink that pauses on 429 and uses idempotency keys. **Serverless** functions take an event-source trigger and an idempotent handler. **Browsers and mobile** apps take a server-push gateway. A **SaaS** application is reached through an integration platform's listener, with a check on its acknowledgment mode. And if the work has *task semantics*, where order does not matter and each item goes to one worker, consider share groups or a queue instead.

### Which Class of Technology

Finally, which class of platform should carry the pattern? the figure shows the tree. Walk it from top to bottom; the first "yes" usually identifies the dominant workload.

*[Figure: Which class of technology.]*
Mostly SaaS endpoints with business-led delivery points to an **integration platform** (checking where data is processed). Bulk data into analytics points to **ELT and CDC tooling**. Partner documents and EDI point to **managed file transfer and a B2B gateway**. High-volume events with many consumers point to **Kafka or a streaming platform**. Transactional messaging in a mainframe estate points to an **enterprise service bus and message queue** estate. Engineering-led teams that work Git-first point to **code-first services**, and cloud-native estates to the cloud's own workflow and messaging services. Whatever the tree says, validate with a proof of concept against the hardest real flow.

## The Scorecard Method

The trees decide one question at a time. A real integration has many answers at once, and they pull in different directions: freshness favors webhooks, the network favors polling, replay favors streaming. A **scorecard** combines them. The idea is simple. For each answer, ask which candidate patterns it favors or disfavors, and add points. The pattern with the most points leads, and the tally shows why.

**Table: A scorecard for the shop-to-ERP order flow**
| Discovery answer | Webhook + queue | Polling with watermark | Change data capture | Nightly batch file |
|---|---|---|---|---|
| Goal: keep operational systems in sync | +1 | +2 | +1 | 0 |
| Freshness: a few minutes | +2 | +2 | +1 | -2 |
| Volume: thousands per day | 0 | 0 | 0 | +1 |
| Replay: occasionally, from the source | -1 | +1 | +1 | +1 |
| Source: webhooks and a modified-since filter | +3 | +2 | 0 | 0 |
| Network: inbound allowed through a gateway | +1 | +1 | 0 | 0 |
| Skills: a Python team | +1 | +1 | -1 | 0 |
| **Total** | **7** | **9** | **2** | **0** |

The scores are the author's judgment, not natural constants, and you should adjust them for your context. Their value is in forcing each answer to be weighed explicitly. Here polling leads with 9, webhooks follow with 7, change data capture trails because the source is a SaaS product with no database to read, and the nightly file is out because it cannot meet the freshness target.

### Reading a Close Second

The difference between first and second is only two points. When the top two are within about three points, the scorecard is telling you not to choose one. Instead, *combine them*. Webhooks supply the speed that polling cannot, and polling supplies the completeness and replay that webhooks lack. The combination, a webhook feeding a queue as the fast path, plus a reconciliation poll as the slow path, is exactly the "reliable SaaS notifications" recipe from Chapter 7. That is the design Larkspur chose.

> **Why this matters**
    A near-tie is information. It usually means each candidate has a weakness that the other covers. Forcing a choice discards the covering strength. Teams that pick "webhooks" alone discover, within a month, that a weekend outage lost orders. Teams that pick "polling" alone discover that the freshness target is missed whenever the poll interval is long. The combination costs a little more, and is much more robust.

### Taming the Unknown Answers

A scorecard with blank cells is still useful. Treat each unanswered question as a *risk to resolve*, and check whether any answer could flip the leader. If the missing answer is "can the ERP's create call be made idempotent?", and a "no" would add an idempotency ledger to every candidate, then the missing answer changes the cost but not the winner, and you can proceed. If a missing answer would flip the winner, resolve it before the gate.

## Three Worked Examples

Working through different integrations shows how the method generalizes.

**A warehouse load from a legacy database.** Larkspur wants its ERP's order tables replicated to the analytics platform with a freshness of ten minutes. The source tree says: no API, direct database access allowed, and the vendor permits reading the transaction log, so **log-based change data capture**. The Kafka tree says: data volume and the number of consumers (analytics, fraud, a search index) justify Kafka, entering through CDC. The exit tree says: a sink connector into the warehouse. The scorecard confirms it, and the recipe adds a snapshot-and-diff job as a weekly audit.

**A supplier's purchase orders.** A large retailer sends Larkspur purchase orders as X12 documents over AS2. The class-of-technology tree says: partner documents and EDI point to managed file transfer and a B2B gateway. The target tree says the ERP accepts documents through IDocs, which are idempotent by document number. The recipe is EDI over managed file transfer, with acknowledgments returned automatically. No scorecard is needed: the constraint (a trading partner's format) decided it.

**A two-way ticket synchronization.** A service desk and a project tool both edit tickets. The scorecard favors bidirectional sync, but the design review asks the authority question first. The authority matrix shows that only comments are truly shared; status belongs to the service desk and the description to the project tool. The result is two one-way flows and an append-only comment sync, a far simpler design than the bidirectional merge the first scorecard suggested.

## Recording the Decision

A decision that cannot be reconstructed will be remade, so record it as an architecture decision record. Include the options considered, the scores or tree path that led to the choice, the *rejected alternatives and why*, and the conditions under which you would revisit it. A decision record for the shop-to-ERP flow might read: "Chosen: webhook plus queue as the fast path, and a fifteen-minute reconciliation poll. Rejected: polling alone (misses the five-minute target at peak), change data capture (the shop is SaaS, with no database access). Revisit if the shop adds an event stream with replay."

## Limits of the Method

Be honest about what trees and scorecards cannot do. They cannot capture political constraints (a platform mandated by the CIO), organizational realities (a team that has never run Kafka), or the cost of a choice over three years. They treat answers as facts when many are estimates. They favor patterns that the author of the scorecard understood.

Use them as a drafting aid and a teaching tool, never as an oracle. Their strength is not that they produce the correct answer but that they make your reasoning inspectable. When a colleague disagrees with your scorecard, you can ask which row they would change, and the argument becomes productive instead of tribal. Chapter 23 adds the cost and platform dimensions that this chapter leaves aside.

## Summary

Seven decision trees handle the recurring choices: source extraction, target writes, runtime hosting, authentication, Kafka entry, Kafka exit, and technology class. Each ends in a mechanism or class, never a product. A scorecard combines many answers by adding points for each pattern, and a close second place tells you to combine patterns, as when webhooks supply speed and a reconciliation poll supplies completeness.

Unknown answers become risks, and you check whether any could flip the winner. Worked examples show the method adapting to a database replication, an EDI exchange, and a two-way sync that the authority split reduces to two one-way flows. The decision, its rejected alternatives, and its revisit conditions go into a decision record. The method makes reasoning inspectable; it does not replace judgment.

## Exercises

1. **Walk the trees.** Take an integration you are planning and walk all seven trees. Write the outcome of each. Where did a tree disagree with your instinct?
2. **Build a scorecard.** Choose three candidate patterns for a real flow, list ten discovery answers, and fill in a scorecard. Which answer moved the result most?
3. **Resolve a near-tie.** Find a case where two patterns scored within three points. Design the combination and write the sequence in which the two paths cooperate.
4. **Write the rejected alternatives.** For a past decision of yours, write the "rejected alternatives" section of a decision record, giving a specific reason for each.



---

# Part III. Design and Build

Reading other people's APIs, designing your own, moving and transforming data, authenticating, writing clients that survive production, keeping systems in sync, and testing and shipping the result.



# Chapter 10. Reading API Documentation Like an Architect

When Larkspur's team first read the shop vendor's API documentation, they found the call they needed in ten minutes: `GET /orders`, returning a list of orders with a field called `total`. They wrote the mapping that afternoon. A week later, in testing, the field turned out to be called `totalAmount`, the list returned at most 50 orders per page regardless of the `limit` parameter, the `updatedSince` filter ignored time zones, and a change to an order's shipping address did not change its `updatedAt` timestamp. None of this was in the documentation. All of it was discoverable in an hour of poking at the sandbox.

Developers read documentation to find the call they need. Architects read it to find **what can go wrong**. The difference is a habit, and it is the subject of this chapter. The goal is a one-page *reconnaissance sheet* that answers every design question about an API before anyone writes a line of integration code, and a practice of checking the documentation against the running system, because the two disagree more often than anyone admits.

> **In this chapter**
    * Apply a ten-step reading method that extracts the facts a design depends on
    * Fill in an API reconnaissance sheet, and probe a real API to verify it
    * Analyze an OpenAPI contract with a short script that lists hints and gaps
    * Choose between offset, cursor, keyset, and link-header pagination, and explain why offsets fail under change
    * Recognize the signs of untrustworthy documentation and know what to do about them
    * Turn a reconnaissance sheet directly into a design

## The Ten-Step Reading Method

Work through the documentation with these ten questions, in order. Each yields a fact that will appear in the design, and for each you should be ready to write down either an answer or an explicit "unknown, ask X."

1. **Find the contract.** Is there an OpenAPI (formerly Swagger) specification, a Postman collection, or a WSDL for a SOAP service? A machine-readable contract beats prose every time, because tools can read it, compare it with the real API, and warn you when it changes. Download it and keep it in version control.
2. **Base URL, environments, and versions.** Are there separate hosts for sandbox and production? Is the version in the path (`/v2/`), in a header, or date-based? What is the deprecation policy, and how much notice does the vendor give?
3. **Authentication and authorization.** Which scheme, which scopes, what token lifetime? Who issues credentials, and is there a concept of a service account? (Chapter 13 treats this in depth.)
4. **Resource model.** List the nouns and how they relate, and draw them. Identify the stable identifier of each, and whether a human-readable key also exists. Is the ID a UUID, a number, or something that changes when the record is renamed?
5. **Read paths.** How do you list, filter, sort, and fetch by ID? What is the maximum page size? Is there a "modified since" filter or a change feed?
6. **Write paths.** How do you create, update (does `PUT` replace the whole resource while `PATCH` merges?), and delete (hard or soft)? Are there bulk endpoints? Are writes idempotent, or do they accept an idempotency key?
7. **Pagination.** Offset, page number, cursor, or link header? Is the total count expensive to compute? Is ordering stable while you page?
8. **Limits.** Rate limits (per second, per day, per tenant), payload size limits, concurrency limits, timeouts, and the headers that report your remaining budget.
9. **Errors and asynchrony.** What does an error body look like? Which codes are retryable? Is partial success possible? Do long operations return a job ID to poll?
10. **Eventing.** Are there webhooks, event subscriptions, or streams? How are they signed? What are the retry and replay behaviors?

The order is deliberate. The first three questions tell you whether you can connect at all. The next four describe the data and the ways to move it. The last three describe what happens when things go wrong, and they are the ones that documentation most often skips.

## The API Reconnaissance Sheet

Copy the template in the table into your project folder and fill it in during the first week. It becomes the basis of the design document and, later, of the support runbook. The "Answer" column holds example answers for a typical SaaS API; yours will differ, and the value is in having a written answer for every row.

**Table: The API reconnaissance sheet, with example answers**
| Topic | Questions | Example answer |
|---|---|---|
| Contract | Where is the specification? Which version? When did it last change? | `openapi.json` 3.1, Git tag v2.4 |
| Environments | Which hosts? How is sandbox data refreshed? | `sandbox.example.com`, refreshed monthly |
| Authentication | Which scheme and scopes? Expiry? Rotation? | OAuth 2.0 client credentials, one-hour token, scope `read:orders` |
| Identity | Primary key, natural key, uniqueness rules? | UUID `id`; unique `number` per tenant |
| Read | Filters, sorting, field selection, maximum page? | `limit` up to 1,000; `updatedSince` in ISO 8601 UTC |
| Pagination | Type, cost of totals, stability? | Cursor via `nextCursor`; no total |
| Write | Upsert? Idempotency key? Bulk? | `POST /orders/bulk` up to 500 items; header `Idempotency-Key` |
| Delete | Hard or soft? How to detect? | Soft: `status=archived`; no delete feed |
| Limits | Rate, size, concurrency? | 600 per minute per tenant; header `X-RateLimit-Remaining` |
| Errors | Shape, retryable codes, partial success? | 429 and 503 retryable; 207 with per-item status |
| Asynchrony | Job endpoints, polling interval? | 202 plus `Location`; poll every 5 s, maximum 10 min |
| Events | Webhooks, signature, replay? | HMAC-SHA256 header; 24-hour retry; no replay |
| Time | Time zone, precision, server clock? | UTC, milliseconds; `Date` header present |
| Support | Status page, contact, change notices? | `status.example.com`; breaking changes with 90 days notice |

Two cells deserve special attention because they decide the architecture. **"No delete feed"** means you cannot learn about deletions from the API at all, and you will need a periodic comparison (Chapter 15). **"No replay"** on webhooks means a missed event is gone, so webhooks can only be an accelerator, never the sole source.

## Probe Before You Trust

Ten minutes of `curl` tells you more than an hour of reading. Run these probes against the sandbox, and record the results, with the date and environment, in the sheet. The examples use the book's lab server so you can try them immediately; replace the URL with your target.

```bash
# 1. Headers reveal rate limits, versions, paging, and caching
curl -sS -D - -o /dev/null "http://127.0.0.1:8080/orders?limit=1"

# 2. What does an error look like? Send a deliberately bad request
curl -sS -i -X POST http://127.0.0.1:8080/orders -d '{"sku": null}'

# 3. What is the true maximum page size? Ask for far too many
curl -sS "http://127.0.0.1:8080/orders?limit=100000" | python3 -c \
  "import json,sys; print(len(json.load(sys.stdin)['results']))"

# 4. Does the incremental filter really work? Touch one record, then ask
#    (replace the date with today's date)
curl -sS -X POST http://127.0.0.1:8080/admin/touch/A1005 -o /dev/null
curl -sS "http://127.0.0.1:8080/orders?updatedSince=2026-11-23T00:00:00Z"
```

Look at what each probe teaches. The first shows which headers the API sends (does it report rate-limit budget?). The second shows the shape of an error body and whether it is machine-readable. The third reveals the real page-size cap. The lab server seeds 250 orders and caps any page at 500, so it prints 250; a real API may silently cap at 50 or 100, and the count you get back is the evidence. The fourth checks that the change filter works *and* that touching a record really moves its timestamp, which is not guaranteed; some systems update the timestamp only for certain fields.

> **Probe with care**
    Probes that write data (the second and fourth above) belong in a sandbox. Never run exploratory writes against production. When a sandbox is not available, restrict yourself to read-only probes, and ask the vendor how to test writes safely.

## Let a Script Read the Contract

If the API publishes an OpenAPI document, much of the reconnaissance can be automated. The script below reads an OpenAPI 3.x JSON file and prints what an architect wants to know: the servers, the security schemes, every endpoint with its documented response codes, *hints* (incremental filters, asynchronous operations, bulk endpoints), and *gaps* (lists with no paging, writes with no idempotency key, endpoints that never mention rate limiting). It needs only the Python standard library.

```python
#!/usr/bin/env python3
"""Summarize an OpenAPI 3.x document the way an architect reads it.

Usage: python3 openapi_recon.py openapi.json
"""
import json, sys

METHODS = ("get", "post", "put", "patch", "delete")
PAGING = {"limit", "page_size", "per_page", "pagesize",
          "cursor", "offset", "page"}
SINCE = {"updatedsince", "modified_since", "modifiedsince",
         "since", "updated_after"}

def params_of(item, op):
    found = {}
    for p in item.get("parameters", []) + op.get("parameters", []):
        found[p.get("name", "").lower()] = p.get("in")
    return found

def analyze(spec):
    info = {"title": spec.get("info", {}).get("title", "?"),
            "version": spec.get("info", {}).get("version", "?"),
            "servers": [s.get("url") for s in spec.get("servers", [])],
            "security": {}, "endpoints": [], "hints": [], "gaps": []}
    hints, gaps = info["hints"], info["gaps"]
    schemes = spec.get("components", {}).get("securitySchemes", {})
    for name, s in schemes.items():
        kind = s.get("type")
        if kind == "oauth2":
            kind += " (" + ", ".join(s.get("flows", {})) + ")"
        elif kind == "http":
            kind += " " + s.get("scheme", "")
        info["security"][name] = kind
    for path, item in spec.get("paths", {}).items():
        for method in METHODS:
            op = item.get(method)
            if not op:
                continue
            prm = params_of(item, op)
            codes = set(op.get("responses", {}))
            name = "%s %s" % (method.upper(), path)
            info["endpoints"].append(
                {"op": name, "params": sorted(prm), "codes": sorted(codes)})
            is_list = method == "get" and not path.rstrip("/").endswith("}")
            if is_list and not PAGING & set(prm):
                gaps.append("%s is a list with no paging parameter" % name)
            if is_list and SINCE & set(prm):
                found = ", ".join(sorted(SINCE & set(prm)))
                hints.append("%s supports incremental reads (%s)"
                             % (name, found))
            if method == "post" and "idempotency-key" not in prm:
                gaps.append("%s has no Idempotency-Key header" % name)
            if "202" in codes:
                hints.append("%s is asynchronous (202): plan polling" % name)
            if any(w in path.lower() for w in ("bulk", "batch", "import")):
                hints.append("%s is a bulk candidate" % name)
            if "429" not in codes:
                gaps.append("%s documents no 429 response" % name)
    if not info["servers"]:
        gaps.append("no servers listed: base URL and sandbox unknown")
    if not info["security"]:
        gaps.append("no security schemes declared")
    return info

def main(path):
    with open(path) as f:
        info = analyze(json.load(f))
    print("%s %s" % (info["title"], info["version"]))
    print("Servers:  ", ", ".join(info["servers"]) or "none")
    print("Security: ", info["security"] or "none")
    print("Endpoints: %d" % len(info["endpoints"]))
    for e in info["endpoints"]:
        print("  %-28s codes=%s" % (e["op"], ",".join(e["codes"])))
    for title, key in (("Hints", "hints"), ("Gaps to ask about", "gaps")):
        print("\n%s:" % title)
        for line in info[key] or ["none"]:
            print("  -", line)

if __name__ == "__main__":
    main(sys.argv[1])
```
Running it against a specification produces a report like this:

```text
Orders 2.4
Servers:   https://api.example.com/v2
Security:  {'oauth': 'oauth2 (clientCredentials)'}
Endpoints: 4
  GET /orders                  codes=200,429
  POST /orders                 codes=201
  GET /orders/{id}             codes=200
  POST /orders/bulk            codes=202

Hints:
  - GET /orders supports incremental reads (updatedsince)
  - POST /orders/bulk is asynchronous (202): plan polling
  - POST /orders/bulk is a bulk candidate

Gaps to ask about:
  - POST /orders has no Idempotency-Key header
  - POST /orders documents no 429 response
  - GET /orders/{id} documents no 429 response
  - POST /orders/bulk documents no 429 response
```

The report is a *list of questions for the vendor*, not a verdict. A missing `Idempotency-Key` header in the specification does not prove the API cannot be retried safely; it means you must ask. And a contract can be incomplete or out of date, which is why the script complements the `curl` probes rather than replacing them.

## Pagination: The Detail That Breaks Synchronization

Of everything in an API, pagination is the topic most worth understanding deeply, because an extraction that pages incorrectly loses or duplicates data *silently*. The core problem is shown in the figure.

*[Figure: pagination-offset-drift]*
**Offset paging** asks for "the records starting at position 5, five at a time." It is simple, and it assumes that the list does not change while you read it. When it does, positions shift. If a record is inserted at the front between your first and second requests, everything moves down one place, and the second page begins with a record you have already seen. If a record is deleted instead, everything moves up, and the second page begins one record too late: a record is skipped without any error. For a one-off report, this does not matter. For a synchronization that reads thousands of records while users are working, it matters constantly.

**Cursor paging** replaces the position with a bookmark. The server returns, with each page, an opaque token marking the last record delivered, and the next request says "give me the records after this one." Insertions and deletions elsewhere in the list do not move the bookmark, so nothing is repeated or skipped. Cursors also tend to perform at constant cost, however deep you go, whereas offset queries get slower the further you page.

**Table: The five pagination styles and how to use each**
| Style | Looks like | Strength | Weakness | Integration advice |
|---|---|---|---|---|
| Offset and limit | `?offset=2000&limit=500` | Simple; random access | Slower when deep; shifts under change | Acceptable for small, static sets; avoid for full extracts |
| Page number | `?page=5&per_page=100` | Simple | Same drift as offsets | Cap the page count; sort by a stable key |
| Cursor or token | `?cursor=eyJpZCI6…` | Stable and fast | No random access; cursors may expire | Preferred for bulk reads; save the last cursor as a checkpoint |
| Link header | `Link: <…>; rel="next"` | Self-describing | Requires parsing headers | Follow links exactly; never build URLs by hand |
| Keyset | `?after_id=981233` | Fast and simple | Needs a sortable unique key | Excellent when you control the sort key |

Four practical rules cover most situations. **Prefer cursors for anything you extract in bulk**, and persist the last cursor as a checkpoint. **Never mix paging styles** in one read: many APIs reject, or silently misinterpret, a request that carries both an offset and a cursor. **Always specify a stable sort field** so that "the order" means the same thing on every page. And **ask whether the total count is expensive**. Some APIs compute a total on every offset request, which on a large collection can be the slowest part of the call, and offer a parameter to switch it off; others return nothing for the total with cursors. If you do not need the total, do not ask for it.

> **Read the page-size limit per endpoint**
    The maximum page size often differs between endpoints on the same API: a search endpoint might allow 1,000, a list endpoint 100. Read it per endpoint, probe it, and never assume one global value. A client that requests 500 and silently receives 100 will compute its progress wrongly.

Finally, look for **bulk and job endpoints** before looping over single calls. If you must load two million records, an import endpoint that takes a file and returns a job ID is usually orders of magnitude faster, and gentler on the vendor's rate limits, than two million requests.

## Signs the Documentation Is Lying

Documentation is written by people who know the system, for people who do not, and it is rarely tested against reality. Learn to recognize the signs.

**Table: Warning signs in documentation, and what to do about them**
| Warning sign | What to do about it |
|---|---|
| Examples show only success responses | Capture real error responses and ask for the error catalog |
| Field types are listed as "string" everywhere | Capture real responses and diff them against the specification |
| No mention of limits or pagination | Ask the API owner to confirm limits in writing |
| "Last updated" is two years ago | Check the changelog and release notes, not just the reference |
| Example IDs are `123` but real IDs are UUIDs | Treat all examples as illustrative; probe with real data |

When a specification, a wiki page, and the running API disagree, for example when they use different field names for the same request, **trust the running API**, record the discrepancy explicitly with the date and environment, and tell the owner. Silently picking one version is how drift enters a client deliverable. A line in the reconnaissance sheet saying "docs say `caller`, API returns `caller_id` (observed 2026-11-23, sandbox)" is worth more than ten pages of design that assume the wrong name.

## From Reconnaissance to Design

A complete reconnaissance sheet makes the design nearly write itself. Suppose probing a ticketing API produced these facts: cursor pagination; a `modified_since` filter; no delete feed; 300 requests per minute; webhooks available but without replay; and OAuth 2.0 client credentials with one-hour tokens. The design follows almost mechanically:

* **Primary path:** a scheduled pull every five minutes using `modified_since` minus a two-minute overlap, cursor pagination, and an upsert by the source's ID.
* **Deletes:** a nightly comparison of the full ID list, because there is no delete feed.
* **Webhooks:** an optional accelerator only. Because there is no replay, never rely on them alone.
* **Budget:** at most four requests per second sustained, which keeps use under the 300-per-minute limit with headroom; back off on 429 and honor `Retry-After`.
* **Authentication:** cache the token, refresh at 80 percent of its lifetime, and retry once on 401.

Every bullet traces back to a row in the sheet. When a reviewer asks "why do you reconcile nightly?", the answer is "no delete feed," and the evidence is a dated observation. That is what documentation *reading* for an architect looks like: not finding the call, but extracting the facts that make a design defensible.

## Summary

Architects read API documentation to find what can go wrong. A ten-step method, covering the contract, environments, authentication, resource model, read and write paths, pagination, limits, errors, and eventing, extracts the facts a design depends on, and a one-page reconnaissance sheet records them with dates. Probing the real API with `curl` verifies the documentation, and a short script can read an OpenAPI contract and list hints and gaps as questions for the vendor.

Pagination deserves particular attention: offsets drift when data changes during a read, silently duplicating or skipping records, so bulk extractions should use cursors, with a saved checkpoint and a stable sort field. Look for bulk endpoints before looping, treat documentation that omits errors, limits, and real types with suspicion, and, when sources disagree, trust the running API and record the discrepancy.

## Exercises

1. **Fill in a sheet.** Choose an API you integrate with, or a public one such as GitHub's, and fill in every row of the reconnaissance sheet. Mark the rows you could answer only by probing.
2. **Find the real page size.** For three endpoints of the same API, find the maximum page size by experiment. Do they differ from the documentation?
3. **Run the analyzer.** Run `openapi_recon.py` on a real OpenAPI document. Turn the first five gaps into questions you would send to the API owner.
4. **Demonstrate drift.** Using the lab server, write a loop that reads all orders with offset paging, touching one record between pages. Then repeat with cursors. Count duplicates and gaps in each.



# Chapter 11. Designing APIs, Webhooks, and Events

Every complaint you have ever had about a vendor's API is a design rule in disguise. The list endpoint with no way to ask "what changed since yesterday?" taught you that providers must offer change detection. The create call that made a duplicate when you retried it taught you about idempotency keys. The error message that said only "Bad Request" taught you that errors are part of the interface. The webhook feed that went silent for a weekend, with no way to ask what you missed, taught you about replay.

Chapter 10 taught you to read other people's interfaces. Architects also *design* interfaces that others will consume: an API placed in front of a legacy system, a webhook feed for partners, a stream of business events on a shared platform. The consumers of those interfaces are integrators like you, and the quality of your design determines whether their integrations are simple and safe or fragile and expensive. This chapter turns the lessons of every difficult integration you will ever build into rules for the provider's side of the fence.

> **In this chapter**
    * Describe the lifecycle of an API, from contract-first design to retirement
    * Apply the design rules that make an API easy to integrate: stable identifiers, change detection, cursor paging, idempotent writes, bulk paths, and consistent errors
    * Use RFC 9457 problem details for errors, and write an OpenAPI contract that encodes the rules
    * Build a reliable webhook feed: outbox, signatures, retries, delivery log, and replay
    * Design events with the same care as APIs, including schema, versioning, and ordering guarantees
    * Review a design against a checklist before consumers depend on it

## The API Lifecycle

An API is a product with a lifecycle, and the most common mistake is to design only its first phase. the figure shows the full arc.

*[Figure: The lifecycle of an API. Contract first, published with documentation, evolved additively, and deprecated with notice. Retiring an API is a planned step, not an accident.]*
It begins with **design**, ideally *contract first*: write the OpenAPI or AsyncAPI specification before the implementation, because a contract is cheap to change and code is not (step 1). The contract goes through **mock and review** against a style guide, where consumers can try it before it exists (step 2). Then **build and test**, including contract tests that verify the implementation matches the specification (step 3). The API is **published** with documentation and registered in a catalog (step 4) and **operated** with service levels and usage analytics (step 5). It **evolves** through additive changes that do not break consumers (step 6). When a breaking change is unavoidable, the old version is **deprecated** with a notice period and a visible sunset date (step 7), and finally **retired**.

The two phases most often forgotten are the last two. An API without a deprecation policy accumulates versions forever, each with consumers nobody can identify, and the cost of maintaining them never stops growing. Decide, at design time, how you will retire what you are creating.

## Design Rules That Save Your Consumers

the table lists the rules that make an API pleasant to integrate. Each one corresponds to a problem integrators meet daily, so each includes why integrators care.

**Table: Design rules for integration-friendly APIs**
| Topic | Rule | Why integrators care |
|---|---|---|
| Resources and naming | Plural nouns; stable identifiers in paths (`/orders/{orderId}`); consistent casing; verbs only for real actions (`POST /orders/{id}/cancellation`) | Predictable code with fewer special cases |
| Identifiers | Opaque, immutable IDs; accept and return the consumer's external ID where useful | Upserts by key; no duplicates after a rename |
| Change detection | Offer `updatedSince` with server-set timestamps, a change feed, or events, and a way to detect deletes | Incremental synchronization without full scans |
| Pagination | Cursor-based with a stable sort; return the next cursor; document the maximum page size | Consistent extraction while data changes |
| Writes | `PUT` or `PATCH` for updates; upsert by external key; an `Idempotency-Key` header for creates | Safe retries |
| Bulk | Provide bulk endpoints or asynchronous jobs (202 plus a status URL) with per-item results | Volume without millions of calls |
| Concurrency | Use ETags with `If-Match`, or version fields | No lost updates |
| Errors | One machine-readable format; stable error codes; a correlation ID in every response | Correct retry and quarantine decisions |
| Limits | Document them; answer 429 with `Retry-After`; report the remaining budget in headers | Clients can pace themselves |
| Versioning | Additive changes need no new version; breaking changes get a new major version and a migration window | No surprise breakage |
| Deprecation | Announce in documentation and changelog; send the `Sunset` header (RFC 8594) and a deprecation signal; notify known consumers | Time to migrate |
| Security | OAuth 2.0 scopes per capability; object-level authorization on every call; no secrets in URLs | See the OWASP API risks in Chapter 27 |

Six of these rules repay a closer look.

### Change Detection

An integrator who wants to keep a copy of your data current needs to ask, cheaply, "what changed since I last looked?" If your API cannot answer, integrators will read everything repeatedly, which is expensive for them and for you. The best provision is an `updatedSince` filter backed by a **server-set** timestamp (never one the client can write) that moves whenever *any* field of the record changes. Add a way to learn about deletions: soft-deleted records that remain visible with a status, a "deleted since" endpoint, or a tombstone event. An API with a modified-since filter but no way to see deletes forces every consumer to build a full-comparison job, so decide whether you can afford to provide it once for all of them.

### Pagination

Offer cursors, as the figure explained, with a stable sort, a documented maximum page size, and a `nextCursor` that is absent on the last page. Keep cursors valid for a reasonable time, and document how long. If you also support offsets for convenience, document that they are unsafe for extraction under change.

### Idempotent Writes

Support an `Idempotency-Key` header on every `POST` that creates something. The server stores, for each key, a fingerprint of the request and the response it produced, for a window such as 24 hours. A repeated request with the same key and the same body returns the stored response (flagged, for instance, with a header) instead of repeating the work. A repeated key with a *different* body is a client bug, and should fail with `422` or `409` rather than silently doing something unexpected. The lab server in Appendix E implements a simple version, and an IETF draft is standardizing the header.

### Bulk Paths

Single-record endpoints are fine for interactive use and ruinous for volume. Provide either a bulk endpoint that accepts an array and returns a per-item result, or an asynchronous job interface (submit a file, receive `202 Accepted` and a status URL). Whatever you choose, return *per-item* results: "item 17 failed validation because the email address is malformed" is worth ten times a blanket failure.

### Errors

Errors are part of the interface. They need a consistent, machine-readable shape, stable codes consumers can switch on, a human-readable message, and a correlation ID that lets a support engineer find the exact request in your logs. The next section gives you the standard format.

### Versioning and Deprecation

Distinguish **additive** changes (a new optional field, a new endpoint, a new enum value that old clients can ignore) from **breaking** changes (removing or renaming a field, changing a type, tightening validation). Additive changes should never require a new version. Breaking changes require a new major version, a published migration guide, a notice period, and a `Sunset` header on the old version so that consumers' tooling can see the date. Measure usage per consumer so that you know whom to contact. A breaking change shipped without notice is the single most reliable way to make integrators distrust your platform.

## A Standard Error Body

Do not invent your own error format. RFC 9457, "Problem Details for HTTP APIs," defines a JSON shape with the media type `application/problem+json`. Using it means every client library can parse your errors the same way.

```http
HTTP/1.1 422 Unprocessable Content
Content-Type: application/problem+json

{
  "type": "https://api.example.com/problems/validation-error",
  "title": "Validation failed",
  "status": 422,
  "detail": "2 fields are invalid",
  "instance": "/v2/orders/10492",
  "correlationId": "c0a8-7f3a-91e2",
  "errors": [
    {"field": "email", "code": "FORMAT",
     "message": "must be a valid address"},
    {"field": "quantity", "code": "RANGE",
     "message": "must be between 1 and 99"}
  ]
}
```

The standard fields are `type` (a URI that identifies the kind of problem and can link to documentation), `title`, `status`, `detail`, and `instance`. The `correlationId` and `errors` array are extensions, which the standard explicitly allows. The pairing of a stable `type` with a per-field `code` gives consumers something they can write `if` statements against, which free-text messages never do.

## Contract First

Write the contract before the code, and let it encode the rules. The fragment below, in OpenAPI 3.1 (version 3.2.0, released in September 2025, keeps 3.1 descriptions valid), specifies the paging, change-detection, idempotency, and error behaviors of an orders API in about twenty lines.

```yaml
openapi: 3.1.0
info: {title: Orders API, version: 2.4.0}
paths:
  /orders:
    get:
      parameters:
        - {name: updatedSince, in: query,
           schema: {type: string, format: date-time}}
        - {name: cursor, in: query, schema: {type: string}}
        - {name: limit, in: query,
           schema: {type: integer, maximum: 500, default: 100}}
      responses:
        "200": {description: A page of orders and nextCursor}
        "429": {description: Rate limited; honor Retry-After}
    post:
      parameters:
        - {name: Idempotency-Key, in: header, required: true,
           schema: {type: string}}
      responses:
        "201": {description: Created}
        "409": {description: Conflict with an existing order}
        "422": {description: Validation error (problem+json)}
```

A contract written this way has three benefits beyond documentation. Consumers can generate clients and mock servers from it, so they can start work before you finish. You can lint it against a style guide in your delivery pipeline, so every API in the company follows the same rules. And contract tests (Chapter 16) can verify that the implementation does what the contract says.

## Webhooks as a Provider

If integrators cannot poll you efficiently, or you want to notify them promptly, you will offer webhooks. They look simple, and the difference between a naive webhook feed and a reliable one is large. the figure shows the reliable design.

*[Figure: A reliable webhook feed records events first, then delivers them with signatures, retries, a delivery log, and a replay endpoint.]*
Your service records each event in an **outbox or event store** in the same transaction as the business change (step 1). A **dispatcher** reads the store (step 2), signs each event, and sends it to each subscriber (steps 3 and 4). It records every attempt in a delivery log (step 5). If a subscriber is slow or down (failure point A), the dispatcher retries with backoff over hours, and after repeated failure disables the subscription and notifies the owner (step 6) rather than retrying forever.

**Table: Practices for a reliable webhook provider**
| Practice | Detail |
|---|---|
| Record before you send | Write events to an outbox or event store in the same transaction as the business change; a dispatcher delivers them |
| Sign every delivery | An HMAC over the timestamp and body, with the timestamp in a header; publish verification code samples |
| Unique event IDs and types | Consumers deduplicate by ID; event types are versioned (`order.updated.v1`) |
| Retry with backoff | Retry on timeouts and 5xx over hours, with growing intervals; treat 2xx as delivered; treat 4xx as the subscriber's error |
| Delivery log and replay | Let subscribers see attempts and request redelivery for a time window; this removes the biggest weakness of webhooks |
| Thin or fat payloads | Choose deliberately, as described below |
| Endpoint verification | Confirm ownership of a new subscriber URL with a challenge before sending data |
| Disable gracefully | After repeated failure, disable the subscription and notify its owner |

The decision between **thin** and **fat** payloads shapes every consumer. A thin payload carries only an event type and an ID, forcing the consumer to call your API for the details. It is never stale and leaks little, but it multiplies calls and requires you to keep a read API available. A fat payload carries the full state, saving calls, but becomes a public contract that is hard to change and can arrive out of order, so it needs a version number. Thin payloads suit sensitive data and fast-changing entities; fat payloads suit stable data and consumers who cannot afford a callback. If you choose fat, include a per-entity version so that consumers can discard stale updates.

Most important of all is the **delivery log with replay**. Giving subscribers a way to see what you sent and to ask for it again converts the webhook's chief weakness, that a missed event is gone, into a solved problem, and saves your support team countless tickets.

## Events as a Provider

An event published to Kafka or another broker is an API with a longer memory: old events remain in the log, and consumers replay them months later. Design events with the same care, and document them with the same rigor. AsyncAPI is the counterpart of OpenAPI for event-driven interfaces.

```yaml
asyncapi: 3.0.0
info: {title: Order events, version: 1.0.0}
channels:
  orderUpdated:
    address: sales.order.events.v1
    messages:
      orderUpdated: {$ref: '#/components/messages/OrderUpdated'}
operations:
  publishOrderUpdated:
    action: send
    channel: {$ref: '#/channels/orderUpdated'}
components:
  messages:
    OrderUpdated:
      payload:
        type: object
        required: [orderId, status, version, occurredAt]
        properties:
          orderId: {type: string}
          status: {type: string,
                   enum: [CREATED, PAID, SHIPPED, CANCELLED]}
          version: {type: integer,
                    description: Increases with every change to the order}
          occurredAt: {type: string, format: date-time}
```

The contract states the topic name (with a version), the payload shape, and, in the `version` field, the property that lets consumers discard stale or duplicate events.

**Table: Event design: do and avoid**
| Do | Avoid |
|---|---|
| Name events in the past tense by business meaning (`OrderShipped`) | Naming by table or operation (`orders_row_updated`) |
| Include the entity key, a per-entity version, the event time, and a unique event ID | Omitting a version, so consumers cannot discard stale updates |
| Use a standard envelope such as CloudEvents and a registered schema with a compatibility mode | Breaking schema changes made in place |
| State the ordering guarantee and the retention period in the contract | Huge payloads where a claim check would do |
| Name an owner and a deprecation policy | Publishing internal database rows as the public contract |

The last pair deserves emphasis. A table-change event leaks your internal schema to every consumer, so the moment you rename a column, a dozen teams break. A business event such as `OrderShipped` is something you can keep stable while the internals change.

## An API Design Review Checklist

Before consumers start to depend on an interface, ask these questions about the design. Each "no" is something integrators will have to work around, for years.

* Is there a contract (OpenAPI or AsyncAPI), linted against a style guide and reviewed before the build?
* Can a consumer synchronize incrementally, detect deletes, and page consistently?
* Are writes idempotent, and are bulk paths available?
* Is the error format standard, with correlation IDs and stable codes?
* Are limits documented and enforced with `429` and `Retry-After`?
* Are authorization checks done per object and per property, not only per endpoint?
* Is there a versioning and deprecation policy, with a named owner?
* Is there a sandbox with realistic data and a published changelog?

## Summary

An API is a product with a lifecycle that begins with a contract and ends with planned retirement. The rules that make it easy to integrate mirror the problems integrators meet daily: stable identifiers, server-set change detection with a way to see deletes, cursor paging, idempotent writes with an idempotency key, bulk paths with per-item results, consistent errors in RFC 9457 format, and additive evolution with a deprecation policy.

Webhook feeds are reliable only when events are recorded before delivery, signed, retried, logged, and replayable, and when the choice between thin and fat payloads is made deliberately. Events deserve the same rigor, with business names, versions, registered schemas, stated ordering and retention, and an owner. A short checklist at design review catches the problems that would otherwise burden every consumer.

## Exercises

1. **Audit an API you use.** Score a vendor API against the twelve rules in the table. Which missing rule has cost you the most effort?
2. **Write a problem-details body.** Design the error response for an order that fails because the requested quantity exceeds available stock. Choose the `type`, `code`, and extension fields.
3. **Design a webhook feed.** For an `order.shipped` event, decide thin or fat, define the signature scheme, the retry schedule, and the replay window. Justify each choice in one sentence.
4. **Sketch the contract.** Write an OpenAPI fragment for `GET /customers` with cursor paging, an `updatedSince` filter, and a documented 429. What would you add to let consumers detect deletions?



# Chapter 12. Data Formats, Mapping, and Transformation

Most integration code is not about transport. Moving a message from A to B is a solved problem, and platforms provide it ready-made. Most of the code, and most of the production incidents, are about turning *one system's idea of a record into another's*. A field that is a string in one system and a number in the other. A date written with a time zone in the source and without one in the target. A name that arrives with an accent and leaves as two garbled characters. A blank value that means "unknown" on one side and "erase this" on the other.

These are not exotic failures. They are the ordinary texture of integration work, and they respond well to discipline: know the formats you will meet, know the traps hidden in common values, structure the transformation as a pipeline that validates on the way in and on the way out, and write the mapping down as a reviewed document rather than leaving it buried in code. This chapter covers each of these, with code you can run.

> **In this chapter**
    * Recognize the data formats you will meet and the typical trap of each
    * Avoid the seven value traps: money, time, text, identifiers, nulls, enumerations, and units
    * Structure a transformation as a pipeline with validation on both sides and a quarantine
    * Validate and map records with typed models, and prove the mapping with golden-file tests
    * Write a mapping specification that business owners can review and sign
    * Decide between a canonical model and direct mapping

## The Formats You Will Meet

Whatever interaction style two systems use, they must agree on how to write the data down. the table lists the formats that cover almost every integration, with the schema language that describes each, and the trap you should expect.

**Table: Common data formats, their schemas, and their traps**
| Format | Typical home | Schema language | Strength | Trap |
|---|---|---|---|---|
| JSON | REST APIs, webhooks, events | JSON Schema, OpenAPI | Ubiquitous and readable | No native decimal or date type; some parsers lose precision on large numbers |
| XML | SOAP, B2B, enterprise suites | XSD | Strong typing, namespaces, mature tooling | Namespaces; external-entity attacks (disable them); verbosity |
| CSV | Batch exports, spreadsheets | None standard (document it) | Simple and compact | Delimiters and quotes inside data, encodings, lost leading zeros, locale number formats |
| Fixed-width | Mainframe and banking files | Copybooks, record layouts | Fast and compact | EBCDIC encoding, packed decimals, padding rules |
| Avro | Kafka, data platforms | Avro schema (JSON) | Compact; rich evolution rules | Needs a schema registry; readers need the writer's schema |
| Protobuf | gRPC, events | `.proto` files | Compact, typed, code generation | Field numbers must never be reused |
| Parquet | Lakes and warehouses | Embedded schema | Columnar; efficient for analytics | Unsuited to record-at-a-time exchange |
| EDI (X12, EDIFACT) | Supply-chain partners | Implementation guides | Universal in B2B | Partner-specific variants; segment terminators |
| HL7 v2, FHIR | Healthcare | Message and resource profiles | Industry standard | Local customizations (Z-segments, extensions) |
| SAP IDoc | SAP ERP | IDoc types and segments | Native to SAP processes | Status handling and custom extensions |

Two of these deserve a word of explanation, because they appear on nearly every project. **CSV** has no schema at all, so every producer and consumer carries its own assumptions about delimiters, quoting, encoding, headers, and number formats; the only defense is to *write the assumptions down*, and to validate every file against them on arrival. **JSON** looks self-describing but is deceptively loose: a number may be an integer or a floating-point value depending on the parser, a date is merely a string, and a missing field is indistinguishable from a null one unless the contract says otherwise.

## Values That Break Integrations

A handful of value types cause a disproportionate share of production defects. Learn them as a list, because each hides in plain sight.

**Table: Seven value traps and the rule for each**
| Value | The problem | The rule |
|---|---|---|
| Money and quantities | Binary floating point cannot represent 0.10 exactly, so sums drift | Use decimals (or integer minor units such as cents) end to end; carry the currency |
| Dates and times | Missing zones, daylight-saving changes, mixed formats, epoch seconds versus milliseconds | ISO 8601 with an offset; UTC internally; convert only at the edges; document precision |
| Text | Wrong encoding produces garbled characters; a byte-order mark corrupts the first column; emoji exceed old column limits | UTF-8 everywhere; strip BOMs; test with accented, non-Latin, and emoji characters |
| Identifiers | Leading zeros are lost when parsed as numbers; case differences | Treat identifiers as strings; define case rules |
| Null, empty, missing | Three different meanings: unknown, deliberately blank, not sent | Define, per field, whether missing means "leave unchanged" or "clear" |
| Booleans and enumerations | `Y`/`N`, `1`/`0`, `true`/`false`, localized labels | Map through governed code lists, never by guesswork |
| Units | Kilograms versus pounds, centimeters versus inches, net versus gross | Carry the unit with the value; convert explicitly |

### Money

The rule about floating point is not pedantry. In Python, `0.1 + 0.2` yields `0.30000000000000004`, `1.1 * 3` yields `3.3000000000000003`, and `4.35 * 100` yields `434.99999999999994`, so converting that price to whole cents with `int()` gives 434, not 435. Multiply by several million transactions and a finance team will find cents that do not reconcile. Use a decimal type, or store integer minor units (1999 for 19.99), choose one rounding rule (banker's rounding is common in finance), and write it in the mapping specification. Carry the currency with every amount: a number without a currency is a bug waiting for its second country.

### Time

Most time bugs come from *unlabeled* times. The string `2026-11-23T10:00:00` has no zone; the receiving system will assume a zone, and half the time it will be the wrong one. In the autumn when clocks go back, an hour of local times occurs twice, and a sync keyed on local time will either skip or duplicate it. The cure is simple to state: carry the offset (`2026-11-23T10:00:00+01:00` or `...Z` for UTC), store and compare in UTC, and convert to local time only for display. Also write down the *precision*: a source that rounds to the second and a target that stores milliseconds will disagree about equality. Chapter 14 shows how time errors break watermarks.

### Text

A customer named "Zoë Müller" arrives in a CSV encoded as Latin-1 and is read as UTF-8, producing "ZoÃ« MÃ¼ller", the classic sign of an encoding mismatch. Another file begins with an invisible byte-order mark that attaches itself to the first column name, so a lookup for `id` fails because the column is called `\ufeffid`. A product title with an emoji exceeds a database column sized for two-byte characters. Standardize on UTF-8 everywhere, strip byte-order marks when reading, size columns in characters, and include accented, non-Latin, and emoji text in your test data. A test file that contains only "John Smith" proves very little.

### Identifiers and Nulls

Identifiers that look like numbers are not numbers. A postal code `02134` or a customer number `00042` loses its leading zeros the moment a spreadsheet or a lazy parser treats it as an integer. Treat identifiers as strings in schemas and code, always.

The three meanings of blank deserve their own rule, because they decide whether an update destroys data. A *null* usually means "unknown," an *empty string* means "deliberately blank," and a *missing field* means "not sent." In a partial update, a missing field should normally leave the target unchanged, while a null or empty value may clear it. If the mapping does not state the rule per field, a sync that omits an optional field will wipe out data it was never meant to touch.

## The Transformation Pipeline

A transformation that does all its work in one function is hard to test and harder to debug. Structure it as a pipeline of small stages. the figure shows the shape.

*[Figure: A transformation pipeline. Validate on the way in and on the way out. Quarantine instead of guessing. Keep mapping tables as governed reference data.]*
Bytes are *received* and handed to the parser (arrow 1), which decodes them from their wire format into structures and passes them to the first validation against the source's rules (arrow 2). Valid records are *mapped and enriched* (arrow 3), using code lists and lookups held as reference data (arrow 7), then *validated again* against the target's rules (arrow 4), and finally *serialized and delivered* (arrow 5). A record that fails either validation is sent to **quarantine** (arrows 6 and 8) together with the reason and the original payload, so that a person can fix it and replay it, and the rest of the batch continues.

The second validation is the one teams skip. It catches the cases where your *own mapping* produces something the target will reject: a value that is valid in the source but too long for the target field, or a mapped code that is not in the target's list. Finding that before the call to the target means a precise local error instead of a vague remote one.

**Table: Kinds of transformation**
| Kind | Example |
|---|---|
| Structural mapping | Flatten a nested customer address into target fields; nest order lines under an order header |
| Value mapping (code lists) | Source status `3` becomes target status `Accepted` through a mapping table |
| Enrichment | Look up the cost center from the employee ID |
| Split and aggregate | One order file becomes many order messages; many line events become one daily summary |
| Normalization | Trim, case, phone and address formatting, unit conversion |
| Derivation | Compute `fullName`; derive the region from the country |
| Filtering | Only active products; only changes to fields the target owns |

### Tools for Transformation

You will meet several tools, and a good architect recognizes what each is best at. **Python with typed models** can do anything and can be tested; it is the choice for custom integrations. **SQL and dbt** are ideal for set-based transformation inside a warehouse. **jq and JSONata** reshape JSON concisely in scripts and in some integration platforms. **XSLT** transforms XML to XML or text, and still runs in many enterprise buses. **DataWeave** is the mapping language of the MuleSoft platform. **Visual mappers**, the drag-and-drop field mapping in platforms such as Boomi, Workato, SnapLogic, and Informatica, are quick to build and, without discipline, hard to review and version.

## Validate with Typed Models

In Python, the pydantic library lets you describe a record's shape and rules once and enforce them on every record. The module below validates an order, converts the timestamp to UTC, and maps the status through a governed code list. An unmapped status raises an error, which the caller sends to quarantine instead of guessing.

```python
"""Typed validation and mapping for an order, with a governed code list."""
from datetime import datetime, timezone
from decimal import Decimal
from pydantic import BaseModel, Field, field_validator

STATUS_MAP = {"1": "New", "2": "Accepted", "3": "Shipped", "9": "Cancelled"}

class OrderIn(BaseModel):
    id: str                                     # IDs are strings: keep zeros
    total: Decimal = Field(ge=0)                # never float for money
    currency: str = Field(pattern=r"^[A-Z]{3}$")
    status: str
    created_at: datetime

    @field_validator("created_at")
    @classmethod
    def must_have_zone(cls, v):
        if v.tzinfo is None:
            raise ValueError("timestamp must include a time zone")
        return v.astimezone(timezone.utc)

def to_target(o):
    if o.status not in STATUS_MAP:
        raise ValueError("unmapped status %r" % o.status)   # quarantine
    return {"externalId": o.id, "amount": str(o.total), "currency": o.currency,
            "status": STATUS_MAP[o.status], "createdAt": o.created_at.isoformat()}
```
Notice what the model enforces. The identifier is a `str`, so leading zeros survive. The total is a `Decimal` with a non-negative constraint, never a float. The currency is checked against a pattern. The validator *rejects* a timestamp without a time zone rather than assuming one, which turns a silent bug into a loud error on the first bad record. And `to_target` refuses to guess an unmapped status. The tests in the companion code exercise exactly these cases: a happy path that converts `10:00+01:00` to `09:00 UTC`, a missing time zone, a negative total, and an unknown status.

## The Mapping Specification: A Deliverable, Not a Side Effect

Write the mapping down as a reviewed document, a versioned spreadsheet or a YAML file, *before* building. It is how business owners approve meaning, how testers derive cases, and how support teams answer "why does this field say X?" two years later.

**Table: A mapping specification for the shop-to-ERP order**
| Target field | Source | Rule | If missing | Validation | Owner |
|---|---|---|---|---|---|
| `externalId` | `order.id` | Copy as a string | Reject | Unique per source | Integration team |
| `status` | `order.status` | Code list `ORDER_STATUS_v3` | Quarantine if unmapped | In the list | Order management |
| `amount` | `order.total` | Decimal, two places, half-even rounding | Reject | At least 0 | Finance |
| `createdAt` | `order.created_at` | Convert to UTC, ISO 8601 | Reject if no zone | Not in the future | Integration team |
| `customerName` | `customer.first` + `last` | Trim; join with a space | Leave unchanged if both empty | At most 120 characters | CRM team |

The **Owner** column is the one most specifications omit, and it matters most. Each rule encodes a business decision: how amounts are rounded is Finance's call, not the integrator's. Naming the owner makes the sign-off real and tells future maintainers whom to ask.

> **Golden-file tests**
    Keep pairs of real, anonymized source records and the expected target output in the repository, and run the mapping against them in every build. When a production record breaks the mapping, fix the mapping and add that record to the golden set. Over a year, the golden set becomes the most valuable test asset the integration owns, because every entry is a real failure that will never return unnoticed.

```python
import json, pathlib
import pytest
from mapping import OrderIn, to_target

CASES = sorted(pathlib.Path("golden").glob("*.in.json"))

@pytest.mark.parametrize("path", CASES, ids=lambda p: p.name)
def test_golden(path):
    source = json.loads(path.read_text())
    expected = json.loads(path.with_name(
        path.name.replace(".in.", ".out.")).read_text())
    assert to_target(OrderIn(**source)) == expected
```

## Canonical Model or Direct Mapping?

When many systems exchange the same entity, you face a choice. In **direct mapping**, each pair of systems has its own transformation. In a **canonical model**, every system maps to and from one shared definition, so a new system needs one mapping instead of one per existing system.

Direct mapping fits when there are only two or three systems, when different teams own each side, and when the entities differ in *meaning*, not only in shape. A canonical model fits when many systems exchange the same entity (customer, product, order), when a hub or event backbone exists, and when someone owns and governs the canonical definition. The cost of a canonical model is that committee: someone must maintain it, and every change requires agreement from every consumer. For that reason, adopt canonical models only for the few entities that are truly shared and stable, a policy Chapter 7 recommended and Chapter 29 develops.

## Summary

Most integration code turns one system's record into another's, and the failures hide in values, not transport. Know the formats, JSON, XML, CSV, fixed-width, Avro, Protobuf, Parquet, EDI, HL7, and IDoc, and the trap in each. Seven value traps cause most defects: money in floating point, unlabeled times, text encodings, identifiers parsed as numbers, the three meanings of blank, ungoverned enumerations, and unlabeled units.

Structure the transformation as a pipeline: receive, parse, validate in, map and enrich with governed code lists, validate out, deliver, with a quarantine that keeps the reason and the payload. Typed models enforce the rules in code, a mapping specification with named owners gets business sign-off, and golden-file tests turn every production failure into a permanent regression test. Choose a canonical model only for the few shared, stable entities that justify the governance it costs.

## Exercises

1. **Hunt for traps.** Take a real mapping in your organization and check each of the seven traps. Which is handled worst?
2. **Time zones.** Write a test that feeds your mapping a timestamp without a zone, one in `+01:00`, and one in UTC. What does each produce? What should each produce?
3. **Write a mapping spec.** Choose five fields from a real integration and write the table in the table, including the owner. Show it to the owner of one field and record their corrections.
4. **Start a golden set.** Collect five real, anonymized records, including the ugliest you can find, and create expected outputs. Run your mapping against them.



# Chapter 13. Authentication and Authorization

Authentication answers "who are you?" Authorization answers "what may you do?" Integrations usually authenticate as a *machine identity*, not as a person, and the design of that identity is half of the security posture of the whole integration. A shared administrator password pasted into a configuration file is the most common integration vulnerability in enterprises, and it is also the most common cause of outages: the password expires, someone rotates it, an account is locked, and the integration quietly stops.

This chapter teaches the schemes you will meet, the flows that matter for unattended jobs, and the code that handles tokens correctly. It then covers the discipline around credentials that separates a demo from a production integration: where secrets live, how identities are scoped, how they are rotated, and how you verify callers who contact *you*.

> **In this chapter**
    * Compare the authentication schemes you will meet, and choose one for a given situation
    * Explain the OAuth 2.0 client-credentials flow and implement a token provider that refreshes early and is safe across threads
    * Describe authorization code with PKCE, JWT bearer grants, and mutual TLS, and when each applies
    * Keep secrets out of code and configuration, and rotate them without downtime
    * Design service accounts with least privilege, one identity per integration
    * Verify signed webhooks, and diagnose the common authentication failures

## The Schemes You Will Meet

Eight schemes cover almost everything. the table compares them; read it as a ladder from convenient and weak to strong and demanding.

**Table: Authentication schemes compared**
| Scheme | How it works | Typical use | Strength | Weakness |
|---|---|---|---|---|
| Basic authentication | Username and password in an `Authorization: Basic` header, encoded but not encrypted | Older internal APIs and tools | Trivial to start | A long-lived secret; no scopes; must use TLS |
| API key | A static key in a header or query string | SaaS and simple partner APIs | Easy | Often over-privileged; leaks into logs if in the query string |
| Bearer token (opaque) | A token obtained elsewhere, sent in a header | Everywhere after login | Short-lived | Needs a token source and refresh logic |
| OAuth 2.0 client credentials | The application exchanges its client ID and secret for an access token | The default for service-to-service calls | Scoped, short-lived, rotatable | Token expiry must be handled |
| OAuth 2.0 authorization code with PKCE | A person signs in and the application receives a token on their behalf | User-facing apps; delegated access | Acts as the user | Refresh-token storage; unsuited to unattended jobs |
| OAuth 2.0 JWT bearer or private key | The application signs a JWT with its private key to obtain a token | Large SaaS platforms, cloud service accounts | No shared secret on the wire | Key management; clock skew |
| Mutual TLS (mTLS) | Both sides present certificates | Banking, regulated, internal meshes | Strong; can bind tokens to the client | Certificate lifecycle burden |
| HMAC signature | Each request or webhook is signed with a shared secret | Webhooks, cloud provider APIs | Tamper-evident | Canonicalization details are fiddly |

Single sign-on protocols such as SAML and OpenID Connect belong in the picture too, but they are for *people* using browsers; an unattended integration should never depend on one.

## OAuth 2.0 Client Credentials: The Workhorse

For service-to-service calls, the standard flow is OAuth 2.0 *client credentials*. the figure shows it.

*[Figure: OAuth 2.0 client credentials: the standard flow for unattended integrations.]*
The integration is registered with an authorization server, which gives it a **client ID** and a **client secret**, along with the scopes it may request. When it needs to call an API, it sends those two values to the authorization server's token endpoint (step 1) and receives an **access token** and its lifetime (step 2). It then calls the target API with the token in an `Authorization: Bearer` header (step 3), and the API validates the token and responds (step 4).

The benefits over a password are significant. The token is *short-lived*, usually minutes to an hour, so a leaked token expires on its own. It is *scoped*: it grants only the permissions the client was registered for. And the long-lived secret is sent only to the token endpoint, never to every API. Access tokens may live for minutes or for hours depending on the provider and the tenant configuration, and some vendors support different schemes on different endpoints, so never assume a lifetime: read `expires_in`, refresh early, handle one surprise 401, and confirm which methods each endpoint you need supports.

### A Token Provider That Is Correct

The code that obtains and caches tokens is small and surprisingly easy to get wrong. The version below, from the book's companion code, handles the three requirements: it refreshes *before* expiry, it is safe when many threads ask at once, and it can be told to forget a token that the server rejected.

```python
"""OAuth 2.0 client-credentials token cache with early refresh."""
import threading, time
import requests

class TokenProvider:
    def __init__(self, token_url, client_id, client_secret, leeway=60):
        self.url, self.leeway = token_url, leeway
        self.cid, self.secret = client_id, client_secret
        self._token, self._expires = None, 0.0
        self._lock = threading.Lock()
        self.fetches = 0

    def get(self):
        with self._lock:                      # one thread refreshes; others wait
            if self._token is None or time.time() > self._expires - self.leeway:
                self._refresh()
            return self._token

    def invalidate(self):
        with self._lock:
            self._token = None

    def _refresh(self):
        r = requests.post(self.url, timeout=(5, 15), data={
            "grant_type": "client_credentials",
            "client_id": self.cid, "client_secret": self.secret})
        r.raise_for_status()
        body = r.json()
        self._token = body["access_token"]
        self._expires = time.time() + float(body.get("expires_in", 300))
        self.fetches += 1
```
Study the details. The `get` method holds a lock, so if twenty workers all discover an expired token at once, one of them refreshes and the others wait, instead of twenty simultaneous token requests, which some providers treat as abuse. The `leeway` of 60 seconds means that a token is renewed a minute before it expires, so no request is ever sent with a token that dies in flight. And `invalidate` lets the HTTP client, on a 401 response, discard the token and force one refresh (Chapter 14 shows the client side). The lab server in Appendix E implements the other end of this exchange, so you can run the whole flow, including a revoked token, on your own machine.

## Authorization Code with PKCE

When an application acts on behalf of a *person*, for example a dashboard that reads the user's calendar, the flow changes. The user is redirected to the identity provider, signs in, and consents, and the application receives a short-lived **authorization code** that it exchanges for a token. **PKCE** (Proof Key for Code Exchange, pronounced "pixie") adds a one-time secret to the exchange, so that an intercepted code is useless to an attacker. It is the recommended pattern for browser and mobile applications.

For unattended integrations this flow is usually wrong, because it ties the integration's authority to one person and to a refresh token that must be stored and renewed. A job that runs on a *user's* delegated grant stops the day the user leaves the company, changes role, or has their password reset. Use client credentials, or a signed JWT, for jobs; reserve the authorization code flow for software with a human at the keyboard.

## JWT Bearer and Mutual TLS

Two stronger options remove the shared secret entirely.

In the **JWT bearer** (or private-key) grant, the application holds a private key. To obtain a token it builds a small JSON Web Token, signs it with that key, and presents it to the token endpoint; the server, which holds the matching public key, verifies the signature. The secret never crosses the network, and the key can be rotated by publishing a new public key. The costs are key management and, because the token carries timestamps, sensitivity to clock skew: a server whose clock is five minutes wrong will reject every assertion.

In **mutual TLS**, both parties present certificates during the connection handshake, so the server knows exactly which client is calling before a single byte of the request is read. It is common in banking and other regulated settings and can be combined with tokens that are *bound* to the client certificate, so that a stolen token is useless without the matching key. Its cost is the certificate lifecycle: every certificate expires, and an expiry is an outage unless someone has automated renewal and alerting.

## Keeping Secrets Out of Code

A secret that lives in source control, in a configuration file on a shared drive, or in a container image will eventually leak. The rules are simple to state and surprisingly rarely followed.

* **Keep secrets in a vault.** A secrets manager (HashiCorp Vault, AWS Secrets Manager, Azure Key Vault, Google Secret Manager) stores them encrypted, logs every access, and can rotate them. The integration fetches the secret at start-up using its own workload identity, not another secret.
* **Pass references, not values.** Configuration should say `secret_ref: vault:kv/integrations/orders`, resolved at start-up, or inject the value into the environment at launch.
* **Never log a secret.** Scrub tokens and passwords from logs, error messages, and traces, including debug output and exception text.
* **Use workload identity where possible.** Cloud platforms can give a running service an identity (a managed identity, an IAM role) so it can call the vault and other services without any stored credential at all.
* **Scan for leaks.** Run a secret scanner in the delivery pipeline and on the repository's history, because a secret committed once and deleted is still in history.

> **A demo configuration is not a production configuration**
    A configuration file with `"username": "svc-int"` and `"password": "Pssw0rd!"` is acceptable in a tutorial and unacceptable in production. When you receive an integration package or example that stores credentials in plain text, treat the file as a *template* and replace the values with references before it goes anywhere near a real environment.

## Service Accounts Done Properly

The identity the integration runs as deserves the same care as the code.

* **One identity per integration**, never a shared administrator. Audit trails then say which job did what, and a compromised credential can be revoked without stopping everything else.
* **Least privilege.** Grant only the permissions the flow needs. A read-only synchronization should hold read-only rights. Where a platform filters what an account can see, scope deliberately, and test with the integration's real permissions.
* **Exclude the account from your own change feed.** Bidirectional integrations filter out changes made by their own user to avoid echo loops (Chapter 8). This works only if the integration has a dedicated identity.
* **A rotation plan.** Document who rotates the secret, how often, and how the running job picks up the new value without a redeploy. Overlapping validity (two valid secrets at once) makes rotation safe.
* **A break-glass procedure.** What happens when the account is locked or its password expires on a Sunday? Who can restore it, and how is that action recorded?

## Verifying Webhooks

When the *source* calls you, the roles reverse: you must verify the caller. A webhook endpoint is a public door, and anyone can post to it. The standard defense is an HMAC signature: the sender computes a keyed hash of a timestamp and the request body using a secret you share, and sends it in a header. You recompute the hash and compare. A timestamp window rejects replays of captured requests.

```python
"""Verify signed webhooks and drop duplicates."""
import hashlib, hmac, sqlite3, time

def sign(secret, timestamp, body):
    msg = ("%s." % timestamp).encode() + body
    return hmac.new(secret.encode(), msg, hashlib.sha256).hexdigest()

def verify(secret, body, signature, timestamp, tolerance=300, now=None):
    """True only if the signature matches and the timestamp is recent."""
    now = time.time() if now is None else now
    try:
        if abs(now - float(timestamp)) > tolerance:
            return False                       # too old (replay) or too far ahead
    except (TypeError, ValueError):
        return False
    return hmac.compare_digest(sign(secret, timestamp, body), signature or "")

class Ledger:
    """Remember event IDs so a redelivered event is processed once."""
    def __init__(self, path=":memory:"):
        self.db = sqlite3.connect(path)
        self.db.execute("CREATE TABLE IF NOT EXISTS seen (id TEXT PRIMARY KEY)")

    def first_time(self, event_id):
        try:
            with self.db:
                self.db.execute("INSERT INTO seen (id) VALUES (?)", (event_id,))
            return True
        except sqlite3.IntegrityError:
            return False
```
The `verify` function rejects a request whose timestamp is more than five minutes from now, which stops an attacker from replaying a captured message later. It uses `hmac.compare_digest` for a *constant-time* comparison, because an ordinary string comparison returns earlier when the first byte differs, leaking information about the correct signature to a patient attacker. And it never raises on malformed input; it simply returns `False`. The `Ledger` class addresses the other half of the problem, the sender's legitimate retries: it records each event ID and answers whether this is the first time. Signature schemes vary by vendor (what exactly is signed, how the header is formatted), so follow the vendor's documentation, but keep the structure: verify, reject stale, deduplicate.

## Authorization: What the Caller May Do

Authentication establishes identity; **authorization** decides what that identity may do, and most real breaches exploit authorization, not authentication. The relevant ideas for integrators are these.

**Scopes** limit what a token may be used for: `read:orders` but not `write:orders`. Request the narrowest scope that works. **Object-level authorization** checks that the caller may access *this particular record*, not merely the type of record; an API that returns any order when given its ID, regardless of whose it is, has a classic and serious flaw (Chapter 27 covers it). **Permission filtering** means that an integration user may see only some of the data: fields hidden by role, records outside its tenant. This produces a subtle failure, where the integration reads *less* than the documentation promises, with no error. Always test with the integration's real permissions, and compare counts with what an administrator sees.

## Troubleshooting Authentication

Authentication failures follow a few patterns. the table lists the most common, with likely causes and fixes.

**Table: Authentication symptoms, causes, and fixes**
| Symptom | Likely cause | Fix |
|---|---|---|
| 401 right after obtaining a token | Wrong audience or scope; a token for the wrong environment | Decode the token (a JWT is readable) and compare `aud`, `scope`, and `iss` |
| 401 after exactly N minutes | The token expired and nothing refreshed it | Refresh before expiry; retry once on 401 |
| 403 on some endpoints only | A missing scope or role | Compare the service account's role with the endpoint's documented permission |
| Works locally, 401 from the server | A corporate proxy rewrites headers; clock skew breaks a JWT assertion | Test with `curl` from the server; synchronize time with NTP |
| TLS handshake errors | Corporate TLS inspection with a private certificate authority | Add the authority to the runtime's trust store; never disable verification |
| Intermittent 401 with parallel workers | Each worker refreshes its own token, invalidating the others' | Share one token provider with a lock |

## Choosing a Scheme

When the vendor gives you a choice, a short decision procedure helps. For a *person*, use single sign-on with the authorization code flow and PKCE. For an unattended *job*, prefer OAuth 2.0 client credentials with short tokens and the secret in a vault; if that is unavailable, a JWT bearer grant or mutual TLS; then a scoped, rotated API key; and as a last resort, basic authentication over TLS with one service account and a vault. For an incoming *webhook*, an HMAC signature with a timestamp plus deduplication by event ID. Whatever you choose, record it in the reconnaissance sheet, and write down who approves the account, because that approval is often the longest wait of the whole project.

## Summary

Integrations authenticate as machine identities, and the design of that identity is half the security of the integration. Basic authentication and API keys are easy and weak; OAuth 2.0 client credentials is the default for service-to-service calls; JWT bearer grants and mutual TLS remove the shared secret at the cost of key and certificate management; authorization code with PKCE is for people, not jobs.

A correct token provider refreshes before expiry, holds a lock so parallel workers refresh once, and discards a rejected token exactly once. Secrets live in a vault and are passed by reference; each integration has its own least-privilege service account, a rotation plan, and a break-glass procedure. Incoming webhooks are verified by signature and timestamp with a constant-time comparison and deduplicated by event ID. And because breaches exploit authorization more often than authentication, test with the integration's real permissions and the narrowest scopes that work.

## Exercises

1. **Run the flow.** Start the lab server with authentication enabled (omit `--no-auth`), request a token with `curl`, and use it. Then restart the server and observe the 401. Which line of your client handles it?
2. **Audit a configuration.** Find a configuration file in your organization that stores a credential. Replace it with a reference, and describe how the running job would obtain the value.
3. **Break the webhook.** Using `webhook.py`, send a request with a valid signature but a timestamp one hour old, then one with a tampered body. Confirm both are rejected.
4. **Plan a rotation.** Write the steps to rotate an integration's client secret with zero downtime. Where does the overlap period appear?



# Chapter 14. Python Clients That Survive Production

Python with the `requests` library is the most common way to build REST integrations, and for good reasons: it is quick to write, easy to read, and every team has someone who knows it. The difference between a *script* and an *integration* is a handful of habits. A script runs once on a developer's laptop, against a healthy API, and its author watches it finish. An integration runs unattended at 03:00, against an API that is occasionally slow, occasionally down, and sometimes returns surprises, and nobody watches it at all until something goes wrong.

This chapter teaches the habits that make the difference, and shows them in working code from the book's companion repository: a hardened HTTP client, a paginating reader, a watermark poller with atomic checkpoints, a rate limiter, and a run loop that quarantines bad data. Every listing here is exercised by automated tests, including tests that kill the process halfway through a run, so you can trust the behavior and adapt the code to your own work.

> **In this chapter**
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

```python
"""A hardened HTTP client: timeouts, bounded retries, backoff with jitter,
Retry-After, and cursor pagination."""
import random, time
from email.utils import parsedate_to_datetime
import requests

RETRY_STATUS = {429, 500, 502, 503, 504}
SAFE_METHODS = {"GET", "HEAD", "PUT", "DELETE", "OPTIONS"}
TIMEOUT = (5, 30)                       # (connect, read) seconds

class ApiError(Exception):
    def __init__(self, status, body, url):
        super().__init__("%s from %s: %s" % (status, url, body[:200]))
        self.status, self.body, self.url = status, body, url

def build_session(token_provider=None):
    s = requests.Session()
    s.headers["User-Agent"] = "orders-sync/1.0"
    s.token_provider = token_provider
    return s

def parse_retry_after(value):
    """Seconds to wait, from either '3' or an HTTP date; None if absent."""
    if not value:
        return None
    if value.isdigit():
        return float(value)
    try:
        when = parsedate_to_datetime(value)
        return max(0.0, when.timestamp() - time.time())
    except (TypeError, ValueError):
        return None

def backoff_delay(attempt, base=0.5, cap=30.0):
    """Full jitter: a random wait between 0 and min(cap, base * 2^attempt)."""
    return random.uniform(0, min(cap, base * 2 ** attempt))

def request(session, method, url, *, max_attempts=6, sleep=time.sleep, **kw):
    kw.setdefault("timeout", TIMEOUT)
    headers = dict(kw.pop("headers", {}) or {})
    retryable = method.upper() in SAFE_METHODS or "Idempotency-Key" in headers
    refreshed = False
    for attempt in range(max_attempts):
        if session.token_provider:
            headers["Authorization"] = "Bearer " + session.token_provider.get()
        try:
            r = session.request(method, url, headers=headers, **kw)
        except (requests.ConnectionError, requests.Timeout):
            if not retryable or attempt == max_attempts - 1:
                raise
            sleep(backoff_delay(attempt))
            continue
        if r.status_code == 401 and session.token_provider and not refreshed:
            session.token_provider.invalidate()      # one refresh, then give up
            refreshed = True
            continue
        last = attempt == max_attempts - 1
        if r.status_code in RETRY_STATUS and retryable and not last:
            wait = parse_retry_after(r.headers.get("Retry-After"))
            sleep(wait if wait is not None else backoff_delay(attempt))
            continue
        if r.status_code >= 400:
            raise ApiError(r.status_code, r.text, url)
        return r
    raise RuntimeError("unreachable")

def iter_records(session, url, params=None, limit=100, max_pages=10_000):
    """Yield every record from a cursor-paginated endpoint."""
    params = dict(params or {}, limit=limit)
    for _ in range(max_pages):                 # guard against endless loops
        body = request(session, "GET", url, params=params).json()
        yield from body["results"]
        cursor = body.get("nextCursor")
        if not cursor:
            return
        params = {"cursor": cursor, "limit": limit}   # cursor replaces filters
    raise RuntimeError("pagination did not finish in %d pages" % max_pages)
```
### What Gets Retried, and What Does Not

The first design decision is in two constants at the top. `RETRY_STATUS` lists the status codes that usually mean "try again later": 429 (too many requests) and the 5xx server errors. `SAFE_METHODS` lists the HTTP methods that are idempotent: `GET`, `HEAD`, `PUT`, `DELETE`, and `OPTIONS`. In `request`, a call is `retryable` only if its method is in that list *or* the caller supplied an `Idempotency-Key` header. A plain `POST` is therefore never retried, which is the correct default: a failure leaves you not knowing whether the order was created, and the safe action is to look rather than to repeat. The companion tests prove it: a `POST` against a server that always fails is attempted exactly once, while the same request with an idempotency key is retried and replayed safely.

Network errors, such as a connection reset or a timeout, follow the same rule. If the method is not retryable, the exception propagates immediately; if it is, the client waits and tries again, up to `max_attempts`.

### Backoff with Full Jitter

When a retry is warranted, how long should the client wait? Waiting a fixed second is better than nothing, and waiting longer after each failure is better still: that is **exponential backoff**, in which the delay doubles each time up to a cap. But exponential backoff alone has a flaw. If a hundred clients all hit an outage at the same moment, they all retry at the same moments, in synchronized waves, which can keep a recovering server down. the figure shows the effect.

*[Figure: backoff-jitter]*
The fix is **jitter**: randomness. The function `backoff_delay` implements the "full jitter" strategy, which waits a random time between zero and the exponential ceiling: `random.uniform(0, min(cap, base * 2 ** attempt))`. The load spreads out, and the server sees a trickle instead of a wave. With `base=0.5` and `cap=30`, the ceilings are 0.5, 1, 2, 4, 8, 16, and then 30 seconds.

### Honoring Retry-After

Backoff is a guess; `Retry-After` is the server telling you the answer. When a 429 or 503 response carries that header, the client uses it instead of its own computation. The header comes in two forms, a number of seconds (`Retry-After: 3`) or an HTTP date, and `parse_retry_after` handles both, returning `None` for anything it cannot understand, in which case the client falls back to backoff. The companion test points the client at a server limited to three requests per second and verifies that every wait the client chooses equals the one second the server demanded.

### One Re-Authentication

The `refreshed` flag implements the rule from Chapter 8: on a 401, discard the cached token, fetch a new one, and retry *once*. A second 401 is raised as an error. Without the flag, a revoked credential would produce an endless loop of token requests, and a loop of failed logins can lock the account.

### Raising Meaningful Errors

Finally, any status of 400 or above that is not retried becomes an `ApiError` carrying the status, the first 200 characters of the body, and the URL. That small convenience matters at 03:00: the log line says "422 from https://…/orders: field quantity must be between 1 and 99," and the cause is visible without a debugger.

## Reading Large Collections with Generators

The `iter_records` function at the bottom of `client.py` reads a cursor-paginated collection as a stream. A *generator* produces one record at a time and pauses between requests, so memory use stays flat whether the collection holds a hundred records or a hundred million. Three details deserve attention. After the first page, the parameters become only `cursor` and `limit`, because, as Chapter 10 warned, many APIs reject a request that mixes a cursor with other filters. The loop is bounded by `max_pages`, so a server bug that returns the same cursor forever causes an error instead of an infinite loop. And because the function is a generator, the caller can stop early and resume later by saving the cursor.

```python
for order in iter_records(session, BASE + "/orders", limit=200):
    handle(order)          # one record at a time; memory stays flat
```

## Watermarks and Checkpoints

The most common synchronization job reads "everything that changed since last time." Two ideas make it reliable: a **watermark** that records how far you have read, and an **overlap** that guards against late-committed rows. the figure shows the failure that overlap prevents.

*[Figure: watermark-overlap-timeline]*
A row can be *modified* at 09:59:58 but only become *visible* to queries at 10:00:03, because its transaction committed late. If the job's first run ended at 10:00:00 and stored that as the watermark, the second run asks for changes since 10:00:00, and the row, whose timestamp is earlier, is never returned. It is missed forever, with no error anywhere. The remedy is to reach back: each run asks for changes since the watermark *minus a safety margin*, here two minutes. Re-reading a few rows is harmless if the writes are idempotent, and the late row is caught.

```python
"""Incremental sync: watermark, overlap window, atomic checkpoints."""
import json, os, tempfile
from datetime import datetime, timedelta, timezone
from client import iter_records

FMT = "%Y-%m-%dT%H:%M:%S.%fZ"

def load_watermark(path, default="1970-01-01T00:00:00.000000Z"):
    try:
        with open(path) as f:
            return json.load(f)["watermark"]
    except FileNotFoundError:
        return default

def save_watermark(path, value):
    """Write to a temp file, then rename: a crash can never leave half a file."""
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(os.path.abspath(path)))
    with os.fdopen(fd, "w") as f:
        json.dump({"watermark": value}, f)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)

def run_once(session, base_url, state_path, upsert, overlap_seconds=120):
    """Fetch records changed since the last watermark (minus an overlap) and
    upsert them. Returns the number of records processed."""
    wm = load_watermark(state_path)
    start = datetime.strptime(wm, FMT).replace(tzinfo=timezone.utc)
    since = (start - timedelta(seconds=overlap_seconds)).strftime(FMT)
    newest, count = wm, 0
    url = base_url + "/orders"
    for rec in iter_records(session, url, {"updatedSince": since}):
        upsert(rec)               # must be idempotent: overlap repeats rows
        newest = max(newest, rec["updatedAt"])
        count += 1
    save_watermark(state_path, newest)   # commit only after the batch succeeded
    return count
```
The module implements the whole discipline in about thirty lines. `run_once` loads the watermark, subtracts the overlap, reads every changed record through the paginating generator, upserts each (the callback `upsert` must be idempotent, because the overlap repeats rows), and tracks the newest `updatedAt` it saw. Only after the loop completes does it save the new watermark, with `save_watermark`.

That function is worth reading closely. It writes the value to a temporary file in the same directory, flushes it, forces it to disk with `fsync`, and then calls `os.replace`, which atomically swaps the new file in. A crash at any instant leaves either the old watermark or the new one, never a half-written file. And because the watermark is saved *last*, a crash in the middle of a batch leaves it unchanged: the next run starts from the same point, re-reads the same records, and the upserts make the repetition harmless. The companion test proves exactly this. It makes the upsert callback raise an error halfway through, asserts that the watermark did not move, and then verifies that a following run captures every change.

> **Why this matters**
    The two rules, *move the watermark last* and *make the writes idempotent*, convert "at least once" processing into "effectively once" results. The overlap and the re-reads are not a defect to be eliminated; they are the price of safety, and idempotency is how you pay it.

Use the **source's timestamps**, never your own clock, to compute the watermark. Your clock and the server's differ by seconds or minutes, and any difference in the wrong direction skips rows. Store the watermark in UTC, with the precision the source provides.

## Staying Within the Rate Limit

An integration that reads or writes fast enough will meet the API's rate limit. Backoff on 429 is the safety net, but a well-behaved client avoids hitting the limit in the first place by *pacing itself*. Start with arithmetic. If the API allows 300 requests per minute, that is five per second; plan for four, which leaves 20 percent headroom for other integrations sharing the same limit. A job that must make 36,000 calls therefore needs at least 9,000 seconds, two and a half hours, and no amount of parallelism will change that. If the window is shorter, look for bulk endpoints.

The standard pacing tool is the **token bucket**. Imagine a bucket that holds up to `burst` tokens and is refilled at `rate` tokens per second. Each request takes one token; if the bucket is empty, the caller waits until a token arrives.

```python
"""A token bucket: allow `rate` calls per second, with bursts up to `burst`."""
import threading, time

class TokenBucket:
    def __init__(self, rate, burst=None, clock=time.monotonic, sleep=time.sleep):
        self.rate = float(rate)
        self.capacity = float(burst or rate)
        self.tokens = self.capacity
        self.clock, self.sleep = clock, sleep
        self.updated = clock()
        self.lock = threading.Lock()

    def acquire(self, n=1):
        """Block until n tokens are available, then take them."""
        while True:
            with self.lock:
                now = self.clock()
                gained = (now - self.updated) * self.rate
                self.tokens = min(self.capacity, self.tokens + gained)
                self.updated = now
                if self.tokens >= n:
                    self.tokens -= n
                    return
                wait = (n - self.tokens) / self.rate
            self.sleep(wait)             # sleep outside the lock
```
The `acquire` method computes how many tokens have accumulated since the last call, takes one if available, and otherwise sleeps for exactly the time needed, *outside* the lock so that other threads are not blocked. Injecting the clock and sleep function, as the constructor does, lets the test run in virtual time: with a rate of two per second and a burst of two, six acquisitions complete after exactly two seconds of waiting.

### Bounded Concurrency

Concurrency can speed up an integration that waits on the network, but only within limits. Use a small, fixed pool of workers, such as four, with a *shared* token bucket so that the pool as a whole respects the API's budget, and a shared token provider (Chapter 13) so that they do not each refresh credentials. A pool of 50 threads hitting a vendor with a limit of five per second does not finish sooner; it produces 429s, retries, and a lot of heat. Concurrency is also a risk to *ordering*: if two records for the same entity are processed in parallel, the older update may land last. Partition the work by entity key so that each key is handled by one worker at a time.

## Quarantine Instead of Crash

Habit seven is about proportion. A single malformed record should not stop a million good ones, and a systemic failure should not be mistaken for a bad record. The run loop below makes the distinction explicit.

```python
"""Process records one by one: quarantine bad data, fail loudly on the rest."""
import json, logging, uuid

log = logging.getLogger("sync")

def process(records, upsert, quarantine_path, run_id=None):
    """Returns run counts. ValueError means bad data: park it and go on.
    Any other exception (network, bug) stops the run: do not hide it."""
    run_id = run_id or uuid.uuid4().hex[:8]
    counts = {"run_id": run_id, "read": 0, "written": 0, "quarantined": 0}
    with open(quarantine_path, "a") as parked:
        for rec in records:
            counts["read"] += 1
            try:
                upsert(rec)
                counts["written"] += 1
            except ValueError as err:
                counts["quarantined"] += 1
                parked.write(json.dumps({"run_id": run_id, "reason": str(err),
                                         "record": rec}) + "\n")
                log.warning("quarantined id=%s run=%s reason=%s",
                            rec.get("id"), run_id, err)
    log.info("run summary %s", json.dumps(counts))
    return counts
```
The convention is simple. If processing a record raises `ValueError`, the *data* is at fault, so the record is written to a quarantine file with its reason and the run continues. Any other exception, such as a network failure after retries or a bug in the mapping, propagates and stops the run, because continuing would hide the problem. At the end, the loop logs a **run summary**: records read, written, and quarantined, keyed by a run ID. That summary is the most useful single line an integration emits. Alert if the quarantine count rises above a threshold, such as one percent, and alert if a scheduled run produces no summary at all, a *heartbeat* check that catches the integration that silently stopped.

## Logging You Can Use at 3 A.M.

When an integration fails, the log is the only witness. Structured logs, in which every line is a set of named fields rather than a sentence, can be searched and counted.

```json
{"ts":"2026-11-23T09:14:07.311Z","level":"WARN","service":"orders-sync",
 "run_id":"r-20261123-0905","entity":"order","entity_id":"A1043",
 "action":"create","target":"erp","outcome":"quarantined",
 "reason":"unmapped sku TENT-9X","duration_ms":182}
```

Every line carries a run ID, so one search retrieves a whole run; an entity ID, so one search retrieves one order's history; and an outcome and reason as fields, so a dashboard can count them. It carries no payloads containing personal data, and never a token or a secret. Chapter 26 extends the idea to traces that follow a transaction across systems.

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

Claims such as "it handles restarts" are opinions. Tests make them facts, and the companion test suite for this chapter's code checks, among other things, that a poller killed mid-batch does not advance its watermark and loses nothing on the next run; that the client honors the server's `Retry-After` exactly; that a `POST` without an idempotency key is attempted once; that a flaky server returning 503 half the time still yields every record; that a revoked token triggers exactly one refresh; and that a run containing bad records quarantines them and finishes. Chapter 16 explains how to build such a suite for your own integrations, including a failure-injection checklist.

## Summary

The difference between a script and an integration is seven habits: always set timeouts, retry only what is safe, back off with jitter, page with generators, make writes idempotent, log with correlation, and fail loudly while parking bad records gently. A hardened client retries only idempotent methods or requests with an idempotency key, honors `Retry-After` before computing its own full-jitter backoff, refreshes a rejected token exactly once, and raises errors that say what failed.

Incremental sync depends on a watermark that moves only after the whole batch succeeds, written atomically, plus an overlap window that guards against late-committed rows and idempotent upserts that make the repetition harmless. A token bucket paces requests below the API's limit, concurrency stays bounded and partitioned by key, and a run loop quarantines bad data, stops on systemic errors, and emits a run summary. A conventional project layout with environment configuration, pinned dependencies, and an in-repository runbook makes the whole thing maintainable by someone else.

## Exercises

1. **Watch the retries.** Start the lab server with `--flaky 0.3`, run the client against it, and print each wait the client chooses. Do the waits grow? Do they ever exceed the cap?
2. **Prove atomicity.** Modify `save_watermark` to write the file directly instead of using a temporary file and `os.replace`. Describe a crash timing that would corrupt it, and why the original cannot be corrupted that way.
3. **Size a job.** An API allows 600 requests per minute, shared among three integrations. Your job must update 90,000 records, one call each. How long will it take at a fair share of the budget, and what would you ask the vendor for?
4. **Add a metric.** Extend `process` to count records that took more than one second, and include that count in the run summary. What alert would you attach to it?



# Chapter 15. Synchronization Design

Moving bytes is easy. Deciding what counts as *the same thing* in two systems, what to do when a record disappears, and how to stop two systems from overwriting each other is where integrations are won or lost. These are questions about meaning and state, not transport, and the code to answer them is short once the design is right and endless if it is not.

This chapter covers the decisions at the heart of any synchronization: how records are matched across systems, how to choose between full and incremental reads, how to detect deletes (the forgotten half), how to keep field mappings in data rather than code, how bidirectional sync fails and how to prevent it, and how a reconciliation job turns an integration from "probably correct" into "provably correct." It ends with the special case of the initial load.

> **In this chapter**
    * Choose an identity strategy, and explain why storing the foreign ID beats matching by name
    * Pick full, incremental, or hybrid synchronization for a given source
    * Detect and handle deletes safely, with a guard against deleting too much
    * Keep mappings and status translations in configuration that owners can review
    * Name the four problems of bidirectional sync, and prevent each
    * Build a reconciliation job and use it as the integration's safety net
    * Plan an initial load that does not corrupt the target

## Identity: How Do You Know It Is the Same Record?

Every synchronization begins with an unglamorous question. A record arrives from the shop. Does the ERP already have it? To answer, you need a rule that decides whether two records, in two systems, are the same thing. the table compares the common strategies.

**Table: Identity strategies compared**
| Strategy | How it works | Strength | Weakness | Example |
|---|---|---|---|---|
| Store the foreign ID | The target keeps the source's ID in a dedicated field | Stable under renames; reliable | Needs a field on the target | The ERP's customer-reference field holds the shop's order number |
| Natural key | Match by a business key (a code, a number, a full name) | No extra field needed | Breaks when the key changes | Matching products by SKU |
| Name match | Match by display name | Works for a first run | Renames create duplicates; collisions | Searching for a ticket by its title |
| Walk related records | Follow existing relationships to find the external ID | Uses data already present | Longer paths, more calls; fragile if links are incomplete | Table to column to the BI tool's identifier |

The rule is to **always prefer a stored foreign ID**. Name matching is acceptable only as a bootstrap for the very first run, and you must define what happens when two records share a name. Renames are the leading source of duplicates in production: a customer renames a company, the name-matching sync no longer finds it, and creates a second record, which then diverges from the first for years.

Where a system gives you no field to store the foreign ID, look for an alternative: a custom attribute, a reference or external-ID field, or a separate **crosswalk table** in the integration's own database mapping source IDs to target IDs. A crosswalk is unglamorous and robust, and it also gives you a place to record when each link was created and last verified.

## Full or Incremental?

The second decision is how much to read each time. the table lays out the options.

**Table: Full, incremental, and hybrid synchronization**
| Approach | When | Mechanics | Gotchas |
|---|---|---|---|
| Full snapshot, replace | Small data; reference data | Read everything, upsert everything, delete what is missing | Delete only if the read *completed*; guard with a threshold (abort if more than 5 to 20 percent would be removed) |
| Incremental by timestamp | The source has a reliable modified time | A watermark with overlap (Chapter 14) | Time-zone mix-ups; late commits; no deletes |
| Incremental by change feed | The source exposes an audit or event log | Consume changes in order; checkpoint the position | Feed retention is limited; missing a window needs a full resync |
| Hybrid | Most enterprise cases | Frequent incremental runs plus a nightly or weekly full reconciliation | The reconciliation must not fight the incremental run: schedule them and lock |

In practice, almost every durable integration is a **hybrid**: a frequent incremental job provides freshness, and a slower full comparison catches whatever the incremental job missed, whether because of a late commit, a dropped event, or a delete. The incremental job is the fast path; the reconciliation is the repair path. The two should share the same upsert code so that they cannot disagree about what a correct record looks like.

## Deletes: The Forgotten Half

Most designs think carefully about creates and updates and forget deletes, because a deleted record produces no data to react to. It simply stops appearing. The result is a target that grows stale, accumulating records that no longer exist at the source: customers who left, products that were discontinued, orders that were cancelled.

Four situations cover most cases.

* **The source has soft delete.** Records are flagged (status `archived`, a `deletedAt` timestamp) rather than removed. Synchronize the flag, and map it to a target status such as `Retired` instead of hard-deleting; you keep the history and avoid destructive actions.
* **The source has a delete feed or events.** Process them, but *also* reconcile periodically, because feeds drop events.
* **The source offers neither.** Run an ID-list comparison. Fetch only the identifiers (cheap), compare with what you hold, and handle the difference. This is the *snapshot and diff* pattern.
* **Whatever the mechanism, install a safety valve.** Never delete more than a threshold in a single run without human approval.

The safety valve deserves the emphasis. A comparison that deletes "everything in the target that is not in the source" is only as good as its read of the source. If the source API returns an empty page because of an outage, a misconfigured filter, or a permissions change, an unguarded job concludes that every record has been deleted, and deletes them. The guard below, from the companion code, makes the job refuse.

```python
"""Compare two systems and guard against deleting too much."""

def compare(src, tgt):
    """src and tgt map record id -> checksum. Returns the differences."""
    missing = sorted(set(src) - set(tgt))
    orphans = sorted(set(tgt) - set(src))
    changed = sorted(k for k in set(src) & set(tgt) if src[k] != tgt[k])
    return {"count_src": len(src), "count_tgt": len(tgt),
            "missing_in_target": missing, "orphans_in_target": orphans,
            "changed": changed}

def deletion_guard(report, max_fraction=0.05):
    """Return the ids that may be deleted, or refuse if there are too many."""
    n = len(report["orphans_in_target"])
    total = report["count_tgt"]
    if total and n / total > max_fraction:
        raise RuntimeError("refusing to delete %d of %d records" % (n, total))
    return report["orphans_in_target"]
```
The `compare` function takes two dictionaries mapping record IDs to checksums and returns four things: how many records each side has, which IDs are missing from the target, which target IDs are orphans, and which records exist on both sides with different checksums. The `deletion_guard` raises an error if the orphans exceed five percent of the target; with a real, small number of orphans, it returns the list. A job that deletes only after passing the guard cannot turn a transient read failure into a disaster.

## Field Mapping: Make It Data, Not Code

Hard-coded mappings force a code release for every change, and business rules change constantly. A new status is added; two systems rename a value; a country is added to a region. Keep mappings and status translations in **configuration** that owners can review and administrators can change.

A particularly clear design defines every status once, with an alias and the system's own ID, and then maps aliases to aliases in each direction.

```json
{
  "system_a": {
    "statuses": {"New": "st-101", "Accepted": "st-105",
                 "Resolved": "st-109"},
    "to_system_b": {"Accepted": "New", "Resolved": "Resolved"}
  },
  "system_b": {
    "statuses": {"New": "1", "In Progress": "2", "Resolved": "6"},
    "to_system_a": {"In Progress": "Accepted", "Resolved": "Resolved"}
  }
}
```

Reading from the top: each system's statuses are listed once, with their local identifiers. The two mapping tables use only the *aliases*, so a human reading `"Accepted": "New"` understands it without looking up IDs. If a status arrives that has no entry in the mapping table, the integration should *skip the change and log the reason* ("no mapping for status Accepted-Pending"), never guess. A guess is a silent error; a logged skip is a visible one that someone can fix by adding a row.

## Bidirectional Sync: The Hard Mode

Chapter 7 recommended avoiding bidirectional synchronization through the authority split. Sometimes it cannot be avoided: two teams, each loyal to its own tool, both edit the same ticket. the figure shows the shape of a sound design.

*[Figure: A bidirectional synchronization reads the change history of both systems, merges the changes in time order, applies them under a lock, and ignores the changes made by its own identity.]*
The design reads each system's *change history* (an activity log on one side, an audit table on the other), skips changes it has already synchronized by using a checkpoint, merges the remainder into one list sorted by time, and applies them one at a time in order. Each application takes a lock on the record and filters out changes made by the integration's own user.

Four problems must be solved, and a design that does not name them will meet them in production.

**Table: The four problems of bidirectional synchronization**
| Problem | What goes wrong | Solutions |
|---|---|---|
| Echo loops | The integration writes to B, which emits a change event, which the integration copies back to A | Filter out changes made by the integration's own user; stamp writes with an origin marker; compare values and skip no-ops |
| Ordering | Applying updates out of order restores old values | Sort by change time; use per-record version numbers; allow one writer per record at a time |
| Concurrency | Parallel workers update the same record | Lock with an expiring lease, or partition the work by record key so a record always goes to the same worker |
| Conflicts | Both sides change the same field within one cycle | Per-field authority; last-writer-wins only for fields you do not care about; flag the rest for a human |

The **lock lease** deserves a note. A plain lock held by a worker that crashes is held forever. A *lease* expires on its own after a set time, such as sixty seconds, so that a crash delays the record rather than blocking it. If the work can take longer than the lease, the worker must renew it, or two workers may end up processing the same record. When you evaluate a synchronization product or a third-party package for a client, read the code or documentation for exactly these behaviors: how ordering is established, what the lock covers, and what filters the integration's own writes. Claims such as "synchronizes chronologically" are easy to make, and worth verifying.

> **Prefer fewer bidirectional fields**
    Each field that flows both ways multiplies the conflict surface. Before building a two-way sync, return to the authority matrix and ask whether each field truly needs both directions. Status may belong to one system and description to the other; comments can be append-only. Often, "bidirectional" collapses to two one-way flows and a small append-only exception.

## Reconciliation: The Safety Net

Even a perfect incremental sync drifts. A late commit slips through, an event is dropped, a deploy misbehaves for a weekend, someone edits the target by hand. The only way to know the integration is right is to *check*. A reconciliation job compares the two systems on a schedule, reports differences, and optionally repairs them.

A good reconciliation compares three things per entity type: **counts** (are there as many records on each side?), **identifiers** (which are missing on either side?), and **checksums** (do the records that exist on both sides agree?). The checksum is a hash of the fields the integration is responsible for, computed identically on both sides. For very large collections, compare in slices (by date range, or by the first character of the key) and sample the checksums rather than computing all of them.

Run the reconciliation on a schedule, such as nightly, and *after any incident*. Treat a non-zero drift as an alert, and track the number over time: a slowly rising drift means a defect that individual runs hide. When the report shows differences, decide in advance who is authoritative, so that repair is mechanical: records missing from the target are created, changed records are overwritten with the source's version, and orphans are deleted subject to the guard.

> **Larkspur Outdoor: what the reconciliation found**
    Larkspur's first reconciliation, run in the test environment, reported 41 orders missing from the ERP out of 12,000. The cause was a window of 38 minutes during an earlier ERP restart in which webhooks had been delivered to a receiver that did not queue them. Nobody had noticed, because every order that *did* arrive was correct. The reconciliation job, running every fifteen minutes in production, now repairs such gaps automatically, and the weekly report has been empty since go-live.

## The Initial Load

The first synchronization is special. The target is empty or holds old data, the source holds years of history, and the incremental machinery is not yet running. Three mistakes recur: loading through the same slow, per-record path used for steady state, which takes days; loading while the source keeps changing, so the copy is stale on arrival; and discovering at cutover that the load corrupted the target.

A sound plan has four parts. **Use the bulk path**: an import API, a file load, or a database bulk copy, because they are orders of magnitude faster than record-by-record calls and gentler on rate limits. **Freeze, copy, catch up**: record the watermark *before* starting the bulk copy, copy the history, then start the incremental job from the recorded watermark so that changes made during the copy are applied afterward. **Throttle** the load so that it does not starve live traffic on either system. And **verify before switching**: run the reconciliation on the loaded data, and treat a clean report as the acceptance criterion. Chapter 28 covers cutover strategies built on this sequence.

## Summary

Synchronization turns on a few decisions about meaning and state. Match records by a stored foreign ID, using a crosswalk when the target has no field for it, and treat name matching as a bootstrap only. Combine frequent incremental reads with a slower full reconciliation, using the same upsert code in both. Plan for deletes explicitly through soft-delete flags, delete feeds, or ID-list comparison, and always guard against deleting too much, because a failed read looks like a deleted source.

Keep mappings in reviewed configuration, define statuses once and map aliases, and log unmapped values instead of guessing. In bidirectional sync, solve echo loops, ordering, concurrency, and conflicts explicitly, with leases rather than plain locks, and prefer one-way flows where the authority matrix allows. A reconciliation of counts, identifiers, and checksums, run on schedule and after incidents, is what makes the integration verifiably correct, and the same discipline underpins a safe initial load: bulk path, freeze-copy-catch-up, throttle, verify.

## Exercises

1. **Choose an identity strategy.** For two systems you know, list how a record is matched today. What happens on a rename? Where could a foreign ID be stored?
2. **Test the guard.** Using `reconcile.py`, build a source with 100 records and a target with 100, then remove 20 from the source. What does `deletion_guard` do at a 5 percent threshold, and at 25 percent?
3. **Design a status map.** Write the alias-based mapping for two systems with different ticket statuses. Which statuses have no equivalent, and what should happen to them?
4. **Plan a load.** Write the four steps of an initial load for a table of 5 million records that changes about 200 times per minute. Where do you record the watermark, and what is the acceptance criterion?



# Chapter 16. Testing Integrations

Integrations fail at the boundaries. A field changes type. A partner retries. A token expires between two calls. A page of results arrives out of order. A record contains a character nobody expected. Demonstration-driven acceptance, in which someone clicks through a happy path in front of the business owner and everyone nods, finds none of these. It tests that the integration works when nothing goes wrong, which is the one situation that does not need testing.

This chapter gives you a test strategy that finds the failures that matter, with the tools and code to run it in a delivery pipeline. It extends the classic test pyramid with the layers that integrations specifically need, introduces a failure-injection checklist you can apply to any integration, and shows how to turn "it works" into numbers a business owner can sign.

> **In this chapter**
    * Extend the test pyramid with contract tests, failure injection, and production checks
    * Apply the twelve-row failure-injection matrix to any integration
    * Build a harness that runs the real integration against a mock API behind a fault proxy
    * Write tests for retry behavior, idempotency, and crash recovery, using the companion code as models
    * Use contract tests as a consumer and as a provider
    * Create realistic test data and state acceptance criteria as numbers

## The Integration Test Pyramid

The traditional pyramid has many fast unit tests at the bottom and a few slow end-to-end tests at the top. Integrations need the same shape with three additions, shown in the figure.

*[Figure: The test pyramid for integrations. Many fast tests at the bottom, a few slow end-to-end tests at the top, and checks that keep running in production.]*
Contract tests sit in the middle, to catch interface changes before they reach production. Non-functional tests, including failure injection, check how the integration behaves when things go wrong. And a layer of production checks continues the testing after go-live.

**Table: The layers of integration testing**
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

Every integration should pass the twelve checks in the table before go-live. Each row is a test you can automate. They are the most valuable testing an integration will receive, because each one corresponds to something that *will* happen in production.

**Table: The failure-injection matrix**
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

Some failures are hard to cause on demand: slow networks, connection resets, a broker that disappears. For these, build a harness in which the integration runs for real against controllable dependencies. the figure shows the arrangement.

*[Figure: A failure-injection test harness. The real integration runs against a mock API behind a fault proxy, a real Kafka in a container, and a real database in a container. The test asserts the end state.]*
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

Test data deserves attention, because an integration tested with tidy data is untested. Aim for data that is **realistic but not real**: production-shaped, with personal fields masked or synthesized. Include the ugly cases deliberately: emoji, very long names, leading zeros, every status value, missing optional fields, a record with four hundred lines. Keep **golden files**, pairs of anonymized source records and their expected target output, versioned with the mapping, and run them on every build (Chapter 12). Make the environments **resettable**: a script that puts the sandbox into a known state before each run, so that tests do not depend on what the previous run left behind. And have a **volume generator** that produces production-sized data for load tests; the best time to learn that the job takes nine hours is before go-live.

## Acceptance by Numbers

The business owner signs off acceptance, and a signature on "it works" means little. State the criteria as numbers, agree them in the brief (Chapter 4), and produce evidence for each.

**Table: Acceptance criteria stated as numbers**
| Criterion | Example target | Evidence |
|---|---|---|
| Completeness | 100% of source records present in the target after reconciliation | Reconciliation report |
| Correctness | Zero field mismatches on a random sample of 1,000 records | Sample comparison |
| Freshness | 95% of changes visible within 5 minutes | Freshness metric over a week |
| Resilience | All failure-injection rows pass | Test report |
| Volume | The peak day processed within the window, using under 70% of the API budget | Load-test report |
| Operability | The support team executes the runbook unaided | Signed handover |

The last row connects testing to the gates of Chapter 3: gate three requires this evidence, and gate four requires that the operations team has actually used the runbook. An integration that passes its numbers and has a rehearsed runbook is ready. One that "looked fine in the demo" is a hope.

## Summary

Integrations fail at boundaries, and acceptance by demonstration tests only the happy path. Extend the test pyramid with contract tests in the middle, failure injection beside it, and production checks above it. The unit layer, covering mappings, retry decisions, and watermark logic, is the largest and fastest, and tests pure logic without a network.

Apply the twelve-row failure-injection matrix to every integration: kill it mid-run, run it twice, throttle it, take the target down, expire the token, send bad records, duplicate messages, reorder updates, slow the network, change the schema, skew the clock, and load it to production volume. A harness with a mock API, a fault proxy, and containerized dependencies lets you do so repeatably. Use contract tests as both consumer and provider so interface changes are caught in the pull request. Use realistic, ugly test data and golden files, and state acceptance as numbers backed by evidence.

## Exercises

1. **Run the matrix.** Pick an integration you maintain and run the first nine rows of the failure-injection matrix against it. Which row fails first?
2. **Write the missing test.** Using the companion tests as a model, write a test proving that a duplicate webhook is processed once.
3. **Break a contract.** Take an OpenAPI file, rename a response field, and show how a validation step in your build detects it. Where would the check run?
4. **Define the numbers.** For a real integration, write the six acceptance criteria with numeric targets. Which would the business owner challenge?



# Chapter 17. Delivery: Pipelines, Configuration, and Environments

An integration built by hand in one environment and copied, with edits, to the next is a liability. It cannot be rebuilt if the server is lost. It cannot be reviewed, because nobody can see what changed. It cannot be tested, because the test environment differs from production in ways nobody recorded. And it cannot be handed over, because the knowledge of how it works lives in one person's head and one person's shell history.

The remedy is the same one software engineering found decades ago: treat everything as code. The flows, the mappings, the topics, the connectors, the gateway policies, even the configuration of the target systems should be versioned, reviewed, tested, and promoted by a pipeline. This chapter describes how, including the traps that are specific to integrations: release strategies that behave strangely when the "traffic" is a queue, environments whose sandboxes lie, and the awkward fact that you cannot undeploy data.

> **In this chapter**
    * Describe a delivery pipeline for integrations, from commit to production, with the same artifact in every environment
    * List what should live in version control besides the code, and how each item is applied
    * Separate configuration and secrets from the artifact, and plan environments realistically
    * Version APIs, events, mappings, and releases consistently
    * Choose a release strategy, and explain what changes when the work arrives through a queue or a topic
    * Plan for the fact that rolling back code does not roll back data

## The Pipeline

A pipeline turns a commit into a running integration through a fixed series of automated steps, each of which can stop it. the figure shows one.

*[Figure: A delivery pipeline for integrations. Build once, promote the same artifact through the environments, and approve with evidence.]*
A change enters as a reviewed commit (step 1). The build runs linting, unit tests, and contract tests (step 2) and then security scans for known-vulnerable dependencies and leaked secrets (step 3). If everything passes, it **packages once** (step 4): the output is an immutable artifact, such as a container image tagged with the commit identifier. That *same artifact* is deployed to a test environment through infrastructure as code (step 5), where integration and volume tests run (step 6). An approval step (step 7) records who accepted the release, and on what evidence, before the release reaches production by a controlled strategy such as a canary or a shadow run.

The principle that matters most is "build once, deploy many." The artifact tested in the test environment must be *byte for byte* the one that runs in production. Rebuilding for each environment, however convenient, means that what you tested is not what you shipped. Differences between environments belong in configuration, never in the build.

A minimal pipeline for a Python integration, expressed for GitHub Actions, looks like this; the same stages translate directly to any other system.

```yaml
name: integration-ci
on:
  pull_request:
  push: {branches: [main]}
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: {python-version: "3.12"}
      - run: pip install -r requirements.txt -r requirements-dev.txt
      - run: ruff check . && pytest -q
      - run: pip-audit -r requirements.txt       # known-vulnerable packages
  package:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: docker build -t registry.example.com/orders-sync:${{ github.sha }} .
      - run: docker push registry.example.com/orders-sync:${{ github.sha }}
  deploy-test:
    needs: package
    environment: test             # environment-scoped secrets and approvals
    runs-on: ubuntu-latest
    steps:
      - run: ./deploy.sh test ${{ github.sha }}   # the tested image tag
```

## Everything as Code

The code is the smallest part of an integration. Everything that defines its behavior should be in version control, and each item needs a defined way of being applied.

**Table: What to keep in version control, and how it is applied**
| Asset | Keep in Git as | Applied by |
|---|---|---|
| Integration code and flows | Source code, or exported platform artifacts | The build pipeline; platform deployment tooling (for example, Maven-based deployment for MuleSoft) |
| Mappings and code lists | YAML or CSV, with reviews | Loaded at start-up, or published to a reference-data store |
| Infrastructure (runtimes, queues, networks) | Terraform, Bicep, CloudFormation, or Pulumi | The infrastructure pipeline |
| Kafka topics, ACLs, schemas | Declarative topic and ACL definitions; schema files | A topic operator or provider; registry upload with a compatibility check |
| Connector configurations | JSON per connector, with secrets as references | The Kafka Connect REST API, called from the pipeline |
| Gateway policies | Declarative policy files | The gateway's management API |
| Target-system configuration (asset types, attributes, statuses) | JSON resource files | An idempotent installation script |
| Dashboards and alerts | Dashboard and alert definitions | Monitoring as code |

The last-but-one row hides a technique worth copying. Many integrations require configuration *in the target system*: custom attribute types, statuses, relation types, assignment rules. If an administrator creates them by clicking, the test environment and the production environment will differ in ways nobody remembers. Instead, describe them in JSON files and apply them with an *idempotent* script that creates what is missing and updates what exists, so that running it twice is harmless. The script is then the documentation, the installer, and the drift detector in one.

## Configuration and Secrets

Three rules keep configuration under control.

**One artifact, many environments.** Settings that vary, such as URLs, batch sizes, and schedules, come from the environment in which the artifact runs, never from rebuilt code. **Secrets by reference.** The pipeline and the runtime fetch credentials from a vault using a workload identity; nothing secret lives in Git, in variables visible to everyone, or in logs (Chapter 13). **Validation at start-up.** The program checks its configuration when it starts and fails immediately, with a clear message, if a required setting is missing or malformed, instead of failing three hours into a run.

Add two operational tools. A **feature flag** lets you turn a flow, a target, or a new mapping on and off without a deployment, and a **kill switch**, a single flag that pauses all writing, gives operations a safe response to "something is wrong, stop it now." Check flags per message, not just at start-up, and log their state so that later investigators know which behavior was active.

## Environments

An integration typically passes through four kinds of environment, with different purposes and different data.

**Table: Environment strategy**
| Environment | Connected to | Data | Purpose |
|---|---|---|---|
| Local or development | Mocks and containers | Synthetic | Fast feedback |
| Test | Vendor sandboxes | Synthetic or masked | Integration and failure tests |
| User acceptance or pre-production | Production-like systems | A masked copy of production | Business acceptance, volume tests, shadow runs |
| Production | Real systems | Real | Serving the business; never a test bed |

> **Sandboxes lie**
    Vendor sandboxes typically differ from production in rate limits, data volume, enabled features, authentication settings, and refresh schedules. An integration that passes in the sandbox has proved only that it works in the sandbox. List the known differences in the reconnaissance sheet (Chapter 10), and plan a *shadow run* in pre-production, against production-like systems, to cover what the sandbox cannot.

## Versioning

Consistent versioning lets people reason about change. Four things need versions, and each has a rule.

**Table: What to version and how**
| Thing | Scheme | Rule |
|---|---|---|
| APIs you publish | Major version in the path or header; minor changes are additive | A breaking change means a new major version and a deprecation window |
| Event schemas | Registry versions with a compatibility mode | The pipeline rejects incompatible changes |
| Integration releases | Semantic versioning on the artifact | Release notes list mapping and behavior changes |
| Mappings and code lists | Versioned files | Each change is reviewed by the data owner |

## Release Strategies and the Integration Traps

How you release a new version matters more for an integration than for a typical web service, because integrations hold *state* and receive work through *queues*, and both complicate the familiar strategies.

**Table: Release strategies and the trap each hides for integrations**
| Strategy | How it works | The integration-specific trap |
|---|---|---|
| Rolling | Replace instances one at a time | Old and new versions run together, so mappings and state formats must be compatible both ways during the overlap |
| Blue-green | Run the new stack alongside, then switch traffic | For queue or Kafka consumers there is no "traffic" to switch (see below) |
| Canary | Send a small share of the work to the new version | Route by key (a few customers, one region) so each entity is handled by one version; otherwise ordering and versions interleave |
| Shadow | The new version processes copies of the work and writes to a scratch target; results are compared | The best way to prove a new mapping; make sure the shadow cannot write to production by mistake |
| Feature flag | Deploy the code dark; enable it by flag | Check flags per message, and log their state |

The blue-green trap is worth working through, because it surprises experienced teams. With a web service, you switch the load balancer from blue to green and the old version stops receiving requests. A consumer of a queue or a Kafka topic *pulls* its work. If the green deployment joins the *same consumer group* as blue, Kafka divides the partitions between the two, so both versions process live traffic simultaneously. If green uses a *new* group, both versions process *every* message, and you get duplicates. Neither is what blue-green intended. The safe approach is a deliberate handover: stop blue's consumers (or pause them), start green's, and rely on idempotent processing for the moment of overlap.

> **You cannot undeploy data**
    Rolling back code is easy; rolling back what the integration already wrote is not. If a bad release wrote wrong values into a million target records, redeploying the old version does not correct them. Plan *forward fixes*: a corrective job, and enough history to replay from a checkpoint. Test the "undo" path for any change that writes in bulk, before you need it, and keep the kill switch within reach.

## Delivery on Different Platforms

The principles hold on every platform, but the mechanics differ. **Integration platforms** have their own packaging and promotion: packaged components with environment extensions, exported project bundles, command-line or Maven-based deployment. Check that your platform supports Git-based review, automated tests, and promotion without hand edits; if it does not, wrap it in a scripted process, because a platform whose only deployment method is a click in a console cannot be audited. **Serverless functions and containers** fit standard pipelines; keep timeouts, memory, and concurrency settings in code. **Kafka Connect** connector configurations belong in Git and are applied through the REST API; editing them by hand in production produces precisely the drift that pipelines exist to prevent.

## Summary

Treat everything about an integration as code, reviewed and promoted through a pipeline. Build once and deploy the same immutable artifact through every environment, with differences confined to configuration. Keep in version control not just the code but mappings, infrastructure, topics and schemas, connector configurations, gateway policies, target-system configuration applied by idempotent scripts, and dashboards and alerts.

Configuration comes from the environment, secrets by reference from a vault, and the program validates both at start-up. Four environments serve different purposes, and sandboxes should be assumed to differ from production until a shadow run proves otherwise. Version APIs, schemas, releases, and mappings with explicit rules. Release strategies need adaptation for queue-based work: blue-green consumers split or duplicate the work, canaries should route by key, and shadow runs prove mappings. Because data cannot be undeployed, plan forward fixes and keep a kill switch.

## Exercises

1. **Audit your pipeline.** List everything that defines one of your integrations. Mark each item as *in version control and applied by a pipeline*, *in version control only*, or *neither*. Which gap is most dangerous?
2. **Write the idempotent installer.** Describe, in pseudocode, a script that ensures three custom attributes exist in a target system, creating or updating each. How does it behave on a second run?
3. **Plan a blue-green for a consumer.** Write the exact steps to move a Kafka consumer from version 1 to version 2 without processing a message twice, or at least without harm if you do.
4. **Design the kill switch.** Decide where an integration checks its kill switch, who may flip it, and how it is logged.



---

# Part IV. Messaging and Streaming

Kafka from first principles to production, the many ways data enters and leaves a streaming platform, the other interfaces you will meet, and the large SaaS platforms most enterprises depend on.



# Chapter 18. Kafka Fundamentals

Apache Kafka is a distributed, durable, replayable commit log. It is not a queue, although it can behave like one. It is not a database, although it stores data. And it is not magic, although the way people talk about it sometimes suggests otherwise. Understood correctly, it is one of the most useful tools an integration architect can have: a shared, ordered, retained record of events that many systems can read independently, at their own pace, and replay when something goes wrong.

Understood incorrectly, it is an expensive way to move two hundred messages a day. This chapter takes you from the mental model to the settings that decide whether a pipeline loses data, duplicates it, or runs without incident. It begins with the question that most Kafka projects skip, whether you should use it at all, then explains the model, notes what changed in the 4.x releases, and covers producers and consumers in enough depth to write correct ones. Chapter 19 then covers topic design, Kafka Connect, schemas, security, and operations, and Chapter 20 the many ways data enters and leaves.

> **In this chapter**
    * Decide whether Kafka is the right tool, using the criteria that justify its operational cost
    * Explain topics, partitions, offsets, brokers, replication, and consumer groups
    * Describe what changed in the 4.x releases and why an architect cares
    * Configure a producer so that it does not lose or duplicate data
    * Compare delivery semantics, and explain why "exactly once" ends at Kafka's boundary
    * Write a consumer that commits after processing, handles bad records, and survives rebalances
    * Monitor consumer lag, the one metric most worth alerting on

## Should You Use Kafka at All?

The most common Kafka mistake in enterprise projects is adopting it for a flow of 200 events a day. Kafka earns its place through a specific set of strengths, and if your requirement does not need them, a simpler tool serves better. the table compares Kafka with polling, webhooks, and message queues across the needs that usually decide the matter.

**Table: When Kafka is, and is not, the right tool**
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

the figure shows the pieces. We take them in turn.

*[Figure: Topics are split into partitions; partitions are replicated across brokers; consumer groups share partitions.]*
### Topics, Partitions, and Offsets

A **topic** is a named stream of records, such as `orders.events.v1`. To scale, each topic is split into **partitions**, and each partition is an ordered, append-only sequence of records, a *log*. Every record in a partition has a number, its **offset**, which never changes: the first record is offset 0, the next 1, and so on. the figure shows one partition.

*[Figure: kafka-partition-log]*
Producers append records at the end of the log. Consumers read from a position they choose, and, crucially, **reading does not remove anything**. The record stays until the topic's *retention* expires, which might be seven days, or a size limit, or forever. This is the difference between a log and a queue, and it is what makes replay possible: a consumer that needs to reprocess last week's events simply moves its position back.

### Keys and Ordering

A record has an optional **key**, and the key decides which partition the record goes to: records with the same key always go to the same partition. Because a partition is an ordered log, records with the same key are therefore *ordered relative to each other*. the figure shows three orders, each in its own partition, with their events in sequence.

*[Figure: kafka-key-to-partition]*
Kafka guarantees order *within a partition*, and nothing about order *across* partitions. This leads to the single most important design rule about keys: **use the business entity's identifier** (the order ID, the customer ID) as the key, so that all events about one entity are ordered, and never use a random or missing key if order matters. A topic whose records have no key is spread across partitions with no ordering relationship at all.

### Brokers and Replication

A Kafka cluster consists of **brokers**, the servers that store the partitions. Each partition is *replicated* across several brokers: one is the **leader**, which handles all reads and writes for that partition, and the others are **followers**, which copy the leader's data. If a leader fails, one of the followers that is *in sync* is promoted. A replication factor of three is the usual production choice: the data exists on three brokers, and the cluster survives the loss of one without losing data or availability.

### Consumer Groups

Consumers read in **groups**. Within one group, each partition is assigned to exactly one consumer, so the group as a whole reads each record once, and the work is divided among its members. Two partitions and two consumers means one partition each; with six partitions, up to six consumers can work in parallel, and a seventh would sit idle. *Different* groups are fully independent: the billing group and the search group each read the entire topic, each with their own position. A new consumer team gets its own group, and no coordination with existing consumers is needed. This is the fan-out strength that distinguishes Kafka from a queue.

When a consumer joins or leaves, the group **rebalances**: the partitions are redistributed among the remaining members. Section "Rebalances" below explains why this matters.

## What Changed in Kafka 4.x

Kafka has changed significantly in recent releases, and a design that assumes older behavior may be wrong. the table summarizes the changes that matter to architects.

**Table: Kafka 4.x changes and why an architect cares**
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

A producer sends records to the cluster, and most data loss in Kafka pipelines begins here, through settings that favor speed over safety. the table lists the settings that matter for integrations, with the values to prefer.

**Table: Producer settings for integrations**
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

> **produce() only queues the message**
    The call places the record in a local buffer; it does not mean the record reached Kafka. Without a delivery callback and a final `flush()`, a job can exit "successfully" having sent nothing. Check every delivery report, and fail the run, or alert, if any reports an error.

## Consumers, Groups, and Offsets

A consumer reads records, processes them, and *commits its offset* to record how far it has got. When it restarts, it resumes from the committed offset. *When* it commits relative to processing determines what happens when something fails.

### Delivery Semantics

**Table: Delivery semantics and when to use each**
| Semantics | How you get it | Outcome on failure | Use for |
|---|---|---|---|
| At most once | Commit the offset *before* processing | Messages can be lost | Metrics where loss is tolerable |
| At least once | Process, *then* commit | Messages can be repeated | The normal choice; pair with idempotent processing |
| Exactly once (within Kafka) | Idempotent producer plus transactions, `isolation.level=read_committed` | Neither lost nor duplicated inside Kafka topics | Kafka-to-Kafka stream processing |
| Effectively once (end to end) | At least once plus an idempotent sink (upsert by key, deduplication table) | Duplicates arrive but have no effect | Kafka to a database, API, or other system |

"Exactly once" is a precise claim with a boundary: it holds *within Kafka*, for records that are read from Kafka topics and written to Kafka topics in a transaction. The moment your consumer calls a REST API or writes to a database, you are outside the boundary and back to at-least-once, and your safety comes from idempotent writes. Design the sink first. For nearly every integration, the right answer is "at least once, with an idempotent sink," which delivers *effectively once* results, as Chapter 8 showed in sequence.

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



# Chapter 19. Kafka in Production

Understanding Kafka's model is the beginning. Running integrations on it is a matter of a few dozen decisions that look minor and are not: how many partitions, what retention, which key, which schema rules, how errors are handled, who may read what, and what you watch. Each is easy to get roughly right and costly to correct once other teams depend on it, because a topic, unlike a private function, is a shared interface with a long memory.

This chapter covers topic design, event design, Kafka Connect and change data capture, schemas and their evolution, stream processing, error handling with retry topics and dead letter queues, security, and operations, including capacity arithmetic and multi-region options. It closes with a troubleshooting matrix and the questions to ask a client before any Kafka design begins.

> **In this chapter**
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

**Table: Retention policies and their uses**
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

It sets twelve partitions, three replicas, a minimum of two in-sync replicas (so that `acks=all` means two copies), seven days of retention (604,800,000 milliseconds), and a one-megabyte record limit. Keep events small and link to large payloads using the claim-check pattern of Chapter 7.

### Naming and Versioning

Adopt a naming pattern and enforce it. A common one is `<domain>.<entity>.<kind>.v<major>`, giving names such as `sales.order.events.v1`, `sales.order.state.v1` (a compacted topic), and `sales.order.events.dlq.v1`. Increase the major version in the name only for *breaking* changes; compatible changes use schema evolution. Isolate environments by cluster, not by name suffix, wherever possible; if tenants must share a cluster, encode tenant and environment in the name and apply quotas and ACLs per tenant.

## Event Design on Kafka

Chapter 11 set out the principles for events as a provider. On Kafka, the styles available are worth comparing.

**Table: Event styles on Kafka**
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

The `id` is unique per event and is the consumer's deduplication key. The `subject` identifies the entity and is also the natural Kafka key. The `time` is *event time*, when the thing happened, in UTC. Carry both event time and processing time (when your system handled it), because late events are normal. And include a per-entity `version` so that consumers can discard stale or reordered events, since Kafka orders only within a partition. Notice that the monetary amount is a string, to avoid the floating-point trap of Chapter 12.

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

Several properties encode decisions. The `topic.prefix` makes the topics `pg.public.orders` and `pg.public.order_items`. The `database.password` is a *reference* to a file, not a literal, as Chapter 13 insists. The `slot.name` names a PostgreSQL *replication slot*, which keeps the database from discarding log segments the connector has not yet read. That is essential for correctness, and also the connector's main hazard: an idle or stopped connector leaves the slot holding log data, which can fill the source database's disk. Monitor the slot's lag. The `heartbeat.interval.ms` makes the connector advance the slot even when the captured tables are quiet, so that unrelated database activity does not accumulate log. The `snapshot.mode` of `initial` takes a full snapshot first and then streams changes. And the *unwrap* transformation flattens Debezium's envelope into a simple record, with deletes kept visible as a flag.

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

**Table: Change-data-capture hazards and mitigations**
| Hazard | Why it happens | Mitigation |
|---|---|---|
| The source disk fills up | The replication slot retains log data while the connector is down or slow | Alert on slot lag and disk; use heartbeats; drop the slot deliberately when decommissioning |
| Schema change breaks consumers | CDC exposes the physical table | Use an outbox or a view as the contract; use schema compatibility rules |
| The initial snapshot is slow or locks tables | A large table is read in one pass | Use incremental snapshots; run during low traffic |
| Deletes are lost | Consumers ignore tombstones or compaction removes them | Keep the delete flag; set `delete.retention.ms` above the longest consumer outage |
| Out-of-order updates | Multiple partitions or reprocessing | Key by primary key; carry the source's log position or a version |

## Schemas and Their Evolution

Records without schemas are strings, and strings drift. A **schema registry** stores the schema of each topic's records, assigns each version an identifier, and checks new versions against a **compatibility mode** before they are accepted. Producers embed the schema identifier in each record (a few bytes), and consumers fetch the schema by identifier to decode it. The registry therefore acts as an enforcement point: a producer that tries to publish a breaking change is refused.

**Table: Schema compatibility modes**
| Mode | Allowed change | Who must upgrade first |
|---|---|---|
| Backward | New schema can read data written with the old one (for example, delete a field or add one with a default) | Consumers, then producers |
| Forward | Old consumers can read data written with the new schema (for example, add a field) | Producers, then consumers |
| Full | Both directions | Either order |
| None | Anything goes | Nobody is protected |

Three rules cover most evolution. **Add optional fields with defaults**; this is compatible in the common modes. **Never change a field's type or meaning**, because even a compatible-looking change corrupts consumers that rely on the old meaning. And, for Protobuf, **never reuse a field number**. The formats, Avro, Protobuf, and JSON Schema, differ in details, but the discipline is the same: evolve additively, validate in the build before anything is produced, and choose the strictest compatibility mode your producers can live with. Enforce the mode in the pipeline (Chapter 17), so a pull request that would break consumers fails before deployment.

## Stream Processing: When to Transform Inside Kafka

Some transformations belong inside the streaming platform: filtering, enriching with reference data, joining two streams, aggregating over time windows. **Stateful stream processing** (Chapter 7) keeps state between events and handles *late* and *out-of-order* data using event time and windows. Kafka Streams, Apache Flink, and ksqlDB are the common tools. Use them when the result is itself a stream that other consumers need, or when the computation requires continuity over time that a request-based job cannot provide. Do *not* use them to perform ordinary business integration, such as calling an ERP: that is the job of a consumer with an idempotent sink. The honest costs to weigh are the state's size and recovery time, the handling of late data, and the skill the team needs.

## Errors, Retries, and Dead Letter Topics

A consumer that fails on a record has two bad options: stop, and block everything behind it, or skip, and lose data. Retry topics and a dead letter topic give a third. the figure shows a **non-blocking retry** design.

*[Figure: Non-blocking retries. A failed record moves to a delay topic so the main partition keeps flowing. After the last attempt it moves to the dead letter topic for a human.]*
When the main consumer fails to process a record because of a *transient* error, it publishes the record to a **retry topic** with a delay, instead of retrying in place. The main partition keeps flowing, so one troublesome record does not stall thousands of healthy ones. A retry consumer processes the delayed record after the delay, and, if it still fails, may pass it on to a longer-delay topic. After the final attempt, or immediately for a *permanent* error such as a malformed message, the record goes to the **dead letter topic**, with the failure reason in its headers.

The trade-off is ordering: a retried record arrives after later records for the same key, so the consumer must tolerate out-of-order arrival, using the per-entity version to ignore stale events. If strict order matters, the alternative is to *pause* the partition and retry in place, accepting the stall. Either way, the dead letter topic needs an owner, an alert on its depth, and a tool to inspect and replay its records once the cause is fixed. Chapter 26 returns to this operational discipline.

## Security

A Kafka cluster shared by many applications is a high-value target, and its security has four layers.

**Encryption in transit.** Use TLS between clients and brokers and between brokers. **Authentication.** Every client authenticates as a distinct principal: mutual TLS, SASL/SCRAM with per-application credentials, or SASL/OAUTHBEARER for token-based identity. Never share one credential among applications. **Authorization.** Use access control lists to grant each principal only what it needs: write to *its* topics, read from *its* input topics, and use *its* consumer group. Prefixed ACLs (such as `sales.order.*`) keep this manageable. **Protection of data.** Do not publish personal data to broadly readable topics; tokenize or encrypt sensitive fields, and remember that retention keeps data for days or weeks, so a deletion request must account for the log. Apply quotas so that one runaway producer cannot starve the rest.

> **A topic is a shared interface**
    Anyone who can read a topic can read all of it, including history. Classify topics by sensitivity, separate the sensitive ones, and review who holds read permission as carefully as you would for a database table.

## Operations

### Capacity Arithmetic

Estimate storage before the cluster exists. The formula is *ingest rate × retention × replication factor*. A topic carrying 20 MB/s retained for 7 days needs 20 × 86,400 seconds × 7 days = about 12.1 TB for one copy, and with a replication factor of three, about 36 TB. Add headroom of at least 30 percent. Network follows a similar rule: with replication, each byte produced is written to the network several times, and each consumer group multiplies the read traffic.

### What to Monitor

Four groups of signals predict trouble. *Replication health:* under-replicated partitions and offline partitions should both be zero, and a shrinking in-sync replica set means a struggling broker. *Resources:* disk use, network throughput, and request latency. *Consumers:* lag in records and in time, per group, and rebalance frequency. *Connect:* the status of every connector and task, and the dead letter topic's depth. For CDC, add the replication slot's retained size.

### Multi-Region Options

Spanning regions is a trade between simplicity and recovery. **Active-passive** replication (using MirrorMaker 2, or a vendor's cluster-linking feature) copies topics from a primary region to a standby: simple, suitable for disaster recovery, with the cost that failover requires translating consumer offsets and accepting a small window of loss. **Active-active** runs producers and consumers in both regions with topics replicated each way, which demands care to avoid loops and conflicts. A **stretch cluster** spans three sites in one cluster, rack-aware, with synchronous replication: it offers very low loss but needs low-latency links. Chapter 20 shows each in a diagram, and Chapter 28 connects them to recovery objectives.

## Kafka and the Data Catalog

A governed estate wants to know which topics exist, who owns them, which schemas they carry, and where the data goes. Catalogs can harvest topic and schema metadata from the registry. *Lineage* across topics can be derived from connector configurations (this source feeds that topic, this sink reads it) or emitted as **OpenLineage** events by stream processors and orchestrators, the open specification for run, job, and dataset lineage. Linking topics to owners, classifications, and data contracts (Chapter 29) turns the streaming platform from a black box into a governed asset.

## A Troubleshooting Matrix

**Table: Kafka symptoms, causes, and fixes**
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



# Chapter 20. Kafka as an Integration Backbone

Chapters 18 and 19 explained how Kafka works. This chapter answers the question an architect actually faces: *given a source system and a target system, how should each connect to Kafka?* The answer is never "use Kafka." A design is a *pair*: which way in for this source, and which way out for that target. A CRM-to-warehouse flow is change data capture in and a warehouse sink out. A SaaS-webhook-to-ERP flow is an HTTP gateway in and a consumer application out. Naming both ends on the diagram is the first sign of a real design.

There are many ways in and many ways out, and the right choice depends mainly on one question, *who initiates?*, because that decides where retries, backpressure, and failures live. This chapter maps them all, then covers how consumers can share a stream, how clusters can be combined across sites, how integration platforms plug in, and how to choose between Kafka and its alternatives.

> **In this chapter**
    * Explain the push-and-pull asymmetry of Kafka and what it means for failure handling
    * Choose among twelve ways of getting data into Kafka and eleven ways of getting it out
    * Apply fan-out, competing, broadcast, replay, and bootstrap consumption strategies
    * Compare active-passive, active-active, aggregate, and stretch-cluster topologies
    * Describe how integration platforms consume from Kafka, and what to check in their connectors
    * Compare Kafka with its alternatives and pick a way in and out for a given flow

## Settling the Push-versus-Pull Confusion

People say "Kafka pushes to my application" or "my application pulls from Kafka" interchangeably, and the confusion leads to wrong designs. The facts are simple. Kafka is **push on the write side and pull on the read side**. Producers push records to brokers. Consumers *pull* records from brokers with long-polling fetch requests; the broker never pushes to a consumer. Anything that looks like "Kafka pushes to my REST API" is a *separate process*, a sink connector or a bridge, that pulls from Kafka and then pushes to the target. the figure shows who opens each connection.

*[Figure: Read the arrows as "who opens the request". The connectors are the bridge between systems that cannot speak the Kafka protocol.]*
**Table: Who initiates, and what that means for design**
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

the figure shows six of the common entrances, and the table lists twelve in all. Many estates use four or five of them at once.

*[Figure: Six common entrances. Many estates use four or five of them at once.]*
**Table: Ways of getting data into Kafka**
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

**HTTP ingest gateways** (row 4) are how SaaS webhooks get into Kafka. The gateway must do everything the webhook receiver of Chapter 8 does: verify the signature, produce to Kafka, and answer quickly. Crucially, when Kafka is slow or the producer's buffer is full, answer `429` or `503` so that the sender retries, instead of accepting the request and buffering unboundedly in memory. A REST proxy call looks like this, with the details depending on the product and version:

```bash
curl -X POST https://rest-proxy.example.com:8082/topics/orders.events.v1 \
  -H "Content-Type: application/vnd.kafka.json.v2+json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"records":[{"key":"order-42",
        "value":{"id":"evt-9f2","status":"SHIPPED"}}]}'
```

**Query-based JDBC sources** (row 3) are a quick win and a quiet hazard. They poll with a `SELECT` using a timestamp or incrementing column, so they miss deletes and rows that share a timestamp, and they add query load to the source. Prefer log-based CDC when the database permits; fall back to the query-based connector when it does not.

**The outbox relay** (row 10) is the right way in whenever your own service writes to its own database *and* must publish an event: write both in one transaction and let a relay publish, as Chapter 7 explained.

## Ways Out

Every exit starts with a pull from Kafka. What differs is what happens next and who owns the target's failures. the figure and the table show the exits.

*[Figure: Every exit starts with a pull from Kafka. What differs is what happens next and who owns the target's failures.]*
**Table: Ways of getting data out of Kafka**
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

The same topic can be consumed in several ways, depending on how consumer groups are used. the figure illustrates six common strategies.

*[Figure grid: Six consumption strategies on one platform.]*
**Fan-out** (a): each consuming team uses its own group ID, and each group receives every record. This is the way to feed many independent downstream systems from one event stream. **Competing consumers** (b): one group with many instances, among which Kafka divides the partitions; this scales a single processing job. **Broadcast** (c): every instance has its own unique group, so each sees all records; use it for in-memory caches that must all know every change. **Replay and backfill** (d): a new group, or a reset of offsets to a timestamp, fixes bugs, rebuilds projections, and onboards a new consumer from history. **Bootstrap from state** (e): a new service reads a *compacted* topic from the beginning and obtains the current state of every key without history. **Request-reply** (f): a request topic, a reply topic, and a correlation ID header give RPC-like behavior; use it sparingly, since HTTP is simpler for true RPC.

Three more are worth knowing. **Priority** is not supported per record, so use separate topics per priority and let the consumer poll the high-priority topic first. **Delayed retry** uses retry topics with the consumer pausing until the due time. **Tenant partitioning** uses the tenant ID as the key, or a topic per tenant for strong isolation, although beware growth in the number of topics.

## Multi-Cluster and Multi-Region Topologies

When one cluster is not enough, four topologies recur. the figure shows them together.

*[Figure grid: Four multi-cluster topologies.]*
**Table: Multi-cluster topologies compared**
| Topology | Mechanism | Benefit | Risk |
|---|---|---|---|
| Active-passive (a) | MirrorMaker 2 or cluster linking replicates to a standby | Simple disaster recovery | Failover needs offset translation and client reconfiguration; some data may not have replicated |
| Active-active (b) | Bidirectional replication with prefixed topics | Local latency in both regions | Conflict resolution; duplicates; loops if topics are not prefixed |
| Aggregate or hub (c) | Many edge clusters replicate to a central cluster | Stores and factories keep working offline | Central cluster sizing; schema management across sites |
| Stretch cluster (d) | One cluster across three sites with rack awareness and synchronous replication | No data loss on a site failure | Needs low-latency links; a quorum of sites must stay up |

Pick by recovery objectives: how much data you can afford to lose, and how long you can afford to be down. Chapter 28 turns these into numbers.

## Kafka Meets the Integration Platforms

Integration platforms consume from and produce to Kafka through connectors, and their behavior has details that decide correctness. The MuleSoft Kafka connector, for example, offers a *message listener* that receives records one at a time and a *batch message listener* that receives them in groups, and supports several acknowledgment modes (automatic, manual, duplicates-allowed, and immediate), which differ in when the offset is committed relative to the flow's success. Other platforms have analogous settings. Three questions apply to any of them:

* **When is the offset committed?** After the flow succeeds, or before? This decides loss versus duplication.
* **How many consumers run, relative to partitions?** More consumers than partitions leaves some idle; fewer limits throughput.
* **What happens on an error?** Does the flow's error handler decide whether the record is retried, committed, or dead-lettered, and does the *default* match what you want?

Platform behavior changes with versions, so read the current connector documentation, and test the failure cases (a failing record, a restart mid-batch) rather than assuming.

## Kafka Versus the Alternatives

Kafka is not the only streaming platform, and some alternatives fit some situations better. the table offers a short orientation, and every claim should be verified against current documentation before it is relied upon.

**Table: Kafka and its alternatives**
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

Return to the decision trees of Chapter 9. The "which way in" tree asks where the data enters: from your own application, use a producer (with an outbox if it also writes a database); from a database, use change data capture, or a JDBC poll if the need is simple; from SaaS webhooks, use an HTTP gateway or an integration platform; from legacy MQ, files, or MQTT, use a source connector or a bridge. The "which way out" tree asks where the data leaves: to a store or warehouse, a sink connector; to a rate-limited API, a consumer or HTTP sink that pauses on 429 and uses idempotency keys; to serverless, an event-source trigger with an idempotent handler; to browsers, a server-push gateway; to a SaaS application through flows, an integration-platform listener.

> **Larkspur Outdoor: both ends named**
    Larkspur's analytics feed pairs a *change-data-capture source* on the ERP's database (way in 2) with a *warehouse sink connector* (way out 2), keyed by order ID. Its shop-to-ERP orders use an *application producer with an outbox* (way in 1 and 10) feeding a *consumer application* (way out 1) that calls the ERP with a lookup-before-retry safeguard. Each diagram names the way in and the way out; neither says merely "Kafka."

## Summary

Kafka is push on the write side and pull on the read side; connectors bridge to systems that cannot speak its protocol, and the consumer's control of pace gives natural backpressure toward a throttled target. There are about a dozen ways in (producers, CDC, JDBC polling, HTTP gateways, files, MQ and MQTT bridges, SaaS feeds, stream processors, outbox relays, replication, and bulk loaders) and about a dozen out (consumer applications, sink connectors, HTTP sinks, queryable state, serverless triggers, platform listeners, server push, share groups, warehouse ingest, request-reply, and archives), and a design names one of each.

Consumer groups give fan-out, competing consumption, broadcast, replay, and bootstrap from compacted state. Four multi-cluster topologies trade simplicity, latency, and data-loss risk, chosen by recovery objectives. Integration-platform connectors differ in when offsets commit, how many consumers run, and how errors are handled: verify each, and test failure cases. Alternatives to Kafka exist, and the choice follows from ecosystem, operational model, and cloud alignment.

## Exercises

1. **Name both ends.** For three integrations in your estate that involve Kafka, write the way in and the way out. Is any described only as "via Kafka"?
2. **Handle the throttle.** A consumer writes to an API with a limit of 5 calls per second. Describe exactly what it does when it receives 429, and what happens to the records that arrive meanwhile.
3. **Choose a multi-cluster topology.** A company has two regions and may lose at most 30 seconds of data, with failover in under 10 minutes. Which topology would you propose, and which would you reject?
4. **Interrogate a connector.** For an integration-platform Kafka connector you use, answer the three questions: when does it commit, how many consumers run, and what happens on error?



# Chapter 21. Beyond REST and Kafka

REST and Kafka dominate conversations about integration, and an architect who knows only them will, sooner or later, meet a client whose most valuable data is reachable only through something else. A mainframe that speaks MQ. A bank that exchanges files over SFTP. A hospital whose systems talk HL7. A factory whose machines speak OPC UA. A supplier who sends purchase orders as X12 over AS2. A 15-year-old ERP exposed as SOAP services described by a WSDL.

None of these is exotic. Each is the right answer in its own world, and each has conventions, pitfalls, and a body of practice that you can learn in an afternoon, provided you know what to look for. This chapter surveys the interfaces you will meet beyond REST and Kafka, concentrating on the *integration-relevant* facts: how each is reached, how it fails, and what to ask. It then treats two practices that recur across all of them: file-based integration done properly, and the webhook receiver that accepts fast and processes later.

> **In this chapter**
    * Recognize SOAP, gRPC, GraphQL, database, queue, industrial, healthcare, B2B, and mainframe interfaces and know what each demands
    * Design file-based integration with manifests, atomic delivery, checksums, and idempotent loading
    * Build a webhook receiver that verifies, persists, acknowledges, and defers processing
    * Choose between an API, a database read, and a file when a system offers all three

## A Tour of Other Interfaces

**Table: Interfaces beyond REST and Kafka**
| Interface | Typical home | What to know | Common pitfall |
|---|---|---|---|
| SOAP and WSDL | Older ERPs, banking, government | A strongly typed XML contract; tooling generates clients from the WSDL | Namespaces and versioned WSDLs; large envelopes; WS-Security variants |
| gRPC | Internal services, high-performance APIs | Protobuf contracts over HTTP/2; streaming | Browser and proxy limitations; field-number discipline |
| GraphQL | Front-end-driven APIs, some SaaS | The client chooses the fields; one endpoint | Query cost and depth limits; caching; pagination conventions |
| JDBC and ODBC database access | Databases and warehouses | Direct reads, sometimes writes; the fastest path | Bypasses business rules; couples you to the physical schema; production load |
| IBM MQ, JMS | Mainframes, banking, retail | Reliable queues with transactional semantics | Message formats (copybooks, EBCDIC); poison messages; XA transactions |
| MQTT | Devices and IoT | Lightweight publish and subscribe with quality-of-service levels | Intermittent connections; topic design; device identity |
| OPC UA, Modbus | Factories, plants | Industrial data models and registers | Security zones; time synchronization; vendor-specific profiles |
| HL7 v2 and FHIR | Healthcare | v2 is pipe-delimited messaging over MLLP; FHIR is REST with standard resources | Local customizations; identity matching of patients |
| EDI (X12, EDIFACT) over AS2, SFTP, VANs | Supply chains | Standard documents with envelopes and acknowledgments | Partner-specific variants; certificate management |
| SFTP and file drops | Everywhere | Batch exchange; simple and robust | Partial files; encodings; duplicates |

A few of these deserve a brief expansion.

### SOAP and WSDL

SOAP services publish a WSDL, a machine-readable description of every operation, message, and type. That is a strength: client libraries generate code from it, and the contract is explicit. The common difficulties are practical. Different WSDLs for different service versions may coexist. Security headers (WS-Security) come in several variants. And a service that returns large XML envelopes can be slow to parse. The reconnaissance sheet of Chapter 10 applies equally: find the WSDL, its version, the authentication, the limits, and the fault format, and probe with a tool such as `curl` or a SOAP test client before designing.

### Database Integration

Reading a database directly is tempting: it is fast, complete, and needs no API. It also bypasses the application's business rules, couples you to the *physical* schema (a column renamed in a release breaks you), and places load on a production system whose owners did not agree to it. If you must read directly, use a read replica; use change data capture rather than polling where the database allows it; agree the schema as a *contract* with the owning team, ideally through a view that they promise to keep stable; and avoid writing to another team's tables, which is among the most reliable ways to cause an incident.

### Industrial and Device Interfaces

Factory and device protocols such as OPC UA, Modbus, and MQTT arrive with their own architecture. The network is divided into security zones, and crossing from the operational network to the corporate one is a project of its own. Connectivity is intermittent, so a site broker must buffer and forward (Chapter 5). Clocks matter: a sensor with the wrong time produces misleading data. And the volume can be large, so edge filtering and aggregation are often needed before the data crosses the wide-area link.

### Healthcare Interfaces

Hospitals typically exchange **HL7 v2** messages, a pipe-delimited format carried over a simple transport (MLLP), through an *integration engine* that routes and transforms them. **FHIR** is the newer, REST-based standard, with defined resources such as `Patient` and `Observation`. The perennial difficulties are local: each hospital customizes segments and fields, and matching a patient across systems (the *master patient index* problem) is a serious data-quality problem. Treat the engine's channels as integrations: name them, test them, and monitor them.

### B2B and EDI

Trading partners exchange standard documents, purchase orders (X12 850) and invoices (X12 810) in North America, or EDIFACT equivalents elsewhere, through AS2, SFTP, or a value-added network. Each document is wrapped in envelopes, and receipt is confirmed by a *functional acknowledgment* (X12 997). The standard is a baseline; each partner has an *implementation guide* with their own rules, so onboarding the tenth partner is almost as much work as the first. Certificates for AS2 signing and encryption expire and must be tracked.

## File-Based Integration Done Properly

Files remain the best way to move large volumes, to talk to legacy systems, and to satisfy strict audit requirements. They also fail in characteristic ways that a careful design anticipates. Four failures account for most incidents.

**The partial file.** The consumer picks up a file while the producer is still writing it, and loads half of it. The defense is *atomic delivery*: the producer writes to a temporary name (`orders.csv.part`) and renames it to the final name only when complete, and the consumer only looks for final names. A rename within one file system is atomic.

**The silent truncation.** A transfer fails halfway, and a file with the right name and the wrong content arrives. The defense is a **manifest**: a small companion file listing the expected file names, sizes, row counts, and checksums. The loader verifies each file against the manifest before processing, and refuses on mismatch.

**The encoding and format surprise.** A file arrives in Latin-1 instead of UTF-8, with semicolons instead of commas, or with a header row added. The defense is a *written file specification* (Chapter 12) and validation on arrival, quarantining files that do not conform.

**The duplicate delivery.** The same file arrives twice. The defense is idempotent loading: record the identity of every processed file (name and checksum) in a ledger, and skip repeats; and make the row-level load an upsert.

A sound loader therefore follows a fixed sequence: detect a new file, verify against the manifest, check the ledger, validate the format, load idempotently in batches, record success in the ledger, and *archive* the file (never delete it immediately), with the file's disposition logged in the run summary. A failure at any stage moves the file to a quarantine folder with the reason.

> **Keep the file, keep the evidence**
    Archive every received file, unmodified, for a period that matches your audit obligations. When a number in the target is questioned six months later, the original file is the only complete evidence of what the source actually sent.

## A Webhook Receiver: Accept Fast, Process Later

Chapter 8 showed the sequence; here is the structure of the code. A receiver does exactly three things on the request path: verify, persist, and acknowledge. Everything else happens later, off the request path.

```python
def handle_request(headers, body):
    # 1. VERIFY: reject anything we cannot trust (no processing yet)
    if not webhook.verify(SECRET, body, headers.get("X-Signature"),
                          headers.get("X-Timestamp")):
        return 401
    # 2. PERSIST: put the raw event somewhere durable
    queue.put({"received_at": now(), "headers": dict(headers),
               "body": body})
    # 3. ACKNOWLEDGE: answer in milliseconds
    return 200

def worker():
    while True:
        item = queue.get()
        event = json.loads(item["body"])
        if ledger.first_time(event["id"]):      # deduplicate
            apply_to_target(event)              # idempotent write
```

The handler contains no business logic, so it cannot fail for business reasons and cannot be slow. The queue can be a broker, a database table, or a cloud queue; what matters is that the event is durable before the `200` is sent, because the sender will not retry after a success response. The worker deduplicates by event ID and applies the change idempotently. Add the reconciliation pull from Chapter 7 to repair whatever the fast path misses, and a webhook feed becomes dependable. The verification and ledger functions are the tested ones from the companion code (Appendix E).

## API, Database, or File?

When a system offers all three, the decision follows the requirement.

* **Use the API** when you need current data, small volumes, the application's business rules, or the ability to write safely. It is the right default.
* **Use the database** (or CDC) when you need every change with full history, the volume is high, or no API exists, and you can accept the coupling to the physical schema.
* **Use files** when volume is large, the freshness requirement is hours, the source is a batch system, or audit evidence matters.

Combining them is common and sensible: an API for the live path, a file for the nightly reconciliation, and CDC for the warehouse.

## Summary

Beyond REST and Kafka lie SOAP, gRPC, GraphQL, direct database access, queues, industrial and device protocols, healthcare messaging, B2B exchanges, and files. Each has conventions an architect can learn quickly: find the contract, the authentication, the limits, and the failure modes. Direct database reads are fast and risky, and should go through replicas, CDC, and agreed views. Industrial networks have zones, intermittent links, and clock concerns; healthcare has local customizations and patient-matching problems; B2B has partner-specific implementation guides and expiring certificates.

File-based integration done well uses atomic delivery, manifests with checksums, written specifications, idempotent loading with a ledger, and archives. A webhook receiver verifies, persists, and acknowledges, and defers everything else to a worker that deduplicates. When a system offers an API, a database, and files, choose by the requirement, and combine them where it helps.

## Exercises

1. **Write a file specification.** For an incoming CSV, write the specification (encoding, delimiter, header, types, null handling) and the manifest format. What does the loader do on a mismatch?
2. **Find the risk.** Identify one integration in your estate that reads another team's database tables directly. What would you ask the owning team to promise?
3. **Sketch a receiver.** Write the verify, persist, and acknowledge steps for a webhook from a system you integrate with, including what storage you would use for the queue.
4. **Choose the interface.** For a nightly reconciliation of 5 million records against a legacy system that offers an API, a database view, and an SFTP export, choose and justify.



# Chapter 22. Integrating Enterprise SaaS Platforms

Most enterprise integrations touch a handful of large platforms: a CRM, an ERP, a service-management tool, a human-resources suite, a productivity and identity platform. Each is a large product with its own history, its own vocabulary, and its own way of exposing data. Each has interfaces that are excellent for some jobs and unsuitable for others, change-detection mechanisms that range from elegant to absent, and traps that bite people who treat it as "just another REST API."

This chapter is a field guide to six such platforms: Salesforce, SAP S/4HANA, ServiceNow, Workday, Microsoft's cloud, and Oracle NetSuite. It does not replace the vendors' documentation, which changes with every release. Its purpose is to tell you *what to look for*: which interfaces exist, how to learn about changes, what the upsert key is, where the limits are, how to authenticate unattended, and which traps the experienced have learned the hard way. Use each section as the starting point for a reconnaissance sheet (Chapter 10), and confirm every point against the client's edition and release.

> **In this chapter**
    * List the main interfaces of six major enterprise platforms and when each fits
    * Identify, for each, how to detect changes, what key to upsert by, and where the limits sit
    * Choose an unattended authentication method appropriate to each platform
    * Avoid the characteristic traps: hidden fields, side effects of writes, expiring subscriptions, effective dating
    * Apply twelve questions to any new SaaS platform before designing

> **Why this matters**
    Vendors change APIs, limits, and authentication options with every release, and editions differ. The sections below tell you the questions to ask and where to look. They are not a substitute for confirming the answers for your client's exact edition and version. A design built on a remembered limit that changed last year is a defect waiting for production.

## Salesforce

Salesforce offers the widest set of interfaces of the six. The **REST API** and **SOAP API** handle record operations. The **Bulk API 2.0** is an asynchronous interface for large volumes: you submit a CSV, receive a job identifier, and poll for the result, the asynchronous request-reply pattern of Chapter 6. The **Composite API** lets one call perform several operations. The **Metadata API** manages configuration. And the **Pub/Sub API**, based on gRPC, carries event streams.

**Table: Salesforce at a glance**
| Aspect | What to know |
|---|---|
| Interfaces | REST, SOAP, Bulk API 2.0, Composite, Metadata, Pub/Sub API (gRPC) |
| Change detection | Change Data Capture events and Platform Events through the Pub/Sub API; or queries on `SystemModstamp` or `LastModifiedDate` for polling |
| Upsert key | *External ID* fields allow an upsert by your own key, the standard way to avoid duplicates |
| Limits | An org-wide rolling 24-hour allocation of API requests that depends on edition and licenses, plus per-transaction governor limits; Bulk API has its own job limits |
| Authentication | OAuth 2.0 through an external client app (new connected apps are disabled by default from the Spring '26 release); JWT bearer and client-credentials flows are common for integrations, and the username-password flow is being phased out; use a dedicated integration user |
| Watch out | Field-level security can hide fields from the integration user, so reads silently return less than expected; triggers and flows fire on your writes; event retention is limited, so subscribers must track their replay position and resubscribe in time |

Two traps deserve emphasis. **Field-level security** means the integration user may see only a subset of fields; a query succeeds and returns *fewer fields than you expect*, with no error. Always test with the integration user's real permissions. And **side effects**: a write through the API fires the same triggers, flows, and validation rules as a write by a person, so a bulk load can launch thousands of automations, send emails, and exceed limits. Ask the Salesforce team whether the integration user should bypass specific automations, and test with production-like volume.

**Platform deprecations** deserve a place in every design review. From the Spring '26 release, Salesforce disables the creation of new connected apps by default and steers integrations toward external client apps; it is also phasing out the OAuth username-password flow and the legacy SOAP `login()` call. An older integration may keep running, but the next one cannot simply copy its authentication.

## SAP S/4HANA

SAP exposes functionality in several ways, reflecting decades of evolution. **OData APIs**, published per release in SAP's API catalog, are the modern interface for synchronous access. **SOAP services** remain for some functions. **IDocs** are asynchronous documents used for exchange between SAP systems and others. **BAPIs and RFCs** are remote function calls into SAP business logic, and **CDS views** support extraction. Business events can be published to an event mesh.

**Table: SAP S/4HANA at a glance**
| Aspect | What to know |
|---|---|
| Interfaces | OData APIs, SOAP services, IDocs, BAPIs and RFCs, CDS views for extraction |
| Change detection | Business events published to an event mesh; IDoc change pointers; delta-enabled extraction from CDS views |
| Upsert key | Business keys (order number, material number); external references such as the customer's purchase-order number support duplicate checks |
| Limits | Set by application-server capacity and dialog work processes; bulk loads are often scheduled in batch windows |
| Authentication | Technical communication users with role-based authorizations; OAuth or certificates through integration middleware; cloud editions use communication arrangements |
| Watch out | IDoc status monitoring (for example, status 51, "application document not posted") needs an owner; authorization objects take time to get right; transports move configuration between systems; prefer released APIs over custom code to keep the core clean |

The most valuable advice about SAP is organizational. Prefer **released APIs**: SAP promises to keep them stable, whereas direct table access or custom code in the core makes upgrades painful, a stance often called "keeping the core clean." And treat **IDoc monitoring** as part of the integration. An IDoc that fails to post sits in an error status, visible only to someone looking at the right screen; if nobody owns that screen, orders silently fail to arrive. Name an owner and alert on statuses, as Chapter 26 describes.

## ServiceNow

ServiceNow's **Table API** is a REST interface to any table, which is both its power and its hazard: one endpoint pattern reads and writes incidents, changes, users, and custom tables. The **Import Set API**, with **transform maps**, stages data in a table and then maps it to targets, which is the preferred route for loads. **Scripted REST APIs** expose custom endpoints, **IntegrationHub spokes** provide prebuilt connectors in Flow Designer, and outbound REST messages call other systems.

**Table: ServiceNow at a glance**
| Aspect | What to know |
|---|---|
| Interfaces | Table API, Import Set API with transform maps, Scripted REST APIs, IntegrationHub spokes, outbound REST messages |
| Change detection | Queries on `sys_updated_on`; business rules or flows that call out on change; audit history (`sys_audit`) for field-level changes |
| Upsert key | `sys_id` internally; in transform maps, the *coalesce* setting decides whether a row updates an existing record or inserts a new one |
| Limits | Instance-level REST rate-limit rules configurable by administrators; large queries need paging |
| Authentication | OAuth or basic authentication for an integration user with roles and ACLs; a MID Server reaches on-premises systems from the cloud instance |
| Watch out | ACLs filter what the integration user sees; business rules fire on API writes; transform maps that coalesce on the wrong field create duplicates |

The **coalesce** trap is the classic: a transform map that coalesces on the wrong field, or on none, inserts a new record on every run instead of updating, and a month later the table holds thirty duplicates of each incident. Test the load twice and check the row count, the idempotency test of Chapter 16. For on-premises connectivity, the **MID Server**, an agent installed in the customer's network, plays exactly the role of the outbound agent from Chapter 5.

## Workday

Workday's integration surface reflects its role as a system of record for people. **Workday Web Services** (SOAP, versioned) cover most operations, and newer **REST APIs** are growing. **Reports-as-a-Service** exposes custom reports as web services, a very common way to extract data. The **Enterprise Interface Builder** (EIB) supports file-based loads and extracts, and **Workday Studio** handles complex integrations.

**Table: Workday at a glance**
| Aspect | What to know |
|---|---|
| Interfaces | Web Services (SOAP, versioned), REST APIs, Reports-as-a-Service, EIB for file-based loads, Studio for complex integrations |
| Change detection | Reports with effective-date and entry-date filters; transaction logs; scheduled integrations |
| Upsert key | Workday IDs and reference IDs (for example, `Employee_ID`) |
| Limits | Tenant-level throttling and long-running report timeouts; schedule heavy extracts off-peak |
| Authentication | An Integration System User (ISU) with security groups; OAuth for REST; certificates or credentials for SOAP |
| Watch out | Effective dating; future-dated hires and terminations; security-group changes silently remove fields from reports |

**Effective dating** is Workday's defining trait and the source of its subtlest integration bugs. A change can be *entered today* but *effective next month*, so "what changed since yesterday" is two different questions: what was entered, and what takes effect. A new hire entered in October with a January start date appears now but must not receive an account until January. Decide, with the business, which date drives each downstream action, and test future-dated and retroactive changes explicitly.

## Microsoft 365, Entra ID, and Dynamics 365

Microsoft's cloud presents a unified surface. **Microsoft Graph** is the API for users, groups, mail, calendars, files, and Teams. The **Dataverse Web API** (OData) serves Dynamics 365 and the Power Platform's data.

**Table: Microsoft's cloud at a glance**
| Aspect | What to know |
|---|---|
| Interfaces | Microsoft Graph; the Dataverse Web API (OData) |
| Change detection | Graph *delta queries* for incremental reads; Graph *change notifications* (webhooks) through subscriptions that expire and must be renewed; Dataverse change tracking |
| Upsert key | Object IDs; *alternate keys* in Dataverse allow an upsert by a business key |
| Limits | Throttling returns 429 with `Retry-After`; limits vary by service and tenant |
| Authentication | App registrations in Entra ID; application permissions with client credentials or certificates for unattended jobs; many scopes require administrator consent |
| Watch out | Expired notification subscriptions stop events silently; over-broad application permissions |

The Graph pattern is a textbook case of the "fast path plus repair path" design: **change notifications** give speed, and **delta queries** give completeness. The trap is that notification subscriptions *expire*, after a period that depends on the resource, and a subscription that has lapsed simply stops delivering, with no error. Renew subscriptions on a schedule, and reconcile with a delta query so that a missed window is repaired. Regarding authentication, application permissions (as opposed to delegated ones) let a job act without a person, but they are broad by default; prefer the narrowest, resource-scoped permissions the platform offers, and request administrator consent early, since it requires a person with authority.

## Oracle NetSuite

NetSuite offers **SuiteTalk** web services in REST and SOAP forms, **SuiteQL** for SQL-like queries, **RESTlets** (custom server-side endpoints written in the platform's scripting), CSV import, and saved searches. SOAP is on its way out. According to Oracle's published timeline at the time of writing, the 2025.2 endpoint is the last planned SOAP endpoint, new integrations can no longer be built on SOAP from the 2027.1 release, and SOAP is scheduled for removal with the 2028.2 release. New integrations should use REST web services with OAuth 2.0.

**Table: Oracle NetSuite at a glance**
| Aspect | What to know |
|---|---|
| Interfaces | SuiteTalk REST web services (the strategic interface), SuiteQL, RESTlets, CSV import, saved searches; SuiteTalk SOAP is being removed |
| Change detection | `lastModifiedDate` filters in queries and saved searches; user-event scripts that call out on change |
| Upsert key | `externalId` on records enables an upsert by your own key |
| Limits | Account-level concurrency limits on web-service requests; script governance units for custom code |
| Authentication | OAuth 2.0 for new integrations; token-based authentication remains only for existing integrations |
| Watch out | Concurrency limits shared with every other integration on the account; role permissions decide which fields are visible; custom fields and forms differ between sandbox and production |

NetSuite's **concurrency limit** is the constraint teams most often meet. The limit applies to simultaneous requests for the whole account, so a new integration with eight parallel workers can starve the existing ones. Count the total and request an allocation. The differences in **custom fields** between sandbox and production are a specific case of the general warning that sandboxes lie.

## Twelve Questions for Any New SaaS Platform

When you meet a platform not covered here, ask these twelve questions before you design.

1. Which interfaces exist: REST, bulk, events, files, SOAP? Is there an OpenAPI specification?
2. How do I read only what changed, and how do I see deletes?
3. Can I upsert by my own external key?
4. What are the limits, and are they shared with other integrations on the tenant?
5. Which authentication methods suit an unattended job, and who approves them?
6. What does the integration user see? Are fields hidden by permissions?
7. Do my writes trigger workflows, emails, or other side effects?
8. How are events delivered, retained, and replayed?
9. Is there a sandbox, and how does it differ from production?
10. How are API versions released and retired?
11. Is there an official connector for the client's integration platform, and what does it not support?
12. What do the vendor's status page and changelog look like? How quickly are problems acknowledged?

The questions are the same ones that Chapter 10 taught you to ask of any API; the platform sections above show how the answers look in practice.

## Summary

Six major platforms each have their own interfaces, change-detection mechanisms, keys, limits, and traps. Salesforce offers bulk, composite, and gRPC event interfaces, upserts by external ID, and hides fields behind field-level security. SAP S/4HANA exposes OData, IDocs, and events; prefer released APIs and assign an owner to IDoc monitoring. ServiceNow's Table API is powerful, its transform-map coalesce setting decides between update and duplicate, and a MID Server reaches on-premises systems. Workday's effective dating makes "changed since" two questions and its reports-as-services are the usual extraction path.

Microsoft's Graph pairs change notifications with delta queries, and expiring subscriptions must be renewed and reconciled. NetSuite's account-wide concurrency limit is shared among all integrations. For any new platform, twelve questions on interfaces, change detection, keys, limits, authentication, visibility, side effects, events, sandboxes, versions, connectors, and vendor behavior prepare the design.

## Exercises

1. **Build a cheat sheet.** Choose a SaaS platform you integrate with that is not covered here, and fill in the six rows (interfaces, change detection, upsert key, limits, authentication, watch out).
2. **Test the visibility.** For one platform, compare what an administrator sees with what your integration user sees, using record counts and field lists. Where do they differ?
3. **Find the side effects.** List every automation (trigger, workflow, flow) that fires when your integration writes to a target platform. Could a bulk load overwhelm any of them?
4. **Renew the subscription.** For a platform with expiring notification subscriptions, write the schedule for renewal and the reconciliation that covers a lapse.



---

# Part V. Platforms and Practice

Integration platforms and how to choose among them, nine composite case studies, and one project followed from the first meeting to the first incident.



# Chapter 23. Integration Platforms

Most large enterprises run several integration technologies at once. There is a message broker from the 2000s, an enterprise service bus from the 2010s, an integration platform as a service from the late 2010s, cloud-native services from the 2020s, and a layer of scripts nobody remembers writing. Each was the right choice when it was bought, and each is still doing real work. An architect arriving in such an estate does not choose from a blank sheet; they navigate a landscape, decide what to add and what to retire, and have to explain the choice to people who own the old systems and people who want the new ones.

This chapter maps that landscape, takes one widely used platform, MuleSoft's Anypoint, apart in enough detail to read any similar product's documentation, surveys the others, and ends with a method for choosing. Throughout, remember the principle of Chapter 9: choose the platform to *carry* the pattern, not to dictate it.

> **In this chapter**
    * Place integration technologies in twelve categories, and recognize who typically owns each
    * Explain the control-plane and runtime-plane architecture of an integration platform and the runtime hosting options
    * Describe the building blocks that every platform renames: flows, connectors, transformation language, state, queues, batch, policies
    * Use error-handling semantics, such as MuleSoft's continue versus propagate, to avoid silent data loss
    * Compare Boomi, Workato, hyperscaler stacks, and enterprise technologies you may inherit
    * Choose a platform with a weighted scorecard, a proof of concept with failure injection, and a three-year cost view

## The Landscape in One Table

**Table: Twelve categories of integration technology**
| Category | What it does | Names you will meet | Typical owner |
|---|---|---|---|
| iPaaS (integration platform as a service) | Low-code flows, connectors, API management, monitoring, often hybrid runtimes | MuleSoft Anypoint, Boomi, Workato, SnapLogic, Informatica, Celigo, Jitterbit, Tray.ai, Oracle Integration, SAP Integration Suite, IBM App Connect, Microsoft Azure Integration Services | Central IT or an integration center of excellence |
| ESB and enterprise messaging | Routing, transformation, and guaranteed delivery in the data center | IBM MQ and App Connect Enterprise, TIBCO BusinessWorks and EMS, webMethods, Oracle SOA Suite, WSO2, Apache ServiceMix | Core banking, insurance, telecom, government |
| API management | Gateways, developer portals, policies, analytics | Apigee, Kong, Azure API Management, AWS API Gateway, MuleSoft API Manager, Axway, WSO2, Tyk | Platform or API teams |
| Event brokers and streaming | Asynchronous messaging and logs | Kafka (and managed offerings), Pulsar, RabbitMQ, Solace, NATS, Event Hubs, Pub/Sub, Kinesis | Platform engineering, data teams |
| Cloud-native integration services | Building blocks for serverless integration | EventBridge, Step Functions, SQS and SNS, AppFlow; Logic Apps, Service Bus, Event Grid, Functions; Pub/Sub, Workflows, Eventarc | Cloud center of excellence |
| ELT, CDC, and replication | Bulk and incremental data movement into analytics platforms | Fivetran, Airbyte, Matillion, Qlik Replicate, Oracle GoldenGate, Striim, Debezium, AWS DMS | Data engineering |
| Virtualization and reverse ETL | Query across sources; push warehouse data back to applications | Denodo, Trino and Starburst, Dremio; Hightouch, Census | Data and analytics teams |
| Managed file transfer and B2B | Partner exchange, secure files, standard documents | Axway, IBM Sterling, GoAnywhere, Cleo, OpenText, SPS Commerce | Supply chain, finance operations |
| Orchestration and workflow | Durable business processes and data pipelines | Camunda, Temporal, Airflow, Dagster, Prefect, Step Functions, Logic Apps | Process or data engineering |
| Code-first frameworks | Integration libraries for developers | Apache Camel, Spring Integration, Spring Cloud Stream, Quarkus, Apache NiFi | Engineering teams with JVM skills |
| Citizen automation | Business-user workflows | Power Automate, Zapier, Make, n8n | Business units, often ungoverned |
| Domain engines | Healthcare, industrial, and financial standards | Rhapsody, Mirth Connect, InterSystems (HL7, FHIR); HiveMQ, EMQX (MQTT); SWIFT and ISO 20022 gateways | Hospitals, manufacturers, banks |

The market is crowded and changes constantly: vendors are acquired (IBM acquired webMethods and StreamSets from Software AG in 2024, for instance), merge product lines, and reposition. Analyst reports can help you make a long list, but vendor rankings change every year, and no report knows your skills, your estate, or your budget. Treat analysts as one input and run your own proof of concept.

## MuleSoft Anypoint Platform, in Depth

MuleSoft, a Salesforce company, combines an integration runtime (Mule), API management, and design and governance tooling in its Anypoint Platform, and popularized the API-led approach of Chapter 6. It is common in large enterprises and in Salesforce-centered estates, and a good representative of the category: if you understand its architecture, you can read any competitor's documentation.

### Architecture: Two Planes

the figure shows the central idea of most modern integration platforms: a split between a *control plane* and a *runtime plane*.

*[Figure: The control plane manages and monitors; the runtime plane executes flows and carries your data. You can host the runtime plane yourself even when the vendor hosts the control plane.]*
The **control plane** is where you design, deploy, monitor, and govern. It is normally hosted by the vendor. The **runtime plane** is where flows execute and *your data* passes through. The importance of the split is that the two can be in different places. A company can use the vendor's cloud for design and monitoring while running the runtime in its own data center or cloud account, so that business data never leaves its network. That is the answer to most data-residency objections, and the question to ask of *any* platform: where does my data flow, and where does the logic execute?

**Table: Runtime hosting options for an integration platform (MuleSoft terms)**
| Option | What it is | Choose it when | Think about |
|---|---|---|---|
| CloudHub | Vendor-managed, worker-based hosting (the older model) | Existing estates already on it | Being superseded by the newer container-based service |
| CloudHub 2.0 | Vendor-managed, container-based hosting with private spaces | Systems reachable from the cloud; minimum operations | Private connectivity to on-premises needs a VPN or similar; data lives in the vendor's cloud region |
| Runtime Fabric | The runtime on your own Kubernetes (cloud or on premises), managed from the control plane | Data residency; existing Kubernetes; hybrid | You own cluster operations and capacity |
| Standalone (hybrid) | The runtime on your servers or virtual machines | Traditional data-center estates | Patching, clustering, and high availability are yours |

Licensing is usually by compute capacity (such as virtual cores) or by number of flows, which makes sizing a commercial as well as a technical decision. These option names and models change; confirm the current offerings with the vendor.

Runtime versions also follow a published cadence, with *Edge* and *Long-Term Support* release channels and defined support windows. On the managed runtimes, an application still running a version that has reached end of life can be force-upgraded, so version support belongs in the operational plan and not only in the contract.

### API-Led Connectivity in Platform Terms

the figure shows the three layers.

*[Figure: System APIs unlock a back end once; process APIs encode business logic; experience APIs adapt data to each channel.]*
It works well when many consumers will reuse the same system APIs, when teams are organized around the layers and a central platform team exists, and when governance (policies, service levels, discovery in a catalog) is valued. It hurts when the estate has three systems, because the layers add latency and meetings; when process APIs become a dumping ground for business logic that nobody owns; and when every call chains through three network hops.

### Building Blocks You Should Recognize

Every platform renames the same ideas. Learn them in one platform and you can translate to any other.

**Table: Building blocks of an integration platform, and their equivalents**
| Concept | What it is | Equivalent elsewhere |
|---|---|---|
| Flow and sub-flow | A unit of processing started by a source (an HTTP listener, a scheduler, a message listener) | A recipe (Workato), a process (Boomi), a pipeline (SnapLogic) |
| Connector | A packaged client for a system (HTTP, Salesforce, SAP, database, Kafka, files) | A connector or snap |
| Transformation language | The expression language for mapping, filtering, and reshaping data (DataWeave in MuleSoft) | XSLT, JSONata, Jolt, visual maps |
| Object store | Key-value persistence for state such as watermarks and deduplication keys | A cache or document properties; lookup tables; a database table |
| Queues | Managed cloud messaging, or in-memory queues between flows of one application | SQS, Service Bus |
| Batch job | Record-level processing in steps, with failure thresholds | An ETL job |
| Policy | Declarative API protection at a gateway: client-ID enforcement, rate limits, token validation | Gateway policies elsewhere |
| Exchange or catalog | A catalog of reusable assets, API specifications, and templates | An internal developer portal |

### Error Handling: The Part That Decides Reliability

Of everything in an integration platform, the semantics of error handling deserve the most attention, because they decide whether failures are visible. In Mule 4, an error is routed to the first matching handler, and there are two handler types whose difference is the single most important thing to know.

**Table: Two error handlers with opposite consequences**
| Handler | What happens | Transactions | The caller sees | Use for |
|---|---|---|---|---|
| `on-error-continue` | Runs the handler, then treats the owner (the flow or scope) as though it had succeeded | Committed | Success | Bad records you quarantine; recoverable conditions |
| `on-error-propagate` | Runs the handler, then rethrows the error to the parent | Rolled back | Failure | Transient failures that must retry or alert; anything you must not hide |

A catch-all `on-error-continue` of type `ANY` at flow level makes *every* failure look like success, both to the caller and to monitoring. The run summary says "OK" while records vanish. Reserve *continue* for errors you have deliberately dealt with, and let everything else propagate. The same lesson applies to every platform: find out what the default error behavior is, and what makes a failure visible to the scheduler and to monitoring.

Other platform defaults to check: a **batch job** in Mule by default stops at the first failed record (a threshold of zero); you can set a positive tolerance, or -1 to continue regardless, and inspect failed records in a completion phase to route them to quarantine. Use **reconnection strategies** for connectivity problems and an **until-successful** scope for operation retries, with a cap, and never retry non-idempotent writes without an idempotency key. For deduplication, use an idempotent validator backed by the object store, or natural idempotency through upserts.

### An Illustrative Flow

The following sketch shows the shape of a flow that polls a CRM every five minutes, keeping its watermark in the object store, and transforms the result. It is illustrative, not a tested listing, and attribute names vary by version; its purpose is to show that the *same pattern* of Chapter 14 appears in platform form.

```xml
<flow name="sync-customers-flow">
  <scheduler>
    <scheduling-strategy>
      <fixed-frequency frequency="5" timeUnit="MINUTES"/>
    </scheduling-strategy>
  </scheduler>
  <!-- the object store holds the watermark between runs -->
  <os:retrieve key="customers.watermark" objectStore="wmStore" target="since">
    <os:default-value>#["1970-01-01T00:00:00Z"]</os:default-value>
  </os:retrieve>
  <http:request method="GET" config-ref="CRM_HTTP" path="/customers">
    <http:query-params>
      #[{ modified_since: vars.since, limit: 500 }]
    </http:query-params>
  </http:request>
  <ee:transform>
    <ee:message><ee:set-payload><![CDATA[%dw 2.0
output application/json
---
payload.results map (c) -> {
  externalId: c.id,
  name: trim((c.firstName default "") ++ " " ++ (c.lastName default "")),
  email: lower(c.email default ""),
  modified: c.modified
}]]></ee:set-payload></ee:message>
  </ee:transform>
</flow>
```

Read it against the Python poller: a scheduler (the tick), a stored watermark (the checkpoint), an HTTP request with `modified_since` (the incremental read), and a transformation (the mapping). The platform removes the plumbing and keeps the design decisions: overlap, idempotent upsert, and advancing the watermark only after success all still have to be built.

## Boomi

Boomi is a widely deployed iPaaS whose architecture emphasizes a distributed runtime. the figure shows how it separates a cloud control plane from runtimes that sit where the customer wants.

*[Figure: A cloud control plane separated from a distributed runtime. The runtime sits where the customer wants it: a single-tenant node, a cluster, or the vendor's cloud.]*
The runtime comes in shapes that differ in resilience and location: a *basic runtime* on a single node, a *runtime cluster* for high availability and scale, and a *cloud runtime* that is multi-tenant and hosted by the vendor. Flows (called processes) are built visually, with a large connector library and strong support for B2B and master data. As with any such platform, ask where the logic executes, how deployments are versioned and promoted, and how errors are made visible.

## Workato and Business-Led Automation Platforms

Workato represents a category aimed at business-led delivery: low-code "recipes" that connect applications through triggers and actions, with a vast connector library and, in its on-premises agent, an outbound connection that needs no inbound firewall rules. Such platforms are fast to deliver and popular with business technology teams. Their characteristic risks are *task-based pricing* that grows with volume, flows built by people without engineering practices (no tests, no version control), and unclear boundaries between what runs locally and what runs in the vendor's cloud. Check each against your requirements, and bring such tools inside the governance framework of Chapter 29 rather than leaving them as shadow integration.

## The Hyperscaler Stacks

Each major cloud offers integration building blocks that can replace or supplement a commercial platform. On **AWS**: EventBridge for event routing, SQS and SNS for queues and topics, Step Functions for orchestration, AppFlow for SaaS data flows, Glue and DMS for data pipelines, and Lambda for compute. On **Azure**: Logic Apps and Power Automate for workflows, Service Bus and Event Grid for messaging, Functions, API Management, and Data Factory. On **Google Cloud**: Pub/Sub, Workflows, Application Integration, Eventarc, Dataflow, and Datastream. The translation table in Chapter 5 maps them to each other.

The trade-off against an iPaaS is the familiar one. Cloud-native services give you fine control, low per-unit cost, and tight integration with the cloud, at the price of assembling and operating many parts, and of skills that a business-led team may not have. They suit estates with engineering capacity, where flows are code and delivered by pipelines, and where the integrations stay within one cloud.

## Enterprise Technologies You May Inherit

You will meet technologies that are not fashionable and are very much alive.

* **IBM MQ and IBM App Connect Enterprise** carry the transaction traffic of many banks and insurers, with strong guarantees of delivery and transactional semantics.
* **TIBCO and webMethods** are long-established ESBs, with large installed bases; webMethods now belongs to IBM.
* **Solace** and **SAP Advanced Event Mesh** provide event meshes across sites and clouds.
* **Managed file transfer and EDI products** (Axway, IBM Sterling, GoAnywhere, Cleo, OpenText) run partner exchange for retailers and manufacturers.
* **Apache NiFi** and **Apache Camel** are open-source tools for dataflow and routing, popular with engineering-led teams.
* **Healthcare engines** (Rhapsody, Mirth, InterSystems) and **industrial gateways** carry the standards of their domains.
* **CDC and replication tools** (GoldenGate, Qlik Replicate, Striim, Debezium) feed analytics and event platforms.

The right attitude toward such systems is respect and incremental change: put an anti-corruption layer in front, offload via events or CDC, and replace piece by piece using the strangler fig. Replacing an ESB in one step is how migration programs become multi-year failures.

## Choosing a Platform

A platform decision lasts for years and costs real money, and it deserves a method rather than a preference. Four steps make it defensible.

**Step 1: Define criteria and weight them.** Typical criteria include connector fit with your systems, skills available, runtime flexibility and data residency, governance features, delivery and testing support (can flows live in Git and deploy by pipeline?), observability, cost model, lock-in, and vendor viability. Weight them by what matters to *this* organization.

**Table: An example weighted scorecard**
| Criterion | Weight | Platform A | Platform B | Platform C |
|---|---|---|---|---|
| Connector fit for the estate | 20% | 4 | 5 | 3 |
| Team skills and hiring | 15% | 3 | 3 | 5 |
| Runtime location and residency | 15% | 5 | 3 | 4 |
| Delivery pipeline and testing support | 15% | 4 | 3 | 5 |
| Observability and operations | 10% | 4 | 4 | 3 |
| Governance and security | 10% | 5 | 4 | 3 |
| Three-year cost | 10% | 2 | 4 | 5 |
| Lock-in and exit | 5% | 2 | 3 | 5 |
| **Weighted score** | 100% | **3.9** | **3.8** | **4.1** |

Multiply each score by its weight and add. The numbers are inventions to show the method; the useful result is not the total but the *argument*: when a stakeholder challenges the winner, you can ask which weight or score they disagree with.

**Step 2: Run a proof of concept on the hardest real flow,** not on a demo that the vendor prepared. Include failure injection (Chapter 16): kill a run mid-way, throttle the target, send a bad record, expire a token. Measure how each platform behaves and how visible the failures are.

**Step 3: Model three-year cost,** including licenses, infrastructure, skilled staff, training, and the cost of migrating *away*. Per-task and per-call pricing models can grow nonlinearly with volume, so model the volume you expect in year three, not year one.

**Step 4: Record the decision and its revisit conditions** in a decision record, so the reasoning survives the people who made it.

> **Beware the platform that is chosen before the problem**
    The commonest platform failure is not a bad product but a mismatched one: a business-led tool for engineering-heavy flows, a heavyweight ESB for five simple integrations, a streaming platform for two hundred events a day. Return to the decision trees (Chapter 9) and ask what *class* of platform the dominant workload needs before comparing products.

## Summary

Integration technology comes in twelve categories, and most enterprises run several generations at once. Modern platforms split a control plane from a runtime plane, which lets the runtime sit where the data must stay, and the first question about any platform is where data flows and where logic executes. MuleSoft's architecture illustrates building blocks every platform renames, and its error-handling semantics, in particular the difference between continuing and propagating, show why a platform's defaults can make failures invisible.

Boomi, Workato, the hyperscaler stacks, and inherited ESBs, MQ, and file-transfer products each have a characteristic fit and risk: distributed runtimes, business-led speed with pricing and governance risks, fine control with assembly effort, and respect for what already works. Choose with a weighted scorecard, a proof of concept on the hardest real flow with failure injection, a three-year cost model, and a decision record. Choose the class of platform before the product.

## Exercises

1. **Map your estate.** List every integration technology your organization runs and place each in one of the twelve categories. Which category is missing, and which is duplicated?
2. **Ask the control-plane question.** For one platform you use, find out where flows execute and where data passes through. Does the answer match what your security team believes?
3. **Audit the error defaults.** Find the default error behavior of your platform. Construct a flow that fails, and check whether the scheduler, the monitor, and the caller see it.
4. **Build a scorecard.** Write six criteria and weights for a platform decision you face. Score two real candidates. Which weight would change the winner?



# Chapter 24. Case Studies

Patterns and platforms become convincing when you see them applied to a whole situation: a business problem, the constraints that shaped the answer, the decisions that were made, and the places where the design later hurt. This chapter presents nine architectures modeled on situations that enterprises genuinely face, using the technologies those enterprises typically run.

They are **composites**, built from common public architectures and widely repeated lessons, not descriptions of any specific organization. No customer, product decision, or incident here belongs to a real company, and any resemblance is coincidental. Use them as worked examples in design sessions: cover the "design decisions" and ask a group what *they* would do, then compare.

> **In this chapter**
    * Analyze nine integration architectures, from API-led order-to-cash to a governed data platform
    * Trace each design decision to a constraint and to patterns from Chapters 6 and 7
    * Anticipate the characteristic pitfalls of each situation
    * Recognize what the nine have in common

## Case 1: Order-to-Cash Across SAP, Salesforce, and a Web Shop

A global manufacturer sells through a web shop and through field sales using Salesforce. Orders, prices, and stock live in SAP S/4HANA, and a warehouse system ships. Every new sales channel used to mean another point-to-point project, each with its own mapping and its own way of failing.

*[Figure: Case 1: order-to-cash with API-led layers. Experience APIs serve each channel, a process API owns order rules, and system APIs isolate each back end.]*
**Design decisions.** The company built one *system API* per back end, owned by the team that knows it. SAP access is isolated behind a single translator, so an S/4HANA upgrade touches one place. A *process API* owns the order rules and the saga: reserve stock, confirm the price, create the sales order, and compensate if the warehouse rejects. Invoices and shipping notices travel asynchronously through a queue, so the web shop never waits on them. Gateway policies, client-ID enforcement, rate limiting, and token validation, apply at the experience layer, and the internal layers trust only the layer above.

**Pitfalls.** SAP's IDoc status handling and the *idempotent creation* of orders are the sharpest edges; the team used the web order number as an external key so that a retried creation could find the order it had already made. Chained synchronous hops add latency, so each layer has a time budget. And the process API tends to become a dumping ground for business rules that no one owns; the cure is a named owner and a rule that the process layer holds only orchestration and decisions.

**Platform notes.** An integration platform with governance features, reusable connectors for SAP and Salesforce, and one place to apply policy suits this estate. A comparable build on cloud-native services is possible, but the team would assemble the governance itself.

**Patterns used:** API-led connectivity, orchestration, saga, queue, API gateway, anti-corruption layer.

## Case 2: A Bank Offloads Mainframe Events to Kafka

A bank's core system runs on a mainframe with IBM MQ and Db2. Fraud detection, digital channels, and analytics all want core events in near real time. But mainframe query load is billed by usage, and the system is under change freeze for most of the year.

*[Figure: Case 2: mainframe offload. Messages already on MQ are copied to Kafka by a bridge, and database changes are captured from the Db2 log. Fraud scoring runs as a stream processor; consumers read through separate groups.]*
**Design decisions.** The core is not modified. Messages that already flow through MQ are copied to Kafka by a bridge connector; tables with no messages are captured from the Db2 log. Topics are keyed by account, so per-account ordering holds. Fraud scoring runs as a stateful stream processor with a time window. The data lake and the channel services consume through *separate consumer groups*, so one team's lag never affects another's. Schemas in Avro or Protobuf are registered and owned by the core team, with a backward-transitive compatibility mode because replay is part of the operating model.

**Pitfalls.** An MQ unit of work does not map to a Kafka transaction, so the team defined precisely what "delivered" means and made every consumer idempotent. Copybook-defined messages carry EBCDIC text and packed decimals that need careful conversion. And account numbers are *sensitive*: they are tokenized before they land in broadly readable topics.

**Platform notes.** IBM MQ and its integration products remain the system of record for messaging; Kafka, managed or self-run, becomes the new fan-out layer, fed by a bridge connector or a Camel route.

**Patterns used:** queue, change data capture, event streaming, stream processing, event-carried state transfer.

## Case 3: Retail Stores, an Event Mesh, and Cloud Inventory

A retailer with 1,200 stores wants real-time stock and sales events in the cloud. Stores must keep trading when the wide-area link fails.

*[Figure: Case 3: stores with local brokers connected through an event mesh to cloud brokers, with a bridge copying a subset to Kafka for the data platform.]*
**Design decisions.** A small broker in each store buffers events and, when the link returns, forwards them in order, so stores never depend on the cloud in order to sell. Hierarchical topics (for example `retail/EU/store-0412/sale/completed`) let services subscribe to a country, a store, or a product family without code changes. The mesh routes events only to where subscribers exist, which keeps wide-area traffic small, and an analytics bridge copies a subset to Kafka for the data platform. The ERP receives summarized events rather than every scan.

**Pitfalls.** Topic taxonomy needs governance, or the mesh becomes a swamp. Clock drift on store devices breaks ordering by timestamp. And device certificates must be issued, rotated, and revoked across thousands of endpoints.

**Platform notes.** An event-mesh product, or Kafka with MirrorMaker or cluster linking from store clusters. The deciding factors are the number of sites, the mix of protocols, and operational skill.

**Patterns used:** event mesh, publish and subscribe, claim check, edge topology.

## Case 4: Hospital Interfaces, HL7 v2 to FHIR

A hospital group runs dozens of clinical systems, admissions, laboratory, radiology, pharmacy, that exchange HL7 v2 messages through an integration engine. A new patient portal and analytics program need the same data as FHIR resources.

*[Figure: Case 4: clinical systems send HL7 v2 messages to an integration engine, which routes them, translates them to FHIR resources, and feeds a FHIR server and downstream consumers.]*
**Design decisions.** The integration engine remains the hub: each clinical system keeps its existing HL7 v2 interface, and the engine translates messages into FHIR resources for a central FHIR server, which the portal and analytics read. Every channel is named, owned, and monitored as an integration, with acknowledgments checked and failed messages parked for a person. A master patient index matches patient records across systems, and no message is allowed to create a new patient without passing it. A documented *downtime procedure* says what clinical staff do when the engine is unavailable.

**Pitfalls.** Local customizations of HL7 segments differ per system, so every mapping needs testing with real, anonymized messages. Patient matching errors are a patient-safety issue, not merely a data-quality one. And regulation (privacy, retention, audit) applies to every hop, so access logging is part of the design.

**Platform notes.** Specialist healthcare engines carry the standards natively and are the usual choice; a general-purpose platform can work with the right adapters.

**Patterns used:** hub and spoke, message translator, content-based router, retry and dead letter queue, master data management.

## Case 5: Factory Floor to ERP and Lakehouse

A manufacturer wants machine data and production events from plants to reach the ERP (for orders and confirmations), a manufacturing execution system, and a cloud data lakehouse.

*[Figure: Case 5: machines speak OPC UA to an edge gateway, which publishes to a site MQTT broker. A bridge forwards to Kafka in the cloud, and an integration platform with an agent in the plant exchanges orders and confirmations with the ERP.]*
**Design decisions.** Machines and controllers speak OPC UA to an edge gateway in the plant's operational network. The gateway publishes to a site MQTT broker, which buffers during outages. A bridge forwards selected topics to Kafka in the cloud, from which a sink loads the lakehouse. Orders and confirmations flow between the manufacturing execution system and the ERP through an integration platform whose agent sits in the plant and opens only outbound connections, so no inbound firewall rule crosses the operational boundary.

**Pitfalls.** Security zones: the operational network is separated from the corporate one, and every crossing needs a review. Time synchronization across devices. Data volume: filtering and aggregating at the edge cuts the stream to what is valuable. And the cultural gap between operational technology and IT teams, which delays more projects than any technical issue.

**Patterns used:** hybrid agent, event streaming, edge and store-and-forward, outbox, idempotent receiver.

## Case 6: Joiner, Mover, Leaver

A company with 20,000 employees provisions accounts manually. New hires wait days for access, and leavers' accounts linger for weeks, which auditors have noticed.

*[Figure: Case 6: the HR system is the source of truth, an identity provider provisions accounts and roles into applications through standard connectors, and a reconciliation finds orphan accounts.]*
**Design decisions.** The HR system is the *only* source of truth for who works at the company. An identity provider consumes HR events (hire, transfer, termination), and provisions, updates, and removes accounts and roles in applications through the SCIM standard where supported, and through connectors where not. Role assignment rules live in the identity provider, with approval workflows for sensitive roles. A daily *reconciliation* compares accounts in every application against the HR roster and reports orphans.

**Pitfalls.** Effective dating: a hire entered in October for a January start must not receive access in October. Rehires who return with new identifiers duplicate people. Leavers must lose access within hours, so the termination event has to be prompt and reliable, with a reconciliation as backstop. Attribute mappings differ per application.

**Patterns used:** identity provisioning, publish and subscribe, snapshot and diff, saga for multi-system provisioning.

## Case 7: Retail Supply Chain EDI

A retailer exchanges purchase orders, shipping notices, and invoices with several hundred suppliers using EDI, and onboarding a new supplier takes months.

*[Figure: Case 7: suppliers exchange X12 documents over AS2 or SFTP with a managed file transfer gateway, an EDI translator maps them to a canonical order model, and the ERP receives IDocs. Acknowledgments return automatically.]*
**Design decisions.** All partner traffic enters through a managed file transfer gateway in the DMZ. An EDI translator maps each partner's variant of the standard documents to a *canonical order model*, so the ERP sees one format regardless of partner, and the partner-specific variations are isolated at the edge. Acknowledgments (X12 997) return automatically, and an onboarding kit with test documents and a checklist shortens the partner queue.

**Pitfalls.** Partner-specific interpretations of the "standard." Certificate expiry for AS2, so a calendar and alerts for every partner certificate. And the long tail: the last fifty suppliers use obscure variants that need custom mapping.

**Patterns used:** B2B and EDI exchange, managed file transfer, canonical model, message translator, idempotent receiver.

## Case 8: A Modern Data Platform

A company is building a data platform that ingests from SaaS applications and operational databases, transforms the data in a lakehouse, and returns insights, such as customer scores, to operational tools.

*[Figure: Case 8: an ELT tool loads SaaS data; CDC and Kafka stream operational databases; transformations run in the lakehouse; reverse ETL pushes scores back to CRM and marketing; lineage events feed a catalog.]*
**Design decisions.** A managed ELT tool loads SaaS applications into the lakehouse's raw zone. Change data capture and Kafka stream operational databases. Transformation from raw to curated runs as versioned SQL models, with tests. Reverse ETL pushes customer scores and segments back into the CRM and marketing tools through their APIs. Every job emits lineage events to the data catalog, so analysts can see where a number came from.

**Pitfalls.** SaaS rate limits slow loads. Identity resolution (matching a warehouse customer to a CRM contact) decides whether reverse ETL works. Ownership of the *fields* that reverse ETL overwrites must be agreed with the CRM team. And lineage is only as good as the jobs that emit it.

**Patterns used:** scheduled ELT, change data capture, event streaming, reverse ETL, read-model replication.

## Case 9: Integrating a Data Catalog with the Estate

A company introduces a data catalog to govern its data, and needs it connected to databases, BI tools, process tools, and orchestrators, so that it reflects reality instead of becoming a stale spreadsheet.

*[Figure: Case 9: scanner agents harvest metadata and lineage from databases and BI tools; custom jobs and vendor packages use the catalog's REST import APIs; workflows create tasks that integrations poll; orchestrators emit lineage events.]*
**Design decisions.** Scanner agents inside the network harvest metadata and lineage from databases and BI tools, using outbound connections only. Custom jobs, and vendor-supplied packages, register and synchronize metadata through the catalog's REST import APIs, from ticketing systems, process tools, transformation tools, and API specifications. Catalog workflows create *user tasks* that integrations poll, so that a steward's approval can trigger actions elsewhere. Orchestrators and transformation tools emit lineage in the open lineage format.

**Pitfalls.** Naming and identity: matching an asset in the catalog to the object in the source depends on a consistent naming scheme, so the scheme is decided before the first scan. Permissions: an integration user that cannot see all assets silently synchronizes a subset. Ownership: a field edited both in the catalog and in the source needs an authority rule.

**Patterns used:** hybrid agent, polling with a watermark, asynchronous request-reply (bulk import), authority split, lineage events.

## What the Nine Have in Common

Read together, the cases share traits that are worth naming.

* **Boundaries were protected.** Anti-corruption layers, gateways, adapters, DMZ components, and edge gateways keep each system's model from leaking into the others.
* **Authority was explicit.** Every case answers "who owns this field?" and builds one-way flows where it can.
* **Asynchrony absorbed the shocks.** Queues, brokers, and logs sit between systems that fail at different times.
* **Idempotency appears everywhere.** Order numbers as external keys, event IDs, upserts, and acknowledgments make retries harmless.
* **A repair path accompanies every fast path.** Reconciliations, snapshot-and-diff jobs, and replay cover what real-time flows miss.
* **Ownership was named,** for topics, channels, accounts, and certificates, because an unowned component decays.

The cases differ in technology and domain; they agree on these habits. When you face a new situation, ask which of the six the design already has, and which is missing.

## Summary

Nine composite cases show patterns and platforms in situations: API-led order-to-cash, mainframe offload to Kafka, store-and-forward retail events through a mesh, HL7-to-FHIR translation in a hospital, factory data across security zones, joiner-mover-leaver provisioning, supply-chain EDI, a governed modern data platform, and a data catalog connected to a whole estate. Each shows how constraints shaped decisions and where the design later hurt.

Across the cases, boundaries were protected, authority was explicit, asynchrony absorbed failures, idempotency made retries harmless, every fast path had a repair path, and ownership was named. Those six habits are a better predictor of an integration's long-term health than any choice of product.

## Exercises

1. **Cover and compare.** Choose one case, cover the design decisions, and write your own. Compare, and note where the case's constraint changed the answer.
2. **Find the missing habit.** Score an integration of yours against the six shared habits. Which is missing?
3. **Adapt a case.** Take Case 2 and change one constraint, for example allowing changes to the core, or requiring the bank to run in two regions. What changes in the design?
4. **Write a tenth case.** Describe an integration from your experience in the same format: situation, design decisions, pitfalls, platform notes, and patterns used.



# Chapter 25. Capstone: Larkspur Outdoor

Every earlier chapter explains a piece. This chapter puts the pieces together on one realistic project, from the first meeting to the first incident after go-live, and shows the actual artifacts an architect produces along the way. The company and the numbers are fictional. The decisions, the problems, and the fixes are the ones real projects meet.

Read it twice. The first time, follow the story. The second time, close the book at the end of each stage, write down what *you* would produce, and compare. The exercise that turns knowledge into skill is the one in which you make the decisions yourself and then see how a design that reasoned from the same facts turned out.

> **In this chapter**
    * Follow one integration through eight stages: discovery, decisions, design, mapping and security, numbers, testing and cutover, hypercare, and estimation
    * See how the artifacts of earlier chapters (the brief, authority matrix, decision records, sequence diagrams, mapping specification, failure-injection results) fit together
    * Recognize how a daylight-saving incident exposes a flaw that testing missed, and how the team fixed it
    * Produce your own set of artifacts for a similar project

## The Situation

Larkspur Outdoor sells camping gear online in six countries. Orders from its commerce SaaS reach SAP S/4HANA through a nightly CSV export that staff fix by hand each morning. Customers complain that shipping updates arrive a day late. The chief operating officer wants orders in SAP within minutes and shipping status back on the web shop within the hour, before peak season in fourteen weeks.

You know this company from Chapter 1. Now we build the integration.

## Stage 1: Discovery

The team ran the workshops of Chapter 4, and recorded the critical answers together with the design consequence of each.

**Table: Larkspur's critical discovery answers and their design consequences**
| Critical question | Answer | Design consequence |
|---|---|---|
| Outcome and measure | 99% of orders in SAP within 5 minutes; shipping status on the shop within 30 minutes of shipment | Event-driven or near-real-time; freshness measured as a service-level objective |
| Cost of downtime | About 1,200 orders per hour at peak; an hour down means manual entry the next morning | A second availability tier; replay is required; business-hours plus peak on-call |
| Authority | The shop owns order capture and customer data; SAP owns price confirmation, fulfillment, and invoices | Two one-way flows; no conflict resolution needed |
| Identity | The shop's order number is unique; SAP assigns its own sales-order number | Store both; use the shop number as SAP's customer reference |
| Volume | 4,000 orders per day, 1,200 per hour at peak, 3 lines per order on average, 30% annual growth | About 0.33 orders per second at peak: modest |
| Source interfaces | Webhooks (signed, retried for 24 hours, no replay) and a REST API with an updated-since filter | Webhook plus a reconciliation pull |
| Target interfaces | SAP's sales-order OData API (the create call is not idempotent); business events for delivery and goods issue | Lookup before retry for creation; consume events for status |
| Network | SAP in the company data center, reachable from the cloud account over a private link; outbound internet only | The runtime lives in the cloud account; the webhook receiver sits behind the API gateway |
| Security | Personal data (names, addresses); a security review with four weeks of lead time | File the review in week one; mask personal data in logs |
| Platforms and skills | No integration platform; an existing managed Kafka used for analytics; a Python team | Code-first services on containers; publish order events to Kafka for analytics |
| Operations owner | The e-commerce platform team (business hours), on-call extended for peak | A runbook, with alerts to their channel |

Two answers shaped everything that followed: the **non-idempotent create call** in SAP, and the **webhook feed with no replay**. Both appear on the risk register of the brief in Chapter 4, with owners and dates.

## Stage 2: Decisions

Running the decision method of Chapter 9 with these answers ranks *webhook with a queue* first and *scheduled polling* close behind, the near-tie that signals a combination: webhooks for speed, a reconciliation pull every 15 minutes for completeness. The architecture recorded three decisions.

```text
ADR-001  Orders in: webhooks + queue + 15-minute reconciliation pull
  Because: 5-minute target; webhooks have no replay; the reconciliation
  repairs gaps; an outbound-only runtime can still poll.
  Rejected: polling only (load and latency at peak); CDC on the shop
  (SaaS, no database access).

ADR-002  Creating orders in SAP: OData API with lookup-before-retry
  Because: the create API is not idempotent; the shop order number stored
  as the customer reference lets us find an order SAP created before a
  timeout. Rejected: IDoc inbound (team skills, status-monitoring burden).

ADR-003  Code-first services on the existing container platform;
         order events to the existing Kafka
  Because: Python skills, no integration-platform license, Kafka already
  run by the data team. Revisit if more than five SaaS-to-SAP flows
  appear (then evaluate an integration platform).
```

Notice the "Rejected" lines. They are the part a successor will thank you for, and the "Revisit" line in ADR-003 turns a permanent verdict into a conditional one.

## Stage 3: The Design

the figure shows the architecture. It consists of two one-way flows: orders in, and status out, plus a stream of order events to Kafka for analytics.

*[Figure: The Larkspur architecture. Orders flow in through a webhook receiver, a queue, and a worker, with a reconciliation job as the repair path. Status flows back from SAP business events. Order events go to Kafka through an outbox for analytics.]*
**Orders in.** The commerce SaaS posts `order.created` to the **webhook receiver** (step 1). The receiver verifies the signature and timestamp, puts the event on the **order queue** (step 2), and answers at once. The **order worker** takes events from the queue (step 3), maps them (Chapter 12), checks its deduplication ledger, and creates the sales order in SAP through the OData API (step 4). Failure point A is the lost webhook: if the receiver was down during an outage, the event is gone, and *the reconciliation job* repairs it. Every 15 minutes the job lists orders from the shop updated since a watermark (step 5), compares them with what the ledger holds, and enqueues any missing orders (step 6).

**Status back.** SAP publishes a business event when goods are issued (step 7). The **status worker** consumes the event (step 8) and updates the order's status on the shop through its API (step 9). It is a second one-way flow, with SAP authoritative.

**Events for analytics.** The order worker writes order events through an **outbox** (step 10) to Kafka, and the status worker does likewise (step 11); the data platform reads them with a sink (step 12).

Failure point B in step 4 is the most important behavior in the design. the figure shows it.

*[Figure: The most important behavior: after a timeout, find before you create again.]*
The shop posts the event (step 1), the receiver enqueues it and acknowledges it (steps 2 and 3), and the queue delivers it to the worker (step 4). The worker asks the ledger whether it has seen order A1043 (step 5) and learns it has not (step 6). It then calls SAP to create the order, with the shop's order number as the customer reference (step 7), and *SAP commits the order, but the response times out*. The worker cannot tell whether the order exists. It does not retry the create. Instead, it asks SAP to *find an order by that reference* (step 8) and learns the order exists, with number 4500012 (step 9). It records the mapping (step 10) and moves on. The lookup-before-retry turns an API that cannot be called twice into one that can safely be retried. Never blindly re-POST.

## Stage 4: Mapping and Security

The mapping specification, in the format of Chapter 12, fixed the translation field by field.

**Table: Larkspur's order mapping to SAP**
| SAP field | Shop source | Rule |
|---|---|---|
| Sales order type | Constant | Online order type for the country (a code list per sales organization) |
| Sold-to party | `customer.email` | Look up the SAP business partner through a crosswalk; create a one-time customer if none exists (an approved rule) |
| Customer reference | `order.number` | Copy; used for the duplicate lookup |
| Material | `line.sku` | Crosswalk the SKU to a material number; quarantine if missing |
| Quantity, price | `line.qty`, `line.price` | Decimals; SAP confirms the price, and the shop's price is kept for comparison |
| Requested delivery date | `order.created_at` | Convert to the plant's local date |

The threat discussion (Chapter 27) found four concerns and a control for each. *Forged webhooks:* HMAC signature plus a timestamp window. *Personal data in logs:* masking in the logging library. *An over-privileged SAP account:* a communication user limited to creating and reading sales orders. *Replay of old webhooks:* the timestamp window and the deduplication ledger.

## Stage 5: The Numbers

**Table: Capacity and budget checks**
| Check | Arithmetic | Result |
|---|---|---|
| Peak throughput needed | 1,200 orders per hour, growing 30% a year for two years, gives about 2,000 per hour | 0.56 orders per second |
| SAP capacity measured in test | One worker creates 2 orders per second with 3 lines each | Two workers give more than 6 times headroom |
| Shop API budget | The reconciliation reads about 300 orders per 15 minutes at peak in 3 pages; status updates 1,200 per hour | Well within the 4 requests per second allowance |
| Outage tolerance | A 4-hour SAP maintenance window at 1,200 orders per hour | 4,800 queued messages, drained in about 40 minutes by two workers |

The last row is reassuring and was worth computing: a four-hour outage does not need heroic measures, because two workers clear the backlog in under an hour.

## Stage 6: Tests, Cutover, and Go-Live

The team ran the failure-injection matrix of Chapter 16: SAP timeouts after commit, duplicate webhooks, a SKU missing from the crosswalk, token expiry, and a four-hour SAP outage replayed at five times speed. They ran a **shadow run** for two weeks in pre-production, in which the new path created orders in a scratch sales organization and a daily report compared them with the output of the nightly CSV path.

Cutover (Chapter 28) was **phased by country**: the two smallest countries first, the largest in week three, with the CSV export kept as a fallback until the rollback window closed. They defined five service-level indicators and alerts: freshness (95th-percentile order-to-SAP time under five minutes), quarantine rate above one percent, queue age above fifteen minutes, reconciliation drift above zero, and a heartbeat for each worker.

## Stage 7: What Actually Went Wrong in Hypercare

> **Incident: orders missing on the night of a daylight-saving change**
    The reconciliation job asked the shop for orders updated since its watermark minus two minutes, but computed the watermark in *local time*, while the shop filtered in UTC. On the night the clocks changed, an hour of orders fell outside the window, and their webhooks had been dropped by a gateway restart. The freshness alert fired at 07:10; the team reran the reconciliation with a wider window, and all orders reached SAP by 08:00.

    **Fix:** timezone-aware UTC watermarks everywhere, a 15-minute overlap, a test case for daylight-saving transitions, and a nightly full-day reconciliation as a second safety net.

Study how the incident unfolded. *Two* defenses failed at once: the webhook (the fast path) lost events during a gateway restart, which was expected, and the reconciliation (the repair path) had a time-zone defect, which was not. Because the *freshness alert* existed, the problem was detected within hours, by a machine, and resolved within one morning. Had the team relied on "someone would notice," the orders would have sat in the shop until customers complained. The lessons are the ones of earlier chapters: unlabeled times break watermarks (Chapter 12), overlap windows must be computed from the *source's* clock (Chapter 14), and measurable freshness turns incidents into alerts.

## Stage 8: The Estimate That Was Approved

Using the estimation method of Chapter 28, the team counted three entities (orders, order status, a customer crosswalk), two systems plus Kafka, OAuth, a private link already in place, one-way flows, medium volume, freshness in minutes, some data-quality issues, medium criticality, a standard review, some platform experience, and three environments. The result was size L, with a range of about 45 to 75 person-days. Elapsed time was eleven weeks, driven not by development but by the security review and the shadow run, and delivery came three weeks before peak.

## The Artifacts This Project Produced

Count what exists at the end, apart from the code:

* the integration brief and discovery checklist (Chapter 4);
* the authority matrix and two reconnaissance sheets (Chapters 4 and 10);
* three decision records (Chapter 9);
* architecture and sequence diagrams (Chapters 7 and 8);
* the mapping specification and golden-file tests (Chapter 12);
* a threat summary (Chapter 27);
* the test plan and failure-injection report (Chapter 16);
* the cutover plan, the runbook, and the alert catalog (Chapters 28 and 26);
* the service-level dashboard, and a post-incident review (Chapter 26).

Templates for all of them are in Appendix D. A project that ends with this list is one that can be handed over, audited, and extended; one that ends only with code is one whose knowledge lives in people's heads.

## Summary

The Larkspur project followed the journey of Chapter 3. Discovery produced eleven critical answers, two of which, a non-idempotent create call and a webhook feed without replay, shaped the design. The decision method pointed to a combination of a webhook and a reconciliation pull, recorded in three decision records with rejected alternatives and revisit conditions. The design consisted of two one-way flows with a repair path, a lookup before retry for the create call, and an outbox for analytics events.

A mapping specification and a threat discussion followed; capacity arithmetic confirmed headroom; failure injection, a shadow run, and phased cutover reduced risk. A daylight-saving defect in the reconciliation job surfaced in hypercare and was caught by a freshness alert within hours. The estimate was a size L, about 45 to 75 person-days, and the project's real critical path was the security review and the shadow run.

## Exercises

1. **Make the decisions yourself.** Close the book after Stage 1 and write your own three decisions. Compare them with ADR-001 to ADR-003. Where did you differ, and why?
2. **Find the second incident.** Imagine another failure in hypercare: SAP's business events stop arriving. Which alert would fire, which would not, and what would you add?
3. **Remove a safeguard.** Remove the reconciliation job from the design. List the failure modes that would then go undetected.
4. **Adapt it.** Rewrite Stages 2 and 3 for a company whose shop offers webhooks *with* replay and whose ERP accepts idempotency keys. What can you drop?



---

# Part VI. Operate, Secure, Govern

Keeping integrations reliable and observable, secure by design, recoverable, and governed as an estate rather than a pile of projects.



# Chapter 26. Reliability and Observability

An integration that works is not the same as an integration you can rely on. The first is a statement about a moment; the second is a statement about months of operation, through outages, deployments, expired certificates, and upstream changes. Reliability is the discipline of designing for the unreliable world in which integrations actually live, and observability is the discipline of *knowing* what is happening, so that you hear about a problem from your own alert and not from a customer.

This chapter assembles the reliability toolkit that earlier chapters introduced piece by piece, and adds what they did not cover: how to follow one transaction across queues and systems with traces, how to define service-level indicators and objectives for an integration, how to design alerts that people act on, and how to write the runbook that makes the difference between a three-minute and a three-hour incident.

> **In this chapter**
    * Combine timeouts, retries, idempotency, circuit breakers, bulkheads, backpressure, dead letters, and reconciliation into a reliability design
    * Instrument an integration with logs, metrics, and traces, and propagate trace context across asynchronous hops
    * Define service-level indicators and objectives for freshness, completeness, correctness, and headroom
    * Design alerts that are symptom-based, owned, and actionable
    * Write a runbook that someone other than the author can execute

## The Reliability Toolkit

Reliability for integrations comes from a small set of mechanisms, each answering a specific failure. the table collects them, with where each is described in this book.

**Table: The reliability toolkit**
| Mechanism | The failure it answers | Where described |
|---|---|---|
| Timeouts | A call that hangs forever | Chapter 14 |
| Bounded retries with backoff and jitter | Transient errors; retry storms | Chapter 14 |
| Idempotency | Duplicates from retries and redelivery | Chapters 1, 14, 15 |
| Circuit breaker | A failing dependency that is hammered | Chapter 8 |
| Bulkhead | One slow dependency exhausting shared resources | This chapter |
| Backpressure | A producer faster than a consumer | Chapters 18 and 20 |
| Dead letter queue and quarantine | Poison messages and bad records | Chapters 7 and 19 |
| Checkpoints | Crashes mid-run | Chapter 14 |
| Reconciliation | Drift from every cause | Chapter 15 |
| Replay | A bug that corrupted data | Chapters 18 and 28 |

Two are new to this chapter, or deserve a fuller treatment.

**Bulkheads.** A ship's bulkheads keep a leak in one compartment from sinking the whole vessel. In software, the idea is to give each dependency its own *limited* pool of resources, such as threads, connections, and queue capacity, so that when one slows down it exhausts only its own pool. Without bulkheads, a slow ERP can consume every worker thread, and the integration that has nothing to do with the ERP stops too. In practice: separate worker pools or queues per target system, and a cap on concurrent calls to each.

**Backpressure.** When a producer can outrun a consumer, something must give. Either the producer is slowed (backpressure), or the data accumulates somewhere (a queue or log, which is a deliberate buffer), or it is dropped (data loss). Good designs choose the first two on purpose: a pull-based consumer simply stops pulling; a webhook receiver answers 429 or 503 so the sender slows down; and queues are sized and monitored so that "the buffer is filling" is an alert, not a surprise.

> **Why this matters**
    Reliability mechanisms work in *combination* and fail in combination. A retry without backoff hammers a target; backoff without a circuit breaker still wastes threads; a circuit breaker without a dead letter path discards messages; a dead letter queue without an owner is data loss with extra steps. Review a design by asking, for each failure in the table, which mechanism answers it, and who watches that mechanism.

## Observability: Knowing What Is Happening

An integration is almost always invisible when it works. **Observability** is the practice of making its behavior knowable through three kinds of evidence: *logs* (what happened), *metrics* (how much and how fast), and *traces* (how one transaction moved through the system).

### Logs

Logs should be *structured*, with every line a set of named fields, as Chapter 14 showed, so they can be searched and counted. Every line carries a run ID, a trace ID, and the entity ID; outcome and reason are fields rather than prose; and no line carries a secret or unmasked personal data.

### Metrics

Metrics are numbers over time, cheap to store and fast to alert on. For an integration, the essential ones are throughput (records per minute in and out), error counts by class, latency of calls to each dependency, queue depth or consumer lag, the age of the oldest unprocessed item, quarantine counts, and the time since the last successful run.

### Traces

Logs tell you what one component did; a **trace** tells you what happened to one business transaction across all of them. Integrations break traces at every queue and topic, because the receiving side has no idea which transaction a message belongs to, unless the context travels *with* the message. The W3C Trace Context standard defines a `traceparent` header (for example `00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01`, holding a version, a trace ID, a parent span ID, and flags), and OpenTelemetry propagates it over HTTP and, with a few lines of code, over message headers. the figure shows the idea.

*[Figure: Inject the trace context when you send; extract it when you receive. The result is one trace from the webhook to the analytics consumer.]*
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

An integration needs measurable goals, or "reliable" means whatever the loudest stakeholder says it means. A **service-level indicator** (SLI) is a measurement; a **service-level objective** (SLO) is a target for it. the table lists the indicators that suit integrations.

**Table: Service-level indicators and example objectives for an integration**
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



# Chapter 27. Security and Threat Modeling

Integrations are attractive targets. They hold credentials that open several systems. They sit on network paths that cross trust boundaries. They move data in bulk. And they are often built quickly, owned vaguely, and reviewed late. An attacker who compromises an integration's service account may reach everything that account can reach, in every system it connects, often with more privilege than any single human user.

This chapter gives you a practical approach to integration security: a way of thinking, threat modeling, that finds problems early; a map of the most relevant risks, using the OWASP API Security list; and the controls for data protection, supply chain, and the review process itself. It is deliberately practical. A security review of an integration should take days, not weeks, if you arrive with the right evidence, and the review pack at the end of the chapter says what that is.

> **In this chapter**
    * Draw a data-flow diagram with trust boundaries and apply STRIDE to it
    * Map the OWASP API Security Top 10 (2023) to integrations, and name the control for each risk
    * Choose controls for spoofing, tampering, repudiation, information disclosure, denial of service, and privilege escalation
    * Protect data in flows through minimization, classification, masking, retention, and erasure
    * Reduce supply-chain risk from dependencies, connectors, and packages
    * Prepare a security review pack that shortens approval

## Threat Modeling an Integration

A **threat model** answers four questions: what are we building, what can go wrong, what are we going to do about it, and did we do a good enough job? For an integration, the exercise takes about an hour and has a fixed shape. *Draw the data flow, with its trust boundaries. Walk every element and every flow through the STRIDE categories. Rank what you find. Give each threat a control and an owner.*

the figure shows a data-flow diagram of a typical integration, with the trust boundaries marked as dashed regions.

*[Figure: Trust boundaries of an integration. Every arrow that crosses a dashed boundary needs authentication, integrity protection, and a decision about what may be logged.]*
A partner or SaaS application on the *internet* sends requests to an API gateway with a web application firewall in the *DMZ*. The gateway passes validated requests to the integration service in the *internal network*, which fetches its secrets from a vault, calls internal systems with least-privilege credentials, and writes masked logs to a monitoring system. Failure points mark the threats: spoofing, replay, and flooding at the first boundary (A); elevation if the service account holds more privilege than it needs (B); and disclosure of personal data through logs (C).

The value of the diagram is that it forces you to find every place where data crosses a boundary. Each crossing needs three things: *authentication* (who is on the other end?), *integrity protection* (was it altered in transit?), and a decision about *what may be logged or stored there*.

## STRIDE

STRIDE, devised at Microsoft, is a mnemonic for six categories of threat. Walking each element and flow through the six categories prompts the questions that experience would otherwise have to supply.

**Table: STRIDE applied to integrations**
| Category | How it shows up in integrations | Typical controls |
|---|---|---|
| **S**poofing | Forged webhooks; stolen service-account credentials; a fake partner endpoint | HMAC signatures with timestamps; mutual TLS or OAuth; credential rotation; endpoint verification |
| **T**ampering | Modified payloads in transit or in file drops; replayed messages | TLS; signed payloads; checksums and manifests; deduplication by event ID; timestamp windows |
| **R**epudiation | "We never sent that order"; shared accounts hide who changed what | Dedicated identities; immutable audit logs; acknowledgments; signed B2B messages |
| **I**nformation disclosure | Personal data in logs, quarantine files, dead letter queues, broadly readable topics, vendor clouds | Data minimization; masking; field-level encryption; topic ACLs; retention limits; approved regions |
| **D**enial of service | Retry storms; unbounded batches; floods on a public receiver; quota exhaustion that blocks other integrations | Rate limits; backoff with jitter; circuit breakers; payload size limits; separate quotas |
| **E**levation of privilege | Administrator service accounts; missing object-level checks; agent tools with write access | Least privilege; separate read and write identities; object-level authorization; human approval for agent writes |

A useful prompt for each flow is simply to say the six words aloud: *Could someone pretend to be this? Change it? Deny they did it? Read it? Stop it? Gain more power through it?* Most flows have two or three real threats among the six, and the exercise is to find them before an attacker does.

## The OWASP API Security Top 10

The OWASP API Security Top 10 is the standard list of the most serious API risks. The 2023 edition was the most recent API list when this was written; OWASP's separate Top 10 for web applications was updated in 2025, and the two lists should not be confused. Most items concern *authorization*, which is exactly where integrations are weakest, since they often run with broad service accounts. the table maps each risk to an integration's concerns.

**Table: The OWASP API Security Top 10 (2023) through an integration lens**
| Risk | Integration angle | Control |
|---|---|---|
| API1: Broken Object Level Authorization | An integration or partner reads another tenant's or customer's record by changing an ID | Check ownership on every object access, also for machine clients |
| API2: Broken Authentication | Long-lived keys, tokens in URLs, weak webhook verification | Short-lived tokens, signatures, no secrets in URLs, lockout monitoring |
| API3: Broken Object Property Level Authorization | Responses expose fields the consumer should not see; mass assignment through writes | Explicit request and response schemas per role; reject unknown writable fields |
| API4: Unrestricted Resource Consumption | Bulk endpoints and integrations without limits exhaust shared capacity | Quotas per client, page-size caps, timeouts, cost-aware limits |
| API5: Broken Function Level Authorization | An integration user can call administrative functions | Role design per integration; deny by default |
| API6: Unrestricted Access to Sensitive Business Flows | Automated abuse of flows such as order creation or refunds | Business-level rate limits, anomaly detection, approvals |
| API7: Server-Side Request Forgery | The integration follows a URL from a payload or webhook and reaches internal systems | Allowlist outbound destinations; block internal address ranges |
| API8: Security Misconfiguration | Verbose errors, permissive CORS, TLS verification disabled to get past a proxy | Hardened defaults, configuration review, never disable verification |
| API9: Improper Inventory Management | Forgotten test endpoints, old API versions, and abandoned integrations still live | An inventory of integrations and APIs with owners; retire what is unused |
| API10: Unsafe Consumption of APIs | Trusting data from third-party APIs more than user input | Validate, size-limit, and time-limit everything received from partners and vendors |

Two of these deserve a closer look because they are easy to miss from the integrator's side of the fence. **API7, server-side request forgery,** arises when an integration fetches a URL that arrives in data, for example a webhook payload that contains a "callback URL" or an attachment link. An attacker supplies an address inside your network, and your integration, which sits behind the firewall, obligingly fetches it. Never fetch arbitrary URLs from payloads; allowlist the destinations. **API10, unsafe consumption,** is the habit of trusting a partner's or vendor's response because it comes from a "known" source. Treat everything received from outside as untrusted input: validate its shape, limit its size, and set time limits, as Chapter 12 recommends for any record.

## Data Protection in Flows

Moving data is the integration's reason for existing and its principal source of exposure. Seven principles govern how to move it responsibly.

**Table: Principles of data protection in flows**
| Principle | In practice |
|---|---|
| Minimize | Move only the fields the target needs; challenge "send everything" |
| Classify | Tag each field (public, internal, confidential, personal, special category); classification drives logging and storage rules |
| Protect in motion and at rest | TLS everywhere; encrypted queues, topics, buckets, and quarantine folders |
| Mask and tokenize | Mask in logs and test data; tokenize identifiers before they reach broadly readable topics |
| Retain deliberately | Set retention per store (topics, dead letter queues, quarantine, logs) aligned with policy |
| Erase across copies | Propagate deletion requests; for immutable logs, use per-subject keys so that destroying the key erases the data (crypto-shredding) |
| Respect residency | Know where every component processes and stores data, including vendor control planes |

The principle most often broken in practice is the *copies*. A customer's record may exist in the source, the target, a queue, a dead letter topic, a quarantine file, a log, a backup, and a developer's test dataset. A deletion request or a retention policy must reach them all. Make an inventory of where each class of data lands, and give each store a retention rule. Pay particular attention to the places that nobody thinks of as data stores: quarantine folders, dead letter queues, and debug logs.

## Supply-Chain and Platform Hygiene

An integration is built from components written by others: libraries, connectors, container images, and packages, and each is a path for compromise.

* **Pin and scan dependencies.** Lock versions, scan for known vulnerabilities in every build (Chapter 17), and keep a software bill of materials for each integration.
* **Vet connectors and packages before use.** Who maintains them? What permissions do they need? How do they store credentials? A packaged integration that keeps passwords in a plain configuration file is a template to be hardened, not a product to be deployed.
* **Patch on a schedule.** Runtimes, agents, and gateways need updates; monitor vendor security advisories.
* **Separate duties.** The person who writes a flow should not be the only one who can promote it to production.

## A Threat Checklist

When you need a faster start than a full threat model, tick the characteristics that apply to your integration and discuss the corresponding threats with your security team. the table lists the characteristics, the threats each brings, and the controls to propose.

**Table: Characteristics and the threats to discuss**
| If the integration... | Discuss these threats | Propose these controls |
|---|---|---|
| Exposes a public endpoint | Forged requests; flooding or oversized payloads; replay of captured requests | HMAC signatures with a timestamp window or mutual TLS; gateway rate limits and a WAF; payload size limits; accept-then-queue; a deduplication ledger |
| Moves personal or regulated data | Personal data in logs, quarantine, and test copies; more fields moved than needed | Masking; encrypted stores with retention; synthetic test data; field minimization reviewed with the privacy owner |
| Connects partners | Impersonated partners and expired certificates; disputes about what was sent; one partner reading another's data | mTLS or signed tokens per partner; a certificate inventory with expiry alerts; signed messages and acknowledgments; object-level authorization |
| Uses long-lived or shared credentials | Stolen keys reused; shared accounts hiding who did what | OAuth or mutual TLS; a vault; rotation; one identity per integration |
| Follows URLs from payloads | Server-side request forgery | An allowlist of outbound hosts; block private and metadata address ranges |
| Consumes third-party APIs | Unsafe consumption; a slow vendor stalling your flows | Validate everything received; timeouts; circuit breaker; a bulkhead per dependency |
| Publishes to shared topics | Any consumer reads sensitive events; a rogue producer writes bad events | Topic ACLs; tokenized identifiers; producer ACLs; schema validation |
| Is processed in a vendor-hosted platform | Data outside approved regions; vendor staff access | Confirm regions, sub-processors, and the data processing agreement; customer-managed keys where offered |
| Exposes tools to AI agents | Writes nobody approved; prompt injection through tool results; data exposed to users who should not see it | Read-only tools by default; human approval for writes; scoped credentials; treat tool output as untrusted; enforce the end user's permissions |
| Exchanges files | Tampered or partial files; files readable by too many accounts; malware in received files | Checksums and manifests; write-then-rename; per-integration bucket policies; scanning on arrival |
| Runs on a person's delegated grant | Access tied to a person who leaves; a stolen refresh token | A service identity for unattended jobs; a vault; revocation on offboarding |
| Uses an administrator account | A large blast radius if credentials leak; bulk mistakes | Scope down; separate read and write identities; a kill switch and dry-run mode |

Always add the baseline: TLS everywhere, secrets in a vault, least privilege, and dependency scanning.

## Network Security by Topology

Chapter 5 described seven topologies. Each raises its own security questions, which belong on the review agenda.

*[Figure: An integration agent on a customer server makes outbound calls only. This is the simplest pattern to approve: the firewall needs only the existing outbound rules, and no inbound path to the data center is opened.]*
For an **outbound agent**, ask what the agent can reach inside the network, how it is authenticated to the control plane, who patches it, and what data it logs. For a **private link**, ask who can route into it, and what segments it connects. For an **event backbone**, ask who may produce and consume each topic. For **partner connectivity**, ask which IP ranges and certificates are allowed, and how an incident with one partner is contained. For **edge sites**, ask how device identities are issued, rotated, and revoked. And for every topology, ask where *logs* go, since they cross boundaries too.

## The Security Review Pack

Arrive at the security review with the evidence the reviewers need and they will approve in days. The pack contains the following.

* A **data-flow diagram** with trust boundaries marked.
* **Data classification** per field, and where each class lands (stores, logs, topics).
* **Identities and permissions** per system, showing least privilege.
* **Secret storage and rotation**: where secrets live, who rotates them, and how often.
* The **network path** and any firewall changes required.
* The **threat table** (STRIDE) with controls and owners, and accepted residual risks.
* **Logging and retention rules.**
* The **vendor and sub-processor list**, with regions.
* **Test evidence**: signature checks, authorization tests, a dependency scan.

The pack also makes the lead time visible: if the security review takes four weeks, the request is filed on day one (Chapter 3), with this pack following as the design matures.

## Summary

Integrations hold powerful credentials, cross trust boundaries, and move data in bulk, which makes them attractive to attackers. A threat model draws the data flow with trust boundaries, and walks each element and flow through STRIDE: spoofing, tampering, repudiation, information disclosure, denial of service, and elevation of privilege. The OWASP API Security Top 10 (2023), concerned mostly with authorization, maps closely to integration weaknesses, notably object-level authorization, server-side request forgery, and unsafe consumption of third-party APIs.

Data protection means minimizing, classifying, encrypting, masking, retaining deliberately, erasing across all copies, and respecting residency, with special attention to quarantines, dead letter queues, and logs. Supply-chain hygiene pins and scans dependencies and vets packages. A checklist of characteristics gives a fast start on threats and controls, each topology has its own questions, and a prepared security review pack converts a weeks-long review into a few days.

## Exercises

1. **Draw and walk.** Draw the data flow of an integration you know, mark the trust boundaries, and apply the six STRIDE prompts to each crossing. Which threat surprised you?
2. **Find the copies.** List every place a customer's email address lands as it passes through one integration, including logs, queues, and quarantine. What is the retention of each?
3. **Test object-level authorization.** For an API you offer or use, request a record that belongs to a different tenant with valid credentials of your own. What happens?
4. **Prepare the pack.** Assemble the nine items of the security review pack for a real integration. Which is hardest to produce, and why?



# Chapter 28. Recovery, Cutover, Capacity, and Estimation

Four questions remain after a design is chosen and secured, and they are the ones that executives ask. What happens if it all goes down? How do we switch from the old way to the new one without a disaster? Will it be big enough, and fast enough, for the load it will actually carry? And how long will it take, and what will it cost?

These are questions about *numbers* and *plans*, and they reward the habit of doing arithmetic early. This chapter covers recovery in terms the business can agree to, five cutover strategies and when each fits, the capacity arithmetic that decides whether a design is feasible, and an estimation method that gives a defensible range rather than a single optimistic figure. It ends with a view of cost over three years, because the cheapest integration to build is rarely the cheapest to own.

> **In this chapter**
    * Define recovery objectives with the business, and map failure scenarios to responses
    * Choose among five cutover strategies, and plan a parallel run with a delta feed
    * Do the capacity arithmetic that tests throughput, API budgets, and outage recovery
    * Estimate effort with a transparent method that produces a range, and state its assumptions
    * Model three-year cost, including the cost of leaving

## Recovery in Terms the Business Can Agree To

Two terms anchor every discussion of recovery. The **recovery point objective** (RPO) is how much data you can afford to lose, measured as time: "up to five minutes of orders." The **recovery time objective** (RTO) is how long you can afford to be down: "back within one hour." They are business decisions, not technical ones. The architect's job is to turn them into designs and costs, and to make the trade-off visible: a smaller RPO and RTO cost progressively more.

**Table: Illustrative resilience tiers to agree with the business**
| Tier | Typical RPO | Typical RTO | What it implies |
|---|---|---|---|
| 1: Business stops | Near zero | Minutes | Active-active or synchronous replication; automated failover; round-the-clock on-call |
| 2: Significant impact | Minutes | An hour or so | Replicated state; warm standby; replay from durable queues; extended on-call at peaks |
| 3: Inconvenient | Hours | A day | Backups and rebuild from code; business-hours support |
| 4: Best effort | A day | Days | Redeploy and reprocess; minimal operational machinery |

The figures are illustrations to start a conversation, not standards. The conversation is what matters: ask the business owner what an hour of outage costs (a discovery question from Chapter 4), propose a tier, show what it costs, and record the decision.

### What Must Survive

Recovery fails most often because something essential was not backed up or was backed up in an unusable form. For an integration, the state that must survive a failure is short and specific: the **watermarks and checkpoints** (or the integration will re-read everything or skip data); the **deduplication ledger** (or replays create duplicates); the **crosswalk** of identifiers between systems; the **configuration** and mapping tables, which belong in version control; the **queues and topics** whose contents represent undelivered work; and the **secrets and certificates**, with a procedure for reissuing them. Write the list for each integration, with where each item lives and how it is restored.

### Failure Scenarios and Responses

**Table: Failure scenarios and planned responses**
| Scenario | Detected by | Response | Verified by |
|---|---|---|---|
| The target system is down for hours | Freshness alert; breaker open | Queue absorbs work; pause consumers; resume after recovery | Queue drains; reconciliation clean |
| The integration runtime is lost | Heartbeat alert | Redeploy from the pipeline; restore checkpoints; replay from the last good point | No gaps or duplicates after restart |
| A certificate or credential expires | Expiry alert (60 days ahead); 401 alerts | Rotate using the documented procedure | Calls succeed; no extra token requests |
| Bad data is written to the target | Reconciliation drift; business report | Stop with the kill switch; scope from logs; run a corrective job | Drift returns to zero |
| A region is lost | Platform alerts | Fail over per the multi-region design (Chapter 19) | Smoke tests; reconciliation after failback |
| The source changes its API | Contract test; quarantine alert | Pin the version; adapt the mapping | Contract tests pass |

A plan that has never been rehearsed is a hope. Rehearse the scenarios at least once, in a test environment, and record how long each took.

## Cutover and Migration Strategies

A new integration usually replaces an old one, and the moment of replacement is the riskiest part of the project. the table compares five strategies.

**Table: Five cutover strategies**
| Strategy | How it works | Best when | Risk |
|---|---|---|---|
| Big bang | Switch everything at once, at a scheduled time | Small scope; a clean window; easy rollback | Everything is at stake at once; rollback may be hard |
| Phased by region or entity | Move groups one at a time | Many independent units; the capacity to learn from the first group | A long coexistence period with two systems to run |
| Parallel run | Run old and new side by side, compare, and then switch | High criticality; need for proof | Cost of running both; reconciling the differences |
| Pilot or canary | Move a small, representative slice first | Uncertainty about real-world behavior | The slice may not be representative |
| Strangler (gradual) | Route more traffic to the new system over time | Replacing a large legacy system | Data synchronization between old and new; defining the end |

Most important integrations use a parallel run, often combined with phasing. the figure shows a timeline.

*[Figure: A parallel-run cutover. The delta feed starts before the switch so the new system is never behind, and the old path is retained until the rollback window closes.]*
The sequence has a particular logic. The initial bulk load copies history into the new system. A **delta feed**, which carries changes made since the load began, starts *before* the switch, so that the new system is never behind. For a period, both paths run and a daily comparison shows where they differ. When the comparison is clean for an agreed period, traffic switches, and the old path remains available as the *rollback* until the rollback window closes. Only then is the old path retired. Each step has a criterion, expressed as a number: for example, "no differences for seven consecutive days" before the switch, and "no rollback in thirty days" before retirement.

> **Write the rollback before the cutover**
    For every cutover, write down the *exact steps* to return to the old path, who decides, and what has to be true for the decision to be safe. A rollback plan that depends on data the cutover has already changed is not a plan. Rehearse it.

## Capacity and Performance Arithmetic

Many feasibility questions can be answered with arithmetic that takes minutes. Do it early, aloud, and write down the assumptions.

**Throughput.** If 5,000,000 rows must move in a 2-hour window of 7,200 seconds, the job must sustain about 700 rows per second. Is that possible with one call per row, at the target's per-call time? If each call takes 150 ms with four parallel workers, throughput is about 27 calls per second, which is 26 times too slow, so the design needs a bulk path.

**API budgets.** Divide the allowance by the number of integrations that share it, and leave headroom. 600 requests per minute shared by three integrations is 200 each; at 70 percent use, 140 per minute, or about 2.3 per second.

**Outage recovery.** A four-hour outage at 1,200 orders per hour accumulates 4,800 messages. At 2 orders per second per worker and two workers, the backlog drains at 4 per second, in 1,200 seconds, or 20 minutes (and, with live traffic arriving at 0.33 per second, a little longer).

**Storage.** For a Kafka topic or a quarantine store, multiply ingest rate, retention, and replication, as in Chapter 19.

**Latency.** Multiply the round-trip time by the number of sequential calls, as in Chapter 5. A hundred sequential calls at 80 ms is eight seconds.

> **Why this matters**
    A fifteen-minute calculation can invalidate a design that would take three months to discover to be infeasible. The arithmetic also builds credibility: a stakeholder who sees you derive "this cannot work with one call per record" in front of them is far more likely to accept the more complex design.

## Estimating Effort

Estimation is the art of being usefully wrong. A single number invites a promise; a *range with stated assumptions* invites a conversation. The method below is deliberately simple and transparent. It is a **rule of thumb, uncalibrated**: its constants are the author's judgment, and you should adjust them against your own past projects.

**Step 1: a base.** Start with 10 person-days for design, setup, and handover, plus 5 person-days for each entity that must be mapped and synchronized, plus 8 person-days for each system beyond the first two.

**Step 2: multiply by complexity factors.** Each characteristic of the project adds a factor, and the factors multiply.

**Table: Illustrative complexity factors**
| Characteristic | Factor |
|---|---|
| Volume: medium (high) | 1.05 (1.20) |
| Freshness: minutes (seconds) | 1.10 (1.25) |
| Data quality: some issues (poor) | 1.15 (1.30) |
| Criticality: medium (high) | 1.10 (1.20) |
| Security review: standard (heavy) | 1.05 (1.15) |
| Team platform experience: some (none) | 1.10 (1.25) |
| Direction: two-way | 1.40 |
| Authentication: legacy or certificate-based | 1.15 |
| Network: new private link required | 1.20 |
| Environments: four or more | 1.10 |

**Step 3: state the range.** Multiply the result by 0.8 and by 1.35 to give a low and a high figure, and map the midpoint to a size: small below 15 person-days, medium 15 to 40, large 40 to 80, extra large above 80.

For Larkspur (Chapter 25), the base is 10 + (3 entities × 5) + (1 extra system, Kafka, × 8) = 33 person-days. The factors that apply are medium volume (1.05), freshness in minutes (1.10), some data-quality issues (1.15), medium criticality (1.10), a standard security review (1.05), and some platform experience (1.10), which multiply to about 1.69. The midpoint is therefore about 56 person-days, the range 45 to 75, and the size *large*.

Three cautions apply. The elapsed time is not the effort divided by the team size: Larkspur's elapsed time of eleven weeks was set by the security review and the shadow run, not by the build. The estimate must list its *assumptions* (what is in scope, what is already in place), because a changed assumption changes the number. And the method should be *calibrated*: after each project, compare the estimate with the actual and adjust the constants.

## Three-Year Cost

The build cost is the visible part of the bill. A three-year view includes the rest.

**Table: Components of a three-year cost view**
| Component | Includes |
|---|---|
| Build | Effort from the estimate, at the loaded daily cost |
| Licenses and platform | Subscription or license fees; per-task or per-call charges at the *year-three* volume |
| Infrastructure | Compute, storage, network, and data transfer (egress between clouds can dominate) |
| Operations | On-call, monitoring, incident handling, patching, certificate renewal |
| Change | Adapting to API changes, new fields, new consumers |
| Exit | The cost of migrating away, or retiring the integration |

Two habits improve such models. Model *year three's volume*, not year one's, because per-unit pricing can grow faster than volume. And include **exit cost** explicitly: lock-in is a cost that does not appear until you try to leave.

## Summary

Recovery begins with objectives the business agrees to, a recovery point and a recovery time, matched to a resilience tier and its cost. The state that must survive is short and specific: checkpoints, the deduplication ledger, the identifier crosswalk, configuration, queues, and secrets. Failure scenarios should be mapped to detection, response, and verification, and rehearsed.

Five cutover strategies, big bang, phased, parallel run, pilot, and strangler, suit different risks, and most important integrations use a parallel run with a delta feed and numeric criteria for switching and for retiring the old path, with the rollback written and rehearsed in advance. Capacity arithmetic on throughput, API budgets, outage backlog, storage, and latency settles feasibility in minutes. An estimate is a range with assumptions, built from a base and complexity factors and calibrated against actuals. A three-year view includes licenses at year-three volume, operations, change, and the cost of exit.

## Exercises

1. **Set the objectives.** For an integration, propose an RPO and an RTO and a tier. What would the business owner say it costs them per hour? What would your proposal cost?
2. **Plan a cutover.** Write the criteria, as numbers, for each of the four steps of a parallel-run cutover: start the delta feed, begin the parallel run, switch, retire.
3. **Do the arithmetic.** A job must update 2 million records in a 4-hour window against an API that allows 8 calls per second. Is one call per record feasible? What would you do?
4. **Estimate it.** Apply the method to a project you know. State the assumptions, give the range, and compare with the actual effort if the project is complete.



# Chapter 29. Governance and the Operating Model

One integration is a project. A hundred integrations are an estate, and an estate behaves differently from a project. Without an operating model, estates grow into duplicate flows that do the same thing three ways, forgotten credentials that nobody dares revoke, failures that no one owns, and five overlapping platforms bought by five departments. Each integration was sensible when it was built; together they form something no one understands.

This chapter describes how to run integration as a *capability* rather than a series of projects: who does what, how requests flow, which standards matter, how the estate is inventoried and measured, and how data contracts and lineage tie integrations into data governance. It is the chapter for people who will set standards and shape teams, and the background for everyone else on why the standards they meet exist.

> **In this chapter**
    * Compare central, federated, and platform-plus-paved-road operating models
    * Design an intake process with a fast lane for standard patterns and review for the rest
    * Define a standards catalog and an integration inventory, and keep both alive
    * Use data contracts to make agreements between producers and consumers machine-checkable
    * Connect integrations to lineage and a data catalog
    * Retire integrations properly, and measure the health of the estate
    * Govern citizen automation and AI agent tools

## Operating Models

Three operating models cover most organizations.

**Table: Three operating models for integration**
| Model | How it works | Works when | Fails when |
|---|---|---|---|
| Central integration team | One team builds and runs all integrations | Small estates; heavy regulation; scarce skills | Demand outgrows the team and it becomes a queue |
| Federated delivery | Each domain builds its own integrations | Strong engineering in the domains | There are no standards: duplication, sprawl, uneven security |
| **Platform plus paved road** | A platform team provides runtimes, templates, pipelines, connectors, and guardrails; domain teams build on it; high-risk designs receive a light review | Most medium and large enterprises | The paved road is harder than the dirt track, so teams go around it |

the figure shows the third model.

*[Figure: The platform team makes the right way the easy way. Domain teams deliver. An inventory and catalogs keep the estate visible.]*
The platform team maintains the **standards, templates, pipelines, and connectors**, and *enables* the domain teams (sales, finance, data), which build integrations on that foundation. Each domain registers what it builds in the **integration inventory and the API and event catalogs**. A lightweight **architecture review** examines only high-risk designs. The key phrase in the table is the failure mode: the paved road must be *easier* than going around it. If the standard template takes longer to use than a quick script, teams will write quick scripts, and the platform will have standards that nobody follows. Measure the platform by how many teams *choose* it.

## Intake: How a New Request Flows

How a request enters the system determines whether the paved road is used. the figure shows an intake process with two lanes.

*[Figure: Most requests should match a standard pattern and take the fast lane. Only novel or high-risk designs need a full review.]*
A request arrives as a one-page brief and is triaged for tier and risk (arrow 1). One question then sorts it (arrow 2): does it match a standard pattern? If yes (arrow 3), it takes the **fast lane**, using a template and the paved road; if not (arrow 4), it receives an architecture review with decision records. Either way (arrows 5 and 6), the result is built and *registered in the inventory*. A healthy platform sees the large majority of requests in the fast lane, and measures the lead time from request to production for each lane.

## The Standards Catalog

Standards are agreements that make estates predictable. A catalog lists them in one place, each with an owner and a reference implementation.

**Table: A standards catalog for integration**
| Standard | Contents |
|---|---|
| Pattern catalog | Approved patterns (Chapters 6 and 7) with when to use them and reference implementations |
| API style guide | Naming, versioning, pagination, errors, security, deprecation (Chapter 11) |
| Event style guide | Envelope, naming, keys, versions, schema compatibility, topic naming and ownership |
| Error handling and logging | Retry rules, quarantine and dead letter conventions, the log schema, correlation and trace propagation (Chapter 26) |
| Security baseline | Identities, secrets, encryption, data classification handling, review triggers (Chapter 27) |
| Delivery standard | Repositories, pipelines, environments, release strategies (Chapter 17) |
| Operational readiness | A runbook, alerts, objectives, an owner, and a recovery tier before go-live (Chapters 26 and 28) |

A standard without a *reference implementation* is a document; with one, it is a starting point that saves a team a week. Ship templates, not just rules.

## The Integration Inventory

You cannot govern what you cannot see. The **inventory** records every integration, ideally harvested automatically from platforms and pipelines rather than typed by hand.

**Table: Fields of an integration inventory record**
| Field | Why |
|---|---|
| Name, purpose, business owner, technical owner | Someone to call and someone to decide |
| Source and target systems, entities, data classification | Impact analysis, privacy, lineage |
| Pattern, platform, runtime location | Standards compliance, migration planning |
| Criticality tier, objectives, support model | Alert routing and recovery expectations |
| Credentials used and their rotation dates | Security hygiene; avoids surprise expiries |
| Contracts (API specifications, schemas, data contracts) and versions | Change management |
| Status (live, deprecated, retired) and last review date | Lifecycle; finds zombies |

A record for the Larkspur order flow, in a compact format:

```yaml
id: INT-0042
name: Orders to ERP
purpose: Create sales orders from web shop orders within 5 minutes
owners: {business: Head of E-commerce, technical: Commerce platform team}
systems: {source: Commerce SaaS, target: ERP, also: Kafka order events}
data: {entities: [order, customer-crosswalk], classification: personal}
pattern: webhook + queue + reconciliation
platform: containers (cloud account)
tier: 2
objectives: {freshness_p95_minutes: 5, completeness: "100%"}
credentials: [{system: ERP, identity: comm-user-orders,
               rotate_by: 2027-05-01}]
contracts: [openapi: commerce-v2.4, mapping-spec: v1.3]
status: live
last_review: 2026-11-15
```

## Data Contracts

A **data contract** is an agreement between the producer and the consumers of a dataset or stream: its schema, its meaning, its quality rules, its service levels, and its owner, written in a machine-readable file that tooling can check. It formalizes what the mapping specification and the authority matrix capture informally, and makes them enforceable in the pipeline and in monitoring.

The Open Data Contract Standard (ODCS), maintained by the Bitol project under the Linux Foundation, is a common YAML format. Version 3.1.0 appeared in December 2025 and version 3.2.0 in September 2026; the sketch below follows 3.2.0. It is illustrative, so check the field names against the current specification. Note that it spells out the SLA unit (`minutes`), because the single letter `m` is ambiguous between minutes and months in some tools.

```yaml
apiVersion: v3.2.0
kind: DataContract
id: orders-events-contract
name: Order events
version: 1.2.0
status: active
domain: sales
dataProduct: order-events
description:
  purpose: Orders created and updated through all sales channels
schema:
  - id: order_events_obj
    name: order_events
    physicalName: sales.order.events.v1
    properties:
      - id: order_id_prop
        name: order_id
        logicalType: string
        required: true
        primaryKey: true
      - id: total_amount_prop
        name: total_amount
        logicalType: number
        required: true
        quality:
          - metric: nullValues
            mustBe: 0
      - id: occurred_at_prop
        name: occurred_at
        logicalType: timestamp
        required: true
slaProperties:
  - property: latency
    value: 5
    unit: minutes
team:
  name: order-platform-team
  members:
    - username: order-platform-lead
      role: Owner
```

The value of a contract is what happens *around* it: a pipeline that validates new schema versions against it, a monitor that checks the quality rules and the latency, and a catalog entry that shows consumers whom to ask. A contract that lives in a repository and is never checked is just another document.

## Lineage and the Data Catalog

A governed estate must be able to answer *where does this field come from, who uses it, and what breaks if we change it?* Four practices make that possible.

* **Register integrations as processes** linking source and target assets in the catalog, so that impact analysis covers them.
* **Emit lineage events** from orchestrators, transformation tools, and custom integrations, using the OpenLineage specification where possible, and harvest connector configurations for Kafka (Chapter 19).
* **Link data contracts, owners, and classifications** to the catalog assets they describe.
* **Use lineage to answer governance questions** about origin, usage, and the impact of change.

## Lifecycle: Versioning, Deprecation, Retirement

Every integration has a lifecycle, and the end of it is the part most often skipped. Five rules keep an estate from filling with zombies. Every interface and integration has a version and an owner. A breaking change requires a new version and a published deprecation window. Usage is measured per consumer, so you know whom to contact. Deprecated items receive reminders, then, where policy allows, scheduled brownouts, then retirement. And **retirement removes everything**: credentials, firewall rules, topics, schedules, and the inventory entry, not merely the code. A decommissioned integration whose service account still exists is a security finding waiting to happen.

## Measuring the Estate

**Table: Estate health indicators**
| Indicator | Healthy direction |
|---|---|
| Integrations with a named owner, runbook, and alerts | Toward 100% |
| Incidents per month and mean time to restore | Down |
| Change failure rate (releases causing incidents) | Down |
| Lead time from request to production | Down, especially for standard patterns |
| Reuse of APIs, connectors, and templates | Up |
| Integrations on deprecated platforms or versions | Down |
| Credentials past their rotation date | Zero |
| Run cost per integration and per million messages | Known and stable |

Review these quarterly. The first and the next-to-last matter most: an unowned integration and a credential past its rotation date are the two most reliable predictors of a future incident.

## A Light Architecture Review

Review only what needs it: new patterns, tier-one integrations, regulated data, new platforms, and new external parties. Use a short checklist, the design review questions of Chapter 2 plus the security review pack of Chapter 27, give an answer within a week, and record the outcome as decision records. A review process that takes a month trains teams to avoid it.

## Citizen Integration and AI Agents

Two newer sources of integration challenge governance. **Citizen automation tools** put integration in the hands of business users: personal productivity flows, team notifications, small data movements. Allow them within data-loss-prevention policies, inventory them, and *promote* anything business-critical onto the governed platform with an owner. **AI agent tools**, exposed through protocols such as MCP, are integrations too, and should be governed as such: inventory each tool, scope its credentials, require human approval for writes, log every call, and review which data the agent can reach (Chapter 27).

## Summary

An estate needs an operating model. The platform-plus-paved-road model, in which a platform team provides templates, pipelines, and guardrails and domain teams build on them, suits most organizations, provided the paved road is genuinely easier than going around it. Intake with a fast lane for standard patterns and review for novel or risky designs keeps lead times short and risk visible.

A standards catalog with reference implementations, an inventory harvested from platforms, machine-checkable data contracts, and lineage linked to a catalog make the estate legible. Retirement removes credentials and rules as well as code, and a handful of indicators, owner coverage, incidents, lead time, reuse, and credentials past rotation, show whether the estate is improving. Citizen automation and AI agent tools belong inside the same governance framework.

## Exercises

1. **Write an inventory record.** For three integrations you know, fill in the record fields. Which fields can you not fill, and who could?
2. **Find the zombies.** List integrations whose owner has left or whose purpose is forgotten. What would retiring each involve beyond deleting code?
3. **Design the fast lane.** Define three "standard patterns" for your organization with a template for each. What makes each easy to use?
4. **Write a contract.** Draft a data contract for an event or dataset you produce: schema, quality rules, latency, and owner. Who would check it, and how?



# Chapter 30. A Troubleshooting Field Guide

When an integration fails, the person on the other end of the pager is rarely the person who built it. They are tired, they have a business user waiting, and they need a way to narrow a very large space of possible causes to the one that matters. This chapter is for that person. It gives a method first, because a method works on problems nobody has seen before, then a set of symptom tables for the failures that recur, and finally a short list of the evidence to gather before asking a vendor or another team for help.

The tables collect, in one place, material from earlier chapters, with pointers to the chapter that explains each fix. Use them as an index into the book.

> **In this chapter**
    * Apply a five-question method that narrows any failure to its layer
    * Bisect a data path to find where records stop
    * Recognize the common symptoms of connectivity, authentication, data, synchronization, messaging, performance, and delivery failures
    * Collect the evidence that lets a vendor or colleague help you quickly

## The Five-Question Method

Most integration failures yield to five questions, asked in order. They are cheap, and skipping them to chase a clever theory is the most common way to lose an afternoon.

**1. What changed?** Almost every failure follows a change: a deployment, a configuration edit, a credential rotation, a vendor release, a certificate expiry, a network change, a new data pattern, a volume spike. Ask for the change log of *every* party, not just yours. If nothing changed in your system, ask the other side; if nothing changed anywhere, look at time (a certificate that reached its expiry date is a change nobody made).

**2. Where does the flow stop?** *Bisect the path.* A record travels from source through several stages to the target. Check the middle: is it in the queue? Is it in the log? Did the worker see it? The answer halves the search. Trace identifiers (Chapter 26) make this a search, not an investigation; without them, pick a record and follow it by hand.

**3. Is it the connection, the credential, the data, or the capacity?** These four categories cover most failures. A connection failure shows as timeouts, resets, and DNS errors; a credential failure as 401 and 403; a data failure as 400 and 422, or as a quarantine; a capacity failure as 429, slowness, and growing lag.

**4. Can I reproduce it by hand?** A `curl` call from the runtime's own host, with the same credentials, removes your code from the equation. If `curl` fails, the problem is not your code; if it works, the problem is in it.

**5. What does the evidence say?** Read the actual error body, the actual log line, the actual response headers. The most expensive mistake in troubleshooting is the theory formed before looking.

> **The first ten minutes**
    Check the dashboard's five questions (Chapter 26): running, fresh, complete and correct, healthy, safe for peak. Then the change log. Then bisect. Most incidents are located within ten minutes by following that order, and the remainder are the ones that deserve a fresh look.

## Connectivity and Network

**Table: Connectivity and network symptoms**
| Symptom | Likely cause | Fix |
|---|---|---|
| Works from a laptop, fails from the server | A firewall or proxy; egress addresses not allowlisted; DNS differs | Trace the path from the server; check proxy settings; compare DNS answers |
| TLS handshake errors | TLS inspection with a private authority; an expired certificate; wrong trust store | Add the authority to the runtime's trust store; check expiry; never disable verification |
| Intermittent resets on long requests | An idle timeout on a load balancer or firewall | Set client keepalives and timeouts below the shortest idle timeout |
| Timeouts only at certain hours | A batch window or maintenance on the target; a shared link saturated | Check the target's calendar; measure link use; move the schedule |
| Large payloads fail, small ones work | MTU or fragmentation; a gateway size limit | Check path MTU; raise gateway limits; use a claim check |

## Authentication

Chapter 13 contains a full table; the most common patterns are repeated here as pointers. A 401 immediately after obtaining a token usually means the wrong audience or scope. A 401 after exactly N minutes means the token expired and nothing refreshed it. A 403 on some endpoints only means a missing scope or role. Intermittent 401s with parallel workers usually mean each worker is refreshing its own token and invalidating the others', so share one token provider.

## Data and Mapping

**Table: Data and mapping symptoms**
| Symptom | Likely cause | Fix |
|---|---|---|
| Garbled characters (for example "Ã©" instead of "é") | UTF-8 read as Latin-1, or the reverse | Declare and enforce UTF-8 at every hop; test with accented characters |
| Totals off by a cent | Floating-point money or inconsistent rounding | Decimals end to end; one rounding rule in the mapping |
| Identifiers lose leading zeros | Identifiers parsed as numbers, often by spreadsheets | Treat identifiers as strings in schemas and code |
| Records rejected for a missing field that the source documents | The field is optional in some conditions, or renamed | Compare real responses with the contract; update the mapping |
| A status value rejected or skipped | No entry in the mapping table | Add the mapping; the integration should log and skip, not guess |
| Fewer fields returned than documented | Field-level security or role permissions on the integration user | Test with the integration user's real permissions |

## Synchronization and State

**Table: Synchronization symptoms**
| Symptom | Likely cause | Fix |
|---|---|---|
| Records missing around a clock change | Local-time watermarks | UTC and timezone-aware datetimes; overlap windows; a test for daylight-saving transitions |
| Duplicates after a rerun | Non-idempotent writes; wrong match key | Upsert by a stored foreign ID; deduplication ledger |
| Deleted records still in the target | No delete detection | Soft-delete mapping or a periodic ID comparison, with a deletion guard |
| Two systems keep overwriting each other | No authority split; echo loop | Per-field authority; ignore the integration's own edits |
| Imports create duplicates instead of updates | The wrong coalesce or external-ID field in the import mapping | Fix the key; deduplicate; add an idempotency test |
| Counts differ after an incident | Missed window with no repair path | Run the reconciliation; extend it to run after incidents |

## Messaging and Kafka

Chapter 19 contains the full Kafka matrix. The most common patterns: lag that grows steadily means a slow consumer, a hot partition, or a throttled target; duplicates in the target mean at-least-once delivery meeting a non-idempotent sink; frequent rebalances mean processing that outlasts `max.poll.interval.ms` or an autoscaler that flaps; and a trace that stops at a queue means the trace context is not carried in message headers.

## Performance

**Table: Performance symptoms**
| Symptom | Likely cause | Fix |
|---|---|---|
| Works in test, times out in production | Sandbox data volume or limits differ | Test at production volume; list sandbox differences |
| The job gets slower each run | Offset pagination that deepens; an unbounded state | Cursor paging; bound state; check for growth |
| 429 responses under parallel load | The concurrency exceeds the shared limit | A token bucket; bounded workers; ask for a larger allocation |
| One slow dependency stalls everything | No bulkheads | Separate pools or queues per target |
| Memory grows without bound | Loading a whole collection instead of streaming | Generators and bounded batches |

## Delivery and Environments

**Table: Delivery symptoms**
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



---

# Part VII. Growing as an Architect

Turning knowledge into skill: the learning path, the habits that compound, and how to prove your ability.



# Chapter 31. Becoming an Integration Architect

You have now read the whole of a field. Knowledge, however, is not the same as skill. A reader who has absorbed every chapter can explain idempotency and still build a job that duplicates records, because skill comes from doing the work, seeing it fail, and correcting it. This final chapter turns the book into a path: five levels, each ending in artifacts you can show a manager or a client, and the habits that compound over years.

It closes with the question every practitioner eventually faces: how do you *prove* it? Interviews, design reviews, and client workshops all test the same abilities, and the final sections explain what assessors listen for and how to answer.

> **In this chapter**
    * Follow a five-level learning path from newcomer to principal, with an artifact for each milestone
    * Build habits that compound: reconnaissance, incident reviews, pattern logs, plain explanations, and reading changelogs
    * Choose books and certifications that support the path
    * Understand how interviewers and clients assess an integration architect
    * Answer design questions with a repeatable structure

## The Learning Path

the figure shows the five levels. Each ends in artifacts you can show, not courses you attended.

*[Figure: Five levels from newcomer to principal. Each level ends with artifacts you can show.]*
Expect about a year from level 0 to level 3 with steady practice alongside real work. Level 4 is a career stage rather than a course.

### Level 0: Newcomer (Weeks 1 to 4)

You are learning the vocabulary and making your first calls. The milestones are to read Chapters 1 and 2 and explain synchronous versus asynchronous communication in your own words; to call three public APIs with `curl` and read the status codes, headers, and bodies; to read an OpenAPI specification and list its authentication, pagination, and error model; to write a Python script with timeouts that handles 200, 404, and 429 differently; and to answer the foundation-level questions in Appendix B.

### Level 1: Practitioner (Months 2 to 3)

You are building components that work. The milestones are to build a watermark poller with pagination, retries with jitter, and a checkpoint (Chapter 14); to implement OAuth 2.0 client credentials with a cached, refreshed token (Chapter 13); to write a mapping specification and golden-file tests for one entity (Chapter 12); to build a webhook receiver that verifies signatures and deduplicates events; and to write a reconnaissance sheet for one real API (Chapter 10).

### Level 2: Integration Engineer (Months 4 to 6)

You are building systems, with streams and pipelines. The milestones are to run Kafka locally, produce keyed events, and watch consumer groups rebalance (Chapter 18); to capture changes from a PostgreSQL database with Debezium into Kafka and sink them to a second database; to automate the failure-injection matrix for one integration (Chapter 16); to put an integration through a delivery pipeline with contract tests (Chapter 17); and to write a reconciliation job and a run summary with alerts (Chapter 26).

### Level 3: Solution Architect (Months 6 to 12)

You are leading designs. The milestones are to lead a discovery workshop with the question bank and reach the design gate (Chapters 3 and 4); to produce a brief, an authority matrix, decision records, and a threat model for a real project; to run the decision method and defend the choice against the runner-up (Chapter 9); to estimate with stated assumptions and plan cutover and recovery (Chapter 28); and to pass the senior questions and two whiteboard exercises in Appendix B.

### Level 4: Principal (Year 2 and Beyond)

You are shaping a practice. The milestones are to write or refresh the standards catalog (Chapter 29); to run a platform proof of concept with failure injection and a three-year cost model (Chapter 23); to set up an integration inventory and estate indicators; to mentor two engineers through levels 1 and 2; and to explain an integration program to an executive in five minutes with one diagram.

> **Tick a milestone only when you have the artifact**
    The test of a milestone is a file, a repository, or a document that someone else could read. "I understand it" is not an artifact; "here is the poller, and here is the test that kills it mid-run" is. The artifacts also form your portfolio.

## Habits That Compound

Five habits produce growth beyond what any course gives.

* **Read one vendor API reference a week** and fill a reconnaissance sheet. Patterns in API design become obvious quickly, and you begin to recognize good and bad choices at a glance.
* **Write a short post-incident review for every problem you meet,** even small ones. Writing forces you to separate the cause from the symptom.
* **Keep a pattern log:** for each project, which patterns you used, what went wrong, and what you would change. After ten projects it is your own book.
* **Explain a design to a non-engineer every month.** If they cannot follow, simplify; the skill transfers directly to sponsors and executives.
* **Read the changelogs** of the platforms you depend on. Most surprises are announced somewhere weeks before they arrive.

## Reading and Certifications

The books below deepen the topics of this one. Appendix G gives fuller details.

**Table: Books that deepen the path**
| Book | Authors | Why |
|---|---|---|
| *Enterprise Integration Patterns* | Gregor Hohpe and Bobby Woolf | The vocabulary of messaging patterns still used by every platform |
| *Designing Data-Intensive Applications* | Martin Kleppmann | Replication, consistency, logs, and streams explained properly |
| *Kafka: The Definitive Guide* | Gwen Shapira and co-authors | Kafka internals and operations |
| *Building Event-Driven Microservices* | Adam Bellemare | Event design and stream-based architecture |
| *Release It!* | Michael Nygard | Stability patterns: timeouts, circuit breakers, bulkheads |
| *Fundamentals of Software Architecture* | Mark Richards and Neal Ford | Architecture characteristics and trade-off thinking |
| *API Design Patterns* | JJ Geewax | Designing APIs others can integrate with |
| *Site Reliability Engineering* | Google (Beyer and co-editors) | Objectives, error budgets, incident practice |
| *Team Topologies* | Matthew Skelton and Manuel Pais | Platform teams and operating models |

Certifications are useful signals but not substitutes for delivered integrations. Common choices are vendor tracks for the platforms you use (for example, MuleSoft developer and integration architect certifications, Confluent's Kafka developer and administrator certifications, the solution architect certifications of AWS, Azure, and Google Cloud) and general architecture frameworks such as TOGAF. Catalogs change often, so check the vendors' current lists before planning.

## How You Will Be Assessed

Hiring managers, sponsors, and clients probe an integration architect in four ways: *fundamentals* (do you understand the ideas?), *depth* (have you operated this?), *judgment* (what would you do when constraints conflict?), and *communication* (can you explain it to a non-engineer?). The signals they listen for are consistent across all four.

**Table: What assessors listen for**
| They listen for | A strong signal | A weak signal |
|---|---|---|
| Trade-offs | "It depends on freshness, volume, and network direction; here is how I would decide." | A product name or favorite pattern with no conditions |
| Failure thinking | Unprompted mention of retries, idempotency, duplicates, reconciliation, and monitoring | Describes only the happy path |
| Questions before answers | Clarifies authority, volume, freshness, network, and ownership before drawing | Starts drawing immediately |
| Numbers | Back-of-envelope arithmetic for throughput, limits, and cost | "It should scale" |
| Operations | Runbooks, alerts, ownership, rotation, recovery | Stops at "deployed" |
| Communication | One diagram, plain words, the decision needed | Protocol vocabulary for a non-technical audience |

### A Reusable Answer Structure

For a design question ("design an integration between our CRM and ERP") use a seven-step structure that mirrors the book.

1. **Clarify.** Ask about the outcome, the four numbers, authority, network, and ownership. Say what you are assuming.
2. **Constraints first.** State which constraints rule options out.
3. **Choose a pattern family and a pattern,** and name the runner-up and why you rejected it.
4. **Sketch the flow,** one diagram, with the failure points marked.
5. **Handle failure:** idempotency, retries, quarantine, reconciliation, and what is monitored.
6. **Cover security and operations:** identities, secrets, alerts, owner, runbook.
7. **State the trade-offs and the conditions to revisit the decision.**

The structure shows an assessor, in order, the habits they are looking for. It also keeps you from the commonest failure of a nervous candidate: drawing boxes for ten minutes before asking a single question. Appendix B contains over 150 questions with model answers, what each tests, and the red-flag answer to avoid. Practice them aloud, then mark yourself honestly; the discipline of explaining out loud exposes gaps that silent reading hides.

## Final Words

Integration is, at bottom, the craft of making independent things cooperate despite their differences and failures. The technologies will keep changing, with new platforms, new protocols, and new fashions, but the problems the book has described, meaning, time, and failure, will not. The architect who asks the five questions of Chapter 1, who finds the authority split, who designs for the retry and the duplicate and the outage, who writes the runbook before go-live, and who measures what matters, will be useful on any technology, in any company, for as long as systems need to talk to each other. Which is likely to be a long time.

## Summary

Knowledge becomes skill through deliberate practice with artifacts. Five levels, newcomer, practitioner, integration engineer, solution architect, and principal, each end in things you can show, and five habits compound: reading API references, writing incident reviews, keeping a pattern log, explaining designs plainly, and following changelogs. Books and certifications support the path but do not replace delivered work. Assessors listen for trade-offs, failure thinking, questions before answers, numbers, operations, and clear communication, and a seven-step answer structure presents those signals in order.

## Exercises

1. **Place yourself.** Which level are you on? List the milestones you have *artifacts* for, and the three you will complete next.
2. **Start a pattern log.** Create a document, and enter the last integration you worked on: patterns used, what went wrong, what you would change.
3. **Practice aloud.** Pick five questions from Appendix B, answer them aloud without notes, and then compare with the model answers. Which category is weakest?
4. **Explain it in five minutes.** Explain one integration to a non-engineer using one diagram. Ask them to tell you what they understood.



# Appendix A. The Discovery Question Bank

This appendix contains 125 questions for the discovery phase (Chapter 4), grouped by the stakeholder who can answer them. Questions marked **C** are *critical*: an unfavorable or missing answer changes the architecture, so they must be answered, or placed on the risk register with an owner and a date, before the design gate (Chapter 3). Every question lists its **design consequence**, which says why you are asking and what the answer changes.

Do not read a list aloud. Send each group its section a day ahead, hold a 60 to 90 minute session per group, and record the answers. Count a question as answered only when you hold a real answer, not an intention to find one.


## Business owner and sponsor

*Ask:* Business owner, product owner, sponsor. *14 questions, 5 critical.*

| | # | Question | Design consequence |
|:-:|--:|---|---|
| **C** | 1 | What business outcome or decision depends on this integration, and how will we measure success? | Defines acceptance criteria and stops gold-plating. |
| **C** | 2 | Who is the accountable business owner, and who can approve scope changes? | Names the person who signs off and arbitrates trade-offs. |
| **C** | 3 | What does one hour, one day and one week of the integration being down or wrong cost the business? | Sets the availability tier, alerting, DR and support model. |
| **C** | 4 | Is this a one-time migration, a recurring sync or a continuous flow? | One-time work needs far less operational machinery. |
|  | 5 | Which teams and processes consume the result, and what exactly do they do with it? | Reveals the real consumer count and the real freshness need. |
|  | 6 | How is this done manually today, and how long does it take? | Gives a baseline, a fallback procedure and the business case. |
| **C** | 7 | Is there a regulatory or audit driver (SOX, GDPR, HIPAA, PCI, BCBS 239, local rules)? | Adds audit trail, lineage, retention and residency requirements. |
|  | 8 | What is the target go-live date, and is it a hard date (contract, regulation) or a soft one? | Hard dates force scope cuts instead of date slips. |
|  | 9 | What is the budget envelope, and who pays for run costs (licenses, cloud, support)? | Constrains platform choice and the three-year total cost. |
|  | 10 | What is explicitly out of scope? | Prevents scope creep; documents what was deliberately deferred. |
|  | 11 | Are other initiatives touching these systems in the next two years (upgrades, migrations, mergers)? | Predicts API changes and re-work; may argue for a facade. |
|  | 12 | Who are the end users, and how will they learn what changes for them? | Triggers change management and training work. |
|  | 13 | What would make you cancel this project? | Exposes risk appetite and the true priorities. |
|  | 14 | What does "done" look like in one sentence? | A shared definition prevents a perpetual project. |

## Data, semantics and governance

*Ask:* Data owner, data steward, governance lead. *19 questions, 9 critical.*

| | # | Question | Design consequence |
|:-:|--:|---|---|
| **C** | 15 | Which entities and fields are in scope, and which are explicitly excluded? | The field list drives mapping, volume and security review. |
| **C** | 16 | For each field, which system is authoritative? Can both sides edit it? | Decides one-way versus bidirectional flows and the conflict rules. |
| **C** | 17 | What is the unique, stable identifier in each system? Can it change or be reused? | Determines the matching strategy and the duplicate risk. |
|  | 18 | How are records matched across systems today (keys, crosswalks)? Are there known duplicates? | Matching rules or a crosswalk table become part of the design. |
| **C** | 19 | How are deletes represented (hard delete, soft flag, archive, no signal), and should they propagate? | No signal means an ID-list diff job is required. |
|  | 20 | How are renames, merges and splits handled in the source? | Name-based matching will create duplicates; use stored foreign IDs. |
| **C** | 21 | How many records now, in three years, at peak per hour, and what is the largest record or file? | Sizing, pagination, memory, timeouts and pattern choice. |
| **C** | 22 | What is the data quality like (nulls, duplicates, free text, odd characters, wrong types)? Who fixes bad records? | Validation, quarantine and an owner for rejects. |
| **C** | 23 | What data classification applies (public, internal, confidential, personal, regulated)? | Masking, encryption, logging rules and who may process it. |
| **C** | 24 | Does the data cross borders or regions? Are there residency or sovereignty rules? | Restricts vendor-cloud processing and replication topologies. |
|  | 25 | What are the retention rules, and how does the right to erasure reach copies? | Purge propagation, crypto-shredding for immutable logs. |
|  | 26 | Are code lists and reference data shared or mapped? Who maintains the mapping tables? | Mapping tables as governed configuration, with an owner. |
|  | 27 | Which time zone, precision and clock does each system use? | Watermark correctness; UTC internally, convert at the edges. |
|  | 28 | Which units, currencies, languages, encodings and date formats are in use? | Normalization rules and test cases for edge characters. |
|  | 29 | Is there a business glossary or data contract for these entities? | Shared semantics reduce rework; contract owner for changes. |
|  | 30 | Is history needed? How far back, and how large is the initial load? | Backfill strategy that does not starve production. |
|  | 31 | Which fields are derived or computed and should not be copied? | Avoids copying values that will be recomputed differently. |
| **C** | 32 | Does the order of changes matter: per entity, or globally? | Partitioning keys, sequencing, single-writer rules. |
|  | 33 | Is lineage required, and at what level (system, table, column)? | Lineage emission (for example OpenLineage) becomes a work item. |

## Source system owner

*Ask:* Source application owner, API team. *16 questions, 7 critical.*

| | # | Question | Design consequence |
|:-:|--:|---|---|
| **C** | 34 | Which interfaces exist (REST, SOAP, database, files, queues, events)? Is there a machine-readable contract? | Fixes the possible patterns; a spec is the starting artifact. |
| **C** | 35 | Is there a sandbox with realistic data? How often is it refreshed? | Test realism; production-sized data surprises otherwise. |
| **C** | 36 | Which authentication methods are supported, and who issues and approves service accounts? | Lead time for credentials; auth design. |
| **C** | 37 | What are the rate limits, quotas, concurrency limits and maintenance windows? | Request budget, backoff, scheduling. |
| **C** | 38 | Is there a modified-since filter, change feed, webhook or CDC option? | Incremental versus snapshot design. |
|  | 39 | What is the pagination style, maximum page size and ordering stability? | Extraction loop design; cursor versus offset. |
|  | 40 | Are there bulk or asynchronous export endpoints? | Volume handling without paging millions of rows. |
|  | 41 | How are errors reported (codes, bodies)? Can a 200 response contain per-item failures? | Per-item result checking and error classification. |
| **C** | 42 | What is the versioning and deprecation policy, and how are changes announced? | Maintenance risk; contract tests; a facade may be warranted. |
|  | 43 | Who do we call when it breaks, and what are the support hours and SLA? | Escalation path and realistic recovery expectations. |
|  | 44 | Has anyone outside the owning team called this interface in production? | Untested internal APIs break under external load. |
|  | 45 | What is the source system's own availability and maintenance pattern? | Defines retry windows and acceptable staleness during outages. |
|  | 46 | Are there load restrictions (read replica only, business hours, batch windows)? | Scheduling and the choice of replica versus primary. |
|  | 47 | Is the data permission-filtered per user, and what will our service account see? | Incomplete reads that look like successes. |
| **C** | 48 | Are timestamps reliable (set by the database or the app, always updated on change, which zone)? | Whether a watermark is safe or a snapshot is needed. |
|  | 49 | Do deleted records keep a stable ID or disappear entirely? | Delete detection strategy. |

## Target system owner

*Ask:* Target application owner, platform admin. *14 questions, 4 critical.*

| | # | Question | Design consequence |
|:-:|--:|---|---|
| **C** | 50 | How do we write: API (create, update, upsert), bulk import, database or files? | Fixes the load pattern and the batching approach. |
| **C** | 51 | Are writes idempotent (upsert by key, idempotency key)? | Without it, retries create duplicates and you need a lookup or single writer. |
| **C** | 52 | What are the rate and bulk limits, and what happens when they are hit? | Throttling, queueing and use of bulk endpoints. |
|  | 53 | How are validation errors reported, and is partial success possible? | Per-record error handling and quarantine. |
|  | 54 | Do writes fire triggers, workflows or notifications in the target? | Side effects to suppress, batch or accept. |
|  | 55 | Which fields and relationships are mandatory, and in what order must parents and children be created? | Two-pass loading: entities first, relations second. |
|  | 56 | Which statuses or lifecycle states exist, and are writes forbidden in some of them? | Mapping rules and skipped-record reasons. |
| **C** | 57 | Can we store the source ID and origin on target records (custom fields)? | Stored foreign IDs and loop prevention. |
|  | 58 | Can the integration user be identified in the target's history? | Needed to filter your own edits in bidirectional sync. |
|  | 59 | Is there a sandbox, how is it reset, and what test-data rules apply? | Test strategy and repeatability. |
|  | 60 | Does an API user consume a license, and are there daily API-call allowances? | Cost and capacity limits that are not technical. |
|  | 61 | What happens to records the integration created if it is switched off? | Ownership after decommissioning. |
|  | 62 | How do deletes and archives work in the target? | Delete mapping and recoverability. |
|  | 63 | May bulk loads run during business hours? | Scheduling and throttling for the initial load. |

## Security and identity

*Ask:* CISO office, IAM team, privacy officer. *16 questions, 7 critical.*

| | # | Question | Design consequence |
|:-:|--:|---|---|
| **C** | 64 | Which machine-authentication methods are accepted, and who approves new service accounts? | Lead time and the authentication design. |
| **C** | 65 | What is the least-privilege permission set, and are accounts separate per environment? | Role design; avoids a shared admin account. |
| **C** | 66 | Where do secrets live, who rotates them, and how often? | Vault integration and a zero-downtime rotation plan. |
| **C** | 67 | Is a security review, threat model or penetration test required, and what is the lead time? | Schedule risk: often the longest dependency. |
| **C** | 68 | How must classified data be protected in transit, at rest, in logs and in topics? | Encryption, masking, tokenization, log hygiene. |
|  | 69 | Which payload fields may be logged, and which must be masked? | Logging rules baked into the framework. |
|  | 70 | Which countries and cloud regions may process the data? Which sub-processors are approved? | Constrains hosting and vendor choice. |
|  | 71 | Is TLS inspection used? Are private CAs or mutual TLS required? | Trust-store work; avoids "disable verification" shortcuts. |
|  | 72 | What audit logging is required for integration actions, and for how long? | Dedicated identity, structured logs, retention. |
| **C** | 73 | Is there an approved reference architecture or list of approved integration platforms? | Saves arguments; defines the allowed solution space. |
| **C** | 74 | May a vendor-hosted platform process this data? | Decides cloud iPaaS versus customer-hosted runtime. |
|  | 75 | Who is alerted on suspected credential compromize, and what is the revocation procedure? | Incident playbook and break-glass design. |
|  | 76 | What dependency and vulnerability policy applies (scanning, approved libraries)? | Build pipeline checks and library choices. |
|  | 77 | Who may promote changes to production (separation of duties)? | Pipeline approvals and role design. |
|  | 78 | May we expose a public endpoint (for webhooks)? Is a WAF or IP allowlist required? | Webhook feasibility; otherwise poll. |
|  | 79 | If an OAuth grant is user-delegated, whose identity owns it and what happens when that person leaves? | Prefer service identities; plan for ownership change. |

## Network and infrastructure

*Ask:* Network team, platform and cloud engineering. *14 questions, 7 critical.*

| | # | Question | Design consequence |
|:-:|--:|---|---|
| **C** | 80 | Where do the source, target and integration runtime live (on-premises, which cloud and region, SaaS)? | Selects the topology (Chapter 5). |
| **C** | 81 | Which direction may connections be initiated? Is any inbound traffic allowed? | Outbound-only favors polling and agents over webhooks. |
| **C** | 82 | What proxies, egress filters and allowlists apply? Are static egress IPs available? | Connectivity design; vendor allowlists. |
| **C** | 83 | Is private connectivity (VPN, private link) required, and what is the lead time for circuits and firewall changes? | Long-lead item: start in week one. |
|  | 84 | How does DNS resolve private names from the runtime host? | Classic cause of "works on my laptop". |
|  | 85 | What are latency and bandwidth between the sites, compared with payload sizes? | Batching versus chatty protocols. |
|  | 86 | What time-synchronization standard applies (NTP)? | Prevents clock-skew failures in tokens and watermarks. |
| **C** | 87 | Which runtime hosting options exist (VM, container, Kubernetes, serverless), and who provides them? | Deployment model and ownership. |
| **C** | 88 | Which environments exist (dev, test, UAT, production), and how closely do they match? | Promotion path and test realism. |
|  | 89 | What quotas and budget guardrails apply in the cloud accounts? | Prevents surprise limits at go-live. |
|  | 90 | Who issues and renews certificates, and who watches expiry? | Certificate inventory with alerts at 30 and 7 days. |
| **C** | 91 | What RPO and RTO apply to an integration of this tier, and where is the DR site? | State replication, runtime failover, replay strategy. |
|  | 92 | What are the patch and maintenance windows of runtime hosts? | Scheduling and restart-safety requirements. |
|  | 93 | Which network zones (OT and IT, DMZ) must be crossed, and who approves crossings? | One-way paths and gateways for sensitive zones. |

## Operations and support

*Ask:* Operations manager, service desk, SRE. *14 questions, 5 critical.*

| | # | Question | Design consequence |
|:-:|--:|---|---|
| **C** | 94 | Which named team runs, monitors and supports the integration after go-live? | No owner means no production. |
| **C** | 95 | What are the support hours, on-call model, escalation path and target response times? | Alerting severity and runbook depth. |
|  | 96 | Which monitoring and alerting tools are used, and how do alerts reach people (ITSM, chat, paging)? | Fits alerts into existing practice. |
|  | 97 | Which logging platform, retention period and access controls apply? | Log format, correlation IDs, retention limits. |
| **C** | 98 | What is the release process (CI/CD, approvals, windows, rollback)? | Packaging and promotion design. |
|  | 99 | What runbook and knowledge-transfer deliverables are expected? | Runbook is a deliverable, not an afterthought. |
|  | 100 | How are secret and certificate rotations scheduled? | Rotation runbook and monitoring. |
| **C** | 101 | Who reconciles source and target and owns discrepancies and data fixes? | Reconcile job output needs a human owner. |
|  | 102 | What is the process for replaying or reprocessing failed records? | Replay tooling and DLQ triage. |
|  | 103 | Who owns capacity planning and cost monitoring? | Prevents silent cost growth. |
|  | 104 | Which vendor support contracts and SLAs apply to the platforms in the path? | Escalation path to vendors. |
| **C** | 105 | How are upgrades of the source and target communicated to the integration team? | Early warning for breaking changes. |
|  | 106 | Which KPIs or SLOs will be reported (freshness, error rate, backlog)? | Metrics to emit from day one. |
|  | 107 | How will we know when to retire the integration? | Decommissioning criteria and an owner. |

## Legal, compliance and procurement

*Ask:* Legal, privacy, procurement, compliance. *8 questions, 2 critical.*

| | # | Question | Design consequence |
|:-:|--:|---|---|
| **C** | 108 | Are data processing agreements in place with every vendor in the data path? | Blocks go-live if missing. |
|  | 109 | Do API terms of use restrict automated or commercial access or set contractual rate limits? | Hidden limits and license breaches. |
|  | 110 | How are connectors and platforms licensed (cores, tasks, connectors), and when do contracts renew? | Three-year cost and exit options. |
|  | 111 | Do export-control or sovereignty rules apply? | Restricts regions and vendors. |
|  | 112 | What audit evidence must be retained, and for how long? | Evidence generation as a requirement. |
|  | 113 | Who owns the integration code and artifacts (consultants, vendors)? | Handover and IP clauses. |
|  | 114 | What is the procurement lead time for tools, accounts and cloud resources? | Schedule risk. |
| **C** | 115 | Who signs off the privacy impact assessment? | Gate before processing personal data. |

## Delivery and project management

*Ask:* Project manager, delivery lead, QA. *10 questions, 4 critical.*

| | # | Question | Design consequence |
|:-:|--:|---|---|
| **C** | 116 | Who are the decision makers and the named technical contacts on each side? | Prevents stalls waiting for answers. |
| **C** | 117 | What is the test strategy, and who provides test data and gives acceptance? | Acceptance criteria and test environments. |
| **C** | 118 | How will the initial load or backfill and the cutover be executed and validated? | Cutover plan, reconciliation, rollback. |
| **C** | 119 | Which dependencies (teams, environments, accounts) exist, and what are their lead times? | Critical path and risk register. |
|  | 120 | What release or freeze calendars apply? | Go-live windows. |
|  | 121 | How will progress and risks be reported and escalated? | Governance rhythm. |
|  | 122 | Which documents are expected (design, contracts, runbook)? | Deliverable list and effort. |
|  | 123 | What skills exist in the team, and what training is needed? | Platform choice and staffing. |
|  | 124 | What distinguishes a change request from a defect? | Prevents disputes about scope. |
|  | 125 | How long is hypercare, and what are the exit criteria? | Support cost and the handover moment. |



# Appendix B. Interview and Knowledge-Check Questions

Hiring managers, sponsors, and clients probe an integration architect in four ways: fundamentals, depth, judgment, and communication (Chapter 31). This appendix holds 153 questions in 16 categories. Each has a level, a **model answer**, what the question **tests**, and the **red flag** answer to avoid. Use it to prepare for an interview, to run a team knowledge check, or to build a hiring loop.

Read the question, answer aloud in your own words, and only then read the model answer. Mark yourself honestly: *Foundation* means anyone working in integration should answer it; *Senior* means a lead or architect should; *Principal* means it probes judgment and organizational design. The model answers are deliberately generic. Adapt them to your own experience, because an interviewer will probe any claim you cannot illustrate with a real example.


## Fundamentals and patterns

<div class="qa"><p class="qq"><span class="qn">1.</span> What is the difference between synchronous and asynchronous integration, and when do you choose each? <span class="lvl">Foundation</span></p><p class="qans"><b>Model answer.</b> Synchronous: the caller waits for the reply. Simple and immediate, but it couples availability and latency. Asynchronous: the caller hands off through a queue, event or file and continues. It is resilient and decoupled, but needs correlation, duplicate handling and ordering rules. Use synchronous for lookups and validations that need an answer now; asynchronous for notifications, bulk work and anything the user need not wait for.</p><p class="qmeta"><b>Tests:</b> Whether you reason about coupling in time, not fashion. <b>Red flag:</b> "Async is always better" or "REST is always fine".</p></div>

<div class="qa"><p class="qq"><span class="qn">2.</span> What is idempotency, and why does it matter in integration? <span class="lvl">Foundation</span></p><p class="qans"><b>Model answer.</b> An operation is idempotent if doing it twice has the same effect as doing it once. Retries, redeliveries and reruns are normal, so every write must tolerate them: upsert by key, idempotency keys on APIs, dedupe ledgers for messages.</p><p class="qmeta"><b>Tests:</b> The single most important reliability concept. <b>Red flag:</b> Cannot explain how a retry could create a duplicate.</p></div>

<div class="qa"><p class="qq"><span class="qn">3.</span> Compare point-to-point, hub-and-spoke and event-driven integration. <span class="lvl">Foundation</span></p><p class="qans"><b>Model answer.</b> Point-to-point is simplest for two systems but grows as N times N minus one. Hub-and-spoke centralizes translation and routing (ESB, iPaaS) so links grow linearly, at the price of a shared component to govern. Event-driven decouples producers from consumers through a broker, gaining fan-out and replay but losing visibility of who depends on what.</p><p class="qmeta"><b>Tests:</b> Ability to state trade-offs rather than preferences. <b>Red flag:</b> Names a product instead of a pattern.</p></div>

<div class="qa"><p class="qq"><span class="qn">4.</span> Explain at-most-once, at-least-once and exactly-once delivery. Is exactly-once achievable? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> At-most-once may lose messages; at-least-once may duplicate; exactly-once is neither. It is achievable inside a system that controls both ends (for example Kafka transactions between topics), but not across the boundary to a database or REST API. End to end you build effectively-once: at-least-once delivery plus idempotent processing.</p><p class="qmeta"><b>Tests:</b> Honest understanding of guarantees and their boundaries. <b>Red flag:</b> Claims a product gives exactly-once end to end.</p></div>

<div class="qa"><p class="qq"><span class="qn">5.</span> Webhooks or polling: how do you choose? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Webhooks give low latency but need an inbound endpoint, signature verification, sender retries (dedupe) and offer no replay when you are down. Polling is simple, outbound-only and replayable by resetting a watermark, but adds latency and request cost and can miss deletes. Many designs use both: webhooks for speed, polling as the reconcile path.</p><p class="qmeta"><b>Tests:</b> Operational realism: replay, network direction, failure modes. <b>Red flag:</b> Picks webhooks without mentioning missed events.</p></div>

<div class="qa"><p class="qq"><span class="qn">6.</span> How do you choose between batch and streaming? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Start from the freshness number and the consumer count. Hours of latency, one consumer and bulk volume suggest batch. Seconds of latency, many consumers, replay or continuous changes suggest streaming. Streaming has an operating cost (platform, schemas, lag monitoring), so it must earn its place.</p><p class="qmeta"><b>Tests:</b> Requirement-driven choice with cost awareness. <b>Red flag:</b> "Real-time" with no number attached.</p></div>

<div class="qa"><p class="qq"><span class="qn">7.</span> What is the dual-write problem and how does the outbox pattern solve it? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Writing to a database and publishing an event are two operations; one can succeed and the other fail, so state and events diverge. The outbox writes the state change and the event to the same database in one transaction; a relay (CDC or poller) publishes the outbox rows afterwards. It removes divergence but not duplicates, so consumers still dedupe.</p><p class="qmeta"><b>Tests:</b> Depth on reliable event publication. <b>Red flag:</b> Suggests "just retry the publish".</p></div>

<div class="qa"><p class="qq"><span class="qn">8.</span> Orchestration versus choreography: trade-offs? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Orchestration uses a coordinator that owns the sequence and state: easy to see and change, but a central dependency. Choreography has services react to events: loosely coupled and scalable, but the end-to-end flow is invisible without tracing and an event catalog. Mixed designs are common: choreography between domains, orchestration inside a business process.</p><p class="qmeta"><b>Tests:</b> Systems thinking and observability awareness. <b>Red flag:</b> One-sided answer.</p></div>

<div class="qa"><p class="qq"><span class="qn">9.</span> Why not use a two-phase commit across systems? What do you do instead? <span class="lvl">Principal</span></p><p class="qans"><b>Model answer.</b> Distributed transactions need all participants to support the protocol, hold locks across network calls and fail badly under partition. Most SaaS and modern APIs do not support them. Use sagas: a sequence of local transactions with compensating actions, durable saga state, and idempotent steps. Accept eventual consistency and tell the business what "temporarily inconsistent" means.</p><p class="qmeta"><b>Tests:</b> Practical consistency strategy and communication. <b>Red flag:</b> Wants a global transaction manager across SaaS.</p></div>

<div class="qa"><p class="qq"><span class="qn">10.</span> What is change data capture and when do you prefer it over API polling? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> CDC reads a database transaction log and publishes every row change without touching the application. Prefer it when you need every change including deletes, low latency, no schema or code change in the source, and the source is a database you may legitimately read. It exposes the physical schema, needs DBA cooperation and replication-slot monitoring.</p><p class="qmeta"><b>Tests:</b> Knows both benefits and operational hazards. <b>Red flag:</b> Ignores schema coupling and slot growth.</p></div>

<div class="qa"><p class="qq"><span class="qn">11.</span> What are the strangler fig pattern and an anti-corruption layer? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Strangler: route traffic through a proxy and move functionality from legacy to new piece by piece. Anti-corruption layer: an adapter that translates a legacy or foreign model so it does not leak into new services. They combine well: the layer isolates, the proxy shifts traffic gradually.</p><p class="qmeta"><b>Tests:</b> Migration strategy without big bang. <b>Red flag:</b> Only knows rewrite-and-switch.</p></div>

<div class="qa"><p class="qq"><span class="qn">12.</span> When would you advise NOT building an integration? <span class="lvl">Principal</span></p><p class="qans"><b>Model answer.</b> When the systems should be consolidated, when a native feature or built-in connector already does it, when volume and change rate make a manual or scheduled export good enough, when the data has no clear owner, or when the business outcome could be met by a report. Every integration is a long-term liability; the cheapest one is the one not built.</p><p class="qmeta"><b>Tests:</b> Judgment and business orientation. <b>Red flag:</b> Always proposes new build.</p></div>

<div class="qa"><p class="qq"><span class="qn">13.</span> What is a canonical data model and what are its risks? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> A shared model that every system maps to, so adding a system needs one mapping instead of many. Risks: committee-driven design, lowest-common-denominator fields, and a bottleneck on change. Use it for a few stable, widely shared entities; use bounded contexts and explicit mappings elsewhere.</p><p class="qmeta"><b>Tests:</b> Pragmatism about enterprise modeling. <b>Red flag:</b> Wants one enterprise-wide model for everything.</p></div>

<div class="qa"><p class="qq"><span class="qn">14.</span> What is backpressure and how do you implement it? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Backpressure is how a slow consumer slows a fast producer instead of being overwhelmed. Implement it with bounded queues, pull-based consumption, pausing a Kafka consumer while the target throttles, rate limiters, concurrency limits, and returning 429 or 503 from ingestion endpoints.</p><p class="qmeta"><b>Tests:</b> Flow-control awareness. <b>Red flag:</b> Unbounded buffering "to be safe".</p></div>


## APIs and contracts

<div class="qa"><p class="qq"><span class="qn">15.</span> PUT versus PATCH versus POST: which are idempotent and why does it matter? <span class="lvl">Foundation</span></p><p class="qans"><b>Model answer.</b> PUT (replace) and DELETE are idempotent by definition; PATCH (partial update) usually is if it sets values rather than increments them; POST creates and is not idempotent unless the API supports an idempotency key. It matters because retries after timeouts are only safe for idempotent calls.</p><p class="qmeta"><b>Tests:</b> Protocol semantics tied to retries. <b>Red flag:</b> Treats all verbs the same.</p></div>

<div class="qa"><p class="qq"><span class="qn">16.</span> Which pagination styles exist and which do you prefer for extraction? <span class="lvl">Foundation</span></p><p class="qans"><b>Model answer.</b> Offset or page number (simple, but slower deep in the set and unstable when data changes), cursor or token (constant cost, stable), keyset (fast with a sortable key) and link headers. Prefer cursors for full extracts, persist the last cursor as a checkpoint, and never mix paging styles in one request.</p><p class="qmeta"><b>Tests:</b> Practical extraction experience. <b>Red flag:</b> Offset paging over millions of changing rows.</p></div>

<div class="qa"><p class="qq"><span class="qn">17.</span> How do you evolve an API without breaking consumers? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Make only additive, backward-compatible changes (new optional fields, new endpoints), version breaking changes, publish deprecation timelines, use contract tests, and tolerate unknown fields on the consumer side. For events, use schema compatibility modes and a registry.</p><p class="qmeta"><b>Tests:</b> Contract discipline. <b>Red flag:</b> Silent breaking changes "because it is internal".</p></div>

<div class="qa"><p class="qq"><span class="qn">18.</span> Which HTTP status codes must an integration handle explicitly and how? <span class="lvl">Foundation</span></p><p class="qans"><b>Model answer.</b> 2xx success (check per-item results on 207 or bodies); 400 and 422 are permanent validation errors (quarantine); 401 re-authenticate once; 403 stop and alert; 404 depends on context; 409 conflict (version or duplicate); 429 and 503 retry with backoff honoring Retry-After; 5xx transient retry with a cap; timeouts need an idempotent retry.</p><p class="qmeta"><b>Tests:</b> Error classification. <b>Red flag:</b> Retries everything, or nothing.</p></div>

<div class="qa"><p class="qq"><span class="qn">19.</span> How do you design a client around rate limits? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Read the limit and budget from documentation and headers, add a shared token-bucket limiter across workers, back off with jitter on 429, honor Retry-After, prefer bulk endpoints, spread schedules, and monitor remaining quota. Leave headroom for other consumers of the same quota.</p><p class="qmeta"><b>Tests:</b> Operational empathy for the provider. <b>Red flag:</b> Parallelizes until it works.</p></div>

<div class="qa"><p class="qq"><span class="qn">20.</span> REST, GraphQL, gRPC and SOAP: how do you compare them for integration? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> REST: universal, easy to probe. GraphQL: fetch exactly what you need, but query-cost limits and pagination complexity. gRPC: fast, typed, streaming, weaker through some proxies. SOAP: strong contracts and WS-Security, verbose. Choose by consumer, contract and network, not preference.</p><p class="qmeta"><b>Tests:</b> Balanced judgment. <b>Red flag:</b> Dogmatic.</p></div>

<div class="qa"><p class="qq"><span class="qn">21.</span> OpenAPI versus AsyncAPI: how do you use contracts? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> OpenAPI describes request-response HTTP APIs; AsyncAPI describes channels and messages for event-driven APIs. Write the contract first, generate documentation, mocks and clients, validate in CI, and store specs with versions. Pair with schemas and an owner.</p><p class="qmeta"><b>Tests:</b> Contract-first practice. <b>Red flag:</b> Documentation after the fact.</p></div>

<div class="qa"><p class="qq"><span class="qn">22.</span> A bulk endpoint returns 200 but some items failed. How do you handle it? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Never trust the status alone. Parse the per-item results (often 207 Multi-Status or a result array), retry only the transient failures, quarantine the permanent ones with reasons, and report counts in the run summary. Alert when the reject rate crosses a threshold.</p><p class="qmeta"><b>Tests:</b> Partial-failure thinking. <b>Red flag:</b> Marks the run successful.</p></div>

<div class="qa"><p class="qq"><span class="qn">23.</span> How do idempotency keys work and who implements what? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> The client sends a unique key per logical operation; the server stores the key with the result for a retention window and returns the stored result on repeat. The client must generate a stable key per operation (not per attempt) and reuse it on retries.</p><p class="qmeta"><b>Tests:</b> Concrete mechanics. <b>Red flag:</b> Generates a new key per retry.</p></div>

<div class="qa"><p class="qq"><span class="qn">24.</span> How do you design for long-running operations? <span class="lvl">Principal</span></p><p class="qans"><b>Model answer.</b> Accept the request, return 202 with a status URL, process asynchronously, expose status with Retry-After, deliver the result by URL or callback, make submission idempotent, and define expiry for results. Clients poll with a timeout and cap.</p><p class="qmeta"><b>Tests:</b> Asynchronous request-reply. <b>Red flag:</b> Holds an HTTP request open for minutes.</p></div>

<div class="qa"><p class="qq"><span class="qn">25.</span> How do you prevent lost updates when two systems edit the same record? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Use optimistic concurrency: ETags with If-Match, version numbers, or last-modified checks; reject or merge on conflict. Better, avoid the conflict with per-field authority so each field has one writer.</p><p class="qmeta"><b>Tests:</b> Concurrency control. <b>Red flag:</b> Last-writer-wins without thought.</p></div>

<div class="qa"><p class="qq"><span class="qn">26.</span> You get an unfamiliar API. How do you read its documentation? <span class="lvl">Foundation</span></p><p class="qans"><b>Model answer.</b> Look for the machine-readable contract, then base URL and environments, auth and scopes, resource model and identifiers, read paths and filters, write semantics, pagination, limits, error model, async operations and eventing. Probe with curl before designing, record findings in a reconnaissance sheet, and treat the live behavior as the truth.</p><p class="qmeta"><b>Tests:</b> A repeatable method. <b>Red flag:</b> Reads only the quick-start.</p></div>


## Security and identity

<div class="qa"><p class="qq"><span class="qn">27.</span> Compare OAuth 2.0 client credentials, authorization code and JWT bearer flows. <span class="lvl">Foundation</span></p><p class="qans"><b>Model answer.</b> Client credentials: a machine identity gets a scoped, short-lived token: the default for unattended integration. Authorization code with PKCE: a human consents and the app acts as that user. JWT bearer: the client proves identity by signing an assertion with a private key, avoiding a shared secret on the wire.</p><p class="qmeta"><b>Tests:</b> Chooses the flow by who is calling. <b>Red flag:</b> Uses authorization code for a nightly job.</p></div>

<div class="qa"><p class="qq"><span class="qn">28.</span> Where do secrets live and how are they rotated without downtime? <span class="lvl">Foundation</span></p><p class="qans"><b>Model answer.</b> In a vault or platform secret store, never in code, config files, tickets or logs. Rotation: support two active credentials, update the vault, let the runtime re-read at start or on signal, then revoke the old one. Monitor for authentication failures after rotation.</p><p class="qmeta"><b>Tests:</b> Operational security. <b>Red flag:</b> Passwords in config.json.</p></div>

<div class="qa"><p class="qq"><span class="qn">29.</span> How do you secure a webhook endpoint? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Verify an HMAC signature over the body with a timestamp, reject old timestamps, dedupe by event ID, rate-limit and size-limit the endpoint, put it behind a WAF or allowlist where possible, answer quickly and process asynchronously.</p><p class="qmeta"><b>Tests:</b> Layered defense. <b>Red flag:</b> Trusts the source IP alone.</p></div>

<div class="qa"><p class="qq"><span class="qn">30.</span> mTLS, API keys, OAuth: when do you use which? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> OAuth 2.0 for scoped, short-lived, revocable access. mTLS where identity must be bound to the channel (regulated, service mesh, partner links). API keys only when nothing better exists, scoped and rotated, in headers not query strings.</p><p class="qmeta"><b>Tests:</b> Risk-based choice. <b>Red flag:</b> Prefers whichever is easiest.</p></div>

<div class="qa"><p class="qq"><span class="qn">31.</span> What does least privilege mean for an integration account? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> A dedicated identity per integration and environment with only the roles the flows need, reviewed periodically. It gives meaningful audit trails and limits blast radius. Where performance depends on permissions, scope deliberately rather than granting admin.</p><p class="qmeta"><b>Tests:</b> Practical access design. <b>Red flag:</b> One shared admin account.</p></div>

<div class="qa"><p class="qq"><span class="qn">32.</span> How do you protect personal data across topics, logs and copies? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Minimize what is copied; encrypt in transit and at rest; mask or tokenize before broad-access topics; never log full payloads; use field-level encryption with per-subject keys so erasure can be done by destroying the key (crypto-shredding) in immutable logs; document retention.</p><p class="qmeta"><b>Tests:</b> Privacy by design. <b>Red flag:</b> "We will delete it if asked."</p></div>

<div class="qa"><p class="qq"><span class="qn">33.</span> What happens if a token expires mid-run? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Cache tokens and refresh at about 80 percent of lifetime; on a 401 re-authenticate once and retry once; a second 401 stops the run and alerts. Share one token provider across workers with a lock so they do not invalidate each other.</p><p class="qmeta"><b>Tests:</b> Robust auth handling. <b>Red flag:</b> Infinite retry on 401.</p></div>

<div class="qa"><p class="qq"><span class="qn">34.</span> A corporate TLS-inspecting proxy breaks your calls. What do you do? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Install the corporate CA in the runtime trust store, configure the proxy settings, and test from the production host. Never disable certificate verification. Document the trust chain in the runbook.</p><p class="qmeta"><b>Tests:</b> Integrity under pressure. <b>Red flag:</b> verify=False.</p></div>

<div class="qa"><p class="qq"><span class="qn">35.</span> What injection-style risks exist in integrations? <span class="lvl">Principal</span></p><p class="qans"><b>Model answer.</b> XML external entity attacks in SOAP and XML parsing, deserialization of untrusted payloads, server-side request forgery when following URLs from messages, SQL injection in dynamic queries, and prompt injection when AI agents consume tool results. Validate, constrain parsers, allowlist outbound destinations, and treat message content as untrusted data.</p><p class="qmeta"><b>Tests:</b> Security breadth. <b>Red flag:</b> Only considers authentication.</p></div>

<div class="qa"><p class="qq"><span class="qn">36.</span> SAML or OIDC for integrations? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> They are for humans signing in through a browser. Machines use OAuth 2.0 client credentials, JWT assertions or certificates. SSO can govern who administers the integration platform, not how jobs authenticate.</p><p class="qmeta"><b>Tests:</b> Boundary between human and machine identity. <b>Red flag:</b> Suggests SAML for a batch job.</p></div>

<div class="qa"><p class="qq"><span class="qn">37.</span> Which OWASP API risks matter most for integrations? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Object-level authorization (machine clients often see too much), broken authentication (long-lived keys, weak webhook checks), property-level authorization (over-exposed fields), unrestricted resource consumption, SSRF when following URLs from payloads, improper inventory (forgotten endpoints and integrations) and unsafe consumption of third-party APIs.</p><p class="qmeta"><b>Tests:</b> Current security knowledge. <b>Red flag:</b> Only mentions SQL injection.</p></div>

<div class="qa"><p class="qq"><span class="qn">38.</span> How do you threat-model an integration? <span class="lvl">Principal</span></p><p class="qans"><b>Model answer.</b> Draw the data flow with trust boundaries, apply STRIDE to each element and flow, rank threats by likelihood and impact, assign controls and owners, record accepted residual risk, and revisit when the design changes.</p><p class="qmeta"><b>Tests:</b> Structured security thinking. <b>Red flag:</b> "Security will review it."</p></div>


## Data, synchronization and consistency

<div class="qa"><p class="qq"><span class="qn">39.</span> How do you match records between two systems? <span class="lvl">Foundation</span></p><p class="qans"><b>Model answer.</b> Prefer a stored foreign ID on each side; fall back to a natural key (code, number); use name matching only to bootstrap, with collision rules. Renames and merges break name matching and create duplicates.</p><p class="qmeta"><b>Tests:</b> Identity strategy. <b>Red flag:</b> Matches on name forever.</p></div>

<div class="qa"><p class="qq"><span class="qn">40.</span> How do you handle deletes? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Sync a soft-delete flag if present; consume a delete feed if offered but still reconcile; otherwise run a periodic ID-list diff. Add a safety threshold so an abnormal read cannot delete most of the target without approval.</p><p class="qmeta"><b>Tests:</b> Completeness thinking. <b>Red flag:</b> Never considers deletes.</p></div>

<div class="qa"><p class="qq"><span class="qn">41.</span> Describe an incremental sync and its traps. <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Persist a watermark, read changes since watermark minus an overlap, upsert idempotently, advance the watermark only after the whole run succeeds, using the maximum timestamp actually received. Traps: clock skew, late-committed rows, time-zone mix-ups, missed deletes.</p><p class="qmeta"><b>Tests:</b> Practical correctness. <b>Red flag:</b> Sets the watermark to now().</p></div>

<div class="qa"><p class="qq"><span class="qn">42.</span> How do you design bidirectional sync? <span class="lvl">Principal</span></p><p class="qans"><b>Model answer.</b> First try to avoid it with per-field authority. If needed: filter changes made by the integration user, stamp origin, serialize per record with a lease, order changes by time or version, define conflict rules, and reconcile on a schedule.</p><p class="qmeta"><b>Tests:</b> Handles loops, ordering and conflicts. <b>Red flag:</b> Two naive one-way syncs.</p></div>

<div class="qa"><p class="qq"><span class="qn">43.</span> How do you explain eventual consistency to a business stakeholder? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> There will be a short period, with a defined maximum, during which the two systems differ. We choose which system is right during that window, show a timestamp of last sync where it matters, and have a reconcile process to repair drift.</p><p class="qmeta"><b>Tests:</b> Communication. <b>Red flag:</b> Technical jargon only.</p></div>

<div class="qa"><p class="qq"><span class="qn">44.</span> What is a reconciliation job and what does it check? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> A scheduled comparison of source and target: counts per entity, ID-list differences, checksums or sampled field comparisons. It reports drift, optionally repairs it, and runs after incidents.</p><p class="qmeta"><b>Tests:</b> Safety net mindset. <b>Red flag:</b> Trusts incremental sync blindly.</p></div>

<div class="qa"><p class="qq"><span class="qn">45.</span> How do you run an initial load without hurting production? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Throttle, use bulk endpoints or read replicas, schedule off-peak, load in dependency order (entities then relations), checkpoint progress, validate counts and samples, and keep live change capture running so the delta can be applied after the snapshot.</p><p class="qmeta"><b>Tests:</b> Operational care. <b>Red flag:</b> Single huge query at 10:00.</p></div>

<div class="qa"><p class="qq"><span class="qn">46.</span> The source changes its schema. How does your design survive? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Read by field name, validate against an expected set, fail with a precise message, version mappings as configuration, use contract tests in CI, subscribe to change notices, and for events use compatibility modes in a schema registry.</p><p class="qmeta"><b>Tests:</b> Change resilience. <b>Red flag:</b> Positional parsing.</p></div>

<div class="qa"><p class="qq"><span class="qn">47.</span> How do you handle bad records? <span class="lvl">Foundation</span></p><p class="qans"><b>Model answer.</b> Validate, quarantine with a reason and the payload, continue the run, report reject counts, alert above a threshold, and give an owner a way to fix and replay. Never stop the whole run for one record, and never drop silently.</p><p class="qmeta"><b>Tests:</b> Operational pragmatism. <b>Red flag:</b> Crashes or swallows errors.</p></div>

<div class="qa"><p class="qq"><span class="qn">48.</span> What goes wrong with time zones and clocks? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Naive datetimes, daylight saving, systems in different zones, skewed clocks and low-precision timestamps. Use UTC internally, timezone-aware types, server-issued timestamps, overlap windows and NTP everywhere.</p><p class="qmeta"><b>Tests:</b> Detail awareness. <b>Red flag:</b> Assumes everyone uses UTC.</p></div>

<div class="qa"><p class="qq"><span class="qn">49.</span> Describe the main master data management styles. <span class="lvl">Principal</span></p><p class="qans"><b>Model answer.</b> Registry (index of IDs, data stays in sources), consolidation (golden record for analytics), coexistence (golden record synced back to sources) and centralized (hub is the system of entry). Choice depends on how much control you have over source systems and on stewardship capacity.</p><p class="qmeta"><b>Tests:</b> Enterprise data depth. <b>Red flag:</b> Equates MDM with a database.</p></div>

<div class="qa"><p class="qq"><span class="qn">50.</span> How do you preserve ordering? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Define the ordering boundary (per entity), use a key that maps the entity to one partition or queue group, keep a single writer per key, carry a version number so stale updates are ignored, and avoid parallelism across the same key.</p><p class="qmeta"><b>Tests:</b> Practical ordering design. <b>Red flag:</b> Claims global ordering is free.</p></div>

<div class="qa"><p class="qq"><span class="qn">51.</span> How do you move large files or payloads? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Stream in chunks, avoid loading into memory, use manifests with checksums, atomic rename on delivery, claim-check for messages (blob plus reference), and resumable transfers for unreliable links.</p><p class="qmeta"><b>Tests:</b> Scale awareness. <b>Red flag:</b> Base64 in a JSON message.</p></div>


## Kafka and messaging

<div class="qa"><p class="qq"><span class="qn">52.</span> What is a partition and how does ordering work in Kafka? <span class="lvl">Foundation</span></p><p class="qans"><b>Model answer.</b> A partition is an append-only log and the unit of parallelism and ordering. Order is guaranteed only within a partition; the record key decides the partition, so choose the key that defines the ordering boundary (for example the order ID).</p><p class="qmeta"><b>Tests:</b> Core model. <b>Red flag:</b> Believes topic-wide ordering.</p></div>

<div class="qa"><p class="qq"><span class="qn">53.</span> How do consumer groups and rebalances work? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Within a group each partition is assigned to one consumer; different groups each get every record. Joins, leaves, slow processing beyond max.poll.interval.ms or deployments trigger rebalances. Cooperative assignment, the newer KIP-848 protocol and static membership reduce disruption.</p><p class="qmeta"><b>Tests:</b> Operational Kafka. <b>Red flag:</b> Does not know why consumers get kicked out.</p></div>

<div class="qa"><p class="qq"><span class="qn">54.</span> Which settings prevent data loss? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Producer acks=all with idempotence enabled (explicitly in librdkafka-based clients), topic replication factor 3 with min.insync.replicas=2, no unclean leader election, delivery callbacks with a final flush, and manual offset commits after processing on the consumer side.</p><p class="qmeta"><b>Tests:</b> Reliability configuration. <b>Red flag:</b> Only mentions replication.</p></div>

<div class="qa"><p class="qq"><span class="qn">55.</span> Explain Kafka delivery semantics and where exactly-once ends. <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Idempotent producers and transactions give exactly-once within Kafka (consume-transform-produce). Reading from or writing to an external system returns you to at-least-once, so make the sink idempotent.</p><p class="qmeta"><b>Tests:</b> Boundary knowledge. <b>Red flag:</b> Says "Kafka is exactly-once".</p></div>

<div class="qa"><p class="qq"><span class="qn">56.</span> How do you choose the number of partitions? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Take the larger of target throughput divided by per-partition producer throughput and divided by per-partition consumer throughput, add headroom, remember that adding partitions later changes key-to-partition mapping, and avoid excessive counts that slow recovery.</p><p class="qmeta"><b>Tests:</b> Sizing method. <b>Red flag:</b> A round number from habit.</p></div>

<div class="qa"><p class="qq"><span class="qn">57.</span> Retention versus compaction? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Retention deletes old segments by time or size: for event streams. Compaction keeps the latest record per key and uses tombstones for deletes: for current-state topics. A compacted topic bootstraps new consumers with latest state, but is not an audit history.</p><p class="qmeta"><b>Tests:</b> Topic design. <b>Red flag:</b> Compacts an audit stream.</p></div>

<div class="qa"><p class="qq"><span class="qn">58.</span> What does a schema registry give you and which compatibility mode do you choose? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Central schema storage and compatibility checks so producers and consumers can evolve independently. Backward is the common default; use the transitive variants when consumers may replay long histories.</p><p class="qmeta"><b>Tests:</b> Contract governance. <b>Red flag:</b> No schema, plain JSON.</p></div>

<div class="qa"><p class="qq"><span class="qn">59.</span> How do retry topics and dead letter topics work, and what do they cost? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Failed records move to delay topics so the main partition keeps flowing, and after a cap to a DLQ with context headers. The cost is that ordering for that key is no longer guaranteed, and the DLQ needs an owner, alerts and a replay tool.</p><p class="qmeta"><b>Tests:</b> Error-handling design. <b>Red flag:</b> DLQ nobody watches.</p></div>

<div class="qa"><p class="qq"><span class="qn">60.</span> Consumer lag keeps growing. How do you diagnose it? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Is it all partitions or one? All: consumers too slow, target throttling or too few consumers (up to the partition count). One: hot key or a poison record in a retry loop. Check processing time per batch, downstream errors, rebalances, and add time-lag alerts.</p><p class="qmeta"><b>Tests:</b> Diagnostic method. <b>Red flag:</b> Add more consumers blindly.</p></div>

<div class="qa"><p class="qq"><span class="qn">61.</span> What is Kafka Connect and how do you handle errors in it? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> A runtime for source and sink connectors configured by JSON. For errors: errors.tolerance=all with a dead letter queue topic and context headers, retry timeouts, restart failed tasks via the REST API, and idempotent upserts in sinks.</p><p class="qmeta"><b>Tests:</b> Tooling knowledge. <b>Red flag:</b> Writes custom code for everything.</p></div>

<div class="qa"><p class="qq"><span class="qn">62.</span> Kafka versus RabbitMQ, IBM MQ or SQS? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Kafka: replayable partitioned log for high volume, many consumers and stream processing. RabbitMQ and MQ: flexible routing and transactional queues for task distribution. SQS: simple managed queue. Choose by replay, fan-out, ordering, throughput and operational ownership.</p><p class="qmeta"><b>Tests:</b> Fit-for-purpose. <b>Red flag:</b> Kafka for everything.</p></div>

<div class="qa"><p class="qq"><span class="qn">63.</span> The target REST API throttles. How do you push events from Kafka to it? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Use a consumer app or HTTP sink that pulls, calls the API with idempotency keys, and on 429 pauses the partitions (pause and resume) for Retry-After while still polling to stay in the group; classify 4xx as poison (DLQ) and 5xx as transient; keep one in-flight call per key to preserve order.</p><p class="qmeta"><b>Tests:</b> Backpressure with Kafka. <b>Red flag:</b> Buffers unboundedly.</p></div>

<div class="qa"><p class="qq"><span class="qn">64.</span> What changed in Kafka 4.x that an architect should know? <span class="lvl">Principal</span></p><p class="qans"><b>Model answer.</b> ZooKeeper is gone (KRaft only), so older clusters must migrate first; the KIP-848 consumer protocol is available and opt-in (needs broker 4.0 or later and a supporting client); share groups add queue-like consumption, becoming production-ready in 4.2; Java baselines moved to 17 for brokers and 11 for clients.</p><p class="qmeta"><b>Tests:</b> Currency of knowledge. <b>Red flag:</b> Still describes ZooKeeper operations.</p></div>

<div class="qa"><p class="qq"><span class="qn">65.</span> Describe multi-region Kafka strategies. <span class="lvl">Principal</span></p><p class="qans"><b>Model answer.</b> Active-passive with MirrorMaker 2 or cluster linking for DR (offset translation on failover), active-active with prefixed topics and conflict thinking, aggregation from edge clusters to a core cluster, and stretch clusters across three low-latency sites with rack awareness.</p><p class="qmeta"><b>Tests:</b> Topology depth. <b>Red flag:</b> Ignores consumer offsets in failover.</p></div>

<div class="qa"><p class="qq"><span class="qn">66.</span> How do you replay events safely? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Use a new consumer group or reset offsets to a timestamp, confirm retention covers the window, ensure consumers are idempotent or have a dedupe ledger, throttle so live traffic is not starved, and use transitive schema compatibility for old records.</p><p class="qmeta"><b>Tests:</b> Operational replay. <b>Red flag:</b> Resets production offsets without a plan.</p></div>


## Platforms and tools

<div class="qa"><p class="qq"><span class="qn">67.</span> iPaaS, ESB or custom code: how do you decide? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Look at workload shape, where data may be processed, runtime control, team skills, cost curve at year three, lock-in and exit, governance needs and existing enterprise agreements. Validate with a proof of concept on the hardest flow, including failure injection.</p><p class="qmeta"><b>Tests:</b> Structured decision-making. <b>Red flag:</b> Buys whatever the vendor demoed.</p></div>

<div class="qa"><p class="qq"><span class="qn">68.</span> What is API-led connectivity, and when does it help or hurt? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Layer APIs into system, process and experience tiers so back ends are unlocked once, logic is composed centrally and channels are tailored. It helps when many consumers reuse system APIs and governance matters; it hurts in small estates where layers add latency and meetings.</p><p class="qmeta"><b>Tests:</b> Pattern with trade-offs. <b>Red flag:</b> Recites marketing.</p></div>

<div class="qa"><p class="qq"><span class="qn">69.</span> In MuleSoft, what is the difference between on-error-continue and on-error-propagate? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Continue handles the error and treats the owner as successful, committing transactions: use for bad records you quarantine. Propagate handles then re-throws, rolling back: use for transient failures that must retry or alert. A catch-all continue hides failures from monitoring.</p><p class="qmeta"><b>Tests:</b> Practical platform detail. <b>Red flag:</b> Uses continue everywhere.</p></div>

<div class="qa"><p class="qq"><span class="qn">70.</span> Where does an iPaaS agent execute your logic, and why does it matter? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Some products run the runtime in your network and phone home to a cloud control plane; others use an on-premises agent for access while flows execute in the vendor cloud. It decides whether payloads leave your network, which matters for residency and security review.</p><p class="qmeta"><b>Tests:</b> Asks the right procurement question. <b>Red flag:</b> Assumes "agent" means local processing.</p></div>

<div class="qa"><p class="qq"><span class="qn">71.</span> When do cloud-native services beat an iPaaS? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> When the estate is concentrated on one hyperscaler, volumes are high or spiky, the team is engineering-led with Git and CI/CD, and license costs per flow matter. You trade connector convenience and governance tooling for flexibility and cost.</p><p class="qmeta"><b>Tests:</b> Balanced view. <b>Red flag:</b> Dismisses either camp.</p></div>

<div class="qa"><p class="qq"><span class="qn">72.</span> How would you run a proof of concept for an integration platform? <span class="lvl">Principal</span></p><p class="qans"><b>Model answer.</b> Pick the hardest real flow, define success criteria (throughput, error handling, observability, deployment pipeline, cost at projected volume), include failure injection and a security review, have the future owning team build it, and compare against the alternatives on the same flow.</p><p class="qmeta"><b>Tests:</b> Evaluation rigour. <b>Red flag:</b> Happy-path demo.</p></div>

<div class="qa"><p class="qq"><span class="qn">73.</span> What are the risks of citizen integration tools? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Shadow flows with business-critical logic, personal-account credentials, no testing or versioning, data leaving approved boundaries, and unmonitored failures. Mitigate with an inventory, data-loss policies, a promotion path for critical flows and clear ownership.</p><p class="qmeta"><b>Tests:</b> Governance awareness. <b>Red flag:</b> Blocks them all or allows everything.</p></div>

<div class="qa"><p class="qq"><span class="qn">74.</span> When do you use managed file transfer and EDI, and what matters? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> For partner exchange of files and standard business documents. Matters: protocol (AS2, SFTP), certificates and their expiry, acknowledgments (997, CONTRL), per-partner variants, non-repudiation and onboarding repeatability.</p><p class="qmeta"><b>Tests:</b> B2B literacy. <b>Red flag:</b> Treats EDI as legacy noize.</p></div>

<div class="qa"><p class="qq"><span class="qn">75.</span> What is an event mesh? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Interconnected brokers across sites and clouds that route events dynamically to subscribers wherever they are, with topic hierarchies and store-and-forward. It suits multi-site retail, manufacturing and multi-cloud estates; governance of the topic taxonomy is the hard part.</p><p class="qmeta"><b>Tests:</b> Modern messaging breadth. <b>Red flag:</b> Confuses it with a VPN.</p></div>

<div class="qa"><p class="qq"><span class="qn">76.</span> ETL, ELT and reverse ETL: what is the difference? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> ETL transforms before loading; ELT loads raw data and transforms inside the warehouse; reverse ETL pushes curated warehouse data back into operational tools. Each has a different failure surface: connector maintenance, SQL tests and SaaS rate limits respectively.</p><p class="qmeta"><b>Tests:</b> Data platform awareness. <b>Red flag:</b> Uses the terms interchangeably.</p></div>

<div class="qa"><p class="qq"><span class="qn">77.</span> How would you offload events from a mainframe without changing it? <span class="lvl">Principal</span></p><p class="qans"><b>Model answer.</b> Copy what already flows through MQ with an MQ-to-Kafka bridge, and capture table changes from the Db2 log with a CDC product. Respect change freezes and MIPS cost, handle EBCDIC and packed decimals with copybook parsers, and define delivery semantics explicitly.</p><p class="qmeta"><b>Tests:</b> Legacy modernization. <b>Red flag:</b> Proposes new mainframe code.</p></div>


## Hybrid, networking and cloud

<div class="qa"><p class="qq"><span class="qn">78.</span> How do you integrate an on-premises system with a SaaS without opening inbound ports? <span class="lvl">Foundation</span></p><p class="qans"><b>Model answer.</b> Run an agent or runtime inside the network that opens outbound TLS connections to the cloud control plane or target, or poll from inside. Everything is initiated outward, which is why security teams approve it fastest.</p><p class="qmeta"><b>Tests:</b> Network-aware design. <b>Red flag:</b> Asks to open the firewall.</p></div>

<div class="qa"><p class="qq"><span class="qn">79.</span> It works from your laptop but fails from the server. How do you troubleshoot? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Test with curl from the server. Check DNS resolution, proxy settings, TLS trust (private CA or inspection), allowlists and egress IPs, clock skew, and credentials or environment differences. Compare headers and error bodies, not assumptions.</p><p class="qmeta"><b>Tests:</b> Systematic diagnosis. <b>Red flag:</b> Reinstalls things.</p></div>

<div class="qa"><p class="qq"><span class="qn">80.</span> Which private connectivity options exist and what are the traps? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Site-to-site VPN, Direct Connect or ExpressRoute or Interconnect circuits, private link or private endpoints to PaaS, SD-WAN. Traps: lead time of circuits, overlapping IP ranges after mergers, DNS across the boundary, MTU and egress costs.</p><p class="qmeta"><b>Tests:</b> Network literacy. <b>Red flag:</b> Public internet only.</p></div>

<div class="qa"><p class="qq"><span class="qn">81.</span> What are the challenges of multi-cloud integration? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Egress charges, differing identity and secret systems, inconsistent services, latency between clouds, duplicated tooling and skills, and governance. An event backbone or iPaaS can hide some differences but adds a shared dependency.</p><p class="qmeta"><b>Tests:</b> Realistic view. <b>Red flag:</b> "Cloud agnostic" without cost.</p></div>

<div class="qa"><p class="qq"><span class="qn">82.</span> Design store-and-forward for sites with intermittent connectivity. <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> A local broker or queue at the site buffers events, the link forwards them in order when available, events carry unique IDs and timestamps, the core dedupes, and retention at the site exceeds the longest expected outage.</p><p class="qmeta"><b>Tests:</b> Edge reliability. <b>Red flag:</b> Assumes the WAN is always up.</p></div>

<div class="qa"><p class="qq"><span class="qn">83.</span> How do data residency rules shape the design? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> They constrain where payloads may be processed and stored: pick regions, avoid vendor clouds that route data elsewhere, use customer-hosted runtimes or in-region control planes, keep keys in region, and separate metadata from payloads where allowed.</p><p class="qmeta"><b>Tests:</b> Compliance in architecture. <b>Red flag:</b> Ignores sub-processors.</p></div>

<div class="qa"><p class="qq"><span class="qn">84.</span> Why do chatty protocols hurt over a WAN? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Every round trip pays latency; 1,000 sequential calls at 60 ms is a minute of waiting before any work. Batch calls, use bulk endpoints, keep the runtime near the data, and parallelize within limits.</p><p class="qmeta"><b>Tests:</b> Performance reasoning. <b>Red flag:</b> Adds more threads without limit.</p></div>

<div class="qa"><p class="qq"><span class="qn">85.</span> What is a DMZ and how do partners reach internal systems? <span class="lvl">Foundation</span></p><p class="qans"><b>Model answer.</b> A perimeter zone hosting internet-facing components (WAF, API gateway, MFT) so partner traffic terminates there and internal systems accept connections only from those components, never directly from the internet.</p><p class="qmeta"><b>Tests:</b> Network zoning basics. <b>Red flag:</b> Exposes the ERP.</p></div>


## Reliability, operations and performance

<div class="qa"><p class="qq"><span class="qn">86.</span> Explain retries with exponential backoff and jitter. What should you never retry blindly? <span class="lvl">Foundation</span></p><p class="qans"><b>Model answer.</b> Wait longer after each failure (base times two to the attempt, capped) and randomize the delay so clients do not retry in lockstep. Retry transient errors only; never retry non-idempotent writes without an idempotency key, and never retry 4xx validation errors.</p><p class="qmeta"><b>Tests:</b> Core resilience. <b>Red flag:</b> Fixed-interval infinite retries.</p></div>

<div class="qa"><p class="qq"><span class="qn">87.</span> What is a circuit breaker and when does it help? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> It counts consecutive failures to a dependency and, past a threshold, fails fast for a cool-down, then probes (half-open). It stops you hammering a failing system and protects your own threads and queues.</p><p class="qmeta"><b>Tests:</b> Resilience pattern. <b>Red flag:</b> Never heard of it.</p></div>

<div class="qa"><p class="qq"><span class="qn">88.</span> What do you monitor for an integration? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Heartbeat or last-success time, freshness (age of newest synced record), records read, written, skipped and rejected, error rate by class, retry counts, queue or consumer lag, DLQ depth, latency, and quota usage. Alert on absence of success, not only on errors.</p><p class="qmeta"><b>Tests:</b> Observability design. <b>Red flag:</b> Only CPU and memory.</p></div>

<div class="qa"><p class="qq"><span class="qn">89.</span> How would you know an integration is silently failing? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> A heartbeat alert for missing runs, freshness SLOs, run summaries with counts and expected ranges, reconcile jobs, and alerts on unexpected zeros or sudden drops. Silence must look unhealthy.</p><p class="qmeta"><b>Tests:</b> Detects the absence of signals. <b>Red flag:</b> Waits for user complaints.</p></div>

<div class="qa"><p class="qq"><span class="qn">90.</span> What belongs in a runbook? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Purpose and diagram, how to run, rerun, backfill and pause; where logs, metrics and quarantine live; how to read the run summary; top failure modes and fixes; secret and certificate rotation; escalation contacts; and the kill switch.</p><p class="qmeta"><b>Tests:</b> Operational readiness. <b>Red flag:</b> "Read the code."</p></div>

<div class="qa"><p class="qq"><span class="qn">91.</span> How do you design disaster recovery for an integration? <span class="lvl">Principal</span></p><p class="qans"><b>Model answer.</b> Classify by tier with RPO and RTO; identify the state that must survive (watermarks, offsets, ledgers, queues, config, secrets, certificates); replicate or back it up; keep configuration as code; plan runtime failover and DNS; ensure replay from the source or from a replicated log; and rehearse in game days.</p><p class="qmeta"><b>Tests:</b> Resilience at system level. <b>Red flag:</b> Backs up only the database.</p></div>

<div class="qa"><p class="qq"><span class="qn">92.</span> How do you tune performance? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Measure first. Then batch requests, use bulk endpoints, paginate with cursors, parallelize within rate limits, reuse connections, avoid per-row lookups with caches or joins, compress payloads, and move the runtime close to the data.</p><p class="qmeta"><b>Tests:</b> Evidence-based tuning. <b>Red flag:</b> Guesses.</p></div>

<div class="qa"><p class="qq"><span class="qn">93.</span> Walk me through a capacity calculation. <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Example: 5 million rows nightly in a 2 hour window needs about 700 rows per second. If the API allows 10 calls per second with 100 rows per call, that is 1,000 rows per second: feasible with bulk calls but not with single-row calls (10 per second would take almost six days). State assumptions, add headroom for retries.</p><p class="qmeta"><b>Tests:</b> Back-of-envelope rigour. <b>Red flag:</b> No arithmetic.</p></div>

<div class="qa"><p class="qq"><span class="qn">94.</span> What is your testing strategy for integrations? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Unit tests for mappings, contract tests against recorded or sandbox responses, failure injection (kill, throttle, corrupt, duplicate), volume tests at production scale, reconciliation as acceptance evidence, and a repeatable test dataset.</p><p class="qmeta"><b>Tests:</b> Quality engineering. <b>Red flag:</b> Manual demo only.</p></div>

<div class="qa"><p class="qq"><span class="qn">95.</span> How do you release and roll back an integration safely? <span class="lvl">Principal</span></p><p class="qans"><b>Model answer.</b> Build once, promote the same artifact through environments, version mappings as configuration, deploy with a kill switch, run in shadow mode when possible, keep the watermark and ledgers compatible across versions, and be able to replay from the previous checkpoint.</p><p class="qmeta"><b>Tests:</b> Change safety. <b>Red flag:</b> Edits production flows in the UI.</p></div>

<div class="qa"><p class="qq"><span class="qn">96.</span> How do you trace one transaction across a queue or Kafka? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Carry W3C Trace Context (traceparent) in message headers: inject on send and extract on receive with OpenTelemetry, use span links for batch consumers, and put trace and entity IDs in every log line.</p><p class="qmeta"><b>Tests:</b> Observability across async boundaries. <b>Red flag:</b> Searches logs by timestamp.</p></div>

<div class="qa"><p class="qq"><span class="qn">97.</span> Which SLIs and SLOs fit an integration? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Freshness, completeness, correctness, availability of receivers and APIs, headroom against limits, and reject rate, each with a target and an error budget that decides when reliability work comes first.</p><p class="qmeta"><b>Tests:</b> Measurable reliability. <b>Red flag:</b> Uptime of the server only.</p></div>


## Governance, cost and vendor judgment

<div class="qa"><p class="qq"><span class="qn">98.</span> What criteria decide build versus buy? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Differentiation (is this core to the business), time to value, total cost over three years including run and change, skills and capacity, control and compliance needs, connector availability, lock-in and exit cost, and vendor viability.</p><p class="qmeta"><b>Tests:</b> Commercial judgment. <b>Red flag:</b> Preference-based.</p></div>

<div class="qa"><p class="qq"><span class="qn">99.</span> How do you estimate the total cost of ownership of an integration platform? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Include licenses or consumption, infrastructure, implementation, skilled staff, support, upgrades, training, monitoring, and the cost of change over three years. Model volume growth and the price curve rather than year one only.</p><p class="qmeta"><b>Tests:</b> Financial literacy. <b>Red flag:</b> Looks at license only.</p></div>

<div class="qa"><p class="qq"><span class="qn">100.</span> How do you document architecture decisions? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Architecture decision records: context, options, decision, reasons, consequences and revisit triggers, stored with the code. They explain why, which is what future teams cannot recover from diagrams.</p><p class="qmeta"><b>Tests:</b> Knowledge continuity. <b>Red flag:</b> Wiki pages nobody updates.</p></div>

<div class="qa"><p class="qq"><span class="qn">101.</span> How do you limit vendor lock-in? <span class="lvl">Principal</span></p><p class="qans"><b>Model answer.</b> Own the contracts (OpenAPI, AsyncAPI, schemas), keep business logic in portable forms where practical, keep mappings as exportable configuration, use open protocols (Kafka, OAuth, CloudEvents, OpenLineage), and know the exit cost before signing.</p><p class="qmeta"><b>Tests:</b> Strategic thinking. <b>Red flag:</b> "We will never leave."</p></div>

<div class="qa"><p class="qq"><span class="qn">102.</span> How do you govern APIs and events at scale? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Catalog them with owners, versioning and deprecation policies, enforce design standards and security policies through gateways and CI checks, register schemas with compatibility rules, track consumers, and retire what nobody uses.</p><p class="qmeta"><b>Tests:</b> Platform governance. <b>Red flag:</b> Governance by committee only.</p></div>

<div class="qa"><p class="qq"><span class="qn">103.</span> How do you keep an inventory of integrations and their lineage? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Harvest from the platforms (APIs, exports, connector configs), tag owners and criticality, emit lineage as OpenLineage where tools support it, stitch with catalog connectors, and review citizen-built flows on a schedule.</p><p class="qmeta"><b>Tests:</b> Estate visibility. <b>Red flag:</b> Spreadsheet of hopes.</p></div>

<div class="qa"><p class="qq"><span class="qn">104.</span> Center of excellence or federated teams? <span class="lvl">Principal</span></p><p class="qans"><b>Model answer.</b> Central teams ensure standards but become queues; federated teams move faster and drift. A platform team providing paved roads (templates, pipelines, guardrails) plus federated delivery is the usual compromize.</p><p class="qmeta"><b>Tests:</b> Organizational design. <b>Red flag:</b> Dogmatic.</p></div>

<div class="qa"><p class="qq"><span class="qn">105.</span> How do you decide what is reusable? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Reuse system-level building blocks that several consumers need (an API over a back end, a schema) and avoid premature generalization of process logic. Publish with owners, SLAs and documentation, and measure actual reuse.</p><p class="qmeta"><b>Tests:</b> Pragmatic reuse. <b>Red flag:</b> Reusable everything.</p></div>

<div class="qa"><p class="qq"><span class="qn">106.</span> What is a data contract, and how does it relate to integrations? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> An agreement between producer and consumers of data covering schema, meaning, quality rules, service levels and ownership, in a machine-readable file (for example ODCS) that CI and monitoring can check. It formalizes the mapping spec and authority decisions for streams and datasets.</p><p class="qmeta"><b>Tests:</b> Data governance link. <b>Red flag:</b> Thinks it is a legal document only.</p></div>

<div class="qa"><p class="qq"><span class="qn">107.</span> How would you set up an integration operating model in a large company? <span class="lvl">Principal</span></p><p class="qans"><b>Model answer.</b> A platform team providing a paved road (runtimes, templates, pipelines, connectors, guardrails), federated delivery by domain teams, a fast lane for standard patterns and light review for high-risk designs, an inventory and catalogs, standards, and KPIs reviewed quarterly.</p><p class="qmeta"><b>Tests:</b> Organizational design. <b>Red flag:</b> A central team that builds everything.</p></div>

<div class="qa"><p class="qq"><span class="qn">108.</span> Which KPIs show that an integration estate is healthy? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Share of integrations with owner, runbook and alerts; incidents and time to restore; change failure rate; lead time; reuse; integrations on deprecated platforms; credentials past rotation; run cost per integration.</p><p class="qmeta"><b>Tests:</b> Estate management. <b>Red flag:</b> Number of integrations built.</p></div>


## API and event design (provider side)

<div class="qa"><p class="qq"><span class="qn">109.</span> How would you design an API that integrators will thank you for? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Contract first. Stable opaque IDs and upsert by external key; an updatedSince filter with server timestamps plus a way to detect deletes; cursor pagination; idempotent writes with an Idempotency-Key for creates; bulk or asynchronous endpoints for volume; one error format (RFC 9457 problem details) with correlation IDs; documented limits with 429 and Retry-After; versioning and deprecation policy; a realistic sandbox and a changelog.</p><p class="qmeta"><b>Tests:</b> Empathy for consumers turned into concrete rules. <b>Red flag:</b> Talks only about URL naming.</p></div>

<div class="qa"><p class="qq"><span class="qn">110.</span> Thin or fat webhook payloads? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Thin payloads (ID and event type) force the consumer to fetch current state, so they are never stale and leak little, at the cost of extra calls and a read API. Fat payloads carry full state, saving calls, but become a public contract and can arrive out of order, so they need a version field. Choose per consumer need and data sensitivity.</p><p class="qmeta"><b>Tests:</b> Trade-off reasoning. <b>Red flag:</b> One answer for every case.</p></div>

<div class="qa"><p class="qq"><span class="qn">111.</span> You provide webhooks to partners. How do you make them reliable? <span class="lvl">Principal</span></p><p class="qans"><b>Model answer.</b> Record events in an outbox in the same transaction as the business change; a dispatcher signs and delivers them; retry with backoff for hours; unique event IDs for dedupe; a delivery log and a replay endpoint; verify new endpoints; disable and notify after repeated failure; document that ordering is not guaranteed and include versions.</p><p class="qmeta"><b>Tests:</b> Provider-side reliability. <b>Red flag:</b> Fire-and-forget POSTs.</p></div>

<div class="qa"><p class="qq"><span class="qn">112.</span> How do you deprecate an API version without breaking consumers? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Announce with a timeline, publish a migration guide, send deprecation and Sunset headers, measure usage per client, contact remaining consumers directly, optionally run brownouts, and retire only after usage reaches zero or the deadline passes with sign-off.</p><p class="qmeta"><b>Tests:</b> Lifecycle discipline. <b>Red flag:</b> Switches it off on the announced date regardless.</p></div>

<div class="qa"><p class="qq"><span class="qn">113.</span> What makes a good event? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> A past-tense business name, the entity key, a per-entity version, the event time, a unique ID, a standard envelope, a registered schema with a compatibility mode, a stated ordering guarantee and retention, and a named owner.</p><p class="qmeta"><b>Tests:</b> Event contract thinking. <b>Red flag:</b> Publishes database rows.</p></div>


## Data formats and transformation

<div class="qa"><p class="qq"><span class="qn">114.</span> Why should you never use floating point for money? <span class="lvl">Foundation</span></p><p class="qans"><b>Model answer.</b> Binary floating point cannot represent most decimal fractions exactly, so sums drift by fractions of a cent. Use decimal types or integer minor units end to end, carry the currency, and document one rounding rule.</p><p class="qmeta"><b>Tests:</b> Attention to detail. <b>Red flag:</b> "Floats are fine for two decimals."</p></div>

<div class="qa"><p class="qq"><span class="qn">115.</span> What is the difference between null, empty and missing, and why does it matter? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Null usually means unknown, empty means deliberately blank, missing means not sent. In partial updates, missing should usually leave the target unchanged while null or empty may clear it. Define the meaning per field in the mapping, or updates will wipe data.</p><p class="qmeta"><b>Tests:</b> Semantics in mapping. <b>Red flag:</b> Treats them as the same.</p></div>

<div class="qa"><p class="qq"><span class="qn">116.</span> How do you handle code lists between systems? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> As governed reference data: versioned mapping tables with an owner, loaded by the integration, with unmapped values quarantined rather than guessed. Changes are reviewed by the data owner and tested with golden files.</p><p class="qmeta"><b>Tests:</b> Governance of mappings. <b>Red flag:</b> Hard-coded if statements.</p></div>

<div class="qa"><p class="qq"><span class="qn">117.</span> What goes into a mapping specification, and who signs it? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> For each target field: source, transformation rule, default or missing behavior, validation, and owner. Data owners sign it because it encodes business meaning; testers derive cases from it; support uses it to answer questions.</p><p class="qmeta"><b>Tests:</b> Deliverable mindset. <b>Red flag:</b> The code is the spec.</p></div>


## Testing and delivery

<div class="qa"><p class="qq"><span class="qn">118.</span> How do you test against a vendor API you do not control? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Validate recorded and sandbox responses against the vendor's OpenAPI in CI, mock from the contract for fast tests, run integration tests against the sandbox, inject failures with a fault proxy, keep a consumer contract of what you rely on, and watch the vendor changelog.</p><p class="qmeta"><b>Tests:</b> Layered strategy. <b>Red flag:</b> Only manual testing in the sandbox.</p></div>

<div class="qa"><p class="qq"><span class="qn">119.</span> Which failure scenarios must pass before go-live? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Kill mid-run, rerun the same input, 429 with Retry-After, sustained 503, token expiry, malformed record, duplicate message, out-of-order update, slow network, schema change, clock skew, and production-sized volume.</p><p class="qmeta"><b>Tests:</b> Failure imagination. <b>Red flag:</b> Happy path only.</p></div>

<div class="qa"><p class="qq"><span class="qn">120.</span> What is consumer-driven contract testing? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Consumers publish the interactions they depend on; the provider verifies those contracts in its pipeline before releasing. It catches breaking changes before deployment rather than in production.</p><p class="qmeta"><b>Tests:</b> Contract testing knowledge. <b>Red flag:</b> Confuses it with schema linting only.</p></div>

<div class="qa"><p class="qq"><span class="qn">121.</span> You deploy a new version of a Kafka consumer blue-green. What can go wrong? <span class="lvl">Principal</span></p><p class="qans"><b>Model answer.</b> If green joins the same consumer group, partitions are split between blue and green, so both versions process live traffic. If it uses a new group, both process every message and duplicates appear. Hand over deliberately (stop blue consumers, then start green), keep processing idempotent, and keep state formats compatible.</p><p class="qmeta"><b>Tests:</b> Platform-aware release thinking. <b>Red flag:</b> Assumes traffic switching works like HTTP.</p></div>

<div class="qa"><p class="qq"><span class="qn">122.</span> How do you promote integration changes between environments? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Build once, promote the same artifact, take configuration from the environment and secrets from a vault, apply infrastructure, topics, connectors and policies as code, and require approvals with test evidence.</p><p class="qmeta"><b>Tests:</b> Delivery discipline. <b>Red flag:</b> Rebuilds or hand-edits per environment.</p></div>

<div class="qa"><p class="qq"><span class="qn">123.</span> An integration wrote bad data to production. How do you roll back? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> You cannot undeploy data. Stop it with the kill switch, scope the damage from logs and run summaries, deploy the fix, run a forward-correction job or replay from the last good checkpoint, then reconcile and report.</p><p class="qmeta"><b>Tests:</b> Incident realism. <b>Red flag:</b> "Redeploy the old version" and stop there.</p></div>


## SaaS platforms

<div class="qa"><p class="qq"><span class="qn">124.</span> How do you avoid duplicates when loading data into Salesforce? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Use an external ID field and upsert by it; use Bulk API 2.0 for volume; check per-record results; remember that triggers and flows fire on your writes.</p><p class="qmeta"><b>Tests:</b> Platform-specific idempotency. <b>Red flag:</b> Insert then dedupe later.</p></div>

<div class="qa"><p class="qq"><span class="qn">125.</span> Your integration reads fewer fields from ServiceNow or Salesforce than the documentation shows. Why? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Permissions: ACLs, roles or field-level security on the integration user hide fields, and the API returns what that user may see. Test with the integration user and request the access explicitly.</p><p class="qmeta"><b>Tests:</b> Permission awareness. <b>Red flag:</b> Blames the API.</p></div>

<div class="qa"><p class="qq"><span class="qn">126.</span> How do you get changes from Microsoft Graph reliably? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Delta queries with stored delta tokens for incremental reads, change notifications for speed, scheduled renewal of notification subscriptions before they expire, and a delta-query reconcile to cover missed notifications; handle 429 with Retry-After.</p><p class="qmeta"><b>Tests:</b> Notification plus reconcile. <b>Red flag:</b> Relies on notifications alone.</p></div>

<div class="qa"><p class="qq"><span class="qn">127.</span> What is special about integrating with Workday? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Effective dating (changes entered today may take effect later), future-dated hires and terminations, Reports-as-a-Service for extraction, an Integration System User whose security groups decide visible data, and versioned SOAP web services.</p><p class="qmeta"><b>Tests:</b> Domain-specific traps. <b>Red flag:</b> Treats it like a simple CRUD API.</p></div>

<div class="qa"><p class="qq"><span class="qn">128.</span> How do you integrate with SAP S/4HANA without custom code in SAP? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Use released OData APIs and SOAP services for synchronous work, business events or IDocs for asynchronous flows, and SAP Integration Suite or an iPaaS connector in between; respect authorizations and clean-core principles.</p><p class="qmeta"><b>Tests:</b> Modern SAP integration. <b>Red flag:</b> Proposes direct table writes.</p></div>


## Questions managers and executives ask

<div class="qa"><p class="qq"><span class="qn">129.</span> How long will it take? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Give a range with assumptions: base the estimate on entities, systems, auth and network complexity, bidirectionality, volume and compliance, add lead times for accounts, firewall changes and security review, and state what would move it. Offer a staged plan: a thin vertical slice first, then hardening.</p><p class="qmeta"><b>Tests:</b> Estimation under uncertainty. <b>Red flag:</b> One number with no assumptions.</p></div>

<div class="qa"><p class="qq"><span class="qn">130.</span> What will it cost to build and to run? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Build: effort by phase. Run: licenses or cloud consumption, support staff, monitoring, certificate and secret operations, change requests, and periodic upgrades. Show a three-year view with volume growth and name the main cost drivers.</p><p class="qmeta"><b>Tests:</b> Financial framing. <b>Red flag:</b> Quotes build only.</p></div>

<div class="qa"><p class="qq"><span class="qn">131.</span> What are the biggest risks? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Typically: unclear data ownership, lead times (security review, firewall, accounts), source API limits or changes, data quality, ownership after go-live, and test realism. Present each with likelihood, impact and mitigation, and ask the sponsor for decisions on the top three.</p><p class="qmeta"><b>Tests:</b> Risk communication. <b>Red flag:</b> Generic list.</p></div>

<div class="qa"><p class="qq"><span class="qn">132.</span> Why can't we just use the tool we already own? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> We probably can: evaluate it against this workload (connectors, throughput, hosting, security, cost at volume, skills). Reuse is the default if it fits; if there are gaps, quantify them and compare the cost of the gap with the cost of another platform.</p><p class="qmeta"><b>Tests:</b> Humility and evidence. <b>Red flag:</b> Dismisses existing tools.</p></div>

<div class="qa"><p class="qq"><span class="qn">133.</span> What if the vendor changes its API? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Contract tests detect it early, versioned and facade-isolated integrations limit the blast radius, vendor change notices are subscribed, and a runbook covers emergency fixes. The risk is real; the design makes it manageable.</p><p class="qmeta"><b>Tests:</b> Change resilience. <b>Red flag:</b> "They won't."</p></div>

<div class="qa"><p class="qq"><span class="qn">134.</span> How will we know it works? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Acceptance tests with agreed numbers, reconciliation reports comparing source and target counts and samples, a freshness dashboard, error-rate alerts, and a hypercare period with exit criteria.</p><p class="qmeta"><b>Tests:</b> Evidence-based acceptance. <b>Red flag:</b> A demo.</p></div>

<div class="qa"><p class="qq"><span class="qn">135.</span> What do you need from my team? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Named business owner and technical contacts, authority decisions per field, credentials and environments with lead times, test data and acceptance time, an ops owner for after go-live, and quick answers to open questions.</p><p class="qmeta"><b>Tests:</b> Dependency management. <b>Red flag:</b> Vague.</p></div>

<div class="qa"><p class="qq"><span class="qn">136.</span> We are late. What can we cut? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Cut scope, not safety: reduce entities or fields, defer bidirectional features, start with one-way sync, accept a longer freshness target, and postpone dashboards. Do not cut idempotency, error handling, monitoring or the runbook.</p><p class="qmeta"><b>Tests:</b> Principled trade-offs. <b>Red flag:</b> Skips testing.</p></div>

<div class="qa"><p class="qq"><span class="qn">137.</span> Explain this integration to the CFO in two minutes. <span class="lvl">Principal</span></p><p class="qans"><b>Model answer.</b> One diagram, one sentence of business value, the numbers (volume, cost, savings or risk avoided), the main risk and the decision needed. No protocol names.</p><p class="qmeta"><b>Tests:</b> Executive communication. <b>Red flag:</b> Walks through the technology.</p></div>

<div class="qa"><p class="qq"><span class="qn">138.</span> Who supports it after you leave? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> A named operations owner with a runbook, alerts routed to their channel, knowledge transfer sessions, documented decisions, and a hypercare period where we still fix issues. Ownership is agreed before go-live.</p><p class="qmeta"><b>Tests:</b> Sustainability. <b>Red flag:</b> "The vendor will."</p></div>

<div class="qa"><p class="qq"><span class="qn">139.</span> What happens if it fails during month-end close or peak season? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Know the criticality tier: critical flows have 24x7 alerting, tested replay and a manual fallback procedure agreed with the business; freeze windows protect peaks; the runbook says what to do in the first 30 minutes.</p><p class="qmeta"><b>Tests:</b> Business continuity. <b>Red flag:</b> No fallback.</p></div>


## Behavioral and judgment

<div class="qa"><p class="qq"><span class="qn">140.</span> Tell me about an integration that failed in production. What did you learn? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Structure: context, what failed (symptom and root cause), detection, response, fix, and the lasting change (alerts, tests, design). Show ownership, not blame, and a concrete improvement.</p><p class="qmeta"><b>Tests:</b> Honesty and learning. <b>Red flag:</b> Claims nothing ever failed.</p></div>

<div class="qa"><p class="qq"><span class="qn">141.</span> A stakeholder insists on real-time but does not need it. What do you do? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Ask what decision depends on the data and how stale it can be, show the cost and risk difference between five minutes and five seconds, propose a measurable target and a path to tighten it later.</p><p class="qmeta"><b>Tests:</b> Requirement shaping. <b>Red flag:</b> Builds it as asked.</p></div>

<div class="qa"><p class="qq"><span class="qn">142.</span> The client has chosen a tool you think is wrong. What do you do? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Test the assumption with a proof of concept on a hard flow, document the risks and mitigations as an ADR, escalate with evidence, and if the decision stands, design to reduce the risk and record it.</p><p class="qmeta"><b>Tests:</b> Professional disagreement. <b>Red flag:</b> Refuses or stays silent.</p></div>

<div class="qa"><p class="qq"><span class="qn">143.</span> Mid-project you discover the source API lacks a needed feature. What now? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Quantify the impact, explore alternatives (other endpoints, bulk export, CDC, webhook plus reconcile, vendor roadmap or support), propose options with cost and schedule, and get a decision from the sponsor.</p><p class="qmeta"><b>Tests:</b> Problem solving and communication. <b>Red flag:</b> Hides it.</p></div>

<div class="qa"><p class="qq"><span class="qn">144.</span> Two teams both claim to own a field. How do you resolve it? <span class="lvl">Principal</span></p><p class="qans"><b>Model answer.</b> Facilitate an authority decision based on who creates and maintains the value; if both genuinely must edit, split the field or define append-only semantics with origin tags; document the decision and the exception rules.</p><p class="qmeta"><b>Tests:</b> Facilitation. <b>Red flag:</b> Builds conflict resolution to avoid the conversation.</p></div>

<div class="qa"><p class="qq"><span class="qn">145.</span> How do you keep documentation current? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Keep it near the code (README, ADRs, specs in Git), generate what can be generated (OpenAPI docs, diagrams from config), make the runbook part of the release checklist, and review it after every incident.</p><p class="qmeta"><b>Tests:</b> Pragmatism. <b>Red flag:</b> Documents at the end.</p></div>

<div class="qa"><p class="qq"><span class="qn">146.</span> How do you hand over to the operations team? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> Walk the runbook with them, run a failure-injection session together, give them access and alerts early, have them perform a rotation and a replay, and define the hypercare exit criteria.</p><p class="qmeta"><b>Tests:</b> Transition quality. <b>Red flag:</b> Emails a document.</p></div>

<div class="qa"><p class="qq"><span class="qn">147.</span> You have four weeks. How do you choose what to build? <span class="lvl">Senior</span></p><p class="qans"><b>Model answer.</b> A thin vertical slice with the highest-value entity, end to end through production-like conditions, with idempotency, error handling and monitoring, then expand. Delivering breadth without reliability is the usual trap.</p><p class="qmeta"><b>Tests:</b> Prioritization. <b>Red flag:</b> Builds everything shallowly.</p></div>


## Whiteboard exercises

<div class="qa"><p class="qq"><span class="qn">148.</span> Design bidirectional sync between an ITSM tool and a governance catalog for issues. <span class="lvl">Principal</span></p><p class="qans"><b>Model answer.</b> Clarify: authority per field (incident state owned by ITSM, description by catalog, comments append-only), volumes and freshness (minutes). Design: polling sync service in the customer network, config asset with status mapping, stored foreign ID, filter integration user, locks with lease, checkpoints per side, nightly reconcile, run summary and alerts. Risks: renames, unmapped statuses, lock timeouts.</p><p class="qmeta"><b>Tests:</b> Structured approach: clarify, decide authority, pick pattern, handle loops and failures. <b>Red flag:</b> Starts drawing before asking questions.</p></div>

<div class="qa"><p class="qq"><span class="qn">149.</span> Real-time stock across 1,200 stores and the cloud, stores must keep trading offline. <span class="lvl">Principal</span></p><p class="qans"><b>Model answer.</b> Store brokers with store-and-forward, event mesh or Kafka with cluster linking to the core, hierarchical topics, idempotent consumers, a compacted state topic for current stock, summarized events to ERP, device certificates, clock handling, and reconcile with periodic counts.</p><p class="qmeta"><b>Tests:</b> Edge reliability and event design. <b>Red flag:</b> Central API calls from every till.</p></div>

<div class="qa"><p class="qq"><span class="qn">150.</span> Load 5 million ERP rows nightly into a catalog within a two-hour window. <span class="lvl">Principal</span></p><p class="qans"><b>Model answer.</b> Compute throughput (about 700 rows per second), check API limits (single-row calls fail the window), use bulk import or file-based load, manifest and validation, two-pass load (entities then relations), snapshot with delete detection and a safety threshold, checkpoints, and reconcile.</p><p class="qmeta"><b>Tests:</b> Arithmetic and bulk thinking. <b>Red flag:</b> Loops over a REST API.</p></div>

<div class="qa"><p class="qq"><span class="qn">151.</span> Expose a legacy SOAP service to a mobile app securely. <span class="lvl">Principal</span></p><p class="qans"><b>Model answer.</b> Facade or anti-corruption layer translating SOAP to a clean REST API, behind an API gateway with OAuth 2.0, rate limits and WAF, back-end credentials in a vault, caching where safe, timeouts and circuit breakers, observability and a contract.</p><p class="qmeta"><b>Tests:</b> Layered security and facade design. <b>Red flag:</b> Calls SOAP from the app.</p></div>

<div class="qa"><p class="qq"><span class="qn">152.</span> Move a 10 TB on-premises database to a cloud warehouse with minimal downtime. <span class="lvl">Principal</span></p><p class="qans"><b>Model answer.</b> Initial snapshot copied through private connectivity while CDC captures changes from a recorded log position; apply the delta; validate with counts, checksums and sampling; parallel run; cut over in a freeze window; keep rollback and reverse replication for a period.</p><p class="qmeta"><b>Tests:</b> Migration discipline. <b>Red flag:</b> One big dump over a weekend.</p></div>

<div class="qa"><p class="qq"><span class="qn">153.</span> A company runs five integration tools. What strategy do you propose? <span class="lvl">Principal</span></p><p class="qans"><b>Model answer.</b> Inventory flows and owners, classify by workload, define a target platform per class with guardrails, stop new work on the sunset tools, migrate by value and risk, govern citizen tools, and measure reuse and cost. Avoid a big-bang rewrite.</p><p class="qmeta"><b>Tests:</b> Portfolio strategy. <b>Red flag:</b> Standardize on one tool for everything.</p></div>




# Appendix C. Workshop Scenario Cards

Ten realistic situations, described in technology-neutral terms. For each, cover the design and discuss what you would do; then compare. Use them as exercises in a study group, as workshop material for a team, or as templates for describing your own client scenarios. Each card gives the context, the constraints, a recommended design with its reasoning, and the traps. They are composites, not accounts of real engagements.

## Scenario 1: Ticket Synchronization Between a Service Desk and a Governance Tool

**Context.** A bank tracks data-quality problems as issues in a governance tool and as incidents in its service-desk platform. Stewards want one lifecycle across both.

**Constraints.** Both teams edit; comments must flow both ways; the service desk has strict rate limits; the integration host can only call out.

**Design.** A polling integration every two to five minutes, with a configuration document in the governance tool holding status aliases and mappings for each direction. Per-field authority: incident state belongs to the service desk, issue description to the governance tool, and comments are append-only with an origin tag. A stored foreign ID on the issue, never name matching after the first link. Echo-loop prevention by ignoring the integration's own user, and locks with lease expiry for parallel workers. The incident is created only when the issue reaches an agreed status, to avoid noise.

**Why.** Per-field authority turns one bidirectional merge into mostly one-way flows (Chapter 7).

**Traps.** Renaming an issue duplicates it if matching is by name; unmapped statuses skip silently; time-zone assumptions in change ordering; lock timeouts shorter than a slow API call.

**Ask the client.** Which statuses exist on both sides? Who may close? What happens when a ticket is reopened in the service desk after the issue closed in the governance tool?

## Scenario 2: ERP Master Data, Nightly Bulk

**Context.** A manufacturer wants material and supplier master data described in a catalog. The ERP team will not allow API access during business hours but can produce nightly extracts.

**Design.** A scheduled file delivery to a landing area, with a manifest of row counts and checksums, and a loader that validates, transforms, and upserts through a bulk import. A full snapshot each night, because reference data is small, with delete detection by ID-list comparison and a 20 percent safety threshold.

**Why.** Files respect the ERP team's constraints, leave an audit trail, and make reruns trivial; a snapshot makes drift self-healing.

**Traps.** Encoding of special characters in names; leading zeros lost in material numbers (treat as text); duplicate keys across plants; files that arrive late or twice.

## Scenario 3: CRM Change Events into a Data Platform

**Context.** A retailer wants customer changes from its CRM in analytics within a minute, and available to three other teams without each integrating separately.

**Design.** A change-event stream (or CDC) into Kafka keyed by customer ID; event-carried state with a version field; a compacted state topic and a retained event topic; a sink connector to the warehouse with upsert; a schema registry with backward-transitive compatibility; personal fields tokenized before publication.

**Why.** Fan-out and replay justify Kafka; keyed ordering keeps per-customer updates coherent; the state topic gives a new consumer an immediate bootstrap.

**Traps.** Customer merges and unmerges (the key changes); hot keys for large business accounts; deletion requests (tombstones and crypto-shredding); the CRM's API limits for a backfill.

## Scenario 4: A Legacy Partner with SOAP and SFTP

**Context.** An insurer exchanges claims data with a partner that supports only a SOAP service for status lookups and an SFTP drop for daily claim files.

**Design.** A thin adapter that wraps the SOAP calls behind a clean REST interface for internal consumers, and an SFTP poller with trigger-file semantics, a checksum ledger, and schema validation. Every file and SOAP exchange is stored raw for audit.

**Why.** You cannot change the partner, so contain the awkwardness. The facade gives the enterprise a stable contract and a place to enforce retries and observability.

**Traps.** Expiring WS-Security certificates; XML namespaces that change without notice; the partner's business-hours-only availability; large files that time out mid-transfer (require resume support).

## Scenario 5: A Product Information System Behind a Customer Firewall

**Context.** A retailer's cloud product information system holds logical attributes and physical columns. Governance wants them in a catalog as a logical model linked to physical columns.

**Design.** An integration on a customer-network server, outbound only: call the product system's APIs, map entities and fields into the catalog's logical model with properties (mandatory flag, position) as attributes, import physical tables and columns, and link logical to physical. Quality, matching, and survivorship rules are deferred and clearly marked out of scope.

**Why.** A clear logical-to-physical hierarchy gives stewards immediate value; deferring rule synchronization avoids sprawl.

**Traps.** Multi-valued fields with child fields need a grouping relation; properties that fit no standard attribute type need custom types; descriptions edited in the catalog drift from the source.

## Scenario 6: Pushing Governance Metadata into a BI Tool

**Context.** Stewards certify data sources and add tags in the catalog. Analysts want to see certification, warnings, and contacts inside the BI tool.

**Design.** A workflow-triggered push: when a tracked attribute or tag changes, a workflow creates a task; the integration polls tasks, looks up the BI tool's identifier for the entity, and calls the BI tool's REST API. A contact rule: the steward overrides the owner.

**Why.** Stewards act in one place and changes propagate under governance; the workflow supplies an audit trail and a natural throttle.

**Traps.** The lookup of external IDs depends on lineage stitching between the catalog and the BI model, and unstitched assets cannot be updated; usernames must exist in the BI tool; tag removal must be handled, not only addition.

## Scenario 7: Merging Three HR Systems into One Identity Source

**Context.** After acquisitions, a company has three HR systems with overlapping employees and different ID schemes. Roles and access depend on a single trusted identity list.

**Design.** An authority matrix per attribute (legal name from system A, department from system B, and so on); a canonical employee ID in a crosswalk table; nightly full extracts from each system, matched through the crosswalk and published to the identity provider (SCIM) and to downstream tools.

**Why.** Clean authority splits remove conflict resolution, and the crosswalk is the durable asset.

**Traps.** Rehires with new IDs; name collisions; leavers who must be deprovisioned quickly (feed events, or a daily full comparison); privacy of HR attributes.

## Scenario 8: Lineage Across a Kafka-Based Data Platform

**Context.** Operational applications stream through Kafka into a cloud warehouse and BI. Auditors need column-level lineage from source application fields to dashboards.

**Design.** Crawl topics and schema subjects as static assets; run an extractor that joins Kafka Connect configurations with registry schemas and emits OpenLineage events with column lineage; take warehouse and BI lineage from their standard connectors, and stitch the three.

**Traps.** Single message transforms that rename fields; topics produced by custom code have no configuration to parse, so those producers should emit lineage themselves; stream processors need their own lineage capture.

## Scenario 9: An API Inventory from OpenAPI Specifications

**Context.** A company has hundreds of APIs and no catalog showing which endpoint returns which data structures.

**Design.** A pipeline that reads OpenAPI specifications from a repository, converts paths, response codes, component schemas, and properties into catalog assets (API, endpoint, code value, data structure, data element), and upserts them, with relations for composition and one that flags unused structures. Run it on every merge to the specification repository.

**Traps.** Specifications with inline anonymous schemas; polymorphism (`oneOf`, `anyOf`) mapping; a hierarchy view that must be configured once per domain; and, above all, specification quality, which is the real limit.

## Scenario 10: A Process Tool and a Catalog with a Clean Authority Split

**Context.** A process-modeling tool documents business processes, sub-processes (one to three levels), and activities. A catalog is the single source of truth for business objects. The business wants each activity to show which data concepts it uses, and each concept to show which activities touch it.

**Design.** *Authority split:* the process tool owns process structure and documentation; the catalog owns business objects; no co-owned fields, so no conflict resolution and no chronological merge. *Model:* one asset type for all process levels, with a level attribute and a decomposition relation, which is simpler than a type per level. *Identity:* the process tool has an entity ID (the stable identity of the object) and occurrence IDs (each appearance in a diagram); always key on the entity ID. Explain it to non-technical stakeholders as a passport versus a photograph: one identity, many pictures. *Direction:* catalog to process tool for business objects, process tool to catalog for structure and usage links.

**Traps.** Keying on occurrence IDs creates duplicates per diagram; deep hierarchies make traversals expensive (consider a derived relation that skips hops); some relation types may already exist, so check before creating.



# Appendix D. Templates

These templates are starting points. Copy them into a project repository, adapt the fields to your organization, and keep them with the code they describe. Others appear in the chapters: the architecture decision record (Chapter 2), the integration brief (Chapter 4), the API reconnaissance sheet (Chapter 10), the mapping specification (Chapter 12), the integration inventory record (Chapter 29), and the runbook outline (Chapter 26).

## Integration Brief (One Page)

```text
Title:            <Source> to <Target>: <entities>
Business owner:   <name>        Technical owner: <name>   Support: <team>
Purpose:          <one sentence outcome>
In scope:         <entities and fields>
Out of scope:     <explicit>
Authority:        <link to the field-level matrix>
Direction:        one-way / two-way (conflict rule: <rule>)
Freshness:        <minutes>   Volume: <today / three years / peak per hour>
Pattern:          <chosen>   Alternatives rejected because: <reasons>
Interfaces:       <source> (<spec link>)   <target> (<spec link>)
Authentication:   <scheme / account / rotation>
Runs on:          <host or platform>   Network path: <diagram link>
Failure handling: retry / quarantine / dead letters / reconciliation
Observability:    logs / metrics / alerts / dashboard
Risks:            <top five, each with an owner and a date>
Acceptance:       <test cases and numbers>
```

## Design Document Outline

1. Context, goals, and non-goals
2. Architecture diagram and data flow, including failure paths
3. Source and target reconnaissance sheets
4. Authority matrix and field mapping (configuration-driven)
5. Identity and matching strategy
6. Extraction strategy: full, incremental, delete handling
7. Load strategy: upsert, ordering, batching, rate budget
8. Error handling and recovery: retry, quarantine, dead letters, reconciliation
9. Security: accounts, secrets, network, data classification
10. Observability and alerting
11. Deployment, configuration, and environments
12. Test strategy and acceptance criteria
13. Operations: runbook, ownership, handover
14. Risks, assumptions, and open questions

## Test Plan Skeleton

**Table: A test plan skeleton**
| Test | What you check |
|---|---|
| Happy path | Create, update, and delete flow end to end with field-level assertions |
| Idempotency | Run twice; the second run changes nothing |
| Rename and re-key | Rename in the source; no duplicate in the target |
| Late and out-of-order change | An older change arrives after a newer one; the end state is correct |
| Failure injection | Kill the process mid-run; restart; no loss and no duplicates |
| Rate limit | Simulate 429 responses; backoff observed; no failure |
| Authentication expiry | Expire the token mid-run; a single re-authentication succeeds |
| Bad data | Null, oversize, emoji, wrong encoding: quarantined, and the run continues |
| Volume | A production-sized dataset: duration, memory, API budget |
| Reconciliation | Introduce drift; the reconciliation detects and repairs it |
| Concurrency | Two workers, one record: no double processing |

## Go-Live Checklist

* Service accounts created with least privilege; secrets in the vault; rotation documented
* The network path tested from the production host
* Target-system configuration (types, relations, attributes, layouts) installed and verified
* The initial load completed and reconciled
* Alerts routed to a real on-call person; heartbeat verified
* The runbook reviewed with the support team; the kill switch tested
* The rollback plan written and rehearsed: how to undo the load
* Stakeholders informed about expected behavior and known limitations

## Threat Model (One Page)

```text
Integration: <name>   Version: <n>   Date: <date>   Reviewed by: <contact>
Data-flow diagram: <link> (trust boundaries marked)
Data classification: <fields and classes>
#  | Element/flow     | STRIDE | Threat          | Likelihood | Impact
1  | Webhook receiver | S      | Forged webhook  | Medium     | High
   | Control: HMAC + timestamp window | Owner: Team A | Status: done
Residual risks accepted by: <name, date>
```

## Operational Readiness Review (Before Go-Live)

* An owner is named and trained; the runbook has been executed by someone other than its author
* Alerts have been tested end to end, and they reach a person; the dashboard answers the five questions
* Objectives are agreed; the reconciliation is scheduled and a drift alert is active
* Secrets are in the vault with rotation dates; certificates are inventoried
* The recovery tier is agreed and recovery has been rehearsed at least once
* The rollback and forward-fix plans are written; the kill switch is tested
* The inventory record exists; the data contract or mapping specification is published

## Post-Incident Review

```text
Summary:    what happened; the impact (records, users, duration); how and
            when it was detected
Timeline:   UTC timestamps from the first signal to recovery
Root cause: the technical cause AND why it was possible (a missing test,
            alert, or review)
What went well / what did not
Actions:    | action | owner | due | type (prevent / detect / recover) |
Follow-up:  tests added, runbook updated, standards changed
```

## Test Strategy (One Page)

```text
Scope and risks to cover
Levels: unit, contract, integration, non-functional, end to end, production checks
Environments and test data
Failure-injection matrix and results
Acceptance numbers and the evidence for each
Tools; who runs what, and when
Exit criteria for each gate
```

## Authority Matrix

**Table: An authority matrix template**
| Entity and field | Authoritative system | Other systems | Direction | Conflict rule needed? | Notes |
|---|---|---|---|---|---|
| | | | | | |



# Appendix E. Companion Code

The companion code is a small set of Python modules that the chapters use and discuss, each exercised by automated tests. It needs Python 3.9 or later. The lab server uses only the standard library; the client and tests need two packages and the mapping module a third:

```bash
pip install requests pytest pydantic
python3 -m pytest -q test_all.py test_more.py
```

The code is copyright 2026 Stefan Živanović and is licensed under the MIT License, which is included in the archive. Like the rest of this book, it was generated with AI assistance (Claude, by Anthropic) under the author's direction, and each file in the archive says so in its header. It is provided as is, without warranty.

All tests run in a few seconds and need no external services. They include crash tests (a poller killed mid-batch), failure injection (a server that is rate-limited or randomly unavailable), and idempotency tests (a duplicate request, a duplicate event). The listings in the Kafka, OpenTelemetry, and platform chapters are sketches that need external services, and are not part of this set.

**Table: The companion modules and where the book discusses them**
| Module | Purpose | Chapter |
|---|---|---|
| `labserver.py` | A local order API with pagination, rate limiting, random failures, OAuth tokens, and idempotency keys | 1, 10, and throughout |
| `client.py` | A hardened HTTP client with retries, backoff, jitter, and cursor pagination | 14 |
| `tokens.py` | An OAuth 2.0 client-credentials token provider | 13 |
| `poller.py` | A watermark poller with an overlap window and atomic checkpoints | 14 |
| `ratelimit.py` | A token-bucket rate limiter | 14 |
| `runloop.py` | A run loop that quarantines bad data and reports a summary | 14 |
| `webhook.py` | Webhook signature verification and an event-ID ledger | 13 |
| `outbox.py` | A transactional outbox with an at-least-once relay | 7, 8 |
| `reconcile.py` | A reconciliation comparison and a deletion guard | 15 |
| `openapi_recon.py` | An OpenAPI analyzer that lists hints and gaps | 10 |
| `mapping.py` | Typed validation and mapping of an order | 12 |

The modules discussed in full in a chapter are not repeated here. The lab server, the outbox, and the tests follow.

## The Lab Server

```python
#!/usr/bin/env python3
"""A small order API for the exercises in this book (standard library only).

Run it:   python3 labserver.py --port 8080
Options:  --rate-limit N   allow N requests per second, then answer 429
          --flaky P        answer 503 for a fraction P of requests
          --token-ttl S    lifetime of OAuth tokens in seconds
          --no-auth        skip bearer-token checks
"""
import argparse, base64, json, random, threading, time, uuid
from datetime import datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

LOCK = threading.Lock()
ORDERS = {}          # id -> order dict
IDEMPOTENT = {}      # Idempotency-Key -> (status, body)
TOKENS = {}          # access token -> expiry (epoch seconds)
WINDOW = []          # request timestamps for the rate limiter
CFG = {"rate_limit": 0, "flaky": 0.0, "token_ttl": 3600, "auth": True}
CLIENT = ("larkspur-client", "s3cret")
BASE = datetime(2026, 11, 1, tzinfo=timezone.utc)

def iso(dt):
    return dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

def seed(n):
    for i in range(n):
        oid = "A%04d" % (1000 + i)
        ORDERS[oid] = {"id": oid, "sku": "TENT-%d" % (i % 7), "qty": 1 + i % 3,
                       "status": "CREATED",
                       "updatedAt": iso(BASE + timedelta(seconds=i * 30))}

def page(since, limit, cursor):
    rows = sorted(ORDERS.values(), key=lambda o: (o["updatedAt"], o["id"]))
    if cursor:
        ts, oid = base64.urlsafe_b64decode(cursor).decode().split("|")
        rows = [o for o in rows if (o["updatedAt"], o["id"]) > (ts, oid)]
    elif since:
        rows = [o for o in rows if o["updatedAt"] > since]
    chunk = rows[:limit]
    nxt = None
    if len(rows) > limit:
        last = chunk[-1]
        raw = ("%s|%s" % (last["updatedAt"], last["id"])).encode()
        nxt = base64.urlsafe_b64encode(raw).decode()
    return {"results": chunk, "nextCursor": nxt}

class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, *args):
        pass

    def send(self, status, body=None, headers=None):
        data = json.dumps(body).encode() if body is not None else b""
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        for k, v in (headers or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(data)

    def chaos(self):
        """Rate limit and random failures; True if the request was answered."""
        now = time.time()
        with LOCK:
            WINDOW[:] = [t for t in WINDOW if now - t < 1.0]
            WINDOW.append(now)
            limited = CFG["rate_limit"] and len(WINDOW) > CFG["rate_limit"]
        if limited:
            self.send(429, {"error": "rate_limited"}, {"Retry-After": "1"})
            return True
        if CFG["flaky"] and random.random() < CFG["flaky"]:
            self.send(503, {"error": "unavailable"})
            return True
        return False

    def authorized(self):
        if not CFG["auth"]:
            return True
        token = self.headers.get("Authorization", "")[7:]
        if TOKENS.get(token, 0) > time.time():
            return True
        self.send(401, {"error": "invalid_token"}, {"WWW-Authenticate": "Bearer"})
        return False

    def body(self):
        n = int(self.headers.get("Content-Length") or 0)
        return self.rfile.read(n) if n else b""

    def do_POST(self):
        path = urlparse(self.path).path
        if path == "/oauth/token":
            form = parse_qs(self.body().decode())
            got = (form.get("client_id", [""])[0],
                   form.get("client_secret", [""])[0])
            if form.get("grant_type") != ["client_credentials"] or got != CLIENT:
                return self.send(401, {"error": "invalid_client"})
            token = uuid.uuid4().hex
            TOKENS[token] = time.time() + CFG["token_ttl"]
            return self.send(200, {"access_token": token, "token_type": "Bearer",
                                   "expires_in": CFG["token_ttl"]})
        if self.chaos() or not self.authorized():
            return
        if path == "/orders":
            key = self.headers.get("Idempotency-Key")
            if not key:
                return self.send(400, {"error": "Idempotency-Key required"})
            with LOCK:
                if key in IDEMPOTENT:
                    status, body = IDEMPOTENT[key]
                    return self.send(status, body, {"Idempotent-Replay": "true"})
                data = json.loads(self.body() or b"{}")
                oid = "A%04d" % (1000 + len(ORDERS))
                now = iso(datetime.now(timezone.utc))
                order = {"id": oid, "sku": data.get("sku", "?"),
                         "qty": data.get("qty", 1), "status": "CREATED",
                         "updatedAt": now}
                ORDERS[oid] = order
                IDEMPOTENT[key] = (201, order)
            return self.send(201, order, {"Location": "/orders/" + oid})
        if path.startswith("/admin/touch/"):
            oid = path.rsplit("/", 1)[1]
            with LOCK:
                if oid in ORDERS:
                    ORDERS[oid]["updatedAt"] = iso(datetime.now(timezone.utc))
                    return self.send(200, ORDERS[oid])
            return self.send(404, {"error": "not_found"})
        self.send(404, {"error": "not_found"})

    def do_GET(self):
        url = urlparse(self.path)
        if url.path == "/health":
            return self.send(200, {"status": "ok"})
        if self.chaos() or not self.authorized():
            return
        q = parse_qs(url.query)
        if url.path == "/orders":
            limit = min(int(q.get("limit", ["50"])[0]), 500)
            with LOCK:
                out = page(q.get("updatedSince", [""])[0], limit,
                           q.get("cursor", [""])[0])
            return self.send(200, out)
        if url.path.startswith("/orders/"):
            order = ORDERS.get(url.path.rsplit("/", 1)[1])
            if order:
                return self.send(200, order)
            return self.send(404, {"error": "not_found"})
        self.send(404, {"error": "not_found"})

def make_server(port=8080, **cfg):
    CFG.update(cfg)
    return ThreadingHTTPServer(("127.0.0.1", port), Handler)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8080)
    ap.add_argument("--rate-limit", type=int, default=0)
    ap.add_argument("--flaky", type=float, default=0.0)
    ap.add_argument("--token-ttl", type=int, default=3600)
    ap.add_argument("--no-auth", action="store_true")
    a = ap.parse_args()
    seed(250)
    srv = make_server(a.port, rate_limit=a.rate_limit, flaky=a.flaky,
                      token_ttl=a.token_ttl, auth=not a.no_auth)
    print("lab server on http://127.0.0.1:%d" % a.port)
    print("client id / secret: %s / %s" % CLIENT)
    srv.serve_forever()
```
## The Transactional Outbox

```python
"""Transactional outbox: write the business change and the event together."""
import json, sqlite3

SCHEMA = """
CREATE TABLE IF NOT EXISTS orders (id TEXT PRIMARY KEY, status TEXT);
CREATE TABLE IF NOT EXISTS outbox (
  seq INTEGER PRIMARY KEY AUTOINCREMENT, event_id TEXT UNIQUE,
  payload TEXT, sent INTEGER DEFAULT 0);
"""

def connect(path=":memory:"):
    db = sqlite3.connect(path)
    db.executescript(SCHEMA)
    return db

def place_order(db, order_id, status="CREATED"):
    with db:                          # one transaction: both rows or neither
        db.execute("INSERT OR REPLACE INTO orders VALUES (?, ?)",
                   (order_id, status))
        event = {"event_id": "%s:%s" % (order_id, status), "order_id": order_id,
                 "status": status}
        db.execute("INSERT OR IGNORE INTO outbox (event_id, payload) "
                   "VALUES (?, ?)", (event["event_id"], json.dumps(event)))

def relay(db, publish, batch=100):
    """Publish unsent events in order, then mark them sent. A crash between the
    two steps causes a re-publish: delivery is at-least-once, so consumers
    must dedupe."""
    rows = db.execute("SELECT seq, payload FROM outbox WHERE sent = 0 "
                      "ORDER BY seq LIMIT ?", (batch,)).fetchall()
    for seq, payload in rows:
        publish(json.loads(payload))
        with db:
            db.execute("UPDATE outbox SET sent = 1 WHERE seq = ?", (seq,))
    return len(rows)
```
## Tests, Part One

```python
import json, os, threading, time
import pytest, requests
import labserver, client, tokens, poller, webhook, outbox


@pytest.fixture(scope="module")
def server():
    labserver.ORDERS.clear()
    labserver.seed(250)
    srv = labserver.make_server(
        0, rate_limit=0, flaky=0.0, token_ttl=3600, auth=False
    )
    t = threading.Thread(target=srv.serve_forever, daemon=True)
    t.start()
    yield "http://127.0.0.1:%d" % srv.server_address[1]
    srv.shutdown()


def no_sleep(_):
    pass


def test_pagination_returns_every_record_once(server):
    s = client.build_session()
    ids = [
        r["id"] for r in client.iter_records(s, server + "/orders", limit=40)
    ]
    assert len(ids) == 250 and len(set(ids)) == 250


def test_retry_after_is_honored(server):
    labserver.CFG.update(rate_limit=3)
    waits = []
    s = client.build_session()
    try:
        for _ in range(8):
            client.request(
                s,
                "GET",
                server + "/orders",
                params={"limit": 1},
                sleep=lambda w: (waits.append(w), time.sleep(w)),
            )
    finally:
        labserver.CFG.update(rate_limit=0)
    assert waits and all(w == 1.0 for w in waits)  # the server said 1 second


def test_flaky_server_eventually_succeeds(server):
    labserver.CFG.update(flaky=0.5)
    s = client.build_session()
    try:
        r = client.request(
            s, "GET", server + "/orders/A1000", max_attempts=12, sleep=no_sleep
        )
    finally:
        labserver.CFG.update(flaky=0.0)
    assert r.json()["id"] == "A1000"


def test_post_without_idempotency_key_is_not_retried(server):
    labserver.CFG.update(flaky=1.0)
    s = client.build_session()
    calls = []
    real = s.request
    s.request = lambda *a, **k: (calls.append(1), real(*a, **k))[1]
    try:
        with pytest.raises(client.ApiError):
            client.request(
                s, "POST", server + "/orders", json={"sku": "X"}, sleep=no_sleep
            )
    finally:
        labserver.CFG.update(flaky=0.0)
    assert len(calls) == 1


def test_idempotent_post_replays(server):
    s = client.build_session()
    h = {"Idempotency-Key": "k-123"}
    a = client.request(
        s, "POST", server + "/orders", json={"sku": "T", "qty": 2}, headers=h
    )
    b = client.request(
        s, "POST", server + "/orders", json={"sku": "T", "qty": 2}, headers=h
    )
    assert a.status_code == 201 and a.json()["id"] == b.json()["id"]
    assert b.headers["Idempotent-Replay"] == "true"


def test_backoff_bounds():
    for attempt in range(10):
        d = client.backoff_delay(attempt, base=0.5, cap=30)
        assert 0 <= d <= min(30, 0.5 * 2**attempt)


def test_parse_retry_after():
    assert client.parse_retry_after("3") == 3.0
    assert client.parse_retry_after(None) is None
    assert client.parse_retry_after("garbage") is None


def test_token_refresh_and_401_recovery():
    labserver.ORDERS.clear()
    labserver.seed(10)
    srv = labserver.make_server(
        0, rate_limit=0, flaky=0.0, token_ttl=3600, auth=True
    )
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = "http://127.0.0.1:%d" % srv.server_address[1]
    try:
        tp = tokens.TokenProvider(base + "/oauth/token", *labserver.CLIENT)
        s = client.build_session(tp)
        assert client.request(s, "GET", base + "/orders").status_code == 200
        assert tp.fetches == 1
        labserver.TOKENS.clear()  # server forgets the token: surprise 401
        assert client.request(s, "GET", base + "/orders").status_code == 200
        assert tp.fetches == 2  # exactly one refresh
        bad = tokens.TokenProvider(base + "/oauth/token", "x", "y")
        with pytest.raises(requests.HTTPError):
            bad.get()
    finally:
        srv.shutdown()
        labserver.CFG.update(auth=False)


def test_watermark_poller_resumes_without_loss(server, tmp_path):
    labserver.ORDERS.clear()
    labserver.seed(100)
    state = str(tmp_path / "wm.json")
    got = {}

    def upsert(rec):
        got[rec["id"]] = rec

    s = client.build_session()
    assert poller.run_once(s, server, state, upsert) == 100
    # a record changes during the next window; one older record sits
    # inside the overlap
    requests.post(server + "/admin/touch/A1005")
    n = poller.run_once(s, server, state, upsert)
    assert (
        got["A1005"]["updatedAt"] > "2026-11-01T01:00"
    )  # the change was captured
    assert 1 <= n <= 6  # overlap re-reads only a few
    # crash safety: failing mid-batch must not move the watermark
    before = poller.load_watermark(state)
    requests.post(server + "/admin/touch/A1010")

    def boom(rec):
        raise RuntimeError("crash")

    with pytest.raises(RuntimeError):
        poller.run_once(s, server, state, boom)
    assert poller.load_watermark(state) == before
    poller.run_once(s, server, state, upsert)
    assert got["A1010"]["updatedAt"] > before


def test_webhook_signature_and_replay_window():
    body = b'{"event_id":"e1"}'
    ts = str(int(time.time()))
    sig = webhook.sign("topsecret", ts, body)
    assert webhook.verify("topsecret", body, sig, ts)
    assert not webhook.verify("wrong", body, sig, ts)
    assert not webhook.verify("topsecret", body + b" ", sig, ts)
    old = str(int(time.time()) - 3600)
    assert not webhook.verify(
        "topsecret", body, webhook.sign("topsecret", old, body), old
    )
    assert not webhook.verify("topsecret", body, None, ts)
    assert not webhook.verify("topsecret", body, sig, "not-a-number")


def test_ledger_drops_duplicates():
    led = webhook.Ledger()
    assert (
        led.first_time("e1")
        and not led.first_time("e1")
        and led.first_time("e2")
    )


def test_outbox_is_at_least_once_and_dedupe_fixes_it():
    db = outbox.connect()
    outbox.place_order(db, "A1", "CREATED")
    outbox.place_order(db, "A2", "CREATED")
    sent = []

    # crash after publishing the first event but before marking it sent
    def flaky_publish(ev):
        sent.append(ev["event_id"])
        if len(sent) == 1:
            raise RuntimeError("crash after publish")

    with pytest.raises(RuntimeError):
        outbox.relay(db, flaky_publish)
    outbox.relay(
        db, sent.append if False else (lambda ev: sent.append(ev["event_id"]))
    )
    assert sent.count("A1:CREATED") == 2  # duplicate publish: at-least-once
    led = webhook.Ledger()
    processed = [e for e in sent if led.first_time(e)]
    assert sorted(processed) == ["A1:CREATED", "A2:CREATED"]
    assert (
        db.execute("SELECT COUNT(*) FROM outbox WHERE sent=0").fetchone()[0]
        == 0
    )
```
## Tests, Part Two

```python
import json, subprocess, sys, pytest
import mapping, openapi_recon
from pydantic import ValidationError

SPEC = {
    "openapi": "3.1.0",
    "info": {"title": "Orders", "version": "2.4"},
    "servers": [{"url": "https://api.example.com/v2"}],
    "components": {
        "securitySchemes": {
            "oauth": {"type": "oauth2", "flows": {"clientCredentials": {}}}
        }
    },
    "paths": {
        "/orders": {
            "get": {
                "parameters": [
                    {"name": "updatedSince", "in": "query"},
                    {"name": "cursor", "in": "query"},
                ],
                "responses": {"200": {}, "429": {}},
            },
            "post": {"responses": {"201": {}}},
        },
        "/orders/{id}": {"get": {"responses": {"200": {}}}},
        "/orders/bulk": {
            "post": {
                "parameters": [{"name": "Idempotency-Key", "in": "header"}],
                "responses": {"202": {}},
            }
        },
    },
}


def test_recon_finds_hints_and_gaps():
    info = openapi_recon.analyze(SPEC)
    assert info["security"] == {"oauth": "oauth2 (clientCredentials)"}
    assert any("incremental" in h for h in info["hints"])
    assert any("asynchronous" in h for h in info["hints"])
    assert any("bulk candidate" in h for h in info["hints"])
    assert any("POST /orders has no Idempotency-Key" in g for g in info["gaps"])
    assert any("GET /orders/{id} documents no 429" in g for g in info["gaps"])
    assert not any("GET /orders is a list" in g for g in info["gaps"])


def test_recon_cli(tmp_path):
    p = tmp_path / "spec.json"
    p.write_text(json.dumps(SPEC))
    out = subprocess.run(
        [sys.executable, "openapi_recon.py", str(p)],
        capture_output=True,
        text=True,
    )
    assert out.returncode == 0 and "Gaps to ask about" in out.stdout


def test_mapping_happy_path_and_traps():
    o = mapping.OrderIn(
        id="00042",
        total="19.90",
        currency="EUR",
        status="3",
        created_at="2026-11-23T10:00:00+01:00",
    )
    t = mapping.to_target(o)
    assert (
        t["externalId"] == "00042"
        and t["amount"] == "19.90"
        and t["createdAt"].startswith("2026-11-23T09:00:00")
    )
    with pytest.raises(ValidationError):
        mapping.OrderIn(
            id="1",
            total="1",
            currency="EUR",
            status="1",
            created_at="2026-11-23T10:00:00",
        )  # no zone
    with pytest.raises(ValidationError):
        mapping.OrderIn(
            id="1",
            total="-1",
            currency="EUR",
            status="1",
            created_at="2026-11-23T10:00:00Z",
        )
    with pytest.raises(ValueError):
        mapping.to_target(
            mapping.OrderIn(
                id="1",
                total="1",
                currency="EUR",
                status="7",
                created_at="2026-11-23T10:00:00Z",
            )
        )


import ratelimit, runloop


def test_token_bucket_paces_calls():
    t = [0.0]
    slept = []

    def sleep(s):
        slept.append(s)
        t[0] += s

    b = ratelimit.TokenBucket(rate=2, burst=2, clock=lambda: t[0], sleep=sleep)
    for _ in range(6):
        b.acquire()
    assert (
        not slept[:0] and abs(sum(slept) - 2.0) < 1e-9
    )  # 2 burst free, then 4 at 2/s


def test_run_loop_quarantines_bad_data_but_stops_on_bugs(tmp_path):
    q = str(tmp_path / "q.jsonl")

    def upsert(rec):
        if rec["id"] == "bad":
            raise ValueError("unmapped status 7")
        if rec["id"] == "boom":
            raise RuntimeError("target down")

    counts = runloop.process(
        [{"id": "a"}, {"id": "bad"}, {"id": "b"}], upsert, q
    )
    assert (counts["read"], counts["written"], counts["quarantined"]) == (
        3,
        2,
        1,
    )
    line = json.loads(open(q).readline())
    assert (
        line["reason"] == "unmapped status 7" and line["record"]["id"] == "bad"
    )
    with pytest.raises(RuntimeError):
        runloop.process([{"id": "a"}, {"id": "boom"}], upsert, q)


import reconcile


def test_reconcile_report_and_deletion_guard():
    src = {"a": "1", "b": "2", "c": "3"}
    tgt = {"a": "1", "b": "X", "z": "9"}
    r = reconcile.compare(src, tgt)
    assert r["missing_in_target"] == ["c"] and r["orphans_in_target"] == ["z"]
    assert r["changed"] == ["b"]
    with pytest.raises(RuntimeError):
        reconcile.deletion_guard(r, max_fraction=0.05)  # 1 of 3 is too many
    assert reconcile.deletion_guard(r, max_fraction=0.5) == ["z"]
```


# Appendix F. Glossary

Terms are defined as this book uses them. The index lists the pages where each is discussed.

**ADR**
:   Architecture decision record: context, options, decision and consequences.

**Anti-corruption layer**
:   An adapter that translates between a legacy or external model and a clean internal one, so the foreign model does not spread.

**API-led connectivity**
:   Layering APIs into system, process and experience tiers (popularized by MuleSoft).

**Authority (system of record)**
:   The system whose value wins for a given field.

**Authority matrix**
:   A table stating which system owns each field.

**Backoff with jitter**
:   Waiting longer after each failed attempt, with a random component, so that clients do not retry in synchronized waves.

**Backpressure**
:   Slowing a producer when a consumer cannot keep up.

**Bulkhead**
:   A limited, separate pool of resources per dependency, so a slow dependency cannot exhaust everything.

**Canonical model**
:   A shared definition of an entity that every system maps to and from, instead of mapping to each other directly.

**CDC**
:   Change data capture: reading a database's change log to publish row changes.

**Circuit breaker**
:   A guard that stops calling a failing dependency for a cool-down period.

**Claim check**
:   Storing a large payload elsewhere and passing a reference in the message.

**CloudEvents**
:   A specification for describing event metadata in a common way.

**Compaction**
:   Kafka retention policy that keeps the latest record per key.

**Consumer group**
:   A set of Kafka consumers that share the partitions of a topic, so that each record is processed by one member of the group.

**Consumer lag**
:   How far a consumer group is behind the end of a partition.

**Contract test**
:   A test that checks a client and an API (or a producer and a consumer) still agree on the interface.

**Control plane / runtime plane**
:   The management layer of a platform versus the engine where flows actually execute and data moves.

**Crosswalk**
:   A table mapping identifiers in one system to identifiers in another.

**Data contract**
:   A machine-readable agreement between data producer and consumers covering schema, quality, service levels and ownership.

**Data virtualization**
:   Querying across sources at read time without copying data.

**DLQ**
:   Dead letter queue: where unprocessable messages are parked with context.

**EDI / AS2 / VAN**
:   Standard business documents (X12, EDIFACT); a secure transport; and a value-added network that relays them.

**ESB**
:   Enterprise service bus: a central integration runtime that routes and transforms messages.

**Event mesh**
:   Interconnected event brokers that route events across sites and clouds.

**Four numbers**
:   Records now, records in three years, peak changes per hour, and acceptable staleness.

**Gate**
:   A decision point at the end of a project stage, passed only when stated criteria are met on named evidence.

**Golden file**
:   A stored pair of input and expected output used to test a mapping.

**HL7 / FHIR / MLLP**
:   Healthcare message standard; its REST-based resource model; and the TCP framing used for HL7 v2.

**Hypercare**
:   A defined period after go-live in which the build team stays on call while the operations team takes over.

**Idempotency key**
:   A unique value a client sends with a request so that the server can recognize a retry and return the original result instead of repeating the work.

**Idempotent**
:   An operation that has the same effect whether performed once or many times.

**iPaaS**
:   Integration platform as a service.

**ISR**
:   In-sync replicas of a partition.

**KRaft**
:   Kafka's built-in metadata consensus, replacing ZooKeeper.

**Lookup before retry**
:   Checking whether a create succeeded before retrying it, to make a non-idempotent API safe.

**MCP**
:   Model Context Protocol: a standard for exposing tools to AI agents.

**MFT**
:   Managed file transfer: secure, audited file exchange (SFTP, AS2, FTPS).

**MQTT**
:   Lightweight publish-subscribe protocol for devices.

**mTLS**
:   Mutual TLS: both client and server present certificates when the connection is established.

**OAuth 2.0 client credentials**
:   The OAuth 2.0 flow in which an application exchanges its own identity and secret for a short-lived access token; the standard choice for unattended integrations.

**Offset**
:   The position of a record within a Kafka partition; consumers commit offsets to record how far they have read.

**OpenLineage**
:   An open standard for emitting lineage events from data jobs.

**Outbox pattern**
:   Writing an event to a table in the same transaction as the state change, then publishing it reliably.

**Overlap window**
:   A safety margin by which an incremental read reaches back before the watermark, to catch late-committed rows.

**Parallel run**
:   Running old and new paths side by side and comparing outputs before switching.

**Partition**
:   An ordered, append-only log that forms part of a Kafka topic; order is guaranteed only within a partition.

**Paved road**
:   The supported, easiest way to build an integration using platform-provided templates and guardrails.

**PKCE**
:   Proof Key for Code Exchange: a protection for the OAuth 2.0 authorization code flow used by applications that act for a person.

**Problem details**
:   RFC 9457 JSON error format (application/problem+json).

**Quarantine**
:   A holding area for records that failed validation, kept with the reason and the original payload.

**Reconciliation**
:   Comparing two systems to detect and repair drift.

**Reconnaissance sheet**
:   A one-page record of an API's contract, authentication, limits, pagination, errors, and events, filled in by probing.

**Reverse ETL**
:   Pushing curated warehouse data back into operational applications.

**RPO / RTO**
:   Recovery point objective (acceptable data loss) and recovery time objective (acceptable downtime).

**Saga**
:   A business transaction split into local transactions with compensating actions.

**Schema registry**
:   A service that stores the schemas of event payloads and refuses incompatible changes.

**Shadow run**
:   Running a new path on copies of real traffic and comparing results without affecting production.

**Share group**
:   Kafka 4.x consumption model with queue-like semantics and per-record acknowledgment.

**SLI / SLO / error budget**
:   A measured indicator, its target, and the tolerated shortfall that triggers reliability work.

**SMT**
:   Single message transform in Kafka Connect.

**Strangler fig**
:   Replacing a legacy system gradually by routing more and more functionality to new services until the old system can be retired.

**STRIDE**
:   Threat categories: spoofing, tampering, repudiation, information disclosure, denial of service, elevation of privilege.

**Token bucket**
:   A rate limiter that refills tokens at a fixed rate; each request takes a token, so traffic stays within a budget.

**traceparent**
:   W3C Trace Context header carrying trace and span identifiers across services and messages.

**Upsert**
:   Insert if absent, update if present, keyed by an identifier.

**Watermark**
:   The position (timestamp or token) up to which a source has been read.

**Webhook**
:   An HTTP request that a source system sends to your endpoint when something changes.




# Appendix G. Further Reading, Standards, and Sources

## Books

**Table: Books that deepen the topics of this one**
| Book | Authors | Why read it |
|---|---|---|
| *Enterprise Integration Patterns* | Gregor Hohpe and Bobby Woolf | The vocabulary of messaging patterns still used by every platform |
| *Designing Data-Intensive Applications* | Martin Kleppmann | Replication, consistency, logs, and streams explained properly |
| *Kafka: The Definitive Guide* | Gwen Shapira and co-authors | Kafka internals and operations |
| *Building Event-Driven Microservices* | Adam Bellemare | Event design and stream-based architecture |
| *Release It!* | Michael Nygard | Stability patterns: timeouts, circuit breakers, bulkheads |
| *Fundamentals of Software Architecture* | Mark Richards and Neal Ford | Architecture characteristics and trade-off thinking |
| *API Design Patterns* | JJ Geewax | Designing APIs others can integrate with |
| *Site Reliability Engineering* | Google (edited by Betsy Beyer and others) | Objectives, error budgets, incident practice |
| *Team Topologies* | Matthew Skelton and Manuel Pais | Platform teams and operating models |

## Standards and Specifications Referenced

**Table: Standards and specifications mentioned in this book**
| Standard | What it defines | Where it appears |
|---|---|---|
| IETF RFC 9110 | HTTP semantics: methods, status codes, headers | Chapter 1 |
| IETF RFC 9457 | Problem Details for HTTP APIs (`application/problem+json`) | Chapter 11 |
| IETF RFC 8594 | The `Sunset` HTTP header field | Chapter 11 |
| IETF Internet-Draft, Idempotency-Key | A proposed standard header for safe retries of `POST` (still a draft in the sources checked) | Chapters 1, 11 |
| IETF RFC 6749 | The OAuth 2.0 authorization framework | Chapter 13 |
| IETF RFC 7636 | Proof Key for Code Exchange (PKCE) | Chapter 13 |
| IETF RFC 7523 | JWT bearer assertion profile for OAuth 2.0 | Chapter 13 |
| W3C Trace Context | The `traceparent` and `tracestate` headers | Chapter 26 |
| CloudEvents 1.0 (CNCF) | A common envelope for event data | Chapters 11, 19 |
| OpenAPI Specification 3.1 and 3.2 | Description of HTTP APIs (3.2.0 appeared in September 2025; 3.1 descriptions remain valid) | Chapters 10, 11 |
| AsyncAPI 3.x | Description of event-driven APIs | Chapter 11 |
| OpenLineage | An open specification for run, job, and dataset lineage events | Chapters 19, 29 |
| Open Data Contract Standard (Bitol) | A YAML format for data contracts | Chapter 29 |
| OWASP API Security Top 10 (2023) | The most serious API risks (the most recent API list when checked; the web-application Top 10 was updated in 2025) | Chapter 27 |
| STRIDE | A mnemonic for six threat categories | Chapter 27 |

## Sources and Currency

The technical principles in this book are stable. Statements about products, versions, limits, and standards' current versions are time-sensitive. At the time of writing, in November 2026, the following were checked against public sources:

* **Apache Kafka.** The release announcements and upgrade notes for the 4.x line, covering the removal of ZooKeeper, the new consumer rebalance protocol, share groups, and Java requirements; and client documentation on idempotent producers.
* **OWASP.** The API Security Top 10 2023 edition was the most recent published list.
* **Open Data Contract Standard.** Version 3.2.0 (September 2026) was the latest published release; 3.1.0 appeared in December 2025.
* **MuleSoft and other platforms.** Vendor documentation on error handling, batch processing, runtime options, and the Kafka connector. Product names and licensing models change, so confirm current offerings.
* **Salesforce and NetSuite.** Vendor documentation on the Spring '26 connected-app restriction and external client apps, and on Oracle's timeline for removing SOAP web services.
* **OpenAPI and Kafka.** The OpenAPI 3.2.0 release (September 2025) and the Apache Kafka 4.2 announcement, which marks share groups production-ready.
* **Industry events.** IBM's 2024 acquisition of webMethods and StreamSets from Software AG.

Anything in these categories should be confirmed against current documentation before a client deliverable relies on it. The book's own heuristics, the decision-tree scores, the estimation constants, and the learning-path durations, are the author's judgment and are not drawn from any standard.



# About the Author

**Stefan Živanović** is a Solution Architect based in Prague, Czech Republic. He works on the implementation and configuration of data governance and integration solutions for enterprise clients, advises teams on architecture and best practice, and teaches workshops and training sessions.

He directed the writing of this book with the help of an AI assistant; the section "How This Book Was Made" explains how.



# Colophon

*Integration Architecture in Practice*, First Edition, November 2026.

The text, diagrams, index, cover, and code of this book were generated with AI assistance (Claude, by Anthropic) under the author's direction, and the pages were typeset with WeasyPrint from Markdown sources.

The body text is set in Source Serif 4; headings, tables, and captions in Source Sans 3; and code in Source Code Pro. All three families are licensed under the SIL Open Font License. The page size is 7 by 9.19 inches. The diagrams are vector graphics in a palette designed to remain legible in grayscale. The index was generated automatically from a list of terms.
