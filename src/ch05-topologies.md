# Where Integrations Run

Before patterns come places. Two integrations that use exactly the same pattern, say "poll the source every five minutes and upsert into the target," can be trivial or painful depending on one question: *where do the systems live, and who may open a connection to whom?* A poller between two cloud applications is an afternoon's work. The same poller between a mainframe in a locked-down data center and a SaaS product can take six weeks, because the work is no longer the polling; it is the firewall change, the certificate, the proxy, and the approval chain.

For that reason, experienced architects draw the network before they draw the data flow. This chapter describes the seven topologies that cover almost every engagement, with the tools you will meet in each and the failure modes to look for. It then compares the places an integration runtime can live, translates the vocabulary of the three major clouds into one another, and ends with a checklist of network facts to establish in week one.

!!! goals "In this chapter"
    * Recognize the seven integration topologies and the one question that distinguishes them
    * Explain why an outbound agent is the approach security teams approve fastest
    * Choose where an integration runtime should live, and what each choice costs
    * Translate a design between AWS, Azure, Google Cloud, and on-premises equivalents
    * Run a network fluency check that finds firewall, proxy, and certificate problems before go-live

## The Question That Decides Everything: Who Opens the Connection?

Every topology in this chapter is, at bottom, an answer to one question: **which side is allowed to initiate a connection?** In a modern cloud, any service can call any other over the internet, so the question barely arises. Inside a corporate network, the default is the opposite. Firewalls block inbound traffic from outside, and outbound traffic is allowed only through approved proxies to approved destinations. Security teams are conservative about inbound rules for good reason: each one is a door that attackers can try.

This asymmetry explains most of the patterns you will see. An agent that opens a connection *outward* needs no inbound rule, which is why it is approved quickly. A webhook, which requires the source to call *you*, needs an inbound path and often a long review. Polling needs only outbound access, and that, as much as technical preference, is why it remains the workhorse of enterprise integration. When you read the topologies below, notice in each one which arrow crosses a firewall, and in which direction.

## Topology 1: SaaS to SaaS

The simplest topology connects cloud applications to each other. Larkspur's marketing platform needs customers from the shop; the support tool needs orders from the ERP's cloud edition. Everything is reachable over the internet, authentication is OAuth, and rate limits are the main constraint. {{ref fig:topology-saas-to-saas-via-cloud-ipaas}} shows the shape.

{{fig topology-saas-to-saas-via-cloud-ipaas | SaaS to SaaS. Everything is reachable over the internet. A cloud integration platform or serverless glue is usually the fastest answer. Webhooks and polling both work; REST calls write to the targets.}}

The runtime sits in a vendor's or your own cloud account. One SaaS application sends webhooks to the platform, or the platform polls it (arrow 1), and the platform writes to the other two applications through REST calls (arrows 2 and 3). Typical tools are cloud integration platforms such as Workato, Boomi, Celigo, or MuleSoft's cloud runtime, lightweight automation services such as Zapier and Power Automate for simple flows, and serverless functions for custom glue.

**Watch for:** vendor API rate limits shared with other integrations on the same tenant; the reliability of webhooks, especially whether the vendor can *replay* missed events; the question of whose user identity the integration runs as (a flow built on an employee's OAuth grant breaks the day the employee leaves); and task-based pricing that grows with volume.

## Topology 2: On Premises to the Cloud Through an Agent

Often one of the systems lives inside the company network: the ERP in the data center, a database, a file share. The cloud integration platform cannot reach it, and nobody will open an inbound firewall rule for it. The standard answer is the **agent**: a small piece of software installed inside the network that opens a connection *outward* to the cloud platform and keeps it open. {{ref fig:topology-on-prem-to-saas-via-agent}} shows the arrangement.

{{fig topology-on-prem-to-saas-via-agent | On premises to the cloud through an outbound agent. The agent opens the connection outward, so no inbound firewall rule is required. That is why security teams approve it fastest.}}

Inside the customer data center, the agent reads the ERP, the database, and the file shares locally (using protocols such as JDBC and SMB). It holds an outbound TLS connection to the platform's cloud control plane, where the flows are designed and monitored, and it reaches SaaS applications over HTTPS. Because every connection starts inside and goes out, the firewall needs only the rules that already allow outbound web traffic.

Products with this shape include Boomi's Atom, Workato's on-premises agent, SnapLogic's Groundplex, Microsoft's self-hosted integration runtime and on-premises data gateway, and customer-hosted runtimes of MuleSoft. The details differ in a way that matters: in some products the agent *runs* the business logic locally and only reports to the cloud, in others the agent merely provides access while the logic executes in the vendor's cloud. That changes where your data is processed, which matters to privacy and residency reviews. Ask the question explicitly rather than assuming.

**Watch for:** where logic and data actually execute; agent high availability (a single agent is a single point of failure, so use clustered agents); who patches the agent; and whether it supports your corporate proxy, including authenticated proxies.

## Topology 3: Hybrid with Private Connectivity

When volumes are high, latency matters, or policy forbids sending data across the public internet, companies join their data center to a cloud network with a private link. {{ref fig:topology-hybrid-with-private-connectivity}} shows the arrangement.

{{fig topology-hybrid-with-private-connectivity | Hybrid with private connectivity. A private link joins the data center to a cloud network. Platform services are reached through private endpoints, never over the public internet.}}

On the left, the data center holds the on-premises applications and message queues behind a firewall and proxy. A private link (a site-to-site VPN, or a dedicated circuit such as AWS Direct Connect, Azure ExpressRoute, or Google Cloud Interconnect) carries traffic to the cloud network on the right. There the integration runtime, perhaps on virtual machines or a Kubernetes cluster, calls the cloud's managed services through *private endpoints* that never expose them to the internet.

The technology is mature, and the difficulty is almost entirely organizational. **Lead time** is the first surprise: a dedicated circuit takes weeks to provision, so order it before you finish the design. Next, **overlapping IP ranges**: two companies that merged often both use the same private address space, and no routing trick fully hides that. Then **DNS across the boundary**: a name that resolves one way inside the data center and another way inside the cloud will produce failures that look like application bugs. Add MTU and fragmentation issues for large payloads, and the cost of data leaving the cloud.

## Topology 4: Multi-Cloud with an Event Backbone

Large companies rarely live in one place. Applications run in two clouds and a data center, a data platform consumes from all of them, and partners connect through an integration layer. Point-to-point links between all these locations multiply quickly. The answer is an **event backbone**: a streaming platform, such as Kafka, or an event mesh that all locations publish to and subscribe from. {{ref fig:topology-multi-cloud-with-an-event-backbone}} shows it.

{{fig topology-multi-cloud-with-an-event-backbone | Multi-cloud with an event backbone. Applications in each cloud and in the data center publish to and subscribe from a shared backbone, which also feeds the data platform and, through connectors and an integration platform, SaaS applications and partners.}}

Applications in a first cloud, a second cloud, and the data center all publish and consume events through the backbone at the center. The backbone feeds the data platform (a lakehouse, through sink connectors) and reaches SaaS applications and partners through an integration platform. No application knows the location of any other; each knows only the backbone. Tools include Kafka with cluster linking or MirrorMaker 2, commercial event meshes such as Solace or SAP Advanced Event Mesh, and cloud-native buses bridged by connectors. Chapters {{ref ch:kafka1}} to {{ref ch:kafkaio}} cover this in depth.

**Watch for:** data egress charges between clouds, which can dominate the bill; topic governance, since a backbone that anyone can write to becomes a swamp; schema ownership; and the temptation to make a single cluster the single point of failure for the whole company.

## Topology 5: Mainframe and Legacy Offload

Core systems of record, often mainframes, hold the most valuable data in a company and are the systems everyone is most afraid to touch. The pattern here is to **leave the core alone** and take data from the edges of it. {{ref fig:topology-mainframe-offload}} shows two ways.

{{fig topology-mainframe-offload | Mainframe and legacy offload. The core system is left untouched. Messages are taken from its message queue, or changes are captured from its database log, and published outward.}}

The mainframe runs its transaction monitor, its COBOL programs, and its Db2 database. Many of its applications already write messages to IBM MQ, and an MQ-to-Kafka bridge or connector can publish them outward without any change to the applications. Alternatively, a change data capture tool reads Db2's log and publishes every row change. Both approaches avoid adding queries to the core, which matters because mainframe capacity is often billed by usage.

**Watch for:** EBCDIC text encoding and packed-decimal numbers, which need conversion; batch windows in which the system is busy; per-query cost; change-freeze calendars that block deployments for months; and, above all, the small number of people who still understand the system. Find them early.

## Topology 6: Partner and B2B Connectivity

When external parties connect, such as suppliers sending invoices or retailers sending orders, the security posture changes. Partners are outside your control, and anything exposed to them is exposed to the internet. {{ref fig:topology-partner-connectivity-via-dmz}} shows the standard shape.

{{fig topology-partner-connectivity-via-dmz | Partner and B2B connectivity. Partners enter through a hardened component in the demilitarized zone, a web application firewall and API gateway for APIs, or a managed file transfer server for files. Nothing from the internet touches internal systems directly.}}

A partner reaches either a web application firewall and API gateway (for API calls) or a managed file transfer server (for AS2 or SFTP exchanges), both located in a demilitarized zone, or DMZ, a network segment between the internet and the internal network. Messages pass from there to an integration layer, which validates and translates them before anything reaches the ERP and core systems. At no point does a partner's traffic reach an internal system directly.

Typical tools are API gateways with web application firewalls, managed file transfer products such as Axway, IBM Sterling, GoAnywhere, and Cleo, AS2 and value-added-network gateways, and EDI translators. **Watch for:** partner certificates and their rotation, IP allowlists that partners insist on, acknowledgment and non-repudiation requirements, and the onboarding effort per partner, which is usually the real bottleneck.

## Topology 7: Edge, Factory, and Store Sites

The last topology is the one where the network is least reliable. Factories, warehouses, ships, and retail stores must keep operating when the wide-area link fails. {{ref fig:topology-edge-and-iot}} shows how.

{{fig topology-edge-and-iot | Edge, factory, and store sites. Local devices connect through an edge gateway to a local broker that buffers and forwards when the wide-area link returns. The cloud side receives the messages through an IoT hub and passes them to Kafka and the lake.}}

At the site, sensors and programmable logic controllers speak industrial protocols such as OPC UA and Modbus. An edge gateway converts them to a common messaging protocol and passes them to a **site broker**, often an MQTT broker. The broker stores messages while the wide-area link is down and forwards them when it returns. In the cloud, an IoT hub receives the messages and bridges them to Kafka and the data lake.

**Watch for:** intermittent connectivity and what "store and forward" does to message ordering; the management of device identities and certificates across thousands of devices; time synchronization, because a sensor with a wrong clock produces wrong data; and the data volume, which can be enormous.

!!! why "Why this matters"
    A design that is correct for a data center is often wrong for a store. A store may lose connectivity for hours and must keep selling. If your integration treats "the ERP is unreachable" as an error that stops the checkout, you have designed for the data center. Ask of every site: "what happens when the link drops for an hour?"

## Where Should the Integration Runtime Live?

Having drawn the topology, you must decide where the integration code actually runs. {{ref tbl:runtime}} compares the main options.

{{tbl runtime | Where an integration runtime can live}}

| Option | Best when | Control | Operational burden | Main risk |
|---|---|---|---|---|
| Vendor-hosted cloud runtime | All endpoints are SaaS or internet-reachable | Low | Low | Data residency and cost curve |
| Customer-hosted runtime (VM, container, Kubernetes) | Data must stay in your network or region; high volume | High | High | You own patching and scaling |
| Agent plus cloud control plane | You want cloud tooling but have on-premises sources | Medium | Medium | Unclear where processing happens |
| Serverless functions | Small event-driven glue | Medium | Low | Time limits, cold starts, hidden coupling |
| Containers on Kubernetes | Many small integrations and a platform team | High | High | Cluster expertise required |
| A scheduled job on a virtual machine | Few integrations; simple schedules; outbound only | High | Medium | Becomes a snowflake without delivery pipelines and monitoring |

The last row deserves a comment, because it is how many integrations begin. A Python script on a virtual machine is cheap, understandable, and a reasonable start. It becomes dangerous when it is the *only* copy, nobody has the deployment steps, and its monitoring is "someone would notice." Chapter {{ref ch:delivery}} describes how to turn such a script into a maintainable service, and Chapter {{ref ch:platforms}} describes when a platform is a better choice.

## The Cloud-Service Translation Table

An architect who knows one cloud can read the others if they know the equivalents. {{ref tbl:cloud}} lists the equivalent service for each common integration capability. Treat it as a map, not an equivalence: services with similar names differ in limits, semantics, and pricing, so verify the details before you rely on a mapping.

{{tbl cloud | Equivalent services across clouds and on premises}}

| Capability | AWS | Azure | Google Cloud | On premises or neutral |
|---|---|---|---|---|
| Queue | SQS, Amazon MQ | Service Bus queues, Storage queues | Pub/Sub (pull subscription), Cloud Tasks | IBM MQ, RabbitMQ, ActiveMQ Artemis |
| Topic (pub/sub) | SNS, EventBridge | Service Bus topics, Event Grid | Pub/Sub, Eventarc | RabbitMQ exchanges, Solace |
| Streaming log | Kinesis, MSK | Event Hubs (with Kafka endpoint) | Pub/Sub, managed Kafka | Kafka, Redpanda, Pulsar |
| API management | API Gateway | API Management | Apigee, API Gateway | Kong, WSO2, Axway, MuleSoft |
| Workflow | Step Functions | Logic Apps, Durable Functions | Workflows, Application Integration | Camunda, Temporal, Airflow |
| Serverless compute | Lambda | Functions | Cloud Functions, Cloud Run | Knative, OpenFaaS |
| File transfer | Transfer Family, S3 | Blob Storage SFTP, Data Factory | Storage Transfer Service | Axway, Sterling, GoAnywhere |
| Data pipelines | Glue, DMS, AppFlow | Data Factory, Synapse pipelines | Dataflow, Datastream, Data Fusion | Informatica, Talend, NiFi, Airflow |
| SaaS connectors | AppFlow, EventBridge API destinations | Logic Apps connectors, Power Automate | Application Integration connectors | iPaaS connector libraries |

## Network Fluency: What to Establish in Week One

Many integration incidents are network incidents wearing an application costume. The following facts, collected in the first week, prevent most of them. Treat them as questions for the network and security teams, and record the answers in the design.

**The path.** Trace a request from the integration runtime to each system, naming every hop: proxy, firewall, load balancer, gateway. Every hop is a place a request can be blocked, rewritten, or delayed. If you cannot draw the path, you do not know it.

**The proxy.** Does outbound traffic go through a proxy? Does it require authentication? Does it inspect TLS, replacing the server's certificate with the company's own? TLS inspection is a frequent cause of "it works on my laptop, but not on the server": the runtime does not trust the company's certificate authority. Fix it by installing the corporate certificate authority into the runtime's trust store, never by disabling certificate verification.

**Egress addresses.** Vendors often allow API access only from approved IP addresses. Find out what address your runtime's traffic leaves from. A cloud runtime may use a pool of addresses that change; request a fixed one (a NAT gateway with a static address) if the vendor needs an allowlist.

**DNS.** Does the name of the target resolve to the same address from the runtime as from your laptop? Private endpoints and split-horizon DNS make this a common cause of confusing failures.

**Certificates and expiry.** List every certificate in the path: server certificates, client certificates for mutual TLS, partner certificates. Record the expiry dates in the inventory and alert sixty days ahead. Certificate expiry is among the most predictable outages and still among the most common.

**Idle timeouts.** Load balancers, firewalls, and NAT devices close idle connections after a period, often 60 to 350 seconds. A long-running request, or a pooled connection reused after sitting idle, can fail with a reset. Set client-side keepalives and timeouts below the shortest idle timeout on the path.

**Time.** Make sure the runtime's clock is synchronized (NTP). Signed requests, token validity, and replay protection all assume clocks agree to within a few minutes, and so do your watermarks.

**Latency and bandwidth.** Estimate the round-trip time between the runtime and each system and multiply it by the number of sequential calls. One hundred sequential calls at 80 milliseconds each is eight seconds; across a continent it can be much more. This arithmetic decides whether a design should batch or run calls in parallel.

## Summary

Before patterns come places. The question that distinguishes topologies is *who may open the connection*: inbound rules are scarce and slow to obtain, outbound access is easy, and that asymmetry explains the popularity of polling and agents. Seven topologies cover most work: SaaS to SaaS; on premises to cloud through an outbound agent; hybrid with private connectivity; multi-cloud with an event backbone; mainframe offload; partner connectivity through a DMZ; and edge sites that must survive a lost link.

Where the runtime lives is a separate choice, trading control against operational burden. A cloud translation table helps read designs across providers. A short network checklist covering the path, proxy, egress addresses, DNS, certificates, idle timeouts, time, and latency converts the most common production surprises into week-one facts.

## Exercises

1. **Draw your network.** Draw the path of a request from an integration runtime to one system you integrate with, naming every hop. Mark every place a connection must be opened inbound. Which of those has the longest approval time?
2. **Classify your estate.** Choose three integrations in your organization and label each with one of the seven topologies. Do any fit none of them cleanly?
3. **Certificates.** List every certificate your most critical integration depends on, with expiry dates. Which expires first, and who gets the alert?
4. **Latency arithmetic.** An integration makes 250 sequential API calls across a link with 120 ms round-trip time. How long does one run take? How would you change the design to bring it under 30 seconds?
