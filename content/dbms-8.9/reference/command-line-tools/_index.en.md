---
type: docs
title: '16.4 Command-Line Tool Reference'
weight: 40
toc: true
---

Machbase provides command-line tools for server administration, data import/export, and query
execution. This section is a quick reference to their options and usage.

## Tools

| Tool | Edition | Description |
|------|--------|------|
| [machadmin](./machadmin/) | Standard / Cluster | Server startup/shutdown, database creation/deletion, and license management |
| [machsql](./machsql/) | Standard / Cluster | Interactive SQL terminal |
| [machloader](./machloader/) | Standard / Cluster | Import/export of CSV and other text files |
| [csvimport / csvexport](./csvimport-csvexport/) | Standard / Cluster | Simple CSV import/export wrappers |
| [tagmetaimport](./tagmetaimport/) | Standard / Cluster | Bulk TAG table metadata import |
| [machclusterctl](./machclusterctl/) | Cluster | Cluster-wide startup, shutdown, and management |
| [machcoordinatoradmin](./machcoordinatoradmin/) | Cluster | Coordinator node management and cluster configuration |
| [machdeployeradmin](./machdeployeradmin/) | Cluster | Deployer node management |

## Common Connection Options

The following connection options apply to `machsql`. Option names and defaults vary by tool; check
the tool's option dictionary or `--help` output before using another tool. In particular, distinguish
`machadmin` server administration options from SQL client connection options.

| Option | Default | Description |
|------|--------|------|
| `-s`, `--server` | 127.0.0.1 | Server IP address |
| `-P`, `--port` | 5656 | Server port |
| `-u`, `--user` | SYS | Username |
| `-p`, `--password` | MANAGER | User password |

## Tool Location

Tools included in the installation package are in `$MACHBASE_HOME/bin/`.
Availability depends on the installed edition and package.

```bash
ls $MACHBASE_HOME/bin/
# machadmin  machsql  machloader  csvimport  csvexport  tagmetaimport  ...
```

If `$MACHBASE_HOME/bin` is in PATH, run each tool by name.

```bash
export PATH=$MACHBASE_HOME/bin:$PATH
machadmin -e
```
