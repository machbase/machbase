---
type: docs
title: 'Volatile テーブル'
weight: 30
toc: true
---

リアルタイムで頻繁に更新するデータ向けの、Machbase のインメモリテーブルである Volatile テーブルについて説明します。

## 概要 {#overview}

Volatile テーブルは高速処理のためにすべてのデータをメモリに保存します。主キーによる UPDATE と DELETE をサポートし、リアルタイムダッシュボードやセッション管理に適しています。

## 主な機能 {#key-features}

- **すべてのデータをメモリに保存**
- PRIMARY KEY による **UPDATE と DELETE**
- 毎秒**数万件の操作**
- **キーによる高速検索**（O(log n)）
- **警告：シャットダウン時にデータが失われます**

## 基本構文 {#basic-syntax}

```sql
CREATE VOLATILE TABLE table_name (
    key_column data_type PRIMARY KEY,
    column1 data_type,
    column2 data_type,
    ...
);
```

## 適した用途 {#when-to-use}

- リアルタイムダッシュボード
- ユーザーセッション
- リアルタイムの状態表示
- キャッシュ層
- 一時的な計算

## 適さない用途 {#when-not-to-use}

- 永続保存が必要なデータ
- 大量のストリーミングデータ（Tag/Log テーブルを使用）
- 大規模なデータセット（RAM 容量による制限あり）

## 関連ドキュメント {#related-documentation}

- [データの挿入と更新](./insert-update/)
- [基本概念：テーブルの種類](../../core-concepts/table-types-overview/)
