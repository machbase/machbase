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
| Windows[^1] | x64     | [machbase-neo-{{< neo_latestver >}}-windows-amd64.zip]({{< neo_releases_url >}}/download/{{< neo_latestver >}}/machbase-neo-{{< neo_latestver >}}-windows-amd64.zip)[^2] |


<!--
### GUI Launcher for macOS

The (_experimental_) GUI releases for macOS users.

| OS         | Architecture   |  Download |
|:-----------|:---------------|:----------|
| macOS      | Apple          | [neow-{{< neo_latestver >}}-darwin-arm64.zip]({{< neo_releases_url >}}/download/{{< neo_latestver >}}/neow-{{< neo_latestver >}}-darwin-arm64.zip)|
| macOS      | Intel          | [neow-{{< neo_latestver >}}-darwin-amd64.zip]({{< neo_releases_url >}}/download/{{< neo_latestver >}}/neow-{{< neo_latestver >}}-darwin-amd64.zip)|
-->

### What's Changed {{< neo_latestver >}}

[Changes](https://github.com/machbase/neo-server/releases/tag/{{< neo_latestver >}})

### Previous releases

Find previously released versions in [here](https://github.com/machbase/neo-server/releases).


{{< callout type="warning" emoji="⚠️">}}
**The edge and fog editions** of the previsous **v1.5.0** -
Since v1.5.0, the editions are integrated into the single "standard" edition.<br/>
If you plan to run old version of machbase-neo on a small device such as Raspberry Pi, select the Edge edition.<br/>
For machines with larger memory and more CPU cores, such as a personal workstation or server, choose the Fog edition.
{{< /callout >}}

[^1]: Windows Fall 2018 or newer versions.
[^2]: Windows release includes both of the `machbase-neo` and `neow` (GUI frontend) executables.
