# Data Formats, Mapping, and Transformation

Most integration code is not about transport. Moving a message from A to B is a solved problem, and platforms provide it ready-made. Most of the code, and most of the production incidents, are about turning *one system's idea of a record into another's*. A field that is a string in one system and a number in the other. A date written with a time zone in the source and without one in the target. A name that arrives with an accent and leaves as two garbled characters. A blank value that means "unknown" on one side and "erase this" on the other.

These are not exotic failures. They are the ordinary texture of integration work, and they respond well to discipline: know the formats you will meet, know the traps hidden in common values, structure the transformation as a pipeline that validates on the way in and on the way out, and write the mapping down as a reviewed document rather than leaving it buried in code. This chapter covers each of these, with code you can run.

!!! goals "In this chapter"
    * Recognize the data formats you will meet and the typical trap of each
    * Avoid the seven value traps: money, time, text, identifiers, nulls, enumerations, and units
    * Structure a transformation as a pipeline with validation on both sides and a quarantine
    * Validate and map records with typed models, and prove the mapping with golden-file tests
    * Write a mapping specification that business owners can review and sign
    * Decide between a canonical model and direct mapping

## The Formats You Will Meet

Whatever interaction style two systems use, they must agree on how to write the data down. {{ref tbl:formats}} lists the formats that cover almost every integration, with the schema language that describes each, and the trap you should expect.

{{tbl formats | Common data formats, their schemas, and their traps}}

| Format | Typical home | Schema language | Strength | Trap |
|---|---|---|---|---|
| JSON | REST APIs, webhooks, events | JSON Schema, OpenAPI | Ubiquitous and readable | No native decimal or date type; some parsers lose precision on large numbers |
| XML | SOAP, B2B, enterprise suites | XSD | Strong typing, namespaces, mature tooling | Namespaces; external-entity attacks (disable them); verbosity |
| CSV | Batch exports, spreadsheets | None standard (document it) | Simple and compact | Delimiters and quotes inside data, encodings, lost leading zeros, locale number formats |
| Fixed-width | Mainframe and banking files | Copybooks, record layouts | Fast and compact | EBCDIC encoding, packed decimals, padding rules |
| Avro | Kafka, data platforms | Avro schema (JSON) | Compact; rich evolution rules | Needs a schema registry; readers need the writer's schema |
| Protobuf | gRPC, events | `.proto` files | Compact, typed, code generation | Field numbers must never be reused |
| Parquet | Lakes and warehouses | Embedded schema | Columnar; efficient for analytics | Unsuited to record-at-a-time exchange |
| EDI (X12, EDIFACT) | Supply-chain partners | Implementation guides | Universal in B2B | Partner-specific variants; segment terminators |
| HL7 v2, FHIR | Healthcare | Message and resource profiles | Industry standard | Local customizations (Z-segments, extensions) |
| SAP IDoc | SAP ERP | IDoc types and segments | Native to SAP processes | Status handling and custom extensions |

Two of these deserve a word of explanation, because they appear on nearly every project. **CSV** has no schema at all, so every producer and consumer carries its own assumptions about delimiters, quoting, encoding, headers, and number formats; the only defense is to *write the assumptions down*, and to validate every file against them on arrival. **JSON** looks self-describing but is deceptively loose: a number may be an integer or a floating-point value depending on the parser, a date is merely a string, and a missing field is indistinguishable from a null one unless the contract says otherwise.

## Values That Break Integrations

A handful of value types cause a disproportionate share of production defects. Learn them as a list, because each hides in plain sight.

{{tbl traps | Seven value traps and the rule for each}}

| Value | The problem | The rule |
|---|---|---|
| Money and quantities | Binary floating point cannot represent 0.10 exactly, so sums drift | Use decimals (or integer minor units such as cents) end to end; carry the currency |
| Dates and times | Missing zones, daylight-saving changes, mixed formats, epoch seconds versus milliseconds | ISO 8601 with an offset; UTC internally; convert only at the edges; document precision |
| Text | Wrong encoding produces garbled characters; a byte-order mark corrupts the first column; emoji exceed old column limits | UTF-8 everywhere; strip BOMs; test with accented, non-Latin, and emoji characters |
| Identifiers | Leading zeros are lost when parsed as numbers; case differences | Treat identifiers as strings; define case rules |
| Null, empty, missing | Three different meanings: unknown, deliberately blank, not sent | Define, per field, whether missing means "leave unchanged" or "clear" |
| Booleans and enumerations | `Y`/`N`, `1`/`0`, `true`/`false`, localized labels | Map through governed code lists, never by guesswork |
| Units | Kilograms versus pounds, centimeters versus inches, net versus gross | Carry the unit with the value; convert explicitly |

### Money

The rule about floating point is not pedantry. In Python, `0.1 + 0.2` yields `0.30000000000000004`, `1.1 * 3` yields `3.3000000000000003`, and `4.35 * 100` yields `434.99999999999994`, so converting that price to whole cents with `int()` gives 434, not 435. Multiply by several million transactions and a finance team will find cents that do not reconcile. Use a decimal type, or store integer minor units (1999 for 19.99), choose one rounding rule (banker's rounding is common in finance), and write it in the mapping specification. Carry the currency with every amount: a number without a currency is a bug waiting for its second country.

### Time

Most time bugs come from *unlabeled* times. The string `2026-11-23T10:00:00` has no zone; the receiving system will assume a zone, and half the time it will be the wrong one. In the autumn when clocks go back, an hour of local times occurs twice, and a sync keyed on local time will either skip or duplicate it. The cure is simple to state: carry the offset (`2026-11-23T10:00:00+01:00` or `...Z` for UTC), store and compare in UTC, and convert to local time only for display. Also write down the *precision*: a source that rounds to the second and a target that stores milliseconds will disagree about equality. Chapter {{ref ch:python}} shows how time errors break watermarks.

### Text

A customer named "Zoë Müller" arrives in a CSV encoded as Latin-1 and is read as UTF-8, producing "ZoÃ« MÃ¼ller", the classic sign of an encoding mismatch. Another file begins with an invisible byte-order mark that attaches itself to the first column name, so a lookup for `id` fails because the column is called `\ufeffid`. A product title with an emoji exceeds a database column sized for two-byte characters. Standardize on UTF-8 everywhere, strip byte-order marks when reading, size columns in characters, and include accented, non-Latin, and emoji text in your test data. A test file that contains only "John Smith" proves very little.

### Identifiers and Nulls

Identifiers that look like numbers are not numbers. A postal code `02134` or a customer number `00042` loses its leading zeros the moment a spreadsheet or a lazy parser treats it as an integer. Treat identifiers as strings in schemas and code, always.

The three meanings of blank deserve their own rule, because they decide whether an update destroys data. A *null* usually means "unknown," an *empty string* means "deliberately blank," and a *missing field* means "not sent." In a partial update, a missing field should normally leave the target unchanged, while a null or empty value may clear it. If the mapping does not state the rule per field, a sync that omits an optional field will wipe out data it was never meant to touch.

## The Transformation Pipeline

A transformation that does all its work in one function is hard to test and harder to debug. Structure it as a pipeline of small stages. {{ref fig:transform-transformation-pipeline}} shows the shape.

{{fig transform-transformation-pipeline | A transformation pipeline. Validate on the way in and on the way out. Quarantine instead of guessing. Keep mapping tables as governed reference data.}}

Bytes are *received* and handed to the parser (arrow 1), which decodes them from their wire format into structures and passes them to the first validation against the source's rules (arrow 2). Valid records are *mapped and enriched* (arrow 3), using code lists and lookups held as reference data (arrow 7), then *validated again* against the target's rules (arrow 4), and finally *serialized and delivered* (arrow 5). A record that fails either validation is sent to **quarantine** (arrows 6 and 8) together with the reason and the original payload, so that a person can fix it and replay it, and the rest of the batch continues.

The second validation is the one teams skip. It catches the cases where your *own mapping* produces something the target will reject: a value that is valid in the source but too long for the target field, or a mapped code that is not in the target's list. Finding that before the call to the target means a precise local error instead of a vague remote one.

{{tbl xform | Kinds of transformation}}

| Kind | Example |
|---|---|
| Structural mapping | Flatten a nested customer address into target fields; nest order lines under an order header |
| Value mapping (code lists) | Source status `3` becomes target status `Accepted` through a mapping table |
| Enrichment | Look up the cost center from the employee ID |
| Split and aggregate | One order file becomes many order messages; many line events become one daily summary |
| Normalization | Trim, case, phone and address formatting, unit conversion |
| Derivation | Compute `fullName`; derive the region from the country |
| Filtering | Only active products; only changes to fields the target owns |

### Tools for Transformation

You will meet several tools, and a good architect recognizes what each is best at. **Python with typed models** can do anything and can be tested; it is the choice for custom integrations. **SQL and dbt** are ideal for set-based transformation inside a warehouse. **jq and JSONata** reshape JSON concisely in scripts and in some integration platforms. **XSLT** transforms XML to XML or text, and still runs in many enterprise buses. **DataWeave** is the mapping language of the MuleSoft platform. **Visual mappers**, the drag-and-drop field mapping in platforms such as Boomi, Workato, SnapLogic, and Informatica, are quick to build and, without discipline, hard to review and version.

## Validate with Typed Models

In Python, the pydantic library lets you describe a record's shape and rules once and enforce them on every record. The module below validates an order, converts the timestamp to UTC, and maps the status through a governed code list. An unmapped status raises an error, which the caller sends to quarantine instead of guessing.

{{code mapping.py}}

Notice what the model enforces. The identifier is a `str`, so leading zeros survive. The total is a `Decimal` with a non-negative constraint, never a float. The currency is checked against a pattern. The validator *rejects* a timestamp without a time zone rather than assuming one, which turns a silent bug into a loud error on the first bad record. And `to_target` refuses to guess an unmapped status. The tests in the companion code exercise exactly these cases: a happy path that converts `10:00+01:00` to `09:00 UTC`, a missing time zone, a negative total, and an unknown status.

## The Mapping Specification: A Deliverable, Not a Side Effect

Write the mapping down as a reviewed document, a versioned spreadsheet or a YAML file, *before* building. It is how business owners approve meaning, how testers derive cases, and how support teams answer "why does this field say X?" two years later.

{{tbl mapspec | A mapping specification for the shop-to-ERP order}}

| Target field | Source | Rule | If missing | Validation | Owner |
|---|---|---|---|---|---|
| `externalId` | `order.id` | Copy as a string | Reject | Unique per source | Integration team |
| `status` | `order.status` | Code list `ORDER_STATUS_v3` | Quarantine if unmapped | In the list | Order management |
| `amount` | `order.total` | Decimal, two places, half-even rounding | Reject | At least 0 | Finance |
| `createdAt` | `order.created_at` | Convert to UTC, ISO 8601 | Reject if no zone | Not in the future | Integration team |
| `customerName` | `customer.first` + `last` | Trim; join with a space | Leave unchanged if both empty | At most 120 characters | CRM team |

The **Owner** column is the one most specifications omit, and it matters most. Each rule encodes a business decision: how amounts are rounded is Finance's call, not the integrator's. Naming the owner makes the sign-off real and tells future maintainers whom to ask.

!!! tip "Golden-file tests"
    Keep pairs of real, anonymized source records and the expected target output in the repository, and run the mapping against them in every build. When a production record breaks the mapping, fix the mapping and add that record to the golden set. Over a year, the golden set becomes the most valuable test asset the integration owns, because every entry is a real failure that will never return unnoticed.

```python
import json, pathlib
import pytest
from mapping import OrderIn, to_target

CASES = sorted(pathlib.Path("golden").glob("*.in.json"))

@pytest.mark.parametrize("path", CASES, ids=lambda p: p.name)
def test_golden(path):
    source = json.loads(path.read_text())
    expected = json.loads(path.with_name(
        path.name.replace(".in.", ".out.")).read_text())
    assert to_target(OrderIn(**source)) == expected
```

## Canonical Model or Direct Mapping?

When many systems exchange the same entity, you face a choice. In **direct mapping**, each pair of systems has its own transformation. In a **canonical model**, every system maps to and from one shared definition, so a new system needs one mapping instead of one per existing system.

Direct mapping fits when there are only two or three systems, when different teams own each side, and when the entities differ in *meaning*, not only in shape. A canonical model fits when many systems exchange the same entity (customer, product, order), when a hub or event backbone exists, and when someone owns and governs the canonical definition. The cost of a canonical model is that committee: someone must maintain it, and every change requires agreement from every consumer. For that reason, adopt canonical models only for the few entities that are truly shared and stable, a policy Chapter {{ref ch:patterns2}} recommended and Chapter {{ref ch:governance}} develops.

## Summary

Most integration code turns one system's record into another's, and the failures hide in values, not transport. Know the formats, JSON, XML, CSV, fixed-width, Avro, Protobuf, Parquet, EDI, HL7, and IDoc, and the trap in each. Seven value traps cause most defects: money in floating point, unlabeled times, text encodings, identifiers parsed as numbers, the three meanings of blank, ungoverned enumerations, and unlabeled units.

Structure the transformation as a pipeline: receive, parse, validate in, map and enrich with governed code lists, validate out, deliver, with a quarantine that keeps the reason and the payload. Typed models enforce the rules in code, a mapping specification with named owners gets business sign-off, and golden-file tests turn every production failure into a permanent regression test. Choose a canonical model only for the few shared, stable entities that justify the governance it costs.

## Exercises

1. **Hunt for traps.** Take a real mapping in your organization and check each of the seven traps. Which is handled worst?
2. **Time zones.** Write a test that feeds your mapping a timestamp without a zone, one in `+01:00`, and one in UTC. What does each produce? What should each produce?
3. **Write a mapping spec.** Choose five fields from a real integration and write the table in {{ref tbl:mapspec}}, including the owner. Show it to the owner of one field and record their corrections.
4. **Start a golden set.** Collect five real, anonymized records, including the ugliest you can find, and create expected outputs. Run your mapping against them.
