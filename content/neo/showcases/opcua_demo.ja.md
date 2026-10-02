---
title: OPC UA データ収集デモ
type: docs
weight: 969
---

Kepware OPC UA サーバーを Machbase Neo に接続し、証明書を設定してデータを収集する手順を紹介します。

{{< icon "github" >}} https://github.com/machbase/neo-prom
<p/>

{{< youtube BgrEGzDoQLU >}}

このガイドでは、Machbase Neo OPC UA Client を使って Kepware からデータを収集する一連の手順を紹介します。まず OPC UA サーバーのエンドポイントとセキュリティ設定を登録し、安全な通信に必要な証明書を作成して適用します。

サーバーに接続したら、ノードの構造を確認して収集するタグを選択します。選択したタグを収集ジョブに登録すると、Machbase データベースに一定間隔で保存されます。

この動画では、個別の収集プログラムを開発せずに、Web 画面から OPC UA サーバーに接続し、証明書を管理して必要な設備データを収集する方法を紹介します。