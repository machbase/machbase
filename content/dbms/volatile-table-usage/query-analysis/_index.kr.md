---
title: '10.5 조회와 분석'
weight: 50
toc: true
---

VOLATILE 테이블의 데이터 조회 방법을 다룹니다.


<a id="original-85-querying-data"></a>

## Volatile 데이터 추출

VOLATILE 테이블은 다른 테이블 타입과 동일하게 `SELECT` 문으로 조회합니다. 데이터와 인덱스가 메모리에 있으므로 최신 상태 캐시, 임시 집계, 작업 상태 조회처럼 반복 조회가 많은 용도에 적합합니다.

```sql
Mach> create volatile table vtable (id integer primary key, name varchar(20));
Created successfully.
Mach> insert into vtable values(1, 'west device');
1 row(s) inserted.
Mach> insert into vtable values(2, 'east device');
1 row(s) inserted.
Mach> insert into vtable values(3, 'north device');
1 row(s) inserted.
Mach> insert into vtable values(4, 'south device');
1 row(s) inserted.
Mach> select * from vtable;
ID          NAME
-------------------------------------
1           west device
2           east device
3           north device
4           south device
[4] row(s) selected.
Mach> select * from vtable where id = 1;
ID          NAME
-------------------------------------
1           west device
[1] row(s) selected.
Mach> select * from vtable where name like 'west%';
ID          NAME
-------------------------------------
1           west device
[1] row(s) selected.
```

<a id="query-volatile-primary-key"></a>

## PRIMARY KEY 조회

PRIMARY KEY가 있는 VOLATILE 테이블은 키 조건으로 단건 데이터를 조회합니다.

```sql
CREATE VOLATILE TABLE device_status (
    device_id  VARCHAR(64) PRIMARY KEY,
    status     VARCHAR(16),
    value      DOUBLE,
    updated_at DATETIME
);

SELECT device_id, status, value, updated_at
FROM device_status
WHERE device_id = 'DEV-01';
```

최신 상태 캐시는 대부분 PRIMARY KEY 조회로 구성합니다. `ON DUPLICATE KEY UPDATE`로 같은 키의 값을 계속 갱신하면 조회 쿼리는 항상 최신 상태만 읽습니다.

<a id="query-volatile-index"></a>

## 인덱스 기반 조회

PRIMARY KEY 외 컬럼을 조건이나 범위로 자주 조회하면 보조 인덱스를 생성합니다.

```sql
CREATE VOLATILE TABLE sensor_cache (
    sensor_id  VARCHAR(64) PRIMARY KEY,
    value      DOUBLE,
    updated_at DATETIME,
    status     VARCHAR(16)
);

CREATE INDEX idx_sensor_cache_time ON sensor_cache(updated_at);
CREATE INDEX idx_sensor_cache_status ON sensor_cache(status);
```

```sql
SELECT sensor_id, value, updated_at
FROM sensor_cache
WHERE updated_at >= '2026-01-01 10:00:00'
  AND updated_at <  '2026-01-01 11:00:00';
```

모든 인덱스는 메모리를 사용합니다. 조회에 사용하지 않는 인덱스를 과도하게 만들면 메모리 사용량과 갱신 비용이 증가합니다.

<a id="query-volatile-temporary-analysis"></a>

## 임시 집계 조회

짧은 주기의 집계 결과를 VOLATILE 테이블에 저장하면 대시보드나 알람 판단에서 반복 계산을 줄일 수 있습니다.

```sql
CREATE VOLATILE TABLE sensor_1min_summary (
    summary_key VARCHAR(96) PRIMARY KEY,
    sensor_id   VARCHAR(64),
    bucket_time DATETIME,
    avg_value   DOUBLE,
    max_value   DOUBLE,
    sample_cnt  LONG
);

SELECT sensor_id, bucket_time, avg_value, max_value
FROM sensor_1min_summary
WHERE sensor_id = 'TEMP-01'
ORDER BY bucket_time DESC
LIMIT 10;
```

집계 결과를 장기 보관해야 하면 VOLATILE 테이블에만 두지 말고 LOG 또는 RDB 테이블로 주기적으로 복사합니다.

<a id="query-volatile-limitations"></a>

## 조회 시 주의사항

- 서버 재시작 후 VOLATILE 데이터는 비어 있을 수 있으므로 조회 결과가 0건인 상황을 처리합니다.
- PRIMARY KEY 조회가 중심이면 PRIMARY KEY를 반드시 지정합니다.
- 범위 조회나 정렬 조건에 자주 쓰는 컬럼은 보조 인덱스를 검토합니다.
- JSON 컬럼은 VOLATILE 테이블에서 사용할 수 없습니다.
- 중요한 원본 데이터는 TAG, LOG, LOOKUP, RDB 같은 영속 테이블에 저장하고 VOLATILE은 캐시로 사용합니다.
