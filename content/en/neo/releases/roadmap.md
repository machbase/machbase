---
title: Roadmap
type: docs
toc: false
---

## 2023 Q1

- [x] HTTP Server

```mermaid
flowchart RL
    client["Http Client"] --"Request GET/POST"---> machbase-neo
    subgraph machbase-neo
        direction RL
        http["HTTP Listener"] --Read/Write--> machbase
        machbase[("machbase engine")]
    end
```

- [x] MQTT Server

```mermaid
flowchart RL
    client["MQTT Client"] --PUBLISH---> machbase-neo
    subgraph machbase-neo
        direction RL
        http["MQTT Listener"] --Write--> machbase
        machbase[("machbase engine")]
    end
```

## 2023 Q2

- [x] MQTT Subscriber

```mermaid
flowchart RL
    external-system --PUBLISH--> machbase-neo
    machbase-neo --SUBSCRIBE--> external-system
    subgraph machbase-neo
        direction RL
        subscriber["MQTT Subscriber"] --Write--> machbase
        machbase[("machbase engine")]
    end
    subgraph external-system
        direction RL
        client["MQTT Client"] --PUBLISH--> mqtt[[MQTT Broker]]
    end
```

## 2023 2H

- [ ] Kafka Consumer

```mermaid
flowchart RL
    external-system --CONSUME--> machbase-neo
    machbase-neo --SUBSCRIBE--> external-system
    subgraph machbase-neo
        direction RL
        subscriber["Kafka Consumer"] --Write--> machbase
        machbase[("machbase engine")]
    end
    subgraph external-system
        direction RL
        client["Kafka Producer"] --PRODUCE--> mqtt[[Kafka Server]]
    end
```

- [ ] NATS Subscriber

```mermaid
flowchart RL
    external-system --PUBLISH--> machbase-neo
    machbase-neo --SUBSCRIBE--> external-system
    subgraph machbase-neo
        direction RL
        subscriber["NATS Subscriber"] --Write--> machbase
        machbase[("machbase engine")]
    end
    subgraph external-system
        direction RL
        client["NATS Client"] --PUBLISH--> mqtt[[NATS Server]]
    end
```
