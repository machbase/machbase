---
title: Prometheus Monitoring Demo
type: docs
weight: 971
---

Collect Machbase Neo Prometheus metrics and open a Grafana dashboard using the steps for your operating system.

{{< icon "github" >}} https://github.com/machbase/neo-prom
<p/>

{{< youtube -pDn6ysLCh0 >}}

This demo uses Docker-based Prometheus to collect metrics from the Machbase Neo endpoint at `http://127.0.0.1:5654/debug/metrics` and monitor time-series data in a Grafana dashboard.

**Prerequisites**

- Docker and Docker Compose
- Ports 5654, 9090, and 3000 available
- The Machbase Neo executable