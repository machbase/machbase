---
type: docs
title: 'LOAD DATA INFILE'
weight: 130
toc: true
---

LOAD DATA INFILE reads a CSV-format file directly on the server and inserts its data into a table.

> For large loads, use machloader. It offers parallel processing and additional options for higher ingestion throughput.

## Syntax

```sql
LOAD DATA INFILE 'file_path' INTO TABLE table_name
    [TABLESPACE tablespace_name]
    [AUTO { BULKLOAD | HEADUSE | HEADUSE_ESCAPE }]
    [{ FIELDS | COLUMNS } [TERMINATED BY 'char'] [ENCLOSED BY 'char']]
    [LINES TERMINATED BY 'char']
    [TRIM { ON | OFF }]
    [IGNORE number LINES]
    [MAX_LINE_LENGTH number]
    [ENCODED BY coding_name]
    [ON ERROR { STOP | IGNORE }]
```

## Options

| Option | Description |
|------|------|
| AUTO BULKLOAD | Insert each entire line into one column |
| AUTO HEADUSE | Create a table from first-row column names, then load data |
| AUTO HEADUSE_ESCAPE | Like HEADUSE, but replace reserved words/special characters with _ |
| TERMINATED BY 'char' | Field separator; default: , |
| ENCLOSED BY 'char' | Field quote character; default: " |
| LINES TERMINATED BY 'char' | Record separator |
| TRIM { ON \| OFF } | Remove leading/trailing column whitespace; default: ON |
| IGNORE number LINES | Skip the first N lines, for example a header |
| MAX_LINE_LENGTH number | Maximum line length; default: 512 KB |
| ENCODED BY coding_name | File encoding; default: UTF8 |
| ON ERROR STOP\|IGNORE | Stop or ignore on errors; default: STOP |

Supported encodings: UTF8, MS949, KSC5601, EUCJP, SHIFTJIS, BIG5, GB231280.

## Examples

```sql
-- Load a default CSV file (separator: ,  quote: ")
LOAD DATA INFILE '/tmp/sensor_data.csv' INTO TABLE sensor_log;

-- Skip one header line and load semicolon-separated data
LOAD DATA INFILE '/tmp/data.csv' INTO TABLE sample_data
    FIELDS TERMINATED BY ';' ENCLOSED BY '\''
    IGNORE 1 LINES
    ON ERROR IGNORE;

-- AUTO BULKLOAD: one column per line; create the table automatically
LOAD DATA INFILE '/tmp/raw.txt' INTO TABLE raw_table AUTO BULKLOAD;

-- AUTO HEADUSE: create columns from the first line, then load
LOAD DATA INFILE '/tmp/data_with_header.csv' INTO TABLE auto_table AUTO HEADUSE;

-- Specify encoding
LOAD DATA INFILE '/tmp/korean_data.csv' INTO TABLE Korean_table ENCODED BY MS949;
```

## Considerations

- Without AUTO, every target column must be VARCHAR or TEXT.
- The Machbase server process must be able to access the file path.
- Rows already inserted are not rolled back after an ingestion error.
- machloader offers better performance for large files.

## Comparison with machloader

| Item | LOAD DATA INFILE | machloader |
|------|-----------------|------------|
| Parallel processing | Unsupported | Supported |
| Interface | SQL statement | CLI utility |
| Use | Small loads and scripts | Large bulk loads |

## Related Documentation

- [SAVE DATA INTO Syntax](../save-data-into-syntax/) — Save SELECT results to files
