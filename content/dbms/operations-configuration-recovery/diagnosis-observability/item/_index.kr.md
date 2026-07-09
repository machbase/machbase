---
type: docs
title: '13.4.2 메타 테이블 활용'
weight: 20
---

메타 테이블은 Machbase의 스키마 정보(테이블 정의, 컬럼, 인덱스, 사용자 등)를 조회할 수 있는 읽기 전용 시스템 테이블입니다. 테이블 이름은 모두 `M$`로 시작합니다. 사용자가 직접 데이터를 추가하거나 변경할 수 없으며, DDL 명령 실행 결과가 자동으로 반영됩니다.

## 메타 테이블 목록

| 테이블 이름 | 용도 |
|-----------|------|
| M$SYS_TABLES | 사용자가 생성한 테이블 목록과 타입 |
| M$SYS_TABLE_PROPERTY | 테이블에 적용된 속성 정보 |
| M$SYS_COLUMNS | 테이블 컬럼 정의 (타입, 길이 등) |
| M$SYS_INDEXES | 인덱스 정의 |
| M$SYS_INDEX_COLUMNS | 인덱스를 구성하는 컬럼 정보 |
| M$SYS_TABLESPACES | 테이블스페이스 목록 |
| M$SYS_TABLESPACE_DISKS | 테이블스페이스가 사용하는 디스크 경로 |
| M$SYS_USERS | 등록된 사용자 목록 |
| M$SYS_VIEWS | 뷰 정의 SQL 텍스트 |
| M$SYS_USER_ACCESS | 테이블별 사용자 권한 |
| M$RETENTION | Retention Policy 정보 |
| M$TABLES | M$ 메타 테이블 자체 목록 |
| M$COLUMNS | M$ 메타 테이블의 컬럼 목록 |

## 주요 테이블 컬럼

### M$SYS_TABLES

| 컬럼명 | 설명 |
|-------|------|
| NAME | 테이블 이름 |
| TYPE | 테이블 타입 (0: Log, 1: Fixed, 3: Volatile, 4: Lookup, 5: Key Value, 6: Tag) |
| ID | 테이블 식별자 |
| USER_ID | 테이블 생성 사용자 식별자 |
| COLCOUNT | 컬럼 수 |
| FLAG | 서브 타입 (1: Tag Data, 2: Rollup, 4: Tag Meta, 8: Tag Stat) |

### M$SYS_COLUMNS

| 컬럼명 | 설명 |
|-------|------|
| NAME | 컬럼명 |
| TYPE | 컬럼 데이터 타입 |
| TABLE_ID | 소속 테이블 식별자 |
| LENGTH | 컬럼 최대 길이 |
| PART_PAGE_COUNT | 파티션당 페이지 수 |
| MINMAX_CACHE_SIZE | MIN-MAX 캐시 크기 |

### M$SYS_INDEXES

| 컬럼명 | 설명 |
|-------|------|
| NAME | 인덱스 이름 |
| TYPE | 인덱스 타입 |
| TABLE_ID | 소속 테이블 식별자 |
| COLCOUNT | 인덱스 컬럼 수 |
| MAX_LEVEL | 최대 LSM 레벨 |

## SQL 예제

### 전체 테이블 목록 조회

```sql
-- 사용자 테이블 전체 목록
SELECT name, type, colcount
  FROM m$sys_tables
 ORDER BY name;
```

타입 값의 의미: `0` = Log 테이블, `1` = Fixed 테이블, `3` = Volatile 테이블, `6` = Tag 테이블

### 특정 테이블 정의 조회

```sql
-- SENSOR_LOG 테이블의 메타 정보
SELECT name, type, colcount, flag
  FROM m$sys_tables
 WHERE name = 'SENSOR_LOG';
```

### 테이블의 컬럼 정보 조회

```sql
-- SENSOR_LOG 테이블의 컬럼 목록
SELECT c.name AS col_name,
       c.type AS col_type,
       c.length
  FROM m$sys_columns c
  JOIN m$sys_tables  t ON c.table_id = t.id
 WHERE t.name = 'SENSOR_LOG'
 ORDER BY c.id;
```

### 인덱스 목록 조회

```sql
-- 특정 테이블에 생성된 인덱스 목록
SELECT i.name AS idx_name,
       i.type AS idx_type,
       i.colcount
  FROM m$sys_indexes i
  JOIN m$sys_tables  t ON i.table_id = t.id
 WHERE t.name = 'SENSOR_LOG';
```

### 인덱스 컬럼 확인

```sql
-- 인덱스를 구성하는 컬럼 확인
SELECT ic.name AS col_name,
       ic.index_type
  FROM m$sys_index_columns ic
  JOIN m$sys_indexes i ON ic.index_id = i.id
  JOIN m$sys_tables  t ON i.table_id = t.id
 WHERE t.name = 'SENSOR_LOG';
```

### 테이블스페이스 디스크 경로 확인

```sql
-- 테이블스페이스가 사용하는 물리 경로
SELECT ts.name AS tbs_name,
       d.path,
       d.io_thread_count
  FROM m$sys_tablespace_disks d
  JOIN m$sys_tablespaces ts ON d.tablespace_id = ts.id;
```

### 사용자 목록 조회

```sql
-- 등록된 사용자와 패스워드 정책 확인
SELECT user_id, name, pwd_policy_level, valid_before
  FROM m$sys_users;
```

### Retention Policy 확인

```sql
-- 설정된 Retention Policy 목록
SELECT policy_name, duration, interval
  FROM m$retention;
```

> **참고**: 메타 테이블은 읽기 전용입니다. `INSERT`, `UPDATE`, `DELETE` 명령은 오류를 반환합니다. 스키마를 변경하려면 반드시 `CREATE TABLE`, `ALTER TABLE`, `DROP TABLE` 등의 DDL 명령을 사용하십시오.
