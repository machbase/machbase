---
title: '6.15 ROLLUP_REBUILD'
weight: 140
toc: true
---

<a id="validation-policy-tag-data-update-stat-index-rollup"></a>

## TAG data UPDATE와 통계/롤업 영향

TAG data UPDATE는 원본 TAG row를 수정합니다. 통계와 인덱스는 변경값에 맞게 처리되지만,
이미 구체화된 롤업 데이터는 자동으로 보정되지 않습니다. UPDATE한 구간을 롤업 조회에
사용하려면 `ROLLUP_REBUILD`로 재구성합니다.

### UPDATE 후 영향을 받는 구조

#### 원본 TAG row

`UPDATE tag SET value = ... WHERE name ... AND time ...` 문은 조건에 맞는 원본 TAG row의
데이터 컬럼을 변경합니다.

#### 통계 정보와 인덱스

`SUMMARIZED` 컬럼과 데이터 파티션 인덱스는 UPDATE 대상 row에 맞게 갱신됩니다.
대량 UPDATE는 내부 정리 비용이 커질 수 있으므로 대상 범위를 태그와 시간 조건으로 좁게 지정합니다.

#### 롤업

`WITH ROLLUP` 또는 롤업 테이블을 사용하는 환경에서는 이미 계산된 롤업 row가 원본 UPDATE를
자동으로 반영하지 않습니다. 정정 구간의 롤업 조회가 필요하면 `ROLLUP_REBUILD`로
해당 롤업을 재구성합니다.

```sql
EXEC ROLLUP_REBUILD(sensor_tag, 'TEMP-01',
    TO_DATE('2026-07-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'),
    TO_DATE('2026-07-02 00:00:00', 'YYYY-MM-DD HH24:MI:SS'));
```

### 검증 절차

1. UPDATE 전 같은 WHERE 조건으로 대상 row 수와 값 범위를 확인합니다.
2. UPDATE를 실행합니다.
3. 원본 TAG 테이블에서 변경 값을 확인합니다.
4. 롤업 조회가 필요한 경우 `ROLLUP_REBUILD`를 실행한 뒤 집계 값을 확인합니다.

```sql
SELECT COUNT(*), MIN(value), MAX(value)
  FROM sensor_tag
 WHERE name = 'TEMP-01'
   AND time >= TO_DATE('2026-07-01', 'YYYY-MM-DD')
   AND time <  TO_DATE('2026-07-02', 'YYYY-MM-DD');
```

<a id="original-85-rollup-rebuild"></a>

## Rollup Rebuild 사용자 가이드


### 개요

이상 데이터가 수집되면 원본 데이터는 삭제 후 정상 데이터로 다시 넣을 수 있지만, 이미 생성된 rollup 통계는 자동으로 되감기지 않습니다. 영향 버킷의 rollup 데이터를 다시 만들어야 합니다.

서버 내장 Procedure `EXEC ROLLUP_REBUILD(...)`로 rollup을 재구성합니다.

- built-in rollup + rollup extension + custom rollup 대상
- SQL에서 직접 호출 가능
- custom rollup dependency tree를 따라 stop/rebuild/start 수행

### 제약사항

`EXEC ROLLUP_REBUILD(...)`에는 아래 제약이 있습니다.

1. standard edition에서 지원하며, **cluster edition에서는 지원하지 않습니다.**
2. `table_name`, `tag_name`, `begin_time`, `end_time` 기준의 단일 tag rebuild만 지원합니다.
3. rebuild 대상 구간은 부분 시간이 아니라 영향 버킷 전체를 기준으로 delete 후 insert 해야 합니다.

### Rollup Rebuild 프로시저 사용법

#### 호출 문법

```sql
EXEC ROLLUP_REBUILD(table_name, tag_name, begin_time, end_time);
```

예:

```sql
EXEC ROLLUP_REBUILD(tag,
                    'tag-00045',
                    TO_DATE('2025-09-02 01:00:00'),
                    TO_DATE('2025-09-02 01:00:00'));

EXEC ROLLUP_REBUILD(sys.tag,
                    'tag-00045',
                    TO_DATE('2025-09-02 01:00:00'),
                    TO_DATE('2025-09-02 01:00:00'));
```

#### 매개변수 의미

1. `table_name`
   - 대상 source TAG 테이블 이름
   - 필요 시 `schema.table` 형태 사용
2. `tag_name`
   - 재구성 대상 tag key 값
3. `begin_time`
   - 이상 데이터 보정 시작 시각
4. `end_time`
   - 이상 데이터 보정 종료 시각

#### 적용 범위

- built-in rollup
- rollup extension
- custom rollup
- rollup-on-rollup dependency 환경

### Custom Rollup Rebuild 원리

#### built-in처럼 고정 SQL로 처리할 수 없는 이유

custom rollup은 다음이 모두 사용자 정의입니다.

- destination table 이름
- destination 컬럼 수와 타입
- 집계 함수
- source가 root table인지, 다른 rollup destination인지

따라서 범용 rebuild는 "고정 스키마 재삽입"이 아니라 "원래 custom SELECT를 다시 실행하되, tag/time 버킷만 좁혀서 다시 넣는 방식"이어야 합니다.

#### 버킷 경계 확장

예를 들어 1분 custom rollup에서 원본 이상 구간이 아래와 같다고 가정합니다.

- 원본 오류 시간: `2026-01-27 09:30:12` ~ `2026-01-27 09:31:07`

실제 rebuild 대상은 아래처럼 버킷 전체입니다.

- 시작 버킷: `2026-01-27 09:30:00`
- 종료 버킷: `2026-01-27 09:31:59.999999999`

부분 집계 row가 destination table에 이미 있을 수 있으므로, 삭제 없이 insert만 하면 중복 집계가 발생합니다. 대상 버킷을 먼저 삭제한 뒤 insert 해야 합니다.

#### 수동 rebuild 절차

프로시저를 사용하지 않고 수동으로 하려면 다음 절차를 따릅니다.

1. 영향 받는 모든 custom rollup stop
2. source 이상 데이터 수정 또는 재적재
3. 버킷 경계 계산
4. destination delete
5. 원래 `CREATE ROLLUP ... AS (SELECT ...)`와 같은 집계식으로 재insert
6. destination flush
7. 상위 custom rollup이 있으면 하위부터 차례대로 반복
8. rollup start

### Custom Rollup 수동 Rebuild 예제

#### 1분 custom rollup

아래는 `stock_tick -> stock_rollup_1m`에 대해 `09:30` ~ `09:31` 버킷을 다시 만드는 예제입니다.

```sql
STOP ROLLUP rollup_stock_1m;

DELETE FROM stock_rollup_1m
WHERE time BETWEEN TO_DATE('2026-01-27 09:30:00')
               AND TO_DATE('2026-01-27 09:31:59');

INSERT INTO stock_rollup_1m
SELECT code,
       DATE_TRUNC('minute', time) AS time,
       SUM(price)                 AS sum_price,
       SUM(volume)                AS sum_volume,
       COUNT(*)                   AS cnt
FROM stock_tick
WHERE time BETWEEN TO_DATE('2026-01-27 09:30:00')
               AND TO_DATE('2026-01-27 09:31:59')
GROUP BY code, time;

EXEC TABLE_FLUSH('stock_rollup_1m');
START ROLLUP rollup_stock_1m;
```

#### FIRST/LAST 가 있는 custom rollup

`FIRST/LAST`를 쓰는 custom rollup은 보조 시간 컬럼도 같이 다시 계산해야 합니다.

```sql
STOP ROLLUP rollup_stock_candle_1m;

DELETE FROM stock_candle_1m
WHERE time = TO_DATE('2026-01-27 09:30:00');

INSERT INTO stock_candle_1m
SELECT code,
       DATE_TRUNC('minute', time) AS time,
       MIN(time)                  AS firsttime,
       MAX(time)                  AS lasttime,
       FIRST(time, price)         AS open,
       MAX(price)                 AS high,
       MIN(price)                 AS low,
       LAST(time, price)          AS close,
       SUM(volume)                AS volume,
       COUNT(*)                   AS cnt
FROM stock_tick
WHERE time BETWEEN TO_DATE('2026-01-27 09:30:00')
               AND TO_DATE('2026-01-27 09:30:59')
GROUP BY code, time;

EXEC TABLE_FLUSH('stock_candle_1m');
START ROLLUP rollup_stock_candle_1m;
```

최종 조회는 기존과 동일하게 `FIRST(firsttime, open)`, `LAST(lasttime, close)`로 재병합해야 합니다.

#### rollup-on-rollup 순서

예:

- 1차: `stock_tick -> stock_rollup_1m`
- 2차: `stock_rollup_1m -> stock_rollup_1h`

rebuild 순서는 반드시 하위부터입니다.

1. `stock_rollup_1h` stop
2. `stock_rollup_1m` stop
3. `stock_rollup_1m` rebuild
4. `stock_rollup_1h` delete / rebuild
5. `stock_rollup_1m` start
6. `stock_rollup_1h` start

상위를 먼저 재구성하면 아직 복원되지 않은 하위 결과를 읽게 되어 다시 잘못된 집계가 들어갑니다.

### 운영 권장사항

1. custom rollup rebuild 전에는 먼저 영향 버킷 범위를 확인합니다.
2. 운영 적용 전후에 `v$rollup`으로 dependency를 확인합니다.
3. custom rollup destination table은 append-only 결과가 누적되므로 rebuild 시 반드시 delete 후 insert 합니다.
4. rollup-on-rollup 구조에서는 반드시 하위부터 rebuild 하고, 이후 상위를 재구성합니다.
5. 오류 구간이 여러 버킷에 걸치면 전체 범위를 지정해서 `EXEC ROLLUP_REBUILD(...)`를 호출합니다.

### 최신 데이터를 포함한 효율적인 Rollup 질의 정리

앞서 설명한 최신 데이터 조회 원칙은 built-in rollup과 custom rollup 모두 동일합니다.

핵심 규칙:

1. 안정 구간은 rollup table 사용
2. 최근 구간은 source table 직접 집계
3. 두 결과를 `UNION ALL`
4. 필요하면 바깥에서 한 번 더 최종 집계

#### 일반 1분 rollup 예

```sql
SELECT ROLLUP('minute', 1, time) AS mtime, AVG(value)
FROM tag
WHERE name = 'TAG_0001'
  AND time < DATE_TRUNC('minute', SYSDATE) - 2m
GROUP BY mtime

UNION ALL

SELECT DATE_TRUNC('minute', time) AS mtime, AVG(value)
FROM tag
WHERE name = 'TAG_0001'
  AND time >= DATE_TRUNC('minute', SYSDATE) - 2m
GROUP BY mtime;
```

#### 일반 20분 집계 예

```sql
SELECT ROLLUP('minute', 20, time) AS mtime, AVG(value)
FROM tag
WHERE name = 'TAG_0001'
  AND time < DATE_BIN('minute', 20, SYSDATE, 0) - 20m
GROUP BY mtime

UNION ALL

SELECT DATE_BIN('minute', 20, time, 0) AS mtime, AVG(value)
FROM tag
WHERE name = 'TAG_0001'
  AND time >= DATE_BIN('minute', 20, SYSDATE, 0) - 20m
GROUP BY mtime;
```

#### custom rollup 예

custom rollup도 동일합니다. 단, rollup 쪽은 destination table을 읽고, 최근 구간은 source를 직접 다시 집계합니다.

```sql
SELECT code, time,
       SUM(sum_price) / SUM(cnt) AS avg_price
FROM (
      SELECT code, time,
             SUM(sum_price) AS sum_price,
             SUM(cnt)       AS cnt
      FROM stock_rollup_1m
      WHERE time < DATE_TRUNC('minute', SYSDATE) - 2m
      GROUP BY code, time

      UNION ALL

      SELECT code,
             DATE_TRUNC('minute', time) AS time,
             SUM(price)                 AS sum_price,
             COUNT(*)                   AS cnt
      FROM stock_tick
      WHERE time >= DATE_TRUNC('minute', SYSDATE) - 2m
      GROUP BY code, time
     )
GROUP BY code, time
ORDER BY code, time;
```

<a id="correction-abnormal-data-rollup-rebuild"></a>

## 이상 데이터 정정 후 ROLLUP Rebuild

### 시나리오 개요

잘못 입력된 센서 데이터를 삭제 또는 정정하고, 영향받은 ROLLUP 집계를 재구성하는 운영 절차입니다.

센서 오작동, 수집기 버그, 단위 변환 오류 등으로 비정상 값이 삽입되면 ROLLUP 집계(최솟값, 최댓값, 평균 등)가 오염됩니다. 이상 데이터를 탐지하고 TAG data UPDATE로 정정한 뒤 `ROLLUP_REBUILD`로 집계를 재계산하는 절차입니다.

> **주의**: Cluster Edition에서는 `ROLLUP_REBUILD`를 지원하지 않습니다. 이 시나리오는 Standard Edition 대상입니다.

> **권장**: 대량 정정 전 해당 기간의 백업을 수행하십시오. `name` 또는 `time` 자체를 바꿔야 해서 삭제/재입력이 필요한 경우 삭제된 TAG 데이터는 복구할 수 없습니다.

### 1단계: 이상 데이터 탐지

#### 범위 이탈 값 확인

정상 범위를 벗어난 값을 쿼리합니다. 온도 센서의 정상 범위가 -40 ~ 200도라면 다음과 같이 확인합니다.

```sql
-- 범위 이탈 데이터 확인
SELECT name, time, value
  FROM sensor_tag
 WHERE name = 'sensor-01'
   AND (value < -40 OR value > 200)
 ORDER BY time;
```

#### 특정 기간 데이터 분포 확인

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

#### 이상 데이터 샘플 조회

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

### 2단계: 데이터 백업 (권장)

대량 UPDATE 전 해당 기간 데이터를 백업합니다.

```sql
-- 이상 데이터가 포함된 기간을 기간 백업
BACKUP DATABASE
    FROM TO_DATE('2024-01-01', 'YYYY-MM-DD')
    TO   TO_DATE('2024-01-02', 'YYYY-MM-DD')
    INTO DISK = '/backup/before_correction_20240101';
```

백업이 완료된 후 다음 단계를 진행합니다.

### 3단계: 이상 데이터 정정

TAG 테이블에서 이상 데이터를 직접 정정합니다. UPDATE 조건을 정확히 지정해 정상 데이터가 수정되지 않도록 합니다.

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

### 4단계: 삭제/재입력이 필요한 경우

`name` 또는 `time` 값을 바꿔야 하는 경우에는 TAG data UPDATE로 처리할 수 없습니다. 새
`name`/`time` 값으로 정정 데이터를 입력하고, 운영 정책에 따라 기존 데이터를 삭제합니다.

#### machsql로 직접 삽입

```sql
-- 정정된 name/time 값으로 직접 삽입
INSERT INTO sensor_tag VALUES ('sensor-01', TO_DATE('2024-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'), 25.3);
INSERT INTO sensor_tag VALUES ('sensor-01', TO_DATE('2024-01-01 00:01:00', 'YYYY-MM-DD HH24:MI:SS'), 25.5);
```

#### CSV 파일로 대량 재입력

정정된 데이터를 CSV 파일로 준비한 뒤 machloader로 적재할 수도 있습니다.

```bash
# CSV 파일 형식: name,time,value
# sensor-01,2024-01-01 00:00:00 000:000:000,25.3
# sensor-01,2024-01-01 00:01:00 000:000:000,25.5

machloader -i -t sensor_tag -d corrected_data.csv \
    -F "time YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn"
```

### 5단계: ROLLUP Rebuild 실행

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

### 6단계: Rebuild 완료와 상태 확인

`ROLLUP_REBUILD` 호출은 대상 내장·확장·Custom Rollup의 재구축을 완료한 뒤 반환합니다.
호출이 성공한 후 ROLLUP이 다시 활성 상태인지 확인합니다.

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

### 7단계: 정정 전후 비교 검증

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

### 정기 데이터 품질 점검 패턴

이상 데이터를 조기에 탐지하기 위한 정기 점검 쿼리입니다.

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

### 요약

| 단계 | 작업 |
|------|------|
| 1 | 범위 이탈·이상값 탐지 쿼리 실행 |
| 2 | 이상 데이터 포함 기간 백업 |
| 3 | `UPDATE sensor_tag SET ... WHERE name ... AND time ...` 이상 데이터 정정 |
| 4 | name/time 변경이 필요한 경우에만 정정 데이터 재입력 후 기존 데이터 삭제 |
| 5 | `EXEC ROLLUP_REBUILD(...)` ROLLUP 재계산 |
| 6 | `v$rollup`으로 Rebuild 완료 확인 |
| 7 | 원시 데이터 집계와 ROLLUP 집계 비교 검증 |

### 관련 문서

- [백업, 복원, 마운트](../../operations-configuration-recovery/backup-restore-mount/)
- [센서 데이터 저장과 ROLLUP 분석](/dbms/tag-rollup-usage/patterns-scenarios/#storage-sensor-data-rollup)
