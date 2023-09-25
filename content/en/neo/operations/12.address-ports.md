---
title: IP Address and ports
type: docs
weight: 12
---

## Bind Address

machbase-neo runs and listens to only localhost by default for the security reason. If clients on the remote hosts need to read/write data from/to machbase-neo through network, it requires that machbase-neo starts with bind address option `--host <bind address>`.

To allow listening from all addresses, use `0.0.0.0`

```sh
machbase-neo serve --host 0.0.0.0
```

To allow listening from specific address, set the IP address of the host.

```sh
machbase-neo serve --host 192.168.1.10
```

## Listening Ports

There are more flag options for the protocol ports.

| flag            | default      | desc                                                      |
|:----------------|:-------------|:----------------------------------------------------------|
| `--mach-port`   | 5656         | machbase native port for JDBC/ODBC drivers                |
| `--grpc-port`   | 5655         | gRPC port                                                 |
| `--http-port`   | 5654         | HTTP port                                                 |
| `--mqtt-port`   | 5653         | MQTT port                                                 |
| `--shell-port`  | 5652         | for ssh, open `machbase-neo shell` prompt remotely        |

