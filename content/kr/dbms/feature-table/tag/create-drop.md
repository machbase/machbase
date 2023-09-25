---
title : '태그 테이블 생성 및 삭제'
type: docs
weight: 10
---

사용자는 테이블 타입으로 TAG라고 명시적으로 지정하여야 하며, 이후에 이 테이블을 조작함으로써 센서 데이터를 다양한 형태로 활용할 수 있다.

과거 버전과 달리 테이블 이름을 TAG로 하지 않아도 되며, 자유롭게 지정 가능하다.

데이터베이스가 처음 설치되었을 때는 TAG 테이블이 없다는 점에 유의하라.

TAG 테이블은 기본적으로 사용자의 센서 데이터를 저장하기 위한 목적이므로, 아래의 세가지 필수 항목은 반드시 포함되어야 한다.

* 이름
* 입력 시간
* 값 

그러나, 마크베이스의 TAG 테이블은 위의 세가지 뿐만 아니라 부가 컬럼의 입력도 허용하기 때문에 위의 필수 컬럼을 위한 키워드를 동반한다.

7.5 버전부터는 태그 값에 SUMMARIZED 키워드는 선택 사항이다.

* 태그 이름 : PRIMARY KEY
* 태그 입력 시간 : BASETIME

그리고, 이 태그 이름은 다음 장에 설명될 태그 메타 정보로서 활용된다.

## 태그 테이블 생성

가장 간단한 태그 테이블은 아래와 같이 생성된다.

```sql
Mach> CREATE TAG TABLE tag (name VARCHAR(20) PRIMARY KEY, time DATETIME, value DOUBLE);
[ERR-02253: Mandatory column definition (PRIMARY KEY / BASETIME) is missing.]
==> 위와 같이 키워드를 넣지 않으면, 위와 같은 에러가 발생한다.
 
Mach> CREATE TAG TABLE tag (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE SUMMARIZED);
Executed successfully.
==> 통계 정보 활용을 위해서는 태그 값에 SUMMARIZED 키워드를 추가해야 한다.
 
Mach> desc tag;
[ COLUMN ]              
----------------------------------------------------------------
NAME      TYPE        LENGTH
----------------------------------------------------------------
NAME      varchar        20
TIME      datetime       31
VALUE     double         17
 
Mach> CREATE TAG TABLE other_tag (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE);
Executed successfully.
 
Mach> desc other_tag;
[ COLUMN ]              
----------------------------------------------------------------
NAME      TYPE        LENGTH
----------------------------------------------------------------
NAME      varchar        20
TIME      datetime       31
VALUE     double         17
```

즉, TAG 라는 이름을 가진 테이블이 생성되었다. 성능 향상을 위해 4개의 파티션으로 나뉘어진 내부 테이블이 생성된다.

## 추가 센서 컬럼

실제로 TAG 테이블을 활용할 때 단지 3개의 컬럼만으로는 주어진 문제를 해결하기 힘든 경우가 있다.

특히, 입력되는 센서 데이터의 정보가 이름과 시간, 값 뿐만 아니라 특정 그룹이나 인터넷 주소의 경우도 있기 때문에 아래와 같이 추가할 수 있다.

```sql
Mach> create tag table TAG (name varchar(20) primary key, time datetime basetime, value double, grpid short, myip ipv4) ;
Executed successfully.
 
Mach> desc tag;
[ COLUMN ]              
----------------------------------------------------------------
NAME             TYPE        LENGTH
----------------------------------------------------------------
NAME             varchar         20
TIME             datetime        31
VALUE            double          17
GRPID            short            6       <=== 추가됨
MYIP             ipv4            15       <=== 추가됨
```

그러나, 5.5를 포함한 구버전에서는 VARCHAR 타입의 값은 부가 컬럼에 들어갈 수 없다는 점에 유의하자.

```sql
Mach> create tag table TAG (name varchar(20) primary key, time datetime basetime, value double summarized, myname varchar(100)) ;
[ERR-01851: Variable length columns are not allowed in tag table.]
```

문자열 타입의 경우에는 위와 같이 에러가 발생한다. 5.6 이후의 버전에서는TAG 테이블의 추가 컬럼에서도 VARCHAR를 지원한다.

## 추가 메타데이터 컬럼

TAG 테이블에는 센서 컬럼 추가만 가능한 것이 아니라, 각 태그 이름에 종속된 정보를 함께 입력할 수 있다.

이 정보는 센서 데이터에 중복 저장할 필요가 없는 정보이기 때문에, 효율적으로 관리하기 위한 별도의 컬럼 정의 구문인 METADATA (...) 을 추가해야 한다.

```sql
Mach> create tag table TAG (name varchar(20) primary key, time datetime basetime, value double)
   2  metadata (room_no integer, tag_description varchar(100));
```

여기서 room_no, tag_description 은 name 에 종속된 정보이다. 예를 들면, 이런 정보를 입력해 둘 수 있다.

|name|room_no|tag_description|
|--|--|--|
|temp_001|1|It reads current temperature as Celsius|
|humid_001|1|It reads current humidity as percentage|

입력한 이후에는, TAG 테이블에서 SELECT 를 통해 같이 조회할 수 있다.

```sql

Mach> SELECT name, time, value, tag_description FROM tag LIMIT 1;
name                  time                            value
--------------------------------------------------------------------------------------
tag_description
------------------------------------------------------------------------------------
temp_001              2019-03-01 09:52:17 000:000:000 25.3
It reads current temperature as Celsius
```

## 테이블 프로퍼티 지정

태그 테이블 생성 시, 아래 3가지 프로퍼티를 지정할 수 있다.

|이름|설명|값|
|--|--|--|
|TAG_STAT_ENABLE|TAG ID별 통계 정보를 저장하는 기능의 활성화 여부를 지정할 수 있다.|Default: 1<br>Min: 0 (disable)<br>Max: 1 (enable)|
|TAG_PARTITION_COUNT|메모리 및 CPU 사용량을 조절하기 위해 파티션 개수를 지정할 수 있다.	|Default: 4<br>Min: 1<br>Max: 1024|
|TAG_DATA_PART_SIZE|파티션 별 메모리 및 CPU 사용량을 조절하기 위해 데이터 크기를 지정할 수 있다.<br>  BYTE 단위로 지정하며, MB 단위로 ALIGN 된다.|Default: 16777216 (16MB)<br>Min: 1048576 (1MB)<br>Max: 1073741824 (1GB)|

```sql
Mach> CREATE TAG TABLE tag (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE) TAG_PARTITION_COUNT=1;
Executed successfully.
 
Mach> CREATE TAG TABLE tag (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE) TAG_DATA_PART_SIZE=1048576;
Executed successfully.
 
Mach> CREATE TAG TABLE tag (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE) TAG_STAT_ENABLE=0;
Executed successfully.
 
Mach> CREATE TAG TABLE tag (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE) TAG_PARTITION_COUNT=2, TAG_STAT_ENABLE=1;
Executed successfully.
```

## 태그 테이블 삭제

만일 생성된 태그 테이블을 다시 만들거나, 필요가 없어져 디스크 공간을 확보해야 하는 경우에는 다음과 같은 DROP 명령어를 통해 삭제할 수 있다.

TAG 테이블에 관련된 모든 자료, 즉 태그 데이터, 메타데이터 테이블이 모두 삭제되므로 유의해야 한다.

```sql
Mach> DROP TABLE tag;
Dropped successfully.
 
Mach> DESC tag;
tag does not exist.
```
