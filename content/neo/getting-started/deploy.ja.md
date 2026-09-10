---
toc: true
title: デプロイモード
type: docs
weight: 13
---


## ヘッドオンリーモード {#헤드-온리-모드}

{{< neo_since ver="8.0.45" />}}

`--data`フラグに別のMachbase DBMSのmachポート（`5656`）を指すURLを指定する場合は、次のように実行します。

```sh
machbase-neo serve --data machbase://sys:manager@192.168.1.100:5656
```

ユーザー名とパスワードを環境変数で渡すこともできます。

```sh
SECRET="sys:manager" \
machbase-neo serve --data machbase://${SECRET}@192.168.1.100:5656
```

このモードでは、machbase-neoプロセスは独自のデータベースを持たず、接続先のデータベースを使用します。
「ヘッドオンリーmachbase-neo」はポート5656のサービスを提供せず、他のすべてのAPIは接続先のDBMSと連携します。

{{< figure src="/neo/getting-started/img/head-only-1.png" width="600px" >}}


## ヘッドレスモード {#헤드리스-모드}

{{< neo_since ver="8.0.45" />}}

`machbase-neo serve-headless`は、Machbase DBMSのmachポート（`5656`）だけを使用するDBMSプロセスを起動します。他のサービスポート（HTTP、MQTT、gRPC、SSH）とその関連機能を使わずにDBMSだけを稼働させる場合に便利です。

この実行モードは、別に起動する「ヘッドオンリー」プロセスとの連携を前提としており、
APIサービスとDBMSエンジンを分離できます。

{{< figure src="/neo/getting-started/img/head-only-2.png" width="600px" >}}
