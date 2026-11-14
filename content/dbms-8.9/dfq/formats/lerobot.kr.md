---
type: docs
title: '12.4.10 LeRobot'
weight: 100
toc: true
---

서버에 준비한 LeRobot v2.1/v3.0 디렉터리를 하나의 데이터셋으로 읽습니다. 포함된 학습용 샘플은 200 step·2 episode입니다. 상태·동작 값은 학습용 합성 데이터이며 영상 프레임과 물리적으로 동기화된 측정값이 아닙니다. 미디어 참조와 미디어 디코딩은 별개입니다.

## 실습 준비

[실습 파일 묶음](/assets/dbms-8.9/dfq/samples.zip)을 **DB 서버**의 `/srv/dfq`에 풉니다.
경로가 다르면 SQL의 `/srv/dfq`를 실제 서버 경로로 바꿉니다. 접속과 권한 준비는
[시작하기](../../getting-started/)를 참고합니다. SQL마다 별도의 준비 명령 없이 같은 입력을 사용합니다.
센서 샘플의 id=1~5, v=id×10이므로 COUNT=5, SUM(id)=15, SUM(v)=150입니다.
LeRobot 샘플은 이 센서 파일과 별개입니다.

## 작업별 빠른 찾기

| 목적 | 조합한 설정 | 예제 |
|---|---|---|
| v3 데이터셋의 step 수 | `format`, `target`, `parallel` | [예제 1](#example-1) |
| 특정 episode의 step 조회 | `format`, `target`, `parallel` | [예제 2](#example-2) |
| episode 길이와 원본 정보 | `format`, `target`, `columns` | [예제 3](#example-3) |
| task의 텍스트 조회 | `format`, `target`, `columns` | [예제 4](#example-4) |
| 미디어 자산 목록 확인 | `format`, `target`, `columns` | [예제 5](#example-5) |
| 출력 컬럼과 타입 확인 | `format`, `target`, `mode`, `view` | [예제 6](#example-6) |
| v2.1 데이터셋의 step 조회 | `format`, `target`, `parallel` | [예제 7](#example-7) |
| 선택 미디어의 원본 바이트 추출 | target·row·mode와 media_id·raw 표현 | [예제 8](#example-8) |
| step의 동작 배열을 원소로 조회 | target·row·mode와 field | [예제 9](#example-9) |

## 파일과 조회 대상

```text
dataset root
 ├─ meta/info.json              → 버전·feature·data/media 경로 선언
 ├─ meta의 episode/task 정보     → target=episodes / tasks
 ├─ data의 Parquet step 정보     → target=steps
 └─ 미디어 경로/내장 자산 참조    → target=media

 v2.1: episode별 파일
 v3.0: 공유 shard와 episode의 행 구간

 media 목록/참조 ≠ 영상·음성·이미지 디코딩
```

## 전체 포맷 옵션

| 옵션 | 기본값 | 허용값·범위 | 역할 |
|---|---|---|---|
| `names` | 지정하지 않음 | CSV 인용을 사용하는 쉼표 목록 | 원본 순서대로 출력 컬럼명 지정 |
| `type.*` | 지정하지 않음 | 아래 설명의 문자열·타입 규칙 | 컬럼별 SQL 타입. * 위치에 컬럼명 사용 |
| `parallel` | auto | auto,false | 실행 정책. 아래 지원 조합 확인 |
| `on_error` | error | error | error만 지원. 오류 행 건너뛰기 미지원 |
| `union_by_name` | false | false만 지원 | 여러 입력의 컬럼 결합 정책. 아래 reader별 제약 확인 |
| `media_id` | 지정하지 않음 | 아래 설명의 문자열·타입 규칙 | 안정적인 미디어 자산 식별자 선택 |
| `filename` | false | false | 출처 파일명 컬럼 추가 |
| `sources` | 지정하지 않음 | CSV 인용을 사용하는 쉼표 목록 | 순서 있는 파일 목록. 위치형·source와 혼용 금지 |

공통 mode·columns·target·row·field·project·column·source·raw 설정은
[READ 공통 옵션](../../read-options/)을 함께 적용합니다. 위 표의 값 목록은 입력 형식이며
아래 제약에서 제한한 값은 해당 reader에서 실행할 수 없습니다. 특히 parallel의 등록된 값 목록이
실제 병렬 처리 지원을 뜻하지 않습니다. view별 상세 설정은 inspect의 options/capabilities도 확인합니다.

## 우선순위와 허용 조합

입력은 데이터셋 root 하나입니다. sources의 여러 root, filename=true, parallel=true는 지원하지 않습니다. task·episode·step은 별도 target이며 episode ID는 row가 아닙니다. 외부 파일은 root 아래의 허용된 상대 경로를 사용합니다. 영상·음성·이미지의 재생·재인코딩·프레임 디코딩은 클라이언트가 수행합니다.

## 옵션 조합 예제

<a id="example-1"></a>

### 1. v3 데이터셋의 step 수

데이터셋 전체의 step을 읽습니다.

```sql
SELECT COUNT(*) AS N
FROM READ('/srv/dfq/lerobot/v30', 'format=lerobot', 'target=steps',
 'parallel=false') ;
```

반환 컬럼: `N`. 반환 행 수: 1.

다음은 처음 최대 3행의 표시입니다. 긴 값은 미리보기로 줄였습니다.

| N |
| --- |
| 200 |

[SQL 다운로드](/assets/dbms-8.9/dfq/lerobot/01.sql)

<a id="example-2"></a>

### 2. 특정 episode의 step 조회

row 번호와 episode ID는 다르므로 episode는 SQL 조건으로 선택합니다.

```sql
SELECT episode_index,frame_index,"index"
FROM READ('/srv/dfq/lerobot/v30', 'format=lerobot', 'target=steps',
 'parallel=false') WHERE episode_index=42 ORDER BY "index" LIMIT 3;
```

반환 컬럼: `episode_index`, `frame_index`, `index`. 반환 행 수: 3.

다음은 처음 최대 3행의 표시입니다. 긴 값은 미리보기로 줄였습니다.

| episode_index | frame_index | index |
| --- | --- | --- |
| 42 | 0 | 100 |
| 42 | 1 | 101 |
| 42 | 2 | 102 |

[SQL 다운로드](/assets/dbms-8.9/dfq/lerobot/02.sql)

<a id="example-3"></a>

### 3. episode 길이와 원본 정보

episode 단위 metadata를 조회합니다.

```sql
SELECT episode_index,"length"
FROM READ('/srv/dfq/lerobot/v30', 'format=lerobot', 'target=episodes',
 'columns=native') ORDER BY episode_index;
```

반환 컬럼: `episode_index`, `length`. 반환 행 수: 2.

다음은 처음 최대 3행의 표시입니다. 긴 값은 미리보기로 줄였습니다.

| episode_index | length |
| --- | --- |
| 10 | 100 |
| 42 | 100 |

[SQL 다운로드](/assets/dbms-8.9/dfq/lerobot/03.sql)

<a id="example-4"></a>

### 4. task의 텍스트 조회

task와 step을 구분합니다.

```sql
SELECT task_index,task
FROM READ('/srv/dfq/lerobot/v30', 'format=lerobot', 'target=tasks',
 'columns=native') ORDER BY task_index;
```

반환 컬럼: `task_index`, `task`. 반환 행 수: 2.

다음은 처음 최대 3행의 표시입니다. 긴 값은 미리보기로 줄였습니다.

| task_index | task |
| --- | --- |
| 0 | pick red block |
| 1 | place blue block 한글 |

[SQL 다운로드](/assets/dbms-8.9/dfq/lerobot/04.sql)

<a id="example-5"></a>

### 5. 미디어 자산 목록 확인

미디어 참조의 존재와 실제 디코딩은 별개입니다.

```sql
SELECT media_id,path,kind
FROM READ('/srv/dfq/lerobot/v30', 'format=lerobot', 'target=media',
 'columns=native') LIMIT 3;
```

반환 컬럼: `media_id`, `path`, `kind`. 반환 행 수: 2.

다음은 처음 최대 3행의 표시입니다. 긴 값은 미리보기로 줄였습니다.

| media_id | path | kind |
| --- | --- | --- |
| videos/observation.images.front/chunk-000/file-000.mp4 | videos/observation.images.front/chunk-000/file-000.mp4 | video |
| videos/observation.images.wrist/chunk-000/file-000.mp4 | videos/observation.images.wrist/chunk-000/file-000.mp4 | video |

[SQL 다운로드](/assets/dbms-8.9/dfq/lerobot/05.sql)

<a id="example-6"></a>

### 6. 출력 컬럼과 타입 확인

점이 들어간 원본 컬럼은 SQL에서 큰따옴표로 선택합니다.

```sql
SELECT COLUMN_NAME,SQL_TYPE
FROM READ('/srv/dfq/lerobot/v30', 'format=lerobot', 'target=steps',
 'mode=inspect',
 'view=columns') ORDER BY COLUMN_ORDINAL;
```

반환 컬럼: `COLUMN_NAME`, `SQL_TYPE`. 반환 행 수: 9.

다음은 처음 최대 3행의 표시입니다. 긴 값은 미리보기로 줄였습니다.

| COLUMN_NAME | SQL_TYPE |
| --- | --- |
| episode_index | LONG |
| frame_index | LONG |
| index | LONG |

[SQL 다운로드](/assets/dbms-8.9/dfq/lerobot/06.sql)

<a id="example-7"></a>

### 7. v2.1 데이터셋의 step 조회

같은 SQL 인터페이스로 v2.1의 episode별 파일을 읽습니다.

```sql
SELECT COUNT(*) AS N
FROM READ('/srv/dfq/lerobot/v21', 'format=lerobot', 'target=steps',
 'parallel=false') ;
```

반환 컬럼: `N`. 반환 행 수: 1.

다음은 처음 최대 3행의 표시입니다. 긴 값은 미리보기로 줄였습니다.

| N |
| --- |
| 200 |

[SQL 다운로드](/assets/dbms-8.9/dfq/lerobot/07.sql)

<a id="example-8"></a>

### 8. 선택 미디어의 원본 바이트 추출

media 목록에서 받은 media_id로 자산을 먼저 선택한 뒤 row=0을 지정합니다. MP4 컨테이너 전체의 원래 바이트이며 episode 구간만 자르거나 프레임을 디코딩하지 않습니다.

```sql
SELECT _OFFSET,_LENGTH,_LAST,_CONTENT FROM READ('/srv/dfq/lerobot/v30','format=lerobot','target=media','media_id=videos/observation.images.front/chunk-000/file-000.mp4','row=0','mode=raw','raw.representation=payload_bytes','raw.chunk_bytes=65536') ORDER BY _OFFSET;
```

반환 컬럼: `_OFFSET`, `_LENGTH`, `_LAST`, `_CONTENT`. 반환 행 수: 1.

바이트열은 _OFFSET 순으로 합칩니다. _LENGTH의 합은 제공한 원본 미디어 파일의 크기와 같아야 합니다. _CONTENT의 화면상 hex와 실제 BINARY bytes를 구분합니다.

[SQL 다운로드](/assets/dbms-8.9/dfq/lerobot/08.sql)

<a id="example-9"></a>

### 9. step의 동작 배열을 원소로 조회

원래 첫 step의 action 배열을 펼칩니다. row=0은 episode ID가 아니라 전체 step의 논리 첫 행입니다.

```sql
SELECT * FROM READ('/srv/dfq/lerobot/v30','format=lerobot','target=steps','row=0','mode=elements','field=action');
```

반환 컬럼: `_SOURCE`, `_TARGET`, `_ROW`, `_TIME_NS`, `_CLOCK`, `DATA`, `_META`, `_REFS`, `_ELEMENT`, `_INDEX`. 반환 행 수: 2.

샘플 action의 두 성분이 순서대로 반환됩니다.

[SQL 다운로드](/assets/dbms-8.9/dfq/lerobot/09.sql)

## 오류와 해결

### 지원하지 않는 옵션 사용

```sql
SELECT *
FROM READ('/srv/dfq/lerobot/v30',
 'format=lerobot',
 'unknown_option=true');
```

예상 오류: `INVALID_OPTION`. 등록되지 않은 옵션은 무시되지 않고 INVALID_OPTION으로 거부됩니다. 옵션표의 이름을 사용합니다.

[오류 SQL 다운로드](/assets/dbms-8.9/dfq/lerobot/10.sql)

### 형식 또는 선택 조건 오류

```sql
SELECT *
FROM READ('/srv/dfq/lerobot/v30',
 'format=lerobot',
 'parallel=true');
```

예상 오류: `INVALID_OPTION`. LeRobot은 동기 reader입니다. parallel=auto 또는 false를 사용합니다.

[오류 SQL 다운로드](/assets/dbms-8.9/dfq/lerobot/11.sql)

## 타입·구조·표현의 상세 규칙

### target별 기본 반환 컬럼

| Target | 기본 native 결과 |
|---|---|
| steps | 원본 Parquet의 step 컬럼과 미디어 descriptor |
| episodes | episode_index LONG, length LONG, tasks JSON, data JSON, media JSON, details JSON |
| tasks | task_index LONG, task TEXT |
| media | media_id TEXT, path TEXT, kind VARCHAR, feature TEXT, size LONG, details JSON |

서버 로컬 디렉터리의 LeRobot v2.1/v3.0을 READ()의 하나의 논리 소스로 읽습니다. 일반 JSON/Parquet 파일의 기존 읽기 의미는 유지합니다. 서버에 데이터셋을 미리 내려받아야 하며 Hub 인증·다운로드는 클라이언트/JSH의 역할입니다.

`"observation.state"`는 점을 포함하는 하나의 원본 컬럼명입니다. SQL 컬럼 선택에서는 큰따옴표를 사용합니다. 원래 `timestamp`의 상대 초 값을 보존하며 이를 임의의 Unix epoch DATETIME으로 바꾸지 않습니다. 배열은 원래 순서와 구조를 보존하며 dtype·shape·관절 이름은 metadata로 제공합니다.

공식 v3 task 설명이 pandas의 이름 없는 문자열 index `__index_level_0__`에 저장된 경우에도 `task`로 정규화합니다. episode의 `details`에는 원래 index 행을 보존합니다. `data.slices`는 파일별 `from_row` 포함/`to_row` 제외 범위이며, `media`의 시간 범위는 원본 컨테이너 안의 범위다. 논리 `row` 옵션은 episode ID와 같지 않다.

### 미디어 bytes 얻기

기본 steps는 영상 파일이나 내장 이미지·음성 bytes를 매 행마다 전송하지 않고 descriptor와 재조회 경로를 제공합니다. `target=media`는 영상 자산과 내장/외부 image·audio 자산을 나열합니다. 공유 영상·외부 파일은 경로로 중복을 제거하고 내장 자산은 원본 Parquet 위치·행·feature로 식별합니다.

`_CONTENT`는 SQL BINARY다. 별도 BLOB 타입을 새로 만들지 않습니다. 청크 기본값은64KiB, 허용 범위는1byte~1MiB다. `_OFFSET`은 선택한 **원본 자산 바이트열 내부**의 위치이며 Parquet 파일의 물리 압축 offset이나 영상 시각이 아닙니다. OFFSET 순으로 이어 붙이면 원본 자산을 복원할 수 있습니다.

MP4는 여러 episode를 포함한 원본 컨테이너 전체를 반환합니다. 클라이언트가 episode의 시간 범위로 seek·clip·decode합니다. 컨테이너 안에 음성 트랙이 있으면 그것도 원본 컨테이너의 일부이며 따로 추출하지 않습니다. 내장 PNG/WAV 등은 Parquet cell에 저장된 bytes를 그대로 반환합니다. codec이나 확장자가 알려져 있어도 서버는 재생 가능성을 확인하지 않습니다.

내장 자산의 `size`는 원본 bytes 길입니다. 외부 영상·이미지·음성 파일은 목록 조회에서 본문을 열지 않으므로 `size`가NULL일 수 있습니다. 누락된 미디어도 참조 목록에 남기고 실제 payload 요청 시 오류를 반환합니다.

재조회에는 descriptor 또는 `_REFS`의 `locator.operations.raw_payload.example_sql`을 사용하는 것이 좋다. 생성 SQL은 안정적인 `media_id`와 경로 quoting을 포함합니다. 직접 사용할 때에는 `target=media`, `media_id=<반환된 값>`, `row=0`을 조합할 수 있습니다. 자산 식별자로 한 자산을 선택한 결과의 논리 첫 행이므로 이때 `row=0`입니다.

### 공통 READ 인터페이스와 옵션

기존 `name=value` 인자, native/envelope, list·schema·inspect·elements·nodes·canonical JSON·추가 column/project와 참조 재조회를 연결합니다. 반환 가능한 target은 `mode=inspect, view=targets`로 확인합니다.

LeRobot reader 옵션은 `names`, `type.*`, `parallel`, `on_error`, `union_by_name`, `media_id`다. `parallel`은auto/false만 허용하고 동기 방식으로 읽습니다. 손상 행을 건너뛰지 않으며 `on_error=error`, 동일 step schema의 `union_by_name=false` 정책입니다. 하나의 dataset root만 받으며 `sources`로 여러 root를 합치거나 `filename=true`를 요청하지 않습니다. 다른 형식의 전용 decoder·time·axis 옵션은 지원하지 않습니다.

metadata의 `info` 원문과 선택적인 `stats.json`, `episodes_stats.jsonl` 원문을 schema/type 정의와 facts에 보존합니다. optional 파일은ENOENT일 때만NULL로 처리하며 존재하는 손상 파일·권한 거부·링크는 무시하지 않습니다. 숫자 lexeme는 정밀도를 보존하고 배열 순서와 문자열 타입을 구분합니다. 큰 설명은 기존 READ의 bounded catalog/locator 규약을 따릅니다.

### 일관성·권한·자원 계약


따라서 오류가 난 prepared statement를 정리한 뒤 같은 SQL을 새로 prepare하면 새 metadata를 기준으로 준비할 수 있습니다. 기존 prepared statement의 Execute가 자동으로 성공하는 것으로 해석하지 않습니다. 이 오류 분류에 대한 폐기 계약이며 다른 모든 SQL 오류를 이유 없이 같은 방식으로 처리하는 것은 아닙니다. 같은 SQL의 여러 lease/idle handle과 제한된 cache plan 수가 함께 있는 경우도 stale idle entry가 새 prepare를 계속 방해하지 않아야 합니다.

best_effort는 실제 metadata 파일과 현재 data source의 열린 FD·이름이 가리키는 파일 identity를 검사해 중간 수정·atomic rename을 감지합니다. strong은 실제 캡처한 metadata/data의 동일 source를 Dataset 수명 동안 보존하고 reader가 차용합니다. 아직 읽지 않은 외부 미디어는 그 group snapshot에 포함했다고 표시하지 않습니다. 동일 snapshot의 미디어 재조회 보장을 임의로 yes로 만들지 않습니다.

metadata index 최대1,048,576행, feature 최대4,096개, shape rank 최대64, 열린 의존 파일 최대4,096개다. SQL·Arrow·문서의 실제 메모리 예산과 spool 제한이 먼저 적용될 수 있습니다. 내장 미디어 자산 목록은 bytes를 base64로 복제하지 않고 Arrow의 borrowed bytes/path와 길이를 조사합니다. raw 반환도 원본 cell을 BINARY 청크로 전달합니다.

내부 Parquet schema는 Dataset 소유 scratch arena에 할당하고 각 내부 reader 종료 후 회수합니다. 실제 Arrow·JSON 입력·DOM 예산 소유자는 원래 statement다. schema 단계별 사용량과 runtime 동안의 schema 사용량도 실제 statement 작업 예산에 반영합니다. 개별 recursive field clone 내부 순간 peak까지 새 allocator로 사전 예약하는 정책은 아닙니다. 성공·오류·취소·Dataset 종료 시 Arrow reader→scratch arena→최종 문서 순으로 소유권을 정리합니다.

0행 Parquet의 footer가 있으면 원래 native schema를 사용해 COUNT0을 반환합니다. Parquet 자체가 없는0 episode 데이터셋은 metadata/list를 제공하지만, shape만으로 임의의 SQL step schema를 만들어내지 않고 native steps 조회와 기본 DESC에 SCHEMA_UNAVAILABLE을 반환합니다.

집계에 필요하지 않은 미디어 참조는 가능한 경우 생성하지 않습니다. `COUNT(media_column)`은 실제 미디어 값과 NULL을 확인하며, 미선택 컬럼의 기존 타입 오류 검사도 유지합니다. 행 반환 전 원본 변경·READ 권한 검사를 생략하는 옵션은 추가하지 않습니다.

`READ_COMPOSITE`는 처리 행, logical/native 값, 미디어 참조, source 검사·행 내부 중복 제거, 준비 계획 재사용 횟수를 표시합니다. `plan_admitted`는 준비 계획을 저장했는지 나타내는 상태값입니다. `plan_reuses`는 실제 계획 재사용 횟수이며 같은 실행의 rescan마다 중복 증가하지 않습니다.

준비 계획은 실행별 원본·권한·파일 목록·내용 fingerprint를 확인한 후 사용합니다. 계획 저장 한도나 weak fingerprint의 추가 해시 한도를 넘으면 캐시를 생략해 원래 해석 경로를 사용합니다. 정상 READ 입력의 크기 제한은 아닙니다. Strong은 기존 snapshot SHA256을 재사용합니다.

## 관련 문서

- [구조와 컬럼 확인](../../inspect/)
- [구조화된 값과 원문 추출](../../extract/)
- [권한과 운영](../../operations/)
