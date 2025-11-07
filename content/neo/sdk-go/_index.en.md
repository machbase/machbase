---
title: Go SDK
type: docs
weight: 65
---

Machbase-neo provides two types of Go client libraries for Go developers.
The first is the Go standard SQL driver compatible `machrpc`, and the other is the `machcli` package, which is a wrapper around a native C client library.

- `machcli` is a Go wrapper around a C implementation that communicates through the *native port*, which defaults to port `5656`.
- `machrpc` does not require CGo since it is a pure Go implementation. Since it relies on the gRPC layer for transportation, it requires TLS certification by default. The gRPC port is `5655`.

## Other programming languages

If you are using a programming language other than Go, consider using the HTTP API for the best flexibility. If you prefer not to use HTTP for database interactions, you can use gRPC by transpiling the proto file.

The latest `.proto` file is hosted on GitHub. Please [find it here](https://github.com/machbase/neo-server/tree/main/api/proto/machrpc.proto).

{{< callout type="warning" >}}
Since the gRPC interface provides low-level APIs, client programs must use them correctly. Improper usage may cause Machbase to malfunction.
{{< /callout >}}


## In this chapter

{{< children_toc />}}
