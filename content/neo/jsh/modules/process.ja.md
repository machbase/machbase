---
toc: true
title: "process"
type: docs
weight: 100
---

{{< neo_since ver="8.0.75" />}}

`process`モジュールは、JSHアプリケーションで使用するために設計されています。

## addShutdownHook() {#addshutdownhook}

現在のプロセスの終了時に呼び出すコールバック関数を追加します。

現在の実装では、JSHランタイムが管理する終了処理に入ったときに、このフックを呼び出します。
たとえば、スクリプトが正常に終了した場合や、`process.exit()`を呼び出した場合に実行します。

以下の場合は、呼び出しが保証されません。

- `SIGKILL`や`kill -9`などの強制終了
- OSまたはGoランタイムレベルの致命的な異常終了
- `process.on(signal, handler)`で捕捉していないシグナルの既定動作による終了

捕捉可能なシグナルでクリーンアップが必要な場合は、`process.on(signal, handler)`内でクリーンアップを実行してから終了処理に進むようにしてください。

複数の終了フックを登録すると、登録の逆順に実行します。現在の実装では、フックがpanicや例外を発生させても、残りのフックは実行を続けます。

<h6>構文</h6>

```js
addShutdownHook(()=>{})
```

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
process.addShutdownHook(()=>{
    console.println("shutdown hook called.");
})
console.println("running...")

// 出力：
// running...
// shutdown hook called.
```

<h6>注意事項</h6>

`addShutdownHook()`は、すべての終了状況で呼び出されるわけではありません。強制終了も含めて重要な処理を保護するには、ファイルのフラッシュ、外部トランザクションの終了処理、ロックの解放などをフックだけに依存せず、可能な時点で明示的に実行してください。

## arch {#arch}

ホストマシンのOSアーキテクチャを識別する文字列です。
一般的な値は`amd64`、`aarch64`です。

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
console.println(process.arch);
```

## argv {#argv}

現在のプロセスに渡されたコマンドライン引数の配列です。

- `argv[0]`: JSH実行ファイルの絶対パス
- `argv[1]`: 実行中のスクリプト名（またはパス）
- `argv[2:]`: スクリプトに渡された残りの引数

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
console.println('argv[0]:', process.argv[0]);
console.println('argv[1]:', process.argv[1]);
console.println('argv[2]:', process.argv[2]);
console.println('argv   :', process.argv);
```

## chdir() {#chdir}

現在の作業ディレクトリを変更します。

`path`が空文字列の場合、JSHは`$HOME`として解釈します。

<h6>構文</h6>

```js
chdir(path)
```

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
console.println('before:', process.cwd());
process.chdir('/lib');
console.println('after :', process.cwd());
```

## cpuUsage() {#cpuusage}

CPU使用量情報を返します。

現在の実装はプレースホルダーであり、両フィールドとも数値`0`を返します。

<h6>返されるフィールド</h6>

- `user`
- `system`

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
const cpu = process.cpuUsage();
console.println(typeof cpu.user, typeof cpu.system);
```

## cwd() {#cwd}

現在の作業ディレクトリのパスを返します。

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
console.println(process.cwd());
```

## exit() {#exit}

現在のプロセスを終了します。*code*を省略すると、既定値は`0`です。

<h6>構文</h6>

```js
exit([code])
```

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
process.exit(-1);
```


## which() {#which}

`PATH`からJavaScriptコマンドを検索し、解決したファイルパスを返します。

コマンドに`.js`拡張子がない場合は、自動的に追加します。

<h6>構文</h6>

```js
which(command)
```

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
console.println(process.which('echo')); // 例： /sbin/echo.js
```

## expand() {#expand}

文字列内の`$HOME`、`${HOME}`などの環境変数を展開します。

<h6>構文</h6>

```js
expand(value)
```

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
console.println(process.expand('$HOME/file.txt'));
console.println(process.expand('${HOME}/../lib/file.txt'));
```

## env {#env}

JSHランタイムの環境オブジェクトです。

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
console.println(process.env.get('HOME'));
```


## exec() {#exec}

JavaScriptコマンドファイルを実行し、終了コードを返します。

<h6>構文</h6>

```js
exec(command, ...args)
```

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
const path = process.which('echo');
const code = process.exec(path, 'hello from exec');
console.println('exit code:', code);
```

## execPath {#execpath}

ホストOS上の、現在のプロセスの実行ファイルの絶対パスです。

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
console.println(process.execPath);
```

## execString() {#execstring}

文字列で渡したJavaScriptソースコードを実行し、終了コードを返します。

<h6>構文</h6>

```js
execString(source, ...args)
```

<h6>使用例</h6>


## hrtime() {#hrtime}

高分解能の時刻タプル`[seconds, nanoseconds]`を返します。

以前のタプルを渡すと、その時点からの経過時間を返します。

<h6>構文</h6>

```js
hrtime([previous])
```

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
const start = process.hrtime();
const diff = process.hrtime([start[0], start[1]]);
console.println(Array.isArray(diff), diff.length);
```

## kill() {#kill}

指定したプロセスIDに、実際のOSシグナルを送信します。

- `pid`は正の整数である必要があります。
- `signal`を省略すると、既定値は`SIGTERM`です。
- 成功すると`true`を返します。
- 失敗すると`Error`オブジェクトを返します。
- `signal`には、文字列の名前または数値のシグナル番号を指定できます。

文字列の名前は大文字と小文字を区別せず、`SIG`接頭辞を省略できます。

この別名のサポートは、`process.kill()`に適用されます。

例：

- `SIGTERM`
- `term`
- `sigint`

数値シグナルは、現在以下の値に対応しています。

| 数値 | リテラル |
| --- | --- |
| `0` | なし |
| `1` | `SIGHUP` |
| `2` | `SIGINT` |
| `3` | `SIGQUIT` |
| `6` | `SIGABRT` |
| `9` | `SIGKILL` |
| `10` | `SIGUSR1` |
| `11` | `SIGSEGV` |
| `12` | `SIGUSR2` |
| `13` | `SIGPIPE` |
| `14` | `SIGALRM` |
| `15` | `SIGTERM` |

`signal`の値`0`は、実際のシグナルを送信せずに、対象プロセスの存在と権限を確認するために使用できます。

Windowsの`process.kill(pid, 'SIGINT')`は、Unixの`kill(2)`のように実際のシグナルを直接送信する動作ではありません。
代わりに、対象のプロセスグループが`SIGINT`に近い割り込みとして認識できるよう、コンソール制御イベントの送信を試みます。
これはWindowsでNode.jsの割り込み動作にできるだけ近づけたものですが、ベストエフォートです。
対象はコンソールに接続したプロセスグループである必要があり、Windowsが制御イベントをルーティングできない場合は失敗します。

Windowsの`SIGTERM`、`SIGQUIT`、`SIGKILL`は、Unixのように異なる実シグナルとしてではなく、終了要求として扱います。

<h6>構文</h6>

```js
kill(pid[, signal])
```

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
console.println(process.kill(12345, 'SIGKILL'));
console.println(process.kill(12345, 'term'));
console.println(process.kill(12345, 15));
```

<h6>Windowsの割り込みの例</h6>

```js
const process = require('process');
console.println(process.kill(12345, 'SIGINT'));
```

Windowsが制御イベントをルーティングできない場合、`process.kill()`は`Error`オブジェクトを返します。

<h6>プロセスの存在確認の例</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
console.println(process.kill(process.pid, 0));
```

## memoryUsage() {#memoryusage}

メモリ使用量情報をオブジェクトで返します。

現在の実装はプレースホルダーであり、すべてのフィールドに数値`0`を返します。

<h6>返されるフィールド</h6>

- `rss`
- `heapTotal`
- `heapUsed`
- `external`
- `arrayBuffers`

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
const mem = process.memoryUsage();
console.println(typeof mem.rss, typeof mem.heapUsed);
```

## nextTick() {#nexttick}

次のイベントループで実行するコールバックを予約します。

第1引数が関数でなければ、何もせず`undefined`を返します。

<h6>構文</h6>

```js
nextTick(callback, ...args)
```

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
console.println('main');
process.nextTick((a, b) => console.println('tick:', a, b), 'first', 'second');
```

## now() {#now}

現在時刻をJavaScriptの日時オブジェクトで返します。

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
const now = process.now();
console.println(typeof now); // object
```

## pid {#pid}

現在のプロセスのIDです。
値は数値（Number）で、現在のプロセスIDを表します。

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
console.println(process.pid);
```

## platform {#platform}

ホストマシンのOSプラットフォームを識別する文字列です。
一般的な値は、`windows`、`linux`、`darwin`（macOS）です。

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
console.println(process.platform);
```

## ppid {#ppid}

親プロセスのIDです。
値は数値（Number）で、親プロセスのIDを表します。

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
console.println(process.ppid);
```

## シグナルイベント {#signal-events}

`process`は、`EventEmitter`のようにシグナルイベントを受信できます。

このドキュメントの時点では、以下のシグナル名に対応しています。

- `SIGHUP`
- `SIGINT`
- `SIGQUIT`
- `SIGABRT`
- `SIGKILL`
- `SIGUSR1`
- `SIGSEGV`
- `SIGUSR2`
- `SIGPIPE`
- `SIGALRM`
- `SIGTERM`

シグナルイベントリスナーは、大文字と小文字を区別しません。
イベント名は、`SIG`接頭辞を含む形式にのみ対応しています。

たとえば、以下の名前は同じ動作になります。

- `SIGTERM`
- `sigterm`

`term`などの接頭辞のない別名は、シグナルイベント名として扱いません。
この値は、通常の`EventEmitter`のイベント名として扱います。

リスナーを登録すると、JSHがそのOSシグナルをイベントとして渡します。
リスナーがなければ、OSの既定のシグナル動作に従います。

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const process = require('process');

process.on('sigint', () => {
  console.println('caught SIGINT');
});
```

<h6>対応するリスナー登録の例</h6>

```js
process.on('sigterm', handler);
process.once('SIGTERM', handler);
process.addListener('sigquit', handler);
```

## stdin, stdout, stderr {#stdin-stdout-stderr}

`stdin`、`stdout`、`stderr`のストリームです。

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
process.stdout.write('Enter text: ');
const text = process.stdin.readLine();
console.println('Your input:', text);

// 出力：
// Enter text: hello?
// Your input: hello?
```

## title {#title}

現在のプログラムを識別する文字列です。

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
console.println(process.title);
```

## uptime() {#uptime}

プロセスの稼働時間（秒）を数値で返します。

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
const up = process.uptime();
console.println('uptime >= 0:', up >= 0);
```

## version {#version}

JSHランタイムのバージョンを識別する文字列です。

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
console.println(process.version);
```

## versions {#versions}

ランタイムの詳細なバージョン情報を提供するオブジェクトです。

- `versions.jsh`: JSHランタイムのバージョン文字列
- `versions.go`: Goランタイムのバージョン文字列

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
console.println('jsh:', process.versions.jsh);
console.println('go :', process.versions.go);
```

## which() {#which-1}

`PATH`からJavaScriptコマンドを検索し、解決したファイルパスを返します。

コマンドに`.js`拡張子がない場合は、自動的に追加します。

<h6>構文</h6>

```js
which(command)
```

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
console.println(process.which('echo')); // 例： /sbin/echo.js
```

## dispatchEvent() {#dispatchevent}

JSHイベントループから、イベントエミッターオブジェクトにイベントを配信します。

イベントのスケジュールに成功すると`true`、イベントループが終了済みの場合は`false`を返します。

<h6>構文</h6>

```js
dispatchEvent(target, eventName, ...args)
```

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
process.on('hello', (msg) => console.println(msg));
const ok = process.dispatchEvent(process, 'hello', 'from dispatchEvent');
console.println('scheduled:', ok);
```

## dumpStack() {#dumpstack}

デバッグ用に、指定した深さまで現在のJavaScript呼び出しスタックを出力します。

<h6>構文</h6>

```js
dumpStack(depth)
```

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
function trace() {
  process.dumpStack(5);
}
trace();
```

## expand() {#expand-1}

文字列内の`$HOME`、`${HOME}`などの環境変数を展開します。

<h6>構文</h6>

```js
expand(value)
```

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const process = require('process');
console.println(process.expand('$HOME/file.txt'));
console.println(process.expand('${HOME}/../lib/file.txt'));
```
