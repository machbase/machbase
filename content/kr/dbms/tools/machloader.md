---
title : machloader
type : docs
weight: 30
---

마크베이스 서버에 텍스트 파일 데이터를 import/export하기 위해서 machloader를 사용한다. 기본적으로 CSV 파일을 이용하여 동작하지만, 다른 포맷도 지원한다.

machloader의 특징은 다음과 같다.

* machloader는 datetime 형식을 스키마 파일에서 지정할 수 있다. 지정하는 datetime 형식은 마크베이스 서버에서 지원하는 형식이어야 한다. 하나의 datetime 형식을 모든 필드에 적용할 수도 있고, 각 필드마다 다른 형식을 지정할 수도 있다.
* 입력 대상 테이블의 데이터를 삭제하고 입력하려면 "-m replace" 옵션을 사용하면 된다.
* machloader는 스키마와 데이터 파일의 정합성을 검증하지 않는다. 사용자는 스키마, 테이블, 데이터 파일이 정합성을 만족하는지 검사해야만 한다.
* machloader는 APPEND 모드를 기본으로 지원한다.
* machloader는 기본적으로는 "_ARRIVAL_TIME" 컬럼을 사용하지 않는다. 해당 컬럼 데이터를 import/export하려면 "-a" 옵션을 사용하여야 한다.

* machloader의 옵션은 다음 명령으로 볼 수 있다.

```bash
[mach@localhost]$ machloader -h
```

|옵션|설명|
|----|----|
|-s, --server=SERVER|	마크베이스 서버의 IP 주소를 입력한다.(default : 127.0.0.1)|
|-u, --user=USER|	접속할 사용자명을 입력한다.(default : SYS)|
|-p, --password=PASSWORD|	접속할 사용자의 패스워드 (default : MANAGER)|
|-P, --port=PORT|	마크베이스 서버의 포트 번호 (default : 5656)|
|-i, --import|	데이터 import 명령 옵션|
|-o, --export|	데이터 export 명령 옵션|
|-c, --schema| 데이터베이스의 테이블 정보를 이용하여 스키마 파일을 만드는 명령 옵션|
|-t, --table=TABLE_NAME|	스키마 파일을 생성할 테이블 명을 설정|
|-f, --form=SCHEMA_FORM_FILE|	스키마 파일명을 지정|
|-d, --data=DATA_FILE|	데이터 파일명을 지정|
|-l, --log=LOG_FILE|	machloader 실행 로그 파일을 지정|
|-b, --bad=BAD_FILE|-i 옵션 실행시 입력 오류가 발생한 데이터를 기록하며, 에러 설명을 기록하는 파일명을 지정한다.|
|-m, --mode=MODE|-i 옵션 실행시 import 방법을 지시한다. append 또는 replace 옵션이 사용가능 하다. append는 기존 데이터 |이후에 데이터를 입력하고 replace는 기존 데이터를 삭제하고 데이터를 입력한다.|
|-D, –delimiter=DELIMITER|	각 필드 구분자를 설정한다. 기본값은 ','이다.|
|-n, --newline=NEWLINE|	각 레코드 구분자를 설정한다. 기본값은 '\n'이다.|
|-e, --enclosure=ENCLOSURE|	각 필드의 enclosing 구분자를 설정한다.|
|-r, --format=FORMAT|	파일 입력/출력 시 포맷을 지정한다. (default : csv)|
|-a, --atime|	내장 컬럼 "_ARRIVAL_TIME"을 사용할 것인지를 결정한다. 기본값은 사용하지 않는 것이다.|
|-z, --timezone|	Set timezone ex) +0900 -1230|
|-I, --silent|	저작권 관련 출력 및 import/export 상태 정보를 표시하지 않는다.|
|-h, --help|	옵션 리스트를 표시한다.|
|-F, --dateformat=DATEFORMAT|컬럼 dateformat을 설정한다. ("_arrival_time YYYY-MM-DD HH24:MI:SS")<br>\* dateformat 대신 'unixtimestamp' 을 설정하면, 입력되는 값을 unix timestamp 값으로 간주한다. ("time_column unixtimestamp")<br>\* dateformat 대신 'nanotimestamp' 을 설정하면, 입력되는 값을 nanosecond 단위의 timestamp 값으로 간주한다. ("time_column nanotimestamp")<br>`unixtimestamp, nanotimestamp format 은 5.7 부터 지원합니다.`|
|-E, --encoding=CHARACTER_SET|	입/출력하는 파일의 인코딩을 설정한다. 지원되는 인코딩은 UTF8(기본값), ASCII, MS949, KSC5601, EUCJP, SHIFTJIS, BIG5, GB231280, UTF16이다.|
|-C, --create|	import시에 table이 없으면 생성한다.|
|-H, --header|	import/export시에 헤더 정보의 유무를 설정한다. 기본값은 미설정이다.|
|-S, --slash|	backslash 구분자를 지정한다.|

자세한 사용법은 아래와 같다.

## CSV 파일 Import

마크베이스 서버에 CSV 파일을 import한다.

Option:
```bash
-i: import 지정 옵션
-d: 데이터 파일명 지정 옵션
-t: 테이블명 지정 옵션
```

Example:
```bash
machloader -i -d data.csv -t table_name
```

## CSV 파일 Export

데이터를 CSV 파일에 기록한다.

Option:
```sql
-o: export 지정 옵션
-d: 데이터 파일명 지정 옵션
-t: 테이블명 지정 옵션
```
Example:
```bash
machloader -o -d data.csv -t table_name
```

## CSV 파일 헤더 사용

CSV 파일의 헤더 관련 설정이다.

Option:
```bash
-i -H: import 할 때 csv 파일의 첫번째 라인을 헤더로 인식한다. 따라서 첫번째 라인은 입력에서 제외된다.
-o -H: export 할 때 테이블의 컬럼명으로 csv 헤더를 생성한다.
```

Example:
```bash
machloader -i -d data.csv -t table_name -H
machloader -o -d data.csv -t table_name -H
```

## 테이블 자동 생성

테이블 자동 생성에 관련한 내용이다.

Option:
```sql
-C: import할 때 테이블을 자동 생성한다. 컬럼명은 c0, c1, ... 자동으로 생성된다. 생성되는 컬럼은 varchar(32767) 타입이다.
-H: import할 때 csv 헤더명으로 컬럼명을 생성한다.
```

Example:
```sql
machloader -i -d data.csv -t table_name -C
machloader -i -d data.csv -t table_name -C -H
```

## CSV 포맷 이외 파일

CSV 포맷이 아닌 파일에 대해서 구분자를 설정하여 사용한다.

Option:
```bash
-D: 각 필드의 구분자 지정 옵션
-n: 각 레코드 구분자 지정 옵션
-e: 각 필드의 enclosing character 지정 옵션
```

Example:
```bash
machloader -i -d data.txt -t table_name -D '^' -n '\n' -e '"'
machloader -o -d data.txt -t table_name -D '^' -n '\n' -e '"'
```

## 입력 모드 지정

import 시 (-i 옵션 설정 시) REPLACE와 APPEND의 두 가지 모드가 있다. APPEND가 기본값이다. REPLACE 모드인 경우, 기존 데이터를 삭제하므로 주의해야 한다.

Option:
```bash
-m: import 모드 지정
```

Example:
```bash
machloader -i -d data.csv -t table_name -m replace
```

## 접속 정보 지정

서버 IP, 사용자, 패스워드를 별도로 지정한다.

Option:
```sql
-s: 서버 IP 주소 지정 (default: 127.0.0.1)
-P: 서버 포트 번호 지정 (default: 5656)
-u: 접속할 사용자명 지정 (default: SYS)
-p: 접속할 사용자의 패스워드 지정 (default: MANAGER)
```

Example:
```bash
machloader -i -s 192.168.0.10 -P 5656 -u mach -p machbase -d data.csv -t table_name
```

## 로그 파일 생성

machloader의 실행 로그 파일을 생성한다.

Option:
```bash
-b: import할 때 입력되지 않은 데이터를 생성할 로그 파일명 설정한다.
-l: import할 때 입력되지 않은 데이터와 에러 메시지를 생성할 로그 파일명을 설정한다.
```

Example:
```bash
machloader -i -d data.csv -t table_name -b table_name.bad -l table_name.log
```

## 스키마 파일 생성

machloader의 스키마 파일을 생성할 수 있다. 스키마 파일을 이용하여  데이터 타입 형식을 바꾸거나 테이블과 데이터 파일의 컬럼 수가 다른 경우에도 import/export가 가능하다.

Option:
```bash
-c: 스키마 파일 생성 옵션
-t: 테이블명 지정 옵션
-f: 생성될 스키마 파일명 지정 옵션
```

Example:
```bash
machloader -c -t table_name -f table_name.fmt
machloader -c -t table_name -f table_name.fmt -a
```

## 스키마 파일에서 datetime 형식 설정

DATEFORMAT 옵션으로 dateformat을 원하는 대로 설정할 수 있다.

Syntax:

```bash
# 모든 datetime 컬럼에 대해서 설정한다.
DATEFORMAT <dateformat>

# 개별 datetime 컬럼에 대해서 설정한다.
DATEFORMAT <column_name> <format>
```

Example:
```sql
-- 스키마 파일(datetest.fmt)에 datetest.csv 파일의 각 필드에 맞게 dateformat을 설정한다.
datetest.fmt
table datetest
{
INS_DT datetime;
UPT_DT datetime;
}
DATEFORMAT ins_dt "YYYY/MM/DD HH12:MI:SS"
DATEFORMAT upt_dt "YYYY DD MM HH12:MI:SS"
 
datetest.csv
2017/02/20 11:05:23,2017 20 02 11:05:23
2017/02/20 11:06:34,2017 20 02 11:06:34
 
-- datetest.csv 파일을 import 하고 입력된 데이터를 확인한다.
machloader -i -f datetest.fmt -d datetest.csv
-----------------------------------------------------------------
Machbase Data Import/Export Utility.
Release Version 5.1.9.community
Copyright 2014, MACHBASE Corporation or its subsidiaries.
All Rights Reserved.
-----------------------------------------------------------------
Import time : 0 hour 0 min 0.39 sec
Load success count : 2
Load fail count : 0
 
mach> SELECT * FROM datetest;
INS_DT UPT_DT
-------------------------------------------------------------------
2017-02-20 11:06:34 000:000:000 2017-02-20 11:06:34 000:000:000
2017-02-20 11:05:23 000:000:000 2017-02-20 11:05:23 000:000:000
[2] row(s) selected.
Elapsed time: 0.000
```

## IGNORE

CSV 파일의 특정 필드를 입력하려 하지 않을 때, IGNORE 옵션을 fmt 파일에 설정할 수 있다.

ignoretest.csv 파일은 세 개의 필드를 갖지만, 마지막 필드가 필요 없을 경우, fmt 파일에 필요 없는 컬럼에 IGNORE를 명시한다.

Example:
```sql
-- ignoretest.fmt 파일에 마지막 필드에 대해서 ignore 옵션을 설정한다.
ignoretest.fmt
table ignoretest
{
ID integer;
MSG varchar(40);
SUB_ID integer IGNORE;
}
 
ignoretest.csv
1, "msg1", 3
2, "msg2", 4
 
-- ignoretest.csv 파일을 import 하고 입력된 데이터를 확인한다.
machloader -i -f ignoretest.fmt -d ignoretest.csv
-----------------------------------------------------------------
Machbase Data Import/Export Utility.
Release Version 5.1.9.community
Copyright 2014, MACHBASE Corporation or its subsidiaries.
All Rights Reserved.
-----------------------------------------------------------------
NLS : US7ASCII EXECUTE MODE : IMPORT
SCHMEA FILE : ignoretest.fmt DATA FILE : ignoretest.csv
IMPORT_MODE : APPEND FILED TERM : ,
ROW TERM : \n ENCLOSURE : "
ARRIVAL_TIME : FALSE ENCODING : NONE
HEADER : FALSE CREATE TABLE : FALSE
 
Progress bar Imported records Error records
2 0
 
Import time : 0 hour 0 min 0.39 sec
Load success count : 2
Load fail count : 0
 
 
mach> SELECT * FROM ignoretest;
ID MSG
---------------------------------------------------------
2 msg2
1 msg1
[2] row(s) selected.
Elapsed time: 0.000
```

## 컬럼 개수가 필드 개수보다 많은 경우

테이블의 컬럼 개수가 데이터 파일의 필드 개수보다 많은 경우에는 스키마 파일에 지정된 컬럼만 입력되고 다른 컬럼은 NULL로 입력된다.

## 컬럼 개수가 필드 개수보다 적은 경우

테이블의 컬럼 개수가 데이터 파일의 필드 개수보다 적은 경우에는 테이블에 없는 필드는 IGNORE 옵션을 제외하고 입력하여야 한다.

Example:
```sql
-- 마지막 필드에 대해서 ignore 옵션을 설정해서 제외한다.
loader_test.fmt
table loader_test
{
ID integer;
MSG varchar (40);
SUB_ID integer IGNORE;
}
```
