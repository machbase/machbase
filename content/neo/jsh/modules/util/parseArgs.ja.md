---
toc: true
title: "parseArgs"
type: docs
weight: 100
---

{{< neo_since ver="8.0.75" />}}

`util/parseArgs`モジュールは、コマンドライン形式の引数配列を解析します。
`require('util/parseArgs')`で読み込んで使用します。

## parseArgs() {#parseargs}

1つ以上の設定オブジェクトを使って引数配列を解析します。

<h6>構文</h6>

```js
parseArgs(args, ...configs)
```

<h6>パラメーター</h6>

- `args` `String[]`: 解析する引数配列
- `...configs` `Object`: 1つ以上のパーサー設定

複数の設定を渡し、その一部に`command`がある場合、パーサーは`args[0]`とコマンド名を比較し、一致する設定を選択します。

<h6>設定フィールド</h6>

| フィールド | 型 | 既定値 | 説明 |
|:-----|:-----|:-------|:-----|
| `command` | String |        | `args[0]`と照合するサブコマンド名 |
| `options` | Object | `{}` | オプション定義 |
| `strict` | Boolean | `true` | 不明なオプションや想定外の位置引数で例外を発生 |
| `allowNegative` | Boolean | `false` | ブール型の長いオプションに`--no-`形式を許可 |
| `tokens` | Boolean | `false` | 結果にトークン情報を含める |
| `allowPositionals` | Boolean | `positionals`に基づいて決定 | 位置引数を許可するかどうか |
| `positionals` | Array |        | 位置引数の定義一覧 |
| `usage` | String |        | `formatHelp()`で使用 |
| `description` | String |        | `formatHelp()`で使用 |
| `longDescription` | String |        | 複数コマンドのヘルプで使用 |

## オプション定義 {#옵션-정의}

`config.options`の各項目のキーは、JavaScriptのプロパティ名です。
パーサーは、camelCaseの名前をkebab-caseのCLIフラグに自動変換します。

たとえば、`maxRetryCount`は`--max-retry-count`に変換されます。

| フィールド | 型 | 説明 |
|:-----|:-----|:-----|
| `type` | String | `boolean`、`string`、`integer`、`float`のいずれか |
| `short` | String | `-v`の`v`のような1文字の短いフラグ |
| `multiple` | Boolean | 繰り返し指定した値を配列に格納 |
| `default` | any | 解析前に適用する既定値 |
| `description` | String | `formatHelp()`で使用する説明 |

対応する入力形式：

- `--output file.txt`のような長いオプション
- `--output=file.txt`のような長いオプションへのインライン値
- `-o file.txt`のような短いオプション
- `-o=file.txt`のような短いオプションへのインライン値
- `-abc`のような短いブール型オプションのグループ
- オプション終端記号`--`

## 位置引数の定義 {#positional-정의}

`positionals`には、単純な文字列配列または詳細なオブジェクト配列を指定できます。

簡単な形式：

```js
positionals: ['inputFile', 'outputFile']
```

詳細な形式：

```js
positionals: [
    { name: 'input-file' },
    { name: 'output-file', optional: true, default: 'stdout' },
    { name: 'files', variadic: true }
]
```

規則：

- 可変長の位置引数は、最後に指定する必要があります。
- 必須の位置引数がない場合は、`TypeError`が発生します。
- `result.namedPositionals`のキーは、kebab-caseからcamelCaseに変換されます。

## 戻り値 {#반환값}

`parseArgs()`は、以下のフィールドを持つオブジェクトを返します。

| フィールド | 型 | 説明 |
|:-----|:-----|:-----|
| `values` | Object | 解析したオプション値 |
| `positionals` | String[] | 順に格納した位置引数の値 |
| `namedPositionals` | Object | `positionals`の設定がある場合に含む |
| `tokens` | Object[] | `tokens: true`の場合に含む |
| `command` | String | サブコマンドの設定が一致した場合に含む |

## 使用例 {#사용-예시}

```js {linenos=table,linenostart=1}
const parseArgs = require('util/parseArgs');

const result = parseArgs(['-v', '--output', 'file.txt', 'input.sql'], {
    options: {
        verbose: { type: 'boolean', short: 'v' },
        output: { type: 'string' }
    },
    allowPositionals: true,
    positionals: ['input-file']
});

console.println(JSON.stringify(result.values));
console.println(JSON.stringify(result.namedPositionals));
```

## 数値の解析 {#숫자-파싱}

整数には`integer`、小数には`float`を使用します。

- `integer`は、小数点を含む値を許可しません。
- `integer`と`float`は、どちらもJavaScriptのnumberを返します。

```js {linenos=table,linenostart=1}
const parseArgs = require('util/parseArgs');

const result = parseArgs(['--port', '8080', '--ratio', '0.75'], {
    options: {
        port: { type: 'integer' },
        ratio: { type: 'float' }
    }
});
```

## ブール型オプションの否定 {#negative-boolean}

`allowNegative: true`を指定すると、ブール型の長いオプションに`--no-...`形式を使用できます。

```js {linenos=table,linenostart=1}
const parseArgs = require('util/parseArgs');

const result = parseArgs(['--no-color', '--verbose'], {
    options: {
        color: { type: 'boolean' },
        verbose: { type: 'boolean' }
    },
    allowNegative: true
});
```

## サブコマンドの解析 {#sub-command-파싱}

複数の設定を渡すと、最初の引数でコマンド別の設定を選択できます。

```js {linenos=table,linenostart=1}
const parseArgs = require('util/parseArgs');

const commitConfig = {
    command: 'commit',
    options: {
        message: { type: 'string', short: 'm' },
        all: { type: 'boolean', short: 'a' }
    }
};

const pushConfig = {
    command: 'push',
    options: {
        force: { type: 'boolean', short: 'f' }
    },
    allowPositionals: true,
    positionals: ['remote', { name: 'branch', optional: true }]
};

const result = parseArgs(['push', '-f', 'origin', 'main'], commitConfig, pushConfig);
console.println(result.command);
console.println(JSON.stringify(result.namedPositionals));
```

## parseArgs.formatHelp() {#parseargsformathelp}

`parseArgs()`と同じ設定構造を受け取り、読みやすいヘルプテキストを生成します。

<h6>構文</h6>

```js
parseArgs.formatHelp(...configs)
```

次の両方に対応しています。

- 単一コマンドのヘルプ出力
- コマンドの概要とコマンド別の詳細を含む、複数コマンドのヘルプ出力

```js {linenos=table,linenostart=1}
const parseArgs = require('util/parseArgs');

const help = parseArgs.formatHelp({
    usage: 'Usage: myapp [options] <file>',
    options: {
        userName: { type: 'string', short: 'u', description: 'User name', default: 'guest' },
        enableDebug: { type: 'boolean', short: 'd', description: 'Enable debug mode', default: false }
    },
    positionals: [
        { name: 'file', description: 'Input file to process' }
    ]
});

console.println(help);
```

## parseArgs.toKebabCase() {#parseargstokebabcase}

JavaScriptのcamelCaseのオプション名を、CLI用のkebab-case文字列に変換します。

<h6>構文</h6>

```js
parseArgs.toKebabCase(name)
```

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const parseArgs = require('util/parseArgs');

console.println(parseArgs.toKebabCase('maxRetryCount'));
```

## 動作に関する注意 {#동작-참고}

- 第1引数は配列である必要があります。それ以外は`TypeError`が発生します。
- `strict`モードでは、不明なオプションと想定外の位置引数に対して`TypeError`が発生します。
- `multiple: true`は、繰り返し指定した値を配列に格納します。
- 既定値は、明示的なオプション値の解析前に適用します。
