---
type: docs
title: '3.5 Installation Validation Checklist'
weight: 50
toc: true
---

Validation goes beyond checking that a process is running. Actual clients must connect to the
intended server version and configuration, then write and read data within their permissions.
Work through server status, connectivity, version and license, SQL, and Cluster replication in order.

Record the execution host, installation home, connection address and port, time, and any errors for
each result. For an upgrade, compare these with the pre-upgrade record. `SYS`/`MANAGER` are initial
exercise credentials; substitute the actual account. Check that exercise table names do not collide
with existing business objects.

## Standard Edition checklist

### 1. Check the server process

```bash
machadmin -e
# Machbase server is running with PID(<pid>).
```

You can also inspect processes directly, but distinguish the target server from servers running
under other installation homes. Verify that `MACHBASE_HOME` identifies the instance being checked.

```bash
ps -ef | grep machbased | grep -v grep
```

### 2. Check the listening port

```bash
ss -tlnp | grep 5656
# LISTEN 0 128 0.0.0.0:5656 ...
```

Use a port-inspection tool appropriate for the operating system. Replace `5656` with the actual SQL
port and check that the listener uses the intended interface. A listening socket and a successful
remote client connection are separate checks; test connectivity from the application host too.

### 3. Test a machsql connection

```bash
machsql -s 127.0.0.1 -P 5656 -u SYS -p MANAGER
# MACHBASE_CONNECT_MODE=INET, PORT=5656 EDITION=STANDARD
# Mach>
```

If local connections succeed but remote connections fail, check the address, port, listener, and
firewall. For authentication errors, check the username, authentication method, and expiry status.
If connection succeeds but object access fails, check the current database and SQL permissions
separately.

### 4. Check the version

```sql
SELECT * FROM V$VERSION;
SELECT CURRENT_DATABASE();
```

### 5. Check the license

```sql
SELECT ID, ISSUE_DATE, TYPE, VIOLATE_STATUS FROM V$LICENSE_INFO;
```

Check that `VIOLATE_STATUS` is 0 and that the installed license type and validity period match the
operating plan. If a violation is reported, inspect `VIOLATE_MSG` and the server logs for its cause.

### 6. Test basic SQL

```sql
CREATE LOG TABLE check_test (id INTEGER, ts DATETIME);
INSERT INTO check_test (id, ts) VALUES (1, NOW);
SELECT id, ts FROM check_test;
DROP TABLE check_test;
```

Verify that one row with `id=1` and a timestamp is returned and that DROP succeeds. This checks
only basic LOG input. If the service uses TAG, TRANSACTION, Append, or other paths, also test
representative writes and queries using those tables and the actual SDK.

## Additional Cluster Edition checks

### 7. Check cluster node status

```bash
machcoordinatoradmin --cluster-status
# Compare node count and role-specific states with the deployment record.
```

### 8. Test a Broker connection

```bash
machsql -s 192.168.1.11 -P 5656 -u SYS -p MANAGER
```

```sql
SELECT * FROM V$NODE_STATUS;
```

Healthy state names differ by role: for example, Coordinator `primary`, Broker `leader`, and
Warehouse replication states. Do not compare every node against one status string. Check the
desired and actual states, group membership, and addresses against the deployment record.

### 9. Check data replication

First verify input and queries through a Broker, then inspect replication within Warehouse groups.
Reading a row through a Broker does not by itself prove that every replica has synchronized.

```sql
-- Insert through a Broker.
CREATE LOG TABLE cluster_check_test (id INTEGER, ts DATETIME);
INSERT INTO cluster_check_test (id, ts) VALUES (1, NOW);

-- Verify the input through the Broker.
SELECT COUNT(*) FROM cluster_check_test;
```

Direct SQL connections to Warehouses are an administrative replication diagnostic, not the normal
application path. Use `machcoordinatoradmin --cluster-status` to identify active and standby peers
in the same replication group. When needed, connect to each peer's native port with an
administrative account and compare the same query results. Do not assume nodes in different
Warehouse groups all contain the same rows.

After validation, remove the exercise table through the Broker connection.

```sql
DROP TABLE cluster_check_test;
```

---

<a id="문제-발생-시"></a>

## Acceptance criteria and troubleshooting

Proceed with service acceptance once server, connection, permission, representative SQL, and
required replication checks pass. To validate persistence, retain test data in a separate
validation environment and compare results before and after a normal restart. Do not reinitialize
a server containing business data merely to check installation.

If a check fails, preserve the first error and relevant logs, then investigate the failed stage.

- Server log: `$MACHBASE_HOME/trc/machbase.trc`
- See [operations and diagnostics](/dbms/operations-configuration-recovery/diagnosis-observability/).
