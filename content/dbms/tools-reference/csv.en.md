---
title : 'csvimport / csvexport'
type : docs
weight: 10
---

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
