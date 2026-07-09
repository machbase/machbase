---
title: '5.6 인덱스와 성능'
weight: 60
toc: true
---
인덱스와 성능에 해당하는 세부 문서를 모았습니다.


<a id="index-tuning-tag"></a>

## TAG 인덱스 튜닝

TAG 테이블은 태그명과 시간 축을 기준으로 자동 인덱스가 구성됩니다. 이 페이지에서는 TAG 테이블의 자동 인덱스 구조를 이해하고, 값 컬럼에 추가로 생성할 수 있는 TAG/KV secondary index 활용 기준을 설명합니다.

### 자동 3단계 파티션 인덱스

TAG 테이블에 데이터를 삽입하면 Machbase는 내부적으로 다음과 같은 3단계 인덱스 구조를 자동 유지합니다.

```
태그명 (PRIMARY KEY)
  └──► 시간 파티션 범위
          └──► 파티션 내 컬럼 값
```

| 단계 | 역할 | 자동 여부 |
|-----|------|---------|
| 1단계: 태그명 인덱스 | 특정 태그(센서)를 O(log n)으로 검색 | 자동 |
| 2단계: 시간 파티션 | 시간 범위에 해당하는 파티션만 스캔 | 자동 |
| 3단계: 파티션 내 값 통계 | SUMMARIZED 컬럼의 집계·범위 조회 보조 | 자동 |

#### 인덱스를 최대한 활용하는 쿼리 패턴

모든 3단계 인덱스를 사용하는 최적 쿼리입니다.

```sql
-- 최적: 태그명 + 시간 범위 + 값 조건 모두 명시
SELECT * FROM sensor_tag
WHERE name = 'sensor_A'
  AND time BETWEEN TO_DATE('2026-07-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
               AND TO_DATE('2026-07-01 23:59:59', 'YYYY-MM-DD HH24:MI:SS')
  AND value > 80.0;
```

태그명 없이 값 조건만 사용하면 전체 태그를 순차 스캔합니다.

```sql
-- 비효율: 태그명 없음 → 모든 태그 파티션 스캔
SELECT * FROM sensor_tag WHERE value > 80.0;
```

### METADATA 컬럼 인덱스

TAG 테이블에서 메타데이터 속성(예: 센서 유형, 설치 위치, 담당 팀 등)으로 태그를 필터링하는 경우, METADATA 컬럼을 사용합니다. 검증한 빌드에서는 TAG 테이블 생성 시 METADATA 컬럼에 인덱스가 자동 생성되므로, 같은 컬럼에 `CREATE INDEX`를 다시 실행하면 이미 인덱스가 있다는 오류가 반환됩니다.

```sql
-- TAG 테이블 생성 예시 (METADATA 컬럼 포함)
CREATE TAG TABLE sensor_tag (
    name     VARCHAR(64) PRIMARY KEY,
    time     DATETIME BASETIME,
    value    DOUBLE SUMMARIZED
) METADATA (
    sensor_type   VARCHAR(32),
    install_loc   VARCHAR(128),
    team_name     VARCHAR(64)
);
```

```sql
-- sensor_type에는 이미 인덱스가 있으므로 다시 생성하지 않음
CREATE INDEX idx_type ON sensor_tag METADATA (sensor_type);
-- [ERR-02174: The index already exists in the column(SENSOR_TYPE).]
```

```sql
-- 인덱스 활용 쿼리 예시
SELECT name, time, value
FROM sensor_tag
WHERE sensor_type = 'temperature'
  AND time BETWEEN TO_DATE('2026-07-01', 'YYYY-MM-DD')
               AND TO_DATE('2026-07-08', 'YYYY-MM-DD');
```

> METADATA는 태그 속성 정보로, 시계열 데이터 Append와 독립적인 경로로 처리됩니다. 태그 속성으로 자주 필터링해야 한다면 TAG 테이블 생성 시 METADATA 컬럼으로 정의합니다.

### Min-Max Cache

Machbase는 LOG 테이블의 `_ARRIVAL_TIME`과 LOG 일반 컬럼에 대해 Min-Max Cache를 제공합니다. TAG 테이블의 값 컬럼에는 이 페이지의 검증 대상 빌드에서 `MINMAX_CACHE_SIZE`를 직접 지정할 수 없습니다. TAG 조회 성능은 태그명, 시간 범위, METADATA 인덱스, ROLLUP 설계로 조정합니다.

```
[파티션 1] MIN=10.0, MAX=50.0 → 검색값 85.0 → 건너뜀
[파티션 2] MIN=60.0, MAX=80.0 → 검색값 85.0 → 건너뜀
[파티션 3] MIN=80.0, MAX=95.0 → 검색값 85.0 → 스캔 ✓
```

#### TAG 값 범위 조회 시 조정 방향

`value > 80.0` 같은 값 조건만으로 넓은 기간을 조회하면 많은 데이터 파티션을 확인해야 합니다. TAG 테이블에서는 먼저 `name`과 `time` 범위를 최대한 좁히고, 반복 집계 쿼리는 ROLLUP을 사용합니다.

```sql
SELECT name, time, value
FROM   sensor_tag
WHERE  name = 'TEMP-01'
  AND  time BETWEEN '2026-07-07 10:00:00' AND '2026-07-07 11:00:00'
  AND  value > 80.0;
```

LOG 테이블 컬럼의 `MINMAX_CACHE_SIZE` 조정은 [메모리 설정 튜닝](/dbms/performance-tuning/cache-tuning-memory/#tuning-memory-configuration)을 참조하세요.

### 값 컬럼 TAG/KV 인덱스

TAG 테이블의 시계열 값 컬럼(`value`, `temperature` 등)에는 TAG/KV secondary index를 생성할 수 있습니다. 값 조건을 단독으로 자주 사용하거나, 태그명과 시간 범위로 좁힌 뒤 값 조건을 추가로 적용하는 조회가 많을 때 검토합니다.

```sql
-- 값 컬럼 TAG/KV 인덱스 생성
CREATE INDEX idx_value ON sensor_tag (value) INDEX_TYPE TAG;
```

검증한 빌드에서 생성된 값 컬럼 인덱스는 `SHOW INDEXES` 결과의 `INDEX_TYPE`에
`TAG`로 표시됩니다. `INDEX_TYPE LSM`을 지정해도 TAG 테이블에서는 LOG 테이블의
LSM 인덱스가 아니라 TAG/KV secondary index로 생성됩니다.

단, TAG 테이블의 기본 최적 경로는 여전히 `name`과 `time` 조건입니다. 값 컬럼 TAG/KV 인덱스는 조회 조건을 보조하지만, 넓은 시간 범위 전체를 자주 조회하는 집계 워크로드는 ROLLUP으로 처리하는 편이 적합합니다.

**생성할 수 없는 패턴**:

```sql
-- TAG 테이블의 시간 축 컬럼에는 별도 인덱스를 생성할 수 없음
CREATE INDEX idx_time ON sensor_tag (time) INDEX_TYPE LSM;
-- [ERR-02332: Unable to create an index on the column (TIME).]
```

### 핵심 정리

| 최적화 항목 | 권장 사항 |
|------------|---------|
| 자동 파티션 인덱스 | 별도 생성 불필요, 태그명 + 시간 범위를 항상 WHERE에 포함 |
| METADATA 필터링 | TAG 테이블 생성 시 METADATA 컬럼으로 정의, 인덱스는 자동 생성 |
| 값 범위 조회 | `name`과 `time` 범위를 먼저 좁히고, 반복 집계는 ROLLUP 사용 |
| 값 컬럼 인덱스 | 필요한 경우 `CREATE INDEX ... ON tag_table(value) INDEX_TYPE TAG`로 TAG/KV 인덱스 생성 |

<a id="original-85-tag-indexes"></a>

## Tag 테이블 인덱스

> **8.5 원문 보강 자료**: 이 문서는 기존 8.5 매뉴얼의 내용을 새 장 구조에 맞춰 보존한 것입니다. Machbase 8.6 기준과 표현이 다른 부분은 같은 절의 최신 리뉴얼 문서를 우선합니다.

### 개요

tag 테이블의 인덱스는 추가 컬럼이나 JSON 경로로 검색할 때 쿼리 성능을 크게 향상시킵니다. 이 가이드는 TAG 인덱스를 효과적으로 생성하고 관리하는 방법을 다룹니다.

### TAG 인덱스란?

Machbase TAG 테이블에 TAG 인덱스 유형을 생성할 수 있습니다.

자세한 내용은 SQL 참조의 DDL 섹션을 참조하세요.

* TAG Index: TAG 인덱스는 TAG 테이블의 추가 컬럼에 생성할 수 있습니다.


### 인덱스 생성

CREATE INDEX 문을 사용하여 특정 컬럼에 인덱스를 생성합니다.

```sql
CREATE INDEX index_name ON table_name (column_name) [index_type]
    index_type ::= INDEX_TYPE { TAG }
```

```bash
Mach> CREATE INDEX id_index ON tag (id) INDEX_TYPE TAG;
Created successfully.
```

버전 7.5부터는 tag 테이블에서만 json 타입 컬럼에 대해 각 json 경로마다 인덱스를 생성할 수 있습니다.

기존 인덱스 생성 구문에 연산자로 json 경로를 연결하기만 하면 됩니다.

json 연산자의 반환 타입은 VARCHAR이므로 VARCHAR를 비교할 때만 인덱스가 사용됩니다.

```bash
Mach> CREATE TAG TABLE tag (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, jval JSON);
Executed successfully.

Mach> CREATE INDEX idx_jval_value1 ON tag (jval->'$.value1');
Created successfully.

Mach> CREATE INDEX idx_jval_value2 ON tag (jval->'$.value2');
Created successfully.

Mach> EXPLAIN SELECT * FROM tag WHERE jval->'$.value1' = '10';
PLAN
------------------------------------------------------------------------------------
 PROJECT
  TAG READ (RAW)
   KEYVALUE INDEX SCAN (_TAG_DATA_0)
    [KEY RANGE]
     * jval->'$.value1' = '10'
   VOLATILE FULL SCAN (_TAG_META)
[6] row(s) selected.
```

### Tag 메타데이터 JSON path 인덱스

`TAG METADATA` 의 JSON 컬럼에도 path 인덱스를 생성할 수 있습니다.

```sql
CREATE TAG TABLE ships (
    name VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE
)
METADATA (
    status VARCHAR(20),
    info JSON
);

CREATE INDEX idx_ship_owner
ON ships METADATA (info->'$.owner');
```

생성 시 함께 선언할 수도 있습니다.

```sql
CREATE TAG TABLE ships (
    name VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE
)
METADATA (
    info JSON INDEX('name', 'ship.status')
);
```

주의사항:

- metadata JSON path 인덱스는 `CREATE INDEX ... ON TAG METADATA (...)` 문법을 사용합니다.
- `INFO JSON INDEX(...)` 는 생성 시 자주 사용하는 path를 함께 선언하는 방식입니다.
- 현재 JSON path 인덱스는 문자열 literal 비교 중심으로 동작합니다.
- 숫자 literal 비교는 full scan 으로 처리될 수 있습니다.

### 인덱스 삭제

DROP INDEX 문을 사용하여 지정된 인덱스를 삭제합니다. 그러나 테이블을 검색하고 있는 다른 세션이 있으면 오류와 함께 실패합니다.

```sql
DROP INDEX index_name;
```

```bash
Mach> DROP INDEX id_index;
Dropped successfully.
```

metadata JSON path 인덱스도 인덱스 이름만으로 삭제합니다.

```sql
DROP INDEX idx_ship_owner;
```
