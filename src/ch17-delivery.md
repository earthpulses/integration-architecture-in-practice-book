# Delivery: Pipelines, Configuration, and Environments

An integration built by hand in one environment and copied, with edits, to the next is a liability. It cannot be rebuilt if the server is lost. It cannot be reviewed, because nobody can see what changed. It cannot be tested, because the test environment differs from production in ways nobody recorded. And it cannot be handed over, because the knowledge of how it works lives in one person's head and one person's shell history.

The remedy is the same one software engineering found decades ago: treat everything as code. The flows, the mappings, the topics, the connectors, the gateway policies, even the configuration of the target systems should be versioned, reviewed, tested, and promoted by a pipeline. This chapter describes how, including the traps that are specific to integrations: release strategies that behave strangely when the "traffic" is a queue, environments whose sandboxes lie, and the awkward fact that you cannot undeploy data.

!!! goals "In this chapter"
    * Describe a delivery pipeline for integrations, from commit to production, with the same artifact in every environment
    * List what should live in version control besides the code, and how each item is applied
    * Separate configuration and secrets from the artifact, and plan environments realistically
    * Version APIs, events, mappings, and releases consistently
    * Choose a release strategy, and explain what changes when the work arrives through a queue or a topic
    * Plan for the fact that rolling back code does not roll back data

## The Pipeline

A pipeline turns a commit into a running integration through a fixed series of automated steps, each of which can stop it. {{ref fig:delivery-delivery-pipeline-for-integrations}} shows one.

{{fig delivery-delivery-pipeline-for-integrations | A delivery pipeline for integrations. Build once, promote the same artifact through the environments, and approve with evidence.}}

A change enters as a reviewed commit (step 1). The build runs linting, unit tests, and contract tests (step 2) and then security scans for known-vulnerable dependencies and leaked secrets (step 3). If everything passes, it **packages once** (step 4): the output is an immutable artifact, such as a container image tagged with the commit identifier. That *same artifact* is deployed to a test environment through infrastructure as code (step 5), where integration and volume tests run (step 6). An approval step (step 7) records who accepted the release, and on what evidence, before the release reaches production by a controlled strategy such as a canary or a shadow run.

The principle that matters most is "build once, deploy many." The artifact tested in the test environment must be *byte for byte* the one that runs in production. Rebuilding for each environment, however convenient, means that what you tested is not what you shipped. Differences between environments belong in configuration, never in the build.

A minimal pipeline for a Python integration, expressed for GitHub Actions, looks like this; the same stages translate directly to any other system.

```yaml
name: integration-ci
on:
  pull_request:
  push: {branches: [main]}
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: {python-version: "3.12"}
      - run: pip install -r requirements.txt -r requirements-dev.txt
      - run: ruff check . && pytest -q
      - run: pip-audit -r requirements.txt       # known-vulnerable packages
  package:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: docker build -t registry.example.com/orders-sync:${{ github.sha }} .
      - run: docker push registry.example.com/orders-sync:${{ github.sha }}
  deploy-test:
    needs: package
    environment: test             # environment-scoped secrets and approvals
    runs-on: ubuntu-latest
    steps:
      - run: ./deploy.sh test ${{ github.sha }}   # the tested image tag
```

## Everything as Code

The code is the smallest part of an integration. Everything that defines its behavior should be in version control, and each item needs a defined way of being applied.

{{tbl code | What to keep in version control, and how it is applied}}

| Asset | Keep in Git as | Applied by |
|---|---|---|
| Integration code and flows | Source code, or exported platform artifacts | The build pipeline; platform deployment tooling (for example, Maven-based deployment for MuleSoft) |
| Mappings and code lists | YAML or CSV, with reviews | Loaded at start-up, or published to a reference-data store |
| Infrastructure (runtimes, queues, networks) | Terraform, Bicep, CloudFormation, or Pulumi | The infrastructure pipeline |
| Kafka topics, ACLs, schemas | Declarative topic and ACL definitions; schema files | A topic operator or provider; registry upload with a compatibility check |
| Connector configurations | JSON per connector, with secrets as references | The Kafka Connect REST API, called from the pipeline |
| Gateway policies | Declarative policy files | The gateway's management API |
| Target-system configuration (asset types, attributes, statuses) | JSON resource files | An idempotent installation script |
| Dashboards and alerts | Dashboard and alert definitions | Monitoring as code |

The last-but-one row hides a technique worth copying. Many integrations require configuration *in the target system*: custom attribute types, statuses, relation types, assignment rules. If an administrator creates them by clicking, the test environment and the production environment will differ in ways nobody remembers. Instead, describe them in JSON files and apply them with an *idempotent* script that creates what is missing and updates what exists, so that running it twice is harmless. The script is then the documentation, the installer, and the drift detector in one.

## Configuration and Secrets

Three rules keep configuration under control.

**One artifact, many environments.** Settings that vary, such as URLs, batch sizes, and schedules, come from the environment in which the artifact runs, never from rebuilt code. **Secrets by reference.** The pipeline and the runtime fetch credentials from a vault using a workload identity; nothing secret lives in Git, in variables visible to everyone, or in logs (Chapter {{ref ch:auth}}). **Validation at start-up.** The program checks its configuration when it starts and fails immediately, with a clear message, if a required setting is missing or malformed, instead of failing three hours into a run.

Add two operational tools. A **feature flag** lets you turn a flow, a target, or a new mapping on and off without a deployment, and a **kill switch**, a single flag that pauses all writing, gives operations a safe response to "something is wrong, stop it now." Check flags per message, not just at start-up, and log their state so that later investigators know which behavior was active.

## Environments

An integration typically passes through four kinds of environment, with different purposes and different data.

{{tbl envs | Environment strategy}}

| Environment | Connected to | Data | Purpose |
|---|---|---|---|
| Local or development | Mocks and containers | Synthetic | Fast feedback |
| Test | Vendor sandboxes | Synthetic or masked | Integration and failure tests |
| User acceptance or pre-production | Production-like systems | A masked copy of production | Business acceptance, volume tests, shadow runs |
| Production | Real systems | Real | Serving the business; never a test bed |

!!! warning "Sandboxes lie"
    Vendor sandboxes typically differ from production in rate limits, data volume, enabled features, authentication settings, and refresh schedules. An integration that passes in the sandbox has proved only that it works in the sandbox. List the known differences in the reconnaissance sheet (Chapter {{ref ch:readdocs}}), and plan a *shadow run* in pre-production, against production-like systems, to cover what the sandbox cannot.

## Versioning

Consistent versioning lets people reason about change. Four things need versions, and each has a rule.

{{tbl versions | What to version and how}}

| Thing | Scheme | Rule |
|---|---|---|
| APIs you publish | Major version in the path or header; minor changes are additive | A breaking change means a new major version and a deprecation window |
| Event schemas | Registry versions with a compatibility mode | The pipeline rejects incompatible changes |
| Integration releases | Semantic versioning on the artifact | Release notes list mapping and behavior changes |
| Mappings and code lists | Versioned files | Each change is reviewed by the data owner |

## Release Strategies and the Integration Traps

How you release a new version matters more for an integration than for a typical web service, because integrations hold *state* and receive work through *queues*, and both complicate the familiar strategies.

{{tbl release | Release strategies and the trap each hides for integrations}}

| Strategy | How it works | The integration-specific trap |
|---|---|---|
| Rolling | Replace instances one at a time | Old and new versions run together, so mappings and state formats must be compatible both ways during the overlap |
| Blue-green | Run the new stack alongside, then switch traffic | For queue or Kafka consumers there is no "traffic" to switch (see below) |
| Canary | Send a small share of the work to the new version | Route by key (a few customers, one region) so each entity is handled by one version; otherwise ordering and versions interleave |
| Shadow | The new version processes copies of the work and writes to a scratch target; results are compared | The best way to prove a new mapping; make sure the shadow cannot write to production by mistake |
| Feature flag | Deploy the code dark; enable it by flag | Check flags per message, and log their state |

The blue-green trap is worth working through, because it surprises experienced teams. With a web service, you switch the load balancer from blue to green and the old version stops receiving requests. A consumer of a queue or a Kafka topic *pulls* its work. If the green deployment joins the *same consumer group* as blue, Kafka divides the partitions between the two, so both versions process live traffic simultaneously. If green uses a *new* group, both versions process *every* message, and you get duplicates. Neither is what blue-green intended. The safe approach is a deliberate handover: stop blue's consumers (or pause them), start green's, and rely on idempotent processing for the moment of overlap.

!!! why "You cannot undeploy data"
    Rolling back code is easy; rolling back what the integration already wrote is not. If a bad release wrote wrong values into a million target records, redeploying the old version does not correct them. Plan *forward fixes*: a corrective job, and enough history to replay from a checkpoint. Test the "undo" path for any change that writes in bulk, before you need it, and keep the kill switch within reach.

## Delivery on Different Platforms

The principles hold on every platform, but the mechanics differ. **Integration platforms** have their own packaging and promotion: packaged components with environment extensions, exported project bundles, command-line or Maven-based deployment. Check that your platform supports Git-based review, automated tests, and promotion without hand edits; if it does not, wrap it in a scripted process, because a platform whose only deployment method is a click in a console cannot be audited. **Serverless functions and containers** fit standard pipelines; keep timeouts, memory, and concurrency settings in code. **Kafka Connect** connector configurations belong in Git and are applied through the REST API; editing them by hand in production produces precisely the drift that pipelines exist to prevent.

## Summary

Treat everything about an integration as code, reviewed and promoted through a pipeline. Build once and deploy the same immutable artifact through every environment, with differences confined to configuration. Keep in version control not just the code but mappings, infrastructure, topics and schemas, connector configurations, gateway policies, target-system configuration applied by idempotent scripts, and dashboards and alerts.

Configuration comes from the environment, secrets by reference from a vault, and the program validates both at start-up. Four environments serve different purposes, and sandboxes should be assumed to differ from production until a shadow run proves otherwise. Version APIs, schemas, releases, and mappings with explicit rules. Release strategies need adaptation for queue-based work: blue-green consumers split or duplicate the work, canaries should route by key, and shadow runs prove mappings. Because data cannot be undeployed, plan forward fixes and keep a kill switch.

## Exercises

1. **Audit your pipeline.** List everything that defines one of your integrations. Mark each item as *in version control and applied by a pipeline*, *in version control only*, or *neither*. Which gap is most dangerous?
2. **Write the idempotent installer.** Describe, in pseudocode, a script that ensures three custom attributes exist in a target system, creating or updating each. How does it behave on a second run?
3. **Plan a blue-green for a consumer.** Write the exact steps to move a Kafka consumer from version 1 to version 2 without processing a message twice, or at least without harm if you do.
4. **Design the kill switch.** Decide where an integration checks its kill switch, who may flip it, and how it is logged.
