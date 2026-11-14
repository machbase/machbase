---
type: docs
title: 'LOOKUPの述語DELETE'
weight: 40
toc: true
---

LOOKUPテーブルの`DELETE`は、主キーの等価条件だけでなく、一般の述語を`WHERE`句で使用できます。
条件に一致するすべての行が削除されます。

## 構文

```sql
DELETE FROM table_name
 WHERE predicate;
```

`WHERE`句なしで実行すると、LOOKUPテーブルの全行が削除されます。

## サポートする条件の例

```sql
-- 一般列の条件
DELETE FROM device_lookup
WHERE status = 'EXPIRED';

-- 日付と範囲の条件
DELETE FROM device_lookup
WHERE updated_at < TO_DATE('2026-01-01 00:00:00')
   OR score < 10;

-- JSONパス条件
DELETE FROM device_lookup
WHERE meta->'$.region' = 'kr'
  AND JSON_EXTRACT_INTEGER(meta, '$.level') < 2;
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
| WHERE句なしの全件削除 | O |

## 運用上の注意事項

一般述語の`DELETE`は、条件に一致するすべての行を削除します。
本番データでは、先に同じ条件で対象範囲を確認してから実行します。

```sql
SELECT COUNT(*)
FROM device_lookup
WHERE status = 'EXPIRED';

DELETE FROM device_lookup
WHERE status = 'EXPIRED';
```

## 関連文書

- [LOOKUPの述語UPDATE構文](../lookup-predicate-update-syntax/)
- [LOOKUP SQL/JSON対応表](../../../../support-scope-constraints/lookup-sql-json/)
