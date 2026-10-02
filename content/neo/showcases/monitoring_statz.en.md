---
title: Operations Metrics Dashboard
type: docs
weight: 949
---

Use the built-in NEO STATZ operations dashboard to see how Machbase Neo collects and displays its own runtime metrics.

{{< youtube CYw1bhzrwSQ >}}

This guide uses the built-in NEO STATZ operations dashboard to show how Machbase Neo collects and displays its own runtime metrics.

Open the dashboard from the REFERENCE panel to see 15 panels covering CPU and memory, network connections, connection pools, APPEND throughput, rollup delays, query execution, HTTP responses, and more.

The metrics are written to the `NEOSTATZ` table in the Machbase database every 60 seconds. Query the table in the SQL editor to inspect the values shown in the dashboard and confirm the collection interval.

No separate monitoring stack or metrics collector is required. Check server operations in the web interface as soon as Machbase Neo is installed.