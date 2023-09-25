---
title : '휘발성 인덱스 생성 및 관리'
type : docs
weight: 50
---

## 인덱스 생성 및 활용

휘발성 테이블은 실시간 검색에 최적화된 레드블랙(RED-BLACK) 트리를 기본으로 제공하고 있으며, 모든 데이터 타입에 대해서 인덱스를 설치할 수 있다. 단, 하나의 컬럼에 대해 하나의 인덱스가 생성 가능하며, 복합(composite) 인덱스는 제공하지 않는다.

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

## 기본 키 인덱스

또한 휘발성 테이블의 특정 컬럼에 기본 키를 부여하게 되면, 여기에 레드블랙 트리 인덱스를 자동으로 생성하게 된다. 이 때는 유일성(Uniqueness) 속성을 지닌 특별한 인덱스가 생성되며 중복된 값을 허용하지 않는다.

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
 
## 다른 인덱스 유형

로그 테이블에서 사용하던 비트맵 혹은 키워드 인덱스는 휘발성 테이블에서 사용할 수 없다.

```sql
Mach> create bitmap   index idx_1237 on vtable(id1);
[ERR-02069 : Error in index for invalid table. BITMAP Index can only be created for LOG Table.]
Mach> create keyword  index idx_1238 on vtable(name);
[ERR-02069 : Error in index for invalid table. KEYWORD Index can only be created for LOG Table.]
```
