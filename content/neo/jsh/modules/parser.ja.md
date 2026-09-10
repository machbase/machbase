---
toc: true
title: "parser"
type: docs
weight: 100
---

{{< neo_since ver="8.0.75" />}}

`parser`モジュールは、CSVとNDJSONデータ用のストリーミングデコーダーを提供します。
JSHストリームとともに使用するために設計されており、解析したオブジェクトをイベントで渡します。

一般的な使用方法は以下のとおりです。

```js
const parser = require('parser');
```

## エクスポートされるメンバー {#내보내는-구성원}

- `csv(options)`
- `ndjson(options)`
- `CSVParser`
- `NDJSONParser`

## csv() {#csv}

CSVパーサーストリームを作成します。

<h6>構文</h6>

```js
parser.csv([options])
```

<h6>オプション</h6>

| オプション | 型 | 既定値 | 説明 |
|:-------|:-----|:--------|:------------|
| `separator` | String | `,` | フィールド区切り文字 |
| `quote` | String | `"` | 引用符 |
| `escape` | String | `quote`と同じ | エスケープ文字 |
| `headers` | `true` / `false` / `String[]` | `true` | ヘッダーの処理方式 |
| `skipLines` | Number | `0` | 先頭でスキップする行数 |
| `skipComments` | Boolean \| String | `false` | コメント行をスキップ。文字列を指定すると、その文字列をコメントの接頭辞に使用 |
| `strict` | Boolean | `false` | 列数が異なる場合は失敗 |
| `mapHeaders` | Function | | ヘッダー名の変換関数 |
| `mapValues` | Function | | 行を出力する前に値を変換 |
| `trimLeadingSpace` | Boolean | `true` | 各フィールドの先頭の空白を除去 |

<h6>戻り値</h6>

`CSVParser`インスタンスを返します。

## CSVParser {#csvparser}

モジュールがエクスポートするCSVパーサークラスです。

<h6>作成</h6>

```js
new parser.CSVParser([options])
```

コンストラクターは、`parser.csv()`と同じオプションを受け取ります。

<h6>イベント</h6>

- `headers`: ヘッダー行の解析後に1回発生
- `data`: 解析した行オブジェクトごとに発生
- `error`: strictモードでの解析失敗時に発生
- `end`: 上流のストリームが終了すると発生

<h6>プロパティ</h6>

- `bytesWritten`: 受信した入力のバイト数
- `bytesRead`: パーサーが消費したバイト数

<h6>行の構造</h6>

- `headers`を省略するか`true`にすると、最初の有効な行をヘッダーとして使用します。
- `headers`が`false`の場合、フィールド名は`"0"`、`"1"`、`"2"`のようになります。
- `headers`が配列の場合、その名前を使用し、最初の行をデータとして扱います。
- non-strictモードでは、追加の列は`_3`のような`_N`フィールドで出力します。

## ndjson() {#ndjson}

NDJSONパーサーストリームを作成します。

<h6>構文</h6>

```js
parser.ndjson([options])
```

<h6>オプション</h6>

| オプション | 型 | 既定値 | 説明 |
|:-------|:-----|:--------|:------------|
| `strict` | Boolean | `true` | 不正なJSON行で失敗するか、スキップするかを指定 |

<h6>戻り値</h6>

`NDJSONParser`インスタンスを返します。

## NDJSONParser {#ndjsonparser}

モジュールがエクスポートするNDJSONパーサークラスです。

<h6>作成</h6>

```js
new parser.NDJSONParser([options])
```

コンストラクターは、`parser.ndjson()`と同じオプションを受け取ります。

<h6>イベント</h6>

- `data`: 解析したJSONオブジェクトごとに発生
- `warning`: `strict: false`で不正な行をスキップした場合に発生
- `error`: strictモードでの解析失敗時に発生
- `end`: 上流のストリームが終了すると発生

`warning`イベントのオブジェクトには、以下のフィールドがあります。

| プロパティ | 型 | 説明 |
|:---------|:-----|:------------|
| `line` | Number | スキップしたレコードの行番号 |
| `data` | String | 前後の空白を除去した元の行のテキスト |
| `error` | String | 解析エラーメッセージ |

<h6>プロパティ</h6>

- `bytesWritten`: 受信した入力のバイト数
- `bytesRead`: パーサーが消費したバイト数

## CSV 例 {#csv-예제}

```js {linenos=table,linenostart=1}
const fs = require('fs');
const parser = require('parser');

fs.createReadStream('/work/sample.csv')
    .pipe(parser.csv({
        headers: true,
        mapValues: ({ header, value }) => header === 'age' ? parseInt(value, 10) : value,
    }))
    .on('headers', (headers) => {
        console.println(headers.join(','));
    })
    .on('data', (row) => {
        console.println(row.name, row.age);
    });
```

## NDJSON 例 {#ndjson-예제}

```js {linenos=table,linenostart=1}
const fs = require('fs');
const parser = require('parser');

fs.createReadStream('/work/sample.ndjson')
    .pipe(parser.ndjson({ strict: false }))
    .on('data', (obj) => {
        console.println(obj.id);
    })
    .on('warning', (warn) => {
        console.println('Skipped line:', warn.line);
    });
```

## 進捗表示の例 {#진행률-예제}

両パーサーストリームは`bytesWritten`と`bytesRead`を提供するため、ストリーミング中の進捗を追跡できます。

```js {linenos=table,linenostart=1}
const fs = require('fs');
const parser = require('parser');

const decoder = parser.csv();

fs.createReadStream('/work/sample.csv', { highWaterMark: 8 })
    .pipe(decoder)
    .on('data', () => {
        console.println(decoder.bytesWritten, decoder.bytesRead);
    });
```

## 動作に関する注意 {#동작-메모}

- 両パーサークラスは、JSHの`stream.Transform`実装を継承します。
- 解析した行とオブジェクトは、`data`イベントで渡されます。
- 両パーサーとも空行を無視します。
- `NDJSONParser`は、各行を解析する前に`trim()`を適用します。
- `CSVParser`は、`\r\n`形式の入力を処理するため、行末の`\r`を除去します。
