---
type: docs
title: '8.5 Complete Command-Line Tools Reference'
weight: 95
tocSort: true
---


## machadmin


machadmin is used to start up or shut down the Machbase server and to check the creation, deletion, and execution status.

## Option and Features

The options for machadmin are as follows. The functions described in the previous installation section are omitted.

```bash
mach@localhost:~$ machadmin -h
```

| Options| Describe |
|--|--|
|-u, --startup|Starts the Machbase server |
|--recovery[=simple,complex,reset]|Recovery mode used with startup (default: simple) |
|-s, --shutdown |Machbase server shuts down normally |
|-c, --createdb |Creates Machbase database |
| -d, --destroydb| Deletes Machbase database |
| -k, --kill| Force quits Machbase server |
| -i, --silent| Runs with less output |
| -r, --restore |Restores database from backup |
| -x, --extract| Converts backup files to backup directory |
| -w, --viewimage| Displays information of a backup image file |
|-e, --check| Checks Machbase server run status |
|-t, --licinstall| Installs license file |
|-f, --licinfo| Outputs installed license information|
|--home-path=path|Specifies the Machbase home path |

## Recovery Mode

Syntax

```
machadmin -u --recovery=[simple | complex | reset]
```

The recovery mode is as follows:

* simple: If there is no power loss when the server is running, simple recovery mode is run by default.
* complex: The complex recovery mode takes longer to execute than the simple mode. It is executed by default when restarting after the power is turned off.
* reset: When recovery is not performed in simple or complex mode, all data in all tables are checked to recover the database. In this case, some loss of data may occur.

## Server Normal Shutdown

Example:

```
mach@localhost:~$ machadmin -s

-----------------------------------------------------------------
     Machbase Administration Tool
     Release Version - 8.5.4.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-----------------------------------------------------------------
Waiting for the server shut down...
Server shut down successfully.
```

## Create Database

Example:

```
mach@localhost:~$ machadmin -c
-----------------------------------------------------------------
     Machbase Administration Tool
     Release Version - 8.5.4.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-----------------------------------------------------------------
Database created successfully.
```

## Delete Database

Example:

```
mach@localhost:~$ machadmin -d
-----------------------------------------------------------------
     Machbase Administration Tool
     Release Version - 8.5.4.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-----------------------------------------------------------------
Destroy Machbase database- Are you sure?(y/N) y
Database destroyed successfully.
```

## Force to abort Server

Syntax:

```
machadmin -k
```

Example:

```
mach@localhost:~$ machadmin -k
-----------------------------------------------------------------
     Machbase Administration Tool
     Release Version - 8.5.4.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-----------------------------------------------------------------
Waiting for Machbase terminated...
Server terminated successfully.
```

## Run Silent Mode

Removes the message that is output when 'machadmin'  runs.

Syntax:

```
machadmin -i
```

## Database Recovery

Syntax:

```
machadmin -r backup_database_path
```

Example:

```
mach@localhost:~$ machadmin -r 'backup'
-----------------------------------------------------------------
     Machbase Administration Tool
     Release Version - 8.5.4.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-----------------------------------------------------------------
Backed up database restored successfully.
```

## Check server is running

Syntax:

```
machadmin -e
```


Example when server is not running:

```
mach@localhost:~$ machadmin -e
-----------------------------------------------------------------
     Machbase Administration Tool
     Release Version - 8.5.4.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-----------------------------------------------------------------
[ERR] Server is not running.
```


Example when server is running:

```
mach@localhost:~$ machadmin -e
-----------------------------------------------------------------
     Machbase Administration Tool
     Release Version - 8.5.4.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-----------------------------------------------------------------
Machbase server is already running with PID (14098).
```

## Install License File

Syntax:

```
machadmin -t license_file
```


Example:

```
mach@localhost:~$ machadmin -t license.dat
-----------------------------------------------------------------
     Machbase Administration Tool
     Release Version - 8.5.4.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-----------------------------------------------------------------
License installed successfully.
```

## Check License

Example:

```
mach@localhost:~$ machadmin -f
-----------------------------------------------------------------
     Machbase Administration Tool
     Release Version - 8.5.4.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-----------------------------------------------------------------
	                   INFORMATION
ID                                : 00000001
Issue Date                        : 2099-12-31
License Type(Version 3)           : FOGUNLIMITED
Company                           : MACHBASE
Project(Product)                  : NONE
Country Code                      : KR
Install Date                      : 2026-06-13 15:08:00
-----------------------------------------------------------------
License information displayed successfully.
-----------------------------------------------------------------
License information displayed successfully.
```

## machsql


machsql is an interactive tool that performs SQL queries through the terminal screen.

## Run Option Description

```
[mach@localhost]$ machsql -h
```

|Short Option|Full Option| Description|
|--|--|--|
|-s | --server | Connecting server IP address (default: 127.0.0.1)|
|-u | --user | User name (default: SYS)|
|-p | --password | User password (default: MANAGER)|
|-K | --auth-key-file | Authentication private key file path (Machbase 8.5+)|
|-P | --port | Server port number (default: 5656)|
|-n | --nls | NLS configuration|
|-f | --script | SQL script file to run|
|-z | --timezone=+-HHMM | Set Timezone ex) +0900   -1230|
|-o | --output | Filename to save query results|
|-i | --silent | Runs without the copyright notice|
|-v | --verbose | Detailed output|
|-x | --testing | Execute in testing mode|
|-r | --format | Specifies output file format (default: csv)|
|   | --auth-sig-scheme | Authentication signature scheme (`ECDSA`, `RSA_PKCS1_V15`, `RSA_PSS`; Machbase 8.5+)|
|-h | --help | Displays options|
|-c | --connstr | Add connection parameters (supported from version 6.1 or later)|

Example:

```
machsql -s localhost -u sys -p manager
machsql --server=localhost --user=sys --password=manager
machsql -s localhost -u sys -p manager -f script.sql
machsql -s localhost -u app_user -K /opt/machbase/keys/app_user_ecdsa.pem --auth-sig-scheme=ECDSA -f script.sql
## Supported from version 6.1 or later
machsql -s 127.0.0.1 -u sys -p manager -P 8888 -c ALTERNATIVE_SERVERS=192.168.0.147:9209;CONNECTION_TIMEOUT=10
```

## AUTH KEY Challenge Authentication

> **Note**: This feature is supported from Machbase 8.5 or later.

`machsql` supports public-key-based challenge authentication in addition to password
authentication.

### Using Dedicated Options

```bash
machsql -s 127.0.0.1 -u app_user \
    -K /opt/machbase/keys/app_user_ecdsa.pem \
    --auth-sig-scheme=ECDSA \
    -f script.sql
```

```bash
machsql -s 127.0.0.1 -u app_user \
    -K /opt/machbase/keys/app_user_rsa.pem \
    --auth-sig-scheme=RSA_PSS \
    -f script.sql
```

Notes:

- `-K`, `--auth-key-file` internally enables `AUTH_MODE=CHALLENGE`.
- If `--auth-sig-scheme` is omitted, the default scheme is chosen from the key algorithm.
  - ECDSA key: `ECDSA`
  - RSA key: `RSA_PKCS1_V15`
- Supported key parameters are ECDSA `P-256`, `P-384`, `P-521` and RSA `2048`, `3072`,
  `4096` bits.
- To use RSA-PSS authentication, specify `--auth-sig-scheme=RSA_PSS`.
- `-p` is not used for authentication when `AUTH_MODE=CHALLENGE`.
- On POSIX systems, restricting the private key file permission to `600` is recommended.

### Using a Connection String

```bash
machsql -c "SERVER=127.0.0.1;PORT_NO=5656;UID=APP_USER;AUTH_MODE=CHALLENGE;AUTH_SIG_SCHEME=ECDSA;AUTH_KEY_FILE=/opt/machbase/keys/app_user_ecdsa.pem;" -f script.sql
```

Because the connection string form may expose the key file path in process arguments or
logs, using `-K` is recommended when possible.

### Failure Cases

- Authentication fails if the key file does not exist.
- Authentication fails if the key type does not match `AUTH_SIG_SCHEME`.
- Expired (`VALID_BEFORE`) or deactivated AUTH KEY entries cannot be used for
  authentication.

## Environment Variable MACHBASE_CONNECTION_STRING

Specifies basic connection parameters. For example, to add CONNECTION_TIMEOUT, ALTERNATIVE_SERVERS, you may use environment variable setting below.

```
export MACHBASE_CONNECTION_STRING=ALTERNATIVE_SERVERS=192.168.0.148:8888;CONNECTION_TIMEOUT=3
```

Setting connection parameter with -c option, it takes precedence over environment variables. This option is supported from version 6.1 or later


## Using HEREDOC for SQL Scripts

machsql supports HEREDOC (Here Document) syntax, allowing you to pass SQL commands directly from the shell without creating a separate file. This is particularly useful for automation scripts and one-time SQL execution.

> **Note**: This feature is supported from Machbase version 8.0.50 or later.

### Basic Syntax

```bash
machsql -s <server> -u <user> -p <password> <<'DELIMITER'
SQL statements here
DELIMITER
```

The delimiter can be any string (commonly `EOF`, `SQL`, or `SQLBLOCK`). Using quotes around the delimiter (`<<'DELIMITER'`) prevents shell variable expansion.

### Examples

**Simple query execution:**

```bash
machsql -s 127.0.0.1 -u sys -p manager <<'SQLBLOCK'
select 'WORKS!!!!' from v$tables limit 2;
SQLBLOCK
```

**Multiple statements:**

```bash
machsql -s 127.0.0.1 -u sys -p manager <<'EOF'
CREATE TABLE test_table (id INTEGER, name VARCHAR(100));
INSERT INTO test_table VALUES (1, 'First Record');
INSERT INTO test_table VALUES (2, 'Second Record');
SELECT * FROM test_table;
DROP TABLE test_table;
EOF
```

**Using variables (without quotes on delimiter):**

```bash
TABLE_NAME="my_table"
machsql -s 127.0.0.1 -u sys -p manager <<EOF
SELECT COUNT(*) FROM ${TABLE_NAME};
EOF
```

**With output redirection:**

```bash
machsql -s 127.0.0.1 -u sys -p manager <<'SQL' > output.csv
SELECT name, time, value FROM tag_table
WHERE time >= NOW - INTERVAL 1 HOUR
ORDER BY time DESC;
SQL
```

### Benefits of HEREDOC

1. **No temporary files**: Execute SQL without creating separate script files
2. **Inline scripts**: Embed SQL directly in shell scripts for better readability
3. **Automation**: Simplify deployment and maintenance scripts
4. **Variable substitution**: Use shell variables in SQL when needed (without quotes)

### Notes

- Use quotes around the delimiter (`<<'DELIMITER'`) to prevent variable expansion
- Remove quotes (`<<DELIMITER`) if you want to use shell variables in your SQL
- The delimiter must appear alone on a line to terminate the HEREDOC
- Works with all machsql command-line options


## SHOW Command

Displays information such as tables, tablespaces, and indexes.

SHOW command list:

* SHOW INDEX
* SHOW INDEXES
* SHOW INDEXGAP
* SHOW LSM
* SHOW LICENSE
* SHOW STATEMENTS
* SHOW STORAGE
* SHOW TABLE
* SHOW TABLES
* SHOW TABLESPACE
* SHOW TABLESPACES
* SHOW USERS

### SHOW INDEX
Displays index information.

Syntax:

```
SHOW INDEX index_name
```

Example:

```
Mach> CREATE TABLE t1 (c1 INTEGER, c2 VARCHAR(10));
Created successfully.
Mach> CREATE VOLATILE TABLE t2 (c1 INTEGER, c2 VARCHAR(10));
Created successfully.
Mach> CREATE INDEX t1_idx1 ON t1(c1) INDEX_TYPE LSM;
Created successfully.
Mach> CREATE INDEX t1_idx2 ON t1(c2) INDEX_TYPE BITMAP;
Created successfully.
Mach> CREATE INDEX t2_idx1 ON t2(c1) INDEX_TYPE REDBLACK;
Created successfully.
Mach> CREATE INDEX t2_idx2 ON t2(c2) INDEX_TYPE REDBLACK;
Created successfully.

Mach> SHOW INDEX t1_idx2;
TABLE_NAME                                          COLUMN_NAME                                         INDEX_NAME                                          INDEX_TYPE   KEY_COMPRESS  MAX_LEVEL
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
PART_VALUE_COUNT BITMAP_ENCODE
-----------------------------------
T1                                                  C2                                                  T1_IDX2                                             LSM          COMPRESSED    2
100000           EQUAL
[1] row(s) selected.
```

### SHOW INDEXES

Displays entire index list.

**Syntax:**

```
SHOW INDEXES
```

**Example:**

```sql
Mach> CREATE TABLE t1 (c1 INTEGER, c2 VARCHAR(10));
Created successfully.
Mach> CREATE VOLATILE TABLE t2 (c1 INTEGER, c2 VARCHAR(10));
Created successfully.
Mach> CREATE INDEX t1_idx1 ON t1(c1) INDEX_TYPE LSM;
Created successfully.
Mach> CREATE INDEX t1_idx2 ON t1(c2) INDEX_TYPE BITMAP;
Created successfully.
Mach> CREATE INDEX t2_idx1 ON t2(c1) INDEX_TYPE REDBLACK;
Created successfully.
Mach> CREATE INDEX t2_idx2 ON t2(c2) INDEX_TYPE REDBLACK;
Created successfully.

Mach> SHOW INDEXES;
USER_NAME             TABLE_NAME                                          COLUMN_NAME                                         INDEX_NAME                                          INDEX_TYPE
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
SYS                   T1                                                  C1                                                  T1_IDX1                                             LSM
SYS                   T1                                                  C2                                                  T1_IDX2                                             LSM
SYS                   T2                                                  C2                                                  T2_IDX2                                             REDBLACK
SYS                   T2                                                  C1                                                  T2_IDX1                                             REDBLACK
[4] row(s) selected.
```

### SHOW INDEXGAP

Displays index building GAP information.

Example:

```
Mach> SHOW INDEXGAP
TABLE_NAME                                INDEX_NAME                                GAP
-------------------------------------------------------------------------------------------------------------
INDEX_TABLE                               T1_IDX1                                   0
INDEX_TABLE                               T1_IDX2                                   0
```

### SHOW LSM

Displays LSM index building information.

Example:

```
Mach> SHOW LSM;
TABLE_NAME                                INDEX_NAME                                LEVEL       COUNT
--------------------------------------------------------------------------------------------------------------------------
T1                                        IDX1                                      0           0
T1                                        IDX1                                      1           100000
T1                                        IDX1                                      2           0
T1                                        IDX1                                      3           0
T1                                        IDX2                                      0           100000
T1                                        IDX2                                      1           0
[6] row(s) selected.
```

### SHOW LICENSE

Displays license information.

Example:

```
Mach> SHOW LICENSE
INSTALL_DATE          ISSUE_DATE            EXPIRY_DATE  TYPE        POLICY
---------------------------------------------------------------------------------------
2016-07-01 10:24:37   20160325              20170325    2           0
[1] row(s) selected.
```

### SHOW STATEMENTS

Displays all query statements (Prepare, Execute, Fetch) registered in the server.

Example:

```
Mach> SHOW STATEMENTS
USER_ID     SESSION_ID  QUERY
--------------------------------------------------------------------------------------------------------------
0           2           SELECT ID USER_ID, SESS_ID SESSION_ID, QUERY FROM V$STMT
[1] row(s) selected.
```

### SHOW STORAGE

Displays the disk usage for each table created by the user.

Syntax:

```
SHOW STORAGE
```

Example:

```
Mach> CREATE TAG TABLE TAG (name varchar(20) primary key, time datetime basetime, value double summarized);
Created successfully.

Mach> SHOW STORAGE
TABLE_NAME                                          DATA_SIZE            INDEX_SIZE           TOTAL_SIZE
------------------------------------------------------------------------------------------------------------------------
_TAG_DATA_0                                         50335744             0                    50335744
_TAG_DATA_1                                         50335744             0                    50335744
_TAG_DATA_2                                         50335744             0                    50335744
_TAG_DATA_3                                         50335744             0                    50335744
_TAG_META                                           0                    0                    0
```

### SHOW TABLE

Displays information about the table created by the user.

Syntax:

```
SHOW TABLE table_name
```

Example:

```
Mach> CREATE TABLE t1 (c1 INTEGER, c2 VARCHAR(10));
Created successfully.
Mach> CREATE INDEX t1_idx1 ON t1(c1) INDEX_TYPE LSM;
Created successfully.
Mach> CREATE INDEX t1_idx2 ON t1(c1) INDEX_TYPE BITMAP;
Created successfully.

Mach> SHOW TABLE T1
[ COLUMN ]
----------------------------------------------------------------
NAME                          TYPE                LENGTH
----------------------------------------------------------------
C1                            integer             11
C2                            varchar             10

[ INDEX ]
----------------------------------------------------------------
NAME                          TYPE                COLUMN
----------------------------------------------------------------
T1_IDX1                       LSM                 C1
T1_IDX2                       LSM                 C1
```

### SHOW TABLES

Displays a list of all tables created by the user.

Example:

```
Mach> SHOW TABLES
NAME
--------------------------------------------
BONUS
DEPT
EMP
SALGRADE
[4] row(s) selected.
```

### SHOW TABLESPACE

Displays tablespace information.

Example:

```
Mach> CREATE TABLE t1 (id integer);
Created successfully.
Mach> CREATE INDEX t1_idx_id ON t1(id);
Created successfully.

Mach> SHOW TABLESPACE SYSTEM_TABLESPACE;
[TABLE]
NAME                                      TYPE
-------------------------------------------------------
T1                                        LOG
[1] row(s) selected.

[INDEX]
TABLE_NAME                                COLUMN_NAME                               INDEX_NAME
----------------------------------------------------------------------------------------------------------------------------------
T1                                        ID                                        T1_IDX_ID
[1] row(s) selected.
```

### SHOW TABLESPACES

Displays a complete list of tablespaces.

Example:

```
Mach> CREATE TABLESPACE tbs1 DATADISK disk1 (DISK_PATH="tbs1_disk1"), disk2 (DISK_PATH="tbs1_disk2"), disk3 (DISK_PATH="tbs1_disk3");
Created successfully.

-- Insert data here
...
...


Mach> SHOW TABLESPACES;
NAME                                                                              DISK_COUNT  USAGE
-----------------------------------------------------------------------------------------------------------------------
SYSTEM_TABLESPACE                                                                 1           0
TBS1                                                                              3           25824256
[2] row(s) selected.
```

### SHOW USERS

Displays a list of users.

Example:

```
Mach> CREATE USER testuser IDENTIFIED BY 'test1234';
Created successfully.

Mach> SHOW USERS;
USER_NAME
--------------------------------------------
SYS
TESTUSER
[2] row(s) selected.
```

## machloader


machloader is used to import/export text file data to the Machbase server. It works with CSV files by default, but it also supports other formats.

The features of machloader are as follows.

* machloader can specify a datetime type in the schema file. The datetime type specified must be of the type supported by the Machbase server. One datetime type can be applied to all fields, and each field can have a different format.
* To delete and input the input target table data, use the "-m replace" option.
* machloader does not verify the schema and data file consistency. The user must check that the schema, tables, and data files meet the consistency.
* machloader supports APPEND mode by default.
* machloader does not use the `_ARRIVAL_TIME` column by default. You must use the "-a" option to import/export the corresponding column data.

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

Imports CSV file to Machbase server.

Option:

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
-o -H: Upon export, generates the csv header as the column name of the table.
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

## csv


'csvimport' and 'csvexport' are tools used to import/export CSV files to the Machbase server.

The options have been simplified for simpler use of the CSV file using the machloader.

In addition to the options described below, all options available in machloader are available.

For supported date/time formatting tokens, see [TO_CHAR](../../sql-reference/functions/#to_char).

## Common Wrapper Options

The CSV wrappers expose the following frequently used machloader options:

|Option|Applies to|Description|
|--|--|--|
|-P, --port=PORT|csvimport, csvexport|Server port number (default: 5656)|
|-l, --log=LOG_FILE|csvimport, csvexport|Execution log file|
|-b, --bad=BAD_FILE|csvimport|Bad-data file for rows that fail during import|
|-m, --mode=MODE|csvimport|Import mode (`append` or `replace`; default: `append`)|
|-a, --atime|csvimport, csvexport|Include the `_ARRIVAL_TIME` column|
|-I, --silent|csvimport, csvexport|Produce less output|
|-F, --dateformat=DATEFORMAT|csvimport, csvexport|Date format for columns, such as `_arrival_time YYYY-MM-DD HH24:MI:SS`|

## csvimport

CSV files can be easily entered into the server using csvimport.

### Basic Usage

Enter the table name and data file name according to the following options.

Options:

```
-t: table name specification option
-d: data file naming options
* You can do this with just the table name and data file name without specifying the option.
```

Example:

```
csvimport -t table_name -d table_name.csv
csvimport table_name file_path
csvimport file_path table_name
```

### CSV Header Exception

Use the following option to enter the CSV file except for the header at the time of input.

Options:

```
-H: Treats the first line of the CSV file as a header and excludes it from imported data.
```

Example:

```
csvimport -t table_name -d table_name.csv -H
```

### Automatic Table Creation

If a table is not created to be entered at the time of input, the table can be created at the same time through the following options.

Option

```
-C: Automatically creates the table during import. Column names are automatically created as c0, c1, .... The created column is varchar (32767) type.
-H: Creates column name with csv header name during import.
```

Example:

```
csvimport -t table_name -d table_name.csv -C
csvimport -t table_name -d table_name.csv -C -H
```


## csvexport

The database table data can be easily exported to the CSV file with 'csvexport'.

### Basic Usage

Option:

```
-t: table name specification option
-d: data file naming options
* You can do this with just the table name and data file name without specifying the option.
```

Example:

```
csvexport -t table_name -d table_name.csv
csvexport table_name file_path
csvexport file_path table_name
```

### Using CSV Header

With the following option, you can add a header to the CSV file to be exported with a column name.

Option:

```
-H: Creates the header of the csv file with the table column name.
```

Example:

```
csvexport -t table_name -d table_name.csv -H
```

## machcoordinatoradmin


Coordinator is a cluster-wide management tool.

Only exists in Cluster Edition Package.

## Options and Features

The options for machcoordinatoradmin are as follows. The functions described in the previous section are omitted.

```
mach@localhost:~$ machcoordinatoradmin -h
```


|Options| Description|
|--|--|
|-u, --startup | Runs the Coordinator process|
|-s, --shutdown | Terminates Coordinator process|
|-k, --kill| Stops Coordinator process|
|-c, --createdb | Creates Coordinator meta|
|-d, --destroydb| Removes Coordinator meta, Deletes the package files in $MACHBASE_COORDINATOR_HOME/package|
|-e, --check | Checks that the Coordinator process is running|
|-i, --silent | Mutes the banner|
|--configuration[=name] | Outputs keys and values in configuration settings (only certain keys can be output)|
|--configure | Lists the system properties |
|--activate | Switches Cluster status to Service|
|--deactivate | Switches Cluster status to Deactivate|
|--list-package[=package] | Lists information of registered packages (only specific packages can be output)|
|--add-package=package | Adds package|
|--remove-package=package | Deletes package|
|--list-node[=node] | Lists information of nodes (only specific nodes can be output)|
|--add-node=node | Adds node|
|--remove-node=node | Deletes node|
|--attach-node=node | Attaches an existing node to cluster metadata|
|--detach-node=node | Detaches a node from cluster metadata|
|--upgrade-node=node | Upgrades node|
|--startup-node=node | Runs node|
|--shutdown-node=node | Terminates node|
|--kill-node=node | Stops node|
|--startup-lookup | Starts lookup nodes|
|--shutdown-lookup | Stops lookup nodes|
|--set-lookup-master=node | Sets the lookup master node|
|--cluster-status | Outputs each node status of the cluster|
|--cluster-status-full | Outputs of each node status of cluster in detail|
|--verbose | Prints deployer status together in cluster status output|
|--cluster-node | Outputs information of cluster|
|--set-group-state=`[normal | readonly]` | Changes the status of a specific warehouse group|
|--set-warehouse-state=`[normal | scrapped]` | Changes the state of the warehouse node specified by `--node`|
|--force-restore-warehouse=node | Force-restores a scrapped warehouse node|
|--get-host-resource | Outputs host resource information where each node is located|
|--host-resource-enable | Starts collecting Host resource information of each node|
|--host-resource-disable | Stops collecting Host resource information for each node|
|--deactivate-broker=node | Changes the specified node to inactive state|
|--activate-broker=node | Changes the specified node to normal state|
|--snapshot-interval=sec | Sets the snapshot interval|
|--exec-snapshot | Executes a snapshot (requires `--group`)|
|--snapshot-recover=node | Recovers snapshot data for the specified node|
|--exec-sync=node | Executes sync for the specified node|
|--snapshot-clean | Cleans snapshots|

|Additional Options|Description|Required Options|
|--|--|--|
|--file-name=filename | File name| --add-package|
|--port-no=portno | Service port number| --add-node, --attach-node|
|--http-port-no=portno | HTTP administration port number| --add-node, --attach-node|
|--deployer=node | Deployer node name| --add-node|
|--package-name=packagename | Package name to use as the installation source| --add-node, --upgrade-node|
|--home-path=path | Installation path of the current node, based on the Deployer server| --add-node, --attach-node|
|--node-type=`[broker | warehouse | lookup]` | Node type| --add-node, --attach-node |
|--lookup-type=`[master | slave | monitor]` | Lookup node type| --add-node, --attach-node |
|--node=node | Target node name or alias for state changes| --set-warehouse-state|
|--alias=alias | Alias of the node to add or attach| --add-node, --attach-node|
|--dbs-path=path | Database file path for broker/warehouse nodes| --add-node|
|--group=groupname | Group name of the node to install| --add-node, --attach-node, --set-group-state, --exec-snapshot |
|--replication=host:port | host:port to exchange replication| --add-node, --attach-node |
|--no-replicate |Does not use Replication on the node to install |--add-node, --attach-node|
|--primary=host:port | Specifies the node name of the Primary Coordinator when installing the Secondary Coordinator |-u, --startup|
|--host=host | Specifies specific host to output Host resource information| --get-host-resource|
|--metric=`[cpu|memory|disk|network]` | Specifies specific metric to output Host resource information| --get-host-resource|

## Check Running Status

Example:

```
mach@localhost:~$ machcoordinatoradmin -e
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
Machbase Coordinator is running with pid(29245)!
```

## Create / Delete Meta

Example:

```
mach@localhost:~$ machcoordinatoradmin -c
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
Coordinator metadata created successfully.

mach@localhost:~$ machcoordinatoradmin -d
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
Coordinator metadata destroyed successfully.
```

## Output Configuration

Syntax:

```
machcoordinatoradmin --configuration[=name]
```

Example:

```
mach@localhost:~$ machcoordinatoradmin --configuration
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
Name  : CLUSTER
Value : 3

Name  : DECISION
Value : ON

Name  : HOST-RESOURCE
Value : OFF

mach@localhost:~$ machcoordinatoradmin --configuration=decision
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
              Name : DECISION
             Value : ON
            Format : text/plain
```

## List the system properties

Syntax

```
machcoordinatoradmin --configure
```

Example

```
mach@localhost:~$ machcoordinatoradmin --configure

CLUSTER_LINK_HOST=192.168.0.30
CLUSTER_LINK_PORT_NO=36110
CLUSTER_LINK_THREAD_COUNT=16
CLUSTER_LINK_MAX_LISTEN=512
CLUSTER_LINK_MAX_POLL=4096
CLUSTER_LINK_ACCEPT_TIMEOUT=5000000
CLUSTER_LINK_CHECK_INTERVAL=1000000
CLUSTER_LINK_CONNECT_RETRY_TIMEOUT=60000000
CLUSTER_LINK_CONNECT_TIMEOUT=5000000
CLUSTER_LINK_HANDSHAKE_TIMEOUT=5000000
CLUSTER_LINK_LONG_TERM_CALLBACK_INTERVAL=1000000
CLUSTER_LINK_LONG_WAIT_INTERVAL=1000000
CLUSTER_LINK_RECEIVE_TIMEOUT=5000000
CLUSTER_LINK_REQUEST_TIMEOUT=60000000
CLUSTER_LINK_SEND_TIMEOUT=5000000
CLUSTER_LINK_SESSION_TIMEOUT=3600000000
CLUSTER_LINK_ERROR_ADD_ORIGIN_HOST=0
CLUSTER_LINK_BUFFER_SIZE=33554432
..
..
```


## Change Cluster Status

Example:

```
mach@localhost:~$ machcoordinatoradmin --activate
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
              Name : CLUSTER
             Value : 3
            Format : text/plain


mach@localhost:~$ machcoordinatoradmin --deactivate
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
              Name : CLUSTER
             Value : 0
            Format : text/plain
```

## List Package Information

Syntax:

```
machcoordinatoradmin --list-package[=package]
```

Example:

```
mach@localhost:~$ machcoordinatoradmin --list-package
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
Package Name : machbase
File Name    : machbase-cluster-6bab497c9.develop-LINUX-X86-64-release-lightweight.tgz
File Size    : 64630670 bytes

Package Name : machbase2
File Name    : machbase-cluster-e3c0717.develop-LINUX-X86-64-release-lightweight.tgz
File Size    : 64677030 bytes


mach@localhost:~$ machcoordinatoradmin --list-package=machbase
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
Package Name : machbase
File Name    : machbase-cluster-6bab497c9.develop-LINUX-X86-64-release-lightweight.tgz
File Size    : 64630670 bytes
```

## Add Node, Alias, And DBS_PATH

When adding a broker or warehouse node, specify `--node-type`, `--deployer`, `--package-name`, `--home-path`, and `--port-no` together. If an HTTP administration port is required, specify `--http-port-no`.

Example:

```
machcoordinatoradmin \
  --add-node=192.168.0.32:5401 \
  --node-type=warehouse \
  --deployer=192.168.0.32:5201 \
  --package-name=machbase \
  --home-path=/home/machbase/warehouse_a1 \
  --port-no=5400 \
  --http-port-no=5402 \
  --group=Group1 \
  --alias=warehouse-a1 \
  --dbs-path=/data/machbase/warehouse_a1_dbs
```

When adding or attaching a lookup node, specify `--node-type=lookup` and `--lookup-type` together.

Example:

```
machcoordinatoradmin \
  --add-node=192.168.0.32:5601 \
  --node-type=lookup \
  --lookup-type=master \
  --deployer=192.168.0.32:5201 \
  --package-name=machbase \
  --home-path=/home/machbase/lookup1 \
  --alias=lookup-master-1
```

Use `--attach-node` to attach an existing node to cluster metadata. `--attach-node` can use `--alias`, but it cannot use `--dbs-path`.

```
machcoordinatoradmin \
  --attach-node=192.168.0.32:5401 \
  --node-type=warehouse \
  --home-path=/home/machbase/warehouse_a1 \
  --port-no=5400 \
  --http-port-no=5402 \
  --group=Group1 \
  --alias=warehouse-a1
```

`--alias` can be specified with `--add-node` and `--attach-node`. If it is omitted, the coordinator automatically generates an alias in the form `coordinator-N`, `deployer-N`, `broker-N`, `warehouse-N`, or `lookup-N` according to the node type.

An alias must be at least one character and can contain only letters, digits, `-`, `_`, and `.`. It must be unique across the cluster and must not collide with any real node name.

There is no separate command to change only the alias after registration.

When resolving a command target, the coordinator checks the real node name first and then checks the alias. Therefore aliases can be used with `--startup-node`, `--shutdown-node`, `--kill-node`, `--remove-node`, `--detach-node`, `--upgrade-node`, `--set-lookup-master`, `--set-warehouse-state`, `--force-restore-warehouse`, `--snapshot-recover`, and `--exec-sync`. Status output can display a node as `alias(real-node-name)` when an alias exists.

`--dbs-path` can be used only when adding a broker or warehouse node with `--add-node`. It cannot be used for lookup, coordinator, or deployer nodes, and it cannot be combined with other commands such as `--attach-node` or `--upgrade-node`.

The `--dbs-path` value must start with `/` or `?`. Newlines, tabs, and trailing blanks are not allowed. Values that directly specify system paths such as `/`, `/etc`, `/usr`, `/home`, and `/bin` are rejected. A real data directory under a system path, such as `/home/machbase/warehouse_a1_dbs`, can be specified as a separate directory.

When an absolute path is specified as a custom `DBS_PATH`, the directory must not exist when the node is added. The deployer creates the directory before running `machadmin -c`. If the directory already exists, adding the node fails with `DBS_PATH already exists`. If `--dbs-path` is omitted, the broker/warehouse configuration records the default value `DBS_PATH = ?/dbs`. When a broker/warehouse node is removed with `--remove-node`, an explicit absolute `DBS_PATH` is cleaned up separately from the node home path.


## List Node Information

Syntax:

```
machcoordinatoradmin --list-node[=node]
```

Example:

```
mach@localhost:~$  machcoordinatoradmin --list-node
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
Node Name             : 192.168.0.32:5101
Node Type             : coordinator
HTTP Admin Port       : 5102
Group Name            : Coordinator
Desired State         : primary
Actual State          : primary
Coordinator Host      : 192.168.0.32:5101
Last Response Time    : 497590
Last Modify Time      : 421020408
Last Response Elapsed : 1006148

Node Name             : 192.168.0.32:5201
Node Type             : deployer
Group Name            : Deployer
Desired State         : normal
Actual State          : normal
Coordinator Host      : 192.168.0.32:5101
Last Response Time    : 497594
Last Modify Time      : 404915419
Last Response Elapsed : 1006128

Node Name             : 192.168.0.32:5301
Node Type             : broker
Port Number           : 5757
Http Port             : 5302
Deployer              : 192.168.0.32:5201
Package Name          : machbase
Home Path             : /home/machbase/broker1
Group Name            : Broker
Desired State         : leader
Actual State          : leader
Coordinator Host      : 192.168.0.32:5101
Last Response Time    : 497544
Last Modify Time      : 353606480
Last Response Elapsed : 1006157

Node Name             : 192.168.0.32:5401
Node Type             : warehouse
Port Number           : 5400
Http Port             : 5402
Deployer              : 192.168.0.32:5201
Package Name          : machbase
Home Path             : /home/machbase/warehouse_a1
Group Name            : Group1
Desired State         : normal
Actual State          : normal
Coordinator Host      : 192.168.0.32:5101
Last Response Time    : 497556
Last Modify Time      : 332480933
Last Response Elapsed : 1006160

mach@localhost:~$  machcoordinatoradmin --list-node=192.168.0.32:5401
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
Node Name             : 192.168.0.32:5401
Node Type             : warehouse
Port Number           : 5400
Http Port             : 5402
Deployer              : 192.168.0.32:5201
Package Name          : machbase
Home Path             : /home/cumulus/warehouse_a1
Group Name            : Group1
Desired State         : normal
Actual State          : normal
Coordinator Host      : 192.168.0.32:5101
Last Response Time    : 648879
Last Modify Time      : 419153148
Last Response Elapsed : 1005962
```


## Output Cluster Node Status

Example:

```
mach@localhost:~$ machcoordinatoradmin --cluster-status
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
+-------------+-------------------+-------------------+-------------------+--------------+
|  Node Type  |     Node Name     |    Group Name     |    Group State    |     State    |
+-------------+-------------------+-------------------+-------------------+--------------+
| coordinator | 192.168.0.32:5101 | Coordinator       | normal            | primary      |
| deployer    | 192.168.0.32:5201 | Deployer          | normal            | normal       |
| broker      | 192.168.0.32:5301 | Broker            | normal            | leader       |
| warehouse   | 192.168.0.32:5401 | Group1            | normal            | normal       |
+-------------+-------------------+-------------------+-------------------+--------------+

mach@localhost:~$ machcoordinatoradmin --cluster-status-full
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
+-------------+-------------------+-------------------+-------------------+-------------------------------+-------------+
|  Node Type  |     Node Name     |    Group Name     |    Group State    |    Desired & Actual State     |  RP State   |
+-------------+-------------------+-------------------+-------------------+-------------------------------+-------------+
| coordinator | 192.168.0.32:5101 | Coordinator       | normal            | primary       | primary       | ----------- |
| deployer    | 192.168.0.32:5201 | Deployer          | normal            | normal        | normal        | ----------- |
| broker      | 192.168.0.32:5301 | Broker            | normal            | leader        | leader        | ----------- |
| warehouse   | 192.168.0.32:5401 | Group1            | normal            | normal        | normal        | ----------- |
+-------------+-------------------+-------------------+-------------------+-------------------------------
```


## Output Cluster Information

Example:

```
mach@localhost:~$ machcoordinatoradmin --cluster-node
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
Token Pid      : 29245
Token Time     : 1553153902646178
Modify Time    : 1553154010296715
Modify Count   : 8
Cluster Status : Service
Broker         : 192.168.0.32:5301
Warehouse      : 192.168.0.32:5401
```


## Change Group State

Syntax:

```
machcoordinatoradmin --set-group-state=[ normal | readonly ] --group=group
```

Example:

```
mach@localhost:~$ machcoordinatoradmin --set-group-state=readonly --group=Group1
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
Group Name: Group1
Flag      : 1

mach@localhost:~$ machcoordinatoradmin --cluster-status
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
+-------------+-------------------+-------------------+-------------------+--------------+
|  Node Type  |     Node Name     |    Group Name     |    Group State    |     State    |
+-------------+-------------------+-------------------+-------------------+--------------+
| coordinator | 192.168.0.32:5101 | Coordinator       | normal            | primary      |
| deployer    | 192.168.0.32:5201 | Deployer          | normal            | normal       |
| broker      | 192.168.0.32:5301 | Broker            | normal            | leader       |
| warehouse   | 192.168.0.32:5401 | Group1            | readonly          | normal       |
+-------------+-------------------+-------------------+-------------------+--------------+
```

## Output Host Resource

Syntax:

```
machcoordinatoradmin --host-resource-enable [--metric=metric] [host=host]
```

Example:

```
mach@localhost:~$ machcoordinatoradmin --host-resource-enable
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
              Name : HOST-RESOURCE
             Value : ON
            Format : text/plain

mach@localhost:~$ machcoordinatoradmin --get-host-resource
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
Host Name : 192.168.0.32
   CPU Info :
      Model Name          : Intel(R) Xeon(R) CPU E3-1231 v3 @ 3.40GHz
      Number of CPUs      : 8
      Number of CPU Cores : 4
      CPU Utilization     : 14.0%
      CPU IOWait Ratio    : 0.0%
   Memory Info :
      Physical Memory Utilization : 99.1%
      Virtual Memory Utilization  : 98.6%
   Network Info :
      Receive Bytes(per second)    : 42809
      Receive Packets(per second)  : 337
      Transmit Bytes(per second)   : 42885
      Transmit Packets(per second) : 332
   Disk Info :
      /dev/sda1 : 87.4%
         |-> 192.168.0.32:5101   /home/cumulus/coordinator1
         |-> 192.168.0.32:5301   /home/cumulus/broker1
         |-> 192.168.0.32:5401   /home/cumulus/warehouse_a1
Host Name : 192.168.0.33
   CPU Info :
      Model Name          : Intel(R) Xeon(R) CPU E3-1231 v3 @ 3.40GHz
      Number of CPUs      : 8
      Number of CPU Cores : 4
      CPU Utilization     : 2.0%
      CPU IOWait Ratio    : 0.0%
   Memory Info :
      Physical Memory Utilization : 46.9%
      Virtual Memory Utilization  : 22.8%
   Network Info :
      Receive Bytes(per second)    : 12336
      Receive Packets(per second)  : 103
      Transmit Bytes(per second)   : 13500
      Transmit Packets(per second) : 103
   Disk Info :
      /dev/sda1 : 64.2%
         |-> 192.168.0.33:5101   /home/cumulus/coordinator2
         |-> 192.168.0.33:5401   /home/cumulus/warehouse_a2

mach@localhost:~$ machcoordinatoradmin --get-host-resource --metric=cpu
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
Host Name : 192.168.0.32
   CPU Info :
      Model Name          : Intel(R) Xeon(R) CPU E3-1231 v3 @ 3.40GHz
      Number of CPUs      : 8
      Number of CPU Cores : 4
      CPU Utilization     : 13.9%
      CPU IOWait Ratio    : 0.0%
Host Name : 192.168.0.33
   CPU Info :
      Model Name          : Intel(R) Xeon(R) CPU E3-1231 v3 @ 3.40GHz
      Number of CPUs      : 8
      Number of CPU Cores : 4
      CPU Utilization     : 1.9%
      CPU IOWait Ratio    : 0.0%

mach@localhost:~$ machcoordinatoradmin --get-host-resource --host=192.168.0.33
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
Host Name : 192.168.0.33
   CPU Info :
      Model Name          : Intel(R) Xeon(R) CPU E3-1231 v3 @ 3.40GHz
      Number of CPUs      : 8
      Number of CPU Cores : 4
      CPU Utilization     : 2.0%
      CPU IOWait Ratio    : 0.0%
   Memory Info :
      Physical Memory Utilization : 46.9%
      Virtual Memory Utilization  : 22.8%
   Network Info :
      Receive Bytes(per second)    : 12588
      Receive Packets(per second)  : 106
      Transmit Bytes(per second)   : 13330
      Transmit Packets(per second) : 100
   Disk Info :
      /dev/sda1 : 64.2%
         |-> 192.168.0.33:5101   /home/cumulus/coordinator2
         |-> 192.168.0.33:5401   /home/cumulus/warehouse_a2

mach@localhost:~$ machcoordinatoradmin --host-resource-disable
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
              Name : HOST-RESOURCE
             Value : OFF
            Format : text/plain
```

## machdeployeradmin


You can check the status of the Deployer, or directly issue the Deployer's startup/shutdown/stop commands.

Normally the fastest way to issue the commands is through machcoordinatoradmin, but if not possible, you must do the following.

Only exists in Cluster Edition Package.

## Options and Features

The options for machdeployeradmin are as follows. The functions described in the previous section are omitted.

```
mach@localhost:~$ machdeployeradmin -h
```


|Options|Description|
|--|--|
|-u, --startup | Runs Deployer process|
|-s, --shutdown | Terminates Deployer process|
|-k, --kill | Stops Deployer process|
|-c, --createdb | Creates Deployer meta|
|-d, --destroydb | Deletes Deployer meta|
|-i, --silent | Mutes the banner|
|-e, --check | Checks to see if Deployer process is running|


## Checking Running Status

Example:

```
mach@localhost:~$ machdeployeradmin -e
-------------------------------------------------------------------------
     Machbase Deployer Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
Machbase Deployer is running with pid(29373)!
```
