---
type: docs
title: '18.1.1.11 DDL'
weight: 110
toc: true
---

DDL(Data Definition Language)은 테이블, 인덱스, 뷰, 롤업 등 데이터베이스 객체를 생성·수정·삭제하는 구문입니다.

> **권한**: 일반 사용자가 active database에서 DDL을 실행하려면 `GRANT DDL ON DATABASE database_name TO user_name;` 또는 `GRANT CREATE ON DATABASE database_name TO user_name;`이 필요합니다. 자세한 내용은 [GRANT/REVOKE](../user-auth-syntax/#grant-revoke)를 참고하십시오.

## CREATE TABLE

```sql
create_table_stmt ::=
    'CREATE' table_type? 'TABLE' ['IF NOT EXISTS'] table_name
    '(' column_def ( ',' column_def )* ')'
    [ 'METADATA' '(' column_def ( ',' column_def )* ')' ]
    [ table_property_list ]
    [ 'TABLESPACE' tablespace_name ]
    [ 'WITH ROLLUP' rollup_interval_spec ]

table_type ::= 'LOG' | 'TAG' | 'VOLATILE' | 'LOOKUP' | 'TRANSACTION' | 'TXN'
-- table_type을 생략하면 TRANSACTION 테이블이 생성됩니다.

column_def ::= column_name column_type
               [ 'PRIMARY KEY' ]
               [ 'NOT NULL' ]
               [ column_axis ]
               [ 'SUMMARIZED' ]
               [ 'DEFAULT' value ]
               [ 'PROPERTY' '(' column_property_list ')' ]

decimal_type ::= ( 'DECIMAL' | 'NUMERIC' | 'DEC' | 'FIXED' | 'NUMBER' )
                 [ '(' precision [ ',' scale ] ')' ]

column_axis ::= 'BASETIME' | 'BASE TIME' | 'BASE DISTANCE' | 'BASEDISTANCE'

column_property_list ::=
    ( 'MINMAX_CACHE_SIZE' '=' number
    | 'PART_PAGE_COUNT'   '=' number
    | 'PAGE_VALUE_COUNT'  '=' number
    | 'MAX_CACHE_PART_COUNT' '=' number
    | 'SEQUENCE' '=' number )
    ( ',' column_property_list )*

table_property_list ::=
    ( 'TAG_PARTITION_COUNT'           '=' number
    | 'TAG_DATA_PART_SIZE'            '=' number
    | 'TAG_STAT_ENABLE'               '=' ( '0' | '1' )
    | 'TAG_DUPLICATE_CHECK_DURATION'  '=' number
    | 'VARCHAR_FIXED_LENGTH_MAX'      '=' number )
    ( ',' table_property_list )*
```

### 테이블 유형

| 키워드 | 설명 |
|--------|------|
| (없음) | **TRANSACTION 테이블** - 관계형 데이터와 트랜잭션 지원 |
| `LOG` | **LOG 테이블** - 시계열 로그 데이터. 추가(INSERT) 중심, 일반 UPDATE 불가 |
| `TAG` | **TAG 테이블** - 태그 이름/시간/값 구조의 시계열 데이터. BASETIME 컬럼 필수 |
| `LOOKUP` | **LOOKUP 테이블** - 메모리 상주. PRIMARY KEY 필수. DML 전체 지원 |
| `VOLATILE` | **VOLATILE 테이블** - 메모리 상주. 서버 재시작 시 데이터 소멸. PRIMARY KEY 선택 |
| `TRANSACTION`, `TXN` | **TRANSACTION 테이블** - 전체 이름과 축약형은 같은 테이블을 생성 |

무수식 `CREATE TABLE`, `CREATE TRANSACTION TABLE`, `CREATE TXN TABLE`은 모두 TRANSACTION
테이블을 생성합니다. LOG 테이블을 만들 때는 `CREATE LOG TABLE`을 사용합니다. 이전 공개
명칭인 `RDB`와 `TRX`는 테이블 유형 별칭으로 지원하지 않습니다. TRANSACTION 테이블은 Standard
Edition 전용이므로 Cluster Edition에서는 세 TRANSACTION 생성 문법이 모두 거부됩니다.

`DECIMAL`은 모든 테이블 유형에서 사용할 수 있습니다. precision은 1~65, scale은 0~30이며
scale은 precision보다 클 수 없습니다. 자세한 내용은 [DECIMAL과 NUMERIC 고정소수점
타입](/dbms/reference/sql/type-data-types-dictionary/decimal-numeric-fixed-point/)을 참고하십시오.

### 예시

```sql
-- LOG 테이블 생성: LOG 키워드를 명시합니다.
CREATE LOG TABLE sensor_log (
    id      INTEGER,
    name    VARCHAR(64),
    value   DOUBLE,
    status  VARCHAR(20)
);

-- TAG 테이블 생성 (BASETIME 필수, SUMMARIZED는 롤업 대상 컬럼에 지정)
CREATE TAG TABLE tag (
    name  VARCHAR(40) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE SUMMARIZED
);

-- TAG 테이블 + 메타데이터 + 프로퍼티
CREATE TAG TABLE sensors (
    name     VARCHAR(40) PRIMARY KEY,
    time     DATETIME BASETIME,
    value    DOUBLE SUMMARIZED
) METADATA (
    location VARCHAR(100),
    unit     VARCHAR(20)
) TAG_PARTITION_COUNT = 4;

-- LOOKUP 테이블 (PRIMARY KEY 필수)
CREATE LOOKUP TABLE devices (
    device_id  VARCHAR(40) PRIMARY KEY,
    ip         IPV4,
    status     VARCHAR(20)
);

-- VOLATILE 테이블
CREATE VOLATILE TABLE cache_data (
    id    INTEGER PRIMARY KEY,
    value DOUBLE
);

-- TRANSACTION 테이블의 exact fixed-point 컬럼
CREATE TRANSACTION TABLE invoice (
    id      LONG PRIMARY KEY,
    amount  DECIMAL(18,2),
    tax     NUMERIC(18,4)
);

-- IF NOT EXISTS 사용
CREATE TAG TABLE IF NOT EXISTS tag (
    name  VARCHAR(40) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE SUMMARIZED
);

-- NOT NULL 제약 조건
CREATE TABLE t1 (
    c1 INTEGER NOT NULL,
    c2 VARCHAR(200)
);
```

### 사전 정의 시스템 컬럼

LOG/TAG 테이블 생성 시 두 개의 시스템 컬럼이 자동으로 추가됩니다.

| 컬럼 | 타입 | 설명 |
|------|------|------|
| `_ARRIVAL_TIME` | DATETIME | 레코드가 삽입된 시각. `DURATION` 조회 기준 |
| `_RID` | LONG | 레코드 고유 식별자. 사용자가 직접 지정 불가 |

---

## DROP TABLE

```sql
drop_table_stmt ::= 'DROP TABLE' table_name
```

지정한 테이블과 해당 테이블의 모든 데이터 및 인덱스를 삭제합니다. 다른 세션에서 해당 테이블을 조회 중이면 오류가 발생합니다.

```sql
DROP TABLE sensor_log;
```

---

## ALTER TABLE

`ALTER TABLE`은 테이블의 스키마를 변경합니다. 사용할 수 있는 하위 구문은 테이블 타입에 따라
다릅니다. TRANSACTION 테이블은 `ADD COLUMN`, `DROP COLUMN`, `RENAME COLUMN`, `RENAME TO`를
지원합니다. TAG 메타데이터 컬럼은 `METADATA ADD COLUMN`과 `METADATA DROP COLUMN`을
사용합니다.

### ADD COLUMN

```sql
alter_table_add_stmt ::=
    'ALTER TABLE' table_name 'ADD COLUMN'
    '(' column_name column_type [ 'DEFAULT' value ] ')'
```

```sql
-- 컬럼 추가
ALTER TABLE sensor_log ADD COLUMN (quality FLOAT);

-- TRANSACTION 컬럼 추가
ALTER TABLE product_master ADD COLUMN (stock_qty INTEGER DEFAULT 0);

-- 기본값과 함께 추가
ALTER TABLE sensor_log ADD COLUMN (flag INTEGER DEFAULT 0);
ALTER TABLE sensor_log ADD COLUMN (tag_ip IPV4 DEFAULT '192.168.0.1');
```

### DROP COLUMN

```sql
alter_table_drop_stmt ::=
    'ALTER TABLE' table_name 'DROP COLUMN' '(' column_name ')'
```

```sql
ALTER TABLE sensor_log DROP COLUMN (quality);
ALTER TABLE product_master DROP COLUMN (stock_qty);
```

### RENAME COLUMN

```sql
alter_table_column_rename_stmt ::=
    'ALTER TABLE' table_name 'RENAME COLUMN' old_column_name 'TO' new_column_name
```

```sql
ALTER TABLE sensor_log RENAME COLUMN status TO device_status;
ALTER TABLE product_master RENAME COLUMN name TO product_name;
```

### MODIFY COLUMN

```sql
alter_table_modify_stmt ::=
    'ALTER TABLE' table_name 'MODIFY COLUMN'
    ( '(' column_name 'VARCHAR' '(' new_size ')' ')'
    | column_name ( 'NOT NULL' | 'NULL' | 'SET' 'MINMAX_CACHE_SIZE' '=' value ) )
```

LOG·TAG 일반 컬럼에서 VARCHAR 컬럼의 길이를 늘리거나(줄이기 불가), NOT NULL 제약 조건을
추가·제거하거나, MINMAX_CACHE_SIZE를 변경합니다. TRANSACTION 테이블은 `MODIFY COLUMN`을
지원하지 않습니다.

```sql
-- VARCHAR 길이 확장 (줄이기 불가)
ALTER TABLE sensor_log MODIFY COLUMN (name VARCHAR(128));

-- NOT NULL 추가
ALTER TABLE sensor_log MODIFY COLUMN id NOT NULL;

-- NOT NULL 해제
ALTER TABLE sensor_log MODIFY COLUMN id NULL;

-- MINMAX_CACHE_SIZE 변경
ALTER TABLE sensor_log MODIFY COLUMN id SET MINMAX_CACHE_SIZE = 10240;
```

### RENAME TO

```sql
alter_table_rename_stmt ::=
    'ALTER TABLE' table_name 'RENAME TO' new_name
```

```sql
-- TRANSACTION 테이블에서 지원
ALTER TABLE product_master RENAME TO product_catalog;
```

### ADD / DROP RETENTION

Retention 연결과 해제 문법은 [RETENTION syntax](../retention-syntax/)를 참고하십시오.

---

## TRUNCATE TABLE

```sql
truncate_table_stmt ::= 'TRUNCATE TABLE' table_name
```

테이블의 모든 데이터를 삭제합니다. 다른 세션에서 해당 테이블을 조회 중이면 오류가 발생합니다.

```sql
TRUNCATE TABLE sensor_log;
```

---

## CREATE INDEX

인덱스 타입, 테이블별 지원 범위, JSON path와 속성은 [INDEX syntax](../index-syntax/)를
참고하십시오.

---

## DROP INDEX

삭제 문법과 제약은 [INDEX syntax](../index-syntax/#drop-index)를 참고하십시오.

---

## CREATE TABLESPACE

```sql
create_tablespace_stmt ::=
    'CREATE TABLESPACE' tablespace_name 'DATADISK' datadisk_list

datadisk_list ::= data_disk ( ',' data_disk )*

data_disk ::= disk_name
    '(' 'DISK_PATH' '=' '"' path '"'
        [ ',' 'PARALLEL_IO' '=' number ]
    ')'
```

```sql
-- 단일 디스크 테이블스페이스
CREATE TABLESPACE tbs1 DATADISK disk1 (DISK_PATH="tbs1_disk1");

-- 병렬 I/O 설정
CREATE TABLESPACE tbs2 DATADISK disk1 (DISK_PATH="tbs2_disk1", PARALLEL_IO = 5);

-- 다중 디스크
CREATE TABLESPACE tbs3
  DATADISK disk1 (DISK_PATH="tbs3_d1", PARALLEL_IO = 10),
           disk2 (DISK_PATH="tbs3_d2"),
           disk3 (DISK_PATH="tbs3_d3");
```

---

## DROP TABLESPACE

```sql
drop_tablespace_stmt ::= 'DROP TABLESPACE' tablespace_name
```

```sql
DROP TABLESPACE tbs1;
```

테이블스페이스에 생성된 객체가 있으면 삭제할 수 없습니다.

---

## CREATE ROLLUP

기본, 조건부, custom ROLLUP 문법은 [ROLLUP syntax](../rollup-syntax/)를 참고하십시오.

---

## DROP ROLLUP

삭제 문법은 [ROLLUP syntax](../rollup-syntax/#drop-rollup)를 참고하십시오.

---

## ALTER ROLLUP

시작, 중지, 강제 실행과 주기 변경은 [ROLLUP syntax](../rollup-syntax/#alter-rollup)를
참고하십시오.

---

## CREATE RETENTION

생성 문법과 테이블 연결은 [RETENTION syntax](../retention-syntax/)를 참고하십시오.

---

## DROP RETENTION

삭제 문법과 연결 해제 순서는 [RETENTION syntax](../retention-syntax/#drop-retention)를
참고하십시오.

---

## DDL 동시성과 잠금 {#ddl-concurrency}

Machbase 8.7.0 Standard Edition은 서로 독립적인 객체의 DDL을 객체 단위로 조정합니다. 따라서
같은 데이터베이스에서 서로 다른 이름의 LOG, TAG, VOLATILE, LOOKUP, TRANSACTION 테이블을
생성하거나 변경하는 DDL은 동시에 진행될 수 있습니다.

| Edition | 독립 객체의 DDL | 충돌 범위 | 충돌 시 대기 설정 |
|---------|-----------------|-----------|-------------------|
| Standard | 동시에 진행 가능 | 동일 객체와 직접 관련된 객체 | `DDL_LOCK_TIMEOUT` |
| Cluster | 기존 정책에 따라 직렬화 | 카탈로그 범위 | `DDL_LOCK_TIMEOUT`을 제공하지 않음 |

독립 객체의 DDL이 동시에 시작되더라도 메타데이터 처리나 스토리지 I/O 같은 공통 작업을 공유할
수 있습니다. 따라서 클라이언트 수에 비례한 처리량 향상이나 모든 DDL의 동시 완료를 보장하지는
않습니다.

### 충돌하는 객체

| 동시 실행 상황 | 동작 |
|----------------|------|
| 이름이 서로 다른 독립 테이블 | 테이블 유형과 관계없이 동시에 진행할 수 있음 |
| 동일 객체 또는 동일 이름의 객체 | 한 DDL만 진행하고 다른 DDL은 대기하거나 오류 반환 |
| 테이블 변경·삭제 DDL과 해당 테이블의 인덱스 DDL | 서로 관련된 객체로 처리 |
| 뷰 DDL과 뷰가 참조하는 테이블의 변경·삭제 DDL | 서로 관련된 객체로 처리 |
| TAG 테이블 변경·삭제 DDL과 해당 Rollup 또는 Retention DDL | 서로 관련된 객체로 처리 |
| `DROP VIEW`, `CREATE OR REPLACE VIEW`, 시스템 범위 DDL | 더 넓은 범위에서 직렬화될 수 있음 |

테이블 유형이 달라도 같은 테이블 이름은 하나의 이름 공간을 사용합니다. 예를 들어 같은 이름으로
LOG 테이블과 TAG 테이블을 동시에 생성하면 둘 중 하나만 생성됩니다.

### DDL 잠금 대기 시간

Standard Edition에서는 `DDL_LOCK_TIMEOUT`으로 충돌한 DDL 잠금을 기다릴 시간을 초 단위로
설정합니다.

| 값 | 동작 |
|---:|------|
| `0` | 기다리지 않고 즉시 `ERR-02031: Resource busy (<object>)` 반환 |
| 양수 | 지정한 시간까지 기다린 후 잠금을 얻지 못하면 `ERR-02031` 반환 |

오류 메시지의 괄호에는 대표 충돌 객체가 표시됩니다. 넓은 범위에서 충돌한 DDL은 객체 이름 대신
`DDL`로 표시될 수 있습니다.

기본값은 `0`이고 설정 범위는 `0`~`1000000`입니다. 현재 세션의 값을 변경하려면 다음 문을
실행합니다.

```sql
ALTER SESSION SET DDL_LOCK_TIMEOUT = 10;
```

하나의 DDL이 여러 잠금 단계를 거치더라도 대기 시간은 단계마다 다시 시작되지 않습니다. 잠금을
얻은 뒤에는 객체와 의존 관계를 다시 확인하므로, 선행 DDL의 결과에 따라 `already exists`,
`table not found` 같은 일반 SQL 오류가 반환될 수 있습니다.

`DDL_LOCK_TIMEOUT`은 DDL 잠금을 기다리는 시간만 제한하며 SQL 전체 실행 시간을 제한하지
않습니다. 실행 중인 DDL은 시작 시점의 값을 계속 사용하고, `ALTER SESSION`으로 변경한 값은
다음 DDL부터 적용됩니다. DDL의 커밋과 복구 동작은 이전 버전과 동일하며 암시적 커밋을 새로
수행하지 않습니다.

| 설정 | 단위 | 제한 대상 |
|------|------|-----------|
| `DDL_LOCK_TIMEOUT` | 초 | Standard Edition의 DDL 잠금 대기 |
| `SESSION_QUERY_TIMEOUT_SEC` / `QUERY_TIMEOUT` | 초 | 쿼리 실행 및 응답 대기 |
| `TRANSACTION_BUSY_TIMEOUT_MS` | 밀리초 | TRANSACTION 테이블의 동시 쓰기 충돌 대기 |

---

## 관련 문서

- [테이블 유형](/dbms/data-modeling-table-design/) - LOG, TAG, LOOKUP, VOLATILE, TRANSACTION 테이블 특성 및 사용 가이드
- [TAG 테이블 롤업](/dbms/tag-table-usage/create-alter-drop/#original-85-creating-tag-tables) - 롤업 생성 및 운영 가이드
- [GRANT/REVOKE](../user-auth-syntax/#grant-revoke) - DDL 실행에 필요한 권한 부여
- [ALTER SESSION](../system-session-alter-syntax/#alter-session) - 현재 세션의 DDL 잠금 대기 시간 설정
- [스키마 변경 체크리스트](/dbms/operations-configuration-recovery/checklist-schema-alter/) - 운영 중 DDL 실행과 충돌 대응
