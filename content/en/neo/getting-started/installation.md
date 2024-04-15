---
title: Install machbase-neo
type: docs
weight: 10
---

The installation process of machbase-neo is just simple as downloading, unarchiving and run the executable.

{{% steps %}}

### Download

Use the instant download with the script below.

```sh
sh -c "$(curl -fsSL https://docs.machbase.com/install.sh)"
```

Or, download the latest version for your platform from [releases](/neo/releases) page.
Then unarchive the file into a preferred directory.

### Unarchive

Unarchive downloaded file.

```sh
unzip machbase-neo-{{< neo_latestver >}}-${platform}-${arch}.zip
```

### Confirm executable

```sh
machbase-neo version
```

{{< figure src="../img/server-version.gif" width="600" >}}

{{% /steps %}}
