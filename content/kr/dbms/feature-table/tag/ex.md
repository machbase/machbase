---
title : '태그 테이블 활용 샘플 예제'
type: docs
weight: 50
---

## 개요

태그 테이블은 일반적인 센서 데이터가 저장된 파일의 구조 형태를 로딩할 수 있다.

가장 흔히 볼 수 있는 형태의 텍스트 저장 파일은 아무런 설명 없이, (콤마)나 나뉘어진 다수의 숫자형 값을 그냥 나열한 무작위의 파일 내용인 <값,값,값><값,값,값><반복..> 형태가 대표적이고, 시간을 포함한 파일의 경우에는 <시간,값,값,값> <시간, 값,값,값><반복..>이 있다.

이런 파일의 데이터는 PLC (programmable Logic Controller)라고 불리는 장비에서 1개 이상의 센서 값을 지속적으로 입력된 데이터를 오랜 기간동안 수집했을 경우에 만들어진다. 아래의 사진이 그 예이다.

![tag-ex1](../img/tag-ex1.png)

이제 이 파일을 어떻게 마크베이스의 태그 테이블로 한꺼번에 배치 형태로 로딩하겠다.


## 데이터 변환 순서도

![tag-ex2](../img/tag-ex2.png)

위의 그림에서 볼 수 있듯이 원시 CSV 파일을 마크베이스의 로그 테이블로 한꺼번에 로딩을 한 이후, 이를 태그 테이블로 변환할 것이다.


## 태그 테이블 생성 및 태그 메타 로딩

아래와 같이 태그 테이블을 생성하고 tagmetaimport라는 도구를 이용해서 CSV 파일에 저장된 태그 이름(태그 메타)들을 한꺼번에 로딩한다.

아래 기술된 Option이외에도 machloader에서 사용할 수 있는 옵션을 모두 사용 가능하다.

```sql
Mach> create tag table tag (name varchar(32) primary key, time datetime basetime, value double
summarized);
Executed successfully.
Elapsed time: 3.032
 
$ cat tag_meta.csv
MTAG_V00
MTAG_V01
MTAG_C00
MTAG_C01
MTAG_C02
MTAG_C03
MTAG_C04
MTAG_C05
MTAG_C06
MTAG_C07
MTAG_C08
MTAG_C09
MTAG_C10
MTAG_C11
MTAG_C12
MTAG_C13
MTAG_C14
MTAG_C15
 
$ tagmetaimport -d tag_meta.csv
Import time : 0 hour 0 min 0.340 sec
Load success count : 18
```

(Machbase 포트번호를 기본값에서 변경했으면, tagmetaimport에 -P 옵션을 사용해서 변경된 포트번호를 사용해야한다.)
위와 같이 성공적으로 태그 메타 정보(이름) 18개가 로딩되었다.


## PLC 데이터 로딩을 위한 테이블 생성

아래의 쿼리를 수행해 로그 테이블을 생성한다.

```sql
create table plc_tag_table(
    tm datetime,
    V0 DOUBLE ,
    V1 DOUBLE ,
    C0 DOUBLE ,
    C1 DOUBLE ,
    C2 DOUBLE ,
    C3 DOUBLE ,
    C4 DOUBLE ,
    C5 DOUBLE,
    C6 DOUBLE ,
    C7 DOUBLE ,
    C8 DOUBLE ,
    C9 DOUBLE ,
    C10 DOUBLE ,
    C11 DOUBLE ,
    C12 DOUBLE ,
    C13 DOUBLE ,
    C14 DOUBLE ,
    C15 DOUBLE
);
```

{{< callout type="warning" >}}
주의할 점은 이 테이블은 로그 테이블 타입이라는 것이다(파일명 때문에 헷갈리지 않도록 하자). 마크베이스에서는 별도의 테이블 지정자를 명시하지 않으면, 로그 테이블로 생성된다.
{{< /callout >}}

## PLC 데이터 로딩

아래와 같이 machloader를 사용해 200만 건의 원시 PLC 데이터가 저장된 plc_tag.csv 파일을 위에서 생성한 로그 테이블 plc_tag_table에 PLC 입력 형태로 입력한다. plc_tag.csv 파일은 첫 컬럼은 시간이며, 이후 순서대로 V0, V1, …C15 까지 컬럼이 나뉘어져 있다. 데이터의 패턴은 1초에 0~99mili second까지 약 100개의 데이터가 입력되고, 100 mili second에서 999까지는 입력이 없다가, 다음 1초 동안 동일한 패턴으로 입력된다.

```bash
$ machloader -t plc_tag_table -i -d plc_tag.csv -F "tm YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn"
-----------------------------------------------------------------
Machbase Data Import/Export Utility.
Release Version 5.5.0.official
Copyright 2014, MACHBASE Corporation or its subsidiaries.
All Rights Reserved.
-----------------------------------------------------------------
NLS : US7ASCII EXECUTE MODE : IMPORT
TARGET TABLE : plc_tag_table DATA FILE : 4_plc_tag.csv
IMPORT MODE : APPEND FIELD TERM : ,
ROW TERM : \n ENCLOSURE : "
ESCAPE : \ ARRIVAL_TIME : FALSE
ENCODING : NONE HEADER : FALSE
CREATE TABLE : FALSE
Progress bar Imported records Error records
============================== 2000000 0
Import time : 0 hour 0 min 26.544 sec
Load success count : 2000000
Load fail count : 0
```

## 태그 메타 이름 생성 규칙

이제 태그 테이블에 데이터를 넣어서 실제로 Tag Analyzer를 통해서 데이터를 확인할 수 있도록 한다. 이를 위해서 plc_tag_table 의 정보를 모두 태그 테이블에 넣어야 하는데, 이를 위해서 insert-select 구문을 이용해서 한꺼번에 넣는다. 그리고, 각 컬럼의 값이 모든 태그 테이블의 이름과 맵핑이 되어야 하기 때문에 다음과 같이 매타 태그의 이름 정보를 미리 결정하였다.

|로그 테이블의 컬럼명| 태그 테이블의 Name 컬럼에 입력되는 이름|
|--|--|
|V0|MTAG_V00|
|V1|MTAG_V01|
|C0|MTAG_C00|
|C1|MTAG_C01|
|...||
|C15|MTAG_C15|

## 태그 테이블 데이터 로딩

이제 마지막으로 실제 데이터를 태그 테이블로 로딩할 차례이다. 아래의 쿼리를 수행하면 하나씩 순차적으로 태그 테이블에 넣는다. 

```sql
Mach> insert into tag select 'MTAG_V00', tm, v0 from plc_tag_table;
2000000 row(s) inserted.
Elapsed time: 4.898
Mach> insert into tag select 'MTAG_V01', tm, v1 from plc_tag_table;
2000000 row(s) inserted.
Elapsed time: 5.577
Mach> insert into tag select 'MTAG_C00', tm, c0 from plc_tag_table;
2000000 row(s) inserted.
Elapsed time: 6.327
Mach> insert into tag select 'MTAG_C01', tm, c1 from plc_tag_table;
2000000 row(s) inserted.
Elapsed time: 7.445
Mach> insert into tag select 'MTAG_C02', tm, c2 from plc_tag_table;
2000000 row(s) inserted.
Elapsed time: 6.898
Mach> insert into tag select 'MTAG_C03', tm, c3 from plc_tag_table;
2000000 row(s) inserted.
Elapsed time: 7.078
Mach> insert into tag select 'MTAG_C04', tm, c4 from plc_tag_table;
2000000 row(s) inserted.
Elapsed time: 6.799
Mach> insert into tag select 'MTAG_C05', tm, c5 from plc_tag_table;
2000000 row(s) inserted.
Elapsed time: 7.210
Mach> insert into tag select 'MTAG_C06', tm, c6 from plc_tag_table;
2000000 row(s) inserted.
Elapsed time: 9.232
Mach> insert into tag select 'MTAG_C07', tm, c7 from plc_tag_table;
2000000 row(s) inserted.
Elapsed time: 6.398
Mach> insert into tag select 'MTAG_C08', tm, c8 from plc_tag_table;
2000000 row(s) inserted.
Elapsed time: 6.432
Mach> insert into tag select 'MTAG_C09', tm, c9 from plc_tag_table;
2000000 row(s) inserted.
Elapsed time: 6.734
Mach> insert into tag select 'MTAG_C10', tm, c10 from plc_tag_table;
2000000 row(s) inserted.
Elapsed time: 7.692
Mach> insert into tag select 'MTAG_C11', tm, c11 from plc_tag_table;
2000000 row(s) inserted.
Elapsed time: 8.628
Mach> insert into tag select 'MTAG_C12', tm, c12 from plc_tag_table;
2000000 row(s) inserted.
Elapsed time: 8.229
Mach> insert into tag select 'MTAG_C13', tm, c13 from plc_tag_table;
2000000 row(s) inserted.
Elapsed time: 9.517
Mach> insert into tag select 'MTAG_C14', tm, c14 from plc_tag_table;
2000000 row(s) inserted.
Elapsed time: 7.231
Mach> insert into tag select 'MTAG_C15', tm, c15 from plc_tag_table;
2000000 row(s) inserted.
Elapsed time: 7.830
```

총 3600 만건의 데이터가 로딩된 것을 확인할 수 있다.



