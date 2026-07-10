---
title: '8.16 AUTO_INCREMENT'
weight: 160
toc: true
---

`AUTO_INCREMENT`는 RDB 테이블의 PRIMARY KEY 값을 서버가 자동으로 생성하도록 하는 컬럼 속성이다. 응용 프로그램이 row마다 고유한 식별자를 직접 계산하지 않아도 되므로, 장비 마스터, 작업 큐, 이벤트 인덱스, 외부 데이터 이관 테이블처럼 단일 숫자 ID가 필요한 RDB 테이블에 사용할 수 있다.

이 기능은 RDB 테이블 전용이다. LOOKUP 테이블의 `PROPERTY(SEQUENCE)` 및 `NEXTVAL()`과는 별개의 기능이다.

## 지원 범위

`AUTO_INCREMENT`는 컬럼 단위 PRIMARY KEY에만 사용할 수 있다.

```sql
CREATE RDB TABLE device_master (
    id LONG PRIMARY KEY AUTO_INCREMENT,
    device_name VARCHAR(80),
    site_code VARCHAR(32)
);

CREATE RDB TABLE work_order (
    id INT64 AUTO_INCREMENT PRIMARY KEY,
    status VARCHAR(16),
    created_at DATETIME
);
```

지원 타입은 다음과 같다.

| 타입 | 지원 여부 | 설명 |
| --- | --- | --- |
| `LONG` | 지원 | RDB `AUTO_INCREMENT` PRIMARY KEY로 사용할 수 있다. |
| `INT64` | 지원 | `LONG`과 같은 64비트 정수 계열로 사용할 수 있다. |
| `SHORT`, `INTEGER`, `ULONG` 등 | 미지원 | `AUTO_INCREMENT` 컬럼으로 사용할 수 없다. |
| `VARCHAR`, `DATETIME`, `TEXT`, `BINARY`, `BLOB`, `CLOB` 등 | 미지원 | 숫자 자동 생성 대상이 아니므로 사용할 수 없다. |

제한 사항은 다음과 같다.

- RDB 테이블에서만 사용할 수 있다.
- `LONG` 또는 `INT64` 컬럼에만 사용할 수 있다.
- 해당 컬럼은 컬럼 단위 `PRIMARY KEY`여야 한다.
- 테이블 단위 PRIMARY KEY, 복합 PRIMARY KEY에는 사용할 수 없다.
- LOOKUP 테이블의 `PROPERTY(SEQUENCE)`와 함께 사용할 수 없다.
- `NEXTVAL()`은 RDB `AUTO_INCREMENT` 컬럼에 사용할 수 없다.

## 기본 사용법

자동 생성 컬럼을 INSERT 컬럼 목록에서 생략하면 서버가 값을 생성한다.

```sql
CREATE RDB TABLE device_master (
    id LONG PRIMARY KEY AUTO_INCREMENT,
    device_name VARCHAR(80),
    site_code VARCHAR(32)
);

INSERT INTO device_master(device_name, site_code)
VALUES ('compressor-01', 'SEOUL-A');

INSERT INTO device_master(device_name, site_code)
VALUES ('pump-02', 'SEOUL-A');

SELECT id, device_name, site_code
FROM device_master
ORDER BY id;
```

예상 결과 형태는 다음과 같다.

```text
ID  DEVICE_NAME    SITE_CODE
--  -------------  ---------
1   compressor-01  SEOUL-A
2   pump-02        SEOUL-A
```

자동 생성 컬럼에 `NULL`을 명시해도 자동값이 생성된다. 이 방식은 INSERT 문을 생성하는 응용 코드가 모든 컬럼을 항상 나열해야 할 때 사용할 수 있다.

```sql
INSERT INTO device_master(id, device_name, site_code)
VALUES (NULL, 'fan-03', 'SEOUL-B');
```

필요하면 `AUTO_INCREMENT` 컬럼에 `NULL`이 아닌 값을 직접 지정할 수 있다.

```sql
INSERT INTO device_master(id, device_name, site_code)
VALUES (1000, 'legacy-boiler-01', 'BUSAN-A');

INSERT INTO device_master(device_name, site_code)
VALUES ('new-boiler-02', 'BUSAN-A');
```

직접 지정한 값이 현재 자동 sequence보다 크면 이후 자동값은 그 이후 값으로 진행될 수 있다. 따라서 `AUTO_INCREMENT` 값은 고유 식별자로 사용하고, 빠짐없는 연속 번호가 필요한 업무 규칙에는 사용하지 않는 것이 좋다.

중복 PRIMARY KEY INSERT는 실패한다.

```sql
INSERT INTO device_master(id, device_name, site_code)
VALUES (1000, 'duplicate-device', 'BUSAN-A');
```

실패한 INSERT 이후 자동값 재사용 여부에 의존하지 않는다. 응용 프로그램은 `AUTO_INCREMENT` 값을 순번 보장 수단이 아니라 row 식별자로 다루어야 한다.

## INSERT SELECT와 이관 패턴

대상 테이블의 자동 생성 컬럼을 생략하면 `INSERT ... SELECT`에서도 row마다 자동값이 생성된다.

```sql
CREATE RDB TABLE staging_device (
    device_name VARCHAR(80),
    site_code VARCHAR(32)
);

CREATE RDB TABLE device_master (
    id LONG PRIMARY KEY AUTO_INCREMENT,
    device_name VARCHAR(80),
    site_code VARCHAR(32)
);

INSERT INTO staging_device VALUES ('compressor-01', 'SEOUL-A');
INSERT INTO staging_device VALUES ('pump-02', 'SEOUL-A');
INSERT INTO staging_device VALUES ('fan-03', 'SEOUL-B');

INSERT INTO device_master(device_name, site_code)
SELECT device_name, site_code
FROM staging_device
ORDER BY device_name;

SELECT id, device_name, site_code
FROM device_master
ORDER BY id;
```

이 패턴은 CSV 또는 외부 시스템에서 임시 테이블로 적재한 데이터를 최종 RDB 마스터 테이블로 옮길 때 사용할 수 있다.

외부 시스템의 key를 보존하면서 Machbase 내부 key를 새로 부여할 수도 있다.

```sql
CREATE RDB TABLE erp_device_stage (
    erp_device_id VARCHAR(40),
    device_name VARCHAR(80),
    site_code VARCHAR(32)
);

CREATE RDB TABLE device_master (
    id LONG PRIMARY KEY AUTO_INCREMENT,
    erp_device_id VARCHAR(40),
    device_name VARCHAR(80),
    site_code VARCHAR(32)
);

INSERT INTO erp_device_stage VALUES ('ERP-10001', 'compressor-01', 'SEOUL-A');
INSERT INTO erp_device_stage VALUES ('ERP-10002', 'pump-02', 'SEOUL-A');

INSERT INTO device_master(erp_device_id, device_name, site_code)
SELECT erp_device_id, device_name, site_code
FROM erp_device_stage
ORDER BY erp_device_id;
```

이 방식은 외부 ID와 내부 ID를 동시에 보관해야 하는 migration 또는 동기화 작업에 적합하다.

## 활용 예제

시계열 TAG 테이블은 장비의 측정값을 저장하고, RDB 테이블은 장비의 업무 속성을 관리하는 데 사용할 수 있다. `AUTO_INCREMENT` ID를 내부 식별자로 사용하면 장비 이름이 바뀌어도 내부 참조를 안정적으로 유지할 수 있다.

```sql
CREATE RDB TABLE asset_master (
    asset_id LONG PRIMARY KEY AUTO_INCREMENT,
    asset_name VARCHAR(80),
    tag_name VARCHAR(80),
    location VARCHAR(80),
    enabled INTEGER
);

INSERT INTO asset_master(asset_name, tag_name, location, enabled)
VALUES ('compressor A', 'comp_a.temp', 'plant-1', 1);

INSERT INTO asset_master(asset_name, tag_name, location, enabled)
VALUES ('compressor B', 'comp_b.temp', 'plant-1', 1);

SELECT asset_id, asset_name, tag_name, location
FROM asset_master
WHERE enabled = 1
ORDER BY asset_id;
```

응용 프로그램은 `asset_id`를 내부 key로 저장하고, 사용자가 보는 이름이나 태그 매핑은 별도 컬럼으로 관리할 수 있다.

RDB 테이블을 작업 큐나 명령 상태 저장소로 사용할 때도 `AUTO_INCREMENT`가 유용하다.

```sql
CREATE RDB TABLE command_queue (
    command_id LONG PRIMARY KEY AUTO_INCREMENT,
    asset_id LONG,
    command_type VARCHAR(32),
    payload JSON,
    status VARCHAR(16),
    created_at DATETIME
);

INSERT INTO command_queue(asset_id, command_type, payload, status, created_at)
VALUES (
    1,
    'SET_THRESHOLD',
    '{"temperature": 85}',
    'READY',
    TO_DATE('2026-07-10 09:00:00')
);

INSERT INTO command_queue(asset_id, command_type, payload, status, created_at)
VALUES (
    2,
    'RESTART_SENSOR',
    '{"reason": "manual"}',
    'READY',
    TO_DATE('2026-07-10 09:05:00')
);

SELECT command_id, asset_id, command_type, status
FROM command_queue
WHERE status = 'READY'
ORDER BY command_id;
```

## Catalog 확인과 DDL 변경

`AUTO_INCREMENT` 여부는 `M$SYS_COLUMNS.FLAG`의 `1048576` bit로 확인할 수 있다.

```sql
SELECT C.NAME,
       BITAND(C.FLAG, 1048576) AS AUTO_INCREMENT_FLAG
FROM M$SYS_COLUMNS C, M$SYS_TABLES T
WHERE C.TABLE_ID = T.ID
  AND T.NAME = 'DEVICE_MASTER'
ORDER BY C.ID;
```

`AUTO_INCREMENT_FLAG`가 `1048576`이면 해당 컬럼이 `AUTO_INCREMENT` 컬럼이다.

JDBC `DatabaseMetaData.getColumns()`는 이 flag를 기준으로 `IS_AUTOINCREMENT`를 `YES`로 반환한다. ODBC descriptor의 `SQL_DESC_AUTO_UNIQUE_VALUE`는 현재 지원 범위에 포함되지 않는다. ODBC 응용 프로그램은 catalog query를 사용해 확인한다.

`AUTO_INCREMENT` 속성은 system catalog에 저장되므로 정상 shutdown/startup 후에도 유지된다. RDB `ALTER TABLE ... DROP COLUMN` 과정에서 sidecar table이 rebuild되어도 `AUTO_INCREMENT` 속성과 다음 자동값은 유지된다.

```sql
CREATE RDB TABLE maintenance_ticket (
    ticket_id LONG PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(120),
    obsolete_note VARCHAR(120)
);

INSERT INTO maintenance_ticket(title, obsolete_note)
VALUES ('replace pressure sensor', 'temporary');

ALTER TABLE maintenance_ticket DROP COLUMN (obsolete_note);

INSERT INTO maintenance_ticket(title)
VALUES ('inspect valve');

SELECT ticket_id, title
FROM maintenance_ticket
ORDER BY ticket_id;
```

## SQLAppendBatch 사용 시 주의 사항

`SQLAppendBatch`는 SQL 컬럼 목록처럼 특정 컬럼을 생략하는 표현이 없다. 따라서 append API에서 자동값을 생성하려면 auto 컬럼을 포함하고, 값은 `SQL_APPEND_LONG_NULL` sentinel로 전달한다.

지원되는 입력 방식은 다음과 같다.

| 항목 | 값 |
| --- | --- |
| append type | `SQL_APPEND_TYPE_INT64` |
| append value | `SQL_APPEND_LONG_NULL` |

개념 예시는 다음과 같다.

```c
/*
 * table schema:
 * CREATE RDB TABLE append_device (
 *     id LONG PRIMARY KEY AUTO_INCREMENT,
 *     name VARCHAR(32)
 * );
 */

/* id column */
append_types[0] = SQL_APPEND_TYPE_INT64;
append_values[0].mLong = SQL_APPEND_LONG_NULL;

/* name column */
append_types[1] = SQL_APPEND_TYPE_VARCHAR;
append_values[1].mVar.mLength = strlen("append-device-01");
append_values[1].mVar.mData = "append-device-01";

/* SQLAppendBatch(...) 실행 */
```

`SQL_APPEND_TYPE_NULL`은 지원하지 않는다. RDB append 경로는 append type metadata와 테이블 컬럼 타입을 먼저 비교하므로, auto 컬럼이라도 append type이 `NULL`이면 column type mismatch로 처리된다.

## 지원하지 않는 예

다음 DDL은 지원되지 않는다.

```sql
-- INTEGER는 AUTO_INCREMENT 지원 타입이 아닙니다.
CREATE RDB TABLE bad_integer (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(32)
);

-- PRIMARY KEY가 아니므로 지원되지 않습니다.
CREATE RDB TABLE bad_no_pk (
    id LONG AUTO_INCREMENT,
    name VARCHAR(32)
);

-- table-level primary key와 결합한 AUTO_INCREMENT는 지원하지 않습니다.
CREATE RDB TABLE bad_table_pk (
    id LONG AUTO_INCREMENT,
    name VARCHAR(32),
    PRIMARY KEY(id)
);

-- RDB table이 아니므로 지원되지 않습니다.
CREATE TABLE bad_log_table (
    id LONG PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(32)
);

-- lookup sequence 속성과 혼용하지 않습니다.
CREATE RDB TABLE bad_sequence_mix (
    id LONG PROPERTY(SEQUENCE=1) PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(32)
);
```

## 운영 권장 사항

- `AUTO_INCREMENT` 값은 내부 식별자 용도로 사용한다.
- 업무상 빠짐없는 연속 번호가 필요하면 별도 채번 정책을 사용한다.
- 외부 시스템 key가 있는 경우 `AUTO_INCREMENT` ID와 외부 key를 별도 컬럼으로 함께 보관한다.
- 대량 이관 시에는 staging table에 먼저 적재한 뒤 `INSERT ... SELECT`로 최종 테이블에 넣는 방식을 사용한다.
- append API를 사용하는 경우 auto 컬럼을 생략하지 말고 `SQL_APPEND_TYPE_INT64`와 `SQL_APPEND_LONG_NULL` 조합을 사용한다.
