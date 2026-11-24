# Making the Decision

Discovery produces answers. Patterns offer options. The step between them, deciding, is where many architects improvise, and where an explicit method pays for itself. Improvised decisions have two weaknesses: they favor whatever the decider knows best, and they leave no trail, so nobody can later tell whether the choice was reasoned or merely habitual.

This chapter gives you a method with two parts. The first is a set of **seven decision trees** for the choices that recur in every project: how to get data out of the source, how to write to the target, where the runtime should live, which authentication to use, whether to use Kafka and how to feed it, how to take data out of it, and which class of technology to build on. The second is a **scorecard** that combines your answers into a ranked recommendation, with a worked example. Neither replaces judgment. Both make it visible, which is what allows a colleague to challenge it.

!!! goals "In this chapter"
    * Use seven decision trees to make the recurring technical choices in an integration
    * Explain why each tree ends in a mechanism or a class, never in a product name
    * Score candidate patterns against discovery answers, and interpret a close second place
    * Combine two near-tied patterns into one design, such as webhook plus reconciliation poll
    * Record the decision, the rejected alternatives, and the conditions for revisiting them

## Seven Decision Trees

Read each tree from the left. Diamonds are questions you can answer from discovery; rounded boxes are outcomes. Every tree ends in a *mechanism* or a *class*, not in a product. That is deliberate: products change, mechanisms last. After the tree tells you "use log-based change data capture," choosing between Debezium and a commercial tool is a separate, later question.

### How to Get Data Out of the Source

Start with what the source really offers, because that, more than your preferences, decides the extraction mechanism. {{ref fig:tree-how-to-get-data-out-of-the-source}} shows the tree.

{{fig tree-how-to-get-data-out-of-the-source | How to get data out of the source.}}

If the source exposes an API, the first question is whether it supports a modified-since filter or a change feed. If so, **poll with a watermark and reconcile**. If not, ask whether it sends webhooks or events; if so, use a **webhook with a queue and a reconciliation poll**. If neither exists, ask whether listing everything is feasible; for small and medium datasets, use **snapshot and diff**. If listing is infeasible, ask the vendor for a change feed, or, failing that, read the underlying database's log.

If the source offers no API, ask whether direct database access is allowed. If you may read the transaction log, use **log-based change data capture**; if not, a **JDBC query poll** against a replica using a timestamp column. If there is no database access, look for files (**a file drop with a manifest**), a message queue (**a bridge or subscription**), or, failing everything, UI automation as a stopgap while you push for a real interface.

### How to Write to the Target

The target's write semantics decide how safely you can retry, so this tree is about idempotency. {{ref fig:tree-how-to-write-to-the-target}} shows it.

{{fig tree-how-to-write-to-the-target | How to write to the target.}}

If the target supports an **idempotent upsert by key**, everything is easy: for more than about 100,000 records per run, use a bulk import API in batches; for fewer, upsert per record behind a rate limiter. If it does not, check whether it accepts an **idempotency-key header**: if yes, create with the key and keep a deduplication ledger. If not, ask whether you can read the target to check for existence; if yes, *look up before you write*, store the foreign ID, and allow only one writer per key. If you cannot even read, you are left with a single-writer queue plus reconciliation, and you should ask the vendor for an upsert. A strict rate limit on the target adds a queue and a throttle in front of any of these.

### Where the Runtime Should Live

Data-processing boundaries and network direction decide hosting before preferences do. {{ref fig:tree-where-the-runtime-should-live}} shows the tree.

{{fig tree-where-the-runtime-should-live | Where the runtime should live.}}

If payloads may not leave your network or region, use a customer-hosted runtime if the platform offers one (and check its capacity); otherwise run containers or virtual machines with your own code or a self-hosted runtime. If payloads may leave, ask whether the endpoints are reachable from the internet. If yes, a vendor-cloud integration platform or serverless functions is usually fastest. If not, ask whether an outbound-only agent is allowed: if so, use an **agent plus cloud control plane**, and verify where the logic actually runs; if not, you need a private link or VPN to a cloud or on-premises runtime.

### Which Authentication

Machine identity first; human flows only for humans. {{ref fig:tree-which-authentication}} shows the tree.

{{fig tree-which-authentication | Which authentication to use.}}

Ask first who or what is calling. For **a person**, use single sign-on with an authorization-code flow and PKCE. For **a job**, prefer OAuth 2.0 client credentials with short-lived tokens and secrets in a vault. If those are not offered, look for a JWT bearer grant or mutual TLS (and alert on certificate expiry), then an API key (in a header, scoped, and rotated), and as a last resort basic authentication over TLS with a single service account and a vault. For **a webhook**, authenticate by an HMAC signature with a timestamp, and deduplicate by event ID. Chapter {{ref ch:auth}} covers each of these.

### Do You Need Kafka, and Which Way In

Kafka earns its place through replay, fan-out, or throughput. {{ref fig:tree-do-you-need-kafka-and-which-way-in}} shows the tree.

{{fig tree-do-you-need-kafka-and-which-way-in | Do you need Kafka, and which way in.}}

If you need none of the three, do not use Kafka; poll, use a webhook with a queue, or use an integration platform. If you do, choose the entrance that matches the source. Your own **application** produces events directly, with an outbox for atomicity. A **database** feeds through change data capture, or a JDBC poll if the need is simple. **SaaS webhooks** are published by an HTTP gateway or an integration platform. **Legacy** sources, such as MQ, files, and MQTT, use a source connector or a bridge.

### Which Way Out of Kafka

Every exit starts with a pull from Kafka; the target decides what happens next. {{ref fig:tree-which-way-out-of-kafka}} shows the tree.

{{fig tree-which-way-out-of-kafka | Which way out of Kafka.}}

A **store or warehouse** takes a sink connector. A **REST API with limits** takes a consumer or an HTTP sink that pauses on 429 and uses idempotency keys. **Serverless** functions take an event-source trigger and an idempotent handler. **Browsers and mobile** apps take a server-push gateway. A **SaaS** application is reached through an integration platform's listener, with a check on its acknowledgment mode. And if the work has *task semantics*, where order does not matter and each item goes to one worker, consider share groups or a queue instead.

### Which Class of Technology

Finally, which class of platform should carry the pattern? {{ref fig:tree-which-class-of-technology}} shows the tree. Walk it from top to bottom; the first "yes" usually identifies the dominant workload.

{{fig tree-which-class-of-technology | Which class of technology.}}

Mostly SaaS endpoints with business-led delivery points to an **integration platform** (checking where data is processed). Bulk data into analytics points to **ELT and CDC tooling**. Partner documents and EDI point to **managed file transfer and a B2B gateway**. High-volume events with many consumers point to **Kafka or a streaming platform**. Transactional messaging in a mainframe estate points to an **enterprise service bus and message queue** estate. Engineering-led teams that work Git-first point to **code-first services**, and cloud-native estates to the cloud's own workflow and messaging services. Whatever the tree says, validate with a proof of concept against the hardest real flow.

## The Scorecard Method

The trees decide one question at a time. A real integration has many answers at once, and they pull in different directions: freshness favors webhooks, the network favors polling, replay favors streaming. A **scorecard** combines them. The idea is simple. For each answer, ask which candidate patterns it favors or disfavors, and add points. The pattern with the most points leads, and the tally shows why.

{{tbl score | A scorecard for the shop-to-ERP order flow}}

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

The difference between first and second is only two points. When the top two are within about three points, the scorecard is telling you not to choose one. Instead, *combine them*. Webhooks supply the speed that polling cannot, and polling supplies the completeness and replay that webhooks lack. The combination, a webhook feeding a queue as the fast path, plus a reconciliation poll as the slow path, is exactly the "reliable SaaS notifications" recipe from Chapter {{ref ch:patterns2}}. That is the design Larkspur chose.

!!! why "Why this matters"
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

Use them as a drafting aid and a teaching tool, never as an oracle. Their strength is not that they produce the correct answer but that they make your reasoning inspectable. When a colleague disagrees with your scorecard, you can ask which row they would change, and the argument becomes productive instead of tribal. Chapter {{ref ch:platforms}} adds the cost and platform dimensions that this chapter leaves aside.

## Summary

Seven decision trees handle the recurring choices: source extraction, target writes, runtime hosting, authentication, Kafka entry, Kafka exit, and technology class. Each ends in a mechanism or class, never a product. A scorecard combines many answers by adding points for each pattern, and a close second place tells you to combine patterns, as when webhooks supply speed and a reconciliation poll supplies completeness.

Unknown answers become risks, and you check whether any could flip the winner. Worked examples show the method adapting to a database replication, an EDI exchange, and a two-way sync that the authority split reduces to two one-way flows. The decision, its rejected alternatives, and its revisit conditions go into a decision record. The method makes reasoning inspectable; it does not replace judgment.

## Exercises

1. **Walk the trees.** Take an integration you are planning and walk all seven trees. Write the outcome of each. Where did a tree disagree with your instinct?
2. **Build a scorecard.** Choose three candidate patterns for a real flow, list ten discovery answers, and fill in a scorecard. Which answer moved the result most?
3. **Resolve a near-tie.** Find a case where two patterns scored within three points. Design the combination and write the sequence in which the two paths cooperate.
4. **Write the rejected alternatives.** For a past decision of yours, write the "rejected alternatives" section of a decision record, giving a specific reason for each.
