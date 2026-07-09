---
title : Volatile 데이터 삭제
type : docs
weight: 40
---

> **8.5 원문 보강 자료**: 이 문서는 기존 8.5 매뉴얼의 내용을 새 장 구조에 맞춰 보존한 것입니다. Machbase 8.6 기준과 표현이 다른 부분은 같은 절의 최신 리뉴얼 문서를 우선합니다.

##  데이터 삭제

Volatile 테이블은 조건절(WHERE 절)에서 primary key 값 조건을 사용하여 데이터를 삭제할 수 있습니다.

* **volatile 테이블에는 primary key 컬럼이 지정되어 있어야 합니다.**
* (Primary key 컬럼) = (값) 조건만 허용되며, 다른 조건과 함께 사용할 수 없습니다.
* primary key 컬럼이 아닌 다른 컬럼을 사용할 수 없습니다.

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
[4] row(s) selected.
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
