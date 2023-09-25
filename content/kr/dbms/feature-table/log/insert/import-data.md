---
title : '데이터 불러오기 : import'
type: docs
weight: 30
---

machloader 도구를 이용하여, CSV 또는 다른 구분자로 구별된 텍스트 파일을 입력할 수 있다.

machloader 도구에 대한 자세한 설명은 [machloader](../../../tools/machloader.md) 문서를 참조한다.


## 테이블 생성

```sql
CREATE TABLE import_sample
(
    srcip IPV4,
    srcport INTEGER,
    dstip IPV4,
    dstport INTEGER,
    protocol SHORT,
    eventlog VARCHAR(1024),
    eventcode SHORT,
    eventsize LONG
);
```

## 데이터 불러오기

machloader 도구를 이용하여 csv 파일을 입력한다.

```sql
machloader -i -t import_sample -d sample_data.csv
```

## 입력 데이터 확인

입력 데이터를 확인한다.

```
SELECT COUNT(*) FROM import_sample;
```

## 샘플 예제

아래는, 실제 machloader 와 machsql 을 이용한 샘플 예제 과정을 나타낸 것이다.

```sql
Mach> CREATE TABLE import_sample
(
    srcip IPV4,
    srcport INTEGER,
    dstip IPV4,
    dstport INTEGER,
    protocol SHORT,
    eventlog VARCHAR(1024),
    eventcode SHORT,
    eventsize LONG
);
Created successfully.
Mach> quit
```

```bash
[mach@localhost ]$ cd $MACHBASE_HOME/sample/quickstart
[mach@localhost ~]$ ls -l sample_data.csv
-rw-r--r--- 1 mach mach 110477124 2017-02-23 15:18 sample_data.csv
[mach@localhost ~]$ machloader -i -t import_sample -d sample_data.csv
machloader -i -t import_sample -d sample_data.csv -P 16000
-----------------------------------------------------------------
     Machbase Data Import/Export Utility.
     Release Version x.x.x.official
     Copyright 2014, MACHBASE Corporation or its subsidiaries.
     All Rights Reserved.
-----------------------------------------------------------------
PORT           : 16000               NLS            : US7ASCII            
EXECUTE MODE   : IMPORT              TARGET TABLE   : import_sample       
DATA FILE      : sample_data.csv     IMPORT MODE    : APPEND              
FIELD TERM     : ,                   ROW TERM       : \n                  
ENCLOSURE      : "                   ESCAPE         : \                   
ARRIVAL_TIME   : FALSE               ENCODING       : NONE                
HEADER         : FALSE               CREATE TABLE   : FALSE               

 Progress bar                       Imported records        Error records
                                             1000000                    0

Import time         :  0 hour  0 min  2.569 sec 
Load success count  : 1000000
Load fail count     : 0
```
