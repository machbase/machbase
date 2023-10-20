---
title: Install machbase-neo
type: docs
weight: 10
---

The intallation process of machbase-neo is just simple as downloading, unarchiving and run the executable.

{{% steps %}}

### Download

Use the instant download with the script below.

```sh
sh -c "$(curl -fsSL https://machbase.com/install.sh)"
```

Or, download the latest version for your platform from [releases](/neo/releases) page.
Then unarchive the file into a preferred directory.

### Unarchive

Unarchive downloaded file.

```sh
unzip machbase-neo-v${X.Y.Z}-${platform}-${arch}.zip
```

### Confirm executable

```sh
machbase-neo version
```

![server-version](../img/server-version.gif)

{{% /steps %}}
