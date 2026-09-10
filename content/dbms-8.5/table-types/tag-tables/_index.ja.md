---
type: docs
title: 'Tag テーブル'
weight: 10
toc: true
---

センサー、デバイス、距離軸の系列データ向けに特化した Machbase の Tag テーブルについて説明します。

## 概要 {#overview}

Tag テーブルは `(tag_name, axis, value)` 形式のデータ保存に最適化されています。軸には時刻または距離を使用でき、メタデータ管理と軸に沿った高速な範囲検索を提供します。

## 主な機能 {#key-features}

- **毎秒数百万件の挿入**
- **時間軸テーブルの自動ロールアップ集計**（秒、分、時間単位）
- **3 階層のパーティションインデックス**
- センサー情報を管理する**メタデータ層**
- **高い圧縮率**（10 ～ 100 倍）

## 基本構文 {#basic-syntax}

```sql
-- 時間軸
CREATE TAG TABLE sensor_data (
    tag_name VARCHAR(32) PRIMARY KEY,
    event_time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
);

-- 距離軸
CREATE TAG TABLE trip_data (
    tag_name VARCHAR(32) PRIMARY KEY,
    distance_m DOUBLE BASE DISTANCE,
    value DOUBLE
);
```

## 適した用途 {#when-to-use}

- IoT センサーデータ
- 産業機器のテレメトリー
- スマートメーター
- GPS 追跡
- コンベヤーや走行距離計に基づくテレメトリー
- 環境監視
- `(tag_name, time|distance, value)` 形式のデータ

## 関連ドキュメント {#related-documentation}

- [Tag データの挿入](./inserting-data/)
- [基本概念：テーブルの種類](../../core-concepts/table-types-overview/)
- [Tag テーブルの作成と削除](./creating-tag-tables/)
- [ノイズを除外する条件付きロールアップ](./rollup-conditional/)
- [カスタムロールアップ：ユーザー定義集計](./rollup-custom/)
- [ロールアップの再構築](./rollup-rebuild/)
- [バイナリー列](./binary-columns/)
- [Tag メタデータ](./tag-metadata/)
- [Tag テーブルのインデックス](./tag-indexes/)
