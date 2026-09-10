---
title : Lookup テーブルの作成と管理
type: docs
weight: 10
toc: true
---

Lookup テーブルの作成方法を示します。

## Lookup テーブルの作成 {#creating-lookup-table}

```sql
CREATE LOOKUP TABLE lktable (id INTEGER PRIMARY KEY, name VARCHAR(20));
```

Lookup テーブルには主キーを指定する必要があります。


## Lookup テーブルの削除 {#deleting-lookup-table}

```sql
DROP TABLE lktable;
```
