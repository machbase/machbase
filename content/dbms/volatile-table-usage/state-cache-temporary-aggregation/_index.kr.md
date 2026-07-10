---
title: '10.14 상태 캐시와 임시 집계 패턴'
weight: 140
toc: true
---

VOLATILE 테이블의 상태 캐시와 임시 집계 패턴을 다룹니다. 이 절의 패턴은 원본 데이터를 영속 테이블에 보관하고, VOLATILE 테이블에는 빠른 조회를 위한 최신 상태나 중간 결과만 유지하는 방식입니다.

<a id="pattern-volatile-latest-state"></a>

## 최신 상태 캐시

장비나 센서의 최신 상태만 빠르게 조회해야 하면 PRIMARY KEY를 장비 ID로 둔 VOLATILE 테이블을 사용합니다.

```sql
CREATE VOLATILE TABLE device_latest (
    device_id  VARCHAR(64) PRIMARY KEY,
    status     VARCHAR(16),
    value      DOUBLE,
    updated_at DATETIME
);
```

데이터 입력은 UPSERT로 처리합니다.

```sql
INSERT INTO device_latest VALUES ('DEV-01', 'NORMAL', 23.5, NOW)
ON DUPLICATE KEY UPDATE SET status = 'NORMAL', value = 23.5, updated_at = NOW;
```

대시보드나 알람 판단은 최신 상태 캐시를 조회합니다.

```sql
SELECT device_id, status, value, updated_at
FROM device_latest
WHERE device_id = 'DEV-01';
```

원본 이력은 TAG 또는 LOG 테이블에 별도로 저장합니다.

<a id="pattern-volatile-temporary-aggregation"></a>

## 임시 집계 테이블

짧은 주기의 집계 결과를 임시로 유지할 때 VOLATILE 테이블을 사용합니다.

```sql
CREATE VOLATILE TABLE sensor_1min_summary (
    summary_key VARCHAR(96) PRIMARY KEY,
    sensor_id   VARCHAR(64),
    bucket_time DATETIME,
    avg_value   DOUBLE,
    max_value   DOUBLE,
    sample_cnt  LONG
);
```

집계 키는 센서 ID와 시간 버킷을 조합해 만듭니다.

```sql
INSERT INTO sensor_1min_summary
VALUES ('TEMP-01:202601011200', 'TEMP-01', '2026-01-01 12:00:00', 23.5, 24.1, 60)
ON DUPLICATE KEY UPDATE;
```

집계 결과를 장기 보관해야 하면 주기적으로 RDB 또는 LOG 테이블에 복사합니다.

```sql
INSERT INTO sensor_summary_history
SELECT summary_key, sensor_id, bucket_time, avg_value, max_value, sample_cnt
FROM sensor_1min_summary;
```

<a id="pattern-volatile-work-queue-state"></a>

## 작업 상태 캐시

배치나 수집 작업의 현재 상태를 공유해야 할 때도 VOLATILE 테이블을 사용할 수 있습니다.

```sql
CREATE VOLATILE TABLE job_state (
    job_id     VARCHAR(64) PRIMARY KEY,
    status     VARCHAR(16),
    progress   DOUBLE,
    updated_at DATETIME
);

INSERT INTO job_state VALUES ('collector-01', 'RUNNING', 35.0, NOW)
ON DUPLICATE KEY UPDATE SET status = 'RUNNING', progress = 35.0, updated_at = NOW;
```

운영 화면은 이 테이블을 조회해 현재 상태를 표시합니다. 작업 이력이나 감사 로그가 필요하면 별도 LOG 또는 RDB 테이블에 기록합니다.

<a id="pattern-volatile-rebuild"></a>

## 재구성 패턴

VOLATILE 테이블은 재시작 후 비어 있으므로, 원본 데이터에서 다시 구성할 수 있어야 합니다.

```sql
-- 원본 TAG 테이블에서 최근 데이터를 읽어 최신 캐시 재구성
INSERT INTO device_latest
SELECT name, 'UNKNOWN', value, time
FROM sensor_data
WHERE time >= NOW - 60000000000;
```

실제 재구성 쿼리는 원본 테이블의 중복 처리 기준과 최신값 판정 기준에 맞게 작성합니다.

<a id="pattern-volatile-guidelines"></a>

## 설계 지침

- 원본 데이터는 영속 테이블에 보관합니다.
- VOLATILE 테이블에는 최신 상태나 재계산 가능한 결과만 저장합니다.
- PRIMARY KEY는 재구성 시에도 같은 값을 만들 수 있어야 합니다.
- 보존이 필요한 임시 집계는 주기적으로 영속 테이블에 플러시합니다.
- 서버 재시작 후 캐시가 비어 있어도 애플리케이션이 동작하도록 처리합니다.
