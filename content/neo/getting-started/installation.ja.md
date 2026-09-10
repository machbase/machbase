---
toc: true
title: インストール
type: docs
weight: 10
---

machbase-neoは、ダウンロード、展開、実行ファイルの起動という簡単な手順でインストールできます。

{{% steps %}}

### ダウンロード {#다운로드}

以下のスクリプトですぐにダウンロードできます。

```sh
sh -c "$(curl -fsSL https://docs.machbase.com/install.sh)"
```

または、[リリース](/neo/releases)ページで使用中のプラットフォームに対応する最新バージョンをダウンロードし、
任意のディレクトリに展開してください。

### 展開 {#압축-해제}

ダウンロードしたファイルを展開してください。

```sh
unzip machbase-neo-{{< neo_latestver >}}-${platform}-${arch}.zip
```

### 実行ファイルの確認 {#실행-파일-확인}

```sh
machbase-neo version
```

{{< figure src="/neo/getting-started/img/server-version.gif" width="600" >}}

{{% /steps %}}
