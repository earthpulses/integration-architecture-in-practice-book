# Case Studies

Patterns and platforms become convincing when you see them applied to a whole situation: a business problem, the constraints that shaped the answer, the decisions that were made, and the places where the design later hurt. This chapter presents nine architectures modeled on situations that enterprises genuinely face, using the technologies those enterprises typically run.

They are **composites**, built from common public architectures and widely repeated lessons, not descriptions of any specific organization. No customer, product decision, or incident here belongs to a real company, and any resemblance is coincidental. Use them as worked examples in design sessions: cover the "design decisions" and ask a group what *they* would do, then compare.

!!! goals "In this chapter"
    * Analyze nine integration architectures, from API-led order-to-cash to a governed data platform
    * Trace each design decision to a constraint and to patterns from Chapters 6 and 7
    * Anticipate the characteristic pitfalls of each situation
    * Recognize what the nine have in common

## Case 1: Order-to-Cash Across SAP, Salesforce, and a Web Shop

A global manufacturer sells through a web shop and through field sales using Salesforce. Orders, prices, and stock live in SAP S/4HANA, and a warehouse system ships. Every new sales channel used to mean another point-to-point project, each with its own mapping and its own way of failing.

{{fig case-case-1-order-to-cash-across-sap-salesforce-a | Case 1: order-to-cash with API-led layers. Experience APIs serve each channel, a process API owns order rules, and system APIs isolate each back end.}}

**Design decisions.** The company built one *system API* per back end, owned by the team that knows it. SAP access is isolated behind a single translator, so an S/4HANA upgrade touches one place. A *process API* owns the order rules and the saga: reserve stock, confirm the price, create the sales order, and compensate if the warehouse rejects. Invoices and shipping notices travel asynchronously through a queue, so the web shop never waits on them. Gateway policies, client-ID enforcement, rate limiting, and token validation, apply at the experience layer, and the internal layers trust only the layer above.

**Pitfalls.** SAP's IDoc status handling and the *idempotent creation* of orders are the sharpest edges; the team used the web order number as an external key so that a retried creation could find the order it had already made. Chained synchronous hops add latency, so each layer has a time budget. And the process API tends to become a dumping ground for business rules that no one owns; the cure is a named owner and a rule that the process layer holds only orchestration and decisions.

**Platform notes.** An integration platform with governance features, reusable connectors for SAP and Salesforce, and one place to apply policy suits this estate. A comparable build on cloud-native services is possible, but the team would assemble the governance itself.

**Patterns used:** API-led connectivity, orchestration, saga, queue, API gateway, anti-corruption layer.

## Case 2: A Bank Offloads Mainframe Events to Kafka

A bank's core system runs on a mainframe with IBM MQ and Db2. Fraud detection, digital channels, and analytics all want core events in near real time. But mainframe query load is billed by usage, and the system is under change freeze for most of the year.

{{fig case-case-2-bank-offloads-mainframe-events-to-kaf | Case 2: mainframe offload. Messages already on MQ are copied to Kafka by a bridge, and database changes are captured from the Db2 log. Fraud scoring runs as a stream processor; consumers read through separate groups.}}

**Design decisions.** The core is not modified. Messages that already flow through MQ are copied to Kafka by a bridge connector; tables with no messages are captured from the Db2 log. Topics are keyed by account, so per-account ordering holds. Fraud scoring runs as a stateful stream processor with a time window. The data lake and the channel services consume through *separate consumer groups*, so one team's lag never affects another's. Schemas in Avro or Protobuf are registered and owned by the core team, with a backward-transitive compatibility mode because replay is part of the operating model.

**Pitfalls.** An MQ unit of work does not map to a Kafka transaction, so the team defined precisely what "delivered" means and made every consumer idempotent. Copybook-defined messages carry EBCDIC text and packed decimals that need careful conversion. And account numbers are *sensitive*: they are tokenized before they land in broadly readable topics.

**Platform notes.** IBM MQ and its integration products remain the system of record for messaging; Kafka, managed or self-run, becomes the new fan-out layer, fed by a bridge connector or a Camel route.

**Patterns used:** queue, change data capture, event streaming, stream processing, event-carried state transfer.

## Case 3: Retail Stores, an Event Mesh, and Cloud Inventory

A retailer with 1,200 stores wants real-time stock and sales events in the cloud. Stores must keep trading when the wide-area link fails.

{{fig case-case-3-retail-stores-an-event-mesh-and-cloud | Case 3: stores with local brokers connected through an event mesh to cloud brokers, with a bridge copying a subset to Kafka for the data platform.}}

**Design decisions.** A small broker in each store buffers events and, when the link returns, forwards them in order, so stores never depend on the cloud in order to sell. Hierarchical topics (for example `retail/EU/store-0412/sale/completed`) let services subscribe to a country, a store, or a product family without code changes. The mesh routes events only to where subscribers exist, which keeps wide-area traffic small, and an analytics bridge copies a subset to Kafka for the data platform. The ERP receives summarized events rather than every scan.

**Pitfalls.** Topic taxonomy needs governance, or the mesh becomes a swamp. Clock drift on store devices breaks ordering by timestamp. And device certificates must be issued, rotated, and revoked across thousands of endpoints.

**Platform notes.** An event-mesh product, or Kafka with MirrorMaker or cluster linking from store clusters. The deciding factors are the number of sites, the mix of protocols, and operational skill.

**Patterns used:** event mesh, publish and subscribe, claim check, edge topology.

## Case 4: Hospital Interfaces, HL7 v2 to FHIR

A hospital group runs dozens of clinical systems, admissions, laboratory, radiology, pharmacy, that exchange HL7 v2 messages through an integration engine. A new patient portal and analytics program need the same data as FHIR resources.

{{fig case-case-4-hospital-interfaces-hl7-v2-to-fhir | Case 4: clinical systems send HL7 v2 messages to an integration engine, which routes them, translates them to FHIR resources, and feeds a FHIR server and downstream consumers.}}

**Design decisions.** The integration engine remains the hub: each clinical system keeps its existing HL7 v2 interface, and the engine translates messages into FHIR resources for a central FHIR server, which the portal and analytics read. Every channel is named, owned, and monitored as an integration, with acknowledgments checked and failed messages parked for a person. A master patient index matches patient records across systems, and no message is allowed to create a new patient without passing it. A documented *downtime procedure* says what clinical staff do when the engine is unavailable.

**Pitfalls.** Local customizations of HL7 segments differ per system, so every mapping needs testing with real, anonymized messages. Patient matching errors are a patient-safety issue, not merely a data-quality one. And regulation (privacy, retention, audit) applies to every hop, so access logging is part of the design.

**Platform notes.** Specialist healthcare engines carry the standards natively and are the usual choice; a general-purpose platform can work with the right adapters.

**Patterns used:** hub and spoke, message translator, content-based router, retry and dead letter queue, master data management.

## Case 5: Factory Floor to ERP and Lakehouse

A manufacturer wants machine data and production events from plants to reach the ERP (for orders and confirmations), a manufacturing execution system, and a cloud data lakehouse.

{{fig case-case-5-factory-floor-to-erp-and-lakehouse | Case 5: machines speak OPC UA to an edge gateway, which publishes to a site MQTT broker. A bridge forwards to Kafka in the cloud, and an integration platform with an agent in the plant exchanges orders and confirmations with the ERP.}}

**Design decisions.** Machines and controllers speak OPC UA to an edge gateway in the plant's operational network. The gateway publishes to a site MQTT broker, which buffers during outages. A bridge forwards selected topics to Kafka in the cloud, from which a sink loads the lakehouse. Orders and confirmations flow between the manufacturing execution system and the ERP through an integration platform whose agent sits in the plant and opens only outbound connections, so no inbound firewall rule crosses the operational boundary.

**Pitfalls.** Security zones: the operational network is separated from the corporate one, and every crossing needs a review. Time synchronization across devices. Data volume: filtering and aggregating at the edge cuts the stream to what is valuable. And the cultural gap between operational technology and IT teams, which delays more projects than any technical issue.

**Patterns used:** hybrid agent, event streaming, edge and store-and-forward, outbox, idempotent receiver.

## Case 6: Joiner, Mover, Leaver

A company with 20,000 employees provisions accounts manually. New hires wait days for access, and leavers' accounts linger for weeks, which auditors have noticed.

{{fig case-case-6-joiner-mover-leaver-across-hr-identit | Case 6: the HR system is the source of truth, an identity provider provisions accounts and roles into applications through standard connectors, and a reconciliation finds orphan accounts.}}

**Design decisions.** The HR system is the *only* source of truth for who works at the company. An identity provider consumes HR events (hire, transfer, termination), and provisions, updates, and removes accounts and roles in applications through the SCIM standard where supported, and through connectors where not. Role assignment rules live in the identity provider, with approval workflows for sensitive roles. A daily *reconciliation* compares accounts in every application against the HR roster and reports orphans.

**Pitfalls.** Effective dating: a hire entered in October for a January start must not receive access in October. Rehires who return with new identifiers duplicate people. Leavers must lose access within hours, so the termination event has to be prompt and reliable, with a reconciliation as backstop. Attribute mappings differ per application.

**Patterns used:** identity provisioning, publish and subscribe, snapshot and diff, saga for multi-system provisioning.

## Case 7: Retail Supply Chain EDI

A retailer exchanges purchase orders, shipping notices, and invoices with several hundred suppliers using EDI, and onboarding a new supplier takes months.

{{fig case-case-7-retail-supply-chain-edi | Case 7: suppliers exchange X12 documents over AS2 or SFTP with a managed file transfer gateway, an EDI translator maps them to a canonical order model, and the ERP receives IDocs. Acknowledgments return automatically.}}

**Design decisions.** All partner traffic enters through a managed file transfer gateway in the DMZ. An EDI translator maps each partner's variant of the standard documents to a *canonical order model*, so the ERP sees one format regardless of partner, and the partner-specific variations are isolated at the edge. Acknowledgments (X12 997) return automatically, and an onboarding kit with test documents and a checklist shortens the partner queue.

**Pitfalls.** Partner-specific interpretations of the "standard." Certificate expiry for AS2, so a calendar and alerts for every partner certificate. And the long tail: the last fifty suppliers use obscure variants that need custom mapping.

**Patterns used:** B2B and EDI exchange, managed file transfer, canonical model, message translator, idempotent receiver.

## Case 8: A Modern Data Platform

A company is building a data platform that ingests from SaaS applications and operational databases, transforms the data in a lakehouse, and returns insights, such as customer scores, to operational tools.

{{fig case-case-8-modern-data-platform-with-saas-elt-cd | Case 8: an ELT tool loads SaaS data; CDC and Kafka stream operational databases; transformations run in the lakehouse; reverse ETL pushes scores back to CRM and marketing; lineage events feed a catalog.}}

**Design decisions.** A managed ELT tool loads SaaS applications into the lakehouse's raw zone. Change data capture and Kafka stream operational databases. Transformation from raw to curated runs as versioned SQL models, with tests. Reverse ETL pushes customer scores and segments back into the CRM and marketing tools through their APIs. Every job emits lineage events to the data catalog, so analysts can see where a number came from.

**Pitfalls.** SaaS rate limits slow loads. Identity resolution (matching a warehouse customer to a CRM contact) decides whether reverse ETL works. Ownership of the *fields* that reverse ETL overwrites must be agreed with the CRM team. And lineage is only as good as the jobs that emit it.

**Patterns used:** scheduled ELT, change data capture, event streaming, reverse ETL, read-model replication.

## Case 9: Integrating a Data Catalog with the Estate

A company introduces a data catalog to govern its data, and needs it connected to databases, BI tools, process tools, and orchestrators, so that it reflects reality instead of becoming a stale spreadsheet.

{{fig case-case-9-integrating-a-data-governance-catalog | Case 9: scanner agents harvest metadata and lineage from databases and BI tools; custom jobs and vendor packages use the catalog's REST import APIs; workflows create tasks that integrations poll; orchestrators emit lineage events.}}

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
