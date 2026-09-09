---
type: docs
title: '15.3 Ingestion and Loading Problems'
weight: 30
toc: true
---

<a id="failure"></a>

## Ingestion fails

First record the full client error, target database and table, ingestion method, and last
successful row. Check error meanings in the [Error Code Reference](/dbms/reference/error-codes/)
instead of relying on a fixed code table on this page.

```sql
DESC target_table;
SELECT NAME, TYPE, COLCOUNT
  FROM M$SYS_TABLES
 WHERE NAME = 'TARGET_TABLE';
```

Check the following:

- Input column count, order, types, and nullability
- Current database and table owner
- User `CONNECT` and table `INSERT` privileges
- Time string format and connection time zone
- File system space and `V$STORAGE_USAGE`
- Append API return values, failed rows, and flush results

Support for out-of-order timestamps and UPDATE/DELETE predicates differs by table type.
Check the constraints in the relevant table usage chapter.

<a id="failure-csv-import"></a>

## CSV import fails

Check the current distribution's options with `machloader -h`.

```bash
machloader -h
machloader -s 127.0.0.1 -P 5656 -u app_user \
  -t target_table -i /data/input.csv \
  -b /data/input.bad -l /data/input.log
```

Reproduce the failure with a small file, in this order:

1. Check absolute paths and file permissions on the loader host, not the server host.
2. Compare the column count of one CSV row with `DESC target_table`.
3. Check encoding names against the current help. Available names include `UTF8`, `MS949`,
   `KSC5601`, and `EUCJP`.
4. Match delimiter and quote options to the actual file.
5. Specify both the target column name and format in date format options.
6. Correct the first rejected row in the bad file, then load it into a separate validation table.

For exact `-F` syntax and loader options, use the
[machloader Command and Option Reference](/dbms/reference/command-line-tools/machloader/).
When retrying after partial success, check the already ingested range to prevent duplicates.
