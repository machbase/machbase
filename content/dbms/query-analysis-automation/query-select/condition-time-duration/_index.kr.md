---
type: docs
title: '시간 조건과 DURATION'
weight: 30
---

시계열 데이터 조회에서 시간 범위를 효율적으로 지정하는 방법입니다.

## WHERE 시간 조건

DATETIME 컬럼에 직접 조건을 지정합니다.

```sql
-- 특정 시간 범위
SELECT * FROM sensor_log
WHERE ts BETWEEN '2024-01-15 00:00:00' AND '2024-01-15 23:59:59';

-- TO_DATE 함수 사용
SELECT * FROM sensor_log
WHERE ts >= TO_DATE('2024-01-15', 'YYYY-MM-DD')
  AND ts < TO_DATE('2024-01-16', 'YYYY-MM-DD');

-- TAG 테이블 시간 조건
SELECT name, time, value FROM tag
WHERE time BETWEEN '2024-01-15 00:00:00' AND '2024-01-15 12:00:00';
```

## DURATION 키워드

`DURATION`은 `_ARRIVAL_TIME` 컬럼을 기준으로 조회 범위를 쉽고 빠르게 지정합니다. TAG 테이블에서는 BASETIME 컬럼 기준으로 동작합니다.

```sql
DURATION number {YEAR|MONTH|WEEK|DAY|HOUR|MINUTE|SECOND}
         [BEFORE number {YEAR|MONTH|WEEK|DAY|HOUR|MINUTE|SECOND}]

DURATION FROM expr TO expr
```

### 기본 사용법

```sql
-- 최근 1시간 데이터
SELECT * FROM sensor_log DURATION 1 HOUR;

-- 최근 7일 데이터
SELECT * FROM sensor_log DURATION 7 DAY;

-- 최근 1개월
SELECT * FROM sensor_log DURATION 1 MONTH;
```

### BEFORE 절

기준 시점 이전의 특정 구간을 조회합니다.

```sql
-- 1일 전 시점부터 1시간 구간
SELECT * FROM sensor_log DURATION 1 HOUR BEFORE 1 DAY;

-- 1주일 전 시점부터 1일 구간
SELECT * FROM sensor_log DURATION 1 DAY BEFORE 1 WEEK;
```

### 명시적 범위

```sql
-- 특정 날짜 범위를 명시적으로 지정
SELECT * FROM sensor_log
DURATION FROM TO_DATE('2024-01-01', 'YYYY-MM-DD')
         TO   TO_DATE('2024-01-31', 'YYYY-MM-DD');
```

## DURATION vs WHERE 시간 조건 비교

| 항목 | DURATION | WHERE 시간 조건 |
|------|---------|--------------|
| 조건 대상 | `_ARRIVAL_TIME` 또는 BASETIME | 사용자 지정 컬럼 |
| 상대 시간 | O (1 HOUR, 7 DAY 등) | 별도 계산 필요 |
| 성능 최적화 | 내부적으로 파티션 스캔 최적화 | 인덱스 활용 필요 |
| 명시적 범위 | DURATION FROM ... TO ... | BETWEEN / >=, <= |

**성능 팁**: 대용량 테이블에서는 `DURATION`을 사용하거나 인덱스가 있는 컬럼으로 WHERE 시간 조건을 지정하면 전체 스캔을 방지합니다.
