---
type: docs
title: '数値ARRAY'
weight: 30
toc: true
---

Machbase DBMS 8.7.0は、同じ数値型の値を決まった個数保存する固定長1次元の`ARRAY`型をサポートします。
センサーの座標や軸別の測定値など、1行に複数の数値をまとめて保存し、要素ごとに参照する場合に使用します。

一部の位置だけを取り込む方法と選択列Append APIは、
[Sparse ARRAYと選択列Append API](../../../../development-tools-integration/data-input-load-export/array-append/)を参照してください。

## 対応する型と宣言範囲

列の宣言では、数値の要素型の後に`[cardinality]`を付けます。cardinalityは配列の要素数で、各行の
非NULL要素数ではなく、列に宣言した固定長を表します。配列全体が存在しない状態（whole NULL）と、
配列内の特定の値だけが存在しない状態（element NULL）は区別します。

| 要素型 | DDL例 | 説明 |
|---|---|---|
| `INT16` | `INT16[4]` | 16ビット符号付き整数 |
| `UINT16` | `UINT16[4]` | 16ビット符号なし整数 |
| `INT32` | `INT32[4]` | 32ビット符号付き整数 |
| `UINT32` | `UINT32[4]` | 32ビット符号なし整数 |
| `INT64` | `INT64[4]` | 64ビット符号付き整数 |
| `UINT64` | `UINT64[4]` | 64ビット符号なし整数 |
| `FLOAT` | `FLOAT[4]` | 単精度浮動小数点 |
| `DOUBLE` | `DOUBLE[4]` | 倍精度浮動小数点 |
| `DECIMAL(p,s)` | `DECIMAL(12,4)[4]` | 固定小数点数 |

- cardinalityの範囲は`1..1024`です。
- `DECIMAL`のprecisionの範囲は`1..65`です。
- `DECIMAL`のscaleの範囲は`0..30`で、precisionを超えることはできません。

次の別名は、対応する正規の要素型として扱います。

| 別名 | 正規の型 |
|---|---|
| `SHORT` | `INT16` |
| `USHORT` | `UINT16` |
| `INT`, `INTEGER` | `INT32` |
| `UINTEGER` | `UINT32` |
| `LONG` | `INT64` |
| `ULONG` | `UINT64` |
| `NUMERIC`, `DEC`, `FIXED`, `NUMBER` | `DECIMAL` |

## テーブルの作成と列の追加

次の例は、4つのチャネル値、3つの累積値、2つの固定小数点値を保存します。

```sql
CREATE LOG TABLE SENSOR_ARRAY
(
    ID       INTEGER,
    CHANNELS DOUBLE[4],
    COUNTERS UINT64[3],
    AMOUNTS  DECIMAL(12,4)[2]
);
```

`ADD COLUMN`に対応する既存テーブルには、同じARRAY宣言を使用して列を追加できます。
削除には既存の`DROP COLUMN`構文を使用します。

```sql
ALTER TABLE SENSOR_ARRAY
    ADD COLUMN (STATUS_VALUES INT32[3]);

ALTER TABLE SENSOR_ARRAY
    ADD COLUMN (LIMITS DECIMAL(12,4)[2] DEFAULT [0.0000, NULL]);

ALTER TABLE SENSOR_ARRAY
    DROP COLUMN (STATUS_VALUES);

ALTER TABLE SENSOR_ARRAY
    DROP COLUMN (LIMITS);
```

`DECIMAL(12)[2]`のようにscaleを省略すると、`DECIMAL(12,0)[2]`として扱います。

TAG METADATA ARRAYには`METADATA ADD COLUMN`と`METADATA DROP COLUMN`を使用します。

```sql
ALTER TABLE SENSOR_TAG METADATA
    ADD COLUMN (LIMITS DECIMAL(12,4)[2] DEFAULT [0.0000, NULL]);

ALTER TABLE SENSOR_TAG METADATA
    DROP COLUMN (LIMITS);
```

`ARRAY`は次の場所の通常のデータ列に使用できます。

- LOGテーブル
- TAG DATAの通常のDATA列
- TAG METADATAの通常のメタデータ列
- VOLATILEテーブル
- LOOKUPテーブル
- Standard EditionのTRANSACTIONテーブル

`ARRAY`の追加によって各テーブルの既存のDML範囲が広がることはありません。例えばLOGテーブルの
`UPDATE`は引き続き非対応であり、TAGテーブルの`UPDATE`も既存の許容されたDATAまたはMETADATA経路のみ使用できます。

### ADD COLUMNのサポート範囲

| Edition | テーブルまたは列の領域 | ARRAY ADD/DROP |
|---|---|:---:|
| Standard | LOG | O |
| Standard | VOLATILE | O |
| Standard | LOOKUP | O |
| Standard | TRANSACTION | O |
| Standard | TAG METADATA | O |
| Standard | TAG DATAの通常列 | X |
| Cluster | LOG | O |
| Cluster | その他のテーブルまたはTAG METADATA | X |

TAG DATAの通常のARRAY列は`CREATE TABLE`で宣言できますが、ALTERでは追加できません。

<a id="default와-기존-row"></a>

### DEFAULTと既存行

- DEFAULTがなければ、ALTER前から存在する行の新しいARRAY列は全体がNULLになります。
- LOG、LOOKUP、TRANSACTION、TAG METADATAは、明示したARRAY DEFAULTを既存行に適用します。
- VOLATILEはスカラー列の`ADD COLUMN`と同様、既存行をDEFAULTで書き直さないため、新しいARRAY列は全体がNULLになります。
- Cluster LOGは、明示したARRAY DEFAULTを既存行に適用します。
- DEFAULTの配列コンストラクターの要素数は、宣言したcardinalityと完全に一致する必要があります。

ALTER後にTAG DATAのINSERTまたはAppendで新しいタグが自動登録される場合、新しいメタデータ行には
ADD COLUMNのDEFAULTを適用しません。追加したARRAYメタデータ列は全体がNULLとして作成されます。
このDEFAULTは、ALTER前から存在するメタデータ行にのみ適用します。

次の用途には`ARRAY`を使用できません。

- PRIMARY KEY、UNIQUE、通常のインデックスキー
- `AUTO_INCREMENT`、`SEQUENCE`
- TAGテーブルのNAME、BASETIME、BASE DISTANCE、SUMMARIZED列

TAG METADATA ARRAY列には自動インデックスを作成しません。明示的なインデックスも非対応です。

次の宣言はサポートしません。

```sql
INT32[]
INT32[0]
INT32[1025]
VARCHAR[4]
INT32[2][3]
DECIMAL[4](12,4)
```

## ARRAY値の取り込み

`ARRAY[...]`と省略形`[...]`の両方を使用できます。

```sql
INSERT INTO SENSOR_ARRAY VALUES
    (1,
     ARRAY[1.5, NULL, 3.5, 4.5],
     [1, NULL, 3],
     [12.3400, NULL]);

INSERT INTO SENSOR_ARRAY VALUES
    (2,
     [10.0, 20.0, 30.0, 40.0],
     [4, 5, 6],
     [1.2500, 2.5000]);

INSERT INTO SENSOR_ARRAY VALUES (3, NULL, NULL, NULL);
```

コンストラクターの要素数は対象列のcardinalityと完全に一致する必要があります。長さが異なる場合は、
埋め合わせや切り詰めを行わず文を失敗させます。空の`[]`や`ARRAY[]`も、cardinalityが0の保存値としては使用できません。

各要素に、対象数値型の変換、符号、範囲、`DECIMAL`のprecisionとscaleの規則を適用します。
1つでも変換できない要素があれば文全体が失敗し、`ARRAY`の一部だけを保存することはありません。

### 数値の範囲

整数型は内部のNULL番兵値を実際の値として保存できません。

| 型 | 保存可能な範囲 |
|---|---|
| `INT16` | `-32767..32767` |
| `UINT16` | `0..65534` |
| `INT32` | `-2147483647..2147483647` |
| `UINT32` | `0..4294967294` |
| `INT64` | `-9223372036854775807..9223372036854775807` |
| `UINT64` | `0..18446744073709551614` |

`FLOAT`と`DOUBLE`でも、NULL番兵値として予約された最大有限値は実際の要素として保存できません。
それを超える入力のInfinity処理は、対応するスカラー型と同じです。

### 対象列がない場合のARRAY型推論

`SELECT [1,2,3]`など対象列のない文脈では、全要素から共通の型を推論します。

- すべての非NULL要素が同じ型なら、その型を維持します。
- 符号付き整数と符号なし整数は、すべての値を格納できる最小の整数型へ昇格します。
- 符号付き整数と`UINT64`が混在する場合は`DECIMAL(20,0)`を使用します。
- `DECIMAL`同士では、必要な整数桁数とscaleを組み合わせます。
- `FLOAT`のみなら`FLOAT`を維持し、他の数値型と混在する場合は`DOUBLE`へ昇格します。
- 空の配列、全要素がNULLの配列、非数値要素、入れ子の配列は推論エラーです。

INSERT、UPDATE、プリペアドパラメーターなど対象列がある場合は、対象列の要素型、cardinality、
`DECIMAL`メタデータで各要素を検証します。

### 配列全体のNULLと要素のNULL

`ARRAY`自体のNULLと、NULL要素を持つ`ARRAY`は異なる値です。

```sql
-- ARRAY自体がNULLです。
INSERT INTO SENSOR_ARRAY (ID, CHANNELS) VALUES (10, NULL);

-- ARRAYは存在し、4つの要素がすべてNULLです。
INSERT INTO SENSOR_ARRAY (ID, CHANNELS)
VALUES (11, [NULL, NULL, NULL, NULL]);
```

`NOT NULL`は`ARRAY`全体のNULLのみを制限します。このため、全要素がNULLの`ARRAY`は
`NOT NULL`列にも取り込めます。

## 要素の参照

要素の位置は0始まりです。cardinalityが4の場合、有効な位置は`0..3`です。

```sql
SELECT CHANNELS,
       CHANNELS[0] AS FIRST_CHANNEL,
       CHANNELS[3] AS LAST_CHANNEL,
       CHANNELS[4] AS OUT_OF_RANGE
  FROM SENSOR_ARRAY;
```

次の場合は、エラーではなくSQL `NULL`を返します。

- 添字が負数、またはcardinality以上の場合
- 添字の式がSQL NULLの場合
- `ARRAY`全体がNULLの場合
- 該当要素がNULLの場合

{{< callout type="warning" >}}
要素の位置を表す`[位置]`は、引用符で囲んでいない単純な列名の後にのみ付けられます。
`A[0]`は使用できますが、`T.A[0]`と`"A"[0]`は使用できません。
{{< /callout >}}

## ARRAY_LENGTH

`ARRAY_LENGTH()`は、配列全体がNULLでなければ、宣言された要素数（cardinality）を返します。

```sql
SELECT ID, ARRAY_LENGTH(CHANNELS)
  FROM SENSOR_ARRAY;
```

すべての要素がNULLでもcardinalityを返します。配列全体がNULLならNULLを返します。
型情報のない`ARRAY_LENGTH(NULL)`は引数の型を決定できないため、エラーになります。

## ARRAY全体のCAST

同じcardinalityの数値`ARRAY`は、`CAST(array_expression AS TYPE[N])`で全要素の型を変換できます。

```sql
SELECT CAST(CHANNELS AS INT32[4])
  FROM SENSOR_ARRAY;

SELECT CAST(AMOUNTS AS DECIMAL(10,2)[2])
  FROM SENSOR_ARRAY;
```

- 入力は数値`ARRAY`またはSQL `NULL`である必要があります。
- 変換先には、このドキュメントの数値要素型と別名を使用できます。
- 入力と変換先のcardinalityは完全に一致する必要があります。
- 配列全体のNULLと各要素のNULLは変換後も保持します。
- 各非NULL要素には、対応するスカラーCASTの数値変換規則を適用します。
- `DECIMAL[N]`は`DECIMAL(10,0)[N]`、`DECIMAL(p)[N]`は`DECIMAL(p,0)[N]`として扱います。
- 1つでも範囲や変換規則に違反する要素があれば、CASTとそれを含む文全体が失敗します。

プリペアドステートメントでは、CASTの変換先がパラメーターと結果の要素型、cardinality、
DECIMALの精度と小数桁数を決定します。同じ文にARRAY値、配列全体のNULL、一部の位置のみを指定する
疎なARRAYを再バインドできます。

```sql
SELECT CAST(? AS INT32[3]);
SELECT CAST(? AS DECIMAL(12,4)[3]);
```

`CASE`や`UNION ALL`でARRAY結果を組み合わせるには、要素型、cardinality、DECIMALのprecision/scaleが
すべて一致する必要があります。異なる場合は、明示的に同じARRAY型へCASTしてから組み合わせます。

次の変換はサポートしません。

- スカラー値をARRAYへ展開
- ARRAYをスカラーへ縮小
- 異なるcardinality間の埋め合わせや切り詰め
- 文字列、日付、IP、BINARY、JSONのARRAYを変換先に指定

構文、数値変換、エラー規則の詳細は[CAST関数](../../functions/functions-full/#cast)を参照してください。

## 比較と式

`ARRAY`全体に`=`、`<>`、`IS NULL`、`IS NOT NULL`を使用できます。同じ位置のNULL要素同士は、
`ARRAY`全体の等値比較では一致します。配列全体のNULLの比較は通常のSQL NULL規則に従います。

```sql
SELECT ID
  FROM SENSOR_ARRAY
 WHERE CHANNELS = [1.5, NULL, 3.5, 4.5]
    OR CHANNELS[1] IS NULL;
```

要素の式は、対応する数値型の通常の式や述語で使用できます。ただし、`ARRAY`全体を次の場所で
使用することはできません。

- `DISTINCT`
- `GROUP BY`
- `ORDER BY`
- 集約関数のDISTINCT引数

## VIEW、INSERT SELECT、CASE、upsert

VIEWと`INSERT ... SELECT`は、要素型、cardinality、`DECIMAL`のprecisionとscaleを保持します。
異なる数値`ARRAY`型へ取り込む場合は各要素を対象型へ変換し、1つでも変換できなければ文全体が失敗します。

INSERTとUPDATEの`CASE`結果にも、対象`ARRAY`の規則を適用します。

```sql
UPDATE SENSOR_LOOKUP
   SET AMOUNTS = CASE WHEN ID = 1
                     THEN [12345678.1234, NULL]
                     ELSE AMOUNTS
                 END
 WHERE ID = 1;
```

LOOKUPやVOLATILEテーブルの重複キーupsertでも、直接の`ARRAY`、定数`CASE`、プリペアドステートメントの
配列全体のバインドに同じ変換規則を適用します。upsertの右辺の式で既存行の列を参照できるかどうかは、
各テーブルの既存のポリシーに従います。

## メタデータと表示形式

`DESC`とSQLエクスポートには正規の宣言形式を表示します。

```sql
DESC SENSOR_ARRAY;
```

システムカタログは`ARRAY`型コード、cardinality、precision、scaleを個別のフィールドに保持します。
SQLCLIまたはODBCの`SQLColumns()`は次の情報を返します。

- `DATA_TYPE`: `SQL_MACHBASE_ARRAY`
- `TYPE_NAME`: `INT32[3]`、`DECIMAL(12,4)[2]`などの正規の宣言形式
- `COLUMN_SIZE`: cardinality
- `DECIMAL_DIGITS`: `DECIMAL`要素のscale

`machsql`、汎用ODBCのテキスト参照、Goの`database/sql`など文字列結果が必要な経路では、
`[value,null,value]`形式を使用します。小文字の`null`は要素のNULLで、列結果のSQL `NULL`は配列全体のNULLです。

## SDKでのARRAYの読み書き

次の例では、共通のテーブルとデータを使用します。

```sql
CREATE LOG TABLE SDK_ARRAY_SAMPLE
(
    ID INTEGER,
    A_I32 INT32[3],
    A_U64 UINT64[3],
    A_DEC DECIMAL(12,4)[3]
);

INSERT INTO SDK_ARRAY_SAMPLE VALUES
    (1,
     [1,NULL,-3],
     [1,NULL,18446744073709551614],
     [1.2500,NULL,-3.7500]);
INSERT INTO SDK_ARRAY_SAMPLE (ID) VALUES (2);
```

配列全体のNULLは各SDKのNULL値、要素のNULLはコレクション内部のNULL値で表します。
`UINT64`と`DECIMAL`には、SDKが提供する精度を保持できる型を使用してください。

### C SQLCLI

型付きフェッチには`SQL_C_MACHBASE_ARRAY`と`SQL_MACHBASE_ARRAY_DESC`を使用します。

```c
SQLINTEGER values[3] = {0};
SQLLEN elements[3] = {0};
SQLLEN outer = 0;
SQL_MACHBASE_ARRAY_DESC array = {0};

array.struct_size = sizeof(array);
array.element_c_type = SQL_C_SLONG;
array.capacity = 3;
array.values = values;
array.element_indicators = elements;

SQLExecDirect(stmt,
    (SQLCHAR*)"SELECT A_I32 FROM SDK_ARRAY_SAMPLE WHERE ID=1", SQL_NTS);
SQLBindCol(stmt, 1, SQL_C_MACHBASE_ARRAY, &array, sizeof(array), &outer);
SQLFetch(stmt);
/* outer != SQL_NULL_DATA, array.count == 3,
 * values[0] == 1, elements[1] == SQL_NULL_DATA, values[2] == -3 */
```

配列全体がNULLの場合は`outer == SQL_NULL_DATA`で、`array.count == 0`です。NULL要素を区別するには
`element_indicators`を指定します。`DECIMAL`を文字列で取得する場合は`element_c_type = SQL_C_CHAR`と
要素バッファー間の`value_stride`を設定します。

プリペアドINSERTでは`capacity`、`count`、`ColumnSize`に対象のcardinalityを設定します。

```c
array.count = 3;
SQLPrepare(stmt,
    (SQLCHAR*)"INSERT INTO SDK_ARRAY_SAMPLE(ID,A_I32) VALUES(3,?)", SQL_NTS);
SQLBindParameter(stmt, 1, SQL_PARAM_INPUT,
    SQL_C_MACHBASE_ARRAY, SQL_MACHBASE_ARRAY, 3, 0,
    &array, sizeof(array), &outer);
SQLExecute(stmt);
```

配列全体のNULLの取り込みは`outer = SQL_NULL_DATA`で指定します。ARRAYのパラメーターセット実行は
現在サポートせず、`HYC00`を返します。従来の`SQLAppendBatch`もARRAY型コードがないためARRAYは非対応ですが、
同じSQLSTATEが返される保証はありません。

### C++

C++ではSQLCLIの記述子ABIをそのまま使用します。バインドからフェッチ完了まで`vector`のアドレスが
変わらないようにサイズを固定してください。

```cpp
std::vector<SQLINTEGER> values(3);
std::vector<SQLLEN> indicators(3);
SQLLEN outer = 0;
SQL_MACHBASE_ARRAY_DESC array{};
array.struct_size = sizeof(array);
array.element_c_type = SQL_C_SLONG;
array.capacity = values.size();
array.values = values.data();
array.element_indicators = indicators.data();

SQLBindCol(stmt, 1, SQL_C_MACHBASE_ARRAY,
           &array, sizeof(array), &outer);
```

アプリケーションモデルでは、`std::optional<std::vector<std::optional<T>>>`の外側の`optional`で
配列全体のNULLを、内側の`optional`で要素のNULLを表せます。

### Machbase ODBCと汎用ODBC

Machbase専用ヘッダーを使用するODBC Cプログラムは、C SQLCLIと同じARRAY記述子を使用します。
専用型を解釈しない汎用ツールでは、正規のテキスト形式で参照するか、各要素を個別に射影します。

```sql
SELECT ID, A_I32, A_I32[1], A_I32[2], A_I32[3]
  FROM SDK_ARRAY_SAMPLE
 ORDER BY ID;
```

### JDBC

JDBCは`java.sql.Array`を返します。`UINT64`は`BigInteger`、`DECIMAL`は`BigDecimal`で保持します。

```java
try (Connection con = DriverManager.getConnection(
         "jdbc:machbase://127.0.0.1:5656/machbasedb", "SYS", "MANAGER");
     Statement st = con.createStatement();
     ResultSet rs = st.executeQuery(
         "SELECT A_I32 FROM SDK_ARRAY_SAMPLE ORDER BY ID")) {
    rs.next();
    java.sql.Array sqlArray = rs.getArray(1);
    Object[] values = (Object[])sqlArray.getArray();
    // [Integer(1), null, Integer(-3)]
    rs.next();
    assert rs.getArray(1) == null && rs.wasNull();
}
```

メタデータのJDBC型は`Types.ARRAY`、precisionはcardinality、`DECIMAL`のscaleは要素のscaleです。
`Connection.createArrayOf()`で作成した値を`PreparedStatement.setArray()`に渡せます。

### Python

PythonはARRAYを`list`、要素のNULLをリスト内の`None`、配列全体のNULLを列自体の`None`として返します。
`UINT64`は任意精度の`int`、`DECIMAL`は`Decimal`です。

```python
from decimal import Decimal
from machbaseAPI import connect

conn = connect(host="127.0.0.1", port=5656,
               user="SYS", password="MANAGER")
try:
    rows = conn.cursor(dictionary=True).execute(
        "SELECT A_I32,A_U64,A_DEC FROM SDK_ARRAY_SAMPLE ORDER BY ID"
    ).fetchall()
    assert rows[0]["A_I32"] == [1, None, -3]
    assert rows[0]["A_U64"][2] == 18446744073709551614
    assert rows[0]["A_DEC"][0] == Decimal("1.2500")
    assert rows[1]["A_I32"] is None
finally:
    conn.close()
```

プリペアド`execute()`と`executemany()`は`list`や`tuple`をARRAYとしてエンコードします。
`cursor.column_metadata`でARRAY型コード、cardinality、`DECIMAL`要素のメタデータを確認できます。

### Node.js

Node.jsはARRAYをJavaScriptの`Array`で返します。`INT64`と`UINT64`は`bigint`、
`DECIMAL`は精度保持のため文字列で返します。

```javascript
const { createConnection } = require('@machbase/ts-client');
const conn = createConnection({
  host: '127.0.0.1', port: 5656, user: 'SYS', password: 'MANAGER',
});
await conn.connect();
try {
  const [rows] = await conn.query(
    'SELECT A_I32,A_U64,A_DEC FROM SDK_ARRAY_SAMPLE ORDER BY ID',
  );
  console.log(rows[0].A_I32); // [1, null, -3]
  console.log(rows[0].A_U64); // [1n, null, 18446744073709551614n]
  console.log(rows[1].A_I32); // null: whole NULL
} finally {
  await conn.end();
}
```

`JSON.stringify()`の前に`bigint`を文字列へ変換してください。`DECIMAL`文字列を`Number`へ強制変換しないでください。
プリペアドステートメントの`getColumns()`で、ARRAYのcardinalityと要素のprecision/scaleメタデータを確認できます。

### .NET full/legacy provider

MachConnector40 full/legacyプロバイダーはARRAYを`object[]`で返します。要素のNULLは配列内の`null`、
配列全体のNULLは`IsDBNull()`で区別します。

```csharp
using Mach.Data.MachClient;
using var conn = new MachConnection(
    "SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD=MANAGER");
conn.Open();
using var cmd = new MachCommand(
    "SELECT A_I32 FROM SDK_ARRAY_SAMPLE ORDER BY ID", conn);
using var reader = cmd.ExecuteReader();
reader.Read();
var values = (object[])reader.GetValue(0);
Console.WriteLine((int)values[0]);
Console.WriteLine(values[1] is null);
reader.Read();
Console.WriteLine(reader.IsDBNull(0));
```

各要素は`short`、`ushort`、`int`、`uint`、`long`、`ulong`、`float`、`double`、`decimal`です。
CLRの`decimal`の範囲外の値は、カルチャに依存しない文字列で返します。`GetSchemaTable()`は
プロバイダー型、cardinality、要素のscale、`object[]`フィールド型を提供します。

### Go neo-client

この項目は、`neo-client`がMachbase DBMSへ直接接続するSDK経路を扱い、Machbase Neoサーバーは対象外です。
0始まりのARRAY APIは、[`neo-client` PR #17](https://github.com/machbase/neo-client/pull/17)以降の
v2モジュールソースにあります。公開v2リリースが指定されるまでは、該当ソースのチェックアウトと
`go.work`や`replace`などによる明示的なローカルモジュール接続が必要です。公開v1リリースに
機能が含まれていると仮定しないでください。

```go
import (
    "context"
    "database/sql"
    "fmt"

    client "github.com/machbase/neo-client/v2"
    "github.com/machbase/neo-client/v2/api"
)

db, err := sql.Open(client.DefaultDriverName, dsn)
if err != nil { return err }
defer db.Close()

dense, err := api.NewArray(api.SqlTypeInt32,
    int32(10), nil, int32(30))
if err != nil { return err }
if _, err = db.ExecContext(context.Background(),
    "INSERT INTO SDK_ARRAY_SAMPLE(ID,A_I32) VALUES(3,?)", dense); err != nil {
    return err
}

rows, err := db.QueryContext(context.Background(),
    "SELECT A_I32 FROM SDK_ARRAY_SAMPLE WHERE ID=3")
if err != nil { return err }
defer rows.Close()
for rows.Next() {
    var raw sql.NullString
    if err := rows.Scan(&raw); err != nil { return err }
    fmt.Println(raw.String) // [10,null,30]
}
return rows.Err()
```

`database/sql`の結果は正規の文字列形式です。`sql.NullString`で配列全体のNULLを確認し、有効な値は
`array.Scan(raw.String)`、配列全体のNULLは`array.Scan(nil)`で解析します。元の幅の狭い整数型と
`FLOAT`型も保持するには、要素のメタデータから受け取り先を事前に作成します。
`DECIMAL`のprecision/scaleは`NewSparseArrayWithMeta()`で指定します。

`ColumnTypes()`の`DatabaseTypeName()`はARRAY型名を、`DecimalSize()`は`DECIMAL`要素のprecision/scaleを
提供します。現在の`Length()`はエンコードされたペイロードのバイト長であり、cardinalityとして使用しないでください。
標準の`database/sql`メタデータだけではcardinalityを直接取得できません。

## コマンドラインツールとデータ移動

### machsql

`machsql`は正規の`ARRAY`文字列を出力します。

```sql
SELECT ID, CHANNELS, ARRAY_LENGTH(CHANNELS), CHANNELS[1]
  FROM SENSOR_ARRAY
 ORDER BY ID;
```

SQLファイルに保存し、次のように実行できます。

```bash
machsql -s 127.0.0.1 -P 5656 -u SYS -p MANAGER -f array_query.sql
```

### machloader

machloaderのテキスト入出力は正規の`[value,null,value]`形式を使用します。ARRAY内部に区切り文字や
引用符が含まれるため、CSVではARRAYフィールドを囲み文字で囲みます。

```csv
1,"[1.5,null,3.5,4.5]"
```

配列全体のNULLと、全要素がNULLの`ARRAY`が相互に変わらないことを、エクスポートと再インポートで確認します。
CSVのテーブル自動作成では`ARRAY`を推論しないため、事前にテーブルを明示的に作成してください。

### バックアップ、復元、マウント

バックアップと復元は、要素型、cardinality、`DECIMAL`のprecision/scale、NULL情報を保持します。
マウント後のクエリも同じ結果とメタデータを提供します。ARRAYを含むデータのバックアップ、復元、マウントは
Machbase DBMS 8.7.0環境で実行してください。

## バージョンとエラー処理

- `ARRAY`型はMachbase DBMS 8.7.0でサポートします。
- ARRAYのSQL要素位置とMachbase専用SDKのpositionは0始まりです。従来の1始まりのSQLやSDK呼び出しでは、各位置を1減らしてください。
- Machbase DBMS 8.7.0サーバーとARRAY機能を含むSDKビルドを併用します。
- 非対応のサーバーやSDKは、ARRAYを他の型へ自動変換せずエラーを返します。
- cardinality、position、要素変換のエラーは文全体を失敗させ、ARRAYの一部だけを保存することはありません。
- アプリケーションでは配列全体のNULLと全要素がNULLの`ARRAY`を別の値として扱ってください。
- このドキュメントはMachbase DBMSのSQLとSDK機能を扱い、Machbase Neo、HTTP、TQL、ILPは対象外です。
