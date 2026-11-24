# Reading API Documentation Like an Architect

When Larkspur's team first read the shop vendor's API documentation, they found the call they needed in ten minutes: `GET /orders`, returning a list of orders with a field called `total`. They wrote the mapping that afternoon. A week later, in testing, the field turned out to be called `totalAmount`, the list returned at most 50 orders per page regardless of the `limit` parameter, the `updatedSince` filter ignored time zones, and a change to an order's shipping address did not change its `updatedAt` timestamp. None of this was in the documentation. All of it was discoverable in an hour of poking at the sandbox.

Developers read documentation to find the call they need. Architects read it to find **what can go wrong**. The difference is a habit, and it is the subject of this chapter. The goal is a one-page *reconnaissance sheet* that answers every design question about an API before anyone writes a line of integration code, and a practice of checking the documentation against the running system, because the two disagree more often than anyone admits.

!!! goals "In this chapter"
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
3. **Authentication and authorization.** Which scheme, which scopes, what token lifetime? Who issues credentials, and is there a concept of a service account? (Chapter {{ref ch:auth}} treats this in depth.)
4. **Resource model.** List the nouns and how they relate, and draw them. Identify the stable identifier of each, and whether a human-readable key also exists. Is the ID a UUID, a number, or something that changes when the record is renamed?
5. **Read paths.** How do you list, filter, sort, and fetch by ID? What is the maximum page size? Is there a "modified since" filter or a change feed?
6. **Write paths.** How do you create, update (does `PUT` replace the whole resource while `PATCH` merges?), and delete (hard or soft)? Are there bulk endpoints? Are writes idempotent, or do they accept an idempotency key?
7. **Pagination.** Offset, page number, cursor, or link header? Is the total count expensive to compute? Is ordering stable while you page?
8. **Limits.** Rate limits (per second, per day, per tenant), payload size limits, concurrency limits, timeouts, and the headers that report your remaining budget.
9. **Errors and asynchrony.** What does an error body look like? Which codes are retryable? Is partial success possible? Do long operations return a job ID to poll?
10. **Eventing.** Are there webhooks, event subscriptions, or streams? How are they signed? What are the retry and replay behaviors?

The order is deliberate. The first three questions tell you whether you can connect at all. The next four describe the data and the ways to move it. The last three describe what happens when things go wrong, and they are the ones that documentation most often skips.

## The API Reconnaissance Sheet

Copy the template in {{ref tbl:recon}} into your project folder and fill it in during the first week. It becomes the basis of the design document and, later, of the support runbook. The "Answer" column holds example answers for a typical SaaS API; yours will differ, and the value is in having a written answer for every row.

{{tbl recon | The API reconnaissance sheet, with example answers}}

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

Two cells deserve special attention because they decide the architecture. **"No delete feed"** means you cannot learn about deletions from the API at all, and you will need a periodic comparison (Chapter {{ref ch:sync}}). **"No replay"** on webhooks means a missed event is gone, so webhooks can only be an accelerator, never the sole source.

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

!!! warning "Probe with care"
    Probes that write data (the second and fourth above) belong in a sandbox. Never run exploratory writes against production. When a sandbox is not available, restrict yourself to read-only probes, and ask the vendor how to test writes safely.

## Let a Script Read the Contract

If the API publishes an OpenAPI document, much of the reconnaissance can be automated. The script below reads an OpenAPI 3.x JSON file and prints what an architect wants to know: the servers, the security schemes, every endpoint with its documented response codes, *hints* (incremental filters, asynchronous operations, bulk endpoints), and *gaps* (lists with no paging, writes with no idempotency key, endpoints that never mention rate limiting). It needs only the Python standard library.

{{code openapi_recon.py}}

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

Of everything in an API, pagination is the topic most worth understanding deeply, because an extraction that pages incorrectly loses or duplicates data *silently*. The core problem is shown in {{ref fig:pagination-offset-drift}}.

{{fig pagination-offset-drift}}

**Offset paging** asks for "the records starting at position 5, five at a time." It is simple, and it assumes that the list does not change while you read it. When it does, positions shift. If a record is inserted at the front between your first and second requests, everything moves down one place, and the second page begins with a record you have already seen. If a record is deleted instead, everything moves up, and the second page begins one record too late: a record is skipped without any error. For a one-off report, this does not matter. For a synchronization that reads thousands of records while users are working, it matters constantly.

**Cursor paging** replaces the position with a bookmark. The server returns, with each page, an opaque token marking the last record delivered, and the next request says "give me the records after this one." Insertions and deletions elsewhere in the list do not move the bookmark, so nothing is repeated or skipped. Cursors also tend to perform at constant cost, however deep you go, whereas offset queries get slower the further you page.

{{tbl paging | The five pagination styles and how to use each}}

| Style | Looks like | Strength | Weakness | Integration advice |
|---|---|---|---|---|
| Offset and limit | `?offset=2000&limit=500` | Simple; random access | Slower when deep; shifts under change | Acceptable for small, static sets; avoid for full extracts |
| Page number | `?page=5&per_page=100` | Simple | Same drift as offsets | Cap the page count; sort by a stable key |
| Cursor or token | `?cursor=eyJpZCI6…` | Stable and fast | No random access; cursors may expire | Preferred for bulk reads; save the last cursor as a checkpoint |
| Link header | `Link: <…>; rel="next"` | Self-describing | Requires parsing headers | Follow links exactly; never build URLs by hand |
| Keyset | `?after_id=981233` | Fast and simple | Needs a sortable unique key | Excellent when you control the sort key |

Four practical rules cover most situations. **Prefer cursors for anything you extract in bulk**, and persist the last cursor as a checkpoint. **Never mix paging styles** in one read: many APIs reject, or silently misinterpret, a request that carries both an offset and a cursor. **Always specify a stable sort field** so that "the order" means the same thing on every page. And **ask whether the total count is expensive**. Some APIs compute a total on every offset request, which on a large collection can be the slowest part of the call, and offer a parameter to switch it off; others return nothing for the total with cursors. If you do not need the total, do not ask for it.

!!! tip "Read the page-size limit per endpoint"
    The maximum page size often differs between endpoints on the same API: a search endpoint might allow 1,000, a list endpoint 100. Read it per endpoint, probe it, and never assume one global value. A client that requests 500 and silently receives 100 will compute its progress wrongly.

Finally, look for **bulk and job endpoints** before looping over single calls. If you must load two million records, an import endpoint that takes a file and returns a job ID is usually orders of magnitude faster, and gentler on the vendor's rate limits, than two million requests.

## Signs the Documentation Is Lying

Documentation is written by people who know the system, for people who do not, and it is rarely tested against reality. Learn to recognize the signs.

{{tbl lying | Warning signs in documentation, and what to do about them}}

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
