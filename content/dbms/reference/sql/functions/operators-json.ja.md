---
type: docs
title: 'JSON関数とJSONドット表記'
weight: 40
toc: true
---

Machbaseは、`JSON`型の列に保存されたデータを操作・参照する関数とJSONドット表記を提供します。

## クイックリファレンス

| 関数/表記 | 構文 | 説明 |
|-------------|------|------|
| JSONドット表記 | `col.key` | JSONオブジェクトからキーの値を抽出 |
| `JSON_EXTRACT` | `JSON_EXTRACT(doc, path)` | JSONパスの値をJSON文字列として抽出 |
| `JSON_EXTRACT_STRING` | `JSON_EXTRACT_STRING(doc, path)` | JSONパスの値を文字列として抽出 |
| `JSON_EXTRACT_INTEGER` | `JSON_EXTRACT_INTEGER(doc, path)` | JSONパスの値を整数として抽出 |
| `JSON_EXTRACT_DOUBLE` | `JSON_EXTRACT_DOUBLE(doc, path)` | JSONパスの値を実数として抽出 |
| `JSON_TYPEOF` | `JSON_TYPEOF(doc, path)` | 指定したJSONパスの値の型を確認 |
| `JSON_IS_VALID` | `JSON_IS_VALID(json_text)` | JSON文字列の妥当性を確認 |
| `JSON_SET` | `JSON_SET(doc, path, scalar)` | JSONパスにスカラー値を設定 |
| `JSON_SET_JSON` | `JSON_SET_JSON(doc, path, json_text)` | JSONパスにJSONサブツリーを設定 |
| `JSON_REMOVE` | `JSON_REMOVE(doc, path)` | JSONパスのメンバーを削除 |

`JSON_TYPEOF`の`path`は必須引数です。JSONドキュメント全体の型は`JSON_TYPEOF(doc, '$')`で確認します。

---

## JSONドット表記

JSON列の後にドット（`.`）とキー名を付けて、そのキーの値を参照します。
JSONPath文字列を書かずにJSON列のメンバーへアクセスする場合に使用します。

```sql
json_column.key
```

```sql
-- JSON列から特定キーの値を抽出
SELECT data.temperature AS temp FROM sensor_log;

-- WHERE句で使用
SELECT * FROM sensor_log
 WHERE data.status = 'active';
```

JSONPath文字列を直接指定する場合は、`data -> '$.temperature'`のように`->`演算子を使用します。
上記のJSONドット表記とは区別して記述してください。

---

## JSON_SET

JSONドキュメントの指定パスにSQLスカラー値をJSONスカラーとして保存します。

```sql
JSON_SET(json_doc, path, scalar)
```

- `path`には完全なJSONPath（`$.key.subkey`形式）を使用してください。
- `JSON_SET(..., path, NULL)`はJSONの`null`を保存します。
- JSONドキュメント引数がSQL `NULL`なら、結果はSQL `NULL`です。
- 配列要素の更新（`$.items[0]`）はサポートしません。

```sql
Mach> SELECT JSON_SET('{"ship":{"status":"READY"}}', '$.ship.status', 'DONE') FROM dual;
{"ship":{"status":"DONE"}}

Mach> SELECT JSON_SET('{"count":0}', '$.count', 42) FROM dual;
{"count":42}
```

---

## JSON_SET_JSON

第3引数をJSON文字列として解析し、オブジェクトまたは配列のサブツリーを保存します。

```sql
JSON_SET_JSON(json_doc, path, json_text)
```

- 第3引数がSQL `NULL`なら、結果はSQL `NULL`です。
- 無効なJSON文字列はエラーになります。
- 配列要素の更新はサポートしません。

```sql
Mach> SELECT JSON_SET_JSON('{"ship":{}}', '$.ship.owner', '{"name":"machbase"}') FROM dual;
{"ship":{"owner":{"name":"machbase"}}}

Mach> SELECT JSON_SET_JSON('{"tags":{}}', '$.tags.sensors', '[1,2,3]') FROM dual;
{"tags":{"sensors":[1,2,3]}}
```

---

## JSON_REMOVE

JSONドキュメントから特定のメンバーまたは下位パスを削除します。

```sql
JSON_REMOVE(json_doc, path)
```

- `path`には完全なJSONPathを使用してください。
- 存在しないパスは何も変更しません。
- `JSON_REMOVE(..., '$')`は許可しません。
- JSONドキュメント引数がSQL `NULL`なら、結果はSQL `NULL`です。

```sql
Mach> SELECT JSON_REMOVE('{"owner":{"name":"machbase","team":"db"}}', '$.owner.team') FROM dual;
{"owner":{"name":"machbase"}}

Mach> SELECT JSON_REMOVE('{"a":1,"b":2}', '$.a') FROM dual;
{"b":2}
```

---

## JSONデータの挿入例

```sql
-- JSON型の列を含むLOGテーブル
CREATE LOG TABLE device_log (
    ts    DATETIME,
    data  JSON
);

-- JSONデータの挿入
INSERT INTO device_log VALUES (NOW, '{"temperature":23.5,"humidity":60,"status":"active"}');

-- JSONドット表記で値を抽出
SELECT ts, data.temperature AS temp
  FROM device_log
 WHERE data.status = 'active';
```

---

## テーブルタイプ別のJSONサポート状況

| テーブルタイプ | JSON列 | JSON path query | 備考 |
|------------|:---------:|:---------------:|------|
| TAG | O | O | JSON列とJSON関数をサポート。JSON PKは非対応 |
| LOG | O | O | 完全にサポート |
| LOOKUP | O | O | 通常の列としてサポート。JSONパスインデックスは非対応 |
| VOLATILE | X | X | JSON列の作成不可 |
| TRANSACTION | O | O | 完全にサポート |

詳細は[JSON型のテーブルタイプ別サポート範囲](/dbms/lookup-table-usage/json-column-query/)を参照してください。
