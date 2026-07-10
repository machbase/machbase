---
title: '10.2 테이블 구조와 스키마'
weight: 20
toc: true
---

VOLATILE 테이블의 PRIMARY KEY 설계와 스키마 구성 방법을 다룹니다.


<a id="primary-key-design-primary-key"></a>

### PRIMARY KEY 설계

VOLATILE 테이블은 PRIMARY KEY 없이도 생성할 수 있습니다. 단, PK 기반 조회나 `ON DUPLICATE KEY UPDATE`를 사용하려면 PRIMARY KEY가 필요합니다.

#### 단일 PRIMARY KEY

```sql
CREATE VOLATILE TABLE volatile_device_state (
    device_id  VARCHAR(32) PRIMARY KEY,
    state      VARCHAR(16),
    updated_at DATETIME
);
```

#### 복합 키가 필요한 경우

여러 컬럼 조합으로 행을 고유하게 식별해야 하면 조합 키를 별도 PRIMARY KEY 컬럼으로 둡니다.

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

#### ON DUPLICATE KEY UPDATE와 함께 사용

```sql
-- PRIMARY KEY 중복 시 UPDATE 실행
INSERT INTO volatile_device_state VALUES ('DEV-01', 'ONLINE', NOW)
ON DUPLICATE KEY UPDATE SET state = 'ONLINE', updated_at = NOW;
```

#### 주의사항

- PRIMARY KEY 없이 생성할 수 있지만, PK 기반 동작(UPSERT, PK 조회 등)은 사용할 수 없습니다.
- PRIMARY KEY 값은 중복할 수 없습니다 (ON DUPLICATE KEY UPDATE 사용 시 제외).
- PRIMARY KEY 컬럼은 하나만 지정합니다.

<a id="volatile-table-design"></a>

## VOLATILE 테이블 설계

VOLATILE 테이블은 메모리에만 존재하며, 서버 재시작 시 데이터가 소멸됩니다. 여러 세션이
공유하되 재시작 후 복구할 필요가 없는 상태나 캐시 용도로 활용합니다.

- **[활용 사례](/dbms/volatile-table-usage/patterns-scenarios/#use-cases-volatile)**
- **[영속성 차이·DDL](/dbms/volatile-table-usage/create-alter-drop/#differences-persistence-ddl)**
- **[메모리 생명주기](/dbms/volatile-table-usage/memory-lifecycle/#lifecycle-memory)**
- **[PRIMARY KEY 설계](/dbms/volatile-table-usage/table-structure-schema/#primary-key-design-primary-key)**
- **[Red-Black 트리 인덱스](/dbms/volatile-table-usage/red-black-index/#index-strategy-red-black)**
- **[ON DUPLICATE KEY UPDATE](/dbms/volatile-table-usage/on-duplicate-key-update/#on-duplicate-key-update)**
- **[데이터 손실 위험](/dbms/volatile-table-usage/restart-data-loss/#data-loss)**
