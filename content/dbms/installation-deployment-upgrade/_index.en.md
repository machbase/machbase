---
type: docs
title: '3. Installation, Deployment, and Upgrade'
weight: 30
toc: true
---

This chapter prepares Machbase DBMS 8.7.0 for use and checks that it can accept and query data.
Installing a new server and upgrading a server that already contains data have different starting
points. First decide which features and deployment environment you need, then choose the matching
procedure.

The data models and Edition differences introduced in Chapter 2 also affect deployment. Check
Standard Edition support if you need TRANSACTION tables, Restore, or Mount. If you need distributed
storage and replication, plan Cluster node roles, networking, and recovery together.

## Choose an Installation Path

| Edition | Deployment structure | What to check |
|---|---|---|
| Standard Edition | One DBMS server handles SQL processing and storage | Required features and whether server resources can support ingestion, queries, and retention |
| Cluster Edition | Separate Coordinator, Deployer, Lookup, Broker, and Warehouse roles | Distribution groups, replication, communication paths, and node operations |

A single server is not limited to small data sets. Measure the required storage and performance
using representative data. Similarly, adding Cluster nodes does not make every query proportionally
faster. See [Edition Differences](/dbms/core-concepts/concepts-edition/#differences-standard-edition-cluster).

### Distinguish the Installation Components

| Component | Meaning | Examples to check |
|---|---|---|
| Distribution package | Executables, libraries, and sample configuration | Version, Edition, OS, and CPU architecture |
| Installation home | Executable and configuration location for a server or node | `MACHBASE_HOME`, `conf/machbase.conf` |
| Data storage path | Location where the DBMS reads and writes data | `DBS_PATH`, free space, and access permissions |
| Server instance or node | DBMS process running with that configuration | Process status, logs, and connection ports |
| Logical database | SQL object namespace selected by a connection | Current database, users, privileges, and tables |

Extracting a package, creating a new instance's database, starting the server, and creating tables
are separate steps. Do not run new-instance initialization against a home containing existing data.
The installation home and actual data path can also differ; check both before backup or upgrade.

A logical database selected through SQL is distinct from an installation home. See
[Multi-Database Operations](/dbms/operations-configuration-recovery/multi-database/) for selecting,
creating, and granting access to multiple databases.

## Installation Sequence

### Standard Edition

1. Use [Pre-Installation Preparation](./pre-install-preparation/) to check the package, server
   account, resources, and ports.
2. Prepare a dedicated home and environment following the procedure for your operating system.
   - [Linux — Tarball](./standard-edition/#linux-tarball)
   - [Linux — Docker](./standard-edition/#linux-docker)
   - [Windows — Package](./standard-edition/#windows-package)
3. Check configuration and data paths. If using a separate license, follow
   [License Installation](./pre-install-preparation/#license) before the first startup.
4. Create the new database and start the server as described in the selected installation procedure.
5. Use the [Validation Checklist](./validation-checklist/) to check the process, port, connection,
   version, license, and a small insert/query workflow.

A container deployment still needs the correct package version, a data volume, and write access
for the server account. The relationship between container startup and DBMS initialization depends
on the image, so follow its installation procedure.

### Cluster Edition

1. Review [Pre-Installation Preparation](./pre-install-preparation/) and
   [Cluster Environment Preparation](./cluster-edition/#preparation-environment-cluster-edition).
2. Decide each node's host, home, SQL/management/inter-node ports, and Warehouse replication group.
3. Prepare packages and licenses, then choose a deployment method.
   - [machclusterctl](./cluster-edition/#machclusterctl): configuration-based deployment and plan review
   - [Manual Installation](./cluster-edition/#manual-machcoordinatoradmin): stepwise registration and startup
4. Check role-specific node states and replication configuration, then connect to a Broker with SQL.
5. Use the [Validation Checklist](./validation-checklist/) to check ingestion/query behavior
   separately from replication state within a group.

A successful SQL connection does not establish that every replica is healthy. Different Warehouse
groups need not contain identical data. Continue with
[Cluster Operations](/dbms/operations-configuration-recovery/cluster/) for failure handling.

## Upgrade

For an existing system, follow [Upgrade](./upgrade/). Check compatibility of data files, SQL and
SDKs, configuration, licenses, and backup/recovery paths as well as the new executables. Do not
replace production settings with package samples or treat binary replacement alone as a completed
upgrade.

Keep baseline measurements and a backup from before the upgrade, and measure recovery time in an
isolated environment. Returning to an earlier version requires data and configuration that the
earlier version can read, not just its executables.

## Next Steps

Installation validation begins operational preparation. Use the
[Quick Start](/dbms/getting-started/quick-start/) to learn the SQL workflow, then model your data in
[Table Type Selection and Schema Design](../data-modeling-table-design/). Before production use,
prepare dedicated accounts, ingestion error handling, retention and backup, representative load
tests, and monitoring.

See the [Operations Checklist](/dbms/operations-configuration-recovery/checklist/) and
[Performance Tuning Approach](/dbms/performance-tuning/performance-approach/) for that process.
