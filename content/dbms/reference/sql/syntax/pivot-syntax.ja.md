---
type: docs
title: 'PIVOT'
weight: 70
toc: true
---

`PIVOT`は行方向のデータを列方向へ変換する構文です。GROUP BYの集計結果を列に並べ替え、読みやすいレポート形式で表示する場合に使用します。

> PIVOT構文はMachbase 5.6以降でサポートします。

## 構文

```sql
SELECT *
  FROM (inline_view)
 PIVOT (aggregate_function(value_col) FOR category_col IN ('val1', 'val2', ...))
[WHERE ...]
```

- `inline_view`でPIVOT句に使用されない列をGROUP BYします。
- `FOR category_col IN (...)`: ピボットの基準列と、出力列へ変換する値の一覧を指定します。
- 結果列名はIN句に指定した文字列値になります。

## 例

### センサー別集計を列へ変換

```sql
-- インラインビューを使用したPIVOT
SELECT * FROM (
    SELECT regtime, tagid, dvalue FROM result_d
     WHERE regtime BETWEEN TO_DATE('2024-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
                       AND TO_DATE('2024-01-02 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
) PIVOT (
    SUM(dvalue) FOR tagid IN ('FRONT_AXIS_TORQUE', 'REAR_AXIS_TORQUE', 'HOIST_AXIS_TORQUE', 'SLIDE_AXIS_TORQUE')
)
WHERE FRONT_AXIS_TORQUE >= 40 AND REAR_AXIS_TORQUE >= 20;
```

### CASE文より簡潔な表現

```sql
-- PIVOTを使わずCASEを使用
SELECT regtime,
       SUM(CASE WHEN tagid = 'SENSOR_A' THEN dvalue ELSE 0 END) AS sensor_a,
       SUM(CASE WHEN tagid = 'SENSOR_B' THEN dvalue ELSE 0 END) AS sensor_b
  FROM result_d
 GROUP BY regtime;

-- PIVOTで簡潔に表現
SELECT * FROM (
    SELECT regtime, tagid, dvalue FROM result_d
) PIVOT (SUM(dvalue) FOR tagid IN ('SENSOR_A', 'SENSOR_B'));
```

### TAGテーブルとPIVOTの組み合わせ

```sql
SELECT * FROM (
    SELECT name, time, value
      FROM sensor_tag
     WHERE time BETWEEN TO_DATE('2024-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
                    AND TO_DATE('2024-01-01 01:00:00', 'YYYY-MM-DD HH24:MI:SS')
) PIVOT (
    AVG(value) FOR name IN ('sensor-01', 'sensor-02', 'sensor-03')
);
```

## 制約

- PIVOTは必ずインラインビュー（サブクエリ）と併用してください。
- インラインビューではPIVOT集計列（`value_col`）と基準列（`category_col`）以外の全列が自動的にGROUP BYの対象になります。
- IN句の値はコンパイル時に確定するリテラルである必要があります（動的な列一覧は不可）。

## 関連ドキュメント

- [SELECT hint syntax](../select-hint-syntax/) — SELECTヒントの構文と使用例
