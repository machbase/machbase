---
type: docs
title: '1. Getting Started'
weight: 10
toc: true
---

This chapter is a starting point for readers new to databases and for developers coming from
another DBMS. It introduces how Machbase DBMS 8.7.0 stores data, then walks through the basic SQL
workflow by inserting and querying one event.

You can read the overview before installing a database. To run the example, you need a running
DBMS server and its SQL client, `machsql`. The prerequisites in
[10-Minute Quick Start](./quick-start/) explain how to prepare the server and connection.

## What You Will Learn

1. Understand the roles of tables, rows, columns, and SQL.
2. Distinguish historical records from current state.
3. Identify Machbase table types for measurements, events, and reference data.
4. Connect to the server, create a LOG table, and insert and query data.
5. Compare event time with server arrival time and choose your next learning path.

## Reading Order

| Section | What you can do afterward |
|---|---|
| [Machbase DBMS Overview](./overview/) | Explain the purpose of a time-series database and the roles of its table types. |
| [10-Minute Quick Start](./quick-start/) | Connect, insert and query data, and clean up the practice table. |
| [Basic Command Cheatsheet](./command-cheatsheet/) | Distinguish shell commands from SQL and find common commands. |
| [Choose the Next Document](./choose-next-doc/) | Find the documents relevant to your data, development tasks, and operations. |

The example uses a small SQL `INSERT` so you can inspect the result directly. For continuous,
high-volume ingestion and error handling, continue with
[Data Input and Export](/dbms/development-tools-integration/data-input-load-export/).
