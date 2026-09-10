---
type: docs
title: 'Named Bind Parameter'
weight: 30
toc: true
---

Named Bind Parameterは、SQLの値の位置に`:name`形式の名前を指定し、実行時に値をバインドする機能です。
繰り返すパラメーターの意味を名前で表せるため、SQLとアプリケーションコードの対応関係を明確に保てます。

```sql
SELECT ID, NAME
FROM SENSOR_DATA
WHERE ID = :id;
```

## 名前の構文

名前付きマーカーは次の形式を使用します。

```text
:[A-Za-z_$][A-Za-z0-9_$]*
```

| 区分 | 例 |
|---|---|
| 有効な名前 | `:id`, `:sensor_id`, `:value2`, `:_from_time`, `:select` |
| 無効な名前 | `:1id`, `:`, `::id` |

複数のSDKで同じSQLを共有する場合は、`[A-Za-z][A-Za-z0-9_]*`形式の名前を推奨します。

パラメーター名は大文字と小文字を区別します。`:VALUE`、`:value`、`:VaLuE`は異なる名前です。
.NETの`MachParameterCollection`は、既存プロバイダーとの互換性のため、大文字と小文字を区別せず名前を検索します。

## 使用できる位置

名前付きマーカーは、値や式を指定する位置で使用します。

```sql
SELECT ID, NAME, VALUE
FROM SENSOR_DATA
WHERE CREATED_AT >= :from_time
  AND CREATED_AT < :to_time
  AND VALUE >= :minimum_value
ORDER BY CREATED_AT
LIMIT :row_count OFFSET :start_row;
```

次のような識別子やSQL構造は、パラメーターに置き換えられません。

```sql
SELECT * FROM :table_name;               -- 使用不可
SELECT :column_name FROM SENSOR_DATA;     -- 列識別子の置き換えではない
SELECT * FROM SENSOR_DATA ORDER BY ID :direction; -- 使用不可
```

動的な識別子が必要なら、アプリケーションで許可リストを検査してからSQLを構成します。

文字列とSQLコメント内のコロンは、パラメーターとして認識されません。

```sql
SELECT ':not_a_parameter'
FROM SENSOR_DATA
WHERE ID = :id /* :ignored */;
```

## パラメーターの出現順序

パラメーター数は一意な名前の数ではなく、SQL内の出現回数で数えます。
次のSQLには`target`が2回現れるため、パラメーターは2つです。

```sql
SELECT ID, NAME
FROM SENSOR_DATA
WHERE ID = :target
   OR PARENT_ID = :target;
```

- `SQLNumParams()`は`2`を返します。
- 位置指定APIは、1番目と2番目の位置を個別にバインドします。
- 名前指定APIは、1つの`target`値を同名の両方の位置に適用します。
- パラメーターメタデータには、各位置が別の項目として現れます。

1つのSQL文で使用できるパラメーターの出現回数は、最大256です。

## 位置指定マーカーとの関係

低レベルの位置指定APIは、`?`と`:name`をSQLの出現順にバインドできます。
名前・オブジェクト・マッピングによるAPIは、匿名マーカー`?`と名前付きマーカーを併用するとエラーを返します。
1つのSQL文では1種類のマーカーを使用してください。

| 方式 | SQLマーカー | バインド |
|---|---|---|
| 位置指定 | `?` | SQL出現順の1始まりの位置番号 |
| 名前付きSQLと位置指定API | `:name` | SQL出現順の1始まりの位置番号 |
| 名前指定API | `:name` | パラメーター名 |

## DMLでの使用例

Named Bind Parameterは、既存のプリペアドステートメントと同じ型規則を使用します。

```sql
INSERT INTO SENSOR_DATA
    (ID, PARENT_ID, NAME, VALUE, CREATED_AT)
VALUES
    (:id, :parent_id, :name, :value, :created_at);
```

Named Bind Parameterは、テーブルごとのDMLポリシーやEdition制約を変更しません。
サポートされるDMLと条件は、[DML構文](../dml-syntax/)および
[サポート範囲と制約](../../../support-scope-constraints/)を参照してください。

Standard EditionとCluster Editionは、同じ`:name`構文と位置番号規則を使用します。
実行可能なSQLとテーブルタイプは、各Editionの既存のサポート範囲に従います。

<a id="named-bind-tag-data-update"></a>

### TAGデータUPDATEでの使用

Machbase 8.7.0から、Standard EditionのTAGデータUPDATEでは、`WHERE`句のNAMEとBASETIME条件値に名前付きマーカーを使用できます。

```sql
UPDATE sensor_tag
   SET value = :value,
       status = :status,
       note = :note
 WHERE name = :name
   AND time = :time;
```

同じプリペアドステートメントの再実行時に、SET、NAME、TIMEの値を新しくバインドできます。
一致する行がなければ、影響行数`0`で成功します。
バインドの使用にかかわらずタグ選択条件とBASETIME条件は両方必要で、SET対象列の制約も変わりません。

サポートされる条件形式とパラメーターメタデータは、
[TAGデータUPDATE](../dml-syntax/tag-data-update-syntax/#tag-data-update-predicate-bind)を参照してください。

## CTEでの使用

Standard Editionでは、CTE本文とメインの`SELECT`でNamed Bind Parameterを使用できます。

```sql
WITH FILTERED AS (
    SELECT ID, NAME, VALUE
    FROM SENSOR_DATA
    WHERE ID > :minimum_id
      AND NAME = :label
)
SELECT ID, NAME, VALUE
FROM FILTERED
WHERE ID = :target_id
ORDER BY ID;
```

上のSQLのパラメーターの位置番号は、`minimum_id`、`label`、`target_id`の順です。
CTEのサポート範囲とStandard Edition制約は、[WITH / CTE構文](../cte-syntax/)を参照してください。

## NULLとデータ型

NULLは、各SDKの標準のNULL値またはインジケーターで渡します。

| SDK | NULL値 |
|---|---|
| Machbase SQLCLI | インジケーターの`SQL_NULL_DATA` |
| ODBC | インジケーターの`SQL_NULL_DATA` |
| JDBC | `null` |
| Node.js/TypeScript | `null` |
| Python | `None` |
| .NET | `DBNull.Value` |

`column = :value`にNULLをバインドしても、`column IS NULL`と同じ条件にはなりません。
NULLを検索するには、SQLのNULL比較規則に従って`IS NULL`を使用します。

`INTEGER`、`VARCHAR`、`DOUBLE`、`DECIMAL`、`NUMERIC`、`DATETIME`など、既存のプリペアドステートメントのデータ型を使用できます。
`DECIMAL`や`NUMERIC`の精度を保持するには、SDKのdecimal型または文字列表現を使用してください。

## SDK別のバインド方法

| SDKまたはツール | 名前による使用方法 |
|---|---|
| Machbase SQLCLI | `SQLBindParameterByName()`, `SQLBindParameterByNameW()` |
| ODBC | `:name`のSQLを`SQLBindParameter()`の位置番号でバインド |
| JDBC | `MachPreparedStatement.setObject(String name, Object value)` |
| Node.js/TypeScript | 配列は位置指定、オブジェクトは名前指定入力 |
| Python DB-API | mappingを渡す。2.4のprepared cursorは、呼び出し間で`:name`と`%(name)s`を再使用 |
| .NET | `MachCommand.Parameters.AddWithValue(":name", value)` |
| Go native | `api.Named("name", value)` |
| Go `database/sql` | `sql.Named("name", value)` |
| machsql | SQLは`:name`、値は`$1`、`$2`の順で指定 |

詳細なAPIとエラー処理は、[開発ツール連携](../../../../development-tools-integration/)と
[machsqlコマンド・オプションリファレンス](../../../command-line-tools/machsql/)を参照してください。

## 互換性とエラー

Machbase 8.7.0の名前指定SDK APIには、この機能に対応するクライアントとサーバーの両方が必要です。
旧バージョンと併用する必要がある場合は、`?`と位置指定APIを使用してください。

| 状況 | 代表的なエラー |
|---|---|
| 必要な名前がない | missing parameter |
| SQLにない名前を渡す | unknownまたはextra parameter |
| 名前指定と位置指定を混在 | sequenceまたはmixed error |
| 値の型がSQL型と合わない | typeまたはconversion error |
| 名前指定APIを旧サーバーに使用 | unsupported |

本番コードでは、エラー文字列よりSQLSTATE、エラーコード、例外型を優先して確認してください。
バージョンの組み合わせごとの動作とSDK別のエラーコードは、
[クライアント・サーバープロトコル互換性](../../../support-scope-constraints/compatibility-xma-protocol/)を参照してください。
