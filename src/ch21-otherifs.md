# Beyond REST and Kafka

REST and Kafka dominate conversations about integration, and an architect who knows only them will, sooner or later, meet a client whose most valuable data is reachable only through something else. A mainframe that speaks MQ. A bank that exchanges files over SFTP. A hospital whose systems talk HL7. A factory whose machines speak OPC UA. A supplier who sends purchase orders as X12 over AS2. A 15-year-old ERP exposed as SOAP services described by a WSDL.

None of these is exotic. Each is the right answer in its own world, and each has conventions, pitfalls, and a body of practice that you can learn in an afternoon, provided you know what to look for. This chapter surveys the interfaces you will meet beyond REST and Kafka, concentrating on the *integration-relevant* facts: how each is reached, how it fails, and what to ask. It then treats two practices that recur across all of them: file-based integration done properly, and the webhook receiver that accepts fast and processes later.

!!! goals "In this chapter"
    * Recognize SOAP, gRPC, GraphQL, database, queue, industrial, healthcare, B2B, and mainframe interfaces and know what each demands
    * Design file-based integration with manifests, atomic delivery, checksums, and idempotent loading
    * Build a webhook receiver that verifies, persists, acknowledges, and defers processing
    * Choose between an API, a database read, and a file when a system offers all three

## A Tour of Other Interfaces

{{tbl interfaces | Interfaces beyond REST and Kafka}}

| Interface | Typical home | What to know | Common pitfall |
|---|---|---|---|
| SOAP and WSDL | Older ERPs, banking, government | A strongly typed XML contract; tooling generates clients from the WSDL | Namespaces and versioned WSDLs; large envelopes; WS-Security variants |
| gRPC | Internal services, high-performance APIs | Protobuf contracts over HTTP/2; streaming | Browser and proxy limitations; field-number discipline |
| GraphQL | Front-end-driven APIs, some SaaS | The client chooses the fields; one endpoint | Query cost and depth limits; caching; pagination conventions |
| JDBC and ODBC database access | Databases and warehouses | Direct reads, sometimes writes; the fastest path | Bypasses business rules; couples you to the physical schema; production load |
| IBM MQ, JMS | Mainframes, banking, retail | Reliable queues with transactional semantics | Message formats (copybooks, EBCDIC); poison messages; XA transactions |
| MQTT | Devices and IoT | Lightweight publish and subscribe with quality-of-service levels | Intermittent connections; topic design; device identity |
| OPC UA, Modbus | Factories, plants | Industrial data models and registers | Security zones; time synchronization; vendor-specific profiles |
| HL7 v2 and FHIR | Healthcare | v2 is pipe-delimited messaging over MLLP; FHIR is REST with standard resources | Local customizations; identity matching of patients |
| EDI (X12, EDIFACT) over AS2, SFTP, VANs | Supply chains | Standard documents with envelopes and acknowledgments | Partner-specific variants; certificate management |
| SFTP and file drops | Everywhere | Batch exchange; simple and robust | Partial files; encodings; duplicates |

A few of these deserve a brief expansion.

### SOAP and WSDL

SOAP services publish a WSDL, a machine-readable description of every operation, message, and type. That is a strength: client libraries generate code from it, and the contract is explicit. The common difficulties are practical. Different WSDLs for different service versions may coexist. Security headers (WS-Security) come in several variants. And a service that returns large XML envelopes can be slow to parse. The reconnaissance sheet of Chapter {{ref ch:readdocs}} applies equally: find the WSDL, its version, the authentication, the limits, and the fault format, and probe with a tool such as `curl` or a SOAP test client before designing.

### Database Integration

Reading a database directly is tempting: it is fast, complete, and needs no API. It also bypasses the application's business rules, couples you to the *physical* schema (a column renamed in a release breaks you), and places load on a production system whose owners did not agree to it. If you must read directly, use a read replica; use change data capture rather than polling where the database allows it; agree the schema as a *contract* with the owning team, ideally through a view that they promise to keep stable; and avoid writing to another team's tables, which is among the most reliable ways to cause an incident.

### Industrial and Device Interfaces

Factory and device protocols such as OPC UA, Modbus, and MQTT arrive with their own architecture. The network is divided into security zones, and crossing from the operational network to the corporate one is a project of its own. Connectivity is intermittent, so a site broker must buffer and forward (Chapter {{ref ch:topologies}}). Clocks matter: a sensor with the wrong time produces misleading data. And the volume can be large, so edge filtering and aggregation are often needed before the data crosses the wide-area link.

### Healthcare Interfaces

Hospitals typically exchange **HL7 v2** messages, a pipe-delimited format carried over a simple transport (MLLP), through an *integration engine* that routes and transforms them. **FHIR** is the newer, REST-based standard, with defined resources such as `Patient` and `Observation`. The perennial difficulties are local: each hospital customizes segments and fields, and matching a patient across systems (the *master patient index* problem) is a serious data-quality problem. Treat the engine's channels as integrations: name them, test them, and monitor them.

### B2B and EDI

Trading partners exchange standard documents, purchase orders (X12 850) and invoices (X12 810) in North America, or EDIFACT equivalents elsewhere, through AS2, SFTP, or a value-added network. Each document is wrapped in envelopes, and receipt is confirmed by a *functional acknowledgment* (X12 997). The standard is a baseline; each partner has an *implementation guide* with their own rules, so onboarding the tenth partner is almost as much work as the first. Certificates for AS2 signing and encryption expire and must be tracked.

## File-Based Integration Done Properly

Files remain the best way to move large volumes, to talk to legacy systems, and to satisfy strict audit requirements. They also fail in characteristic ways that a careful design anticipates. Four failures account for most incidents.

**The partial file.** The consumer picks up a file while the producer is still writing it, and loads half of it. The defense is *atomic delivery*: the producer writes to a temporary name (`orders.csv.part`) and renames it to the final name only when complete, and the consumer only looks for final names. A rename within one file system is atomic.

**The silent truncation.** A transfer fails halfway, and a file with the right name and the wrong content arrives. The defense is a **manifest**: a small companion file listing the expected file names, sizes, row counts, and checksums. The loader verifies each file against the manifest before processing, and refuses on mismatch.

**The encoding and format surprise.** A file arrives in Latin-1 instead of UTF-8, with semicolons instead of commas, or with a header row added. The defense is a *written file specification* (Chapter {{ref ch:formats}}) and validation on arrival, quarantining files that do not conform.

**The duplicate delivery.** The same file arrives twice. The defense is idempotent loading: record the identity of every processed file (name and checksum) in a ledger, and skip repeats; and make the row-level load an upsert.

A sound loader therefore follows a fixed sequence: detect a new file, verify against the manifest, check the ledger, validate the format, load idempotently in batches, record success in the ledger, and *archive* the file (never delete it immediately), with the file's disposition logged in the run summary. A failure at any stage moves the file to a quarantine folder with the reason.

!!! tip "Keep the file, keep the evidence"
    Archive every received file, unmodified, for a period that matches your audit obligations. When a number in the target is questioned six months later, the original file is the only complete evidence of what the source actually sent.

## A Webhook Receiver: Accept Fast, Process Later

Chapter {{ref ch:time}} showed the sequence; here is the structure of the code. A receiver does exactly three things on the request path: verify, persist, and acknowledge. Everything else happens later, off the request path.

```python
def handle_request(headers, body):
    # 1. VERIFY: reject anything we cannot trust (no processing yet)
    if not webhook.verify(SECRET, body, headers.get("X-Signature"),
                          headers.get("X-Timestamp")):
        return 401
    # 2. PERSIST: put the raw event somewhere durable
    queue.put({"received_at": now(), "headers": dict(headers),
               "body": body})
    # 3. ACKNOWLEDGE: answer in milliseconds
    return 200

def worker():
    while True:
        item = queue.get()
        event = json.loads(item["body"])
        if ledger.first_time(event["id"]):      # deduplicate
            apply_to_target(event)              # idempotent write
```

The handler contains no business logic, so it cannot fail for business reasons and cannot be slow. The queue can be a broker, a database table, or a cloud queue; what matters is that the event is durable before the `200` is sent, because the sender will not retry after a success response. The worker deduplicates by event ID and applies the change idempotently. Add the reconciliation pull from Chapter {{ref ch:patterns2}} to repair whatever the fast path misses, and a webhook feed becomes dependable. The verification and ledger functions are the tested ones from the companion code (Appendix {{ref app:codelab}}).

## API, Database, or File?

When a system offers all three, the decision follows the requirement.

* **Use the API** when you need current data, small volumes, the application's business rules, or the ability to write safely. It is the right default.
* **Use the database** (or CDC) when you need every change with full history, the volume is high, or no API exists, and you can accept the coupling to the physical schema.
* **Use files** when volume is large, the freshness requirement is hours, the source is a batch system, or audit evidence matters.

Combining them is common and sensible: an API for the live path, a file for the nightly reconciliation, and CDC for the warehouse.

## Summary

Beyond REST and Kafka lie SOAP, gRPC, GraphQL, direct database access, queues, industrial and device protocols, healthcare messaging, B2B exchanges, and files. Each has conventions an architect can learn quickly: find the contract, the authentication, the limits, and the failure modes. Direct database reads are fast and risky, and should go through replicas, CDC, and agreed views. Industrial networks have zones, intermittent links, and clock concerns; healthcare has local customizations and patient-matching problems; B2B has partner-specific implementation guides and expiring certificates.

File-based integration done well uses atomic delivery, manifests with checksums, written specifications, idempotent loading with a ledger, and archives. A webhook receiver verifies, persists, and acknowledges, and defers everything else to a worker that deduplicates. When a system offers an API, a database, and files, choose by the requirement, and combine them where it helps.

## Exercises

1. **Write a file specification.** For an incoming CSV, write the specification (encoding, delimiter, header, types, null handling) and the manifest format. What does the loader do on a mismatch?
2. **Find the risk.** Identify one integration in your estate that reads another team's database tables directly. What would you ask the owning team to promise?
3. **Sketch a receiver.** Write the verify, persist, and acknowledge steps for a webhook from a system you integrate with, including what storage you would use for the queue.
4. **Choose the interface.** For a nightly reconciliation of 5 million records against a legacy system that offers an API, a database view, and an SFTP export, choose and justify.
