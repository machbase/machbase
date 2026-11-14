---
type: docs
title: 'JSON型のテーブルタイプ別サポート範囲'
weight: 10
toc: true
---

JSON型の列を各テーブルタイプで使用する場合のサポート範囲を示します。

## サポート範囲の概要

| テーブルタイプ | JSON列の作成 | JSON path query | JSON PK | 備考 |
|------------|:-------------:|:---------------:|:-------:|------|
| TAG | O | O | X | JSON列とJSON関数をサポート。PKは非対応 |
| LOG | O | O | X | JSON列とJSON関数をサポート |
| LOOKUP | O | O | X | 通常の列としてサポート。JSONパスインデックスは非対応 |
| VOLATILE | X | X | X | JSON列の作成不可 |
| TRANSACTION | O | O | X | JSON列とJSON関数をサポート |

## LOOKUPテーブル

LOOKUPテーブルはJSON型の列を通常の列としてサポートします。

```sql
CREATE LOOKUP TABLE config_lookup (
    key    VARCHAR(64) PRIMARY KEY,
    site   VARCHAR(32),
    config JSON
);

INSERT INTO config_lookup VALUES (
    'device-001',
    'SEOUL',
    '{"region":"kr","level":3,"state":"ready"}'
);

SELECT key
FROM config_lookup
WHERE config->'$.region' = 'kr'
  AND JSON_EXTRACT_INTEGER(config, '$.level') >= 3;
```

JSON列は`JSON_SET`、`JSON_SET_JSON`、`JSON_REMOVE`などのJSON関数で更新できます。

```sql
UPDATE config_lookup
SET config = JSON_SET(config, '$.state', 'active')
WHERE site = 'SEOUL';
```

ただし、JSON列は主キーとして宣言できません。

```sql
-- エラー
CREATE LOOKUP TABLE invalid_lookup (
    config JSON PRIMARY KEY
);
```

## VOLATILEテーブル

VOLATILEテーブルではJSON型の列を作成できません。

```sql
CREATE VOLATILE TABLE session_data (
    session_id VARCHAR(64) PRIMARY KEY,
    payload    JSON
);
```

## JSON関連関数のテーブルタイプ別サポート

| 関数/演算子 | TAG | LOG | LOOKUP | VOLATILE | TRANSACTION |
|-------------|:---:|:---:|:------:|:--------:|:---:|
| `->`演算子 | O | O | O | X | O |
| `JSON_EXTRACT*` | O | O | O | X | O |
| `JSON_TYPEOF` | O | O | O | X | O |
| `JSON_IS_VALID` | O | O | O | O | O |
| `JSON_SET` | O | O | O | X | O |
| `JSON_SET_JSON` | O | O | O | X | O |
| `JSON_REMOVE` | O | O | O | X | O |

## 使用上の注意

- JSONパス文字列は単一引用符（`'$.key'`）で囲みます。
- 数値の比較には`JSON_EXTRACT_INTEGER`、`JSON_EXTRACT_DOUBLE`などの型別の関数を使用します。
- LOOKUPテーブルではJSONパス専用インデックスをサポートしないため、頻繁に検索する値は別の列に分離します。
