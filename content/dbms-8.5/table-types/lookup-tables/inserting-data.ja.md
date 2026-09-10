---
title : Lookup データの挿入
type: docs
weight: 20
toc: true
---

基本的な挿入方法と更新方法は Volatile テーブルと同じです。

異なる点は、Lookup テーブルへの APPEND で主キーが重複した場合に、`LOOKUP_APPEND_UPDATE_ON_DUPKEY` プロパティの設定によって該当行を更新できることです。

`LOOKUP_APPEND_UPDATE_ON_DUPKEY` の詳細は、[プロパティ](../../../configuration/property/#lookup_append_update_on_dupkey)を参照してください。


## Lookup テーブルの再読み込み {#lookup-table-reload}

Machbase 6.7 以降では、Lookup ノードが Lookup テーブルのデータを管理します。

Lookup ノードから Lookup テーブルのデータを再読み込みするには、EXEC TABLE_REFRESH コマンドを使用します。

```sql
EXEC TABLE_REFRESH(lktable);
```
