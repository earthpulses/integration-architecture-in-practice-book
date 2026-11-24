# Integrating Enterprise SaaS Platforms

Most enterprise integrations touch a handful of large platforms: a CRM, an ERP, a service-management tool, a human-resources suite, a productivity and identity platform. Each is a large product with its own history, its own vocabulary, and its own way of exposing data. Each has interfaces that are excellent for some jobs and unsuitable for others, change-detection mechanisms that range from elegant to absent, and traps that bite people who treat it as "just another REST API."

This chapter is a field guide to six such platforms: Salesforce, SAP S/4HANA, ServiceNow, Workday, Microsoft's cloud, and Oracle NetSuite. It does not replace the vendors' documentation, which changes with every release. Its purpose is to tell you *what to look for*: which interfaces exist, how to learn about changes, what the upsert key is, where the limits are, how to authenticate unattended, and which traps the experienced have learned the hard way. Use each section as the starting point for a reconnaissance sheet (Chapter {{ref ch:readdocs}}), and confirm every point against the client's edition and release.

!!! goals "In this chapter"
    * List the main interfaces of six major enterprise platforms and when each fits
    * Identify, for each, how to detect changes, what key to upsert by, and where the limits sit
    * Choose an unattended authentication method appropriate to each platform
    * Avoid the characteristic traps: hidden fields, side effects of writes, expiring subscriptions, effective dating
    * Apply twelve questions to any new SaaS platform before designing

!!! why "Why this matters"
    Vendors change APIs, limits, and authentication options with every release, and editions differ. The sections below tell you the questions to ask and where to look. They are not a substitute for confirming the answers for your client's exact edition and version. A design built on a remembered limit that changed last year is a defect waiting for production.

## Salesforce

Salesforce offers the widest set of interfaces of the six. The **REST API** and **SOAP API** handle record operations. The **Bulk API 2.0** is an asynchronous interface for large volumes: you submit a CSV, receive a job identifier, and poll for the result, the asynchronous request-reply pattern of Chapter {{ref ch:patterns1}}. The **Composite API** lets one call perform several operations. The **Metadata API** manages configuration. And the **Pub/Sub API**, based on gRPC, carries event streams.

{{tbl salesforce | Salesforce at a glance}}

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

{{tbl sap | SAP S/4HANA at a glance}}

| Aspect | What to know |
|---|---|
| Interfaces | OData APIs, SOAP services, IDocs, BAPIs and RFCs, CDS views for extraction |
| Change detection | Business events published to an event mesh; IDoc change pointers; delta-enabled extraction from CDS views |
| Upsert key | Business keys (order number, material number); external references such as the customer's purchase-order number support duplicate checks |
| Limits | Set by application-server capacity and dialog work processes; bulk loads are often scheduled in batch windows |
| Authentication | Technical communication users with role-based authorizations; OAuth or certificates through integration middleware; cloud editions use communication arrangements |
| Watch out | IDoc status monitoring (for example, status 51, "application document not posted") needs an owner; authorization objects take time to get right; transports move configuration between systems; prefer released APIs over custom code to keep the core clean |

The most valuable advice about SAP is organizational. Prefer **released APIs**: SAP promises to keep them stable, whereas direct table access or custom code in the core makes upgrades painful, a stance often called "keeping the core clean." And treat **IDoc monitoring** as part of the integration. An IDoc that fails to post sits in an error status, visible only to someone looking at the right screen; if nobody owns that screen, orders silently fail to arrive. Name an owner and alert on statuses, as Chapter {{ref ch:reliability}} describes.

## ServiceNow

ServiceNow's **Table API** is a REST interface to any table, which is both its power and its hazard: one endpoint pattern reads and writes incidents, changes, users, and custom tables. The **Import Set API**, with **transform maps**, stages data in a table and then maps it to targets, which is the preferred route for loads. **Scripted REST APIs** expose custom endpoints, **IntegrationHub spokes** provide prebuilt connectors in Flow Designer, and outbound REST messages call other systems.

{{tbl servicenow | ServiceNow at a glance}}

| Aspect | What to know |
|---|---|
| Interfaces | Table API, Import Set API with transform maps, Scripted REST APIs, IntegrationHub spokes, outbound REST messages |
| Change detection | Queries on `sys_updated_on`; business rules or flows that call out on change; audit history (`sys_audit`) for field-level changes |
| Upsert key | `sys_id` internally; in transform maps, the *coalesce* setting decides whether a row updates an existing record or inserts a new one |
| Limits | Instance-level REST rate-limit rules configurable by administrators; large queries need paging |
| Authentication | OAuth or basic authentication for an integration user with roles and ACLs; a MID Server reaches on-premises systems from the cloud instance |
| Watch out | ACLs filter what the integration user sees; business rules fire on API writes; transform maps that coalesce on the wrong field create duplicates |

The **coalesce** trap is the classic: a transform map that coalesces on the wrong field, or on none, inserts a new record on every run instead of updating, and a month later the table holds thirty duplicates of each incident. Test the load twice and check the row count, the idempotency test of Chapter {{ref ch:testing}}. For on-premises connectivity, the **MID Server**, an agent installed in the customer's network, plays exactly the role of the outbound agent from Chapter {{ref ch:topologies}}.

## Workday

Workday's integration surface reflects its role as a system of record for people. **Workday Web Services** (SOAP, versioned) cover most operations, and newer **REST APIs** are growing. **Reports-as-a-Service** exposes custom reports as web services, a very common way to extract data. The **Enterprise Interface Builder** (EIB) supports file-based loads and extracts, and **Workday Studio** handles complex integrations.

{{tbl workday | Workday at a glance}}

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

{{tbl microsoft | Microsoft's cloud at a glance}}

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

{{tbl netsuite | Oracle NetSuite at a glance}}

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

The questions are the same ones that Chapter {{ref ch:readdocs}} taught you to ask of any API; the platform sections above show how the answers look in practice.

## Summary

Six major platforms each have their own interfaces, change-detection mechanisms, keys, limits, and traps. Salesforce offers bulk, composite, and gRPC event interfaces, upserts by external ID, and hides fields behind field-level security. SAP S/4HANA exposes OData, IDocs, and events; prefer released APIs and assign an owner to IDoc monitoring. ServiceNow's Table API is powerful, its transform-map coalesce setting decides between update and duplicate, and a MID Server reaches on-premises systems. Workday's effective dating makes "changed since" two questions and its reports-as-services are the usual extraction path.

Microsoft's Graph pairs change notifications with delta queries, and expiring subscriptions must be renewed and reconciled. NetSuite's account-wide concurrency limit is shared among all integrations. For any new platform, twelve questions on interfaces, change detection, keys, limits, authentication, visibility, side effects, events, sandboxes, versions, connectors, and vendor behavior prepare the design.

## Exercises

1. **Build a cheat sheet.** Choose a SaaS platform you integrate with that is not covered here, and fill in the six rows (interfaces, change detection, upsert key, limits, authentication, watch out).
2. **Test the visibility.** For one platform, compare what an administrator sees with what your integration user sees, using record counts and field lists. Where do they differ?
3. **Find the side effects.** List every automation (trigger, workflow, flow) that fires when your integration writes to a target platform. Could a bulk load overwhelm any of them?
4. **Renew the subscription.** For a platform with expiring notification subscriptions, write the schedule for renewal and the reconciliation that covers a lapse.
