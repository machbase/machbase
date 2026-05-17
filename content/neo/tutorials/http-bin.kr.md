---
title: HTTP Binary 컬럼 튜토리얼
type: docs
weight: 35
---

{{< callout emoji="📌">}}
이 튜토리얼은 HTTP `write` API와 `query` API를 통해 `binary` 컬럼을 저장하고 조회하는 방법을 설명합니다.
{{< /callout >}}

{{< neo_since ver="8.5.2" />}}

## 예제 테이블 생성

```sql
CREATE TAG TABLE IF NOT EXISTS example (
  name varchar(100) primary key,
  time datetime basetime,
  value double,
  bindata binary
);
```

HTTP API에서 `binary` 컬럼은 문자열로 표현합니다. 쓰기 API는 입력 문자열의 형태로 인코딩을 판별하고, 조회 API는 `binaryformat` 파라미터로 출력 형식을 선택합니다.

## Binary 문자열 규칙

쓰기 API에서 `binary` 컬럼에 문자열을 전달하면 다음 규칙으로 디코딩합니다.

| 입력 문자열 | 의미 |
| --- | --- |
| `0x0102` | `0x` 또는 `0X` 접두어가 있으므로 hex 문자열로 디코딩합니다. |
| `AQI=` | `0x` 접두어가 없으므로 표준 base64 문자열로 디코딩합니다. |

조회 API의 기본 출력은 hex 문자열입니다.

| `binaryformat` | 출력 예시 | 설명 |
| --- | --- | --- |
| 생략 또는 `hex` | `0x0102` | 전체 바이트를 hex 문자열로 출력합니다. |
| `base64` | `AQI=` | 표준 base64 문자열로 출력합니다. |
| `bytes` | `[1 2]` | 바이트 값을 10진수 배열 형태로 출력합니다. |
| `preview` | `0x0102030405..` | 앞부분만 hex 문자열로 출력합니다. 긴 값 확인용입니다. |

아래 예시에서는 다음 값을 사용합니다.

- `0x0102` 와 `AQI=` 는 같은 바이트 값입니다.
- `0x0304` 와 `AwQ=` 는 같은 바이트 값입니다.

## JSON으로 binary 데이터 입력

이 예시는 HTTP Write API를 `method=insert`로 사용합니다. JSON 입력에서는 hex 문자열과 base64 문자열을 모두 사용할 수 있습니다.

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
      ["json-hex", 1713675600, 1.23, "0x0102"],
      ["json-base64", 1713675601, 2.34, "AwQ="]
    ]
  }
}
```
~~~

## CSV로 binary 데이터 입력

이 예시는 HTTP Write API를 `method=append`로 사용합니다. CSV 입력에서도 `binary` 컬럼 값은 문자열이며, `0x` 접두어가 있으면 hex로, 없으면 base64로 디코딩됩니다.

~~~
```http
POST http://127.0.0.1:5654/db/write/example
  ?timeformat=s
  &method=append
  &header=columns
Content-Type: text/csv

name,time,value,bindata
csv-hex,1713675610,10.5,0x0102
csv-base64,1713675611,20.5,AwQ=
```
~~~

## 기본 형식으로 데이터 조회

Query API에서 `format=json`을 사용합니다. `binaryformat`을 생략하면 `bindata` 컬럼은 hex 문자열로 반환됩니다.

~~~
```http
GET http://127.0.0.1:5654/db/query
  ?q=select name,time,value,bindata from example where name in ('json-hex','json-base64','csv-hex','csv-base64')
  &timeformat=s
  &format=json
```
~~~

```json
{
  "data": {
    "rows": [
      ["json-hex", 1713675600, 1.23, "0x0102"],
      ["json-base64", 1713675601, 2.34, "0x0304"],
      ["csv-hex", 1713675610, 10.5, "0x0102"],
      ["csv-base64", 1713675611, 20.5, "0x0304"]
    ]
  }
}
```

## Base64 형식으로 데이터 조회

base64 문자열로 응답을 받고 싶으면 `binaryformat=base64`를 지정합니다. 같은 옵션은 `format=csv`, `format=ndjson`, `format=box`에도 적용됩니다.

~~~
```http
GET http://127.0.0.1:5654/db/query
  ?q=select name,time,value,bindata from example where name in ('json-hex','json-base64','csv-hex','csv-base64')
  &timeformat=s
  &format=csv
  &binaryformat=base64
```
~~~

```csv
NAME,TIME,VALUE,BINDATA
json-hex,1713675600,1.23,AQI=
json-base64,1713675601,2.34,AwQ=
csv-hex,1713675610,10.5,AQI=
csv-base64,1713675611,20.5,AwQ=
```
