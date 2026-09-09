---
type: docs
title: '16.4.3 machloader'
weight: 30
toc: true
---

`machloader` imports and exports data between text files, such as CSV, and a Machbase server. It
uses APPEND mode by default and supports more complex conversions through schema files.

## Options

```bash
machloader -h
```

| Option | Description |
|------|------|
| `-s`, `--server=SERVER` | Server IP address (default: 127.0.0.1) |
| `-P`, `--port=PORT` | Server port (default: 5656) |
| `-u`, `--user=USER` | Username (default: SYS) |
| `-p`, `--password=PASSWORD` | User password (default: MANAGER) |
| `-i`, `--import` | Import mode |
| `-o`, `--export` | Export mode |
| `-c`, `--schema` | Schema file generation mode |
| `-t`, `--table=TABLE_NAME` | Target table name |
| `-f`, `--form=SCHEMA_FILE` | Schema filename |
| `-d`, `--data=DATA_FILE` | Data filename |
| `-m`, `--mode=MODE` | Import mode: `append` (default) or `replace` |
| `-H`, `--header` | Treat the first import row as a header; write column names as a header on export |
| `-D`, `--delimiter=DELIMITER` | Field delimiter (default: `,`) |
| `-n`, `--newline=NEWLINE` | Record delimiter (default: `\n`) |
| `-e`, `--enclosure=ENCLOSURE` | Field enclosure character |
| `-r`, `--format=FORMAT` | File format (default: csv) |
| `-E`, `--encoding=CHARSET` | File encoding: UTF8 (default), ASCII, MS949, KSC5601, EUCJP, SHIFTJIS, BIG5, GB231280, UTF16 |
| `-F`, `--dateformat=DATEFORMAT` | Date format for datetime columns. Supports `unixtimestamp` and `nanotimestamp` |
| `-z`, `--timezone` | Timezone, such as `+0900` or `-1230` |
| `-a`, `--atime` | Include `_ARRIVAL_TIME` (excluded by default) |
| `-C`, `--create` | Create the table on import if missing |
| `-l`, `--log=LOG_FILE` | Execution log file |
| `-b`, `--bad=BAD_FILE` | Bad file for failed import rows |
| `--first=FIRST_ROW` | First row number to process |
| `-I`, `--silent` | Run without banner or progress output |
| `-S`, `--slash` | Set the backslash delimiter |
| `--summary` | Display selected options and exit without processing |
| `-h`, `--help` | Display options |

## Importing CSV Files

Basic import:

```bash
machloader -i -d data.csv -t sensor_data
```

Specify a server connection:

```bash
machloader -i -s 192.168.0.10 -P 5656 -u SYS -p MANAGER \
    -d data.csv -t sensor_data
```

Import CSV with a header:

```bash
machloader -i -d data.csv -t sensor_data -H
```

Delete existing data before import (replace mode):

```bash
machloader -i -d data.csv -t sensor_data -m replace
```

Start at a specific row:

```bash
machloader -i -d data.csv -t sensor_data --first=10
```

## Exporting CSV Files

```bash
machloader -o -d output.csv -t sensor_data
machloader -o -d output.csv -t sensor_data -H
```

Export including `_ARRIVAL_TIME`:

```bash
machloader -o -d output.csv -t sensor_data -a
```

### ARRAY Columns

Machbase DBMS 8.7.0 imports and exports ARRAY columns as `[value,null,value]`.
Enclose the CSV field because the ARRAY contains commas.

```csv
1,"[1.5,null,3.5,4.5]"
```

A NULL field represents a whole-array NULL; `"[null,null]"` represents a non-NULL ARRAY whose elements
are all NULL. Automatic table creation with `-C` does not infer ARRAY types. Explicitly create
tables that require ARRAY columns before importing. For type and NULL rules, see
[Numeric ARRAY Types](/dbms/reference/sql/types/array/).

## Encoding and Delimiters

EUC-KR encoding with a tab delimiter:

```bash
machloader -i -d data.txt -t table_name -E MS949 -D '\t'
```

Pipe (`|`) delimiter:

```bash
machloader -i -d data.txt -t table_name -D '|'
machloader -o -d data.txt -t table_name -D '|'
```

## Specifying a Timezone

```bash
machloader -i -d data.csv -t sensor_data -z +0900
machloader -i -d data.csv -t sensor_data -z -1230
```

## Specifying datetime Formats

Set the format directly on the command line:

```bash
machloader -i -d data.csv -t sensor_data \
    -F "_arrival_time YYYY-MM-DD HH24:MI:SS"
```

Import Unix timestamps:

```bash
machloader -i -d data.csv -t sensor_data \
    -F "time_column unixtimestamp"
```

Import nanosecond timestamps:

```bash
machloader -i -d data.csv -t sensor_data \
    -F "time_column nanotimestamp"
```

## Using Schema Files

Generate a schema file:

```bash
machloader -c -t sensor_data -f sensor_data.fmt
```

Import/export with a schema file:

```bash
machloader -i -f sensor_data.fmt -d data.csv
machloader -o -f sensor_data.fmt -d output.csv
```

Example schema file (`sensor_data.fmt`):

```
table sensor_data
{
    name   varchar(64);
    time   datetime;
    value  double;
}
DATEFORMAT time "YYYY-MM-DD HH24:MI:SS"
```

Ignore a specific column:

```
table sensor_data
{
    id     integer;
    name   varchar(64);
    extra  varchar(32) IGNORE;
}
```

## Log and Bad Files

```bash
machloader -i -d data.csv -t sensor_data \
    -l import.log -b import.bad
```

- `-l`: Import execution log with success/failure statistics
- `-b`: Failed row data in its original format

## Automatic Table Creation

Create the table if missing. Columns are named `c0`, `c1`, ... and have type `varchar(32767)`.

```bash
machloader -i -d data.csv -t new_table -C
machloader -i -d data.csv -t new_table -C -H   # Use header values as column names
```

## Examples

```bash
# Check settings before import (--summary)
machloader -i -d data.csv -t sensor_data --summary

# Import a large file with log and bad files
machloader -i -d bigdata.csv -t sensor_data \
    -H -z +0900 \
    -l import_20240101.log -b import_20240101.bad

# Export the entire table
machloader -o -d export_20240101.csv -t sensor_data -H -a
```
