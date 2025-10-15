---
type: docs
title : Volatile 인덱스 생성 및 관리
type : docs
weight: 50
---

##  인덱스 생성 및 사용

volatile 테이블은 실시간 검색에 최적화된 RED-BLACK Tree를 제공합니다. 모든 데이터 유형에 대해 인덱스를 설정할 수 있습니다. 그러나 하나의 컬럼에 대해 하나의 인덱스만 생성할 수 있으며, 복합 인덱스는 제공되지 않습니다.

```sql
Mach> create volatile table vtable (id integer, name varchar(10));
Created successfully.
Mach> create index idx_vrb on vtable (name) index_type redblack;
Created successfuly.
Mach> desc vtable;
----------------------------------------------------------------
NAME                          TYPE                LENGTH
----------------------------------------------------------------
ID                            integer             11
NAME                          varchar             10

[ INDEX ]
----------------------------------------------------------------
NAME                          TYPE                COLUMN
----------------------------------------------------------------
IDX_VRB                       REDBLACK            NAME
iFlux>
```


##  Primary Key 인덱스

volatile 테이블의 특정 컬럼에 primary key가 할당되면 RED-BLACK Tree 인덱스가 자동으로 생성됩니다. 이 경우 Uniqueness 속성을 가진 특수 인덱스가 생성되며 중복 값을 허용하지 않습니다.

```sql
Mach> create volatile table vtable (id integer primary key, name varchar(20));
Created successfully.
Mach> desc vtable;
----------------------------------------------------------------
NAME                          TYPE                LENGTH
----------------------------------------------------------------
ID                            integer             11
NAME                          varchar             20

[ INDEX ]
----------------------------------------------------------------
NAME                          TYPE                COLUMN
----------------------------------------------------------------
__PK_IDX_VTABLE               REDBLACK            ID

iFlux>
```


##  기타 인덱스 유형

log 테이블에서 사용되는 bitmap 또는 keyword 인덱스는 volatile 테이블에서 사용할 수 없습니다.

```sql
Mach> create bitmap   index idx_1237 on vtable(id1);
[ERR-02069 : Error in index for invalid table. BITMAP Index can only be created for LOG Table.]
Mach> create keyword  index idx_1238 on vtable(name);
[ERR-02069 : Error in index for invalid table. KEYWORD Index can only be created for LOG Table.]
```
