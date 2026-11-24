# Security and Threat Modeling

Integrations are attractive targets. They hold credentials that open several systems. They sit on network paths that cross trust boundaries. They move data in bulk. And they are often built quickly, owned vaguely, and reviewed late. An attacker who compromises an integration's service account may reach everything that account can reach, in every system it connects, often with more privilege than any single human user.

This chapter gives you a practical approach to integration security: a way of thinking, threat modeling, that finds problems early; a map of the most relevant risks, using the OWASP API Security list; and the controls for data protection, supply chain, and the review process itself. It is deliberately practical. A security review of an integration should take days, not weeks, if you arrive with the right evidence, and the review pack at the end of the chapter says what that is.

!!! goals "In this chapter"
    * Draw a data-flow diagram with trust boundaries and apply STRIDE to it
    * Map the OWASP API Security Top 10 (2023) to integrations, and name the control for each risk
    * Choose controls for spoofing, tampering, repudiation, information disclosure, denial of service, and privilege escalation
    * Protect data in flows through minimization, classification, masking, retention, and erasure
    * Reduce supply-chain risk from dependencies, connectors, and packages
    * Prepare a security review pack that shortens approval

## Threat Modeling an Integration

A **threat model** answers four questions: what are we building, what can go wrong, what are we going to do about it, and did we do a good enough job? For an integration, the exercise takes about an hour and has a fixed shape. *Draw the data flow, with its trust boundaries. Walk every element and every flow through the STRIDE categories. Rank what you find. Give each threat a control and an owner.*

{{ref fig:security-trust-boundaries-of-an-integration}} shows a data-flow diagram of a typical integration, with the trust boundaries marked as dashed regions.

{{fig security-trust-boundaries-of-an-integration | Trust boundaries of an integration. Every arrow that crosses a dashed boundary needs authentication, integrity protection, and a decision about what may be logged.}}

A partner or SaaS application on the *internet* sends requests to an API gateway with a web application firewall in the *DMZ*. The gateway passes validated requests to the integration service in the *internal network*, which fetches its secrets from a vault, calls internal systems with least-privilege credentials, and writes masked logs to a monitoring system. Failure points mark the threats: spoofing, replay, and flooding at the first boundary (A); elevation if the service account holds more privilege than it needs (B); and disclosure of personal data through logs (C).

The value of the diagram is that it forces you to find every place where data crosses a boundary. Each crossing needs three things: *authentication* (who is on the other end?), *integrity protection* (was it altered in transit?), and a decision about *what may be logged or stored there*.

## STRIDE

STRIDE, devised at Microsoft, is a mnemonic for six categories of threat. Walking each element and flow through the six categories prompts the questions that experience would otherwise have to supply.

{{tbl stride | STRIDE applied to integrations}}

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

The OWASP API Security Top 10 is the standard list of the most serious API risks. The 2023 edition was the most recent API list when this was written; OWASP's separate Top 10 for web applications was updated in 2025, and the two lists should not be confused. Most items concern *authorization*, which is exactly where integrations are weakest, since they often run with broad service accounts. {{ref tbl:owasp}} maps each risk to an integration's concerns.

{{tbl owasp | The OWASP API Security Top 10 (2023) through an integration lens}}

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

Two of these deserve a closer look because they are easy to miss from the integrator's side of the fence. **API7, server-side request forgery,** arises when an integration fetches a URL that arrives in data, for example a webhook payload that contains a "callback URL" or an attachment link. An attacker supplies an address inside your network, and your integration, which sits behind the firewall, obligingly fetches it. Never fetch arbitrary URLs from payloads; allowlist the destinations. **API10, unsafe consumption,** is the habit of trusting a partner's or vendor's response because it comes from a "known" source. Treat everything received from outside as untrusted input: validate its shape, limit its size, and set time limits, as Chapter {{ref ch:formats}} recommends for any record.

## Data Protection in Flows

Moving data is the integration's reason for existing and its principal source of exposure. Seven principles govern how to move it responsibly.

{{tbl dataprot | Principles of data protection in flows}}

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

* **Pin and scan dependencies.** Lock versions, scan for known vulnerabilities in every build (Chapter {{ref ch:delivery}}), and keep a software bill of materials for each integration.
* **Vet connectors and packages before use.** Who maintains them? What permissions do they need? How do they store credentials? A packaged integration that keeps passwords in a plain configuration file is a template to be hardened, not a product to be deployed.
* **Patch on a schedule.** Runtimes, agents, and gateways need updates; monitor vendor security advisories.
* **Separate duties.** The person who writes a flow should not be the only one who can promote it to production.

## A Threat Checklist

When you need a faster start than a full threat model, tick the characteristics that apply to your integration and discuss the corresponding threats with your security team. {{ref tbl:threats}} lists the characteristics, the threats each brings, and the controls to propose.

{{tbl threats | Characteristics and the threats to discuss}}

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

Chapter {{ref ch:topologies}} described seven topologies. Each raises its own security questions, which belong on the review agenda.

{{fig security-network-topology-cloud-app-customer-firewall | An integration agent on a customer server makes outbound calls only. This is the simplest pattern to approve: the firewall needs only the existing outbound rules, and no inbound path to the data center is opened.}}

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

The pack also makes the lead time visible: if the security review takes four weeks, the request is filed on day one (Chapter {{ref ch:journey}}), with this pack following as the design matures.

## Summary

Integrations hold powerful credentials, cross trust boundaries, and move data in bulk, which makes them attractive to attackers. A threat model draws the data flow with trust boundaries, and walks each element and flow through STRIDE: spoofing, tampering, repudiation, information disclosure, denial of service, and elevation of privilege. The OWASP API Security Top 10 (2023), concerned mostly with authorization, maps closely to integration weaknesses, notably object-level authorization, server-side request forgery, and unsafe consumption of third-party APIs.

Data protection means minimizing, classifying, encrypting, masking, retaining deliberately, erasing across all copies, and respecting residency, with special attention to quarantines, dead letter queues, and logs. Supply-chain hygiene pins and scans dependencies and vets packages. A checklist of characteristics gives a fast start on threats and controls, each topology has its own questions, and a prepared security review pack converts a weeks-long review into a few days.

## Exercises

1. **Draw and walk.** Draw the data flow of an integration you know, mark the trust boundaries, and apply the six STRIDE prompts to each crossing. Which threat surprised you?
2. **Find the copies.** List every place a customer's email address lands as it passes through one integration, including logs, queues, and quarantine. What is the retention of each?
3. **Test object-level authorization.** For an API you offer or use, request a record that belongs to a different tenant with valid credentials of your own. What happens?
4. **Prepare the pack.** Assemble the nine items of the security review pack for a real integration. Which is hardest to produce, and why?
