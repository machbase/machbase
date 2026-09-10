---
toc: true
title: Windowsサービス
type: docs
weight: 81
---

`machbase-neo service`コマンドでWindowsサービスの登録を管理します。
サービスをインストールすると、Windowsの起動時にmachbase-neoが自動的に起動します。

{{< callout emoji="📌">}}
この操作には**管理者権限**が必要です。
{{< /callout >}}


## machbase-neo service install {#machbase-neo-service-install}

machbase-neoをWindowsサービスに登録します。

```cmd
machbase-neo.exe service install --host 0.0.0.0 --data D:\database --file D:\database\files --log-filename D:\database\machbase-neo.log
```

## machbase-neo service remove {#machbase-neo-service-remove}

Windowsサービスからmachbase-neoを削除します。

```cmd
machbase-neo.exe service remove
```

## 開始と停止 {#start-and-stop}

サービスを開始・停止します。Windowsのサービス管理画面と同じ操作です。

```cmd
machbase-neo.exe service start
```

```cmd
machbase-neo.exe service stop
```
