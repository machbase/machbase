---
weight: 0
title: ロードマップ
type: docs
toc: false
draft: true
---

## 2023年第1四半期 {#2023년-1분기}

- [x] HTTPサーバー

```mermaid
flowchart RL
    client["HTTPクライアント"] --"GET/POSTリクエスト"---> machbase-neo
    subgraph machbase-neo
        direction RL
        http["HTTPリスナー"] --読み取り/書き込み--> machbase
        machbase[("Machbaseエンジン")]
    end
```

- [x] MQTTサーバー

```mermaid
flowchart RL
    client["MQTTクライアント"] --PUBLISH---> machbase-neo
    subgraph machbase-neo
        direction RL
        http["MQTTリスナー"] --書き込み--> machbase
        machbase[("Machbaseエンジン")]
    end
```

## 2023年第2四半期 {#2023년-2분기}

- [x] MQTTサブスクライバー

```mermaid
flowchart RL
    external-system --PUBLISH--> machbase-neo
    machbase-neo --SUBSCRIBE--> external-system
    subgraph machbase-neo
        direction RL
        subscriber["MQTTサブスクライバー"] --書き込み--> machbase
        machbase[("Machbaseエンジン")]
    end
    subgraph external-system
        direction RL
        client["MQTTクライアント"] --PUBLISH--> mqtt[[MQTTブローカー]]
    end
```

## 2023年第4四半期 {#2023년-4분기}
- [x] データの可視化

  Apache EChartsへの対応

## 2024年第2四半期 {#2024년-2분기}

- [X] NATSサブスクライバー

```mermaid
flowchart RL
    external-system --PUBLISH--> machbase-neo
    machbase-neo --SUBSCRIBE--> external-system
    subgraph machbase-neo
        direction RL
        subscriber["NATSサブスクライバー"] --書き込み--> machbase
        machbase[("Machbaseエンジン")]
    end
    subgraph external-system
        direction RL
        client["NATSクライアント"] --PUBLISH--> mqtt[[NATSサーバー]]
    end
```

## 2024年以降 {#2024년-이후}

- [ ] Kafkaコンシューマー (計画中)

```mermaid
flowchart RL
    external-system --CONSUME--> machbase-neo
    machbase-neo --SUBSCRIBE--> external-system
    subgraph machbase-neo
        direction RL
        subscriber["Kafkaコンシューマー"] --書き込み--> machbase
        machbase[("Machbaseエンジン")]
    end
    subgraph external-system
        direction RL
        client["Kafkaプロデューサー"] --PRODUCE--> mqtt[[Kafkaサーバー]]
    end
```

- [ ] 位置情報に基づく可視化(計画中)

   leaflet.jsによる地理情報の可視化に対応
