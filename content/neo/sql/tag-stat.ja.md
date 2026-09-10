---
title: タグ統計
type: docs
weight: 21
toc: true
---

## はじめに

Machbase の TAG テーブルでは、特定のタグ識別子（Tag ID）に対応する時系列データの統計をよく検索します。`NAME` と時刻の条件で直接検索できますが、大量のデータからタグごとの最小値・最大値、件数、時間範囲を計算すると、負荷と待ち時間が増加します。

Machbase は、専用のシステムビューでタグごとの主要な統計を事前計算・保持します。生データから毎回計算する場合より高速に取得できます。Rollup の事前集計と同様の効果がありますが、時間区間ではなくタグ単位の統計を提供します。

## `v$tag_table_name_stat` ビュー

TAG テーブルを作成すると、対応する `v$tag_table_name_stat` システムビューを自動生成します。`tag_table_name` は元の TAG テーブル名です。このビューは Tag ID ごとに集計した統計を提供します。

ビューの内容は Machbase エンジンが内部で更新・管理するため、利用者が集計処理を個別に構成する必要はありません。

## 統計収集の有効化

統計の収集内容は、TAG テーブルの定義時の次の設定によって決まります。

1. **`TAG_STAT_ENABLE` プロパティ**: タグ別統計の収集を制御します。デフォルトは `1`（有効）です。`CREATE TAG TABLE ... TAG_STAT_ENABLE=0` と指定すると、ビューにタグ別統計は格納されません。
2. **`SUMMARIZED` キーワード**: 最小値・最大値とその時刻を収集するには、対象の値列（通常はセンサー値を格納する 3 番目の列）に `SUMMARIZED` を指定します。省略した場合は件数と時間範囲、直近の時刻だけを収集し、値に関するフィールドは NULL になります。

**構文例（すべての統計を有効化）:**

```sql
CREATE TAG TABLE device_metrics (
    name VARCHAR(80) PRIMARY KEY, -- タグ ID 列
    time DATETIME BASETIME,        -- タイムスタンプ列
    value DOUBLE SUMMARIZED        -- SUMMARIZED を指定した値列
)
TAG_STAT_ENABLE=1; -- デフォルト値のため省略可能
```

## 提供する統計

`v$tag_table_name_stat` は、元の TAG テーブルの Tag ID ごとに次の統計列を提供します。

| 列名 | データ型 | 説明 | `SUMMARIZED` が必要 |
| :-- | :-- | :-- | :-- |
| `NAME` | VARCHAR | 一意のタグ識別子（Tag ID）。 | いいえ |
| `ROW_COUNT` | ULONG | タグのデータ件数。 | いいえ |
| `MIN_TIME` | DATETIME | タグのデータに記録された最も早い時刻。 | いいえ |
| `MAX_TIME` | DATETIME | タグのデータに記録された最も遅い時刻。 | いいえ |
| `MIN_VALUE` | DOUBLE | `SUMMARIZED` 列に記録されたタグの最小値。 | **はい** |
| `MIN_VALUE_TIME` | DATETIME | `MIN_VALUE` が最初に現れたデータの時刻。 | **はい** |
| `MAX_VALUE` | DOUBLE | `SUMMARIZED` 列に記録されたタグの最大値。 | **はい** |
| `MAX_VALUE_TIME` | DATETIME | `MAX_VALUE` が最初に現れたデータの時刻。 | **はい** |
| `RECENT_ROW_TIME` | DATETIME | タグに最後に挿入されたデータの時刻。 | いいえ |

*`MIN_VALUE` と `MAX_VALUE` は、統計ビューでは DOUBLE 型で公開します。*

## 統計の検索

大量の生データを走査せず、統計ビューから主要な統計を高速に取得できます。

**基本的なクエリパターン:**

```sql
-- 特定タグの最小・最大時刻を取得
SELECT min_time, max_time
FROM v$your_tag_table_stat -- your_tag_table を実際のテーブル名に置き換える
WHERE name = 'specific_tag_id';

-- 複数タグの最小・最大時刻を取得
SELECT name, min_time, max_time
FROM v$your_tag_table_stat
WHERE name IN ('tag_id_1', 'tag_id_2', 'tag_id_3');

-- 特定タグの件数と最小・最大値を取得（SUMMARIZED が必要）
SELECT row_count, min_value, max_value
FROM v$your_tag_table_stat
WHERE name = 'specific_tag_id';

-- すべてのタグの全統計を取得
SELECT *
FROM v$your_tag_table_stat;

-- タグに最後に挿入された実データを取得
SELECT *
FROM your_tag_table
WHERE name = 'specific_tag_id'
  AND time = (SELECT recent_row_time
              FROM v$your_tag_table_stat
              WHERE name = 'specific_tag_id');

-- タグの最小値に対応する実データを取得
SELECT *
FROM your_tag_table
WHERE name = 'specific_tag_id'
  AND time = (SELECT min_value_time
              FROM v$your_tag_table_stat
              WHERE name = 'specific_tag_id');
```

## 制約事項

タグ別統計には次の制約があります。

* **統計の種類は固定**: タグ識別子に加えて 8 種類の統計を提供します。標準偏差、パーセンタイルなどが必要な場合は、元のテーブルで直接計算するか、Rollup などの機能を使用します。
* **元のデータ品質に依存**: 誤った値やノイズも MIN_VALUE、MAX_VALUE などに反映されます。入力データの検証・クレンジングを推奨します。
* **設定条件**: すべての統計を使用するには、`TAG_STAT_ENABLE=1` と値列の `SUMMARIZED` が必要です。設定が不適切な場合は、一部またはすべての統計が取得できません。

## 使用例

タグ別統計の設定と検索の例を示します。

### 前提: スキーマ作成とデータ取り込み

次の例では `tag` という TAG テーブルを作成し、データを取り込みます。

**1. スキーマ定義（統計を有効化）:**

```sql
-- 必要に応じて既存テーブルを削除
-- DROP TABLE tag;

-- 統計を有効にし、value に SUMMARIZED を指定して TAG テーブルを作成
CREATE TAG TABLE tag (
    name VARCHAR(80) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED -- 値の統計に必要な SUMMARIZED を指定
)
tag_partition_count=1, -- プロパティの例
TAG_STAT_ENABLE=1;    -- デフォルトは 1 だが明示指定
```

**2. データの取り込み（machbase-neo の import）:**

`tag_name,unix_timestamp,value` 形式の CSV ファイル `homes.csv` があるものとします。

```bash
# 取り込みコマンドの例（必要に応じてパスとオプションを変更）
machbase-neo shell import --input C:/path/to/homes.csv --timeformat s --method append TAG
```

### 統計と基本クエリの確認

**1. 統計ビューの構造を確認:**

```sql
-- 自動生成された統計ビューの列と型を表示
DESC v$tag_stat;
```

**2. タグごとの件数を確認:**

```sql
-- 統計ビューで効率的に件数を取得
SELECT name, row_count
FROM v$tag_stat
ORDER BY name;

-- 元のテーブルからの直接集計と比較（大量データでは遅くなる）
SELECT name, COUNT(*) AS direct_count
FROM tag
GROUP BY name
ORDER BY name;
```

**3. 時間範囲の取得:**

```sql
-- 特定タグの最小・最大時刻を取得
SELECT name, min_time, max_time
FROM v$tag_stat
WHERE name IN ('use', 'gen', 'temperature');
```

**4. 統計に対応する実データの検索:**

```sql
-- use タグに最後に追加されたレコード全体を取得
SELECT *
FROM tag
WHERE name = 'use'
  AND time = (SELECT recent_row_time FROM v$tag_stat WHERE name = 'use');

-- temperature の最小値に対応するレコード全体を取得
SELECT *
FROM tag
WHERE name = 'temperature'
  AND time = (SELECT min_value_time FROM v$tag_stat WHERE name = 'temperature');

-- gen タグの最大時刻に対応する値を取得
SELECT value
FROM tag
WHERE name = 'gen'
  AND time = (SELECT max_time FROM v$tag_stat WHERE name = 'gen');
```

### 設定による統計収集の違い

設定によって統計収集がどう変わるかを確認します。

**準備:** 設定の異なる 3 つのテーブルに、同じサンプルデータを取り込みます。

```sql
-- テーブル 1: すべての統計を有効化（標準構成）
DROP TABLE IF EXISTS stat1;
CREATE TAG TABLE stat1 (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE SUMMARIZED) TAG_STAT_ENABLE=1;

-- テーブル 2: SUMMARIZED を省略
DROP TABLE IF EXISTS stat2;
CREATE TAG TABLE stat2 (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE) TAG_STAT_ENABLE=1; -- SUMMARIZED なし

-- テーブル 3: プロパティで統計を無効化
DROP TABLE IF EXISTS stat3;
CREATE TAG TABLE stat3 (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE SUMMARIZED) TAG_STAT_ENABLE=0; -- 統計を明示的に無効化

-- 3 つのテーブルに同じサンプルデータを挿入
INSERT INTO stat1 VALUES('tag-0', TO_DATE('2022-08-11'), 10);
INSERT INTO stat1 VALUES('tag-0', TO_DATE('2022-08-13'), 20);
INSERT INTO stat1 VALUES('tag-0', TO_DATE('2022-08-14'), 5);
INSERT INTO stat1 VALUES('tag-1', TO_DATE('2023-08-12'), 200);
INSERT INTO stat1 VALUES('tag-1', TO_DATE('2023-08-13'), 50);
INSERT INTO stat1 VALUES('tag-1', TO_DATE('2023-08-15'), 120);

INSERT INTO stat2 VALUES('tag-0', TO_DATE('2022-08-11'), 10);
INSERT INTO stat2 VALUES('tag-0', TO_DATE('2022-08-13'), 20);
INSERT INTO stat2 VALUES('tag-0', TO_DATE('2022-08-14'), 5);
INSERT INTO stat2 VALUES('tag-1', TO_DATE('2023-08-12'), 200);
INSERT INTO stat2 VALUES('tag-1', TO_DATE('2023-08-13'), 50);
INSERT INTO stat2 VALUES('tag-1', TO_DATE('2023-08-15'), 120);

INSERT INTO stat3 VALUES('tag-0', TO_DATE('2022-08-11'), 10);
INSERT INTO stat3 VALUES('tag-0', TO_DATE('2022-08-13'), 20);
INSERT INTO stat3 VALUES('tag-0', TO_DATE('2022-08-14'), 5);
INSERT INTO stat3 VALUES('tag-1', TO_DATE('2023-08-12'), 200);
INSERT INTO stat3 VALUES('tag-1', TO_DATE('2023-08-13'), 50);
INSERT INTO stat3 VALUES('tag-1', TO_DATE('2023-08-15'), 120);

```

**結果の確認:**

```sql
-- テーブル 1 の統計を検索（全統計）
SELECT * FROM v$stat1_stat;
-- 想定: MIN/MAX_VALUE とその時刻を含む全列に値が入る。

-- テーブル 2 の統計を検索（SUMMARIZED なし）
SELECT * FROM v$stat2_stat;
-- 想定: MIN_VALUE、MIN_VALUE_TIME、MAX_VALUE、MAX_VALUE_TIME は NULL。
--          ROW_COUNT、MIN_TIME、MAX_TIME、RECENT_ROW_TIME は値が入る。

-- テーブル 3 の統計を検索（TAG_STAT_ENABLE=0）
SELECT * FROM v$stat3_stat;
-- 想定: 行が返されない。ビュー自体が未作成の場合はエラー。
--          このテーブルでは統計収集を完全に無効化している。
```

タグ別統計をすべて使用するには、`SUMMARIZED` と `TAG_STAT_ENABLE` を正しく指定してください。