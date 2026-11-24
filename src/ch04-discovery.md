# Discovery: Asking the Right Questions

Larkspur's second attempt began with a workshop, and the first ten minutes were uncomfortable. The business owner, Head of E-commerce, described the goal as "getting orders into the ERP faster." The ERP product owner said that was already happening, because the nightly import worked. The warehouse manager disagreed, loudly, and mentioned the 214 rejected rows. The finance lead pointed out that order totals in the shop and the ERP differed by small amounts after discounts and nobody knew why. The architect wrote four numbers on the whiteboard and asked for each of them, and nobody in the room knew more than two.

By the end of ninety minutes the room had agreed on something precise: *99 percent of orders in the ERP within five minutes; shipping status back on the shop within thirty minutes of dispatch; the shop owns the order and the customer's address; the ERP owns price confirmation, stock, and invoices.* That sentence took ninety minutes and replaced three weeks of misaligned assumptions.

Discovery is the discipline of getting to that sentence on purpose. It is the cheapest phase of an integration project and the one most often cut. This chapter teaches you to run it: the seven dimensions to cover, the four numbers to leave with, how to run a workshop that produces answers instead of opinions, and how to turn the answers into a brief the business will sign.

!!! goals "In this chapter"
    * Cover the seven dimensions of integration discovery and recognize red-flag answers
    * Turn a vague request into a precise brief, and read the design consequences hidden in it
    * Obtain the four numbers that let you size almost any design
    * Plan and run a ninety-minute discovery workshop, and the follow-up sessions
    * Build an authority matrix that makes ownership explicit
    * Handle unanswered questions as risks rather than assumptions

## The Seven Dimensions

Before choosing REST or Kafka, run discovery across seven dimensions. They are deliberately broader than "technical requirements," because most of the facts that decide an integration are not technical. {{ref tbl:dimensions}} lists each dimension with the questions to ask, what a good answer looks like, and the red-flag answer that should make you probe harder.

{{tbl dimensions | The seven dimensions of discovery}}

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

!!! example "A vague request and its precise brief"
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

!!! tip "Getting a number out of someone who does not have one"
    When a stakeholder says "I don't know how many," do not accept it, and do not guess for them. Ask a bracketing question: "Is it closer to a thousand, a hundred thousand, or ten million?" Almost everyone can answer that, and one order of magnitude is enough for design. Then ask who *could* give an exact figure, and record that person's name.

### Estimating Volume in Your Head

You will often need to turn a business statement into a request rate on the spot. The arithmetic is simple, and doing it aloud in the workshop builds credibility. Larkspur's shop takes 4,000 orders per day, with a peak hour carrying about 1,200. Each order has three lines on average. Creating one order in the ERP takes one API call. At the peak that is 1,200 calls per hour, or one call every three seconds, about 0.33 calls per second. Even allowing growth of 30 percent a year for three years, you need roughly 0.7 calls per second: well under the ERP's limit of one per second. That single paragraph of arithmetic tells you *one call per order is feasible, and no batching is required*.

Now change one number. If the ERP's limit were 0.2 calls per second, the same arithmetic would say the design is infeasible, and you would need a bulk endpoint or an import job. The calculation took thirty seconds and saved a failed design.

## The Authority Matrix

Of all the artifacts discovery produces, the most valuable is the **authority matrix**: a table that lists each entity and field and names the one system that is authoritative for it. It is the document that prevents the most expensive kind of integration problem, two systems both editing the same data.

{{tbl authority | An authority matrix for the shop-to-ERP integration}}

| Entity and field | Authoritative system | Other systems | Direction of change | Notes |
|---|---|---|---|---|
| Order: lines, quantities | Shop | ERP (read-only copy) | Shop to ERP | Frozen once the ERP confirms |
| Order: confirmed price | ERP | Shop (read-only) | ERP to shop | Shop price kept for comparison only |
| Order: shipping status | ERP | Shop | ERP to shop | Events from the warehouse system |
| Customer: shipping address | Shop | ERP | Shop to ERP | Customer edits at checkout and in the account page |
| Customer: credit limit | ERP | Shop | None | The shop never needs it |
| Product: stock level | ERP | Shop (cache) | ERP to shop | Refresh every five minutes |

The matrix does two jobs. It tells the build team which flows exist and which direction each runs. More valuably, it forces a conversation. The first time Larkspur filled in the row for "customer shipping address," the shop team and the ERP team each assumed they owned it. The resolution, shop-owned with the ERP receiving a copy, was reached in five minutes and eliminated a whole class of overwrite bugs. When you genuinely cannot assign a single owner to a field, you have found a problem that needs a business decision, not a technical one. Chapter {{ref ch:patterns2}} covers what to do when two systems must both edit.

## Running the First Workshop

Discovery is a conversation, and conversations need structure. A ninety-minute first workshop with the business owner, both system owners, and the architect covers six topics.

{{tbl agenda | A ninety-minute first-workshop agenda}}

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

**Send each group their questions a day ahead.** Do not read a list aloud to a room of five groups. Send business, data, interface, security, and operations stakeholders the questions that concern them, and run a short session per group. Appendix {{ref app:discoverybank}} contains the full bank of 125 questions, grouped by who can answer them, with the design consequence of each.

### Red-Flag Questions

When something feels off, these questions reliably surface the truth. Ask them politely, and listen to the pause before the answer.

* "Has anyone actually called this API in production?" Many internal APIs have never been called by anyone outside the team that wrote them.
* "What happened the last time the source team changed this interface?"
* "Can I see the largest record or file you have?"
* "Which fields are free text, and who types into them?"
* "If this integration stopped for a week, who would notice first?"

The last question is the most revealing. If the answer is "nobody," the integration may not be needed. If the answer is "the CFO," you have just identified your real business owner.

## Reading the Design Consequences

Every discovery question exists because its answer changes the design. Making that link explicit helps you decide which questions to press and which to let go. {{ref tbl:consequences}} shows ten examples from the question bank.

{{tbl consequences | Ten questions and what their answers change}}

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

Read the brief again with the design in mind. The two open risks are the ones that will shape the architecture: a non-idempotent create call and a webhook feed with no replay. Chapter {{ref ch:capstone}} shows how Larkspur's design answered both.

## Summary

Discovery is the cheapest and most skipped phase of an integration project. It covers seven dimensions, business, data, interface, timing, non-functional, security and network, and operations, and a good answer in any of them has a number, a name, or a document attached. Vague answers are placeholders, not answers.

Four numbers (records now, records in three years, peak changes per hour, acceptable staleness) let you size almost any design, and simple arithmetic on them decides feasibility in seconds. The authority matrix assigns every field to exactly one system and surfaces ownership disputes early. A ninety-minute workshop, run with drawings of the real current state, real records, and a separation of needs from solutions, produces the answers. Unknowns become risks with owners and dates, never silent assumptions, and the whole exercise ends in a signed one-page brief.

## Exercises

1. **Convert a vague request.** Take a one-sentence integration request from your own work and rewrite it as a precise brief of five or six sentences. List the design decisions that the precise version implies.
2. **Do the arithmetic.** For an integration you know, estimate the four numbers. Compute the average and the peak request rate per second. Does the target system's rate limit allow it?
3. **Build an authority matrix.** Choose two systems and ten fields they share. For each, name the authoritative system. For which fields did you hesitate? Whom would you ask?
4. **Run the red-flag questions.** Ask the five red-flag questions about an integration in your organization. Write down the most surprising answer.
