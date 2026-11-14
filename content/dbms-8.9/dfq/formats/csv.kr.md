---
type: docs
title: '12.4.1 CSV'
weight: 10
toc: true
---

구분자·헤더·인코딩과 컬럼 타입을 조합해 행을 읽습니다. 샘플은 id,v,label,day 4개 컬럼과 5행입니다.

## 실습 준비

[실습 파일 묶음](/assets/dbms-8.9/dfq/samples.zip)을 **DB 서버**의 `/srv/dfq`에 풉니다.
경로가 다르면 SQL의 `/srv/dfq`를 실제 서버 경로로 바꿉니다. 접속과 권한 준비는
[시작하기](../../getting-started/)를 참고합니다. SQL마다 별도의 준비 명령 없이 같은 입력을 사용합니다.
센서 샘플의 id=1~5, v=id×10이므로 COUNT=5, SUM(id)=15, SUM(v)=150입니다.
LeRobot 샘플은 이 센서 파일과 별개입니다.

## 작업별 빠른 찾기

| 목적 | 조합한 설정 | 예제 |
|---|---|---|
| 헤더와 숫자 타입 고정 | `format`, `header`, `type.id`, `type.v` | [예제 1](#example-1) |
| 헤더 없이 이름과 타입 지정 | `format`, `header`, `names`, `type.id`, `type.v` | [예제 2](#example-2) |
| 날짜 형식과 전체 표본 지정 | `format`, `type.day`, `dateformat.day`, `sample_size` | [예제 3](#example-3) |
| 필드 선택과 별칭 타입 지정 | `format`, `project.key`, `project.reading`, `type.id` | [예제 4](#example-4) |
| 원래 컬럼에 파일과 물리 줄 추가 | `format`, `column.source_file`, `column.line_no` | [예제 5](#example-5) |
| 여러 파일을 이름 기준으로 결합 | `format`, `sources`, `union_by_name`, `filename` | [예제 6](#example-6) |
| gzip과 고정 타입으로 조회 | `format`, `compression`, `type.v`, `parallel` | [예제 7](#example-7) |
| 메모리와 반환 타입을 고려해 TEXT 지정 | `format`, `type.label`, `auto_detect`, `header` | [예제 8](#example-8) |
| 소수점·천 단위와 명시 타입 조합 | `format`, `delimiter`, `header`, `type.id`, `type.v`, `decimal_separator`, `thousands` | [예제 9](#example-9) |
| NULL 표식·인용 NULL·누락 필드 조합 | `format`, `header`, `type.id`, `type.v`, `type.label`, `null_values`, `allow_quoted_nulls`, `null_padding`, `force_not_null` | [예제 10](#example-10) |
| 주석·앞줄 건너뛰기·헤더 없는 타입 조합 | `format`, `skip`, `comment`, `header`, `names`, `all_varchar`, `type.v` | [예제 11](#example-11) |

## 전체 포맷 옵션

| 옵션 | 기본값 | 허용값·범위 | 역할 |
|---|---|---|---|
| `parallel` | auto | auto,true,false | 실행 정책. 아래 지원 조합 확인 |
| `threads` | 지정하지 않음 | 1~32 | 작업자 수 상한. reader에 따라 병렬 작업자를 만들지 않음 |
| `header` | true | true / false | 첫 논리 레코드를 헤더로 사용 |
| `names` | 지정하지 않음 | CSV 인용을 사용하는 쉼표 목록 | 원본 순서대로 출력 컬럼명 지정 |
| `delimiter` | 쉼표 | 아래 설명의 문자열·타입 규칙 | 구분 문자 하나. TSV는 탭 고정 |
| `encoding` | auto | auto,utf-8,cp949,latin-1,utf-16 | 입력 문자를 엄격하게 디코딩 |
| `null_values` | 빈 값 | CSV 인용을 사용하는 쉼표 목록 | 정확하게 일치하는 비인용 NULL 표식 목록 |
| `type.*` | 지정하지 않음 | string,int64,uint64,float64,bool,int16,int32,uint16,uint32,float32,VARCHAR,LONG,BIGINT,ULONG,UBIGINT,SHORT,SMALLINT,INTEGER,INT,USHORT,USMALLINT,UINTEGER,FLOAT,REAL,DOUBLE,BOOLEAN,DECIMAL,NUMERIC,date,datetime,TIMESTAMP,TIME,TEXT | 컬럼별 SQL 타입. * 위치에 컬럼명 사용 |
| `auto_detect` | true | true / false | 헤더·구분자·타입 추론 |
| `all_varchar` | false | true / false | 추론 타입 대신 VARCHAR 사용. 명시 type은 우선 |
| `sample_size` | 20480 | 아래 설명의 문자열·타입 규칙 | 양의 레코드 수 또는 -1(전체) |
| `quote` | 큰따옴표 | 아래 설명의 문자열·타입 규칙 | 인용 문자. 빈 값은 인용 해제 |
| `escape` | 큰따옴표 | 아래 설명의 문자열·타입 규칙 | escape 문자. 빈 값은 escape 해제 |
| `dateformat` | 지정하지 않음 | 아래 설명의 문자열·타입 규칙 | 공통 날짜 해석 형식 |
| `dateformat.*` | 지정하지 않음 | 아래 설명의 문자열·타입 규칙 | 컬럼별 날짜 형식, 공통 형식보다 우선 |
| `timestampformat.*` | 지정하지 않음 | 아래 설명의 문자열·타입 규칙 | 컬럼별 시각 형식 |
| `timestampformat` | 지정하지 않음 | 아래 설명의 문자열·타입 규칙 | 공통 시각 해석 형식 |
| `timezone` | UTC | 아래 설명의 문자열·타입 규칙 | UTC 또는 숫자 offset. 이름 기반 시간대 제외 |
| `auto_type_candidates` | 지정하지 않음 | CSV 인용을 사용하는 쉼표 목록 | 타입 추론 후보군. 문자열 fallback은 별도 |
| `on_error` | error | error,skip | 복구 가능한 완전한 행의 변환 오류 처리. 손상 전체를 무시하는 기능 아님 |
| `null_padding` | false | true / false | 부족한 뒤쪽 필드를 SQL NULL로 채움 |
| `allow_quoted_nulls` | false | true / false | 인용 필드에도 NULL 표식 적용 |
| `force_not_null` | 지정하지 않음 | CSV 인용을 사용하는 쉼표 목록 | 현재 값이 NULL 표식과 일치해도 NULL로 바꾸지 않는 컬럼 |
| `decimal_separator` | . | 아래 설명의 문자열·타입 규칙 | 숫자 소수점 문자 |
| `thousands` | 지정하지 않음 | 아래 설명의 문자열·타입 규칙 | 숫자 천 단위 구분 문자 |
| `comment` | 지정하지 않음 | 아래 설명의 문자열·타입 규칙 | 인용 밖 물리 줄의 주석 시작 문자 |
| `skip` | 0 | 0~9223372036854775807 | 헤더 감지 전 건너뛸 물리 줄 수 |
| `strict_mode` | true | true / false | 잘못된 인용에 대한 엄격한 처리 |
| `compression` | auto | auto,none,gzip,zstd | 외부 파일 압축 형식 |
| `sources` | 지정하지 않음 | CSV 인용을 사용하는 쉼표 목록 | 순서 있는 파일 목록. 위치형·source와 혼용 금지 |
| `union_by_name` | false | true / false | 여러 입력의 컬럼 결합 정책. 아래 reader별 제약 확인 |
| `filename` | false | true / false | 출처 파일명 컬럼 추가 |

공통 mode·columns·target·row·field·project·column·source·raw 설정은
[READ 공통 옵션](../../read-options/)을 함께 적용합니다. 위 표의 값 목록은 입력 형식이며
아래 제약에서 제한한 값은 해당 reader에서 실행할 수 없습니다. 특히 parallel의 등록된 값 목록이
실제 병렬 처리 지원을 뜻하지 않습니다. view별 상세 설정은 inspect의 options/capabilities도 확인합니다.

## 우선순위와 허용 조합

`names`는 `header=false`와 조합합니다. `type.*`는 원본 입력 컬럼 이름에 지정합니다. 자동 감지에서는 미지정 header·delimiter·type을 추정하며, 표의 header 기본 true는 자동 감지를 끈 경우입니다. 명시 type은 all_varchar와 자동 추정보다 우선합니다. type을 실행 중 조용히 넓히지 않습니다. 날짜는 전역 형식보다 컬럼별 형식을 우선합니다.

## 옵션 조합 예제

<a id="example-1"></a>

### 1. 헤더와 숫자 타입 고정

헤더를 명시하고 숫자 합계를 정확하게 계산합니다.

```sql
SELECT COUNT(*) AS N,SUM(v) AS TOTAL
FROM READ('/srv/dfq/sensor.csv', 'format=csv', 'header=true',
 'type.id=LONG',
 'type.v=LONG') ;
```

반환 컬럼: `N`, `TOTAL`. 반환 행 수: 1.

다음은 처음 최대 3행의 표시입니다. 긴 값은 미리보기로 줄였습니다.

| N | TOTAL |
| --- | --- |
| 5 | 150 |

[SQL 다운로드](/assets/dbms-8.9/dfq/csv/01.sql)

<a id="example-2"></a>

### 2. 헤더 없이 이름과 타입 지정

헤더가 없는 입력의 첫 행을 데이터로 보존합니다.

```sql
SELECT id,v
FROM READ('/srv/dfq/no-header.csv', 'format=csv', 'header=false',
 'names=id,v,label,day',
 'type.id=LONG',
 'type.v=LONG') ORDER BY id LIMIT 3;
```

반환 컬럼: `id`, `v`. 반환 행 수: 3.

다음은 처음 최대 3행의 표시입니다. 긴 값은 미리보기로 줄였습니다.

| id | v |
| --- | --- |
| 1 | 10 |
| 2 | 20 |
| 3 | 30 |

[SQL 다운로드](/assets/dbms-8.9/dfq/csv/02.sql)

<a id="example-3"></a>

### 3. 날짜 형식과 전체 표본 지정

날짜를 문자열로 두지 않고 지정 형식으로 변환합니다.

```sql
SELECT id,day
FROM READ('/srv/dfq/sensor.csv', 'format=csv', 'type.day=DATE',
 'dateformat.day=%Y-%m-%d',
 'sample_size=-1') LIMIT 3;
```

반환 컬럼: `id`, `day`. 반환 행 수: 3.

다음은 처음 최대 3행의 표시입니다. 긴 값은 미리보기로 줄였습니다.

| id | day |
| --- | --- |
| 1 | 2026-11-01 09:00:00 |
| 2 | 2026-11-01 09:00:00 |
| 3 | 2026-11-01 09:00:00 |

[SQL 다운로드](/assets/dbms-8.9/dfq/csv/03.sql)

<a id="example-4"></a>

### 4. 필드 선택과 별칭 타입 지정

CSV/TSV는 type에 원본 입력 컬럼 이름을 사용하고, project는 출력 별칭을 정합니다.

```sql
SELECT key,reading
FROM READ('/srv/dfq/sensor.csv', 'format=csv', 'project.key=id',
 'project.reading=v',
 'type.id=LONG') ORDER BY key LIMIT 3;
```

반환 컬럼: `key`, `reading`. 반환 행 수: 3.

다음은 처음 최대 3행의 표시입니다. 긴 값은 미리보기로 줄였습니다.

| key | reading |
| --- | --- |
| 1 | 10 |
| 2 | 20 |
| 3 | 30 |

[SQL 다운로드](/assets/dbms-8.9/dfq/csv/04.sql)

<a id="example-5"></a>

### 5. 원래 컬럼에 파일과 물리 줄 추가

논리 행과 물리 줄 번호는 인용 개행·헤더 때문에 다를 수 있습니다.

```sql
SELECT id,source_file,line_no
FROM READ('/srv/dfq/sensor.csv', 'format=csv', 'column.source_file=meta.source',
 'column.line_no=meta.csv.start_line') LIMIT 3;
```

반환 컬럼: `id`, `source_file`, `line_no`. 반환 행 수: 3.

다음은 처음 최대 3행의 표시입니다. 긴 값은 미리보기로 줄였습니다.

| id | source_file | line_no |
| --- | --- | --- |
| 1 | /srv/dfq/sensor.csv | 2 |
| 2 | /srv/dfq/sensor.csv | 3 |
| 3 | /srv/dfq/sensor.csv | 4 |

[SQL 다운로드](/assets/dbms-8.9/dfq/csv/05.sql)

<a id="example-6"></a>

### 6. 여러 파일을 이름 기준으로 결합

source와 sources를 함께 쓰지 않습니다.

```sql
SELECT COUNT(*) AS N,SUM(v) AS TOTAL
FROM READ('format=csv', 'sources=/srv/dfq/part-1.csv,/srv/dfq/part-2.csv',
 'union_by_name=true',
 'filename=true') ;
```

반환 컬럼: `N`, `TOTAL`. 반환 행 수: 1.

다음은 처음 최대 3행의 표시입니다. 긴 값은 미리보기로 줄였습니다.

| N | TOTAL |
| --- | --- |
| 10 | 300 |

[SQL 다운로드](/assets/dbms-8.9/dfq/csv/06.sql)

<a id="example-7"></a>

### 7. gzip과 고정 타입으로 조회

압축 입력의 해석과 숫자 타입을 명시하고 순차 실행합니다.

```sql
SELECT COUNT(*) AS N,SUM(v) AS TOTAL
FROM READ('/srv/dfq/sensor.csv.gz', 'format=csv', 'compression=gzip',
 'type.v=LONG',
 'parallel=false') ;
```

반환 컬럼: `N`, `TOTAL`. 반환 행 수: 1.

다음은 처음 최대 3행의 표시입니다. 긴 값은 미리보기로 줄였습니다.

| N | TOTAL |
| --- | --- |
| 5 | 150 |

[SQL 다운로드](/assets/dbms-8.9/dfq/csv/07.sql)

<a id="example-8"></a>

### 8. 메모리와 반환 타입을 고려해 TEXT 지정

TEXT 명시는 자동 감지보다 우선합니다. LENGTH는 바이트 길이입니다.

```sql
SELECT id,LENGTH(label) AS BYTES
FROM READ('/srv/dfq/sensor.csv', 'format=csv', 'type.label=TEXT',
 'auto_detect=false',
 'header=true') LIMIT 3;
```

반환 컬럼: `id`, `BYTES`. 반환 행 수: 3.

다음은 처음 최대 3행의 표시입니다. 긴 값은 미리보기로 줄였습니다.

| id | BYTES |
| --- | --- |
| 1 | 8 |
| 2 | 8 |
| 3 | 8 |

[SQL 다운로드](/assets/dbms-8.9/dfq/csv/08.sql)

<a id="example-9"></a>

### 9. 소수점·천 단위와 명시 타입 조합

구분자와 숫자의 소수점·천 단위 문자를 별도로 지정합니다. 천 단위는 엄격한 세 자리 그룹 규칙입니다.

```sql
SELECT COUNT(*) AS N,SUM(v) AS TOTAL
FROM READ('/srv/dfq/locale.csv',
 'format=csv',
 'delimiter=;',
 'header=true',
 'type.id=LONG',
 'type.v=DOUBLE',
 'decimal_separator=,
 ',
 'thousands=.');
```

반환 컬럼: `N`, `TOTAL`. 반환 행 수: 1.

다음은 처음 최대 3행의 표시입니다. 긴 값은 미리보기로 줄였습니다.

| N | TOTAL |
| --- | --- |
| 2 | 3234.75 |

[SQL 다운로드](/assets/dbms-8.9/dfq/csv/09.sql)

<a id="example-10"></a>

### 10. NULL 표식·인용 NULL·누락 필드 조합

비인용 NULL과 인용 NULL 모두 표식으로 읽고, 짧은 마지막 행의 누락 label도 SQL NULL로 채웁니다. 실제 빈 문자열과 구분합니다.

```sql
SELECT id,label
FROM READ('/srv/dfq/nulls.csv',
 'format=csv',
 'header=true',
 'type.id=LONG',
 'type.v=LONG',
 'type.label=TEXT',
 'null_values=NULL',
 'allow_quoted_nulls=true',
 'null_padding=true',
 'force_not_null=id') ORDER BY id;
```

반환 컬럼: `id`, `label`. 반환 행 수: 3.

다음은 처음 최대 3행의 표시입니다. 긴 값은 미리보기로 줄였습니다.

| id | label |
| --- | --- |
| 1 | NULL |
| 2 | NULL |
| 3 | NULL |

[SQL 다운로드](/assets/dbms-8.9/dfq/csv/10.sql)

<a id="example-11"></a>

### 11. 주석·앞줄 건너뛰기·헤더 없는 타입 조합

물리 첫 줄을 건너뛰고 주석 줄을 제외합니다. 나머지는 문자열로 읽되 v만 명시 LONG으로 고정합니다.

```sql
SELECT COUNT(*) AS N,SUM(v) AS TOTAL
FROM READ('/srv/dfq/comments.csv',
 'format=csv',
 'skip=1',
 'comment=#',
 'header=false',
 'names=id,v,label',
 'all_varchar=true',
 'type.v=LONG');
```

반환 컬럼: `N`, `TOTAL`. 반환 행 수: 1.

다음은 처음 최대 3행의 표시입니다. 긴 값은 미리보기로 줄였습니다.

| N | TOTAL |
| --- | --- |
| 2 | 30 |

[SQL 다운로드](/assets/dbms-8.9/dfq/csv/11.sql)

## 오류와 해결

### 지원하지 않는 옵션 사용

```sql
SELECT *
FROM READ('/srv/dfq/sensor.csv',
 'format=csv',
 'unknown_option=true');
```

예상 오류: `INVALID_OPTION`. 등록되지 않은 옵션은 무시되지 않고 INVALID_OPTION으로 거부됩니다. 옵션표의 이름을 사용합니다.

[오류 SQL 다운로드](/assets/dbms-8.9/dfq/csv/12.sql)

### 형식 또는 선택 조건 오류

```sql
SELECT *
FROM READ('/srv/dfq/sensor.csv',
 'format=csv',
 'header=true',
 'names=id,v,label,day');
```

예상 오류: `INVALID_OPTION`. names는 header=false와 조합합니다. 헤더가 있으면 원래 이름을 사용하거나 헤더를 데이터로 읽는 방식을 명시합니다.

[오류 SQL 다운로드](/assets/dbms-8.9/dfq/csv/13.sql)

## 타입·구조·표현의 상세 규칙

모든 인자는 `'이름=값'` SQL 문자열 리터럴입니다. **config=JSON 입력을 허용하지 않습니다.** 상세 규칙은 평면 옵션에 있습니다. DATA/_META/_REFS/DETAILS와 config_schema의 JSON 출력은 유지합니다.

columns는 data의 결과 형식이며 list/schema는 해당 방식을 설명합니다. elements/nodes/raw에는 columns 명시를 금지합니다. row는 명시 target의 원래 부모 번호다. field는 원래 논리값 기준 경로이며 native data에는 금지합니다. 물리 raw에는 row/field/format/profile/CSV 설정/time/axis/canonical_json을 붙이지 않습니다.

인용은 큰따옴표, 내부 escape는 두 큰따옴표다. trim/주석/skip_rows/자동 날짜·숫자 타입 추정은 없습니다. 빈 문자열과 NULL을 구분하고 표현 불가 값을 조용히 바꾸지 않습니다. 일반 반환은 string→VARCHAR, int64→LONG, uint64→ULONG, float64→DOUBLE, bool→INTEGER 0·1입니다. LONG의 INT64_MIN과 ULONG의 UINT64_MAX는 SQL NULL 예약값이므로 native/project 조회에서 NATIVE_VALUE_UNREPRESENTABLE 오류이며 envelope에서는 정확한 십진 문자열로 보존합니다. 구체적인 한도는 한도와 경로에 있습니다.


## 자동 감지·인용·NULL의 세부 규칙

명시하지 않은 구분자·헤더·타입은 auto_detect로 추정합니다. CSV에서 auto_detect=false의
기본 구분자는 쉼표이고 TSV는 탭입니다. sample_size는 레코드 수이며 기본 20,480,
-1은 전체 표본입니다. 비압축 입력은 앞·중간·끝의 유한 표본을 사용합니다.
표본에 없던 긴 값이나 다른 타입이 실행 중 나타나면 자동 승격하지 않습니다.

encoding=auto는 BOM이 있으면 UTF-8/UTF-16을 선택하고 없으면 엄격한 UTF-8로 해석합니다.
CP949·Latin-1은 명시합니다. 인용 안의 구분자·개행과 doubled quote는 셀의 일부입니다.
quote·escape는 각각 ASCII 문자 또는 역슬래시를 지정하고 빈 값이면 해당 처리를 끕니다.
strict_mode=false도 모든 손상 framing을 복구하는 옵션은 아닙니다.

null_values는 기본 빈 목록으로 비인용 표식에 적용합니다. 인용된 빈 문자열과 SQL NULL을
구분하며 allow_quoted_nulls는 인용 필드에도 표식을 적용합니다. force_not_null은 존재하는
값의 표식 변환을 막지만 null_padding으로 채운 실제 누락값에는 적용하지 않습니다.

on_error=skip은 경계가 확실한 행의 컬럼 수·값 변환 오류를 건너뜁니다. 인코딩 오류,
닫히지 않은 인용, I/O·자원·취소는 숨기지 않습니다. mode=inspect/view=rejects는
ROW·START_LINE·COLUMN_NAME·CODE·MESSAGE·RAW_PREFIX_HEX 등의 진단을 제공합니다.
이 조회는 이전 실행 결과를 저장해 보여주는 것이 아니라 파일을 다시 읽습니다.

문자열 표본이 UTF-8 32 KiB를 넘으면 자동 TEXT를 선택합니다. 명시 VARCHAR·all_varchar는
VARCHAR 한도를 유지하고 명시 TEXT는 그보다 우선합니다. TEXT 한 셀의 64 MiB와 별도로
CSV/TSV 레코드는 디코딩된 필드 바이트와 필드별 terminator 1바이트 합계가 64 MiB 이하여야 합니다.
따라서 한 필드 payload도 정확히 64 MiB를 모두 사용할 수 없습니다.

## 관련 문서

- [구조와 컬럼 확인](../../inspect/)
- [구조화된 값과 원문 추출](../../extract/)
- [권한과 운영](../../operations/)
