---
title : '휘발성 테이블의 삭제'
type : docs
weight: 40
---

## 데이터 삭제

휘발성 테이블은 조건 절(WHERE 절)에서 기본 키 값 조건을 이용해 데이터를 삭제할 수 있다.
* 휘발성 테이블에 기본 키 컬럼이 지정되어 있어야 한다.
* (기본 키 컬럼) = (값)의 조건만 허용하며, 다른 조건과 함께 사용할 수 없다.
* 기본 키 컬럼이 아닌 다른 컬럼을 사용할 수 없다.

```sql
Mach> create volatile table vtable (id integer primary key, name varchar(20));
Created successfully.
Mach> insert into vtable values(1, 'west device');
1 row(s) inserted.
Mach> insert into vtable values(2, 'east device');
1 row(s) inserted.
Mach> insert into vtable values(3, 'north device');
1 row(s) inserted.
Mach> insert into vtable values(4, 'south device');
1 row(s) inserted.
Mach> select * from vtable;
ID          NAME                 
-------------------------------------
1           west device          
2           east device          
3           north device         
4           south device         
[4] row(s) inserted.
Mach> delete from vtable where id = 2;
[1] row(s) deleted.
Mach> select * from vtable;
ID          NAME                 
-------------------------------------
1           west device          
3           north device         
4           south device         
[3] row(s) selected.
```
