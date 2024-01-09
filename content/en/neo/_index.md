---
title: machbase-neo
weight: 10
toc: false
---

✓ Performant timeseries database<br/>
✓ Scalable from Raspberry Pi to high-end servers<br/>
✓ Easy to install - instant download and run<br/>
✓ Easy to learn - familiar SQL with Tables and Columns<br/>
✓ Easy to write and query via **HTTP**, **MQTT** and **gRPC**<br/>
✓ Bridge to SQLite, PostgreSQL, MySQL, MSSQL, MQTT Broker<br/>

{{< button color="purple" href="./getting-started/">}} Get Started {{< /button >}}
{{< button color="green" href="./releases/">}} Download  {{< /button >}}
{{< label color="green" >}} LATEST <i>{{< neo_latestver >}}</i> {{< /label>}}

Machbase is the world's fastest timeseries database[^1] with a minimal footprint. It's an ideal solution for environments that require scalability, from small servers with limited resources like the Raspberry Pi to horizontally scaled clusters. Machbase Neo, built on Machbase, adds crucial features required for the IoT industry. It ingests and handles query data through various protocols, such as MQTT for direct data transfer from IoT sensors, and SQL via HTTP for data retrieval by applications.

{{< figure src="/images/interfaces.jpg" width="700" >}}

### API and Interfaces

- [x] HTTP : Applications and Sensors read/write data via HTTP REST API
- [x] MQTT : Sensors write data via MQTT protocol
- [x] gRPC : The first class API for extensions
- [x] SSH : Command line interface for human and batch process
- [x] WEB : User interface

### Data Transformation and Visualization

Data transformation and visualization language *TQL* is supproted out of the box.

- [TQL](/neo/tql) is the DSL for data transformation.
- [CHART()](/neo/tql/chart/) for the data visualization examples.

### Bridges

Integration with external systems

- [x] SQLite
- [x] PostgreSQL
- [x] MySQL
- [x] MS-SQL
- [x] MQTT Broker
- [ ] Kafka
- [ ] NATS


### Download 

{{< tabs items="Linux/macOS,Windows,Choose Manually">}}
    {{< tab >}}
    Paste the script below into the shell prompt for the latest version of the platform.

    ```bash
    sh -c "$(curl -fsSL https://machbase.com/install.sh)"
    ```
    {{< /tab >}}

    {{< tab >}}
    If GUI is preferred rather than command line, then execute `neow` included in the Windows release.

    Download the latest release for [Windows]({{< neo_releases_url >}}/download/{{< neo_latestver >}}/machbase-neo-{{< neo_latestver >}}-windows-amd64.zip)

    ![interfaces](/images/neow-win.png)
    {{< /tab >}}

    {{< tab >}}
    Find and download the file for the version and platform from the [releases](./releases/) page.
    {{< /tab >}}
{{< /tabs >}}


### Contributing

We welcome and encourage community contributions to documents and examples for other developers. Typo and broken link fixes are appreciated.


[^1]: [TPCx-IoT Performance Results](https://www.tpc.org/tpcx-iot/results/tpcxiot_perf_results5.asp?version=2)

