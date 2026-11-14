---
type: docs
title: '12.4.8 MCAP'
weight: 80
toc: true
---

파일 안의 메시지·토픽·스키마·첨부·메타데이터를 선택합니다. 샘플은 /sensor 토픽의 JSON 메시지 5개이며 본문에 id와 v가 있습니다.

## 실습 준비

[실습 파일 묶음](/assets/dbms-8.9/dfq/samples.zip)을 **DB 서버**의 `/srv/dfq`에 풉니다.
경로가 다르면 SQL의 `/srv/dfq`를 실제 서버 경로로 바꿉니다. 접속과 권한 준비는
[시작하기](../../getting-started/)를 참고합니다. SQL마다 별도의 준비 명령 없이 같은 입력을 사용합니다.
센서 샘플의 id=1~5, v=id×10이므로 COUNT=5, SUM(id)=15, SUM(v)=150입니다.
LeRobot 샘플은 이 센서 파일과 별개입니다.

## 작업별 빠른 찾기

| 목적 | 조합한 설정 | 예제 |
|---|---|---|
| 토픽을 선택해 숫자 필드 조회 | `format`, `topic` | [예제 1](#example-1) |
| 본문과 기록 시각을 함께 조회 | `format`, `topic`, `column.time_ns`, `column.seq` | [예제 2](#example-2) |
| 메시지의 필드를 골라 투영 | `format`, `topic`, `project.key`, `project.reading`, `type.reading` | [예제 3](#example-3) |
| 메시지를 envelope로 확인 | `format`, `topic`, `columns`, `target`, `row` | [예제 4](#example-4) |
| 토픽 목록과 스키마 살펴보기 | `format`, `target`, `mode` | [예제 5](#example-5) |
| 컬럼과 SQL 타입 확인 | `format`, `topic`, `mode`, `view` | [예제 6](#example-6) |
| payload 원본을 작은 청크로 읽기 | `format`, `topic`, `target`, `row`, `mode`, `raw.representation`, `raw.chunk_bytes` | [예제 7](#example-7) |

## 파일과 조회 대상

```text
sensor.mcap
 └─ channel: /sensor
     ├─ message 0: sequence=0, log_time=1000000000 → {id:1,v:10}
     ├─ message 1: sequence=1, log_time=1000000001 → {id:2,v:20}
     └─ ... 5 messages

 topic=/sensor                  → native id/v
 target=messages + row=0         → 첫 메시지
 raw.representation=message_bytes → 첫 메시지 payload 원본
 mode=raw (stored)              → MCAP 파일 자체
```

## 전체 포맷 옵션

| 옵션 | 기본값 | 허용값·범위 | 역할 |
|---|---|---|---|
| `topic` | 지정하지 않음 | 아래 설명의 문자열·타입 규칙 | 대소문자를 구분하는 정확한 MCAP 토픽명 |
| `decode` | 지정하지 않음 | none,auto | 명시적인 메시지 해석 정책. 생략한 자동 native 조회와 구분 |
| `sensor` | 지정하지 않음 | points,pixels,joints | 해석된 points/pixels/joints 배열 선택 |
| `names` | 지정하지 않음 | CSV 인용을 사용하는 쉼표 목록 | 원본 순서대로 출력 컬럼명 지정 |
| `type.*` | 지정하지 않음 | VARCHAR,TEXT,SHORT,INTEGER,LONG,USHORT,UINTEGER,ULONG,FLOAT,DOUBLE,DECIMAL,NUMERIC,DATETIME,TIMESTAMP,JSON,BINARY,VARBINARY | 컬럼별 SQL 타입. * 위치에 컬럼명 사용 |
| `filename` | false | true / false | 출처 파일명 컬럼 추가 |
| `union_by_name` | true | true / false | 여러 입력의 컬럼 결합 정책. 아래 reader별 제약 확인 |
| `on_error` | error | error | 복구 가능한 완전한 행의 변환 오류 처리. 손상 전체를 무시하는 기능 아님 |
| `max_uncompressed_bytes` | 1073741824 | 1~9223372036854775807 | 선택 압축 chunk/member의 해제 바이트 상한 |
| `max_spool_bytes` | 4294967296 | 1~9223372036854775807 | 실행 단위 spool 바이트 상한 |
| `parallel` | auto | auto / false (순차 실행) | 실행 정책. 아래 지원 조합 확인 |
| `threads` | 지정하지 않음 | 1~32 | 작업자 수 상한. reader에 따라 병렬 작업자를 만들지 않음 |
| `sources` | 지정하지 않음 | CSV 인용을 사용하는 쉼표 목록 | 순서 있는 파일 목록. 위치형·source와 혼용 금지 |

공통 mode·columns·target·row·field·project·column·source·raw 설정은
[READ 공통 옵션](../../read-options/)을 함께 적용합니다. 위 표의 값 목록은 입력 형식이며
아래 제약에서 제한한 값은 해당 reader에서 실행할 수 없습니다. 특히 parallel의 등록된 값 목록이
실제 병렬 처리 지원을 뜻하지 않습니다. view별 상세 설정은 inspect의 options/capabilities도 확인합니다.

## 우선순위와 허용 조합

topic은 정확한 대소문자 이름입니다. topic을 선택하고 decode를 생략하면 해석 가능한 본문을 native 필드로 받습니다. decode=auto를 명시한 공통 메시지 행의 결과 형태는 별도로 확인합니다. message_bytes는 메시지 payload, payload_bytes는 스키마·첨부의 원 data입니다. parallel=true는 지원하지 않습니다.

## 옵션 조합 예제

<a id="example-1"></a>

### 1. 토픽을 선택해 숫자 필드 조회

선택한 JSON 메시지의 본문을 native 컬럼으로 해석합니다.

```sql
SELECT COUNT(*) AS N,SUM(v) AS TOTAL
FROM READ('/srv/dfq/sensor.mcap', 'format=mcap', 'topic=/sensor') ;
```

반환 컬럼: `N`, `TOTAL`. 반환 행 수: 1.

다음은 처음 최대 3행의 표시입니다. 긴 값은 미리보기로 줄였습니다.

| N | TOTAL |
| --- | --- |
| 5 | 150 |

[SQL 다운로드](/assets/dbms-8.9/dfq/mcap/01.sql)

<a id="example-2"></a>

### 2. 본문과 기록 시각을 함께 조회

기록 시각과 본문에 포함된 시각은 별개입니다.

```sql
SELECT id,v,time_ns,seq
FROM READ('/srv/dfq/sensor.mcap', 'format=mcap', 'topic=/sensor',
 'column.time_ns=meta.mcap.log_time',
 'column.seq=meta.mcap.sequence') ORDER BY id LIMIT 3;
```

반환 컬럼: `id`, `v`, `time_ns`, `seq`. 반환 행 수: 3.

다음은 처음 최대 3행의 표시입니다. 긴 값은 미리보기로 줄였습니다.

| id | v | time_ns | seq |
| --- | --- | --- | --- |
| 1 | 10 | 1000000000 | 0 |
| 2 | 20 | 1000000001 | 1 |
| 3 | 30 | 1000000002 | 2 |

[SQL 다운로드](/assets/dbms-8.9/dfq/mcap/02.sql)

<a id="example-3"></a>

### 3. 메시지의 필드를 골라 투영

선택 토픽의 해석 가능한 필드만 투영합니다.

```sql
SELECT key,reading
FROM READ('/srv/dfq/sensor.mcap', 'format=mcap', 'topic=/sensor',
 'project.key=id',
 'project.reading=v',
 'type.reading=DOUBLE') ORDER BY key LIMIT 3;
```

반환 컬럼: `key`, `reading`. 반환 행 수: 3.

다음은 처음 최대 3행의 표시입니다. 긴 값은 미리보기로 줄였습니다.

| key | reading |
| --- | --- |
| 1 | 10.0 |
| 2 | 20.0 |
| 3 | 30.0 |

[SQL 다운로드](/assets/dbms-8.9/dfq/mcap/03.sql)

<a id="example-4"></a>

### 4. 메시지를 envelope로 확인

본문의 논리 구조를 한 행씩 확인합니다.

```sql
SELECT DATA
FROM READ('/srv/dfq/sensor.mcap', 'format=mcap', 'topic=/sensor',
 'columns=envelope',
 'target=messages',
 'row=0') ;
```

반환 컬럼: `DATA`. 반환 행 수: 1.

다음은 처음 최대 3행의 표시입니다. 긴 값은 미리보기로 줄였습니다.

| DATA |
| --- |
| {"id":1,"v":10} |

[SQL 다운로드](/assets/dbms-8.9/dfq/mcap/04.sql)

<a id="example-5"></a>

### 5. 토픽 목록과 스키마 살펴보기

메시지 본문 대신 파일의 토픽 목록을 읽습니다.

```sql
SELECT *
FROM READ('/srv/dfq/sensor.mcap', 'format=mcap', 'target=topics',
 'mode=data') ;
```

반환 컬럼: `SOURCE`, `CHANNEL_ID`, `TOPIC`, `SCHEMA_ID`, `SCHEMA_NAME`, `MESSAGE_ENCODING`. 반환 행 수: 1.

다음은 처음 최대 3행의 표시입니다. 긴 값은 미리보기로 줄였습니다.

| SOURCE | CHANNEL_ID | TOPIC | SCHEMA_ID | SCHEMA_NAME | MESSAGE_ENCODING |
| --- | --- | --- | --- | --- | --- |
| /srv/dfq/sensor.mcap | 1 | /sensor | 1 | Sensor | json |

[SQL 다운로드](/assets/dbms-8.9/dfq/mcap/05.sql)

<a id="example-6"></a>

### 6. 컬럼과 SQL 타입 확인

토픽 선택에 따른 반환 컬럼을 확인합니다.

```sql
SELECT COLUMN_NAME,SQL_TYPE
FROM READ('/srv/dfq/sensor.mcap', 'format=mcap', 'topic=/sensor',
 'mode=inspect',
 'view=columns') ORDER BY COLUMN_ORDINAL;
```

반환 컬럼: `COLUMN_NAME`, `SQL_TYPE`. 반환 행 수: 2.

다음은 처음 최대 3행의 표시입니다. 긴 값은 미리보기로 줄였습니다.

| COLUMN_NAME | SQL_TYPE |
| --- | --- |
| id | LONG |
| v | LONG |

[SQL 다운로드](/assets/dbms-8.9/dfq/mcap/06.sql)

<a id="example-7"></a>

### 7. payload 원본을 작은 청크로 읽기

JSON 표현이 아닌 원래 메시지 payload 바이트입니다. _OFFSET 순으로 재결합합니다.

```sql
SELECT *
FROM READ('/srv/dfq/sensor.mcap', 'format=mcap', 'topic=/sensor',
 'target=messages',
 'row=0',
 'mode=raw',
 'raw.representation=message_bytes',
 'raw.chunk_bytes=16') ;
```

반환 컬럼: `_SOURCE`, `_TARGET`, `_ROW`, `_FIELD`, `_OFFSET`, `_LENGTH`, `_TOTAL_SIZE`, `_LAST`, `_CONTENT`, `_META`. 반환 행 수: 2.

[SQL 다운로드](/assets/dbms-8.9/dfq/mcap/07.sql)

## 오류와 해결

### 지원하지 않는 옵션 사용

```sql
SELECT *
FROM READ('/srv/dfq/sensor.mcap',
 'format=mcap',
 'unknown_option=true');
```

예상 오류: `INVALID_OPTION`. 등록되지 않은 옵션은 무시되지 않고 INVALID_OPTION으로 거부됩니다. 옵션표의 이름을 사용합니다.

[오류 SQL 다운로드](/assets/dbms-8.9/dfq/mcap/08.sql)

### 형식 또는 선택 조건 오류

```sql
SELECT *
FROM READ('/srv/dfq/bad.mcap',
 'format=mcap');
```

예상 오류: `CORRUPT_DATA`. 손상된 파일은 정상 빈 결과가 아닙니다. 원본 형식과 파일 내용을 확인합니다.

[오류 SQL 다운로드](/assets/dbms-8.9/dfq/mcap/09.sql)

## 타입·구조·표현의 상세 규칙

MCAP 파일은 여러 토픽의 메시지를 담은 기록 파일입니다. 처음에는 파일을 열고,
토픽 목록에서 이름을 확인한 뒤, 그 토픽을 지정하면 메시지 필드를 SQL 컬럼으로 읽을 수 있습니다.

파일의 물리 구조와 옵션별 조회 범위는 40절 MCAP 구조·SELECT 그림을 참고합니다. 메시지10개를 가정한 그림과 실제 base.mcap에서 바로 실행할 SQL을 함께 제공합니다.

세 번째 조회의 토픽과 컬럼 이름은 실제 파일에 맞게 바꾼다. 기본 목록 조회는
본문을 해석하지 않으며, `topic=`만 지정한 조회는 지원되는 본문을 필드 컬럼으로 해석합니다.

### 먼저 파일 안의 메시지 확인하기

옵션 없이 읽으면 **메시지 한 개가 한 행**입니다. 메시지 본문을 해석하지 않고
토픽·시각·타입과 원본 조회 참조를 반환합니다. 여러 토픽이 섞이거나 일부 타입의
decoder가 없어도 파일을 탐색할 수 있습니다. 형식은 파일 내용으로 자동 감지하며,
필요하면 `'format=mcap'`으로 고정합니다. `profile=mcap.standard@1`도 형식만
고정하며 토픽이나 메시지 스키마를 고정하지 않습니다.

출력은 파일에 기록된 순서다. `LOG_TIME`이 증가한다고 가정하지 않습니다. 시간순
정렬이 필요하면 SQL `ORDER BY LOG_TIME`을 사용합니다. 여러 파일도 요청한 source
순서로 읽으며 자동으로 시간순 병합하지 않습니다.

`data/01/base.mcap`에는 `/counter` 토픽의 메시지 100개가 들어 있습니다. 파일은
바이너리이며, 아래 `.msg` 텍스트는 그 안에 저장된 스키마다.

첫 메시지의 직렬화 payload는 다음 20바이트다. MCAP 파일 전체의 원문과 구분합니다.

샘플의 독립 기대값은 다음과 같습니다.

기본 조회의 `DATA`는 NULL이고 상태는 `NOT_DECODED`다. 이것은 원본 메시지 값이
NULL이라는 뜻이 아닙니다. `_REFS`를 통해 원본 payload를 읽을 수 있습니다.

### 토픽을 고르면 필드를 컬럼으로 조회하기

먼저 토픽 목록을 확인합니다.

`topic=`만 지정하면 지원되는 메시지의 최상위 필드를 SQL 컬럼으로 반환합니다.

위 샘플은 `id=1,2,3`, `value=10,20,30`을 담고 있습니다. `id`는 INTEGER,
`value`는 LONG으로 설명됩니다. 문자열은 TEXT, 중첩 객체·배열은 정규 JSON을 담은
TEXT 컬럼으로 반환합니다. SQL 타입은 준비 단계에 고정하며 첫 행이 작다고 JSON으로
반환했다가 뒤에서 TEXT로 바꾸지 않습니다. TEXT 한도는 UTF-8 바이트 기준 64MiB다.

토픽 이름은 대소문자를 구분하는 정확한 이름입니다. `/joint_states`와
`joint_states`를 같은 이름으로 바꾸지 않습니다. 실제 공개 샘플에는
`io_teleop/joint_states`처럼 선행 `/`가 없는 토픽도 있습니다.

컬럼 전체에 별칭을 주려면 `names=`를 사용합니다. 목록 순서는 원래 컬럼 순서이며
개수가 맞아야 합니다.

같은 토픽에 서로 호환되지 않는 스키마가 섞이면 native 조회는
`SCHEMA_CHANGED` 오류다. 같은 필드 이름이라도 배열 길이나 중첩 필드 타입이
다르면 호환되지 않을 수 있습니다. 단순한 주석·기본값·타입 이름 alias의 차이는
실제 타입 구조를 비교합니다.

### 큰 이미지에서 작은 필드만 조회하기

큰 byte 배열도 기본 TEXT에 정규 JSON으로 표현하지만, JSON 숫자 배열은 원래 byte
배열보다 커질 수 있습니다. 필요한 필드만 `project`로 지정하면 출력 크기와 작업 메모리를
줄일 수 있습니다. 64MiB를 넘는 값은 원본·canonical 청크로 조회합니다.

문자열 컬럼은 TEXT로 설명될 수 있습니다. MIN 같은 기존 SQL 함수가 VARCHAR 인자를
요구하면 실제 값보다 충분한 길이로 먼저 변환합니다. 아래 고정 샘플의 format은
모두 네 글자인 `jpeg`다.

`CompressedImage`의 `format`과 압축된 이미지 바이트는 조회 대상이지만, JPEG나
PNG를 픽셀로 복호화하는 기능은 지원 범위에 포함하지 않습니다.

### 전체 목록에 해석 결과를 함께 보기

`decode=auto`는 지원되는 메시지의 내용을 해석하면서 기본 공통 컬럼을 유지합니다.
`topic=/counter`와 함께 쓰면 그 토픽만 공통 컬럼으로 반환합니다.

미지원 메시지나 잘못된 본문은 기본 목록·원본 바이트 조회를 막지 않습니다.
`decode=auto`는 메시지별 상태와 이유를 제공합니다. 반면 native 필드 조회나 명시한
센서 의미 해석에서 실패하면 오류를 반환합니다. 컨테이너 구조·CRC·I/O·메모리·취소
오류는 메시지 상태로 숨기지 않습니다.

공통 컬럼의 상태 경로는 `_META.mcap`입니다. 기존 공통 READ envelope를 요청하는
`columns=envelope`에서는 같은 MCAP 확장 정보가 `_META.extensions.mcap`에 있습니다.

### DATA와 native 컬럼의 SQL 타입

TEXT로 반환해도 원래 논리 kind·source type·배열 shape는 유지됩니다. 예를 들어 배열을
TEXT로 읽었다고 `_META.types`에서 원래 배열을 문자열 타입으로 바꾸지 않습니다.

기존 JSON SQL 타입이 필요하면 명시합니다. 아래 고정 자료의 `obj`는 작은 객체다.

`type.필드=...`는 자동 선택보다 우선합니다. 이름을 바꾼 project 컬럼은
`project.payload=obj`, `type.payload=JSON`처럼 별칭으로 지정합니다. 논리 DATA의
명시 타입은 TEXT 또는 JSON입니다. JSON은 32,768바이트, TEXT는 67,108,864바이트다.
`mode=inspect, view=columns`에서 실제 SQL 타입과 컬럼 크기를 확인할 수 있습니다.

### TEXT 안의 JSON 필드 꺼내기

MCAP의 TEXT 객체·배열에도 다음 JSON 함수를 바로 사용할 수 있습니다.

두 번째 예제는 `[1,2,true]`를 TEXT로 반환합니다. `JSON_EXTRACT_TEXT`는 JSON 문자열에서
인용 부호를 제거한 내용, 객체·배열에서는 직렬화된 JSON을 반환합니다. 잘못된 JSON과
존재하지 않는 경로는 오류다. `JSON_EXTRACT_STRING`은 기존처럼 없는 경로에서 NULL을
반환합니다. 문자열 반환 함수의 출력 한도 초과는 오류이며 자동 참조로 바뀌지 않습니다.

기존 두 VARCHAR 함수의 반환 한도는 TEXT 입력을 받더라도 늘어나지 않습니다. INTEGER와
DOUBLE은 기존 수치 변환 범위를 유지하며, READ가 보존한 큰 정수 원문까지 모든 JSON
수치 함수가 정밀하게 추출하도록 범위를 확장한 것은 아닙니다.

### NULL·빈 값·내부 NUL 구분

nodes는 object/array의 DATA를 생략하고 자식 노드를 별도로 반환합니다. 위 표의 객체·배열
표현을 nodes 컨테이너 행에도 적용하지 않습니다.

명시 JSON의 기존 NULL 동작은 유지합니다. 공통 messages DATA의 JSON null은 SQL NULL이며,
envelope/elements/nodes의 scalar JSON null은 `null` JSON 바이트로 표현합니다.

새 `JSON_EXTRACT_TEXT`는 JSON 문자열 안의 NUL도 길이에 포함해 보존합니다. 예를 들어
고정 샘플의 `obj.nul`은 `a`, NUL, `b`의 3바이트다. 기존 `JSON_EXTRACT`와
`JSON_EXTRACT_STRING`의 문자열 처리는 그대로여서 이 샘플에서는 NUL 앞 1바이트를
반환합니다. MCAP 문자열을 native TEXT로 직접 읽을 때의 내부 NUL 오류 정책은 유지합니다.

CLI/JDBC 같은 클라이언트에서도 NUL을 포함한 값을 읽을 때는 반환 길이를 함께 사용합니다.
TEXT 입력 지원은 위 다섯 함수에 적용되며 다른 JSON 함수의 지원 확대를 뜻하지 않습니다.
문자열의 숫자 변환도 기존 규칙을 따릅니다. 예를 들어 `JSON_EXTRACT_DOUBLE`은 문자열
`bad`를 0.0으로 변환하지만 지수 범위 오류는 NULL로 반환할 수 있으므로, 숫자 문자열의
유효성 검사용 함수로 사용하지 않습니다.

### 스키마·첨부파일·메타데이터 살펴보기

- `topics`는 채널당 한 행, `schemas`는 schema ID당 한 행입니다. Summary에 반복된
  같은 정의를 중복 출력하지 않습니다.
- 스키마 `DATA`는 표현 가능한 UTF-8 원문을 JSON 문자열로 제공합니다. 바이너리
  스키마나 큰 원문은 참조로 조회합니다.
- 첨부파일은 설명과 크기를 반환하고 실제 내용은 원본 payload로 조회합니다.
- Metadata는 원래 레코드의 key/value별로 행을 반환합니다.

파일 `DESC`는 옵션 없는 기본 조회의 공통 컬럼을 설명합니다.

특정 토픽의 필드 타입은 다음과 같이 확인합니다.

`mode=schema`의 `DETAILS`는 READ가 생성하는 고정 JSON 컬럼입니다. `type.details=json`은
이 컬럼의 타입을 지정하지 않고 원본 MCAP 데이터에서 details라는 컬럼을 찾으므로,
그런 컬럼이 없으면 `MCAP type.* names an absent output column` 오류가 발생합니다.
DETAILS 조회에는 type 옵션을 넣지 않습니다.

토픽을 생략하면 기본 공통 메시지 컬럼의 스키마를 설명합니다. 필드 정의가 SQL JSON
셀 한도를 넘으면 DETAILS의 type.locator에 전체 정의를 읽는 참조가 반환됩니다.
전체 정의는 locator의 raw_canonical 재조회 SQL로 읽습니다. 필드별 컬럼명과 SQL
타입만 필요하면 위 inspect/columns가 간단하다.

### 중첩 필드와 센서 배열 접근하기

`row=`는 선택한 target·topic 결과에서의 **0부터 시작하는 메시지 순번**입니다.
MCAP의 `SEQUENCE` 값이나 타임스탬프와 구분합니다. 여러 파일에서는 선택 결과 전체의
순번입니다. `field=`에는 기존 READ의 SQL형 경로를 사용합니다.

선택 배열의 크기는 행을 지정하고 dimensions로 확인합니다. 빈 배열은 extent 0인
축을 반환하고 scalar는 축을 반환하지 않습니다.

envelope의 `_META.types`는 원본 필드 경로를 사용합니다. SQL 컬럼 별칭을 주더라도
원본 경로를 바꾸지 않습니다. 넓은 객체의 필드 주석이 작업 한도를 넘으면 개별
필드 주석 대신 객체 전체의 주석을 반환하고,
`_META.extensions.mcap.type_coverage`에 `root_only_size_limit`을 표시합니다.
명시적으로 선택한 배열의 shape는 이 축약과 별도로 제공합니다.

센서의 저장 배열을 실제 포인트·픽셀·관절 객체로 보려면 `sensor=`를 지정합니다.
`decode=auto`, `target=messages`, 명시적인 `row=`가 필요합니다.

샘플 첫 PointCloud2 메시지에는 `{x:1,y:2,z:3,intensity:0.5}`와
`{x:2,y:4,z:6,intensity:0.5}`의 두 점이 있습니다. 저장 padding을 점 속성으로 읽지
않습니다. 첫 mono8 Image의 픽셀은 1과 2다. 첫 JointState는 left/right 이름과
position 0.5/1.0을 가지며 velocity·effort는 원본에서 비어 있습니다.

PointCloud2는 원래 `fields`의 이름·offset·datatype·count와 point/row 간격을
사용합니다. x/y/z의 존재를 가정하지 않습니다. Image 픽셀은 행 우선이며, 여러 채널은
원 encoding 순서로 반환합니다. JointState의 빈 선택 배열은 관절별 값에서 NULL로
보이고 메타데이터에 원래 배열이 비어 있었다는 정보를 남깁니다.

픽셀 해석은 `mono8`, `mono16`, `rgb8`, `bgr8`, `rgba8`, `bgra8`, `16UC1`,
`32FC1`을 지원 대상으로 합니다. 다른 encoding도 메시지 필드와 원본 data는 보존합니다.

### 원본 바이트와 큰 값을 청크로 읽기

독립 원문 기준으로 20바이트인 첫 payload는 7·7·6바이트로 나뉜다. `_OFFSET`은
이 **반환 byte열 안의 위치**다. 압축된 MCAP 파일 안의 물리 offset과 혼동하지 않습니다.
메시지 본문이 해석 불가능해도 원본 조회는 가능하다. `message_bytes`는 메시지 전체를
대상으로 하며 임의 하위 `field`의 직렬화 byte 추출을 뜻하지 않습니다.

기본 TEXT의 한도는 64MiB이고 명시 JSON의 한도는 32KiB다. native/project 값이
TEXT 한도를 넘으면 `LIMIT_EXCEEDED` 오류이며, 공통·논리 DATA는 기존 참조 경로를
사용합니다. 명시 JSON의 native/project 한도 초과도 오류다. 더 큰 값은 위 청크 조회로
읽습니다. NaN·Infinity는 JSON number로 나타낼 수 없으므로 canonical 변환은 명시 오류를
반환하고 원본 메시지 바이트를 대안으로 제공합니다. 원본 바이트에 포함된 padding과
IEEE 비트는 그대로 유지합니다.

### 같은 원본 재조회와 strong snapshot

`READ_SQL`은 그대로 실행할 수 있는 조회문이고, `READ_TOKEN`이 발급되면 다음
형태로 실행합니다. 실제 token 문자열은 위 조회 결과를 사용합니다.

`_REFS`에도 조회 인자와 예제 SQL이 있습니다. 원본 메시지 작업 이름은 `raw_message`,
스키마·첨부 원문은 `raw_payload`, canonical JSON은 `raw_canonical`입니다. 참조는
source 집합·topic·target·row·field·표현과 명시 타입 및 mapping/source guard를 유지합니다.

자동 TEXT 정책은 mapping fingerprint에 포함됩니다. 변경 전 JSON 기본 정책으로 발급한
토큰이나 `source.expected_mapping`이 새 정책과 다르면 `MAPPING_CHANGED` 오류로
거부합니다. 예전 mapping을 그대로 받아 출력 타입만 조용히 바꾸지 않습니다. 현재 환경에서
참조를 새로 발급하고, JSON 타입이 필요하면 `type.필드=JSON`을 명시합니다.

`source.consistency=strong`은 선택한 source 집합의 snapshot을 사용합니다.

- 열린 실행의 잔여 행과 같은 실행 안의 재스캔은 pin한 snapshot을 읽습니다.
- 다음 실행이나 발급된 참조의 재조회는 원래 선택한 파일의 변경·삭제를 검사합니다.
- glob에 나중에 추가된 파일을 기존 prepared/ref의 source 집합에 섞지 않습니다.
  새 독립 READ에서는 새로운 파일을 포함할 수 있습니다.

### 지원 범위와 한도

64MiB는 결과 한 셀의 표현 한도이며 질의 메모리 예산과 별개다. 결과 셀뿐 아니라
입력·파싱 DOM·직렬화 버퍼·다른 컬럼도 `MAX_QPX_MEM`을 사용하므로, 64MiB 이하의 값도
질의 예산이 부족하면 실패할 수 있습니다. 예산·I/O·취소 오류는 참조 행으로 숨기지 않습니다.

테스트처럼 큰 값을 읽을 때 세션 예산을 명시할 수 있습니다. 아래 값은 512MiB이며 모든
파일·질의에서 충분한 메모리를 보장하는 수치는 아닙니다.

ROS2 정수는 native 타입의 SQL NULL 예약값과 충돌할 수 있습니다. 예를 들어
INT64 최솟값 `-9223372036854775808`은 LONG의 NULL 예약값이고, UINT64 최댓값
`18446744073709551615`는 ULONG의 NULL 예약값입니다. 원래 숫자를 조용히 NULL로
바꾸지 않고 오류로 알린다. 해당 값까지 읽으려면 명시적으로 타입을 바꾼다.

일반적인 int64·uint64 필드는 각각 LONG·ULONG으로 읽고, 예약값을 포함한 전체
정수 범위가 필요할 때 `type.컬럼=DECIMAL(20,0)`을 사용합니다. 시간 메타데이터는
처음부터 DECIMAL(20,0)으로 반환하므로 uint64 전체 범위를 유지합니다. 문자열의 내부 NUL,
큰 JSON, 비유한 실수처럼 native 표현에 제한이 있으면 원본·envelope 경로를 사용합니다.

## 관련 문서

- [구조와 컬럼 확인](../../inspect/)
- [구조화된 값과 원문 추출](../../extract/)
- [권한과 운영](../../operations/)
