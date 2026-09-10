---
toc: true
title: サービスプロキシ
type: docs
weight: 120
---

{{< neo_since ver="8.5.2" />}}

JSHサービスは、独自のHTTPサーバーを起動し、machbase-neoの`/web/services/<service_name>/<prefix>/*`パスで公開できます。
サービス開発者は、外部クライアントにサービスのポートを知らせる必要はなく、起動時にプロキシエンドポイントを登録します。
クライアントはmachbase-neoと同じオリジンでアクセスするため、別途ポートを調べたりCORSを設定したりする必要はありません。

## 概要 {#개요}

実行中のJSHサービスが、`SERVICE_CONTROLLER`を介してサービスプロキシを動的に登録します。
登録したパスへのHTTPリクエストは、登録先のサーバーにリバースプロキシされます。

公開パスの形式は以下のとおりです。

```text
/web/services/<service_name>/<prefix>/*
```

たとえば、サービス名が`github.com/acme/chart`、prefixが`/api/`の場合、クライアントは次のアドレスにアクセスします。

```text
/web/services/github.com/acme/chart/api/series
```

## 命名規則 {#이름-규칙}

`service_name`に、別途名前空間の制限は設けていません。
同じ`service_name`と`prefix`の組み合わせは、最初に登録したプロセスが所有します。
後から別のtargetで同じ組み合わせを登録すると、競合エラーが発生します。

パッケージとして配布するサービスは、名前の競合を避けるため、パッケージ名を`service_name`に使用することを推奨します。

```javascript
service: 'github.com/acme/chart'
```

1つのサービスに、複数のプロキシエンドポイントを登録できます。

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

## Targetの制限 {#target-제한}

プロキシのtargetは、machbase-neoサーバーが安全にアクセスできるローカルエンドポイントに制限されます。

許可されるtargetは以下のとおりです。

- `http://127.0.0.1:<port>`
- `http://localhost:<port>`
- その他のループバックIPアドレス
- `unix://<absolute_socket_path>`

外部ホストと`https://`のtargetは、既定では許可しません。
この制限は、サービスプロキシが任意の外部アドレスに接続するオープンプロキシになることを防ぎます。

## 登録 {#등록}

サービスのコードでは、`service`モジュールの`proxy.register()`を使用します。

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

登録項目には、以下のフィールドを使用します。

| フィールド | 型 | 説明 |
| --- | --- | --- |
| `service` | `String` | 公開パスのサービス名 |
| `prefix` | `String` | サービス配下のプロキシのprefix |
| `target` | `String` | リクエストを転送する、ローカルHTTPまたはUnixソケットのエンドポイント |
| `stripPrefix` | `String` | 省略可能。targetに転送する前に除去する公開パスのprefix |
| `healthPath` | `String` | 省略可能。ヘルスチェック用パスのメタデータ |

`stripPrefix`を省略すると、既定で`/web/services/<service_name>/<prefix>`を除去してtargetに転送します。
たとえば、`/web/services/github.com/acme/chart/api/series`へのリクエストは、targetサーバーに`/series`として転送します。

**stripPrefix**

サービス内部のルーターが公開パスの一部を必要とする場合は、`stripPrefix`を直接指定できます。
たとえば、プロキシのprefixを`/api/`で登録し、targetサーバーで`/api/series`を処理するには、サービスのベースパスだけを除去します。

```javascript
service.proxy.register({
    service: 'github.com/acme/chart',
    prefix: '/api/',
    target: 'http://127.0.0.1:18080',
    stripPrefix: '/web/services/github.com/acme/chart'
}, callback);
```

この設定では、以下のようにパスを転送します。

| 公開リクエストパス | targetサーバーが受け取るパス |
| --- | --- |
| `/web/services/github.com/acme/chart/api/series` | `/api/series` |
| `/web/services/github.com/acme/chart/api/healthz` | `/api/healthz` |

`stripPrefix`を省略すると、既定で`/web/services/github.com/acme/chart/api`を除去するため、targetサーバーは`/series`、`/healthz`を受け取ります。

## 登録解除 {#등록-해제}

サービスの終了時には、登録したプロキシエンドポイントを解除することを推奨します。

特定のprefixだけを解除するには、以下のように呼び出します。

```javascript
service.proxy.unregister('github.com/acme/chart', '/api/', function(err) {
    if (err) {
        console.println('proxy unregister failed:', err.message);
    }
});
```

サービス名に属するすべてのエンドポイントを解除するには、prefixを省略します。

```javascript
service.proxy.unregister('github.com/acme/chart', function(err) {
    if (err) {
        console.println('proxy unregister failed:', err.message);
    }
});
```

## 検索 {#조회}

現在の登録状態は、`proxy.list()`と`proxy.get()`で確認できます。

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

## servicectlの管理コマンド {#servicectl-관리-명령}

稼働中のプロキシの登録状態は、`servicectl proxy`コマンドでも確認・管理できます。
このコマンドは`SERVICE_CONTROLLER`に接続するため、`--controller`オプションまたは`SERVICE_CONTROLLER`環境変数を使用します。

```sh
servicectl proxy list
servicectl proxy list github.com/acme/chart
servicectl proxy get github.com/acme/chart /api/
```

テストや手動運用では、CLIから直接登録することもできます。

```sh
servicectl proxy register github.com/acme/chart /api/ http://127.0.0.1:18080 --health-path /healthz
servicectl proxy unregister github.com/acme/chart /api/
```

`proxy unregister <service_name>`のようにprefixを省略すると、そのサービス名で登録したすべてのプロキシエンドポイントを削除します。
通常のサービスコードでは、開始時に`service.proxy.register()`、終了時に`service.proxy.unregister()`を呼び出す方式を推奨します。`servicectl proxy`は、運用確認とデバッグに使用します。

## TCP 例 {#tcp-예시}

次の例は、サービスがローカルHTTPサーバーを起動し、`/web/services/github.com/acme/chart/api/*`パスに登録する手順を示します。

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

## Unixドメインソケットの例 {#unix-domain-socket-예시}

JSHの`http.Server`は、`network: 'unix'`設定に対応しています。
サービス専用のHTTPサーバーを、TCPポートではなくUnixドメインソケットにバインドすると、外部ポートを開かずにサービスプロキシと接続できます。
`target`には、`unix://`の後にソケットの絶対パスを指定します。

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

たとえば、`/web/services/github.com/acme/chart/api/series`へのリクエストは、Unixソケットで接続したサービスサーバーの`/series`に転送されます。
ソケットのパスは絶対パスである必要があります。本番環境では、サービス間で競合しないパスを使用してください。

## 注意事項 {#주의-사항}

- 登録情報はランタイムの状態です。サービスを再起動した場合は、再登録する必要があります。
- 同じ`service_name`と`prefix`の組み合わせは、最初に登録したプロセスが所有します。
- 未登録の`/web/services/<service_name>/<prefix>/*`リクエストは、他のパッケージ処理にフォールバックしません。
- サービスには、外部公開ポートではなく、ループバックまたはUnixドメインソケットの使用を推奨します。
