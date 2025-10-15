---
title: HTTP API
type: docs
weight: 40
---

machbase-neo는 HTTP API를 통해 두 가지 주요 기능을 제공합니다.
하나는 모든 종류의 SQL 구문을 실행할 수 있는 `query`, 다른 하나는 `INSERT INTO ...` SQL과 동일한 기능을 제공하는 `write`입니다.

HTTP API의 일반적인 목적은 센서와 디바이스가 MQTT와 HTTP로 데이터를 적재하는 동안,
사용자 서비스 애플리케이션과 데이터 분석 도구가 machbase 데이터베이스에 저장된 데이터에 접근할 수 있도록 기능을 노출하는 데 있습니다.

{{< figure src="/images/interfaces.jpg" width="500" >}}


## Endpoints

애플리케이션과 센서는 HTTP API를 통해 데이터를 읽고 쓸 수 있습니다.

### Database Query

| Method  | Path             | Description                                     |
| :-----: | :--------------- | :-----------------------------------------------|
| GET     | `/db/query`      | `q` 매개변수를 사용해 쿼리를 실행합니다.        |
| POST    | `/db/query`      | JSON 또는 폼 데이터를 사용해 쿼리를 실행합니다. |

### Database Write

| Method  | Path             | Description                                      |
| :-----: | :--------------- | :----------------------------------------------- |
| POST    | `/db/write`      | JSON 또는 CSV 형식으로 데이터를 저장합니다.      |
| POST    | `/metrics/write` | ILP(Influx Line Protocol) 형식으로 데이터를 저장합니다. |

### TQL Endpoints

| Method  | Path                      | Description                                                                    |
| :-----: | :------------------------ | :------------------------------------------------------------------------------|
| GET     | `/db/tql/{tql_file_path}` | 경로로 지정한 TQL 파일을 실행합니다.                                          |
| POST    | `/db/tql/{tql_file_path}` | 요청 본문을 입력값으로 사용해 지정한 TQL 파일을 실행합니다.                   |
| POST    | `/db/tql`                 | 요청 본문에 포함된 TQL 스크립트를 실행합니다.                                 |
| POST    | `/db/tql?$={tql_script}`  | 쿼리 매개변수 `$`로 전달된 TQL 스크립트를 요청 본문과 함께 실행합니다. {{< neo_since ver="8.0.17" />}} |

## Testing HTTP API

machbase-neo 웹 UI에는 REST API 클라이언트가 내장되어 있어 아래 예시처럼 워크시트의 마크다운이나 TQL에서 바로 HTTP API를 테스트할 수 있습니다.

- 워크시트의 마크다운

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

## 이 장에서 안내하는 내용

{{< children_toc />}}
