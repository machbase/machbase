---
title: HTTP 쓰기
type: docs
weight: 20
---

쓰기 API 엔드포인트는 `/db/write/{TABLE}`이며, `{TABLE}`은 데이터를 저장할 테이블 이름입니다.

`query` API로도 `INSERT` 구문을 실행할 수 있지만, 요청마다 `q` 매개변수에 정적인 SQL 문자열을 구성해야 하므로 비효율적입니다.
데이터를 적재할 때는 `INSERT`와 동일하게 동작하는 `write` API를 사용하시는 것이 일반적입니다.
또한 `write` API를 사용하면 하나의 요청으로 여러 레코드를 한꺼번에 삽입할 수 있다는 장점이 있습니다.

## 매개변수

**쓰기 매개변수**

| param       | default | description                                                    |
|:----------- |---------|:---------------------------------------------------------------|
| timeformat  | `ns`     | 시간 단위: `s`, `ms`, `us`, `ns`                               |
| tz          | `UTC`    | 시간대: `UTC`, `Local`, 특정 지역                              |
| method      | `insert` | 데이터 쓰기 방식: `insert`, `append`                           |

**INSERT vs. APPEND**

기본적으로 `/db/write` API는 `INSERT INTO ...` 구문을 사용해 데이터를 저장합니다. 소량의 레코드를 적재할 때는 `append` 방식과 성능 차이가 거의 없습니다.

수십만 건 이상의 대량 데이터를 적재할 때는 `method=append` 매개변수를 사용해 주십시오. 이렇게 지정하면 `method=insert`가 암묵적으로 적용되는 기본 동작 대신 Machbase Neo가 “append” 방식을 사용하도록 설정됩니다.

**Content-Type 헤더**

machbase-neo 서버는 `Content-Type` 헤더를 통해 입력 데이터 스트림의 형식을 판별합니다.
예를 들어 JSON 데이터는 `Content-Type: application/json`, CSV 데이터는 `Content-Type: text/csv`, 줄 단위 JSON은 `Content-Type: application/x-ndjson`을 지정해야 합니다.

**Content-Encoding 헤더**

클라이언트가 gzip으로 압축된 스트림을 전송할 경우 `Content-Encoding: gzip` 헤더를 설정하여 입력 데이터가 gzip으로 인코딩되었음을 machbase-neo에 알려야 합니다.

## Inputs

### JSON

이 요청 메시지는 `INSERT INTO {table} (columns...) VALUES (values...)` 구문과 동일한 구조입니다.

| name         | type       |  description            |
|:------------ |:-----------|:------------------------|
| data         | object     | 데이터 본문 전체        |
| data.columns | array of strings | 컬럼 목록을 지정합니다. |
| data.rows    | array of tuples  | 레코드 값 배열입니다.   |

**JSON**

```json
{
    "data": {
        "columns":["name", "time", "value"],
        "rows": [
            [ "json-data", 1670380342000000000, 1.0001 ],
            [ "json-data", 1670380343000000000, 2.0002 ]
        ]
    }
}
```

`Content-Type` 헤더를 `application/json`으로 설정해 주십시오.

{{< tabs items="HTTP,cURL">}}
{{< tab >}}
~~~
```http
POST http://127.0.0.1:5654/db/write/EXAMPLE
Content-Type: application/json

{
    "data": {
        "columns":["name", "time", "value"],
        "rows": [
            [ "json-data", 1670380342000000000, 1.0001 ],
            [ "json-data", 1670380343000000000, 2.0002 ]
        ]
    }
}
```
~~~
{{< /tab >}}
{{< tab >}}
```sh
curl -X POST http://127.0.0.1:5654/db/write/EXAMPLE \
    -H "Content-Type: application/json" \
    --data-binary "@post-data.json"
```
{{< /tab >}}
{{< /tabs >}}

**압축 JSON**

입력 스트림이 gzip으로 압축되었다면 `Content-Encoding: gzip` 헤더를 설정하여 machbase-neo에 알려야 합니다.

{{< tabs items="HTTP,cURL">}}
{{< tab >}}
~~~
```http
POST http://127.0.0.1:5654/db/write/EXAMPLE
Content-Type: application/json
Content-Encoding: gzip

< /csv/post-data.json.gz
```
~~~
{{< /tab >}}
{{< tab >}}
```sh
curl -X POST http://127.0.0.1:5654/db/write/EXAMPLE \
    -H "Content-Type: application/json" \
    -H "Content-Encoding: gzip" \
    --data-binary "@post-data.json.gz"
```
{{< /tab >}}
{{< /tabs >}}

**timeformat을 사용하는 JSON**

시간 필드가 UNIX 에포크가 아닌 문자열 형식이라면 `timeformat`과 `tz` 매개변수를 함께 지정해 주십시오.

{{< tabs items="HTTP, cURL">}}
{{< tab >}}
~~~
```http
POST http://127.0.0.1:5654/db/write/EXAMPLE
    ?timeformat=DEFAULT
    &tz=Asia/Seoul
Content-Type: application/json

{
    "data": {
        "columns":["name", "time", "value"],
        "rows": [
            [ "json-data", "2022-12-07 02:32:22", 1.0001 ],
            [ "json-data", "2022-12-07 02:32:23", 2.0002 ]
        ]
    }
}
```
~~~
{{< /tab >}}
{{< tab >}}
```sh
curl -X POST 'http://127.0.0.1:5654/db/write/EXAMPLE?timeformat=DEFAULT&tz=Asia/Seoul' \
    -H "Content-Type: application/json" \
    --data-binary "@post-data.json"
```

- `post-data.json`

```json
{
    "data": {
        "columns":["name", "time", "value"],
        "rows": [
            [ "json-data", "2022-12-07 02:32:22", 1.0001 ],
            [ "json-data", "2022-12-07 02:32:23", 2.0002 ]
        ]
    }
}
```
{{< /tab >}}
{{< /tabs >}}

### NDJSON

NDJSON(Newline Delimited JSON)은 각 줄이 유효한 JSON 객체인 스트리밍 형식입니다. 대용량 데이터나 스트리밍 데이터를 처리할 때 유용합니다.

이 요청 메시지 역시 `INSERT INTO {table} (columns...) VALUES (values...)` 구문과 동일한 구조입니다.

**NDJSON**

```json
{"NAME":"ndjson-data", "TIME":1670380342000000000, "VALUE":1.001}
{"NAME":"ndjson-data", "TIME":1670380343000000000, "VALUE":2.002}
```

`Content-Type` 헤더를 `application/x-ndjson`으로 설정해 주십시오.

{{< tabs items="HTTP,cURL">}}
{{< tab >}}
~~~
```http
POST http://127.0.0.1:5654/db/write/EXAMPLE
Content-Type: application/x-ndjson

{"NAME":"ndjson-data", "TIME":1670380342000000000, "VALUE":1.001}
{"NAME":"ndjson-data", "TIME":1670380343000000000, "VALUE":2.002}
```
~~~
{{< /tab >}}
{{< tab >}}
```sh
curl -X POST http://127.0.0.1:5654/db/write/EXAMPLE \
    -H "Content-Type: application/x-ndjson" \
    --data-binary "@post-data.json"
```
{{< /tab >}}
{{< /tabs >}}


**timeformat을 사용하는 NDJSON**

시간 필드가 UNIX 에포크가 아닌 문자열 형식이면 다음과 같이 작성할 수 있습니다.

```json
{"NAME":"ndjson-data", "TIME":"2022-12-07 02:33:22", "VALUE":1.001}
{"NAME":"ndjson-data", "TIME":"2022-12-07 02:33:23", "VALUE":2.002}
```

`timeformat`과 `tz` 매개변수를 함께 지정해 주십시오.

{{< tabs items="HTTP,cURL">}}
{{< tab >}}
~~~
```http
POST http://127.0.0.1:5654/db/write/EXAMPLE
    ?timeformat=DEFAULT
    &tz=Local
Content-Type: application/x-ndjson

{"NAME":"ndjson-data", "TIME":"2022-12-07 02:33:22", "VALUE":1.001}
{"NAME":"ndjson-data", "TIME":"2022-12-07 02:33:23", "VALUE":2.002}
```
~~~
{{< /tab >}}
{{< tab >}}
```sh
curl -X POST 'http://127.0.0.1:5654/db/write/EXAMPLE?timeformat=Default&tz=Local' \
    -H "Content-Type: application/x-ndjson" \
    --data-binary "@post-data.json"
```
{{< /tab >}}
{{< /tabs >}}


### CSV

다음 옵션은 본문이 CSV 형식일 때만 적용됩니다.

| param         | default | description                                                                 |
|:------------- |---------|:----------------------------------------------------------------------------|
| header {{< neo_since ver="8.0.33" />}} |         | `skip`: 첫 줄을 건너뜁니다.<br/>`columns`: 헤더 줄이 테이블 컬럼명과 일치합니다. |
| heading       | false   | 더 이상 사용하지 않습니다. `heading=true`는 `header=skip`과 동일합니다.      |
| delimiter     | ,       | 필드 구분자                                                                   |

CSV 데이터에 헤더 줄이 포함되어 있다면 `header=skip` 쿼리 매개변수를 설정해 첫 줄을 무시하도록 하십시오.

헤더 줄에서 사용할 컬럼을 지정하고 싶다면 `header=columns`를 사용합니다. 헤더가 테이블 컬럼명과 일치해야 하며, 내부적으로 `INSERT INTO TABLE(columns...) VALUES(...)`의 컬럼 목록으로 활용됩니다.

헤더 줄이 없고 `header` 옵션을 생략(기본값, `heading=false`와 동일)한 경우에는 각 줄의 필드가 테이블의 모든 컬럼 순서와 정확히 일치해야 합니다. 이는 `INSERT INTO TABLE VALUES(...)` 구문에 대응하기 위해서입니다.

> append 방식의 특성상 `method=append`와 함께 사용할 때는 `header=columns` 옵션이 동작하지 않습니다.

**header=skip**

`header=skip`을 지정하면 서버가 첫 줄을 무시하며, 데이터는 테이블 컬럼과 동일한 순서로 배치되어야 합니다.

```csv
NAME,TIME,VALUE
csv-data,1670380342000000000,1.0001
csv-data,1670380343000000000,2.0002
```

`Content-Type` 헤더는 `text/csv`로 지정해야 합니다.
{{< tabs items="HTTP,cURL">}}
{{< tab >}}
~~~
```http
POST http://127.0.0.1:5654/db/write/EXAMPLE?header=skip
Content-Type: text/csv

NAME,TIME,VALUE
csv-data,1670380342000000000,1.0001
csv-data,1670380343000000000,2.0002
```
~~~
{{< /tab >}}
{{< tab >}}
```sh
curl -X POST http://127.0.0.1:5654/db/write/EXAMPLE?header=skip \
    -H "Content-Type: text/csv" \
    --data-binary "@post-data.csv"
```
{{< /tab >}}
{{< /tabs >}}

**header=columns**

CSV 필드 순서가 실제 테이블 컬럼과 다르거나 일부 컬럼만 포함되어 있다면 `header=columns`를 지정합니다. 그러면 서버는 첫 줄을 컬럼명으로 처리하며, 아래 예시는 내부적으로 `INSERT INTO EXAMPLE (TIME, NAME, VALUE) VALUES(?, ?, ?)`와 동일한 구문을 생성합니다.

```csv
TIME,NAME,VALUE
1670380342000000000,csv-data,1.0001
1670380343000000000,csv-data,2.0002
```

`Content-Type` 헤더는 `text/csv`로 지정해야 합니다.

{{< tabs items="HTTP,cURL">}}
{{< tab >}}
~~~
```http
POST http://127.0.0.1:5654/db/write/EXAMPLE?header=columns
Content-Type: text/csv

TIME,NAME,VALUE
1670380342000000000,csv-data,1.0001
1670380343000000000,csv-data,2.0002
```
~~~
{{< /tab >}}
{{< tab >}}
```sh
curl -X POST http://127.0.0.1:5654/db/write/EXAMPLE?header=columns \
    -H "Content-Type: text/csv" \
    --data-binary "@post-data.csv"
```
{{< /tab >}}
{{< /tabs >}}

**압축 CSV**

입력 스트림이 gzip으로 압축되었다면 `Content-Encoding: gzip` 헤더를 설정해 machbase-neo에 알려야 합니다.

{{< tabs items="HTTP,cURL">}}
{{< tab >}}
~~~
```http
POST http://127.0.0.1:5654/db/write/EXAMPLE?header=skip
Content-Type: text/csv
Content-Encoding: gzip

< /csv/post-data.json.gz
```
~~~
{{< /tab >}}
{{< tab >}}
```sh
curl -X POST http://127.0.0.1:5654/db/write/EXAMPLE?header=skip \
    -H "Content-Type: text/csv" \
    -H "Content-Encoding: gzip" \
    --data-binary "@post-data.csv.gz"
```
{{< /tab >}}
{{< /tabs >}}


**timeformat을 사용하는 CSV**

`timeformat`과 `tz` 쿼리 매개변수를 함께 지정합니다.

~~~
```http
POST http://127.0.0.1:5654/db/write/EXAMPLE
    ?header=skip
    &timeformat=Default
    &tz=Asia/Seoul
Content-Type: text/csv

NAME,TIME,VALUE
csv-data,2022-12-07 11:39:32,1.0001
csv-data,2022-12-07 11:39:33,2.0002
```
~~~

## 예시

API의 자세한 설명은 [Request endpoint and params](/neo/api-http/write#request-endpoint-and-params)를 참고해 주십시오.

**테스트 테이블**

{{< tabs items="HTTP,cURL">}}
{{< tab >}}
~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=create tag table if not exists EXAMPLE (name varchar(40) primary key, time datetime basetime, value double)
```
~~~
{{< /tab >}}
{{< tab >}}
```sh
curl -o - http://127.0.0.1:5654/db/query \
    --data-urlencode \
    "q=create tag table EXAMPLE (name varchar(40) primary key, time datetime basetime, value double)"
```
{{< /tab >}}
{{< /tabs >}}

**Time**

이 예제에서 사용하는 샘플 파일의 시간 값은 초 단위 UNIX 에포크로 저장되어 있습니다. 따라서 데이터를 불러올 때는 `timeformat=s` 옵션을 지정해 주십시오. 다른 시간 정밀도로 저장된 데이터라면 해당 값에 맞춰 옵션을 수정해야 합니다. Machbase Neo는 기본적으로 시간 정밀도를 `나노초(ns)`로 가정하고 처리합니다.

### JSON with epoch

~~~
```http
POST http://127.0.0.1:5654/db/write/EXAMPLE
    ?timeformat=s
Content-Type: application/json

{
  "data":  {
    "columns":["NAME","TIME","VALUE"],
    "rows": [
        ["wave.sin",1676432361,0],
        ["wave.sin",1676432362,0.406736],
        ["wave.sin",1676432363,0.743144],
        ["wave.sin",1676432364,0.951056],
        ["wave.sin",1676432365,0.994522]
    ]
  }
}
```
~~~

**행 조회**

~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=select * from EXAMPLE limit 10
```
~~~

### CSV with epoch

CSV 데이터에 다음과 같이 헤더 줄이 있다면 `header=skip` 쿼리 매개변수를 지정해 주십시오.

~~~
```http
POST http://127.0.0.1:5654/db/write/EXAMPLE
    ?timeformat=s
    &header=skip
Content-Type: text/csv

NAME,TIME,VALUE
wave.sin,1676432361,0.000000
wave.cos,1676432361,1.000000
wave.sin,1676432362,0.406736
wave.cos,1676432362,0.913546
wave.sin,1676432363,0.743144

```
~~~

### 헤더 없는 CSV

~~~
```http
POST http://127.0.0.1:5654/db/write/EXAMPLE?timeformat=s
Content-Type: text/csv

wave.sin,1676432361,0.000000
wave.cos,1676432361,1.000000
wave.sin,1676432362,0.406736
wave.cos,1676432362,0.913546
wave.sin,1676432363,0.743144
```
~~~

### CSV

**Insert**

~~~
```http
POST http://127.0.0.1:5654/db/write/EXAMPLE
    ?timeformat=Default
Content-Type: text/csv

wave.sin,2023-02-15 03:39:21,0.111111
wave.sin,2023-02-15 03:39:22.111,0.222222
wave.sin,2023-02-15 03:39:23.222,0.333333
wave.sin,2023-02-15 03:39:24.333,0.444444
wave.sin,2023-02-15 03:39:25.444,0.555555
```
~~~

~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=select * from EXAMPLE limit 10
    &timeformat=Default
    &format=csv
```
~~~

**Append**

대용량 CSV 파일을 적재할 때는 “append” 방식을 사용하면 “insert” 방식보다 여러 배 빠르게 입력할 수 있습니다.

~~~
```http
POST http://127.0.0.1:5654/db/write/EXAMPLE?timeformat=s&method=append
Content-Type: text/csv

wave.sin,1676432361,0.000000
wave.cos,1676432361,1.000000
wave.sin,1676432362,0.406736
wave.cos,1676432362,0.913546
wave.sin,1676432363,0.743144
```
~~~

### 시간대를 지정한 CSV

~~~
```http
POST http://127.0.0.1:5654/db/write/EXAMPLE
    ?timeformat=Default
    &tz=Asia/Seoul
Content-Type: text/csv

wave.sin,2023-02-15 12:39:21,0.111111
wave.sin,2023-02-15 12:39:22.111,0.222222
wave.sin,2023-02-15 12:39:23.222,0.333333
wave.sin,2023-02-15 12:39:24.333,0.444444
wave.sin,2023-02-15 12:39:25.444,0.555555
```
~~~

**UTC 기준으로 조회**

~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=select * from EXAMPLE limit 10
    &timeformat=Default
    &format=csv
```
~~~

### `RFC3339`

~~~
```http
POST http://127.0.0.1:5654/db/write/EXAMPLE
    ?timeformat=RFC3339
Content-Type: text/csv

wave.sin,2023-02-15T03:39:21Z,0.111111
wave.sin,2023-02-15T03:39:22Z,0.222222
wave.sin,2023-02-15T03:39:23Z,0.333333
wave.sin,2023-02-15T03:39:24Z,0.444444
wave.sin,2023-02-15T03:39:25Z,0.555555
```
~~~

**UTC 기준으로 조회**

~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=select * from EXAMPLE limit 10
    &format=csv
    &timeformat=RFC3339
```
~~~

### 시간대를 포함한 `RFC3339Nano`

~~~
```http
POST http://127.0.0.1:5654/db/write/EXAMPLE
    ?timeformat=RFC3339Nano
    &tz=America/New_York
Content-Type: text/csv

wave.sin,2023-02-14T22:39:21.000000000-05:00,0.111111
wave.sin,2023-02-14T22:39:22.111111111-05:00,0.222222
wave.sin,2023-02-14T22:39:23.222222222-05:00,0.333333
wave.sin,2023-02-14T22:39:24.333333333-05:00,0.444444
wave.sin,2023-02-14T22:39:25.444444444-05:00,0.555555
```
~~~


**America/New_York 시간대로 조회**

~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=select * from EXAMPLE limit 10
    &format=box
    &timeformat=RFC3339Nano
    &tz=America/New_York
```
~~~

### Timeformat

~~~
```http
POST http://127.0.0.1:5654/db/write/EXAMPLE
    ?timeformat=Default
Content-Type: text/csv

wave.sin,2023-02-15 03:39:21,0.111111
wave.sin,2023-02-15 03:39:22.111111111,0.222222
wave.sin,2023-02-15 03:39:23.222222222,0.333333
wave.sin,2023-02-15 03:39:24.333333333,0.444444
wave.sin,2023-02-15 03:39:25.444444444,0.555555
```
~~~

**UTC 기준으로 조회**

~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=select * from EXAMPLE limit 10
    &format=csv
    &timeformat=Default

```
~~~

### 사용자 정의 Timeformat

- 뉴욕 시간대를 기준으로 `hour:min:sec-SPLIT-year-month-day` 형식 사용

~~~
```http
POST http://127.0.0.1:5654/db/write/EXAMPLE
    ?timeformat=03:04:05.999999999-SPLIT-2006-01-02
    &tz=America/New_York
Content-Type: text/csv

wave.sin,10:39:21-SPLIT-2023-02-14 ,0.111111
wave.sin,10:39:22.111111111-SPLIT-2023-02-14 ,0.222222
wave.sin,10:39:23.222222222-SPLIT-2023-02-14 ,0.333333
wave.sin,10:39:24.333333333-SPLIT-2023-02-14 ,0.444444
wave.sin,10:39:25.444444444-SPLIT-2023-02-14 ,0.555555
```
~~~

**행 조회**

~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=select * from EXAMPLE limit 5
    &format=csv
    &timeformat=2006-01-02 03:04:05.999999999
    &tz=America/New_York
```
~~~
