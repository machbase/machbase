---
title: '6.9 ROLLUP 제어와 상태 확인'
weight: 90
toc: true
aliases:
  - /dbms/tag-rollup-usage/state-check-rollup/
  - /dbms/tag-rollup-usage/operational-notes-rollup/
---

<a id="ingestion-start-stop-immediate-collect-rollup"></a>

## 시작·중지와 즉시 수집

ROLLUP 스레드는 생성 시 자동으로 시작됩니다. 필요에 따라 수동으로 제어할 수 있습니다.
`EXEC` 형식의 인자 수·범위·오류 계약은
[EXEC procedure 정본](/dbms/reference/sql/syntax-dictionary-sql/execute-procedure-syntax/#rollup-start-stop)을
참고합니다.

### 시작 / 중지

```sql
-- SQL 방식
ALTER ROLLUP rollup_name START;
ALTER ROLLUP rollup_name STOP;

-- 프로시저 방식 (동일한 기능)
EXEC ROLLUP_START('rollup_name');
EXEC ROLLUP_STOP('rollup_name');
```

STOP 후 재시작하면 중단된 시점부터 이어서 집계합니다.

### 즉시 수집 (WAKEUP / FORCE)

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

### WAKEUP INTERVAL 조정

기본 wakeup 주기는 ROLLUP 주기와 동일합니다. 더 자주 집계하려면 wakeup 주기를 ROLLUP 주기의 약수로 설정합니다.

```sql
-- 1분 ROLLUP을 10초마다 깨우기
ALTER ROLLUP _tag_ru_1m SET WAKEUP INTERVAL 10 SEC;
```

규칙:
- wakeup 주기는 0보다 커야 합니다.
- wakeup 주기는 ROLLUP 주기보다 클 수 없습니다.
- ROLLUP 주기가 wakeup 주기의 정수배여야 합니다.

### 데이터 로드 후 즉시 집계 패턴

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

<a id="state-status-rollup-wakeup-interval-vrollup"></a>

## V$ROLLUP 상태 확인

`V$ROLLUP`에서 등록된 ROLLUP의 현재 상태를 조회합니다.

| 컬럼 | 설명 |
|------|------|
| ROLLUP_TABLE | ROLLUP table 이름 |
| SOURCE_TABLE | 집계 source table |
| INTERVAL_TIME | ROLLUP 주기(ms) |
| WAKEUP_INTERVAL | wakeup 주기(ms) |
| LAST_WAKEUP_TIME | 마지막 wakeup 시각 |
| NEXT_WAKEUP_TIME | 다음 wakeup 예정 시각 |
| ENABLED | 활성화 여부(1=활성, 0=중지) |
| END_RID | 마지막으로 처리한 source RID |
| LAST_ELAPSED_MSEC | 직전 집계 소요 시간(ms) |
| RUN_STATE | `I`=INIT, `S`=SLEEPING, `R`=RUNNING |
| PREDICATE | 조건 ROLLUP의 filter, 없으면 NULL |

```sql
SELECT ROLLUP_TABLE, SOURCE_TABLE, INTERVAL_TIME, WAKEUP_INTERVAL,
       ENABLED, RUN_STATE, LAST_ELAPSED_MSEC, PREDICATE
  FROM V$ROLLUP
 ORDER BY ROLLUP_TABLE;
```

`ENABLED=0`이면 STOP 상태로 wakeup하지 않습니다. 오래 걸리는 대상을 찾을 때는
`LAST_ELAPSED_MSEC`를 내림차순으로 조회합니다.

## SHOW ROLLUPGAP

machsql에서는 다음 client 명령으로 아직 처리하지 못한 RID gap을 확인합니다.

```sql
SHOW ROLLUPGAP;
```

이 명령은 서버 SQL이 아닙니다. 계층의 모든 source→ROLLUP 행이 0인지 확인해야 전체 계층이
따라잡았다고 판단할 수 있습니다. 출력과 `GAP` 계산 계약은
[EXEC procedure와 ROLLUPGAP 정본](/dbms/reference/sql/syntax-dictionary-sql/execute-procedure-syntax/#show-rollupgap)을
참고합니다.
