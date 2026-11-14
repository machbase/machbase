---
type: docs
title: '16.4.4 csvimport / csvexport'
weight: 40
toc: true
---

`csvimport` and `csvexport` are simple CSV import/export wrappers. They simplify the CSV options of
`machloader`; options not listed below can be used as with `machloader`.

## csvimport

Import a CSV file into a Machbase table.

### Options

| Option | Description |
|------|------|
| `-t`, `--table=TABLE_NAME` | Target table name |
| `-d`, `--data=DATA_FILE` | CSV file to import |
| `-s`, `--server=SERVER` | Server IP address (default: 127.0.0.1) |
| `-P`, `--port=PORT` | Server port (default: 5656) |
| `-u`, `--user=USER` | Username (default: SYS) |
| `-p`, `--password=PASSWORD` | User password (default: MANAGER) |
| `-H` | Treat the first CSV row as a header and exclude it from ingestion |
| `-C` | Create the table if missing (with `-H`, use header values as column names) |
| `-m`, `--mode=MODE` | Import mode: `append` (default) or `replace` |
| `-a`, `--atime` | Include `_ARRIVAL_TIME` |
| `-F`, `--dateformat=DATEFORMAT` | Date format for datetime columns |
| `-l`, `--log=LOG_FILE` | Execution log file |
| `-b`, `--bad=BAD_FILE` | Bad file for failed import rows |
| `-I`, `--silent` | Run without banner or status output |

### Basic Usage

Specify the table and filename.

```bash
csvimport -t table_name -d data.csv
```

You can also use positional arguments without options, in either order.

```bash
csvimport table_name data.csv
csvimport data.csv table_name
```

### Header Handling

Treat the first CSV row as a header and exclude it from the data.

```bash
csvimport -t table_name -d data.csv -H
```

### Automatic Table Creation

Create the table automatically if it does not exist.

```bash
# Generate column names c0, c1, ...
csvimport -t table_name -d data.csv -C

# Use CSV header values as column names
csvimport -t table_name -d data.csv -C -H
```

All automatically created columns have type `varchar(32767)`.

### Replace Mode

Delete existing data and refill the table from the CSV file.

```bash
csvimport -t table_name -d data.csv -m replace
```

### Specifying a Server Connection

```bash
csvimport -s 192.168.0.10 -P 5656 -u SYS -p MANAGER \
    -t sensor_data -d data.csv
```

## csvexport

Export Machbase table data to a CSV file.

### Options

| Option | Description |
|------|------|
| `-t`, `--table=TABLE_NAME` | Table to export |
| `-d`, `--data=DATA_FILE` | Output CSV filename |
| `-s`, `--server=SERVER` | Server IP address (default: 127.0.0.1) |
| `-P`, `--port=PORT` | Server port (default: 5656) |
| `-u`, `--user=USER` | Username (default: SYS) |
| `-p`, `--password=PASSWORD` | User password (default: MANAGER) |
| `-H` | Write column names as the CSV header |
| `-a`, `--atime` | Include `_ARRIVAL_TIME` |
| `-F`, `--dateformat=DATEFORMAT` | Date format for datetime columns |
| `-l`, `--log=LOG_FILE` | Execution log file |
| `-I`, `--silent` | Run without banner or status output |

### Basic Usage

```bash
csvexport -t table_name -d output.csv
```

You can also use positional arguments without options.

```bash
csvexport table_name output.csv
csvexport output.csv table_name
```

### Exporting with a Header

Write column names as the first row (header) of the CSV file.

```bash
csvexport -t table_name -d output.csv -H
```

### Exporting `_ARRIVAL_TIME`

```bash
csvexport -t table_name -d output.csv -a
```

## Examples

```bash
# Basic import
csvimport -t sensor_data -d sensor_20240101.csv

# Import CSV with a header
csvimport -t sensor_data -d sensor_20240101.csv -H

# Export all data, including a header
csvexport -t sensor_data -d export_20240101.csv -H

# Import with log files
csvimport -t sensor_data -d data.csv -H \
    -l import.log -b import.bad

# Export from a remote server
csvexport -s 192.168.0.10 -P 5656 -u SYS -p MANAGER \
    -t sensor_data -d remote_export.csv -H -a
```
