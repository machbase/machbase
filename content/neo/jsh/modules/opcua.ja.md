---
toc: true
title: "opcua"
type: docs
weight: 100
---

{{< neo_since ver="8.0.75" />}}

`opcua`モジュールは、JSHアプリケーションからOPC UAサーバーを読み書きするクライアントAPIを提供します。

## Client {#client}

OPC UAクライアントオブジェクトです。

<h6>作成</h6>

```js
new Client(options)
```

- 戻り値: `Client`
- `options`を省略すると、例外（`missing client options`）が発生します。

<h6>オプション</h6>

| オプション                | 型     | 既定値                          | 説明 |
|:--------------------|:---------|:--------------------------------|:-----|
| endpoint            | `string` | `""`                            | OPC UAサーバーのエンドポイント（`opc.tcp://host:port`） |
| readRetryInterval   | `number` | `100`（100ms未満の場合は100に補正） | `read()`の再試行間隔（ミリ秒） |
| messageSecurityMode | `number` | `MessageSecurityMode.None`      | セキュリティモード。[MessageSecurityMode](#messagesecuritymode)を参照 |

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const ua = require("opcua");
const nodes = [
    "ns=1;s=NoPermVariable",
    "ns=1;s=ReadWriteVariable",
    "ns=1;s=ReadOnlyVariable",
    "ns=1;s=NoAccessVariable",
];

let client;
try {
    client = new ua.Client({ endpoint: "opc.tcp://localhost:4840" });
    const values = client.read({
        nodes,
        timestampsToReturn: ua.TimestampsToReturn.Both,
    });
    values.forEach((v, idx) => {
        console.println(nodes[idx], v.status, v.statusCode, v.value, v.type);
    });
} catch (e) {
    console.println("Error:", e);
} finally {
    if (client !== undefined) client.close();
}
```

### close() {#close}

クライアント接続を閉じます。

<h6>構文</h6>

```js
close()
```

- 戻り値: 成功時は`null`

### read() {#read}

指定したノード一覧の値を読み取ります。

<h6>構文</h6>

```js
read(readRequest)
```

<h6>パラメーター</h6>

- `readRequest` (`object`): [ReadRequest](#readrequest)

<h6>戻り値</h6>

- `object[]`: [ReadResult](#readresult)の配列

エラー時の動作：

- `nodes`がない場合や空の場合は、例外が発生します。

### write() {#write}

1つ以上のノード値を書き込みます。

<h6>構文</h6>

```js
write(...writeRequest)
```

<h6>パラメーター</h6>

- `writeRequest` (`object`, 可変長引数): [WriteRequest](#writerequest)

<h6>戻り値</h6>

- `object`: [WriteResult](#writeresult)

エラー時の動作：

- 引数がない場合は例外（`missing argument`）

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const ua = require("opcua");

let client;
try {
    client = new ua.Client({ endpoint: "opc.tcp://localhost:4840" });

    let rsp = client.read({ nodes: ["ns=1;s=rw_bool", "ns=1;s=rw_int32"] });
    console.println("read response:", rsp[0].value, rsp[1].value);

    rsp = client.write(
        { node: "ns=1;s=rw_bool", value: false },
        { node: "ns=1;s=rw_int32", value: 1234 },
    );
    console.println("write response error:", rsp.error, ", results:", rsp.results);

    rsp = client.read({ nodes: ["ns=1;s=rw_bool", "ns=1;s=rw_int32"] });
    console.println("read response:", rsp[0].value, rsp[1].value);
} catch (e) {
    console.println("Error:", e);
} finally {
    if (client !== undefined) client.close();
}
```

### browse() {#browse}

1つ以上のノードの参照を検索します。

<h6>構文</h6>

```js
browse(browseRequest)
```

<h6>パラメーター</h6>

- `browseRequest` (`object`): [BrowseRequest](#browserequest)

<h6>戻り値</h6>

- `object[]`: [BrowseResult](#browseresult)の配列

エラー時の動作：

- `nodes`がない場合や空の場合は、例外が発生します。

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const ua = require("opcua");

let client;
try {
    client = new ua.Client({ endpoint: "opc.tcp://localhost:4840" });
    const results = client.browse({
        nodes: ["ns=1;i=85"],
        nodeClassMask: ua.NodeClass.Variable,
        requestedMaxReferencesPerNode: 2,
    });

    console.println("continuationPoint:", results[0].continuationPoint);
    results[0].references.forEach((ref) => {
        console.println(ref.browseName, ref.nodeId, ref.nodeClass);
    });
} catch (e) {
    console.println("Error:", e);
} finally {
    if (client !== undefined) client.close();
}
```

### browseNext() {#browsenext}

`browse()`または`browseNext()`が返した継続ポイントを使って、次のページを取得します。

<h6>構文</h6>

```js
browseNext(browseNextRequest)
```

<h6>パラメーター</h6>

- `browseNextRequest` (`object`): [BrowseNextRequest](#browsenextrequest)

<h6>戻り値</h6>

- `object[]`: [BrowseResult](#browseresult)の配列

エラー時の動作：

- `continuationPoints`がない場合や空の場合は、例外が発生します。

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const ua = require("opcua");

let client;
try {
    client = new ua.Client({ endpoint: "opc.tcp://localhost:4840" });

    let results = client.browse({
        nodes: ["ns=1;i=85"],
        nodeClassMask: ua.NodeClass.Variable,
        requestedMaxReferencesPerNode: 2,
    });

    while (results[0].continuationPoint) {
        results = client.browseNext({
            continuationPoints: [results[0].continuationPoint],
        });
        results[0].references.forEach((ref) => {
            console.println(ref.browseName, ref.nodeId, ref.nodeClass);
        });
    }
} catch (e) {
    console.println("Error:", e);
} finally {
    if (client !== undefined) client.close();
}
```

### children() {#children}

指定したノードの直接の子参照を返します。

<h6>構文</h6>

```js
children(childrenRequest)
```

<h6>パラメーター</h6>

- `childrenRequest` (`object`): [ChildrenRequest](#childrenrequest)

<h6>戻り値</h6>

- `object[]`: [ChildrenResult](#childrenresult)の配列

エラー時の動作：

- `node`がない場合や空の場合は、例外が発生します。

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const ua = require("opcua");

let client;
try {
    client = new ua.Client({ endpoint: "opc.tcp://localhost:4840" });
    const refs = client.children({
        node: "ns=1;i=85",
        nodeClassMask: ua.NodeClass.Variable,
    });

    refs.forEach((ref) => {
        console.println(ref.browseName, ref.nodeId, ref.nodeClass);
    });
} catch (e) {
    console.println("Error:", e);
} finally {
    if (client !== undefined) client.close();
}
```

## ReadRequest {#readrequest}

| プロパティ            | 型       | 既定値                       | 説明 |
|:--------------------|:-----------|:-----------------------------|:-----|
| nodes               | `string[]` |                               | 読み取るOPC UAノードIDの一覧 |
| maxAge              | `number`   | `0`                           | 許容するキャッシュの経過時間（ミリ秒） |
| timestampsToReturn  | `number`   | `TimestampsToReturn.Neither` | タイムスタンプの返却方針 |

## ReadResult {#readresult}

| プロパティ        | 型     | 説明 |
|:----------------|:---------|:-----|
| status          | `number` | OPC UAステータスコード（`uint32`） |
| statusText      | `string` | 状態テキスト |
| statusCode      | `string` | ステータスコード名（例：`StatusGood`） |
| value           | `any`    | 読み取った値 |
| type            | `string` | 値の型名（例：`Boolean`、`Int32`、`Double`） |
| sourceTimestamp | `number` | ソースタイムスタンプ（Unixエポックミリ秒） |
| serverTimestamp | `number` | サーバータイムスタンプ（Unixエポックミリ秒） |

## WriteRequest {#writerequest}

| プロパティ | 型     | 説明 |
|:---------|:---------|:-----|
| node     | `string` | 書き込み先のノードID |
| value    | `any`    | 書き込む値 |

## WriteResult {#writeresult}

| プロパティ      | 型       | 説明 |
|:--------------|:-----------|:-----|
| error         | `Error\|null` | リクエスト処理のエラー |
| timestamp     | `number`   | レスポンスタイムスタンプ（Unixエポックミリ秒） |
| requestHandle | `number`   | OPC UAリクエストハンドル |
| serviceResult | `number`   | OPC UAサービスの結果コード |
| stringTable   | `string[]` | OPC UA文字列テーブル |
| results       | `number[]` | ノードごとのステータスコードの配列 |

## BrowseRequest {#browserequest}

| プロパティ                      | 型       | 既定値                    | 説明 |
|:------------------------------|:-----------|:--------------------------|:-----|
| nodes                         | `string[]` |                           | 検索するOPC UAノードIDの一覧 |
| browseDirection               | `number`   | `BrowseDirection.Forward` | 検索方向 |
| referenceTypeId               | `string`   | すべての参照            | 追跡する参照型のノードID |
| includeSubtypes               | `boolean`  | `true`                    | `referenceTypeId`のサブタイプを含めるかどうか |
| nodeClassMask                 | `number`   | `0`                       | 含めるノードクラスのビットマスク |
| resultMask                    | `number`   | `BrowseResultMask.All`    | 返すフィールドのビットマスク |
| requestedMaxReferencesPerNode | `number`   | `0`                       | サーバーがページ分割して返す、ノードごとの最大参照数のヒント |

## BrowseNextRequest {#browsenextrequest}

| プロパティ                 | 型       | 既定値  | 説明 |
|:-------------------------|:-----------|:--------|:-----|
| continuationPoints       | `string[]` |         | `browse()`または`browseNext()`が返したbase64形式の継続ポイントの一覧 |
| releaseContinuationPoints| `boolean`  | `false` | 次の参照を要求せずに、サーバー側の継続ポイントを解放するかどうか |

## BrowseResult {#browseresult}

| プロパティ          | 型       | 説明 |
|:------------------|:-----------|:-----|
| status            | `number`   | OPC UAステータスコード（`uint32`） |
| statusText        | `string`   | 状態テキスト |
| continuationPoint | `string`   | base64形式の継続ポイント。次のページがない場合は空文字列 |
| references        | `object[]` | [BrowseReference](#browsereference)の配列 |

## BrowseReference {#browsereference}

| プロパティ        | 型      | 説明 |
|:----------------|:----------|:-----|
| referenceTypeId | `string`  | 参照型のノードID |
| isForward       | `boolean` | 順方向の参照かどうか |
| nodeId          | `string`  | 対象のノードID |
| browseName      | `string`  | ブラウズ名 |
| displayName     | `string`  | 表示名 |
| nodeClass       | `number`  | OPC UAノードクラスの値 |
| typeDefinition  | `string`  | 型定義のノードID |

## ChildrenRequest {#childrenrequest}

| プロパティ      | 型     | 説明 |
|:--------------|:---------|:-----|
| node          | `string` | 親ノードID |
| nodeClassMask | `number` | 含めるノードクラスのビットマスク |

## ChildrenResult {#childrenresult}

| プロパティ        | 型      | 説明 |
|:----------------|:----------|:-----|
| referenceTypeId | `string`  | 参照型のノードID |
| isForward       | `boolean` | 順方向の参照かどうか |
| nodeId          | `string`  | 子ノードID |
| browseName      | `string`  | ブラウズ名 |
| displayName     | `string`  | 表示名 |
| nodeClass       | `number`  | OPC UAノードクラスの値 |
| typeDefinition  | `string`  | 型定義のノードID |

## BrowseDirection {#browsedirection}

- `BrowseDirection.Forward`
- `BrowseDirection.Inverse`
- `BrowseDirection.Both`
- `BrowseDirection.Invalid`

## NodeClass {#nodeclass}

- `NodeClass.Unspecified`
- `NodeClass.Object`
- `NodeClass.Variable`
- `NodeClass.Method`
- `NodeClass.ObjectType`
- `NodeClass.VariableType`
- `NodeClass.ReferenceType`
- `NodeClass.DataType`
- `NodeClass.View`

## BrowseResultMask {#browseresultmask}

- `BrowseResultMask.None`
- `BrowseResultMask.ReferenceTypeId`
- `BrowseResultMask.IsForward`
- `BrowseResultMask.NodeClass`
- `BrowseResultMask.BrowseName`
- `BrowseResultMask.DisplayName`
- `BrowseResultMask.TypeDefinition`
- `BrowseResultMask.All`
- `BrowseResultMask.ReferenceTypeInfo`
- `BrowseResultMask.TargetInfo`

## MessageSecurityMode {#messagesecuritymode}

- `MessageSecurityMode.None`
- `MessageSecurityMode.Sign`
- `MessageSecurityMode.SignAndEncrypt`
- `MessageSecurityMode.Invalid`

## TimestampsToReturn {#timestampstoreturn}

- `TimestampsToReturn.Source`
- `TimestampsToReturn.Server`
- `TimestampsToReturn.Both`
- `TimestampsToReturn.Neither`
- `TimestampsToReturn.Invalid`

## OPCUAクライアント {#opcua-클라이언트}

この例は、OPC UAサーバーに接続してシステムメトリクスを読み取り、データベースに保存する収集プログラムを実装します。

**処理の流れ**

1. OPC UA連携：`opcua`モジュールで`opc.tcp://localhost:4840`サーバーに接続し、`sys_cpu`、`sys_mem`、`load1`などのノード値を取得します。
2. 定期収集：`setInterval()`で10秒ごとにデータを読み取ります。
3. データの取り込み：収集した値を、`EXAMPLE`テーブルの`name`、`time`、`value`列に保存します。

### データ収集プログラム {#데이터-수집기}

スクリプトを`opcua-client.js`として保存し、JSHターミナルでバックグラウンド実行してください。

```
jsh / > opcua-client
jsh / > ps
┌──────┬──────┬──────┬──────────────────┬────────┐ 
│  PID │ PPID │ USER │ NAME             │ UPTIME │ 
├──────┼──────┼──────┼──────────────────┼────────┤ 
│ 1044 │ 1    │ sys  │ /opcua-client.js │ 13s    │ 
│ 1045 │ 1025 │ sys  │ ps               │ 0s     │ 
└──────┴──────┴──────┴──────────────────┴────────┘ 
```

- opcua-client.js

```js {linenos=table,linenostart=1}
opcua = require("opcua");
process = require("process");
machcli = require("machcli");

const nodes = [
    "ns=1;s=sys_cpu",
    "ns=1;s=sys_mem",
    "ns=1;s=load1",
    "ns=1;s=load5",
    "ns=1;s=load15",
];
const tags = [
    "sys_cpu", "sys_mem", "sys_load1", "sys_load5", "sys_load15"
];
const dbConf = { host: '127.0.0.1', port: 5656, user: 'sys', password: 'manager' };
const sqlText = `INSERT INTO EXAMPLE (name,time,value) values(?,?,?)`;
const uaClient = new opcua.Client({ endpoint: "opc.tcp://localhost:4840" });
process.addShutdownHook(()=>{
    uaClient.close();
});
setInterval(()=>{
    const ts = process.now();
    const vs = uaClient.read({
        nodes: nodes,
        timestampsToReturn: opcua.TimestampsToReturn.Both
    });
    var dbClient, conn;
    try {
        dbClient = new machcli.Client(dbConf);
        conn = dbClient.connect();
        vs.forEach((v, idx) => {
            if( v.value !== null ) {
                conn.exec(sqlText, tags[idx], ts, v.value);
            }
        })
    } catch (e) {
        console.println("Error:", e.message);
    } finally {
        conn && conn.close();
        dbClient && dbClient.close();
    }
}, 10*1000);
```

### シミュレーターサーバー {#시뮬레이터-서버}

`opcua-client.js`をテストするには、必要なシステムメトリクスのノードを提供するOPC UAサーバーが必要です。
実環境がない場合は、以下のリポジトリが提供するシミュレーターを使用してください。
`sys_cpu`、`sys_mem`、`load1`、`load5`、`load15`などのサンプルデータを提供し、収集と可視化の流れを検証できます。

設定方法は、リポジトリの手順に従ってください。

[https://github.com/machbase/neo-server/tree/main/jsh/native/opcua/test_server](https://github.com/machbase/neo-server/tree/main/jsh/native/opcua/test_server)

シミュレーターを起動してから`opcua-client.js`を実行すると、OPC UAクライアントが接続してデータを収集します。
