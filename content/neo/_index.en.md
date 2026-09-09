---
title: machbase-neo
weight: 10
toc: true
---

✓ Data platform for the Physical AI era, powered by a high-performance time-series database<br/>
✓ Scalable from edge devices (Raspberry Pi) to high-end servers<br/>
✓ Ingest, transform, and visualize data from the physical world<br/>
✓ Real-time monitoring of field data with dashboards<br/>
✓ Easy to install - instant download and run<br/>
✓ Easy to learn - familiar SQL with Tables and Columns<br/>
✓ Easy to write and query via **HTTP**, **MQTT**, and SQL<br/>
✓ Bridge to SQLite, PostgreSQL, MySQL, MSSQL, MQTT Broker, NATS<br/>

{{< button color="purple" href="./getting-started/">}} Get Started {{< /button >}}
{{< button color="green" href="./releases/">}} Download  {{< /button >}}
{{< label color="green" >}} LATEST <i>{{< neo_latestver >}}</i> {{< /label>}}

`machbase-neo` is a data platform for the Physical AI era, built on the high-performance
Machbase time-series database engine implemented in C.
It collects, stores, transforms, and visualizes time-series data generated in the physical
world—by robots, autonomous systems, smart factories, and edge devices—and serves it in a
form that applications and AI models can use directly for training and inference.
By combining real-time MQTT ingestion, HTTP-based SQL access, TQL transformation,
dashboards, and bridges to external systems, `machbase-neo` turns field data into
AI-ready datasets and services.
Its lightweight architecture runs across a wide range of environments, from edge devices
to high-end servers.

### Download 

{{< tabs >}}
    {{< tab name="Linux/macOS" icon="terminal">}}
    Paste the script below into the shell prompt for the latest version of the platform.

    ```bash
    sh -c "$(curl -fsSL https://docs.machbase.com/install.sh)"
    ```
    {{< /tab >}}

    {{< tab name="Windows" icon="desktop-computer">}}
    If GUI is preferred rather than command line, then execute `neow` included in the Windows release.

    Download the latest release for [Windows]({{< neo_releases_url >}}/download/{{< neo_latestver >}}/machbase-neo-{{< neo_latestver >}}-windows-amd64.zip)

    ![interfaces](/images/neow-win.png)
    {{< /tab >}}

    {{< tab name="Choose Manually" icon="globe">}}
    Find and download the file for the version and platform from the [releases](./releases/) page.
    {{< /tab >}}
{{< /tabs >}}


### Data Visualization

Data transformation and visualization language *TQL* is supported out of the box.

{{< figure src="/images/data-visualization.jpg" width="740" >}}

- [TQL](/neo/tql) is the DSL for data transformation.
- [CHART()](/neo/tql/chart/) for the data visualization.
- [SCRIPT()](/neo/tql/script/) for implementing custom logic.

Geodetic data visualization.

{{< figure src="/images/map-visualization.jpg" width="600" >}}

- [GEOMAP()](/neo/tql/geomap/) for map visualization.

### Dashboard

Realtime data monitoring on the fly.

{{< figure src="/images/dashboard.png" width="740" >}}

### API and Interfaces

- [x] HTTP : Applications and edge devices read/write data via [HTTP](/neo/api-http) REST API
- [x] MQTT : Robots, machines, and edge devices write data via [MQTT](/neo/api-mqtt) protocol (MQTT v3.1.1 & v5)
- [x] SSH : Command line user interface via [ssh](/neo/shell/#remote-access-via-ssh)
- [x] GUI : [Web](/neo/getting-started/webui/) user interface

{{< figure src="/images/interfaces.jpg" width="600" >}}

### Bridges

Integration with external systems

- [x] SQLite
- [x] PostgreSQL
- [x] MySQL
- [x] MS-SQL
- [x] MQTT Broker
- [x] NATS


### Contributing

We welcome and encourage community contributions to documents and examples for other developers. Typo and broken link fixes are appreciated.


[^1]: [TPCx-IoT Performance Results](https://www.tpc.org/tpcx-iot/results/tpcxiot_perf_results5.asp?version=2)

