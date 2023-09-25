---
title : '데이터 입력 : Insert'
type: docs
weight: 10
---

다른 상용 RDBMS와 유사하게, 테이블을 먼저 생성하고 데이터는 INSERT INTO 문을 이용하여 데이터를 입력할 수 있다.

마크베이스는 'machsql' 도구를 대화형 질의 처리기로 제공한다.

## 테이블 생성

```sql
CREATE TABLE table_name (
    column1 datatype,
    column2 datatype,
    column3 datatype,
    ....
);
CREATE TABLE sensor_data
(
    id VARCHAR(32),
    val DOUBLE
);
```

## 데이터 입력

```sql
INSERT INTO table_name
VALUES (value1, value2, value3, ...);
```

```sql
INSERT INTO sensor_data VALUES('sensor1', 10.1);
INSERT INTO sensor_data VALUES('sensor2', 20.2);
INSERT INTO sensor_data VALUES('sensor3', 30.3);
```

## 데이터 입력 확인

```sql
SELECT column1, column2, ...
FROM table_name;
```

```sql
SELECT * FROM sensor_data;
```

## 전체 과정

아래는 machsql 을 사용한 예제이다.

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
ID                                VAL
-----------------------------------------------------------------
sensor3                           30.3
sensor2                           20.2
sensor1                           10.1
[3] row(s) selected.
```