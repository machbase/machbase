---
title: Releases
type: docs
weight: 10
toc: false
---


### Latest version {{< neo_latestver >}}

Choose the latest version for your platform.

| OS         | Architecture   |  Download |
|:-----------|:---------------|:----------|
| Linux      | arm64          | [machbase-neo-{{< neo_latestver >}}-linux-arm64.zip]({{< neo_releases_url >}}/download/{{< neo_latestver >}}/machbase-neo-{{< neo_latestver >}}-linux-arm64.zip)   |
| Linux      | x64            | [machbase-neo-{{< neo_latestver >}}-linux-amd64.zip]({{< neo_releases_url >}}/download/{{< neo_latestver >}}/machbase-neo-{{< neo_latestver >}}-linux-amd64.zip)   |
| Linux      | arm32          | [machbase-neo-{{< neo_latestver >}}-linux-arm32.zip]({{< neo_releases_url >}}/download/{{< neo_latestver >}}/machbase-neo-{{< neo_latestver >}}-linux-arm32.zip)   |
| macOS      | arm64          | [machbase-neo-{{< neo_latestver >}}-darwin-arm64.zip]({{< neo_releases_url >}}/download/{{< neo_latestver >}}/machbase-neo-{{< neo_latestver >}}-darwin-arm64.zip) |
| macOS      | x64            | [machbase-neo-{{< neo_latestver >}}-darwin-amd64.zip]({{< neo_releases_url >}}/download/{{< neo_latestver >}}/machbase-neo-{{< neo_latestver >}}-darwin-amd64.zip) |
| Windows    | x64     | [machbase-neo-{{< neo_latestver >}}-windows-amd64.zip]({{< neo_releases_url >}}/download/{{< neo_latestver >}}/machbase-neo-{{< neo_latestver >}}-windows-amd64.zip) |

### What about other Linux

{{< callout type="warning" >}}
The pre-built Linux packages will be based on Ubuntu 22.04.
Due to the deprecation of GitHub's action runner image on 2025-02-01,
Machbase Neo pre-built packages will transition to Ubuntu 22.04 as per [the schedule](https://github.com/actions/runner-images/issues/11101).
{{< /callout >}}

The pre-build linux packages are built on ubuntu 20.04.
If the pre-built packages are not compatible with your Linux distribution, you can still build from the source code on your system.

0. Ensure you have Go 1.23 and gcc installed.
1. Clone the neo-server repository from [GitHub](https://github.com/machbase/neo-server).
2. Run `go run mage.go install-neo-web` to download the web UI for Machbase Neo.
3. Run `go run mage.go machbase-neo` to build Machbase Neo.
4. Locate the executable binary in `./tmp/machbase-neo`.
5. Copy the executable binary to the directory where you want to install.

### What's Changed {{< neo_latestver >}}

[Changes](https://github.com/machbase/neo-server/releases/tag/{{< neo_latestver >}})

### How to upgrade from the previous v8.0.x version

The upgrade process is straightforward and involves replacing the executable file.

1. Shut down the machbase-neo process.
2. Replace the executable file `machbase-neo` (or `machbase-neo.exe`).
3. Start the machbase-neo process.

### Previous releases

Find previously released versions in [here](https://github.com/machbase/neo-server/releases).


{{< callout type="warning" emoji="⚠️">}}
**The edge and fog editions** of the previous **v1.5.0** -
Since v1.5.0, the editions are integrated into the single "standard" edition.<br/>
If you plan to run old version of machbase-neo on a small device such as Raspberry Pi, select the Edge edition.<br/>
For machines with larger memory and more CPU cores, such as a personal workstation or server, choose the Fog edition.
{{< /callout >}}

### SDK with CLASSIC

This releases are the legacy MACHBASE DBMS and application driver such as JDBC, ODBC and C client library.

| OS         | Architecture   |  Download |
|:-----------|:---------------|:----------|
| Linux      | x64            | [machbase-SDK-{{< classic_version >}}.official-LINUX-X86-64-release.tgz](https://stage.machbase.com/package/download/machbase-SDK-{{< classic_version >}}.official-LINUX-X86-64-release.tgz) |
| Linux      | arm64          | [machbase-SDK-{{< classic_version >}}.official-LINUX-ARM_CORTEX_A53-64-release.tgz](https://stage.machbase.com/package/download/machbase-SDK-{{< classic_version >}}.official-LINUX-ARM_CORTEX_A53-64-release.tgz) |
| Windows    | x64            | [machbase-SDK-8.0.32.official-WINDOWS-X86-64-release.msi](https://github.com/machbase/packages/releases/download/8.0.32/machbase-SDK-8.0.32.official-WINDOWS-X86-64-release.msi)
| Windows    | x86            | [machbase-SDK-{{< classic_version >}}.official-WINDOWS-X86-32-release.msi](https://stage.machbase.com/package/download/machbase-SDK-{{< classic_version >}}.official-WINDOWS-X86-32-release.msi) |
| macOS      | arm64          | [machbase-SDK-{{< classic_version >}}.official-DARWIN-ARM_M1-64-release.tgz](https://stage.machbase.com/package/download/machbase-SDK-{{< classic_version >}}.official-DARWIN-ARM_M1-64-release.tgz) |
| macOS      | x64            | [machbase-SDK-{{< classic_version >}}.official-DARWIN-X86-64-release.tgz](https://stage.machbase.com/package/download/machbase-SDK-{{< classic_version >}}.official-DARWIN-X86-64-release.tgz) |