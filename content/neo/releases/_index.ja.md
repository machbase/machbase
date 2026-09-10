---
title: リリース
type: docs
weight: 10
toc: false
---


### 最新バージョン {{< neo_latestver >}} {#latest-version}

使用中のプラットフォームに対応する最新パッケージを選択してください。

| OS         | アーキテクチャ       |  ダウンロード |
|:-----------|:---------------|:----------|
| Linux      | arm64          | [machbase-neo-{{< neo_latestver >}}-linux-arm64.zip]({{< neo_releases_url >}}/download/{{< neo_latestver >}}/machbase-neo-{{< neo_latestver >}}-linux-arm64.zip)   |
| Linux      | x64            | [machbase-neo-{{< neo_latestver >}}-linux-amd64.zip]({{< neo_releases_url >}}/download/{{< neo_latestver >}}/machbase-neo-{{< neo_latestver >}}-linux-amd64.zip)   |
| macOS      | arm64          | [machbase-neo-{{< neo_latestver >}}-darwin-arm64.zip]({{< neo_releases_url >}}/download/{{< neo_latestver >}}/machbase-neo-{{< neo_latestver >}}-darwin-arm64.zip) |
| macOS      | x64            | [machbase-neo-{{< neo_latestver >}}-darwin-amd64.zip]({{< neo_releases_url >}}/download/{{< neo_latestver >}}/machbase-neo-{{< neo_latestver >}}-darwin-amd64.zip) |
| Windows    | x64     | [machbase-neo-{{< neo_latestver >}}-windows-amd64.zip]({{< neo_releases_url >}}/download/{{< neo_latestver >}}/machbase-neo-{{< neo_latestver >}}-windows-amd64.zip) |

### その他のLinuxディストリビューション {#기타-linux-배포판}

提供されているパッケージが使用中のディストリビューションと互換性がない場合は、ソースコードからビルドできます。

1. Go 1.24とgccがインストールされていることを確認します。
2. [GitHub](https://github.com/machbase/neo-server)から`neo-server`リポジトリをクローンします。
3. `go run mage.go install-neo-web`を実行して、Machbase NeoのWeb UIをダウンロードします。
4. `go run mage.go machbase-neo`を実行して、Machbase Neoをビルドします。
5. ビルドした実行ファイルは、`./tmp/machbase-neo`に生成されます。
6. 任意のインストール先に実行ファイルをコピーします。

### 変更内容 {{< neo_latestver >}} {#changes}

変更の詳細は、[変更履歴](https://github.com/machbase/neo-server/releases/tag/{{< neo_latestver >}})で確認できます。

### v8.0.xからのアップグレード {#v80x에서-업그레이드하기}

アップグレードは、実行ファイルを置き換えるだけで完了します。

1. 実行中のmachbase-neoプロセスを停止します。
2. `machbase-neo`（Windowsの場合は`machbase-neo.exe`）の実行ファイルを新しいファイルに置き換えます。
3. machbase-neoプロセスを再起動します。

### 以前のバージョン {#이전-버전}

以前のバージョンは、[GitHubのリリースページ](https://github.com/machbase/neo-server/releases)からダウンロードできます。

{{< callout type="warning" emoji="⚠️">}}
**v1.5.0**まで提供していた**Edge / Fogエディション**は、v1.5.0以降、単一の「Standard」エディションに統合されました。<br/>
Raspberry Piなどの小型機器で旧バージョンを実行する場合は、Edgeエディションを選択してください。<br/>
ワークステーションやサーバーなど、メモリとCPUコアが十分にある環境ではFogエディションを使用します。
{{< /callout >}}

### CLASSIC SDK {#classic-sdk}

以下のパッケージには、従来のMACHBASE DBMSと、JDBC、ODBC、Cクライアントライブラリなどのアプリケーションドライバーが含まれています。

| OS         | アーキテクチャ       |  ダウンロード |
|:-----------|:---------------|:----------|
| Linux      | x64            | [machbase-SDK-8.5.2.official-LINUX-X86-64-release.tgz](https://github.com/machbase/packages/releases/download/8.5.2/machbase-SDK-8.5.2.official-LINUX-X86-64-release.tgz) |
| Linux      | arm64          | [machbase-SDK-8.5.2.official-LINUX-ARM_CORTEX_A53-64-release.tgz](https://github.com/machbase/packages/releases/download/8.5.2/machbase-SDK-8.5.2.official-LINUX-ARM_CORTEX_A53-64-release.tgz) |
| Linux      | arm32          | [machbase-SDK-8.5.2.official-LINUX-ARM_CORTEX_A8-32-release.tgz](https://github.com/machbase/packages/releases/download/8.5.2/machbase-SDK-8.5.2.official-LINUX-ARM_CORTEX_A8-32-release.tgz) |
| Windows    | x64            | [machbase-SDK-8.5.2.official-WINDOWS-X86-64-release.msi](https://github.com/machbase/packages/releases/download/8.5.2/machbase-SDK-8.5.2.official-WINDOWS-X86-64-release.msi)
| macOS      | arm64          | [machbase-SDK-8.5.2.official-DARWIN-ARM_M1-64-release.tgz](https://github.com/machbase/packages/releases/download/8.5.2/machbase-SDK-8.5.2.official-DARWIN-ARM_M1-64-release.tgz) |
| macOS      | x64            | [machbase-SDK-8.5.2.official-DARWIN-X86-64-release.tgz](https://github.com/machbase/packages/releases/download/8.5.2/machbase-SDK-8.5.2.official-DARWIN-X86-64-release.tgz) |
