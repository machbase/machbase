---
toc: true
title: シェル
type: docs
weight: 21
---

## Web経由のリモート接続 {#웹을-통한-원격-접속}

Shellタブをクリックすると、Web上で対話型シェルを実行できます。

{{< figure src="/images/web-shell-pick.png" width="600" >}}

{{< figure src="/images/web-shell-ui.png" width="600" >}}

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

1. 左下のメニューで「SSH Keys」を選択します。 {{< neo_since ver="8.0.20" />}}

{{< figure src="./img/ssh_keys.jpg" width="207px" >}}

2. 「New SSH Key」ボタンをクリックし、公開鍵を入力してタイトルを指定します。
   最後に「Add SSH Key」ボタンを押して登録を完了します。

{{< figure src="./img/ssh_keys2.jpg" width="630px" >}}

3. 登録したSSHキーが一覧に表示されます。

{{< figure src="./img/ssh_keys3.jpg" width="630px" >}}

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
┌────────┬────────────────────────────┬─────────────────────┬──────────────────────────────────┐
│ ROWNUM │ NAME                       │ KEY TYPE            │ FINGERPRINT                      │
├────────┼────────────────────────────┼─────────────────────┼──────────────────────────────────┤
│      1 │ myid@laptop.local          │ ssh-rsa             │ 80bdaba07591276d065ca915a6037fde │
│      2 │ myid@desktop.local         │ ecdsa-sha2-nistp256 │ e300ee460b890ad4c22cd4c1eae03477 │
└────────┴────────────────────────────┴─────────────────────┴──────────────────────────────────┘
```

3. 登録した公開鍵を削除します。

```sh
machbase-neo» ssh-key del <fingerprint>
```

#### パスワードなしでの接続確認 {#비밀번호-없이-접속-확인}

```sh
$ ssh -p 5652 sys@127.0.0.1 ↵

Greetings, SYS
machbase-neo v8.0.20-snapshot (8f10fa95 2024-06-19T16:32:09) standard
sys machbase-neo»
```

### SSHでのコマンド実行 {#ssh로-명령-실행}

`ssh`だけで、すべてのmachbase-neoシェルコマンドをリモートから実行できます。

```sh
$ ssh -p 5652 sys@127.0.0.1 'select * from example order by time desc limit 5'↵

 ROWNUM  NAME      TIME(UTC)            VALUE     
──────────────────────────────────────────────────
 1       wave.sin  2023-02-09 11:46:46  0.406479  
 2       wave.cos  2023-02-09 11:46:46  0.913660  
 3       wave.sin  2023-02-09 11:46:45  -0.000281 
 4       wave.cos  2023-02-09 11:46:45  1.000000  
 5       wave.cos  2023-02-09 11:46:44  0.913431  
```

### セキュリティ上の注意 {#보안-주의-사항}

公開鍵認証はパスワード認証より安全ですが、秘密鍵を安全に保管することが非常に重要です。
秘密鍵が漏洩すると、その公開鍵を登録したすべてのシステムにログインされる可能性があります。
