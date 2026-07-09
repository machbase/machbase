---
title: '10.13 ON DUPLICATE KEY UPDATE'
weight: 130
toc: true
---
ON DUPLICATE KEY UPDATE에 해당하는 세부 문서를 모았습니다.


<a id="on-duplicate-key-update"></a>

## UPDATE와 ON DUPLICATE KEY UPDATE

VOLATILE 테이블은 PRIMARY KEY 기준의 `UPDATE` 문과 `ON DUPLICATE KEY UPDATE` 구문을
지원합니다.

### 일반 UPDATE

```sql
CREATE VOLATILE TABLE device_status (
    device_id  VARCHAR(64) PRIMARY KEY,
    status     VARCHAR(16),
    value      DOUBLE,
    updated_at DATETIME
);

-- PRIMARY KEY 기준 UPDATE
UPDATE device_status SET status = 'NORMAL', updated_at = NOW WHERE device_id = 'DEV-01';
```

VOLATILE 테이블의 `UPDATE`/`DELETE` 조건은 PRIMARY KEY 동등 조건이어야 합니다. 일반 컬럼
조건이나 전체 행 갱신은 사용할 수 없습니다.

### ON DUPLICATE KEY UPDATE (UPSERT)

PRIMARY KEY가 중복될 때 INSERT 대신 UPDATE를 실행합니다. VOLATILE 테이블의 핵심 UPSERT 패턴입니다.

```sql
-- 처음 삽입 (INSERT)
INSERT INTO device_status VALUES ('DEV-01', 'NORMAL', 23.5, NOW)
ON DUPLICATE KEY UPDATE SET status = 'NORMAL', value = 23.5, updated_at = NOW;

-- 동일 PK 재삽입 (UPDATE 실행)
INSERT INTO device_status VALUES ('DEV-01', 'ALARM', 95.3, NOW)
ON DUPLICATE KEY UPDATE SET status = 'ALARM', value = 95.3, updated_at = NOW;

-- 결과: DEV-01의 status = 'ALARM' (업데이트됨)
```

### 삽입값으로 갱신

삽입하려던 값으로 기존 행을 갱신하려면 `ON DUPLICATE KEY UPDATE` 뒤에 별도 `SET` 절을
쓰지 않는 형식을 사용할 수 있습니다.

```sql
INSERT INTO hourly_summary VALUES ('TEMP-01', '2024-01-01 10:00:00', 23.5, 25.0, 60)
ON DUPLICATE KEY UPDATE;
```

### 카운터 패턴

```sql
CREATE VOLATILE TABLE event_counter (
    event_type VARCHAR(32) PRIMARY KEY,
    cnt        LONG,
    last_seen  DATETIME
);

-- 없으면 1로 시작, 있으면 명시한 값으로 갱신
INSERT INTO event_counter VALUES ('LOGIN', 1, NOW)
ON DUPLICATE KEY UPDATE SET cnt = 1, last_seen = NOW;

INSERT INTO event_counter VALUES ('LOGIN', 2, NOW)
ON DUPLICATE KEY UPDATE SET cnt = 2, last_seen = NOW;
```

### 주의사항

- `ON DUPLICATE KEY UPDATE`는 VOLATILE 테이블에서 동작합니다. TAG, LOG 테이블에서는 사용할 수 없습니다.
- UPDATE 절에서 PRIMARY KEY 컬럼 값을 변경하지 마십시오.
- `ON DUPLICATE KEY UPDATE SET` 절에는 갱신할 값을 명시합니다. `cnt = cnt + 1`처럼 기존 값을
  참조해 계산하는 카운터 표현식은 현재 빌드에서 사용할 수 없습니다.
