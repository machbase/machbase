---
title: 'ノイズを除外する条件付きロールアップ'
type: docs
weight: 61
toc: true
---

## 概要 {#overview}

実際の時系列データには正常値と外れ値が混在します。条件付き（フィルター付き）ロールアップは、条件に合う行だけを集計し、統計の一貫性を保ちます。
回帰テストに基づき、作成 → 読み込み → 結果の検証 → 本番適用の順に説明します。

> 本ページの SQL は `extension.tc` と同じデータを使用します。
> 全体は [extension.tc のサンプル SQL](../rollup-conditional-extension.tc/) を参照してください。

## 適した用途 {#when-should-you-use-conditional-rollup}

- 外れ値が MAX や AVG を歪める場合
- 特定のフラグ（例：`value2=0`）の行だけを集計する場合
- 監視用とレポート用の集計を分ける場合

検索時に `WHERE` を追加する方法と比べ、あらかじめ不要な値を除いた統計を、安定した性能で取得できます。

---

## 1）例のテーブルと列 {#1-example-table-and-column-meanings}

`value` は集計値、`value2` はフラグです。

- `value2=0`：正常
- `value2=1`：外れ値

```sql
CREATE TAG TABLE tag (
    name   VARCHAR(20) PRIMARY KEY,
    time   DATETIME BASETIME,
    value  DOUBLE SUMMARIZED,
    value2 DOUBLE
);
```

---

## 2）ロールアップの連鎖とフィルター {#2-define-a-rollup-chain-and-add-a-filter}

秒と分のロールアップを作成し、分単位にフィルター付きロールアップを追加します。

```sql
CREATE ROLLUP _tag_rollup_custom_1 ON tag(value) INTERVAL 1 SEC  EXTENSION;
CREATE ROLLUP _tag_rollup_custom_2 FROM _tag_rollup_custom_1 INTERVAL 1 MIN EXTENSION;
CREATE ROLLUP _tag_rollup_custom_3 ON tag(value) INTERVAL 1 MIN EXTENSION WHERE value2 = 0;
```

- `_tag_rollup_custom_3` がフィルター付きの分単位ロールアップです。
- `WHERE` は集計前の元データに適用します。
- `value2` など条件に使用する列は、ロールアップテーブルには保存しません。

> `FIRST()` と `LAST()` には EXTENSION ロールアップが必要です。

---

## 3）外れ値を含むサンプルデータ {#3-sample-data-including-outliers}

`extension.tc` のデータを使用します。

```sql
INSERT INTO tag VALUES('APPL', '2020-01-01 00:00:00', 100,  0);
INSERT INTO tag VALUES('APPL', '2020-01-01 00:00:10', 101,  0);
INSERT INTO tag VALUES('APPL', '2020-01-01 00:00:11', 130,  0);
INSERT INTO tag VALUES('APPL', '2020-01-01 00:00:20', 120,  0);
INSERT INTO tag VALUES('APPL', '2020-01-01 00:00:30', 110,  0);
INSERT INTO tag VALUES('APPL', '2020-01-01 00:00:40', 9900, 1);
INSERT INTO tag VALUES('APPL', '2020-01-01 00:00:50', 99,   0);

INSERT INTO tag VALUES('APPL', '2020-01-01 00:01:00', 98,  0);
INSERT INTO tag VALUES('APPL', '2020-01-01 00:01:10', 94,  0);
INSERT INTO tag VALUES('APPL', '2020-01-01 00:01:20', 2990, 1);
INSERT INTO tag VALUES('APPL', '2020-01-01 00:01:30', 92,  0);
INSERT INTO tag VALUES('APPL', '2020-01-01 00:01:40', 99,  0);
INSERT INTO tag VALUES('APPL', '2020-01-01 00:01:50', 102, 0);

INSERT INTO tag VALUES('APPL', '2020-01-01 00:02:00', 110, 0);
INSERT INTO tag VALUES('APPL', '2020-01-01 00:02:10', 120, 0);
INSERT INTO tag VALUES('APPL', '2020-01-01 00:02:20', 140, 0);
INSERT INTO tag VALUES('APPL', '2020-01-01 00:02:30', 66160, 1);
INSERT INTO tag VALUES('APPL', '2020-01-01 00:02:40', 170, 0);
INSERT INTO tag VALUES('APPL', '2020-01-01 00:02:50', 180, 0);
```

---

## 4）テスト用に集計を強制実行 {#4-force-rollup-execution-for-testing}

テストのタイミングをそろえるため、ロールアップを強制実行します。

```sql
EXEC ROLLUP_FORCE(_tag_rollup_custom_1);
EXEC ROLLUP_FORCE(_tag_rollup_custom_2);
EXEC ROLLUP_FORCE(_tag_rollup_custom_3);
```

---

## 5）結果の検索と比較 {#5-query-and-compare-results}

### 5-1．元データの通常集計 {#5-1-normal-aggregation-raw-data}
```sql
SELECT rollup('min', 1, time) AS rt,
       COUNT(value), MIN(value), MAX(value),
       FIRST(time, value), LAST(time, value)
  FROM tag
 GROUP BY rt
 ORDER BY rt;
```

### 5-2．ヒントでフィルター付きロールアップを指定 {#5-2-force-the-filtered-rollup-with-a-hint}
```sql
SELECT /*+ ROLLUP_TABLE(_tag_rollup_custom_3) */
       rollup('min', 1, time) AS rt,
       COUNT(value), MIN(value), MAX(value),
       FIRST(time, value), LAST(time, value)
  FROM tag
 GROUP BY rt
 ORDER BY rt;
```

---

## 6）ヒントが必要な理由 {#6-why-the-hint-is-required}

複数の候補が一致すると、オプティマイザーはフィルターなしのロールアップを優先します。
強制指定しないと、意図しないロールアップが使用される可能性があります。

次の場合はヒントを使用します。

- フィルター付きの結果を検証する必要がある
- 間隔と値列が同じロールアップが複数ある
- `FIRST()`/`LAST()` に EXTENSION が必要

ヒントで、意図したロールアップの使用を保証します。

---

## 7）元データとフィルター結果の比較 {#7-example-summary-raw-vs-filtered}

**件数と最小値・最大値：**

| 分 | 元 COUNT | 元 MIN | 元 MAX | フィルター COUNT | フィルター MIN | フィルター MAX |
|---|---:|---:|---:|---:|---:|---:|
| 00:00 | 7 | 99 | 9900 | 6 | 99 | 130 |
| 00:01 | 6 | 92 | 2990 | 5 | 92 | 102 |
| 00:02 | 6 | 110 | 66160 | 5 | 110 | 180 |

確認できる点：

- 元データの MAX は、外れ値により大きくなります。
- フィルター付きでは外れ値を除外し、安定した統計を取得できます。

### FIRST/LAST の例 {#firstlast-examples}

`FIRST()` と `LAST()` は、各バケットの先頭と末尾の値を示します。EXTENSION ロールアップが必要です。表は対応する時刻と値を併記していますが、関数の戻り値は値です。

| 分 | 元 FIRST(time, `value`) | 元 LAST(time, `value`) | フィルター FIRST(time, `value`) | フィルター LAST(time, `value`) |
|---|---|---|---|---|
| 00:00 | 00:00:00, 100 | 00:00:50, 99 | 00:00:00, 100 | 00:00:50, 99 |
| 00:01 | 00:01:00, 98 | 00:01:50, 102 | 00:01:00, 98 | 00:01:50, 102 |
| 00:02 | 00:02:00, 110 | 00:02:50, 180 | 00:02:00, 110 | 00:02:50, 180 |

このデータでは外れ値が境界にないため、FIRST/LAST は変わりません。
実際の負荷では境界値も変わり得るため、フィルター付きの集計が有効です。

---

## 8）運用への適用 {#8-practical-deployment-flow}

1. 品質フラグ `value2` と一緒に元データを取り込みます。
2. 通常とフィルター付きの 2 種類のロールアップを維持します。
3. ダッシュボードでは通常のロールアップを使用できます。
4. レポートや KPI では、ヒントでフィルター付きを指定します。
5. 原因分析には元データを使用できます。

詳細を残したまま、高速な分析と信頼できる統計を得られます。

---

## 要点 {#정리}

- 条件付きロールアップは、外れ値が混在するデータの統計を安定させます。
- 条件付きロールアップを確実に選択するには、ヒントを指定します。
- 通常のロールアップも併用すると、監視と品質分析の両方に対応できます。

## 関連ドキュメント {#related-documentation}

- [ロールアップテーブル](../rollup-tables/)
- [SELECT ヒント：ROLLUP_TABLE](../../../sql-reference/select-hint/)
