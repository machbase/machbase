---
type: docs
title: 'ON DUPLICATE KEY UPDATE'
weight: 60
---

`ON DUPLICATE KEY UPDATE`는 VOLATILE 테이블의 핵심 기능입니다. PRIMARY KEY가 중복될 때 INSERT 대신 UPDATE를 실행합니다.

## 기본 문법

```sql
INSERT INTO table_name VALUES (pk_val, col2_val, ...)
ON DUPLICATE KEY UPDATE col2 = new_val, col3 = new_val;
```

## 최신 값 캐시 (UPSERT)

```sql
CREATE VOLATILE TABLE sensor_latest (
    sensor_id  VARCHAR(64) PRIMARY KEY,
    value      DOUBLE,
    updated_at DATETIME
);

-- 처음 삽입 (INSERT)
INSERT INTO sensor_latest VALUES ('TEMP-01', 23.5, NOW)
ON DUPLICATE KEY UPDATE value = 23.5, updated_at = NOW;

-- 동일 PK 재삽입 (UPDATE 실행)
INSERT INTO sensor_latest VALUES ('TEMP-01', 24.1, NOW)
ON DUPLICATE KEY UPDATE value = 24.1, updated_at = NOW;

-- 결과: TEMP-01의 value = 24.1 (업데이트됨)
SELECT * FROM sensor_latest WHERE sensor_id = 'TEMP-01';
```

## VALUES() 함수 사용

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

-- 카운트 증가 (없으면 1로 시작, 있으면 +1)
INSERT INTO event_counter VALUES ('LOGIN', 1, NOW)
ON DUPLICATE KEY UPDATE cnt = cnt + 1, last_seen = NOW;
```

## 주의사항

- `ON DUPLICATE KEY UPDATE`는 VOLATILE 테이블 전용입니다. LOG, TAG, RDB 테이블에서는 사용할 수 없습니다.
- UPDATE 절에서 PRIMARY KEY 컬럼 값을 변경하지 마십시오.
