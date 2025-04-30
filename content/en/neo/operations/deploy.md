---
title: Deploy modes
type: docs
weight: 11
---

{{< neo_since ver="8.0.45" />}}

{{< callout type="warning" >}}
**BETA Warning**<br/>
The head-only and headless modes are currently in beta and are not suitable for production environments.
{{< /callout >}}

## Head Only Mode

If the `--data` flag value is a URL pointing to another Machbase DBMS's mach port (`5656`), as shown in the example below:

```sh
SECRET="sys:manager" \
machbase-neo serve --data machbase://${SECRET}@192.168.1.100:5656
```

In this mode, the machbase-neo process starts without its own database and uses the target database instead. 
The "head-only machbase-neo" does not provide the 5656 port service, and all other APIs work with the destination DBMS.

{{< figure src="../img/head-only-1.png" width="600px" >}}


## Headless Mode

{{< neo_since ver="8.0.45" />}}

{{< callout type="warning" >}}
**BETA Warning**<br/>
The head-only and headless modes are currently in beta and are not suitable for production environments.
{{< /callout >}}

`machbase-neo serve-headless` starts a DBMS process using only the Machbase DBMS mach port (`5656`). This mode is useful for running a DBMS process without other service ports (HTTP, MQTT, gRPC, SSH) and their related functions.

This running mode is specifically designed to work with separate "head-only" mode processes,
allowing the separation of API services and the DBMS engine.

{{< figure src="../img/head-only-2.png" width="600px" >}}

