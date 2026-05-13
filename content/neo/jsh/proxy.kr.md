---
title: 서비스 프록시
type: docs
weight: 120
---

{{< neo_since ver="8.5.2" />}}

JSH 서비스는 자체 HTTP 서버를 실행한 뒤, machbase-neo의 `/web/services/<service_name>/<prefix>/*` 경로로 그 서버를 노출할 수 있습니다.
서비스 개발자는 서비스가 사용할 포트를 외부 클라이언트에 알려 줄 필요 없이, 서비스 시작 시 proxy endpoint를 등록하면 됩니다.
클라이언트는 machbase-neo와 같은 origin으로 접근하므로 별도 포트 탐색과 CORS 설정을 피할 수 있습니다.

## 개요

서비스 프록시는 실행 중인 JSH 서비스가 `SERVICE_CONTROLLER`를 통해 동적으로 등록합니다.
등록된 경로로 들어온 HTTP 요청은 예외 없이 등록된 대상 서버로 reverse proxy 됩니다.

공개 경로 형식은 다음과 같습니다.

```text
/web/services/<service_name>/<prefix>/*
```

예를 들어 서비스 이름이 `github.com/acme/chart`이고 prefix가 `/api/`이면 클라이언트는 다음 주소로 접근합니다.

```text
/web/services/github.com/acme/chart/api/series
```

## 이름 규칙

`service_name`에는 별도 namespace 제한을 두지 않습니다.
동일한 `service_name`과 `prefix` 조합은 먼저 등록한 프로세스가 선점합니다.
나중에 다른 target으로 같은 조합을 등록하려고 하면 충돌 오류가 발생합니다.

패키지로 배포하는 서비스는 서비스 이름 충돌을 피하기 위해 package 이름을 `service_name`으로 사용하는 것을 권장합니다.

```javascript
service: 'github.com/acme/chart'
```

하나의 서비스는 여러 proxy endpoint를 등록할 수 있습니다.

```javascript
service.proxy.register({
    service: 'github.com/acme/chart',
    prefix: '/api/',
    target: 'http://127.0.0.1:18080'
}, callback);

service.proxy.register({
    service: 'github.com/acme/chart',
    prefix: '/assets/',
    target: 'http://127.0.0.1:18081'
}, callback);
```

## Target 제한

proxy target은 machbase-neo 서버가 안전하게 접근할 수 있는 로컬 endpoint로 제한됩니다.

허용되는 target은 다음과 같습니다.

- `http://127.0.0.1:<port>`
- `http://localhost:<port>`
- 기타 loopback IP 주소
- `unix://<absolute_socket_path>`

외부 host와 `https://` target은 기본적으로 허용하지 않습니다.
이 제한은 서비스 프록시가 외부 임의 주소로 동작하는 open proxy가 되는 것을 막기 위한 것입니다.

## 등록

서비스 코드에서는 `service` 모듈의 `proxy.register()`를 사용합니다.

```javascript
const service = require('service');

service.proxy.register({
    service: 'github.com/acme/chart',
    prefix: '/api/',
    target: 'http://127.0.0.1:18080'
}, function(err, entry) {
    if (err) {
        console.println('proxy register failed:', err.message);
        return;
    }
    console.println('proxy registered:', entry.service, entry.prefix);
});
```

등록 항목은 다음 필드를 사용합니다.

| 필드 | 타입 | 설명 |
| --- | --- | --- |
| `service` | `String` | 공개 경로의 서비스 이름 |
| `prefix` | `String` | 서비스 아래의 proxy prefix |
| `target` | `String` | 요청을 전달할 로컬 HTTP 또는 Unix socket endpoint |
| `stripPrefix` | `String` | 선택 사항. target으로 전달하기 전에 제거할 공개 경로 prefix |
| `healthPath` | `String` | 선택 사항. 상태 확인용 경로 metadata |

`stripPrefix`를 지정하지 않으면 기본적으로 `/web/services/<service_name>/<prefix>`가 제거되어 target으로 전달됩니다.
예를 들어 `/web/services/github.com/acme/chart/api/series` 요청은 target 서버에 `/series`로 전달됩니다.

**stripPrefix**

서비스 내부 라우터가 공개 경로 일부를 그대로 기대하는 경우에는 `stripPrefix`를 직접 지정할 수 있습니다.
예를 들어 proxy prefix는 `/api/`로 등록하지만 target 서버가 `/api/series` 경로를 처리하도록 만들고 싶다면, 서비스 base path까지만 제거합니다.

```javascript
service.proxy.register({
    service: 'github.com/acme/chart',
    prefix: '/api/',
    target: 'http://127.0.0.1:18080',
    stripPrefix: '/web/services/github.com/acme/chart'
}, callback);
```

이 설정에서는 다음처럼 경로가 전달됩니다.

| 공개 요청 경로 | target 서버가 받는 경로 |
| --- | --- |
| `/web/services/github.com/acme/chart/api/series` | `/api/series` |
| `/web/services/github.com/acme/chart/api/healthz` | `/api/healthz` |

반대로 `stripPrefix`를 생략하면 기본 제거 prefix가 `/web/services/github.com/acme/chart/api`가 되므로 target 서버는 `/series`, `/healthz`를 받습니다.

## 등록 해제

서비스가 종료될 때는 등록한 proxy endpoint를 해제하는 것을 권장합니다.

특정 prefix만 해제하려면 다음처럼 호출합니다.

```javascript
service.proxy.unregister('github.com/acme/chart', '/api/', function(err) {
    if (err) {
        console.println('proxy unregister failed:', err.message);
    }
});
```

서비스 이름에 속한 모든 endpoint를 해제하려면 prefix를 생략합니다.

```javascript
service.proxy.unregister('github.com/acme/chart', function(err) {
    if (err) {
        console.println('proxy unregister failed:', err.message);
    }
});
```

## 조회

현재 등록 상태는 `proxy.list()`와 `proxy.get()`으로 확인할 수 있습니다.

```javascript
service.proxy.list('github.com/acme/chart', function(err, entries) {
    if (err) {
        console.println(err.message);
        return;
    }
    console.println(JSON.stringify(entries));
});

service.proxy.get('github.com/acme/chart', '/api/', function(err, entry) {
    if (err) {
        console.println(err.message);
        return;
    }
    console.println(JSON.stringify(entry));
});
```

## servicectl 관리 명령

운영 중인 proxy 등록 상태는 `servicectl proxy` 명령으로도 확인하고 관리할 수 있습니다.
명령은 `SERVICE_CONTROLLER`에 연결하므로 `--controller` 옵션이나 `SERVICE_CONTROLLER` 환경 변수를 사용합니다.

```sh
servicectl proxy list
servicectl proxy list github.com/acme/chart
servicectl proxy get github.com/acme/chart /api/
```

테스트나 수동 운영 상황에서는 CLI에서 직접 등록할 수도 있습니다.

```sh
servicectl proxy register github.com/acme/chart /api/ http://127.0.0.1:18080 --health-path /healthz
servicectl proxy unregister github.com/acme/chart /api/
```

`proxy unregister <service_name>`처럼 prefix를 생략하면 해당 서비스 이름으로 등록된 모든 proxy endpoint를 제거합니다.
일반 서비스 코드에서는 시작 시 `service.proxy.register()`를 호출하고 종료 시 `service.proxy.unregister()`를 호출하는 방식을 권장하며, `servicectl proxy`는 운영 확인과 디버깅용으로 사용합니다.

## TCP 예시

다음 예시는 서비스가 로컬 HTTP 서버를 시작하고 `/web/services/github.com/acme/chart/api/*` 경로로 등록하는 흐름을 보여 줍니다.

```javascript
const http = require('http');
const service = require('service');

const serviceName = 'github.com/acme/chart';
const port = 18080;

const server = new http.Server({ network: 'tcp', address: '127.0.0.1:' + port });

server.get('/healthz', function(ctx) {
    ctx.text(http.status.OK, 'ok');
});

server.get('/*path', function(ctx) {
    ctx.json(http.status.OK, { path: ctx.request.path });
});

server.serve(function() {
    service.proxy.register({
        service: serviceName,
        prefix: '/api/',
        target: 'http://127.0.0.1:' + port,
        healthPath: '/healthz'
    }, function(err) {
        if (err) {
            console.println('proxy register failed:', err.message);
            return;
        }
        console.println('proxy ready:', '/web/services/' + serviceName + '/api/');
    });
});

process.on('exit', function() {
    server.close();
    service.proxy.unregister(serviceName, '/api/', function() {});
});
```

## Unix domain socket 예시

JSH `http.Server`는 `network: 'unix'` 설정을 지원합니다.
서비스 전용 HTTP 서버를 TCP 포트 대신 Unix domain socket에 바인딩하면 외부 포트를 열지 않고 service proxy와 연결할 수 있습니다.
`target`에는 `unix://` 뒤에 절대 socket 경로를 지정합니다.

```javascript
const http = require('http');
const service = require('service');

const serviceName = 'github.com/acme/chart';
const socketPath = '/tmp/acme-chart.sock';

const server = new http.Server({ network: 'unix', address: socketPath });

server.get('/healthz', function(ctx) {
    ctx.text(http.status.OK, 'ok');
});

server.get('/*path', function(ctx) {
    ctx.json(http.status.OK, { path: ctx.request.path });
});

server.serve(function() {
    service.proxy.register({
        service: serviceName,
        prefix: '/api/',
        target: 'unix://' + socketPath,
        healthPath: '/healthz'
    }, function(err) {
        if (err) {
            console.println('proxy register failed:', err.message);
            server.close();
            return;
        }
        console.println('proxy ready:', '/web/services/' + serviceName + '/api/');
    });
});

process.on('exit', function() {
    server.close();
    service.proxy.unregister(serviceName, '/api/', function() {});
});
```

예를 들어 `/web/services/github.com/acme/chart/api/series` 요청은 Unix socket으로 연결된 서비스 서버의 `/series` 경로로 전달됩니다.
socket 경로는 절대 경로여야 하며, 운영 환경에서는 서비스별로 충돌하지 않는 경로를 사용해야 합니다.

## 주의 사항

- 등록 정보는 runtime 상태입니다. 서비스가 재시작되면 다시 등록해야 합니다.
- 같은 `service_name`과 `prefix` 조합은 먼저 등록한 프로세스가 선점합니다.
- 등록되지 않은 `/web/services/<service_name>/<prefix>/*` 요청은 다른 package 처리로 fallback하지 않습니다.
- 서비스는 외부 공개 포트 대신 loopback 또는 Unix domain socket을 사용하는 것을 권장합니다.
