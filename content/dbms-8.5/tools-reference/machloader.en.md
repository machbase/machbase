---
title : machloader
type : docs
weight: 30
---

machloader is used to import/export text file data to the Machbase server. It works with CSV files by default, but it also supports other formats.

The features of machloader are as follows.

* machloader can specify a datetime type in the schema file. The datetime type specified must be of the type supported by the Machbase server. One datetime type can be applied to all fields, and each field can have a different format.
* To delete the data in the target table before importing, use the `-m replace` option.
* machloader does not verify the consistency between the schema and the data file. The user must check that the schema, tables, and data files are consistent.
* machloader supports APPEND mode by default.
* machloader does not use the `_ARRIVAL_TIME` column by default. You must use the `-a` option to import/export the corresponding column data.

For supported date/time formatting tokens, see [TO_CHAR](../../sql-reference/functions/#to_char).

The options for machloader can be seen with the following command:

```bash
[mach@localhost]$ machloader -h
```

|Option| Description|
|--|--|
|-s, --server=SERVER|Enters Machbase server IP address (default: 127.0.0.1)|
|-u, --user=USER|Enters connecting user name (default: SYS)|
|-p, --password=PASSWORD|Connecting user password (default: MANAGER)|
|-P, --port=PORT|Machbase server port number (default: 5656)|
|-i, --import|Data import command option|
|-o, --export|Data export command option|
|-c, --schema|Command option to create schema file using the database table information|
|-t, --table=TABLE_NAME|Sets table name that is creating a schema file|
|-f, --form=SCHEMA_FORM_FILE|Specifies schema filename|
|-d, --data=DATA_FILE|Specifies a data file name|
|-l, --log=LOG_FILE|Specifies a machloader execution log file|
|-b, --bad=BAD_FILE|Records the data in which the input error occurred and specifies the file name that records the error description when executing -i option.|
|-m, --mode=MODE|Indicates import method when executing -i option. The append or replace option is available. Append enters the data after the existing data and replace deletes the existing data and enters the data.|
|-D, --delimiter=DELIMITER|Sets each field delimiter. The default value is ','.|
|-n, --newline=NEWLINE|Sets each record separator. The default is '\n'.|
|-e, --enclosure=ENCLOSURE|Sets the enclosing delimiter for each field.|
|-r, --format=FORMAT|Specifies the format for file input/output. (default: csv)|
|--first=FIRST_ROW|Sets the first row number to process.|
|-a, --atime|Determines whether to use the built-in column `_ARRIVAL_TIME`. The default value is to not use the column.|
|-z, --timezone|Set timezone ex) +0900 -1230|
|-I, --silent| Does not display copyright-related output and import/export status information.|
|-h, --help	| Displays a list of options.|
|-F, --dateformat=DATEFORMAT| Sets the column dateformat. (`_arrival_time YYYY-MM-DD HH24:MI:SS`)<br> If you set 'unixtimestamp' instead of dateformat, the input value is regarded as the unix timestamp value. ("time_column unixtimestamp")<br> If you set 'nanotimestamp' instead of dateformat, the input value is regarded as a timestamp value in nanoseconds. ("time_column nanotimestamp")|
|-E, --encoding=CHARACTER_SET| Sets the encoding of input/output files. Supported encodings are UTF8 (default), ASCII, MS949, KSC5601, EUCJP, SHIFTJIS, BIG5, GB231280, and UTF16.|
|-C, --create| Creates a table if one does not exist upon import.|
|-H, --header|Sets whether header information is present upon import/export. The default value is unset.|
|--summary|Prints the selected option values and exits without importing or exporting data.|
|-S, --slash|Specifies the backslash delimiter.|

The detailed usages are as follows.

## CSV File Import

Imports a CSV file to the Machbase server.

Options:

- `-i`: Specifies import.
- `-d`: Specifies the data file name.
- `-t`: Specifies the table name.

Example:

```
machloader -i -d data.csv -t table_name
```

## CSV File Export

Writes data to a CSV file.

Options:

- `-o`: Specifies export.
- `-d`: Specifies the data file name.
- `-t`: Specifies the table name.

Example:

```
machloader -o -d data.csv -t table_name
```

## Use CSV File Header

The header-related settings of the CSV file.

Options:

- `-i -H`: Upon import, the first line of the CSV file is recognized as a header and excluded from input.
- `-o -H`: Upon export, the column names of the table are written as the CSV header.

Example:

```
machloader -i -d data.csv -t table_name -H
machloader -o -d data.csv -t table_name -H
```

## Automatic Table Creation

Options for automatic table creation.

Options:

- `-C`: Automatically creates the table when importing. The column names are generated as c0, c1, ..., and the column type is `varchar(32767)`.
- `-H`: Uses the CSV header names as the column names when importing.

Example:

```
machloader -i -d data.csv -t table_name -C
machloader -i -d data.csv -t table_name -C -H
```

## Files Not CSV Format

Sets delimiters for files that are not in CSV format.

Options:

- `-D`: Specifies the delimiter for each field.
- `-n`: Specifies the delimiter for each record.
- `-e`: Specifies the enclosing character for each field.

Example:

```
machloader -i -d data.txt -t table_name -D '^' -n '\n' -e '"'
machloader -o -d data.txt -t table_name -D '^' -n '\n' -e '"'
```

## Specify Input Mode

When importing (with the `-i` option), there are two modes, `replace` and `append`. `append` is the default. Use `replace` mode with caution because it deletes existing data.

Options:

- `-m`: Specifies the import mode.

Example:

```
machloader -i -d data.csv -t table_name -m replace
```

## Specify Connection Information

Specifies the server IP, port, user, and password separately.

Options:

- `-s`: Specifies the server IP address (default: 127.0.0.1).
- `-P`: Specifies the server port number (default: 5656).
- `-u`: Specifies the connecting user name (default: SYS).
- `-p`: Specifies the password of the connecting user (default: MANAGER).

Example:

```
machloader -i -s 192.168.0.10 -P 5656 -u mach -p machbase -d data.csv -t table_name
```

## Create Log File

Creates the machloader execution log file and a bad-data file.

Options:

- `-b`: Sets the name of the bad-data file that records the rows that failed to import.
- `-l`: Sets the name of the execution log file that records the rows that failed to import and their error messages.

Example:

```
machloader -i -d data.csv -t table_name -b table_name.bad -l table_name.log
```

## Create Schema File

You can create a machloader schema file. With a schema file, import/export is possible even if the data type format is changed or the number of columns in the table differs from the number of fields in the data file.

Options:

- `-c`: Creates a schema file.
- `-t`: Specifies the table name.
- `-f`: Specifies the name of the schema file to create.

Example:

```
machloader -c -t table_name -f table_name.fmt
machloader -c -t table_name -f table_name.fmt -a
```

## Set datetime Format in Schema File

You can set the date format with the `DATEFORMAT` option.

Syntax for all datetime columns:

```
DATEFORMAT <dateformat>
```

Syntax for an individual datetime column:

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

When you do not want to import a specific field of the CSV file, you can set the `IGNORE` option in the fmt file.
The `ignoretest.csv` file has three fields; if the last field is not needed, specify `IGNORE` for that column in the fmt file.

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

## If Number of Columns Is More Than Number of Fields

If the number of columns in the table is greater than the number of fields in the data file, only the columns specified in the schema file are imported, and the other columns are set to `NULL`.

## If Number of Columns Is Less Than Number of Fields

If the number of columns in the table is less than the number of fields in the data file, the fields that are not in the table must be excluded with the `IGNORE` option.

Example:

```
-- Exclude the input data by setting the IGNORE option on the last field.
loader_test.fmt
table loader_test
{
ID integer;
MSG varchar (40);
SUB_ID integer IGNORE;
}
```
