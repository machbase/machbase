---
type: docs
title: '12.4.9 HDF5'
weight: 90
toc: true
---

dataset 하나 또는 같은 group의 직계 dataset들을 컬럼으로 묶어 조회합니다. 샘플에는 /records, /table/id, /table/v와 /matrix가 있습니다.

## 실습 준비

[실습 파일 묶음](/assets/dbms-8.9/dfq/samples.zip)을 **DB 서버**의 `/srv/dfq`에 풉니다.
경로가 다르면 SQL의 `/srv/dfq`를 실제 서버 경로로 바꿉니다. 접속과 권한 준비는
[시작하기](../../getting-started/)를 참고합니다. SQL마다 별도의 준비 명령 없이 같은 입력을 사용합니다.
센서 샘플의 id=1~5, v=id×10이므로 COUNT=5, SUM(id)=15, SUM(v)=150입니다.
LeRobot 샘플은 이 센서 파일과 별개입니다.

## 작업별 빠른 찾기

| 목적 | 조합한 설정 | 예제 |
|---|---|---|
| dataset 레코드와 집계 | `format`, `dataset`, `parallel` | [예제 1](#example-1) |
| group의 dataset을 컬럼으로 결합 | `format`, `group`, `source.consistency` | [예제 2](#example-2) |
| dataset의 필드 투영과 타입 지정 | `format`, `dataset`, `project.key`, `project.reading`, `type.key` | [예제 3](#example-3) |
| 행렬 dataset의 첫 행 조회 | `format`, `dataset`, `parallel` | [예제 4](#example-4) |
| dataset과 group 목록 탐색 | `format`, `mode`, `view` | [예제 5](#example-5) |
| 선택한 dataset의 SQL 스키마 | `format`, `dataset`, `mode`, `view` | [예제 6](#example-6) |
| 논리 행을 envelope로 보존 | `format`, `dataset`, `columns`, `target`, `row` | [예제 7](#example-7) |

## 파일과 조회 대상

```text
sensor.h5
 ├─ /records        → dataset=/records → compound id/v, 5행
 ├─ /table
 │   ├─ id [5]      ┐
 │   └─ v  [5]      ┴→ group=/table → id/v, 5행
 └─ /matrix [5,2]   → dataset=/matrix → C1/C2

 mode=inspect + view=datasets → 내부 경로 탐색
```

## 전체 포맷 옵션

| 옵션 | 기본값 | 허용값·범위 | 역할 |
|---|---|---|---|
| `dataset` | 지정하지 않음 | 아래 설명의 문자열·타입 규칙 | /로 시작하는 HDF5 dataset 경로 |
| `group` | 지정하지 않음 | 아래 설명의 문자열·타입 규칙 | /로 시작하는 HDF5 group 경로 |
| `names` | 지정하지 않음 | CSV 인용을 사용하는 쉼표 목록 | 원본 순서대로 출력 컬럼명 지정 |
| `type.*` | 지정하지 않음 | VARCHAR,TEXT,SHORT,INTEGER,LONG,USHORT,UINTEGER,ULONG,FLOAT,DOUBLE,BOOLEAN,DECIMAL,NUMERIC,DATETIME,TIMESTAMP,JSON,BINARY,VARBINARY | 컬럼별 SQL 타입. * 위치에 컬럼명 사용 |
| `filename` | false | true / false | 출처 파일명 컬럼 추가 |
| `sources` | 지정하지 않음 | CSV 인용을 사용하는 쉼표 목록 | 순서 있는 파일 목록. 위치형·source와 혼용 금지 |
| `union_by_name` | true | true / false | 여러 입력의 컬럼 결합 정책. 아래 reader별 제약 확인 |
| `on_error` | error | error,skip | 복구 가능한 완전한 행의 변환 오류 처리. 손상 전체를 무시하는 기능 아님 |
| `parallel` | auto | auto / false (순차 실행) | 실행 정책. 아래 지원 조합 확인 |
| `threads` | 1 | 1~32 | 작업자 수 상한. reader에 따라 병렬 작업자를 만들지 않음 |
| `max_value_bytes` | 67108864 | 1~2147483647 | 논리값·읽기 chunk 바이트 상한. 전체 작업 예산과 별개 |

공통 mode·columns·target·row·field·project·column·source·raw 설정은
[READ 공통 옵션](../../read-options/)을 함께 적용합니다. 위 표의 값 목록은 입력 형식이며
아래 제약에서 제한한 값은 해당 reader에서 실행할 수 없습니다. 특히 parallel의 등록된 값 목록이
실제 병렬 처리 지원을 뜻하지 않습니다. view별 상세 설정은 inspect의 options/capabilities도 확인합니다.

## 우선순위와 허용 조합

dataset과 group은 상호 배타이며 /로 시작하는 내부 경로입니다. group은 직계 dataset을 결합합니다. parallel=auto/false는 순차 실행이고 true는 지원하지 않습니다. external link·VDS·외부 raw storage·임의 동적 plugin은 지원하지 않습니다.

## 옵션 조합 예제

<a id="example-1"></a>

### 1. dataset 레코드와 집계

선택한 compound dataset의 필드를 컬럼으로 읽습니다.

```sql
SELECT COUNT(*) AS N,SUM(v) AS TOTAL
FROM READ('/srv/dfq/sensor.h5', 'format=hdf5', 'dataset=/records',
 'parallel=false') ;
```

반환 컬럼: `N`, `TOTAL`. 반환 행 수: 1.

다음은 처음 최대 3행의 표시입니다. 긴 값은 미리보기로 줄였습니다.

| N | TOTAL |
| --- | --- |
| 5 | 150 |

[SQL 다운로드](/assets/dbms-8.9/dfq/hdf5/01.sql)

<a id="example-2"></a>

### 2. group의 dataset을 컬럼으로 결합

직계 dataset의 첫 축을 기준으로 행을 결합합니다.

```sql
SELECT COUNT(*) AS N,SUM(v) AS TOTAL
FROM READ('/srv/dfq/sensor.h5', 'format=hdf5', 'group=/table',
 'source.consistency=strong') ;
```

반환 컬럼: `N`, `TOTAL`. 반환 행 수: 1.

다음은 처음 최대 3행의 표시입니다. 긴 값은 미리보기로 줄였습니다.

| N | TOTAL |
| --- | --- |
| 5 | 150 |

[SQL 다운로드](/assets/dbms-8.9/dfq/hdf5/02.sql)

<a id="example-3"></a>

### 3. dataset의 필드 투영과 타입 지정

원본 경로와 출력 별칭을 구분합니다.

```sql
SELECT key,reading
FROM READ('/srv/dfq/sensor.h5', 'format=hdf5', 'dataset=/records',
 'project.key=id',
 'project.reading=v',
 'type.key=LONG') ORDER BY key LIMIT 3;
```

반환 컬럼: `key`, `reading`. 반환 행 수: 3.

다음은 처음 최대 3행의 표시입니다. 긴 값은 미리보기로 줄였습니다.

| key | reading |
| --- | --- |
| 1 | 10 |
| 2 | 20 |
| 3 | 30 |

[SQL 다운로드](/assets/dbms-8.9/dfq/hdf5/03.sql)

<a id="example-4"></a>

### 4. 행렬 dataset의 첫 행 조회

행렬의 첫 축이 SQL 행입니다.

```sql
SELECT C1,C2
FROM READ('/srv/dfq/sensor.h5', 'format=hdf5', 'dataset=/matrix',
 'parallel=false') ORDER BY C1 LIMIT 3;
```

반환 컬럼: `C1`, `C2`. 반환 행 수: 3.

다음은 처음 최대 3행의 표시입니다. 긴 값은 미리보기로 줄였습니다.

| C1 | C2 |
| --- | --- |
| 0 | 1 |
| 2 | 3 |
| 4 | 5 |

[SQL 다운로드](/assets/dbms-8.9/dfq/hdf5/04.sql)

<a id="example-5"></a>

### 5. dataset과 group 목록 탐색

선택하기 전에 내부 경로와 타입을 확인합니다.

```sql
SELECT DATASET,KIND,DTYPE,SHAPE
FROM READ('/srv/dfq/sensor.h5', 'format=hdf5', 'mode=inspect',
 'view=datasets') ;
```

반환 컬럼: `DATASET`, `KIND`, `DTYPE`, `SHAPE`. 반환 행 수: 6.

다음은 처음 최대 3행의 표시입니다. 긴 값은 미리보기로 줄였습니다.

| DATASET | KIND | DTYPE | SHAPE |
| --- | --- | --- | --- |
| / | group | none | [] |
| /matrix | dataset | int64 | [5,2] |
| /records | dataset | compound | [5] |

[SQL 다운로드](/assets/dbms-8.9/dfq/hdf5/05.sql)

<a id="example-6"></a>

### 6. 선택한 dataset의 SQL 스키마

원래 dtype과 SQL carrier는 다를 수 있습니다.

```sql
SELECT COLUMN_NAME,SQL_TYPE
FROM READ('/srv/dfq/sensor.h5', 'format=hdf5', 'dataset=/records',
 'mode=inspect',
 'view=columns') ORDER BY COLUMN_ORDINAL;
```

반환 컬럼: `COLUMN_NAME`, `SQL_TYPE`. 반환 행 수: 2.

다음은 처음 최대 3행의 표시입니다. 긴 값은 미리보기로 줄였습니다.

| COLUMN_NAME | SQL_TYPE |
| --- | --- |
| id | LONG |
| v | LONG |

[SQL 다운로드](/assets/dbms-8.9/dfq/hdf5/06.sql)

<a id="example-7"></a>

### 7. 논리 행을 envelope로 보존

compound record의 원래 구조를 보존합니다.

```sql
SELECT DATA
FROM READ('/srv/dfq/sensor.h5', 'format=hdf5', 'dataset=/records',
 'columns=envelope',
 'target=rows',
 'row=0') ;
```

반환 컬럼: `DATA`. 반환 행 수: 1.

다음은 처음 최대 3행의 표시입니다. 긴 값은 미리보기로 줄였습니다.

| DATA |
| --- |
| {"id":"1","v":"10"} |

[SQL 다운로드](/assets/dbms-8.9/dfq/hdf5/07.sql)

## 오류와 해결

### 지원하지 않는 옵션 사용

```sql
SELECT *
FROM READ('/srv/dfq/sensor.h5',
 'format=hdf5',
 'dataset=/records',
 'unknown_option=true');
```

예상 오류: `INVALID_OPTION`. 등록되지 않은 옵션은 무시되지 않고 INVALID_OPTION으로 거부됩니다. 옵션표의 이름을 사용합니다.

[오류 SQL 다운로드](/assets/dbms-8.9/dfq/hdf5/08.sql)

### 형식 또는 선택 조건 오류

```sql
SELECT *
FROM READ('/srv/dfq/bad.h5',
 'format=hdf5');
```

예상 오류: `CORRUPT_DATA`. 손상된 파일은 정상 빈 결과가 아닙니다. 원본 형식과 파일 내용을 확인합니다.

[오류 SQL 다운로드](/assets/dbms-8.9/dfq/hdf5/09.sql)

## 타입·구조·표현의 상세 규칙

### dataset의 행·컬럼 매핑

| 원래 dataset | SQL 행 | 기본 컬럼 |
|---|---:|---|
| scalar |1행 | VALUE |
| 1차원 `(N)` |N행 | VALUE |
| 2차원 숫자 배열 `(N,M)` |N행 | C1 … CM |
| 3차원 이상 `(N,…)` |N행 | 나머지 축의 배열을 담는 VALUE |
| compound 레코드 |첫 축 기준 | 멤버별 컬럼. 중첩 레코드·배열 멤버는 JSON/TEXT |
| 첫 축이 0 또는 null dataspace |0행 | 선언 dtype에 따른 컬럼 |
| `(N,0)` |N행 | 빈 배열 값 |

HDF5 파일 안에서 **dataset 하나**를 고르거나, **같은 group의 dataset들을 컬럼으로 묶어** SQL로 조회합니다. 파일 경로는 DBMS 서버에서 해석합니다. 옵션은 기존 READ와 같이 각각 `'name=value'` 문자열로 지정합니다.

대부분은 다음 순서로 사용하면 됩니다.

### dataset과 group 선택

dataset은 배열이나 레코드 집합입니다. group은 dataset들을 담는 폴더와 비슷하다.

`dataset`과 `group`은 동시에 지정할 수 없습니다. 두 경로 모두 `/`로 시작하고 대소문자를 구분합니다. dataset 옵션으로 group을 지정하거나 그 반대로 지정하면 오류다.

파일에 **고유 dataset이 하나** 있으면 선택을 생략할 수 있습니다. 같은 dataset의 내부 링크 별칭은 별개의 데이터로 세지 않습니다.

데이터 조회에서 고유 dataset이 여러 개면 dataset 또는 group을 선택합니다. 특정 dataset의 SQL 컬럼 확인에는 선택 옵션을 받는 `mode=inspect, view=columns`를 사용합니다.

파일명만으로 구조를 살펴보려면 DESC를 사용합니다. 단일 고유 dataset이면 기존 NAME/TYPE_NAME/COLUMN_SIZE 컬럼 설명을 유지하고, 고유 dataset이0개 또는여러개인 HDF5이면 DATASET/KIND/DTYPE/SHAPE 구조 목록을 자동으로 반환합니다. hard/soft link의 별칭은 같은 dataset으로 계산합니다.

위 값은 고정 샘플의 실제 출력에서 공백·줄바꿈만 정리했다. DTYPE은 HDF5의 원래 타입이며 SQL 반환 타입과 구분합니다. 구조 조회는 긴 문자열·reference payload를 native SQL 값으로 변환하지 않습니다. 파일 손상·권한·자원 오류를 구조 조회 성공으로 숨기지는 않습니다.

SQL로 같은 자동 설명을 받으려면 `mode=inspect, view=describe`, HDF5의 전체 구조를 명시적으로 받으려면 `mode=inspect, view=structure`를 사용합니다. 일반 READ data와 명시 view=columns의 dataset 선택 규칙은 그대로다.

형식은 파일명에 의존하지 않고 HDF5 signature로 자동 감지합니다. 확장자가 `.bin`이어도 실제 HDF5이면 읽고, user block 뒤의 signature도 확인합니다. 형식을 고정하려면 `'format=hdf5'`를 추가합니다. HDF4 지원을 의미하지는 않습니다.

고정 profile도 사용할 수 있습니다. profile이 정한 설정을 같은 호출에 중복 지정하면 OPTION_CONFLICT가 발생할 수 있습니다.

### 배열이 행과 컬럼으로 바뀌는 규칙

예를 들어 `/matrix`의 첫 행이 `[1,10,-1]`이면 C1=1, C2=10, C3=-1을 얻는다.

group은 **직계 dataset만** 결합하며 하위 group을 자동으로 재귀 결합하지 않습니다. 비-scalar dataset의 첫 축 길이는 같아야 합니다. 다르면 SCHEMA_MISMATCH다. scalar는 각 행에 반복하며 모두 scalar이면 1행입니다. 직계 dataset이 없는 group은 INVALID_OPTION입니다.

group의 `state[N,2]`는 `state.C1`, `state.C2`로 펼친다. 컬럼 순서는 dataset 이름의 UTF-8 byte 순서, 멤버 순서, 배열 열 순서다.

### 컬럼 이름과 필요한 필드 선택

SQL에서 점이 포함된 컬럼 이름은 `"state.C1"`처럼 큰따옴표로 감싼다. READ 경로에서도 점이 들어 있는 **한 key**와 중첩 경로를 구분합니다.

names 개수는 전체 출력 컬럼 수와 같아야 합니다. filename=true이면 가상 filename 컬럼도 포함합니다. 별칭 적용 후에도 대소문자 구분 없이 이름이 충돌하면 오류다. type.*에는 별칭 적용 후의 이름을 씁니다. 목록은 쉼표로 구분하며, 값 자체에 쉼표가 있으면 기존 READ의 CSV 따옴표 규칙을 따릅니다.

### SQL 타입과 큰 값

HDF5는 dtype을 갖고 있어 일반 숫자를 문자열 표본으로 추측하지 않습니다. 원래 dtype과 SQL로 반환하는 타입은 구분합니다.

native 실수 지원 범위는 표준 IEEE 32/64비트다. IEEE 16비트·128비트와 비표준 정밀도·지수 배치는 `type.*=DOUBLE`을 지정해도 자동 변환하지 않습니다. 메타데이터 또는 지원되는 고정폭 raw bytes로 확인합니다. enum을 bool로 해석하는 경우도 FALSE=0·TRUE=1이 정확히 대응하는 표준 형태로 제한하며, 그 밖의 enum은 원래 정수 code와 라벨을 보존합니다.

기본 반환 타입을 바꾸려면 type.*를 씁니다. 원래 dtype·enum 라벨·byte order는 이 설정으로 바뀌지 않습니다.

SQL 정수의 NULL 예약값은 정상 숫자로 반환할 수 없습니다. 예를 들어 LONG의 최솟값과 ULONG의 최댓값이 해당합니다. 8비트 원본을 SHORT/USHORT로 확장하면 **반환 SQL 타입의 예약값**을 기준으로 검사합니다. 충돌은 NATIVE_VALUE_UNREPRESENTABLE이며 임의로 NULL로 바꾸지 않습니다. 값에 맞는 VARCHAR/TEXT·DECIMAL 반환 타입, envelope 또는 지원되는 raw 표현을 선택합니다.

NaN/Inf와 SQL NULL 예약 실수도 구분합니다. fill 값이 0이라는 이유로 SQL NULL로 바꾸지 않습니다. 빈 문자열·빈 배열과 NULL은 별개다. SQL 문자열로 표현할 수 없는 내부 NUL이 남는 경우에도 조용히 잘라 반환하지 않습니다.

큰 복합값의 기본 타입은 dtype/shape의 **보수적인 JSON 길이 상한**으로 정합니다. 32,768바이트를 넘을 수 있는 고정 배열·객체나 길이가 정해지지 않은 VLEN 복합값은 TEXT를 선택할 수 있습니다. 실제 한 행이 작아도 이 규칙에 따라 TEXT일 수 있습니다.

SQL native 정수는 정수로 반환합니다. envelope의 정규 JSON에서는 64비트 정밀도를 보존하려고 정수를 십진 문자열로 표현할 수 있습니다. JSON_EXTRACT_STRING 후 LONG 등으로 변환하는 예제가 사용되는 이유다.

### schema와 attributes 확인

SQL 반환 컬럼은 view=columns, 원래 논리 필드는 mode=schema로 확인합니다.

선택한 dataset/group의 attributes는 meta.hdf5.attributes로 추가합니다. JSON 내용을 담는 TEXT이며 기존 JSON 함수로 값을 꺼낼 수 있습니다.

위 fixture의 `/table`에는 run=7이 있습니다. `/table/id` 자체의 unit을 보려면 그 dataset을 선택합니다.

함께 쓸 수 있는 경로는 meta.hdf5.dataset, meta.hdf5.group, meta.hdf5.file_row다. 선택 방식에 해당하지 않는 dataset/group 이름은 NULL입니다. file_row는 현재 파일에서 0부터 시작하는 행 번호이며 여러 파일을 합친 전체 행 번호와 구분합니다.

각 객체의 attributes는 catalog에서도 조회합니다.

attributes는 현재 실행에서 파일을 열 때 읽어 고정합니다. 같은 prepared statement의 다음 Execute는 새로 연 파일의 속성을 읽습니다. dtype·shape·enum 선언이 달라 기존 schema를 사용할 수 없으면 SCHEMA_CHANGED 오류가 발생하므로 다시 prepare합니다.

표준 dimension scale의 DIMENSION_LIST처럼 reference를 담은 배열·VLEN·compound 속성은 자동으로 역참조하지 않습니다. 원래 타입과 `unsupported`·`unsupported_type`·`reason` 등의 미지원 marker를 metadata에 보존합니다. 이런 속성이 있다는 이유로 정상 숫자 dataset 조회를 막지는 않습니다. dataset 자체의 dtype가 미지원 멤버를 포함한 경우에는 datasets 목록의 NATIVE_SUPPORT가 no로 표시됩니다.

일반 조회는 기본 mode=data를 사용합니다. 다른 모드는 구조 확인, 선택한 값 펼치기, bytes 조회에 사용합니다.

row는 **0부터 시작하는 원본 행 번호**다. WHERE나 LIMIT와 다른 옵션이며, row를 쓸 때는 기존 READ 계약에 따라 target=rows도 명시합니다. 배열 index도 0부터 시작합니다.

columns=envelope는 기본 SQL 컬럼 대신 DATA와 `_SOURCE`, `_TARGET`, `_ROW`, `_META`, `_REFS` 등을 반환합니다. 공통 `_TIME_NS`·`_CLOCK` 컬럼도 있지만 HDF5 숫자나 attributes에서 시각을 자동 추정하지 않습니다. DATA가 셀 한도를 넘으면 참조로 다시 읽을 수 있으므로 `_REFS`도 함께 확인합니다.

metadata target인 @read/catalog은 원래 타입 정의와 reader 사실, @read/inventory는 target 목록, @read/diagnostics는 설명·진단을 제공합니다. 이 target의 data 조회에는 columns=envelope를 지정합니다.

파일 내부 dataset 경로를 나열할 때는 `mode=inspect, view=datasets`를 사용합니다. `mode=list`의 READ target 목록과 구분합니다. 다중 dataset 파일에서는 list/schema 조회에도 dataset 또는 group 선택이 필요합니다.

### 원문 bytes를 BINARY로 받기

mode=raw의 `_CONTENT`는 문자열이 아닌 **BINARY**다. 다음 표현을 구분합니다.

클라이언트는 `_CONTENT`를 바이너리로 받아 `_OFFSET` 순서대로 연결합니다. `_LENGTH`는 해당 청크 크기, `_LAST`=1은 마지막 청큽니다. `_TOTAL_SIZE`는 전체 크기를 알 수 있을 때 제공합니다. raw.chunk_bytes는 1바이트부터 1 MiB까지 지정할 수 있습니다.

hdf5_bytes는 독립적인 .h5 파일이 아닙니다. 압축을 푼 논리값의 bytes이므로 클라이언트가 dtype·shape·endian에 맞게 해석합니다. 이미지·음성 등이 고정폭 수치 배열로 저장되어 있을 때도 사용할 수 있으며 이미지·영상·음성 codec을 자동 해석하지 않습니다.

dataset의 compound 행 전체는 원래 itemsize와 멤버 offset을 유지하되 padding은 0으로 재구성합니다. 원본 디스크 padding이라고 해석하면 안 됩니다. group 전체에는 단일 dtype가 없어 hdf5_bytes를 지원하지 않습니다. group 전체가 필요하면 canonical JSON, 고정폭 bytes가 필요하면 개별 field를 선택합니다.

VLEN 문자열·배열과 object/region reference의 메모리 포인터는 bytes로 노출하지 않습니다. 일반 고정밀 숫자를 native로 해석하지 못해도 안전한 고정폭 타입이면 raw 대안을 사용할 수 있습니다. 지원하지 않는 원문 표현은 UNSUPPORTED_FORMAT으로 거부합니다.

### 참조를 이용한 재조회

고정폭 bytes 접근이 가능한 값에는 `_REFS`의 raw_hdf5 작업을 보충합니다. 작은 값의 DATA도 그대로 유지합니다.

반환된 SQL을 실행하면 `_CONTENT` 청크를 얻는다. 발급된 example_sql·query_args를 사용하면 선택 경로와 source/schema/mapping guard를 보존할 수 있습니다. 작업 목록은 mode=inspect, view=ref_operations로도 확인합니다.

참조를 발급했다고 임의의 HDF5 object reference를 역참조하는 것은 아닙니다. HDF5 object/region reference dtype는 metadata만 제공하며 자동으로 따라가지 않습니다.

### 여러 파일과 SQL 조합

같은 내부 선택 경로를 여러 파일에 적용합니다. 위치형 파일 인자는 옵션보다 먼저 나열합니다.

sources=a.h5,b.h5 목록도 사용할 수 있습니다. 명시한 source 순서를 보존하고 glob은 준비한 파일 목록을 사용합니다. 결과 순서를 고정하려면 SQL ORDER BY를 명시합니다. glob은 단일 source의 패턴을 확장하는 방식이며, 여러 위치형 인자나 sources 목록의 각 항목은 실제 파일 경로다. READ('a*.h5', 'b*.h5')처럼 목록 안의 여러 패턴을 각각 확장하는 방식은 지원하지 않습니다.

union_by_name=true가 기본값입니다. 이름이 같고 호환되는 컬럼을 결합하고, 특정 파일에 없는 컬럼은 그 파일의 행에서 NULL입니다. false이면 컬럼 수·순서·타입이 맞아야 합니다. 같은 이름이라고 다른 dtype를 임의 변환하지는 않습니다.

호환되는 혼합 endian이나 enum 파일도 원래 타입 정보를 파일별로 보존합니다. 상세 `_META`.types의 type_id와 catalog definitions를 연결하면 현재 행의 원래 정의를 찾을 수 있습니다. 두 번째 파일만 선언이 바뀌어도 schema·mapping guard에 반영합니다.

filename=true의 가상 컬럼에는 실제 파일 경로가 들어간다. 원래 동명 필드와 충돌하면 names로 구분합니다. 가상 filename의 반환 타입은 VARCHAR/TEXT만 지정할 수 있습니다.

READ는 WHERE·집계·GROUP BY·JOIN·CTE·UNION ALL과 함께 사용합니다.

### 오류 처리, 권한과 한도

on_error=error가 기본값입니다. skip은 완전한 원본 행의 회복 가능한 native 변환 오류에만 적용합니다. SQL 함수·표현식이나 별도 projection 출력 변환의 오류를 일괄 무시하는 설정은 아닙니다. 권한·파일 I/O·압축·손상·자원·취소 오류는 skip하지 않습니다.

회복 가능한 원본 변환 오류 행을 별도로 확인하려면 rejects view를 사용합니다. ROW는 SQL에서 큰따옴표로 감싼다.

일반 사용자는 directory READ 권한이 필요합니다. 관리자는 기존 구문으로 부여·회수합니다.

Windows 일반 사용자의 directory READ 권한은 `E:/data`처럼 drive가 있는 로컬 NTFS 경로를 사용합니다. drive root 자체의 grant, UNC/device 경로, reparse point·junction·symlink, SUBST drive, ADS, case-sensitive directory 등 안전하게 승인할 수 없는 경로는 거부합니다. 예제의 `/data`는 실제 서버 경로로 바꾸며 Windows에서도 `/data`를 Unix 절대 경로로 가정하지 않습니다.

위 최대치 이내라도 작업·metadata 예산에 따라 더 일찍 거부될 수 있습니다.

SQL·VLEN·작업 buffer는 예산에 계상하지만 공식 HDF5 내부 heap 전체의 정확한 statement hard limit을 보장하지는 않습니다. Attribute VLEN의 내부 임시 할당은 공개 DXPL callback을 쓸 수 없어 복사 후 즉시 반환하는 한계가 있습니다.

외부 links·VDS·external raw storage, family/multi driver, 임의 동적 plugin, 활성 SWMR 의존은 지원하지 않습니다. 내부 hard/soft link는 순환·깊이를 제한해 탐색합니다. 미지원 객체는 목록·진단에 남기며 정상 dataset을 명시해 조회할 수 있습니다. 단위·시간 정보를 담은 속성을 timestamp 타입으로 자동 해석하지 않습니다.


## 관련 문서

- [구조와 컬럼 확인](../../inspect/)
- [구조화된 값과 원문 추출](../../extract/)
- [권한과 운영](../../operations/)
