---
title : Volatile 데이터 삽입 및 업데이트
type : docs
weight: 30
---

##  데이터 삽입

volatile 테이블의 데이터 삽입은 다음과 같습니다.

```sql
Mach> create volatile table vtable (id integer, name varchar(20));
Created successfully.
Mach> insert into vtable values(1, 'west device');
1 row(s) inserted.
Mach> insert into vtable values(2, 'east device');
1 row(s) inserted.
Mach> insert into vtable values(3, 'north device');
1 row(s) inserted.
Mach> insert into vtable values(4, 'south device');
1 row(s) inserted.
```


##  데이터 Append

Machbase에서 제공하는 빠른 실시간 데이터 입력 API입니다.
C, C++, C#, Java, Python, PHP, Javascript에서 append를 사용할 수 있습니다.

```sql
Mach> create volatile table vtable (id integer, value double);
```

```c
SQL_APPEND_PARAM sParam[2];
for(int i=0; i<10000; i++)
{
    sParam[0].mInteger  = i;
    sParam[1].mDouble   = i;
    SQLAppendDataV2(stmt, sParam) != SQL_SUCCESS)
}
```

Cluster Edition Append의 경우, Leader Broker에서 수행해야 합니다.

자세한 내용은 [SDK](/dbms/sdk) 가이드를 참조하세요.


##  데이터 업데이트

volatile 테이블에 데이터를 입력할 때, ON DUPLICATE KEY UPDATE 절을 사용하여 중복된 primary key 값을 가진 데이터를 업데이트할 수 있습니다.

### 삽입할 데이터 값으로 업데이트

INSERT 문에서 삽입할 데이터를 지정했지만, 삽입 데이터의 primary key 값과 일치하는 다른 데이터가 있으면 INSERT 문이 실패하고 해당 데이터가 삽입되지 않습니다. 삽입 데이터의 primary key 값과 일치하는 다른 데이터가 있고 삽입 대신 해당 데이터를 업데이트하려면 ON DUPLICATE KEY UPDATE 절을 추가할 수 있습니다.

* 중복된 primary key 데이터가 없으면 삽입할 데이터의 내용이 그대로 삽입됩니다.
* 중복된 primary key 데이터가 있으면 기존 데이터가 삽입할 데이터의 내용으로 업데이트됩니다.

이 기능을 사용하기 위한 제약 조건은 다음과 같습니다.

* volatile 테이블에 primary key가 지정되어 있어야 합니다.
* 삽입할 값에 primary key 값이 포함되어야 합니다.

```sql
Mach> create volatile table vtable (id integer primary key, direction varchar(10), refcnt integer);
Created successfully.
Mach> insert into vtable values(1, 'west', 0);
1 row(s) inserted.
Mach> insert into vtable values(2, 'east', 0);
1 row(s) inserted.
Mach> select * from vtable;
ID          DIRECTION   REFCNT
----------------------------------------
1           west       0
2           east        0
[2] row(s) selected.

Mach> insert into vtable values(1, 'south', 0);
[ERR-01418 : The key already exists in the unique index.]
Mach> insert into vtable values(1, 'south', 0) on duplicate key update;
1 row(s) inserted.

Mach> select * from vtable;
ID          DIRECTION   REFCNT
----------------------------------------
1           south        0
2           east        0
[2] row(s) selected.
```

### 업데이트할 데이터 값 지정

위와 유사하지만 삽입할 데이터 값과 다른 컬럼 값으로 업데이트해야 하는 경우 ON DUPLICATE KEY UPDATE SET 절을 통해 지정할 수 있습니다. 업데이트할 데이터 값은 SET 절 아래에 지정할 수 있습니다.

* primary key 중복 데이터가 존재하지 않으면 삽입할 데이터의 내용이 그대로 삽입됩니다.
* primary key 중복 데이터가 존재하면 기존 데이터는 SET 절에 지정된 업데이트 데이터로만 업데이트됩니다.
* **primary key 값은 업데이트할 데이터 값으로 지정할 수 없습니다.**
* SET 절에 지정되지 않은 컬럼의 값은 업데이트되지 않습니다.

```sql
Mach> create volatile table vtable (id integer primary key, direction varchar(10), refcnt integer);
Created successfully.
Mach> insert into vtable values(1, 'west', 0);
1 row(s) inserted.
Mach> insert into vtable values(2, 'east', 0);
1 row(s) inserted.
Mach> select * from vtable;
ID          DIRECTION   REFCNT
----------------------------------------
1           west        0
2           east        0
[2] row(s) selected.

Mach> insert into vtable values(1, 'west', 0) on duplicate key update set refcnt = 1;
1 row(s) inserted.

Mach> select * from vtable;
ID          DIRECTION   REFCNT
----------------------------------------
1           west        1
2           east        0
[2] row(s) selected.
```
