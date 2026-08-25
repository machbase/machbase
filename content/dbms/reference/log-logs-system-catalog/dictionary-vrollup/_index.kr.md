---
type: docs
title: '17.3.3 V$ROLLUP 사전'
weight: 30
toc: true
---

`V$ROLLUP`은 Tag 데이터의 Rollup 작업 상태를 실시간으로 표시하는 가상 테이블입니다. Rollup이 정상 작동하는지 확인하거나 실행 주기와 소요 시간을 모니터링할 때 사용합니다.

## 컬럼 상세

| 컬럼 이름 | 타입 | 설명 |
|----------|------|------|
| `ID` | INTEGER | Rollup 작업 ID |
| `ROLLUP_TABLE` | VARCHAR | Rollup 결과가 저장되는 테이블 이름 |
| `SOURCE_TABLE` | VARCHAR | 집계 대상 원본 TAG 테이블 이름 |
| `COLUMN_NAME` | VARCHAR | 집계 대상 컬럼 이름 |
| `INTERVAL_TIME` | INTEGER | 실행 주기 (밀리초) |
| `LAST_WAKEUP_TIME` | DATETIME | 최근 실행 시각 |
| `ENABLED` | INTEGER | 활성화 여부 (1: 활성, 0: 비활성) |
| `LAST_ELAPSED_MSEC` | INTEGER | 직전 실행에 걸린 시간 (밀리초) |
| `RUN_STATE` | VARCHAR | 스레드 상태 (I: 초기화, S: 대기, R: 실행중) |

## RUN_STATE 값

| 값 | 설명 |
|----|------|
| `I` | 초기화(Initializing) 중 |
| `S` | 다음 실행을 대기(Sleeping) 중 |
| `R` | 현재 실행(Running) 중 |

## SQL 예제

```sql
-- Rollup 작업 전체 상태 확인
SELECT rollup_table, source_table, column_name,
       interval_time, enabled, last_elapsed_msec, run_state
  FROM v$rollup
 ORDER BY rollup_table;

-- 마지막 실행 시각 확인
SELECT rollup_table, last_wakeup_time, last_elapsed_msec, run_state
  FROM v$rollup;

-- 비활성화된 Rollup 확인
SELECT rollup_table, source_table, enabled
  FROM v$rollup
 WHERE enabled = 0;

-- 실행 시간이 오래 걸리는 Rollup 확인
SELECT rollup_table, interval_time, last_elapsed_msec,
       last_elapsed_msec * 100.0 / interval_time AS usage_ratio
  FROM v$rollup
 WHERE last_elapsed_msec > 0
 ORDER BY last_elapsed_msec DESC;
```

## 주의 사항

- `INTERVAL_TIME`보다 `LAST_ELAPSED_MSEC`가 크게 나타나면 Rollup이 이전 실행을 마치기 전에 다음 주기가 시작되는 상황일 수 있습니다. 집계 대상 데이터 양 또는 집계 주기를 조정합니다.
- `ENABLED = 0`이면 Rollup이 비활성화된 상태입니다. `ALTER ROLLUP ... ENABLE` 명령으로 다시 활성화합니다.
- Rollup 생성과 관리는 [TAG 테이블과 Rollup](/dbms/tag-rollup-usage/overview-use-criteria/#rollup) 섹션을 참고하십시오.
