---
type: docs
title: 'LOOKUPの述語UPDATE'
weight: 30
toc: true
---

LOOKUPテーブルの`UPDATE`は、主キーの等価条件だけでなく、一般の述語を`WHERE`句で使用できます。
条件に一致するすべての行が更新されます。

## 構文

```sql
UPDATE table_name
   SET column_name = expression [, column_name = expression ...]
 WHERE predicate;
```

## サポートする条件の例

```sql
-- 一般列の条件
UPDATE device_lookup
SET status = 'ACTIVE'
WHERE site = 'SEOUL' AND status = 'READY';

-- 範囲と文字列の条件
UPDATE device_lookup
SET score = score + 10
WHERE score BETWEEN 10 AND 80
  AND note LIKE 'sensor-%';

-- JSONパス条件
UPDATE device_lookup
SET meta = JSON_SET(meta, '$.state', 'active')
WHERE meta->'$.region' = 'kr'
  AND JSON_EXTRACT_INTEGER(meta, '$.level') >= 3;
```

`SET`句の右辺の式は、現在の行の値を参照できます。

```sql
UPDATE device_lookup
SET score = score + 1
WHERE group_name IN ('A', 'B');
```

## 条件のサポート範囲

| 条件 | 対応 |
|------|:---:|
| `pk_col = value` | O |
| `non_pk_col = value` | O |
| `<`, `<=`, `>`, `>=`, `<>` | O |
| `BETWEEN` | O |
| `IN`, `NOT IN` | O |
| `LIKE`, `NOT LIKE` | O |
| `AND`, `OR`, `NOT` | O |
| `IS NULL`, `IS NOT NULL` | O |
| `TO_DATE(...)`による日付条件 | O |
| JSONの`->`, `JSON_EXTRACT_*`, `JSON_IS_VALID` | O |

## 制約

- 主キー列自体は`SET`句で変更できません。
- 条件に一致する行が複数あれば、複数行が更新されます。
- JSONパス文字列は単一引用符（`'$.key'`）で記述します。二重引用符はSQL識別子として解釈されます。
- 数値のJSON値を比較する場合は、`JSON_EXTRACT_INTEGER`、`JSON_EXTRACT_DOUBLE`などの型別関数を推奨します。

## 関連文書

- [LOOKUPの述語DELETE構文](../lookup-predicate-delete-syntax/)
- [LOOKUP SQL/JSON対応表](../../../../support-scope-constraints/lookup-sql-json/)
