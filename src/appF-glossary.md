# Glossary

Terms are defined as this book uses them. The index lists the pages where each is discussed.

**ADR**
:   Architecture decision record: context, options, decision and consequences.

**Anti-corruption layer**
:   An adapter that translates between a legacy or external model and a clean internal one, so the foreign model does not spread.

**API-led connectivity**
:   Layering APIs into system, process and experience tiers (popularized by MuleSoft).

**Authority (system of record)**
:   The system whose value wins for a given field.

**Authority matrix**
:   A table stating which system owns each field.

**Backoff with jitter**
:   Waiting longer after each failed attempt, with a random component, so that clients do not retry in synchronized waves.

**Backpressure**
:   Slowing a producer when a consumer cannot keep up.

**Bulkhead**
:   A limited, separate pool of resources per dependency, so a slow dependency cannot exhaust everything.

**Canonical model**
:   A shared definition of an entity that every system maps to and from, instead of mapping to each other directly.

**CDC**
:   Change data capture: reading a database's change log to publish row changes.

**Circuit breaker**
:   A guard that stops calling a failing dependency for a cool-down period.

**Claim check**
:   Storing a large payload elsewhere and passing a reference in the message.

**CloudEvents**
:   A specification for describing event metadata in a common way.

**Compaction**
:   Kafka retention policy that keeps the latest record per key.

**Consumer group**
:   A set of Kafka consumers that share the partitions of a topic, so that each record is processed by one member of the group.

**Consumer lag**
:   How far a consumer group is behind the end of a partition.

**Contract test**
:   A test that checks a client and an API (or a producer and a consumer) still agree on the interface.

**Control plane / runtime plane**
:   The management layer of a platform versus the engine where flows actually execute and data moves.

**Crosswalk**
:   A table mapping identifiers in one system to identifiers in another.

**Data contract**
:   A machine-readable agreement between data producer and consumers covering schema, quality, service levels and ownership.

**Data virtualization**
:   Querying across sources at read time without copying data.

**DLQ**
:   Dead letter queue: where unprocessable messages are parked with context.

**EDI / AS2 / VAN**
:   Standard business documents (X12, EDIFACT); a secure transport; and a value-added network that relays them.

**ESB**
:   Enterprise service bus: a central integration runtime that routes and transforms messages.

**Event mesh**
:   Interconnected event brokers that route events across sites and clouds.

**Four numbers**
:   Records now, records in three years, peak changes per hour, and acceptable staleness.

**Gate**
:   A decision point at the end of a project stage, passed only when stated criteria are met on named evidence.

**Golden file**
:   A stored pair of input and expected output used to test a mapping.

**HL7 / FHIR / MLLP**
:   Healthcare message standard; its REST-based resource model; and the TCP framing used for HL7 v2.

**Hypercare**
:   A defined period after go-live in which the build team stays on call while the operations team takes over.

**Idempotency key**
:   A unique value a client sends with a request so that the server can recognize a retry and return the original result instead of repeating the work.

**Idempotent**
:   An operation that has the same effect whether performed once or many times.

**iPaaS**
:   Integration platform as a service.

**ISR**
:   In-sync replicas of a partition.

**KRaft**
:   Kafka's built-in metadata consensus, replacing ZooKeeper.

**Lookup before retry**
:   Checking whether a create succeeded before retrying it, to make a non-idempotent API safe.

**MCP**
:   Model Context Protocol: a standard for exposing tools to AI agents.

**MFT**
:   Managed file transfer: secure, audited file exchange (SFTP, AS2, FTPS).

**MQTT**
:   Lightweight publish-subscribe protocol for devices.

**mTLS**
:   Mutual TLS: both client and server present certificates when the connection is established.

**OAuth 2.0 client credentials**
:   The OAuth 2.0 flow in which an application exchanges its own identity and secret for a short-lived access token; the standard choice for unattended integrations.

**Offset**
:   The position of a record within a Kafka partition; consumers commit offsets to record how far they have read.

**OpenLineage**
:   An open standard for emitting lineage events from data jobs.

**Outbox pattern**
:   Writing an event to a table in the same transaction as the state change, then publishing it reliably.

**Overlap window**
:   A safety margin by which an incremental read reaches back before the watermark, to catch late-committed rows.

**Parallel run**
:   Running old and new paths side by side and comparing outputs before switching.

**Partition**
:   An ordered, append-only log that forms part of a Kafka topic; order is guaranteed only within a partition.

**Paved road**
:   The supported, easiest way to build an integration using platform-provided templates and guardrails.

**PKCE**
:   Proof Key for Code Exchange: a protection for the OAuth 2.0 authorization code flow used by applications that act for a person.

**Problem details**
:   RFC 9457 JSON error format (application/problem+json).

**Quarantine**
:   A holding area for records that failed validation, kept with the reason and the original payload.

**Reconciliation**
:   Comparing two systems to detect and repair drift.

**Reconnaissance sheet**
:   A one-page record of an API's contract, authentication, limits, pagination, errors, and events, filled in by probing.

**Reverse ETL**
:   Pushing curated warehouse data back into operational applications.

**RPO / RTO**
:   Recovery point objective (acceptable data loss) and recovery time objective (acceptable downtime).

**Saga**
:   A business transaction split into local transactions with compensating actions.

**Schema registry**
:   A service that stores the schemas of event payloads and refuses incompatible changes.

**Shadow run**
:   Running a new path on copies of real traffic and comparing results without affecting production.

**Share group**
:   Kafka 4.x consumption model with queue-like semantics and per-record acknowledgment.

**SLI / SLO / error budget**
:   A measured indicator, its target, and the tolerated shortfall that triggers reliability work.

**SMT**
:   Single message transform in Kafka Connect.

**Strangler fig**
:   Replacing a legacy system gradually by routing more and more functionality to new services until the old system can be retired.

**STRIDE**
:   Threat categories: spoofing, tampering, repudiation, information disclosure, denial of service, elevation of privilege.

**Token bucket**
:   A rate limiter that refills tokens at a fixed rate; each request takes a token, so traffic stays within a budget.

**traceparent**
:   W3C Trace Context header carrying trace and span identifiers across services and messages.

**Upsert**
:   Insert if absent, update if present, keyed by an identifier.

**Watermark**
:   The position (timestamp or token) up to which a source has been read.

**Webhook**
:   An HTTP request that a source system sends to your endpoint when something changes.

