---
toc: true
title: 起動と停止
type: docs
weight: 12
---

## Linux & macOS {#linux--macos}

LinuxとmacOSでは、`serve`コマンドでmachbase-neoを起動します。

```sh
machbase-neo serve
```

{{< figure src="/neo/getting-started/img/server-serve.gif" width="600" >}}

### ポートの公開 {#포트-개방}

machbase-neoは、セキュリティのため既定ではlocalhostでのみ待ち受けます。リモートクライアントからネットワーク経由で接続するには、`--host <bind address>`オプションで待ち受けアドレスを指定してください。

すべてのアドレスで接続を受け付けるには、`0.0.0.0`を指定します。

```sh
machbase-neo serve --host 0.0.0.0
```

特定のアドレスでのみ接続を受け付けるには、ホストのIPアドレスを指定します。

```sh
machbase-neo serve --host 192.168.1.10
```

### 停止 {#종료}

サーバーをフォアグラウンドで実行している場合は、`Ctrl+C`で停止できます。

`shutdown`コマンドも使用できます。このコマンドは、同じホスト上で実行した場合にのみ動作します。

```sh
machbase-neo shell shutdown
```

## Linuxサービス {#linux-service}

machbase-neoをバックグラウンドプロセスとして登録する方法は、[運用/Linuxサービス](../../operations/service-linux/)を参照してください。

## Windows {#windows}

Windowsでは、`neow.exe`をダブルクリックし、ウィンドウ左上の「machbase-neo serve」ボタンを押して起動します。

{{< figure src="/images/neow-win.png" width="600" >}}

### Windowsサービス {#windows-service}

machbase-neoはWindowsサービスとして登録できます。<br/>
以下のコマンドは管理者権限で実行してください。

- インストール

サービスを登録します。`machbase-neo service install`の後に指定する引数は`machbase-neo serve`と同じですが、すべてのパスは*絶対パス*で指定してください。

```
C:\neo-server>.\machbase-neo service install --host 127.0.0.1 --data C:\neo-server\database --file C:\neo-server\files --log-filename C:\neo-server\machbase-neo.log --log-level INFO

```

- 開始と停止

Windowsのサービス管理機能で開始・停止できます。
以下のコマンドを直接実行することもできます。

```
C:\neo-server>.\machbase-neo service start
success to start machbase-neo service.

C:\neo-server>.\machbase-neo service stop
success to stop machbase-neo service.
```

- 削除

Windowsサービスからmachbase-neoを削除します。

```
C:\neo-server>.\machbase-neo service remove
success to remove machbase-neo service.
```
