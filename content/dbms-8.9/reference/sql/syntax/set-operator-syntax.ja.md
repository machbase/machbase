---
type: docs
title: '集合演算子'
weight: 60
toc: true
---

集合演算子は2つ以上の`SELECT`クエリ結果を結合したり、共通集合や差集合を求めたりする演算子です。

> Machbaseは現在、集合演算子`UNION ALL`のみをサポートします。重複を除去する`UNION`、
> `INTERSECT`、`EXCEPT`はサポートしません。

## UNION ALL

2つのクエリ結果を重複除去せずに結合します。

```sql
select_stmt UNION ALL select_stmt
```

```sql
SELECT i1, i2 FROM table_1
UNION ALL
SELECT c1, c2 FROM table_2;
```

## 使用条件

2つの`SELECT`文は次の条件をすべて満たす必要があります。

1. **列数が同じ**であること。
2. **列の型が同じか互換性がある**こと。

1つでも条件を満たさなければエラーを返します。

### 型の互換規則

| 組み合わせ | 互換性 | 結果の型 |
|------|-----------|-----------|
| 符号付き整数 ↔ 符号なし整数 | X | エラー |
| 整数 ↔ 実数 | O | 実数型 |
| 文字型（異なる長さ） | O | 処理可能 |
| IPv6 ↔ IPv4 | X | エラー |

- 結果列名は左側のクエリの列名に従います。

## 例

```sql
-- 2つのテーブルのデータを結合
SELECT id, name FROM active_devices
UNION ALL
SELECT id, name FROM inactive_devices;

-- 異なる期間の統計を結合
SELECT 'Q1' AS quarter, SUM(value) AS total FROM sales WHERE month BETWEEN 1 AND 3
UNION ALL
SELECT 'Q2' AS quarter, SUM(value) AS total FROM sales WHERE month BETWEEN 4 AND 6;

-- 3つのクエリを結合
SELECT name, time, value FROM sensor_a WHERE time > TO_DATE('2024-01-01', 'YYYY-MM-DD')
UNION ALL
SELECT name, time, value FROM sensor_b WHERE time > TO_DATE('2024-01-01', 'YYYY-MM-DD')
UNION ALL
SELECT name, time, value FROM sensor_c WHERE time > TO_DATE('2024-01-01', 'YYYY-MM-DD');
```

## 注意事項

- `UNION ALL`は重複行を削除しません。重複除去が必要な場合は`UNION ALL`結果をサブクエリにし、`DISTINCT`や`GROUP BY`を適用します。
- `FROM`句のないリテラル`SELECT`同士の`UNION ALL`はサポートしません。
- 結果行の順序は保証しません。ソートが必要な場合は全体をインラインビューにし、外側で`ORDER BY`を適用します。

```sql
-- ソートが必要な場合
SELECT * FROM (
    SELECT id, name, time FROM log_a
    UNION ALL
    SELECT id, name, time FROM log_b
) ORDER BY time DESC;
```

## 関連ドキュメント

- [SELECT syntax](../select-syntax/) — SELECTの基本構文
- [WITH / CTE syntax](../cte-syntax/) — CTEでUNION ALLを使用
- [VIEW syntax](../view-syntax/) — UNION ALLを含むVIEWの作成
