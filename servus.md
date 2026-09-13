Servus Analytics - Milestones, Epics and User Stories_doc

# Servus Analytics

## Milestones, Epics and User Stories

## Project backlog for Heitec

## Impressum

```
Hersteller Servus Intralogistics GmbH
Dr. Walter Zumtobel Str. 2
A-6850 Dornbirn
T +43 5572 22 000 – 300
F +43 5572 22 000 – 9300
http://www.servus.info
info@servus.info
Copyright © 2026
Der Inhalt dieses Dokuments darf nicht ohne
schriftliche Genehmigung der Firma
Servus Intralogistics GmbH – auch nicht
auszugsweise – an Dritte weitergegeben
und/oder vervielfältigt werden. Sämtliche
verwendeten technischen Angaben, Zeichnungen
und Fotos sind urheberrechtlich geschützt.
```

## Document revisions

```
Version Changes Date Author Comments
0.1 draft Initial version for the review
with Heitec
```

```
2026 - 09 - 16 Servus
Intralogistics
```

```
Draft, not yet released
```

## Contents

- 1. How to read this document
  - User roles
  - Conventions
  - Working assumptions
  - Definition of Done
- 2. Overview
- 3. Technology overview
- 4. Milestones
  - 4.1 Milestone M1 – Infrastructure in place and MVP implemented
    - Epic E1 – Setup infrastructure
    - Epic E2 – Implement basic components (MVP)
    - Epic E3 – Enhance MVP with features
  - 4.2 Milestone M2 – Order analysis processed and dashboards available
    - Epic E4 – Add order data mappings, aggregations and dashboards
  - 4.3 Milestone M3 – Messages and availability processed and dashboards available
    - Epic E5 – Add message and availability analysis and dashboards
  - 4.4 Milestone M4 – Assistant analysis processed and dashboards available
    - Epic E6 – Add assistant analysis and dashboards
  - 4.5 Milestone M5 – Corporate identity, portal integration and setup done
    - Epic E7 – Apply Servus corporate identity
    - Epic E8 – Portal integration and authentication
    - Epic E9 – Setup and installation

## 1. How to read this document

Structure: a Milestone is a demonstrable state of the product. A milestone consists of Epics. An epic
consists of Stories. Milestones are the sections 4.1–4.5, epics are headed "Epic E<n>", stories are
numbered E<epic>.<n> and carry acceptance criteria (AC) that Heitec verifies before hand-over. Each
level has its own "done" (see Definition of Done below). That is the whole structure.

### User roles

(roles that use the final product)

EXTERNAL (CUSTOMER SIDE)

- Plant User – read-only access to dashboards for consuming data visualisations. Right
  ServusPortal.Dashboard.Access.

INTERNAL (SERVUS SIDE)

- Dashboard Designer – Servus product owner or Heitec data expert who creates dashboards in the
  designer and publishes them as standard dashboards. Right ServusPortal.Dashboard.Design
  (includes Dashboard.Access). Customers do not get the designer (S4).
- Servus Integration Engineer – Servus software-integration engineer who configures the plant
  (mappings, schedules, working hours) and triggers or backfills analyses. Right
  ServusPortal.Analytics.Configure.
- Servus Service Technician – Servus support or operations engineer who installs, monitors and
  troubleshoots plant problems on the server.

Stories that have no product user (repository, CI, documentation, verification) are written as Enabler
stories without a role; they are still verified by acceptance criteria.

### Conventions

- (differs from POC) marks a deliberate deviation from the Python prototype.
- (confirm in E5.1 / E6.1) marks a value that is Servus's expectation and is verified against the POC
  code in the rule-extraction story of that epic before implementation.
- Decisions the team needs that are not covered here are raised with Servus as a short proposal
  (context, options, recommendation) before implementation.
- Versioning: semantic versioning; all Servus Analytics artifacts (data service, BFF, frontend,
  installer, client package) share one version number. Version 1.0.0 is the first version that is part of
  a Servus Manager setup (E9.5). Releases follow the Servus Manager release scheme.
- Language: all deliverables (code, comments, documentation, commit messages, user-facing texts
  where not localised) are in English. User-facing texts are localised in German and English (E7.2).
- Browsers: current Chrome and Edge on desktop and tablet.

### Working assumptions

(open decisions carried as assumptions)

- A1 Timestamps are processed and stored as delivered by SEAS (local plant time, datetime2); hour
  grids in local time; DST hours treated as ordinary hours.
- A2 Servus provides before the respective epic: IdentityServer how-to (authority, audience, claim
  names for rights), portal appConfig/postMessage contract, NGINX routing for the analytics app,
  service ports and names, DevExpress licence and feed access, anonymised SEAS snapshots.
- A3 All plant- and installation-specific configuration is in JSON files of the analytics installation (no
  Configuration Service); Heitec proposes the final file layout and delivers JSON schemas.
- A4 Portal, SWL libraries and analytics frontend are all Angular 22 / DevExtreme 26.1. The frontend
  is offered integrated in the Servus Portal only (external app: iframe + postMessage token
  handover, S9); there is no standalone mode with its own login. Because the versions are aligned,
  the dashboard feature is built as a library so that the portal team can later host it as a native portal
  route without changing the feature code.

### Definition of Done

The Definition of Done has three levels. A story is done when the story checks pass; an epic is done
when all its stories are done and the epic checks pass; a milestone is done when all its epics are done
and the increment is releasable. Every item is a yes/no check.

STORY DONE

1. Pull request reviewed by another Heitec developer and merged to main; CI green with no new
   analyzer warnings or lint findings.
2. Automated tests added and passing in CI: unit tests for business logic, integration tests for data
   access and migrations, a component or end-to-end test for UI changes; the existing suite still
   passes.
3. Acceptance criteria verified by the Heitec tester (not the author) on the test VM from a CI artifact;
   evidence linked in the work item; the Heitec product owner accepts the story.
4. Security: new endpoints and hubs carry the required authorization policy; identifiers and inputs are
   validated; no new high-severity finding in the dependency scan; no secrets in the repository.
5. Contracts current: OpenAPI, AsyncAPI, JSON schemas, the sample configuration set and the
   validation CLI are updated for the change; contract tests pass.
6. Observability: new code paths log with the correlation fields, are covered by traces and metrics
   where they run inside an analysis, and return problem details on errors.
7. User-facing texts exist in German and English; documentation touched by the story is updated in
   English.
8. Defects found and not fixed are recorded as bugs; nothing is silently deferred.

EPIC DONE

1. All stories of the epic are done.
2. The epic's behaviour is demonstrated to Servus on the test VM and Servus accepts.
3. Data dictionary, operations notes, configuration guide sections and ADRs of the epic are complete.
4. For the data-source epics E4–E6: the POC comparison report is accepted by Servus.

MILESTONE DONE (RELEASABLE INCREMENT)

1. All epics of the milestone are accepted.

2. One CI run produced all artifacts (data service, BFF, frontend, installer where it exists, client
   package) with the same version; the repository is tagged with it.
3. A clean installation and an upgrade from the previous milestone's version are verified on the test
   VM (installer, or until M5 the documented manual procedure); data, configuration files and custom
   dashboards survive the upgrade.
4. The smoke-test checklist passes; release notes list changes, configuration changes and known
   issues; no open defect of severity 1 or 2.

## 2. Overview

```
Milestone Demonstrates Epics
M1 – Infrastructure in place and MVP
implemented
```

```
Repository, CI and test VM exist. Both
services and the frontend run end to end: the
data service reads SEAS and writes the
Analytics DB on a schedule, the BFF serves
it, the frontend shows a first data graph
inside the portal (registered manually on the
test VM). Logging, telemetry, health, run
history, manual trigger, file-based
configuration, notifications, dashboard
storage and the viewer with auto-refresh
work.
```

##### E1, E2,

##### E

```
M2 – Order analysis processed and
dashboards available
```

```
The full order analysis runs with JSON-
configured mappings, is idempotent and
reports data quality. The default dashboard
"Orders and ARC utilisation" is shipped as
protected standard dashboard with filters and
auto-refresh; designer and publish work.
```

##### E

```
M3 – Messages and availability processed
and dashboards available
```

```
The message/availability analysis runs from
tblMes_Archive with JSON-configured
originator types, filters and exclusions;
component availability, location and plant
errors are computed idempotently; the
default dashboard "Messages and
availability" is shipped.
```

##### E

```
M4 – Assistant analysis processed and
dashboards available
```

```
The assistant analysis runs from
SeasLogDB.Logs with JSON-configured
instances and area mappings; assistant
sequences, utilisation, traffic monitoring and
cycle counts are computed idempotently; the
default dashboard "Assistants" is shipped.
```

##### E

```
M5 – Corporate identity, portal integration
and setup done
```

```
Servus look and German/English. Analytics
opens from the portal app switcher with real
tokens and rights; the portal integration is
complete and hardened. Installer handles
install, update and uninstall inside the Servus
Manager setup and automates the portal
registration done manually since M1;
operations manual and smoke-test checklist
exist.
```

##### E7, E8,

##### E

```
Epic Title Milestone Depends on
E1 Setup infrastructure M1 –
```

```
Epic Title Milestone Depends on
E2 Implement basic components (MVP) M1 E
E3 Enhance MVP with features M1 E
E4 Add order data mappings, aggregations
and dashboards
```

##### M2 E

```
E5 Add message and availability analysis
and dashboards
```

```
M3 E3, E4 (shared enrichment,
dashboard lifecycle)
E6 Add assistant analysis and dashboards M4 E3, E4 (shared enrichment,
dashboard lifecycle)
E7 Apply Servus corporate identity M5 E3, E4, E5, E6 (dashboards to be
localised and styled)
E8 Portal integration and authentication M5 E
E9 Setup and installation M5 E3, E4, E5, E6, E
```

E4, E5 and E6 are the three data-source epics (orders, messages, assistants) and follow the same
pattern: configuration files → reading and mapping → business rules → aggregations → tables,
quality and POC comparison → default dashboard. E1–E3 and E7–E9 are built once.

Until the installer of E9 exists (M5), Servus Analytics is installed manually on the test VM from CI
artifacts following the deployment procedure of E1.2 and the portal embedding procedure of E2.4. This
is accepted for M1–M4.

## 3. Technology overview

```
Area Technology Notes
Frontend Angular 22 Host app analytics-host plus feature library
@servus/analytics-dashboard; same major as the
Servus Portal and the SWL libraries.
Dashboards DevExpress Dashboard
26.
```

```
Angular client (devexpress-dashboard, devextreme
26.1, same version as the portal) and ASP.NET Core
server (DevExpress.AspNetCore.Dashboard) in server-
side data processing mode. Licence and feed
provided by Servus.
Backend .NET 10 Worker SDK for the data service, ASP.NET Core for
the BFF; C# with nullable enabled and analyzers as
errors.
Hosting Windows Services Host.CreateDefaultBuilder().UseWindowsService(),
Kestrel on fixed ports assigned by Servus
(placeholders 50020 data service, 50021 BFF),
%%HOSTNAME%% placeholders in appsettings.json;
services Servus Analytics and Servus Analytics
BFF.
Application API HTTP/JSON with OpenAPI
3
```

```
Document generated from code at build time and
committed under docs/api/; controllers under
/servus/analytics/... and /servus/analytics-
bff/...; problem details for errors.
Application
notifications
```

```
SignalR with AsyncAPI Servus NotificationHub pattern
(Servus.Seas.Api.Server.SignalR); contracts as
ApiNotificationDefinition<T> in
Servus.Analytics.Client; AsyncAPI document
committed and verified against the implementation
by a test.
Instrumentation OpenTelemetry Traces (one per analysis run, spans per step;
ASP.NET Core request tracing) and metrics; OTLP
exporter configurable, disabled without errors when
no endpoint is set.
Logging Serilog with Servus Logger
sink
```

```
Structured events with RunId, Analysis, Plant; bridge
to Servus.Seas.Logging / Logger service provided by
Servus; rolling file as second sink.
Database MS SQL Server Analytics DB ServusAnalytics (read/write by the
data service, read-only login for the BFF); SEAS
databases SeasObsDB, SeasConfigDB, SeasPathDB,
SeasLogDB read-only.
Authentication JWT bearer via Servus
IdentityServer
```

```
Servus.Api.Authorization policies on top of the
Servus Seas.Api stack; tokens handed over by the
portal shell; no own login.
```

Area Technology Notes

Servus UI
libraries

```
SWL @servus/angular-ui-
library, @servus/angular-
services (Angular 22)
```

```
Layout, theme tokens, typography, services;
consumed from the Servus npm feed, never forked.
```

Installer NSIS Sections following the Servus Manager
seassetup.nsi (sc.exe create, placeholders, service
account, description).

## 4. Milestones

Each milestone below lists its epics, and each epic its stories with acceptance criteria. The order of the
milestones is the planning order.

### 4.1 Milestone M1 – Infrastructure in place and MVP implemented

#### Epic E1 – Setup infrastructure

Goal: Heitec can build, test and deploy autonomously on infrastructure that mirrors a customer
installation.

E1.1 Azure DevOps repository

Enabler: one product repository so that all components are versioned and reviewed in one place.

1. Repository servus-analytics in Azure DevOps (collection Servus, project Externals) with service/,
   bff/, frontend/, installer/, docs/; personalised access for Heitec.
2. Branch policy on main: pull request required, one reviewer, CI must pass, no direct pushes.
3. Private Servus NuGet/npm feeds configured (NuGet.config, .npmrc) without credentials in the repo;
   Central Package Management for .NET.
4. README.md: how to build, test and run every component locally, including required Servus packages
   and the DevExpress licence.

E1.2 Test and development VM

Enabler: a VM that mirrors a customer server so that acceptance criteria are verified in a realistic
setup.

1. Windows Server VM with SQL Server, Servus Manager (SEAS databases restored from an
   anonymised snapshot provided by Servus), Servus Portal, IdentityServer and NGINX.
2. Both analytics Windows Services and the frontend can be deployed to it from CI artifacts; access
   for Heitec and Servus documented.
3. The VM is the reference environment named in the Definition of Done.

E1.3 CI pipeline

Enabler: every change is built, tested and packaged automatically.

1. Pipeline builds the .NET 10 solution and the Angular 22 app; runs unit tests and integration tests
   against SQL Server in a container; publishes test results and coverage.
2. Static analysis enforced: .NET analyzers with warnings as errors, ESLint and Prettier.
3. Versioned artifacts per run: data service, BFF, frontend bundle, later the installer (E9).
4. A reusable SEAS test seed (schema subset of SeasObsDB, SeasPathDB) is available to integration
   tests.

#### Epic E2 – Implement basic components (MVP)

Goal: the thinnest end-to-end slice: SEAS → data service → Analytics DB → BFF → frontend shows
a graph inside the portal on the test VM. Portal embedding is done manually (automated in E9), no
token validation yet (development mode, enforced in E8), no plant configuration yet.

MVP data scope: completed order positions of a time window are read from SEAS and written as raw
rows to a first Orders table; the first graph is "completed order positions per hour".

E2.1 Analytics DB with migrations

As a Servus Service Technician, I want the Analytics DB created and upgraded by scripts so that no
manual DDL is needed.

1. Database ServusAnalytics created if missing; versioned migrations (DbUp with dated scripts,
   Servus pattern, or EF Core migrations; ADR) executed by a Servus.Analytics.DbUp console,
   idempotent on re-run; schema version table.
2. Conventions for every table: Plant column, unique business key Id, time columns datetime2(3).
3. First tables: Orders (MVP columns) and AnalysisRuns (run history, E3.7).
4. Read-only view v_Orders; dashboards bind to views only.

E2.2 Data service: Windows Service with SEAS read and Analytics write

As a Servus Service Technician, I want the data service to run as a Windows Service like other
Servus Manager services.

1. .NET 10 Worker, UseWindowsService(), Kestrel on the port assigned by Servus (placeholder
   50020 ), service name Servus Analytics, delayed-auto start, appsettings.json with %%HOSTNAME%%
   placeholders.
2. Read-only connection to SeasObsDB/SeasPathDB and read/write connection to the Analytics DB, both
   configured, least-privilege logins.
3. Data access behind an interface so that the SEAS source can later be replaced by Servus
   Manager APIs.
4. MVP analysis: reads completed order positions (OrderPositionStatus = 101, ArcId <> 0) of a
   fixed lookback window from ArchiveOrderPosition/ArchiveOrder and writes them to Orders; runs
   once at startup and every 15 minutes (fixed for the MVP).
5. Startup without SEAS DB or Analytics DB does not crash the service; it retries with back-off and
   logs the condition.

E2.3 BFF: DevExpress Dashboard backend with data access to the Analytics DB

As a Plant User, I want dashboards to load their data server-side so that they are fast and do not
expose raw tables.

1. .NET 10 Windows Service Servus Analytics BFF, port placeholder 50021 , base path
   /servus/analytics-bff/ configurable, forwarded headers handled, no AllowAnyOrigin CORS
   (allow-list for development only).
2. DevExpress Dashboard 26.1 DashboardController under api/dashboard,
   DataProcessingMode.Server (differs from POC: client mode with **SELECT \*** ).
3. Exactly one connection (ServusAnalytics, read-only login) exposed through a custom connection-
   strings provider; the data source offers the v\_\* views only; custom SQL disabled by default.

4. API to serve the frontend: GET dashboards (list with { id, name }; extended with isStandard,
   modifiedAt, dataUntil in E3.11/E3.12) and the DevExpress endpoints; the MVP uses the
   DevExpress default file storage for dashboard definitions (replaced in E3.11); OpenAPI 3
   specification generated at build and committed; Swagger UI outside production only.
5. Development mode without authentication behind an explicit configuration switch: the BFF accepts
   any caller and treats it as holding all three rights (real authentication and rights in E8.1).
6. DevExpress licence registration per Servus licence.

E2.4 Angular frontend with DevExpress Dashboard showing a first graph

As a Plant User, I want to open a dashboard from the portal and see a first graph from real data.

1. Angular 22 app with DevExpress Dashboard 26.1 in ViewerOnly mode; dashboard list from the
   BFF; opening a dashboard shows the MVP chart "completed order positions per hour" from
   v_Orders. The MVP dashboard definition is created by Heitec (DevExpress designer in
   development mode or hand-written XML) and committed to the repository.
2. The dashboard feature is an Angular library @servus/analytics-dashboard; a thin host app is the
   deployable. Token, runtime configuration and locale come through injected providers, so the
   productised portal integration (E8.2) extends the host without changing the library, and the portal
   could later host the library directly.
3. Runtime configuration from assets/config.json (BFF base path, hub path, allowed portal origins);
   no compiled-in URLs; all third-party assets bundled locally (no CDN).
4. Manual portal embedding on the test VM: the app is registered by hand as external app in the
   portal appConfig.json, NGINX is configured by hand to serve the bundle under the portal origin
   and to proxy the BFF; the procedure is documented in docs/portal-integration-manual.md and is
   the basis for the installer automation (E9.1).
5. The host implements the minimum of the portal postMessage protocol needed to run inside the
   portal iframe: pageLoaded and requestToken outbound, tokenUpdate inbound; the token is forwarded
   to the BFF, which does not validate it yet (E2.3 AC5).
6. Loading, empty and error states are visible in the UI; no silent console errors.

Depends on: A2 (appConfig/postMessage contract, NGINX routing guidance) is needed already for
the MVP.

E2.5 Initial documentation and test strategy

Enabler: architecture and test strategy are documented so that Servus can limit itself to installation
and smoke tests.

1. docs/architecture.md: component diagram (data service, BFF, frontend, configuration directory,
   SEAS DBs, Analytics DB, IdentityServer, Servus Logger, portal/NGINX), runtime and deployment
   view.
2. docs/decisions/: one ADR per decision the team takes; ADRs conflicting with the high-level
   requirements are discussed with Servus first.
3. docs/test-strategy.md: test levels, tooling, test data, how acceptance criteria are evidenced;
   performance dataset defined (60 days of Orders, 50 ARCs, 1 transport/min/ARC).
4. docs/data-model.md started: every column of every table with type, unit, meaning and source.

#### Epic E3 – Enhance MVP with features

Goal: turn the MVP into an operable product skeleton: observability, robust scheduled data handling,
manual operations, configuration files, notifications, dashboard storage and a usable viewer.
Everything here is independent of the data source.

CROSS-CUTTING

E3.1 Logging with Serilog and Servus Logger

As a Servus Service Technician, I want structured logs in the Servus Logger so that I can diagnose
problems without a debugger.

1. Serilog in both services; structured events; sink into the Servus Logger (bridge provided by Servus)
   plus rolling file.
2. Every log event of a run carries RunId, Analysis, Plant; BFF request logs carry the correlation id.
3. Log levels configurable at runtime through the Logging section of appsettings.json.

E3.2 Telemetry with OpenTelemetry

As a Servus Service Technician, I want traces and metrics so that I can see where time is spent and
when runs fail.

1. One trace per analysis run with spans per step (read, transform, write); ASP.NET Core request
   tracing in the BFF.
2. Metrics analytics_run_duration_seconds, analytics_rows_written,
   analytics_run_failures_total, analytics_data_quality_dropped_rows.
3. OTLP exporter configurable; endpoint may be empty on site (telemetry disabled without errors).

E3.3 Health check endpoints

As a Servus Service Technician, I want health endpoints so that monitoring can tell whether analytics
is working.

1. Both services: /health (liveness) and /health/ready (readiness).
2. Data service readiness: Analytics DB reachable, configuration files valid, last run status per
   analysis with staleness threshold. BFF readiness: Analytics DB reachable, dashboard storage
   readable.
3. Degraded conditions (SEAS unreachable, invalid configuration file) are reported as warnings, not
   as crashes.

DATA SERVICE

E3.4 Time-window processing (from **–** to)

As a Servus Integration Engineer, I want every analysis to work on an explicit time window so that
runs are predictable and repeatable.

1. An analysis is a registered component that receives [from, to), its effective configuration and a
   cancellation token and returns rows read, rows inserted/updated/deleted per table and its data-
   quality counters. The scheduler, history, trigger API, notifications and metrics work for any
   registered analysis. The MVP analysis of E2.2 is refactored into the first registered analysis and
   later grows into the order analysis (E4).

2. Rows are upserted by business key Id (insert new, update changed, leave identical rows) (differs
   from POC: existing IDs were skipped); an analysis may declare rows of the window as obsolete;
   they are deleted when completely inside the window and counted.
3. Writes are transactional per table with configurable batch size; a failed write leaves the previous
   state and marks the run Failed.
4. Integration test: the same window run twice yields identical tables; two overlapping windows yield
   the same result as one covering window.

E3.5 Scheduled data fetching

As a Servus Integration Engineer, I want each analysis to run on a configurable schedule so that
dashboards stay current without manual intervention.

1. Per analysis: interval (minutes) and lookback (hours or days) from configuration (E3.9); order
   analysis default every 15 min with 48 h lookback.
2. A run's window is [now − lookback, now) truncated to the minute; overlapping windows are safe
   because of E3.4.
3. Runs of the same analysis never execute concurrently; failures do not stop the schedule; transient
   SQL errors are retried (3 attempts, exponential back-off, configurable).
4. Schedule changes are picked up without restart.

E3.6 Cancellation and timeout on database access

As a Servus Service Technician, I want long or stuck runs to be stopped so that they cannot block the
service or the SEAS database.

1. Configurable maximum run duration per analysis (default 60 min); an exceeding run is cancelled
   and logged as Cancelled/Failed with reason.
2. SQL command timeouts configurable for SEAS reads and Analytics writes; cancellation tokens are
   honoured by every step.
3. Graceful service shutdown: the running analysis finishes or is cancelled within a configurable
   timeout; state is persisted.

E3.7 Manual operations API: trigger and history

As a Servus Integration Engineer, I want to trigger or backfill an analysis and see the run history so
that I can recover from outages and verify configuration changes.

1. POST /servus/analytics/runs { analysis, from, to } starts a run for an explicit window (max
   length configurable, default 31 days) and returns the run id; a run of the same analysis already
   active leads to queueing or a clear rejection (Heitec decides, documents).
2. GET /servus/analytics/runs?analysis=&from=&to=&status= lists runs from AnalysisRuns: status
   (Running, Succeeded, Failed, Cancelled), window, start/end, rows read and
   inserted/updated/deleted per table, data-quality counters with sample values, error message.
3. DELETE /servus/analytics/runs/{id} cancels a running run.
4. Run history retained for a configurable period (default 90 days); endpoints documented in
   OpenAPI; authorization added in E8.1.

E3.8 Data retention on the Analytics DB

As a Servus Service Technician, I want old data removed automatically so that the database stays
within the agreed size.

1. Age-based retention per table, configurable; defaults for the order tables Orders 60 d,
   AggregatedOrders 730 d, ArcUtilization 730 d and for AnalysisRuns 90 d; the message and
   assistant epics add their defaults in E5.7 and E6.9 (differs from POC: size-driven cleanup).
2. Runs daily at a configurable time, deletes in batches, logs rows deleted per table, never deletes
   data younger than its retention.
3. Optional size guard: exceeding a configured database size raises a warning in log and health; no
   deletion beyond the rules.

E3.9 Configuration directory with JSON files

As a Servus Integration Engineer, I want all analytics settings in JSON files of one directory so that a
plant is configured in one place with a text editor.

1. Directory path in appsettings.json (default %ProgramData%\Servus\Analytics); analytics.json
   holds service settings per analysis (interval, lookback, max run minutes), retention days per table
   and run time, backfill max window, notification minimum refresh interval; documented defaults;
   missing optional files mean defaults.
2. Every file is validated against a shipped JSON schema (schemas/\*.schema.json) on load; an invalid
   file keeps the last valid one active and raises a logged error plus health warning; a missing
   mandatory file skips the affected analysis with a clear error.
3. File changes are detected (debounced watcher) and reloaded; the running analysis finishes with
   the old configuration; the reload is logged with file name and content hash.
4. CLI servus-analytics config validate [<dir>] validates all files and exits non-zero on errors;
   GET /servus/analytics/configuration returns the effective configuration per file (path, hash, load
   time, validation state), secrets excluded.
5. Secrets (connection strings) stay in appsettings.json/environment, never in the configuration files.

E3.10 Notifications on new data

As a Plant User, I want the dashboard to know when new data is available so that it refreshes without
reloading the page.

1. Data service SignalR hub /servus/analytics/notificationhub (Servus NotificationHub pattern)
   with AnalysisRunCompleted { plant, analysis, windowStart, windowEnd, rowsWritten,
   durationMs, counters }, AnalysisRunFailed { plant, analysis, windowStart, windowEnd,
   error }, DataAvailable { plant, table, dataUntil, changed }; changed = false when nothing
   was inserted or updated.
2. Contracts declared as ApiNotificationDefinition<T> in a Servus.Analytics.Client package;
   AsyncAPI specification committed and verified against the implementation by a test.
3. The BFF subscribes via the client package and relays DataAvailable and AnalysisRunFailed to
   browsers on /servus/analytics-bff/notificationhub; documented in the BFF AsyncAPI
   specification.

BFF

E3.11 File-based dashboard storage

As a Dashboard Designer, I want dashboards stored as files next to the plant configuration so that
they are backed up and shipped consistently.

1. Custom IDashboardStorage under the configuration directory: dashboards/standard/{id}.xml
   (shipped), dashboards/custom/{id}.xml (designer-created), dashboards/index.json with { id,
   name, isStandard, version, modifiedBy, modifiedAt }; absolute configured path.
2. Optimistic concurrency via the index version; saving an outdated version is rejected with a clear
   message.
3. Delete is soft (moved to dashboards/deleted/, kept for a configurable period).
4. Files changed outside the BFF (installer, manual) are detected, validated (well-formed DevExpress
   XML, index consistency) and reloaded; invalid files are reported and skipped.
5. Dashboard ids are validated (no path segments) before any file access.

E3.12 Dashboard data-version API

As a Plant User, I want the frontend to know whether the data behind my dashboard changed so that it
refreshes only when needed.

1. GET /servus/analytics-bff/dashboards/{id}/data-version returns a hash/timestamp of the
   underlying tables.
2. dataUntil in the dashboard list is the latest TimeEnd of the dashboard's tables; the tables are
   determined from the views referenced in the dashboard's data source definition.

FRONTEND

E3.13 Dashboard viewer with filters

As a Plant User, I want to select a dashboard and filter it so that I can answer my questions without
editing anything.

1. Dashboard list filtered by rights: Plant Users see standard dashboards; Dashboard Designers
   additionally see the custom dashboards; standard dashboards first and marked; open in
   ViewerOnly; designer switch not rendered without ServusPortal.Dashboard.Design.
2. Filter items defined in the dashboard (e.g. date range, area, shift, ARC) are usable; master filtering
   and drill-down work; export (PDF/Excel/image) available if enabled in configuration.
3. Header shows "data as of" (dataUntil) and last run status; BFF unavailability shows a retry option.
4. Layout fills the available iframe height and is usable at tablet width; verified in current Chrome and
   Edge.

E3.14 Refresh on new data without losing filters

As a Plant User, I want the dashboard to refresh when new data arrives while my filters stay as I set
them.

1. On DataAvailable for a table of the open dashboard the app calls the data-version API; if changed
   it reloads data only (reloadData) and keeps filters, selections, tab and drill level; if unchanged
   nothing happens.

2. Refresh is suppressed while the user interacts (debounce default 5 s) and never more often than a
   configurable minimum (default 30 s).
3. AnalysisRunFailed shows a non-blocking hint "data may be outdated" with the last successful run
   time.
4. Component test proves filter state survives a refresh.

### 4.2 Milestone M2 – Order analysis processed and dashboards available

#### Epic E4 – Add order data mappings, aggregations and dashboards

Goal: the complete order analysis with plant-specific behaviour as JSON configuration, the default
mappings, the aggregated tables, and the default dashboard "Orders and ARC utilisation" shipped as
protected standard dashboard.

Source: SeasObsDB order archive and SeasPathDB.ExternalMapping. Output: Orders, AggregatedOrders,
ArcUtilization. Terminology: an order position is one SEAS movement instruction for an ARC;
ArcAction 2 = load, 4 = drop-off, 1 = stay at parking place, 0 = drive without load handling. A leg is
one Orders row with Action ∈ {Transport, Empty, ParkingDrive, Parking}.

CUSTOMISABLE DATA MAPPINGS (JSON CONFIGURATION)

E4.1 Area mapping **areas.json**

As a Servus Integration Engineer, I want to map SEAS target addresses to logical areas so that
transports are analysed per area.

1. Entries { addressPrefix, area, areaAdditional, doubleCycleArea, indirectDoubleCycleArea,
   indirectDoubleCyclePosition?, levelStart?, levelLength? }; longest prefix of **TargetAddress**
   wins; no match → -.
2. With levelStart/levelLength the effective double-cycle area is doubleCycleArea + "-E" +
   TargetAddress.Substring(levelStart, levelLength).
3. Schema rejects duplicate prefixes and empty areas; the file is mandatory for the order analysis.
4. Import tool servus-analytics config import converts the POC area.csv.

E4.2 Working-hours calendar **working-hours.json**

As a Servus Integration Engineer, I want to define shifts and regular working hours so that KPIs can
be filtered by shift and working time.

1. One entry per (dayOfWeek 1–7, hour 0–23): { workShift, regularWorkingHour }; a compact
   range notation is allowed if the schema documents it.
2. Missing file or hour → workShift = "-", regularWorkingHour = true, one warning per run.
3. Schema and POC import (working_hours/<Plant>.csv).

E4.3 Order analysis settings **orders.json**

As a Servus Integration Engineer, I want the order rules that differ per plant configurable so that no
plant-specific code is needed.

1. Keys with defaults: sourceTables (ArchiveOrderPosition/ArchiveOrder, alternative tblOB\_\*),
   completedStatus (101), descriptionKeywordMap (keyword → normalised description, POC
   area_mapping.csv), durationBucketsMinutes ([10, 20, 30]), parkingAreaNames (["Parkplatz",
   "parking position", "Parking"]), aisleAreaNames (["AKL", "ASRS"]), nioTuIdPrefix ("NIO"),
   utilizationResolutionMinutes (60).
2. Schema shipped; missing file means defaults.
3. A sample configuration set for a demo plant (all files) is in the repo and used by integration tests.

DEFAULT DATA MAPPINGS (ORDER ANALYSIS BUSINESS RULES)

E4.4 Read completed order positions

As a Servus Integration Engineer, I want the service to read the completed order positions of a
window from the configured SEAS tables.

1. Join ArchiveOrderPosition OP, ArchiveOrder AO (OrderId), ExternalMapping M (OP.TargetAddress
   = M.ExternalId); select ArcId, OrderId, TuId, ArcAction, TargetAddress, M.Description,
   M.ParkingPlace, OrderPositionCreated, OrderPositionAccepted, OrderPositionCompleted for
   OrderPositionCompleted ∈ [from, to), OrderPositionStatus = completedStatus, ArcId <> 0,
   ordered by ArcId, OrderPositionCompleted; parameterised; table names from orders.json; read
   isolation level proposed by Heitec in an ADR (the POC used NOLOCK).
2. Rows with the sentinel timestamp 0001 - 01 - 01 are dropped and counted (droppedSentinelRows).
3. Look-behind: the last completed position per ARC before from is read so that the first leg of the
   window has a correct start (differs from POC).
4. Each position gets Area, AreaAdditional, AreaDc, AreaIdc, AreaIdcPosition from areas.json;
   unmapped addresses give - and are counted with the distinct addresses as samples
   (unmappedAddresses).

E4.5 Leg reconstruction per ARC

As a Plant User, I want each ARC's activity split into transport, empty drive, parking drive and parking
so that utilisation and flows can be measured.

1. Per ArcId in OrderPositionCompleted order. Transport: load (ArcAction = 2) → next drop-off
   (ArcAction = 4) of the same order; TimeCreated = Created(load), TimeStart = Completed(load),
   TimeEnd = Completed(drop-off), source = load target, destination = drop-off target, TuId, OrderId.
   Empty: previous leg end → next load; source = previous destination, destination = load target.
2. ParkingDrive: drive (ArcAction = 0) to a target with ParkingPlace = 1, from previous leg end to
   Completed. Parking: follows a parking drive or ArcAction = 1; TimeStart = Completed(parking),
   TimeEnd = Accepted of the first subsequent position that moves the ARC away.
3. Intermediate positions inside a leg are counted in OrderLeg (1-based) and their targets
   concatenated in OrderLegTarget (; ).
4. Duration = TimeEnd − TimeStart in seconds, null if negative (counted negativeDurations); orders
   without drop-off produce no leg (counted incompleteLegs); Id =
   "{Plant}_{ArcId}_{Action}_{OrderId}_{TimeStart:yyyyMMddHHmmss}".
5. Legs ending outside the window because of the look-behind are written only if not already present
   (upsert).
6. Unit tests: single load→drop, consecutive orders with empty drive, parking cycle, drive-only
   intermediates, missing drop-off, first leg via look-behind.

E4.6 KPIs, classification and enrichment

As a Plant User, I want durations, double-cycle classification, NIO flag and calendar attributes on
every row so that I can filter and compare.

1. Transport durations in seconds: DurationCreatedToLoad, DurationCreatedToDropOff,
   DurationLoadToDropOff; bucket labels from durationBucketsMinutes ( 0 - 10 min, 10 - 20 min, 20 - 30

```
min, 30+ min) comparing minutes (differs from POC: seconds compared to minute
thresholds).
```

2. Double-cycle classification on Empty legs, first rule wins: DoubleCycle if AreaDcSource ≠ "" and
   AreaDcSource = AreaDcDestination and AreaDcPositionSource ≤ AreaDcPositionDestination;
   else IndirectDoubleCycle if AreaIdcSource = AreaIdcDestination; else FromParkingPosition if
   AreaSource ∈ parkingAreaNames; else AisleChange if AreaSource ∈ aisleAreaNames and
   AreaSource = AreaDestination; else SingleDrive. Flags (0/1) and TransportType are set on the
   empty leg and copied to the immediately following Transport leg (documented in the data
   dictionary).
3. NIO: Transport legs with TuId starting with nioTuIdPrefix get IsNio = 1 and AreaDestination =
   "NIO" (differs from POC: explicit flag added).
4. Calendar on all three tables from TimeStart: DayOfWeek (1 = Monday), DayName (English), Hour,
   HourString (dd.MM.yyyy, HH), WorkShift, RegularWorkingHour from working-hours.json.
5. Unit tests for every rule and the precedence.

AGGREGATIONS

E4.7 Hourly aggregation of transports

As a Plant User, I want hourly transport counts between areas so that the flow matrix and per-hour
charts stay fast on long ranges.

1. Transport legs only; descriptions normalised with descriptionKeywordMap (first contained keyword
   wins).
2. Count per full hour of TimeStart grouped by Plant, AreaSource, AreaDestination,
   DescriptionSource, DescriptionDestination → AggregatedOrders(Count, TimeStart, TimeEnd);
   Id =
   "{Plant}_{DescriptionSource}_{DescriptionDestination}_{AreaSource}_{AreaDestination}\_{yy
   yyMMddHHmm}" (differs from POC: areas added to the key).
3. Boundary hours are recomputed from all legs of that hour and upserted as a whole (differs from
   POC: incomplete hours dropped).

E4.8 ARC utilisation grid

As a Plant User, I want to see per ARC and hour how much time was spent transporting, driving
empty, driving to parking and parking.

1. Per ArcId and utilizationResolutionMinutes bucket: seconds of Transport, Empty, ParkingDrive,
   Parking clipped to the bucket; NotDefined = bucketSeconds − sum, never negative; overlapping
   legs of one ARC truncated so time counts once.
2. Row: Id = "{Plant}_{ArcId}_{yyyyMMddHHmm}", Resolution, ArcId, TimeStart, TimeEnd, five
   second-columns, calendar; boundary buckets recomputed fully on the next run.
3. Unit tests: leg spanning buckets, overlapping legs, ARC without legs (no row).

E4.9 Order tables, views and data quality

As a Dashboard Designer, I want stable, indexed tables and views and visible data quality so that
dashboards are fast and trustworthy.

1. Tables Orders, AggregatedOrders, ArcUtilization with all columns of E4.5–E4.8; indexes on
   (TimeStart), (Plant, TimeStart), Action, AreaSource, AreaDestination, ArcId; views v_Orders,
   v_AggregatedOrders, v_ArcUtilization; data dictionary complete.
2. Per run the counters rowsRead, per table inserted/updated/deleted, droppedSentinelRows,
   unmappedAddresses (top 50 samples), incompleteLegs, negativeDurations appear in run history,
   metrics and AnalysisRunCompleted.
3. Idempotency integration test on the SEAS seed: same window twice → identical tables; two
   overlapping windows → same as one covering window; legs no longer produced by the source are
   deleted inside the window.
4. Performance: a 48 h run on the performance dataset finishes within 5 min.

E4.10 Reference comparison with the POC (one-off)

Enabler: the .NET results are compared with the Python POC on a shared SEAS snapshot so that
intended deviations are explicit.

1. docs/poc-comparison-orders.md per table: row counts, matching rows by Id, differences explained
   by the marked deviations or identified POC defects.
2. Unexplained differences are raised with Servus before the epic is closed.

DASHBOARDS

E4.11 Default dashboard "Orders and ARC utilisation"

As a Plant User, I want an overview of transports, reject flows, fleet size and ARC utilisation so that I
can assess the plant's material flow.

1. Items: KPI cards Transports (count of Transport legs), NIO transports (IsNio = 1), Active ARCs
   (distinct ArcId), each with sparkline and comparison to the previous equal period; charts
   Transports per hour and per day (v_AggregatedOrders); pivot Material flow matrix source ×
   destination area; stacked bar ARC utilisation per ARC (Transport, Empty, ParkingDrive, Parking,
   NotDefined as share of time); Order duration distribution by bucket.
2. Filters: date range (default last 7 days; presets 24 h / 7 d / 30 d), source/destination area, shift,
   regular working hours only, ARC.
3. Bound to the three views only; opens within 3 s on the performance dataset; culture not hard-coded
   (POC had **ast-ES** ); languages and palette are applied to all standard dashboards in E7.
4. Delivered as dashboards/standard/ seed file, marked standard, described in the user handbook
   section. The MVP graph of E2.4 is replaced by this dashboard.

E4.12 Standard dashboards: designer, protection and publish

As a Dashboard Designer, I want to create dashboards in the browser and publish them as standard
so that all Plant Users get them and upgrades keep them current.

1. Designer mode in the frontend for ServusPortal.Dashboard.Design: DevExpress designer with the
   single views-only data source, a text-box dashboard item for free text (custom item as in the POC),
   save, save-as, soft delete, Publish as standard; data inspector in designer mode only. Work-in-
   progress dashboards are stored in dashboards/custom/ (E3.11) and are visible to designers only.
2. Standard dashboards (dashboards/standard/) are read-only for Dashboard.View; a designer editing
   one is redirected to "Save as" unless using the explicit Publish action; deleting standard
   dashboards through the API is impossible.

3. POST /servus/analytics-bff/dashboards/{id}/publish marks a dashboard as standard (right
   Dashboard.Design), records version and publisher; Plant Users see standard dashboards only,
   listed first and marked in the list.
4. Installer/upgrade replaces dashboards/standard/ and merges the index only if the shipped version
   is newer and the installed file was not modified after publishing; conflicts are reported, never
   silently overwritten; dashboards/custom/ is never touched (executed in E9.3). The standard
   dashboards of the release package are produced by publishing in a Servus environment and
   copying the files into the package; the procedure is documented in docs/.

### 4.3 Milestone M3 – Messages and availability processed and dashboards available

#### Epic E5 – Add message and availability analysis and dashboards

Goal: the message/availability analysis of the POC (availability_analysis, messagesystem,
location_availability_analysis) in the .NET service, with all plant-specific behaviour (profile filter,
exclusions, originator types, merge gap) as JSON configuration, plus the default dashboard
"Messages and availability".

Source: SeasConfigDB.dbo.tblMes_Archive. Output: Messagesystem, ComponentAvailability,
LocationError, PlantError. Terminology: a message is an archived SEAS message with an originator
(the reporting component), a text number, a profile (severity class, e.g. BS_kg) and a start and end
time. The originator type is a class of component derived from keywords in the originator name. A
location is the plant position parsed from the message.

Level of detail: the order rules (E4) were taken from a detailed POC analysis; for the message
analysis the POC analysis is at summary level. E5.1 therefore fixes the exact rules from the POC code
before the business-rule stories start. Where a value below is marked (confirm in E5.1) it is Servus's
expectation, to be verified against the POC.

RULES FROM THE POC

E5.1 Rule extraction from the POC (messages)

Enabler: the exact message rules of the POC are documented and confirmed so that E5.3 _–_ E5.7
implement agreed behaviour, not guesses.

1. docs/rules-messages.md documents from the POC code and the committed plant configurations:
   source columns of tblMes_Archive used (identity, originator, text number, profile, start/end
   timestamps), the profile filter semantics, all originator and text-number exclusions found per plant,
   the originator-type keyword list, the location parsing rule, the merge algorithm for location and plant
   errors, the columns and keys of the four output tables, and the retention values from the POC
   table_config.csv.
2. Every intended deviation is listed with the marker (differs from POC); the list is reviewed and
   confirmed by Servus before E5.3 starts.
3. The SEAS test seed (E1.3) is extended by a SeasConfigDB subset with tblMes_Archive data
   covering overlapping, adjacent and boundary-crossing messages; a performance dataset for
   messages is defined.

CUSTOMISABLE DATA MAPPINGS (JSON CONFIGURATION)

E5.2 Message analysis settings **messages.json**

As a Servus Integration Engineer, I want the message rules that differ per plant configurable so that
no plant-specific SQL is needed.

1. Keys with defaults: sourceTable (tblMes_Archive), profileFilter (["BS_kg"]),
   originatorTypeKeywords (keyword → originator type; POC originator_type.csv),
   excludedOriginators (list, default empty), excludedTextNumbers (list, default empty),
   mergeGapSeconds (15) (differs from POC: hard-coded), locationParsing (parameters of the rule
   fixed in E5.1).

2. Schema shipped; missing file means defaults; an empty exclusion list logs one informational
   message per run so that a forgotten plant configuration is visible.
3. Import tool converts the POC originator_type.csv and the per-plant exclusion SQL of at least one
   committed plant into messages.json; the Varta UNION variant is not supported (S3).
4. Schedule defaults for the message analysis in analytics.json: every 15 min, lookback 72 h
   (confirm in E5.1; long-lived messages need a longer lookback than orders).

DEFAULT DATA MAPPINGS (MESSAGE ANALYSIS BUSINESS RULES)

E5.3 Read archived messages

As a Servus Integration Engineer, I want the service to read the archived messages of a window from
the configured table so that the analysis works without plant-specific SQL.

1. Reads messages whose interval overlaps [from, to) from sourceTable, applying profileFilter,
   excludedOriginators and excludedTextNumbers in the parameterised query; table name from
   configuration; read isolation level as decided in the ADR of E4.4.
2. Messages that start before from or end after to are read completely so that availability seconds
   and merges at the window boundaries are correct; messages still open (no end time) are treated as
   ending at to and recomputed on the next run.
3. Rows with null or sentinel ( 0001 - 01 - 01 ) timestamps are dropped and counted
   (droppedInvalidTimestamps); excluded messages are counted (excludedMessages).

E5.4 Originator type, location and the message table

As a Plant User, I want every message classified by component type and location so that I can
analyse errors per component and area.

1. OriginatorType = type of the first matching keyword of originatorTypeKeywords in the originator
   name; no match → -, counted with the distinct originators as samples (unmappedOriginators).
2. Location and Area parsed from the message per the rule of E5.1; unparsable → -, counted.
3. Every message is written to Messagesystem with originator, originator type, text number, text, profile,
   location, area, TimeStart, TimeEnd, Duration (seconds, null if negative and counted
   negativeDurations), calendar enrichment as in E4.6 AC4 (shared component), and a deterministic
   Id derived from the SEAS message identity (defined in E5.1).

E5.5 Component availability per hour

As a Plant User, I want to see per component and hour how long it was not available so that I can find
the weak components.

1. Per originator (component) and full hour: NotAvailable = seconds covered by the union of the
   component's message intervals clipped to the hour (overlapping messages counted once);
   Available = 3600 − NotAvailable, never negative.
2. Row in ComponentAvailability: Id = "{Plant}_{Originator}_{yyyyMMddHHmm}", originator,
   originator type, TimeStart, TimeEnd, Available, NotAvailable, calendar; no row for a component
   without messages in the hour (confirm in E5.1).
3. Boundary hours are recomputed from all messages of the hour and upserted whole.
4. Unit tests: message spanning several hours, overlapping messages of one component, message
   open at window end.

E5.6 Location and plant error roll-up

As a Plant User, I want overlapping and adjacent messages merged into error periods per location
and for the whole plant so that I can see how long the plant was disturbed.

1. Per location, messages that overlap or follow each other within mergeGapSeconds are merged into
   one LocationError interval: TimeStart (earliest start), TimeEnd (latest end), Duration, MessageCount,
   distinct originators and text numbers; Id = "{Plant}_{Location}_{TimeStart:yyyyMMddHHmmss}".
2. Location errors of the plant are merged with the same rule into PlantError intervals; Id =
   "{Plant}\_{TimeStart:yyyyMMddHHmmss}".
3. Intervals touching the window boundaries are recomputed from all contributing messages on the
   next run (upsert of the interval; a previously written interval that is extended is updated, not
   duplicated).
4. Merge counts are reported (mergedMessages); unit tests: overlapping, adjacent within gap, adjacent
   beyond gap, chain across the window boundary.

TABLES, QUALITY AND VERIFICATION

E5.7 Message tables, views, data quality and retention

As a Dashboard Designer, I want stable, indexed tables and views for messages and availability with
visible data quality.

1. Tables Messagesystem, ComponentAvailability, LocationError, PlantError with the columns of
   E5.4–E5.6 following the table conventions (E2.1 AC2); indexes on (TimeStart), (Plant,
   TimeStart), Originator, OriginatorType, Location; views v_Messagesystem,
   v_ComponentAvailability, v_LocationError, v_PlantError; data dictionary extended.
2. Per run the counters rowsRead, per table inserted/updated/deleted, droppedInvalidTimestamps,
   excludedMessages, unmappedOriginators (top 50), negativeDurations, mergedMessages appear in
   run history, metrics and AnalysisRunCompleted.
3. Idempotency integration test on the seed: same window twice → identical tables; overlapping
   windows → same as one covering window; intervals no longer produced by the source are deleted
   inside the window.
4. Retention defaults in analytics.json: Messagesystem 60 d, ComponentAvailability 730 d,
   LocationError 730 d, PlantError 730 d (confirm against the POC _table_config.csv_ in E5.1).
5. Performance: a 72 h run on the message performance dataset finishes within 5 min.

E5.8 Reference comparison with the POC (one-off)

Enabler: the .NET results are compared with the Python POC on a shared SEAS snapshot so that
intended deviations are explicit.

1. docs/poc-comparison-messages.md per table: row counts, matching rows by Id, differences
   explained by the listed deviations or identified POC defects.
2. Unexplained differences are raised with Servus before the epic is closed.

DASHBOARDS

E5.9 Default dashboard "Messages and availability"

As a Plant User, I want an overview of plant disturbances, component availability and message hot
spots so that I can see where the plant loses time.

1. Content (proposal; the Dashboard Designer confirms or adjusts the item list before
   implementation): KPI cards Plant availability (1 − PlantError seconds / selected period),
   Messages (count in v_Messagesystem), Components with errors (distinct originators), each with
   comparison to the previous equal period; chart Component availability per hour (from
   v_ComponentAvailability); chart Plant error time per day (from v_PlantError); bar Top 10
   components by not-available time; chart Messages per hour by originator type; table Longest
   location errors (location, start, duration, message count).
2. Filters: date range (default last 7 days; presets 24 h / 7 d / 30 d), originator type, location/area,
   shift, regular working hours only.
3. Bound to the message views (E5.7) only; opens within 3 s on the message performance dataset;
   culture not hard-coded (languages and palette are applied to all standard dashboards in E7).
4. Delivered as dashboards/standard/ seed file, marked standard, documented in the user handbook
   section.

### 4.4 Milestone M4 – Assistant analysis processed and dashboards available

#### Epic E6 – Add assistant analysis and dashboards

Goal: the assistant analyses of the POC (assistant_analysis, assistant_and_utilization_analysis,
assistant_analysis_sql, traffic_monitoring_analysis, cycle_counter) in the .NET service, with
instances and mappings as JSON configuration, plus the default dashboard "Assistants".

Source: SeasLogDB.dbo.Logs (assistant log events), SeasConfigDB.dbo.tblAss_Object (instance
number → name), SeasPathDB.dbo.Vertex (vertex → description). Output: AssistantArcData,
AssistantMovementData, AssistantUtilization, AggregatedAssistantData, TrafficMonitoring,
CycleCounter. Terminology: an assistant is a lift or junction instance identified by its instance number.
A sequence is one ARC passing through an assistant: Preregistration → Registration → DriveIn →
OnPosition → Movement → DriveOut → Deregistration. An empty movement is an assistant
movement without an ARC.

Level of detail: as for the message analysis, E6.1 fixes the exact event patterns and rules from the
POC code before the business-rule stories start. Values marked (confirm in E6.1) are Servus's
expectation.

RULES FROM THE POC

E6.1 Rule extraction from the POC (assistants)

Enabler: the exact assistant rules of the POC are documented and confirmed so that E6.3 _–_ E6.8
implement agreed behaviour.

1. docs/rules-assistants.md documents from the POC code and configurations: the Logs columns
   used, how instances and ARCs are identified in log rows, the message pattern per sequence
   phase and for empty movements, the instance-type keywords, the vertex-description → area regex
   semantics (path_mapping.csv), the utilisation window definition, the traffic-monitoring pair and
   travel-time definition, the cycle-counter originators ( 4109 , 4111 , 4112 , 4116 ) and "movement started"
   pattern, the columns and keys of the six output tables, and the POC retention values.
2. Intended deviations are listed with (differs from POC) and confirmed by Servus before E6.3 starts.
3. The SEAS test seed is extended by SeasLogDB.Logs, tblAss_Object and Vertex subsets covering
   complete, incomplete, out-of-order and boundary-crossing sequences; a performance dataset for
   assistants is defined.

CUSTOMISABLE DATA MAPPINGS (JSON CONFIGURATION)

E6.2 Assistant analysis settings **assistants.json**

As a Servus Integration Engineer, I want assistant instances and mappings configurable so that a
plant's lifts and junctions are analysed without code changes.

1. Keys: instances (list of { instanceNumber, name?, type? }; POC instance_numbers.csv;
   mandatory for the assistant analysis), instanceTypeKeywords (name keyword → Lift | Junction),
   vertexAreaPatterns (ordered list of { pattern, area } regexes on the vertex description; first
   match wins; POC path_mapping.csv), utilizationResolutionMinutes (60),
   cycleCounterOriginators ([4109, 4111, 4112, 4116]), trafficBaselineResetAt (optional
   timestamp; baselines observed before it are discarded).

2. Schema shipped (rejects duplicate instance numbers and invalid regexes); missing mandatory file
   skips the assistant analysis with a clear error.
3. Import tool converts the POC instance_numbers.csv and path_mapping.csv of at least one
   committed plant.
4. Schedule defaults in analytics.json: every 15 min, lookback 48 h.

DEFAULT DATA MAPPINGS (ASSISTANT ANALYSIS BUSINESS RULES)

E6.3 Read assistant log events

As a Servus Integration Engineer, I want the service to read the assistant events of a window for the
configured instances so that sequences can be reconstructed.

1. Reads Logs rows of [from, to) for the configured instances and the event patterns of E6.1 with a
   parameterised query; resolves instance names via tblAss_Object and vertex descriptions via
   Vertex; log rows of unknown instances are ignored and counted (unknownInstances, with samples).
2. Look-behind: events of sequences that started before from and are still open are read so that the
   first sequences of the window are complete (differs from POC).
3. Vertices are mapped to areas with vertexAreaPatterns; unmapped → -, counted
   (unmappedVertices, with samples).
4. Data access behind the same interface as the other analyses.

E6.4 Sequence reconstruction per assistant

As a Plant User, I want each ARC passage through a lift or junction split into its phases so that I can
see where ARCs wait.

1. Per assistant and ARC, events are assembled into sequences in time order; each phase gets its
   timestamp; phase durations in seconds: Preregistration→Registration, Registration→DriveIn,
   DriveIn→OnPosition, OnPosition→Movement, Movement→DriveOut, DriveOut→Deregistration, plus
   Total.
2. Completed sequences are written to AssistantArcData: assistant (number, name, type), ARC,
   source and destination vertex and area, phase timestamps and durations, calendar; Id =
   "{Plant}_{Instance}_{ArcId}\_{Registration:yyyyMMddHHmmss}" (confirm in E6.1).
3. Assistant movements with and without ARC are written to AssistantMovementData: assistant,
   MovementType (Arc | Empty), TimeStart, TimeEnd, Duration, ARC if any, calendar; deterministic Id.
4. Incomplete or out-of-order sequences produce no row and are counted (incompleteSequences) and
   logged with assistant, ARC and missing phase (differs from POC: silently discarded).
5. Sequences crossing the window end stay open and are written when complete in a later run;
   sequences completed via look-behind are written only if not already present.
6. Unit tests: complete sequence, empty movement, missing phase, out-of-order events, sequence
   across the window boundary, two ARCs interleaved at one assistant.

E6.5 Assistant utilisation

As a Plant User, I want to see per assistant and hour how busy it was so that I can find bottlenecks.

1. Per assistant and utilizationResolutionMinutes bucket: ArcMovement and EmptyMovement seconds
   from AssistantMovementData clipped to the bucket (overlaps counted once), Idle = bucketSeconds

```
− ArcMovement − EmptyMovement, never negative; Utilization = 1 − Idle / bucketSeconds (POC
formula, kept).
```

2. Row in AssistantUtilization: Id = "{Plant}_{Instance}_{yyyyMMddHHmm}", assistant, TimeStart,
   TimeEnd, the three second-columns, Utilization, Passages (completed sequences in the bucket),
   calendar; boundary buckets recomputed fully on the next run.
3. Unit tests: movement spanning buckets, overlapping movements, assistant without movements in a
   bucket (row with Utilization = 0 (confirm in E6.1)).

AGGREGATIONS

E6.6 Hourly aggregation of passages per area pair

As a Plant User, I want hourly passage counts between areas per assistant so that flow charts stay
fast on long ranges.

1. From completed sequences: count per full hour of Registration grouped by Plant, Instance,
   AreaSource, AreaDestination → AggregatedAssistantData(Count, MeanTotalDuration,
   TimeStart, TimeEnd); Id =
   "{Plant}_{Instance}_{AreaSource}_{AreaDestination}_{yyyyMMddHHmm}".
2. Boundary hours recomputed from all sequences of the hour and upserted whole.

E6.7 Traffic monitoring with persisted baseline

As a Plant User, I want to see whether ARC travel times between assistants degrade over time so that
I can spot traffic problems.

1. For each ARC, the travel time between Deregistration at one assistant and Registration at the
   next assistant forms a traversal of the pair (source assistant, destination assistant) (confirm in
   E6.1).
2. The baseline per pair is the fastest traversal ever observed, persisted in a TrafficBaseline table
   and updated as a rolling minimum; trafficBaselineResetAt discards older observations (differs
   from POC: fastest within the queried window, KPI changed retroactively).
3. Per pair and hour: Count, MeanTravelTime, MedianTravelTime, Baseline, Ratio = MeanTravelTime /
   Baseline → TrafficMonitoring; Id =
   "{Plant}_{SourceInstance}_{DestinationInstance}\_{yyyyMMddHHmm}"; calendar; boundary hours
   recomputed.
4. Unit tests: first observation sets the baseline, faster later observation lowers it, reset discards, hour
   without traversals produces no row.

E6.8 Cycle counter

As a Plant User, I want movement counts per assistant so that maintenance can be planned by
cycles.

1. Per configured cycle-counter originator (instance) and full hour: count of "movement started"
   events from Logs → CycleCounter(Count, TimeStart, TimeEnd); Id =
   "{Plant}_{Instance}_{yyyyMMddHHmm}"; calendar.
2. Boundary hours recomputed and upserted whole.
3. The POC placeholders IsAfterLastService and the never-created MaintenanceInterval table are
   not implemented (differs from POC).

TABLES, QUALITY AND VERIFICATION

E6.9 Assistant tables, views, data quality and retention

As a Dashboard Designer, I want stable, indexed tables and views for assistants with visible data
quality.

1. Tables AssistantArcData, AssistantMovementData, AssistantUtilization,
   AggregatedAssistantData, TrafficMonitoring, CycleCounter, TrafficBaseline with the columns of
   E6.4–E6.8 following the table conventions; indexes on (TimeStart), (Plant, TimeStart),
   Instance, ArcId, AreaSource, AreaDestination; views v_AssistantArcData,
   v_AssistantMovementData, v_AssistantUtilization, v_AggregatedAssistantData,
   v_TrafficMonitoring, v_CycleCounter; data dictionary extended.
2. Per run the counters rowsRead, per table inserted/updated/deleted, unknownInstances (top 50),
   unmappedVertices (top 50), incompleteSequences, droppedInvalidTimestamps appear in run history,
   metrics and AnalysisRunCompleted.
3. Idempotency integration test on the seed: same window twice → identical tables; overlapping
   windows → same as one covering window; the baseline table is unaffected by re-runs of already
   observed windows.
4. Retention defaults in analytics.json: AssistantArcData and AssistantMovementData 30 d (POC),
   AssistantUtilization, AggregatedAssistantData, TrafficMonitoring 730 d, CycleCounter no
   automatic deletion (POC: never; configurable), TrafficBaseline no deletion.
5. Performance: a 48 h run on the assistant performance dataset finishes within 5 min.

E6.10 Reference comparison with the POC (one-off)

Enabler: the .NET results are compared with the Python POC on a shared SEAS snapshot so that
intended deviations are explicit.

1. docs/poc-comparison-assistants.md per table: row counts, matching rows by Id, differences
   explained by the listed deviations (incl. incomplete-sequence counting and the persisted baseline)
   or identified POC defects.
2. Unexplained differences are raised with Servus before the epic is closed.

DASHBOARDS

E6.11 Default dashboard "Assistants"

As a Plant User, I want an overview of lift and junction utilisation, ARC waiting times and traffic so that
I can find bottlenecks in the material flow.

1. Content (proposal; the Dashboard Designer confirms or adjusts before implementation): KPI cards
   Passages (completed sequences), Average utilisation (mean of v_AssistantUtilization),
   Cycles (sum of v_CycleCounter), each with comparison to the previous equal period; bar
   Utilisation per assistant; chart Passages per hour; stacked bar Phase durations per assistant
   (mean seconds per phase); chart Traffic ratio per pair over time (from v_TrafficMonitoring);
   pivot Passages by source × destination area; bar Cycles per instance per day.
2. Filters: date range (default last 7 days; presets 24 h / 7 d / 30 d), assistant, assistant type
   (lift/junction), area, shift, regular working hours only.
3. Bound to the assistant views (E6.9) only; opens within 3 s on the assistant performance dataset;
   culture not hard-coded (languages and palette are applied to all standard dashboards in E7).

4. Delivered as dashboards/standard/ seed file, marked standard, documented in the user handbook
   section.

### 4.5 Milestone M5 – Corporate identity, portal integration and setup done

#### Epic E7 – Apply Servus corporate identity

Goal: the frontend looks and reads like a Servus product in German and English.

E7.1 Servus look through SWL

As a Plant User, I want the Servus look so that Analytics is consistent with the portal.

1. Layout components, theme tokens and typography from @servus/angular-ui-library (Angular
   22); DevExtreme theme identical to the portal's (26.1); no leftover CLI or demo styling.
2. Servus palette (#009FE3 primary, #45B170 positive, #EA5045 negative, greys #939094, #C9C5CA,
   #605D62) applied to dashboards through the DevExpress palette hook without System.Drawing;
   order documented.
3. The app renders no own header, navigation or logout; the portal shell provides them. Only the
   dashboard area and its toolbar are styled by the app.

E7.2 German and English

As a Plant User, I want the app and the dashboards in my language.

1. DevExpress dashboard resources and app strings in German and English; number and date
   formats follow the locale.
2. Locale taken from the portal (token claims or portal message as provided by Servus); no own
   language switch.
3. Titles and captions of all standard dashboards (E4.11, E5.9, E6.11) in both languages.

#### Epic E8 – Portal integration and authentication

Goal: the portal embedding that has run manually on the test VM since E2 is completed and hardened
for customers, and every BFF and data-service endpoint is protected with real tokens and rights. The
automated registration by the installer is in E9.1.

E8.1 Authentication and authorization in BFF and data service

As a Servus Service Technician, I want every endpoint to require a valid portal token and the
appropriate right so that only authorised users reach dashboards, data and operations.

1. JWT bearer validation against the IdentityServer per Servus how-to (authority, audience); the
   tokens handed over by the portal shell are accepted.
2. Policies: Dashboard.View ← ServusPortal.Dashboard.Access; Dashboard.Design ←
   ServusPortal.Dashboard.Design; Analytics.Configure ← ServusPortal.Analytics.Configure.
   Dashboard read/data need View; create/save/delete/publish need Design; run and configuration
   endpoints of the data service need Configure (Servus Seas.Api policy stack).
3. 401/403 with problem details; no stack traces or connection strings in responses; the development
   bypass of E2.3 is off by default.

E8.2 Portal integration completed and hardened

As a Plant User, I want to open Analytics from the portal app switcher and stay logged in so that it
feels like part of the portal.

1. The full portal postMessage protocol as documented by Servus, extending the MVP subset of E2.4
   AC5: pageLoaded (with path) on every navigation, requestToken on start and on token expiry,
   logoutRequest, requestApps if the switcher is rendered inside the app; tokenUpdate inbound is used
   for all BFF and SignalR calls, including re-connection of the SignalR hub after a token refresh. An
   SWL package is used if Servus provides one.
2. Only accepts messages from the portal origins listed in assets/config.json; outside the portal
   iframe the app shows a "please open Analytics from the Servus Portal" page (development builds
   may enable a token stub behind a configuration switch for local work).
3. The app is hidden in the portal switcher for users without ServusPortal.Dashboard.Access (portal-
   side, guided by Servus); the manual registration procedure of E2.4 AC4 is updated to its final form
   and handed to E9.1 for automation.
4. End-to-end test against a portal shell emulator: token handover → list → open dashboard → filter
   → refresh → token refresh → logout.

#### Epic E9 – Setup and installation

Goal: Analytics is installed, updated and removed by the Servus Manager setup; Servus can operate
it without Heitec.

E9.1 Script-based installer

As a Servus Service Technician, I want Analytics installed by a script so that no manual steps are
needed.

1. NSIS section(s) following seassetup.nsi: copy both services, replace %%HOSTNAME%% and DB
   placeholders in appsettings.json, create the Windows Services with the configured account
   (sc.exe, delayed-auto, description), run the DbUp migration, copy the frontend bundle to the
   NGINX web root and write assets/config.json, write the portal appConfig.json entry and the
   NGINX location/proxy configuration; this automates the manual procedure of E2.4 AC4 / E8.2 AC3
   so that no manual portal step remains.
2. Silent-install parameters documented; installer produced by CI as a versioned artifact.

E9.2 First-time installation scenario

As a Servus Service Technician, I want a clean first installation to result in a working system.

1. Database created, migrations applied, configuration directory created with the sample configuration
   set if absent, standard dashboards seeded, services started, health green.
2. Verified on the test VM from a clean state; documented step list with expected results.

E9.3 Update scenarios

As a Servus Service Technician, I want updates to preserve customer data and configuration.

1. Backup of the Analytics DB before the update (script or documented prerequisite enforced by the
   installer).
2. Services stopped, files replaced, schema migrations applied forward-only, standard dashboards
   updated per E4.12 AC4, services started.
3. Configuration directory and dashboards/custom/ untouched; existing configuration files are never
   overwritten.
4. Rollback strategy documented (restore backup, reinstall previous version).

E9.4 Uninstall scenario

As a Servus Service Technician, I want an uninstall that removes the software but keeps the
customer's data.

1. Services stopped and removed, program files and frontend bundle removed, portal appConfig.json
   entry and NGINX configuration written by E9.1 removed.
2. Analytics DB and configuration directory kept; documented how to remove them deliberately.

E9.5 Integration into the Servus Manager setup

As a Servus Service Technician, I want Analytics to be part of the standard Servus Manager setup so
that it is installed like every other service.

1. The analytics installer sections are integrated into the Servus Manager setup (ports, service names
   and account per Servus assignment) or delivered as a component the setup includes; verified on
   the test VM with a complete Servus Manager installation.
2. Operations manual docs/operations.md: prerequisites, ports, accounts and DB permissions,
   configuration directory and files with defaults, portal registration and NGINX routing of the frontend,
   log locations and key events, health endpoints, telemetry, common failures and remedies.
3. Configuration guide docs/configuration-guide.md for the Servus Integration Engineer: creating
   analytics.json, areas.json, working-hours.json, orders.json, messages.json and
   assistants.json for a new plant, validating with the CLI, importing POC files.
4. Smoke-test checklist for the Servus Service Technician (under one hour): services running, health
   green, migration version, a manual run of each analysis for the last 24 h writes rows, each standard
   dashboard opens from the portal with the viewer right, designer hidden for viewer, filters work,
   refresh after a run, logs in the Servus Logger; each step with expected result and evidence.
