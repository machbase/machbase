---
title: MQTT API
type: docs
weight: 120
---


Machbase Neo supports writing and query data via MQTT protocols. 

{{< callout emoji="📢">}}
MQTT `v3.1.1` (or `v3.1`) is officially supported. `v5` is early experimental state and does **not** recommended to use.
{{< /callout >}}

The real benefit of MQTT api compare to HTTP is it utilizes `append` feature of Machbase that provides robust performance of writing data.
Since MQTT is connection oriented protocol and keeping a connection through the session, clients can repeatedly send messages to write.
Also MQTT protocol is widely adopted by majority of IoT devices.

So it is the best way to make the sensors to write its collecting data to machbase-neo via MQTT.

{{< figure src="/images/interfaces.jpg" width="500" >}}

## In this chapter

{{< children_toc />}}
