---
title: "service"
type: docs
weight: 100
---

{{< neo_since ver="8.0.75" />}}

`service` 모듈은 JSH 애플리케이션에서 service controller의 JSON-RPC API를 호출할 수 있도록 해주는 클라이언트 모듈입니다.

일반적으로 아래처럼 사용합니다.

```js
const service = require('service');
```

service controller 주소는 보통 shell/session이 설정한 `SERVICE_CONTROLLER` 환경 변수에서 가져옵니다.

controller는 실행할 때마다 random 주소로 열릴 수 있으므로 일반적으로는 주소를 하드코딩하지 않습니다.
별도의 controller 주소를 이미 알고 있거나 명시적으로 다른 controller에 연결해야 하는 경우에만 `options.controller`를 사용합니다.

## createClient()

service controller와 통신하는 `Client` 인스턴스를 생성합니다.

<h6>사용 형식</h6>

```js
createClient([options])
```

<h6>옵션</h6>

| 옵션       | 타입     | 기본값 | 설명 |
|:-----------|:---------|:-------|:-----|
| controller | String   |        | 명시적으로 사용할 controller 주소. 지정하지 않으면 `SERVICE_CONTROLLER` 환경 변수를 사용합니다. |
| timeout    | Number   | `5000` | RPC 타임아웃(밀리초)입니다. 같은 값이 callback 기반 요청이 완료되거나 timeout 될 때까지 request lifetime을 유지하는 데도 사용됩니다. |

`controller`는 고정된 기본 주소를 갖지 않습니다.
`SERVICE_CONTROLLER`가 없고 `options.controller`도 지정하지 않으면 클라이언트 생성은 실패합니다.

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[2]}
const service = require('service');
const client = service.createClient({ timeout: 1000 });
```

위 예시는 `SERVICE_CONTROLLER` 환경 변수가 이미 설정되어 있다고 가정합니다.

명시적으로 다른 controller 주소를 사용할 때만 아래처럼 `controller`를 지정합니다.

```js {linenos=table,linenostart=1,hl_lines=[3]}
const service = require('service');
const client = service.createClient({
    controller: 'unix:///tmp/example-service-controller.sock',
    timeout: 1000,
});
```

## call()

임의의 service controller RPC 메서드를 직접 호출합니다.

<h6>사용 형식</h6>

```js
call(method[, params][, options], callback)
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[3]}
const service = require('service');

service.call('service.list', null, (err, result) => {
    if (err) {
        console.println(err.message);
        return;
    }
    console.println(result.length);
});
```

## Client

`createClient()`가 반환하는 service controller 클라이언트입니다.

<h6>주요 프로퍼티</h6>

- `controller`
- `timeout`
- `runtime`
- `details`

**Client 메서드**

- `call(method[, params], callback)`
- `list(callback)`
- `get(name, callback)`
- `read(callback)`
- `update(callback)`
- `reload(callback)`
- `install(config, callback)`
- `uninstall(name, callback)`
- `start(name, callback)`
- `stop(name, callback)`

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[4,8]}
const service = require('service');
const client = service.createClient();

client.list((err, services) => {
    if (err) {
        console.println(err.message);
        return;
    }
    console.println('count=', services.length);
});
```

## runtime.get()

서비스의 runtime snapshot을 조회합니다.

- 반환값에는 `output`과 `details`가 포함됩니다.

<h6>사용 형식</h6>

```js
runtime.get(name[, options], callback)
client.runtime.get(name, callback)
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[3,7]}
const service = require('service');

service.runtime.get('alpha', (err, runtime) => {
    if (err) {
        console.println(err.message);
        return;
    }
    console.println(JSON.stringify(runtime.details || {}));
});
```

## details.get()

서비스 detail 값을 조회합니다.

- `key`를 생략하면 전체 `details` snapshot을 반환합니다.
- `key`를 지정하면 해당 key가 없을 때 오류를 반환합니다.

<h6>사용 형식</h6>

```js
details.get(name[, key][, options], callback)
client.details.get(name[, key], callback)
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[3,7]}
const service = require('service');

service.details.get('alpha', 'health', (err, runtime) => {
    if (err) {
        console.println(err.message);
        return;
    }
    console.println(runtime.details.health);
});
```

## details.add()

새 detail key/value를 추가합니다.

- 동일한 key가 이미 존재하면 오류를 반환합니다.

<h6>사용 형식</h6>

```js
details.add(name, key, value[, options], callback)
client.details.add(name, key, value, callback)
```

## details.update()

기존 detail key/value를 갱신합니다.

- key가 존재하지 않으면 오류를 반환합니다.

<h6>사용 형식</h6>

```js
details.update(name, key, value[, options], callback)
client.details.update(name, key, value, callback)
```

## details.set()

detail key/value를 설정합니다.

- key가 없으면 새로 생성하고, 있으면 덮어씁니다.

<h6>사용 형식</h6>

```js
details.set(name, key, value[, options], callback)
client.details.set(name, key, value, callback)
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[3]}
const service = require('service');

service.details.set('alpha', 'health', 'ok', (err, runtime) => {
    if (err) {
        console.println(err.message);
        return;
    }
    console.println(runtime.details.health);
});
```

## details.delete()

detail key를 제거합니다.

- key가 없으면 오류를 반환합니다.

<h6>사용 형식</h6>

```js
details.delete(name, key[, options], callback)
client.details.delete(name, key, callback)
```

## parseController()

controller 주소 문자열을 파싱합니다.

- 지원 형식: `host:port`, `tcp://host:port`, `unix://path`

<h6>사용 형식</h6>

```js
parseController(value)
```

<h6>사용 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[2]}
const service = require('service');
const endpoint = service.parseController('unix:///tmp/example-service-controller.sock');
console.println(endpoint.network, endpoint.path);
```

## resolveController()

controller 주소를 결정합니다.

- 인자를 넘기면 그 값을 사용합니다.
- 인자가 없으면 `SERVICE_CONTROLLER` 환경 변수를 조회합니다.

<h6>사용 형식</h6>

```js
resolveController([value])
```

<h6>동작 예시</h6>

```js {linenos=table,linenostart=1,hl_lines=[2,3]}
const service = require('service');
console.println(service.resolveController());
console.println(service.resolveController('unix:///tmp/example-service-controller.sock'));
```

## 동작 참고

- 모든 API는 callback 기반 비동기 스타일입니다.
- Promise / `await`는 사용하지 않습니다.
- controller 연결 실패, timeout, RPC 오류는 callback의 첫 번째 인자로 전달됩니다.
- service RPC가 진행 중인 동안에는 짧은 top-level script가 callback 전에 종료되지 않도록 module이 내부적으로 request lifetime을 유지합니다.
- 이 keepalive 구간은 실제 `timeout` 값에 맞춰 동작하고, 요청이 성공, 실패, timeout 중 하나로 정리되면 바로 해제됩니다.
- `createClient()`, `call()`, `runtime.get()`, `details.*()`는 `options.controller`를 생략하면 `SERVICE_CONTROLLER`를 기본으로 사용합니다.
- top-level helper(`service.details.get(...)`)는 내부적으로 매 호출마다 client를 생성합니다.
