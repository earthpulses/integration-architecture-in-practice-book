# The Integration Journey

Larkspur Outdoor's first attempt to fix the nightly CSV problem took one week. A contractor wrote a script that read new orders from the shop's database and called the ERP's order API for each one. It worked on the contractor's laptop and in a demo. It went live on a Tuesday.

By week three, security discovered that the script used a personal ERP login and ordered it disabled. By week five, the ERP team revealed that the order API allowed 60 calls per minute, which was fewer than the shop produced at peak. By week eight, the shop's database administrator found the script's queries were slowing checkout and asked for it to be switched off. By week nine, nobody could say who was responsible for any of it, because the contractor had left.

None of these problems was exotic, and every one of them could have been found in the first two weeks by asking someone. The project did not lack skill. It lacked a *journey*: a sequence of stages, each ending with a decision, each decision backed by evidence, each piece of evidence owned by a person. This chapter describes that journey, and the four gates that keep a project honest.

!!! goals "In this chapter"
    * Explain what a gate is, and what separates a real gate from a rubber stamp
    * Describe the four gates of an integration project and the evidence each requires
    * Turn discovery answers into an architecture in the right order: constraints, pattern family, delivery vehicle
    * Assign roles with a RACI chart, and know who is usually missing from the room
    * Plan the first two weeks of a project so that long-lead items start on day one
    * Define "ready to build" and "done" so that both can be checked

## Why Projects Need Gates

A **gate** is a decision point at the end of a stage. The project does not proceed to the next stage until a named person agrees, on the basis of stated evidence, that the criteria for the stage have been met. That is all a gate is. It is not necessarily a meeting, it is not a bureaucratic ritual, and it is not a delay. It is the point at which the team stops and asks, "do we actually know what we think we know?"

Gates exist because integration projects carry a distinctive risk profile. The expensive surprises are rarely about code. They are about things outside the team's immediate control: a security review that takes six weeks, a firewall rule that needs a change board, an API limit nobody mentioned, a data owner who disagrees about who owns a field. These surprises cost the same whether they are discovered in week one or week eight, with one crucial difference. In week one you can plan around them. In week eight you are already committed.

The failure mode of gates is the rubber stamp. A gate review where the criteria are vague ("design is reasonable"), the evidence is a slide deck, and the approver has not read the material does not reduce risk. It manufactures false confidence. The cure is to define each gate with *testable criteria* and *named evidence*, which the rest of this chapter does.

!!! why "Why this matters"
    Skipping a gate does not save time. It moves the discovery to production, where it is a lot more expensive. A useful test when someone proposes skipping a gate is to ask, "which of the things this gate checks do we already know for certain?" Usually the answer is "some of them," and the right response is to pass quickly on those and spend the time on the rest.

## The Journey with Four Gates

Every integration, on every technology, passes through the same sequence of stages. {{ref fig:journey-integration-journey-with-approval-gates}} shows them with the four gates that separate them.

{{fig journey-integration-journey-with-approval-gates | The integration journey. Each of the four gates has criteria, an owner, and a list of evidence. A fifth, optional gate at the very start asks whether the integration should be built at all.}}

{{tbl gates | The gates, the question each answers, and the evidence that passes it}}

| Gate | The question it answers | Passes when | Evidence | Failure if skipped |
|---|---|---|---|---|
| G0 (optional): Worth doing? | Should this be built at all? | Business outcome, owner, and a cheaper alternative have been considered | One-page case | Building integrations nobody needs |
| G1: Brief signed | Do we understand the problem? | At least 90% of critical discovery questions are answered; authority matrix agreed; the four numbers are known | Integration brief; question checklist; named owners | The right solution to the wrong problem |
| G2: Design approved | Is the design safe, feasible, and approvable? | Pattern chosen with rejected alternatives; contracts, authentication, and network path defined; security review done; decisions recorded | Design document; security approval; network diagram; ADRs | Firewall and review surprises in week eight |
| G3: Ready to release | Will it behave in production? | Contract, failure, and volume tests pass; reconciliation is clean; runbook accepted; rollback rehearsed | Test report; runbook; go-live checklist | Acceptance by demo |
| G4: Handover accepted | Can someone else run it? | The operations owner confirms; alerts reach them; hypercare exit criteria are met | Signed handover; alert test | Nobody owns it after you leave |

### G0: Is It Worth Doing?

Gate zero is optional because many integrations arrive pre-approved by someone senior. Even so, it pays to ask for a one-page case. State the business outcome, name the owner, and, most importantly, record the cheaper alternative you considered. Sometimes the cheaper alternative is "fix the nightly CSV so it rejects fewer rows," and sometimes it is "let the warehouse team query the ERP report directly." If nobody can describe an alternative, nobody has thought about the problem hard enough.

### G1: The Brief Is Signed

Gate one proves that you understand the problem. Its evidence is the **integration brief**, a document of one or two pages that Chapter {{ref ch:discovery}} teaches you to write. It states the outcome, the systems and entities, the direction of flow, the authority for each field, and the four numbers: records now, records in three years, peak changes per hour, and acceptable staleness. The gate passes when at least 90 percent of the critical discovery questions have answers, and the remainder are on a risk register with an owner and a date.

The business owner signs this gate, not the architect. The reason is that the brief is, in effect, a promise: "this is what we will deliver, to this standard, for these people." If the business owner has not agreed to that promise, the project will be re-scoped halfway through.

### G2: The Design Is Approved

Gate two proves the design can actually be built and operated. The evidence is the design document, together with approvals from the people who can say no: security, network, and the owners of both systems. The document names the chosen pattern, and, just as importantly, names the alternatives that were rejected and why. It defines the contracts (what each API call looks like), the authentication method, and the network path, and it contains the decision records.

This is the gate teams skip most often, because it feels like paperwork. It is also the gate that would have saved Larkspur's contractor, because a network-and-security review in week one would have found the personal login, the rate limit, and the load on the shop's database before a line of code was written.

### G3: Ready to Release

Gate three proves the integration will behave in production, not merely in a demo. The evidence is test results, including the failure-injection tests that Chapter {{ref ch:testing}} describes. It includes a reconciliation report showing that source and target agree, a runbook that someone other than the author has actually executed, and a rollback plan that has been rehearsed.

The most commonly missed criterion is the rollback rehearsal. Teams write a rollback plan, never test it, and discover during an incident that it assumed a database backup that nobody had taken. Rehearse it once in a test environment, and the plan stops being fiction.

### G4: Handover Accepted

Gate four proves that someone else can run what you built. A typical project ends with a few weeks of **hypercare**, a period of intensified monitoring during which the build team remains on call. The gate passes when the exit criteria for hypercare are met (for example, three weeks without a severity-one incident), the operations owner confirms they can run the integration from the runbook, and a test alert has demonstrably reached them.

Without this gate the integration ends the way Larkspur's first attempt did: with a service nobody owns, running on a contractor's account, until the day it breaks.

## From Answers to Architecture

Discovery produces answers. Architecture is what you do with them. The order in which you use the answers matters more than most people expect, and {{ref fig:journey-from-answers-to-architecture}} shows the correct order.

{{fig journey-from-answers-to-architecture | Constraints come first and rule options out. Only then do you choose a pattern family, and only after that a delivery vehicle. Unknowns are carried forward as risks, never silently assumed.}}

**Constraints come first.** Some answers eliminate options outright. If the network allows only outbound connections from the customer's data center, then any design that needs the source to call you (a webhook) needs an extra component or is out. If the target allows 60 requests per minute and you need 200, one-call-per-record is out. If the data is regulated and may not leave a region, some vendor clouds are out. Constraints are not preferences; you cannot negotiate with them, so apply them before anything else.

**Then the pattern family.** With the constraints applied, you choose among the families that remain: request-based, data-movement, messaging, routing and hub, authority and identity, or specialized. Chapters {{ref ch:patterns1}} and {{ref ch:patterns2}} describe forty-one patterns across these families. Narrowing to a family first prevents you from comparing a webhook with a nightly batch as though they answered the same question.

**Last, the delivery vehicle.** Only now do you ask whether to build the integration as code, on an integration platform, with cloud-native services, or on a streaming platform. The reason this comes last is that the vehicle should be chosen to *carry* the pattern, not to dictate it. Teams that pick the tool first spend the rest of the project arguing with it.

**Unknowns are risks.** If a critical question has no answer yet, the design must not silently assume a favorable one. Record the unknown as a risk with an owner and a date, and design so that either answer is survivable if you can. If you cannot, the gate stays closed.

Chapter {{ref ch:decide}} turns this order into a repeatable method with decision trees.

## Who Must Be Involved, and When

Integration projects span organizational boundaries, and one of the most reliable predictors of trouble is a missing voice. The usual absentees are security, network, and operations, who are also the people who can block a go-live. {{ref tbl:raci}} lists the roles that should be involved in each activity, using the standard RACI notation: **R**esponsible (does the work), **A**ccountable (answers for the outcome; exactly one per activity), **C**onsulted (is asked before the decision), and **I**nformed (is told after).

{{tbl raci | A RACI chart for an integration project}}

| Activity | Business owner | Architect | Source owner | Target owner | Security | Network | Developers | QA | Operations |
|---|---|---|---|---|---|---|---|---|---|
| Define outcome and scope | A | R | C | C | I | I | I | I | I |
| Authority matrix and mappings | C | A | R | R | I | | C | I | I |
| Pattern and platform choice | C | A/R | C | C | C | C | C | | C |
| Security review and credentials | I | R | C | C | A | C | C | | I |
| Network path and firewall changes | I | R | C | C | C | A | C | | C |
| Build | I | C | C | C | I | I | A/R | C | C |
| Test and acceptance | A | C | C | C | I | | R | R | C |
| Cutover and backfill | A | R | C | C | I | C | R | R | R |
| Runbook, alerts, handover | I | C | I | I | I | | R | C | A |

Names will differ from project to project; the roles will not. Three points are worth drawing out. First, the architect is accountable for the authority matrix and the pattern choice, but is only *responsible* (not accountable) for security and network work: those belong to the people who own the decision. Second, the **operations** role is accountable for the handover, which is why they must be named before build starts, not at the end. Third, the **source owner** and **target owner** are responsible for the mapping, because only they know what their fields really mean.

## The First Two Weeks

A good project start looks unremarkable and saves months. The overriding principle is that **long-lead items start on day one**. Service accounts, sandbox access, firewall changes, and security reviews all depend on other people's calendars, and most of them take longer than you expect. {{ref tbl:firsttwo}} shows a typical plan.

{{tbl firsttwo | A plan for the first two weeks}}

| Days | Activity | Output |
|---|---|---|
| 1 to 2 | Kick off with the business owner and both system owners. File every long-lead request now: service accounts, sandbox access, firewall and security review. | Named contacts; requests filed with dates |
| 2 to 4 | Run the discovery workshops using the question bank. Draw the current-state flow, including the manual steps. | Answered and open question lists; current-state diagram |
| 4 to 6 | Explore both APIs with `curl` against the sandbox (Chapter {{ref ch:readdocs}}). Record limits, pagination, errors, and authentication in a reconnaissance sheet. | Two reconnaissance sheets based on observed behavior |
| 6 to 8 | Hold the authority and mapping workshop. Agree identity, deletes, and ordering. | Signed authority matrix |
| 8 to 10 | Apply the decision method (Chapter {{ref ch:decide}}), compare the top two patterns, write the decision records, and estimate (Chapter {{ref ch:recovery}}). | Draft design and an estimate range |

Notice what is *absent* from this plan: no coding. The first technical activity is exploring the real APIs with `curl`, because documentation is wrong somewhere and you want to learn where before you design around it. Chapter {{ref ch:readdocs}} shows how.

!!! example "Larkspur Outdoor: the second attempt"
    When Larkspur restarted the project with a proper journey, the first two days produced five requests that would have taken the contractor's project eight weeks to discover: a service account for the ERP, a sandbox for the shop, a firewall review for the private link, a security review slot, and a calendar hold with the ERP team's DBA. The fastest of the five took nine working days to complete. Because they were filed on day one, none of them delayed the build.

## Definitions of Ready and Done

Two short checklists prevent most arguments about whether work is ready to start or finished. Write them down at the start and agree them with the business owner.

**Ready to start building** means the following are all true:

* Gate G2 has passed: security and network approvals are in hand.
* Credentials and sandboxes exist for every environment.
* The authority matrix and mapping table are signed.
* Acceptance criteria are written as numbers.
* An operations owner is named.

**Done** means these are all true:

* The integration is idempotent and restart-safe, *proved by killing it mid-run*.
* Failure handling, quarantine, and dead letter handling are in place.
* Alerts, a dashboard, and a run summary are live.
* The runbook is accepted and has been rehearsed.
* The reconciliation report shows agreement and the backfill is complete.

The phrase "proved by killing it mid-run" is deliberate. Statements such as "it handles restarts" are opinions; a test that kills the process halfway through a batch and then verifies that the target has no gaps and no duplicates is evidence.

## Running a Gate Review

A gate review does not need to be long, but it does need to be real. A format that works for most projects:

1. **Circulate the evidence 48 hours ahead.** The approver reads it before the meeting, not during it.
2. **Spend the meeting on the weakest evidence,** not the strongest. The team should say, "here is what we are least sure of," and the approver should push on exactly those points.
3. **Record one of three outcomes:** *pass*, *pass with conditions* (each condition has an owner and a date), or *fail* (with the specific missing evidence).
4. **Publish the outcome** where the whole project can see it.

The third outcome, "pass with conditions," is the most useful and the most abused. A condition must be concrete ("security approval for the ERP service account, due by the 14th") and must be checked at the next gate. A condition such as "monitor security risks" is a way of not deciding.

## Gates in Agile Delivery

Teams that work in short iterations sometimes feel that gates belong to a slower world. They do not have to. The idea of a gate is *criteria checked before proceeding*, and agile teams already use the concept under other names: a "definition of ready" for stories, a "definition of done," a release checklist. The adaptation is to apply the integration-specific gates to the *whole integration* while the team still delivers in thin slices.

In practice that means three things. Run discovery and design for the whole integration up front, in the first one or two weeks, so that the expensive surprises surface early. Build in vertical slices (one entity, end to end, through to a test environment) so that each slice proves the network path, the authentication, and the failure handling on a small scale. And treat G3 and G4 as release-level criteria that apply to the first production slice and are inherited, with only the changes re-checked, by later ones.

## Handover and Hypercare

The final stage is where good projects distinguish themselves. **Hypercare** is a defined period, typically two to four weeks, in which the build team stays on call, the alert thresholds are tuned on real traffic, and the operations owner shadows and then takes over incident response. Define its exit criteria up front, as numbers: no severity-one incidents for fourteen consecutive days; alert noise below an agreed level; reconciliation clean for seven consecutive days; the operations owner has resolved at least one real incident using the runbook alone.

Hypercare is also when the runbook is corrected. No runbook survives contact with production unchanged. Every question the operations team asks during hypercare is a gap in the document, and every gap should be closed before the gate. Chapter {{ref ch:reliability}} describes what a good runbook contains.

## Summary

An integration project needs a journey: stages that end in decisions, decisions that rest on evidence, evidence that someone owns. Four gates give the journey its shape. G1 proves you understand the problem, G2 that the design is safe and feasible, G3 that it will behave in production, and G4 that someone else can run it. An optional G0 asks whether to build it at all.

Discovery answers become architecture in a fixed order: constraints rule options out, then you choose a pattern family, and only then a delivery vehicle. Unknowns are recorded as risks, never assumed away. A RACI chart makes sure that security, network, and operations are in the room, and the first two weeks put long-lead requests in motion before any code is written. Definitions of ready and done turn opinions into checks, and a gate review, held honestly, replaces a rubber stamp with a decision.

## Exercises

1. **Gate your current project.** Take an integration you are working on and evaluate it against G1 to G4. For each gate, list the criteria you cannot yet prove. Which would you close first?
2. **Find the missing role.** Fill in the RACI chart for a real project. Which column has no named person? What would happen if that person learned about the project in week eight?
3. **Write the long-lead list.** List every request on your project that depends on someone else's calendar (accounts, access, reviews, network changes). Estimate the elapsed time of each, and work out which one sets the earliest date you can go live.
4. **Define your own hypercare exit.** For a real or imagined integration, write five numeric exit criteria for hypercare.
