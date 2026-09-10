---
toc: true
title: "readline"
type: docs
weight: 100
---

{{< neo_since ver="8.0.75" />}}

`readline`モジュールは、JSHアプリケーションで対話的な行入力を処理します。
JSHのネイティブreadline実装をラップする、`ReadLine`クラスを提供します。

一般的な使用方法は以下のとおりです。

```js
const { ReadLine } = require('readline');
```

## ReadLine {#readline}

対話型の行リーダーを作成します。

<h6>構文</h6>

```js
new ReadLine([options])
```

<h6>オプション</h6>

| オプション | 型 | 既定値 | 説明 |
|:-----|:-----|:-------|:-----|
| history | String | `readline` | JSHの設定ディレクトリに保存する履歴ファイルの名前です。 |
| prompt | Function | 組み込みプロンプト | 各行に表示するプロンプト文字列を返すコールバックです。 |
| submitOnEnterWhen | Function | 常に確定 | Enterキーで現在の入力を確定するかどうかを決めるコールバックです。 |
| autoInput | String[] |        | 主に自動テストで使用する入力シーケンスです。 |

`prompt`を省略すると、最初の行は`> `、2行目以降は`. `形式の継続プロンプトを使用します。
`history`を省略すると、既定の履歴ファイル名は`readline`になります。
`history`オプションはパスではなくファイル名として扱い、実際の履歴ファイルは`$HOME/.config/.jsh/`に保存します。`history`にはファイル名だけを指定し、ディレクトリ区切り文字を含めないでください。

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const { ReadLine } = require('readline');

const reader = new ReadLine({
    prompt: (lineno) => lineno === 0 ? 'prompt> ' : '....... ',
});
```

## readLine() {#readline-1}

1つの論理的な入力値を読み取ります。

- 単一行の入力では、1つの文字列を返します。
- 複数行の入力では、各行を`\n`で連結した文字列を返します。
- ネイティブリーダーがエラーで終了すると、JSHは`Error`オブジェクトを返します。

<h6>構文</h6>

```js
reader.readLine([options])
```

`readLine()`は、コンストラクターと同じ形式のオプションを受け取ります。
呼び出し時のオプションが、コンストラクターのオプションより優先されます。

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const { ReadLine } = require('readline');

const reader = new ReadLine({
    prompt: () => 'input> ',
});
const line = reader.readLine();
if (line instanceof Error) {
    throw line;
}
console.println(line);
```

## addHistory() {#addhistory}

readlineの履歴に1行を追加します。

<h6>構文</h6>

```js
reader.addHistory(line)
```

同じ内容の行がある場合は、既存の項目を削除してから末尾に再追加します。

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const { ReadLine } = require('readline');

const reader = new ReadLine();
const line = reader.readLine();
if (line instanceof Error) {
    throw line;
}
reader.addHistory(line);
```

## close() {#close}

現在のreadlineセッションを終了します。

<h6>構文</h6>

```js
reader.close()
```

`readLine()`が入力待ちの間に`close()`を呼び出すと、待機中の呼び出しは`EOF`で終了します。

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const { ReadLine } = require('readline');

const reader = new ReadLine();
const timer = setTimeout(() => {
    reader.close();
}, 200);
const line = reader.readLine();
clearTimeout(timer);
```

## prompt オプション {#prompt-옵션}

`prompt`は、各行のプロンプト文字列を生成します。

<h6>シグネチャ</h6>

```js
prompt(lineno) => string
```

- `lineno`は0から始まります。
- その行に表示するプロンプト文字列をそのまま返します。

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const { ReadLine } = require('readline');

const reader = new ReadLine({
    prompt: (lineno) => lineno === 0 ? 'sql> ' : '...> ',
});
```

## submitOnEnterWhen オプション {#submitonenterwhen-옵션}

`submitOnEnterWhen`は、Enterキーで現在の入力を確定するか、複数行の編集を続けるかを決めます。

<h6>シグネチャ</h6>

```js
submitOnEnterWhen(lines, idx) => boolean
```

- `lines`は、現在までの行の配列です。
- `idx`は、現在の行インデックスです。
- `true`を返すと確定し、`false`を返すと編集を続けます。

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const { ReadLine } = require('readline');

const reader = new ReadLine({
    submitOnEnterWhen: (lines, idx) => {
        return lines[idx].endsWith(';');
    },
});
```

## autoInput オプション {#autoinput-옵션}

`autoInput`は、用意した入力をリーダーに渡します。
主にテストと非対話型スクリプトに使用します。

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const { ReadLine } = require('readline');

const reader = new ReadLine({
    autoInput: [
        'Hello World',
        ReadLine.CtrlJ,
    ],
});
```

## 複数行入力の例 {#multi-line-입력-예시}

`submitOnEnterWhen`は、現在の行がアプリケーションの規則を満たすまで編集を続けるためによく使用します。

```js {linenos=table,linenostart=1}
const { ReadLine } = require('readline');

const reader = new ReadLine({
    autoInput: ['select *', ReadLine.Enter, 'from dual;', ReadLine.Enter],
    submitOnEnterWhen: (lines, idx) => {
        return lines[idx].endsWith(';');
    },
});
const text = reader.readLine();
console.println(text);
```

## 静的なキー定数 {#정적-키-상수}

`ReadLine`は、入力のシミュレーションやキー処理に使用できるさまざまなキー定数を提供します。
代表的な定数は以下のとおりです。

- Controlキー： `CtrlA` ... `CtrlZ`, `CtrlLeft`, `CtrlRight`, `CtrlUp`, `CtrlDown`
- 移動キー： `Up`, `Down`, `Left`, `Right`, `Home`, `End`, `PageUp`, `PageDown`
- 編集キー： `Backspace`, `Delete`, `Enter`, `ShiftTab`, `Escape`
- Altキー： `AltA` ... `AltZ`, `ALTBackspace`
- ファンクションキー： `F1` ... `F24`

名前の全一覧は、`ReadLine`の静的プロパティを参照してください。

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const { ReadLine } = require('readline');

console.printf('%X\n', ReadLine.CtrlJ);
```

## 動作に関する注意 {#동작-참고}

- JavaScriptレベルでは、コールバックを使わず同期的に読み取ります。`readLine()`は、確定した値を直接返します。
- 実際の行編集、カーソル移動、履歴、複数行入力は、ネイティブバックエンドが処理します。
- `readLine()`は`Error`オブジェクトを返す場合があるため、失敗を明示的に処理する場合は`line instanceof Error`を確認してください。
- `close()`は、タイマーや他のイベントから入力待ちを中断する場合に主に使用します。
