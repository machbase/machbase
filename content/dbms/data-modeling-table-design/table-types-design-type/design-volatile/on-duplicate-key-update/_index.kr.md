---
type: docs
title: 'UPDATE와 ON DUPLICATE KEY UPDATE'
weight: 60
---

VOLATILE 테이블은 일반 `UPDATE` 문과 `ON DUPLICATE KEY UPDATE` 구문을 모두 지원합니다.

## 일반 UPDATE

```sql
CREATE VOLATILE TABLE device_status (
    device_id  VARCHAR(64) PRIMARY KEY,
    status     VARCHAR(16),
    value      DOUBLE,
    updated_at DATETIME
);

-- 일반 UPDATE (WHERE 조건)
UPDATE device_status SET status = 'NORMAL', updated_at = NOW WHERE device_id = 'DEV-01';

-- 여러 행 UPDATE
UPDATE device_status SET status = 'OFFLINE' WHERE updated_at < NOW - 300000000000;

-- 전체 행 UPDATE
UPDATE device_status SET status = 'UNKNOWN';
```

## ON DUPLICATE KEY UPDATE (UPSERT)

PRIMARY KEY가 중복될 때 INSERT 대신 UPDATE를 실행합니다. VOLATILE 테이블의 핵심 UPSERT 패턴입니다.

```sql
-- 처음 삽입 (INSERT)
INSERT INTO device_status VALUES ('DEV-01', 'NORMAL', 23.5, NOW)
ON DUPLICATE KEY UPDATE status = 'NORMAL', value = 23.5, updated_at = NOW;

-- 동일 PK 재삽입 (UPDATE 실행)
INSERT INTO device_status VALUES ('DEV-01', 'ALARM', 95.3, NOW)
ON DUPLICATE KEY UPDATE status = 'ALARM', value = 95.3, updated_at = NOW;

-- 결과: DEV-01의 status = 'ALARM' (업데이트됨)
```

## VALUES() 함수

INSERT하려던 값을 UPDATE 절에서 참조할 때 `VALUES()` 함수를 사용합니다.

```sql
INSERT INTO hourly_summary VALUES ('TEMP-01', '2024-01-01 10:00:00', 23.5, 25.0, 60)
ON DUPLICATE KEY UPDATE
    avg_val = VALUES(avg_val),
    max_val = VALUES(max_val),
    count   = VALUES(count);
```

## 카운터 패턴

```sql
CREATE VOLATILE TABLE event_counter (
    event_type VARCHAR(32) PRIMARY KEY,
    cnt        LONG,
    last_seen  DATETIME
);

-- 없으면 1로 시작, 있으면 +1
INSERT INTO event_counter VALUES ('LOGIN', 1, NOW)
ON DUPLICATE KEY UPDATE cnt = cnt + 1, last_seen = NOW;
```

## 주의사항

- `ON DUPLICATE KEY UPDATE`는 VOLATILE 테이블에서 동작합니다. TAG, LOG 테이블에서는 사용할 수 없습니다.
- UPDATE 절에서 PRIMARY KEY 컬럼 값을 변경하지 마십시오.
