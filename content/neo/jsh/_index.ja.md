---
toc: true
title: JSH
type: docs
weight: 75
tags: JavaScript
---

{{< neo_since ver="8.5.0" />}}

{{< callout type="warning" >}}
**ベータ版について**<br/>
JSHは現在ベータ版です。今後のリリースでAPIやコマンドが変更される可能性があります。
{{< /callout >}}


JSHを使用すると、Machbase Neoを利用するJavaScriptアプリケーションを作成できます。
Machbase Neoは、拡張子が`.js`のファイル、または`index.js`を含むディレクトリを、実行可能なアプリケーションとして認識します。

## コマンド {#명령어}

- `exit` 現在のJSHセッションを終了します。
- `ls` 現在の作業ディレクトリのファイル一覧を表示します。
- `cd` 作業ディレクトリを変更するか、`/work`に移動します。

すべてのコマンドについては、[コマンドリファレンス](./commands/)を参照してください。

## パイプとリダイレクト {#파이프와-리다이렉션}

JSHは、外部コマンドに対してシェル形式のパイプとリダイレクト演算子をサポートします。

- `cmd1 | cmd2`は、`cmd1`の標準出力を`cmd2`の標準入力に渡します。
- `< file`は、ファイルを標準入力にリダイレクトします。
- `> file`は、標準出力をファイルに書き込み、既存の内容を上書きします。
- `>> file`は、標準出力をファイルの末尾に追記します。
- `2> file`は、標準エラー出力をファイルに書き込み、既存の内容を上書きします。
- `2>> file`は、標準エラー出力をファイルの末尾に追記します。
- `2>&1`は、標準エラー出力を標準出力に統合します。

例:

```sh
 cat sample.txt | wc -l
 sort < input.txt > output.txt
 write-stderr boom 1 2> error.log
 write-stderr boom 0 2>&1 | wc -l
```

注意：

- パイプとリダイレクト演算子は、引用符の外側でのみ解釈されます。たとえば、`echo "a | b"`の`|`は通常の文字として扱います。
- パイプラインでは、入力リダイレクトは最初の段階、出力リダイレクトは最後の段階でのみ使用できます。
- `cd`、`ls`、`exit`などの内部コマンドは、リダイレクトにもパイプラインにも対応していません。

## Hello Worldの例 {#hello-world-예제}

以下のコードをコピーし、`hello.js`として保存してください。

```js
console.print("Hello World?\n")
```

「New...」ページで「JSH」を選択します。

{{< figure src="./img/fish.jpg" width="86">}}

`.js`ファイルを実行するためのシンプルなコマンドラインインタープリターとして動作します。

保存したスクリプトを実行するには、次のコマンドを入力します。

```
/work > ./hello.js
Hello World? 
```

{{< figure src="./img/fish-hello.jpg" width="486">}}

## ディレクトリのマウント {#디렉터리-마운트}

JSHランタイムは、ホストOSのファイルシステムから分離された仮想ファイルシステムを使用します。
JSHを起動して内部で`ls -l /`を実行すると、以下のようにホストOSとは異なるディレクトリツリーを確認できます。

{{< figure src="/neo/jsh/img/fish-ls.jpg" width="513">}}

既定のディレクトリのうち、`/sbin`と`/lib`にはJSHに組み込まれた読み取り専用ファイルがあります。 
JSHの起動時に別途指定しない場合、`/work`にはOSの現在のディレクトリ、またはWeb環境のファイルエクスプローラーに表示されるディレクトリが自動的にマウントされます。

任意のディレクトリをマウントするには、`-v mount_point=os_dir`オプションを使用します。
たとえば、OSの`/var/tmp`をJSHの`/tmp`にマウントするには、以下のように実行します。

```sh
$ machbase-neo jsh -v /tmp=/var/tmp
```

{{< figure src="/neo/jsh/img/fish-ls-mount.jpg" width="513">}}

## 外部での実行 {#외부-실행}

作成したJavaScriptアプリケーションは、machbase-neoの実行ファイルがあれば、サーバープロセスから独立した環境で以下のように実行できます。
`machbase-neo jsh`を実行すると、JSHインタープリターが指定したスクリプトを実行します。
この方法では、追加のツールを使わずに、machbase-neo実行ファイルだけでデータベースへの書き込み・検索を行うアプリケーションを作成できます。

短いJavaScriptコードをスクリプトファイルに保存せず、コマンドラインから直接実行するには、
`-C <code>`オプションを使用します。

```sh
$ /path/to/the/machbase-neo jsh -C 'console.println("Hello World?")'
Hello World?
```

ローカルディレクトリをマウントせずに保存済みのスクリプトを実行するには、`-C @script_path`オプションでスクリプトのパスを指定します。

```sh
# hello.jsが./src/hello.jsにある場合
$ /path/to/the/machbase-neo jsh -C @./src/hello.js
Hello World?
```

ローカルディレクトリ内のスクリプトを実行するには、`-v <mount_point>=<src_dir>`オプションを使用します。
このオプションはホストのディレクトリをJSHランタイムにマウントするため、マウント先のパスからスクリプトを実行できます。
特に、スクリプトが同じディレクトリ内の他のファイルに依存する場合に便利です。

```sh
# hello.jsが./src/hello.jsにある場合、srcディレクトリを/scriptにマウントします。
$ /path/to/the/machbase-neo jsh -v /script=./src /script/hello.js
Hello World?
```


## データベースの例 {#데이터베이스-예제}

Machbaseのデータを検索・書き込みするアプリケーションを簡単に作成できます。

```js
'use strict';
// Machbaseクライアントモジュールを読み込みます。
const machcli = require('machcli');
// データベースクライアントのインスタンスを作成します。
const db = new machcli.Client({
    host: '127.0.0.1',
    port: 5656, // Machbaseのネイティブポート
    username:'sys',
    password: 'manager'
})

var conn, rows;
try {
    // データベース接続を作成します。
    conn = db.connect();
    // クエリを実行します。
    rows = conn.query('SELECT NAME, TYPE, COLCOUNT FROM m$sys_tables LIMIT 5');
    // 結果セットを反復処理します。
    for (const row of rows) {
        console.println(row.NAME, row.TYPE, row.COLCOUNT);
    }
} finally {
    // リソースを解放
    rows && rows.close();
    conn && conn.close();
}
```

## モジュール {#모듈}
JSHは、TQLの`SCRIPT()`と`*.js`アプリケーションで使用できるさまざまなJavaScriptモジュールを提供します。
ただし、`$.yield()`などの便利なメソッドを提供するTQLコンテキストオブジェクト`$`はTQL専用で、`*.js`アプリケーションからはアクセスできません。

詳細は、各モジュールのドキュメントを参照してください。

{{< children_toc />}}
