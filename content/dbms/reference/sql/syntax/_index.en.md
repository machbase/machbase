---
type: docs
title: '16.1.1 SQL Syntax Dictionary'
weight: 10
toc: true
---

The SQL Syntax Dictionary provides BNF notation and minimal examples for all SQL statements
supported by Machbase.

## Supported SQL Statements

| Statement | Category | Description |
|------|------|------|
| [CREATE TABLE](./ddl-syntax/#create-table) | DDL | Create LOG/TAG/LOOKUP/VOLATILE/TRANSACTION tables |
| [DROP TABLE](./ddl-syntax/#drop-table) | DDL | Drop tables |
| [ALTER TABLE](./ddl-syntax/#alter-table) | DDL | Change schemas: add/drop/modify/rename columns |
| [TRUNCATE TABLE](./ddl-syntax/#truncate-table) | DDL | Delete all table data |
| [CREATE INDEX](./index-syntax/#create-index) | DDL | Conditional creation and index support by table type |
| [DROP INDEX](./index-syntax/#drop-index) | DDL | Drop indexes |
| [CREATE ROLLUP](./rollup-syntax/#create-rollup) | DDL | Create TAG ROLLUP definitions |
| [DROP ROLLUP / ALTER ROLLUP](./rollup-syntax/#drop-rollup) | DDL | Delete and control ROLLUPs |
| [CREATE RETENTION](./retention-syntax/#create-retention) | DDL | Create retention policies |
| [CREATE VIEW / DROP VIEW](./view-syntax/) | DDL | Create and drop stored views |
| [CREATE TABLESPACE](./ddl-syntax/#create-tablespace) | DDL | Create tablespaces |
| [INSERT INTO](./dml-syntax/#insert-into) | DML | Insert single or multiple rows |
| [INSERT SELECT](./dml-syntax/#insert-select) | DML | Insert query results into another table |
| [UPDATE](./dml-syntax/#update) | DML | Modify TRANSACTION/LOOKUP/VOLATILE rows and correct TAG data with restricted predicates |
| [DELETE](./dml-syntax/#delete) | DML | Delete table data |
| [LOAD DATA INFILE](./load-data-infile-syntax/) | DML | Load CSV files directly |
| [SELECT](./select-syntax/) | SELECT | Query data with JOIN, GROUP BY, ORDER BY, and LIMIT |
| [WITH / CTE](./cte-syntax/) | SELECT | Nonrecursive common table expressions in Standard Edition |
| [Named Bind Parameter](./named-bind-parameter-syntax/) | Common SQL | Value parameters in `:name` form |
| [CAST](../functions/functions-full/#cast) | SQL expression | Explicitly convert values to a specified type |
| [SAVE DATA INTO](./save-data-into-syntax/) | SELECT | Save query results to CSV |
| [BACKUP](./backup-restore-mount-syntax/#backup) | Operations | Back up databases or tables |
| [RESTORE](./backup-restore-mount-syntax/#restore) | Operations | Logical database restore and offline restore using `machadmin -r` |
| [MOUNT / UMOUNT DATABASE](./backup-restore-mount-syntax/#mount-database) | Operations | Mount/unmount backup databases |
| [CREATE USER / DROP USER / ALTER USER](./user-auth-syntax/#create-drop-alter-user) | Users | Create/drop users and change passwords |
| [GRANT / REVOKE](./user-auth-syntax/#grant-revoke) | Users | Grant and revoke privileges |
| [AUTH KEY Management](./user-auth-syntax/#auth-key) | Users | Register/manage public-key authentication keys |
| [ALTER SYSTEM](./system-session-alter-syntax/#alter-system) | System | Session control, PVO Cache flush, license installation, and more |
| [ALTER SESSION](./system-session-alter-syntax/#alter-session) | Session | Configure session parameters |
| [PIVOT](./pivot-syntax/) | Analysis | Convert rows to columns |
| [WINDOW FUNCTION (OVER)](./window-function-over-syntax/) | Analysis | Window functions and OVER |
| [SERIES BY](./series-syntax/) | Analysis | Group consecutive records meeting conditions |
| [SEARCH / ESEARCH / REGEXP](./search-esearch-regexp-syntax/) | Search | Keyword-index-based text search |
| [ROLLUP REBUILD](./rollup-rebuild-syntax/) | Operations | Recalculate ROLLUP results |
| [DATABASE](./database-syntax/) | DDL/session | Create/select/drop logical databases and check status |
| [AUTO_INCREMENT](./auto-increment-syntax/) | DDL | Generate 64-bit PRIMARY KEY values automatically |
| [EXEC procedure / SHOW ROLLUPGAP](./execute-procedure-syntax/) | Control | Table flush/refresh and ROLLUP control/status |


## BNF Conventions

This dictionary uses the following Backus–Naur Form (BNF) conventions.

| Notation | Meaning |
|------|------|
| `'keyword'` | SQL reserved word, case-insensitive |
| `name` | User-defined name |
| `( A \| B )` | Either A or B |
| `[ ... ]` | Optional element |
| `( ... )*` | Zero or more repetitions |
| `( ... )+` | One or more repetitions |
| `( ... )?` | Zero or one occurrence |
