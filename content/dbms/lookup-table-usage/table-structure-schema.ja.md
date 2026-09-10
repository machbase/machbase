---
type: docs
title: '9.2 テーブル構造とスキーマ'
weight: 20
toc: true
---

LOOKUPテーブルの構造とスキーマ設計を説明します。

<a id="lookup-table-design"></a>

## LOOKUPテーブルの設計

LOOKUPテーブルは、コードテーブルとマスターデータを保存するタイプです。
PRIMARY KEYで各行を識別し、PRIMARY KEYまたは一般条件式によるUPDATE/DELETEをサポートし、ディスクに永続保存されます。

### 永続保存とメモリ検索の構造

LOOKUPテーブルは、永続性とメモリ検索性能を提供する2層構造です。

1. 変更された行は、再起動後も保持できるよう永続ストレージに記録されます。
2. サーバー起動時に永続ストレージのLOOKUP行をすべて読み取り、各列の値を含むメモリ上の行として復元します。
3. 各メモリ行は、必須の`PRIMARY KEY`の赤黒木インデックスに登録されます。
4. SQLクエリは、復元されたメモリ行とインデックスを使用します。

概念上、1行は次のようなキーと値の項目として捉えられます。

```
PRIMARY KEY                       その他の列の値
sensor_id = 'TEMP-01'  ───────►  { site, unit, status, ... }
          key                              value
```

このためLOOKUPは、SQLテーブルのインターフェース、一般条件検索、JOIN、セカンダリインデックスに対応しながら、
特に`PRIMARY KEY`検索に適しています。
永続ストレージがあっても、検索時に必要な行だけをディスクから読み出す構造ではありません。
全行と作成した赤黒木セカンダリインデックスがメモリを使用するため、スキーマ設計では、
行数だけでなく可変長列、JSON値、セカンダリインデックスのサイズも考慮してください。

- **[活用例](/dbms/lookup-table-usage/patterns-scenarios/#use-cases-lookup)**
- **[PRIMARY KEYの設計](/dbms/lookup-table-usage/primary-key-policy/#design-primary-key)**
- **[列とシーケンスの設計](/dbms/lookup-table-usage/sequence-column/#design-column-lookup-sequence)**
- **[JSON列とクエリ](/dbms/lookup-table-usage/json-column-query/#condition-query-lookup-json)**
- **[参照設計パターン](/dbms/lookup-table-usage/patterns-scenarios/#patterns-reference-design)**
- **[インデックス戦略](/dbms/lookup-table-usage/index-performance/#index-strategy-lookup)**
- **[PRIMARY KEYポリシー](/dbms/lookup-table-usage/primary-key-policy/#policy-lookup-primary-key)**
- **[一般条件式によるUPDATE・DELETE](/dbms/lookup-table-usage/predicate-update-delete/)**
- **[バックアップ・復旧のサポート範囲](/dbms/lookup-table-usage/operations-lifecycle/#recovery-support-scope-backup-lookup)**
- **[制約と注意事項](/dbms/lookup-table-usage/constraints-errors-troubleshooting/#limitations-lookup)**
