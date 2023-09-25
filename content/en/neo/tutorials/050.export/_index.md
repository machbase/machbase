---
title: Export
type: docs
weight: 50
---

{: .important }
> For smooth practice, the following query should be run to prepare tables and data.
> ```sql
> CREATE TAG TABLE IF NOT EXISTS EXAMPLE (NAME VARCHAR(20) PRIMARY KEY, TIME DATETIME BASETIME, VALUE DOUBLE SUMMARIZED);
> INSERT INTO EXAMPLE VALUES('TAG0', TO_DATE('2021-08-12'), 100);
> INSERT INTO EXAMPLE VALUES('TAG0', TO_DATE('2021-08-13'), 110);
> ```
>

Table data can be extracted into a data file using the Export function.

## Export csv

Export data

```sh
machbase-neo shell export      \
    --output ./data_out.csv    \
    --format csv               \
    --timeformat ns            \
    EXAMPLE
```

Select data

```sh
cat data_out.csv 

TAG0,1628694000000000000,100
TAG0,1628780400000000000,110
```

## Export json

Export data

```sh
machbase-neo shell export      \
    --output ./data_out.json   \
    --format json              \
    --timeformat ns            \
    EXAMPLE
```

Select data

```sh
cat data_out.json

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
        100
      ],
      [
        "TAG0",
        1628780400000000000,
        110
      ]
    ]
  },
  "success": true,
  "reason": "success",
  "elapse": "1.847207ms"
}
```

