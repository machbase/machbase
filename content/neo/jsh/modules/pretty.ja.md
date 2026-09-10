---
toc: true
title: "pretty"
type: docs
weight: 100
---

{{< neo_since ver="8.0.75" />}}

`pretty`モジュールは、JSHアプリケーションで値の書式設定とターミナル向けの出力を行います。
読みやすい表、バイト数や時間を表す文字列、長時間処理の進捗表示が必要な場合に便利です。

処理に合わせて、以下のAPIを選択します。

- 罫線付きの表、CSV、TSV、JSON、NDJSON、HTML、Markdown形式には、`Table()`を使用します。
- 読みやすい数値や時間の文字列には、`Bytes()`、`Ints()`、`Durations()`を使用します。
- 長時間実行する処理の進捗をターミナルに表示するには、`Progress()`を使用します。

## インストール {#설치}

```js
const pretty = require('pretty');
```

## Table() {#table}

テーブルwriterを作成します。

<h6>構文</h6>

```js
Table(config)
```

<h6>主なオプション</h6>

| オプション | 型 | 説明 | 既定値 |
| --- | --- | --- | --- |
| `format` | `String` | `box`、`csv`、`tsv`、`json`、`ndjson`、`html`、`md`などの出力形式 | `box` |
| `boxStyle` | `String` | `light`、`double`、`bold`、`rounded`、`simple`、`compact`などの罫線スタイル | `light` |
| `rownum` | `Boolean` | 先頭に`ROWNUM`列を追加するかどうか | `true` |
| `timeformat` | `String` | 日時形式 | `default` |
| `tz` | `String` | `local`、`UTC`、またはIANAタイムゾーン名 | `local` |
| `precision` | `Number` | `0`以上の場合、浮動小数点数を丸める | `-1` |
| `header` | `Boolean` | ヘッダー行を出力するかどうか | `true` |
| `footer` | `Boolean` | フッターまたはキャプションを出力するかどうか | `true` |
| `pause` | `Boolean` | ターミナルでページごとに一時停止するかどうか | `true` |
| `nullValue` | `String` | null値を表示する文字列 | `NULL` |
| `stringEscape` | `Boolean` | 表示できない文字を`\uXXXX`にエスケープ | `false` |

<h6>主なメソッド</h6>

- `appendHeader(values)` ヘッダー行を追加
- `appendRow(row)` 単一行を追加
- `appendRows(rows)` 複数行を追加
- `append(values)` 行または行の一覧を追加
- `row(...values)` テーブルの変換規則を適用した行を作成
- `render()` 現在の出力結果を文字列で返す
- `close()` 残りの行を出力し、最後の結果を返す
- `resetRows()` バッファー内の行をクリア
- `pauseAndWait()` ページ表示モードでキー入力を待つ

<h6>使用例: 基本的な罫線付きテーブル</h6>

```js {linenos=table,linenostart=1}
const pretty = require('pretty');
const tw = pretty.Table({ boxStyle: 'light' });
tw.appendHeader(['Name', 'Age']);
tw.appendRow(tw.row('Alice', 30));
tw.appendRow(tw.row('Bob', 25));
console.println(tw.render());
```

出力：

```text
┌────────┬───────┬─────┐
│ ROWNUM │ NAME  │ AGE │
├────────┼───────┼─────┤
│      1 │ Alice │  30 │
│      2 │ Bob   │  25 │
└────────┴───────┴─────┘
```

<h6>使用例: 浮動小数点数の丸め</h6>

```js {linenos=table,linenostart=1}
const pretty = require('pretty');
const tw = pretty.Table({ boxStyle: 'light', precision: 2 });
tw.appendHeader(['Item', 'Price']);
tw.appendRow(tw.row('Apple', 1.234));
tw.appendRow(tw.row('Orange', 2.567));
console.println(tw.render());
```

出力：

```text
┌────────┬────────┬───────┐
│ ROWNUM │ ITEM   │ PRICE │
├────────┼────────┼───────┤
│      1 │ Apple  │  1.23 │
│      2 │ Orange │  2.57 │
└────────┴────────┴───────┘
```

<h6>使用例: 時刻の書式設定</h6>

```js {linenos=table,linenostart=1}
const pretty = require('pretty');
const tw = pretty.Table({ boxStyle: 'light', timeformat: 'DATETIME', tz: 'UTC' });
tw.appendHeader(['Event', 'Time']);
tw.append(['Start', new Date('2024-03-15T14:30:45.000Z')]);
tw.append(['End', new Date('2024-03-15T18:20:30.000Z')]);
console.println(tw.render());
```

出力：

```text
┌────────┬───────┬─────────────────────┐
│ ROWNUM │ EVENT │ TIME                │
├────────┼───────┼─────────────────────┤
│      1 │ Start │ 2024-03-15 14:30:45 │
│      2 │ End   │ 2024-03-15 18:20:30 │
└────────┴───────┴─────────────────────┘
```

組み込みの`timeformat`キーワードは、`DATETIME`、`DATE`、`TIME`、`RFC3339`、`RFC1123`、
`ANSIC`、`KITCHEN`、`STAMP`、`STAMPMILLI`、`STAMPMICRO`、`STAMPNANO`です。
必要に応じて、Go形式の時刻レイアウト文字列を直接渡すこともできます。

<h6>使用例: 罫線スタイル</h6>

```js {linenos=table,linenostart=1}
const pretty = require('pretty');
for (const style of ['light', 'double', 'bold', 'rounded', 'compact']) {
	const tw = pretty.Table({ boxStyle: style, rownum: false });
	tw.appendHeader(['Col']);
	tw.appendRow(tw.row('Val'));
	console.println(style + ':');
	console.println(tw.render());
}
```

出力例の一部を以下に示します。

```text
light:
┌─────┐
│ COL │
├─────┤
│ Val │
└─────┘

double:
╔═════╗
║ COL ║
╠═════╣
║ Val ║
╚═════╝

compact:
 COL 
─────
 Val 
```

<h6>使用例: JSON出力</h6>

```js {linenos=table,linenostart=1}
const pretty = require('pretty');
const tw = pretty.Table({ format: 'json', rownum: false });
tw.appendHeader(['ID', 'Status', 'Value']);
tw.append([1, 'active', 42.5]);
tw.append([2, 'pending', 31.2]);
console.println(tw.render());
```

出力：

```json
{"columns":["ID","Status","Value"],"rows":[[1,"active",42.5],[2,"pending",31.2]]}
```

<h6>使用例: CSV出力</h6>

```js {linenos=table,linenostart=1}
const pretty = require('pretty');
const tw = pretty.Table({ format: 'csv', rownum: false });
tw.appendHeader(['Name', 'Score']);
tw.append(['Alice', 98]);
tw.append(['Bob', 87]);
console.println(tw.render());
```

出力：

```text
Name,Score
Alice,98
Bob,87
```

<h6>使用例: TSV出力</h6>

```js {linenos=table,linenostart=1}
const pretty = require('pretty');
const tw = pretty.Table({ format: 'tsv', rownum: false });
tw.appendHeader(['Name', 'Score']);
tw.append(['Alice', 98]);
tw.append(['Bob', 87]);
console.println(tw.render());
```

出力：

```text
Name	Score
Alice	98
Bob	87
```

<h6>使用例: NDJSON出力</h6>

```js {linenos=table,linenostart=1}
const pretty = require('pretty');
const tw = pretty.Table({ format: 'ndjson', rownum: false });
tw.appendHeader(['Name', 'Score']);
tw.append(['Alice', 98]);
tw.append(['Bob', 87]);
console.println(tw.render());
```

出力：

```json
{"Name":"Alice","Score":98}
{"Name":"Bob","Score":87}
```

<h6>使用例: Markdown出力</h6>

```js {linenos=table,linenostart=1}
const pretty = require('pretty');
const tw = pretty.Table({ format: 'md', rownum: false });
tw.appendHeader(['Name', 'Score']);
tw.append(['Alice', 98]);
tw.append(['Bob', 87]);
console.println(tw.render());
```

出力：

```md
| Name  | Score |
| ----- | ----: |
| Alice |    98 |
| Bob   |    87 |
```

<h6>使用例: 表示できない文字のエスケープ</h6>

```js {linenos=table,linenostart=1}
const pretty = require('pretty');
const tw = pretty.Table({ stringEscape: true, rownum: false });
tw.appendHeader(['Value']);
tw.appendRow(tw.row('hello\u0007world'));
console.println(tw.render());
```

`stringEscape`が`true`の場合、表示できない文字をエスケープしたUnicode文字列で表示します。

## MakeRow() {#makerow}

指定したサイズの空の行配列を作成します。

<h6>構文</h6>

```js
MakeRow(size)
```

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const pretty = require('pretty');
const row = pretty.MakeRow(3);
console.println(row.length);
console.println(Array.isArray(row));
```

## Progress() {#progress}

ターミナル用の進捗writerを作成します。

<h6>構文</h6>

```js
Progress(options)
```

<h6>オプション</h6>

- `showPercentage` `Boolean` 百分率を表示するかどうか。既定値`true`
- `showETA` `Boolean` 予想残り時間を表示するかどうか。既定値`true`
- `showSpeed` `Boolean` 処理速度を表示するかどうか。既定値`true`
- `updateFrequency` `Number` 更新間隔（ミリ秒）。既定値`250`
- `trackerLength` `Number` プログレスバーの長さ。既定値`20`

返されるwriterは、`tracker(options)`を提供します。
trackerは`message`と`total`を受け取り、`increment(n)`、`value()`、`markAsDone()`、`isDone()`に対応しています。

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const pretty = require('pretty');
const pw = pretty.Progress({ showPercentage: true, showETA: true });
const tracker = pw.tracker({ message: 'Processing', total: 100 });

let interval = setInterval(function() {
	tracker.increment(10);
	if (tracker.value() >= 100) {
		tracker.markAsDone();
		clearInterval(interval);
	}
}, 200);
```

この機能は、対話型のターミナルセッション用です。テストや非対話実行では、バーの表示そのものより、
`isDone()`の状態に達することが重要です。

## Bytes() {#bytes}

バイト数を読みやすい文字列に整形します。

<h6>構文</h6>

```js
Bytes(value)
```

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const pretty = require('pretty');
console.println(pretty.Bytes(512));
console.println(pretty.Bytes(1536));
console.println(pretty.Bytes(1048576));
console.println(pretty.Bytes(1073741824));
```

出力：

```text
512B
1.5KB
1.0MB
1.0GB
```

## Ints() {#ints}

整数を桁区切り付きの文字列に整形します。

<h6>構文</h6>

```js
Ints(value)
```

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const pretty = require('pretty');
console.println(pretty.Ints(1234567890));
console.println(pretty.Ints(0));
console.println(pretty.Ints(-999));
```

出力：

```text
1,234,567,890
0
-999
```

## Durations() {#durations}

ナノ秒単位の時間を、短く読みやすい文字列に整形します。

<h6>構文</h6>

```js
Durations(nanoseconds)
```

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const pretty = require('pretty');
console.println(pretty.Durations(1234));
console.println(pretty.Durations(2340000));
console.println(pretty.Durations(3010000000));
console.println(pretty.Durations(3661000000000));
console.println(pretty.Durations(86400000000000));
```

出力：

```text
1.23μs
2.34ms
3.01s
1h 1m
1d 0h
```

60秒未満の値は、`μs`、`ms`、`s`などの単位で小数表示します。
それ以上の時間は、`2m 5s`、`1h 1m`、`2d 0h`のように上位2つの単位だけを表示します。

## Align {#align}

詳細な列設定で使用する配置定数を提供します。

使用できる定数は、`default`、`left`、`center`、`justify`、`right`、`auto`です。

## ターミナルヘルパー {#terminal-helpers}

このモジュールは、以下のヘルパーも提供します。

- `isTerminal()` stdinがターミナルに接続されているかどうかを返す
- `getTerminalSize()` ターミナルの幅と高さを返す
- `pauseTerminal()` キー入力を待ち、`q`または`Q`なら`false`を返す
- `parseTime(value, format, tz)` 文字列を時刻値として解析

これらのヘルパーは、主に`Table()`や`Progress()`を使った対話型ターミナルツールの作成に便利です。
