---
type: docs
title: 'TAG 인덱스 튜닝'
weight: 10
---

TAG 테이블은 `CREATE INDEX`를 실행하지 않아도 자동으로 인덱스가 구성됩니다. 이 페이지에서는 TAG 테이블의 자동 인덱스 구조를 이해하고, 추가로 활용할 수 있는 최적화 옵션을 설명합니다.

## 자동 3단계 파티션 인덱스

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
| 3단계: 파티션 내 값 인덱스 | SUMMARIZED 컬럼의 범위 조회 가속 | 자동 |

### 인덱스를 최대한 활용하는 쿼리 패턴

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

## METADATA 컬럼에 LSM 인덱스 생성

TAG 테이블에서 메타데이터 속성(예: 센서 유형, 설치 위치, 담당 팀 등)으로 태그를 필터링하는 경우, METADATA 컬럼에 LSM 인덱스를 생성하면 검색 속도를 높일 수 있습니다.

```sql
-- TAG 테이블 생성 예시 (METADATA 컬럼 포함)
CREATE TAG TABLE sensor_tag (
    name     VARCHAR(64) PRIMARY KEY,
    time     DATETIME BASETIME,
    value    DOUBLE SUMMARIZED,
    sensor_type   VARCHAR(32) METADATA,
    install_loc   VARCHAR(128) METADATA,
    team_name     VARCHAR(64) METADATA
);
```

```sql
-- sensor_type으로 자주 필터링하는 경우 인덱스 생성
CREATE INDEX idx_type ON sensor_tag METADATA (sensor_type);
```

```sql
-- 인덱스 활용 쿼리 예시
SELECT name, time, value
FROM sensor_tag
WHERE sensor_type = 'temperature'
  AND time BETWEEN TO_DATE('2026-07-01', 'YYYY-MM-DD')
               AND TO_DATE('2026-07-08', 'YYYY-MM-DD');
```

> METADATA 컬럼에 인덱스를 생성해도 시계열 데이터 삽입 성능에는 거의 영향을 미치지 않습니다. METADATA는 태그 속성 정보로, 시계열 데이터 Append와 독립적인 경로로 처리됩니다.

## Min-Max Cache 조정

Machbase는 각 파티션의 특정 컬럼에 대해 최솟값·최댓값을 메모리에 유지하는 **Min-Max Cache**를 제공합니다. 이 캐시 덕분에 검색 대상 값이 파티션의 범위를 벗어나면 해당 파티션 전체를 건너뛸 수 있습니다.

```
[파티션 1] MIN=10.0, MAX=50.0 → 검색값 85.0 → 건너뜀
[파티션 2] MIN=60.0, MAX=80.0 → 검색값 85.0 → 건너뜀
[파티션 3] MIN=80.0, MAX=95.0 → 검색값 85.0 → 스캔 ✓
```

### MINMAX_CACHE_SIZE 설정

`value` 컬럼처럼 범위 조회가 잦은 컬럼은 캐시 크기를 늘려 더 많은 파티션 정보를 메모리에 유지합니다.

```sql
-- 테이블 생성 시 캐시 크기 지정 (단위: bytes)
CREATE TAG TABLE sensor_tag (
    name  VARCHAR(64) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE SUMMARIZED PROPERTY(MINMAX_CACHE_SIZE = 102400)  -- 100KB
);
```

```sql
-- 기존 테이블 컬럼의 캐시 크기 변경
ALTER TABLE sensor_tag MODIFY COLUMN value SET MINMAX_CACHE_SIZE = 102400;
```

| 항목 | 기본값 |
|------|--------|
| 일반 컬럼 MINMAX_CACHE_SIZE | 10KB (10240 bytes) |
| `_ARRIVAL_TIME` 숨김 컬럼 | 100MB (자동 적용) |
| VARCHAR 컬럼 | 0 고정 (캐시 미지원) |

- 파티션 수가 증가할수록 설정된 크기만큼 메모리 사용량이 점진적으로 늘어납니다.
- 조회 빈도가 낮은 컬럼은 기본값(10KB)을 유지하거나 0으로 설정해 메모리를 절약합니다.

## 시계열 데이터 컬럼에 별도 인덱스는 불필요

TAG 테이블의 시계열 데이터 컬럼(`value`, `temperature` 등)에 `CREATE INDEX`로 추가 인덱스를 생성하는 것은 지원되지 않으며, 이미 자동 파티션 인덱스와 Min-Max Cache가 값 범위 조회를 효율적으로 처리합니다.

**피해야 할 패턴**:

```sql
-- TAG 테이블의 시계열 컬럼에 별도 인덱스는 불필요하며 지원되지 않음
CREATE INDEX idx_value ON sensor_tag (value);  -- 지원되지 않음
```

## 핵심 정리

| 최적화 항목 | 권장 사항 |
|------------|---------|
| 자동 파티션 인덱스 | 별도 생성 불필요, 태그명 + 시간 범위를 항상 WHERE에 포함 |
| METADATA 필터링 | 자주 사용하는 METADATA 컬럼에 LSM 인덱스 생성 |
| Min-Max Cache | 값 범위 조회가 잦은 컬럼의 MINMAX_CACHE_SIZE 증가 |
| 시계열 컬럼 인덱스 | 추가 인덱스 생성 불필요 (자동 구조가 처리) |
