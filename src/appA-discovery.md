# The Discovery Question Bank

This appendix contains 125 questions for the discovery phase (Chapter {{ref ch:discovery}}), grouped by the stakeholder who can answer them. Questions marked **C** are *critical*: an unfavorable or missing answer changes the architecture, so they must be answered, or placed on the risk register with an owner and a date, before the design gate (Chapter {{ref ch:journey}}). Every question lists its **design consequence**, which says why you are asking and what the answer changes.

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
| **C** | 80 | Where do the source, target and integration runtime live (on-premises, which cloud and region, SaaS)? | Selects the topology (Chapter {{ref ch:topologies}}). |
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
