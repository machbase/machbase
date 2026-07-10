---
type: docs
title: '11.4 REST API 연동'
weight: 40
toc: true
---
별도 드라이버 설치 없이 `curl`, Python `requests`, JavaScript `fetch` 등 HTTP 클라이언트만으로 SQL 실행과 Append 삽입을 수행할 수 있습니다.

## REST API 포트

REST API는 DB 연결 포트와 별도의 HTTP 포트를 사용합니다.

| 포트 | 용도 |
|------|------|
| 5656 | ODBC/JDBC/네이티브 드라이버 연결 |
| 5657 | REST API (HTTP) |

기본 URL은 다음과 같습니다.

```text
http://<host>:5657
```

로컬 서버에 접속하는 경우 기본 URL은 `http://127.0.0.1:5657`입니다.

## 주요 API 엔드포인트

현재 Machbase REST 샘플과 서버에서 확인되는 기본 엔드포인트는 다음과 같습니다.

| 엔드포인트 | 메서드 | 설명 |
|-----------|--------|------|
| `/machbase?q=<SQL>` | GET | SQL 실행 및 결과 반환 |
| `/machbase` | POST | JSON 본문으로 여러 행 Append 삽입 |

컬럼 목록과 TAG 데이터 조회는 별도 REST 엔드포인트가 아니라 `/machbase` SQL 실행
API로 `DESC <table>` 또는 TAG 테이블 조회 SQL을 실행합니다.

## 빠른 시작 예제

```bash
curl -G "http://127.0.0.1:5657/machbase" \
  --data-urlencode "q=SELECT 1"
```

응답 예시:

```json
{
  "error_code": 0,
  "error_message": "",
  "columns": [
    {"name": "1", "type": 8, "length": 11}
  ],
  "data": [
    {"1": 1}
  ],
  "timezone": "+0900"
}
```

## 이 섹션의 구성

| 문서 | 내용 |
|------|------|
| [공통 설정](/dbms/application-integration/rest-api/#common-authentication-timezone-rest-api) | HTTP 포트, 인증 설정, 요청 헤더 |
| [SQL REST API](/dbms/application-integration/rest-api/#machbase-sql-rest-api) | `/machbase` GET SQL 실행 |
| [Append REST API](/dbms/application-integration/rest-api/#machbase-append-rest-api) | `/machbase` POST Append 삽입 |
| [TAG 조회](/dbms/application-integration/rest-api/#machiot-tags-tag-rest-api) | TAG 테이블을 SQL REST API로 조회하는 방법 |
| [오류 처리](/dbms/application-integration/rest-api/#error-handling-rest-api) | `error_code`, HTTP 상태 코드, 재시도 전략 |

## REST API vs 드라이버 연결

| 항목 | REST API | 드라이버 (ODBC/JDBC 등) |
|------|----------|-------------------------|
| 설치 | 불필요 | 드라이버 설치 필요 |
| 언어 | 모든 언어 | 해당 언어/런타임 |
| 연결 방식 | HTTP 요청 | TCP 연결 |
| SQL 실행 | `/machbase?q=<SQL>` | 드라이버 API |
| 대량 삽입 | `/machbase` POST Append | 네이티브 Append API |
| 트랜잭션 | HTTP 요청 단위 실행 | RDB 테이블에서 트랜잭션 사용 가능 |

REST API는 간단한 통합, 웹 서비스, 언어 독립 환경에 적합합니다. 초고성능 수집이나
세밀한 연결 제어가 필요한 경우에는 네이티브 드라이버의 Append API를 사용합니다.


<a id="common-authentication-timezone-rest-api"></a>

## REST API 공통 설정

### HTTP 포트

REST API는 `machbase.conf`의 HTTP 설정을 사용합니다. 기본 샘플 설정의 값은 다음과 같습니다.

```text
HTTP_ENABLE = 1
HTTP_PORT_NO = 5657
HTTP_AUTH = 0
```

`HTTP_ENABLE`이 `1`이면 REST API 서비스가 활성화됩니다. `HTTP_PORT_NO`는 REST API가
수신하는 포트입니다.

### 인증

기본 샘플 설정의 `HTTP_AUTH = 0` 상태에서는 REST API 요청에 별도 인증 헤더가 필요하지
않습니다.

```bash
curl -G "http://127.0.0.1:5657/machbase" \
  --data-urlencode "q=SELECT 1"
```

`machbase.conf` 샘플 파일에는 `HTTP_AUTH`가 "REST API 서비스의 Basic Authentication
활성화" 항목으로 제공됩니다. 운영 환경에서 HTTP 인증을 활성화하는 경우 배포 환경의
인증 정책에 맞게 Basic Authentication 설정과 계정을 확인한 뒤 클라이언트에
`Authorization` 헤더를 추가합니다.

```bash
curl -u "SYS:MANAGER" \
  -G "http://127.0.0.1:5657/machbase" \
  --data-urlencode "q=SELECT 1"
```

현재 REST 샘플과 서버 검증 기준으로 별도 로그인 토큰 발급 API나 Bearer 토큰 방식은
사용하지 않습니다.

### Content-Type

요청 본문이 있는 Append 요청은 JSON 본문을 사용하므로 `Content-Type:
application/json` 헤더를 지정합니다.

```bash
curl -X POST "http://127.0.0.1:5657/machbase" \
  -H "Content-Type: application/json" \
  -d '{"name":"curl_sample","values":[[1,"aaa"]]}'
```

SQL 실행처럼 본문이 없는 GET 요청에는 `Content-Type` 헤더가 필요하지 않습니다.

### 타임존

REST SQL 응답에는 `timezone` 필드가 포함됩니다.

```json
{
  "error_code": 0,
  "error_message": "",
  "data": [
    {"NOW": "2026-07-07 12:00:00 000:000:000"}
  ],
  "timezone": "+0000"
}
```

시간 조건을 작성할 때는 Machbase SQL의 `DATETIME`, `NOW`, `SYSDATE`,
`TO_DATE`, `TO_CHAR` 함수와 나노초 단위 시간 연산을 사용합니다.

```bash
curl -G "http://127.0.0.1:5657/machbase" \
  --data-urlencode "q=SELECT TO_CHAR(NOW, 'YYYY-MM-DD HH24:MI:SS') AS now_text"
```

클라이언트가 특정 지역 시간 문자열을 표시해야 하는 경우에는 SQL에서
`TO_CHAR`로 원하는 문자열을 만들거나 애플리케이션에서 응답 값을 변환합니다.

### 공통 헤더 요약

| 헤더 | 필수 여부 | 설명 |
|------|-----------|------|
| `Content-Type: application/json` | POST Append 요청에서 필수 | JSON 본문 파싱 |
| `Authorization` | `HTTP_AUTH` 활성화 시 필요 | Basic Authentication 설정에 맞게 지정 |

### Python 예제

```python
import requests

BASE_URL = "http://127.0.0.1:5657"

def query(sql):
    resp = requests.get(f"{BASE_URL}/machbase", params={"q": sql}, timeout=10)
    resp.raise_for_status()
    result = resp.json()
    if result.get("error_code") != 0:
        raise RuntimeError(result.get("error_message"))
    return result

print(query("SELECT 1"))
```

<a id="machbase-sql-rest-api"></a>

## /machbase SQL REST API

HTTP GET 요청의 `q` 파라미터로 SQL 문을 전달하면 실행 결과를 JSON으로 받을 수 있습니다.
`SELECT`, `INSERT`, `CREATE TABLE`, `DROP TABLE` 등 Machbase에서 지원하는 SQL을
요청 단위로 실행합니다.

### 엔드포인트

```text
GET /machbase?q=<SQL>
```

SQL은 URL 인코딩해야 합니다. `curl`에서는 `-G`와 `--data-urlencode` 옵션을 사용하면
공백과 따옴표를 안전하게 전달할 수 있습니다.

```bash
curl -G "http://127.0.0.1:5657/machbase" \
  --data-urlencode "q=SELECT 1"
```

### 응답 형식

성공한 `SELECT` 응답은 다음 필드를 포함합니다.

```json
{
  "error_code": 0,
  "error_message": "",
  "columns": [
    {"name": "C1", "type": 8, "length": 11},
    {"name": "C2", "type": 5, "length": 20}
  ],
  "data": [
    {"C1": 1, "C2": "aaa"},
    {"C1": 2, "C2": "bbb"}
  ],
  "timezone": "+0900"
}
```

| 필드 | 설명 |
|------|------|
| `error_code` | `0`이면 성공, `0`이 아니면 오류 |
| `error_message` | 오류 메시지. 성공 시 빈 문자열 |
| `columns` | 컬럼 이름, 내부 타입, 길이 정보 |
| `data` | 결과 행. 각 행은 컬럼명을 키로 갖는 JSON 객체 |
| `timezone` | 응답에 적용된 타임존 오프셋 |

DDL이나 DML처럼 결과 행이 없는 SQL도 `error_code`가 `0`이면 성공입니다. 이때
`effect_rows`가 함께 반환될 수 있습니다.

```json
{
  "error_code": 0,
  "error_message": "No Error",
  "timezone": "+0900",
  "effect_rows": "0",
  "data": []
}
```

### SELECT 예제

```bash
curl -G "http://127.0.0.1:5657/machbase" \
  --data-urlencode "q=SELECT C1, C2 FROM curl_sample ORDER BY C1"
```

응답:

```json
{
  "error_code": 0,
  "error_message": "",
  "columns": [
    {"name": "C1", "type": 8, "length": 11},
    {"name": "C2", "type": 5, "length": 20}
  ],
  "data": [
    {"C1": 1, "C2": "aaa"},
    {"C1": 2, "C2": "bbb"}
  ],
  "timezone": "+0900"
}
```

### DDL 예제

```bash
curl -G "http://127.0.0.1:5657/machbase" \
  --data-urlencode "q=CREATE TABLE curl_sample (c1 INT, c2 VARCHAR(20))"
```

테이블을 삭제할 때도 같은 엔드포인트를 사용합니다.

```bash
curl -G "http://127.0.0.1:5657/machbase" \
  --data-urlencode "q=DROP TABLE curl_sample"
```

### INSERT 예제

소량 데이터는 SQL `INSERT`로 입력할 수 있습니다.

```bash
curl -G "http://127.0.0.1:5657/machbase" \
  --data-urlencode "q=INSERT INTO curl_sample VALUES (3, 'ccc')"
```

다건 입력이나 수집성 데이터는 [Append REST API](/dbms/application-integration/rest-api/#machbase-append-rest-api)를
사용합니다.

### Python 예제

```python
import requests

BASE_URL = "http://127.0.0.1:5657"

def query(sql):
    resp = requests.get(f"{BASE_URL}/machbase", params={"q": sql}, timeout=10)
    resp.raise_for_status()
    result = resp.json()
    if result.get("error_code") != 0:
        raise RuntimeError(result.get("error_message"))
    return result

query("DROP TABLE curl_sample")
query("CREATE TABLE curl_sample (c1 INT, c2 VARCHAR(20))")
query("INSERT INTO curl_sample VALUES (1, 'aaa')")

result = query("SELECT * FROM curl_sample ORDER BY c1")
for row in result["data"]:
    print(row)
```

`DROP TABLE`처럼 대상이 없으면 실패할 수 있는 SQL은 `error_code`를 확인하여 애플리케이션
로직에 맞게 처리합니다.

### 주의 사항

- 하나의 요청에는 하나의 SQL 문을 전달합니다.
- SQL 문은 URL 인코딩해서 전달합니다.
- HTTP 상태 코드가 `200`이어도 SQL 실행 오류는 `error_code`와 `error_message`로
  반환될 수 있습니다.
- 대량 삽입은 `/machbase` POST Append API를 사용합니다.

<a id="machbase-append-rest-api"></a>

## /machbase append REST API

HTTP POST 요청으로 여러 행을 한 번에 삽입합니다. 요청
본문에는 대상 테이블 이름과 행 배열을 JSON으로 전달합니다.

### 엔드포인트

```text
POST /machbase
```

### 요청 형식

요청 본문은 `application/json` 형식입니다.

```json
{
  "name": "curl_sample",
  "values": [
    [1, "aaa"],
    [2, "bbb"]
  ]
}
```

| 필드 | 타입 | 설명 |
|------|------|------|
| `name` | string | 데이터를 삽입할 테이블 이름 |
| `values` | array | 삽입할 행 배열. 각 행은 테이블 컬럼 순서와 같은 배열 |

컬럼 이름은 요청에 포함하지 않습니다. `values`의 각 행은 테이블 정의의 컬럼 순서와
일치해야 합니다.

### 응답 형식

삽입 성공 시 Append 성공/실패 건수가 반환됩니다.

```json
{
  "error_code": 0,
  "error_message": "No Error",
  "timezone": "+0900",
  "data": [],
  "append_success": 2,
  "append_failure": 0
}
```

| 필드 | 설명 |
|------|------|
| `error_code` | `0`이면 요청 처리 성공 |
| `error_message` | 오류 메시지. 성공 시 빈 문자열 |
| `append_success` | 성공적으로 삽입된 행 수 |
| `append_failure` | 삽입에 실패한 행 수 |

### curl 예제

먼저 SQL REST API로 예제 테이블을 생성합니다.

```bash
curl -G "http://127.0.0.1:5657/machbase" \
  --data-urlencode "q=CREATE TABLE curl_sample (c1 INT, c2 VARCHAR(20))"
```

두 행을 Append로 삽입합니다.

```bash
curl -X POST "http://127.0.0.1:5657/machbase" \
  -H "Content-Type: application/json" \
  -d '{"name":"curl_sample","values":[[1,"aaa"],[2,"bbb"]]}'
```

삽입 결과를 확인합니다.

```bash
curl -G "http://127.0.0.1:5657/machbase" \
  --data-urlencode "q=SELECT * FROM curl_sample ORDER BY c1"
```

### JavaScript 예제

```javascript
async function appendRows(rows) {
  const resp = await fetch("http://127.0.0.1:5657/machbase", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({
      name: "curl_sample",
      values: rows,
    }),
  });

  const result = await resp.json();
  if (result.error_code !== 0 || result.append_failure > 0) {
    throw new Error(result.error_message || "append failed");
  }
  return result.append_success;
}

appendRows([[1, "aaa"], [2, "bbb"]]).then(console.log);
```

### Python 예제

```python
import requests

BASE_URL = "http://127.0.0.1:5657"

def append_rows(table, rows):
    resp = requests.post(
        f"{BASE_URL}/machbase",
        json={"name": table, "values": rows},
        timeout=10,
    )
    resp.raise_for_status()
    result = resp.json()
    if result.get("error_code") != 0:
        raise RuntimeError(result.get("error_message"))
    if result.get("append_failure", 0) != 0:
        raise RuntimeError(f"append failure: {result['append_failure']}")
    return result["append_success"]

count = append_rows("curl_sample", [[1, "aaa"], [2, "bbb"]])
print(f"inserted rows: {count}")
```

### INSERT와의 비교

| 방법 | 특징 |
|------|------|
| SQL `INSERT` (`GET /machbase?q=...`) | 소량 데이터, SQL 문 단위 실행 |
| Append (`POST /machbase`) | 여러 행을 한 요청으로 삽입, 수집성 데이터에 적합 |

초당 많은 행을 수집하는 애플리케이션에서는 SQL `INSERT`를 반복 실행하기보다 Append API나
네이티브 드라이버의 Append API를 사용합니다.

### 주의 사항

- 요청 본문은 JSON이어야 하며 `Content-Type: application/json`을 지정합니다.
- `values`의 컬럼 순서와 타입은 테이블 정의와 일치해야 합니다.
- SQL 실행 오류와 마찬가지로 HTTP 상태 코드와 함께 `error_code`, `append_failure`를
  확인합니다.

<a id="machiot-tags-tag-rest-api"></a>

## TAG 테이블 REST 조회

TAG 테이블 데이터는 `/machbase` SQL REST API로 조회합니다. 고수준 `/machiot/tags`
엔드포인트는 제공하지 않습니다. TAG 이름 목록, 시간
범위 조회, 최신값 조회는 SQL을 작성해 `/machbase?q=<SQL>`로 실행합니다.

### TAG 테이블 준비

예제에서는 다음 TAG 테이블을 사용합니다.

```bash
curl -G "http://127.0.0.1:5657/machbase" \
  --data-urlencode "q=CREATE TAG TABLE sensor_data (name VARCHAR(64) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE SUMMARIZED)"
```

데이터는 Append REST API로 입력합니다.

```bash
curl -X POST "http://127.0.0.1:5657/machbase" \
  -H "Content-Type: application/json" \
  -d '{"name":"sensor_data","values":[["sensor-01","2026-07-07 10:00:00",23.5],["sensor-01","2026-07-07 10:01:00",23.7]]}'
```

필요하면 조회 전 `EXEC TABLE_FLUSH(sensor_data)`를 실행해 메모리의 Append 데이터를
조회 가능 상태로 반영합니다.

```bash
curl -G "http://127.0.0.1:5657/machbase" \
  --data-urlencode "q=EXEC TABLE_FLUSH(sensor_data)"
```

### TAG 이름 목록 조회

```bash
curl -G "http://127.0.0.1:5657/machbase" \
  --data-urlencode "q=SELECT DISTINCT name FROM sensor_data ORDER BY name"
```

응답 예시:

```json
{
  "error_code": 0,
  "error_message": "",
  "columns": [
    {"name": "name", "type": 5, "length": 64}
  ],
  "data": [
    {"name": "sensor-01"}
  ],
  "timezone": "+0900"
}
```

### 특정 TAG 값 조회

```bash
curl -G "http://127.0.0.1:5657/machbase" \
  --data-urlencode "q=SELECT name, time, value FROM sensor_data WHERE name = 'sensor-01' ORDER BY time DESC LIMIT 10"
```

### 시간 범위 조회

Machbase 시간 연산은 나노초 단위를 사용합니다. 다음 예제는 최근 1시간 데이터를
조회합니다.

```bash
curl -G "http://127.0.0.1:5657/machbase" \
  --data-urlencode "q=SELECT name, time, value FROM sensor_data WHERE name = 'sensor-01' AND time >= SYSDATE - 3600000000000 ORDER BY time DESC LIMIT 100"
```

고정된 시간 범위를 사용할 때는 `TO_DATE`로 시각 문자열을 변환합니다.

```bash
curl -G "http://127.0.0.1:5657/machbase" \
  --data-urlencode "q=SELECT name, time, value FROM sensor_data WHERE time >= TO_DATE('2026-07-07 10:00:00') AND time < TO_DATE('2026-07-07 11:00:00') ORDER BY time"
```

### 최신 값 조회

```bash
curl -G "http://127.0.0.1:5657/machbase" \
  --data-urlencode "q=SELECT name, time, value FROM sensor_data WHERE name = 'sensor-01' ORDER BY time DESC LIMIT 1"
```

### 집계 조회

`DATE_TRUNC`로 시간 버킷을 만들어 집계할 수 있습니다. 단위는 `sec`, `min`, `hour`,
`day` 등을 사용합니다.

```bash
curl -G "http://127.0.0.1:5657/machbase" \
  --data-urlencode "q=SELECT DATE_TRUNC('min', time, 1) AS time, AVG(value) AS avg_value FROM sensor_data WHERE name = 'sensor-01' GROUP BY time ORDER BY time"
```

### Python 예제

```python
import requests

BASE_URL = "http://127.0.0.1:5657"

def query(sql):
    resp = requests.get(f"{BASE_URL}/machbase", params={"q": sql}, timeout=10)
    resp.raise_for_status()
    result = resp.json()
    if result.get("error_code") != 0:
        raise RuntimeError(result.get("error_message"))
    return result.get("data", [])

tags = query("SELECT DISTINCT name FROM sensor_data ORDER BY name")
print(tags)

rows = query(
    "SELECT name, time, value "
    "FROM sensor_data "
    "WHERE name = 'sensor-01' "
    "ORDER BY time DESC LIMIT 10"
)
for row in rows:
    print(row)
```

### `/machiot/tags` 요청이 실패하는 경우

`/machiot/tags`를 호출하면 다음과 같은 REST API URL 오류가 반환됩니다.

```json
{
  "error_code": 3126,
  "error_message": "The requested URL for the REST API is not valid"
}
```

이 경우 `/machbase` SQL REST API로 동일한 조회를 수행합니다.

<a id="error-handling-rest-api"></a>

## REST API 오류 처리

REST API 클라이언트는 HTTP 상태 코드와 응답 JSON의 `error_code`를 함께
확인해야 합니다. SQL 실행 오류는 HTTP `200 OK`와 함께 `error_code != 0`으로 반환될 수
있습니다.

### HTTP 상태 코드

| 상태 코드 | 의미 | 주요 원인 |
|-----------|------|-----------|
| `200 OK` | REST 요청 처리됨 | SQL 성공 또는 SQL 오류 응답 포함 |
| `401 Unauthorized` | 인증 실패 | `HTTP_AUTH` 활성화 상태에서 인증 정보 누락 또는 오류 |
| `404 Not Found` | 엔드포인트 없음 | 존재하지 않는 URL 요청 |
| `500 Internal Server Error` | 서버 오류 | 서버 내부 처리 오류 |

잘못된 REST API URL을 호출하면 HTTP `404`가 반환됩니다.

```bash
curl -i "http://127.0.0.1:5657/db/query"
```

### SQL 오류 응답

SQL 실행에 실패해도 HTTP 상태 코드는 `200`일 수 있습니다. 이때 `error_code`와
`error_message`를 확인합니다.

요청:

```bash
curl -G "http://127.0.0.1:5657/machbase" \
  --data-urlencode "q=SELCT * FROM example"
```

응답 예시:

```json
{
  "error_code": 2001,
  "error_message": "Syntax error: near token (SELCT * FROM example).",
  "timezone": "+0900",
  "data": []
}
```

| 필드 | 설명 |
|------|------|
| `error_code` | `0`이면 성공, `0`이 아니면 오류 |
| `error_message` | 오류 원인 |
| `timezone` | 응답 타임존 오프셋 |

### Append 오류 응답

Append 요청은 전체 요청 처리 결과와 행 단위 성공/실패 수를 함께 확인합니다.

```json
{
  "error_code": 0,
  "error_message": "No Error",
  "timezone": "+0900",
  "data": [],
  "append_success": 2,
  "append_failure": 0
}
```

`error_code`가 `0`이어도 `append_failure`가 `0`보다 크면 일부 행이 삽입되지 않은
것이므로 적절히 처리해야 합니다.

### 재시도 전략

| 오류 유형 | 재시도 여부 | 처리 |
|-----------|-------------|------|
| 네트워크 오류, 타임아웃 | 재시도 권장 | 지수 백오프 후 재시도 |
| HTTP `500` | 재시도 가능 | 서버 로그와 부하 상태 확인 |
| HTTP `404` | 재시도 불필요 | URL과 엔드포인트 수정 |
| `error_code != 0` SQL 오류 | 재시도 불필요 | SQL, 테이블, 권한, 타입 수정 |
| `append_failure > 0` | 애플리케이션 판단 | 실패 행을 확인하고 보정 후 재전송 |

### Python 재시도 예제

```python
import time
import requests

BASE_URL = "http://127.0.0.1:5657"

def query_with_retry(sql, max_retries=3, base_delay=1.0):
    last_error = None

    for attempt in range(max_retries):
        try:
            resp = requests.get(
                f"{BASE_URL}/machbase",
                params={"q": sql},
                timeout=10,
            )

            if resp.status_code == 404:
                raise ValueError("REST 엔드포인트 URL을 확인하십시오.")
            if resp.status_code >= 500:
                last_error = f"server error: HTTP {resp.status_code}"
            else:
                resp.raise_for_status()
                result = resp.json()
                if result.get("error_code") == 0:
                    return result
                raise ValueError(result.get("error_message"))

        except (requests.ConnectionError, requests.Timeout) as e:
            last_error = str(e)

        if attempt < max_retries - 1:
            time.sleep(base_delay * (2 ** attempt))

    raise RuntimeError(f"최대 재시도 횟수 초과: {last_error}")

result = query_with_retry("SELECT COUNT(*) FROM curl_sample")
print(result)
```

### 타임아웃 처리

REST API 요청에는 타임아웃을 설정합니다.

```bash
curl -G "http://127.0.0.1:5657/machbase" \
  --connect-timeout 5 \
  --max-time 30 \
  --data-urlencode "q=SELECT COUNT(*) FROM curl_sample"
```

Python에서는 연결 타임아웃과 읽기 타임아웃을 별도로 지정할 수 있습니다.

```python
resp = requests.get(
    "http://127.0.0.1:5657/machbase",
    params={"q": "SELECT COUNT(*) FROM curl_sample"},
    timeout=(5, 30),
)
```

### 오류 처리 체크리스트

- REST 엔드포인트가 `/machbase`인지 확인합니다.
- HTTP 상태 코드가 `404` 또는 `500`이면 URL 또는 서버 상태를 먼저 확인합니다.
- HTTP `200` 응답에서도 `error_code`가 `0`인지 확인합니다.
- Append 요청은 `append_failure`를 함께 확인합니다.
- 모든 요청에 타임아웃을 설정합니다.
- SQL 오류는 재시도보다 SQL 문, 테이블 존재 여부, 컬럼 타입을 수정합니다.

드라이버와 SDK에 공통으로 적용되는 오류 처리 전략은 [오류 처리와 재시도](/dbms/application-integration/concepts-common/#error-handling-retry)를 참조합니다.
