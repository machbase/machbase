---
title: '10.5 조회와 분석'
weight: 50
toc: true
---

VOLATILE 테이블의 데이터 조회 방법을 다룬다.


<a id="original-85-querying-data"></a>

## Volatile 데이터 추출


### 데이터 조회

다른 테이블 유형과 동일하게 SELECT 문으로 조회한다.

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
Mach> select * from vtable where id = 1;
ID          NAME
-------------------------------------
1           west device
[1] row(s) selected.
Mach> select * from vtable where name like 'west%';
ID          NAME
-------------------------------------
1           west device
[1] row(s) selected.
```
