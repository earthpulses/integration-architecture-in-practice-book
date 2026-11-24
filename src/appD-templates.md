# Templates

These templates are starting points. Copy them into a project repository, adapt the fields to your organization, and keep them with the code they describe. Others appear in the chapters: the architecture decision record (Chapter {{ref ch:mindset}}), the integration brief (Chapter {{ref ch:discovery}}), the API reconnaissance sheet (Chapter {{ref ch:readdocs}}), the mapping specification (Chapter {{ref ch:formats}}), the integration inventory record (Chapter {{ref ch:governance}}), and the runbook outline (Chapter {{ref ch:reliability}}).

## Integration Brief (One Page)

```text
Title:            <Source> to <Target>: <entities>
Business owner:   <name>        Technical owner: <name>   Support: <team>
Purpose:          <one sentence outcome>
In scope:         <entities and fields>
Out of scope:     <explicit>
Authority:        <link to the field-level matrix>
Direction:        one-way / two-way (conflict rule: <rule>)
Freshness:        <minutes>   Volume: <today / three years / peak per hour>
Pattern:          <chosen>   Alternatives rejected because: <reasons>
Interfaces:       <source> (<spec link>)   <target> (<spec link>)
Authentication:   <scheme / account / rotation>
Runs on:          <host or platform>   Network path: <diagram link>
Failure handling: retry / quarantine / dead letters / reconciliation
Observability:    logs / metrics / alerts / dashboard
Risks:            <top five, each with an owner and a date>
Acceptance:       <test cases and numbers>
```

## Design Document Outline

1. Context, goals, and non-goals
2. Architecture diagram and data flow, including failure paths
3. Source and target reconnaissance sheets
4. Authority matrix and field mapping (configuration-driven)
5. Identity and matching strategy
6. Extraction strategy: full, incremental, delete handling
7. Load strategy: upsert, ordering, batching, rate budget
8. Error handling and recovery: retry, quarantine, dead letters, reconciliation
9. Security: accounts, secrets, network, data classification
10. Observability and alerting
11. Deployment, configuration, and environments
12. Test strategy and acceptance criteria
13. Operations: runbook, ownership, handover
14. Risks, assumptions, and open questions

## Test Plan Skeleton

{{tbl tplan | A test plan skeleton}}

| Test | What you check |
|---|---|
| Happy path | Create, update, and delete flow end to end with field-level assertions |
| Idempotency | Run twice; the second run changes nothing |
| Rename and re-key | Rename in the source; no duplicate in the target |
| Late and out-of-order change | An older change arrives after a newer one; the end state is correct |
| Failure injection | Kill the process mid-run; restart; no loss and no duplicates |
| Rate limit | Simulate 429 responses; backoff observed; no failure |
| Authentication expiry | Expire the token mid-run; a single re-authentication succeeds |
| Bad data | Null, oversize, emoji, wrong encoding: quarantined, and the run continues |
| Volume | A production-sized dataset: duration, memory, API budget |
| Reconciliation | Introduce drift; the reconciliation detects and repairs it |
| Concurrency | Two workers, one record: no double processing |

## Go-Live Checklist

* Service accounts created with least privilege; secrets in the vault; rotation documented
* The network path tested from the production host
* Target-system configuration (types, relations, attributes, layouts) installed and verified
* The initial load completed and reconciled
* Alerts routed to a real on-call person; heartbeat verified
* The runbook reviewed with the support team; the kill switch tested
* The rollback plan written and rehearsed: how to undo the load
* Stakeholders informed about expected behavior and known limitations

## Threat Model (One Page)

```text
Integration: <name>   Version: <n>   Date: <date>   Reviewed by: <contact>
Data-flow diagram: <link> (trust boundaries marked)
Data classification: <fields and classes>
#  | Element/flow     | STRIDE | Threat          | Likelihood | Impact
1  | Webhook receiver | S      | Forged webhook  | Medium     | High
   | Control: HMAC + timestamp window | Owner: Team A | Status: done
Residual risks accepted by: <name, date>
```

## Operational Readiness Review (Before Go-Live)

* An owner is named and trained; the runbook has been executed by someone other than its author
* Alerts have been tested end to end, and they reach a person; the dashboard answers the five questions
* Objectives are agreed; the reconciliation is scheduled and a drift alert is active
* Secrets are in the vault with rotation dates; certificates are inventoried
* The recovery tier is agreed and recovery has been rehearsed at least once
* The rollback and forward-fix plans are written; the kill switch is tested
* The inventory record exists; the data contract or mapping specification is published

## Post-Incident Review

```text
Summary:    what happened; the impact (records, users, duration); how and
            when it was detected
Timeline:   UTC timestamps from the first signal to recovery
Root cause: the technical cause AND why it was possible (a missing test,
            alert, or review)
What went well / what did not
Actions:    | action | owner | due | type (prevent / detect / recover) |
Follow-up:  tests added, runbook updated, standards changed
```

## Test Strategy (One Page)

```text
Scope and risks to cover
Levels: unit, contract, integration, non-functional, end to end, production checks
Environments and test data
Failure-injection matrix and results
Acceptance numbers and the evidence for each
Tools; who runs what, and when
Exit criteria for each gate
```

## Authority Matrix

{{tbl authtemplate | An authority matrix template}}

| Entity and field | Authoritative system | Other systems | Direction | Conflict rule needed? | Notes |
|---|---|---|---|---|---|
| | | | | | |
