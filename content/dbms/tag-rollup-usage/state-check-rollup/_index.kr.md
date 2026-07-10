---
title: '6.13 ROLLUP 상태 확인'
weight: 120
toc: true
---

<a id="state-status-rollup-wakeup-interval-vrollup"></a>

## 상태 확인 (V$ROLLUP)

`V$ROLLUP` 가상 테이블에서 등록된 모든 ROLLUP의 현재 상태를 조회합니다.

### V$ROLLUP 주요 컬럼

| 컬럼 | 설명 |
|------|------|
| ROLLUP_TABLE | ROLLUP 테이블 이름 |
| SOURCE_TABLE | 집계 소스 테이블 (TAG 또는 상위 ROLLUP) |
| COLUMN_NAME | 집계 대상 컬럼 |
| INTERVAL_TIME | ROLLUP 주기 (밀리초) |
| WAKEUP_INTERVAL | Wakeup 주기 (밀리초) |
| LAST_WAKEUP_TIME | 마지막 wakeup 시각 |
| NEXT_WAKEUP_TIME | 다음 wakeup 예정 시각 |
| ENABLED | 활성화 여부 (1=활성, 0=중지) |
| END_RID | 마지막으로 처리한 소스 테이블의 RID |
| LAST_ELAPSED_MSEC | 직전 집계 소요 시간 (밀리초) |
| RUN_STATE | 스레드 상태: I=INIT, S=SLEEPING, R=RUNNING |
| PREDICATE | 조건 롤업의 필터 조건 (없으면 NULL) |

### 조회 예시

```sql
-- 전체 ROLLUP 상태 조회
SELECT ROLLUP_TABLE, SOURCE_TABLE, INTERVAL_TIME, WAKEUP_INTERVAL,
       ENABLED, RUN_STATE, LAST_ELAPSED_MSEC, PREDICATE
FROM   V$ROLLUP
ORDER BY ROLLUP_TABLE;
```

```sql
-- 실행 중인 ROLLUP 확인
SELECT ROLLUP_TABLE, RUN_STATE, LAST_WAKEUP_TIME, NEXT_WAKEUP_TIME
FROM   V$ROLLUP
WHERE  RUN_STATE = 'R';  -- RUNNING
```

```sql
-- 집계가 오래 걸리는 ROLLUP 확인
SELECT ROLLUP_TABLE, LAST_ELAPSED_MSEC
FROM   V$ROLLUP
ORDER BY LAST_ELAPSED_MSEC DESC;
```

### SHOW ROLLUPGAP

`show rollupgap` 명령으로도 상태를 확인할 수 있습니다.

```sql
Mach> show rollupgap;
```

RID 기준으로 아직 처리하지 못한 데이터의 양(gap)을 보여줍니다. Gap이 크면 ROLLUP이 입력 속도를 따라가지 못하고 있는 것입니다.

### 상태별 의미

| RUN_STATE | 의미 |
|-----------|------|
| I (INIT) | 초기화 중 |
| S (SLEEPING) | 다음 wakeup 대기 중 |
| R (RUNNING) | 현재 집계 실행 중 |

ENABLED=0이면 STOP 상태로 wakeup하지 않습니다.
