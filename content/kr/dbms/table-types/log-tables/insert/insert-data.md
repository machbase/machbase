---
title : Insert
type: docs
weight: 10
---

다른 상용 RDBMS와 유사하게, 먼저 테이블을 생성하고 INSERT INTO 문을 사용하여 데이터를 입력할 수 있습니다.

Machbase는 대화형 쿼리 프로세서로 'machsql' 도구를 제공합니다.


## 테이블 생성

```sql
CREATE TABLE table_name ( column1 datatype, column2 datatype, column3 datatype, .... );
```

```sql
CREATE TABLE sensor_data ( id VARCHAR(32), val DOUBLE );
```


## 데이터 삽입

```sql
INSERT INTO table_name VALUES (value1, value2, value3, ...);
```

```sql
INSERT INTO sensor_data VALUES('sensor1', 10.1); INSERT INTO sensor_data VALUES('sensor2', 20.2); INSERT INTO sensor_data VALUES('sensor3', 30.3);
```


## 데이터 삽입 확인

```sql
SELECT column1, column2, ... FROM table_name;
```

```sql
SELECT * FROM sensor_data;
```


## 전체 프로세스

다음은 machsql을 사용한 예제입니다.

```sql
Mach> CREATE TABLE sensor_data (id VARCHAR(32), val DOUBLE);
 Created successfully.
Mach> INSERT INTO sensor_data VALUES('sensor1', 10.1);
 1 row(s) inserted.
Mach> INSERT INTO sensor_data VALUES('sensor2', 20.2);
 1 row(s) inserted.
Mach> INSERT INTO sensor_data VALUES('sensor3', 30.3);
 1 row(s) inserted.
Mach> SELECT * FROM sensor_data;
ID VAL
-----------------------------------------------------------------
sensor3 30.3
sensor2 20.2
sensor1 10.1
[3] row(s) selected.
```
