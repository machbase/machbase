---
title: Import & Export
type: docs
weight: 600
---

## Import csv

```sh
curl -o - https://machbase.com/assets/example/example.csv.gz | \
machbase-neo shell import   \
    --input -               \
    --compress gzip         \
    --timeformat s          \
    EXAMPLE
```
The command above is downloading a compressed csv file from the remote web server by `curl`.
It writes out data (compresed, binary) into its stdout stream because we have set `-o -` option, then the output stream is passed to `machbase-neo shell import`, it reads data from stdout by flag `--input -`.

Combining two commands with pipe `|`, so that we don't need to store the data in a temporary file comsuing the local storage.

The result output shows that 1,000 records are imported.

```
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  5352  100  5352    0     0   547k      0 --:--:-- --:--:-- --:--:-- 5226k
import total 1000 record(s) inserted
```

Or, we can download data file in the local storage then import from it.

```sh
curl -o data.csv.gz https://machbase.com/assets/example/example.csv.gz
```

It is possible to import compressed or uncompressed csv file.

Then import csv file from local storage with `--input <file>` flag. And use `--compress gzip` option if the file is gzip'd form.

```sh
machbase-neo shell import \
    --input ./data.csv    \
    --timeformat s        \
    EXAMPLE
```

Query the table to check.

```sh
machbase-neo shell "select * from example order by time desc limit 5"
```
```
 ROWNUM  NAME      TIME(UTC)            VALUE     
──────────────────────────────────────────────────
 1       wave.sin  2023-02-15 03:47:50  0.994540  
 2       wave.cos  2023-02-15 03:47:50  -0.104353 
 3       wave.sin  2023-02-15 03:47:49  0.951002  
 4       wave.cos  2023-02-15 03:47:49  0.309185  
 5       wave.cos  2023-02-15 03:47:48  0.669261  
```

The sample file contains total 1,000 records and the table contains all of them after importing.

```sh
machbase-neo shell "select count(*) from example"
```
```
 ROWNUM  COUNT(*) 
──────────────────
 1       1000     
```

## Export csv

Exporting table is straightforward. Set `--output` flag for a file path where to save the data.
`--format csv` makes machbase-neo to export data in csv format.
`--timeformat ns` makes any datetime fields in output will be expressed in Unix epoch nanoseconds.

```sh
machbase-neo shell export --output ./example_out.csv --format csv --timeformat ns EXAMPLE
```

## Copy a table by combining export & import

We can "copy" a table by combining export and import without a temporary file in local storage.

Make a new table where to copy data into.

```sh
machbase-neo shell \
    "create tag table EXAMPLE_COPY (name varchar(100) primary key, time datetime basetime, value double)"
```

Then execute imort and export command together.

```sh
machbase-neo shell export       \
    --output -                  \
    --no-heading --no-footer    \
    --format csv                \
    --timeformat ns             \
    EXAMPLE  |  \
machbase-neo shell import       \
    --input -                   \
    --format csv                \
    --timeformat ns             \
    EXAMPLE_COPY
```

Query the records count of newly create table.

```sh
 machbase-neo shell "select count(*) from EXAMPLE_COPY"
```
```
 ROWNUM  COUNT(*) 
──────────────────
 1       1000     
```

This example is applicable in a situation that we want to "copy" a table from *A* database to *B* database.
We could set `--server <address>` flag specifies remote machbase-neo server process one of "import" and "export" commands,
And it is also possible set both of commands runs for two different remote servers.

## Import from query result

Let's combine "select" query and import command.

```sh
machbase-neo shell sql \
    --output -         \
    --format csv       \
    --no-rownum        \
    --no-heading       \
    --no-footer        \
    --timeformat ns    \
    "select * from example where name = 'wave.sin' order by time" | \
machbase-neo shell import \
    --input -             \
    --format csv          \
    EXAMPLE_COPY
```

We selected data that tag name is `wave.sin`, then import it into the `EXAMPLE_COPY` table.
It is required `--no-rownum` and `--no-heading` options in `sql` command becuase `import` command need to verify the number of fields and data type of the incoming csv data.

## Import from query result with HTTP API

The scenario importing from query results can be done with machbase-neo's HTTP API.

```sh
curl -o - http://127.0.0.1:5654/db/query        \
    --data-urlencode "q=select * from EXAMPLE order by time desc limit 100" \
    --data-urlencode "format=csv"                \
    --data-urlencode "heading=false" |           \
curl http://127.0.0.1:5654/db/write/EXAMPLE_COPY \
    -H "Content-Type: text/csv"                  \
    -X POST --data-binary @- 
```

## Import method "insert" vs. "append"

The import command writes the incoming data with "INSERT INTO..." statement by default.
As long as the total number of records to write is small, there is not a big difference from "append" method.

When you are expecting a large amount of data (e.g. more than several hundreds thousands records),
Use `--method append` flag that specify machbase-neo to use "append" method 
instead of "INSERT INTO..." statement which is implicitly speicified as `--method insert`. 
