---
type: docs
title: '13.3 Configuration Management'
weight: 30
toc: true
---

Change one setting at a time. Record its current value, the reason for the change, how to apply
it, validation results, and rollback steps. For the full list of properties and defaults, see
the [Configuration Reference](/dbms/reference/configuration/configuration/) for your release.

<a id="file-config-configuration"></a>

## Configuration file

The default configuration file is `$MACHBASE_HOME/conf/machbase.conf`. A package or service
configuration may use another file, so check the startup command and actual environment.

Before changing a setting, record:

- File path, owner, and permissions
- The property's current value in the file and in `V$PROPERTY`
- Units and allowed range
- Whether it can change at runtime and whether a restart is required
- Affected nodes and instances
- Rollback value and validation SQL

Do not include passwords, AUTH KEYs, or license contents in ordinary configuration backups or work logs.

<a id="alter-start-restart-configuration-runtime"></a>

<a id="runtime-변경과-restart"></a>

## Runtime changes and restarts

`ALTER SYSTEM SET` changes only supported runtime properties. Do not attempt to change an
arbitrary property just because a sample command appears in the documentation.

```sql
SELECT NAME, VALUE FROM V$PROPERTY ORDER BY NAME;
```

1. Check the configuration reference for dynamic change support.
2. Define the maintenance scope and affected connections and queries.
3. Save the current value.
4. Change one property in a test environment or under a limited workload.
5. Compare response time, throughput, memory, I/O, and errors.
6. Write the chosen value to the configuration file so it persists after a restart.
7. After restarting, verify the setting with `V$PROPERTY` and a functional test.

<a id="parameters-configuration"></a>

<a id="property-찾기"></a>

## Find a configuration property

```sql
SELECT NAME, VALUE FROM V$PROPERTY
WHERE NAME LIKE 'PVO_CACHE%' ORDER BY NAME;
```

If you know the exact name, query with `NAME = '...'`. Do not configure a property by guessing
from a similar name.

<a id="memory-configuration"></a>

<a id="memory-설정"></a>

## Memory configuration

Budget together for process limits, table space and caches, ingestion buffers, and temporary
query and session memory. Leave memory for the OS and other processes on the same host.

- Resident and available memory under normal and peak workloads
- Whether swapping occurs and when it increases
- Concurrent queries, Appenders, and sessions
- Cache usage, including PVO, Min-Max, LOOKUP, and VOLATILE
- Temporary operations such as index creation, sorting, and aggregation

Do not apply a fixed ratio or sample byte value without validating it for your workload.

<a id="network-session-configuration"></a>

<a id="network와-session"></a>

## Network and sessions

Set listener addresses and ports, maximum sessions, and connection and query timeouts according
to application connection counts and failure isolation requirements. Verify firewall rules and
binding separately. Check for connection leaks and review pool settings before increasing the
session limit.

```sql
SELECT ID, USER_NAME, USER_IP, LOGIN_TIME, CLIENT_TYPE
FROM V$SESSION ORDER BY LOGIN_TIME DESC;
```

<a id="storage-checkpoint-configuration"></a>

<a id="storage와-checkpoint"></a>

## Storage and checkpoints

Settings for `DBS_PATH`, checkpoints, direct I/O, and I/O threads directly affect data location
and recovery time. Do not move production data files manually or guess alternative paths.

- Verify the actual data and backup paths and file systems.
- Compare checkpoint duration and device latency over the same period.
- Prepare outage and recovery procedures for settings that require a restart.
- After a change, verify normal restart, backup, and restore operations.

<a id="timezone"></a>

## Time zones

Configure consistent time zones for parsing and displaying time strings in the server, command-line
tools, and SDKs. Check epoch units and `DATETIME` precision separately, and test writing and reading
the same value.

<a id="timezone-server-configuration"></a>
<a id="timezone-timezone-server-configuration"></a>

<a id="server-timezone"></a>

## Server and session time zones

Distinguish the server's default time zone from the session time zone selected by the client.
Specify the time zone for application string input and output through supported connection
options. Verify it in a new connection with `SHOW TIMEZONE` and a sample `DATETIME` query. See
[Time Zone Configuration](/dbms/reference/configuration/configuration-timezone/) for setup.
Existing connections do not automatically change their session settings.

<a id="machsql-z"></a>
<a id="timezone-machsql-z"></a>

## machsql `-z`

```bash
"$MACHBASE_HOME/bin/machsql"   -s 127.0.0.1 -P 5656   -u APP_USER -p "$MACH_SAMPLE_PASSWORD"   -z +0900
```

Use sample values to verify that input and output strings are interpreted and displayed with
the specified offset.

<a id="machloader-z"></a>
<a id="timezone-machloader-z"></a>

## machloader `-z`

```bash
"$MACHBASE_HOME/bin/machloader"   -s 127.0.0.1 -P 5656   -u APP_USER -p "$MACH_SAMPLE_PASSWORD"   -z +0900 -i -t SENSOR_LOG -d /data/sensor.csv
```

Document both the time zone and date format of the source CSV.

<a id="connection-cli-jdbc-net-timezone"></a>
<a id="timezone-connection-cli-jdbc-net-timezone"></a>

<a id="sdk-connection-timezone"></a>

## SDK connection time zones

Option names differ by SDK. Check the driver's connection options in
[Chapter 11: Development and Application Integration](/dbms/development-tools-integration/).
Verify that the same time zone applies during writes, reads, and connection pool reuse.

## Change record

| Item | Record |
|------|------|
| Target | Host, instance, node, database |
| Change | Property, old value, and new value |
| Rationale | Baseline and target |
| Application | At runtime or after a restart |
| Validation | SQL, workload, and OS metrics |
| Rollback | Values, execution order, and responsible operator |

Do not treat unverified recommendations or defaults from older releases as current settings.
