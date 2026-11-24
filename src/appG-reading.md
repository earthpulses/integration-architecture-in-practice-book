# Further Reading, Standards, and Sources

## Books

{{tbl readbooks | Books that deepen the topics of this one}}

| Book | Authors | Why read it |
|---|---|---|
| *Enterprise Integration Patterns* | Gregor Hohpe and Bobby Woolf | The vocabulary of messaging patterns still used by every platform |
| *Designing Data-Intensive Applications* | Martin Kleppmann | Replication, consistency, logs, and streams explained properly |
| *Kafka: The Definitive Guide* | Gwen Shapira and co-authors | Kafka internals and operations |
| *Building Event-Driven Microservices* | Adam Bellemare | Event design and stream-based architecture |
| *Release It!* | Michael Nygard | Stability patterns: timeouts, circuit breakers, bulkheads |
| *Fundamentals of Software Architecture* | Mark Richards and Neal Ford | Architecture characteristics and trade-off thinking |
| *API Design Patterns* | JJ Geewax | Designing APIs others can integrate with |
| *Site Reliability Engineering* | Google (edited by Betsy Beyer and others) | Objectives, error budgets, incident practice |
| *Team Topologies* | Matthew Skelton and Manuel Pais | Platform teams and operating models |

## Standards and Specifications Referenced

{{tbl standards2 | Standards and specifications mentioned in this book}}

| Standard | What it defines | Where it appears |
|---|---|---|
| IETF RFC 9110 | HTTP semantics: methods, status codes, headers | Chapter 1 |
| IETF RFC 9457 | Problem Details for HTTP APIs (`application/problem+json`) | Chapter 11 |
| IETF RFC 8594 | The `Sunset` HTTP header field | Chapter 11 |
| IETF Internet-Draft, Idempotency-Key | A proposed standard header for safe retries of `POST` (still a draft in the sources checked) | Chapters 1, 11 |
| IETF RFC 6749 | The OAuth 2.0 authorization framework | Chapter 13 |
| IETF RFC 7636 | Proof Key for Code Exchange (PKCE) | Chapter 13 |
| IETF RFC 7523 | JWT bearer assertion profile for OAuth 2.0 | Chapter 13 |
| W3C Trace Context | The `traceparent` and `tracestate` headers | Chapter 26 |
| CloudEvents 1.0 (CNCF) | A common envelope for event data | Chapters 11, 19 |
| OpenAPI Specification 3.1 and 3.2 | Description of HTTP APIs (3.2.0 appeared in September 2025; 3.1 descriptions remain valid) | Chapters 10, 11 |
| AsyncAPI 3.x | Description of event-driven APIs | Chapter 11 |
| OpenLineage | An open specification for run, job, and dataset lineage events | Chapters 19, 29 |
| Open Data Contract Standard (Bitol) | A YAML format for data contracts | Chapter 29 |
| OWASP API Security Top 10 (2023) | The most serious API risks (the most recent API list when checked; the web-application Top 10 was updated in 2025) | Chapter 27 |
| STRIDE | A mnemonic for six threat categories | Chapter 27 |

## Sources and Currency

The technical principles in this book are stable. Statements about products, versions, limits, and standards' current versions are time-sensitive. At the time of writing, in November 2026, the following were checked against public sources:

* **Apache Kafka.** The release announcements and upgrade notes for the 4.x line, covering the removal of ZooKeeper, the new consumer rebalance protocol, share groups, and Java requirements; and client documentation on idempotent producers.
* **OWASP.** The API Security Top 10 2023 edition was the most recent published list.
* **Open Data Contract Standard.** Version 3.2.0 (September 2026) was the latest published release; 3.1.0 appeared in December 2025.
* **MuleSoft and other platforms.** Vendor documentation on error handling, batch processing, runtime options, and the Kafka connector. Product names and licensing models change, so confirm current offerings.
* **Salesforce and NetSuite.** Vendor documentation on the Spring '26 connected-app restriction and external client apps, and on Oracle's timeline for removing SOAP web services.
* **OpenAPI and Kafka.** The OpenAPI 3.2.0 release (September 2025) and the Apache Kafka 4.2 announcement, which marks share groups production-ready.
* **Industry events.** IBM's 2024 acquisition of webMethods and StreamSets from Software AG.

Anything in these categories should be confirmed against current documentation before a client deliverable relies on it. The book's own heuristics, the decision-tree scores, the estimation constants, and the learning-path durations, are the author's judgment and are not drawn from any standard.
