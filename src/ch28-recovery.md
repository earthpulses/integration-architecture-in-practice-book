# Recovery, Cutover, Capacity, and Estimation

Four questions remain after a design is chosen and secured, and they are the ones that executives ask. What happens if it all goes down? How do we switch from the old way to the new one without a disaster? Will it be big enough, and fast enough, for the load it will actually carry? And how long will it take, and what will it cost?

These are questions about *numbers* and *plans*, and they reward the habit of doing arithmetic early. This chapter covers recovery in terms the business can agree to, five cutover strategies and when each fits, the capacity arithmetic that decides whether a design is feasible, and an estimation method that gives a defensible range rather than a single optimistic figure. It ends with a view of cost over three years, because the cheapest integration to build is rarely the cheapest to own.

!!! goals "In this chapter"
    * Define recovery objectives with the business, and map failure scenarios to responses
    * Choose among five cutover strategies, and plan a parallel run with a delta feed
    * Do the capacity arithmetic that tests throughput, API budgets, and outage recovery
    * Estimate effort with a transparent method that produces a range, and state its assumptions
    * Model three-year cost, including the cost of leaving

## Recovery in Terms the Business Can Agree To

Two terms anchor every discussion of recovery. The **recovery point objective** (RPO) is how much data you can afford to lose, measured as time: "up to five minutes of orders." The **recovery time objective** (RTO) is how long you can afford to be down: "back within one hour." They are business decisions, not technical ones. The architect's job is to turn them into designs and costs, and to make the trade-off visible: a smaller RPO and RTO cost progressively more.

{{tbl tiers | Illustrative resilience tiers to agree with the business}}

| Tier | Typical RPO | Typical RTO | What it implies |
|---|---|---|---|
| 1: Business stops | Near zero | Minutes | Active-active or synchronous replication; automated failover; round-the-clock on-call |
| 2: Significant impact | Minutes | An hour or so | Replicated state; warm standby; replay from durable queues; extended on-call at peaks |
| 3: Inconvenient | Hours | A day | Backups and rebuild from code; business-hours support |
| 4: Best effort | A day | Days | Redeploy and reprocess; minimal operational machinery |

The figures are illustrations to start a conversation, not standards. The conversation is what matters: ask the business owner what an hour of outage costs (a discovery question from Chapter {{ref ch:discovery}}), propose a tier, show what it costs, and record the decision.

### What Must Survive

Recovery fails most often because something essential was not backed up or was backed up in an unusable form. For an integration, the state that must survive a failure is short and specific: the **watermarks and checkpoints** (or the integration will re-read everything or skip data); the **deduplication ledger** (or replays create duplicates); the **crosswalk** of identifiers between systems; the **configuration** and mapping tables, which belong in version control; the **queues and topics** whose contents represent undelivered work; and the **secrets and certificates**, with a procedure for reissuing them. Write the list for each integration, with where each item lives and how it is restored.

### Failure Scenarios and Responses

{{tbl scenarios | Failure scenarios and planned responses}}

| Scenario | Detected by | Response | Verified by |
|---|---|---|---|
| The target system is down for hours | Freshness alert; breaker open | Queue absorbs work; pause consumers; resume after recovery | Queue drains; reconciliation clean |
| The integration runtime is lost | Heartbeat alert | Redeploy from the pipeline; restore checkpoints; replay from the last good point | No gaps or duplicates after restart |
| A certificate or credential expires | Expiry alert (60 days ahead); 401 alerts | Rotate using the documented procedure | Calls succeed; no extra token requests |
| Bad data is written to the target | Reconciliation drift; business report | Stop with the kill switch; scope from logs; run a corrective job | Drift returns to zero |
| A region is lost | Platform alerts | Fail over per the multi-region design (Chapter {{ref ch:kafka2}}) | Smoke tests; reconciliation after failback |
| The source changes its API | Contract test; quarantine alert | Pin the version; adapt the mapping | Contract tests pass |

A plan that has never been rehearsed is a hope. Rehearse the scenarios at least once, in a test environment, and record how long each took.

## Cutover and Migration Strategies

A new integration usually replaces an old one, and the moment of replacement is the riskiest part of the project. {{ref tbl:cutover}} compares five strategies.

{{tbl cutover | Five cutover strategies}}

| Strategy | How it works | Best when | Risk |
|---|---|---|---|
| Big bang | Switch everything at once, at a scheduled time | Small scope; a clean window; easy rollback | Everything is at stake at once; rollback may be hard |
| Phased by region or entity | Move groups one at a time | Many independent units; the capacity to learn from the first group | A long coexistence period with two systems to run |
| Parallel run | Run old and new side by side, compare, and then switch | High criticality; need for proof | Cost of running both; reconciling the differences |
| Pilot or canary | Move a small, representative slice first | Uncertainty about real-world behavior | The slice may not be representative |
| Strangler (gradual) | Route more traffic to the new system over time | Replacing a large legacy system | Data synchronization between old and new; defining the end |

Most important integrations use a parallel run, often combined with phasing. {{ref fig:recovery-cutover-timeline-with-parallel-run}} shows a timeline.

{{fig recovery-cutover-timeline-with-parallel-run | A parallel-run cutover. The delta feed starts before the switch so the new system is never behind, and the old path is retained until the rollback window closes.}}

The sequence has a particular logic. The initial bulk load copies history into the new system. A **delta feed**, which carries changes made since the load began, starts *before* the switch, so that the new system is never behind. For a period, both paths run and a daily comparison shows where they differ. When the comparison is clean for an agreed period, traffic switches, and the old path remains available as the *rollback* until the rollback window closes. Only then is the old path retired. Each step has a criterion, expressed as a number: for example, "no differences for seven consecutive days" before the switch, and "no rollback in thirty days" before retirement.

!!! tip "Write the rollback before the cutover"
    For every cutover, write down the *exact steps* to return to the old path, who decides, and what has to be true for the decision to be safe. A rollback plan that depends on data the cutover has already changed is not a plan. Rehearse it.

## Capacity and Performance Arithmetic

Many feasibility questions can be answered with arithmetic that takes minutes. Do it early, aloud, and write down the assumptions.

**Throughput.** If 5,000,000 rows must move in a 2-hour window of 7,200 seconds, the job must sustain about 700 rows per second. Is that possible with one call per row, at the target's per-call time? If each call takes 150 ms with four parallel workers, throughput is about 27 calls per second, which is 26 times too slow, so the design needs a bulk path.

**API budgets.** Divide the allowance by the number of integrations that share it, and leave headroom. 600 requests per minute shared by three integrations is 200 each; at 70 percent use, 140 per minute, or about 2.3 per second.

**Outage recovery.** A four-hour outage at 1,200 orders per hour accumulates 4,800 messages. At 2 orders per second per worker and two workers, the backlog drains at 4 per second, in 1,200 seconds, or 20 minutes (and, with live traffic arriving at 0.33 per second, a little longer).

**Storage.** For a Kafka topic or a quarantine store, multiply ingest rate, retention, and replication, as in Chapter {{ref ch:kafka2}}.

**Latency.** Multiply the round-trip time by the number of sequential calls, as in Chapter {{ref ch:topologies}}. A hundred sequential calls at 80 ms is eight seconds.

!!! why "Why this matters"
    A fifteen-minute calculation can invalidate a design that would take three months to discover to be infeasible. The arithmetic also builds credibility: a stakeholder who sees you derive "this cannot work with one call per record" in front of them is far more likely to accept the more complex design.

## Estimating Effort

Estimation is the art of being usefully wrong. A single number invites a promise; a *range with stated assumptions* invites a conversation. The method below is deliberately simple and transparent. It is a **rule of thumb, uncalibrated**: its constants are the author's judgment, and you should adjust them against your own past projects.

**Step 1: a base.** Start with 10 person-days for design, setup, and handover, plus 5 person-days for each entity that must be mapped and synchronized, plus 8 person-days for each system beyond the first two.

**Step 2: multiply by complexity factors.** Each characteristic of the project adds a factor, and the factors multiply.

{{tbl factors | Illustrative complexity factors}}

| Characteristic | Factor |
|---|---|
| Volume: medium (high) | 1.05 (1.20) |
| Freshness: minutes (seconds) | 1.10 (1.25) |
| Data quality: some issues (poor) | 1.15 (1.30) |
| Criticality: medium (high) | 1.10 (1.20) |
| Security review: standard (heavy) | 1.05 (1.15) |
| Team platform experience: some (none) | 1.10 (1.25) |
| Direction: two-way | 1.40 |
| Authentication: legacy or certificate-based | 1.15 |
| Network: new private link required | 1.20 |
| Environments: four or more | 1.10 |

**Step 3: state the range.** Multiply the result by 0.8 and by 1.35 to give a low and a high figure, and map the midpoint to a size: small below 15 person-days, medium 15 to 40, large 40 to 80, extra large above 80.

For Larkspur (Chapter {{ref ch:capstone}}), the base is 10 + (3 entities × 5) + (1 extra system, Kafka, × 8) = 33 person-days. The factors that apply are medium volume (1.05), freshness in minutes (1.10), some data-quality issues (1.15), medium criticality (1.10), a standard security review (1.05), and some platform experience (1.10), which multiply to about 1.69. The midpoint is therefore about 56 person-days, the range 45 to 75, and the size *large*.

Three cautions apply. The elapsed time is not the effort divided by the team size: Larkspur's elapsed time of eleven weeks was set by the security review and the shadow run, not by the build. The estimate must list its *assumptions* (what is in scope, what is already in place), because a changed assumption changes the number. And the method should be *calibrated*: after each project, compare the estimate with the actual and adjust the constants.

## Three-Year Cost

The build cost is the visible part of the bill. A three-year view includes the rest.

{{tbl cost | Components of a three-year cost view}}

| Component | Includes |
|---|---|
| Build | Effort from the estimate, at the loaded daily cost |
| Licenses and platform | Subscription or license fees; per-task or per-call charges at the *year-three* volume |
| Infrastructure | Compute, storage, network, and data transfer (egress between clouds can dominate) |
| Operations | On-call, monitoring, incident handling, patching, certificate renewal |
| Change | Adapting to API changes, new fields, new consumers |
| Exit | The cost of migrating away, or retiring the integration |

Two habits improve such models. Model *year three's volume*, not year one's, because per-unit pricing can grow faster than volume. And include **exit cost** explicitly: lock-in is a cost that does not appear until you try to leave.

## Summary

Recovery begins with objectives the business agrees to, a recovery point and a recovery time, matched to a resilience tier and its cost. The state that must survive is short and specific: checkpoints, the deduplication ledger, the identifier crosswalk, configuration, queues, and secrets. Failure scenarios should be mapped to detection, response, and verification, and rehearsed.

Five cutover strategies, big bang, phased, parallel run, pilot, and strangler, suit different risks, and most important integrations use a parallel run with a delta feed and numeric criteria for switching and for retiring the old path, with the rollback written and rehearsed in advance. Capacity arithmetic on throughput, API budgets, outage backlog, storage, and latency settles feasibility in minutes. An estimate is a range with assumptions, built from a base and complexity factors and calibrated against actuals. A three-year view includes licenses at year-three volume, operations, change, and the cost of exit.

## Exercises

1. **Set the objectives.** For an integration, propose an RPO and an RTO and a tier. What would the business owner say it costs them per hour? What would your proposal cost?
2. **Plan a cutover.** Write the criteria, as numbers, for each of the four steps of a parallel-run cutover: start the delta feed, begin the parallel run, switch, retire.
3. **Do the arithmetic.** A job must update 2 million records in a 4-hour window against an API that allows 8 calls per second. Is one call per record feasible? What would you do?
4. **Estimate it.** Apply the method to a project you know. State the assumptions, give the range, and compare with the actual effort if the project is complete.
