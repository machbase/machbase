---
title: HTTP 쿼리
type: docs
weight: 10
---

Query API 엔드포인트는 `/db/query`입니다.

이 API는 `SELECT`뿐 아니라 `CREATE TABLE`, `ALTER TABLE`, `INSERT` 등 모든 SQL 구문을 지원합니다.

`/db/query` API는 *GET*, *POST(JSON)*, *POST(form-data)* 요청을 모두 지원하며, 모든 방식에서 동일한 매개변수를 사용할 수 있습니다.

예를 들어 `format` 매개변수는 *GET* 방식에서 `GET /db/query?format=csv`처럼 쿼리 매개변수로 지정할 수 있고,
*POST-JSON* 방식에서는 `{ "format": "csv" }`처럼 JSON 필드로 전달할 수 있습니다.

**쿼리 예시**

{{< tabs items="HTTP,cURL">}}
{{< tab >}}
~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=select * from EXAMPLE limit 2
```
~~~
{{< /tab >}}
{{< tab >}}
```sh 
curl -o - http://127.0.0.1:5654/db/query \
     --data-urlencode "q=select * from EXAMPLE limit 2"
```
{{< /tab >}}
{{< /tabs >}}


## 매개변수

**쿼리 매개변수**

| param       | default | description                                                |
|:----------- |---------|:-----------------------------------------------------------|
| **q**       | _required_ | 실행할 SQL 구문입니다.                                     |
| format      | `json`    | 결과 데이터 형식: json, csv, box, ndjson                  |
| timeformat  | `ns`      | 시간 단위: s, ms, us, ns                                  |
| tz          | `UTC`     | 시간대: UTC, Local, 위치 지정                             |
| compress    | _no compression_   | 압축 방식: gzip                                      |
| rownum      | `false`   | 행 번호 포함 여부: true, false                            |

**`format=json`에서 사용 가능한 매개변수**

* 이 옵션들은 `format=json`일 때만 사용할 수 있으며, 요청당 하나만 선택할 수 있습니다.

| param       | default | description                                                                    |
|:----------- |---------|:-------------------------------------------------------------------------------|
| transpose   | false   | 결과를 행 대신 열 배열로 반환합니다. {{< neo_since ver="8.0.12" />}}          |
| rowsFlatten | false   | JSON 객체의 `rows` 필드 차원을 한 단계 줄입니다. {{< neo_since ver="8.0.12" />}}|
| rowsArray   | false   | 각 레코드를 객체 배열로만 구성한 JSON을 반환합니다. {{< neo_since ver="8.0.12" />}} |

**`format=csv`에서 사용 가능한 매개변수**

| param       | default | description                                                                |
|:----------- |---------|:---------------------------------------------------------------------------|
| header      |         | `skip`을 지정하면 헤더를 포함하지 않습니다. `heading=false`와 동일합니다. |
| heading     | `true`  | 헤더 표시 여부: true, false. 사용 자제, 대신 `header`를 사용하십시오.     |
| precision   | `-1`    | 부동소수점 자릿수: -1은 반올림 없음, 0은 정수로 표시                     |

**시간 형식 옵션**
 
* 사용 가능한 시간 형식은 [API Options/timeformat](../../options/timeformat/)을 참고해 주십시오.

## 출력

응답 본문이 너무 커서 전체 길이를 미리 알 수 없는 경우, `Transfer-Encoding: chunked` 헤더가 설정되고 `Content-Length` 헤더는 생략됩니다. 응답의 끝은 연속된 두 개의 줄바꿈 문자(`\n\n`)로 구분됩니다.

- `Transfer-Encoding: chunked`: 데이터를 여러 조각으로 나누어 전송하며, 스트리밍에 유용합니다.
- `Content-Length` 헤더가 없음: 응답 본문의 총 길이를 사전에 알 수 없음을 의미합니다.

### JSON

`/db/query` API의 기본 출력 형식은 JSON입니다.
쿼리 매개변수 `format=json`을 지정하거나 생략하면 기본값이 적용됩니다.

{{< tabs items="HTTP,cURL">}}
{{< tab >}}
~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=select * from EXAMPLE limit 2
```
~~~
{{< /tab >}}
{{< tab >}}
```sh
curl -o - http://127.0.0.1:5654/db/query \
    --data-urlencode "q=select * from EXAMPLE limit 2"
```
{{< /tab >}}
{{< /tabs >}}


응답은 `Content-Type: application/json`으로 전달됩니다.

| name         | type       |  description                                                                 |
|:------------ |:-----------|:-----------------------------------------------------------------------------|
| **success**  | bool       | 쿼리 실행이 성공하면 `true`                                                  |
| **reason**   | string     | 실행 결과 메시지. `success`가 `false`면 오류 메시지가 포함됩니다.            |
| **elapse**   | string     | 쿼리 실행에 소요된 시간                                                      |
| data         |            | 실행이 성공했을 때만 존재                                                    |
| data.columns | array of strings | 결과 컬럼 정보를 나타냅니다.                                          |
| data.types   | array of strings | 각 컬럼의 데이터 타입을 나타냅니다.                                   |
| data.rows    | array of records | 결과 레코드 배열입니다.<br/>`transpose=true`이면 이 필드는 `cols`로 대체됩니다. |
| data.cols    | array of series  | 결과 컬럼별 시리즈 배열입니다.<br/>`transpose=true`일 때만 존재합니다.  |

{{< tabs items="default,transpose,rowsFlatten,rowsArray">}}
{{< tab >}}
~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=select * from EXAMPLE limit 3
```
~~~

```json
{
  "data": {
    "columns": [ "NAME", "TIME", "VALUE" ],
    "types": [ "string", "datetime", "double" ],
    "rows": [
      [ "wave.sin", 1705381958775759000, 0.8563571936170834 ],
      [ "wave.sin", 1705381958785759000, 0.9011510331449053 ],
      [ "wave.sin", 1705381958795759000, 0.9379488170706388 ]
    ]
  },
  "success": true,
  "reason": "success",
  "elapse": "1.887042ms"
}
```
{{< /tab >}}
{{< tab >}}
~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=select * from EXAMPLE limit 3
    &transpose=true
```
~~~

```json
{
  "data": {
    "columns": [ "NAME", "TIME", "VALUE" ],
    "types": [ "string", "datetime", "double" ],
    "cols": [
      [ "wave.sin", "wave.sin", "wave.sin" ],
      [ 1705381958775759000, 1705381958785759000, 1705381958795759000 ],
      [ 0.8563571936170834, 0.9011510331449053, 0.9379488170706388 ]
    ]
  },
  "success": true,
  "reason": "success",
  "elapse": "4.090667ms"
}
```
{{< /tab >}}
{{< tab >}}
~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=select * from EXAMPLE limit 3
    &rowsFlatten=true
```
~~~

```json
{
  "data": {
    "columns": [ "NAME", "TIME", "VALUE" ],
    "types": [ "string", "datetime", "double" ],
    "rows": [
      "wave.sin", 1705381958775759000, 0.8563571936170834,
      "wave.sin", 1705381958785759000, 0.9011510331449053,
      "wave.sin", 1705381958795759000, 0.9379488170706388
    ]
  },
  "success": true,
  "reason": "success",
  "elapse": "2.255625ms"
}
```
{{< /tab >}}
{{< tab >}}
~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=select * from EXAMPLE limit 3
    &rowsArray=true
```
~~~

```json
{
  "data": {
    "columns": [ "NAME", "TIME", "VALUE" ],
    "types": [ "string", "datetime", "double" ],
    "rows": [
      { "NAME": "wave.sin", "TIME": 1705381958775759000, "VALUE": 0.8563571936170834 },
      { "NAME": "wave.sin", "TIME": 1705381958785759000, "VALUE": 0.9011510331449053 },
      { "NAME": "wave.sin", "TIME": 1705381958795759000, "VALUE": 0.9379488170706388 }
    ]
  },
  "success": true,
  "reason": "success",
  "elapse": "3.178458ms"
}
```
{{< /tab >}}
{{< /tabs >}}

### NDJSON

요청에 `format=ndjson` 쿼리 매개변수를 지정하십시오. {{< neo_since ver="8.0.33" />}}

NDJSON(Newline Delimited JSON)은 각 줄이 유효한 JSON 객체인 스트리밍 형식입니다. 한 번에 하나씩 처리할 수 있어 대규모 데이터나 스트리밍 데이터를 다룰 때 유용합니다.

{{< tabs items="HTTP,cURL">}}
{{< tab >}}
~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=select * from EXAMPLE limit 2
    &format=ndjson
```
~~~
{{< /tab >}}
{{< tab >}}
```sh
curl -o - http://127.0.0.1:5654/db/query \
    --data-urlencode "q=select * from EXAMPLE limit 2" \
    --data-urlencode "format=ndjson"
```
{{< /tab >}}
{{< /tabs >}}

응답의 `Content-Type`은 `application/x-ndjson`입니다.

```json
{"NAME":"wave.sin","TIME":1705381958775759000,"VALUE":0.8563571936170834}
{"NAME":"wave.sin","TIME":1705381958785759000,"VALUE":0.9011510331449053}

```

### CSV

요청에 `format=csv` 쿼리 매개변수를 지정하십시오.

CSV 형식 역시 한 줄씩 처리할 수 있어 대용량 데이터나 스트리밍 데이터 처리에 적합합니다.

{{< tabs items="HTTP,cURL">}}
{{< tab >}}
~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=select * from EXAMPLE limit 2
    &format=csv
```
~~~
{{< /tab >}}
{{< tab >}}
```sh
curl -o - http://127.0.0.1:5654/db/query \
    --data-urlencode "q=select * from EXAMPLE limit 2" \
    --data-urlencode "format=csv"
```
{{< /tab >}}
{{< /tabs >}}

응답의 `Content-Type`은 `text/csv; utf-8`입니다.

```csv
NAME,TIME,VALUE
wave.sin,1705381958775759000,0.8563571936170834
wave.sin,1705381958785759000,0.9011510331449053
```

### BOX

요청에 `format=box` 쿼리 매개변수를 지정하십시오.

{{< tabs items="HTTP,cURL">}}
{{< tab >}}
~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=select * from EXAMPLE limit 2
    &format=box
```
~~~
{{< /tab >}}
{{< tab >}}
```sh
curl -o - http://127.0.0.1:5654/db/query \
    --data-urlencode "q=select * from EXAMPLE limit 2" \
    --data-urlencode "format=box"
```
{{< /tab >}}
{{< /tabs >}}

결과는 ASCII 박스로 표현된 일반 텍스트 형식이며, 응답의 `Content-Type`은 `plain/text`입니다.

```
+----------+---------------------+--------------------+
| NAME     | TIME(UTC)           | VALUE              |
+----------+---------------------+--------------------+
| wave.sin | 1705381958775759000 | 0.8563571936170834 |
| wave.sin | 1705381958785759000 | 0.9011510331449053 |
+----------+---------------------+--------------------+
```

**CSV 형식 응답**

요청에 `format=csv` 쿼리 매개변수를 지정하십시오.

{{< tabs items="HTTP,cURL">}}
{{< tab >}}
~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=select * from EXAMPLE limit 2
    &format=csv
```
~~~
{{< /tab >}}
{{< tab >}}
```sh
curl -o - http://127.0.0.1:5654/db/query \
    --data-urlencode "q=select * from EXAMPLE limit 2" \
    --data-urlencode "format=csv"
```
{{< /tab >}}
{{< /tabs >}}

응답의 `Content-Type`은 `text/csv`입니다.

```csv
NAME,TIME,VALUE
wave.sin,1705381958775759000,0.8563571936170834
wave.sin,1705381958785759000,0.9011510331449053
```

## POST JSON

아래 예시처럼 JSON 형식으로 쿼리를 요청할 수도 있습니다.

**요청 JSON 메시지**

{{< tabs items="HTTP,cURL">}}
{{< tab >}}
~~~
```http
POST http://127.0.0.1:5654/db/query
Content-Type: application/json

{
  "q": "select * from EXAMPLE limit 2"
}
```
~~~
{{< /tab >}}
{{< tab >}}
```sh
curl -o - -X POST http://127.0.0.1:5654/db/query \
    -H 'Content-Type: application/json' \
    -d '{ "q":"select * from EXAMPLE limit 2" }'
```
{{< /tab >}}
{{< /tabs >}}

## POST Form

HTML 폼 데이터 형식도 사용할 수 있습니다. 이 경우 HTTP 헤더 `Content-Type`을 `application/x-www-form-urlencoded`로 설정해야 합니다.

{{< tabs items="HTTP,cURL">}}
{{< tab >}}
~~~
```http
POST http://127.0.0.1:5654/db/query
Content-Type: application/x-www-form-urlencoded

q=select * from EXAMPLE limit 2
```
~~~
{{< /tab >}}
{{< tab >}}
```sh
curl -o - -X POST http://127.0.0.1:5654/db/query \
    --data-urlencode "q=select * from EXAMPLE limit 2"
```
{{< /tab >}}
{{< /tabs >}}

## Examples

Please refer to the detail of the API 
- [Request endpoint and params](/neo/api-http/query)
- [List of Time Zones from wikipedia.org](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)

For this tutorials, pre-write data below.

{{% steps %}}

### Create Table

~~~
```http
POST http://127.0.0.1:5654/db/query
Content-Type: application/json

{
  "q":"create tag table if not exists EXAMPLE (name varchar(40) primary key, time datetime basetime, value double)"
}
```
~~~

### Insert Table

~~~
```http
POST http://127.0.0.1:5654/db/write/EXAMPLE?timeformat=ns
Content-Type: application/json

{
    "data":{
      "columns":["NAME","TIME","VALUE"],
      "rows":[
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

{{% /steps %}}

### Select in CSV

**Request**

Set the `format=csv` query param for CSV format.

~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=select * from EXAMPLE limit 5
    &format=csv
```
~~~

**Response**
```
NAME,TIME,VALUE
wave.sin,1676432361000000000,0.111111
wave.sin,1676432362111111111,0.222222
wave.sin,1676432363222222222,0.333333
wave.sin,1676432364333333333,0.444444
wave.sin,1676432365444444444,0.555555
```

### Select in BOX

**Request**

Set the `format=box` query param for BOX format.

~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=select * from EXAMPLE limit 5
    &format=box
```
~~~

**Response**

```
+----------+---------------------+----------+
| NAME     | TIME                | VALUE    |
+----------+---------------------+----------+
| wave.sin | 1676432361000000000 | 0        |
| wave.sin | 1676432362111111111 | 0.406736 |
| wave.sin | 1676432363222222222 | 0.743144 |
| wave.sin | 1676432364333333333 | 0.951056 |
| wave.sin | 1676432365444444444 | 0.994522 |
+----------+---------------------+----------+
```

### Select in BOX with rownum

**Request**

Set the `format=box` query param for BOX format.

~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=select * from EXAMPLE limit 5
    &format=box
    &rownum=true
```
~~~

**Response**

```
+--------+----------+---------------------+----------+
| ROWNUM | NAME     | TIME                | VALUE    |
+--------+----------+---------------------+----------+
|      1 | wave.sin | 1676432361000000000 | 0.111111 |
|      2 | wave.sin | 1676432362111111111 | 0.222222 |
|      3 | wave.sin | 1676432363222222222 | 0.333333 |
|      4 | wave.sin | 1676432364333333333 | 0.444444 |
|      5 | wave.sin | 1676432365444444444 | 0.555555 |
+--------+----------+---------------------+----------+
```


### Select in BOX without heading

**Request**

Set the `format=box` and `header=skip` query param for BOX format without header.

~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=select * from EXAMPLE limit 5
    &format=box
    &header=skip
```
~~~

**Response**

```
+----------+---------------------+----------+
| wave.sin | 1676432361000000000 | 0        |
| wave.sin | 1676432362111111111 | 0.406736 |
| wave.sin | 1676432363222222222 | 0.743144 |
| wave.sin | 1676432364333333333 | 0.951056 |
| wave.sin | 1676432365444444444 | 0.994522 |
+----------+---------------------+----------+
```

### Select in BOX value in INTEGER

**Request**

Set the `format=box` and `precision=0` query param for BOX format with integer precision.

~~~
```http
GET http://127.0.0.1:5654/db/query
    ?q=select * from EXAMPLE limit 5
    &format=box
    &precision=0
```
~~~

**Response**

```
+----------+---------------------+-------+
| NAME     | TIME                | VALUE |
+----------+---------------------+-------+
| wave.sin | 1676432361000000000 | 0     |
| wave.sin | 1676432362111111111 | 0     |
| wave.sin | 1676432363222222322 | 0     |
| wave.sin | 1676432364333333233 | 0     |
| wave.sin | 1676432365444444444 | 1     |
+----------+---------------------+-------+
```
