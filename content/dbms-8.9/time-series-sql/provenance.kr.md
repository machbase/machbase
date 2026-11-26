---
type: docs
title: '13.9 SOURCE와 PROVENANCE: 원본 관측 추적'
weight: 90
toc: true
---

[WITH SOURCE·WITH PROVENANCE 전체 BNF](../../reference/sql/syntax/source-provenance-syntax/)에서 작성 순서와 인자 제약을 확인합니다.

결과값이 어느 관측에서 왔는지 확인합니다. WITH SOURCE는 안정적인 ID와 clock 정보를 선언하고 WITH PROVENANCE는 결과 마지막에 JSON 컬럼을 추가합니다. 출처를 켜도 데이터 값과 행 수는 유지됩니다.

## 원본 선언

WITH SOURCE는 source alias와 TIMESTAMP 뒤에 둡니다. ID(ID)는 각 원본 행을 식별하는 비NULL scalar 키입니다. 복합 ID도 사용할 수 있으나 서로 다른 원본에 같은 ID를 주지 않습니다. 물리 행 위치를 안정적인 ID로 사용하지 않습니다.

CLOCK_DOMAIN 기본값은 utc입니다. 비UTC 입력은 CLOCK_SESSION도 지정하고 비교 양쪽의 domain/session이 같아야 합니다. 이름만 utc로 바꾸어도 값이 UTC로 변환되지는 않습니다. ORIGINAL_TIME·RECEIVED_TIME은 metadata이며 TIMESTAMP를 자동 교체하지 않습니다. CLOCK_ERROR는 허용차에 자동 가산되지 않습니다.

| SOURCE 항목 | 의미 |
|---|---|
| ID(expr, ...) | 원본 관측의 비NULL 고유 scalar tuple |
| CLOCK_DOMAIN(expr) | clock 이름. 기본 utc |
| CLOCK_SESSION(expr) | 비UTC 실행 세션 식별자. 비UTC에서는 필수 |
| ORIGINAL_TIME(expr) | 원본 DATETIME. 미제공 시 NULL |
| RECEIVED_TIME(expr) | 수신 DATETIME. 미제공 시 NULL |
| CLOCK_VERSION(expr) | 외부 시간 보정 버전 |
| CLOCK_ERROR(expr) | 비음수 정수 나노초 오차. 미제공·NULL은 unknown |

파생 SAMPLE 시간축은 보존된 clock domain/session을 상속합니다. 관측이 전혀 없는 버킷의
clock은 unknown으로 남으며 SOURCE를 생략했다고 UTC 관측으로 바뀌지 않습니다.
서로 다른 clock의 시각을 결합하려면 입력에서 실제 변환·보정을 먼저 수행합니다.

## 출처 JSON 읽기

sources는 SQL 입력 순서, columns는 데이터 출력 순서입니다. 각 원소의 ordinal은 1부터, JSON 배열 첨자는 0부터 시작합니다. selected는 선택 관측, left/right는 보간 양 끝점입니다. status·observed·value_null·reason으로 실제 NULL, 빈 버킷, 미매칭과 채움을 구분합니다.

시각과 기간은 정확한 10진 나노초 **문자열**로 반환합니다. delta_ns는 선택 관측 시각에서 기준 시각을 뺀 값으로, 과거는 음수·미래는 양수입니다. 큰 정수와 DECIMAL을 JSON 부동소수점 숫자로 바꾸지 않습니다. contributors는 최종 값에 기여한 근거이며 입력 관측 목록 전체와 다를 수 있습니다.

아래 표에서는 긴 JSON을 줄여 표시합니다. 각 예제의 전체 결과 JSON 다운로드에서 원본 ID·시각·signed delta 및 보간 양 끝점을 확인할 수 있습니다.

[공통 준비와 정리](../#실습-준비)를 먼저 확인합니다. 아래 SQL은 setup.sql 이후 실행합니다.

## 예제 선택

| 번호 | 목적 | 실행 |
| --- | --- | --- |
| 1 | [과거 관측의 원본과 음수 시간차](#example-1) | 정상 |
| 2 | [미래 선택의 양수 시간차](#example-2) | 정상 |
| 3 | [미매칭과 실제 NULL의 구분](#example-3) | 정상 |
| 4 | [동일 시각을 제외한 원본](#example-4) | 정상 |
| 5 | [보간 양끝의 원본 ID와 시각](#example-5) | 정상 |
| 6 | [같은 비UTC clock session의 결합](#example-6) | 정상 |
| 7 | [다른 clock domain의 결합 거부](#example-7) | 오류 확인 |
| 8 | [명시 원본 ID의 NULL 거부](#example-8) | 오류 확인 |

## 1. 과거 관측의 원본과 음수 시간차 {#example-1}

출처를 켜도 원래 데이터 값과 행 수는 유지합니다. sources 배열의 인덱스는 0부터, ordinal은 1부터입니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/provenance/01.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/provenance/01.json)

```sql
SELECT e.ID,m.VALUE FROM TS13_EVENT e WITH SOURCE(ID(ID),CLOCK_DOMAIN('utc'))
ASOF JOIN TS13_MOTOR m WITH SOURCE(ID(ID),CLOCK_DOMAIN('utc'))
ON e.NAME=m.NAME TOLERANCE 5s WHERE e.ID=2
WITH PROVENANCE AS P;
```

결과 **1행**입니다.

| ID | VALUE | P |
| --- | --- | --- |
| 2 | 324 | 출처 JSON: 전체 결과 참조 |


## 2. 미래 선택의 양수 시간차 {#example-2}

출처를 켜도 원래 데이터 값과 행 수는 유지합니다. sources 배열의 인덱스는 0부터, ordinal은 1부터입니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/provenance/02.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/provenance/02.json)

```sql
SELECT e.ID,m.VALUE FROM TS13_EVENT e WITH SOURCE(ID(ID),CLOCK_DOMAIN('utc'))
NEAREST JOIN TS13_MOTOR m WITH SOURCE(ID(ID),CLOCK_DOMAIN('utc'))
ON e.NAME=m.NAME TOLERANCE 5s WHERE e.ID=2
WITH PROVENANCE AS P;
```

결과 **1행**입니다.

| ID | VALUE | P |
| --- | --- | --- |
| 2 | 484 | 출처 JSON: 전체 결과 참조 |


## 3. 미매칭과 실제 NULL의 구분 {#example-3}

출처를 켜도 원래 데이터 값과 행 수는 유지합니다. sources 배열의 인덱스는 0부터, ordinal은 1부터입니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/provenance/03.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/provenance/03.json)

```sql
SELECT e.ID,m.VALUE FROM TS13_EVENT e WITH SOURCE(ID(ID),CLOCK_DOMAIN('utc'))
ASOF JOIN TS13_MOTOR m WITH SOURCE(ID(ID),CLOCK_DOMAIN('utc'))
ON e.NAME=m.NAME TOLERANCE 5s WHERE e.ID=6
WITH PROVENANCE AS P;
```

결과 **1행**입니다.

| ID | VALUE | P |
| --- | --- | --- |
| 6 | NULL | 출처 JSON: 전체 결과 참조 |


## 4. 동일 시각을 제외한 원본 {#example-4}

출처를 켜도 원래 데이터 값과 행 수는 유지합니다. sources 배열의 인덱스는 0부터, ordinal은 1부터입니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/provenance/04.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/provenance/04.json)

```sql
SELECT e.ID,m.VALUE FROM TS13_EVENT e WITH SOURCE(ID(ID),CLOCK_DOMAIN('utc'))
LT JOIN TS13_MOTOR m WITH SOURCE(ID(ID),CLOCK_DOMAIN('utc'))
ON e.NAME=m.NAME TOLERANCE 5s WHERE e.ID=1
WITH PROVENANCE AS P;
```

결과 **1행**입니다.

| ID | VALUE | P |
| --- | --- | --- |
| 1 | 64 | 출처 JSON: 전체 결과 참조 |


## 5. 보간 양끝의 원본 ID와 시각 {#example-5}

보간값 444의 근거는 18초와 22초 두 원본입니다. 가짜 원본 ID를 만들지 않습니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/provenance/05.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/provenance/05.json)

```sql
SELECT e.ID,m.VALUE FROM TS13_EVENT e WITH SOURCE(ID(ID)) INTERPOLATE JOIN TS13_MOTOR m WITH SOURCE(ID(ID)) ON e.NAME=m.NAME COLUMNS(m.VALUE) MAX GAP 4s WHERE e.ID=2 WITH PROVENANCE AS P;
```

결과 **1행**입니다.

| ID | VALUE | P |
| --- | --- | --- |
| 2 | 444 | 출처 JSON: 전체 결과 참조 |


## 6. 같은 비UTC clock session의 결합 {#example-6}

clock 선언은 시각을 자동 보정하지 않습니다. 서로 비교 가능한 같은 domain/session을 선언합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/provenance/06.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/provenance/06.json)

```sql
SELECT e.ID,m.VALUE FROM TS13_EVENT e WITH SOURCE(ID(ID),CLOCK_DOMAIN('simulation'),CLOCK_SESSION('run1')) ASOF JOIN TS13_MOTOR m WITH SOURCE(ID(ID),CLOCK_DOMAIN('simulation'),CLOCK_SESSION('run1')) ON e.NAME=m.NAME TOLERANCE 5s WHERE e.ID=2 WITH PROVENANCE AS P;
```

결과 **1행**입니다.

| ID | VALUE | P |
| --- | --- | --- |
| 2 | 324 | 출처 JSON: 전체 결과 참조 |


## 7. 다른 clock domain의 결합 거부 {#example-7}

출처 JSON을 출력하지 않아도 clock 비교 규칙은 적용됩니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/provenance/07.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/provenance/07.json)

```sql
SELECT e.ID,m.VALUE FROM TS13_EVENT e WITH SOURCE(ID(ID),CLOCK_DOMAIN('simulation'),CLOCK_SESSION('run1')) ASOF JOIN TS13_MOTOR m WITH SOURCE(ID(ID),CLOCK_DOMAIN('utc')) ON e.NAME=m.NAME WHERE e.ID=2;
```

이 SQL은 오류 동작을 확인하는 예제입니다. 실제 진단:

```text
Syntax error: near token (E_CLOCK_DOMAIN).
```


## 8. 명시 원본 ID의 NULL 거부 {#example-8}

서로 다른 원본 행은 안정적이고 비NULL인 ID로 구분합니다.

[SQL 다운로드](/assets/dbms-8.9/time-series-sql/provenance/08.sql) · [전체 결과 JSON](/assets/dbms-8.9/time-series-sql/provenance/08.json)

```sql
SELECT e.ID,m.VALUE FROM TS13_EVENT e WITH SOURCE(ID(CAST(NULL AS LONG))) ASOF JOIN TS13_MOTOR m WITH SOURCE(ID(ID)) ON e.NAME=m.NAME WHERE e.ID=2 WITH PROVENANCE AS P;
```

이 SQL은 오류 동작을 확인하는 예제입니다. 실제 진단:

```text
2010 - Syntax error: near token (E_PROVENANCE_SOURCE_ID).
```

## READ와 저장 테이블의 출처

선택된 READ 행의 source·target·mapping·locator는 `read_origin`에 있습니다.
strong snapshot의 `read_origin.replay.example_sql`은 revision과 mapping을 고정합니다.
원본 교체나 같은 실행의 재스캔 중 구성 파일 교체는 `SOURCE_CHANGED`로 진단합니다.
고정한 revision을 다시 읽으려면 해당 원본이 필요합니다.

| 저장 원본 | `storage_origin`의 읽기 범위 | 일관성 |
|---|---|---|
| LOG | `log_rid_view` | best_effort |
| TAG | `tag_partition_views` | best_effort |
| 읽기 트랜잭션이 확인된 TRANSACTION | `sqlite_table_snapshot` | 해당 테이블 읽기 범위에서 fixed |

세 저장 범위의 `snapshot`은 NULL입니다. 혼합 질의 전체의 일관성은 각 원본의 범위와 구분합니다.
`query.sql`과 `query.binds`는 실행문과 바인딩을 제공합니다. `query.views`는 확장된
VIEW의 카탈로그 ID, 테이블 ID, 정의 SHA-256을 기록합니다. 이름과 정의의 공개 범위는
`M$SYS_VIEWS` 접근 권한을 따릅니다.
[SQL 셀의 원본 위치](../../dfq/sql-source/#sql-셀의-출처-위치)도 확인할 수 있습니다.

### 원격 주소와 revision

원격 파일을 `source.consistency=strong`으로 읽으면 전체 전송을 마친 바이트로
SHA-256 revision을 계산합니다. `source.expected_revision`으로 같은 원본인지 확인할
수 있습니다. 기본 best_effort에는 공개 SHA-256 revision이 없습니다.

URL의 query 값은 출처와 진단에서 마스킹합니다. query 원문이 필요한 재조회 SQL이나
토큰은 발급하지 않습니다. 사전 서명 URL을 다시 읽을 때는 발급받은 유효한 주소를
새 READ에 전달합니다. 서버 자격증명과 인증 헤더는 결과에 포함하지 않습니다.
[원격 전송과 원본 확인](../../dfq/operations/#remote-read-spool)을 참고합니다.
