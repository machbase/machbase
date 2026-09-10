---
toc: true
title: "dbus"
type: docs
weight: 100
---

{{< neo_since ver="8.5.5" />}}

`dbus`モジュールは、JSHアプリケーション用のLinux専用D-Bus APIを提供します。
メソッド呼び出し、プロパティの読み書き、イントロスペクション、シグナル購読、名前の所有者の監視に対応しています。

## モジュールの読み込み {#모듈-로드}

```js
const dbus = require("dbus");
const conn = new dbus.Connection({ busType: dbus.BusType.Session });
```

ランタイムのOSがLinux以外の場合、接続の作成は失敗します。

## BusType {#bustype}

- `dbus.BusType.Session`
- `dbus.BusType.System`

## Connection {#connection}

D-Bus接続オブジェクトです。

<h6>作成</h6>

```js
new dbus.Connection(options)
```

<h6>オプション</h6>

| オプション | 型 | 既定値 | 説明 |
|:-----|:-----|:-------|:-----|
| busType | `string` | `dbus.BusType.Session` | D-Busバスの種類 |

<h6>戻り値</h6>

- `Connection`

エラー時の動作：

- `busType`が不正な場合は、例外が発生します。
- プラットフォームがLinux以外の場合は、例外が発生します。

### close() {#close}

現在のD-Bus接続を閉じます。

<h6>構文</h6>

```js
conn.close()
```

<h6>戻り値</h6>

- `undefined`

このメソッドは冪等であり、複数回呼び出しても安全です。

### object() {#object}

指定したdestination/pathにバインドされた[ObjectProxy](#objectproxy)を作成します。

<h6>構文</h6>

```js
conn.object(destination, path)
```

<h6>パラメーター</h6>

- `destination` (`string`): サービス名（例：`org.freedesktop.DBus`）
- `path` (`string`): オブジェクトパス（例：`/org/freedesktop/DBus`）

<h6>戻り値</h6>

- `ObjectProxy`

### call() {#call}

D-Busメソッドを呼び出します。

<h6>構文</h6>

```js
conn.call(request)
```

<h6>パラメーター</h6>

- `request` (`object`): [CallRequest](#callrequest)

<h6>戻り値</h6>

- `object`: [CallResult](#callresult)

エラー時の動作：

- 必須フィールドがない場合は、例外が発生します。
- オブジェクトパスが不正な場合は、例外が発生します。

### getProperty() {#getproperty}

D-Busプロパティを読み取ります。

<h6>構文</h6>

```js
conn.getProperty(request)
```

<h6>パラメーター</h6>

- `request` (`object`): [PropertyRequest](#propertyrequest)

<h6>戻り値</h6>

- `object`: [PropertyResult](#propertyresult)

### setProperty() {#setproperty}

D-Busプロパティを書き込みます。

<h6>構文</h6>

```js
conn.setProperty(request)
```

<h6>パラメーター</h6>

- `request` (`object`): [SetPropertyRequest](#setpropertyrequest)

<h6>戻り値</h6>

- `undefined`

### introspect() {#introspect}

オブジェクトのイントロスペクションメタデータを取得します。

<h6>構文</h6>

```js
conn.introspect(request)
```

<h6>パラメーター</h6>

- `request` (`object`): [IntrospectRequest](#introspectrequest)

<h6>戻り値</h6>

- `object`: [IntrospectionNode](#introspectionnode)

### subscribeSignal() {#subscribesignal}

条件に一致するD-Busシグナルを購読します。

<h6>構文</h6>

```js
conn.subscribeSignal(request)
```

<h6>パラメーター</h6>

- `request` (`object`): [SignalWatchRequest](#signalwatchrequest)

<h6>戻り値</h6>

- `Connection` (メソッドチェーンに対応)

エラー時の動作：

- すべての一致条件フィールドが空の場合は、`missing signal match criteria`例外が発生します。

### unsubscribeSignal() {#unsubscribesignal}

登録済みのシグナル購読を解除します。

<h6>構文</h6>

```js
conn.unsubscribeSignal(request)
```

<h6>パラメーター</h6>

- `request` (`object`): [SignalWatchRequest](#signalwatchrequest)

<h6>戻り値</h6>

- `Connection` (メソッドチェーンに対応)

エラー時の動作：

- 一致する購読がない場合は、例外が発生します。

### watchName() {#watchname}

バス名の所有者の変更監視を開始します。

<h6>構文</h6>

```js
conn.watchName(name)
```

<h6>パラメーター</h6>

- `name` (`string`): D-Bus well-known name

<h6>戻り値</h6>

- `Connection` (メソッドチェーンに対応)

### unwatchName() {#unwatchname}

バス名の所有者の変更監視を停止します。

<h6>構文</h6>

```js
conn.unwatchName(name)
```

<h6>パラメーター</h6>

- `name` (`string`): D-Bus well-known name

<h6>戻り値</h6>

- `Connection` (メソッドチェーンに対応)

エラー時の動作：

- 実行中の監視がない場合は、`name watch not found`例外が発生します。

### getNameOwner() {#getnameowner}

バス名の現在の所有者を取得します。

<h6>構文</h6>

```js
conn.getNameOwner(name)
```

<h6>パラメーター</h6>

- `name` (`string`): D-Bus well-known name

<h6>戻り値</h6>

- `object`: [NameOwnerResult](#nameownerresult)

名前に所有者がない場合は、例外をスローせず`hasOwner: false`を返します。

## イベント {#이벤트}

`Connection`は、`EventEmitter`を継承します。

### signal {#signal}

購読したD-Busシグナルを受信するたびに発生します。

```js
conn.on("signal", (sig) => {
    console.println(sig.interface, sig.member, sig.body);
});
```

### name-owner-changed {#name-owner-changed}

監視中の名前の所有者が変わると発生します。

```js
conn.on("name-owner-changed", (evt) => {
    console.println(evt.name, evt.oldOwner, evt.newOwner);
});
```

## ObjectProxy {#objectproxy}

`conn.object(destination, path)`で作成します。

### call() {#call-1}

```js
obj.call(method, ...args)
```

- 戻り値: [CallResult](#callresult)と同じ構造

### getProperty() / get() {#getproperty--get}

```js
obj.getProperty(name, interfaceName)
obj.get(name, interfaceName)
```

- `getProperty()`は、[PropertyResult](#propertyresult)を返します。
- `get()`は、プロパティ値だけを返します（`result.value`）。

### setProperty() / set() {#setproperty--set}

```js
obj.setProperty(name, value, interfaceName)
obj.set(name, value, interfaceName)
```

### introspect() {#introspect-1}

```js
obj.introspect()
```

- 戻り値: [IntrospectionNode](#introspectionnode)

### subscribeSignal() / unsubscribeSignal() {#subscribesignal--unsubscribesignal}

```js
obj.subscribeSignal(member, interfaceName)
obj.unsubscribeSignal(member, interfaceName)
```

destination/pathを自動的に渡す便利なラッパーです。

## リクエスト・レスポンスの構造 {#요청응답-구조}

## CallRequest {#callrequest}

| プロパティ | 型 | 説明 |
|:---------|:-----|:-----|
| destination | `string` | サービス名 |
| path | `string` | オブジェクトパス |
| method | `string` | 完全修飾のメソッド名（`Interface.Method`） |
| args | `any[]` | メソッド引数 |
| flags | `number` | D-Bus呼び出しフラグ |

`args`の型指定規則：

- JavaScriptの数値は、呼び出し時に整数型（`uint16`、`int32`など）の区別が曖昧になる場合があります。
- 正確なD-Bus型が必要な場合は、引数を`"type:value"`文字列で渡せます。
- 例： `"uint16:123"`, `"int32:-7"`, `"bool:true"`, `"objectpath:/org/freedesktop/DBus"`

対応する型（`type:value`）：

- `byte`, `uint8`, `uint16`, `uint32`, `uint64`
- `int16`, `int32`, `int64`
- `float32`, `float64`, `double`
- `bool`, `string`
- `objectpath`, `path`
- `signature`

動作に関する注意:

- 型の接頭辞がない文字列は、通常の文字列として渡します。
- 不明な型の接頭辞（例：`"custom:123"`）は変換せず、そのまま文字列として渡します。
- 値の解析が失敗すると、呼び出し時に例外が発生します。

## CallResult {#callresult}

| プロパティ | 型 | 説明 |
|:---------|:-----|:-----|
| destination | `string` | サービス名 |
| path | `string` | オブジェクトパス |
| method | `string` | 呼び出しに使用したメソッド名 |
| body | `any[]` | 戻り値の一覧 |

## PropertyRequest {#propertyrequest}

| プロパティ | 型 | 説明 |
|:---------|:-----|:-----|
| destination | `string` | サービス名 |
| path | `string` | オブジェクトパス |
| interface | `string` | インターフェース名 |
| name | `string` | プロパティ名 |

## PropertyResult {#propertyresult}

| プロパティ | 型 | 説明 |
|:---------|:-----|:-----|
| signature | `string` | D-Busシグネチャ |
| value | `any` | プロパティ値 |

## SetPropertyRequest {#setpropertyrequest}

| プロパティ | 型 | 説明 |
|:---------|:-----|:-----|
| destination | `string` | サービス名 |
| path | `string` | オブジェクトパス |
| interface | `string` | インターフェース名 |
| name | `string` | プロパティ名 |
| value | `any` | 書き込むプロパティ値 |

## IntrospectRequest {#introspectrequest}

| プロパティ | 型 | 説明 |
|:---------|:-----|:-----|
| destination | `string` | サービス名 |
| path | `string` | オブジェクトパス |

## IntrospectionNode {#introspectionnode}

| プロパティ | 型 | 説明 |
|:---------|:-----|:-----|
| name | `string` | ノードのパス・名前 |
| interfaces | `object[]` | インターフェースメタデータの一覧 |
| children | `object[]` | 子ノードの一覧 |

各interfaceには、methods/signals/properties/annotationsが含まれます。

## SignalWatchRequest {#signalwatchrequest}

| プロパティ | 型 | 説明 |
|:---------|:-----|:-----|
| destination | `string` | 省略可能。オブジェクトベースの呼び出しとの対称性を保つフィールド |
| sender | `string` | シグナルのsenderフィルター |
| path | `string` | オブジェクトパスのフィルター |
| interface | `string` | インターフェースのフィルター |
| member | `string` | メンバーのフィルター |

`sender`、`path`、`interface`、`member`のうち、少なくとも1つが必要です。

## NameOwnerResult {#nameownerresult}

| プロパティ | 型 | 説明 |
|:---------|:-----|:-----|
| name | `string` | 要求したバス名 |
| owner | `string` | 一意の名前（`:1.xx`）、または空文字列 |
| hasOwner | `boolean` | 現在所有者が存在するかどうか |

## 使用例 {#사용-예시}

### 1) 基本的なメソッド呼び出し {#1-기본-메서드-호출}

```js {linenos=table,linenostart=1}
const dbus = require("dbus");

const conn = new dbus.Connection();
const obj = conn.object("com.plc.manufacture.Service", "/com/plc/device0");

const temp = obj.call("com.plc.manufacture.Interval.GetTemperature");
console.println("temperature:", temp.body[0]);

conn.close();
```

### 2) プロパティの読み書き {#2-프로퍼티-읽기쓰기}

```js {linenos=table,linenostart=1}
const dbus = require("dbus");

const conn = new dbus.Connection();
const dev = conn.object("com.plc.manufacture.Service", "/com/plc/device0");

console.println("mode:", dev.get("Mode", "com.plc.manufacture.Status"));
dev.set("Mode", "MANUAL", "com.plc.manufacture.Status");
console.println("mode:", dev.get("Mode", "com.plc.manufacture.Status"));

conn.close();
```

### 3) イントロスペクション {#3-인트로스펙션}

```js {linenos=table,linenostart=1}
const dbus = require("dbus");

const conn = new dbus.Connection();
const obj = conn.object("com.plc.manufacture.Service", "/com/plc/device0");
const node = obj.introspect();

for (const iface of node.interfaces) {
    console.println("iface:", iface.name);
}

conn.close();
```

### 4) シグナルの購読 {#4-시그널-구독}

```js {linenos=table,linenostart=1}
const dbus = require("dbus");

const conn = new dbus.Connection();
const obj = conn.object("com.plc.manufacture.Service", "/com/plc/device0");

obj.subscribeSignal("TemperatureChanged", "com.plc.manufacture.Interval");
conn.on("signal", (sig) => {
    if (sig.member !== "TemperatureChanged") {
        return;
    }
    console.println("temperature changed:", sig.body[0]);
});
```

### 5) 名前の監視 {#5-이름-감시}

```js {linenos=table,linenostart=1}
const dbus = require("dbus");

const conn = new dbus.Connection();
const name = "com.example.Worker";

const owner = conn.getNameOwner(name);
console.println("has owner:", owner.hasOwner);

conn.watchName(name);
conn.on("name-owner-changed", (evt) => {
    if (evt.name === name) {
        console.println("owner changed:", evt.oldOwner, "->", evt.newOwner);
    }
});
```

## エラー時の動作に関する注意 {#오류-동작-메모}

- `conn.close()`の後にメソッドを呼び出すと、`connection not initialized`例外が発生します。
- リクエストオブジェクトの必須フィールドが欠けている場合は、例外が発生します。
- 不正なオブジェクトパスは、例外を発生させます。
- `getNameOwner()`は、所有者がない場合に`{ hasOwner: false }`を返します。
- D-Busのランタイムとテストの動作は、Linux専用です。
