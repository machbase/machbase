---
title: MQTT API
type: docs
weight: 30
---


Machbase Neo supports writing and query data via MQTT protocols. 

The real benefit of the MQTT API compared to HTTP is that it utilizes the `append` feature of Machbase, which provides robust performance for writing data. Since MQTT is a connection-oriented protocol and maintains a connection throughout the session, clients can repeatedly send messages to write data. Additionally, the MQTT protocol is widely adopted by the majority of IoT devices.

So, using MQTT is the most efficient way for sensors to send their collected data to Machbase Neo.

{{< figure src="/images/interfaces.jpg" width="500" >}}


## In this chapter

{{< children_toc />}}
