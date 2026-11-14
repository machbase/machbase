---
type: docs
title: '12.4.5 PARQUET'
weight: 50
toc: true
---

선언된 컬럼 타입과 중첩 STRUCT/LIST를 보존해 조회합니다. 샘플은 id,v,label,day,pose,items 6개 필드와 5행입니다.

## 실습 준비

[실습 파일 묶음](/assets/dbms-8.9/dfq/samples.zip)을 **DB 서버**의 `/srv/dfq`에 풉니다.
경로가 다르면 SQL의 `/srv/dfq`를 실제 서버 경로로 바꿉니다. 접속과 권한 준비는
[시작하기](../../getting-started/)를 참고합니다. SQL마다 별도의 준비 명령 없이 같은 입력을 사용합니다.
센서 샘플의 id=1~5, v=id×10이므로 COUNT=5, SUM(id)=15, SUM(v)=150입니다.
LeRobot 샘플은 이 센서 파일과 별개입니다.

## 작업별 빠른 찾기

| 목적 | 조합한 설정 | 예제 |
|---|---|---|
| 원본 선언 타입과 집계 | `format`, `parallel` | [예제 1](#example-1) |
| 중첩 스칼라 투영 | `format`, `project.key`, `project.x`, `project.first` | [예제 2](#example-2) |
| 파일 출처와 숫자 carrier 지정 | `format`, `filename`, `type.id` | [예제 3](#example-3) |
| 같은 스키마의 여러 파일 조회 | `format`, `sources`, `parallel` | [예제 4](#example-4) |
| 부모 NULL과 중첩 구조 보존 | `format`, `columns`, `target`, `row`, `field` | [예제 5](#example-5) |
| 실제 반환 컬럼과 타입 확인 | `format`, `mode`, `view` | [예제 6](#example-6) |
| 배열 원소 펼치기 | `format`, `mode`, `target`, `row`, `field` | [예제 7](#example-7) |

## 전체 포맷 옵션

| 옵션 | 기본값 | 허용값·범위 | 역할 |
|---|---|---|---|
| `sources` | 지정하지 않음 | CSV 인용을 사용하는 쉼표 목록 | 순서 있는 파일 목록. 위치형·source와 혼용 금지 |
| `names` | 지정하지 않음 | CSV 인용을 사용하는 쉼표 목록 | 원본 순서대로 출력 컬럼명 지정 |
| `type.*` | 지정하지 않음 | VARCHAR,TEXT,SHORT,INTEGER,LONG,USHORT,UINTEGER,ULONG,FLOAT,DOUBLE,BOOLEAN,DECIMAL,NUMERIC,DATE,DATETIME,TIMESTAMP,TIME,JSON,BINARY,VARBINARY | 컬럼별 SQL 타입. * 위치에 컬럼명 사용 |
| `filename` | false | true / false | 출처 파일명 컬럼 추가 |
| `parallel` | auto | auto,false | 실행 정책. 아래 지원 조합 확인 |
| `on_error` | error | error | error만 지원. 오류 행 건너뛰기 미지원 |
| `union_by_name` | false | false만 지원 | 여러 입력의 컬럼 결합 정책. 아래 reader별 제약 확인 |

공통 mode·columns·target·row·field·project·column·source·raw 설정은
[READ 공통 옵션](../../read-options/)을 함께 적용합니다. 위 표의 값 목록은 입력 형식이며
아래 제약에서 제한한 값은 해당 reader에서 실행할 수 없습니다. 특히 parallel의 등록된 값 목록이
실제 병렬 처리 지원을 뜻하지 않습니다. view별 상세 설정은 inspect의 options/capabilities도 확인합니다.

## 우선순위와 허용 조합

parallel은 auto/false의 동기 실행입니다. union_by_name=true와 on_error=skip은 지원하지 않습니다. 여러 파일은 이름·순서·논리 타입·nullable·의미 metadata가 같아야 합니다. 없는 중첩 필드는 오류이며 부모 NULL 아래의 선언된 자식은 SQL NULL입니다.

## 옵션 조합 예제

<a id="example-1"></a>

### 1. 원본 선언 타입과 집계

파일의 선언 스키마와 내부 압축을 사용합니다.

```sql
SELECT COUNT(*) AS N,SUM(v) AS TOTAL
FROM READ('/srv/dfq/sensor.parquet', 'format=parquet', 'parallel=false') ;
```

반환 컬럼: `N`, `TOTAL`. 반환 행 수: 1.

다음은 처음 최대 3행의 표시입니다. 긴 값은 미리보기로 줄였습니다.

| N | TOTAL |
| --- | --- |
| 5 | 150 |

[SQL 다운로드](/assets/dbms-8.9/dfq/parquet/01.sql)

<a id="example-2"></a>

### 2. 중첩 스칼라 투영

선언된 STRUCT와 LIST의 필드를 선택합니다.

```sql
SELECT key,x,first
FROM READ('/srv/dfq/sensor.parquet', 'format=parquet', 'project.key=id',
 'project.x=pose.x',
 'project.first=items[0]') ORDER BY key LIMIT 3;
```

반환 컬럼: `key`, `x`, `first`. 반환 행 수: 3.

다음은 처음 최대 3행의 표시입니다. 긴 값은 미리보기로 줄였습니다.

| key | x | first |
| --- | --- | --- |
| 1 | 0.5 | 1 |
| 2 | 1.0 | 2 |
| 3 | 1.5 | 3 |

[SQL 다운로드](/assets/dbms-8.9/dfq/parquet/02.sql)

<a id="example-3"></a>

### 3. 파일 출처와 숫자 carrier 지정

가상 filename 컬럼과 원래 컬럼의 이름 충돌을 피합니다.

```sql
SELECT id,v,filename
FROM READ('/srv/dfq/sensor.parquet', 'format=parquet', 'filename=true',
 'type.id=LONG') LIMIT 3;
```

반환 컬럼: `id`, `v`, `filename`. 반환 행 수: 3.

다음은 처음 최대 3행의 표시입니다. 긴 값은 미리보기로 줄였습니다.

| id | v | filename |
| --- | --- | --- |
| 1 | 10 | /srv/dfq/sensor.parquet |
| 2 | 20 | /srv/dfq/sensor.parquet |
| 3 | 30 | /srv/dfq/sensor.parquet |

[SQL 다운로드](/assets/dbms-8.9/dfq/parquet/03.sql)

<a id="example-4"></a>

### 4. 같은 스키마의 여러 파일 조회

컬럼 이름·순서·타입·nullable과 의미 메타데이터가 같아야 합니다.

```sql
SELECT COUNT(*) AS N,SUM(v) AS TOTAL
FROM READ('format=parquet', 'sources=/srv/dfq/part-1.parquet,/srv/dfq/part-2.parquet',
 'parallel=false') ;
```

반환 컬럼: `N`, `TOTAL`. 반환 행 수: 1.

다음은 처음 최대 3행의 표시입니다. 긴 값은 미리보기로 줄였습니다.

| N | TOTAL |
| --- | --- |
| 10 | 300 |

[SQL 다운로드](/assets/dbms-8.9/dfq/parquet/04.sql)

<a id="example-5"></a>

### 5. 부모 NULL과 중첩 구조 보존

선택한 객체 구조를 DATA로 읽습니다.

```sql
SELECT DATA
FROM READ('/srv/dfq/sensor.parquet', 'format=parquet', 'columns=envelope',
 'target=rows',
 'row=0',
 'field=pose') ;
```

반환 컬럼: `DATA`. 반환 행 수: 1.

다음은 처음 최대 3행의 표시입니다. 긴 값은 미리보기로 줄였습니다.

| DATA |
| --- |
| {"x":0.5} |

[SQL 다운로드](/assets/dbms-8.9/dfq/parquet/05.sql)

<a id="example-6"></a>

### 6. 실제 반환 컬럼과 타입 확인

바깥 SELECT의 표현식이 아닌 READ 자체의 결과 스키마입니다.

```sql
SELECT COLUMN_NAME,SQL_TYPE
FROM READ('/srv/dfq/sensor.parquet', 'format=parquet', 'mode=inspect',
 'view=columns') ORDER BY COLUMN_ORDINAL;
```

반환 컬럼: `COLUMN_NAME`, `SQL_TYPE`. 반환 행 수: 6.

다음은 처음 최대 3행의 표시입니다. 긴 값은 미리보기로 줄였습니다.

| COLUMN_NAME | SQL_TYPE |
| --- | --- |
| id | LONG |
| v | LONG |
| label | TEXT |

[SQL 다운로드](/assets/dbms-8.9/dfq/parquet/06.sql)

<a id="example-7"></a>

### 7. 배열 원소 펼치기

선택한 부모 행의 배열을 펼칩니다.

```sql
SELECT *
FROM READ('/srv/dfq/sensor.parquet', 'format=parquet', 'mode=elements',
 'target=rows',
 'row=0',
 'field=items') ;
```

반환 컬럼: `_SOURCE`, `_TARGET`, `_ROW`, `_TIME_NS`, `_CLOCK`, `DATA`, `_META`, `_REFS`, `_ELEMENT`, `_INDEX`. 반환 행 수: 2.

[SQL 다운로드](/assets/dbms-8.9/dfq/parquet/07.sql)

## 오류와 해결

### 지원하지 않는 옵션 사용

```sql
SELECT *
FROM READ('/srv/dfq/sensor.parquet',
 'format=parquet',
 'unknown_option=true');
```

예상 오류: `INVALID_OPTION`. 등록되지 않은 옵션은 무시되지 않고 INVALID_OPTION으로 거부됩니다. 옵션표의 이름을 사용합니다.

[오류 SQL 다운로드](/assets/dbms-8.9/dfq/parquet/08.sql)

### 형식 또는 선택 조건 오류

```sql
SELECT *
FROM READ('/srv/dfq/bad.parquet',
 'format=parquet');
```

예상 오류: `CORRUPT_DATA`. 손상된 파일은 정상 빈 결과가 아닙니다. 원본 형식과 파일 내용을 확인합니다.

[오류 SQL 다운로드](/assets/dbms-8.9/dfq/parquet/09.sql)

## 타입·구조·표현의 상세 규칙

### 원본 타입과 SQL 반환 타입

| Parquet/Arrow 저장 타입 | 기본 native SQL carrier | envelope의 정규값 |
|---|---|---|
| BOOLEAN | INTEGER 0/1 | JSON boolean |
| signed 8/16, 32, 64bit 정수 | SHORT, INTEGER, LONG | 정확한 십진 문자열 |
| unsigned 8/16, 32, 64bit 정수 | USHORT, UINTEGER, ULONG | 정확한 십진 문자열 |
| FLOAT16/FLOAT32, FLOAT64 | FLOAT, DOUBLE | 유한값은 JSON 숫자, 비유한값은 `NaN`·`Infinity`·`-Infinity` 문자열 |
| STRING | VARCHAR | UTF-8 문자열 |
| BINARY·FIXED_LEN_BYTE_ARRAY | BINARY | base64 문자열 |
| DECIMAL | 지원 정밀도 범위의 DECIMAL | scale을 보존하는 정확한 십진 문자열 |
| DATE | DATETIME | 원본 단위의 정확한 tick 문자열 |
| TIMESTAMP·INT96 | DATETIME | 원본 단위의 정확한 tick 문자열 |
| TIME | 자정부터 나노초 LONG | 원본 단위의 정확한 tick 문자열 |
| STRUCT | JSON | 객체 |
| LIST | JSON | 배열 |
| MAP | JSON | `[{"key":...,"value":...},...]` entry 배열 |

기존 SQL 테이블 함수 `READ()`로 서버의 Parquet 파일을 조회합니다. 명시 `format=parquet`와 파일 magic 기반 자동 감지를 지원하며 확장자가 다른 파일도 실제 내용으로 판별합니다. 자동 감지는 선두 `PAR1`·`PARE`뿐 아니라 인가된 파일의 footer magic과 길이도 확인하므로, 같은 인쇄 가능한 문자열로 시작하는 정상 CSV를 Parquet로 가로채지 않습니다. 기본 논리 대상은 `rows`, 기본 데이터 반환은 native SQL 컬럼입니다.

Parquet 쓰기·암호화 파일·원격 저장소·Hive partition dataset·Arrow IPC·Feather SQL reader는 제공하지 않습니다. 필요한 Arrow 코어를 링크하더라도 다른 Arrow 파일 형식을 자동 지원하는 것은 아닙니다.

경로는 클라이언트가 아닌 서버 파일시스템 기준입니다. SYS 이외 사용자는 기존 READ directory grant 정책을 따릅니다. 브리지는 인가된 `qpxReadSource`를 통해 읽고, 파일 이름을 별도로 열어 권한 검사를 우회하지 않습니다.

`list`·`schema`·`inspect`는 현재 READ의 공통 결과 스키마와 진단 형식을 사용합니다. `parquet.standard@1` profile을 명시할 수도 있습니다.

원본 타입·nullable·precision·scale·시간 단위·timezone은 타입 definitions와 metadata에 보존합니다. dictionary는 저장 값 타입으로 읽고, 알 수 없는 확장은 지원 가능한 storage type으로 읽으면서 원래 extension metadata를 보존합니다. storage type 자체를 안전하게 표현할 수 없으면 오류를 반환합니다.

MAP은 객체로 변환하지 않습니다. 키의 원래 타입, entry 순서와 중복 키를 유지합니다. 중첩 필드는 자동 평탄화하지 않으며 원래 이름·대소문자를 보존합니다. SQL 이름이 너무 길거나 대소문자를 무시했을 때 충돌하면 native 조회를 거부합니다. 명시 `names=`로 바꾸거나 envelope를 사용합니다.

SQL NULL은 빈 문자열·빈 BINARY·빈 LIST·빈 MAP과 구별합니다. native FLOAT/DOUBLE은 NaN·무한대·음수 0을 유지하되 DB가 NULL로 예약한 실제 비트 패턴과 범위 초과는 거부합니다. 정수의 NULL 예약값도 정상 값으로 조용히 반환하지 않습니다.

native DATE/TIMESTAMP는 기존 READ 시간 정책에 따라 0 이상이며 SQL 나노초 범위 안이어야 합니다. 음수 epoch, 단위 변환 오버플로는 `NATIVE_VALUE_UNREPRESENTABLE`입니다. envelope에서는 원래 tick을 그대로 조회할 수 있습니다. TIME은 0~86,399,999,999,999 나노초의 LONG이며 원본 `time` 타입과 단위를 별도 보존합니다.

엔진 DECIMAL 최대 정밀도(65)보다 크거나 지원 scale(0~30)을 벗어나는 DECIMAL은 기본 native prepare에서 오류다. envelope 또는 명시 `type.amount=TEXT`·`type.amount=JSON`으로 정확한 십진 표현을 읽습니다. 원본 DECIMAL metadata와 명시 SQL carrier의 precision/scale은 서로 분리됩니다.

중첩 native JSON에는 기존 SQL JSON 셀 크기 한도가 적용됩니다. 더 큰 중첩값을 native로 반환하려면 해당 최상위 컬럼에 `type.<컬럼>=TEXT`를 지정합니다. envelope·탐색·canonical raw도 statement 작업 메모리와 READ 깊이·값 크기 한도를 따릅니다.

명시 파일 목록은 인자 순서를, glob은 공통 READ가 준비한 정렬 순서를 유지합니다. 파일별 컬럼 이름·순서·논리 타입·nullable·의미 metadata가 다르면 `SCHEMA_MISMATCH`로 거부합니다. 자동 이름 재정렬·타입 승격·누락 컬럼 NULL 채우기는 수행하지 않습니다. 최대 4,096개 파일을 허용하며 strong snapshot 다중 파일은 최대 256개다.

공통 strict path를 사용해 중첩값을 선택합니다. 인용이 필요한 필드 이름은 기존 READ 경로 quote 규칙을 따릅니다.

대상 없는 stored raw는 원본 파일 전체 바이트다. 논리 셀은 압축된 page와 분산된 column chunk에서 조립되므로 연속 stored 바이트 범위로 제공하지 않습니다. 논리값 raw는 canonical JSON을 사용합니다. 논리 배열 index와 물리 파일 offset을 혼합하지 않습니다.

비압축, Snappy·Gzip·Brotli·Zstd·LZ4 계열을 정적 패키지에 포함합니다. LZO·암호화는 `UNSUPPORTED_FORMAT`, 손상된 footer/page는 `CORRUPT_DATA`로 보고합니다. I/O·권한·취소·메모리 예산 실패는 원래 진단을 보존합니다.

strong 실행은 private snapshot을 JOIN 재스캔 동안 보유합니다. weak 실행은 Arrow 배치 캐시에 값이 있어도 행을 내보내기 전후 source 변경을 검사하고 취소를 확인합니다.

## 관련 문서

- [구조와 컬럼 확인](../../inspect/)
- [구조화된 값과 원문 추출](../../extract/)
- [권한과 운영](../../operations/)
