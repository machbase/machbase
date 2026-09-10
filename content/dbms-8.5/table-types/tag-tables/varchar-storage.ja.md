---
title: 'VARCHAR ストレージの最適化'
type: docs
weight: 100
toc: true
---

## 概要 {#overview}

VARCHAR データを固定長領域と可変長領域のどちらに保存するかを制御し、性能とストレージ効率を改善します。

## VARCHAR の保存オプション {#varchar-storage-option}
VARCHAR データを固定長領域に保存できる最大サイズを指定します。
この値より長い VARCHAR データは、可変長領域に保存されます。
15 ～ 127 の範囲で指定でき、既定値は 15 です。

```sql
-- 入力する VARCHAR データが 15 以下なら、拡張ファイルではなく固定長データファイルに保存する。
  
CREATE TAG TABLE tag (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE SUMMARIZED, strval VARCHAR(100)) VARCHAR_FIXED_LENGTH_MAX = 15;
```
  
設定値は m$sys_table_property テーブルで確認できます。
```sql
SELECT * FROM m$sys_table_property WHERE id={table_id} AND name = 'VARCHAR_FIXED_LENGTH_MAX';
```
