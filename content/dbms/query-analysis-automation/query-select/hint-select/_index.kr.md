---
type: docs
title: 'SELECT 힌트 사용'
weight: 80
---

SELECT 힌트는 쿼리 최적화 방향을 명시적으로 지정하는 주석 형태의 지시어입니다.

## 힌트 문법

```sql
SELECT /*+ hint_name(option) */ ...
```

## 이 절에서 다루는 힌트

- **[SAMPLING 힌트](./hint-sampling/)**: TAG 데이터 시간 구간별 샘플링
- **[INTERPOLATION 힌트](./hint-interpolation/)**: TAG 데이터 누락 구간 보간

## 기타 힌트

### PARALLEL

병렬 처리 계수를 지정합니다.

```sql
SELECT /*+ PARALLEL(sensor_log, 8) */ sensor_id, AVG(value)
FROM sensor_log
GROUP BY sensor_id;
```

### NOPARALLEL

병렬 처리를 사용하지 않도록 강제합니다.

```sql
SELECT /*+ NOPARALLEL(sensor_log) */ * FROM sensor_log WHERE value > 50.0;
```

### FULL

인덱스를 사용하지 않고 전체 스캔을 수행합니다. 인덱스보다 풀 스캔이 유리한 경우에 사용합니다.

```sql
SELECT /*+ FULL(sensor_log) */ * FROM sensor_log WHERE value > 50.0;
```

### NO_INDEX

특정 인덱스 사용을 방지합니다.

```sql
SELECT /*+ NO_INDEX(sensor_log, idx_value) */ * FROM sensor_log WHERE value > 50.0;
```

### ROLLUP_TABLE

ROLLUP 조회 시 특정 ROLLUP 테이블을 강제 지정합니다.

```sql
SELECT /*+ ROLLUP_TABLE(tag, _rollup_tag_value_min) */ *
FROM tag WHERE name = 'TEMP-01' DURATION 1 DAY;
```

### SCAN_FORWARD / SCAN_BACKWARD

스캔 방향을 지정합니다. 기본값은 역방향(최신 데이터 먼저)입니다.

```sql
-- 오래된 데이터부터 순방향 스캔
SELECT /*+ SCAN_FORWARD(sensor_log) */ * FROM sensor_log LIMIT 100;

-- 최신 데이터부터 역방향 스캔 (기본값과 동일)
SELECT /*+ SCAN_BACKWARD(sensor_log) */ * FROM sensor_log LIMIT 100;
```

### RID_RANGE

특정 RID(Row ID) 범위의 데이터를 직접 조회합니다. 내부 디버깅이나 특정 구간 데이터 추출에 사용됩니다.

```sql
SELECT /*+ RID_RANGE(table_name, start_rid, end_rid) */ _RID, *
FROM table_name;
```

```sql
-- RID 45부터 50까지 데이터 조회
SELECT /*+ RID_RANGE(TEST, 45, 50) */ _RID, * FROM TEST;
```

> `_RID`는 Machbase 내부 행 식별자입니다. 일반적인 운영 쿼리에서는 사용하지 않으며, RID_RANGE 힌트도 디버깅 목적으로만 사용합니다.
