---
type: docs
title: '11.5.4 DatabaseMetaData'
weight: 40
toc: true
aliases:
  - /dbms/reference/sdk-api/jdbc/database-metadata/
---

`Connection.getMetaData()`はドライバー、サーバー、スキーマオブジェクト、JDBC機能の情報を返します。
結果列はJDBC標準の名前と順序を使用するため、数値の位置より列名で読み取ることを推奨します。

```java
import java.sql.DatabaseMetaData;

DatabaseMetaData metadata = connection.getMetaData();

System.out.println(metadata.getDriverName());
System.out.println(metadata.getDriverVersion());
System.out.println(metadata.getDatabaseProductName());
System.out.println(metadata.getDatabaseProductVersion());
```

## テーブルとVIEW

```java
try (ResultSet tables = metadata.getTables(
         null, null, "%", new String[] {"TABLE", "VIEW"})) {
    while (tables.next()) {
        System.out.printf("%s %s%n",
            tables.getString("TABLE_NAME"),
            tables.getString("TABLE_TYPE"));
    }
}
```

`getTables()`はTABLEとVIEWを区別します。Machbaseの詳細なテーブルタイプは`REMARKS`で確認します。
アプリケーションは特定の位置番号に依存せず、標準列名を使用します。

## 列

```java
try (ResultSet columns = metadata.getColumns(
         null, null, "SENSOR_TX", "%")) {
    while (columns.next()) {
        System.out.printf(
            "%s %s size=%d nullable=%s%n",
            columns.getString("COLUMN_NAME"),
            columns.getString("TYPE_NAME"),
            columns.getInt("COLUMN_SIZE"),
            columns.getString("IS_NULLABLE"));
    }
}
```

`NULLABLE`は数値定数、`IS_NULLABLE`は`YES`、`NO`、または空文字列で返ります。
LOOKUPとVOLATILEテーブルのPRIMARY KEYは、明示的なNOT NULL句がなくても`columnNoNulls`と
`NO`で返ります。

VARCHAR、DATETIME、BINARY、BLOB、CLOBなど数値属性が適用されない列の`DECIMAL_DIGITS`と
`NUM_PREC_RADIX`はSQL NULLです。`getInt()`の0だけを見ず、`getObject()`または`wasNull()`で
NULLかどうかを確認します。

## PRIMARY KEYとインデックス

```java
try (ResultSet keys = metadata.getPrimaryKeys(
         null, null, "SENSOR_TX")) {
    while (keys.next()) {
        System.out.printf("%s position=%d%n",
            keys.getString("COLUMN_NAME"),
            keys.getShort("KEY_SEQ"));
    }
}

try (ResultSet indexes = metadata.getIndexInfo(
         null, null, "SENSOR_TX", false, false)) {
    while (indexes.next()) {
        System.out.printf("%s %s%n",
            indexes.getString("INDEX_NAME"),
            indexes.getString("COLUMN_NAME"));
    }
}
```

PRIMARY KEYかどうかを`ResultSetMetaData.isNullable()`の値から推測しません。
`getPrimaryKeys()`と`getIndexInfo()`を使用します。

SELECT結果の直接の列がPKかどうかは、Machbase JDBC拡張の
`MachResultSetMetaData.isPrimaryKey(column)`で確認できます。

```java
import com.machbase.jdbc.MachResultSetMetaData;

try (ResultSet result = statement.executeQuery(
         "SELECT ID, ID + 1 AS ID_EXPR FROM SENSOR_TX")) {
    MachResultSetMetaData resultMetadata =
        (MachResultSetMetaData) result.getMetaData();
    System.out.println(resultMetadata.isPrimaryKey(1)); // trueまたはfalse
    System.out.println(resultMetadata.isPrimaryKey(2)); // 式: false
}
```

`getPrimaryKeys()`はテーブルカタログのPKを検索し、`isPrimaryKey()`は現在のSELECT結果の
列メタデータを取得します。旧バージョンのサーバーまたはSDKに接続した場合、結果列のPKフラグが
`false`として返る場合があります。

## スキーマと型情報

次のメソッドはJDBC標準形式のResultSetを返します。

- `getSchemas()`、`getCatalogs()`、`getTableTypes()`
- `getTypeInfo()`
- `getTables()`、`getColumns()`
- `getPrimaryKeys()`、`getIndexInfo()`

非サポートの任意メタデータ検索は、nullや非標準のResultSetではなく、標準列を持つ空のResultSetを
返す場合があります。機能を使用する前に機能メソッドを確認します。

```java
if (metadata.supportsSavepoints()) {
    // 対応環境でのみセーブポイントを使用します。
}
```

## カタログ

`Connection.getCatalog()`と`setCatalog()`は、ドライバーが公開する現在のカタログ値を管理します。
メタデータメソッドのカタログ引数は、この値と一致する要求をフィルターするために使用します。

```java
String initialCatalog = connection.getCatalog();
connection.setCatalog(initialCatalog);
```

接続プールに論理Connectionを返却すると、カタログはURLで決まる初期値に復元されます。
前の接続貸し出し期間で取得したDatabaseMetaDataオブジェクトは、次の貸し出し期間で再利用しません。

## サポート範囲の確認

Machbase JDBCは実際のサポート範囲を機能情報に反映します。たとえばトランザクションの分離レベル、
ResultSetの種類、セーブポイント、生成キー、複数結果の同時オープンのサポートを次のように確認します。

```java
System.out.println(metadata.supportsTransactions());
System.out.println(metadata.supportsTransactionIsolationLevel(
    Connection.TRANSACTION_SERIALIZABLE));
System.out.println(metadata.supportsResultSetType(
    ResultSet.TYPE_FORWARD_ONLY));
System.out.println(metadata.supportsSavepoints());
System.out.println(metadata.supportsGetGeneratedKeys());
System.out.println(metadata.supportsMultipleOpenResults());
```

`Driver.jdbcCompliant()`が`false`であることと、個々のJDBC APIのサポート状況は別です。
アプリケーションは必要な機能を直接確認します。

Standard EditionでROWID対応サーバーに接続すると、`supportsGetGeneratedKeys()`は`true`、
`getRowIdLifetime()`は`ROWID_VALID_OTHER`を返します。非対応サーバーまたはCluster Editionでは、
それぞれ`false`と`ROWID_UNSUPPORTED`を返します。使用例は
[ROWIDとINSERT結果ID](/dbms/reference/sql/rowid/)を参照してください。
