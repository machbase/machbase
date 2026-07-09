---
type: docs
title: '6.15.3 이상 데이터 정정 후 ROLLUP Rebuild'
weight: 100
---

## 시나리오 개요

잘못 입력된 센서 데이터를 삭제 또는 정정하고, 영향받은 ROLLUP 집계를 재구성하는 운영 절차입니다.

센서 오작동, 수집기 버그, 단위 변환 오류 등으로 비정상적인 값이 TAG 테이블에 삽입되면 ROLLUP 집계(최솟값, 최댓값, 평균 등)가 오염됩니다. 이 시나리오는 이상 데이터를 탐지하고 TAG data UPDATE로 정정한 뒤 `ROLLUP_REBUILD`로 집계를 재계산하는 전체 절차를 다룹니다.

> **주의**: Cluster Edition에서는 `ROLLUP_REBUILD`가 지원되지 않습니다. 이 시나리오는 Standard Edition을 대상으로 합니다.

> **권장**: 대량 정정 전 반드시 해당 기간의 백업을 수행하십시오. `name` 또는 `time` 자체를 바꿔야 해서 삭제/재입력이 필요한 경우 삭제된 TAG 데이터는 복구할 수 없습니다.

## 1단계: 이상 데이터 탐지

### 범위 이탈 값 확인

정상 범위를 벗어난 값을 쿼리합니다. 예를 들어 온도 센서의 정상 범위가 -40°C ~ 200°C라면:

```sql
-- 범위 이탈 데이터 확인
SELECT name, time, value
  FROM sensor_tag
 WHERE name = 'sensor-01'
   AND (value < -40 OR value > 200)
 ORDER BY time;
```

### 특정 기간 데이터 분포 확인

의심되는 기간의 통계를 확인합니다.

```sql
-- 기간별 최솟값/최댓값/평균 확인
SELECT
    name,
    MIN(value)  AS min_val,
    MAX(value)  AS max_val,
    AVG(value)  AS avg_val,
    COUNT(*)    AS cnt
  FROM sensor_tag
 WHERE name = 'sensor-01'
   AND time BETWEEN TO_DATE('2024-01-01') AND TO_DATE('2024-01-02')
 GROUP BY name;
```

### 이상 데이터 샘플 조회

정정 전 이상 데이터의 실제 내용을 확인합니다.

```sql
-- 이상 데이터 미리보기 (정정 전 확인용)
SELECT name, time, value
  FROM sensor_tag
 WHERE name = 'sensor-01'
   AND time BETWEEN TO_DATE('2024-01-01') AND TO_DATE('2024-01-02')
   AND value > 200
 ORDER BY time
 LIMIT 20;
```

## 2단계: 데이터 백업 (권장)

대량 UPDATE 전 해당 기간 데이터를 백업합니다.

```sql
-- 이상 데이터가 포함된 기간을 기간 백업
BACKUP DATABASE
    FROM TO_DATE('2024-01-01', 'YYYY-MM-DD')
    TO   TO_DATE('2024-01-02', 'YYYY-MM-DD')
    INTO DISK = '/backup/before_correction_20240101';
```

백업이 완료된 후 다음 단계를 진행합니다.

## 3단계: 이상 데이터 정정

TAG 테이블에서 이상 데이터를 직접 정정합니다. UPDATE 조건을 정확히 지정하여 정상 데이터가 수정되지 않도록 주의합니다.

```sql
-- 특정 센서의 특정 기간 값을 정정
UPDATE sensor_tag
   SET value = 25.3
 WHERE name = 'sensor-01'
   AND time BETWEEN TO_DATE('2024-01-01') AND TO_DATE('2024-01-02');
```

범위 이탈 값만 선택적으로 정정하려면:

```sql
-- 이상 값만 선택 정정 (값 조건 포함)
UPDATE sensor_tag
   SET value = 25.3
 WHERE name = 'sensor-01'
   AND time BETWEEN TO_DATE('2024-01-01') AND TO_DATE('2024-01-02')
   AND value > 200;
```

정정 후 결과를 확인합니다.

```sql
-- 정정 결과 확인
SELECT COUNT(*) AS corrected
  FROM sensor_tag
 WHERE name = 'sensor-01'
   AND time BETWEEN TO_DATE('2024-01-01') AND TO_DATE('2024-01-02')
   AND value = 25.3;
```

## 4단계: 삭제/재입력이 필요한 경우

`name` 또는 `time` 값을 바꿔야 하는 경우에는 TAG data UPDATE로 처리할 수 없습니다. 새
`name`/`time` 값으로 정정 데이터를 입력하고, 운영 정책에 따라 기존 데이터를 삭제합니다.

### machsql로 직접 삽입

```sql
-- 정정된 name/time 값으로 직접 삽입
INSERT INTO sensor_tag VALUES ('sensor-01', TO_DATE('2024-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'), 25.3);
INSERT INTO sensor_tag VALUES ('sensor-01', TO_DATE('2024-01-01 00:01:00', 'YYYY-MM-DD HH24:MI:SS'), 25.5);
```

### CSV 파일로 대량 재입력

정정된 데이터를 CSV 파일로 준비한 뒤 machloader로 적재할 수도 있습니다.

```bash
# CSV 파일 형식: name,time,value
# sensor-01,2024-01-01 00:00:00 000:000:000,25.3
# sensor-01,2024-01-01 00:01:00 000:000:000,25.5

machloader -i -t sensor_tag -d corrected_data.csv \
    -F "time YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn"
```

## 5단계: ROLLUP Rebuild 실행

데이터 정정 후 영향받은 기간의 ROLLUP 집계를 재계산합니다.

```sql
-- ROLLUP 재계산
-- ROLLUP_REBUILD(테이블명, 태그명, 시작시간, 종료시간)
EXEC ROLLUP_REBUILD(sensor_tag, 'sensor-01',
    TO_DATE('2024-01-01', 'YYYY-MM-DD'),
    TO_DATE('2024-01-02', 'YYYY-MM-DD'));
```

ROLLUP이 여러 단계(1분, 1시간 등)로 설정되어 있어도 두 번째 인자는 ROLLUP 이름이 아니라
재계산할 tag 이름입니다.

```sql
EXEC ROLLUP_REBUILD(sensor_tag, 'sensor-02',
    TO_DATE('2024-01-01', 'YYYY-MM-DD'),
    TO_DATE('2024-01-02', 'YYYY-MM-DD'));
```

> **ROLLUP 상태 확인**: 테이블에 설정된 ROLLUP은 다음 쿼리로 확인합니다.

```sql
SELECT rollup_name, source_table, rollup_table, enabled, run_state
  FROM v$rollup
 WHERE source_table = 'SENSOR_TAG'
    OR root_table = 'SENSOR_TAG';
```

## 6단계: Rebuild 진행 상황 확인

`ROLLUP_REBUILD`는 비동기로 동작할 수 있습니다. 진행 상황은 다음과 같이 확인합니다.

```sql
-- ROLLUP 상태 확인
SELECT
    rollup_name,
    source_table,
    enabled,
    run_state,
    last_wakeup_time,
    last_elapsed_msec
  FROM v$rollup
 WHERE source_table = 'SENSOR_TAG'
    OR root_table = 'SENSOR_TAG';
```

| 상태 값 | 의미 |
|---------|------|
| `ENABLED` | ROLLUP 활성화 여부 |
| `RUN_STATE` | 현재 실행 상태 |
| `LAST_ELAPSED_MSEC` | 마지막 실행 소요 시간 |

## 7단계: 정정 전후 비교 검증

Rebuild 완료 후 ROLLUP 집계 값이 올바르게 갱신되었는지 확인합니다.

```sql
-- 정정 기간의 원시 데이터 집계 (실제 값)
SELECT
    name,
    MIN(value) AS raw_min,
    MAX(value) AS raw_max,
    AVG(value) AS raw_avg,
    COUNT(*)   AS raw_cnt
  FROM sensor_tag
 WHERE name = 'sensor-01'
   AND time BETWEEN TO_DATE('2024-01-01') AND TO_DATE('2024-01-02')
 GROUP BY name;
```

```sql
-- ROLLUP 힌트로 집계 값 확인 (1분 평균)
SELECT /*+ ROLLUP(sensor_tag, min, AVG) */ time, value
  FROM sensor_tag
 WHERE name = 'sensor-01'
   AND time BETWEEN TO_DATE('2024-01-01') AND TO_DATE('2024-01-02')
 ORDER BY time;
```

원시 데이터 집계와 ROLLUP 집계가 일치하면 정정이 완료된 것입니다.

## 정기 데이터 품질 점검 패턴

운영 환경에서 이상 데이터를 조기에 탐지하기 위한 정기 점검 쿼리입니다.

```sql
-- 최근 1시간 내 이상값 탐지 (daily 배치 또는 모니터링 쿼리로 활용)
SELECT
    name,
    COUNT(*) AS anomaly_count,
    MIN(time) AS first_anomaly,
    MAX(time) AS last_anomaly
  FROM sensor_tag
 WHERE time > NOW - INTERVAL '1' HOUR
   AND (value < -40 OR value > 200)
 GROUP BY name
HAVING COUNT(*) > 0
 ORDER BY anomaly_count DESC;
```

```sql
-- NULL 값 또는 0 값 집중 발생 구간 탐지
SELECT
    name,
    DATE_TRUNC('hour', time) AS hour_bucket,
    COUNT(*) AS zero_count
  FROM sensor_tag
 WHERE value = 0
   AND time > NOW - INTERVAL '24' HOUR
 GROUP BY name, hour_bucket
HAVING COUNT(*) > 60   -- 1시간에 60건 이상이면 의심
 ORDER BY zero_count DESC;
```

## 요약

| 단계 | 작업 |
|------|------|
| 1 | 범위 이탈·이상값 탐지 쿼리 실행 |
| 2 | 이상 데이터 포함 기간 백업 |
| 3 | `UPDATE sensor_tag SET ... WHERE name ... AND time ...` 이상 데이터 정정 |
| 4 | name/time 변경이 필요한 경우에만 정정 데이터 재입력 후 기존 데이터 삭제 |
| 5 | `EXEC ROLLUP_REBUILD(...)` ROLLUP 재계산 |
| 6 | `v$rollup`으로 Rebuild 완료 확인 |
| 7 | 원시 데이터 집계와 ROLLUP 집계 비교 검증 |

## 관련 문서

- [백업, 복원, 마운트](../../operations-configuration-recovery/backup-restore-mount/)
- [센서 데이터 저장과 ROLLUP 분석](../storage-sensor-data-rollup/)
- [STREAM으로 LOG를 TAG로 자동 적재](../stream-log-tag/)
