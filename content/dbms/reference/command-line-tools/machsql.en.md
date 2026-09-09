---
type: docs
title: '16.4.2 machsql'
weight: 20
toc: true
---

`machsql` is an interactive terminal client for SQL queries. It also supports SQL script execution,
saving results to files, and public key authentication.

## Options

```bash
machsql -h
```

| Short Option | Long Option | Default | Description |
|----------|---------|--------|------|
| `-s` | `--server` | 127.0.0.1 | Server IP address |
| `-P` | `--port` | 5656 | Server port |
| `-u` | `--user` | SYS | Username |
| `-p` | `--password` | MANAGER | User password |
| `-K` | `--auth-key-file` | - | Private key file for public key authentication (8.5+) |
| | `--auth-sig-scheme` | - | Authentication signature scheme: `ECDSA`, `RSA_PKCS1_V15`, or `RSA_PSS` (8.5+) |
| `-f` | `--script` | - | SQL script file to execute |
| `-o` | `--output` | - | Query result output file |
| `-r` | `--format` | csv | Output format, such as `csv` or `json` |
| `-z` | `--timezone` | - | Timezone, such as `+0900` or `-1230` |
| `-n` | `--nls` | - | NLS settings |
| `-c` | `--connstr` | - | Additional connection parameter string (6.1+) |
| `-D` | `--database` | `MACHBASEDB` | Logical database to use immediately after connection (8.7.0 Standard) |
| `-i` | `--silent` | - | Run without the copyright banner |
| `-v` | `--verbose` | - | Verbose output |
| `-x` | `--testing` | - | Run in test mode |
| `-h` | `--help` | - | Display options |

## Connection Examples

Basic connection:

```bash
machsql -s 127.0.0.1 -u SYS -p MANAGER
machsql --server=localhost --user=SYS --password=MANAGER
```

Specify a port:

```bash
machsql -s 192.168.1.10 -P 5656 -u SYS -p MANAGER
```

Run a SQL script:

```bash
machsql -s 127.0.0.1 -u SYS -p MANAGER -f create_tables.sql
```

Specify a timezone:

```bash
machsql -s 127.0.0.1 -u SYS -p MANAGER -z +0900
machsql -s 127.0.0.1 -u SYS -p MANAGER -z -1230
```

Save results to a file:

```bash
machsql -s 127.0.0.1 -u SYS -p MANAGER -o result.csv -f query.sql
```

## Public Key Authentication (Machbase 8.5+)

You can use public key challenge authentication instead of a password.

Connect with an ECDSA key:

```bash
machsql -s 127.0.0.1 -u app_user \
    -K /opt/machbase/keys/app_user_ecdsa.pem \
    --auth-sig-scheme=ECDSA
```

Connect with an RSA-PSS key:

```bash
machsql -s 127.0.0.1 -u app_user \
    -K /opt/machbase/keys/app_user_rsa.pem \
    --auth-sig-scheme=RSA_PSS
```

Supported key algorithms:

| Algorithm | Key Parameters | Default Signature Scheme |
|---------|-----------|--------------|
| ECDSA | P-256, P-384, P-521 | `ECDSA` |
| RSA | 2048, 3072, 4096 bits | `RSA_PKCS1_V15` |

## Additional Connection Parameters (6.1+)

Use `-c` to supply additional connection parameters.

```bash
machsql -s 127.0.0.1 -u SYS -p MANAGER -P 5656 \
    -c 'ALTERNATIVE_SERVERS=192.168.0.147:9209;CONNECTION_TIMEOUT=10'
```

You can also use an environment variable.

```bash
export MACHBASE_CONNECTION_STRING="ALTERNATIVE_SERVERS=192.168.0.148:8888;CONNECTION_TIMEOUT=3"
machsql -s 127.0.0.1 -u SYS -p MANAGER
```

The `-c` option takes precedence over the environment variable.

## Selecting a Logical Database

In Machbase 8.7.0 Standard Edition, use `-D` or `--database` to select the logical database
immediately after connection.

```bash
machsql -s 127.0.0.1 -u app_a -p 'AppA#1234' -D factory_a
machsql -s 127.0.0.1 -u app_a -p 'AppA#1234' --database=factory_a
```

In a `-c` connection string, specify `DATABASE=factory_a` or its compatibility alias,
`DBNAME=factory_a`. If `-D` and the connection string specify different databases, the connection
is rejected. Specify the database once or use the same value. After connecting, verify the actual
server catalog with the following SQL.

```sql
SELECT CURRENT_DATABASE();
SHOW CURRENT DATABASE;
```

## machsql Built-in Commands

These commands are available at the machsql prompt (`Mach>`).

| Command | Description |
|------|------|
| `SHOW TABLES` | List all tables |
| `SHOW TABLE table_name` | Display column and index information for a table |
| `SHOW INDEXES` | List all indexes |
| `SHOW INDEX index_name` | Display a specific index |
| `SHOW INDEXGAP` | Display index build gap information |
| `SHOW LSM` | Display LSM index build information |
| `SHOW TABLESPACES` | List all tablespaces |
| `SHOW TABLESPACE name` | Display a specific tablespace |
| `SHOW STORAGE` | Display disk usage per table |
| `SHOW STATEMENTS` | List queries registered on the server |
| `SHOW USERS` | List users |
| `SHOW LICENSE` | Display license information |
| `SHOW DATABASES` | List active/mounted databases |
| `SHOW CURRENT DATABASE` | Display the current session database |
| `SHOW LAST ROWID` | Display the ROWID of the most recent successful single-row INSERT |
| `SHOW LASTID` | Same as `SHOW LAST ROWID` |

### Checking the Last INSERT's ROWID

In Machbase 8.7.0 Standard Edition, you can check the inserted row's ROWID immediately after a
single-row `INSERT ... VALUES`.

```sql
INSERT INTO orders(item) VALUES('pump');
SHOW LAST ROWID;
```

```text
Last ROWID : 2048
```

`SHOW LASTID` returns the same value. When no ROWID is available, the output is `NULL`, not `0`.
Do not reuse the previous value after a failed INSERT, batch/Append/loader operation,
`INSERT ... SELECT`, UPSERT, or reconnection. Non-INSERT statements such as SELECT and COMMIT
preserve the last value.

For per-table ROWID rules and SDK access, see
[ROWID and INSERT Result IDs](/dbms/reference/sql/rowid/).

## DESC and PRIMARY KEY Metadata

`DESC table_name` displays a `[ PRIMARY KEY ]` section after column and index information. It
shows the PRIMARY KEY name, column names, and key sequence. It covers declared primary keys in
TRANSACTION, LOOKUP, and VOLATILE tables, and `NAME` in TAG tables. Ordinary LOG tables display
no primary key rows.

```sql
DESC ACCOUNT;
```

This output is separate from SELECT result column metadata. To check whether a SELECT result
column is part of a primary key through an SDK, see
[PRIMARY KEY Metadata Support](/dbms/development-tools-integration/sdk-support-scope/#support-scope-sdk-primary-key-metadata).


## ARRAY Display and DESC

In Machbase DBMS 8.7.0, `DESC` displays ARRAY columns using canonical declarations such as
`INT32[3]` and `DECIMAL(12,4)[2]`. Query results use
`[value,null,value]`, where lowercase `null` represents an element NULL. If the entire column value
is NULL, it appears as ordinary SQL `NULL`.

```sql
SELECT ID, CHANNELS, ARRAY_LENGTH(CHANNELS), CHANNELS[1]
  FROM SENSOR_ARRAY
 ORDER BY ID;
```

For ARRAY declarations, NULL distinctions, and expressions, see
[Numeric ARRAY Types](/dbms/reference/sql/types/array/).

## Named Bind Parameter

You can use `:name` markers in `machsql` `PREPARE` SQL. Assign values to `$1`, `$2`, ... variables
in SQL occurrence order, rather than by name.

```sql
PREPARE INSERT INTO SENSOR_DATA (ID, NAME, VALUE)
        VALUES (:id, :name, :value);
$1 := 900;
$2 := 'machsql-client';
$3 := 72.125000;
EXECUTE;
PREPARE CLEAN;
```

Assign a value to each occurrence even when a name is repeated.

```sql
PREPARE SELECT ID, NAME
        FROM SENSOR_DATA
        WHERE ID = :id OR PARENT_ID = :id;
$1 := 900;
$2 := 900;
EXECUTE;
PREPARE CLEAN;
```

For marker naming syntax and occurrence ordering, see
[Named Bind Parameter Syntax](../../sql/syntax/named-bind-parameter-syntax/).


## Examples

```bash
# Connect interactively
machsql -s 127.0.0.1 -u SYS -p MANAGER

# Check tables after connecting
Mach> SHOW TABLES;

# Check table structure
Mach> SHOW TABLE sensor_data;

# Execute a SQL script and save results as CSV
machsql -s 127.0.0.1 -u SYS -p MANAGER \
    -f report.sql -o report_output.csv -i
```
