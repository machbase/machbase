---
type: docs
title: 'PRIMARY KEY 설계'
weight: 40
---

VOLATILE 테이블은 PRIMARY KEY가 필수입니다. `ON DUPLICATE KEY UPDATE` 구문을 위해서도 PRIMARY KEY가 필요합니다.

## 단일 PRIMARY KEY

```sql
CREATE VOLATILE TABLE device_state (
    device_id  VARCHAR(32) PRIMARY KEY,
    state      VARCHAR(16),
    updated_at DATETIME
);
```

## 복합 PRIMARY KEY

여러 컬럼의 조합으로 행을 고유하게 식별합니다.

```sql
CREATE VOLATILE TABLE hourly_avg (
    sensor_id VARCHAR(64) PRIMARY KEY,
    hour_ts   DATETIME    PRIMARY KEY,
    avg_value DOUBLE,
    count     INTEGER
);

-- 복합 PK 삽입
INSERT INTO hourly_avg VALUES ('TEMP-01', '2024-01-01 10:00:00', 23.5, 60);
INSERT INTO hourly_avg VALUES ('TEMP-01', '2024-01-01 11:00:00', 24.1, 60);
INSERT INTO hourly_avg VALUES ('TEMP-02', '2024-01-01 10:00:00', 21.0, 60);

-- 복합 PK 조회
SELECT * FROM hourly_avg WHERE sensor_id = 'TEMP-01' AND hour_ts = '2024-01-01 10:00:00';
```

## ON DUPLICATE KEY UPDATE와 함께 사용

```sql
-- PRIMARY KEY 중복 시 UPDATE 실행
INSERT INTO device_state VALUES ('DEV-01', 'ONLINE', NOW)
ON DUPLICATE KEY UPDATE state = 'ONLINE', updated_at = NOW;
```

## 주의사항

- VOLATILE 테이블에 PRIMARY KEY를 지정하지 않으면 `CREATE` 오류가 발생합니다.
- PRIMARY KEY 값은 중복될 수 없습니다 (ON DUPLICATE KEY UPDATE 사용 시 제외).
