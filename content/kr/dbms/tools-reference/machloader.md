---
type: docs
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
|-D, –delimiter=DELIMITER|각 필드 구분자 설정. 기본값은 ','입니다.|
|-n, --newline=NEWLINE|각 레코드 구분자 설정. 기본값은 '\n'입니다.|
|-e, --enclosure=ENCLOSURE|각 필드의 둘러싸는 구분자 설정|
|-r, --format=FORMAT|파일 입출력 형식 지정 (기본값: csv)|
|-a, --atime|내장 컬럼 `_ARRIVAL_TIME` 사용 여부 결정. 기본값은 컬럼을 사용하지 않습니다|
|-z, --timezone|타임존 설정 예) +0900 -1230|
|-I, --silent| 저작권 관련 출력 및 가져오기/내보내기 상태 정보를 표시하지 않습니다|
|-h, --help	| 옵션 목록 표시|
|-F, --dateformat=DATEFORMAT| 컬럼 날짜 형식 설정 (`_arrival_time YYYY-MM-DD HH24:MI:SS`)<br> dateformat 대신 'unixtimestamp'를 설정하면 입력 값이 unix 타임스탬프 값으로 간주됩니다. ("time_column unixtimestamp")<br> dateformat 대신 'nanotimestamp'를 설정하면 입력 값이 나노초 단위의 타임스탬프 값으로 간주됩니다. ("time_column nanotimestamp")|
|-E, --encoding=CHARACTER_SET| 입출력 파일의 인코딩 설정. 지원되는 인코딩은 UTF8(기본값), ASCII, MS949, KSC5601, EUCJP, SHIFTJIS, BIG5, GB231280, UTF16입니다.|
|-C, --create| 가져오기 시 테이블이 없으면 테이블을 생성합니다.|
|-H, --header|가져오기/내보내기 시 헤더 정보 존재 여부 설정. 기본값은 설정되지 않습니다|
|-S, --slash|백슬래시 구분자 지정|

자세한 사용법은 다음과 같습니다.

## CSV 파일 가져오기

CSV 파일을 Machbase 서버로 가져옵니다.

옵션:

```
-i: import specification options
-d: data file naming options
-t: table name specification option
```

Example:

```
machloader -i -d data.csv -t table_name
```

## CSV File Export

Writes data to a CSV file.

Option:

```
-o: export specification options
-d: data file naming options
-t: table name specification option
```

Example:

```
machloader -o -d data.csv -t table_name
```

## Use CSV File Header

The header-related setting of the CSV file.

Option:

```
-i -H: Upon import, the first line of the csv file is recognized as a header. Therefore, the first line is excluded from input.
-o -H: Upon export, generates the csv header as the column name of the table.e
```

Example:

```
machloader -i -d data.csv -t table_name -H
machloader -o -d data.csv -t table_name -H
```


## Automatic Table Creation

Regards automatic table creation.

Option:

```
-C: Automatically generates the table when importing. The column names are automatically generated as c0, c1, .... The generated column is varchar (32767) type.
-H: Generates column names with csv header name when importing.
```

Example:

```
machloader -i -d data.csv -t table_name -C
machloader -i -d data.csv -t table_name -C -H
```


## Files Not CSV Format

Sets delimiter for files that are not in CSV format.

Option:

```
-D: Delimiter option for each field
-n: Specifies each record delimiter option
-e: Specifies the enclosing character for each field.
```

Example:

```
machloader -i -d data.txt -t table_name -D '^' -n '\n' -e '"'
machloader -o -d data.txt -t table_name -D '^' -n '\n' -e '"'
```

## Specify Input Mode

When importing (with -i option), there are two modes, REPLACE and APPEND. APPEND is the default. Use REPLACE mode with caution because it deletes existing data.

Option:

```
-m: Specifies import mode
```

Example:

```
machloader -i -d data.csv -t table_name -m replace
```

## Specify Connection Information

Specifies server IP, user, and password separately.

Option:

```
-s: Specifies server IP address (default: 127.0.0.1)
-P: Specifies server port number (default: 5656)
-u: Specifies the connecting user name (default: SYS)
-p: Specifies the password of the connecting user (default: MANAGER)
```

Example:

```
machloader -i -s 192.168.0.10 -P 5656 -u mach -p machbase -d data.csv -t table_name
```

## Create Log File

Creates the execution log file for machloader.

Option:

```
-b: Sets the name of the log file to generate the data that is not input when importing.
-l: Sets the name of the log file to generate the data and error message that were not input when importing.
```

Example:

```
machloader -i -d data.csv -t table_name -b table_name.bad -l table_name.log
```

## Create Schema File

The machloader schema file can be created. Import/export is possible even if the data type format is changed using a schema file or the number of columns in the table and data file is different.

Option:

```
-c: schema file creation options
-t: table name specification option
-f: created schema file name specification option
```

Example:

```
machloader -c -t table_name -f table_name.fmt
machloader -c -t table_name -f table_name.fmt -a
```

## Set datetime Format in Schema File

The date format can be set to preference with the DATEFORMAT option.

Syntax:

```
## Set for all datetime columns.
DATEFORMAT <dateformat>
```
## Set for individual datetime column.

```
DATEFORMAT <column_name> <format>
```

Example:

```
-- Set dateformat for each field in datetest.csv file in the schema file (datetest.fmt).
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
 
-- Import datetest.csv file and check input data.
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

When you do not want to enter a specific field in the CSV file, you can set the IGNORE option in the fmt file.
The ignoretest.csv file has three fields, but if the last field is not needed, specify IGNORE in the column that is not needed in the fmt file.

Example:

```
-- Set ignore option for last field in ignoretest.fmt file.
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
 
 
-- Import ignoretest.csv file and check input data.
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

## If Number of Columns Is More Than Number of Fields

If the number of columns in the table is greater than the number of fields in the data file, only the columns specified in the schema file are entered, and the other columns are entered as NULL.

## If Number of Columns Is Less Than Number of Fields

If the number of columns in the table is less than the number of fields in the data file, fields not in the table must be excluded with the IGNORE option

Example:

```
-- Import ignoretest.csv file and exclude input data by setting ignore option for last field.
loader_test.fmt
table loader_test
{
ID integer;
MSG varchar (40);
SUB_ID integer IGNORE;
}
```
