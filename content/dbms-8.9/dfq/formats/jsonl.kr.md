---
type: docs
title: '12.4.4 JSONL'
weight: 40
toc: true
---

각 비어 있지 않은 줄을 부모 레코드로 읽습니다. 한 줄의 루트 배열은 자동으로 여러 행이 되지 않으며 records로 펼침을 지정합니다.

## 실습 준비

[실습 파일 묶음](/assets/dbms-8.9/dfq/samples.zip)을 **DB 서버**의 `/srv/dfq`에 풉니다.
경로가 다르면 SQL의 `/srv/dfq`를 실제 서버 경로로 바꿉니다. 접속과 권한 준비는
[시작하기](../../getting-started/)를 참고합니다. SQL마다 별도의 준비 명령 없이 같은 입력을 사용합니다.
센서 샘플의 id=1~5, v=id×10이므로 COUNT=5, SUM(id)=15, SUM(v)=150입니다.
LeRobot 샘플은 이 센서 파일과 별개입니다.

## 작업별 빠른 찾기

| 목적 | 조합한 설정 | 예제 |
|---|---|---|
| 숫자 타입과 순차 실행 | `format`, `type.id`, `parallel` | [예제 1](#example-1) |
| 중첩 배열을 행으로 선택 | `format`, `records`, `type.id` | [예제 2](#example-2) |
| 중첩 필드와 배열 원소를 투영 | `format`, `project.key`, `project.x`, `project.first`, `type.key` | [예제 3](#example-3) |
| 날짜 문자열을 명시 변환 | `format`, `type.day`, `dateformat.day`, `timezone` | [예제 4](#example-4) |
| 부모 한 행의 배열 원소 펼치기 | `format`, `mode`, `target`, `row`, `field` | [예제 5](#example-5) |
| 원문 구조를 envelope로 보존 | `format`, `columns`, `target`, `row`, `field` | [예제 6](#example-6) |
| 압축과 전체 스키마 추론 | `format`, `compression`, `sample_size`, `parallel` | [예제 7](#example-7) |
| 필드 선택과 원래 행 순번 추가 | `format`, `project.key`, `column.position`, `column.original_v` | [예제 8](#example-8) |

## 전체 포맷 옵션

| 옵션 | 기본값 | 허용값·범위 | 역할 |
|---|---|---|---|
| `parallel` | auto | auto,true,false | 실행 정책. 아래 지원 조합 확인 |
| `threads` | 지정하지 않음 | 1~32 | 작업자 수 상한. reader에 따라 병렬 작업자를 만들지 않음 |
| `encoding` | auto | auto,utf-8,cp949,latin-1,utf-16 | 입력 문자를 엄격하게 디코딩 |
| `compression` | auto | auto,none,gzip,zstd | 외부 파일 압축 형식 |
| `records` | 지정하지 않음 | 논리 필드 경로 | 행으로 펼칠 JSON 배열 경로 |
| `on_error` | error | error,skip | 복구 가능한 완전한 행의 변환 오류 처리. 손상 전체를 무시하는 기능 아님 |
| `union_by_name` | true | true / false | 여러 입력의 컬럼 결합 정책. 아래 reader별 제약 확인 |
| `filename` | false | true / false | 출처 파일명 컬럼 추가 |
| `sources` | 지정하지 않음 | CSV 인용을 사용하는 쉼표 목록 | 순서 있는 파일 목록. 위치형·source와 혼용 금지 |
| `sample_size` | -1 | 아래 설명의 문자열·타입 규칙 | 양의 레코드 수 또는 -1(전체) |
| `max_record_bytes` | 67108864 | 1~9223372036854775807 | 디코딩된 UTF-8 레코드 바이트 상한 |
| `type.*` | 지정하지 않음 | VARCHAR,TEXT,LONG,ULONG,SHORT,INTEGER,USHORT,UINTEGER,FLOAT,DOUBLE,BOOLEAN,DECIMAL,NUMERIC,DATE,DATETIME,TIMESTAMP,TIME,JSON | 컬럼별 SQL 타입. * 위치에 컬럼명 사용 |
| `dateformat` | 지정하지 않음 | 아래 설명의 문자열·타입 규칙 | 공통 날짜 해석 형식 |
| `dateformat.*` | 지정하지 않음 | 아래 설명의 문자열·타입 규칙 | 컬럼별 날짜 형식, 공통 형식보다 우선 |
| `timestampformat` | 지정하지 않음 | 아래 설명의 문자열·타입 규칙 | 공통 시각 해석 형식 |
| `timestampformat.*` | 지정하지 않음 | 아래 설명의 문자열·타입 규칙 | 컬럼별 시각 형식 |
| `timezone` | UTC | 아래 설명의 문자열·타입 규칙 | UTC 또는 숫자 offset. 이름 기반 시간대 제외 |

공통 mode·columns·target·row·field·project·column·source·raw 설정은
[READ 공통 옵션](../../read-options/)을 함께 적용합니다. 위 표의 값 목록은 입력 형식이며
아래 제약에서 제한한 값은 해당 reader에서 실행할 수 없습니다. 특히 parallel의 등록된 값 목록이
실제 병렬 처리 지원을 뜻하지 않습니다. view별 상세 설정은 inspect의 options/capabilities도 확인합니다.

## 우선순위와 허용 조합

records는 각 부모 줄의 배열에 적용됩니다. 빈 줄을 제외한 부모 row는 0부터, 원문 물리 줄 번호는 1부터입니다. type·dateformat은 출력 컬럼 이름에 지정합니다. JSON null과 없는 키는 native에서 SQL NULL이며 원래 상태는 envelope·inspect로 구분합니다.

## 옵션 조합 예제

<a id="example-1"></a>

### 1. 숫자 타입과 순차 실행

기본 행 매핑에서 숫자 합계를 확인합니다.

```sql
SELECT COUNT(*) AS N,SUM(v) AS TOTAL
FROM READ('/srv/dfq/sensor.jsonl', 'format=jsonl', 'type.id=LONG',
 'parallel=false') ;
```

반환 컬럼: `N`, `TOTAL`. 반환 행 수: 1.

다음은 처음 최대 3행의 표시입니다. 긴 값은 미리보기로 줄였습니다.

| N | TOTAL |
| --- | --- |
| 5 | 150 |

[SQL 다운로드](/assets/dbms-8.9/dfq/jsonl/01.sql)

<a id="example-2"></a>

### 2. 중첩 배열을 행으로 선택

records는 객체 안의 배열을 행으로 펼칩니다.

```sql
SELECT COUNT(*) AS N,SUM(v) AS TOTAL
FROM READ('/srv/dfq/wrapped.jsonl', 'format=jsonl', 'records=items',
 'type.id=LONG') ;
```

반환 컬럼: `N`, `TOTAL`. 반환 행 수: 1.

다음은 처음 최대 3행의 표시입니다. 긴 값은 미리보기로 줄였습니다.

| N | TOTAL |
| --- | --- |
| 5 | 150 |

[SQL 다운로드](/assets/dbms-8.9/dfq/jsonl/02.sql)

<a id="example-3"></a>

### 3. 중첩 필드와 배열 원소를 투영

중첩 경로와 출력 별칭의 역할을 구분합니다.

```sql
SELECT key,x,first
FROM READ('/srv/dfq/sensor.jsonl', 'format=jsonl', 'project.key=id',
 'project.x=pose.x',
 'project.first=items[0]',
 'type.key=LONG') ORDER BY key LIMIT 3;
```

반환 컬럼: `key`, `x`, `first`. 반환 행 수: 3.

다음은 처음 최대 3행의 표시입니다. 긴 값은 미리보기로 줄였습니다.

| key | x | first |
| --- | --- | --- |
| 1 | 0.5 | 1 |
| 2 | 1.0 | 2 |
| 3 | 1.5 | 3 |

[SQL 다운로드](/assets/dbms-8.9/dfq/jsonl/03.sql)

<a id="example-4"></a>

### 4. 날짜 문자열을 명시 변환

JSON 문자열은 날짜처럼 보여도 자동으로 날짜가 되지 않습니다.

```sql
SELECT id,day
FROM READ('/srv/dfq/sensor.jsonl', 'format=jsonl', 'type.day=DATE',
 'dateformat.day=%Y-%m-%d',
 'timezone=UTC') LIMIT 3;
```

반환 컬럼: `id`, `day`. 반환 행 수: 3.

다음은 처음 최대 3행의 표시입니다. 긴 값은 미리보기로 줄였습니다.

| id | day |
| --- | --- |
| 1 | 2026-11-01 09:00:00 |
| 2 | 2026-11-01 09:00:00 |
| 3 | 2026-11-01 09:00:00 |

[SQL 다운로드](/assets/dbms-8.9/dfq/jsonl/04.sql)

<a id="example-5"></a>

### 5. 부모 한 행의 배열 원소 펼치기

row는 WHERE 적용 전의 0부터 시작하는 원래 부모 행 번호입니다.

```sql
SELECT *
FROM READ('/srv/dfq/sensor.jsonl', 'format=jsonl', 'mode=elements',
 'target=rows',
 'row=0',
 'field=items') ;
```

반환 컬럼: `_SOURCE`, `_TARGET`, `_ROW`, `_TIME_NS`, `_CLOCK`, `DATA`, `_META`, `_REFS`, `_ELEMENT`, `_INDEX`. 반환 행 수: 2.

[SQL 다운로드](/assets/dbms-8.9/dfq/jsonl/05.sql)

<a id="example-6"></a>

### 6. 원문 구조를 envelope로 보존

native 컬럼 대신 선택한 논리 구조를 DATA로 받습니다.

```sql
SELECT DATA
FROM READ('/srv/dfq/sensor.jsonl', 'format=jsonl', 'columns=envelope',
 'target=rows',
 'row=0',
 'field=pose') ;
```

반환 컬럼: `DATA`. 반환 행 수: 1.

다음은 처음 최대 3행의 표시입니다. 긴 값은 미리보기로 줄였습니다.

| DATA |
| --- |
| {"x":0.5} |

[SQL 다운로드](/assets/dbms-8.9/dfq/jsonl/06.sql)

<a id="example-7"></a>

### 7. 압축과 전체 스키마 추론

전체 표본은 prepare 비용을 늘릴 수 있습니다.

```sql
SELECT COUNT(*) AS N,SUM(v) AS TOTAL
FROM READ('/srv/dfq/sensor.jsonl.gz', 'format=jsonl', 'compression=gzip',
 'sample_size=-1',
 'parallel=false') ;
```

반환 컬럼: `N`, `TOTAL`. 반환 행 수: 1.

다음은 처음 최대 3행의 표시입니다. 긴 값은 미리보기로 줄였습니다.

| N | TOTAL |
| --- | --- |
| 5 | 150 |

[SQL 다운로드](/assets/dbms-8.9/dfq/jsonl/07.sql)

<a id="example-8"></a>

### 8. 필드 선택과 원래 행 순번 추가

project와 column은 원래 본문 경로를 기준으로 값을 선택합니다.

```sql
SELECT key,position,original_v
FROM READ('/srv/dfq/sensor.jsonl', 'format=jsonl', 'project.key=id',
 'column.position=meta.row',
 'column.original_v=data.v') ORDER BY key LIMIT 3;
```

반환 컬럼: `key`, `position`, `original_v`. 반환 행 수: 3.

다음은 처음 최대 3행의 표시입니다. 긴 값은 미리보기로 줄였습니다.

| key | position | original_v |
| --- | --- | --- |
| 1 | 0 | 10 |
| 2 | 1 | 20 |
| 3 | 2 | 30 |

[SQL 다운로드](/assets/dbms-8.9/dfq/jsonl/08.sql)

## 오류와 해결

### 지원하지 않는 옵션 사용

```sql
SELECT *
FROM READ('/srv/dfq/sensor.jsonl',
 'format=jsonl',
 'unknown_option=true');
```

예상 오류: `INVALID_OPTION`. 등록되지 않은 옵션은 무시되지 않고 INVALID_OPTION으로 거부됩니다. 옵션표의 이름을 사용합니다.

[오류 SQL 다운로드](/assets/dbms-8.9/dfq/jsonl/09.sql)

### 형식 또는 선택 조건 오류

```sql
SELECT *
FROM READ('/srv/dfq/bad.jsonl',
 'format=jsonl');
```

예상 오류: `CORRUPT_DATA`. 손상된 파일은 정상 빈 결과가 아닙니다. 원본 형식과 파일 내용을 확인합니다.

[오류 SQL 다운로드](/assets/dbms-8.9/dfq/jsonl/10.sql)

## 타입·구조·표현의 상세 규칙

### JSON과 JSONL의 행 매핑

| 입력 | JSON | JSONL |
|---|---|---|
| 객체 | 한 행, 객체의 키가 컬럼 | 해당 줄이 한 행 |
| 최상위 배열 | 원소마다 한 행 | 그 줄의 배열 전체가 한 행 |
| 숫자·문자열·bool·null | 한 행 | 해당 줄이 한 행 |
| 빈 줄 | JSON 공백의 일부 | 행으로 세지 않음 |

서버 파일 경로를 사용합니다. SYS 이외 사용자는 기존 READ 디렉터리 권한을 받아야 합니다.
내용을 보고 형식을 감지하며, 판정이 모호하면 `'format=json'` 또는
`'format=jsonl'`을 지정합니다. `.ndjson`은 JSONL의 확장자 힌트다.

### 행과 컬럼을 만드는 규칙

선택한 행이 모두 객체이면 전체 키를 합쳐 컬럼을 만든다. 키 순서는 파일·행·객체
멤버에서 처음 등장한 순서다. 없는 키와 JSON null은 native 결과에서 SQL NULL입니다.
객체와 다른 값이 섞이면 전체 값을 `"VALUE"` JSON 컬럼 하나로 반환합니다.
빈 배열 등 결과가 0행이거나 빈 객체만 있는 경우에도 VALUE 컬럼으로 설명합니다.

`records` 경로가 없으면 MISSING_VALUE, null 또는 배열 이외 값이면 CORRUPT_DATA다.
빈 배열은 0행입니다. JSON의 명시 records 확장에서는 원래 문서의 parent_row는 0이고
child_index가 배열 순번입니다. JSONL의 parent_row는 빈 줄을 제외한 부모 레코드의
0부터 시작하는 순번입니다. start_line은 빈 줄을 포함한 원문 물리 줄 번호이며 1부터 시작합니다.

자동 컬럼과 지정 project 경로의 타입을 추론합니다. 문자열 `"123"`이나 날짜처럼 보이는
문자열은 그대로 VARCHAR/TEXT로 유지합니다. 숫자는 LONG·ULONG·DECIMAL로 정확하게
표현하고, 호환되지 않는 혼합 값이나 DECIMAL 정밀도 65·소수 자릿수 30을 넘는 숫자는
JSON으로 보존합니다. 서로 다른 정수 폭의 조합도 DECIMAL로 합쳐질 수 있습니다.
DOUBLE/FLOAT는 명시 변환할 때 사용합니다. 정수 NULL 예약값은 자동 추론 시 DECIMAL로
보존하며, 해당 정수 타입을 명시했을 때 표현할 수 없으면 오류다.

`type.*`, `dateformat.*`, `timestampformat.*`의 이름은 출력 컬럼 이름과 일치시킨다.
project를 사용하면 원본 경로 대신 출력 별칭을 지정합니다. timezone은 UTC/Z 또는
숫자 offset이며, 이름 기반 시간대는 지원하지 않습니다.
날짜·시각 명시 변환은 UTC 변환 후1970년 이후인 기존 엔진 나노초 시각 범위를 따릅니다.
과거 연도 데이터는 LONG 또는 원본 문자열로 읽습니다.

기본 `sample_size=-1`은 전체 레코드를 살펴 구조와 타입을 결정합니다. 따라서 LIMIT이
작아도 최초 구조 탐색은 파일 전체를 읽을 수 있습니다. `'sample_size=1000'`처럼 양수로
줄이면 표본 밖의 새 키나 호환되지 않는 원본 타입을 실행 중 SCHEMA_CHANGED로 알린다.
명시한 DATE 등의 변환 규칙에 맞지 않는 값은 타입 구조 변경과 구분해 도메인 오류로 처리합니다.
sniff의 READ_SQL로 같은 해석을 재생할 수 있으며, SQL 셀 한도를 넘는 큰 요청은 READ_TOKEN을 사용합니다.

기본은 오류 즉시 중단입니다. skip은 경계가 확인된 JSON 배열 원소 또는 JSONL 한 줄에
적용합니다. JSONL records 확장에서는 한 자식이라도 변환에 실패하면 부모 줄의 모든
자식을 제외합니다. 단일 JSON 루트의 오류, 경계가 깨진 구조, 인코딩·자원·취소 오류는
skip으로 숨기지 않습니다. DECODED_OFFSET은 디코딩한 UTF-8 기준이며 압축 파일의
저장 바이트 위치로 해석하면 안 됩니다.

### 여러 파일과 공통 옵션

동일 형식의 여러 파일과 glob을 지원합니다. 기본 union_by_name=true이며 false는 파일별
키 집합이 다르면 오류다. 중복 경로는 허용하지 않습니다. auto 호출 하나에서 JSON과
JSONL이 섞이면 별도 READ를 UNION ALL합니다. strong은 모든 파일의 snapshot을 첫 결과
전에 고정하며 최대 256파일입니다. 일반 source 집합 한도는 4096파일입니다.

JSON의 document target은 루트 전체를 한 값으로 제공합니다. JSONL은 하나의 문서가
아니므로 document target을 지원하지 않습니다. DATA의 JSON null은 유효한 JSON 값이며
SQL NULL과 구분합니다. envelope metadata에서는 missing/null/present도 구분합니다.

일반 문자열은 크기에 따라 VARCHAR/TEXT를 사용합니다. native JSON은 32,768바이트까지이며,
이를 넘는 구조·숫자나 native 문자열로 표현할 수 없는 NUL 포함 값은 명시 오류와
envelope reference 또는 raw 추출 경로를 사용합니다. 원본 숫자 토큰은 envelope·canonical
raw에서 유지하며 JSON 전용 encoding은 json_number_lexeme다.

max_record_bytes 기본은 67,108,864바이트이며 양수로 변경할 수 있습니다. 실제 메모리는
MAX_QPX_MEM 등 실행 예산에도 제한됩니다. 중첩 깊이 64, 경로 32KiB, 컬럼 4096 한도를
적용합니다. JSON rows의 큰 배열은 파일 전체 DOM을 만들지 않고 원소 단위로 읽습니다.

JSON·JSONL의 rejects는 원문 레코드 단위다. PATH와 START_LINE·DECODED_OFFSET으로 위치를 찾는다. 공통 결과의 COLUMN_INDEX·COLUMN_NAME은 현재 JSON에서 제공하지 않아 NULL입니다.

rejects의 PATH는 원문에서 레코드 위치를 표시하는 메타데이터다. `records=`와 `project.*=`의 입력 경로 문법과 구분합니다.


## 관련 문서

- [구조와 컬럼 확인](../../inspect/)
- [구조화된 값과 원문 추출](../../extract/)
- [권한과 운영](../../operations/)
