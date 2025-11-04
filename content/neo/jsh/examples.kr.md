---
title: 예제
type: docs
weight: 1
---

## HTTP 서버

이 예제는 `@jsh/http` 모듈을 사용하여 간단한 HTTP 서버를 구현하는 방법을 안내해 드립니다.
서버는 지정한 주소와 포트(`127.0.0.1:56802`)에서 요청을 수신하며 `/hello/:name` REST API 엔드포인트를 제공합니다.
클라이언트가 이름 매개변수를 포함한 GET 요청을 보내면,
서버는 인사 메시지와 전달받은 이름이 들어 있는 JSON 객체로 응답합니다.

동적 라우팅과 JSON 응답을 활용한 경량 HTTP 서버 작성 방법을 익히기에 적합한 예제입니다.

<h6>주요 특징</h6>

1. **데몬 처리**: 스크립트는 `process.ppid()`로 데몬 실행 여부를 확인하고, 아닐 경우 `process.daemonize()`를 호출해 백그라운드에서 동작하도록 전환합니다.
2. **라우팅**: `/hello/:name` 라우트에서 URL 경로에 포함된 `name` 값을 추출합니다.
3. **JSON 응답**: 이름과 환영 메시지를 담은 JSON 객체를 반환합니다.

```js {linenos=table,linenostart=1}
const process = require("@jsh/process");
const {println} = require("@jsh/process");
const http = require("@jsh/http")

// 서버를 백그라운드 프로세스로 실행하도록 보장합니다.
if( process.isDaemon() ) { // equiv. if( process.ppid() == 1)
    runServer();
} else {
    process.daemonize({reload:true});
}

function runServer() {
    // 지정한 주소와 포트에 바인딩된 HTTP 서버를 생성합니다.
    const svr = new http.Server({
        network:'tcp',
        address:'127.0.0.1:56802',
    })
    // 라우트 처리
    svr.get("/hello/:name", ctx => {
        let name = ctx.param("name")
        // URL에서 `name` 매개변수를 꺼내 JSON 객체로 응답합니다.
        ctx.JSON(http.status.OK, {
            "name": name,
            "message": "greetings",
        })
    })

    // 서버를 시작하고 수신 주소를 로그로 기록합니다.
    svr.serve( evt => { 
        println("server started", "http://"+evt.address) ;
    });
}
```

<h6>사용 절차</h6>

1. 스크립트를 실행하여 서버를 기동합니다.
2. `curl`과 같은 도구로 서버에 GET 요청을 보냅니다.

```sh
curl -o - http://127.0.0.1:56802/hello/Karl
```

서버는 다음과 같이 응답합니다.

```json
{"message":"greetings","name":"Karl"}
```

### 유닉스 도메인 소켓

이 예제는 TCP/IP 대신 유닉스 도메인 소켓을 이용해 통신하는 HTTP 서버 구현 방법을 보여 드립니다.
같은 호스트에서 프로세스 간 통신(IPC)이 필요할 때 네트워크 오버헤드 없이 활용하실 수 있습니다.

**동작 흐름**

1. *유닉스 도메인 소켓* 통신  
    - 로컬 통신을 위해 파일 기반 소켓(`/tmp/service.sock`)을 사용합니다.
2. 효율적인 IPC  
    - 동일한 서버의 프로세스 간 통신을 네트워크 없이 처리할 수 있습니다.
3. 도구 호환성  
    - `curl`과 같은 도구로 테스트 및 상호 작용이 가능합니다.

```js {linenos=table,linenostart=1,hl_lines=[4,5]}
const http = require("@jsh/http");

const svr = new http.Server({
    network: "unix",
    address: "/tmp/service.sock",
});
svr.get("/hello/:name", (ctx) => {
    const name = ctx.param("name");
    ctx.JSON(http.status.OK, { message: `Hello, ${name}!` });
});
svr.serve();
```

유닉스 도메인 소켓을 통해 서버에 요청하려면 다음과 같이 입력하십시오.

```sh
curl -o - --unix-socket /tmp/service.sock http://localhost/hello/Karl
```

### 정적 콘텐츠

정적 파일이나 디렉터리를 제공하려면 아래와 같이 설정하십시오.

```js {linenos=table,linenostart=1}
svr.staticFile("/readme", "/path/to/file.txt");
svr.static("/static", "/path/to/static_dir");
```

### 리다이렉트

특정 경로로 이동시키고자 할 때는 다음과 같이 리다이렉션을 지정합니다.

```js {linenos=table,linenostart=1}
svr.get("/readme", ctx => {
    ctx.redirect(http.status.Found, "/docs/readme.html");
});
```

### RESTful API

아래 예제는 목록 조회, 등록, 삭제 요청을 처리하는 기본 REST API 구현입니다.

```js {linenos=table,linenostart=1}
svr.get("/movies", ctx => {
    list = [
        {title:"Indiana Jones", id: 59793, studio: ["Paramount"]},
        {title:"Star Wars", id: 64821, studio: ["Lucasfilm"]},
    ]
    ctx.JSON(http.status.OK, list);
})
svr.post("/movies", ctx => {
    obj = ctx.request.body;
    console.log("post:", JSON.stringify(obj));
    ctx.JSON(http.status.Created, {success: true});
});
svr.delete("/movies/:id", ctx => {
    let id = ctx.param("id");
    console.log("delete:", id)
    ctx.TEXT(http.status.NoContent, "Deleted.")
})
```

다음 명령으로 각 호출을 확인하실 수 있습니다.

- GET 요청
```sh
curl -o - http://127.0.0.1:56802/movies
```
```json
[
  { "id": 59793, "studio": [ "Paramount" ], "title": "Indiana Jones" },
  { "id": 64821, "studio": [ "Lucasfilm" ], "title": "Star Wars" }
]
```

- POST 요청

```sh
curl -o - -X POST http://127.0.0.1:56802/movies \
    -H "Content-Type: application/json" \
    -d '{"title":"new movie", "id":12345, "studio":["Unknown"]}'
```

- DELETE 요청

```sh
curl -v -o - -X DELETE http://127.0.0.1:56802/movies/12345
```

```sh
< HTTP/1.1 204 No Content
< Content-Type: text/plain; charset=utf-8
< Date: Thu, 08 May 2025 20:39:34 GMT
<
```

### HTML 템플릿

다음 설정은 `/*.html` 패턴과 일치하는 모든 HTML 템플릿을 로드합니다.
템플릿을 사용하면 미리 정의된 레이아웃과 실행 시간 데이터를 조합해 동적으로 HTML 응답을 생성하실 수 있습니다.

```js
svr.loadHTMLGlob("/*.html")

// /movielist 라우트를 정의하여 HTML 페이지를 제공합니다.
svr.get("/movielist", ctx => {
    obj = {
        subject: "Movie List",
        list: [
            {title:"Indiana Jones", id: 59793, studio: ["Paramount"]},
            {title:"Star Wars", id: 64821, studio: ["Lucasfilm"]},
        ]
    }
    ctx.HTML(http.status.OK, "movie_list.html", obj)
})
```

- HTML 템플릿 코드 `movie_list.html`

```html
<html>
    <body>
        <h1>{{.subject}}</h1>
        <ol>
        {{range .list }}
            <li> {{.id}} {{.title}} {{.studio}}
        {{end}}
        </ol>
    </body>
</html>
```

`/movielist` 엔드포인트에 GET 요청을 보내면,
서버는 `movie_list.html` 템플릿과 `obj` 데이터를 이용해 HTML 페이지를 생성합니다.

```sh
curl -o - http://127.0.0.1:56802/movielist
```

```html
<html>
    <body>
        <h1>Movie List</h1>
        <ol>
            <li> 59793 Indiana Jones [Paramount]
            <li> 64821 Star Wars [Lucasfilm]
        </ol>
    </body>
</html>
```

## HTTP 클라이언트

이 예제는 `@jsh/http` 모듈을 사용해 HTTP 클라이언트를 구성하는 방법을 보여 드립니다.
클라이언트는 지정한 URL로 GET 요청을 전송하고 서버 응답을 처리합니다.
JavaScript에서 HTTP 요청을 다루고 JSON 응답을 파싱하는 과정을 익히시기에 적합합니다.

<h6>주요 특징</h6>

1. **요청 처리**: 서버로 HTTP GET 요청을 전송합니다.
2. **응답 파싱**: 응답에서 상태, 헤더, 본문을 추출합니다.
3. **오류 처리**: `try-catch` 블록으로 요청 중 발생할 수 있는 오류를 다룹니다.

```js {linenos=table,linenostart=1}
const {println} = require("@jsh/process");
const http = require("@jsh/http")
try {
    // 지정한 URL로 GET 요청을 생성합니다.
    req = http.request("http://127.0.0.1:56802/hello/Steve")
    // URL, 상태, 헤더를 로그로 출력합니다.
    // 응답 본문을 JSON으로 파싱하고 message, name 필드를 출력합니다.
    req.do((rsp) => {
        // url: http://127.0.0.1:56802/hello/Steve
        println("url:", rsp.url);
        // error: <nil>
        println("error:", rsp.error());
        // status: 200
        println("status:", rsp.status);
        // statusText: 200 OK
        println("statusText:", rsp.statusText);
        // content-type: application/json; charset=utf-8
        println("content-type:", rsp.headers["Content-Type"]);
        obj = rsp.json(); // 본문을 JSON 객체로 변환합니다.
        // greetings, Steve
        println("body:", `${obj.message}, ${obj.name}`);
    })
} catch (e) {
    // 요청 과정에서 발생한 오류를 출력합니다.
    println(e);
}
```

<h6>사용 절차</h6>

1. HTTP 서버 예제와 같이 서버가 실행 중인지 확인하십시오.
2. 스크립트를 실행하여 서버에 GET 요청을 전송합니다.

### 유닉스 도메인 소켓

유닉스 도메인 소켓으로 연결하려면 `{unix: "/path/to/unix_domain_socket/file"}` 옵션을 사용하십시오.

```js {linenos=table,linenostart=1}
const {println} = require("@jsh/process");
const http = require("@jsh/http")
try {
    req = http.request("http://localhost/movies", {unix:"/tmp/test.sock"})
    req.do((rsp) => {
        obj = rsp.json();
        println(JSON.stringify(obj))
    })
} catch (e) {
    println(e.toString());
}
```

## MQTT 퍼블리셔

다음 코드는 MQTT 브로커에 주기적으로 메시지를 게시하는 예제입니다.
- `mqtt.js` 파일을 생성하고 아래 코드를 저장하십시오.

```js {linenos=table,linenostart=1}
const mqtt = require("@jsh/mqtt");
const process = require("@jsh/process");
const system = require("@jsh/system")

const log = new system.Log("mqtt-demo");
const testTopic = "test/string";

var client = new mqtt.Client({
    serverUrls: ["tcp://127.0.0.1:5653"],
});

try {
    client.onConnectError = err => { log.error("connect error", err); }
    client.onClientError = err => { log.error("client error", err); }
    client.onConnect = (ack) => { log.info("client connected"); }

    client.connect({timeout: 3*1000});
    
    for(i = 0; i < 10; i++) {
        process.sleep(1000);
        r = client.publish({topic: testTopic, qos: 1}, 'Hello World:'+i)
    }
} catch (e) {
    log.error("Error:", e.message);
} finally {
    client.disconnect({waitForEmptyQueue:true})
}
```

## MQTT 구독자

이 예제는 MQTT 브로커에 연결하여 특정 토픽을 구독하고 수신 메시지를 처리하는 백그라운드 애플리케이션을 구현하는 방법을 보여 드립니다.
`@jsh/process`와 `@jsh/mqtt` 모듈을 이용해 데몬 형태로 실행되며, 연결 수립·메시지 수신·연결 종료와 같은 이벤트를 안정적으로 처리합니다.
실시간 메시지 처리나 경량 백그라운드 작업이 필요한 경우에 활용하시기 좋은 패턴입니다.

- `mqtt-sub.js` 파일을 생성하고 아래 코드를 저장하십시오.

```js {linenos=table,linenostart=1}
// 이 스크립트는 MQTT 브로커에 접속해 토픽(test/topic)을 구독하고
// 수신 메시지를 처리하는 백그라운드 구독자를 생성합니다.
// 연결 이벤트, 오류, 메시지 수신을 JavaScript로 다루는 방법을 보여 드립니다.
//
// @jsh/process 모듈은 데몬화와 출력 등 프로세스 관리 유틸리티를 제공합니다.
const process = require("@jsh/process");
const system = require("@jsh/system")
const log = new system.Log("mqtt-demo");
// @jsh/mqtt 모듈은 브로커 연결과 메시지 처리를 위한 클라이언트를 제공합니다.
const mqtt = require("@jsh/mqtt");

// 부모 프로세스 ID를 확인해 데몬으로 실행 중인지 판단합니다.
if( process.isDaemon() ) {  // equiv. if( process.ppid() == 1)
    // 데몬으로 실행 중이라면 runBackground()를 호출해 구독 로직을 수행합니다.
    log.info("mqtt-sub start...");
    runBackground();
    log.info("mqtt-sub terminated.");
} else {
    // 데몬이 아니라면 process.daemonize()로 백그라운드 프로세스로 전환합니다.
    process.daemonize();
}

// MQTT 구독 로직을 담당하는 메인 함수를 정의합니다.
function runBackground() {
    var client = new mqtt.Client({
        serverUrls: ["tcp://127.0.0.1:5653"],
    });
    try {
        // 접속 중 오류가 발생하면 호출됩니다.
        client.onConnectError = err => { log.warn("connect error", err); }
        // 브로커와의 연결이 끊기면 호출됩니다.
        client.onDisconnect = () => { log.info("disconnected."); }
        var count = 0;
        client.onConnect = ack => {
            log.info("connected.", ack.reasonCode);
            // QoS 2로 test/topic을 구독합니다.
            r = client.subscribe({subscriptions:[{topic:'test/topic', qos: 2}]})
            log.info("subscribe", 'test/topic', "result", r);
            client.onMessage = msg => {
                // 메시지를 수신하면 토픽, QoS, 페이로드를 기록합니다.
                log.info("recv topic:", msg.topic,"payload:", msg.payload.string())
                count++;
                return true;
            }
        }

        // MQTT 브로커에 연결을 시도합니다.
        client.connect({timeout: 3*1000});

        // 토픽에 테스트 메시지를 게시합니다.
        for( let i = 0; i < 10; i++) {
            client.publish({topic:'test/topic', qos: 1}, "test num="+i);
        }
        // 모든 메시지를 받을 때까지 대기합니다.
        while(true) {
            if(count >= 10) break;
            process.sleep(100);
        }
        // 구독 해제
        client.unsubscribe({topics:['test/topic']})
        // 연결 종료
        client.disconnect({waitForEmptyQueue:true})
    } catch (e) {
        log.error("Error", e.message);
    }
}
```

<!-- - JSH에서 `mqtt-sub.js`를 실행하십시오.

```
jsh / > mqtt-sub
jsh / > ps
┌──────┬──────┬──────┬───────────────────┬────────┐ 
│  PID │ PPID │ USER │ NAME              │ UPTIME │ 
├──────┼──────┼──────┼───────────────────┼────────┤ 
│ 1025 │ -    │ sys  │ jsh               │ 4m8s   │ 
│ 1037 │ 1    │ sys  │ /sbin/mqtt-sub.js │ 1s     │ 
│ 1038 │ 1025 │ sys  │ ps                │ 0s     │ 
└──────┴──────┴──────┴───────────────────┴────────┘ 
```

- `mosquitto_pub` 등 MQTT 클라이언트로 메시지를 전송하십시오.

```sh
mosquitto_pub -h 127.0.0.1 -p 5653 -t test/topic -m 'hello?'
```

`mqtt-sub.js` 애플리케이션이 구독을 통해 게시된 메시지를 수신합니다.

```
2025/05/02 09:56:18.381 INFO  /sbin/mqtt-sub.js mqtt-sub start...
2025/05/02 09:56:18.382 INFO  /sbin/mqtt-sub.js connected.
2025/05/02 09:56:18.383 INFO  /sbin/mqtt-sub.js subscribe to test/topic
2025/05/02 09:56:26.149 INFO  /sbin/mqtt-sub.js recv topic: test/topic QoS: 0 payload: hello?
```

- `kill <pid>` 명령으로 백그라운드 프로세스 `mqtt-sub.js`를 종료할 수 있습니다.

```
jsh / > kill 1037
jsh / > ps
┌──────┬──────┬──────┬──────┬────────┐ 
│  PID │ PPID │ USER │ NAME │ UPTIME │ 
├──────┼──────┼──────┼──────┼────────┤ 
│ 1025 │ -    │ sys  │ jsh  │ 16m50s │ 
│ 1041 │ 1025 │ sys  │ ps   │ 0s     │ 
└──────┴──────┴──────┴──────┴────────┘ 
``` -->

## Machbase 클라이언트

이 예제는 포트 5656을 통해 다른 Machbase 인스턴스에 접속하고 쿼리를 실행하는 방법을 보여 드립니다.

8행의 `lowerCaseColumns: true` 설정을 사용하면 21행에서처럼 결과 레코드의 속성명이 소문자로 정규화됩니다.

`dataSource`는 아래 두 가지 형식을 모두 지원합니다.

1. 클래식 형식: `SERVER=${host};PORT_NO=${port};UID=${user};PWD=${pass}`
2. 이름=값 형식: `host=<ip> port=<port> user=<username> password=<pass>`


```js {linenos=table,linenostart=1,hl_lines=[8,21]}
db = require("@jsh/db");
host = "192.168.0.207"
port = 5656
user = "sys"
pass = "manager"
client = db.Client({
    driver: "machbase",
    dataSource: `host=${host} port=${port} user=${user} password=${pass}`,
    lowerCaseColumns: true
})

try {
    sqlText = "select * from example where name = ? limit ?,?";
    tag = "my-car";
    off = 10;
    limit = 5;

    conn = client.connect()
    rows = conn.query(sqlText, tag, off, limit)
    for( rec of rows) {
        console.log(rec.name, rec.time, rec.value)
    }
} catch(e) {
    console.error(e.message)
} finally {
    rows.close()
    conn.close()
}
```

## Machbase Append

아래 코드는 Machbase 테이블에 일괄 데이터를 추가하는 방법을 보여 드립니다.

```js {linenos=table,linenostart=1,hl_lines=[10,16]}
const db = require("@jsh/db");
const { now, parseTime } = require("@jsh/system");

client = new db.Client({lowerCaseColumns:true});
var conn = null;
var appender = null;
try{
    console.log("supportAppend:", client.supportAppend);
    conn = client.connect();
    appender = conn.appender("example", "name", "time", "value");
    let ts = (new Date()).getTime(); // 유닉스 에포크(ms)
    for (let i = 0; i < 100; i++) {
        // 10밀리초씩 증가시킵니다.
        ts = ts + 10;
        // name, time, value 순으로 입력합니다.
        appender.append("tag-append", parseTime(ts, "ms"), i);
    }
} catch(e) {
    console.log("Error:", e);
} finally {
    if (appender) appender.close();
    if (conn) conn.close();
}
console.log("append:", appender.result());

// 예시 출력
// supportAppend: true
// append: {success:100, fail:0}
```

## SQLite 클라이언트

이 예제는 `@jsh/db` 모듈로 메모리 기반 SQLite 데이터베이스를 생성하고, 테이블 생성·데이터 삽입·조회 작업을 수행하는 방법을 보여 드립니다.

```js {linenos=table,linenostart=1,hl_lines=[6]}
const db = require("@jsh/db");

client = new db.Client({
    driver:"sqlite",
    dataSource:"file::memory:?cache=shared"
});

try{
    conn = client.connect()
    // mem_example 테이블을 생성합니다.
    conn.exec(`
        CREATE TABLE IF NOT EXISTS mem_example(
            id         INTEGER NOT NULL PRIMARY KEY,
            company    TEXT,
            employee   INTEGER
        )
    `);

    conn.exec(`INSERT INTO mem_example(company, employee) values(?, ?);`, 
        'Fedel-Gaylord', 12);

    rows = conn.query(`select * from mem_example`);
    for( rec of rows ) {
        console.log(...rec)
    }
}catch(e){
    console.error(e.message);
}finally{
    rows.close();
    conn.close();
}
```

실행하면 삽입된 레코드가 다음과 같이 출력됩니다.
```plaintext
1 Fedel-Gaylord 12
```

## PostgreSQL 클라이언트

PostgreSQL 서버에 연결해 테이블을 생성하고 데이터를 삽입·조회하는 예제입니다.

```js {linenos=table,linenostart=1,hl_lines=[]}
const db = require("@jsh/db");
const { now, parseTime } = require("@jsh/system");

client = new db.Client({
    driver: "postgres",
    dataSource: "host=127.0.0.1 port=15455 dbname=db user=dbuser password=dbpass sslmode=disable",
    lowerCaseColumns:true,
});
var conn = null;
var rows = null;
try{
    conn = client.connect();
    r = conn.exec("CREATE TABLE test (id SERIAL PRIMARY KEY, name TEXT)");
    console.log("create table:", r.message);
    // create table: Created successfully.

    r = conn.exec("INSERT INTO test (name) VALUES ($1)", "foo")
    console.log("insert foo:", r.message, r.rowsAffected);
    // insert foo: a row inserted. 1

    r = conn.exec("INSERT INTO test (name) VALUES ($1)", "bar")
    console.log("insert bar:", r.message, r.rowsAffected);
    // insert bar: a row inserted. 1

    rows = conn.query("SELECT * FROM test ORDER BY id");
    console.log("cols.names:", JSON.stringify(rows.columnNames()));
    // cols.names: ["id","name"]

    for (const rec of rows) {
        console.log(...rec);
    }
    // 1 foo
    // 2 bar
} catch(e) {
    console.log("Error:", e.message);
} finally {
    if(rows) rows.close();
    if(conn) conn.close();
}
```

## System Monitoring

### 데이터 수집기

이 시스템 모니터링 예제는 `@jsh/process`와 `@jsh/psutil` 모듈을 활용해 경량 모니터링 도구를 구성하는 방법을 보여 드립니다.
스크립트는 데몬으로 실행되며 1, 5, 15분 평균 부하와 CPU·메모리 사용률을 주기적으로 수집합니다.

크론과 유사한 구문을 사용해 15초마다 작업을 실행하고, 수집한 데이터를 타임스탬프와 함께 저장합니다.
JavaScript로 프로세스를 관리하고 실시간 지표를 적재하는 예시로 참고하실 수 있습니다.

코드를 `sysmon.js`로 저장한 뒤 JSH 터미널에서 실행하십시오.
시스템 부하와 CPU·메모리 지표는 `EXAMPLE` 테이블에 기록됩니다.

```sh
jsh / > sysmon
jsh / > ps
┌──────┬──────┬──────┬─────────────────┬──────────┐ 
│  PID │ PPID │ USER │ NAME            │ UPTIME   │ 
├──────┼──────┼──────┼─────────────────┼──────────┤ 
│ 1040 │ 1    │ sys  │ /sysmon.js      │ 2h37m43s │ 
│ 1042 │ 1025 │ sys  │ ps              │ 0s       │ 
└──────┴──────┴──────┴─────────────────┴──────────┘ 
```

- sysmon.js

```js {linenos=table,linenostart=1}
const process = require("@jsh/process");
const psutil = require("@jsh/psutil");
const db = require("@jsh/db");
const system = require("@jsh/system");

const tableName = "EXAMPLE";
const tagPrefix = "sys_";

// PID를 확인해 데몬으로 실행 중인지 판단합니다.
if( process.isDaemon() ) {
    // 데몬이라면 바로 모니터링을 시작합니다.
    runSysmon();
} else {
    // 아니라면 백그라운드 데몬으로 전환합니다.
    process.daemonize({reload:true});
}

function runSysmon() {
  // 15초 간격으로 작업을 실행합니다.
  process.schedule("0,15,30,45 * * * * *", (tick) => {
    // 최근 1·5·15분 평균 부하를 가져옵니다.
    let {load1, load5, load15} = psutil.loadAvg();
    // 가상 메모리 사용률을 확인합니다.
    let mem = psutil.memVirtual();
    // 직전 호출 이후의 CPU 사용률을 계산합니다.
    let cpu = psutil.cpuPercent(0, false);
    // 타임스탬프를 네이티브 시간 객체로 변환합니다.
    let ts = system.parseTime(tick, "ms")
    try{
      client = new db.Client({lowerCaseColumns:true});
      conn = client.connect();
      appender = conn.appender(tableName, "name","time","value");
      appender.append(tagPrefix+"load1", ts, load1);
      appender.append(tagPrefix+"load5", ts, load5);
      appender.append(tagPrefix+"load15", ts, load15);
      appender.append(tagPrefix+"cpu", ts, cpu[0]);
      appender.append(tagPrefix+"mem", ts, mem.usedPercent);
    } finally {
      appender.close();
      conn.close();
    }
  })
}
```

### 차트 TQL

수집한 시스템 지표가 데이터베이스에 저장되므로, TQL로 손쉽게 조회하고 시각화할 수 있습니다.

```js {linenos=table,linenostart=1}
SQL(`select time, value from EXAMPLE
    where name = ? and time between ? and ?`, 
    "sys_load1", time("now -12000s"), time("now"))
MAPVALUE(0, list(value(0), value(1)))
POPVALUE(1)
CHART(
    size("500px", "300px"),
    chartJSCode({
        function yformatter(val, idx){ return val.toFixed(1) }
    }),
    chartOption({
        animation: false,
        yAxis: { type: "value", axisLabel:{ formatter: yformatter }},
        xAxis: { type: "time", axisLabel:{ rotate: -90 }},
        series: [
            {type: "line", data: column(0), name: "LOAD1", symbol:"none"},
        ],
        tooltip: {trigger: "axis", valueFormatter: yformatter},
        legend: {}
    })
)
```

{{< figure src="../img/sysmon-tql.jpg" width="538">}}

### SCRIPT() 활용 차트 TQL

```js {linenos=table,linenostart=1}
SCRIPT({
    const db = require("@jsh/db");
    const client = new db.Client();
    const tags = [ "load1", "load5", "load15" ];
    const end = (new Date()).getTime();
    const begin = end - 240*(60*1000);
    var result = {};
    try {
        conn = client.connect();
        for(tag of tags) {
            rows = conn.query(`
                select time, value from example
                where name = 'sys_${tag}'
                and time between ${begin}000000 and ${end}000000`);
            lst = [];
            for( r of rows ) lst.push([r.time, r.value]);
            if(rows) rows.close();
            result[tag] = lst;
        }
    } catch(e) {
        console.log(e.message);
    } finally {
        if(conn) conn.close();
    }
    $.yield({
      animation: false,
      yAxis: { type: "value", axisLabel:{ }},
      xAxis: { type: "time", axisLabel:{ rotate: -90 }},
      series: [
        {type:"line", data:result.load1, name:"LOAD1", symbol:"none", smooth:true},
        {type:"line", data:result.load5, name:"LOAD5", symbol:"none", smooth:true},
        {type:"line", data:result.load15, name:"LOAD15", symbol:"none", smooth:true},
      ],
      tooltip: {trigger: "axis"},
      legend: {}
    });
})
CHART( size("500px", "300px") )
```

{{< figure src="../img/sysmon-tql-js.jpg" width="500">}}

### HTML에서 차트 그리기

다음 HTML을 `sysmon.html`로 저장한 뒤 브라우저에서 열면 수집한 시스템 모니터링 데이터를 시각화할 수 있습니다.

- sysmon.html

```html {linenos=table,linenostart=1}
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>System Monitoring Chart</title>
  <script src="/web/echarts/echarts.min.js"></script>
  <script>
    function loadJS(url) {
      var scriptElement = document.createElement('script');
      scriptElement.src = url;
      document.getElementsByTagName('body')[0].appendChild(scriptElement);
      }
    function buildTQL(table, tag, begin, end, format) {
      return `
      SQL("select time, value from ${table} "+
        "where name = '${tag}' "+
        "and time between ${begin}000000 and ${end}000000")
      MAPVALUE(1, list(value(0), value(1)))
      CHART(
        size("400px", "200px"),
        chartJSCode({
            function unitFormat(val){
                return val.toFixed(1);
            }
            function percentFormat(val) {
                return ""+val.toFixed(0)+"%";
            }
        }),
        chartOption({
            animation: false,
            yAxis: { type: "value", axisLabel:{ formatter:${format} }},
            xAxis: { type: "time", axisLabel:{ rotate: -90 }},
            series: [
              {type:"line", data:column(1), name:"${tag}", symbol:"none"},
            ],
            tooltip: {trigger: "axis", valueFormatter:${format} },
            legend: {}
        })
      )`
    }
    function loadChart(containerID, table, tag, begin, end, format) {
      fetch('/db/tql',
        {method:"POST", body: buildTQL(table, tag, begin, end, format)}
      )
      .then(response => {
        return response.json()
      })
      .then(obj => {
        const container = document.getElementById(containerID)
        const chartDiv = document.createElement('div')
        chartDiv.setAttribute("id", obj.chartID)
        chartDiv.style.width = obj.style.width
        chartDiv.style.height = obj.style.height
        container.appendChild(chartDiv)
        obj.jsCodeAssets.forEach((js) => loadJS(js))
      })
      .catch(error => {
        console.error('Error fetching chart data:', error);
      });
    }
   </script>
</head>
<body>
  <div style='display:flex;float:left;flex-flow:row wrap'>
    <div id="chart1" style="width: 400px; height: 200px;"></div>
    <div id="chart2" style="width: 400px; height: 200px;"></div>
    <div id="chart3" style="width: 400px; height: 200px;"></div>
    <div id="chart4" style="width: 400px; height: 200px;"></div>
  </div>
  <script>
    let end = (new Date()).getTime(); // now in millisec.
    let begin = end - 30*(60*1000);   // 30 minutes before
    loadChart('chart1', "EXAMPLE", "sys_load1", begin, end, "unitFormat")
    loadChart('chart2', "EXAMPLE", "sys_load5", begin, end, "unitFormat")
    loadChart('chart3', "EXAMPLE", "sys_cpu", begin, end, "percentFormat")
    loadChart('chart4', "EXAMPLE", "sys_mem", begin, end, "percentFormat")
  </script>
</body>
</html>
```

{{< figure src="../img/sysmon-html.jpg" width="600">}}

### HTML 템플릿 차트

이 예제는 `/sysmon` 경로를 제공하는 HTTP 서버를 구성해 템플릿 기반 차트를 반환하는 방법을 보여 드립니다.
서버는 데이터베이스에서 부하·CPU·메모리 지표를 조회한 뒤 ECharts 템플릿(`http-sysmon.html`)에 주입해 실시간으로 시각화합니다.

- `sysmon-server.js`
```js {linenos=table,linenostart=1,hl_lines=[14,37]}
const process = require("@jsh/process");
const http = require("@jsh/http")
const db = require("@jsh/db")

if( process.isDaemon() ) {  // equiv. if( process.ppid() == 1)
    runServer();
} else {
    process.daemonize({reload:true});
}

function runServer() {
    const tags = [ "load1", "load5", "load15", "cpu", "mem" ];
    const svr = new http.Server({address:'127.0.0.1:56802'})
    svr.loadHTMLGlob("/*.html")
    svr.get("/sysmon", ctx => {
        const end = (new Date()).getTime();
        const begin = end - 20*(60*1000); // last 20 min.
        var result = {};
        try {
            client = new db.Client({lowerCaseColumns:true});
            conn = client.connect();
            for( tag of tags ) {
                rows = conn.query(`
                    select time, value from example
                    where name = 'sys_${tag}'
                    and time between ${begin}000000 and ${end}000000`)
                lst = [];
                for( r of rows ) lst.push([r.time, r.value]);
                if(rows) rows.close();
                result[tag] = lst;
            }
        } catch(e) {
            console.log(e);
        } finally {
            if (conn) conn.close();
        }
        ctx.HTML(http.status.OK, "http-sysmon.html", result)
    })
    svr.serve( (result)=>{ 
        console.log("server started", "http://"+result.address) ;
    });
}
```

- `http-sysmon.html`

```html
<html>
<head>
    <script src="https://cdn.jsdelivr.net/npm/echarts@5.6.0/dist/echarts.min.js"></script>
</head>
<body>
<div style='display:flex;float:left;flex-flow:row wrap;width:100%;'>
    <div id="load" style="width:400px;height:300px;margin:4px;"></div>
    <div id="cpu" style="width:400px;height:300px;margin:4px;"></div>
    <div id="mem" style="width:400px;height:300px;margin:4px;"></div>
</div>
<script>
    function doChart(element, title, data) {
        let chart = echarts.init(element, "dark");
        chart.setOption({
            animation:false, "color":["#80FFA5", "#00DDFF", "#37A2FF"],
            title:{"text":title},
            legend:{ bottom: 7 }, tooltip:{"trigger":"axis"},
            xAxis:{type:"time", axisLabel:{ rotate: -90 }},
            yAxis:{type:"value"},
            series: data,
        });
    }
    doChart(document.getElementById('load'), "System Load Avg.", [
        { type:"line", name:"load1", symbol:"none", data:{{.load1}} },
        { type:"line", name:"load5", symbol:"none", data:{{.load5}} },
        { type:"line", name:"load15", symbol:"none", data:{{.load15}} },
    ])
    doChart(document.getElementById('cpu'), "CPU Usage", [
        { type:"line", name:"cpu usage", symbol:"none", data:{{.cpu}} },
    ])
    doChart(document.getElementById('mem'), "Memory Usage", [
        { type:"line", name:"mem usage", symbol:"none", data:{{.mem}} },
    ])
</script>
</body>
</html>
```

{{< figure src="../img/sysmon-template.jpg" width="600">}}

## OPCUA 클라이언트

이 예제는 OPC UA 서버에 연결해 시스템 지표를 읽고 데이터베이스에 저장하는 수집기를 구현합니다.

**동작 흐름**

1. OPC UA 연동: `@jsh/opcua` 모듈을 사용해 `opc.tcp://localhost:4840` 서버에 연결하고 `cpu_percent`, `mem_percent`, `load1` 등 노드 값을 조회합니다.
2. 주기 수집: `process.schedule`을 활용해 10초마다 데이터를 읽습니다.
3. 데이터 적재: 수집한 값은 `EXAMPLE` 테이블에 `name`, `time`, `value` 컬럼으로 저장합니다.
4. 시각화: *System Monitoring* 절에서 소개한 TQL이나 HTML 차트 예제를 그대로 활용하실 수 있습니다.

### 데이터 수집기

스크립트를 `opcua-client.js`로 저장한 뒤 JSH 터미널에서 백그라운드로 실행하십시오.

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
opcua = require("@jsh/opcua");
process = require("@jsh/process");
system = require("@jsh/system");
db = require("@jsh/db");

if( process.isDaemon() ) {  // equiv. if( process.ppid() == 1)
  runClient();
} else {
  process.daemonize({reload:true});
}

function runClient() {
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
  const tableName = "EXAMPLE";
  try {
    uaClient = new opcua.Client({ endpoint: "opc.tcp://localhost:4840" });
    dbClient = new db.Client({lowerCaseColumns:true});
    conn = dbClient.connect();
    
    process.schedule("0,10,20,30,40,50 * * * * *", tick => {
      ts = system.parseTime(tick, "ms")
      vs = uaClient.read({
        nodes: nodes,
        timestampsToReturn: opcua.TimestampsToReturn.Both
      });
      sqlText = `INSERT INTO ${tableName} (name,time,value) values(?,?,?)`
      vs.forEach((v, idx) => {
        if( v.value !== null ) {
            conn.exec(sqlText, tags[idx], ts, v.value);
        }
      })
    })
  } catch (e) {
    process.println("Error:", e.message);
  } finally {
    conn.close();
    uaClient.close();
  }
}
```

### 시뮬레이터 서버

`opcua-client.js`를 시험하려면 필요한 시스템 지표 노드를 제공하는 OPC UA 서버가 필요합니다.
실환경이 없다면 아래 저장소에서 제공하는 시뮬레이터를 사용해 주십시오.
`sys_cpu`, `sys_mem`, `load1`, `load5`, `load15` 등의 샘플 데이터를 제공하여 수집기 및 시각화 흐름을 검증하실 수 있습니다.

설정 방법은 저장소의 안내를 따르시면 됩니다.

[https://github.com/machbase/neo-server/tree/main/mods/jsh/opcua/test_server](https://github.com/machbase/neo-server/tree/main/mods/jsh/opcua/test_server)

시뮬레이터를 실행한 뒤 `opcua-client.js`를 가동하면 OPC UA 클라이언트가 정상적으로 연결되어 데이터를 수집합니다.

## 통계

다음 TQL 예제는 `@jsh/analysis` 모듈을 사용해 숫자 배열의 기초 통계량을 계산하는 방법을 보여 드립니다.
평균, 중앙값, 분산, 표준편차를 구한 뒤 `$.yield()`로 반환하여 CSV 등으로 손쉽게 활용할 수 있습니다.


```js {linenos=table,linenostart=1}
SCRIPT({
    const system = require("@jsh/system");
    const ana = require("@jsh/analysis");
    xs = ana.sort([
		32.32, 56.98, 21.52, 44.32,
		55.63, 13.75, 43.47, 43.34,
		12.34,
    ]);
    $.yield("data", JSON.stringify(xs))

    mean = ana.mean(xs)
    variance = ana.variance(xs)
    stddev = Math.sqrt(variance)

    median = ana.quantile(0.5, xs)

    $.yield("mean", mean)
    $.yield("median", median)
    $.yield("variance", variance)
    $.yield("std-dev", stddev)
})
CSV()

// 예시 출력
// data     [12.34,13.75,21.52,32.32,43.34,43.47,44.32,55.63,56.98]
// mean     35.96333333333334
// median   43.34
// variance 285.306875
// std-dev  16.891029423927957
```
