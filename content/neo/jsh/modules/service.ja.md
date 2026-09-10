---
toc: true
title: "service"
type: docs
weight: 100
---

{{< neo_since ver="8.0.75" />}}

`service`モジュールは、JSHアプリケーションからサービスコントローラーのJSON-RPC APIを呼び出すクライアントモジュールです。

一般的な使用方法は以下のとおりです。

```js
const service = require('service');
```

サービスコントローラーのアドレスは、通常はシェルやセッションが設定した`SERVICE_CONTROLLER`環境変数から取得します。

コントローラーは実行ごとにランダムなアドレスで待ち受ける場合があるため、通常はアドレスをハードコードしません。
別のコントローラーアドレスが既知の場合や、明示的に別のコントローラーへ接続する必要がある場合にのみ、`options.controller`を使用します。

## Client {#client}

`Client`は、サービスコントローラーと通信する基本クライアント型です。

再利用するクライアントインスタンスが必要な場合は、`new service.Client(...)`を使用してください。

<h6>構文</h6>

```js
new Client([options])
```

<h6>オプション</h6>

| オプション       | 型     | 既定値 | 説明 |
|:-----------|:---------|:-------|:-----|
| controller | String   |        | 明示的に使用するコントローラーアドレス。省略すると`SERVICE_CONTROLLER`環境変数を使用します。 |
| timeout    | Number   | `5000` | RPCのタイムアウト（ミリ秒）。コールバック方式のリクエストが完了またはタイムアウトするまで、その寿命を維持するためにも同じ値を使用します。 |

`controller`には、固定の既定アドレスはありません。
`SERVICE_CONTROLLER`がなく、`options.controller`も指定しない場合、クライアントの作成は失敗します。

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const service = require('service');
const client = new service.Client({ timeout: 1000 });
```

上記の例は、`SERVICE_CONTROLLER`環境変数が設定済みであることを前提とします。

明示的に別のコントローラーアドレスを使用する場合にのみ、以下のように`controller`を指定します。

```js {linenos=table,linenostart=1}
const service = require('service');
const client = new service.Client({
    controller: 'unix:///tmp/example-service-controller.sock',
    timeout: 1000,
});
```

<h6>主なプロパティ</h6>

- `controller`
- `timeout`
- `runtime`
- `details`

**Client メソッド**

- `call(method[, params], callback)`
- `status([name], callback)`
- `read(callback)`
- `update(callback)`
- `reload(callback)`
- `install(config, callback)`
- `uninstall(name, callback)`
- `start(name, callback)`
- `stop(name, callback)`

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const service = require('service');
const client = new service.Client();

client.status((err, services) => {
    if (err) {
        console.println(err.message);
        return;
    }
    console.println('count=', services.length);
});
```

## call() {#call}

任意のサービスコントローラーRPCメソッドを直接呼び出します。

<h6>構文</h6>

```js
client.call(method[, params], callback)
```

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const service = require('service');
const client = new service.Client();

client.call('service.list', null, (err, result) => {
    if (err) {
        console.println(err.message);
        return;
    }
    console.println(result.length);
});
```

## status() {#status}

現在のサービス状態を取得します。

- `name`を省略すると、サービス一覧のスナップショットを返します。
- `name`を指定すると、単一サービスのスナップショットを返します。
- このメソッドは、`servicectl status [service_name]`コマンドの形式に対応しています。

<h6>構文</h6>

```js
client.status([name], callback)
```

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const service = require('service');
const client = new service.Client();

client.status((err, services) => {
    if (err) {
        console.println(err.message);
        return;
    }
    console.println('count=', services.length);
});

client.status('alpha', (err, snapshot) => {
    if (err) {
        console.println(err.message);
        return;
    }
    console.println(snapshot.status);
});
```

## read() {#read}

サービス設定ディレクトリを再読み込みし、最新の再読み込みスナップショットを返します。

<h6>構文</h6>

```js
client.read(callback)
```

## update() {#update}

現在の再読み込みスナップショットを適用し、更新結果を返します。

- `update()`は、現在の再読み込み結果に含まれる差分だけを適用します。
- 再読み込み結果の影響を受けるサービスだけを、停止・開始・追加・削除します。

<h6>構文</h6>

```js
client.update(callback)
```

## reload() {#reload}

設定を再読み込みし、その結果を直ちに適用します。

- `reload()`は`update()`と異なり、現在実行中のすべてのサービスを先に停止します。
- その後、現在の設定で`enable`になっているサービスだけを再起動します。
- そのため、`reload()`前に実行中だったサービスでも、現在の設定で`enable`でなければ再起動しません。

<h6>構文</h6>

```js
client.reload(callback)
```

## install() {#install}

設定オブジェクトからサービスをインストールし、そのサービスのスナップショットを返します。

<h6>構文</h6>

```js
client.install(config, callback)
```

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const service = require('service');
const client = new service.Client();

client.install({
    name: 'alpha',
    enable: false,
    executable: 'echo',
    args: ['hello'],
}, (err, snapshot) => {
    if (err) {
        console.println(err.message);
        return;
    }
    console.println(snapshot.config.name, snapshot.status);
});
```

## uninstall() {#uninstall}

サービスを削除し、成功時に`true`を返します。

<h6>構文</h6>

```js
client.uninstall(name, callback)
```

## start() {#start}

サービスを開始し、更新したサービスのスナップショットを返します。

<h6>構文</h6>

```js
client.start(name, callback)
```

## stop() {#stop}

サービスを停止し、更新したサービスのスナップショットを返します。

<h6>構文</h6>

```js
client.stop(name, callback)
```

## runtime.get() {#runtimeget}

サービスのランタイムスナップショットを取得します。

- 戻り値には、`output`と`details`が含まれます。

<h6>構文</h6>

```js
client.runtime.get(name, callback)
```

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const service = require('service');
const client = new service.Client();

client.runtime.get('alpha', (err, runtime) => {
    if (err) {
        console.println(err.message);
        return;
    }
    console.println(JSON.stringify(runtime.details || {}));
});
```

## details.get() {#detailsget}

サービスのdetail値を取得します。

- `key`を省略すると、`details`全体のスナップショットを返します。
- `key`を指定し、そのキーがない場合は、エラーを返します。

<h6>構文</h6>

```js
client.details.get(name[, key], callback)
```

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const service = require('service');
const client = new service.Client();

client.details.get('alpha', 'health', (err, runtime) => {
    if (err) {
        console.println(err.message);
        return;
    }
    console.println(runtime.details.health);
});
```

## details.add() {#detailsadd}

新しいdetailのキーと値を追加します。

- 同じキーが存在する場合は、エラーを返します。

<h6>構文</h6>

```js
client.details.add(name, key, value, callback)
```

## details.update() {#detailsupdate}

既存のdetailのキーと値を更新します。

- キーが存在しない場合は、エラーを返します。

<h6>構文</h6>

```js
client.details.update(name, key, value, callback)
```

## details.set() {#detailsset}

detailのキーと値を設定します。

- キーがなければ作成し、あれば上書きします。

<h6>構文</h6>

```js
client.details.set(name, key, value, callback)
```

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const service = require('service');
const client = new service.Client();

client.details.set('alpha', 'health', 'ok', (err, runtime) => {
    if (err) {
        console.println(err.message);
        return;
    }
    console.println(runtime.details.health);
});
```

## details.delete() {#detailsdelete}

detailのキーを削除します。

- キーがない場合は、エラーを返します。

<h6>構文</h6>

```js
client.details.delete(name, key, callback)
```

## resolveController() {#resolvecontroller}

コントローラーのアドレスを決定します。

- 引数を渡すと、その値を使用します。
- 引数がなければ、`SERVICE_CONTROLLER`環境変数を参照します。

<h6>構文</h6>

```js
resolveController([value])
```

<h6>動作例</h6>

```js {linenos=table,linenostart=1}
const service = require('service');
console.println(service.resolveController());
console.println(service.resolveController('unix:///tmp/example-service-controller.sock'));
```

## 動作に関する注意 {#동작-참고}

- すべてのAPIはコールバック方式の非同期形式です。
- コントローラーへの接続失敗、タイムアウト、RPCエラーは、コールバックの第1引数に渡されます。
- サービスRPCの処理中は、短いトップレベルスクリプトがコールバック前に終了しないように、モジュールが内部でリクエストの寿命を維持します。
- このkeepalive期間は、実際の`timeout`値に従い、リクエストが成功・失敗・タイムアウトのいずれかで完了すると直ちに解放されます。
- `new Client()`は、`options.controller`を省略すると、既定で`SERVICE_CONTROLLER`を使用します。
