---
type: docs
title: 'SAVE DATA INTO'
weight: 100
toc: true
---

SAVE DATA INTO saves SELECT query results to CSV.

## Syntax

```sql
SAVE DATA INTO 'file_path'
    [HEADER { ON | OFF }]
    [{ FIELDS | COLUMNS }
        [TERMINATED BY 'char']
        [ENCLOSED BY 'char']
    ]
    [ENCODED BY coding_name]
    AS select_query
```

## Options

| Option | Default | Description |
|------|--------|------|
| `HEADER { ON \| OFF }` | OFF | Whether to write column names in the first row |
| `TERMINATED BY 'char'` | `,` | Field delimiter |
| `ENCLOSED BY 'char'` | `"` | Field quoting character |
| `ENCODED BY coding_name` | UTF8 | Output encoding |

Supported encodings: UTF8, MS949, KSC5601, EUCJP, SHIFTJIS, BIG5, GB231280

## Examples

```sql
-- Basic CSV output
SAVE DATA INTO '/tmp/result.csv' AS SELECT * FROM sensor_log;

-- Include a header and use a semicolon delimiter
SAVE DATA INTO '/tmp/output.csv'
    HEADER ON
    FIELDS TERMINATED BY ';'
    AS SELECT name, time, value FROM sensor_log WHERE time > TO_DATE('2024-01-01', 'YYYY-MM-DD');

-- Specify delimiter and quoting characters
SAVE DATA INTO '/tmp/export.csv'
    HEADER ON
    FIELDS TERMINATED BY ';' ENCLOSED BY '\''
    ENCODED BY MS949
    AS SELECT * FROM t1 WHERE i1 > 100;

-- Export TAG table data
SAVE DATA INTO '/tmp/tag_export.csv'
    HEADER ON
    AS SELECT name, time, value
         FROM sensor_tag
        WHERE name = 'TEMP-01'
          AND time BETWEEN TO_DATE('2024-01-01', 'YYYY-MM-DD')
                       AND TO_DATE('2024-01-02', 'YYYY-MM-DD')
        ORDER BY time;
```

## Notes

- The Machbase server process must be able to write to the path.
- If the output file already exists, an error is returned and the existing file remains unchanged.
  Use another filename or move the existing file before retrying.
- Empty SELECT results may produce an empty file or a header-only file.
- Lack of permission to access the path returns an error.

## Related Documentation

- [LOAD DATA INFILE Syntax](../load-data-infile-syntax/) — Load data from files into tables
