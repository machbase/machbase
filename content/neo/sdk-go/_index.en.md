---
title: Go SDK
type: docs
weight: 65
---

Machbase-neo provides three types of Go client libraries for Go developers.
For best performance and cross-platform deployment, **`machgo` is the recommended client**.
`machcli` is currently kept for backward compatibility, but they may be marked as deprecated and removed in future releases.

- `machgo` <span class="badge-new">NEW!</span>(recommended) is a pure Go implementation for the *native port* (default `5656`) and provides an API compatible with `machcli`. [Learn more](/neo/sdk-go/machgo/)
- `machcli` is a Go wrapper around a C implementation that communicates through the *native port* (default `5656`). It remains available for backward compatibility.

{{< callout type="warning" >}}
`machcli` may be marked as deprecated in future releases and can be removed later.
Use `machgo` for new development whenever possible.
{{< /callout >}}

## Other programming languages

If you are using a programming language other than Go, consider using the HTTP API for the best flexibility.


## In this chapter

{{< children_toc />}}
