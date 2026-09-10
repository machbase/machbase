---
toc: true
title: HTTP API
type: docs
weight: 40
---

machbase-neoは、HTTP APIで2つの主要機能を提供します。
あらゆる種類のSQL文を実行できる`query`と、SQLの`INSERT INTO ...`と同じ機能を提供する`write`です。

HTTP APIは、センサーやデバイスがMQTTやHTTPでデータを取り込む一方で、
ユーザーのサービスアプリケーションやデータ分析ツールが、Machbaseデータベースに保存されたデータにアクセスできるようにすることを主な目的としています。

{{< figure src="/images/interfaces.jpg" width="500" >}}


## エンドポイント {#endpoints}

アプリケーションやセンサーは、HTTP APIでデータを読み書きできます。

### データベースの検索 {#database-query}

| メソッド  | パス             | 説明                                     |
| :-----: | :--------------- | :-----------------------------------------------|
| GET     | `/db/query`      | `q`パラメーターでクエリを実行します。        |
| POST    | `/db/query`      | JSONまたはフォームデータでクエリを実行します。 |

### データベースへの書き込み {#database-write}

| メソッド  | パス             | 説明                                      |
| :-----: | :--------------- | :----------------------------------------------- |
| POST    | `/db/write`      | JSON形式またはCSV形式でデータを保存します。      |
| POST    | `/metrics/write` | ILP（Influx Line Protocol）形式でデータを保存します。 |

### TQLエンドポイント {#tql-endpoints}

| メソッド  | パス                      | 説明                                                                    |
| :-----: | :------------------------ | :------------------------------------------------------------------------------|
| GET     | `/db/tql/{tql_file_path}` | パスで指定したTQLファイルを実行します。                                          |
| POST    | `/db/tql/{tql_file_path}` | リクエストボディを入力として、指定したTQLファイルを実行します。                   |
| POST    | `/db/tql`                 | リクエストボディに含まれるTQLスクリプトを実行します。                                 |
| POST    | `/db/tql?$={tql_script}`  | クエリパラメーター`$`で渡されたTQLスクリプトを、リクエストボディとともに実行します。 {{< neo_since ver="8.0.17" />}} |

## HTTP APIのテスト {#testing-http-api}

machbase-neoのWeb UIにはREST APIクライアントが組み込まれています。以下の例のように、ワークシートのMarkdownやTQLから直接HTTP APIをテストできます。

- ワークシートのMarkdown

~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=select count(*) from example
    &format=ndjson
```
~~~

{{< figure src="./img/http_client_wrk.jpg" width="936" >}}

- TQL

```
HTTP({
    GET http://127.0.0.1:5654/db/query
        ?q=select count(*) from example
        &format=ndjson
})
TEXT()
```

{{< figure src="./img/http_client_tql.jpg" width="733" >}}

## この章の内容 {#이-장에서-안내하는-내용}

{{< children_toc />}}
