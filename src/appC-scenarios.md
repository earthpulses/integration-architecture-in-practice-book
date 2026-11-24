# Workshop Scenario Cards

Ten realistic situations, described in technology-neutral terms. For each, cover the design and discuss what you would do; then compare. Use them as exercises in a study group, as workshop material for a team, or as templates for describing your own client scenarios. Each card gives the context, the constraints, a recommended design with its reasoning, and the traps. They are composites, not accounts of real engagements.

## Scenario 1: Ticket Synchronization Between a Service Desk and a Governance Tool

**Context.** A bank tracks data-quality problems as issues in a governance tool and as incidents in its service-desk platform. Stewards want one lifecycle across both.

**Constraints.** Both teams edit; comments must flow both ways; the service desk has strict rate limits; the integration host can only call out.

**Design.** A polling integration every two to five minutes, with a configuration document in the governance tool holding status aliases and mappings for each direction. Per-field authority: incident state belongs to the service desk, issue description to the governance tool, and comments are append-only with an origin tag. A stored foreign ID on the issue, never name matching after the first link. Echo-loop prevention by ignoring the integration's own user, and locks with lease expiry for parallel workers. The incident is created only when the issue reaches an agreed status, to avoid noise.

**Why.** Per-field authority turns one bidirectional merge into mostly one-way flows (Chapter {{ref ch:patterns2}}).

**Traps.** Renaming an issue duplicates it if matching is by name; unmapped statuses skip silently; time-zone assumptions in change ordering; lock timeouts shorter than a slow API call.

**Ask the client.** Which statuses exist on both sides? Who may close? What happens when a ticket is reopened in the service desk after the issue closed in the governance tool?

## Scenario 2: ERP Master Data, Nightly Bulk

**Context.** A manufacturer wants material and supplier master data described in a catalog. The ERP team will not allow API access during business hours but can produce nightly extracts.

**Design.** A scheduled file delivery to a landing area, with a manifest of row counts and checksums, and a loader that validates, transforms, and upserts through a bulk import. A full snapshot each night, because reference data is small, with delete detection by ID-list comparison and a 20 percent safety threshold.

**Why.** Files respect the ERP team's constraints, leave an audit trail, and make reruns trivial; a snapshot makes drift self-healing.

**Traps.** Encoding of special characters in names; leading zeros lost in material numbers (treat as text); duplicate keys across plants; files that arrive late or twice.

## Scenario 3: CRM Change Events into a Data Platform

**Context.** A retailer wants customer changes from its CRM in analytics within a minute, and available to three other teams without each integrating separately.

**Design.** A change-event stream (or CDC) into Kafka keyed by customer ID; event-carried state with a version field; a compacted state topic and a retained event topic; a sink connector to the warehouse with upsert; a schema registry with backward-transitive compatibility; personal fields tokenized before publication.

**Why.** Fan-out and replay justify Kafka; keyed ordering keeps per-customer updates coherent; the state topic gives a new consumer an immediate bootstrap.

**Traps.** Customer merges and unmerges (the key changes); hot keys for large business accounts; deletion requests (tombstones and crypto-shredding); the CRM's API limits for a backfill.

## Scenario 4: A Legacy Partner with SOAP and SFTP

**Context.** An insurer exchanges claims data with a partner that supports only a SOAP service for status lookups and an SFTP drop for daily claim files.

**Design.** A thin adapter that wraps the SOAP calls behind a clean REST interface for internal consumers, and an SFTP poller with trigger-file semantics, a checksum ledger, and schema validation. Every file and SOAP exchange is stored raw for audit.

**Why.** You cannot change the partner, so contain the awkwardness. The facade gives the enterprise a stable contract and a place to enforce retries and observability.

**Traps.** Expiring WS-Security certificates; XML namespaces that change without notice; the partner's business-hours-only availability; large files that time out mid-transfer (require resume support).

## Scenario 5: A Product Information System Behind a Customer Firewall

**Context.** A retailer's cloud product information system holds logical attributes and physical columns. Governance wants them in a catalog as a logical model linked to physical columns.

**Design.** An integration on a customer-network server, outbound only: call the product system's APIs, map entities and fields into the catalog's logical model with properties (mandatory flag, position) as attributes, import physical tables and columns, and link logical to physical. Quality, matching, and survivorship rules are deferred and clearly marked out of scope.

**Why.** A clear logical-to-physical hierarchy gives stewards immediate value; deferring rule synchronization avoids sprawl.

**Traps.** Multi-valued fields with child fields need a grouping relation; properties that fit no standard attribute type need custom types; descriptions edited in the catalog drift from the source.

## Scenario 6: Pushing Governance Metadata into a BI Tool

**Context.** Stewards certify data sources and add tags in the catalog. Analysts want to see certification, warnings, and contacts inside the BI tool.

**Design.** A workflow-triggered push: when a tracked attribute or tag changes, a workflow creates a task; the integration polls tasks, looks up the BI tool's identifier for the entity, and calls the BI tool's REST API. A contact rule: the steward overrides the owner.

**Why.** Stewards act in one place and changes propagate under governance; the workflow supplies an audit trail and a natural throttle.

**Traps.** The lookup of external IDs depends on lineage stitching between the catalog and the BI model, and unstitched assets cannot be updated; usernames must exist in the BI tool; tag removal must be handled, not only addition.

## Scenario 7: Merging Three HR Systems into One Identity Source

**Context.** After acquisitions, a company has three HR systems with overlapping employees and different ID schemes. Roles and access depend on a single trusted identity list.

**Design.** An authority matrix per attribute (legal name from system A, department from system B, and so on); a canonical employee ID in a crosswalk table; nightly full extracts from each system, matched through the crosswalk and published to the identity provider (SCIM) and to downstream tools.

**Why.** Clean authority splits remove conflict resolution, and the crosswalk is the durable asset.

**Traps.** Rehires with new IDs; name collisions; leavers who must be deprovisioned quickly (feed events, or a daily full comparison); privacy of HR attributes.

## Scenario 8: Lineage Across a Kafka-Based Data Platform

**Context.** Operational applications stream through Kafka into a cloud warehouse and BI. Auditors need column-level lineage from source application fields to dashboards.

**Design.** Crawl topics and schema subjects as static assets; run an extractor that joins Kafka Connect configurations with registry schemas and emits OpenLineage events with column lineage; take warehouse and BI lineage from their standard connectors, and stitch the three.

**Traps.** Single message transforms that rename fields; topics produced by custom code have no configuration to parse, so those producers should emit lineage themselves; stream processors need their own lineage capture.

## Scenario 9: An API Inventory from OpenAPI Specifications

**Context.** A company has hundreds of APIs and no catalog showing which endpoint returns which data structures.

**Design.** A pipeline that reads OpenAPI specifications from a repository, converts paths, response codes, component schemas, and properties into catalog assets (API, endpoint, code value, data structure, data element), and upserts them, with relations for composition and one that flags unused structures. Run it on every merge to the specification repository.

**Traps.** Specifications with inline anonymous schemas; polymorphism (`oneOf`, `anyOf`) mapping; a hierarchy view that must be configured once per domain; and, above all, specification quality, which is the real limit.

## Scenario 10: A Process Tool and a Catalog with a Clean Authority Split

**Context.** A process-modeling tool documents business processes, sub-processes (one to three levels), and activities. A catalog is the single source of truth for business objects. The business wants each activity to show which data concepts it uses, and each concept to show which activities touch it.

**Design.** *Authority split:* the process tool owns process structure and documentation; the catalog owns business objects; no co-owned fields, so no conflict resolution and no chronological merge. *Model:* one asset type for all process levels, with a level attribute and a decomposition relation, which is simpler than a type per level. *Identity:* the process tool has an entity ID (the stable identity of the object) and occurrence IDs (each appearance in a diagram); always key on the entity ID. Explain it to non-technical stakeholders as a passport versus a photograph: one identity, many pictures. *Direction:* catalog to process tool for business objects, process tool to catalog for structure and usage links.

**Traps.** Keying on occurrence IDs creates duplicates per diagram; deep hierarchies make traversals expensive (consider a derived relation that skips hops); some relation types may already exist, so check before creating.
