# Governance and the Operating Model

One integration is a project. A hundred integrations are an estate, and an estate behaves differently from a project. Without an operating model, estates grow into duplicate flows that do the same thing three ways, forgotten credentials that nobody dares revoke, failures that no one owns, and five overlapping platforms bought by five departments. Each integration was sensible when it was built; together they form something no one understands.

This chapter describes how to run integration as a *capability* rather than a series of projects: who does what, how requests flow, which standards matter, how the estate is inventoried and measured, and how data contracts and lineage tie integrations into data governance. It is the chapter for people who will set standards and shape teams, and the background for everyone else on why the standards they meet exist.

!!! goals "In this chapter"
    * Compare central, federated, and platform-plus-paved-road operating models
    * Design an intake process with a fast lane for standard patterns and review for the rest
    * Define a standards catalog and an integration inventory, and keep both alive
    * Use data contracts to make agreements between producers and consumers machine-checkable
    * Connect integrations to lineage and a data catalog
    * Retire integrations properly, and measure the health of the estate
    * Govern citizen automation and AI agent tools

## Operating Models

Three operating models cover most organizations.

{{tbl opmodels | Three operating models for integration}}

| Model | How it works | Works when | Fails when |
|---|---|---|---|
| Central integration team | One team builds and runs all integrations | Small estates; heavy regulation; scarce skills | Demand outgrows the team and it becomes a queue |
| Federated delivery | Each domain builds its own integrations | Strong engineering in the domains | There are no standards: duplication, sprawl, uneven security |
| **Platform plus paved road** | A platform team provides runtimes, templates, pipelines, connectors, and guardrails; domain teams build on it; high-risk designs receive a light review | Most medium and large enterprises | The paved road is harder than the dirt track, so teams go around it |

{{ref fig:governance-integration-operating-model}} shows the third model.

{{fig governance-integration-operating-model | The platform team makes the right way the easy way. Domain teams deliver. An inventory and catalogs keep the estate visible.}}

The platform team maintains the **standards, templates, pipelines, and connectors**, and *enables* the domain teams (sales, finance, data), which build integrations on that foundation. Each domain registers what it builds in the **integration inventory and the API and event catalogs**. A lightweight **architecture review** examines only high-risk designs. The key phrase in the table is the failure mode: the paved road must be *easier* than going around it. If the standard template takes longer to use than a quick script, teams will write quick scripts, and the platform will have standards that nobody follows. Measure the platform by how many teams *choose* it.

## Intake: How a New Request Flows

How a request enters the system determines whether the paved road is used. {{ref fig:governance-integration-intake-process}} shows an intake process with two lanes.

{{fig governance-integration-intake-process | Most requests should match a standard pattern and take the fast lane. Only novel or high-risk designs need a full review.}}

A request arrives as a one-page brief and is triaged for tier and risk (arrow 1). One question then sorts it (arrow 2): does it match a standard pattern? If yes (arrow 3), it takes the **fast lane**, using a template and the paved road; if not (arrow 4), it receives an architecture review with decision records. Either way (arrows 5 and 6), the result is built and *registered in the inventory*. A healthy platform sees the large majority of requests in the fast lane, and measures the lead time from request to production for each lane.

## The Standards Catalog

Standards are agreements that make estates predictable. A catalog lists them in one place, each with an owner and a reference implementation.

{{tbl standards | A standards catalog for integration}}

| Standard | Contents |
|---|---|
| Pattern catalog | Approved patterns (Chapters {{ref ch:patterns1}} and {{ref ch:patterns2}}) with when to use them and reference implementations |
| API style guide | Naming, versioning, pagination, errors, security, deprecation (Chapter {{ref ch:apidesign}}) |
| Event style guide | Envelope, naming, keys, versions, schema compatibility, topic naming and ownership |
| Error handling and logging | Retry rules, quarantine and dead letter conventions, the log schema, correlation and trace propagation (Chapter {{ref ch:reliability}}) |
| Security baseline | Identities, secrets, encryption, data classification handling, review triggers (Chapter {{ref ch:security}}) |
| Delivery standard | Repositories, pipelines, environments, release strategies (Chapter {{ref ch:delivery}}) |
| Operational readiness | A runbook, alerts, objectives, an owner, and a recovery tier before go-live (Chapters {{ref ch:reliability}} and {{ref ch:recovery}}) |

A standard without a *reference implementation* is a document; with one, it is a starting point that saves a team a week. Ship templates, not just rules.

## The Integration Inventory

You cannot govern what you cannot see. The **inventory** records every integration, ideally harvested automatically from platforms and pipelines rather than typed by hand.

{{tbl inventory | Fields of an integration inventory record}}

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
* **Emit lineage events** from orchestrators, transformation tools, and custom integrations, using the OpenLineage specification where possible, and harvest connector configurations for Kafka (Chapter {{ref ch:kafka2}}).
* **Link data contracts, owners, and classifications** to the catalog assets they describe.
* **Use lineage to answer governance questions** about origin, usage, and the impact of change.

## Lifecycle: Versioning, Deprecation, Retirement

Every integration has a lifecycle, and the end of it is the part most often skipped. Five rules keep an estate from filling with zombies. Every interface and integration has a version and an owner. A breaking change requires a new version and a published deprecation window. Usage is measured per consumer, so you know whom to contact. Deprecated items receive reminders, then, where policy allows, scheduled brownouts, then retirement. And **retirement removes everything**: credentials, firewall rules, topics, schedules, and the inventory entry, not merely the code. A decommissioned integration whose service account still exists is a security finding waiting to happen.

## Measuring the Estate

{{tbl kpis | Estate health indicators}}

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

Review only what needs it: new patterns, tier-one integrations, regulated data, new platforms, and new external parties. Use a short checklist, the design review questions of Chapter {{ref ch:mindset}} plus the security review pack of Chapter {{ref ch:security}}, give an answer within a week, and record the outcome as decision records. A review process that takes a month trains teams to avoid it.

## Citizen Integration and AI Agents

Two newer sources of integration challenge governance. **Citizen automation tools** put integration in the hands of business users: personal productivity flows, team notifications, small data movements. Allow them within data-loss-prevention policies, inventory them, and *promote* anything business-critical onto the governed platform with an owner. **AI agent tools**, exposed through protocols such as MCP, are integrations too, and should be governed as such: inventory each tool, scope its credentials, require human approval for writes, log every call, and review which data the agent can reach (Chapter {{ref ch:security}}).

## Summary

An estate needs an operating model. The platform-plus-paved-road model, in which a platform team provides templates, pipelines, and guardrails and domain teams build on them, suits most organizations, provided the paved road is genuinely easier than going around it. Intake with a fast lane for standard patterns and review for novel or risky designs keeps lead times short and risk visible.

A standards catalog with reference implementations, an inventory harvested from platforms, machine-checkable data contracts, and lineage linked to a catalog make the estate legible. Retirement removes credentials and rules as well as code, and a handful of indicators, owner coverage, incidents, lead time, reuse, and credentials past rotation, show whether the estate is improving. Citizen automation and AI agent tools belong inside the same governance framework.

## Exercises

1. **Write an inventory record.** For three integrations you know, fill in the record fields. Which fields can you not fill, and who could?
2. **Find the zombies.** List integrations whose owner has left or whose purpose is forgotten. What would retiring each involve beyond deleting code?
3. **Design the fast lane.** Define three "standard patterns" for your organization with a template for each. What makes each easy to use?
4. **Write a contract.** Draft a data contract for an event or dataset you produce: schema, quality rules, latency, and owner. Who would check it, and how?
