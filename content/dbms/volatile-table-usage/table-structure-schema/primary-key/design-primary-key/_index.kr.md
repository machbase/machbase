---
type: docs
title: 'PRIMARY KEY 설계'
weight: 40
---

VOLATILE 테이블은 PRIMARY KEY 없이도 생성할 수 있습니다. 단, PK 기반 조회나 `ON DUPLICATE KEY UPDATE` 구문을 사용하려면 PRIMARY KEY가 필요합니다.

## 단일 PRIMARY KEY

```sql
CREATE VOLATILE TABLE volatile_device_state (
    device_id  VARCHAR(32) PRIMARY KEY,
    state      VARCHAR(16),
    updated_at DATETIME
);
```

## 복합 키가 필요한 경우

여러 컬럼의 조합으로 행을 고유하게 식별해야 하면 조합 키를 별도 PRIMARY KEY 컬럼으로 둡니다.

```sql
CREATE VOLATILE TABLE hourly_avg (
    key_id    VARCHAR(96) PRIMARY KEY,
    sensor_id VARCHAR(64),
    hour_ts   DATETIME,
    avg_value DOUBLE,
    count     INTEGER
);

-- 조합 키 삽입
INSERT INTO hourly_avg VALUES ('TEMP-01:2024010110', 'TEMP-01', '2024-01-01 10:00:00', 23.5, 60);
INSERT INTO hourly_avg VALUES ('TEMP-01:2024010111', 'TEMP-01', '2024-01-01 11:00:00', 24.1, 60);
INSERT INTO hourly_avg VALUES ('TEMP-02:2024010110', 'TEMP-02', '2024-01-01 10:00:00', 21.0, 60);

-- 조합 키 조회
SELECT * FROM hourly_avg WHERE key_id = 'TEMP-01:2024010110';
```

## ON DUPLICATE KEY UPDATE와 함께 사용

```sql
-- PRIMARY KEY 중복 시 UPDATE 실행
INSERT INTO volatile_device_state VALUES ('DEV-01', 'ONLINE', NOW)
ON DUPLICATE KEY UPDATE SET state = 'ONLINE', updated_at = NOW;
```

## 주의사항

- VOLATILE 테이블은 PRIMARY KEY 없이 생성할 수 있지만, PK 기반 동작을 사용할 수 없습니다.
- PRIMARY KEY 값은 중복될 수 없습니다 (ON DUPLICATE KEY UPDATE 사용 시 제외).
- PRIMARY KEY 컬럼은 하나만 지정합니다.
