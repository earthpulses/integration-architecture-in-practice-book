# Integration Platforms

Most large enterprises run several integration technologies at once. There is a message broker from the 2000s, an enterprise service bus from the 2010s, an integration platform as a service from the late 2010s, cloud-native services from the 2020s, and a layer of scripts nobody remembers writing. Each was the right choice when it was bought, and each is still doing real work. An architect arriving in such an estate does not choose from a blank sheet; they navigate a landscape, decide what to add and what to retire, and have to explain the choice to people who own the old systems and people who want the new ones.

This chapter maps that landscape, takes one widely used platform, MuleSoft's Anypoint, apart in enough detail to read any similar product's documentation, surveys the others, and ends with a method for choosing. Throughout, remember the principle of Chapter {{ref ch:decide}}: choose the platform to *carry* the pattern, not to dictate it.

!!! goals "In this chapter"
    * Place integration technologies in twelve categories, and recognize who typically owns each
    * Explain the control-plane and runtime-plane architecture of an integration platform and the runtime hosting options
    * Describe the building blocks that every platform renames: flows, connectors, transformation language, state, queues, batch, policies
    * Use error-handling semantics, such as MuleSoft's continue versus propagate, to avoid silent data loss
    * Compare Boomi, Workato, hyperscaler stacks, and enterprise technologies you may inherit
    * Choose a platform with a weighted scorecard, a proof of concept with failure injection, and a three-year cost view

## The Landscape in One Table

{{tbl landscape | Twelve categories of integration technology}}

| Category | What it does | Names you will meet | Typical owner |
|---|---|---|---|
| iPaaS (integration platform as a service) | Low-code flows, connectors, API management, monitoring, often hybrid runtimes | MuleSoft Anypoint, Boomi, Workato, SnapLogic, Informatica, Celigo, Jitterbit, Tray.ai, Oracle Integration, SAP Integration Suite, IBM App Connect, Microsoft Azure Integration Services | Central IT or an integration center of excellence |
| ESB and enterprise messaging | Routing, transformation, and guaranteed delivery in the data center | IBM MQ and App Connect Enterprise, TIBCO BusinessWorks and EMS, webMethods, Oracle SOA Suite, WSO2, Apache ServiceMix | Core banking, insurance, telecom, government |
| API management | Gateways, developer portals, policies, analytics | Apigee, Kong, Azure API Management, AWS API Gateway, MuleSoft API Manager, Axway, WSO2, Tyk | Platform or API teams |
| Event brokers and streaming | Asynchronous messaging and logs | Kafka (and managed offerings), Pulsar, RabbitMQ, Solace, NATS, Event Hubs, Pub/Sub, Kinesis | Platform engineering, data teams |
| Cloud-native integration services | Building blocks for serverless integration | EventBridge, Step Functions, SQS and SNS, AppFlow; Logic Apps, Service Bus, Event Grid, Functions; Pub/Sub, Workflows, Eventarc | Cloud center of excellence |
| ELT, CDC, and replication | Bulk and incremental data movement into analytics platforms | Fivetran, Airbyte, Matillion, Qlik Replicate, Oracle GoldenGate, Striim, Debezium, AWS DMS | Data engineering |
| Virtualization and reverse ETL | Query across sources; push warehouse data back to applications | Denodo, Trino and Starburst, Dremio; Hightouch, Census | Data and analytics teams |
| Managed file transfer and B2B | Partner exchange, secure files, standard documents | Axway, IBM Sterling, GoAnywhere, Cleo, OpenText, SPS Commerce | Supply chain, finance operations |
| Orchestration and workflow | Durable business processes and data pipelines | Camunda, Temporal, Airflow, Dagster, Prefect, Step Functions, Logic Apps | Process or data engineering |
| Code-first frameworks | Integration libraries for developers | Apache Camel, Spring Integration, Spring Cloud Stream, Quarkus, Apache NiFi | Engineering teams with JVM skills |
| Citizen automation | Business-user workflows | Power Automate, Zapier, Make, n8n | Business units, often ungoverned |
| Domain engines | Healthcare, industrial, and financial standards | Rhapsody, Mirth Connect, InterSystems (HL7, FHIR); HiveMQ, EMQX (MQTT); SWIFT and ISO 20022 gateways | Hospitals, manufacturers, banks |

The market is crowded and changes constantly: vendors are acquired (IBM acquired webMethods and StreamSets from Software AG in 2024, for instance), merge product lines, and reposition. Analyst reports can help you make a long list, but vendor rankings change every year, and no report knows your skills, your estate, or your budget. Treat analysts as one input and run your own proof of concept.

## MuleSoft Anypoint Platform, in Depth

MuleSoft, a Salesforce company, combines an integration runtime (Mule), API management, and design and governance tooling in its Anypoint Platform, and popularized the API-led approach of Chapter {{ref ch:patterns1}}. It is common in large enterprises and in Salesforce-centered estates, and a good representative of the category: if you understand its architecture, you can read any competitor's documentation.

### Architecture: Two Planes

{{ref fig:platform-anypoint-control-and-runtime-planes}} shows the central idea of most modern integration platforms: a split between a *control plane* and a *runtime plane*.

{{fig platform-anypoint-control-and-runtime-planes | The control plane manages and monitors; the runtime plane executes flows and carries your data. You can host the runtime plane yourself even when the vendor hosts the control plane.}}

The **control plane** is where you design, deploy, monitor, and govern. It is normally hosted by the vendor. The **runtime plane** is where flows execute and *your data* passes through. The importance of the split is that the two can be in different places. A company can use the vendor's cloud for design and monitoring while running the runtime in its own data center or cloud account, so that business data never leaves its network. That is the answer to most data-residency objections, and the question to ask of *any* platform: where does my data flow, and where does the logic execute?

{{tbl runtimes | Runtime hosting options for an integration platform (MuleSoft terms)}}

| Option | What it is | Choose it when | Think about |
|---|---|---|---|
| CloudHub | Vendor-managed, worker-based hosting (the older model) | Existing estates already on it | Being superseded by the newer container-based service |
| CloudHub 2.0 | Vendor-managed, container-based hosting with private spaces | Systems reachable from the cloud; minimum operations | Private connectivity to on-premises needs a VPN or similar; data lives in the vendor's cloud region |
| Runtime Fabric | The runtime on your own Kubernetes (cloud or on premises), managed from the control plane | Data residency; existing Kubernetes; hybrid | You own cluster operations and capacity |
| Standalone (hybrid) | The runtime on your servers or virtual machines | Traditional data-center estates | Patching, clustering, and high availability are yours |

Licensing is usually by compute capacity (such as virtual cores) or by number of flows, which makes sizing a commercial as well as a technical decision. These option names and models change; confirm the current offerings with the vendor.

Runtime versions also follow a published cadence, with *Edge* and *Long-Term Support* release channels and defined support windows. On the managed runtimes, an application still running a version that has reached end of life can be force-upgraded, so version support belongs in the operational plan and not only in the contract.

### API-Led Connectivity in Platform Terms

{{ref fig:platform-api-led-connectivity-layers}} shows the three layers.

{{fig platform-api-led-connectivity-layers | System APIs unlock a back end once; process APIs encode business logic; experience APIs adapt data to each channel.}}

It works well when many consumers will reuse the same system APIs, when teams are organized around the layers and a central platform team exists, and when governance (policies, service levels, discovery in a catalog) is valued. It hurts when the estate has three systems, because the layers add latency and meetings; when process APIs become a dumping ground for business logic that nobody owns; and when every call chains through three network hops.

### Building Blocks You Should Recognize

Every platform renames the same ideas. Learn them in one platform and you can translate to any other.

{{tbl blocks | Building blocks of an integration platform, and their equivalents}}

| Concept | What it is | Equivalent elsewhere |
|---|---|---|
| Flow and sub-flow | A unit of processing started by a source (an HTTP listener, a scheduler, a message listener) | A recipe (Workato), a process (Boomi), a pipeline (SnapLogic) |
| Connector | A packaged client for a system (HTTP, Salesforce, SAP, database, Kafka, files) | A connector or snap |
| Transformation language | The expression language for mapping, filtering, and reshaping data (DataWeave in MuleSoft) | XSLT, JSONata, Jolt, visual maps |
| Object store | Key-value persistence for state such as watermarks and deduplication keys | A cache or document properties; lookup tables; a database table |
| Queues | Managed cloud messaging, or in-memory queues between flows of one application | SQS, Service Bus |
| Batch job | Record-level processing in steps, with failure thresholds | An ETL job |
| Policy | Declarative API protection at a gateway: client-ID enforcement, rate limits, token validation | Gateway policies elsewhere |
| Exchange or catalog | A catalog of reusable assets, API specifications, and templates | An internal developer portal |

### Error Handling: The Part That Decides Reliability

Of everything in an integration platform, the semantics of error handling deserve the most attention, because they decide whether failures are visible. In Mule 4, an error is routed to the first matching handler, and there are two handler types whose difference is the single most important thing to know.

{{tbl errhandlers | Two error handlers with opposite consequences}}

| Handler | What happens | Transactions | The caller sees | Use for |
|---|---|---|---|---|
| `on-error-continue` | Runs the handler, then treats the owner (the flow or scope) as though it had succeeded | Committed | Success | Bad records you quarantine; recoverable conditions |
| `on-error-propagate` | Runs the handler, then rethrows the error to the parent | Rolled back | Failure | Transient failures that must retry or alert; anything you must not hide |

A catch-all `on-error-continue` of type `ANY` at flow level makes *every* failure look like success, both to the caller and to monitoring. The run summary says "OK" while records vanish. Reserve *continue* for errors you have deliberately dealt with, and let everything else propagate. The same lesson applies to every platform: find out what the default error behavior is, and what makes a failure visible to the scheduler and to monitoring.

Other platform defaults to check: a **batch job** in Mule by default stops at the first failed record (a threshold of zero); you can set a positive tolerance, or -1 to continue regardless, and inspect failed records in a completion phase to route them to quarantine. Use **reconnection strategies** for connectivity problems and an **until-successful** scope for operation retries, with a cap, and never retry non-idempotent writes without an idempotency key. For deduplication, use an idempotent validator backed by the object store, or natural idempotency through upserts.

### An Illustrative Flow

The following sketch shows the shape of a flow that polls a CRM every five minutes, keeping its watermark in the object store, and transforms the result. It is illustrative, not a tested listing, and attribute names vary by version; its purpose is to show that the *same pattern* of Chapter {{ref ch:python}} appears in platform form.

```xml
<flow name="sync-customers-flow">
  <scheduler>
    <scheduling-strategy>
      <fixed-frequency frequency="5" timeUnit="MINUTES"/>
    </scheduling-strategy>
  </scheduler>
  <!-- the object store holds the watermark between runs -->
  <os:retrieve key="customers.watermark" objectStore="wmStore" target="since">
    <os:default-value>#["1970-01-01T00:00:00Z"]</os:default-value>
  </os:retrieve>
  <http:request method="GET" config-ref="CRM_HTTP" path="/customers">
    <http:query-params>
      #[{ modified_since: vars.since, limit: 500 }]
    </http:query-params>
  </http:request>
  <ee:transform>
    <ee:message><ee:set-payload><![CDATA[%dw 2.0
output application/json
---
payload.results map (c) -> {
  externalId: c.id,
  name: trim((c.firstName default "") ++ " " ++ (c.lastName default "")),
  email: lower(c.email default ""),
  modified: c.modified
}]]></ee:set-payload></ee:message>
  </ee:transform>
</flow>
```

Read it against the Python poller: a scheduler (the tick), a stored watermark (the checkpoint), an HTTP request with `modified_since` (the incremental read), and a transformation (the mapping). The platform removes the plumbing and keeps the design decisions: overlap, idempotent upsert, and advancing the watermark only after success all still have to be built.

## Boomi

Boomi is a widely deployed iPaaS whose architecture emphasizes a distributed runtime. {{ref fig:platform-boomi-runtime-shapes}} shows how it separates a cloud control plane from runtimes that sit where the customer wants.

{{fig platform-boomi-runtime-shapes | A cloud control plane separated from a distributed runtime. The runtime sits where the customer wants it: a single-tenant node, a cluster, or the vendor's cloud.}}

The runtime comes in shapes that differ in resilience and location: a *basic runtime* on a single node, a *runtime cluster* for high availability and scale, and a *cloud runtime* that is multi-tenant and hosted by the vendor. Flows (called processes) are built visually, with a large connector library and strong support for B2B and master data. As with any such platform, ask where the logic executes, how deployments are versioned and promoted, and how errors are made visible.

## Workato and Business-Led Automation Platforms

Workato represents a category aimed at business-led delivery: low-code "recipes" that connect applications through triggers and actions, with a vast connector library and, in its on-premises agent, an outbound connection that needs no inbound firewall rules. Such platforms are fast to deliver and popular with business technology teams. Their characteristic risks are *task-based pricing* that grows with volume, flows built by people without engineering practices (no tests, no version control), and unclear boundaries between what runs locally and what runs in the vendor's cloud. Check each against your requirements, and bring such tools inside the governance framework of Chapter {{ref ch:governance}} rather than leaving them as shadow integration.

## The Hyperscaler Stacks

Each major cloud offers integration building blocks that can replace or supplement a commercial platform. On **AWS**: EventBridge for event routing, SQS and SNS for queues and topics, Step Functions for orchestration, AppFlow for SaaS data flows, Glue and DMS for data pipelines, and Lambda for compute. On **Azure**: Logic Apps and Power Automate for workflows, Service Bus and Event Grid for messaging, Functions, API Management, and Data Factory. On **Google Cloud**: Pub/Sub, Workflows, Application Integration, Eventarc, Dataflow, and Datastream. The translation table in Chapter {{ref ch:topologies}} maps them to each other.

The trade-off against an iPaaS is the familiar one. Cloud-native services give you fine control, low per-unit cost, and tight integration with the cloud, at the price of assembling and operating many parts, and of skills that a business-led team may not have. They suit estates with engineering capacity, where flows are code and delivered by pipelines, and where the integrations stay within one cloud.

## Enterprise Technologies You May Inherit

You will meet technologies that are not fashionable and are very much alive.

* **IBM MQ and IBM App Connect Enterprise** carry the transaction traffic of many banks and insurers, with strong guarantees of delivery and transactional semantics.
* **TIBCO and webMethods** are long-established ESBs, with large installed bases; webMethods now belongs to IBM.
* **Solace** and **SAP Advanced Event Mesh** provide event meshes across sites and clouds.
* **Managed file transfer and EDI products** (Axway, IBM Sterling, GoAnywhere, Cleo, OpenText) run partner exchange for retailers and manufacturers.
* **Apache NiFi** and **Apache Camel** are open-source tools for dataflow and routing, popular with engineering-led teams.
* **Healthcare engines** (Rhapsody, Mirth, InterSystems) and **industrial gateways** carry the standards of their domains.
* **CDC and replication tools** (GoldenGate, Qlik Replicate, Striim, Debezium) feed analytics and event platforms.

The right attitude toward such systems is respect and incremental change: put an anti-corruption layer in front, offload via events or CDC, and replace piece by piece using the strangler fig. Replacing an ESB in one step is how migration programs become multi-year failures.

## Choosing a Platform

A platform decision lasts for years and costs real money, and it deserves a method rather than a preference. Four steps make it defensible.

**Step 1: Define criteria and weight them.** Typical criteria include connector fit with your systems, skills available, runtime flexibility and data residency, governance features, delivery and testing support (can flows live in Git and deploy by pipeline?), observability, cost model, lock-in, and vendor viability. Weight them by what matters to *this* organization.

{{tbl platformscore | An example weighted scorecard}}

| Criterion | Weight | Platform A | Platform B | Platform C |
|---|---|---|---|---|
| Connector fit for the estate | 20% | 4 | 5 | 3 |
| Team skills and hiring | 15% | 3 | 3 | 5 |
| Runtime location and residency | 15% | 5 | 3 | 4 |
| Delivery pipeline and testing support | 15% | 4 | 3 | 5 |
| Observability and operations | 10% | 4 | 4 | 3 |
| Governance and security | 10% | 5 | 4 | 3 |
| Three-year cost | 10% | 2 | 4 | 5 |
| Lock-in and exit | 5% | 2 | 3 | 5 |
| **Weighted score** | 100% | **3.9** | **3.8** | **4.1** |

Multiply each score by its weight and add. The numbers are inventions to show the method; the useful result is not the total but the *argument*: when a stakeholder challenges the winner, you can ask which weight or score they disagree with.

**Step 2: Run a proof of concept on the hardest real flow,** not on a demo that the vendor prepared. Include failure injection (Chapter {{ref ch:testing}}): kill a run mid-way, throttle the target, send a bad record, expire a token. Measure how each platform behaves and how visible the failures are.

**Step 3: Model three-year cost,** including licenses, infrastructure, skilled staff, training, and the cost of migrating *away*. Per-task and per-call pricing models can grow nonlinearly with volume, so model the volume you expect in year three, not year one.

**Step 4: Record the decision and its revisit conditions** in a decision record, so the reasoning survives the people who made it.

!!! warning "Beware the platform that is chosen before the problem"
    The commonest platform failure is not a bad product but a mismatched one: a business-led tool for engineering-heavy flows, a heavyweight ESB for five simple integrations, a streaming platform for two hundred events a day. Return to the decision trees (Chapter {{ref ch:decide}}) and ask what *class* of platform the dominant workload needs before comparing products.

## Summary

Integration technology comes in twelve categories, and most enterprises run several generations at once. Modern platforms split a control plane from a runtime plane, which lets the runtime sit where the data must stay, and the first question about any platform is where data flows and where logic executes. MuleSoft's architecture illustrates building blocks every platform renames, and its error-handling semantics, in particular the difference between continuing and propagating, show why a platform's defaults can make failures invisible.

Boomi, Workato, the hyperscaler stacks, and inherited ESBs, MQ, and file-transfer products each have a characteristic fit and risk: distributed runtimes, business-led speed with pricing and governance risks, fine control with assembly effort, and respect for what already works. Choose with a weighted scorecard, a proof of concept on the hardest real flow with failure injection, a three-year cost model, and a decision record. Choose the class of platform before the product.

## Exercises

1. **Map your estate.** List every integration technology your organization runs and place each in one of the twelve categories. Which category is missing, and which is duplicated?
2. **Ask the control-plane question.** For one platform you use, find out where flows execute and where data passes through. Does the answer match what your security team believes?
3. **Audit the error defaults.** Find the default error behavior of your platform. Construct a flow that fails, and check whether the scheduler, the monitor, and the caller see it.
4. **Build a scorecard.** Write six criteria and weights for a platform decision you face. Score two real candidates. Which weight would change the winner?
