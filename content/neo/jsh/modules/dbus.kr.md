---
title: "dbus"
type: docs
weight: 100
---

{{< neo_since ver="8.5.5" />}}

`dbus` 모듈은 JSH 애플리케이션에서 사용할 수 있는 Linux 전용 D-Bus API를 제공합니다.
메서드 호출, 프로퍼티 읽기/쓰기, 인트로스펙션, 시그널 구독, 이름 소유자 감시 기능을 지원합니다.

## 모듈 로드

```js
const dbus = require("dbus");
const conn = new dbus.Connection({ busType: dbus.BusType.Session });
```

런타임 OS가 Linux가 아니면 연결 생성에 실패합니다.

## BusType

- `dbus.BusType.Session`
- `dbus.BusType.System`

## Connection

D-Bus 연결 객체입니다.

<h6>생성</h6>

```js
new dbus.Connection(options)
```

<h6>옵션</h6>

| 옵션 | 타입 | 기본값 | 설명 |
|:-----|:-----|:-------|:-----|
| busType | `string` | `dbus.BusType.Session` | D-Bus 버스 타입 |

<h6>반환값</h6>

- `Connection`

오류 동작:

- `busType`이 유효하지 않으면 예외가 발생합니다.
- 플랫폼이 Linux가 아니면 예외가 발생합니다.

### close()

현재 D-Bus 연결을 닫습니다.

<h6>사용 형식</h6>

```js
conn.close()
```

<h6>반환값</h6>

- `undefined`

이 메서드는 idempotent하게 동작하며 여러 번 호출해도 안전합니다.

### object()

지정한 destination/path에 바인딩된 [ObjectProxy](#objectproxy)를 생성합니다.

<h6>사용 형식</h6>

```js
conn.object(destination, path)
```

<h6>매개변수</h6>

- `destination` (`string`): 서비스 이름 (예: `org.freedesktop.DBus`)
- `path` (`string`): 오브젝트 경로 (예: `/org/freedesktop/DBus`)

<h6>반환값</h6>

- `ObjectProxy`

### call()

D-Bus 메서드를 호출합니다.

<h6>사용 형식</h6>

```js
conn.call(request)
```

<h6>매개변수</h6>

- `request` (`object`): [CallRequest](#callrequest)

<h6>반환값</h6>

- `object`: [CallResult](#callresult)

오류 동작:

- 필수 필드가 없으면 예외가 발생합니다.
- 오브젝트 경로가 유효하지 않으면 예외가 발생합니다.

### getProperty()

D-Bus 프로퍼티를 읽습니다.

<h6>사용 형식</h6>

```js
conn.getProperty(request)
```

<h6>매개변수</h6>

- `request` (`object`): [PropertyRequest](#propertyrequest)

<h6>반환값</h6>

- `object`: [PropertyResult](#propertyresult)

### setProperty()

D-Bus 프로퍼티를 기록합니다.

<h6>사용 형식</h6>

```js
conn.setProperty(request)
```

<h6>매개변수</h6>

- `request` (`object`): [SetPropertyRequest](#setpropertyrequest)

<h6>반환값</h6>

- `undefined`

### introspect()

오브젝트 인트로스펙션 메타데이터를 조회합니다.

<h6>사용 형식</h6>

```js
conn.introspect(request)
```

<h6>매개변수</h6>

- `request` (`object`): [IntrospectRequest](#introspectrequest)

<h6>반환값</h6>

- `object`: [IntrospectionNode](#introspectionnode)

### subscribeSignal()

매칭 조건에 맞는 D-Bus 시그널을 구독합니다.

<h6>사용 형식</h6>

```js
conn.subscribeSignal(request)
```

<h6>매개변수</h6>

- `request` (`object`): [SignalWatchRequest](#signalwatchrequest)

<h6>반환값</h6>

- `Connection` (체이닝 가능)

오류 동작:

- 모든 매칭 필드가 비어 있으면 `missing signal match criteria` 예외가 발생합니다.

### unsubscribeSignal()

기존에 등록한 시그널 구독을 해제합니다.

<h6>사용 형식</h6>

```js
conn.unsubscribeSignal(request)
```

<h6>매개변수</h6>

- `request` (`object`): [SignalWatchRequest](#signalwatchrequest)

<h6>반환값</h6>

- `Connection` (체이닝 가능)

오류 동작:

- 일치하는 구독이 없으면 예외가 발생합니다.

### watchName()

버스 이름의 owner 변경 감시를 시작합니다.

<h6>사용 형식</h6>

```js
conn.watchName(name)
```

<h6>매개변수</h6>

- `name` (`string`): D-Bus well-known name

<h6>반환값</h6>

- `Connection` (체이닝 가능)

### unwatchName()

버스 이름의 owner 변경 감시를 중단합니다.

<h6>사용 형식</h6>

```js
conn.unwatchName(name)
```

<h6>매개변수</h6>

- `name` (`string`): D-Bus well-known name

<h6>반환값</h6>

- `Connection` (체이닝 가능)

오류 동작:

- 활성 감시가 없으면 `name watch not found` 예외가 발생합니다.

### getNameOwner()

버스 이름의 현재 owner를 조회합니다.

<h6>사용 형식</h6>

```js
conn.getNameOwner(name)
```

<h6>매개변수</h6>

- `name` (`string`): D-Bus well-known name

<h6>반환값</h6>

- `object`: [NameOwnerResult](#nameownerresult)

이름에 owner가 없을 때는 예외를 던지지 않고 `hasOwner: false`를 반환합니다.

## 이벤트

`Connection`은 `EventEmitter`를 상속합니다.

### signal

구독된 D-Bus 시그널이 수신될 때마다 발생합니다.

```js
conn.on("signal", (sig) => {
    console.println(sig.interface, sig.member, sig.body);
});
```

### name-owner-changed

감시 중인 이름의 owner가 변경되면 발생합니다.

```js
conn.on("name-owner-changed", (evt) => {
    console.println(evt.name, evt.oldOwner, evt.newOwner);
});
```

## ObjectProxy

`conn.object(destination, path)`로 생성합니다.

### call()

```js
obj.call(method, ...args)
```

- 반환값: [CallResult](#callresult)와 동일한 구조

### getProperty() / get()

```js
obj.getProperty(name, interfaceName)
obj.get(name, interfaceName)
```

- `getProperty()`는 [PropertyResult](#propertyresult)를 반환합니다.
- `get()`은 프로퍼티 값만 반환합니다 (`result.value`).

### setProperty() / set()

```js
obj.setProperty(name, value, interfaceName)
obj.set(name, value, interfaceName)
```

### introspect()

```js
obj.introspect()
```

- 반환값: [IntrospectionNode](#introspectionnode)

### subscribeSignal() / unsubscribeSignal()

```js
obj.subscribeSignal(member, interfaceName)
obj.unsubscribeSignal(member, interfaceName)
```

destination/path는 자동으로 전달되는 편의 래퍼입니다.

## 요청/응답 구조

## CallRequest

| 프로퍼티 | 타입 | 설명 |
|:---------|:-----|:-----|
| destination | `string` | 서비스 이름 |
| path | `string` | 오브젝트 경로 |
| method | `string` | 전체 메서드 이름 (`Interface.Method`) |
| args | `any[]` | 메서드 인자 |
| flags | `number` | D-Bus 호출 플래그 |

## CallResult

| 프로퍼티 | 타입 | 설명 |
|:---------|:-----|:-----|
| destination | `string` | 서비스 이름 |
| path | `string` | 오브젝트 경로 |
| method | `string` | 호출에 사용한 메서드 이름 |
| body | `any[]` | 반환 값 목록 |

## PropertyRequest

| 프로퍼티 | 타입 | 설명 |
|:---------|:-----|:-----|
| destination | `string` | 서비스 이름 |
| path | `string` | 오브젝트 경로 |
| interface | `string` | 인터페이스 이름 |
| name | `string` | 프로퍼티 이름 |

## PropertyResult

| 프로퍼티 | 타입 | 설명 |
|:---------|:-----|:-----|
| signature | `string` | D-Bus 시그니처 |
| value | `any` | 프로퍼티 값 |

## SetPropertyRequest

| 프로퍼티 | 타입 | 설명 |
|:---------|:-----|:-----|
| destination | `string` | 서비스 이름 |
| path | `string` | 오브젝트 경로 |
| interface | `string` | 인터페이스 이름 |
| name | `string` | 프로퍼티 이름 |
| value | `any` | 기록할 프로퍼티 값 |

## IntrospectRequest

| 프로퍼티 | 타입 | 설명 |
|:---------|:-----|:-----|
| destination | `string` | 서비스 이름 |
| path | `string` | 오브젝트 경로 |

## IntrospectionNode

| 프로퍼티 | 타입 | 설명 |
|:---------|:-----|:-----|
| name | `string` | 노드 경로/이름 |
| interfaces | `object[]` | 인터페이스 메타데이터 목록 |
| children | `object[]` | 자식 노드 목록 |

각 interface에는 methods/signals/properties/annotations가 포함됩니다.

## SignalWatchRequest

| 프로퍼티 | 타입 | 설명 |
|:---------|:-----|:-----|
| destination | `string` | 선택값, object 기반 호출과의 대칭성 유지를 위한 필드 |
| sender | `string` | 시그널 sender 필터 |
| path | `string` | 오브젝트 경로 필터 |
| interface | `string` | 인터페이스 필터 |
| member | `string` | 멤버 필터 |

`sender`, `path`, `interface`, `member` 중 최소 하나는 필요합니다.

## NameOwnerResult

| 프로퍼티 | 타입 | 설명 |
|:---------|:-----|:-----|
| name | `string` | 요청한 버스 이름 |
| owner | `string` | 고유 이름(`:1.xx`) 또는 빈 문자열 |
| hasOwner | `boolean` | 현재 owner 존재 여부 |

## 사용 예시

### 1) 기본 메서드 호출

```js {linenos=table,linenostart=1}
const dbus = require("dbus");

const conn = new dbus.Connection();
const obj = conn.object("com.plc.manufacture.Service", "/com/plc/device0");

const temp = obj.call("com.plc.manufacture.Interval.GetTemperature");
console.println("temperature:", temp.body[0]);

conn.close();
```

### 2) 프로퍼티 읽기/쓰기

```js {linenos=table,linenostart=1}
const dbus = require("dbus");

const conn = new dbus.Connection();
const dev = conn.object("com.plc.manufacture.Service", "/com/plc/device0");

console.println("mode:", dev.get("Mode", "com.plc.manufacture.Status"));
dev.set("Mode", "MANUAL", "com.plc.manufacture.Status");
console.println("mode:", dev.get("Mode", "com.plc.manufacture.Status"));

conn.close();
```

### 3) 인트로스펙션

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

### 4) 시그널 구독

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

### 5) 이름 감시

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

## 오류 동작 메모

- `conn.close()` 이후 메서드를 호출하면 `connection not initialized` 예외가 발생합니다.
- 요청 객체의 필수 필드가 누락되면 예외가 발생합니다.
- 유효하지 않은 오브젝트 경로는 예외를 발생시킵니다.
- `getNameOwner()`는 owner가 없을 때 `{ hasOwner: false }`를 반환합니다.
- DBus 런타임 및 테스트 동작은 Linux 전용입니다.
