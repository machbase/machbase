---
type: docs
title: 'SELECT 기본 조회'
weight: 10
---

## SELECT 기본 구문

```sql
SELECT target_list [FROM table_list]
[WHERE condition_expr]
[GROUP BY expr] [HAVING expr]
[ORDER BY expr [DESC]] [SERIES BY expr]
[LIMIT n[,n]]
[DURATION duration_expr];
```

## 기본 예시

```sql
-- 전체 조회
SELECT * FROM sensor_log;

-- 특정 컬럼 조회
SELECT sensor_id, ts, value FROM sensor_log;

-- 컬럼 별칭
SELECT sensor_id AS id, value AS temp FROM sensor_log;

-- 수식 활용
SELECT sensor_id, value * 1.8 + 32 AS fahrenheit FROM sensor_log;
```

## FROM 절 없는 SELECT

테이블 조회 없이 상수, 계산식, 함수 결과를 1행으로 반환합니다.

```sql
SELECT 1;
SELECT 'alive';
SELECT 1 + 2;
SELECT ABS(-7);
SELECT NOW;
```

## CASE 문

```sql
-- 조건별 분기
SELECT sensor_id, value,
    CASE
        WHEN value > 80.0 THEN 'HIGH'
        WHEN value > 50.0 THEN 'NORMAL'
        ELSE 'LOW'
    END AS level
FROM sensor_log;

-- 컬럼 값 매핑
SELECT sensor_id,
    CASE status
        WHEN 'A' THEN 'ALARM'
        WHEN 'N' THEN 'NORMAL'
        ELSE 'UNKNOWN'
    END AS status_label
FROM device_status;
```

## 서브쿼리

```sql
-- WHERE에서 서브쿼리
SELECT * FROM sensor_log
WHERE value > (SELECT AVG(value) FROM sensor_log);

-- SELECT 절에서 단일 값 서브쿼리
SELECT sensor_id, value,
    (SELECT MAX(value) FROM sensor_log) AS max_val
FROM sensor_log;

-- IN + 서브쿼리
SELECT * FROM sensor_log
WHERE sensor_id IN (
    SELECT sensor_id FROM alarm_threshold WHERE high_limit < 80.0
);
```

> Machbase는 상관 서브쿼리(외부 쿼리 컬럼 참조)를 지원하지 않습니다.

## 집합 연산자 (UNION ALL)

Machbase는 `UNION ALL`만 지원합니다. 두 SELECT의 컬럼 수와 타입이 호환되어야 합니다.

```sql
SELECT sensor_id, value FROM sensor_log WHERE value > 90.0
UNION ALL
SELECT sensor_id, value FROM backup_log WHERE value > 90.0;
```

결과의 컬럼명은 좌측 SELECT의 컬럼명을 사용합니다.

## 집계 함수

```sql
SELECT
    sensor_id,
    COUNT(*) AS cnt,
    AVG(value) AS avg_val,
    MAX(value) AS max_val,
    MIN(value) AS min_val,
    SUM(value) AS sum_val
FROM sensor_log
GROUP BY sensor_id;
```
