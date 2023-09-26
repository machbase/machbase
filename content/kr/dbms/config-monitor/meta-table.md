---
layout : post
title : 'Meta Table'
type: docs
---

## Index

- [Index](#index)
- [User Object](#user-object)
  - [M$SYS\_TABLES](#msys_tables)
  - [M$SYS\_TABLE\_PROPERTY](#msys_table_property)
  - [M$SYS\_COLUMNS](#msys_columns)
  - [M$SYS\_INDEXES](#msys_indexes)
  - [M$SYS\_INDEX\_COLUMNS](#msys_index_columns)
  - [M$SYS\_TABLESPACES](#msys_tablespaces)
  - [M$SYS\_TABLESPACE\_DISKS](#msys_tablespace_disks)
  - [M$SYS\_USERS](#msys_users)
  - [M$RETENTION](#mretention)
- [Others](#others)
  - [M$TABLES](#mtables)
  - [M$COLUMNS](#mcolumns)


메타 테이블은 마크베이스의 스키마 정보를 제시해 주는 테이블들로 테이블 명이 M$로 시작된다.

이 테이블들은 테이블의 이름과, 컬럼 정보, 인덱스 정보들을 유지하고 있고, DDL문에 의해서 생성, 변경, 삭제된 상황을 반영한다.
이 메타 테이블은 사용자에 의해서 추가, 삭제, 변경될 수 없다.

## User Object
### M$SYS_TABLES
---

사용자가 생성한 테이블을 표시한다.

| 컬럼 이름       | 설명                                                                                              |
| ----------- | ----------------------------------------------------------------------------------------------- |
| NAME        | 테이블 이름                                                                                          |
| TYPE        | 테이블 유형<br>0: Log<br>1: Fixed<br>3: Volatile<br>4: Lookup<br>5: Key Value<br>6: Tag              |
| DATABASE_ID | 데이터베이스 식별자                                                                                      |
| ID          | 테이블 식별자                                                                                         |
| USER ID     | 테이블을 생성한 사용자                                                                                    |
| COLCOUNT    | 컬럼의 개수                                                                                          |
| FLAG        | 테이블 타입 구분<br>1 : Tag Data Table<br>2 : Rollup Table<br>4 : Tag Meta Table<br>8 : Tag Stat Table |

### M$SYS_TABLE_PROPERTY
---

각 테이블에 적용된 테이블 프로퍼티 정보를 표시한다.

| 컬럼 이름 | 설명        |
| ----- | --------- |
| ID    | 대상 테이블 ID |
| NAME  | 프로퍼티 이름   |
| VALUE | 프로퍼티 값    |

### M$SYS_COLUMNS
---

M$SYS_TABLES 에 표시된 사용자 테이블의 컬럼 정보를 표시한다.

| 컬럼 이름                | 설명                |
| -------------------- | ----------------- |
| NAME                 | 컬럼 이름             |
| TYPE                 | 컬럼 타입             |
| DATABASE_ID          | 데이터베이스 식별자        |
| ID                   | 컬럼 식별자            |
| LENGTH               | 컬럼 길이             |
| TABLE_ID             | 컬럼이 속한 테이블의 식별자   |
| FLAG                 | (서버 내부 사용을 위한 정보) |
| PART_PAGE_COUNT      | 파티션 당 페이지 수       |
| PAGE_VALUE_COUNT     | 페이지 당 데이터의 수      |
| MINMAX_CACHE_SIZE    | MIN-MAX 캐쉬의 크기    |
| MAX_CACHE_PART_COUNT | 파티션 캐쉬의 최대 개수     |

### M$SYS_INDEXES
---

사용자가 생성한 인덱스 정보를 표시한다.

| 컬럼 이름            | 설명                            |
| ---------------- | ----------------------------- |
| NAME             | 인덱스의 이름                       |
| TYPE             | 인덱스의 종류                       |
| DATABASE_ID      | 데이터베이스 식별자                    |
| ID               | 인덱스 식별자                       |
| TABLE_ID         | 인덱스를 생성한 테이블 식별자              |
| COLCOUNT         | 인덱스를 생성한 컬럼의 수                |
| PART_VALUE_COUNT | 인덱스가 속한 테이블의 파티션당 데이터 수       |
| BLOOM_FILTER     | Bloom Filter 사용 가능 여부         |
| KEY_COMPRESS     | 키값의 압축 여부                     |
| MAX_LEVEL        | 인덱스의 최대 레벨 (LSM 만 가능)         |
| PAGE_SIZE        | 페이지 크기                        |
| MAX_KEYWORD_SIZE | 최대 키워드 길이 (Keyword 만 가능)      |
| BITMAP_ENCODE    | Bitmap 인코딩 유형 (RANGE / EQUAL) |

### M$SYS_INDEX_COLUMNS
---

M$SYS_INDEXES 에 표시된 사용자 인덱스의 컬럼 정보를 표시한다.

| 컬럼 이름       | 설명         |
| ----------- | ---------- |
| INDEX_ID    | 인덱스 식별자    |
| INDEX_TYPE  | 인덱스 종류     |
| NAME        | 컬럼의 이름     |
| COL_ID      | 컬럼 식별자     |
| DATABASE_ID | 데이터베이스 식별자 |
| TABLE_ID    | 테이블 식별자    |
| TYPE        | 컬럼의 데이터타입  |

### M$SYS_TABLESPACES
---

사용자가 생성한 테이블스페이스 정보를 표시한다.

| 컬럼 이름      | 설명                 |
| ---------- | ------------------ |
| NAME       | 테이블스페이스 이름         |
| ID         | 테이블스페이스 식별자        |
| DISK_COUNT | 테이블스페이스에 속한 디스크의 수 |

### M$SYS_TABLESPACE_DISKS
---

테이블스페이스가 사용하는 디스크 정보를 표시한다.

| 컬럼 이름              | 설명                            |
| ------------------ | ----------------------------- |
| NAME               | 디스크 이름                        |
| ID                 | 디스크 식별자                       |
| TABLESPACE_ID      | 디스크가 속한 테이블스페이스 식별자           |
| PATH               | 디스크의 경로                       |
| IO_THREAD_COUNT    | 이 디스크에 할당된 IO 스레드의 수          |
| VIRTUAL_DISK_COUNT | 이 디스크에 할당된 Virtual Disk 단위 개수 |

### M$SYS_USERS
---

마크베이스에 등록된 사용자 정보를 표시한다.

| 컬럼 이름   | 설명       |
| ------- | -------- |
| USER_ID | 사용자의 식별자 |
| NAME    | 사용자의 이름  |

### M$RETENTION
---

RETENTION POLICY 정보를 표시한다.

| 컬럼 이름   | 설명           |
|-------------|----------------|
| USER_ID     | 사용자 ID      |
| POLICY_NAME | policy 이름    |
| DURATION    | 만료 기간(sec) |
| INTERVAL    | 갱신 주기(sec) |

## Others
### M$TABLES
---

M$로 시작하는 모든 메타테이블을 표시한다.

| 컬럼 이름       | 설명                      |
| ----------- | ----------------------- |
| NAME        | 메타 테이블의 이름              |
| TYPE        | 테이블 유형                  |
| DATABASE_ID | 데이터베이스 식별자              |
| ID          | 메타 테이블의 식별자             |
| USER ID     | 테이블을 생성한 사용자 (여기서는 SYS) |
| COLCOUNT    | 컬럼의 개수                  |

### M$COLUMNS
---

M$TABLES 에 표시된 메타테이블의 컬럼 정보를 표시한다.

| 컬럼 이름                | 설명                |
| -------------------- | ----------------- |
| NAME                 | 컬럼 이름             |
| TYPE                 | 컬럼 타입             |
| DATABASE_ID          | 데이터베이스 식별자        |
| ID                   | 컬럼 식별자            |
| LENGTH               | 컬럼 길이             |
| TABLE_ID             | 컬럼이 속한 테이블의 식별자   |
| FLAG                 | (서버 내부 사용을 위한 정보) |
| PART_PAGE_COUNT      | 파티션당 페이지 수        |
| PAGE_VALUE_COUNT     | 페이지 당 데이터의 수      |
| MINMAX_CACHE_SIZE    | MIN-MAX 캐쉬의 크기    |
| MAX_CACHE_PART_COUNT | 파티션 캐쉬의 최대 개수     |
