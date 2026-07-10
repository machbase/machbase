---
type: docs
title: '17.1.1.9 DDL syntax'
weight: 90
toc: true
---

DDL(Data Definition Language)은 테이블, 인덱스, 뷰, 롤업 등 데이터베이스 객체를 생성·수정·삭제하는 구문입니다.

> **권한**: 일반 사용자가 DDL을 실행하려면 `GRANT DDL ON machbasedb TO user_name;` 또는 `GRANT CREATE ON machbasedb TO user_name;`이 필요합니다. 자세한 내용은 [GRANT/REVOKE](../user-auth-syntax/#grant-revoke)를 참고하십시오.

## CREATE TABLE

```sql
create_table_stmt ::=
    'CREATE' table_type? 'TABLE' ['IF NOT EXISTS'] table_name
    '(' column_def ( ',' column_def )* ')'
    [ 'METADATA' '(' column_def ( ',' column_def )* ')' ]
    [ table_property_list ]
    [ 'TABLESPACE' tablespace_name ]
    [ 'WITH ROLLUP' rollup_interval_spec ]

table_type ::= 'TAG' | 'VOLATILE' | 'LOOKUP' | 'RDB'
-- table_type을 생략하면 LOG 테이블이 생성됩니다.

column_def ::= column_name column_type
               [ 'PRIMARY KEY' ]
               [ 'NOT NULL' ]
               [ column_axis ]
               [ 'SUMMARIZED' ]
               [ 'DEFAULT' value ]
               [ 'PROPERTY' '(' column_property_list ')' ]

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
| (없음) | **LOG 테이블** - 시계열 로그 데이터. 추가(INSERT) 전용, 수정 불가 |
| `TAG` | **TAG 테이블** - 태그 이름/시간/값 구조의 시계열 데이터. BASETIME 컬럼 필수 |
| `LOOKUP` | **LOOKUP 테이블** - 메모리 상주. PRIMARY KEY 필수. DML 전체 지원 |
| `VOLATILE` | **VOLATILE 테이블** - 메모리 상주. 서버 재시작 시 데이터 소멸. PRIMARY KEY 선택 |
| `RDB` | **RDB 테이블** - 관계형 데이터와 트랜잭션 지원 |

### 예시

```sql
-- LOG 테이블 생성
CREATE TABLE sensor_log (
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
다릅니다. RDB 테이블은 `ADD COLUMN`, `DROP COLUMN`, `RENAME COLUMN`, `RENAME TO`를
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

-- RDB 컬럼 추가
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
추가·제거하거나, MINMAX_CACHE_SIZE를 변경합니다. RDB 테이블은 `MODIFY COLUMN`을
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
-- RDB 테이블에서 지원
ALTER TABLE product_master RENAME TO product_catalog;
```

### ADD / DROP RETENTION

```sql
alter_table_add_retention_stmt ::=
    'ALTER TABLE' table_name 'ADD RETENTION' policy_name

alter_table_drop_retention_stmt ::=
    'ALTER TABLE' table_name 'DROP RETENTION'
```

```sql
ALTER TABLE tag ADD RETENTION policy_1d_1h;
ALTER TABLE tag DROP RETENTION;
```

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

```sql
create_index_stmt ::=
    'CREATE' index_type_keyword? 'INDEX' index_name
    'ON' table_name '(' column_name [ json_path ] ')'
    [ 'INDEX_TYPE' ( 'LSM' | 'KEYWORD' | 'BITMAP' | 'REDBLACK' ) ]
    [ 'TABLESPACE' tablespace_name ]
    [ index_property_list ]

index_property_list ::=
    ( 'MAX_LEVEL'        '=' number
    | 'PAGE_SIZE'        '=' number
    | 'BITMAP_ENCODE'    '=' ( 'EQUAL' | 'RANGE' )
    | 'PART_VALUE_COUNT' '=' number )
    ( ',' index_property_list )*
```

### 인덱스 타입과 적용 대상

| 인덱스 타입 | 기본 대상 | 설명 |
|------------|----------|------|
| LSM | LOG 테이블 | 대용량 시계열 데이터에 최적화된 기본 인덱스 |
| KEYWORD | LOG 테이블 | VARCHAR/TEXT 컬럼 텍스트 검색용 |
| BITMAP | LOG 테이블 | 데이터 분석용 (VARCHAR, TEXT, BINARY 제외) |
| REDBLACK | VOLATILE/LOOKUP 테이블 | 실시간 메모리 인덱스 |

### 예시

```sql
-- 기본 인덱스 (LOG 테이블 → LSM)
CREATE INDEX idx_sensor_id ON sensor_log (id);

-- KEYWORD 인덱스 (텍스트 검색용)
CREATE INDEX idx_sensor_name ON sensor_log (name) INDEX_TYPE KEYWORD;

-- BITMAP 인덱스
CREATE INDEX idx_sensor_status ON sensor_log (status) INDEX_TYPE BITMAP BITMAP_ENCODE = RANGE;

-- JSON 컬럼의 특정 경로에 인덱스 생성 (TAG 테이블)
CREATE INDEX tag_metric_idx ON tag (value.sensor.name);
CREATE INDEX tag_metric_idx2 ON tag (value->'$.metric');
```

---

## DROP INDEX

```sql
drop_index_stmt ::= 'DROP INDEX' index_name
```

지정한 인덱스를 삭제합니다. 해당 테이블을 조회 중인 다른 세션이 있으면 오류가 발생합니다.

```sql
DROP INDEX idx_sensor_id;
```

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

```sql
-- 기본 롤업
create_rollup_stmt ::=
    'CREATE ROLLUP' rollup_name
    'ON' src_table_name '(' src_column [ '->' json_path ] ')'
    'INTERVAL' number ( 'SEC' | 'MIN' | 'HOUR' )

-- 조건부 롤업
create_conditional_rollup_stmt ::=
    'CREATE ROLLUP' rollup_name
    ( 'ON' src_table_name '(' src_column [ '->' json_path ] ')'
    | 'FROM' src_rollup_name )
    'INTERVAL' number ( 'SEC' | 'MIN' | 'HOUR' )
    'WHERE' predicate

-- 사용자 정의 롤업
create_custom_rollup_stmt ::=
    'CREATE ROLLUP' rollup_name
    'INTO' '(' dest_table_name ')'
    'AS' '(' select_stmt ')'
    'INTERVAL' number ( 'SEC' | 'MIN' | 'HOUR' )
    [ 'WAKEUP INTERVAL' number ( 'SEC' | 'MIN' | 'HOUR' ) ]
```

```sql
-- 1초 간격 기본 롤업
CREATE ROLLUP _rollup_tag_value_sec ON tag(value) INTERVAL 1 SEC;

-- 조건부 롤업 (quality = 1인 데이터만 집계)
CREATE ROLLUP _rollup_tag_good ON tag(value) INTERVAL 1 MIN WHERE quality = 1;

-- JSON 컬럼 멤버 롤업
CREATE ROLLUP tag_metric_ru ON tag (value->'$.metric') INTERVAL 1 MIN;
```

---

## DROP ROLLUP

```sql
drop_rollup_stmt ::= 'DROP ROLLUP' rollup_name
```

```sql
DROP ROLLUP _rollup_tag_value_sec;
```

---

## ALTER ROLLUP

```sql
alter_rollup_stmt ::=
    'ALTER ROLLUP' rollup_name ( 'START' | 'STOP' | 'WAKEUP' | 'FORCE' )
  | 'ALTER ROLLUP' rollup_name 'SET WAKEUP INTERVAL' number ( 'SEC' | 'MIN' | 'HOUR' )
```

```sql
ALTER ROLLUP _rollup_tag_value_sec START;
ALTER ROLLUP _rollup_tag_value_sec STOP;
ALTER ROLLUP _rollup_tag_value_sec WAKEUP;
ALTER ROLLUP _rollup_tag_value_sec FORCE;
ALTER ROLLUP _rollup_tag_value_sec SET WAKEUP INTERVAL 10 SEC;
```

---

## CREATE RETENTION

```sql
create_retention_stmt ::=
    'CREATE RETENTION' policy_name
    'DURATION' duration ( 'MONTH' | 'DAY' )
    'INTERVAL' interval ( 'DAY' | 'HOUR' )
```

```sql
-- 1일 보존, 1시간 간격으로 정리
CREATE RETENTION policy_1d_1h DURATION 1 DAY INTERVAL 1 HOUR;

-- 30일 보존, 1일 간격으로 정리
CREATE RETENTION policy_30d_1d DURATION 30 DAY INTERVAL 1 DAY;
```

---

## DROP RETENTION

```sql
drop_retention_stmt ::= 'DROP RETENTION' policy_name
```

```sql
DROP RETENTION policy_1d_1h;
```

---

## 관련 문서

- [테이블 유형](/dbms/data-modeling-table-design/) - LOG, TAG, LOOKUP, VOLATILE, RDB 테이블 특성 및 사용 가이드
- [TAG 테이블 롤업](/dbms/tag-table-usage/create-alter-drop/#original-85-creating-tag-tables) - 롤업 생성 및 운영 가이드
- [GRANT/REVOKE](../user-auth-syntax/#grant-revoke) - DDL 실행에 필요한 권한 부여
