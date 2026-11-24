# Designing APIs, Webhooks, and Events

Every complaint you have ever had about a vendor's API is a design rule in disguise. The list endpoint with no way to ask "what changed since yesterday?" taught you that providers must offer change detection. The create call that made a duplicate when you retried it taught you about idempotency keys. The error message that said only "Bad Request" taught you that errors are part of the interface. The webhook feed that went silent for a weekend, with no way to ask what you missed, taught you about replay.

Chapter {{ref ch:readdocs}} taught you to read other people's interfaces. Architects also *design* interfaces that others will consume: an API placed in front of a legacy system, a webhook feed for partners, a stream of business events on a shared platform. The consumers of those interfaces are integrators like you, and the quality of your design determines whether their integrations are simple and safe or fragile and expensive. This chapter turns the lessons of every difficult integration you will ever build into rules for the provider's side of the fence.

!!! goals "In this chapter"
    * Describe the lifecycle of an API, from contract-first design to retirement
    * Apply the design rules that make an API easy to integrate: stable identifiers, change detection, cursor paging, idempotent writes, bulk paths, and consistent errors
    * Use RFC 9457 problem details for errors, and write an OpenAPI contract that encodes the rules
    * Build a reliable webhook feed: outbox, signatures, retries, delivery log, and replay
    * Design events with the same care as APIs, including schema, versioning, and ordering guarantees
    * Review a design against a checklist before consumers depend on it

## The API Lifecycle

An API is a product with a lifecycle, and the most common mistake is to design only its first phase. {{ref fig:apidesign-api-lifecycle}} shows the full arc.

{{fig apidesign-api-lifecycle | The lifecycle of an API. Contract first, published with documentation, evolved additively, and deprecated with notice. Retiring an API is a planned step, not an accident.}}

It begins with **design**, ideally *contract first*: write the OpenAPI or AsyncAPI specification before the implementation, because a contract is cheap to change and code is not (step 1). The contract goes through **mock and review** against a style guide, where consumers can try it before it exists (step 2). Then **build and test**, including contract tests that verify the implementation matches the specification (step 3). The API is **published** with documentation and registered in a catalog (step 4) and **operated** with service levels and usage analytics (step 5). It **evolves** through additive changes that do not break consumers (step 6). When a breaking change is unavoidable, the old version is **deprecated** with a notice period and a visible sunset date (step 7), and finally **retired**.

The two phases most often forgotten are the last two. An API without a deprecation policy accumulates versions forever, each with consumers nobody can identify, and the cost of maintaining them never stops growing. Decide, at design time, how you will retire what you are creating.

## Design Rules That Save Your Consumers

{{ref tbl:rules}} lists the rules that make an API pleasant to integrate. Each one corresponds to a problem integrators meet daily, so each includes why integrators care.

{{tbl rules | Design rules for integration-friendly APIs}}

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
| Security | OAuth 2.0 scopes per capability; object-level authorization on every call; no secrets in URLs | See the OWASP API risks in Chapter {{ref ch:security}} |

Six of these rules repay a closer look.

### Change Detection

An integrator who wants to keep a copy of your data current needs to ask, cheaply, "what changed since I last looked?" If your API cannot answer, integrators will read everything repeatedly, which is expensive for them and for you. The best provision is an `updatedSince` filter backed by a **server-set** timestamp (never one the client can write) that moves whenever *any* field of the record changes. Add a way to learn about deletions: soft-deleted records that remain visible with a status, a "deleted since" endpoint, or a tombstone event. An API with a modified-since filter but no way to see deletes forces every consumer to build a full-comparison job, so decide whether you can afford to provide it once for all of them.

### Pagination

Offer cursors, as {{ref fig:pagination-offset-drift}} explained, with a stable sort, a documented maximum page size, and a `nextCursor` that is absent on the last page. Keep cursors valid for a reasonable time, and document how long. If you also support offsets for convenience, document that they are unsafe for extraction under change.

### Idempotent Writes

Support an `Idempotency-Key` header on every `POST` that creates something. The server stores, for each key, a fingerprint of the request and the response it produced, for a window such as 24 hours. A repeated request with the same key and the same body returns the stored response (flagged, for instance, with a header) instead of repeating the work. A repeated key with a *different* body is a client bug, and should fail with `422` or `409` rather than silently doing something unexpected. The lab server in Appendix {{ref app:codelab}} implements a simple version, and an IETF draft is standardizing the header.

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

A contract written this way has three benefits beyond documentation. Consumers can generate clients and mock servers from it, so they can start work before you finish. You can lint it against a style guide in your delivery pipeline, so every API in the company follows the same rules. And contract tests (Chapter {{ref ch:testing}}) can verify that the implementation does what the contract says.

## Webhooks as a Provider

If integrators cannot poll you efficiently, or you want to notify them promptly, you will offer webhooks. They look simple, and the difference between a naive webhook feed and a reliable one is large. {{ref fig:apidesign-webhook-delivery-as-a-provider}} shows the reliable design.

{{fig apidesign-webhook-delivery-as-a-provider | A reliable webhook feed records events first, then delivers them with signatures, retries, a delivery log, and a replay endpoint.}}

Your service records each event in an **outbox or event store** in the same transaction as the business change (step 1). A **dispatcher** reads the store (step 2), signs each event, and sends it to each subscriber (steps 3 and 4). It records every attempt in a delivery log (step 5). If a subscriber is slow or down (failure point A), the dispatcher retries with backoff over hours, and after repeated failure disables the subscription and notifies the owner (step 6) rather than retrying forever.

{{tbl hooks | Practices for a reliable webhook provider}}

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

{{tbl events | Event design: do and avoid}}

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

1. **Audit an API you use.** Score a vendor API against the twelve rules in {{ref tbl:rules}}. Which missing rule has cost you the most effort?
2. **Write a problem-details body.** Design the error response for an order that fails because the requested quantity exceeds available stock. Choose the `type`, `code`, and extension fields.
3. **Design a webhook feed.** For an `order.shipped` event, decide thin or fat, define the signature scheme, the retry schedule, and the replay window. Justify each choice in one sentence.
4. **Sketch the contract.** Write an OpenAPI fragment for `GET /customers` with cursor paging, an `updatedSince` filter, and a documented 429. What would you add to let consumers detect deletions?
