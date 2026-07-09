---
type: docs
title: '17.1.5 SELECT 힌트 사전'
weight: 50
---

SELECT 문에서 사용 가능한 모든 힌트의 빠른 참조 목록입니다.

힌트는 `SELECT` 키워드 바로 뒤의 `/*+ ... */` 블록에 작성합니다.

```sql
SELECT /*+ hint_name(args) */ ...
```

## 실행 계획 제어 힌트

| 힌트 | 문법 | 적용 대상 | 효과 |
|------|------|-----------|------|
| `PARALLEL` | `/*+ PARALLEL(table, n) */` | LOG, TAG | 병렬 처리 스레드 수 지정 |
| `NOPARALLEL` | `/*+ NOPARALLEL(table) */` | LOG, TAG | 병렬 처리 비활성화 |
| `FULL` | `/*+ FULL(table) */` | LOG, TAG, LOOKUP | 인덱스 스캔 대신 풀 스캔 강제 |
| `NO_INDEX` | `/*+ NO_INDEX(table, index) */` | LOG, TAG | 특정 인덱스 비사용 |
| `RID_RANGE` | `/*+ RID_RANGE(table, start, end) */` | LOG | RID 범위로 스캔 제한 |
| `SCAN_FORWARD` | `/*+ SCAN_FORWARD(table) */` | LOG (Standard Edition) | 가장 오래된 레코드부터 스캔 |
| `SCAN_BACKWARD` | `/*+ SCAN_BACKWARD(table) */` | LOG (Standard Edition) | 가장 최신 레코드부터 스캔 |

## ROLLUP 제어 힌트

| 힌트 | 문법 | 적용 대상 | 효과 |
|------|------|-----------|------|
| `ROLLUP_TABLE` | `/*+ ROLLUP_TABLE(rollup_name) */` | TAG | 특정 ROLLUP 테이블 강제 선택 |

- 힌트가 없으면 옵티마이저가 자동으로 ROLLUP 테이블을 선택합니다.
- 조건부 ROLLUP을 반드시 사용해야 하는 경우 힌트로 지정합니다.
- `FIRST()` / `LAST()` 함수 사용 시 `EXTENSION` 타입 ROLLUP을 힌트로 지정해야 합니다.

## TAG 테이블 전용 힌트

| 힌트 | 문법 | 적용 대상 | 효과 |
|------|------|-----------|------|
| `INTERPOLATION` | `/*+ INTERPOLATION(time_col) */` | TAG | 누락 시간 구간 선형 보간 |
| `INTERPOLATION` | `/*+ INTERPOLATION(col method interval_ns) */` | TAG | 지정 방법으로 보간 (LINEAR, PREV) |
| `SAMPLING` | `/*+ SAMPLING(time_col, 'interval', count) */` | TAG | 구간별 N건 샘플 반환 |

## 힌트 상세 설명 링크

- [PARALLEL / NOPARALLEL](/dbms/reference/sql/syntax-dictionary-sql/select-hint-syntax/) — 병렬 처리 제어
- [FULL / NO_INDEX](/dbms/reference/sql/syntax-dictionary-sql/select-hint-syntax/) — 인덱스 사용 제어
- [ROLLUP_TABLE](/dbms/reference/sql/syntax-dictionary-sql/select-hint-syntax/) — ROLLUP 테이블 선택
- [INTERPOLATION hint](/dbms/reference/sql/syntax-dictionary-sql/select-hint-syntax/interpolation-hint/) — 보간 힌트 상세
- [SAMPLING hint](/dbms/reference/sql/syntax-dictionary-sql/select-hint-syntax/sampling-hint/) — 샘플링 힌트 상세

## 예시

```sql
-- 병렬 처리
SELECT /*+ PARALLEL(sensor_log, 8) */ sensor, AVG(value)
  FROM sensor_log
 WHERE ts BETWEEN TO_DATE('2024-01-01', 'YYYY-MM-DD')
               AND TO_DATE('2024-01-31', 'YYYY-MM-DD')
 GROUP BY sensor;

-- 풀 스캔 강제
SELECT /*+ FULL(sensor_log) */ * FROM sensor_log WHERE value > 100;

-- 인덱스 비사용
SELECT /*+ NO_INDEX(sensor_log, idx_ts) */ * FROM sensor_log
 WHERE ts > TO_DATE('2024-01-01', 'YYYY-MM-DD');

-- ROLLUP 테이블 강제 선택
SELECT /*+ ROLLUP_TABLE(_tag_rollup_cond_1s) */
       name, rollup('sec', 30, time) AS rt, AVG(value)
  FROM tag
 WHERE name = 'TEMP-01'
   AND time BETWEEN '2024-01-01 00:00:00' AND '2024-01-01 00:10:00'
 GROUP BY rt ORDER BY rt;

-- 보간 (TAG 테이블 전용)
SELECT /*+ INTERPOLATION(time) */ name, time, value
  FROM sensor_tag
 WHERE name = 'TEMP-01' DURATION 1 HOUR;

-- 샘플링 (TAG 테이블 전용)
SELECT /*+ SAMPLING(time, '1 min', 1) */ name, time, value
  FROM sensor_tag
 WHERE name = 'TEMP-01' DURATION 1 DAY;

-- 과거 레코드부터 스캔 (LOG 테이블, Standard Edition)
SELECT /*+ SCAN_FORWARD(app_log) */ _ARRIVAL_TIME, value
  FROM app_log LIMIT 10;
```

## 관련 문서

- [SELECT hint syntax](/dbms/reference/sql/syntax-dictionary-sql/select-hint-syntax/) — 힌트 문법 개요
