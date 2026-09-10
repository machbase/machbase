---
title: machbase-neo
weight: 10
toc: true
---

✓ 高性能な時系列データベースを基盤とする、Physical AI時代のデータプラットフォームです。<br/>
✓ エッジデバイス（Raspberry Pi）からハイエンドサーバーまで拡張できます。<br/>
✓ 物理世界のデータを収集、変換、可視化します。<br/>
✓ ダッシュボードで現場のデータをリアルタイムに監視できます。<br/>
✓ ダウンロード後すぐに実行でき、簡単にインストールできます。<br/>
✓ テーブルと列を扱う使い慣れたSQLで、容易に学習できます。<br/>
✓ **HTTP**、**MQTT**、SQLで容易にデータを取り込み、検索できます。<br/>
✓ SQLite、PostgreSQL、MySQL、MSSQL、MQTTブローカー、NATSと連携できます。<br/>

{{< button color="purple" href="./getting-started/">}} はじめに {{< /button >}}
{{< button color="green" href="./releases/">}} ダウンロード {{< /button >}}
{{< label color="green" >}} 最新バージョン <i>{{< neo_latestver >}}</i> {{< /label>}}

`machbase-neo`は、C言語で実装した高性能なMachbase時系列データベースエンジンを
基盤とする、Physical AI時代に必要なデータプラットフォームです。
ロボット、自律システム、スマートファクトリー、エッジデバイスなど、物理世界で発生する
時系列データを収集、保存、変換、可視化し、アプリケーションやAIモデルが
学習・推論にすぐに利用できる形式で提供します。
MQTTによるリアルタイム収集、HTTP経由のSQL検索、TQLによる変換、ダッシュボード、外部システムへのブリッジを
統合し、現場のデータをAIで利用できるデータセットやサービスにつなげます。
エッジデバイスから高性能サーバーまで、幅広い環境にインストールして利用できます。

### ダウンロード {#다운로드}

{{< tabs >}}
    {{< tab name="Linux/macOS" icon="terminal">}}
    以下のスクリプトをシェルプロンプトに貼り付けると、最新バージョンをインストールできます。

    ```bash
    sh -c "$(curl -fsSL https://docs.machbase.com/install.sh)"
    ```
    {{< /tab >}}

    {{< tab name="Windows" icon="desktop-computer">}}
    GUIを使用する場合は、Windows配布パッケージに含まれる`neow`を起動してください。

    [Windows]({{< neo_releases_url >}}/download/{{< neo_latestver >}}/machbase-neo-{{< neo_latestver >}}-windows-amd64.zip)用の最新リリースをダウンロードしてください。

    ![interfaces](/images/neow-win.png)
    {{< /tab >}}

    {{< tab name="手動で選択" icon="globe">}}
    [リリース](./releases/)ページで、必要なバージョンとプラットフォームに対応するファイルをダウンロードしてください。
    {{< /tab >}}
{{< /tabs >}}


### データの可視化 {#데이터-시각화}

データの変換と可視化のための言語*TQL*を標準で提供します。

{{< figure src="/images/data-visualization.jpg" width="740" >}}

- [TQL](/neo/tql)は、データ変換のためのドメイン固有言語（DSL）です。
- [CHART()](/neo/tql/chart/)は、データの可視化に対応します。
- [SCRIPT()](/neo/tql/script/)で独自のロジックを実装できます。

<span class="badge-new">NEW!</span> 地理空間データの可視化に対応しています。

{{< figure src="/images/map-visualization.jpg" width="600" >}}

- [GEOMAP()](/neo/tql/geomap/)で地図を可視化できます。

### ダッシュボード {#대시보드}

リアルタイムデータをすぐに監視できます。

{{< figure src="/images/dashboard.png" width="740" >}}

### APIとインターフェース {#api-및-인터페이스}

- [x] HTTP：アプリケーションやエッジデバイスが[HTTP](/neo/api-http) REST APIでデータを読み書きできます。
- [x] MQTT：ロボット、機器、エッジデバイスが[MQTT](/neo/api-mqtt)プロトコル（MQTT v3.1.1およびv5）でデータを送信できます。
- [x] SSH：[ssh](/neo/shell/#remote-access-via-ssh)経由のコマンドラインインターフェースを提供します。
- [x] GUI：[Web](/neo/getting-started/webui/)ユーザーインターフェースを提供します。

{{< figure src="/images/interfaces.jpg" width="600" >}}

### ブリッジ {#브리지}

外部システムと容易に連携できます。

- [x] SQLite
- [x] PostgreSQL
- [x] MySQL
- [x] MS-SQL
- [x] MQTT Broker
- [x] NATS


### 貢献 {#기여}

他の開発者に役立つドキュメントやサンプルの作成への参加を歓迎します。誤字・脱字やリンク切れを見つけた場合は、お知らせください。


[^1]: [TPCx-IoTの性能結果](https://www.tpc.org/tpcx-iot/results/tpcxiot_perf_results5.asp?version=2)
