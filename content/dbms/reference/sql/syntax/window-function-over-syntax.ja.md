---
type: docs
title: 'ウィンドウ関数 / OVER'
weight: 80
toc: true
---

Machbaseの`LAG()`と`LEAD()`は、クエリ結果の各行から前または後の行の値を参照します。
例えばセンサー別の測定値を時刻順に比較し、直前の測定値との差を求められます。
`GROUP BY`集計と異なり、複数行を1行に集約しません。

## 構文

```sql
LAG(value_expression, offset) OVER (
    [PARTITION BY partition_expression]
    [ORDER BY order_expression]
)

LEAD(value_expression, offset) OVER (
    [PARTITION BY partition_expression]
    [ORDER BY order_expression]
)
```

| 要素 | 説明 |
|------|------|
| `value_expression` | 前または後の行から取得する値 |
| `offset` | 現在行から離れた行数。1以上の整数を指定 |
| `PARTITION BY` | 比較する行をグループに分ける単一の式。省略すると全結果を1グループとして処理 |
| `ORDER BY` | グループ内の比較順序を決める単一の式 |

`OVER`は必須ですが、括弧内の`PARTITION BY`と`ORDER BY`は省略できます。時刻順の比較には
`ORDER BY time`などの基準を明示してください。ソートキーが同じ行の順序は、この式だけでは区別できません。
最終結果の出力順序が必要な場合は、SELECT文の末尾にも`ORDER BY`を指定します。

## 対応するウィンドウ関数

<a id="이동-참조-함수"></a>

| 関数 | 説明 |
|------|------|
| `LAG(value, n)` | 同じグループで現在行のn行前の値 |
| `LEAD(value, n)` | 同じグループで現在行のn行後の値 |

参照する行がなければNULLを返します。`offset`は時間間隔ではなく行数です。測定間隔が不規則な場合、
直前の行が必ず1秒前や1分前の測定値とは限りません。

<a id="순위-함수"></a>
<a id="집계-윈도우-함수"></a>

### 他のDBMSのウィンドウ構文との違い

次の構文をMachbaseの`LAG`/`LEAD`構文と混同しないでください。

- `ROW_NUMBER()`、`RANK()`、`DENSE_RANK()`、`FIRST_VALUE()`、`LAST_VALUE()`はサポートしません。
- `SUM(...) OVER (...)`や`AVG(...) OVER (...)`などの集約ウィンドウ関数はサポートしません。
- `ROWS`/`RANGE`フレームと`UNBOUNDED PRECEDING`、`CURRENT ROW`などのフレーム境界は指定できません。
- `OVER`内の`PARTITION BY`と`ORDER BY`には、それぞれ1つの式のみ指定できます。`ORDER BY`の後に`ASC`/`DESC`を指定する構文もサポートしません。

結果行に番号を付ける`ROWNUM()`と連続区間番号を求める`SERIESNUM()`は、
[ウィンドウ/系列関数](../../functions/series/)で説明します。

## 例

### LAG / LEAD: 前後の値の比較

次の例は、`name`、`time`、`value`列を持つ`sensor_tag`テーブルを使用します。

```sql
SELECT name, time, value,
       LAG(value, 1) OVER (PARTITION BY name ORDER BY time) AS prev_value,
       LEAD(value, 1) OVER (PARTITION BY name ORDER BY time) AS next_value,
       value - LAG(value, 1) OVER (PARTITION BY name ORDER BY time) AS delta
  FROM sensor_tag
 WHERE name = 'TEMP-01'
   AND time >= TO_DATE('2024-01-01', 'YYYY-MM-DD')
 ORDER BY name, time;
```

`prev_value`と`next_value`は参照範囲内の前・次の値です。先頭行の`prev_value`と最終行の`next_value`は
NULLです。`WHERE`で除外した過去の行は比較対象に含まれないため、先頭行の差も必要な場合は参照範囲を過去へ広げます。

<a id="순위-함수-1"></a>
<a id="이동-평균"></a>
<a id="누적-합계"></a>

### 集計結果の前の値との比較

タグ別の時間区間を先に集計し、集計値間の変化を比較できます。次の例は、時間単位のROLLUPを参照できる
`sensor_tag`テーブルを前提とします。

```sql
SELECT name, bucket, avg_val,
       LAG(avg_val, 1) OVER (PARTITION BY name ORDER BY bucket) AS prev_avg
  FROM (
      SELECT name,
             rollup('hour', 1, time) AS bucket,
             AVG(value)              AS avg_val
        FROM sensor_tag
       WHERE time BETWEEN TO_DATE('2024-01-01', 'YYYY-MM-DD')
                      AND TO_DATE('2024-07-01', 'YYYY-MM-DD')
       GROUP BY name, bucket
  ) t
 ORDER BY name, bucket;
```

このクエリは、区間別の平均と直前区間の平均を比較します。移動平均や累積合計を計算するクエリではありません。
データのない区間は自動補完しません。

## 性能上の注意

ウィンドウ計算にはグループ分割、ソート、前後の行値の保持が必要です。時間範囲とタグ条件で対象行を減らし、
長期傾向の比較は集計結果に適用すると処理行数を減らせます。

`LAG`/`LEAD`はSELECTの結果式で使用します。`WHERE`、`HAVING`、`GROUP BY`、`ORDER BY`、JOINの`ON`条件で
直接呼び出さないでください。計算値で絞り込むには、外側のSELECTからインラインビューの結果列を参照します。

## 関連ドキュメント

- [ウィンドウ/系列関数](../../functions/series/) — `ROWNUM()`と`SERIESNUM()`
- [PIVOT構文](../pivot-syntax/) — 行を列へ変換
- [SERIES BY構文](../series-syntax/) — 連続区間の抽出
