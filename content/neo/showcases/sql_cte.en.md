---
title: SQL Extensions
type: docs
weight: 491
---

Run the SQL extensions introduced in Machbase Neo 8.7, including Multi Database, CTE, ARRAY types, and BINARY literals, directly in the web SQL editor.

{{< youtube 0V-sWLzHpog >}}

This video demonstrates four SQL extensions in Machbase Neo 8.7 using data from a water-treatment pump facility.

First is Multi Database. A single server can host multiple databases, and tables in another database can be referenced as `database.owner.table`. The demo joins time-series sensor data in the default database with equipment master data in an operations database, showing each rack's average temperature alongside its responsible team.

Next is CTE. A `WITH` clause names intermediate results and breaks a query into steps. The demo chains multiple CTEs, with each later CTE filtering the previous result. It then uses `INSERT ... WITH ... SELECT` to save a CTE result to a summary table in another database and checks the number of inserted rows.

Finally, ARRAY types and BINARY literals. Four waveform channels are stored in one row of a `DOUBLE[4]` column and retrieved by index. The demo also shows that an array with a size different from its declaration is rejected. It inserts hexadecimal `X'0A0B0C0D'`, binary `B'00001010'`, and octal `O'012'` literals, then checks the stored values and byte lengths.

See how to perform cross-database joins, staged queries, and array and binary operations in SQL, without fetching and assembling data through multiple application calls.