---
toc: true
title: シェル
type: docs
weight: 21
---

## Web経由のリモート接続 {#웹을-통한-원격-접속}

1. 新しいタブの画面で<img src="/neo/shell/img/shell_icon.png" style="display:inline-block;height:1.75em;width:auto;vertical-align:middle;margin:0 3px">`SHELL` を選択します。

{{< figure src="/images/web-shell-pick.png" width="600px" >}}

2. メインエディター領域にシェルが開きます。`sys machbase-neo` プロンプトで SQL 文や machbase-neo シェルコマンドを実行できます。

{{< figure src="/images/web-shell-ui.png" width="700px" >}}

<a id="remote-access-via-ssh"></a>
## SSH経由のリモート接続 {#ssh를-통한-원격-접속}

SSH（Secure Shell）は、リモートシステムに安全に接続するためのプロトコルです。
パスワード認証に加え、より安全な公開鍵認証にも対応しています。

machbase-neoは、リモートでの運用・管理用にSSHインターフェースを提供します。
以下のように、SSHコマンドでSQLインタープリターに接続できます。

- ユーザー： SYS
- 既定のパスワード： manager
- 既定のポート： 5652

```sh
$ ssh -p 5652 sys@127.0.0.1
sys@127.0.0.1's password: manager↵
```

`machbase-neo»`プロンプトが表示されたら、SQL文を実行できます。

```
machbase-neo» select * from example;
┌─────────┬──────────┬─────────────────────────┬───────────┐
│ ROWNUM  │ NAME     │ TIME(UTC)               │ VALUE     │
├─────────┼──────────┼─────────────────────────┼───────────┤
│       1 │ wave.sin │ 2023-01-31 03:58:02.751 │ 0.913716  │
│       2 │ wave.cos │ 2023-01-31 03:58:02.751 │ 0.406354  │
                        ...omit...
│      13 │ wave.sin │ 2023-01-31 03:58:05.751 │ 0.668819  │
│      14 │ wave.cos │ 2023-01-31 03:58:05.751 │ -0.743425 │
└─────────┴──────────┴─────────────────────────┴───────────┘
```

### パスワードなしでのSSH接続 {#비밀번호-없이-ssh-접속하기}

1. **鍵ペアの生成**：接続元のローカルマシンで、`ssh-keygen`コマンドを使って新しい鍵ペアを生成します。

    > 鍵ペアがある場合は、この手順を省略できます。

    ```bash
    ssh-keygen -t rsa
    ```

    このコマンドは、ホームディレクトリの`.ssh`フォルダーに`id_rsa`（秘密鍵）と`id_rsa.pub`（公開鍵）を作成します。

2. **公開鍵のコピー**：生成した公開鍵をリモートサーバーにコピーします。

    Machbaseサーバーに公開鍵を登録するには、以下の手順を実行します。

3. **鍵ペアでのログイン**：これで鍵ペアを使ってMachbaseサーバーにログインできます。
SSHクライアントは秘密鍵で認証データに署名し、サーバーは登録された公開鍵で署名を検証してユーザーを認証します。

    ```bash
    ssh -p 5652 sys@127.0.0.1
    ```

    設定が完了すると、パスワードを入力せずにmachbase-neoに接続できます。

#### Web UIでのSSHキーの登録 {#웹-ui에서-ssh-키-등록}

1. 左メニューの一番下にある<img src="/neo/shell/img/settings_icon.png" style="display:inline-block;height:1.75em;width:auto;vertical-align:middle;margin:0 3px">アイコンをクリックし、`SSH Keys` を選択します。 {{< neo_since ver="8.0.20" />}}

{{< figure src="/neo/shell/img/ssh_keys.jpg" width="200px" >}}

2. `New SSH key` をクリックし、`Title` にキーを識別する名前を、`Public Key` に公開鍵の全文を貼り付けてから `Add SSH key` をクリックします。

{{< figure src="/neo/shell/img/ssh_keys2.jpg" width="590px" >}}

3. 登録したキーが `Authentication Keys` の一覧に表示されます。使わなくなったキーは `Delete` で削除します。

{{< figure src="/neo/shell/img/ssh_keys3.jpg" width="600px" >}}

#### シェルコマンドでのSSHキーの登録 {#셸-명령으로-ssh-키-등록}

machbase-neoサーバーに公開鍵を登録すると、パスワードなしで`machbase-neo shell`コマンドを実行できます。

1. 公開鍵をサーバーに登録します。

```sh
machbase-neo shell ssh-key add `cat ~/.ssh/id_rsa.pub`
```

2. 登録済みの公開鍵一覧を確認します。

```sh
machbase-neo shell ssh-key list
```

または

```
$ machbase-neo shell ↵

machbase-neo» ssh-key list
┌────────┬───────────────────────────────────────────┬─────────────────────┬────────────────────────────────────────────────────┐
│ ROWNUM │ NAME                                      │ KEY TYPE            │ FINGERPRINT                                        │
├────────┼───────────────────────────────────────────┼─────────────────────┼────────────────────────────────────────────────────┤
│      1 │ **DO NOT DELETE** machbase-neo server key │ ecdsa-sha2-nistp521 │ SHA256:osfeJKNiUV+a2bIdZPA92maMDI23xA/40gAFwqAfpyQ │
│      2 │ myid@laptop.local                         │ ecdsa-sha2-nistp256 │ SHA256:0IFv6KPDuNJe2s9PoqUBimreYAYih3sDKcxpCYpZCmE │
└────────┴───────────────────────────────────────────┴─────────────────────┴────────────────────────────────────────────────────┘
```

3. 登録した公開鍵を削除します。

```sh
machbase-neo» ssh-key del <fingerprint>
SSH key deleted successfully.
```

#### パスワードなしでの接続確認 {#비밀번호-없이-접속-확인}

```sh
$ ssh -p 5652 sys@127.0.0.1 ↵

Greetings, SYS
machbase-neo v8.7.1-snapshot (b55f8170 2026-09-10T05:43:13) standard
sys machbase-neo 2026-09-17 17:45:13
> 
```

### SSHでのコマンド実行 {#ssh로-명령-실행}

`ssh`だけで、すべてのmachbase-neoシェルコマンドをリモートから実行できます。

```sh
$ ssh -p 5652 sys@127.0.0.1 'select * from example order by time desc limit 5'↵

┌────────┬────────┬─────────────────────────┬───────────┐
│ ROWNUM │ NAME   │ TIME                    │     VALUE │
├────────┼────────┼─────────────────────────┼───────────┤
│      1 │ signal │ 2026-09-17 17:09:26.712 │ -0.033411 │
│      2 │ signal │ 2026-09-17 17:09:26.711 │ -0.185026 │
│      3 │ signal │ 2026-09-17 17:09:26.71  │ -0.344666 │
│      4 │ signal │ 2026-09-17 17:09:26.709 │ -0.508032 │
│      5 │ signal │ 2026-09-17 17:09:26.708 │ -0.670817 │
└────────┴────────┴─────────────────────────┴───────────┘
5 rows selected.
```

### セキュリティ上の注意 {#보안-주의-사항}

公開鍵認証はパスワード認証より安全ですが、秘密鍵を安全に保管することが非常に重要です。
秘密鍵が漏洩すると、その公開鍵を登録したすべてのシステムにログインされる可能性があります。
