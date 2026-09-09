---
title : machloader
type : docs
weight: 30
---

machloader는 텍스트 파일 데이터를 Machbase 서버로 가져오거나 내보내는 데 사용됩니다. 기본적으로 CSV 파일과 함께 작동하지만 다른 형식도 지원합니다.

machloader의 기능은 다음과 같습니다.

* machloader는 스키마 파일에서 datetime 타입을 지정할 수 있습니다. 지정된 datetime 타입은 Machbase 서버에서 지원하는 타입이어야 합니다. 하나의 datetime 타입을 모든 필드에 적용할 수 있으며, 각 필드는 다른 형식을 가질 수 있습니다.
* 입력 대상 테이블 데이터를 삭제하고 입력하려면 "-m replace" 옵션을 사용합니다.
* machloader는 스키마와 데이터 파일의 일관성을 확인하지 않습니다. 사용자는 스키마, 테이블 및 데이터 파일이 일관성을 충족하는지 확인해야 합니다.
* machloader는 기본적으로 APPEND 모드를 지원합니다.
* machloader는 기본적으로 `_ARRIVAL_TIME` 컬럼을 사용하지 않습니다. 해당 컬럼 데이터를 가져오거나 내보내려면 "-a" 옵션을 사용해야 합니다.

지원하는 날짜/시간 포맷 토큰은 [TO_CHAR](../../sql-reference/functions/#to_char)을 참고하세요.

machloader의 옵션은 다음 명령으로 확인할 수 있습니다:

```bash
[mach@localhost]$ machloader -h
```

|옵션| 설명|
|--|--|
|-s, --server=SERVER|Machbase 서버 IP 주소 입력 (기본값: 127.0.0.1)|
|-u, --user=USER|연결 사용자 이름 입력 (기본값: SYS)|
|-p, --password=PASSWORD|연결 사용자 비밀번호 (기본값: MANAGER)|
|-P, --port=PORT|Machbase 서버 포트 번호 (기본값: 5656)|
|-i, --import|데이터 가져오기 명령 옵션|
|-o, --export|데이터 내보내기 명령 옵션|
|-c, --schema|데이터베이스 테이블 정보를 사용하여 스키마 파일을 생성하는 명령 옵션|
|-t, --table=TABLE_NAME|스키마 파일을 생성할 테이블 이름 설정|
|-f, --form=SCHEMA_FORM_FILE|스키마 파일 이름 지정|
|-d, --data=DATA_FILE|데이터 파일 이름 지정|
|-l, --log=LOG_FILE|machloader 실행 로그 파일 지정|
|-b, --bad=BAD_FILE|-i 옵션 실행 시 입력 오류가 발생한 데이터를 기록하고 오류 설명을 기록하는 파일 이름 지정|
|-m, --mode=MODE|-i 옵션 실행 시 가져오기 방법 표시. append 또는 replace 옵션을 사용할 수 있습니다. Append는 기존 데이터 뒤에 데이터를 입력하고, replace는 기존 데이터를 삭제한 후 데이터를 입력합니다.|
|-D, --delimiter=DELIMITER|각 필드 구분자 설정. 기본값은 ','입니다.|
|-n, --newline=NEWLINE|각 레코드 구분자 설정. 기본값은 '\n'입니다.|
|-e, --enclosure=ENCLOSURE|각 필드의 둘러싸는 구분자 설정|
|-r, --format=FORMAT|파일 입출력 형식 지정 (기본값: csv)|
|--first=FIRST_ROW|처리할 첫 번째 행 번호 설정|
|-a, --atime|내장 컬럼 `_ARRIVAL_TIME` 사용 여부 결정. 기본값은 컬럼을 사용하지 않습니다|
|-z, --timezone|타임존 설정 예) +0900 -1230|
|-I, --silent| 저작권 관련 출력 및 가져오기/내보내기 상태 정보를 표시하지 않습니다|
|-h, --help	| 옵션 목록 표시|
|-F, --dateformat=DATEFORMAT| 컬럼 날짜 형식 설정 (`_arrival_time YYYY-MM-DD HH24:MI:SS`)<br> dateformat 대신 'unixtimestamp'를 설정하면 입력 값이 unix 타임스탬프 값으로 간주됩니다. ("time_column unixtimestamp")<br> dateformat 대신 'nanotimestamp'를 설정하면 입력 값이 나노초 단위의 타임스탬프 값으로 간주됩니다. ("time_column nanotimestamp")|
|-E, --encoding=CHARACTER_SET| 입출력 파일의 인코딩 설정. 지원되는 인코딩은 UTF8(기본값), ASCII, MS949, KSC5601, EUCJP, SHIFTJIS, BIG5, GB231280, UTF16입니다.|
|-C, --create| 가져오기 시 테이블이 없으면 테이블을 생성합니다.|
|-H, --header|가져오기/내보내기 시 헤더 정보 존재 여부 설정. 기본값은 설정되지 않습니다|
|--summary|선택된 옵션 값을 출력하고, 데이터를 가져오거나 내보내지 않고 종료합니다.|
|-S, --slash|백슬래시 구분자 지정|

자세한 사용법은 다음과 같습니다.

## CSV 파일 가져오기

CSV 파일을 Machbase 서버로 가져옵니다.

옵션:

```
-i: 가져오기 지정 옵션
-d: 데이터 파일 이름 지정 옵션
-t: 테이블 이름 지정 옵션
```

예제:

```
machloader -i -d data.csv -t table_name
```

## CSV 파일 내보내기

데이터를 CSV 파일에 씁니다.

옵션:

```
-o: 내보내기 지정 옵션
-d: 데이터 파일 이름 지정 옵션
-t: 테이블 이름 지정 옵션
```

예제:

```
machloader -o -d data.csv -t table_name
```

## CSV 파일 헤더 사용

CSV 파일의 헤더 관련 설정입니다.

옵션:

```
-i -H: 가져오기 시 CSV 파일의 첫 줄을 헤더로 인식하여 입력에서 제외합니다.
-o -H: 내보내기 시 테이블 컬럼명을 CSV 헤더로 생성합니다.
```

예제:

```
machloader -i -d data.csv -t table_name -H
machloader -o -d data.csv -t table_name -H
```


## 자동 테이블 생성

자동 테이블 생성 관련 옵션입니다.

옵션:

```
-C: 가져오기 시 테이블을 자동 생성합니다. 컬럼명은 c0, c1, ... 순서로 생성되며 타입은 varchar(32767)입니다.
-H: 가져오기 시 CSV 헤더명을 컬럼명으로 사용합니다.
```

예제:

```
machloader -i -d data.csv -t table_name -C
machloader -i -d data.csv -t table_name -C -H
```


## CSV가 아닌 파일 형식

CSV 형식이 아닌 파일에 사용할 구분자를 설정합니다.

옵션:

```
-D: 각 필드 구분자 지정
-n: 각 레코드 구분자 지정
-e: 각 필드의 enclosing 문자 지정
```

예제:

```
machloader -i -d data.txt -t table_name -D '^' -n '\n' -e '"'
machloader -o -d data.txt -t table_name -D '^' -n '\n' -e '"'
```

## 입력 모드 지정

가져오기(`-i`) 시 `replace`와 `append` 두 모드를 사용할 수 있습니다. 기본값은
`append`입니다. `replace` 모드는 기존 데이터를 삭제하므로 주의해서 사용해야 합니다.

옵션:

```
-m: 가져오기 모드 지정
```

예제:

```
machloader -i -d data.csv -t table_name -m replace
```

## 접속 정보 지정

서버 IP, 사용자, 비밀번호를 별도로 지정합니다.

옵션:

```
-s: 서버 IP 주소 지정 (기본값: 127.0.0.1)
-P: 서버 포트 번호 지정 (기본값: 5656)
-u: 접속 사용자 이름 지정 (기본값: SYS)
-p: 접속 사용자 비밀번호 지정 (기본값: MANAGER)
```

예제:

```
machloader -i -s 192.168.0.10 -P 5656 -u mach -p machbase -d data.csv -t table_name
```

## 로그 파일 생성

machloader 실행 로그와 bad-data 파일을 생성합니다.

옵션:

```
-b: 가져오기 실패 행을 기록할 bad-data 파일 이름 지정
-l: 가져오기 실패 행과 오류 메시지를 기록할 실행 로그 파일 이름 지정
```

예제:

```
machloader -i -d data.csv -t table_name -b table_name.bad -l table_name.log
```

## 스키마 파일 생성

machloader 스키마 파일을 생성할 수 있습니다. 스키마 파일을 사용하면 데이터 타입
형식을 변경하거나 테이블과 데이터 파일의 컬럼 수가 다른 경우에도 가져오기/내보내기를
수행할 수 있습니다.

옵션:

```
-c: 스키마 파일 생성 옵션
-t: 테이블 이름 지정 옵션
-f: 생성할 스키마 파일 이름 지정 옵션
```

예제:

```
machloader -c -t table_name -f table_name.fmt
machloader -c -t table_name -f table_name.fmt -a
```

## 스키마 파일에서 datetime 형식 설정

`DATEFORMAT` 옵션으로 날짜 형식을 지정할 수 있습니다.

구문:

```
## 모든 datetime 컬럼에 설정
DATEFORMAT <dateformat>
```
## 개별 datetime 컬럼에 설정

```
DATEFORMAT <column_name> <format>
```

예제:

```
-- 스키마 파일(datetest.fmt)에서 datetest.csv 각 필드의 dateformat을 설정합니다.
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
 
-- datetest.csv 파일을 가져오고 입력 데이터를 확인합니다.
machloader -i -f datetest.fmt -d datetest.csv
-----------------------------------------------------------------
Machbase Data Import/Export Utility.
Release Version 8.5.4.develop
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

CSV 파일의 특정 필드를 입력하지 않으려면 fmt 파일에서 `IGNORE` 옵션을 설정할 수
있습니다. `ignoretest.csv` 파일에는 필드가 3개 있지만 마지막 필드가 필요 없다면,
fmt 파일에서 해당 컬럼에 `IGNORE`를 지정합니다.

예제:

```
-- ignoretest.fmt 파일의 마지막 필드에 IGNORE 옵션을 설정합니다.
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
 
 
-- ignoretest.csv 파일을 가져오고 입력 데이터를 확인합니다.
machloader -i -f ignoretest.fmt -d ignoretest.csv
-----------------------------------------------------------------
Machbase Data Import/Export Utility.
Release Version 8.5.4.develop
Copyright 2014, MACHBASE Corporation or its subsidiaries.
All Rights Reserved.
-----------------------------------------------------------------
NLS : US7ASCII EXECUTE MODE : IMPORT
SCHEMA FILE : ignoretest.fmt DATA FILE : ignoretest.csv
IMPORT_MODE : APPEND FIELD TERM : ,
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

## 컬럼 수가 필드 수보다 많은 경우

테이블의 컬럼 수가 데이터 파일의 필드 수보다 많으면, 스키마 파일에 지정한 컬럼만
입력되고 나머지 컬럼은 `NULL`로 입력됩니다.

## 컬럼 수가 필드 수보다 적은 경우

테이블의 컬럼 수가 데이터 파일의 필드 수보다 적으면, 테이블에 없는 필드는 `IGNORE`
옵션으로 제외해야 합니다.

예제:

```
-- 마지막 필드에 IGNORE 옵션을 설정하여 해당 입력 데이터를 제외합니다.
loader_test.fmt
table loader_test
{
ID integer;
MSG varchar (40);
SUB_ID integer IGNORE;
}
```
