---
title: HTTP Binary 컬럼 튜토리얼
type: docs
weight: 35
---

{{< callout emoji="📌">}}
이 튜토리얼은 HTTP `write` API와 `query` API를 통해 `binary` 컬럼을 저장하고 조회하는 방법을 설명합니다.
{{< /callout >}}

{{< neo_since ver="8.5.0" />}}

## 예제 테이블 생성

```sql
CREATE TAG TABLE IF NOT EXISTS example (
  name varchar(100) primary key,
  time datetime basetime,
  value double,
  bindata binary
);
```

HTTP API에서 `bindata` 컬럼은 요청 형식과 응답 형식에 따라 표현 방식이 다릅니다.

- JSON으로 입력할 때는 binary 값을 base64 문자열로 전달합니다.
- CSV로 입력할 때도 `bindata` 필드에 base64 문자열을 넣습니다.
- JSON으로 조회하면 binary 값이 base64 문자열로 반환됩니다.
- CSV로 조회하면 binary 값이 base64 문자열로 반환됩니다.

아래 예시에서는 다음 값을 사용합니다.

- `AQI=` 는 바이트 `0x01 0x02` 를 의미합니다.
- `AwQ=` 는 바이트 `0x03 0x04` 를 의미합니다.

## JSON으로 binary 데이터 입력

이 예시는 HTTP Write API를 `method=insert`로 사용하는 방법입니다.

~~~
```http
POST http://127.0.0.1:5654/db/write/example
  ?timeformat=s
  &method=insert
Content-Type: application/json

{
  "data": {
    "columns": ["name", "time", "value", "bindata"],
    "rows": [
      ["json-insert", 1713675600, 1.23, "AQI="],
      ["json-insert", 1713675601, 2.34, "AwQ="]
    ]
  }
}
```
~~~

## CSV로 binary 데이터 입력

이 예시는 HTTP Write API를 `method=append`로 사용하는 방법입니다.

CSV 입력에서도 `bindata` 필드는 base64 문자열이어야 합니다.

~~~
```http
POST http://127.0.0.1:5654/db/write/example
  ?timeformat=s
  &method=append
  &header=columns
Content-Type: text/csv

name,time,value,bindata
csv-append,1713675610,10.5,AQI=
csv-append,1713675611,20.5,AwQ=
```
~~~

## JSON으로 데이터 조회

Query API에서 `format=json`을 사용합니다.

~~~
```http
GET http://127.0.0.1:5654/db/query
  ?q=select name,time,value,bindata from example where name in ('json-insert','csv-append')
  &timeformat=s
  &format=json
```
~~~

JSON 응답에서는 `bindata` 컬럼이 base64 문자열로 반환됩니다.

```json
{
  "data": {
    "rows": [
      ["json-insert", 1713675600, 1.23, "AQI="],
      ["json-insert", 1713675601, 2.34, "AwQ="],
      ["csv-append", 1713675610, 10.5, "AQI="],
      ["csv-append", 1713675611, 20.5, "AwQ="]
    ]
  }
}
```

## CSV로 데이터 조회

Query API에서 `format=csv`를 사용합니다.

~~~
```http
GET http://127.0.0.1:5654/db/query
  ?q=select name,time,value,bindata from example where name in ('json-insert','csv-append')
  &timeformat=s
  &format=csv
```
~~~

CSV 응답에서는 `bindata` 컬럼이 `0x` 접두어가 붙은 16진수 문자열로 반환됩니다.

```csv
NAME,TIME,VALUE,BINDATA
json-insert,1713675600,1.23,AQI=
json-insert,1713675601,2.34,AwQ=
csv-append,1713675610,10.5,AQI=
csv-append,1713675611,20.5,AwQ=
```
