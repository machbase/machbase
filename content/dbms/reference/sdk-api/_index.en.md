---
type: docs
title: '17.7 SDK API Reference'
weight: 70
toc: true
---

This section provides Machbase SDK API references by SDK type. Use each child
page for installation, connection, SQL execution, Append, and examples.

## Common Connection Information

| Item | Default | Description |
|------|---------|-------------|
| HOST | `127.0.0.1` | Machbase server host name or IP address |
| PORT | `5656` | Machbase server port (`PORT_NO` in `machbase.conf`) |
| USER | `SYS` | User ID |
| PASSWORD | `MANAGER` | User password |

## SDK References

| SDK | Description |
|-----|-------------|
| [CLI/ODBC](./cli-odbc/) | C/C++ CLI/ODBC APIs and examples |
| [JDBC](./jdbc/) | Java JDBC APIs and Append |
| [Python](./python/) | `machbaseapi` Python client |
| [Node.js / TypeScript](./node-js-typescript/) | `@machbase/ts-client` TypeScript client |
| [.NET Connector](./net-connector/) | UniMachNetConnector and ADO.NET APIs |
| [Go](./go/) | `machgo` native client and `database/sql` driver |

The REST API is documented separately in the [REST API Reference](../rest-api/).
