---
type: docs
title: '16.6.5 LOOKUP SQL/JSONサポート表'
weight: 50
toc: true
---

このページでは、LOOKUPテーブルのSQL機能とJSON関連の制約をまとめます。

## サポート状況

| 機能 | サポート | 備考 |
|------|:---:|------|
| **基本CRUD** | | |
| INSERT | O | 通常のINSERTを使用 |
| SELECT | O | 主キー（PK）条件と一般の検索条件の両方を使用可能 |
| UPDATE（PK条件） | O | 主キーの高速アクセスパスを使用 |
| DELETE（PK条件） | O | 主キーの高速アクセスパスを使用 |
| UPDATE（一般の検索条件） | O | 条件に一致する主キー集合を収集してから更新 |
| DELETE（一般の検索条件） | O | 条件に一致する主キー集合を収集してから削除 |
| **JSON機能** | | |
| JSON型列 | O | 通常の列として作成、保存、参照、更新が可能 |
| JSON path query (`$.key`) | O | `->`、`JSON_EXTRACT_*`、`JSON_TYPEOF`、`JSON_IS_VALID`を使用可能 |
| JSON PK | X | JSON列は主キーとして宣言不可 |
| JSON path index | X | 個別のJSONパスインデックスは非対応 |
| **その他** | | |
| 明示的トランザクション（`BEGIN`/`COMMIT`/`ROLLBACK`） | X | DMLは文単位で反映され、複数の文をまとめてロールバックすることは不可 |
| Prepared Statement | O | 主キー条件と一般の検索条件でパラメーターバインドをサポート |
| Append API | △ | 通常のSQL INSERTが基本。AppendはLOOKUP固有のAppendポリシーに従う |

## 正式な参照先

LOOKUPのJSONスキーマと実行例は[JSON列とクエリ](../../../lookup-table-usage/json-column-query/)を、
UPDATE・DELETE構文は[DML構文](../../sql/syntax/dml-syntax/)を参照してください。
