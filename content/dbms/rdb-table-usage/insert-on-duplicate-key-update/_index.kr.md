---
title: '8.17 INSERT ON DUPLICATE KEY UPDATE'
weight: 170
toc: true
---

`INSERT ... ON DUPLICATE KEY UPDATE`는 RDB 테이블에 row를 INSERT하다가 PRIMARY KEY 또는 UNIQUE KEY 충돌이 발생하면, INSERT를 실패로 끝내지 않고 기존 row를 UPDATE하는 구문입니다.

이 구문은 장비 마스터 동기화, 최신 상태 테이블 갱신, 집계 카운터 증가, 외부 시스템 upsert 적재처럼 "없으면 INSERT, 있으면 UPDATE"가 필요한 업무 로직에 사용할 수 있습니다.

## 지원 문법

RDB 테이블에서는 `INSERT ... VALUES ...` 형태의 upsert를 지원합니다.

```sql
INSERT INTO table_name VALUES (...)
    ON DUPLICATE KEY UPDATE;

INSERT INTO table_name VALUES (...)
    ON DUPLICATE KEY UPDATE SET column_name = expression [, ...];

INSERT INTO table_name(column_name, ...)
VALUES (...)
    ON DUPLICATE KEY UPDATE;

INSERT INTO table_name(column_name, ...)
VALUES (...)
    ON DUPLICATE KEY UPDATE SET column_name = expression [, ...];
```

duplicate key로 인정되는 대상은 다음과 같습니다.

- RDB PRIMARY KEY
- RDB UNIQUE INDEX
- RDB 복합 UNIQUE INDEX

## 기본 동작

중복이 없으면 일반 INSERT와 같이 새 row를 추가합니다.

```sql
CREATE RDB TABLE device_state (
    device_id INTEGER PRIMARY KEY,
    status VARCHAR(16),
    alarm_count INTEGER,
    updated_at DATETIME
);

INSERT INTO device_state
VALUES (1, 'NORMAL', 0, TO_DATE('2026-07-10 09:00:00'))
    ON DUPLICATE KEY UPDATE SET
        status = 'NORMAL',
        updated_at = TO_DATE('2026-07-10 09:00:00');
```

PRIMARY KEY가 중복되면 기존 row를 UPDATE합니다.

```sql
INSERT INTO device_state
VALUES (1, 'ALARM', 1, TO_DATE('2026-07-10 09:05:00'))
    ON DUPLICATE KEY UPDATE SET
        status = 'ALARM',
        alarm_count = alarm_count + 1,
        updated_at = TO_DATE('2026-07-10 09:05:00');
```

`SET` 절의 오른쪽 식은 기존 duplicate row를 기준으로 평가됩니다. 따라서 `alarm_count = alarm_count + 1`은 INSERT하려던 row의 `alarm_count`가 아니라 기존 row의 `alarm_count`에 1을 더합니다.

```sql
SELECT device_id, status, alarm_count, updated_at
FROM device_state
WHERE device_id = 1;
```

예상 결과 형태는 다음과 같습니다.

```text
DEVICE_ID  STATUS  ALARM_COUNT  UPDATED_AT
---------  ------  -----------  -----------------------------
1          ALARM   1            2026-07-10 09:05:00 000:000:000
```

`ON DUPLICATE KEY UPDATE` 뒤에 `SET` 절을 쓰지 않을 수 있습니다.

```sql
CREATE RDB TABLE asset_cache (
    asset_id INTEGER PRIMARY KEY,
    asset_name VARCHAR(80),
    location VARCHAR(80),
    keep_value INTEGER
);

INSERT INTO asset_cache VALUES (1, 'compressor-a', 'plant-1', 100);

INSERT INTO asset_cache(asset_id, asset_name, location)
VALUES (1, 'compressor-a-renamed', 'plant-2')
    ON DUPLICATE KEY UPDATE;
```

`SET` 절이 없으면 INSERT 대상 컬럼 중 PRIMARY KEY가 아닌 컬럼만 기존 row에 반영됩니다. 위 예에서는 `asset_name`, `location`이 갱신되고, 컬럼 목록에 없던 `keep_value`는 기존 값을 유지합니다.

```sql
SELECT asset_id, asset_name, location, keep_value
FROM asset_cache
ORDER BY asset_id;
```

예상 결과 형태는 다음과 같습니다.

```text
ASSET_ID  ASSET_NAME            LOCATION  KEEP_VALUE
--------  --------------------  --------  ----------
1         compressor-a-renamed  plant-2   100
```

PRIMARY KEY 컬럼만 있는 테이블에서 중복 row에 `SET` 없는 upsert를 실행하면 갱신 대상 컬럼이 없으므로 row는 변경되지 않습니다.

## UNIQUE INDEX 중복 처리

PRIMARY KEY뿐 아니라 UNIQUE INDEX 충돌도 갱신 경로를 실행합니다.

```sql
CREATE RDB TABLE account_profile (
    id INTEGER PRIMARY KEY,
    email VARCHAR(120),
    display_name VARCHAR(80),
    login_count INTEGER
);

CREATE UNIQUE INDEX uidx_account_profile_email
ON account_profile(email);

INSERT INTO account_profile
VALUES (1, 'ops@example.com', 'ops-user', 1);

INSERT INTO account_profile
VALUES (2, 'ops@example.com', 'ops-renamed', 1)
    ON DUPLICATE KEY UPDATE SET
        display_name = 'ops-renamed',
        login_count = login_count + 1;

SELECT id, email, display_name, login_count
FROM account_profile
ORDER BY id;
```

`email` UNIQUE INDEX가 중복되므로 `id = 1` row가 UPDATE됩니다. INSERT하려던 `id = 2` row는 새로 추가되지 않습니다.

복합 UNIQUE INDEX는 전체 key가 같은 경우 duplicate로 처리됩니다.

```sql
CREATE RDB TABLE daily_device_summary (
    id INTEGER PRIMARY KEY,
    device_id INTEGER,
    summary_day VARCHAR(10),
    event_count INTEGER,
    last_status VARCHAR(16)
);

CREATE UNIQUE INDEX uidx_daily_device_summary
ON daily_device_summary(device_id, summary_day);

INSERT INTO daily_device_summary
VALUES (1, 101, '2026-07-10', 3, 'NORMAL');

INSERT INTO daily_device_summary
VALUES (2, 101, '2026-07-10', 1, 'ALARM')
    ON DUPLICATE KEY UPDATE SET
        event_count = event_count + 1,
        last_status = 'ALARM';

INSERT INTO daily_device_summary
VALUES (3, 101, '2026-07-11', 1, 'NORMAL')
    ON DUPLICATE KEY UPDATE SET
        event_count = event_count + 1;
```

첫 번째 upsert는 `(device_id, summary_day) = (101, '2026-07-10')` row를 UPDATE합니다. 두 번째 upsert는 날짜가 다르므로 새 row를 INSERT합니다.

UNIQUE KEY에 `NULL`이 포함된 row끼리는 duplicate로 처리하지 않습니다.

## 활용 예제

TAG 테이블에는 시간순 측정값이 계속 쌓이고, RDB 테이블에는 장비별 최신 상태만 유지할 수 있습니다.

```sql
CREATE RDB TABLE latest_device_status (
    device_name VARCHAR(80) PRIMARY KEY,
    last_value DOUBLE,
    last_state VARCHAR(16),
    event_count LONG,
    updated_at DATETIME
);

INSERT INTO latest_device_status
VALUES ('compressor-a', 72.5, 'NORMAL', 1, TO_DATE('2026-07-10 09:00:00'))
    ON DUPLICATE KEY UPDATE SET
        last_value = 72.5,
        last_state = 'NORMAL',
        event_count = event_count + 1,
        updated_at = TO_DATE('2026-07-10 09:00:00');

INSERT INTO latest_device_status
VALUES ('compressor-a', 91.2, 'ALARM', 1, TO_DATE('2026-07-10 09:05:00'))
    ON DUPLICATE KEY UPDATE SET
        last_value = 91.2,
        last_state = 'ALARM',
        event_count = event_count + 1,
        updated_at = TO_DATE('2026-07-10 09:05:00');
```

이 패턴은 dashboard가 최신 상태만 빠르게 조회해야 할 때 사용할 수 있습니다.

외부 시스템에서 같은 natural key로 master 데이터를 반복 전송할 때 UNIQUE INDEX를 기준으로 upsert할 수 있습니다.

```sql
CREATE RDB TABLE customer_device (
    id LONG PRIMARY KEY AUTO_INCREMENT,
    external_device_id VARCHAR(64),
    device_name VARCHAR(80),
    owner_name VARCHAR(80),
    enabled INTEGER
);

CREATE UNIQUE INDEX uidx_customer_device_external_id
ON customer_device(external_device_id);

INSERT INTO customer_device(external_device_id, device_name, owner_name, enabled)
VALUES ('ERP-DEV-10001', 'compressor-a', 'line-1', 1)
    ON DUPLICATE KEY UPDATE SET
        device_name = 'compressor-a',
        owner_name = 'line-1',
        enabled = 1;

INSERT INTO customer_device(external_device_id, device_name, owner_name, enabled)
VALUES ('ERP-DEV-10001', 'compressor-a-renamed', 'line-2', 1)
    ON DUPLICATE KEY UPDATE SET
        device_name = 'compressor-a-renamed',
        owner_name = 'line-2',
        enabled = 1;
```

첫 INSERT는 새 row를 생성하고, 두 번째 INSERT는 `external_device_id` UNIQUE INDEX 충돌로 기존 row를 UPDATE합니다. 내부 `id`는 유지됩니다.

소스 데이터의 컬럼 값을 그대로 최신 cache에 반영하고 싶으면 `SET` 절 없는 upsert를 사용할 수 있습니다.

```sql
CREATE RDB TABLE tag_alias_cache (
    alias_name VARCHAR(80) PRIMARY KEY,
    tag_name VARCHAR(80),
    unit VARCHAR(16),
    description VARCHAR(160),
    manually_checked INTEGER
);

INSERT INTO tag_alias_cache
VALUES ('compressor-a-temp', 'comp_a.temp', 'celsius', 'main compressor temp', 1);

INSERT INTO tag_alias_cache(alias_name, tag_name, unit, description)
VALUES ('compressor-a-temp', 'comp_a.temperature', 'celsius', 'renamed tag')
    ON DUPLICATE KEY UPDATE;
```

위 구문은 `tag_name`, `unit`, `description`만 갱신합니다. 컬럼 목록에 없는 `manually_checked`는 기존 값을 유지합니다.

집계 테이블에서 key별 발생 횟수를 누적할 수 있습니다.

```sql
CREATE RDB TABLE alarm_counter (
    alarm_code VARCHAR(32) PRIMARY KEY,
    first_seen DATETIME,
    last_seen DATETIME,
    hit_count LONG
);

INSERT INTO alarm_counter
VALUES (
    'OVER_TEMP',
    TO_DATE('2026-07-10 09:00:00'),
    TO_DATE('2026-07-10 09:00:00'),
    1
)
ON DUPLICATE KEY UPDATE SET
    last_seen = TO_DATE('2026-07-10 09:00:00'),
    hit_count = hit_count + 1;

INSERT INTO alarm_counter
VALUES (
    'OVER_TEMP',
    TO_DATE('2026-07-10 09:05:00'),
    TO_DATE('2026-07-10 09:05:00'),
    1
)
ON DUPLICATE KEY UPDATE SET
    last_seen = TO_DATE('2026-07-10 09:05:00'),
    hit_count = hit_count + 1;
```

`hit_count = hit_count + 1`은 기존 row 기준으로 계산되므로 누적 카운터 구현에 사용할 수 있습니다.

JSON 컬럼도 update 대상 컬럼으로 사용할 수 있습니다.

```sql
CREATE RDB TABLE device_json_state (
    device_id INTEGER PRIMARY KEY,
    state JSON,
    updated_at DATETIME
);

INSERT INTO device_json_state
VALUES (
    1,
    '{"status":"NORMAL","score":10}',
    TO_DATE('2026-07-10 09:00:00')
)
ON DUPLICATE KEY UPDATE SET
    state = '{"status":"NORMAL","score":10}',
    updated_at = TO_DATE('2026-07-10 09:00:00');

INSERT INTO device_json_state
VALUES (
    1,
    '{"status":"ALARM","score":90}',
    TO_DATE('2026-07-10 09:05:00')
)
ON DUPLICATE KEY UPDATE SET
    state = '{"status":"ALARM","score":90}',
    updated_at = TO_DATE('2026-07-10 09:05:00');

SELECT JSON_EXTRACT_STRING(state, '$.status') AS status,
       JSON_EXTRACT_INTEGER(state, '$.score') AS score
FROM device_json_state
WHERE device_id = 1;
```

제한: JSON path UNIQUE INDEX는 duplicate trigger 후보에서 제외됩니다. JSON path UNIQUE INDEX
충돌은 upsert 갱신 경로로 전환되지 않고 unique constraint 오류로 처리됩니다.

## 트랜잭션과 권한

RDB upsert는 일반 INSERT/UPDATE와 같이 트랜잭션 안에서 COMMIT 또는 ROLLBACK됩니다.

```sql
CREATE RDB TABLE tx_device_state (
    id INTEGER PRIMARY KEY,
    status VARCHAR(16),
    count_value INTEGER
);

INSERT INTO tx_device_state VALUES (1, 'NORMAL', 10);

BEGIN;

INSERT INTO tx_device_state VALUES (2, 'NORMAL', 1)
    ON DUPLICATE KEY UPDATE SET count_value = count_value + 1;

INSERT INTO tx_device_state VALUES (1, 'ALARM', 1)
    ON DUPLICATE KEY UPDATE SET
        status = 'ALARM',
        count_value = count_value + 1;

ROLLBACK;

SELECT id, status, count_value
FROM tx_device_state
ORDER BY id;
```

위 예에서는 삽입 경로와 갱신 경로가 모두 ROLLBACK됩니다.

실패한 duplicate update statement가 있어도 explicit transaction 자체는 유지됩니다. 응용 프로그램은 오류를 확인한 뒤 같은 transaction에서 후속 SQL을 실행하거나 ROLLBACK할 수 있습니다.

RDB upsert statement에는 `INSERT` 권한과 `UPDATE` 권한이 모두 필요합니다. 실제 실행 결과가
삽입 경로가 되더라도 statement에 갱신 경로가 포함되므로 두 권한을 모두 부여해야 합니다.

```sql
GRANT INSERT ON SYS.DEVICE_STATE TO app_user;
GRANT UPDATE ON SYS.DEVICE_STATE TO app_user;
```

`SELECT` 권한은 RDB upsert statement 실행 자체에는 필요하지 않습니다. 단, 응용 프로그램이 결과 확인을 위해 `SELECT`를 실행한다면 별도로 `SELECT` 권한이 필요합니다.

## 타입과 지원하지 않는 구문

`SET` 절에서 갱신할 수 있는 컬럼 타입은 일반 RDB `UPDATE`와 같은 public 타입 정책을 따릅니다.

| 분류 | 타입 |
| --- | --- |
| 정수 | `SHORT`, `INT16`, `USHORT`, `UINT16`, `INT`, `INTEGER`, `INT32`, `UINTEGER`, `UINT32`, `LONG`, `INT64`, `ULONG`, `UINT64` |
| 실수 | `FLOAT`, `DOUBLE` |
| 고정소수 | `DECIMAL`, `NUMERIC`, `DEC`, `FIXED`, `NUMBER` |
| 문자열/LOB | `VARCHAR`, `TEXT`, `CLOB`, `BINARY`, `BLOB` |
| 기타 | `DATETIME`, `IPV4`, `IPV6`, `JSON` |

duplicate trigger가 되는 key/index 타입은 RDB PRIMARY KEY 및 UNIQUE INDEX의 타입 정책을
따릅니다. 이 기능은 key 타입의 지원 범위를 확장하지 않습니다.

다음 구문은 지원하지 않습니다.

```sql
-- INSERT SELECT와 ON DUPLICATE KEY UPDATE 결합은 지원하지 않습니다.
INSERT INTO device_state(device_id, status, alarm_count, updated_at)
SELECT device_id, status, alarm_count, updated_at
FROM staging_device_state
ON DUPLICATE KEY UPDATE SET status = 'UPDATED';

-- MySQL VALUES(col) 함수는 지원하지 않습니다.
INSERT INTO device_state VALUES (1, 'ALARM', 1, TO_DATE('2026-07-10 09:00:00'))
ON DUPLICATE KEY UPDATE SET status = VALUES(status);

-- EXCLUDED alias는 지원하지 않습니다.
INSERT INTO device_state VALUES (1, 'ALARM', 1, TO_DATE('2026-07-10 09:00:00'))
ON DUPLICATE KEY UPDATE SET status = EXCLUDED.status;

-- conflict target syntax는 지원하지 않습니다.
INSERT INTO device_state VALUES (1, 'ALARM', 1, TO_DATE('2026-07-10 09:00:00'))
ON CONFLICT (device_id) DO UPDATE SET status = 'ALARM';
```

대상 테이블 제한은 다음과 같습니다.

- RDB 테이블에서만 지원합니다.
- LOG 테이블과 TAG 테이블에는 지원하지 않습니다.
- RDB 테이블이라도 PRIMARY KEY 또는 UNIQUE INDEX가 없으면 사용할 수 없습니다.
- JSON path UNIQUE INDEX는 duplicate trigger로 사용하지 않습니다.

## 충돌과 오류 처리

여러 UNIQUE INDEX가 같은 기존 row를 가리키면 해당 row를 한 번 UPDATE합니다. 그러나 INSERT하려는 row가 여러 UNIQUE INDEX에서 서로 다른 기존 row와 충돌하면 어느 row를 UPDATE해야 하는지 결정할 수 없으므로 statement는 실패합니다.

```sql
CREATE RDB TABLE user_contact (
    id INTEGER PRIMARY KEY,
    email VARCHAR(120),
    phone VARCHAR(40),
    note VARCHAR(80)
);

CREATE UNIQUE INDEX uidx_user_contact_email ON user_contact(email);
CREATE UNIQUE INDEX uidx_user_contact_phone ON user_contact(phone);

INSERT INTO user_contact VALUES (1, 'a@example.com', '010-0000-0001', 'user-a');
INSERT INTO user_contact VALUES (2, 'b@example.com', '010-0000-0002', 'user-b');

-- email은 id=1과 충돌하고 phone은 id=2와 충돌합니다.
-- 서로 다른 row와 충돌하므로 갱신 경로를 선택하지 않고 실패합니다.
INSERT INTO user_contact VALUES (3, 'a@example.com', '010-0000-0002', 'ambiguous')
ON DUPLICATE KEY UPDATE SET note = 'updated';
```

`SET` 결과가 다른 UNIQUE constraint 또는 `NOT NULL` constraint를 위반해도 statement는 실패하며 기존 row는 보존됩니다.

## 운영 권장 사항

- 업무 key가 명확하면 PRIMARY KEY 또는 UNIQUE INDEX를 먼저 정의합니다.
- 카운터 누적에는 `SET count_col = count_col + 1` 형태를 사용합니다.
- 소스 row의 값을 그대로 반영하려면 `SET` 없는 upsert를 사용할 수 있습니다. 이때 컬럼 목록에서 생략한 컬럼은 보존됩니다.
- 여러 UNIQUE INDEX가 있는 테이블에서는 서로 다른 row와 동시에 충돌할 수 있는 입력을 사전에 정리합니다.
- MySQL 호환 SQL을 이식할 때 `VALUES(col)`, `EXCLUDED`, `ON CONFLICT` 구문은 Machbase 지원 구문으로 바꿉니다.
- JSON path UNIQUE INDEX를 upsert key로 사용하는 설계는 피하고, 필요한 경우 별도 일반 컬럼에 key 값을 저장한 뒤 UNIQUE INDEX를 생성합니다.
