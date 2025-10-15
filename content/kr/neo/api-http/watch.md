---
title: 최신 데이터 모니터링
type: docs
weight: 21
---

## Server-Sent Events 활용

클라이언트는 서버에서 전송하는 스트리밍 이벤트를 받아 지정한 테이블의 최신 레코드를 실시간으로 조회할 수 있습니다.

Server-Sent Events(SSE)는 하나의 HTTP 연결을 유지한 채 서버가 클라이언트로 업데이트를 지속적으로 푸시하는 기술입니다.
라이브 피드, 알림, 실시간 분석처럼 지속적인 데이터 갱신이 필요한 애플리케이션에서 널리 사용됩니다.

**Server-Sent Events(SSE)의 특징**

1. **단방향 통신**: 서버는 클라이언트로 업데이트를 보낼 수 있지만, 동일한 연결에서는 클라이언트가 서버로 데이터를 보낼 수 없습니다.
2. **지속 연결**: 클라이언트는 하나의 HTTP 연결을 열어 두고, 서버는 새로운 데이터가 생길 때마다 업데이트를 전송합니다.
3. **자동 재연결**: 연결이 끊어지면 클라이언트가 자동으로 재연결을 시도합니다.
4. **간단한 API**: SSE는 웹 애플리케이션에서 구현하기 쉬운 단순한 API를 제공합니다.

**SSE 동작 방식**
1. **클라이언트 요청**: 클라이언트가 서버에 HTTP 요청을 보내 업데이트 수신을 시작합니다.
2. **서버 전송**: 서버는 `text/event-stream` MIME 타입으로 포맷된 업데이트 스트림을 전송합니다.
3. **클라이언트 처리**: 클라이언트는 수신 즉시 데이터를 처리하며, 보통 사용자 인터페이스를 실시간으로 갱신합니다.

웹 브라우저는 단일 호스트에 대해 동시에 열 수 있는 SSE 연결 수에 제한을 둡니다. 이는 자원 고갈을 방지하고 네트워크 자원을 효율적으로 사용하기 위함입니다. 주요 사항은 다음과 같습니다.

**브라우저의 SSE 연결 제한**

1. **연결 수 제한**: 대부분의 최신 브라우저는 단일 호스트당 SSE 연결을 최대 6개 정도로 제한합니다.
2. **자원 관리**: 연결 수를 제한하면 메모리와 네트워크 대역폭 같은 자원을 관리할 수 있어 단일 페이지가 브라우저나 서버를 과도하게 사용하지 못하도록 합니다.
3. **공정한 사용**: 이러한 제한 덕분에 여러 탭이나 애플리케이션이 네트워크 자원을 공평하게 사용할 수 있으며, 특정 애플리케이션이 연결을 독점하지 못합니다.

이러한 제한을 이해하고 준수해야 견고하고 효율적인 실시간 웹 애플리케이션을 구현할 수 있습니다. 연결 제한을 고려하여 설계하면 사용자 경험과 자원 활용 모두에서 좋은 결과를 얻을 수 있습니다.


## 최신 데이터 감시

{{< neo_since ver="8.0.35" />}}

SSE(Server-Sent Events) 엔드포인트는 다음과 같습니다.

```
/db/watch/{table}
```

*watch* API가 지원하는 쿼리 매개변수는 다음과 같습니다.

| param       | default | description                                                                    |
|:----------- |---------|:-------------------------------------------------------------------------------|
| timeformat  | `ns`     | 출력 시간 단위: s, ms, us, ns                                                  |
| tz          | `UTC`    | 출력 시간대: UTC, Local, 지역 지정                                             |
| period      | `3s`     | 갱신 주기                                                                      |
| keep-alive  | `30s`    | 연결을 유지하고 TCP 타임아웃을 방지하기 위해 서버가 주석 메시지를 보내는 간격 |


**태그 테이블**

대상 테이블이 태그 테이블이라면 `tag` 매개변수를 반드시 지정해야 합니다.

| param       | default | description                                                                 |
|:----------- |---------|:----------------------------------------------------------------------------|
| **tag**     |         | 태그 이름 배열                                                              |
| parallelism | `0`     | 병렬 처리 개수를 지정합니다.<br/>0 또는 태그 수보다 큰 값을 지정하면 태그 개수를 따릅니다. |

{{< callout emoji="📌" >}}
이 API는 지정한 *period* 동안 각 태그의 최신 데이터만 전달합니다.<br/>
해당 기간에 여러 값이 입력되더라도 가장 최근 값만 전송됩니다.
{{< /callout >}}


**로그 테이블**

| param       | default | description                                                                                         |
|:----------- |---------|:----------------------------------------------------------------------------------------------------|
| max-rows    | `20`   | 주기마다 서버가 전송하는 최대 레코드 수입니다.<br/>지정한 수보다 많은 레코드가 있으면 초과분은 해당 주기에서 생략됩니다.<br/>최대 한계는 100입니다. |

## cURL 예시

`curl` 명령으로 태그의 최신 값을 스트림 형태로 받아보십시오.

```sh
curl -o - -v "http://127.0.0.1:5654/db/watch/example"\
"?tag=neo_load1&tag=neo_load5&period=3s&timeformat=s"
```

클라이언트가 연결을 유지하는 동안 서버는 지속적으로 데이터를 전송합니다.

```sh
data: {"NAME":"neo_load1","TIME":1729070964,"VALUE":1.87}

data: {"NAME":"neo_load5","TIME":1729070964,"VALUE":1.37}

data: {"NAME":"neo_load1","TIME":1729070969,"VALUE":1.8}

data: {"NAME":"neo_load5","TIME":1729070969,"VALUE":1.36}

^C
```

## 자바스크립트 예시

```html
<html>
<body>
    <h1>Server-Sent Events 예시</h1>
    <div id="messages"></div>
    <script>
        // EventSource 인스턴스를 생성합니다.
        const addr = 'http://127.0.0.1:5654/db/watch/EXAMPLE';
        const params = 'tag=neo_load1&tag=neo_load5&period=3s&keep-alive=30s&timeformat=default';
        const eventSource = new EventSource(`${addr}?${params}`);

        // 메시지를 표시할 div를 가져옵니다.
        const messagesDiv = document.getElementById('messages');

        // 수신한 메시지를 처리합니다.
        eventSource.onmessage = function (event) {
            // 새 요소를 만듭니다.
            const pre = document.createElement('pre');
            const msg = JSON.parse(event.data);
            // 이벤트 데이터를 텍스트로 설정합니다.
            pre.textContent = event.data + ' => ' + msg.NAME + ':' + msg.VALUE;
            // 요소를 메시지 div에 추가합니다.
            messagesDiv.appendChild(pre);
        };

        // 오류를 처리합니다.
        eventSource.onerror = function (event) {
            console.error('EventSource failed:', event);
        };
    </script>
</body>
</html>
```

## 파이썬 예시

```python
import requests
import sseclient

# 서버 전송 이벤트 엔드포인트에 연결할 URL을 정의합니다.
url = 'http://127.0.0.1:5654/db/watch/EXAMPLE'
params = {
    'tag': ['neo_load1', 'neo_load5'],
    'period': '3s',
    'keep-alive': '30s',
    'timeformat': 'default'
}

# 스트리밍 요청을 생성합니다.
response = requests.get(url, params=params, stream=True)

# sseclient를 사용해 서버 전송 이벤트를 처리합니다.
client = sseclient.SSEClient(response)

# 수신한 메시지를 출력합니다.
for event in client.events():
    print(event.data)
```
