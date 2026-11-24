# Preface

Every company that has more than one system has an integration problem. The sales system must tell the warehouse what to ship. The warehouse must tell the finance system what to invoice. The human-resources system must tell everything else who still works here. The data platform must learn about all of it. Each connection is small; together they decide whether a company's information is trustworthy, and they decide it in ways that executives rarely see until something goes wrong.

This book is about doing that work well. It is for the people who design, build, and run those connections, from the developer writing a first client to the architect deciding how a hundred integrations fit together. It assumes you can read code and understand what a database and a web service are. It does not assume you have built an integration before, and it will not bore you if you have, because it concentrates on the part that experience teaches slowly: *how integrations fail, and how to design so that failure is survivable*.

## Who This Book Is For

You will get the most from this book if you are one of the following:

* **A developer or analyst moving into integration**, who has called an API but not yet had to keep one running for a year.
* **An integration engineer becoming an architect**, who builds well and now has to decide what to build, with whom, and why.
* **A solution architect on enterprise projects**, who needs a repeatable method for discovery, design, and review, and a vocabulary to use with clients.
* **A technical lead or principal** shaping an integration practice, who needs standards, an operating model, and a way to measure health.
* **Someone preparing for an interview or a design review**, who wants the questions and the answers in one place.

## What You Will Learn

By the end, you will be able to run a discovery workshop and turn its answers into a signed brief. You will choose between patterns and platforms using a method that others can inspect. You will read an unfamiliar API like an architect, design your own, and write clients that survive timeouts, retries, duplicates, and rate limits. You will understand Kafka well enough to know when not to use it and how to use it correctly when you should. You will design for failure, test for it, observe it, secure against it, and recover from it. And you will be able to estimate the work and explain the design to an executive in five minutes.

## How This Book Is Organized

The book has seven parts and thirty-one chapters.

**Part I, Foundations,** builds the vocabulary: how systems talk, how HTTP works, why idempotency matters, and how an architect thinks. **Part II, Discover and Decide,** covers the journey of an integration project, the discovery questions, the places integrations run, forty-one patterns, ten sequence diagrams of the hard cases, and a method for deciding. **Part III, Design and Build,** is the practical core: reading and designing APIs, formats and mapping, authentication, Python clients, synchronization, testing, and delivery. **Part IV, Messaging and Streaming,** covers Kafka from first principles to production, the many ways to connect to it, the interfaces beyond REST, and the large SaaS platforms. **Part V, Platforms and Practice,** surveys integration platforms, presents nine case studies, and follows one project from the first meeting to the first incident. **Part VI, Operate, Secure, Govern,** covers reliability and observability, security and threat modeling, recovery and estimation, governance, and troubleshooting. **Part VII, Growing as an Architect,** gives a learning path and a way to prove your skill.

Seven appendices follow: the full discovery question bank, interview and knowledge-check questions with model answers, workshop scenario cards, templates, the companion code, a glossary, and further reading.

You do not have to read straight through. Parts I and II are best read in order. Parts III to V can be read by need. Part VI belongs before your first go-live, and Part VII after a few months of practice.

## A Running Example

Most chapters return to **Larkspur Outdoor**, a fictional company that sells camping gear online and needs its web shop connected to its ERP. The example gives the book continuity: you meet the company's problem in the first chapter, answer its discovery questions in the fourth, see its design decisions at points along the way, and follow its project to production in Chapter {{ref ch:capstone}}. Larkspur and the other organizations in the case studies are composites. No real company or person is described.

## Conventions Used in This Book

The following typographical conventions are used:

*Italic* indicates new terms, emphasis, and the titles of books. `Constant width` indicates code, commands, file names, and parameters. Shaded boxes carry additional material: a *Why this matters* box explains the reasoning behind a practice, a *Warning* box flags a common failure, a *Tip* box offers a shortcut, an *Example* box returns to the running example, and an *In this chapter* box opens each chapter with its learning goals.

Diagrams use a consistent visual language, described in Chapter {{ref ch:patterns1}}: solid arrows wait for an answer, dashed arrows do not, numbered circles give the order of steps, and lettered red circles mark where a design usually fails.

## Using the Code Examples

The companion code is a set of small, tested Python modules: a local lab API server, a hardened HTTP client, a token provider, an incremental poller, a webhook verifier, an outbox, a rate limiter, a run loop with quarantine, a reconciliation module, an OpenAPI analyzer, and a mapping module with its tests. Appendix {{ref app:codelab}} lists them. The code is distributed with the book as a zip archive and is licensed under the MIT License.

Listings marked as sketches, such as the Kafka producer and consumer, the Testcontainers test, the OpenTelemetry example, and the platform flow, are illustrative and need external services to run; they are not part of the automated tests. Product names, product features, limits, and prices change often. Where the book states a fact about a vendor's product, it is a fact as of the writing date, and you should confirm it against current documentation before you rely on it.

## How to Contact the Author

Comments, questions, and corrections are welcome and will be considered for later editions of this book.

## A Note on Authorship

This book was produced with the help of an AI assistant, under the author's direction. The section that follows, "How This Book Was Made," says what the AI did, what the author did, and how the result was checked. Please read it before you rely on any statement about a product or a version.
