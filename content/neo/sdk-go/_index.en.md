---
title: Go SDK
type: docs
weight: 65
---

Machbase-neo provides three types of Go client libraries for Go developers.
For best performance and cross-platform deployment, **`machgo` is the recommended client**.
`machcli` and `machrpc` are currently kept for backward compatibility, but they may be marked as deprecated and removed in future releases.

- `machgo` (recommended) is a pure Go implementation for the *native port* (default `5656`) and provides an API compatible with `machcli`.
- `machcli` is a Go wrapper around a C implementation that communicates through the *native port* (default `5656`). It remains available for backward compatibility.
- `machrpc` is a Go SQL-driver style client based on gRPC (default `5655`) and typically requires TLS certificates. It remains available for backward compatibility.

{{< callout type="warning" >}}
`machcli` and `machrpc` may be marked as deprecated in future releases and can be removed later.
Use `machgo` for new development whenever possible.
{{< /callout >}}

## Other programming languages

If you are using a programming language other than Go, consider using the HTTP API for the best flexibility. If you prefer not to use HTTP for database interactions, you can use gRPC by transpiling the proto file.

The latest `.proto` file is hosted on GitHub. Please [find it here](https://github.com/machbase/neo-server/tree/main/api/proto/machrpc.proto).

{{< callout type="warning" >}}
Since the gRPC interface provides low-level APIs, client programs must use them correctly. Improper usage may cause Machbase to malfunction.
{{< /callout >}}


## In this chapter

{{< children_toc />}}
