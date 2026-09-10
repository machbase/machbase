---
toc: true
title: "os"
type: docs
weight: 100
---

{{< neo_since ver="8.0.75" />}}

`os`モジュールは、JSHアプリケーション用にNode.js互換のOS情報APIを提供します。

## arch() {#arch}

CPUアーキテクチャを返します。

<h6>構文</h6>

```js
arch()
```

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const os = require('os');
console.println(os.arch());
```

## platform() {#platform}

`darwin`、`linux`、`windows`などのプラットフォーム名を返します。

<h6>構文</h6>

```js
platform()
```

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const os = require('os');
console.println(os.platform());
```

## type() {#type}

`Darwin`、`Linux`、`Windows_NT`などのOSの種類を表す文字列を返します。

<h6>構文</h6>

```js
type()
```

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const os = require('os');
console.println(os.type());
```

## release() {#release}

カーネルのリリース・バージョン文字列を返します。

<h6>構文</h6>

```js
release()
```

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const os = require('os');
console.println(os.release());
```

## hostname() {#hostname}

ホスト名を返します。

<h6>構文</h6>

```js
hostname()
```

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const os = require('os');
console.println(os.hostname());
```

## homedir() {#homedir}

現在のユーザーのホームディレクトリのパスを返します。

<h6>構文</h6>

```js
homedir()
```

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const os = require('os');
console.println(os.homedir());
```

## tmpdir() {#tmpdir}

OSの既定の一時ディレクトリのパスを返します。

<h6>構文</h6>

```js
tmpdir()
```

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const os = require('os');
console.println(os.tmpdir());
```

## endianness() {#endianness}

CPUのエンディアンを返します。値は`BE`または`LE`です。

<h6>構文</h6>

```js
endianness()
```

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const os = require('os');
console.println(os.endianness());
```

## EOL {#eol}

プラットフォーム固有の改行文字列です。

- POSIX: `\n`
- Windows: `\r\n`

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const os = require('os');
console.println(JSON.stringify(os.EOL));
```

## totalmem(), freemem() {#totalmem-freemem}

システムの総メモリまたは空きメモリをバイト単位で返します。

<h6>構文</h6>

```js
totalmem()
freemem()
```

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const os = require('os');
console.println('total:', os.totalmem());
console.println('free :', os.freemem());
```

## uptime() {#uptime}

システムの稼働時間を秒単位で返します。

<h6>構文</h6>

```js
uptime()
```

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const os = require('os');
console.println(os.uptime() >= 0);
```

## bootTime() {#boottime}

システムの起動時刻をUnixタイムスタンプで返します。

<h6>構文</h6>

```js
bootTime()
```

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const os = require('os');
console.println(os.bootTime() > 0);
```

## loadavg() {#loadavg}

平均負荷を`[1分, 5分, 15分]`の配列で返します。

<h6>構文</h6>

```js
loadavg()
```

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const os = require('os');
const avg = os.loadavg();
console.println(Array.isArray(avg), avg.length);
```

## cpus() {#cpus}

CPUコアごとの情報の配列を返します。

各項目には、以下のフィールドが含まれます。

- `model`, `speed`, `cores`
- `vendor`, `family`, `model`, `stepping`
- `times.user`, `times.nice`, `times.sys`, `times.idle`, `times.irq` (ミリ秒)

<h6>構文</h6>

```js
cpus()
```

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const os = require('os');
const list = os.cpus();
console.println(Array.isArray(list), list.length > 0);
```

## cpuCounts() {#cpucounts}

CPU数を返します。

- `true`: 論理コア数
- `false`: 物理コア数

<h6>構文</h6>

```js
cpuCounts(logical)
```

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const os = require('os');
console.println(os.cpuCounts(true));
console.println(os.cpuCounts(false));
```

## cpuPercent() {#cpupercent}

CPU使用率（%）の配列を返します。

- `intervalSec`: サンプリング間隔（秒）。`0`の場合は即時の値
- `perCPU`: `true`の場合、コアごとの値の配列を返す

<h6>構文</h6>

```js
cpuPercent(intervalSec, perCPU)
```

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const os = require('os');
console.println(Array.isArray(os.cpuPercent(0, true)));
```

## networkInterfaces() {#networkinterfaces}

ネットワークインターフェース情報をオブジェクトで返します。

戻り値の形式は以下のとおりです。

- key: インターフェース名
- value: アドレス情報の配列
  - `address`
  - `family` (`IPv4`/`IPv6`)
  - `internal` (boolean)

<h6>構文</h6>

```js
networkInterfaces()
```

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const os = require('os');
const ifaces = os.networkInterfaces();
console.println(typeof ifaces);
```

## hostInfo() {#hostinfo}

ホストシステム情報のオブジェクトを返します。

主なフィールドは以下のとおりです。

- `hostname`, `uptime`, `bootTime`, `procs`
- `os`, `platform`, `platformFamily`, `platformVersion`
- `kernelVersion`, `kernelArch`
- `virtualizationSystem`, `virtualizationRole`, `hostId`

<h6>構文</h6>

```js
hostInfo()
```

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const os = require('os');
const info = os.hostInfo();
console.println(typeof info.hostname, typeof info.uptime);
```

## userInfo() {#userinfo}

現在のユーザー情報を返します。

返されるフィールド：

- `username`, `homedir`, `shell`
- `uid`, `gid`

<h6>構文</h6>

```js
userInfo([options])
```

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const os = require('os');
const user = os.userInfo();
console.println(user.username, user.homedir);
```

## diskPartitions() {#diskpartitions}

ディスクパーティション一覧を返します。

<h6>構文</h6>

```js
diskPartitions([all])
```

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const os = require('os');
const parts = os.diskPartitions();
console.println(Array.isArray(parts), parts.length >= 0);
```

## diskUsage() {#diskusage}

指定したパスのディスク使用量情報を返します。

通常は、`total`、`used`、`free`、`usedPercent`フィールドを含みます。

<h6>構文</h6>

```js
diskUsage(path)
```

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const os = require('os');
const usage = os.diskUsage('.');
console.println(typeof usage.total, typeof usage.usedPercent);
```

## diskIOCounters() {#diskiocounters}

ディスクI/Oカウンターを返します。

- `names`が省略または空配列：すべてのデバイス
- `names`を指定：指定したデバイス

<h6>構文</h6>

```js
diskIOCounters([names])
```

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const os = require('os');
const counters = os.diskIOCounters();
console.println(typeof counters);
```

## netProtoCounters() {#netprotocounters}

ネットワークプロトコルのカウンターを返します。

<h6>構文</h6>

```js
netProtoCounters([proto])
```

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const os = require('os');
const counters = os.netProtoCounters();
console.println(typeof counters);
```

## constants {#constants}

OSに関する定数オブジェクトです。

現在は、以下の子オブジェクトを提供します。

- `os.constants.signals`
- `os.constants.priority`

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const os = require('os');

console.println(typeof os.constants.signals.SIGINT);
console.println(typeof os.constants.priority.PRIORITY_NORMAL);
```

## os.constants.signals {#osconstantssignals}

シグナル名と数値を提供する定数オブジェクトです。

これらの定数は、APIの互換性のため、正規化されたUnix形式のシグナル番号を使用します。
Windowsでは、すべての数値が個別のネイティブシグナル動作に1対1で対応するわけではありません。

たとえば、以下の項目を含みます。

| リテラル | 数値 |
| --- | --- |
| `SIGHUP` | `1` |
| `SIGINT` | `2` |
| `SIGQUIT` | `3` |
| `SIGABRT` | `6` |
| `SIGKILL` | `9` |
| `SIGUSR1` | `10` |
| `SIGSEGV` | `11` |
| `SIGUSR2` | `12` |
| `SIGPIPE` | `13` |
| `SIGALRM` | `14` |
| `SIGTERM` | `15` |

これらの値は、`process.kill()`に数値シグナルとして渡せます。

Windowsでは、`SIGINT`を特別に扱います。
JSHは、可能な限り割り込みに相当するコンソール制御イベントとして渡そうとします。
`SIGTERM`、`SIGQUIT`、`SIGKILL`は、Windowsでは終了要求として動作します。

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const os = require('os');
const process = require('process');

process.kill(12345, os.constants.signals.SIGTERM);
```

## processのシグナルAPIとの関係 {#process-시그널-api와의-관계}

`os.constants.signals`はシグナル番号を提供し、実際のシグナル処理と送信は`process`モジュールが行います。

- シグナルの受信： `process.on('SIGINT', handler)`
- シグナルの送信： `process.kill(pid, os.constants.signals.SIGTERM)`

`process.on()`は大文字と小文字を区別しませんが、シグナルイベント名には`SIGINT`、`sigint`のように`SIG`接頭辞を含む正規名を使用する必要があります。
`term`のような接頭辞のない別名は、シグナルリスナー名として使用できません。

`process.kill()`は、正規名に加えて`term`などの別名を許可します。
`os.constants.signals`は、正規化された定数名だけを提供します。

Windowsの`process.kill(pid, os.constants.signals.SIGINT)`はベストエフォートの動作であり、コンソールのルーティング制約により失敗する場合があります。

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const os = require('os');
const process = require('process');

process.on('sigint', () => {
  console.println('caught');
});

process.kill(process.pid, os.constants.signals.SIGINT);
```

## os.constants.priority {#osconstantspriority}

プロセスの優先度を表す定数オブジェクトです。

<h6>主なフィールド</h6>

| 定数 | 説明 |
| --- | --- |
| `PRIORITY_LOW` | 低い優先度 |
| `PRIORITY_BELOW_NORMAL` | 通常より低い優先度 |
| `PRIORITY_NORMAL` | 既定の優先度 |
| `PRIORITY_ABOVE_NORMAL` | 通常より高い優先度 |
| `PRIORITY_HIGH` | 高い優先度 |
| `PRIORITY_HIGHEST` | 最高の優先度 |

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const os = require('os');
console.println(os.constants.priority.PRIORITY_NORMAL);
console.println(os.constants.priority.PRIORITY_HIGH);
```
