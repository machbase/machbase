---
type: docs
title: 'Log テーブル'
weight: 20
toc: true
---

イベントストリーム、アプリケーションログ、タイムスタンプ付きデータを柔軟に扱う Machbase の Log テーブルについて説明します。

## 概要 {#overview}

Log テーブルは、柔軟なスキーマを持つ追記専用のイベントデータに最適化されています。ナノ秒精度のタイムスタンプを自動的に付加し、全文検索をサポートします。

## 主な機能 {#key-features}

- **毎秒数百万件の挿入**
- **_arrival_time 列の自動追加**（ナノ秒精度）
- **柔軟なスキーマ**（任意の列）
- SEARCH キーワードによる**全文検索**
- **最新データから取得**（自動ソート）
- **任意の LSM インデックス**

## 基本構文 {#basic-syntax}

```sql
CREATE TABLE table_name (
    column1 data_type,
    column2 data_type,
    ...
);
-- _arrival_time は自動的に追加される
```

## 適した用途 {#when-to-use}

- アプリケーションログ
- HTTP アクセスログ
- イベントストリーム
- トランザクションログ
- タイムスタンプ付きのイベントデータ

## 関連ドキュメント {#related-documentation}

- [Log データの挿入](./insert/)
- [基本概念：テーブルの種類](../../core-concepts/table-types-overview/)
