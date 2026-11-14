---
type: docs
title: '12.4.6 NPY'
weight: 60
toc: true
---

NumPy 배열의 dtype과 shape에 따라 SQL 행·컬럼을 만듭니다. 샘플 sensor.npy는 id,v 필드를 가진 5개 structured record입니다.

## 실습 준비

[실습 파일 묶음](/assets/dbms-8.9/dfq/samples.zip)을 **DB 서버**의 `/srv/dfq`에 풉니다.
경로가 다르면 SQL의 `/srv/dfq`를 실제 서버 경로로 바꿉니다. 접속과 권한 준비는
[시작하기](../../getting-started/)를 참고합니다. SQL마다 별도의 준비 명령 없이 같은 입력을 사용합니다.
센서 샘플의 id=1~5, v=id×10이므로 COUNT=5, SUM(id)=15, SUM(v)=150입니다.
LeRobot 샘플은 이 센서 파일과 별개입니다.

## 작업별 빠른 찾기

| 목적 | 조합한 설정 | 예제 |
|---|---|---|
| 구조화 배열의 숫자 집계 | `format`, `parallel` | [예제 1](#example-1) |
| 출력 별칭과 타입 지정 | `format`, `names`, `type.key` | [예제 2](#example-2) |
| 구조화 필드를 선택해 투영 | `format`, `project.key`, `project.reading` | [예제 3](#example-3) |
| 배열 구조와 압축 확인 | `format`, `mode`, `view` | [예제 4](#example-4) |
| 행 하나를 envelope로 조회 | `format`, `columns`, `target`, `row` | [예제 5](#example-5) |
| 행렬 배열을 컬럼으로 조회 | `format`, `parallel` | [예제 6](#example-6) |
| 선택 배열의 강한 일관성 조회 | `format`, `source.consistency` | [예제 7](#example-7) |

## 전체 포맷 옵션

| 옵션 | 기본값 | 허용값·범위 | 역할 |
|---|---|---|---|
| `array` | 지정하지 않음 | 아래 설명의 문자열·타입 규칙 | NPZ 전용. NPY에는 지정하지 않음 |
| `names` | 지정하지 않음 | CSV 인용을 사용하는 쉼표 목록 | 원본 순서대로 출력 컬럼명 지정 |
| `type.*` | 지정하지 않음 | VARCHAR,TEXT,SHORT,INTEGER,LONG,USHORT,UINTEGER,ULONG,FLOAT,DOUBLE,DECIMAL,NUMERIC,DATETIME,TIMESTAMP,JSON,BINARY,VARBINARY | 컬럼별 SQL 타입. * 위치에 컬럼명 사용 |
| `filename` | false | true / false | 출처 파일명 컬럼 추가 |
| `union_by_name` | true | true / false | 여러 입력의 컬럼 결합 정책. 아래 reader별 제약 확인 |
| `on_error` | error | error,skip | 복구 가능한 완전한 행의 변환 오류 처리. 손상 전체를 무시하는 기능 아님 |
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

parallel=auto/false는 동기 실행이며 true는 지원하지 않습니다. axis는 임의 reshape 기능이 아닙니다. 첫 축이 행이며 (N,1)은 VALUE가 아니라 C1입니다. native 변환이 불가능한 dtype·값은 envelope 또는 원문 추출 경로를 확인합니다.

## 옵션 조합 예제

<a id="example-1"></a>

### 1. 구조화 배열의 숫자 집계

원본 structured dtype의 id·v를 SQL 컬럼으로 받습니다.

```sql
SELECT COUNT(*) AS N,SUM(v) AS TOTAL
FROM READ('/srv/dfq/sensor.npy', 'format=npy', 'parallel=false') ;
```

반환 컬럼: `N`, `TOTAL`. 반환 행 수: 1.

다음은 처음 최대 3행의 표시입니다. 긴 값은 미리보기로 줄였습니다.

| N | TOTAL |
| --- | --- |
| 5 | 150 |

[SQL 다운로드](/assets/dbms-8.9/dfq/npy/01.sql)

<a id="example-2"></a>

### 2. 출력 별칭과 타입 지정

원본 순서대로 별칭을 정하고 정수 carrier를 유지합니다.

```sql
SELECT key,reading
FROM READ('/srv/dfq/sensor.npy', 'format=npy', 'names=key,reading',
 'type.key=LONG') ORDER BY key LIMIT 3;
```

반환 컬럼: `key`, `reading`. 반환 행 수: 3.

다음은 처음 최대 3행의 표시입니다. 긴 값은 미리보기로 줄였습니다.

| key | reading |
| --- | --- |
| 1 | 10 |
| 2 | 20 |
| 3 | 30 |

[SQL 다운로드](/assets/dbms-8.9/dfq/npy/02.sql)

<a id="example-3"></a>

### 3. 구조화 필드를 선택해 투영

출력 필드를 제한해 SQL에 사용합니다.

```sql
SELECT key,reading
FROM READ('/srv/dfq/sensor.npy', 'format=npy', 'project.key=id',
 'project.reading=v') ORDER BY key LIMIT 3;
```

반환 컬럼: `key`, `reading`. 반환 행 수: 3.

다음은 처음 최대 3행의 표시입니다. 긴 값은 미리보기로 줄였습니다.

| key | reading |
| --- | --- |
| 1 | 10 |
| 2 | 20 |
| 3 | 30 |

[SQL 다운로드](/assets/dbms-8.9/dfq/npy/03.sql)

<a id="example-4"></a>

### 4. 배열 구조와 압축 확인

목록은 헤더 정보이며 전체 payload의 검증 완료를 의미하지 않습니다.

```sql
SELECT *
FROM READ('/srv/dfq/sensor.npy', 'format=npy', 'mode=inspect',
 'view=arrays') ;
```

반환 컬럼: `SOURCE`, `ARRAY_NAME`, `DTYPE`, `SHAPE`, `FORTRAN_ORDER`, `COMPRESSION`, `STORED_BYTES`, `UNCOMPRESSED_BYTES`, `VALIDATION`. 반환 행 수: 1.

[SQL 다운로드](/assets/dbms-8.9/dfq/npy/04.sql)

<a id="example-5"></a>

### 5. 행 하나를 envelope로 조회

structured record를 구조를 유지한 값으로 받습니다.

```sql
SELECT DATA
FROM READ('/srv/dfq/sensor.npy', 'format=npy', 'columns=envelope',
 'target=rows',
 'row=0') ;
```

반환 컬럼: `DATA`. 반환 행 수: 1.

다음은 처음 최대 3행의 표시입니다. 긴 값은 미리보기로 줄였습니다.

| DATA |
| --- |
| {"id":1,"v":10} |

[SQL 다운로드](/assets/dbms-8.9/dfq/npy/05.sql)

<a id="example-6"></a>

### 6. 행렬 배열을 컬럼으로 조회

2차원 배열은 첫 축이 행, 두 번째 축이 C1·C2 컬럼입니다.

```sql
SELECT C1,C2
FROM READ('/srv/dfq/matrix.npy', 'format=npy', 'parallel=false') ORDER BY C1 LIMIT 3;
```

반환 컬럼: `C1`, `C2`. 반환 행 수: 3.

다음은 처음 최대 3행의 표시입니다. 긴 값은 미리보기로 줄였습니다.

| C1 | C2 |
| --- | --- |
| 0 | 1 |
| 2 | 3 |
| 4 | 5 |

[SQL 다운로드](/assets/dbms-8.9/dfq/npy/06.sql)

<a id="example-7"></a>

### 7. 선택 배열의 강한 일관성 조회

원본을 고정해야 하는 조회에 strong 정책을 사용합니다.

```sql
SELECT COUNT(*) AS N,SUM(v) AS TOTAL
FROM READ('/srv/dfq/sensor.npy', 'format=npy', 'source.consistency=strong') ;
```

반환 컬럼: `N`, `TOTAL`. 반환 행 수: 1.

다음은 처음 최대 3행의 표시입니다. 긴 값은 미리보기로 줄였습니다.

| N | TOTAL |
| --- | --- |
| 5 | 150 |

[SQL 다운로드](/assets/dbms-8.9/dfq/npy/07.sql)

## 오류와 해결

### 지원하지 않는 옵션 사용

```sql
SELECT *
FROM READ('/srv/dfq/sensor.npy',
 'format=npy',
 'unknown_option=true');
```

예상 오류: `INVALID_OPTION`. 등록되지 않은 옵션은 무시되지 않고 INVALID_OPTION으로 거부됩니다. 옵션표의 이름을 사용합니다.

[오류 SQL 다운로드](/assets/dbms-8.9/dfq/npy/08.sql)

### 형식 또는 선택 조건 오류

```sql
SELECT *
FROM READ('/srv/dfq/bad.npy',
 'format=npy');
```

예상 오류: `CORRUPT_DATA`. 손상된 파일은 정상 빈 결과가 아닙니다. 원본 형식과 파일 내용을 확인합니다.

[오류 SQL 다운로드](/assets/dbms-8.9/dfq/npy/09.sql)

## 타입·구조·표현의 상세 규칙

### 배열의 행·컬럼 매핑

| 원본 배열 | `READ()`의 한 행 | 컬럼 |
|---|---|---|
| 0D scalar | 값 하나 | `VALUE` |
| 1D `(N,)` | scalar 하나 | `VALUE` |
| 2D `(N,M)`, `M≥1` | 두 번째 축의 값 | `C1` … `CM` |
| 2D `(N,0)` | 빈 배열 `[]` | `VALUE` JSON |
| 3D 이상 `(N,...)` | 나머지 축 전체의 배열 | `VALUE` JSON |
| structured 0D·1D | record 하나 | 원본 필드 이름 |
| structured 2D 이상 | 각 필드의 나머지 축 배열 | 필드별 JSON 컬럼 |
| 첫 축의 길이 0 | 행 0개, dtype schema 유지 | 위 규칙에 따른 컬럼 |

### dtype별 SQL 타입

| NumPy dtype | 기본 SQL 타입 | 값 규칙 |
|---|---|---|
| `bool` | INTEGER | false=0, true=1 |
| `i1`, `i2` / `i4` / `i8` | SHORT / INTEGER / LONG | 부호 있는 정수 |
| `u1`, `u2` / `u4` / `u8` | USHORT / UINTEGER / ULONG | 부호 없는 정수 |
| `f4` / `f8` | FLOAT / DOUBLE | IEEE 원값. native에서는 NaN·±Infinity 구분 |
| `S` | BINARY | 고정 폭 원 byte와 0 padding까지 보존 |
| `U` | VARCHAR 또는 TEXT | UTF-32을 검증해 UTF-8로 전달; 끝의 NUL padding만 제거 |
| `datetime64` | DATETIME | UTC 기준 naive epoch 시각; NaT는 SQL NULL |
| `timedelta64` | LONG | 단위 변환 없는 원 tick; NaT는 SQL NULL |
| nested record·subarray·고차원 slice | JSON | 원래 중첩 구조를 논리 C 순서로 전달 |

파일 경로를 첫 인자에 바로 쓸 수도 있습니다. 내용으로 형식을 감지하지만 판정이
모호하거나 파일명이 형식을 드러내지 않으면 `format=npy` 또는 `format=npz`를
명시합니다. 형식별 표준 프로파일 `profile=npy.standard@1`,
`profile=npz.standard@1`은 해당 형식만 고정하며 배열의 dtype·shape·NPZ 멤버까지
고정하지는 않습니다.

같은 프로파일로 1D 정수 배열과 2D 실수 배열을 각각 읽을 수 있습니다. NPZ에
여러 배열이 있으면 프로파일을 사용해도 `array=`로 멤버를 선택합니다.

`FROM '파일명'`과 `DESC '파일명'`도 파일 인식을 시도합니다. 같은 이름의 실제 테이블이나
뷰가 있으면 그 관계를 먼저 해석합니다. SYS 이외 사용자는 서버 디렉터리에 대한
READ 권한이 필요합니다.

### 배열이 행과 컬럼으로 바뀌는 규칙

첫 축이 행입니다. 값은 원본이 Fortran 순서로 저장됐더라도 **논리적 C 순서**로
읽습니다. 저장 byte offset은 dtype·shape·저장 순서를 사용해 계산합니다.

따라서 `(N,1)`도 scalar `VALUE`가 아니라 **`C1` 컬럼을 가진 객체 행**입니다.
빈 structured dtype은 첫 축의 행 수를 유지하고 `VALUE` JSON `{}`를 반환합니다.
structured 필드 안의 record와 subarray는 JSON으로 보존합니다. padding byte는
컬럼이 아니지만 원문 byte 추출에서는 유지합니다.

### NPZ 안의 배열 선택과 목록

NPZ에 배열이 하나면 자동으로 선택합니다. 둘 이상이면 `array=이름`이 필요합니다.
이름은 대소문자를 구분하고 ZIP 멤버 이름의 **마지막 `.npy`만 제거**한 것입니다.
따라서 `main`과 `main.npy`는 다른 선택입니다. `.npy`라는 멤버의 빈 논리 이름은
`'array='`로 명시할 수 있습니다.

목록의 같은 내용은 catalog의 `reader.arrays` JSON 배열에도 있습니다. catalog의
`shape`는 문자열이 아닌 JSON 숫자 배열이며 `validation`은 `header_only`다.

### NumPy dtype과 SQL 타입

형식은 NPY header의 dtype에서 결정합니다. 값을 표본으로 읽어 숫자나 날짜를
추측하지 않습니다. `mode=inspect,view=columns`로 결과 컬럼의 SQL 타입을 미리
확인할 수 있습니다.

SQL byte carrier의 실제 타입 이름은 **BINARY**이며 가변 길이 byte를 담는다.
`type.컬럼=BINARY`와 `type.컬럼=VARBINARY`는 같은 선언입니다. `S`의 논리
`DATA`와 canonical JSON에서는 원 byte를 **base64 문자열**로 표현하고 `_META`의
encoding을 `base64`로 표시합니다. native BINARY와 논리 base64 문자열을 같은
값의 표시 형식으로 혼동하지 않습니다.

엔진의 각 정수 SQL 타입은 NULL 예약값을 가집니다. 예를 들어 `i8`의 최솟값이나
`u8`의 최댓값을 해당 기본 SQL 타입으로 읽으면 명시 오류이며, 더 넓은 타입이
있으면 지정하고 `i8`/`u8` 경계에는 DECIMAL을 쓸 수 있습니다. `i2`의 최솟값을
`INTEGER`로, `u4`의 최댓값을 `ULONG`으로 지정하는 식의 확장도 가능하다.

FLOAT·DOUBLE에도 각각 SQL NULL 예약 비트가 있습니다. `f4`의 최대 유한값이
기본 FLOAT의 예약값과 같으면 오류지만, `type.n=DOUBLE`을 지정하면
정확한 DOUBLE 값으로 읽을 수 있습니다. `f8`의 DOUBLE 예약값에는 더 넓은
native 실수 타입이 없으므로 원 bit가 필요하면 `numpy_bytes`를 사용합니다.
NULL 충돌 여부는 원본 dtype이 아니라 **선택한 SQL 출력 타입**을 기준으로
판정합니다.

`S0`과 `U0`은 각각 빈 byte와 빈 문자열이며 SQL NULL과 구분합니다. `U` 안의
끝 padding이 아닌 NUL 문자, 잘못된 UTF-32 코드포인트, native로 표현할 수 없는
값은 조용히 변환하지 않고 오류와 원 byte 조회 경로를 제공합니다.
기존 `JSON_EXTRACT_STRING` 함수는 빈 JSON 문자열을 추출하면 SQL NULL로
돌려주는 동작이 있으므로, 원본의 빈 값 여부는 native 컬럼이나 envelope의
`DATA` JSON 값을 직접 확인합니다. 빈 문자열 예제는 인라인 JSON 리터럴 대신
파일에서 읽은 `DATA`를 사용합니다.

### 이름 바꾸기, 중첩 필드, 명시 타입

`names=`는 출력 컬럼 **전체**의 이름을 순서대로 지정하는 CSV 방식 목록입니다.
컬럼 수가 맞아야 하며, 이름에 쉼표가 있으면 CSV 따옴표 규칙으로 값을 감싼다.
`filename=true`를 쓰면 끝에 파일명 컬럼이 추가되므로 그 이름도 `names=`에
포함합니다. 원본 이름의 대소문자와 Unicode를 유지합니다. SQL 컬럼으로 사용할 수
없는 원본 이름이나 SQL 식별자 충돌은 이름을 임의로 바꾸지 않고 오류로 알린다.
`names=` 또는 `project.*=`의 안전한 별칭을 사용합니다.

`type.*`의 이름은 최종 출력 컬럼 이름입니다. `project.x=pose.x`를 사용하면
`type.x=INTEGER`처럼 원본 경로가 아닌 별칭 `x`에 지정합니다. 원 dtype과
subarray shape·byte order·단위는 metadata에 남는다. `dateformat`,
`timestampformat`, `encoding`, `header`, `delimiter`, `sample_size`는 바이너리
dtype 해석에 적용하지 않습니다.

`datetime64`는 원 tick과 단위로 UTC 기준 DATETIME을 계산합니다. `Y`/`M`은
달력의 연도·월로, 다른 고정 단위는 정수 연산으로 변환합니다. 엔진의 시각 범위나
나노초 정밀도로 정확히 표현할 수 없으면 오류다. `type.ts=LONG`을 지정하면
변환 전 원 tick을 볼 수 있습니다. `timedelta64`는 변환하지 않은 LONG tick입니다.

`datetime64`와 `timedelta64`의 논리 `DATA`/canonical JSON은 시각 문자열이
아닌 **원 tick JSON 정수**다. NaT는 논리 JSON null과 native SQL NULL로
나타난다. 선택한 scalar가 NaT이면 `_META.validity.fields`에 `reason=NaT`를
기록합니다. 전체 큰 배열의 NaT 위치를 metadata DOM으로 무제한 나열하지 않습니다.
이 정책은 `numpy_source.nat_reporting=selected_scalar_only`에 표시하며,
배열 전체의 dtype·shape·단위와 원 bit는 별도로 보존합니다.

### 큰 값, 참조, 원 byte

일반 native JSON 셀은 실제 canonical 크기가 **32,768 byte 이하**일 때만
전달합니다. 임의의 행 크기 추정 기준으로 그보다 작은 값을 거부하지 않습니다.
`JSON_EXTRACT_STRING`과 `JSON_EXTRACT`의 반환 VARCHAR 한도도 32,768
byte다. 예를 들어 아래 고정 입력에서는 추출 문자열이 32,760 byte이고
전체 객체가 정확히 32,768 byte여서 둘 다 반환됩니다. 한도를 넘는 추출
결과는 자르거나 서버를 종료하지 않고 `Buffer size insufficient.` 오류를
반환합니다. 이는 원본 native JSON 셀의 허용 여부와 별개인 **함수 결과** 한도다.

큰 배열은 먼저 전체 JSON DOM을 만들지 않고, `_REFS`의 재조회 작업으로
접근합니다. 비유한 FLOAT/DOUBLE은 native SQL에서는 원 IEEE 값이지만 JSON
number로 나타낼 수 없습니다. 이 경우 envelope의 DATA는 SQL NULL,
`_META.selection.status`는 `REFERENCE`이고 `_REFS`에서
`raw_canonical=no`, `raw_numpy=yes`와 실행 가능한 조회 인자를 확인합니다.

`numpy_bytes`는 선택한 값의 **NPY payload 원 byte**를 논리적 C 순서로 모아
반환합니다. 각 scalar의 원 byte order를 유지하며 `S`/`U` padding도 그대로다.
Fortran 저장 순서에서는 서로 떨어진 위치를 각 원소 offset으로 찾아 모은다.
NPZ에서 이는 선택 멤버를 해제한 뒤의 NPY payload byte이며 ZIP 안의 압축
byte나 원본 파일 offset이 아닙니다. `_OFFSET`도 이렇게 반환되는 byte열의 offset입니다.

`raw.representation=canonical_json`은 논리값의 UTF-8 JSON byte를 chunk로
반환합니다. 유한 값의 큰 배열에는 재결합 가능한 JSON을 제공하지만 NaN·Infinity가
포함된 선택값은 첫 chunk 전에 명시 오류로 중단합니다. 형식을 지정하지 않은
`mode=raw`는 파일 자체의 물리 byte를 읽습니다. NPZ에 적용하면 ZIP 파일 byte다.

`_REFS`의 `locator.operations.raw_canonical` 또는 `raw_numpy`에서
`query_args`와 `example_sql`을 얻을 수 있습니다. 같은 값의 재조회에는 원래
source·target·전역 row·절대 field path·mapping·source revision guard가
필요합니다. 강한 snapshot을 요청한 경우 재조회 SQL이 같은 source 집합과
선택한 NPZ 배열을 확인하며, 파일이나 해석이 바뀌면 명시 오류를 낸다.
NPZ 단일 배열 자동 선택은 재조회에 실제 선택 이름을 고정합니다. 여러 NPZ 파일이
서로 다른 단일 배열을 자동 선택한 경우에는 첫 파일 이름을 전체 파일에
강제하지 않고 파일별 선택과 전체 집합 guard를 보존합니다.
단일 NPZ 파일에서도 강한 일관성을 요청한 뒤 원본 파일이 교체되면
재조회는 `SOURCE_CHANGED` 오류를 내며, 임시로 풀어 놓은 멤버를 새
원본인 것처럼 취급하지 않습니다.

첫 SQL의 `replay_sql`을 새 질의로 실행하면 locator가 지정한 원 byte를 다시
조회합니다. 직접 표시할 수 없는 긴 설정은 `READ_SQL` 대신 `READ_TOKEN`을 확인합니다.

### 여러 파일, 오류 행, 실행 정책

주로 쓰는 인자는 다음과 같습니다. 각 항목을 별도의 `'name=value'` SQL 문자열로
전달합니다.

첫 위치형 파일 인자를 여러 개 쓰거나 `sources=` 목록·glob을 사용할 수 있습니다.
같은 형식의 파일들을 요청 순서로 읽습니다. `union_by_name=true`가 기본이며
false면 파일별 컬럼 집합이 달라질 때 오류다. `filename=true`는 원본 파일명
컬럼을 끝에 붙인다. `source.consistency=strong`은 모든 파일의 snapshot을
첫 결과 전 고정합니다. 일반 source 집합은 최대 4096파일, strong 다중 파일은
최대 256파일입니다. 자동 형식 판별에서 NPY와 NPZ가 섞이는 집합은 별도
`READ()`를 사용해 `UNION ALL`합니다.

`on_error=error`가 기본입니다. `on_error=skip`은 **완전한 행의 native 값 변환
실패**만 행 전체를 건너뛴다. 헤더·dtype·ZIP 구조·CRC·I/O·메모리·취소 오류는
skip으로 숨기지 않습니다. 건너뛸 수 있는 오류를 보려면 같은 옵션으로
`mode=inspect,view=rejects`를 별도로 조회합니다.

`parallel=auto`와 `parallel=false`는 현재 순차 실행입니다. `parallel=true`는
지원하지 않는다는 오류를 낸다. `threads`는 1~32 범위에서 검사하지만
작업자를 실제로 사용했다고 보고하지 않습니다.

### 구조 조회, 한도, 지원 범위

`data`, `list`, `schema`, `inspect`, `elements`, `nodes`, `raw`를 사용합니다.
`row=`는 원래 첫 축의 0 기반 행을 고르며 `target=rows`를 함께 지정합니다.
`field=`는 그 부모 논리값 안의 경로다. 예를 들어 고차원 slice의 자식 배열을
보고 싶으면 `mode=elements`와 명시 `row`·`field`를 씁니다. NPY/NPZ에는
JSON document target을 추가하지 않으며, 선택 배열의 `rows`가 기본 대상입니다.

NPZ는 stored·deflate·ZIP64 멤버를 읽습니다. object/pickle(중첩 포함), complex,
float16·float128, 의미 없는 단독 void dtype, 암호화 ZIP, 중복 논리 멤버,
다중 disk ZIP, 지원하지 않는 압축 method는 읽기 오류 또는 미지원 형식 오류로
알린다. 외부 `.npy.gz`, `.npy.zst`, `.npz.gz`, `.npz.zst` wrapping은 이 형식에
적용하지 않습니다. NPZ 내부 deflate와 구분합니다.

## 관련 문서

- [구조와 컬럼 확인](../../inspect/)
- [구조화된 값과 원문 추출](../../extract/)
- [권한과 운영](../../operations/)
