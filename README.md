# Integration Architecture in Practice

**Designing, Building, and Running Enterprise Integrations from REST to Kafka**

*Stefan Živanović · Solution Architect · Prague · First Edition, November 2026*

> **AI disclosure.** This book was generated with AI assistance (Claude, by Anthropic), under the author's direction. The text, diagrams, index, cover, and companion code were produced with an AI assistant. The section "How This Book Was Made" inside the book explains what the AI did, what the author did, and how the result was checked.

📘 **Read the book:** [`book/integration-architecture-in-practice.pdf`](book/integration-architecture-in-practice.pdf) (501 pages, PDF/A-2b)

---

## What this is

A practical, end-to-end guide to enterprise integration: connecting the systems a company runs (ERP, CRM, service desks, HR, data platforms, SaaS products, partners) so that data moves between them correctly, on time, and safely, and keeps doing so after go-live.

It covers the whole life of an integration: the first discovery workshop, choosing a pattern and a platform, designing and building the interfaces, testing for failure, shipping, operating, securing, recovering, and governing a growing estate of integrations. The examples use REST APIs, webhooks, files, Kafka, and the large SaaS platforms, and a fictional company, **Larkspur Outdoor**, runs through the book from its first problem to its first production incident.

The book concentrates on the part that experience usually teaches slowly: **how integrations fail, and how to design so that failure is survivable.**

## What it helps you solve

| If you are dealing with... | The book gives you... | Where |
|---|---|---|
| Vague requirements ("just connect the systems") | Seven discovery dimensions, the "four numbers", an authority matrix, a one-page integration brief, and 125 discovery questions with the design consequence of each | Ch. 4, App. A |
| Surprises late in a project (firewalls, security reviews, API limits) | A stage-gate journey with evidence per gate, and a network checklist for week one | Ch. 3, 5 |
| Choosing between webhooks, polling, CDC, queues, Kafka, files | 41 patterns with diagrams, seven decision trees, and a scorecard method | Ch. 6, 7, 9 |
| Duplicates, lost records, and retries that make things worse | Idempotency, watermarks, outboxes, retries with jitter, circuit breakers, and ten failure sequences traced step by step | Ch. 1, 8, 14 |
| Two systems drifting apart or overwriting each other | Identity matching, delete detection, bidirectional sync without echo loops, and reconciliation | Ch. 15 |
| Unfamiliar or badly documented vendor APIs | A ten-step reading method, a reconnaissance sheet, probes, and an OpenAPI analyzer | Ch. 10 |
| Designing APIs, webhooks, and events others can integrate with | Design rules, RFC 9457 errors, contract-first OpenAPI and AsyncAPI | Ch. 11 |
| Money, time zones, encodings, and nulls corrupting data | Seven value traps, a transformation pipeline with quarantine, typed validation, and golden-file tests | Ch. 12 |
| Authentication, service accounts, and secrets | OAuth 2.0 flows, a correct token provider, webhook signatures, and secret management | Ch. 13 |
| Testing beyond the happy path, and shipping safely | A twelve-row failure-injection matrix, contract tests, pipelines, and release strategies for queue consumers | Ch. 16, 17 |
| Whether and how to use Kafka | When Kafka is (and is not) worth it, producer and consumer settings, Connect and CDC, schemas, and twelve ways in and eleven ways out | Ch. 18–20 |
| Salesforce, SAP, ServiceNow, Workday, Microsoft, NetSuite | Interfaces, change detection, keys, limits, authentication, and traps per platform | Ch. 22 |
| Choosing an integration platform | A landscape of twelve categories, how platforms work, and a weighted selection method | Ch. 23 |
| Running integrations in production | Service-level indicators, alerts, tracing across queues, runbooks, and a troubleshooting method | Ch. 26, 30 |
| Security reviews | Trust boundaries, STRIDE, the OWASP API Top 10 for integrations, and a review pack | Ch. 27 |
| Estimates, cutover plans, and disaster recovery | Recovery tiers, five cutover strategies, capacity arithmetic, and an estimation method with ranges | Ch. 28 |
| Integration sprawl across a company | Operating models, intake, standards, inventory, data contracts, and lineage | Ch. 29 |
| Growing into the role, or hiring for it | A five-level learning path and 153 interview questions with model answers | Ch. 31, App. B |

## Who it is for

- **Developers and analysts moving into integration work**, who have called an API but not yet kept one running for a year.
- **Integration engineers becoming architects**, who build well and now have to decide what to build, with whom, and why.
- **Solution architects on enterprise projects**, who need a repeatable method for discovery, design, and review.
- **Technical leads and principals** shaping an integration practice.
- **Anyone preparing for an interview, a design review, or a client workshop.**

You need to be able to read code and to know what a database and a web service are. You do not need to have built an integration before.

## What's inside

**Part I · Foundations**
1. What Integration Really Is · 2. The Architect's Mindset

**Part II · Discover and Decide**
3. The Integration Journey · 4. Discovery: Asking the Right Questions · 5. Where Integrations Run · 6. Patterns for Requests and Data Movement · 7. Patterns for Messages, Routing, and Authority · 8. Behavior in Time: The Hard Cases · 9. Making the Decision

**Part III · Design and Build**
10. Reading API Documentation Like an Architect · 11. Designing APIs, Webhooks, and Events · 12. Data Formats, Mapping, and Transformation · 13. Authentication and Authorization · 14. Python Clients That Survive Production · 15. Synchronization Design · 16. Testing Integrations · 17. Delivery: Pipelines, Configuration, and Environments

**Part IV · Messaging and Streaming**
18. Kafka Fundamentals · 19. Kafka in Production · 20. Kafka as an Integration Backbone · 21. Beyond REST and Kafka · 22. Integrating Enterprise SaaS Platforms

**Part V · Platforms and Practice**
23. Integration Platforms · 24. Case Studies · 25. Capstone: Larkspur Outdoor

**Part VI · Operate, Secure, Govern**
26. Reliability and Observability · 27. Security and Threat Modeling · 28. Recovery, Cutover, Capacity, and Estimation · 29. Governance and the Operating Model · 30. A Troubleshooting Field Guide

**Part VII · Growing as an Architect**
31. Becoming an Integration Architect

**Appendices**
A. The Discovery Question Bank (125 questions) · B. Interview and Knowledge-Check Questions (153) · C. Workshop Scenario Cards (10) · D. Templates · E. Companion Code · F. Glossary · G. Further Reading, Standards, and Sources

Every chapter opens with learning goals and ends with a summary and exercises. The book contains 130 diagrams, 102 numbered tables, lists of figures and tables, a glossary, and an index.

## How to use the book

You do not have to read it cover to cover. Pick the path that matches what you are doing now.

| Your situation | Read | Then |
|---|---|---|
| **New to integration** | Ch. 1, 2, 6, 7, 8 | Run the lab in [`code/`](code/) and work through Ch. 14 |
| **Starting a project next week** | Ch. 3, 4, 5, 9, 10 | Use App. A for the workshop and App. D for the brief, then follow the capstone in Ch. 25 |
| **An integration is failing in production** | Ch. 30 (five-question method) | Follow its pointers to Ch. 8, 15, 19, and 26 |
| **Deciding whether to use Kafka** | Ch. 18, then 19 and 20 | Use the Kafka decision trees in Ch. 9 |
| **Choosing a platform or vendor** | Ch. 23 and 9 | Run a proof of concept with the failure-injection matrix in Ch. 16 |
| **Preparing a design or security review** | The checklist in Ch. 2, the review pack in Ch. 27 | Check the design against the failure matrix in Ch. 16 |
| **Integrating a specific SaaS platform** | Ch. 22 and 10 | Fill in the reconnaissance sheet for that platform |
| **Running a client workshop or team training** | App. C scenario cards, App. A questions, the agenda in Ch. 4 | Use the exercises at the end of each chapter |
| **Preparing for an interview, or hiring** | App. B and Ch. 31 | Answer the questions aloud before reading the model answers |

**Tips**
- Parts I and II are best read in order; Parts III to V can be read as needed; read Part VI before your first go-live.
- The diagrams share one visual language (explained in Ch. 6): solid arrows wait for an answer, dashed arrows do not, numbered circles give the order of steps, and lettered red circles mark where a design usually fails.
- The templates in App. D (brief, design outline, test plan, go-live checklist, threat model, runbook, post-incident review) can be copied straight into a project.
- `book/integration-architecture-in-practice.md` is a plain-text copy of the whole manuscript, useful for searching. Figures appear there as captions only, so use the PDF to read.

## Companion code

[`code/`](code/) holds small, tested Python modules used throughout the book: a local lab API that can be made slow, rate-limited, or unreliable on purpose; a hardened HTTP client; an OAuth 2.0 token provider; a watermark poller; a webhook verifier; an outbox; a rate limiter; a run loop with quarantine; a reconciliation module; an OpenAPI analyzer; and a mapping module. Appendix E lists them and says where each is discussed.

```bash
cd code
python3 -m venv .venv && source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python3 -m pytest -q test_all.py test_more.py           # 18 tests, a few seconds, no external services

# Start the lab API (Chapter 1). Without --no-auth it requires an OAuth token.
python3 labserver.py --port 8080 --no-auth
curl -s "http://127.0.0.1:8080/orders?limit=2"

# Make it misbehave: rate-limited and randomly failing
python3 labserver.py --port 8080 --no-auth --rate-limit 3 --flaky 0.3

# With authentication: get a token first (client larkspur-client / s3cret)
python3 labserver.py --port 8080
curl -s -X POST http://127.0.0.1:8080/oauth/token \
  -d grant_type=client_credentials -d client_id=larkspur-client -d client_secret=s3cret

# Analyze any OpenAPI 3.x JSON document (Chapter 10)
python3 openapi_recon.py path/to/openapi.json
```

Requires Python 3.9 or later. Listings in the book marked as *sketches* (Kafka producer and consumer, Testcontainers, OpenTelemetry, the MuleSoft flow) need external services and are not part of this test suite.

## Repository layout

```text
book/                 the finished book: PDF, Markdown copy, cover (PDF and PNG)
code/                 companion code, tests, LICENSE (MIT)
src/                  manuscript sources: one Markdown file per chapter and appendix,
                      manifest.yaml (order and titles), index_terms.txt (index)
assets/figs/          the 130 diagrams as SVG
assets/fonts/         embedded fonts (Source Serif 4, Source Sans 3, Source Code Pro)
build_book.py         typesetting pipeline: Markdown -> HTML -> PDF (WeasyPrint)
book.css              page layout and typography
book_meta.yaml        author, edition, publisher, ISBN, and AI statement used on the title pages
registry.json         diagram registry (sizes, captions, failure notes)
lint_refs.py          checks every figure, table, chapter, and code reference
make_cover.py         renders the cover
make_md.py            builds the single-file Markdown copy
```

## Building the book from source

The PDF in `book/` is the released version; you only need this if you want to change something.

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-build.txt     # WeasyPrint also needs Pango; see its install guide

python3 lint_refs.py       # checks references before building
python3 build_book.py      # writes out/book.pdf (about a minute; two passes for page numbers)
python3 make_cover.py      # writes out/cover.pdf, out/cover.png
python3 make_md.py         # writes out/integration-architecture-in-practice.md
```

The build was tested with Python 3.12 and WeasyPrint 70. Publication details (edition date, publisher, ISBN, contact) live in `book_meta.yaml`; empty values are left out of the copyright page. Macros used in the manuscript, such as `{{fig key | caption}}`, `{{tbl key | caption}}`, `{{ref ch:slug}}`, and `{{code file}}`, are documented at the top of `build_book.py`.

## Accuracy and currency

- Statements about products, versions, limits, and standards were checked against public sources in November 2026 where the text says so. Vendors change things often; confirm against current documentation before you rely on a statement for contracts, security reviews, or compliance.
- The case studies and Larkspur Outdoor are fictional composites; no real company or person is described.
- The book has not had a professional copyedit or an independent technical review.

## Feedback and errata

Corrections, questions, and suggestions are welcome through this repository's **Issues**. Please include the page or section and, for technical points, a source.

## License

- **Book** (text, figures, cover, PDF, and Markdown copy): © 2026 Stefan Živanović. All rights reserved. You are welcome to read the book and download it for personal use. Redistribution, modification, or commercial use, beyond brief quotations with attribution, requires written permission from the author. See [`LICENSE.md`](LICENSE.md).
- **Companion code** in [`code/`](code/): MIT License, see [`code/LICENSE`](code/LICENSE).
- The fonts in `assets/fonts/` are licensed under the SIL Open Font License by their authors.

## Citation

```bibtex
@book{zivanovic2026integration,
  author    = {Stefan Živanović},
  title     = {Integration Architecture in Practice: Designing, Building, and Running Enterprise Integrations from REST to Kafka},
  edition   = {First},
  year      = {2026},
  address   = {Prague},
  note      = {Generated with AI assistance (Claude, Anthropic) under the author's direction}
}
```
