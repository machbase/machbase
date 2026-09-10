---
type: docs
title: 'Lookup テーブル'
weight: 40
toc: true
---

参照データ、マスターデータ、ディメンションテーブルに使用する Machbase の Lookup テーブルについて説明します。

## 概要 {#overview}

Lookup テーブルは、更新頻度が低く読み取り頻度が高い参照データに最適化されたディスクベースのテーブルです。すべての CRUD 操作をサポートし、デバイス台帳や設定の保存に適しています。

## 主な機能 {#key-features}

- **すべての CRUD 操作をサポート**（INSERT、UPDATE、DELETE、SELECT）
- **ディスクへの永続保存**
- **高速な読み取り**
- **時系列テーブルとの JOIN**
- **追加の RED-BLACK インデックス（任意）**

## 基本構文 {#basic-syntax}

```sql
CREATE LOOKUP TABLE table_name (
    column1 data_type PRIMARY KEY,
    column2 data_type,
    ...
);
```

## 適した用途 {#when-to-use}

- デバイス台帳
- 設定テーブル
- カテゴリーテーブルやディメンションテーブル
- マスターデータ
- 更新頻度の低い参照データ

## 適さない用途 {#when-not-to-use}

- 高頻度の挿入（Tag/Log テーブルを使用）
- 時系列データ
- 毎秒数百万件の書き込みが必要なデータ

## 関連ドキュメント {#related-documentation}

- [Lookup データの挿入](./inserting-data/)
- [基本概念：テーブルの種類](../../core-concepts/table-types-overview/)
