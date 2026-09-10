---
toc: true
title: コマンドリファレンス
type: docs
weight: 10
---

このページでは、JSHシェルですぐに使用できる基本コマンドを機能別に説明します。

## 概要 {#개요}

コマンドは使用目的ごとに分類しています。

**注意**

- すべてのコマンドは、既定ではホストOSではなくJSHの仮想ファイルシステム上で動作します。
- 相対パスは、現在のJSH作業ディレクトリを基準に解釈します。
- 作業ディレクトリや環境変数など、現在のシェルの状態を変更するコマンドも含みます。
- 一部のコマンドは、Unixツールの機能の一部だけを提供します。

## ファイルシステムコマンド {#filesystem-commands}

### cd {#cd}

現在のJSHシェルセッションの作業ディレクトリを変更します。

<h6>構文</h6>

```sh
cd [directory]
```

引数を省略すると、`$HOME`に移動します。
対象パスがない場合は、エラーを出力し、0以外のステータスを返します。

<h6>使用例</h6>

```sh
/work > cd subdir
/work/subdir >
/work/subdir > cd
/work >
```

### cat {#cat}

ファイルの内容を連結して標準出力に出力します。
行番号、行末の表示、タブの表示、空行の圧縮、構文強調に対応しています。

<h6>構文</h6>

```sh
cat [OPTION]... [FILE]...
```

<h6>オプション</h6>

- `-n, --number` すべての出力行に番号を付けます。
- `-E, --showEnds` 各行の末尾に`$`を表示します。
- `-T, --showTabs` タブ文字を`^I`で表示します。
- `-s, --squeeze` 連続する空行を1行にまとめます。
- `-c, --color` 構文強調を有効にします。
- `-h, --help` ヘルプを表示します。

`-c`は、`.js`、`.json`、`.ndjson`、`.sql`、`.csv`、`.yaml`、`.yml`、`.toml`ファイルの構文強調に対応しています。

<h6>使用例</h6>

```sh
/work > cat -n notes.txt
/work > cat -c script.js
/work > cat -sE log.txt
```

### ls {#ls}

ディレクトリの内容を一覧表示します。
既定の出力は列形式で、隠しファイル、詳細表示、時刻順のソート、再帰的な検索に対応しています。

<h6>構文</h6>

```sh
ls [OPTION]... [PATH]...
```

<h6>オプション</h6>

- `-l, --long` 詳細な一覧形式で出力します。
- `-a, --all` 隠しファイルを含めます。
- `-t, --time` 更新時刻の降順にソートします。
- `-R, --recursive` サブディレクトリを再帰的に一覧表示します。

パス引数では、`*`と`?`のワイルドカードも使用できます。

<h6>使用例</h6>

```sh
/work > ls
/work > ls -la
/work > ls -t /lib
/work > ls -R src
/work > ls *.js
```

### mkdir {#mkdir}

1つ以上のディレクトリを作成します。

<h6>構文</h6>

```sh
mkdir [OPTION]... DIRECTORY...
```

<h6>オプション</h6>

- `-p, --parents` 必要な親ディレクトリも作成します。
- `-v, --verbose` 作成したディレクトリごとにメッセージを出力します。
- `-h, --help` ヘルプを表示します。

`-p`を指定せずに既存のディレクトリを作成すると、エラーを返します。

<h6>使用例</h6>

```sh
/work > mkdir data
/work > mkdir -p logs/app/2026
/work > mkdir -pv build/output
```

### pwd {#pwd}

現在の作業ディレクトリを出力します。

<h6>構文</h6>

```sh
pwd
```

<h6>使用例</h6>

```sh
/work > pwd
/work
```

### rm {#rm}

ファイルやディレクトリを削除します。

<h6>構文</h6>

```sh
rm [OPTION]... FILE...
```

<h6>オプション</h6>

- `-r, -R, --recursive` ディレクトリとその内容を再帰的に削除します。
- `-d, --dir, --directory` 空のディレクトリを削除します。
- `-f, --force` 存在しないパスやオペランド不足のエラーを無視します。
- `-v, --verbose` 削除したパスごとにメッセージを出力します。
- `-h, --help` ヘルプを表示します。

<h6>使用例</h6>

```sh
/work > rm old.txt
/work > rm -rf cache
/work > rm -d empty-dir
/work > rm -fv temp.txt missing.txt
```

## 環境コマンド {#environment-commands}

### env {#env}

環境変数を出力します。
引数を省略するとすべての環境変数をソートして出力し、変数名を指定するとその変数だけを出力します。

<h6>構文</h6>

```sh
env [NAME]...
```

<h6>使用例</h6>

```sh
/work > env
/work > env HOME PWD
```

### alias {#alias}

現在のシェルセッションにコマンドエイリアスを登録するか、表示します。
`alias`だけを実行すると、定義済みのエイリアスをソートして出力します。`alias NAME`は、指定した1つのエイリアスを出力します。
`alias NAME COMMAND [ARG]...`形式でエイリアスを登録すると、その後入力したコマンドの先頭で展開されます。

<h6>構文</h6>

```sh
alias
alias NAME
alias NAME COMMAND [ARG]...
```

<h6>使用例</h6>

```sh
/work > alias ll ls -l
/work > ll
/work > alias
/work > alias ll
```

### setenv {#setenv}

現在のシェルセッションの環境変数を設定します。

<h6>構文</h6>

```sh
setenv NAME VALUE
setenv NAME=VALUE
```

変数名は英字または`_`で始め、その後は英字、数字、`_`だけを使用できます。

<h6>使用例</h6>

```sh
/work > setenv GREETING hello
/work > setenv MESSAGE='hello world'
```

### unsetenv {#unsetenv}

現在のシェルセッションから環境変数を削除します。

<h6>構文</h6>

```sh
unsetenv NAME
```

変数名が不正な場合や引数が不足している場合は、使用方法を表示します。

<h6>使用例</h6>

```sh
/work > unsetenv GREETING
```

## システムコマンド {#system-commands}

### pkg {#pkg}

JSHパッケージとプロジェクトのマニフェストを管理します。
サブコマンド、オプション、手順は、[パッケージマネージャー](../packages/)を参照してください。

<h6>構文</h6>

```sh
pkg <command> [options] [args...]
```

### servicectl {#servicectl}

サービスコントローラーを介して、長時間実行するJSHサービスを管理します。
サブコマンド、オプション、サービスの管理手順は、[サービスマネージャー](../services/)を参照してください。

<h6>構文</h6>

```sh
servicectl [--controller=<addr>] <command> [args...]
```

**servicectl controller**

サービスコントローラーのRPCランタイムメトリクスを取得・リセットします。

<h6>構文</h6>

```sh
servicectl [--controller=<addr>] controller [metrics|get|reset]
```

<h6>動作</h6>

- `controller`と`controller metrics`は同じです。
- `controller get`は、`controller metrics`の別名です。
- `controller reset`は、累積カウンターをリセットし、新しい集計期間を開始します。
- `high_water_mark_connections`は、最後のリセット以降の同時RPC接続数の最大値（ピーク値）を保持します。

<h6>使用例</h6>

```sh
servicectl controller metrics
servicectl controller reset
servicectl controller get
```

## テキスト・ユーティリティコマンド {#text-and-utility-commands}

### echo {#echo}

引数を空白で区切って出力し、末尾に改行を追加します。

<h6>構文</h6>

```sh
echo [ARG]...
```

現在の実装は、`-n`などのシェル形式のフラグや、エスケープシーケンスの解釈には対応していません。

<h6>使用例</h6>

```sh
/work > echo hello world
hello world
```

### sleep {#sleep}

指定した秒数だけ待機して終了します。

<h6>構文</h6>

```sh
sleep [OPTION] <sec>
```

<h6>オプション</h6>

- `-h, --help` ヘルプを表示します。

<h6>使用例</h6>

```sh
/work > sleep 5
```


### tail {#tail}

ファイルの末尾を出力します。
`-f`オプションを指定すると、ファイルに追加された内容をリアルタイムに出力し続けます。

```sh
tail [OPTION]... <file>
```

<h6>オプション</h6>

- `-n, --lines <N>` 末尾のN行を出力します。既定値は`10`です。
- `-f, --follow` ファイルに追加された内容を出力し続けます。`SIGINT`または`SIGTERM`を受信すると終了します。
- `-h, --help` ヘルプを表示します。

<h6>使用例</h6>

```sh
/work > tail app.log
/work > tail -n 20 app.log
/work > tail -f app.log
```

### viz {#viz}

可視化仕様（vizspec、ADVN）を表示・検証・ファイル出力します。
JSHまたはMachbase Neoのワークフローで生成した、レンダラーに依存しない分析結果を扱うユーザー向けコマンドです。

<h6>構文</h6>

```sh
viz <command> [options] <file>
```

<h6>サブコマンド</h6>

- `viz view [options] <file>` vizspecをTUIブロックとして描画します。
- `viz validate <file>` vizspecファイルを検証します。
- `viz export [options] <file>` vizspecをSVGに出力します。

<h6>`view` オプション</h6>

- `--compact` 系列の要約と生データ表を非表示にします。
- `--rows <n>` ブロックごとの詳細行数を制限します。
- `--width <n>` スパークライン、棒グラフ、タイムラインの幅を指定します。
- `--verbose-meta` ブロックのメタデータを表示します。
- pretty-tableオプションも併用できます。

<h6>`export` オプション</h6>

- `--format svg` 出力形式です。現在は`svg`だけに対応しています。
- `-o, --output <file>` 標準出力ではなく、ファイルにSVGを保存します。
- `--width <n>` SVGの幅をピクセル単位で指定します。
- `--height <n>` SVGの高さをピクセル単位で指定します。
- `--padding <n>` SVGの外側の余白をピクセル単位で指定します。
- `--title <text>` SVGのタイトルを指定します。
- `--background <color>` SVGの背景色を指定します。
- `--font-family <name>` SVGのフォントファミリーを指定します。
- `--font-size <n>` SVGの既定のフォントサイズをピクセル単位で指定します。
- `--hide-legend` 凡例を非表示にします。

<h6>使用例</h6>

```sh
/work > viz validate sensor-overview.json
/work > viz view --width 80 sensor-overview.json
/work > viz export --title "CPU Overview" --output cpu.svg sensor-overview.json
```

### wc {#wc}

ファイルごとの行数、単語数、バイト数、文字数を数えます。
ファイルを省略するか`-`を指定すると、標準入力を読み取ります。

<h6>構文</h6>

```sh
wc [OPTION]... [FILE]...
```

<h6>オプション</h6>

- `-l, --lines` 行数を出力します。
- `-w, --words` 単語数を出力します。
- `-c, --bytes` バイト数を出力します。
- `-m, --chars` 文字数を出力します。
- `-h, --help` ヘルプを表示します。

オプションを省略すると、既定で行数、単語数、バイト数を出力します。

<h6>使用例</h6>

```sh
/work > wc notes.txt
/work > wc -l *.log
/work > cat notes.txt | wc -w -
```

### which {#which}

指定したコマンドの、JSHコマンドパス内での場所を出力します。

<h6>構文</h6>

```sh
which <command>
```

コマンドが見つからない場合は、エラーを出力し、0以外のステータスを返します。

<h6>使用例</h6>

```sh
/work > which ls
/sbin/ls.js
```

## メッセージングコマンド {#messaging-commands}

### mqtt_pub {#mqtt_pub}

MQTTブローカーにメッセージを発行します。

<h6>構文</h6>

```sh
mqtt_pub [OPTION]...
```

<h6>オプション</h6>

- `-t, --topic` 発行先のトピックです。
- `-b, --broker` ブローカーアドレスです。既定値は`tcp://localhost:5653`です。
- `-m, --message` 直接指定するメッセージペイロードです。
- `-f, --file` ペイロードを読み取るファイルです。
- `-q, --qos` MQTTのQoSレベルです。`0`、`1`、`2`に対応しています。
- `-d, --debug` デバッグログを出力します。
- `-h, --help` ヘルプを表示します。

`-m`と`-f`は併用できません。

<h6>使用例</h6>

```sh
/work > mqtt_pub -t sensors/temp -m '{"value":21.5}'
/work > mqtt_pub -b tcp://broker:1883 -t logs/app -f payload.json -q 1
```

### nats_pub {#nats_pub}

NATSサブジェクトにメッセージを発行します。
応答サブジェクトを指定するか、requestモードで1件の応答を待機できます。

<h6>構文</h6>

```sh
nats_pub [OPTION]...
```

<h6>オプション</h6>

- `-t, --topic` 発行先のサブジェクトです。
- `-s, --subject` `--topic`と同じ意味の別名です。
- `-b, --broker` ブローカーアドレスです。既定値は`nats://localhost:4222`です。
- `-m, --message` 直接指定するメッセージペイロードです。
- `-f, --file` ペイロードを読み取るファイルです。
- `-r, --reply` 応答を待機する応答サブジェクトです。
- `--request` 一時的なinboxサブジェクトを作成し、1件の応答を待ちます。
- `--timeout` 接続と応答待ちのタイムアウトです。既定値は`10000`msです。
- `-d, --debug` デバッグログを出力します。
- `-h, --help` ヘルプを表示します。

`-m`と`-f`は併用できません。

<h6>使用例</h6>

```sh
/work > nats_pub -t events.demo -m 'hello'
/work > nats_pub -s rpc.echo -m 'ping' --request
/work > nats_pub -s rpc.echo -m 'ping' -r reply.demo --timeout 3000
```

## 対話型コマンド {#interactive-commands}

### repl {#repl}

JSHのJavaScript REPLを開始します。
コマンドシェルとは異なり、JavaScript式を直接実行する対話環境です。

<h6>構文</h6>

```sh
repl
```

### shell {#shell}

新しいJSHシェルセッションを開始します。
現在の環境を基に、別のシェルループを実行する場合に使用します。

<h6>構文</h6>

```sh
shell
```
