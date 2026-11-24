# Capstone: Larkspur Outdoor

Every earlier chapter explains a piece. This chapter puts the pieces together on one realistic project, from the first meeting to the first incident after go-live, and shows the actual artifacts an architect produces along the way. The company and the numbers are fictional. The decisions, the problems, and the fixes are the ones real projects meet.

Read it twice. The first time, follow the story. The second time, close the book at the end of each stage, write down what *you* would produce, and compare. The exercise that turns knowledge into skill is the one in which you make the decisions yourself and then see how a design that reasoned from the same facts turned out.

!!! goals "In this chapter"
    * Follow one integration through eight stages: discovery, decisions, design, mapping and security, numbers, testing and cutover, hypercare, and estimation
    * See how the artifacts of earlier chapters (the brief, authority matrix, decision records, sequence diagrams, mapping specification, failure-injection results) fit together
    * Recognize how a daylight-saving incident exposes a flaw that testing missed, and how the team fixed it
    * Produce your own set of artifacts for a similar project

## The Situation

Larkspur Outdoor sells camping gear online in six countries. Orders from its commerce SaaS reach SAP S/4HANA through a nightly CSV export that staff fix by hand each morning. Customers complain that shipping updates arrive a day late. The chief operating officer wants orders in SAP within minutes and shipping status back on the web shop within the hour, before peak season in fourteen weeks.

You know this company from Chapter {{ref ch:basics}}. Now we build the integration.

## Stage 1: Discovery

The team ran the workshops of Chapter {{ref ch:discovery}}, and recorded the critical answers together with the design consequence of each.

{{tbl capdisc | Larkspur's critical discovery answers and their design consequences}}

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

Two answers shaped everything that followed: the **non-idempotent create call** in SAP, and the **webhook feed with no replay**. Both appear on the risk register of the brief in Chapter {{ref ch:discovery}}, with owners and dates.

## Stage 2: Decisions

Running the decision method of Chapter {{ref ch:decide}} with these answers ranks *webhook with a queue* first and *scheduled polling* close behind, the near-tie that signals a combination: webhooks for speed, a reconciliation pull every 15 minutes for completeness. The architecture recorded three decisions.

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

{{ref fig:capstone-capstone-architecture}} shows the architecture. It consists of two one-way flows: orders in, and status out, plus a stream of order events to Kafka for analytics.

{{fig capstone-capstone-architecture | The Larkspur architecture. Orders flow in through a webhook receiver, a queue, and a worker, with a reconciliation job as the repair path. Status flows back from SAP business events. Order events go to Kafka through an outbox for analytics.}}

**Orders in.** The commerce SaaS posts `order.created` to the **webhook receiver** (step 1). The receiver verifies the signature and timestamp, puts the event on the **order queue** (step 2), and answers at once. The **order worker** takes events from the queue (step 3), maps them (Chapter {{ref ch:formats}}), checks its deduplication ledger, and creates the sales order in SAP through the OData API (step 4). Failure point A is the lost webhook: if the receiver was down during an outage, the event is gone, and *the reconciliation job* repairs it. Every 15 minutes the job lists orders from the shop updated since a watermark (step 5), compares them with what the ledger holds, and enqueues any missing orders (step 6).

**Status back.** SAP publishes a business event when goods are issued (step 7). The **status worker** consumes the event (step 8) and updates the order's status on the shop through its API (step 9). It is a second one-way flow, with SAP authoritative.

**Events for analytics.** The order worker writes order events through an **outbox** (step 10) to Kafka, and the status worker does likewise (step 11); the data platform reads them with a sink (step 12).

Failure point B in step 4 is the most important behavior in the design. {{ref fig:capstone-capstone-order-creation-with-a-timeout}} shows it.

{{fig capstone-capstone-order-creation-with-a-timeout | The most important behavior: after a timeout, find before you create again.}}

The shop posts the event (step 1), the receiver enqueues it and acknowledges it (steps 2 and 3), and the queue delivers it to the worker (step 4). The worker asks the ledger whether it has seen order A1043 (step 5) and learns it has not (step 6). It then calls SAP to create the order, with the shop's order number as the customer reference (step 7), and *SAP commits the order, but the response times out*. The worker cannot tell whether the order exists. It does not retry the create. Instead, it asks SAP to *find an order by that reference* (step 8) and learns the order exists, with number 4500012 (step 9). It records the mapping (step 10) and moves on. The lookup-before-retry turns an API that cannot be called twice into one that can safely be retried. Never blindly re-POST.

## Stage 4: Mapping and Security

The mapping specification, in the format of Chapter {{ref ch:formats}}, fixed the translation field by field.

{{tbl capmap | Larkspur's order mapping to SAP}}

| SAP field | Shop source | Rule |
|---|---|---|
| Sales order type | Constant | Online order type for the country (a code list per sales organization) |
| Sold-to party | `customer.email` | Look up the SAP business partner through a crosswalk; create a one-time customer if none exists (an approved rule) |
| Customer reference | `order.number` | Copy; used for the duplicate lookup |
| Material | `line.sku` | Crosswalk the SKU to a material number; quarantine if missing |
| Quantity, price | `line.qty`, `line.price` | Decimals; SAP confirms the price, and the shop's price is kept for comparison |
| Requested delivery date | `order.created_at` | Convert to the plant's local date |

The threat discussion (Chapter {{ref ch:security}}) found four concerns and a control for each. *Forged webhooks:* HMAC signature plus a timestamp window. *Personal data in logs:* masking in the logging library. *An over-privileged SAP account:* a communication user limited to creating and reading sales orders. *Replay of old webhooks:* the timestamp window and the deduplication ledger.

## Stage 5: The Numbers

{{tbl capnum | Capacity and budget checks}}

| Check | Arithmetic | Result |
|---|---|---|
| Peak throughput needed | 1,200 orders per hour, growing 30% a year for two years, gives about 2,000 per hour | 0.56 orders per second |
| SAP capacity measured in test | One worker creates 2 orders per second with 3 lines each | Two workers give more than 6 times headroom |
| Shop API budget | The reconciliation reads about 300 orders per 15 minutes at peak in 3 pages; status updates 1,200 per hour | Well within the 4 requests per second allowance |
| Outage tolerance | A 4-hour SAP maintenance window at 1,200 orders per hour | 4,800 queued messages, drained in about 40 minutes by two workers |

The last row is reassuring and was worth computing: a four-hour outage does not need heroic measures, because two workers clear the backlog in under an hour.

## Stage 6: Tests, Cutover, and Go-Live

The team ran the failure-injection matrix of Chapter {{ref ch:testing}}: SAP timeouts after commit, duplicate webhooks, a SKU missing from the crosswalk, token expiry, and a four-hour SAP outage replayed at five times speed. They ran a **shadow run** for two weeks in pre-production, in which the new path created orders in a scratch sales organization and a daily report compared them with the output of the nightly CSV path.

Cutover (Chapter {{ref ch:recovery}}) was **phased by country**: the two smallest countries first, the largest in week three, with the CSV export kept as a fallback until the rollback window closed. They defined five service-level indicators and alerts: freshness (95th-percentile order-to-SAP time under five minutes), quarantine rate above one percent, queue age above fifteen minutes, reconciliation drift above zero, and a heartbeat for each worker.

## Stage 7: What Actually Went Wrong in Hypercare

!!! warning "Incident: orders missing on the night of a daylight-saving change"
    The reconciliation job asked the shop for orders updated since its watermark minus two minutes, but computed the watermark in *local time*, while the shop filtered in UTC. On the night the clocks changed, an hour of orders fell outside the window, and their webhooks had been dropped by a gateway restart. The freshness alert fired at 07:10; the team reran the reconciliation with a wider window, and all orders reached SAP by 08:00.

    **Fix:** timezone-aware UTC watermarks everywhere, a 15-minute overlap, a test case for daylight-saving transitions, and a nightly full-day reconciliation as a second safety net.

Study how the incident unfolded. *Two* defenses failed at once: the webhook (the fast path) lost events during a gateway restart, which was expected, and the reconciliation (the repair path) had a time-zone defect, which was not. Because the *freshness alert* existed, the problem was detected within hours, by a machine, and resolved within one morning. Had the team relied on "someone would notice," the orders would have sat in the shop until customers complained. The lessons are the ones of earlier chapters: unlabeled times break watermarks (Chapter {{ref ch:formats}}), overlap windows must be computed from the *source's* clock (Chapter {{ref ch:python}}), and measurable freshness turns incidents into alerts.

## Stage 8: The Estimate That Was Approved

Using the estimation method of Chapter {{ref ch:recovery}}, the team counted three entities (orders, order status, a customer crosswalk), two systems plus Kafka, OAuth, a private link already in place, one-way flows, medium volume, freshness in minutes, some data-quality issues, medium criticality, a standard review, some platform experience, and three environments. The result was size L, with a range of about 45 to 75 person-days. Elapsed time was eleven weeks, driven not by development but by the security review and the shadow run, and delivery came three weeks before peak.

## The Artifacts This Project Produced

Count what exists at the end, apart from the code:

* the integration brief and discovery checklist (Chapter {{ref ch:discovery}});
* the authority matrix and two reconnaissance sheets (Chapters {{ref ch:discovery}} and {{ref ch:readdocs}});
* three decision records (Chapter {{ref ch:decide}});
* architecture and sequence diagrams (Chapters {{ref ch:patterns2}} and {{ref ch:time}});
* the mapping specification and golden-file tests (Chapter {{ref ch:formats}});
* a threat summary (Chapter {{ref ch:security}});
* the test plan and failure-injection report (Chapter {{ref ch:testing}});
* the cutover plan, the runbook, and the alert catalog (Chapters {{ref ch:recovery}} and {{ref ch:reliability}});
* the service-level dashboard, and a post-incident review (Chapter {{ref ch:reliability}}).

Templates for all of them are in Appendix {{ref app:templates}}. A project that ends with this list is one that can be handed over, audited, and extended; one that ends only with code is one whose knowledge lives in people's heads.

## Summary

The Larkspur project followed the journey of Chapter {{ref ch:journey}}. Discovery produced eleven critical answers, two of which, a non-idempotent create call and a webhook feed without replay, shaped the design. The decision method pointed to a combination of a webhook and a reconciliation pull, recorded in three decision records with rejected alternatives and revisit conditions. The design consisted of two one-way flows with a repair path, a lookup before retry for the create call, and an outbox for analytics events.

A mapping specification and a threat discussion followed; capacity arithmetic confirmed headroom; failure injection, a shadow run, and phased cutover reduced risk. A daylight-saving defect in the reconciliation job surfaced in hypercare and was caught by a freshness alert within hours. The estimate was a size L, about 45 to 75 person-days, and the project's real critical path was the security review and the shadow run.

## Exercises

1. **Make the decisions yourself.** Close the book after Stage 1 and write your own three decisions. Compare them with ADR-001 to ADR-003. Where did you differ, and why?
2. **Find the second incident.** Imagine another failure in hypercare: SAP's business events stop arriving. Which alert would fire, which would not, and what would you add?
3. **Remove a safeguard.** Remove the reconciliation job from the design. List the failure modes that would then go undetected.
4. **Adapt it.** Rewrite Stages 2 and 3 for a company whose shop offers webhooks *with* replay and whose ERP accepts idempotency keys. What can you drop?
