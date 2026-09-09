---
type: docs
title: '3.4 Upgrade'
weight: 40
toc: true
---

An upgrade is more than replacing executables: it verifies that existing data, configuration, and
applications retain their intended behavior on the new version. First confirm a supported version
transition, prepare a restorable backup, and define service-resumption criteria. Adjust the example
8.7.0 package names and paths to the distribution you received.

## Before upgrading

- Check compatibility between the current and target versions. A minor-version change can involve
  a different database file format.
- Take a backup before upgrading. See [backup procedures](/dbms/operations-configuration-recovery/backup-restore-mount/#backup).
- Identify clients with ongoing INSERT or Append work.

<a id="upgrade-check-870"></a>

### Machbase 8.7.0 pre-upgrade check

When upgrading from 8.5 to 8.7.0, identify the following dependencies and migrate them to supported
alternatives before replacing binaries.

1. Locate removed properties `HTTP_AUTH`, `HTTP_ENABLE`, `HTTP_MAX_MEM`, `HTTP_PORT_NO`,
   `RS_CACHE_*`, `STREAM_THREAD_COUNT`, and `STREAM_WAIT_MS` in the current configuration and
   compare them with the supported list. Remove obsolete properties and preserve supported ones.
   In particular, Cluster `HTTP_ADMIN_PORT` remains a management port; do not remove it simply
   because it matches `HTTP_*`.
2. Migrate applications calling `/machbase` or `/machiot` to a backend using a supported SDK.
3. Update SQL or operational scripts that invoke `STREAM_*` procedures or `FLUSH RESULT_CACHE`.
4. Migrate C/C++ applications using `machcli.h` and `MachCLI*()` to Machbase SQLCLI or ODBC.
   SQLCLI and ODBC are separate API sets.
5. Replace operational workflows and dashboards that depend on WebAdmin/MWA with command-line
   tools or separate applications.

See
[version compatibility](/dbms/reference/support-scope-constraints/compatibility-version/#removed-features-870)
for the complete list of removed and retained features.

## Upgrade paths

| Edition | Method | Procedure |
|---------|--------|-----------|
| Standard Edition | Stop the server and replace the package | [Standard upgrade](#standard-edition) |
| Cluster Edition | Restart Brokers and Warehouses sequentially | [Online upgrade](#cluster-edition-online) |
| Cluster Edition | Stop the entire cluster | [Full-stop upgrade](#cluster-edition-full-stop) |

For Cluster Edition, choose online or full-stop upgrade according to availability requirements.

---

<a id="standard-edition"></a>

## Standard Edition upgrade

Stop the server, replace the package, and restart. Apply this procedure only to supported version
transitions that can open the existing physical database files. If the transition requires data
conversion or export/import, follow the release-specific migration procedure first.

### Preparation

1. **Take and validate a backup.** Use a supported BACKUP command and verify restoration in a
   separate environment. Simply copying a live data directory does not establish a recoverable backup.
2. **Finish client activity.** Complete ongoing Append and INSERT operations and close connections.
3. **Record the current version:**

   ```bash
   machbased -v
   ```

### Procedure

#### 1. Stop the server

```bash
machadmin -s
# Machbase server shut down successfully.
```

<a id="2-기존-패키지-백업-선택"></a>

#### 2. Preserve the existing package and configuration

Retain the current configuration and license as well as executables and libraries in a separate
location. Check that the destinations below do not already contain an earlier backup.

```bash
cp -a "$MACHBASE_HOME/bin" "$MACHBASE_HOME/bin.bak"
cp -a "$MACHBASE_HOME/lib" "$MACHBASE_HOME/lib.bak"
cp -a "$MACHBASE_HOME/conf" "$MACHBASE_HOME/conf.bak"
```

Preserve `dbs/` and data under any separately configured `DBS_PATH`. These copies preserve
executables and configuration; they do not replace a database backup. Once the new version has
modified data, do not assume that restoring old binaries alone can recover the instance.
Use the backup restoration path you have validated.

#### 3. Extract and apply the new package

Extract the new package into a separate working directory and inspect its contents and configuration
changes first.

```bash
upgrade_stage=$(mktemp -d)
tar zxf machbase-SDK-8.7.0.official-LINUX-X86-64-release.tgz -C "$upgrade_stage"
```

Extraction alone does not replace executables in the existing installation. The following example
applies executables, libraries, and headers from a Standard tarball containing `bin/`, `lib/`,
and `include/`. Confirm that the server is stopped first. If any command fails, do not proceed
to server startup.

```bash
(
  set -e
  test -n "$MACHBASE_HOME"
  test -x "$upgrade_stage/bin/machbased"
  test -d "$upgrade_stage/lib"
  test -d "$upgrade_stage/include"
  test -d "$MACHBASE_HOME/bin"
  test -d "$MACHBASE_HOME/lib"
  test -d "$MACHBASE_HOME/include"
  cp -a "$upgrade_stage/bin/." "$MACHBASE_HOME/bin/"
  cp -a "$upgrade_stage/lib/." "$MACHBASE_HOME/lib/"
  cp -a "$upgrade_stage/include/." "$MACHBASE_HOME/include/"
  "$MACHBASE_HOME/bin/machbased" -v
)
```

Preserve the existing `conf/machbase.conf`, license, and data at the actual `DBS_PATH`, and merge
new configuration entries into the existing configuration. Copying replaces distribution files
with matching names but does not automatically remove files present only in the old version.
Select SDK and plugin files explicitly for the new version, and consult the release instructions
for additional replacements and removals. Start the server only after checking the reported binary
version and reviewing the configuration.

#### 4. Start the server

```bash
machadmin -u
# Machbase server started successfully.
```

#### 5. Check the version

```bash
machbased -v

# Connect to the server.
machsql -s 127.0.0.1 -P 5656 -u SYS -p MANAGER
```

```sql
SELECT EDITION, BINARY_DB_MAJOR_VERSION, BINARY_DB_MINOR_VERSION FROM V$VERSION;
```

### Important constraints

- Do not delete `dbs/` or initialize it with `machadmin -d`.
- Minor-version upgrades may require database file migration. Read the release notes.
- On Windows, stop the Machbase service before applying the new package or installer.

---

<a id="cluster-edition"></a>

## Cluster Edition upgrade

Choose a method according to the required service interruption.

| Method | Service impact | Suitable situation |
|--------|----------------|--------------------|
| [Online upgrade](#cluster-edition-online) | Sequential Broker/Warehouse restarts | Replacing only Brokers and Warehouses |
| [Full-stop upgrade](#cluster-edition-full-stop) | Cluster outage | A maintenance window is available, or a major-version transition is required |

### Common precautions

- Do not run DDL or DELETE during the upgrade.
- Do not concurrently add, start, stop, or remove nodes.
- Online upgrade targets Brokers and Warehouses. Use full-stop upgrade to replace Coordinators,
  Deployers, or Lookups as well.
- Take a backup before upgrading.

---

<a id="cluster-edition-online"></a>

### Online upgrade

Upgrade Brokers and Warehouses sequentially while the cluster is running. If all binaries,
including Coordinator, Deployer, and Lookup, must be replaced, use
[full-stop upgrade](#cluster-edition-full-stop).

#### Procedure

##### 1. Change the package in cluster.yaml

Set `cluster.package.name` and `cluster.package.origin_path` to the new package. When package
contents change, assign distinct names to both the package and archive file.

```yaml
cluster:
  package:
    name: machbase-v8.7.0
    origin_path: /home/machbase/packages/machbase-cluster-8.7.0.official-LINUX-X86-64-release.tgz
```

`registered_path` is the Coordinator package-repository path recorded by `machclusterctl export`.
Use `origin_path` to specify the upgrade archive.

##### 2. Inspect the execution plan

```bash
machclusterctl upgrade -f cluster.yaml --online --dry-run --verbose
```

##### 3. Run the online upgrade

```bash
machclusterctl upgrade -f cluster.yaml --online --yes --verbose
```

Omitting `--online` also selects online mode, but specifying it makes the operational procedure
explicit.

##### 4. Check overall status

```bash
machclusterctl status
```

#### Manual upgrade reference

When calling `machcoordinatoradmin --upgrade-node` directly, specify both the target node and the
package name.

```bash
machcoordinatoradmin --upgrade-node=192.168.1.11:5401 --package-name=machbase-v8.7.0
```

Limit online targets to Brokers and Warehouses. If only one Broker remains, upgrading it can
interrupt client connections for that period.

Online mode avoids stopping the entire cluster; it is not an HA-aware rolling upgrade that
guarantees uninterrupted service. Warehouse groups may temporarily become read-only, so validate
application reconnection, retry handling, and write delays. Use full-stop mode if protocol
compatibility changes or binaries for every role must be aligned.

Check the role-specific states and versions of all target nodes, then validate representative
queries, input, and replication.

---

<a id="cluster-edition-full-stop"></a>

### Full-stop upgrade

Stop the entire cluster and upgrade all nodes. Use this method when all binaries, including
Coordinator, Deployer, and Lookup, must be replaced or when the database file format changes.

#### Procedure

##### 1. Finish client activity

Verify that all INSERT, Append, and SELECT work has completed.

##### 2. Change the package in cluster.yaml

Set `cluster.package.name` and `cluster.package.origin_path` to the new package. There must be no
pending topology changes, such as node additions, removals, or port changes. Apply topology changes
with `apply` before running the upgrade.

`machclusterctl upgrade --full-stop` replaces the package in every node home, including
Coordinator and Deployer. Set `origin_path` to a complete Cluster package containing
`machcoordinatoradmin` and `machdeployeradmin`.

##### 3. Inspect the execution plan

```bash
machclusterctl upgrade -f cluster.yaml --full-stop --dry-run --verbose
```

##### 4. Run the full-stop upgrade

```bash
machclusterctl upgrade -f cluster.yaml --full-stop --yes --verbose
```

With the entire cluster stopped, `machclusterctl` extracts the package into a temporary staging
location and applies it to the node homes.

#### Manual deployment reference

For manual deployment, register the new package with the Coordinator.

```bash
machcoordinatoradmin --add-package=machbase-v8.7.0 \
  --file-name=/home/machbase/packages/machbase-cluster-8.7.0.official-LINUX-X86-64-release.tgz
```

Stop nodes in this order: Warehouse → Broker → Lookup → Deployer → Coordinator.

```bash
machcoordinatoradmin --shutdown-node=192.168.1.13:5501
machcoordinatoradmin --shutdown-node=192.168.1.14:5501
machcoordinatoradmin --shutdown-node=192.168.1.11:5401
machcoordinatoradmin --shutdown-node=192.168.1.10:5301
machdeployeradmin --shutdown
machcoordinatoradmin --shutdown
```

When replacing packages in node homes, preserve `conf/machbase.conf` and the `dbs/`, `meta/`,
and `package/` directories. Extract the package in a separate working location, then replace
files while excluding the paths that must be retained.

Start nodes in this order: Coordinator → Deployer → Lookup → Broker → Warehouse.

```bash
machcoordinatoradmin --startup
machdeployeradmin --startup
machcoordinatoradmin --startup-node=192.168.1.10:5301
machcoordinatoradmin --startup-node=192.168.1.11:5401
machcoordinatoradmin --startup-node=192.168.1.13:5501
machcoordinatoradmin --startup-node=192.168.1.14:5501
```

After restarting, synchronize Broker and Warehouse package metadata with the new package name.

```bash
machcoordinatoradmin --upgrade-node=192.168.1.11:5401 --package-name=machbase-v8.7.0
machcoordinatoradmin --upgrade-node=192.168.1.13:5501 --package-name=machbase-v8.7.0
machcoordinatoradmin --upgrade-node=192.168.1.14:5501 --package-name=machbase-v8.7.0
```

##### 5. Check status

```bash
machclusterctl status
```

Before resuming service, verify Broker connections, representative reads and writes, replication,
license, and configuration as well as node status. Compare
[installation validation](../validation-checklist/) with the pre-upgrade record. Retain the previous
package, configuration, and backup until verification is complete.

#### Important constraints

- A major-version upgrade may change the database file format. Read the release notes and take a
  backup before upgrading.
- Do not delete or initialize `conf/machbase.conf`, `dbs/`, `meta/`, or `package/`.
