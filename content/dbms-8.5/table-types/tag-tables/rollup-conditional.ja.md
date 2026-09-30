---
title: 'ノイズを除外する条件付きロールアップ'
type: docs
weight: 61
toc: true
---

## 概要 {#overview}

実際の時系列データには、正常値と外れ値が混在することがよくあります。**条件付きロールアップ**（フィルター付きロールアップ）を使用すると、条件に合う行だけを集計できるため、ロールアップの統計を一貫した「精製済みの統計」に保てます。  
本ページでは、実際の回帰テストのシナリオに基づき、**ロールアップの作成 → データの読み込み → 結果の検証 → 本番への適用**の流れを説明します。

> 本ページの SQL の例は、回帰テストで使用する `extension.tc` の内容をそのまま使用します。  
> SQL 全体は [extension.tc のサンプル SQL](../rollup-conditional-extension.tc/) を参照してください。

## 条件付きロールアップが適した場面 {#when-should-you-use-conditional-rollup}

- センサーや通信のエラーによる**外れ値が、MAX や AVG などの集計値を歪める**場合
- 特定のフラグ（例：正常を表す `value2=0`）の行だけを**レポートの集計対象**にしたい場合
- 監視用とレポート用の集計を**分けて**管理したい場合

条件付きロールアップは、検索時に `WHERE` 条件を追加する方法よりも安定しています。  
条件をあらかじめ適用した集計テーブルを作成しておくため、**常に同じ品質の統計をすばやく提供**できます。

---

## 1）例のテーブルと列の意味 {#1-example-table-and-column-meanings}

この例では、`value` が集計対象の値、`value2` が正常値と外れ値を区別するフラグです。

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

## 2）ロールアップの連鎖とフィルターの定義 {#2-define-a-rollup-chain-and-add-a-filter}

秒単位と分単位のロールアップを作成し、分単位に**フィルター付きロールアップ**を追加します。

```sql
CREATE ROLLUP _tag_rollup_custom_1 ON tag(value) INTERVAL 1 SEC  EXTENSION;
CREATE ROLLUP _tag_rollup_custom_2 FROM _tag_rollup_custom_1 INTERVAL 1 MIN EXTENSION;
CREATE ROLLUP _tag_rollup_custom_3 ON tag(value) INTERVAL 1 MIN EXTENSION WHERE value2 = 0;
```

- `_tag_rollup_custom_3` は、**正常なデータだけを反映した分単位のロールアップ**です。
- `WHERE` 条件は、集計前の元の行に適用されます。
- 条件に使用した列（`value2` など）は、ロールアップテーブルには**保存されません**。

> `FIRST()` と `LAST()` を使用するには、**EXTENSION ロールアップ**が必要です。

---

## 3）外れ値を含むサンプルデータ {#3-sample-data-including-outliers}

条件付きロールアップの効果を確認できるように、`value2=1` の行を混ぜています。以下のサンプルデータは、`extension.tc` の入力データをそのまま使用しています。

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

外れ値は正常な範囲を大きく外れているため、集計結果に大きく影響します。

---

## 4）テスト用にロールアップを強制実行 {#4-force-rollup-execution-for-testing}

テスト環境では、タイミングを確実にそろえるため、ロールアップを強制実行します。

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

フィルター付きロールアップがあっても、複数の候補が一致すると、オプティマイザーは**フィルターなしのロールアップを自動的に優先**します。  
つまり、ヒントを指定しないと、**フィルター付きロールアップが気付かないうちに無視される**可能性があります。

次の場合はヒントを使用してください。

- フィルター付きの集計結果を**正確に検証**する必要がある場合
- 間隔と値列が同じロールアップが複数あり、**特定のロールアップを選ぶ**必要がある場合
- `FIRST()`/`LAST()` を使用するため、**EXTENSION ロールアップを指定**する必要がある場合

ヒントは、**意図したロールアップが実際に使用されることを保証する安全装置**です。

---

## 7）元データとフィルター結果の比較 {#7-example-summary-raw-vs-filtered}

次の表は、`extension.tc` のデータについて、分単位の集計結果から**主な統計だけをまとめた**例です。

**件数と最小値・最大値：**

| 分（rollup） | 元 COUNT | 元 MIN | 元 MAX | フィルター COUNT | フィルター MIN | フィルター MAX |
|---|---:|---:|---:|---:|---:|---:|
| 00:00 | 7 | 99 | 9900 | 6 | 99 | 130 |
| 00:01 | 6 | 92 | 2990 | 5 | 92 | 102 |
| 00:02 | 6 | 110 | 66160 | 5 | 110 | 180 |

ポイントは次のとおりです。

- **元データの集計では、外れ値によって MAX が大きくなります**。
- **フィルター付きロールアップは正常なデータだけを反映する**ため、安定した統計を得られます。

### FIRST/LAST の例 {#firstlast-examples}

`FIRST()` と `LAST()` は各バケットの先頭と末尾の値を返す関数で、**EXTENSION ロールアップが必要**です。  
次の表は、分単位の実際の FIRST/LAST の結果例です。表には対応する時刻と値を併記していますが、関数が返すのは値だけです。

| 分（rollup） | 元 FIRST(time, value) | 元 LAST(time, value) | フィルター FIRST(time, value) | フィルター LAST(time, value) |
|---|---|---|---|---|
| 00:00 | 00:00:00, 100 | 00:00:50, 99 | 00:00:00, 100 | 00:00:50, 99 |
| 00:01 | 00:01:00, 98 | 00:01:50, 102 | 00:01:00, 98 | 00:01:50, 102 |
| 00:02 | 00:02:00, 110 | 00:02:50, 180 | 00:02:00, 110 | 00:02:50, 180 |

このサンプルでは外れ値がバケットの境界にないため、FIRST/LAST の値は変わりません。  
ただし、実際の運用では外れ値が境界に位置することもあるため、**条件付きロールアップが FIRST/LAST の値にも影響する**場合があります。

---

## 8）運用への適用 {#8-practical-deployment-flow}

実際の現場では、次の流れで条件付きロールアップを適用します。

1. **データの取り込み**：センサーやログのデータを入力するときに、品質フラグ（`value2`）も一緒に記録します。
2. **ロールアップの構成**：通常のロールアップ（全データの統計）とフィルター付きロールアップ（正常データの統計）を**並行して維持**します。
3. **ダッシュボード**：通常のロールアップで全データをすばやく監視します。
4. **レポート・KPI**：**フィルター付きロールアップをヒントで固定**して使用します。
5. **原因分析**：外れ値の原因を調べるときは、元データを直接検索します。

この構成にすると、詳細なデータを失わずに、**高速な分析と信頼できる統計を両立**できます。

---

## 要点 {#summary}

- 条件付きロールアップは、**外れ値が混在する環境で統計を安定させる**実用的な方法です。
- 条件付きロールアップを確実に選択するには、**ヒントが必須**です。
- 運用では、通常のロールアップと条件付きロールアップを併用して**監視と分析を分ける**と効果的です。

---

## 関連ドキュメント {#related-documentation}

- [ロールアップテーブル](../rollup-tables/)
- [SELECT ヒント：ROLLUP_TABLE](../../../sql-reference/select-hint/)
