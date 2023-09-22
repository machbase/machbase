---
title: 'machbase-neo'
weight: 10
---

- ✓ Performant timeseries database
- ✓ Scalable from Raspberry Pi to high-end servers
- ✓ Easy to install - instant download and run
- ✓ Easy to learn - familiar SQL with Tables and Columns
- ✓ Easy to write and query via **HTTP**, **MQTT** and **gRPC**
- ✓ Bridge to SQLite, PostgreSQL, MySQL, MSSQL, MQTT Broker

{{<cards>}}
    {{<card link="./getting-started/" title="Get Started" icon="academic-cap">}}
    {{<card link="./releases/" title="Download" icon="download">}}
{{</cards>}}

> The latest version is {{< neo_latestver >}}

Machbase is the world's fastest timeseries database[^1] with a minimal footprint. It's an ideal solution for environments that require scalability, from small servers with limited resources like the Raspberry Pi to horizontally scaled clusters. Machbase Neo, built on Machbase, adds crucial features required for the IoT industry. It ingests and handles query data through various protocols, such as MQTT for direct data transfer from IoT sensors, and SQL via HTTP for data retrieval by applications.

{{< overview_interfaces >}}

### API and Interfaces

- [x] HTTP : Applications and Sensors read/write data via HTTP REST API
- [x] MQTT : Sensors write data via MQTT protocol
- [x] gRPC : The first class API for extensions
- [x] SSH : Command line interface for human and batch process
- [x] WEB : User interface

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

    ```sh
    sh -c "$(curl -fsSL https://neo.machbase.com/install.sh)"
    ```
    {{< /tab >}}

    {{< tab >}}
    If GUI is preferred rather than command line, then execute `neow` included in the Windows release.

    Download the latest release for [Windows]({{ site.releases_url }}/download/{{ .site.Params.latestNeoVer }}/machbase-neo-{{ site.latest_version }}-windows-amd64.zip)

    ![interfaces](/images/neow-win.png)
    {{< /tab >}}

    {{< tab >}}
    Find and download the file for the version and platform from the [releases](./releases/) page.
    {{< /tab >}}
{{< /tabs >}}


### Tutorials

[Tutorial Waves](./docs/tutorial-waves/00.index.md) tutorial is a good starting point.

[Raspberry PI as IoT server](./docs/tutorials/raspi-server.md) shows how to install machbase-neo on Raspberry PI and utilize it as an IoT server.

[Tutorials](./docs/tutorials/) section has more materials.

### Contributing

We welcome and encourage community contributions to documents and examples for other developers. Typo and broken link fixes are appreciated.


[^1]: [TPCx-IoT Performance Results](https://www.tpc.org/tpcx-iot/results/tpcxiot_perf_results5.asp?version=2)

