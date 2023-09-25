---
title: TQL Basic
type: docs
weight: 0
---

# TQL Basic
{:.no_toc}

1. TOC
{:toc}

{: .important }
> For smooth practice, the following query should be run to prepare tables and data.
> ```sql
> CREATE TAG TABLE IF NOT EXISTS EXAMPLE (NAME VARCHAR(20) PRIMARY KEY, TIME DATETIME BASETIME, VALUE DOUBLE SUMMARIZED);
> INSERT INTO EXAMPLE VALUES('TAG0', TO_DATE('2021-08-12'), 10);
> INSERT INTO EXAMPLE VALUES('TAG0', TO_DATE('2021-08-13'), 11);
> ```
>

## Output

TQL provides multiple types of output functions.

### CSV Format

```js
SQL( `select * from example` )
CSV()
```

`result`

```
TAG0,1628694000000000000,10
TAG0,1628780400000000000,11
```

### JSON Format

```js
SQL( `select * from example` )
JSON()
```

`result`

```json
{
  "data": {
    "columns": [
      "NAME",
      "TIME",
      "VALUE"
    ],
    "types": [
      "string",
      "datetime",
      "double"
    ],
    "rows": [
      [
        "TAG0",
        1628694000000000000,
        10
      ],
      [
        "TAG0",
        1628780400000000000,
        11
      ]
    ]
  },
  "success": true,
  "reason": "success",
  "elapse": "1.571444ms"
}
```

### Markdown Format

```js
SQL( `select * from example` )
MARKDOWN()
```

`result`

```
|NAME|TIME|VALUE|
|:-----|:-----|:-----|
|TAG0|1628694000000000000|10.000000|
|TAG0|1628780400000000000|11.000000|
```

## Database Sink

TQL provides `INSERT()` and `APPEND()` function to write data into the database.

### Insert

`INSERT` function stores incoming records into specified databse table by an `INSERT` statement for each record.

```js
SQL( `select * from example` )
INSERT("name", "time", "value", table("example"))
```

`result`

```
"2 rows inserted."
```

### Append

`APPEND` function stores incoming records into specified databse table via the `APPEND` method of machbase-neo.

- `table()` table(string) specify destination table

```js
SQL( `select * from example` )
APPEND(table('example'))
```

`result`

```
"append 2 rows (success 2, fail 0)."
```
