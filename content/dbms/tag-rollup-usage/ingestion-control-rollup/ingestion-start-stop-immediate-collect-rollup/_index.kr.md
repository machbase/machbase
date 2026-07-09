---
type: docs
title: '시작·중지와 즉시 수집'
weight: 40
---

ROLLUP 스레드는 생성 시 자동으로 시작되며, 필요에 따라 수동으로 제어할 수 있습니다.

## 시작 / 중지

```sql
-- SQL 방식
ALTER ROLLUP rollup_name START;
ALTER ROLLUP rollup_name STOP;

-- 프로시저 방식 (동일한 기능)
EXEC ROLLUP_START('rollup_name');
EXEC ROLLUP_STOP('rollup_name');
```

STOP 후 재시작하면 중단된 시점부터 이어서 집계합니다.

## 즉시 수집 (WAKEUP / FORCE)

데이터를 대량 로드한 직후 즉시 집계가 필요할 때 사용합니다.

```sql
-- WAKEUP: 스레드를 깨우고 즉시 반환 (비블로킹)
ALTER ROLLUP rollup_name WAKEUP;

-- FORCE: 집계 완료까지 대기 (블로킹)
ALTER ROLLUP rollup_name FORCE;

-- 프로시저 방식 (FORCE와 동일)
EXEC ROLLUP_FORCE('rollup_name');
```

| 명령 | 블로킹 | 사용 시점 |
|------|--------|-----------|
| WAKEUP | 비블로킹 | 집계를 트리거만 하고 바로 다음 작업 진행 |
| FORCE | 블로킹 | 집계 완료 후 조회해야 하는 경우 |

## WAKEUP INTERVAL 조정

기본 wakeup 주기는 ROLLUP 주기와 동일합니다. 더 자주 집계하려면 wakeup 주기를 ROLLUP 주기의 약수로 설정합니다.

```sql
-- 1분 ROLLUP을 10초마다 깨우기
ALTER ROLLUP _tag_ru_1m SET WAKEUP INTERVAL 10 SEC;
```

규칙:
- wakeup 주기는 0보다 커야 합니다.
- wakeup 주기는 ROLLUP 주기보다 클 수 없습니다.
- ROLLUP 주기가 wakeup 주기의 정수배여야 합니다.

## 데이터 로드 후 즉시 집계 패턴

```sql
-- 1. 대량 데이터 로드
INSERT INTO tag VALUES (...);
-- 또는 machloader / Append API 사용

-- 2. 하위 롤업부터 순서대로 강제 집계
ALTER ROLLUP _tag_ru_1s FORCE;
ALTER ROLLUP _tag_ru_1m FORCE;
ALTER ROLLUP _tag_ru_1h FORCE;

-- 3. 이후 롤업 조회 가능
SELECT rollup('hour', 1, time) AS rt, AVG(value)
FROM   tag
WHERE  name = 'SENSOR-01'
GROUP BY rt;
```
