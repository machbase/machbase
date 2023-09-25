---
title: Import
type: docs
weight: 40
---

{: .important }
> For smooth practice, the following query should be run to prepare tables and data.
>
> ```sql
> CREATE TAG TABLE IF NOT EXISTS EXAMPLE (NAME VARCHAR(20) PRIMARY KEY, TIME DATETIME BASETIME, VALUE DOUBLE SUMMARIZED);
> ```
>

Data files can be entered into the table using the import function.

## Import csv
{: .no_toc}

Make test data in `data.csv`.

```
name-0,1687405320000000000,123.456
name-1,1687405320000000000,234.567000
name-2,1687405320000000000,345.678000
```

Import data

```sh
machbase-neo shell import \
    --input ./data.csv    \
    --timeformat ns        \
    EXAMPLE
```

Select data

```sh
machbase-neo shell "SELECT * FROM EXAMPLE";

 ROWNUM  NAME    TIME(LOCAL)          VALUE   
──────────────────────────────────────────────
      1  name-0  2023-06-22 12:42:00  123.456 
      2  name-1  2023-06-22 12:42:00  234.567 
      3  name-2  2023-06-22 12:42:00  345.678 
3 rows fetched.
```

