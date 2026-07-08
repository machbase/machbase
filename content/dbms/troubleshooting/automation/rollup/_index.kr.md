---
type: docs
title: 'ROLLUP 결과가 예상과 다를 때'
weight: 10
---

TAG 테이블에 설정된 ROLLUP의 집계값이 예상과 다르거나 최신 데이터가 반영되지 않을 때 원인을 진단하고 해결하는 방법을 설명합니다.

## ROLLUP 상태 확인

ROLLUP이 정상적으로 동작하는지 먼저 상태를 확인합니다.

```sql
SELECT name, table_name, status, last_run_time FROM v$rollup;
```

| 컬럼 | 설명 |
|------|------|
| `name` | ROLLUP 이름 |
| `table_name` | 대상 TAG 테이블 이름 |
| `status` | 현재 상태 (`RUNNING`, `STOPPED`, `ERROR` 등) |
| `last_run_time` | 마지막 실행 시각 |

## 원인별 진단

### 1. ROLLUP이 실행되지 않음

`status`가 `STOPPED` 또는 `ERROR`인 경우 ROLLUP이 중지된 상태입니다.

**확인 방법**

```sql
SELECT name, status, last_run_time FROM v$rollup WHERE status != 'RUNNING';
```

**해결 방법**

ROLLUP을 즉시 실행하거나 재시작합니다.

```sql
-- 모든 ROLLUP 즉시 실행
ALTER SYSTEM FLUSH ROLLUP;
```

서버 트레이스 로그에서 ROLLUP 관련 오류 메시지를 확인합니다.

```bash
grep -i "rollup\|error" $MACHBASE_HOME/trc/machbase.trc | tail -30
```

### 2. 집계값이 원본 데이터와 다름

ROLLUP 집계 범위와 원본 데이터의 시간 범위를 비교합니다.

```sql
-- 원본 데이터 집계 (1분 단위)
SELECT DATE_TRUNC('minute', time) AS ts,
       AVG(value) AS avg_val,
       MIN(value) AS min_val,
       MAX(value) AS max_val
FROM sensor_tag
WHERE name = 'sensor-01'
  AND time >= TO_DATE('2024-01-01 12:00:00')
  AND time <  TO_DATE('2024-01-01 12:10:00')
GROUP BY ts
ORDER BY ts;

-- ROLLUP 집계값 조회
SELECT * FROM sensor_tag ROLLUP(1 MINUTE)
WHERE name = 'sensor-01'
  AND time >= TO_DATE('2024-01-01 12:00:00')
  AND time <  TO_DATE('2024-01-01 12:10:00');
```

두 결과가 다르다면 ROLLUP이 아직 갱신되지 않은 것입니다. `FLUSH ROLLUP` 후 다시 비교합니다.

### 3. 최신 데이터가 ROLLUP에 반영되지 않음

ROLLUP은 설정된 주기(기본값: 분 단위)마다 실행되므로 방금 입력된 데이터가 즉시 ROLLUP에 반영되지 않습니다. 이는 정상적인 동작입니다.

즉시 반영이 필요한 경우 수동으로 ROLLUP을 실행합니다.

```sql
ALTER SYSTEM FLUSH ROLLUP;
```

## ROLLUP 재계산 (Standard Edition 전용)

이미 저장된 ROLLUP 값이 잘못되었다면 특정 시간 범위의 ROLLUP을 재계산할 수 있습니다. 이 기능은 **Standard Edition 전용**입니다.

```sql
EXEC ROLLUP_REBUILD(sensor_tag, rollup_1min,
    TO_DATE('2024-01-01'), TO_DATE('2024-01-02'));
```

| 인수 | 설명 |
|------|------|
| `sensor_tag` | 대상 TAG 테이블 이름 |
| `rollup_1min` | 재계산할 ROLLUP 이름 |
| 세 번째 인수 | 재계산 시작 시각 |
| 네 번째 인수 | 재계산 종료 시각 |

{{< callout type="warning" >}}
**Cluster Edition 주의**

`ROLLUP_REBUILD` 명령은 Cluster Edition에서 지원되지 않습니다. Cluster Edition에서는 ROLLUP 재계산이 필요한 경우 기술 지원에 문의하십시오.
{{< /callout >}}

## ROLLUP 주기 확인

ROLLUP이 얼마나 자주 실행되는지 확인합니다.

```sql
SELECT name, interval FROM v$rollup;
```

주기가 너무 길어서 최신 데이터 반영이 늦다면, ROLLUP 설정을 재검토하거나 `FLUSH ROLLUP`을 필요 시 수동으로 실행합니다.
