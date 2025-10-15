---
type: docs
layout : post
title : 메타 테이블
type : docs
---

## 목차

- [목차](#목차)
- [사용자 객체](#사용자-객체)
  - [M$SYS\_TABLES](#msys_tables)
  - [M$SYS\_TABLE\_PROPERTY](#msys_table_property)
  - [M$SYS\_COLUMNS](#msys_columns)
  - [M$SYS\_INDEXES](#msys_indexes)
  - [M$SYS\_INDEX\_COLUMNS](#msys_index_columns)
  - [M$SYS\_TABLESPACES](#msys_tablespaces)
  - [M$SYS\_TABLESPACE\_DISKS](#msys_tablespace_disks)
  - [M$SYS\_USERS](#msys_users)
  - [M$RETENTION](#mretention)
- [기타](#기타)
  - [M$TABLES](#mtables)
  - [M$COLUMNS](#mcolumns)


메타 테이블은 Machbase의 스키마 정보를 표현하는 테이블입니다. 테이블 이름은 "M$"로 시작합니다.

이 테이블들은 테이블 이름, 컬럼 정보, 인덱스 정보를 보유하며, DDL 문으로 인한 생성, 수정 및 삭제 정보를 반영합니다.
메타 테이블은 사용자가 추가, 삭제 또는 변경할 수 없습니다.


## 사용자 객체

### M$SYS_TABLES
---

사용자가 생성한 테이블을 표시합니다.

|컬럼명|설명|
|--|--|
|NAME|테이블 이름|
|TYPE|테이블 타입<br> - 0: Log<br> - 1: Fixed<br> - 3: Volatile<br> - 4: Lookup<br> - 5: Key Value<br> - 6: Tag|
|DATABASE_ID|데이터베이스 식별자|
|ID|테이블 식별자|
|USER ID|테이블 생성 사용자|
|COLCOUNT|컬럼 수|
|FLAG|테이블 타입 분류<br> - 1 : Tag Data Table<br> - 2 : Rollup Table<br> - 4 : Tag Meta Table<br> - 8 : Tag Stat Table|

### M$SYS_TABLE_PROPERTY
---

각 테이블에 적용된 테이블 속성 정보를 표시합니다.

|컬럼명|설명|
|--|--|
|ID|테이블 식별자|
|NAME|속성 이름|
|VALUE|속성 값|


### M$SYS_COLUMNS
---

M$SYS_TABLES에 표시된 사용자 테이블의 컬럼 정보를 표시합니다.

|컬럼명|설명|
|--|--|
|NAME|컬럼명|
|TYPE|컬럼 타입|
|DATABASE_ID|데이터베이스 식별자|
|ID|컬럼 식별자|
|LENGTH|컬럼 길이|
|TABLE_ID|컬럼의 테이블 식별자|
|FLAG|(서버 내부 사용 정보)|
|PART_PAGE_COUNT|파티션당 페이지 수|
|PAGE_VALUE_COUNT|페이지당 데이터 수|
|MINMAX_CACHE_SIZE|MIN-MAX 캐시 크기|
|MAX_CACHE_PART_COUNT|최대 파티션 캐시 수|


### M$SYS_INDEXES
---

사용자가 생성한 인덱스 정보를 표시합니다.

|컬럼명|설명|
|--|--|
|NAME|인덱스 이름|
|TYPE|인덱스 타입|
|DATABASE_ID|데이터베이스 식별자|
|ID|인덱스 식별자|
|TABLE_ID|인덱스의 테이블 식별자|
|COLCOUNT|생성된 인덱스의 컬럼 수|
|PART_VALUE_COUNT|인덱스 테이블 파티션당 데이터 수|
|BLOOM_FILTER|Bloom Filter 사용 가능 여부|
|KEY_COMPRESS|키 값 압축 상태|
|MAX_LEVEL|인덱스 최대 레벨 (LSM만)|
|PAGE_SIZE|페이지 크기|
|MAX_KEYWORD_SIZE|최대 키워드 길이 (keyword만)|
|BITMAP_ENCODE|비트맵 인코딩 타입 (RANGE / EQUAL)|


### M$SYS_INDEX_COLUMNS
---

M$SYS_INDEXES에 표시된 사용자 인덱스의 컬럼 정보를 표시합니다.

|컬럼명|설명|
|--|--|
|INDEX_ID|인덱스 식별자|
|INDEX_TYPE|인덱스 타입|
|NAME|컬럼명|
|COL_ID|컬럼 식별자|
|DATABASE_ID|데이터베이스 식별자|
|TABLE_ID|테이블 식별자|
|TYPE|컬럼의 데이터 타입|


### M$SYS_TABLESPACES
---

사용자가 생성한 테이블스페이스 정보를 표시합니다.

|컬럼명|설명|
|--|--|
|NAME|테이블스페이스 이름|
|ID|테이블스페이스 식별자|
|DISK_COUNT|테이블스페이스의 디스크 수|


### M$SYS_TABLESPACE_DISKS
---

테이블스페이스가 사용하는 디스크 정보를 유지합니다.

|컬럼명|설명|
|--|--|
|NAME|디스크 이름|
|ID|디스크 식별자|
|TABLESPACE_ID|디스크의 테이블스페이스 식별자|
|PATH|디스크 경로|
|IO_THREAD_COUNT|이 디스크에 할당된 I/O 스레드 수|
|VIRTUAL_DISK_COUNT|이 디스크에 할당된 가상 디스크 단위 수|


### M$SYS_USERS
---

Machbase에 등록된 사용자 정보를 유지합니다.

|컬럼명|설명|
|--|--|
|USER_ID|사용자 식별자|
|NAME|사용자 이름|

### M$RETENTION
---

RETENTION POLICY 정보를 표시합니다.

|컬럼명|설명|
|-------------|----------------|
| USER_ID     | 사용자 ID      |
| POLICY_NAME | 정책 이름    |
| DURATION    | 보존 기간(초) |
| INTERVAL    | 업데이트 주기(초) |

## 기타

### M$TABLES
---

M$로 시작하는 모든 메타 테이블을 표시합니다.

|컬럼명|설명|
|--|--|
|NAME|메타 테이블 이름|
|TYPE|테이블 타입|
|DATABASE_ID|데이터베이스 식별자|
|ID|메타 테이블 식별자|
|USER ID|테이블 사용자 (이 경우 SYS)|
|COLCOUNT|컬럼 수|


### M$COLUMNS
---

M$TABLES에 표시된 메타 테이블의 컬럼 정보를 표시합니다.

|컬럼명|설명|
|--|--|
|NAME|컬럼명|
|TYPE|컬럼 타입|
|DATABASE_ID|데이터베이스 식별자|
|ID|컬럼 식별자|
|LENGTH|컬럼 길이|
|TABLE_ID|컬럼의 테이블 식별자|
|FLAG|(서버 내부 사용 정보)|
|PART_PAGE_COUNT|파티션당 페이지 수|
|PAGE_VALUE_COUNT|페이지당 데이터 수|
|MINMAX_CACHE_SIZE|MIN-MAX 캐시 크기|
|MAX_CACHE_PART_COUNT|최대 파티션 캐시 수|
