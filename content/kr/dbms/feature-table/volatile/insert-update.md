---
title : '휘발성 테이블의 입력 및 갱신'
type : docs
weight: 30
---

## 데이터 입력 (Insert)

휘발성 테이블의 데이터 입력(Insert)은 다음과 같다.

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

## 데이터 입력 (Append)

마크베이스에서 제공하는 빠른 실시간 데이터 입력 API이다.

C, C++, C#, Java, Python, PHP, Javascript 를 이용하여 입력할 수 있다.

```sql
Mach> create volatile table vtable (id integer, value double);
```
```sql
SQL_APPEND_PARAM sParam[2];
for(int i=0; i<10000; i++)
{
    sParam[0].mInteger  = i;
    sParam[1].mDouble   = i;
    SQLAppendDataV2(stmt, sParam) != SQL_SUCCESS)
}
```

Cluster Edition의 경우 Append 입력은 Leader Broker에서 수행해야 한다.

세부 내용은 [SDK](/kr/dbms/sdk) 가이드를 참고한다.

## 데이터 갱신

휘발성 테이블의 데이터 입력 시, ON DUPLICATE KEY UPDATE 절을 사용해 중복된 기본 키 값을 가진 데이터의 갱신을 할 수 있다.

### 삽입할 데이터 값으로 갱신
INSERT 구문에서 삽입할 데이터를 지정했지만, 삽입 데이터의 기본 키 값과 일치하는 다른 데이터가 존재하는 경우에는 INSERT 구문이 실패하게 되고 해당 데이터는 삽입되지 않는다. 삽입 데이터의 기본 키 값과 일치하는 다른 데이터가 존재하는 경우에, 삽입이 아닌 해당 데이터를 갱신하고자 하는 경우에는 ON DUPLICATE KEY UPDATE 절을 추가할 수 있다.

* 기본 키 중복 데이터가 존재하지 않는 경우, 삽입할 데이터 내용이 그대로 삽입된다.
* 기본 키 중복 데이터가 존재하는 경우, 삽입할 데이터 내용으로 기존의 데이터가 갱신된다.

이 기능을 사용하기 위한 제약 조건은 다음과 같다.
* 휘발성 테이블에 기본 키가 지정되어 있어야 한다.
* 삽입하고자 하는 값에, 기본 키 값이 반드시 포함되어야 한다.

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

### 갱신할 데이터 값을 지정

위와 비슷하지만, 삽입할 데이터 값과 다른 컬럼 값으로 갱신해야 하는 경우에는 ON DUPLICATE KEY UPDATE SET 절을 통해 지정할 수 있다. SET 절 아래에 갱신할 데이터 값을 지정할 수 있다.

* 기본 키 중복 데이터가 존재하지 않는 경우, 삽입 데이터 내용이 그대로 삽입된다.
* 기본 키 중복 데이터가 존재하는 경우, SET 절에 명시된 갱신 데이터만으로 기존의 데이터가 갱신된다.
* 기본 키 값을 갱신할 데이터 값으로 지정할 수 없다.
* SET 절에서 명시되지 않은 컬럼들의 값은 갱신되지 않는다.

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
