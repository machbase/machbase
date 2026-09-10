---
type: docs
title: アプリ
weight: 30
toc: true
---

Machbase Neo パッケージは、データ収集・複製、映像監視、AI 分析の機能を拡張します。
Web UI のパッケージ一覧から必要なパッケージをインストールし、ブラウザーで設定・運用を管理できます。

------

{{< cards >}}

  <!-- 代表画像: neo-pkg-replication/docs/images/dashboard-main.png。必要に応じて差し替え可能。 -->
  {{< card link="https://machbase.github.io/neo-pkg-replication/kr/"
    image="/images/package/replication.png" icon="gift"
    title="Replication"
    subtitle="Replication パッケージ（`neo-pkg-replication`）は、Machbase テーブルのデータを別の Machbase サーバーへ複製します。Web 画面で複製条件と列のマッピングを設定し、進捗やログを確認できます。ネットワーク障害やサーバー停止で中断しても、接続復旧後に中断位置から再開してデータの欠落を防ぎます。">}}

  <!-- 代表画像: neo-pkg-opcua-client/docs/images/opcua-dashboard-main.png。必要に応じて差し替え可能。 -->
  {{< card link="https://machbase.github.io/neo-pkg-opcua-client/kr/"
    image="/images/package/opcua-client.png" icon="gift"
    title="OPC UA Client"
    subtitle="OPC UA Client パッケージ（`neo-pkg-opcua-client`）は、OPC UA サーバーの設備・センサーデータを収集し、Machbase Neo に保存します。サーバーのノードを参照して収集対象を選び、列のマッピングと値の変換を設定できます。収集ジョブの開始・停止、状態やログの確認も Web 画面で行います。データビューアーでは、収集結果を表とチャートで確認できます。">}}

  <!-- 代表画像: neo-pkg-blackbox/docs/images/blackbox-dashboard-video-sync.png。必要に応じて差し替え可能。 -->
  {{< card link="https://machbase.github.io/neo-pkg-blackbox/kr/"
    image="/images/package/blackbox.png" icon="gift"
    title="Blackbox"
    subtitle="Blackbox パッケージ（`neo-pkg-blackbox`）は、カメラ映像と検出イベントを管理する映像監視機能です。Blackbox サーバーとカメラを登録し、物体検出・イベント規則を設定して発生履歴を確認できます。Neo ダッシュボードの Video パネルではライブ映像と録画を表示し、録画を時系列チャートの時点に合わせて比較できます。">}}

  <!-- 代表画像: neo-pkg-llm-chat/docs/images/llm-chat-main.png。必要に応じて差し替え可能。 -->
  {{< card link="https://machbase.github.io/neo-pkg-llm-chat/kr/"
    image="/images/package/llm-chat.png" icon="gift"
    title="LLM Chat"
    subtitle="LLM Chat パッケージ（`neo-pkg-llm-chat`）は、自然言語の対話で Machbase Neo データを検索・分析する AI チャット機能です。テーブルやタグを参照し、対話を通じてダッシュボードや分析レポートを作成できます。複数の LLM モデルに対応し、使用するモデルと接続情報を Web 設定画面で管理できます。">}}
{{< /cards >}}
