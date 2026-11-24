# Synchronization Design

Moving bytes is easy. Deciding what counts as *the same thing* in two systems, what to do when a record disappears, and how to stop two systems from overwriting each other is where integrations are won or lost. These are questions about meaning and state, not transport, and the code to answer them is short once the design is right and endless if it is not.

This chapter covers the decisions at the heart of any synchronization: how records are matched across systems, how to choose between full and incremental reads, how to detect deletes (the forgotten half), how to keep field mappings in data rather than code, how bidirectional sync fails and how to prevent it, and how a reconciliation job turns an integration from "probably correct" into "provably correct." It ends with the special case of the initial load.

!!! goals "In this chapter"
    * Choose an identity strategy, and explain why storing the foreign ID beats matching by name
    * Pick full, incremental, or hybrid synchronization for a given source
    * Detect and handle deletes safely, with a guard against deleting too much
    * Keep mappings and status translations in configuration that owners can review
    * Name the four problems of bidirectional sync, and prevent each
    * Build a reconciliation job and use it as the integration's safety net
    * Plan an initial load that does not corrupt the target

## Identity: How Do You Know It Is the Same Record?

Every synchronization begins with an unglamorous question. A record arrives from the shop. Does the ERP already have it? To answer, you need a rule that decides whether two records, in two systems, are the same thing. {{ref tbl:identity}} compares the common strategies.

{{tbl identity | Identity strategies compared}}

| Strategy | How it works | Strength | Weakness | Example |
|---|---|---|---|---|
| Store the foreign ID | The target keeps the source's ID in a dedicated field | Stable under renames; reliable | Needs a field on the target | The ERP's customer-reference field holds the shop's order number |
| Natural key | Match by a business key (a code, a number, a full name) | No extra field needed | Breaks when the key changes | Matching products by SKU |
| Name match | Match by display name | Works for a first run | Renames create duplicates; collisions | Searching for a ticket by its title |
| Walk related records | Follow existing relationships to find the external ID | Uses data already present | Longer paths, more calls; fragile if links are incomplete | Table to column to the BI tool's identifier |

The rule is to **always prefer a stored foreign ID**. Name matching is acceptable only as a bootstrap for the very first run, and you must define what happens when two records share a name. Renames are the leading source of duplicates in production: a customer renames a company, the name-matching sync no longer finds it, and creates a second record, which then diverges from the first for years.

Where a system gives you no field to store the foreign ID, look for an alternative: a custom attribute, a reference or external-ID field, or a separate **crosswalk table** in the integration's own database mapping source IDs to target IDs. A crosswalk is unglamorous and robust, and it also gives you a place to record when each link was created and last verified.

## Full or Incremental?

The second decision is how much to read each time. {{ref tbl:fullinc}} lays out the options.

{{tbl fullinc | Full, incremental, and hybrid synchronization}}

| Approach | When | Mechanics | Gotchas |
|---|---|---|---|
| Full snapshot, replace | Small data; reference data | Read everything, upsert everything, delete what is missing | Delete only if the read *completed*; guard with a threshold (abort if more than 5 to 20 percent would be removed) |
| Incremental by timestamp | The source has a reliable modified time | A watermark with overlap (Chapter {{ref ch:python}}) | Time-zone mix-ups; late commits; no deletes |
| Incremental by change feed | The source exposes an audit or event log | Consume changes in order; checkpoint the position | Feed retention is limited; missing a window needs a full resync |
| Hybrid | Most enterprise cases | Frequent incremental runs plus a nightly or weekly full reconciliation | The reconciliation must not fight the incremental run: schedule them and lock |

In practice, almost every durable integration is a **hybrid**: a frequent incremental job provides freshness, and a slower full comparison catches whatever the incremental job missed, whether because of a late commit, a dropped event, or a delete. The incremental job is the fast path; the reconciliation is the repair path. The two should share the same upsert code so that they cannot disagree about what a correct record looks like.

## Deletes: The Forgotten Half

Most designs think carefully about creates and updates and forget deletes, because a deleted record produces no data to react to. It simply stops appearing. The result is a target that grows stale, accumulating records that no longer exist at the source: customers who left, products that were discontinued, orders that were cancelled.

Four situations cover most cases.

* **The source has soft delete.** Records are flagged (status `archived`, a `deletedAt` timestamp) rather than removed. Synchronize the flag, and map it to a target status such as `Retired` instead of hard-deleting; you keep the history and avoid destructive actions.
* **The source has a delete feed or events.** Process them, but *also* reconcile periodically, because feeds drop events.
* **The source offers neither.** Run an ID-list comparison. Fetch only the identifiers (cheap), compare with what you hold, and handle the difference. This is the *snapshot and diff* pattern.
* **Whatever the mechanism, install a safety valve.** Never delete more than a threshold in a single run without human approval.

The safety valve deserves the emphasis. A comparison that deletes "everything in the target that is not in the source" is only as good as its read of the source. If the source API returns an empty page because of an outage, a misconfigured filter, or a permissions change, an unguarded job concludes that every record has been deleted, and deletes them. The guard below, from the companion code, makes the job refuse.

{{code reconcile.py}}

The `compare` function takes two dictionaries mapping record IDs to checksums and returns four things: how many records each side has, which IDs are missing from the target, which target IDs are orphans, and which records exist on both sides with different checksums. The `deletion_guard` raises an error if the orphans exceed five percent of the target; with a real, small number of orphans, it returns the list. A job that deletes only after passing the guard cannot turn a transient read failure into a disaster.

## Field Mapping: Make It Data, Not Code

Hard-coded mappings force a code release for every change, and business rules change constantly. A new status is added; two systems rename a value; a country is added to a region. Keep mappings and status translations in **configuration** that owners can review and administrators can change.

A particularly clear design defines every status once, with an alias and the system's own ID, and then maps aliases to aliases in each direction.

```json
{
  "system_a": {
    "statuses": {"New": "st-101", "Accepted": "st-105",
                 "Resolved": "st-109"},
    "to_system_b": {"Accepted": "New", "Resolved": "Resolved"}
  },
  "system_b": {
    "statuses": {"New": "1", "In Progress": "2", "Resolved": "6"},
    "to_system_a": {"In Progress": "Accepted", "Resolved": "Resolved"}
  }
}
```

Reading from the top: each system's statuses are listed once, with their local identifiers. The two mapping tables use only the *aliases*, so a human reading `"Accepted": "New"` understands it without looking up IDs. If a status arrives that has no entry in the mapping table, the integration should *skip the change and log the reason* ("no mapping for status Accepted-Pending"), never guess. A guess is a silent error; a logged skip is a visible one that someone can fix by adding a row.

## Bidirectional Sync: The Hard Mode

Chapter {{ref ch:patterns2}} recommended avoiding bidirectional synchronization through the authority split. Sometimes it cannot be avoided: two teams, each loyal to its own tool, both edit the same ticket. {{ref fig:sync-bidirectional-sync-flow-with-loop-prevention}} shows the shape of a sound design.

{{fig sync-bidirectional-sync-flow-with-loop-prevention | A bidirectional synchronization reads the change history of both systems, merges the changes in time order, applies them under a lock, and ignores the changes made by its own identity.}}

The design reads each system's *change history* (an activity log on one side, an audit table on the other), skips changes it has already synchronized by using a checkpoint, merges the remainder into one list sorted by time, and applies them one at a time in order. Each application takes a lock on the record and filters out changes made by the integration's own user.

Four problems must be solved, and a design that does not name them will meet them in production.

{{tbl fourproblems | The four problems of bidirectional synchronization}}

| Problem | What goes wrong | Solutions |
|---|---|---|
| Echo loops | The integration writes to B, which emits a change event, which the integration copies back to A | Filter out changes made by the integration's own user; stamp writes with an origin marker; compare values and skip no-ops |
| Ordering | Applying updates out of order restores old values | Sort by change time; use per-record version numbers; allow one writer per record at a time |
| Concurrency | Parallel workers update the same record | Lock with an expiring lease, or partition the work by record key so a record always goes to the same worker |
| Conflicts | Both sides change the same field within one cycle | Per-field authority; last-writer-wins only for fields you do not care about; flag the rest for a human |

The **lock lease** deserves a note. A plain lock held by a worker that crashes is held forever. A *lease* expires on its own after a set time, such as sixty seconds, so that a crash delays the record rather than blocking it. If the work can take longer than the lease, the worker must renew it, or two workers may end up processing the same record. When you evaluate a synchronization product or a third-party package for a client, read the code or documentation for exactly these behaviors: how ordering is established, what the lock covers, and what filters the integration's own writes. Claims such as "synchronizes chronologically" are easy to make, and worth verifying.

!!! tip "Prefer fewer bidirectional fields"
    Each field that flows both ways multiplies the conflict surface. Before building a two-way sync, return to the authority matrix and ask whether each field truly needs both directions. Status may belong to one system and description to the other; comments can be append-only. Often, "bidirectional" collapses to two one-way flows and a small append-only exception.

## Reconciliation: The Safety Net

Even a perfect incremental sync drifts. A late commit slips through, an event is dropped, a deploy misbehaves for a weekend, someone edits the target by hand. The only way to know the integration is right is to *check*. A reconciliation job compares the two systems on a schedule, reports differences, and optionally repairs them.

A good reconciliation compares three things per entity type: **counts** (are there as many records on each side?), **identifiers** (which are missing on either side?), and **checksums** (do the records that exist on both sides agree?). The checksum is a hash of the fields the integration is responsible for, computed identically on both sides. For very large collections, compare in slices (by date range, or by the first character of the key) and sample the checksums rather than computing all of them.

Run the reconciliation on a schedule, such as nightly, and *after any incident*. Treat a non-zero drift as an alert, and track the number over time: a slowly rising drift means a defect that individual runs hide. When the report shows differences, decide in advance who is authoritative, so that repair is mechanical: records missing from the target are created, changed records are overwritten with the source's version, and orphans are deleted subject to the guard.

!!! example "Larkspur Outdoor: what the reconciliation found"
    Larkspur's first reconciliation, run in the test environment, reported 41 orders missing from the ERP out of 12,000. The cause was a window of 38 minutes during an earlier ERP restart in which webhooks had been delivered to a receiver that did not queue them. Nobody had noticed, because every order that *did* arrive was correct. The reconciliation job, running every fifteen minutes in production, now repairs such gaps automatically, and the weekly report has been empty since go-live.

## The Initial Load

The first synchronization is special. The target is empty or holds old data, the source holds years of history, and the incremental machinery is not yet running. Three mistakes recur: loading through the same slow, per-record path used for steady state, which takes days; loading while the source keeps changing, so the copy is stale on arrival; and discovering at cutover that the load corrupted the target.

A sound plan has four parts. **Use the bulk path**: an import API, a file load, or a database bulk copy, because they are orders of magnitude faster than record-by-record calls and gentler on rate limits. **Freeze, copy, catch up**: record the watermark *before* starting the bulk copy, copy the history, then start the incremental job from the recorded watermark so that changes made during the copy are applied afterward. **Throttle** the load so that it does not starve live traffic on either system. And **verify before switching**: run the reconciliation on the loaded data, and treat a clean report as the acceptance criterion. Chapter {{ref ch:recovery}} covers cutover strategies built on this sequence.

## Summary

Synchronization turns on a few decisions about meaning and state. Match records by a stored foreign ID, using a crosswalk when the target has no field for it, and treat name matching as a bootstrap only. Combine frequent incremental reads with a slower full reconciliation, using the same upsert code in both. Plan for deletes explicitly through soft-delete flags, delete feeds, or ID-list comparison, and always guard against deleting too much, because a failed read looks like a deleted source.

Keep mappings in reviewed configuration, define statuses once and map aliases, and log unmapped values instead of guessing. In bidirectional sync, solve echo loops, ordering, concurrency, and conflicts explicitly, with leases rather than plain locks, and prefer one-way flows where the authority matrix allows. A reconciliation of counts, identifiers, and checksums, run on schedule and after incidents, is what makes the integration verifiably correct, and the same discipline underpins a safe initial load: bulk path, freeze-copy-catch-up, throttle, verify.

## Exercises

1. **Choose an identity strategy.** For two systems you know, list how a record is matched today. What happens on a rename? Where could a foreign ID be stored?
2. **Test the guard.** Using `reconcile.py`, build a source with 100 records and a target with 100, then remove 20 from the source. What does `deletion_guard` do at a 5 percent threshold, and at 25 percent?
3. **Design a status map.** Write the alias-based mapping for two systems with different ticket statuses. Which statuses have no equivalent, and what should happen to them?
4. **Plan a load.** Write the four steps of an initial load for a table of 5 million records that changes about 200 times per minute. Where do you record the watermark, and what is the acceptance criterion?
