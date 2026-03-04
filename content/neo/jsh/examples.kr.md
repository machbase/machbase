---
title: 예제
type: docs
weight: 1
---

## HTTP 서버

이 예제는 `http` 모듈을 사용하여 간단한 HTTP 서버를 구현하는 방법을 안내해 드립니다.
서버는 지정한 주소와 포트(`127.0.0.1:56802`)에서 요청을 수신하며 `/hello/:name` REST API 엔드포인트를 제공합니다.
클라이언트가 이름 매개변수를 포함한 GET 요청을 보내면,
서버는 인사 메시지와 전달받은 이름이 들어 있는 JSON 객체로 응답합니다.

동적 라우팅과 JSON 응답을 활용한 경량 HTTP 서버 작성 방법을 익히기에 적합한 예제입니다.

<h6>주요 특징</h6>

1. **라우팅**: `/hello/:name` 라우트에서 URL 경로에 포함된 `name` 값을 추출합니다.
2. **JSON 응답**: 이름과 환영 메시지를 담은 JSON 객체를 반환합니다.

```js {linenos=table,linenostart=1}
const http = require('http');

const svr = new http.Server({network:'tcp', address:'127.0.0.1:56802'});

svr.get('/hello/:name', (ctx) => {
    const name = ctx.param("name")
    ctx.json(http.status.OK, {
        message: "greetings",
        name: name,
    })
})

svr.serve((result) =>{
    console.println('server started', result.network, result.address);
});
```

<h6>사용 절차</h6>

1. Open *JSH* console.
1. 스크립트를 실행하여 서버를 기동합니다.
2. `curl`과 같은 도구로 서버에 GET 요청을 보냅니다.

```sh
curl -o - http://127.0.0.1:56802/hello/Karl
```

서버는 다음과 같이 응답합니다.

```json
{"message":"greetings","name":"Karl"}
```

### 정적 콘텐츠

정적 파일이나 디렉터리를 제공하려면 아래와 같이 설정하십시오.

```js {linenos=table,linenostart=1}
svr.staticFile('/readme', '/path/to/file.txt');
svr.static('/static', '/path/to/static_dir');
```

### 리다이렉트

특정 경로로 이동시키고자 할 때는 다음과 같이 리다이렉션을 지정합니다.

```js {linenos=table,linenostart=1}
svr.get('/readme', ctx => {
    ctx.redirect(http.status.Found, '/docs/readme.html');
});
```

### RESTful API

아래 예제는 목록 조회, 등록, 삭제 요청을 처리하는 기본 REST API 구현입니다.

```js {linenos=table,linenostart=1}
var list = [
    {title:'Indiana Jones', id: 59793, studio: ['Paramount']},
    {title:'Star Wars', id: 64821, studio: ['Lucasfilm']},
];
svr.get('/movies', ctx => {
    ctx.json(http.status.OK, list);
});
svr.post('/movies', ctx => {
    let obj = ctx.request.body;
    list.push(obj);
    ctx.json(http.status.Created, obj);
});
svr.delete('/movies/:id', ctx => {
    let id = parseInt(ctx.param('id'));
    list = list.filter(item => item.id !== id);
    ctx.json(http.status.NoContent)
});
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
    -d '{"title":"new movie", "id":12345, "studio":["HomeVideo"]}'
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
const http = require('http')
try {
    const url = new URL('http://127.0.0.1:56802/hello/Steve');
    // 지정한 URL로 GET 요청을 생성합니다.
    const req = http.request(url);
    req.end((response) => {
        const {statusCode, statusMessage} = response;
        console.println("Status Code:", statusCode);
        console.println("Status Message:", statusMessage);
        console.println("Body:", response.json());
    })
} catch (e) {
    // 요청 과정에서 발생한 오류를 출력합니다.
    println(e.message);
}
// Output:
//
// Status Code: 200
// Status Message: 200 OK
// Body: {message:greetings, name:Steve}
```

<h6>사용 절차</h6>

1. HTTP 서버 예제와 같이 서버가 실행 중인지 확인하십시오.
2. 스크립트를 실행하여 서버에 GET 요청을 전송합니다.

