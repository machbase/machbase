---
type: docs
title: '基本概念'
weight: 40
toc: true
---

アーキテクチャー、設計原則、主要な概念を詳しく説明します。内部動作と、時系列データに最適化されている理由を理解できます。

## このセクションの内容 {#in-this-section}

### [時系列データの理解](./time-series-data/) {#understanding-time-series-data}

時系列データの特徴と、従来の DB で扱いにくい理由を説明します。
- 時系列ワークロードの特性
- 書き込み中心と読み取り中心のパターン
- 追記専用設計の意義
- 時刻ベースの分割と圧縮

### [テーブルの種類](./table-types-overview/) {#table-types-overview}

適切なテーブルの選択方法を説明します。
- 4 種類の詳細比較
- 選択フローチャートとガイド
- 性能特性
- 一般的な用途と避けるべき使い方
- 各型の使い分け

### [インデックスと性能](./indexing/) {#indexing-and-performance}

高い性能を実現する仕組みを説明します。
- Tag のパーティションインデックス
- LSM（Log-Structured Merge）
- 自動インデックス管理
- クエリー最適化
- ロールアップ統計

## 対象読者 {#who-should-read-this}

次の方を対象とします。
- Machbase アプリケーションを設計する**開発者**
- システムを設計する**アーキテクト**
- 性能を調整する **DBA**
- データパイプラインを実装する**データエンジニア**

## 前提条件 {#prerequisites}

次を確認してから進めてください。
- [はじめに](../getting-started/)を完了
- [テーブルの種類](../table-types/)を確認
- Machbase の基本操作を経験

## 学習の順序 {#learning-path}

次の順を推奨します。

1. **時系列データ**：対象データの理解
2. **テーブルの種類**：適切な選択
3. **インデックス**：性能の最適化

## クイックリファレンス {#quick-reference}

### テーブルの選択 {#table-type-decision-guide}

```
センサーデータ（ID、時刻、値）ですか？
    はい → Tag テーブル

ログやイベントですか？
    はい → Log テーブル

メモリ内で UPDATE/DELETE が必要ですか？
    はい → Volatile テーブル

参照データやマスターですか？
    はい → Lookup テーブル
```

### 性能特性 {#performance-characteristics}

| 型 | 書き込み | 読み取り | UPDATE/DELETE | 保存先 |
|-----------|------------|-----------|---------------|---------|
| Tag | 毎秒数百万 | 非常に高速 | UPDATE 不可*、DELETE は時刻条件 | ディスク |
| Log | 毎秒数百万 | 高速 | UPDATE 不可、DELETE は時刻条件 | ディスク |
| Volatile | 毎秒数万 | 非常に高速 | キー指定 | メモリ |
| Lookup | 毎秒数百 | 高速 | キー指定 | ディスク |

*Tag のメタデータは更新できます。

## 主な概念 {#key-concepts-at-a-glance}

### 追記専用の設計 {#write-once-architecture}

追記中心のデータに最適化されています。
- 行単位のロックなし
- 高速な順次書き込み
- ログの上書きを防ぎ、整合性を維持

### 時刻によるパーティション分割 {#time-based-partitioning}

時刻に基づいて自動的に分割します。
- 効率的な期間検索
- 保持期間の管理が容易
- 圧縮の最適化

### 列指向の圧縮 {#columnar-compression}

列ごとに保存します。
- 10 ～ 100 倍の圧縮率
- 高速な分析クエリー
- ストレージコストの削減

### ロールアップ（Tag） {#rollup-tables-tag-tables}

ロールアップを設定すると、統計を利用できます。
- 秒、分、時間単位の集計
- MIN、MAX、AVG、SUM、COUNT、SUMSQ
- 手動の集計処理が不要

## よくある誤解 {#common-misconceptions}

### 「クエリーごとにインデックスを作る必要がある」 {#i-need-to-create-an-index-for-every-query}

多くの場合は不要です。自動的に適した構造を使用します。
- Tag：3 階層のパーティションインデックス
- Log：時刻による分割（インデックスは任意）
- Volatile：PRIMARY KEY の RED-BLACK ツリー
- 多くの検索は手動の追加なしで実行可能

### 「センサーごとにテーブルを作るべき」 {#i-should-create-one-table-per-sensor}

通常は、1 つの Tag テーブルにまとめます。
- 性能の改善
- 管理の簡略化
- 自動最適化

### 「Lookup は遅い」 {#lookup-tables-are-slow}

書き込みと読み取りで特性が異なります。
- 書き込みは低速（毎秒数百万に対し数百程度）
- 読み取りは高速（SELECT 向け）
- 大量入力ではなく参照データに使用

### 「Volatile は通常のテーブルと同じ」 {#volatile-tables-are-just-like-regular-tables}

次の特性に注意してください。
- すべてメモリ上に保存
- 停止時にデータを喪失
- 一時データやキャッシュに使用

## 設計原則 {#design-principles}

### 1．適切なテーブルを選ぶ {#1-choose-the-right-table-type}

用途に合う型を選択します。
- センサーデータ：Tag
- イベント：Log
- リアルタイムキャッシュ：Volatile
- 参照データ：Lookup

### 2．時刻に基づく機能を活用 {#2-leverage-time-based-features}

時系列向けの機能を使用します。
```sql
-- 推奨：DURATION を使用
SELECT * FROM logs DURATION 1 HOUR;

-- 比較的効率が低い例：手動の時刻条件
SELECT * FROM logs
WHERE _arrival_time BETWEEN TO_DATE('2025-10-10 14:00:00', 'YYYY-MM-DD HH24:MI:SS')
                        AND TO_DATE('2025-10-10 15:00:00', 'YYYY-MM-DD HH24:MI:SS');
```

### 3．保持期間を設定 {#3-implement-data-retention}

データが無制限に増えないよう管理します。
```sql
-- 日次の削除
DELETE FROM logs EXCEPT 30 DAY;
```

### 4．分析にロールアップを使用 {#4-use-rollup-for-analytics}

事前に集計したデータを検索します。
```sql
-- ロールアップによる時間単位の集計
SELECT rollup('hour', 1, time) AS hour_time, AVG(value)
FROM sensors
GROUP BY hour_time;

-- 元データからセンサー別に集計（上の例とは集計単位が異なる）
SELECT sensor_id, AVG(value) FROM sensors GROUP BY sensor_id;
```

## アーキテクチャーの概要 {#architecture-overview}

### ストレージ層 {#storage-layers}

```
┌─────────────────────────────────────┐
│         クエリーエンジン            │
├─────────────────────────────────────┤
│         メモリ管理                  │
│  ┌──────────────┐  ┌──────────────┐│
│  │ Volatile     │  │ 検索キャッシュ││
│  │ テーブル     │  │              ││
│  └──────────────┘  └──────────────┘│
├─────────────────────────────────────┤
│         ストレージエンジン          │
│  ┌──────────────┐  ┌──────────────┐│
│  │ Tag/Log      │  │ Lookup       ││
│  │ テーブル     │  │ テーブル     ││
│  └──────────────┘  └──────────────┘│
└─────────────────────────────────────┘
```

### データの流れ {#data-flow}

```
センサー / アプリケーション
     ↓
  APPEND API（一括入力）
     ↓
  書き込みバッファー（メモリ）
     ↓
  ディスクへフラッシュ（圧縮）
     ↓
  自動インデックス構築
     ↓
  クエリーエンジン
```

## 次のステップ {#next-steps}

詳しくは、次の順に参照してください。

1. [時系列データの理解](./time-series-data/)
2. [テーブルの種類](./table-types-overview/)
3. [インデックスと性能](./indexing/)

関連するガイド：
- [最初の操作](../getting-started/first-steps/)：machsql の実践
- [テーブルの種類](../table-types/)：各型の詳細
- [SQL リファレンス](../sql-reference/)：構文

## さらに詳しく {#further-reading}

- [高度な機能](../advanced-features/)：STREAM、ロールアップ
- [設定](../configuration/)：サーバー調整
- [トラブルシューティング](../troubleshooting/)：性能の改善

---

これらの概念を基に、効率的で拡張しやすいアプリケーションを設計できます。
