---
type: docs
title: '11.5.2 ResultSet、Statement、LOB'
weight: 20
toc: true
aliases:
  - /dbms/reference/sdk-api/jdbc/resultset-lob/
---

Machbase JDBCのResultSetは前方のみの読み取り専用カーソルです。
Connection、Statement、ResultSetはtry-with-resourcesで閉じます。

```java
statement.getResultSetType();        // ResultSet.TYPE_FORWARD_ONLY
statement.getResultSetConcurrency(); // ResultSet.CONCUR_READ_ONLY
```

スクロール可能または更新可能なResultSetはサポートしません。`next()`の前、最終行の後、close後の
getter呼び出しや、範囲外の列インデックスは`SQLException`になります。

## 型指定の検索

`getObject(index, Class<T>)`と`getObject(label, Class<T>)`をサポートします。

```java
import java.math.BigDecimal;
import java.sql.Timestamp;

try (ResultSet result = statement.executeQuery(
         "SELECT id, value, created_at FROM sensor_tx")) {
    while (result.next()) {
        Integer id = result.getObject("ID", Integer.class);
        BigDecimal value =
            result.getObject("VALUE", BigDecimal.class);
        Timestamp createdAt =
            result.getObject("CREATED_AT", Timestamp.class);
    }
}
```

| Javaの型 | 一般的なMachbaseの型 |
|-----------|-------------------------|
| `String` | CHAR、VARCHAR、TEXT、IPV4、IPV6、JSON |
| `Short`, `Integer`, `Long` | 整数型 |
| `Float`, `Double` | 実数型 |
| `BigDecimal` | DECIMAL、NUMERIC |
| `Boolean` | BOOLEAN |
| `Timestamp`, `Date`, `Time` | DATETIME |
| `byte[]` | BINARY |
| `Blob`, `Clob` | BLOB、CLOB |

SQL NULLはオブジェクトgetterでJavaの`null`を返します。プリミティブgetterは0または`false`を返すため、
直後の`wasNull()`でSQL NULLかを確認します。非サポートの変換や対象クラスのnull指定は
`SQLException`になります。

Machbase SQLでは空文字列リテラル`''`はSQLの`NULL`です。そのため、該当結果列の
`ResultSetMetaData.isNullable()`は`columnNullable`、`getObject()`は`null`を返します。
`''''`は単一引用符1文字であり、NULLではない文字列です。

符号なし型のデフォルトのオブジェクトマッピングは次のとおりです。

| Machbaseの型 | `getObject()`の戻り値の型 |
|---------------|-------------------------|
| `USHORT` | `Integer` |
| `UINTEGER` | `Long` |
| `ULONG` | `BigInteger` |

`SHORT`は`Integer`、32ビットの`FLOAT`は`Float`オブジェクトとして返します。
BOOLEAN文字列は`true`と`false`のみ許可します。

## 文字・バイナリストリーム

`setAsciiStream()`、`setBinaryStream()`、`setCharacterStream()`は、長さを`int`、`long`で
指定するオーバーロードと、長さを指定しないオーバーロードを提供します。`setNCharacterStream()`と
`setNString()`は専用のNCHAR保存型ではなく、VARCHAR経路の別名です。

ResultSetでは次のgetterをインデックスまたは列名で使用できます。

- `getAsciiStream()`、`getBinaryStream()`
- `getCharacterStream()`、`getNCharacterStream()`
- `getNString()`

長さ指定の入力が宣言した長さより短い場合、長さが負の場合、`Integer.MAX_VALUE`を超える場合は
`SQLException`になります。現在のストリームはクライアントメモリに全体を実体化するため、
一定のメモリだけで処理する大容量ストリーミングには使用しません。

## BLOBとCLOB

LOGテーブルのBLOB/CLOB列は標準の`Blob`と`Clob`オブジェクトで検索・バインドできます。

```java
import java.io.ByteArrayInputStream;
import java.io.StringReader;
import java.sql.Blob;
import java.sql.Clob;

try (PreparedStatement insert = connection.prepareStatement(
         "INSERT INTO event_log (payload, message) VALUES (?, ?)")) {
    insert.setBlob(1, new ByteArrayInputStream(payload));
    insert.setClob(2, new StringReader(message));
    insert.executeUpdate();
}

try (ResultSet result = statement.executeQuery(
         "SELECT payload, message FROM event_log")) {
    while (result.next()) {
        Blob payloadObject = result.getBlob("PAYLOAD");
        Clob messageObject = result.getClob("MESSAGE");

        byte[] payloadBytes = payloadObject.getBytes(
            1, (int) payloadObject.length());
        String messageText = messageObject.getSubString(
            1, (int) messageObject.length());

        payloadObject.free();
        messageObject.free();
    }
}
```

`Connection.createBlob()`と`createClob()`で変更可能なオブジェクトを作成し、`setBytes()`、
`setString()`、`setBinaryStream()`、`setCharacterStream()`、`truncate()`を使用できます。
使用後は`free()`を呼び出します。

LOBの位置はJDBC標準に従い1から始まります。部分ストリームの要求範囲全体が実際の値の範囲内に
ある必要があり、末尾を超える場合は短く切り詰めて返さず、SQLState `22003`になります。
負の長さやJava配列で表現できない長さは`HY090`です。`free()`後のオブジェクト再使用は
`SQLException`になります。

LOBは値全体をクライアントメモリに実体化します。数百MiB以上の値を一定のメモリで処理する
ストリーミングLOB実装ではありません。

## ResultSetメタデータ

`ResultSetMetaData.isNullable()`でSELECT結果列のNULL許容性を確認します。

```java
ResultSetMetaData metadata = result.getMetaData();
int nullable = metadata.isNullable(columnIndex);
```

`columnNullableUnknown`はNOT NULLを意味しません。テーブル列の制約は
`DatabaseMetaData.getColumns()`、PRIMARY KEYは`DatabaseMetaData.getPrimaryKeys()`で別途確認します。

## 行数とフェッチ設定

JDBC 4.2のlarge update APIは更新件数を`long`で返します。

```java
long count = statement.executeLargeUpdate(
    "DELETE FROM sensor_tx WHERE id < 100");
long[] counts = statement.executeLargeBatch();
```

`setLargeMaxRows()`と`getLargeMaxRows()`も使用できます。`setMaxRows()`または
`setLargeMaxRows()`はResultSetで取得する最大行数を制限しますが、Statementの`fetchSize`値は
変更しません。

## Statementのライフサイクル

- `closeOnCompletion()`を設定すると、最後のResultSetが閉じる際にStatementも閉じます。
- 1つのStatementの前のResultSetは、再実行前に閉じます。
- コミットはResultSetを閉じますが、StatementとPreparedStatementは再利用できます。
- 1つのResultSetの`next()`とgetterを複数スレッドで同時に呼び出しません。

## キャンセルとクエリタイムアウト

`Statement.cancel()`は現在実行中の文を別セッションからキャンセルします。実行中の文がなければ
何もせず、PreparedStatementのバインドとメタデータは維持されます。

`setQueryTimeout(seconds)`が期限切れになると、`SQLTimeoutException`とSQLState `HYT00`が
発生します。同じStatementは例外処理後に次のクエリで再利用できます。
前の実行のタイムアウト処理が、次の実行をキャンセルすることはありません。

独立したクエリを並列実行するには、同じConnectionを複数ワーカーで共有せず、接続プールから
ワーカーごとに論理Connectionを借り出します。実行中のフェッチを終了する場合は、別スレッドから
`close()`、`cancel()`、`Connection.abort()`を呼び出せます。
