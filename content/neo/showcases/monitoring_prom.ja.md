---
title: Prometheus モニタリングデモ
type: docs
weight: 971
---

使用する OS に合わせて Machbase Neo の Prometheus メトリクスを収集し、Grafana ダッシュボードを開く手順を紹介します。

{{< icon "github" >}} https://github.com/machbase/neo-prom
<p/>

{{< youtube -pDn6ysLCh0 >}}

このデモでは、Docker ベースの Prometheus で Machbase Neo のメトリクスエンドポイント `http://127.0.0.1:5654/debug/metrics` からデータを収集し、Grafana ダッシュボードで時系列データを監視します。

**前提条件**

- Docker と Docker Compose が使用できること
- 5654、9090、3000 の各ポートが使用可能であること
- Machbase Neo の実行ファイルがあること