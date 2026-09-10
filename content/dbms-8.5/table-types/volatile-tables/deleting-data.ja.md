---
title : Volatile データの削除
type : docs
weight: 40
toc: true
---

##  データの削除 {#delete-data}

Volatile テーブルでは、WHERE 句で主キーの値を指定してデータを削除できます。

* **Volatile テーブルに主キー列を定義する必要があります。**
* 条件には「主キー列 = 値」のみを指定でき、他の条件と組み合わせることはできません。
* 主キー以外の列は使用できません。

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
