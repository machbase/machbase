---
toc: true
title: "http"
type: docs
weight: 100
---

{{< neo_since ver="8.5.0" />}}

`http`モジュールは、JSHアプリケーション用にNode.js互換のHTTPクライアント/サーバーAPIを提供します。

## request() {#request}

`ClientRequest`オブジェクトを作成します。

対応するシグネチャ：

- `request(url[, options][, callback])`
- `request(options[, callback])`

- 戻り値: `ClientRequest`
- `callback`を指定すると、応答の受信時に`IncomingMessage`を引数として受け取ります。

<h6>構文</h6>

```js
request(url[, options][, callback])
request(options[, callback])
```

<h6>主なリクエストオプション</h6>

- `url` (`string`または`URL`)
- `protocol`, `host`, `hostname`, `port`, `path`
- `method`
- `headers`
- `auth` (`Authorization: Basic ...`に変換)
- `agent`

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const http = require('http');
const req = http.request('http://127.0.0.1:8080/hello');
req.on('response', (res) => {
  console.println(res.statusCode, res.statusMessage);
});
req.end();
```

## get() {#get}

GETリクエストの短縮関数です。内部で`request()`を作成し、自動的に`end()`を呼び出します。

対応するシグネチャ：

- `get(url[, options][, callback])`
- `get(options[, callback])`

- 戻り値: `ClientRequest`
- `callback`を省略した場合は、`response`イベントリスナーで応答を処理できます。

<h6>構文</h6>

```js
get(url[, options][, callback])
get(options[, callback])
```

**status**

HTTPステータスコードのマップです。

例:

- `http.status.OK`
- `http.status.NotFound`
- `http.status.InternalServerError`

**動作に関する注意**

- `response.ok`は、ステータスコードが`200`〜`299`の場合に`true`です。
- `response.headers`のキーは、小文字に正規化されます。
- `setHeader()`、`getHeader()`、`hasHeader()`、`removeHeader()`は、ヘッダー名の大文字と小文字を区別しません。
- `write()`を複数回呼び出すと、リクエストボディを蓄積してから送信します。

## ClientRequest {#clientrequest}

`request()`または`get()`が返すリクエストオブジェクトです。

**ClientRequestのヘッダーメソッド**

- `setHeader(name, value)`
- `getHeader(name)`
- `hasHeader(name)`
- `removeHeader(name)`
- `getHeaders()`
- `getHeaderNames()`

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const http = require('http');
const req = http.request('http://127.0.0.1:8080/hello');
req.setHeader('X-Test-Header', 'TestValue');
console.println(req.hasHeader('X-Test-Header'));
console.println(req.getHeader('X-Test-Header'));
req.end();
```

**ClientRequest.write()**

リクエストボディのチャンクを書き込みます。

- `chunk`は、`string`と`Uint8Array`に対応しています。
- 成功時に`true`、失敗時に`false`を返します。

<h6>構文</h6>

```js
write(chunk[, encoding][, callback])
```

**ClientRequest.end()**

リクエストを完了して送信します。

- `callback`を渡すと、応答オブジェクト（`IncomingMessage`）を引数として受け取ります。

<h6>構文</h6>

```js
end([data[, encoding]][, callback])
```

**ClientRequest.destroy()**

リクエストオブジェクトを破棄し、必要に応じてエラーイベントを発生させます。

<h6>構文</h6>

```js
destroy([err])
```

**ClientRequest イベント**

- `response` (`IncomingMessage`)
- `error` (`Error`)
- `end` ()

## IncomingMessage {#incomingmessage}

HTTPレスポンスオブジェクトです。

<h6>主なプロパティ</h6>

- `statusCode`
- `statusMessage`
- `ok` (2xxの場合はtrue)
- `headers`
- `rawHeaders`
- `httpVersion`
- `complete`
- `raw` (内部のGoレスポンスオブジェクト)

**IncomingMessageのボディメソッド**

- `text([encoding])`
- `json()`
- `readBody([encoding])`
- `readBodyBuffer()`

- `text()`と`readBody()`の既定のエンコーディングは、`utf-8`です。
- `json()`は、解析に失敗すると例外を発生させる場合があります。

**IncomingMessageのユーティリティメソッド**

- `setTimeout(msecs[, callback])`
- `close()`

通常の処理ではレスポンスボディは自動的に閉じます。必要に応じて`close()`を明示的に呼び出せます。

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const http = require('http');
http.get('http://127.0.0.1:8080/hello', (res) => {
  console.println(res.ok, res.statusCode);
  console.println(res.text());
});
```

## Server {#server}

HTTPサーバーオブジェクトです。

<h6>作成</h6>

```js
new Server([options])
```

<h6>オプション</h6>

- `network`: `tcp`または`unix`（既定値：`tcp`）
- `address`: `host:port`またはUnixソケットのパス
- `env`: 環境オブジェクト（省略可能）。ファイルシステムへのアクセスには必要です。

**Serverのルート・静的ファイル用メソッド**

- `get(path, handler)`
- `post(path, handler)`
- `put(path, handler)`
- `delete(path, handler)`
- `ws(path[, options], handler)`
- `static(path, root)`
- `staticFile(path, file)`

**Serverのテンプレートメソッド**

- `loadHTMLFiles(...files)`
- `loadHTMLGlob(pattern)`

**Serverのライフサイクルメソッド**

- `serve([callback])`
- `close([callback])`

`serve(callback)`は、`{ network, address }`を渡します。

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const http = require('http');
const server = new http.Server({ network: 'tcp', address: '127.0.0.1:8080' });
server.get('/hello/:name', (ctx) => {
  const name = ctx.param('name');
  ctx.json(http.status.OK, { greeting: 'hello', name });
});
server.serve();
```

## Server.ws() {#serverws}

{{< neo_since ver="8.5.2" />}}

HTTPサーバーにWebSocketルートを簡単に接続する便利なAPIです。

内部で`require('ws').WebSocketServer`を作成し、現在の`http.Server`に接続します。

<h6>構文</h6>

```js
server.ws(path, handler)
server.ws(path, options, handler)
```

<h6>オプション</h6>

- `verifyClient({ origin, req })`
- `handleProtocols(protocols, req)`
- `clientTracking` (既定値： `true`)

<h6>使用例</h6>

```js {linenos=table,linenostart=1}
const http = require('http');

const server = new http.Server({ network: 'tcp', address: '127.0.0.1:8080' });

server.ws('/ws', {
  verifyClient: ({ req }) => req.query('token') === 'allow',
  handleProtocols: (protocols) => {
    if (protocols.indexOf('machbase.rpc') >= 0) {
      return 'machbase.rpc';
    }
    return false;
  },
}, (socket, request) => {
  console.println(request.path, request.httpVersion, socket.protocol);
  socket.on('message', (event) => {
    socket.send('echo:' + event.data);
  });
});

server.serve();
```

`handler`は`(socket, request)`を受け取ります。`socket`は`ws.WebSocket`と同じイベントモデルを使用し、`request`はハンドシェイクリクエストの情報を持つヘルパーオブジェクトです。

**Server.ws() 動作に関する注意**

- `verifyClient()`と`handleProtocols()`は、同期的に呼び出されます。
- `verifyClient()`が`false`を返すと、ハンドシェイクを拒否します。
- `handleProtocols()`は、選択したプロトコル文字列、または拒否を表すfalsyな値を返す必要があります。
- `request`は、Node.jsの完全な`IncomingMessage`ではなく、JSH用のヘルパーオブジェクトです。
- 低水準の`upgrade`イベントや`handleUpgrade()` APIは提供しません。

**Serverのコンテキスト**

ハンドラーは、リクエスト・レスポンスのヘルパーを含む`ctx`を引数として受け取ります。

<h6>リクエストヘルパー</h6>

- `ctx.request.path`
- `ctx.request.query`
- `ctx.request.body`
- `ctx.request.getHeader(name)`
- `ctx.param(name)`
- `ctx.query(name)`

<h6>レスポンスヘルパー</h6>

- `ctx.setHeader(name, value)`
- `ctx.redirect(status, url)`
- `ctx.abort()`
- `ctx.text(status, format[, ...args])`
- `ctx.html(status, template, data)`
- `ctx.yaml(status, data)`
- `ctx.toml(status, data)`
- `ctx.json(status, data[, { space: number|string }])`
- `ctx.xml(status, data[, { root: string }])`

`ctx.json()`は、インデント用の`space`オプションに対応しています。

```js
ctx.json(http.status.OK, { greeting: 'hello', name: 'neo' }, { space: 2 });
ctx.json(http.status.OK, { greeting: 'hello', name: 'neo' }, { space: '\t' });
```

`ctx.xml()`は、既定でオブジェクトをルート要素`<map>`として出力します。最上位の要素名を変更するには、オプションオブジェクトの`root`フィールドを指定します。

```js {linenos=table,linenostart=1}
svr.get('/formats/xml', (ctx) => {
  ctx.xml(http.status.OK, { str: 'Hello World', num: 123, bool: true });
});

svr.get('/formats/xml-root', (ctx) => {
  ctx.xml(http.status.OK, { name: 'neo', count: 2 }, { root: 'user' });
});
```

既定のXML出力：

```xml
<map><str>Hello World</str><num>123</num><bool>true</bool></map>
```

`root`を指定したXML出力：

```xml
<user><name>neo</name><count>2</count></user>
```

## クライアントの例 {#클라이언트-예제}

### GETリクエスト（コールバック） {#get-요청-callback}

```js {linenos=table,linenostart=1}
const http = require('http');

http.get('http://127.0.0.1:8080/hello', (res) => {
  console.println('Status:', res.statusCode, res.statusMessage);
  console.println('Body:', res.text());
});
```

### GETリクエスト（イベントリスナー） {#get-요청-event-listener}

```js {linenos=table,linenostart=1}
const http = require('http');

const req = http.get('http://127.0.0.1:8080/hello');
req.on('response', (res) => {
  console.println('Status:', res.statusCode, res.statusMessage);
  console.println('Body:', res.text());
});
```

### リクエストヘッダーの設定と取得 {#요청-헤더-설정조회}

```js {linenos=table,linenostart=1}
const http = require('http');

const req = http.request('http://127.0.0.1:8080/hello');
req.setHeader('X-Trace-Id', 'trace-001');
console.println(req.hasHeader('x-trace-id'));
console.println(req.getHeader('X-Trace-Id'));
req.end();
```

### レスポンスヘッダーとボディの読み取り {#응답-헤더본문-읽기}

```js {linenos=table,linenostart=1}
const http = require('http');

http.get('http://127.0.0.1:8080/hello', (res) => {
  const contentType = res.headers['content-type'];
  const contentLength = res.headers['content-length'];

  console.println('Content-Type:', contentType);
  console.println('Content-Length:', contentLength);
  console.println('Body:', res.text());
});
```

### POST JSONリクエスト {#post-json-요청}

```js {linenos=table,linenostart=1}
const http = require('http');

const req = http.request('http://127.0.0.1:8080/echo', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  }
});

req.on('response', (res) => {
  if (!res.ok) {
    throw new Error('request failed: ' + res.statusCode);
  }
  console.println(res.json());
});

req.on('error', (err) => {
  console.println('Request error:', err.message);
});

req.write('{"message":"hello"}');
req.end();
```

### 404レスポンスの処理 {#404-응답-처리}

```js {linenos=table,linenostart=1}
const http = require('http');

http.get('http://127.0.0.1:8080/notfound', (res) => {
  console.println('Status:', res.statusCode, res.statusMessage);
  if (!res.ok) {
    console.println('Request failed');
  }
});
```

### URLオブジェクトによるリクエスト {#url-객체-기반-요청}

サーバーの実行中にGETリクエストを送信し、JSONボディを解析します。

```js {linenos=table,linenostart=1}
const http = require('http');

try {
  const url = new URL('http://127.0.0.1:56802/hello/Steve');
  const req = http.request(url);
  req.end((response) => {
    const { statusCode, statusMessage } = response;
    console.println('Status Code:', statusCode);
    console.println('Status Message:', statusMessage);
    console.println('Body:', response.json());
  });
} catch (e) {
  console.println(e.message);
}
```

## サーバーの例 {#서버-예제}

### 簡単なHTTPサーバー {#간단한-http-서버}

`127.0.0.1:56802`でサーバーを起動し、`/hello/:name`パスでJSONを返します。

```js {linenos=table,linenostart=1}
const http = require('http');

const svr = new http.Server({ network: 'tcp', address: '127.0.0.1:56802' });

svr.get('/hello/:name', (ctx) => {
  const name = ctx.param('name');
  ctx.json(http.status.OK, {
    message: 'greetings',
    name: name,
  });
});

svr.serve((result) => {
  console.println('server started', result.network, result.address);
});
```

```sh
curl -o - http://127.0.0.1:56802/hello/Karl
```

```json
{"message":"greetings","name":"Karl"}
```

### 静的コンテンツとリダイレクト {#정적-콘텐츠리다이렉트}

```js {linenos=table,linenostart=1}
svr.staticFile('/readme', '/path/to/file.txt');
svr.static('/static', '/path/to/static_dir');

svr.get('/readme', (ctx) => {
  ctx.redirect(http.status.Found, '/docs/readme.html');
});
```

### RESTful API {#restful-api}

```js {linenos=table,linenostart=1}
let list = [
  { title: 'Indiana Jones', id: 59793, studio: ['Paramount'] },
  { title: 'Star Wars', id: 64821, studio: ['Lucasfilm'] },
];

svr.get('/movies', (ctx) => {
  ctx.json(http.status.OK, list);
});

svr.post('/movies', (ctx) => {
  const obj = ctx.request.body;
  list.push(obj);
  ctx.json(http.status.Created, obj);
});

svr.delete('/movies/:id', (ctx) => {
  const id = parseInt(ctx.param('id'));
  list = list.filter((item) => item.id !== id);
  ctx.json(http.status.NoContent);
});
```

次のコマンドで、各呼び出しを確認できます。

- GETリクエスト
```sh
curl -o - http://127.0.0.1:56802/movies
```
```json
[
  { "id": 59793, "studio": [ "Paramount" ], "title": "Indiana Jones" },
  { "id": 64821, "studio": [ "Lucasfilm" ], "title": "Star Wars" }
]
```

- POSTリクエスト

```sh
curl -o - -X POST http://127.0.0.1:56802/movies \
    -H "Content-Type: application/json" \
    -d '{"title":"new movie", "id":12345, "studio":["HomeVideo"]}'
```

- DELETEリクエスト

```sh
curl -v -o - -X DELETE http://127.0.0.1:56802/movies/12345
```

```sh
< HTTP/1.1 204 No Content
< Content-Type: text/plain; charset=utf-8
< Date: Thu, 08 May 2025 20:39:34 GMT
<
```

### HTMLテンプレート {#html-템플릿}

以下の設定は、`/*.html`パターンに一致するすべてのHTMLテンプレートを読み込みます。
テンプレートを使用すると、定義済みのレイアウトと実行時のデータを組み合わせて、HTMLレスポンスを動的に生成できます。

```js {linenos=table,linenostart=1}
svr.loadHTMLGlob('/*.html');

svr.get('/movielist', (ctx) => {
  const obj = {
    subject: 'Movie List',
    list: [
      { title: 'Indiana Jones', id: 59793, studio: ['Paramount'] },
      { title: 'Star Wars', id: 64821, studio: ['Lucasfilm'] },
    ],
  };
  ctx.html(http.status.OK, 'movie_list.html', obj);
});
```


- HTMLテンプレートのコード`movie_list.html`

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

`/movielist`エンドポイントにGETリクエストを送信すると、
サーバーは、`movie_list.html`テンプレートと`obj`データを使ってHTMLページを生成します。

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
