---
title: タグ統計
type: docs
weight: 21
toc: true
---

## はじめに

Machbase の TAG テーブルに格納された大量の時系列データを検索するときは、特定のタグ識別子（Tag ID）に対応する統計を取得することがよくあります。`NAME`（Tag ID）と `time` の条件で TAG テーブルを直接検索するのが基本ですが、大量のデータからタグごとに最小値・最大値、件数、時間範囲などの集計を計算すると、大きな計算負荷と待ち時間が発生することがあります。

この課題に対応し、タグごとの主要な統計をすばやく取得できるように、Machbase は専用のシステムビューを中心とした統計の自動集計機能を提供します。この機能は Tag ID ごとに主要な統計を事前に計算・保持するため、元の TAG テーブルのデータから直接計算する場合より大幅に高速に取得できます。Rollup テーブルと同様の性能上の利点がありますが、時間区間ではなくタグ単位の統計を提供します。

## `v$tag_table_name_stat` ビュー

TAG テーブルを作成すると、Machbase は対応する `v$tag_table_name_stat` システムビューを自動生成します。`tag_table_name` は元の TAG テーブル名です。このビューの主な役割は、Tag ID ごとに集計した統計を格納し、すぐに参照できるようにすることです。

ビューの内容は Machbase エンジンが内部で更新・管理するため、これらの一般的な統計のために、利用者が複雑な集計処理を手動で構成・管理する必要はありません。

## 統計収集の有効化

`v$tag_table_name_stat` ビューに統計が格納されるかどうかは、TAG テーブルの定義時の次の設定によって決まります。

1. **`TAG_STAT_ENABLE` プロパティ**: タグ別統計の収集機能全体を有効にするかどうかを制御するテーブルプロパティです。デフォルトは `1`（有効）です。テーブル作成時に `CREATE TAG TABLE ... TAG_STAT_ENABLE=0` と明示的に指定すると、`v$tag_table_name_stat` ビューに統計は格納されず、タグ別統計も保持されません。
2. **`SUMMARIZED` キーワード**: 値に基づく統計（最小値・最大値とそれぞれの時刻）を収集するには、TAG テーブルのスキーマで対象の値列（通常はセンサー値や指標を格納する 3 番目の列）に `SUMMARIZED` キーワードを**必ず**指定します。値列の定義で `SUMMARIZED` を省略した場合は、値に基づかない統計（件数、時間範囲、直近の時刻）だけを収集してビューに格納し、値に関するフィールドは NULL のままになります。

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

`v$tag_table_name_stat` ビューは、元の TAG テーブルにある Tag ID ごとに、事前計算した次の統計列を提供します。

| 列名 | データ型 | 説明 | `SUMMARIZED` が必要 |
| :-- | :-- | :-- | :-- |
| `NAME` | VARCHAR | 一意のタグ識別子（Tag ID）。 | いいえ |
| `ROW_COUNT` | ULONG | この Tag ID に記録されたデータ（行）の総数。 | いいえ |
| `MIN_TIME` | DATETIME | この Tag ID のすべてのデータのうち最も早い時刻。 | いいえ |
| `MAX_TIME` | DATETIME | この Tag ID のすべてのデータのうち最も遅い時刻。 | いいえ |
| `MIN_VALUE` | DOUBLE | この Tag ID について `SUMMARIZED` 列に記録された最小値。 | **はい** |
| `MIN_VALUE_TIME` | DATETIME | `MIN_VALUE` が最初に現れたデータの時刻。 | **はい** |
| `MAX_VALUE` | DOUBLE | この Tag ID について `SUMMARIZED` 列に記録された最大値。 | **はい** |
| `MAX_VALUE_TIME` | DATETIME | `MAX_VALUE` が最初に現れたデータの時刻。 | **はい** |
| `RECENT_ROW_TIME` | DATETIME | この Tag ID に最後に挿入されたデータの時刻。 | いいえ |

*注: 元の TAG テーブルの `SUMMARIZED` 列が整数型でも、`MIN_VALUE` と `MAX_VALUE` は DOUBLE です。*

## 統計の検索

`v$tag_table_name_stat` ビューの主な利点は、大量になりうる元の TAG テーブルのデータを走査せずに、主要な統計を高速に取得できることです。実際のデータを確認するときは、統計ビューから時刻を取得し、元の TAG テーブルの検索と組み合わせます。

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

タグ別統計は性能面で大きな利点がありますが、次の制約があります。

* **統計の種類は固定**: ビューが提供するのは、タグ識別子に加えて、あらかじめ決められた 8 種類の統計です。標準偏差、パーセンタイルなど、別の統計やより複雑な統計が必要な場合は、元の TAG テーブルで直接計算するか、Rollup テーブルなどの機能を使用します。
* **元のデータ品質に依存**: `v$tag_table_name_stat` ビューに格納される統計の正確さは、元の TAG テーブルに取り込まれたデータの品質に直接左右されます。誤った値やノイズも集計値（`MIN_VALUE`、`MAX_VALUE` など）に反映されます。入力データの検証・クレンジングを推奨します。
* **設定条件**: 前述のとおり、すべての統計を収集するには、`TAG_STAT_ENABLE=1` プロパティと、対象の値列への `SUMMARIZED` キーワードの指定が必要です。設定が正しくない場合は、ビューの統計の一部が欠けるか、まったく格納されません。
* **反映のタイミング**: 統計は入力直後ではなく、少し遅れてビューに反映されます。入力直後に検索すると、入力したばかりのデータがまだ統計に含まれていない場合があります。

## 使用例

タグ別統計の設定と使い方を、実際の例で示します。

### 前提: スキーマ作成とデータ取り込み

次の例では、`tag` という TAG テーブルを作成し、データを取り込んであるものとします。

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

**2. データの取り込み（`machbase-neo` の import を使用した例）:**

`tag_name,unix_timestamp,value` 形式の CSV ファイル `homes.csv` があるものとします。`machbase-neo shell` は現在のディレクトリを `/work` にマウントするため、`homes.csv` があるディレクトリでコマンドを実行します。

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

### 設定による統計収集の違い（制約事項）

設定によって統計収集がどう変わるかを示します。

**シナリオの準備:** 設定の異なる 3 つのテーブルを作成し、*同じ*サンプルデータを取り込みます。

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

各テーブルに同じデータを挿入してから統計ビューを検索すると、設定によって収集される項目が異なることを確認できます。

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

これらの例から、タグ別統計の機能をすべて活用するには、テーブル定義（特に `SUMMARIZED` キーワード）と `TAG_STAT_ENABLE` プロパティを正しく指定する必要があることがわかります。
