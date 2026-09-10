---
toc: true
title: Web UI
type: docs
weight: 15
---

## ログイン {#로그인}

Webブラウザーで[http://127.0.0.1:5654/](http://127.0.0.1:5654/)を開きます。既定のアカウント（**ID** `sys`、**パスワード** `manager`）でログインできます。

> machbase-neoをリモートマシンで実行している場合は、[起動と停止](../start-stop)を参照してリモート接続を許可してください。

{{< figure src="/images/web-login.png" width="600" >}}

## パスワードの変更 {#비밀번호-변경}

セキュリティのため、リモート接続を有効にする前に既定のパスワードを変更することを推奨します。

1. 左下のメニューで「Change password」を選択します。 {{< neo_since ver="8.0.20" />}}

{{< figure src="/neo/getting-started/img/change_passwd_ui.jpg" width="203px" >}}

2. ダイアログで新しいパスワードを入力し、確認のためもう一度入力します。

{{< figure src="/neo/getting-started/img/change_passwd_ui2.jpg" width="342px" >}}

### SQL {#sql}

{{< figure src="/neo/getting-started/img/change_passwd.jpg" width="800px" >}}

```sql
ALTER USER sys IDENTIFIED BY new_password;
```

### コマンドライン {#명령줄}

```sh
machbase-neo shell "ALTER USER SYS IDENTIFIED BY new_password"
```

{{< callout type="info" emoji="❗️">}}
**OSシェルでのエスケープ**<br/>
コマンドラインから非対話モードでSQL文を実行する場合は、OSシェルの特殊文字を必ずエスケープしてください。
たとえば、`machbase-neo shell select * from table`を引用符なしで実行すると、
bash（またはzsh）は`*`を「すべてのファイル」と解釈します。
同じ理由で、`\`、`!`、`$`、引用符にも注意が必要です。
<br/>
neo-shellの対話モードを使用することもできます。
`machbase-neo shell`を実行すると、`machbase-neo >>`プロンプトが表示されます。
この対話モードでは、追加のシェルエスケープは不要です。
{{< /callout >}}
