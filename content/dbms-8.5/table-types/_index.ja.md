---
type: docs
title: 'テーブルの種類'
weight: 60
toc: true
---

Machbase の 4 種類のテーブルについて説明します。各セクションで構文、機能、高度な使用方法を示します。

## テーブルの種類 {#table-types}

- [Tag テーブル](./tag-tables/) - センサーやデバイスの時系列データ
- [Log テーブル](./log-tables/) - イベントストリームとログ
- [Volatile テーブル](./volatile-tables/) - インメモリのリアルタイムデータ
- [Lookup テーブル](./lookup-tables/) - 参照データとマスターデータ

## クイックリファレンス {#quick-reference}

| 種類 | 作成構文 | 主な用途 |
|------|--------------|----------|
| Tag | `CREATE TAG TABLE` | センサーデータ（ID、時刻、値） |
| Log | `CREATE TABLE` | イベント、ログ、柔軟なスキーマ |
| Volatile | `CREATE VOLATILE TABLE` | リアルタイムキャッシュ、セッション |
| Lookup | `CREATE LOOKUP TABLE` | デバイス台帳、設定 |

詳細な比較と選択方法は、[テーブルの種類の概要](../core-concepts/table-types-overview/)を参照してください。
