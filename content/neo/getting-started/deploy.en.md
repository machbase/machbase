---
title: Deploy modes
type: docs
weight: 13
---


## Head Only Mode

{{< neo_since ver="8.0.45" />}}

If the `--data` flag value is a URL pointing to another Machbase DBMS's mach port (`5656`), as shown in the example below:

```sh
machbase-neo serve --data machbase://sys:manager@192.168.1.100:5656
```

or using environment variable for username and password pair:

```sh
SECRET="sys:manager" \
machbase-neo serve --data machbase://${SECRET}@192.168.1.100:5656
```

In this mode, the machbase-neo process starts without its own database and uses the target database instead. 
The "head-only machbase-neo" does not provide the 5656 port service, and all other APIs work with the destination DBMS.

{{< figure src="../img/head-only-1.png" width="600px" >}}


## Headless Mode

{{< neo_since ver="8.0.45" />}}

`machbase-neo serve-headless` starts a DBMS process using only the Machbase DBMS mach port (`5656`). This mode is useful for running a DBMS process without other service ports (HTTP, MQTT, gRPC, SSH) and their related functions.

This running mode is specifically designed to work with separate "head-only" mode processes,
allowing the separation of API services and the DBMS engine.

{{< figure src="../img/head-only-2.png" width="600px" >}}

