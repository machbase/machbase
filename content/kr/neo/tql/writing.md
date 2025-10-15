---
title: As Writing API
type: docs
weight: 04
---

{{< callout type="info" >}}
아래 예제를 실행하기 전에 다음 SQL로 테이블을 준비해 주십시오.
{{< /callout >}}

```sql
CREATE TAG TABLE IF NOT EXISTS EXAMPLE (
    NAME VARCHAR(20) PRIMARY KEY,
    TIME DATETIME BASETIME,
    VALUE DOUBLE SUMMARIZED
);
```

## `INSERT` CSV

### 1. TQL 파일 생성

다음 코드를 `input-csv.tql`로 저장해 주십시오.  
TQL 스크립트를 저장하면 편집기 우측 상단에 <img src="/images/copy_addr_icon.jpg" width="24px" style="display:inline"> 아이콘이 나타납니다. 클릭하면 스크립트 주소를 복사할 수 있습니다.

```js {linenos=table,hl_lines=["7"]}
CSV(payload(), 
    field(0, stringType(), 'name'),
    field(1, timeType('ns'), 'time'),
    field(2, floatType(), 'value'),
    header(false)
)
INSERT("name", "time", "value", table("example"))
```

### 2. HTTP POST

{{< tabs items="HTTP,cURL">}}
{{< tab >}}

~~~
```http
POST http://127.0.0.1:5654/db/tql/input-csv.tql
Content-Type: text/csv

TAG0,1628866800000000000,12
TAG0,1628953200000000000,13
```
~~~

{{< /tab >}}
{{< tab >}}

`input-csv.csv` 파일을 준비해 주십시오.

```csv
TAG0,1628866800000000000,12
TAG0,1628953200000000000,13
```

이후 `curl`로 `input-csv.tql`을 호출합니다.

```sh
curl -X POST http://127.0.0.1:5654/db/tql/input-csv.tql \
    -H "Content-Type: text/csv" \
    --data-binary "@input-csv.csv"
```
{{< /tab >}}
{{< /tabs >}}

### 3. MQTT PUBLISH

`input-csv.csv` 파일을 아래처럼 준비해 주십시오.

```csv
TAG1,1628866800000000000,12
TAG1,1628953200000000000,13
```

```sh
mosquitto_pub -h 127.0.0.1 -p 5653 \
    -t db/tql/input-csv.tql \
    -f input-csv.csv
```

## `APPEND` CSV

### 1. TQL 파일 생성

다음 코드를 `append-csv.tql`로 저장해 주십시오.

```js {linenos=table,hl_lines=["7"]}
CSV(payload(), 
    field(0, stringType(), 'name'),
    field(1, timeType('ns'), 'time'),
    field(2, floatType(), 'value'),
    header(false)
)
APPEND(table('example'))
```

### 2. HTTP POST

{{< tabs items="HTTP,cURL">}}
{{< tab >}}

~~~
```http
POST http://127.0.0.1:5654/db/tql/append-csv.tql
Content-Type: text/csv

TAG0,1628866800000000000,12
TAG0,1628953200000000000,13
```
~~~

{{< /tab >}}
{{< tab >}}

`append-csv.csv` 파일을 준비해 주십시오.

```csv
TAG2,1628866800000000000,12
TAG2,1628953200000000000,13
```

`curl`로 `append-csv.tql`을 호출합니다.

```sh
curl -X POST http://127.0.0.1:5654/db/tql/append-csv.tql \
    -H "Content-Type: text/csv" \
    --data-binary "@append-csv.csv"
```
{{< /tab >}}
{{< /tabs >}}

### 3. MQTT PUBLISH

`append-csv.csv` 파일을 아래처럼 준비해 주십시오.

```csv
TAG3,1628866800000000000,12
TAG3,1628953200000000000,13
```

```sh
mosquitto_pub -h 127.0.0.1 -p 5653 \
    -t db/tql/input-csv.tql \
    -f append-csv.csv
```

## 커스텀 JSON

### 1. TQL 파일 생성

`SCRIPT()` 함수를 이용해 커스텀 JSON을 파싱합니다.  
다음 코드를 `input-json.tql`로 저장해 주십시오.

```js {linenos=table}
SCRIPT({
    obj = JSON.parse($.payload)
    obj.data.rows.forEach(r => $.yield(...r))
})
INSERT("name", "time", "value", table("example"))
```

### 2. HTTP POST

{{< tabs items="HTTP,cURL">}}
{{< tab >}}

~~~
```http
POST http://127.0.0.1:5654/db/tql/input-json.tql
Content-Type: application/json

{
  "data": {
    "columns": [ "NAME", "TIME", "VALUE" ],
    "types": [ "string", "datetime", "double" ],
    "rows": [
      [ "TAG0", 1628866800000000000, 12 ],
      [ "TAG0", 1628953200000000000, 13 ]
    ]
  }
}
```
~~~

{{< /tab >}}
{{< tab >}}

`input-json.json` 파일을 준비해 주십시오.

```json
{
  "data": {
    "columns": [ "NAME", "TIME", "VALUE" ],
    "types": [ "string", "datetime", "double" ],
    "rows": [
      [ "TAG0", 1628866800000000000, 12 ],
      [ "TAG0", 1628953200000000000, 13 ]
    ]
  }
}
```

다음 명령으로 업로드합니다.

```sh
curl -X POST http://127.0.0.1:5654/db/tql/input-json.tql \
    -H "Content-Type: application/json" \
    --data-binary "@input-json.json"
```
{{< /tab >}}
{{< /tabs >}}

### 3. MQTT PUBLISH

`input-json.json` 파일을 아래처럼 준비해 주십시오.

```json
{
  "data": {
    "columns": [ "NAME", "TIME", "VALUE" ],
    "types": [ "string", "datetime", "double" ],
    "rows": [
      [ "TAG1", 1628866800000000000, 12 ],
      [ "TAG1", 1628953200000000000, 13 ]
    ]
  }
}
```

```sh
mosquitto_pub -h 127.0.0.1 -p 5653 \
    -t db/tql/input-json.tql \
    -f input-json.json
```

## 커스텀 텍스트

데이터를 가공한 뒤 데이터베이스에 저장해야 한다면, 적절한 *tql* 스크립트를 준비해 `db/tql/{tql_file.tql}` 토픽으로 전송해 주십시오.

### 1. TQL 파일 생성

다음 예시는 여러 줄의 텍스트 데이터를 가공해 테이블에 쓰는 방법을 보여 줍니다.

{{< tabs items="MAP,SCRIPT">}}
{{< tab >}}
MAP 함수를 사용한 변환 예시입니다.

```js {linenos=table,hl_lines=["13-15"],linenostart=1}
// payload()는 HTTP POST 또는 MQTT로 전달된 데이터를 반환합니다.
// ?? 연산자는 내용이 없을 때 오른쪽 값을 사용합니다.
// 웹 UI 편집기에서 테스트할 때 유용합니다.
STRING( payload() ?? ` 12345
                     23456
                     78901
                     89012
                     90123
                  `, separator('\n'), trimspace(true))
FILTER( len(value(0)) > 0 )   // 빈 줄 제거
// 데이터 변환
MAPVALUE(-1, time("now"))     // PUSHVALUE(0, time("now"))와 동일
MAPVALUE(-1, "text_"+key())   // PUSHVALUE(0, "text_"+key())와 동일
MAPVALUE(2, strSub( value(2), 0, 2 ) )

// 테스트 시 CSV 출력
CSV( timeformat("DEFAULT") )
// 실사용 시 아래 주석을 해제하십시오.
// APPEND(table('example'))
```
{{< /tab >}}
{{< tab >}}
`SCRIPT()`를 이용한 대안입니다.

```js {linenos=table,hl_lines=["13-18"],linenostart=1}
// payload()는 HTTP POST 또는 MQTT로 전달된 데이터를 반환합니다.
// ?? 연산자는 내용이 없을 때 오른쪽 값을 사용합니다.
// 웹 UI 편집기에서 테스트할 때 유용합니다.
STRING( payload() ?? ` 12345
                     23456
                     78901
                     89012
                     90123
                  `, separator('\n'), trimspace(true) )
FILTER( len(value(0)) > 0) // 빈 줄 제거
// 데이터 변환
SCRIPT({
  str = $.values[0].trim();   // 공백 제거
  str = str.substring(0, 2);  // 앞 두 글자만 사용
  ts = (new Date()).getTime() * 1000000 // ms → ns
  $.yieldKey("text_"+$.key, ts, parseInt(str))
})
CSV()
// APPEND(table('example'))
```
{{< /tab >}}
{{< /tabs >}}

**결과 예시**

```csv
text_1,2023-12-02 11:03:36.054,12
text_2,2023-12-02 11:03:36.054,23
text_3,2023-12-02 11:03:36.054,78
text_4,2023-12-02 11:03:36.054,89
text_5,2023-12-02 11:03:36.054,90
```

위 코드를 실행해 문제가 없다면 마지막 줄의 `CSV()`를 `APPEND(table('example'))`로 바꾸어 배포해 주십시오.

스크립트를 `script-post-lines.tql`로 저장하고, 테스트 데이터를 `db/tql/script-post-lines.tql` 토픽으로 전송합니다.

- `lines.txt` 예시

```
110000
221111
332222
442222
```

### 2. HTTP POST

동일한 TQL 파일은 HTTP POST 요청과 함께 사용할 수도 있습니다.

```sh
curl -H "Content-Type: text/plain" \
    --data-binary @lines.txt \
    http://127.0.0.1:5654/db/tql/script-post-lines.tql
```

### 3. MQTT PUBLISH

```sh
mosquitto_pub -h 127.0.0.1 -p 5653 \
    -t db/tql/script-post-lines.tql \
    -f lines.txt
```

이후 데이터가 정상적으로 변환·저장되었는지 확인합니다.

```sh
$ machbase-neo shell "select * from example where name like 'text_%'"
 ROW\NUM  NAME    TIME(LOCAL)              VALUE     
────────────────────────────────────────────────────
      1  text_3  2023-07-14 08:51:10.926  44.000000 
      2  text_0  2023-07-14 08:51:10.925  11.000000 
      3  text_1  2023-07-14 08:51:10.926  22.000000 
      4  text_2  2023-07-14 08:51:10.926  33.000000 
4 rows fetched.
```
