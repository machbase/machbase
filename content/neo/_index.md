---
title: 'Welcome to machbase'
date: 2023-09-21T14:41:53+09:00
---

#### Machbase Neo

- ✓ Performant timeseries database
- ✓ Scalable from Raspberry Pi to high-end servers
- ✓ Easy to install - instant download and run
- ✓ Easy to learn - familiar SQL with Tables and Columns
- ✓ Easy to write and query via **HTTP**, **MQTT** and **gRPC**



{{<cards>}}
    {{<card link="./getting-started/" title="Get Started" icon="academic-cap">}}
    {{<card link="./releases/" title="Download" icon="download">}}
{{</cards>}}

{{<callout type="info">}}
The latest version: {{< param latestNeoVer >}}
{{</callout>}}


{{< tabs items="Linux,macOS,Windows">}}
    {{< tab >}}
    ```json
    {"hello":"linux"}
    ```
    {{< /tab >}}
    {{< tab >}}
    ```json
    {"hello":"macOS"}
    ```
    {{< /tab >}}
    {{< tab >}}
    ```json
    {"hello":"Windows"}
    ```
    {{< /tab >}}
{{< /tabs >}}

>> some thing
>>
>> abc

```sh
$ machbase-neo serve
```

<span class="fs-6">
[Get Started](./docs/getting-started/){: .btn .btn-purple .mr-4 } [Download](./releases/){: .btn .btn-green } 
</span>
{: .d-inline-block .v-align-top}

Latest *{{site.latest_version}}*
{:.label .label-green }

Machbase is the world's fastest timeseries database[^1] with a minimal footprint. It's an ideal solution for environments that require scalability, from small servers with limited resources like the Raspberry Pi to horizontally scaled clusters. Machbase Neo, built on Machbase, adds crucial features required for the IoT industry. It ingests and handles query data through various protocols, such as MQTT for direct data transfer from IoT sensors, and SQL via HTTP for data retrieval by applications.

{{ $image := resources.Get "images/interfaces.jpg" }}

<img src="{{ $image.RelPermalink }}" width="{{ $image.Width }}" height="{{ $image.Height }}"/>

![interfaces](/assets/img/interfaces.jpg)

## API and Interfaces

- [x] HTTP : Applications and Sensors read/write data via HTTP REST API
- [x] MQTT : Sensors write data via MQTT protocol
- [x] gRPC : The first class API for extensions
- [x] SSH : Command line interface for human and batch process
- [x] WEB : User interface

## Bridges

Integration with external systems

- [x] SQLite
- [x] PostgreSQL
- [x] MySQL
- [x] MS-SQL
- [x] MQTT Broker
- [ ] Kafka
- [ ] NATS


## Download 

### Instant download

Paste the script below into the shell prompt for the latest version of the platform.

```sh
sh -c "$(curl -fsSL https://neo.machbase.com/install.sh)"
```

### Windows <!--GUI--> users

If you are a Windows user then execute `neow` included in the Windows release.
<!--
the macOS user prefers to use GUI, download neow package from the [releases](./releases/#gui-for-macos) page.
,-->

Download the latest release for [Windows]({{ site.releases_url }}/download/{{ site.latest_version }}/machbase-neo-{{ site.latest_version }}-windows-amd64.zip)
<!--
, [macOS (Apple)]({{ site.releases_url }}/download/{{ site.latest_version }}/neow-fog-{{ site.latest_version }}-macOS-arm64.zip) and [macOS (Intel)]({{ site.releases_url }}/download/{{ site.latest_version }}/neow-fog-{{ site.latest_version }}-macOS-amd64.zip).
-->

![interfaces](/assets/img/neow-win.png)


### Choose the released version manually

Find and download the file for the version and platform from the [releases](./releases/) page.

## Tutorials

[Tutorial Waves](./docs/tutorial-waves/00.index.md) tutorial is a good starting point.

[Raspberry PI as IoT server](./docs/tutorials/raspi-server.md) shows how to install machbase-neo on Raspberry PI and utilize it as an IoT server.

[Tutorials](./docs/tutorials/) section has more tutorials.

## Contributing

We welcome and encourage community contributions to documents and examples for other developers. Typo and broken link fixes are appreciated.

--------------

[^1]: [TPCx-IoT Performance Results](https://www.tpc.org/tpcx-iot/results/tpcxiot_perf_results5.asp?version=2)
{: .fs-1}

