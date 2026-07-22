---
type: docs
title: '4.1 스키마 객체 정의'
weight: 10
toc: true
---
스키마 객체(테이블, 인덱스, 뷰)의 생성·변경·삭제 방법을 다룹니다.

- **[테이블 생성과 삭제](/dbms/data-modeling-table-design/schema-objects-definition/#create-delete)**
- **[테이블 변경](/dbms/data-modeling-table-design/schema-objects-definition/#alter)**
- **[컬럼과 데이터 타입 선택](/dbms/data-modeling-table-design/schema-objects-definition/#selection-type-column-data-types)**
- **[제약 조건과 기본값](/dbms/data-modeling-table-design/schema-objects-definition/#constraints-defaults-condition)**
- **[LOOKUP SEQUENCE 컬럼 정의](/dbms/lookup-table-usage/sequence-column/#definition-column-lookup-sequence)**
- **[LOOKUP JSON 컬럼과 조회](/dbms/lookup-table-usage/json-column-query/#condition-query-lookup-json)**: LOOKUP 테이블의 JSON 컬럼 지원 범위와 조회 제약
- **[인덱스 생성과 삭제](/dbms/data-modeling-table-design/schema-objects-definition/#index-create-delete)**
- **[VIEW 생성과 관리](/dbms/data-modeling-table-design/schema-objects-definition/#create-view)**


<a id="create-delete"></a>

## 테이블 생성과 삭제

### CREATE TABLE

#### LOG 테이블

```sql
CREATE LOG TABLE log_name (
    col1  TYPE1,
    col2  TYPE2,
    ...
);
```

LOG 테이블은 `CREATE LOG TABLE`을 사용합니다. `_arrival_time` 컬럼이 자동으로 추가됩니다.

```sql
-- 예시: 웹 액세스 로그
CREATE LOG TABLE web_access (
    method   VARCHAR(8),
    uri      VARCHAR(1024),
    status   SHORT,
    src_ip   IPV4,
    bytes    INTEGER
);
```

#### TAG 테이블

```sql
CREATE TAG TABLE tag_name (
    name  VARCHAR(n)  PRIMARY KEY,
    time  DATETIME    BASETIME,
    value DOUBLE
) [METADATA (meta_col TYPE, ...)]
  [TAG_PARTITION_COUNT = n]
  [TAG_DATA_PART_SIZE  = n];
```

거리축 TAG 테이블은 `BASETIME` 대신 `BASEDISTANCE`를 사용합니다.

```sql
-- 시간축
CREATE TAG TABLE sensor_data (
    name  VARCHAR(64) PRIMARY KEY,
    time  DATETIME    BASETIME,
    value DOUBLE      SUMMARIZED
);

-- 거리축
CREATE TAG TABLE pipeline_data (
    name      VARCHAR(32) PRIMARY KEY,
    distance  DOUBLE      BASEDISTANCE,
    thickness DOUBLE
);
```

#### TRANSACTION 테이블

테이블 유형을 생략한 `CREATE TABLE`, 전체 이름을 명시한 `CREATE TRANSACTION TABLE`, 축약형
`CREATE TXN TABLE`은 모두 TRANSACTION 테이블을 생성합니다.

```sql
CREATE TRANSACTION TABLE table_name (
    col1  TYPE1,
    col2  TYPE2,
    ...
);
```

```sql
CREATE TRANSACTION TABLE orders (
    order_id LONG,
    customer VARCHAR(64),
    amount   DOUBLE,
    status   VARCHAR(16)
);
```

LOG 테이블은 반드시 `CREATE LOG TABLE`로 유형을 명시합니다. 이전 공개 유형 이름인 `RDB`와
`TRX`는 지원하지 않습니다.

#### VOLATILE 테이블

```sql
CREATE VOLATILE TABLE table_name (
    pk_col  TYPE  PRIMARY KEY,  -- PK 기반 동작이 필요할 때 지정
    col2    TYPE,
    ...
);
```

#### LOOKUP 테이블

```sql
CREATE LOOKUP TABLE table_name (
    pk_col  TYPE  PRIMARY KEY,
    col2    TYPE,
    ...
);
```

#### IF NOT EXISTS

동일한 이름의 테이블이 이미 존재해도 오류가 발생하지 않습니다.

```sql
CREATE LOG TABLE IF NOT EXISTS web_access (...);
```

### DROP TABLE

```sql
DROP TABLE table_name;
```

테이블을 조회 중인 세션이 있으면 오류가 발생합니다. 조회를 종료한 후 삭제합니다.

```sql
DROP TABLE orders;
```

### 테이블 이름 규칙

- 영문자·숫자·언더스코어(`_`) 조합
- 대소문자 구분 없음 (내부 저장 시 대문자 변환)
- 특수문자 사용 시 큰따옴표(`"`)로 감쌉니다

```sql
CREATE LOG TABLE "my-table" (id INTEGER);
```

<a id="alter"></a>

## 테이블 변경

`ALTER TABLE` 문으로 컬럼을 추가하거나 속성을 변경합니다. 지원 범위는 테이블 타입에 따라 다릅니다.

### 테이블 타입별 지원 범위

| 작업 | LOG | TAG | TRANSACTION | VOLATILE | LOOKUP |
|------|-----|-----|-----|----------|--------|
| ADD COLUMN | O | O (METADATA만) | O | O | O |
| DROP COLUMN | O | O (METADATA만) | O | O | O |
| RENAME COLUMN | X | O (일반 컬럼) | O | X | X |
| MODIFY COLUMN | O | O (일반 컬럼) | X | X | X |
| RENAME TABLE | X | X | O | X | X |
| ADD RETENTION | O | O | X | X | X |
| DROP RETENTION | O | O | X | X | X |

KV 테이블도 `ADD RETENTION`과 `DROP RETENTION`을 지원합니다.

### ADD COLUMN

```sql
ALTER TABLE table_name ADD COLUMN (column_name type [DEFAULT value]);
```

```sql
-- LOG 테이블에 컬럼 추가
ALTER TABLE web_access ADD COLUMN (region VARCHAR(32));
ALTER TABLE web_access ADD COLUMN (resp_time DOUBLE);

-- LOOKUP 테이블에 컬럼 추가
ALTER TABLE country_code ADD COLUMN (capital VARCHAR(64));

-- TRANSACTION 테이블에 컬럼 추가
ALTER TABLE orders ADD COLUMN (note VARCHAR(256));

-- TAG 테이블 METADATA에 컬럼 추가
ALTER TABLE sensor_data METADATA ADD COLUMN (unit VARCHAR(16));
```

### DROP COLUMN

```sql
ALTER TABLE table_name DROP COLUMN (column_name);
```

```sql
ALTER TABLE web_access DROP COLUMN (region);

-- TAG 테이블 METADATA 컬럼 삭제
ALTER TABLE sensor_data METADATA DROP COLUMN (unit);
```

### RENAME COLUMN

TAG 일반 컬럼과 TRANSACTION 테이블에서만 지원됩니다. LOG, VOLATILE, LOOKUP 테이블은 지원하지 않습니다.

```sql
ALTER TABLE table_name RENAME COLUMN old_name TO new_name;
```

```sql
-- TAG 테이블 일반 컬럼 이름 변경
ALTER TABLE sensor_data RENAME COLUMN value TO temperature;

-- TRANSACTION 테이블 컬럼 이름 변경
ALTER TABLE orders RENAME COLUMN note TO memo;
```

### MODIFY COLUMN

LOG 테이블과 TAG 테이블의 일반 컬럼에서 지원됩니다. TRANSACTION, VOLATILE, LOOKUP 테이블은 지원하지 않습니다.

```sql
-- VARCHAR 크기 확장 (줄이기는 불가)
ALTER TABLE web_access MODIFY COLUMN (uri VARCHAR(2048));

-- NOT NULL 제약 추가 (LOG 테이블)
ALTER TABLE web_access MODIFY COLUMN status NOT NULL;

-- MINMAX_CACHE_SIZE 변경 (LOG 테이블 컬럼)
ALTER TABLE web_access MODIFY COLUMN status SET MINMAX_CACHE_SIZE = 20480;
```

### RENAME TABLE

TRANSACTION 테이블에서만 지원됩니다.

```sql
ALTER TABLE old_name RENAME TO new_name;
```

```sql
-- TRANSACTION 테이블 이름 변경
ALTER TABLE orders RENAME TO order_history;
```

### 주의사항

- LOG 테이블에 추가된 컬럼은 기존 레코드에서 NULL로 읽힙니다.
- TAG 테이블의 일반 데이터 컬럼(PRIMARY KEY, BASETIME)은 변경할 수 없습니다.
- VOLATILE 테이블 변경 사항은 서버 재시작 후 초기화 스크립트로 재적용해야 합니다.

<a id="selection-type-column-data-types"></a>

## 컬럼과 데이터 타입 선택

사용 가능한 컬럼 데이터 타입은 다음과 같습니다.

### 데이터 타입 전체 목록

| 타입 이름 | 설명 | 값 범위 | NULL 값 |
|-----------|------|---------|---------|
| `SHORT` | 16비트 부호 있는 정수 | -32767 ~ 32767 | -32768 |
| `USHORT` | 16비트 부호 없는 정수 | 0 ~ 65534 | 65535 |
| `INTEGER` | 32비트 부호 있는 정수 | -2147483647 ~ 2147483647 | -2147483648 |
| `UINTEGER` | 32비트 부호 없는 정수 | 0 ~ 4294967294 | 4294967295 |
| `LONG` | 64비트 부호 있는 정수 | -9223372036854775807 ~ 9223372036854775807 | -9223372036854775808 |
| `ULONG` | 64비트 부호 없는 정수 | 0 ~ 18446744073709551614 | 18446744073709551615 |
| `FLOAT` | 32비트 부동 소수점 | — | 양수 최대값 |
| `DOUBLE` | 64비트 부동 소수점 | — | 양수 최대값 |
| `DECIMAL(M,D)` | exact 고정소수점 | M: 1~65, D: 0~30 | — |
| `DATETIME` | 날짜·시간 (나노초) | 1970-01-01 00:00:00.000:000:000 ~ 2262-04-11 23:47:16.854:775:807 | — |
| `VARCHAR(n)` | 가변 길이 문자열 (UTF-8) | 길이 1 ~ 32768 (32K) | — |
| `IPV4` | IPv4 주소 (4바이트) | "0.0.0.0" ~ "255.255.255.255" | — |
| `IPV6` | IPv6 주소 (16바이트) | "0000:...:0000" ~ "FFFF:...:FFFF" | — |
| `TEXT` | 긴 텍스트 (키워드 인덱스 가능) | 길이 0 ~ 64MB | — |
| `BINARY` | 이진 데이터 | LOG: 0 ~ 64MB / TAG: 1 ~ 32767바이트 | — |
| `JSON` | JSON 문서 | 데이터 최대 32K / 경로 최대 512바이트 | — |

### 숫자형

| 타입 | 크기 | 범위 | 용도 |
|------|------|------|------|
| `SHORT` | 2바이트 | -32,767 ~ 32,767 | 상태 코드, 플래그, 포트 번호 |
| `USHORT` | 2바이트 | 0 ~ 65,534 | 부호 없는 16비트 정수 |
| `INTEGER` (`INT`) | 4바이트 | -2,147,483,647 ~ 2,147,483,647 | 일반 정수값 |
| `UINTEGER` | 4바이트 | 0 ~ 4,294,967,294 | 부호 없는 32비트 정수 |
| `LONG` | 8바이트 | -9,223,372,036,854,775,807 ~ 9,223,372,036,854,775,807 | 대용량 카운터, ID |
| `ULONG` | 8바이트 | 0 ~ 18,446,744,073,709,551,614 | 부호 없는 64비트 정수 |
| `FLOAT` | 4바이트 | 7자리 정밀도 | 저정밀도 실수 |
| `DOUBLE` | 8바이트 | 15자리 정밀도 | 근삿값 계측 데이터 |
| `DECIMAL(M,D)` | precision에 따라 가변 | 최대 65자리, scale 최대 30자리 | 금액, 세율, 정산값 |

각 부호 있는 정수 타입(`SHORT`, `INTEGER`, `LONG`)은 C 언어의 해당 정수형과 동일하며, 최소 음수 값을 NULL로 인식합니다. 부동 소수점 타입(`FLOAT`, `DOUBLE`)은 양수 최대값을 NULL로 인식합니다. `SHORT`는 `int16`, `INTEGER`는 `int32` 또는 `int`, `LONG`은 `int64`로도 표시됩니다.

`DECIMAL`은 exact fixed-point 타입입니다. `NUMERIC`, `DEC`, `FIXED`, `NUMBER`는 alias이며
표준 표시명은 `DECIMAL`입니다. 자세한 선언과 연산 규칙은 [DECIMAL과 NUMERIC 고정소수점
타입](/dbms/reference/sql/type-data-types-dictionary/decimal-numeric-fixed-point/)을 참고하십시오.

### 문자형

| 타입 | 최대 크기 | 용도 |
|------|---------|------|
| `VARCHAR(n)` | 32,767바이트 | 일반 문자열, 태그 이름, 코드 |
| `TEXT` | 64MB | 전문 검색(SEARCH) 대상 긴 텍스트 |

`VARCHAR`는 실제 저장 데이터 크기만큼만 공간을 사용합니다. 길이 기준은 바이트 단위이므로 UTF-8 멀티바이트 문자에서는 실제 문자 수와 다를 수 있습니다. `TEXT`는 키워드 인덱스를 통해 검색할 수 있으며, 대용량 텍스트를 별도 컬럼으로 저장·검색하는 데 쓰입니다.

### 날짜·시간

| 타입 | 크기 | 용도 |
|------|------|------|
| `DATETIME` | 8바이트 | 나노초 정밀도 날짜·시각 |

`DATETIME`은 1970년 1월 1일 자정 이후 경과 시간을 나노초 단위로 저장합니다.

```sql
CREATE VOLATILE TABLE t1 (
    ts DATETIME
);

-- 문자열로 삽입
INSERT INTO t1 VALUES ('2024-01-01 12:00:00');
INSERT INTO t1 VALUES ('2024-01-01 12:00:00 123:456:789');  -- 나노초

-- NOW 함수
INSERT INTO t1 VALUES (NOW);
```

### 네트워크 주소

| 타입 | 크기 | 용도 |
|------|------|------|
| `IPV4` | 4바이트 | IPv4 주소 (`'192.168.1.1'`) |
| `IPV6` | 16바이트 | IPv6 주소 (`'2001:db8::1'`) |

문자열 비교 대비 저장 효율이 높고 범위 비교가 빠릅니다. IPv6는 `:` 기호를 사용하는 축약 표기도 지원합니다 (예: `"::FFFF:1232"`, `"::FFFF:192.168.0.3"`).

### 이진·JSON

| 타입 | 최대 크기 | 용도 |
|------|---------|------|
| `BINARY` | LOG: 64MB / TAG: 32767바이트 | 파형, 이미지 등 이진 데이터 |
| `JSON` | 32KB | JSON 문서 |

#### BINARY 타입: LOG vs TAG 차이

- **LOG 테이블**: 이미지나 문서 같은 비정형 데이터를 저장하는 일반 타입으로, 최대 64MB까지 저장할 수 있습니다.
- **TAG 테이블**: `BINARY(n)` 형태의 고정 길이 변형으로, 유효 길이는 1 ~ 32767바이트입니다. SQL에서 `X'...'`, `B'...'`, `O'...'` binary literal을 쓸 수 있으며(소문자 prefix도 지원), 기존 호환성을 위해 `'0x...'` 형태의 문자열 입력도 가능합니다. 선언된 길이를 초과하면 오류가 발생합니다.
- **LOOKUP / VOLATILE 테이블**: `BINARY` 컬럼을 허용하지 않습니다.

자세한 입력 형식은 [Binary 컬럼](/dbms/tag-table-usage/table-structure-schema/#original-85-binary-columns)을 참고하십시오.

### SQL DataType 매핑

다음 표는 데이터 타입별 SQL 타입과 C 타입 매핑입니다.

| Machbase 타입 | Machbase CLI 타입 | SQL 타입 | C 타입 | C 기본 타입 |
|--------------|------------------|---------|--------|------------|
| `short` | SQL_SMALLINT | SQL_SMALLINT | SQL_C_SSHORT | int16_t (short) |
| `ushort` | SQL_USMALLINT | SQL_SMALLINT | SQL_C_USHORT | uint16_t (unsigned short) |
| `integer` | SQL_INTEGER | SQL_INTEGER | SQL_C_SLONG | int32_t (int) |
| `uinteger` | SQL_UINTEGER | SQL_INTEGER | SQL_C_ULONG | uint32_t (unsigned int) |
| `long` | SQL_BIGINT | SQL_BIGINT | SQL_C_SBIGINT | int64_t (long long) |
| `ulong` | SQL_UBIGINT | SQL_BIGINT | SQL_C_UBIGINT | uint64_t (unsigned long long) |
| `float` | SQL_FLOAT | SQL_REAL | SQL_C_FLOAT | float |
| `double` | SQL_DOUBLE | SQL_FLOAT, SQL_DOUBLE | SQL_C_DOUBLE | double |
| `decimal` | SQL_DECIMAL | SQL_DECIMAL / SQL_NUMERIC | SQL_C_NUMERIC | decimal-preserving value |
| `datetime` | SQL_TIMESTAMP / SQL_TIME | SQL_TYPE_TIMESTAMP / SQL_BIGINT / SQL_TYPE_TIME | SQL_C_TYPE_TIMESTAMP / SQL_C_UBIGINT / SQL_C_TIME | char * (YYYY-MM-DD HH24:MI:SS) / int64_t (나노초) / struct tm |
| `varchar` | SQL_VARCHAR | SQL_VARCHAR | SQL_C_CHAR | char * |
| `ipv4` | SQL_IPV4 | SQL_VARCHAR | SQL_C_CHAR | char * (IP 문자열) / unsigned char[4] |
| `ipv6` | SQL_IPV6 | SQL_VARCHAR | SQL_C_CHAR | char * (IP 문자열) / unsigned char[16] |
| `text` | SQL_TEXT | SQL_LONGVARCHAR | SQL_C_CHAR | char * |
| `binary` | SQL_BINARY | SQL_BINARY | SQL_C_BINARY | char * |
| `json` | SQL_JSON | SQL_JSON | SQL_C_CHAR | json_t |

### 사전 정의 시스템 컬럼

사용자가 직접 정의하지 않아도 내부적으로 관리되는 시스템 컬럼이 있습니다.

#### _ARRIVAL_TIME

LOG 테이블의 모든 행에 자동으로 부여되는 수신 시각 컬럼입니다.

- 타입: `DATETIME` (나노초 정밀도)
- INSERT 시 명시하지 않으면 실행 시점의 서버 시각이 자동 부여됩니다.
- `_ARRIVAL_TIME`을 명시하여 삽입할 경우, 지정값이 테이블에 이미 존재하는 가장 최신 `_ARRIVAL_TIME`보다 이전이면 해당 행은 입력되지 않습니다.
- SELECT 쿼리에서 명시적으로 조회하거나 WHERE 조건에 사용할 수 있습니다.

```sql
-- 명시적 삽입
INSERT INTO sensor_log (_arrival_time, sensor_id, value)
VALUES ('2024-01-01 12:00:00', 'TEMP-01', 25.3);

-- 조회
SELECT _arrival_time, sensor_id, value FROM sensor_log;
```

#### _RID

각 행에 고유하게 부여되는 내부 행 식별자(Row ID)입니다.

- 타입: `LONG` (자동 증가)
- SELECT 시 명시적으로 조회할 수 있습니다.
- WHERE 조건에서 특정 행을 지정하는 데 사용할 수 있습니다.

```sql
SELECT _rid, sensor_id, value FROM sensor_log WHERE _rid = 1000;
```

### 타입 선택 지침

| 데이터 | 권장 타입 |
|--------|---------|
| 온도, 전압, 유량 등 센서값 | `DOUBLE` |
| 금액, 세율, 정산값 | `DECIMAL(M,D)` |
| IP 주소 | `IPV4` / `IPV6` |
| 포트 번호 (0~65535) | `USHORT` |
| 상태 코드, 플래그 | `SHORT` 또는 `INTEGER` |
| 태그/센서 이름 | `VARCHAR(64~256)` |
| 긴 설명 텍스트 | `TEXT` |
| 날짜·시각 | `DATETIME` |
| 큰 정수 ID, 누적값 | `LONG` |

### 테이블 타입별 타입 제약

| 컬럼 역할 | 제약 |
|---------|------|
| TAG PRIMARY KEY | `VARCHAR(n)` 필수 |
| TAG BASETIME | `DATETIME` 필수 |
| TAG BASEDISTANCE | `DOUBLE` |
| LOOKUP/VOLATILE PRIMARY KEY | 해당 테이블에서 허용되는 일반 스칼라 타입 |
| LOOKUP SEQUENCE | `LONG` 필수 |

<a id="constraints-defaults-condition"></a>

## 제약 조건과 기본값

테이블에서 사용할 수 있는 컬럼 제약 조건과 기본값 설정입니다.

### PRIMARY KEY

VOLATILE, LOOKUP, TRANSACTION 테이블의 컬럼에 지정합니다. PRIMARY KEY로 지정된 컬럼은 값 중복을 허용하지 않습니다. LOOKUP/VOLATILE은 Red-Black Tree 인덱스를 사용하고, TRANSACTION 테이블은 BTREE 인덱스로 표시됩니다.

- **LOOKUP**: PRIMARY KEY 필수 (PK 없이 생성 불가)
- **VOLATILE**: PRIMARY KEY 선택적. 단, `INSERT ... ON DUPLICATE KEY UPDATE` 구문 사용 시 필수
- **TRANSACTION**: PRIMARY KEY 선택적

```sql
-- LOOKUP: PK 필수
CREATE LOOKUP TABLE alarm_threshold (
    sensor_id VARCHAR(40) PRIMARY KEY,
    high_limit DOUBLE,
    low_limit  DOUBLE
);

-- VOLATILE: PK 지정 시 UPSERT 가능
CREATE VOLATILE TABLE device_status (
    device_id VARCHAR(40) PRIMARY KEY,
    status    VARCHAR(20),
    value     DOUBLE,
    updated_at DATETIME
);

-- TRANSACTION: PK 선택 (지정 시 중복 불가)
CREATE TRANSACTION TABLE orders (
    order_id INTEGER PRIMARY KEY,
    product  VARCHAR(100),
    qty      INTEGER
);
```

### NOT NULL

LOG 테이블 컬럼에 사용합니다. 해당 컬럼에 NULL 삽입을 금지합니다.

```sql
CREATE LOG TABLE sensor_log (
    sensor_id VARCHAR(40) NOT NULL,
    ts        DATETIME,
    value     DOUBLE
);
```

TAG, VOLATILE, LOOKUP 테이블은 NOT NULL 제약을 별도로 선언하지 않아도 PK 컬럼에 자동으로 NOT NULL이 적용됩니다.

### DEFAULT

일반 `CREATE TABLE` 경로에서는 제한적으로 `DATETIME DEFAULT SYSDATE`를 사용할 수 있습니다.
TRANSACTION 테이블은 컬럼 생성 및 `ALTER TABLE ... ADD COLUMN`에서 DEFAULT를 사용할 수 있습니다.
그 외 기본값이 필요하면 INSERT 문이나 애플리케이션 입력 단계에서 값을 명시합니다.

```sql
CREATE TRANSACTION TABLE orders_default_example (
    order_id INTEGER,
    status   VARCHAR(20),
    discount DOUBLE,
    created_at DATETIME DEFAULT SYSDATE
);

INSERT INTO orders_default_example
    (order_id, status, discount)
VALUES
    (1, 'PENDING', 0.0);

ALTER TABLE orders_default_example ADD COLUMN (score INTEGER DEFAULT 7);
```

### 시스템 자동 생성 컬럼

LOG 테이블에는 `_ARRIVAL_TIME`과 `_RID` 시스템 컬럼이 자동으로 추가됩니다. TAG, VOLATILE,
LOOKUP 테이블에는 `_RID`이 내부 행 식별자로 추가됩니다. TRANSACTION 테이블에는 `_ARRIVAL_TIME`이
자동 추가되지 않습니다.

| 컬럼명 | 타입 | 설명 |
|--------|------|------|
| `_ARRIVAL_TIME` | DATETIME | LOG 레코드 삽입 시점의 시스템 시각. Retention과 보존형 DELETE 기준 |
| `_RID` | LONG | 비-TRANSACTION 테이블의 내부 행 식별자. 시스템이 자동 부여하며 사용자 변경 불가 |

```sql
-- _RID로 특정 레코드 검색
SELECT * FROM sensor_log WHERE _RID = 1234;

-- _ARRIVAL_TIME으로 최근 1시간 데이터 조회
SELECT * FROM sensor_log WHERE _ARRIVAL_TIME > NOW - 3600000000000;
```

### 테이블 타입별 제약 조건 지원 범위

| 제약 조건 | TAG | LOG | TRANSACTION | VOLATILE | LOOKUP |
|-----------|-----|-----|-----|---------|--------|
| PRIMARY KEY | O (name 컬럼) | X | O (선택) | O (선택) | O (필수) |
| NOT NULL | X | O | O | X | X |
| DEFAULT | X | 제한적 | O | 제한적 | 제한적 |
| UNIQUE | X | X | O (UNIQUE INDEX) | X | X |
| FOREIGN KEY | X | X | X | X | X |

> FOREIGN KEY 제약은 지원하지 않습니다. 참조 무결성은 애플리케이션 레이어에서 관리해야 합니다.

<a id="index-create-delete"></a>

## 인덱스 생성과 삭제

테이블 타입에 따라 지원되는 인덱스 종류가 다릅니다. 인덱스는 조회 성능을 높이기 위해 사용하며, 불필요한 인덱스는 INSERT 성능에 영향을 줍니다.

### 인덱스 종류

| 인덱스 유형 | 대상 테이블 | 특징 |
|------------|------------|------|
| LSM (Log-Structured Merge) | LOG | 시계열 대량 입력에 최적화된 LOG 컬럼 인덱스 |
| BITMAP | LOG | 카디널리티가 낮은 컬럼에 유효. 복합 조건 쿼리 성능 향상 |
| REDBLACK | LOOKUP, VOLATILE, TAG 메타데이터 | 정확한 값 검색에 최적화 |
| BTREE | TRANSACTION | PRIMARY KEY 및 보조 인덱스에 사용 |
| KEYWORD | LOG | TEXT 컬럼 전문 검색용 |
| TAG/KV | TAG | TAG 값 컬럼 조건 조회를 보조하는 secondary index |

### LOG 테이블 인덱스 생성

```sql
-- LSM 인덱스 (기본, 범위 검색에 유리)
CREATE INDEX idx_sensor_id ON sensor_log (sensor_id);

-- BITMAP 인덱스 (카디널리티 낮은 컬럼: 상태값, 등급 등)
CREATE BITMAP INDEX idx_status ON sensor_log (status);

-- KEYWORD 인덱스 (TEXT 컬럼 전문 검색)
CREATE KEYWORD INDEX idx_msg ON event_log (message);
```

> LOG/TAG/LOOKUP/VOLATILE 인덱스는 단일 컬럼 중심으로 설계합니다. TRANSACTION 테이블은 일반 복합
> 인덱스를 지원하지만, 복합 JSON path 인덱스와 복합 PRIMARY KEY 인덱스는 지원하지 않습니다.

### TAG 테이블 인덱스

TAG 테이블은 태그명과 시간 축에 대한 내부 인덱스를 자동으로 관리합니다. 추가로
METADATA 컬럼 인덱스와 값 컬럼 TAG/KV secondary index를 사용할 수 있습니다.

```sql
-- TAG 메타데이터 JSON 컬럼 인덱스
CREATE TAG TABLE tag (
    name VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
) METADATA (
    location VARCHAR(40),
    dept     VARCHAR(20)
);

-- 메타데이터 컬럼에 인덱스 생성
CREATE INDEX idx_location ON tag METADATA (location);

-- 값 컬럼 TAG/KV 인덱스 생성
CREATE INDEX idx_value ON tag (value) INDEX_TYPE TAG;
```

### LOOKUP/VOLATILE/TRANSACTION 테이블 인덱스

LOOKUP과 VOLATILE은 Red-Black Tree 인덱스를 사용합니다. TRANSACTION 테이블은 BTREE로 표시되는 PRIMARY
KEY 인덱스와 보조 인덱스를 사용합니다.

```sql
-- LOOKUP: PK 지정 시 REDBLACK 인덱스 자동 생성
CREATE LOOKUP TABLE alarm_threshold (
    sensor_id VARCHAR(40) PRIMARY KEY,
    high_limit DOUBLE
);
-- → sensor_id에 REDBLACK 인덱스 자동 생성됨

-- TRANSACTION: PK 지정 시 BTREE 인덱스로 표시
CREATE TRANSACTION TABLE orders (
    order_id INTEGER PRIMARY KEY,
    product  VARCHAR(100),
    status   VARCHAR(16)
);

-- TRANSACTION 보조 인덱스
CREATE INDEX idx_orders_product ON orders(product);

-- TRANSACTION 복합 보조 인덱스
CREATE INDEX idx_orders_product_status ON orders(product, status);
```

```sql
-- TRANSACTION PRIMARY KEY 인덱스 사후 생성
CREATE TRANSACTION TABLE order_work (
    order_id INTEGER,
    product  VARCHAR(100)
);

CREATE PRIMARY KEY INDEX pk_order_work ON order_work(order_id);
```

### 인덱스 삭제

```sql
DROP INDEX idx_sensor_id;
DROP INDEX idx_status;
DROP INDEX idx_msg;
```

PRIMARY KEY에 의해 자동 생성된 인덱스는 별도로 삭제할 수 없으며, 테이블 삭제 시 함께 제거됩니다.

### 인덱스 정보 조회

```sql
-- 인덱스 목록 조회
SHOW INDEXES;

-- 테이블/컬럼과 조합해 상세 조회
SELECT t.name AS table_name,
       c.name AS column_name,
       i.name AS index_name,
       i.type AS index_type
  FROM m$sys_indexes i,
       m$sys_index_columns ic,
       m$sys_tables t,
       m$sys_columns c
 WHERE i.id = ic.index_id
   AND i.table_id = t.id
   AND ic.table_id = c.table_id
   AND ic.col_id = c.id
   AND t.name = 'SENSOR_LOG';
```

### 인덱스 설계 원칙

- **LOG 테이블**: 쿼리 빈도가 높은 컬럼에만 선별적으로 생성. 상태값·등급 등 저카디널리티 컬럼은 BITMAP 고려
- **TAG 테이블**: 태그명·시간 조건을 기본으로 사용하고, 메타데이터 필터나 값 조건이 잦은 경우 해당 인덱스 추가
- **LOOKUP/TRANSACTION**: PK 인덱스와 필요한 보조 인덱스 사용. TRANSACTION 테이블은 복합 보조 인덱스도 가능
- **VOLATILE**: PK 인덱스 중심으로 설계
- **과도한 인덱스**: 대량 INSERT 성능 저하의 원인이 되므로 반드시 필요한 경우에만 생성

<a id="create-view"></a>

## VIEW 생성과 관리

VIEW는 하나 이상의 테이블에 대한 SELECT 쿼리를 저장해 두고 테이블처럼 조회할 수 있게 하는 논리적 객체입니다.

### VIEW 생성

```sql
CREATE VIEW view_name AS
    SELECT ...;
```

#### 예시

```sql
-- 최근 1시간 이상 알람 상태인 센서 뷰
CREATE VIEW active_alarms AS
    SELECT sensor_id, value, status
    FROM device_status
    WHERE status = 'ALARM';

-- TAG 테이블과 LOOKUP 테이블 조인 뷰
CREATE VIEW enriched_sensor_data AS
    SELECT t.name, t.time, t.value, m.location, m.dept
    FROM tag t
    LEFT JOIN device_meta m ON t.name = m.sensor_id;

-- 집계 뷰
CREATE VIEW hourly_avg AS
    SELECT name,
           DATE_TRUNC('hour', time) AS hour,
           AVG(value) AS avg_value
    FROM tag
    GROUP BY name, DATE_TRUNC('hour', time);
```

### VIEW 조회

VIEW는 일반 테이블처럼 SELECT 문에서 사용합니다.

```sql
SELECT * FROM active_alarms WHERE sensor_id = 'TEMP-01';

SELECT location, AVG(avg_value)
FROM hourly_avg
WHERE hour > NOW - 86400000000000
GROUP BY location;
```

### VIEW 삭제

```sql
DROP VIEW active_alarms;
DROP VIEW enriched_sensor_data;
```

### VIEW 목록 조회

```sql
SELECT * FROM M$SYS_VIEWS;
```

### VIEW 정의 확인

```sql
SELECT VIEW_NAME, VIEW_TEXT
FROM M$SYS_VIEWS
WHERE VIEW_NAME = 'ACTIVE_ALARMS';
```

### VIEW 특성과 제한

- VIEW는 데이터를 물리적으로 저장하지 않습니다. 조회할 때마다 정의된 쿼리를 실행합니다.
- VIEW에 대한 INSERT/UPDATE/DELETE는 지원하지 않습니다. 읽기 전용입니다.
- VIEW는 다른 VIEW를 참조할 수 있습니다 (중첩 VIEW).
- TAG, LOG, TRANSACTION, VOLATILE, LOOKUP 테이블 모두 VIEW 정의에 포함할 수 있습니다.

### 활용 패턴

```sql
-- 보안: 일부 컬럼만 노출하는 뷰
CREATE VIEW sensor_public AS
    SELECT sensor_id, time, value FROM sensor_log;
    -- value_raw, internal_code 등은 노출 안 함

-- 복잡한 JOIN을 단순화하는 뷰
CREATE VIEW asset_status AS
    SELECT a.asset_id, a.name, s.status, s.last_seen
    FROM assets a
    LEFT JOIN device_status s ON a.device_id = s.device_id;

-- 쿼리 재사용: 자주 쓰는 필터를 뷰로 저장
CREATE VIEW critical_sensors AS
    SELECT * FROM alarm_threshold WHERE high_limit < 50.0;
```
