---
title: 로드맵
type: docs
toc: false
draft: true
---

## 2023년 1분기

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

## 2023년 2분기

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

## 2023년 4분기
- [x] 데이터 시각화

  Apache ECharts 지원

## 2024년 2분기

- [X] NATS Subscriber

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

## 2024년 이후

- [ ] Kafka Consumer (계획 중)

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

- [ ] 위치 기반 시각화(계획 중)

   leaflet.js를 이용한 지리 정보 시각화 지원
