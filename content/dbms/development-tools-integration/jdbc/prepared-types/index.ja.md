---
type: docs
title: '11.5.1 PreparedStatementと型'
weight: 10
toc: true
aliases:
  - /dbms/reference/sdk-api/jdbc/prepared-types/
---

PreparedStatementはSQLをサーバーでprepareし、パラメーターだけを変えて繰り返し実行します。
Machbase JDBCは標準の位置指定パラメーターと名前付き拡張パラメーターを提供します。

## ParameterMetaData

`PreparedStatement.getParameterMetaData()`で実行前にパラメーターの数と型を確認できます。
INSERT、UPDATE、SELECTで同じように使用します。

```java
import java.sql.ParameterMetaData;
import java.sql.PreparedStatement;

try (PreparedStatement statement = connection.prepareStatement(
         "INSERT INTO sensor_tx " +
         "(id, value, created_at) VALUES (?, ?, ?)")) {
    ParameterMetaData metadata = statement.getParameterMetaData();

    for (int index = 1; index <= metadata.getParameterCount(); index++) {
        System.out.printf(
            "%d: type=%s precision=%d scale=%d nullable=%d%n",
            index,
            metadata.getParameterTypeName(index),
            metadata.getPrecision(index),
            metadata.getScale(index),
            metadata.isNullable(index));
    }
}
```

パラメーターのインデックスは1から始まります。0またはパラメーター数を超えるインデックスは
`SQLException`になります。precisionは型に応じて解釈します。数値型では保存バイト数ではなく、
JDBCの10進桁数を表します。DATETIMEは`java.sql.Types.TIMESTAMP`にマッピングされますが、
データベースの型名は`DATETIME`です。

## Named Bind Parameter

`:name`プレースホルダーと`MachPreparedStatement.setObject(String, Object)`はMachbase拡張です。
同じ名前が複数回現れると、その名前のすべての位置に値が適用されます。

```java
import com.machbase.jdbc.MachPreparedStatement;

try (MachPreparedStatement statement =
         (MachPreparedStatement) connection.prepareStatement(
             "SELECT id FROM sensor_tx " +
             "WHERE id = :id OR parent_id = :id")) {
    statement.setObject("id", Integer.valueOf(10));

    try (ResultSet result = statement.executeQuery()) {
        while (result.next()) {
            System.out.println(result.getInt("ID"));
        }
    }
}
```

- 名前の先頭のコロンは指定・省略のどちらも可能です。
- 名前は大文字と小文字を区別します。
- 1つの文で名前付きsetterと数値インデックスsetterを混用しません。
- SQLにない名前、または名前付き・位置指定の混用はSQLState `07009`になります。
- 名前付きbindをサポートしない旧サーバーではSQLState `0A000`になります。

移植性が必要なアプリケーションは、JDBC標準の`?`と数値インデックスsetterを使用します。
共通の名前構文は[Named Bind Parameter](/dbms/reference/sql/syntax/named-bind-parameter-syntax/)を
参照してください。

## Prepared SELECTの再実行

同じPreparedStatementでSELECTを繰り返し実行できます。前のResultSetを閉じて値を再バインドすると、
次の実行で新しいResultSetを返します。

```java
try (PreparedStatement statement = connection.prepareStatement(
         "SELECT id, name FROM sensor_tx WHERE id = ?")) {
    ResultSetMetaData metadata = statement.getMetaData();
    System.out.println(metadata.getColumnCount());

    for (int id = 1; id <= 2; id++) {
        statement.setInt(1, id);
        try (ResultSet result = statement.executeQuery()) {
            while (result.next()) {
                System.out.println(result.getString("NAME"));
            }
        }
    }
}
```

Machbase JDBCは1つのStatementで複数の結果を同時に開く機能をサポートしません。各実行のResultSetを
読み取って閉じてから、次の実行を開始します。prepare段階の`ResultSetMetaData`は、Statementが
開いている間は再取得できます。

## JDBC 4.2 SQLTypeのバインディング

Java 8の`JDBCType`でパラメーターのSQL型を指定できます。

```java
import java.math.BigDecimal;
import java.sql.JDBCType;
import java.sql.Timestamp;

try (PreparedStatement statement = connection.prepareStatement(
         "INSERT INTO sensor_tx " +
         "(id, name, value, created_at, payload) " +
         "VALUES (?, ?, ?, ?, ?)")) {
    statement.setObject(1, Integer.valueOf(1), JDBCType.INTEGER);
    statement.setObject(2, "sensor-1", JDBCType.VARCHAR);
    statement.setObject(
        3, new BigDecimal("12.3400"), JDBCType.DECIMAL, 4);
    statement.setObject(
        4, Timestamp.valueOf("2026-07-26 10:00:00"),
        JDBCType.TIMESTAMP);
    statement.setObject(5, new byte[] {1, 2, 3}, JDBCType.BINARY);
    statement.executeUpdate();
}
```

不明なベンダー`SQLType`は`SQLFeatureNotSupportedException`になります。
DECIMALとNUMERICは`BigDecimal`を使用し、指定スケールに合わせてバインドします。

### SQL NULL

`setNull()`または`setObject(index, null, JDBCType)`を使用すると、対象型に合うSQL NULLが
渡されます。次の型も型付きNULLをサポートします。

- `REAL`、`BIT`、`TINYINT`、`BOOLEAN`
- `VARBINARY`、`LONGVARBINARY`、`BLOB`、`CLOB`
- `LONGVARCHAR`

符号なしパラメーターのNULLは、ParameterMetaDataに基づいてネイティブのNULL値に変換されます。
符号なし型の最大データ値より1大きい通信上のNULLセンチネルは実データとして保存できず、
その値を渡すとSQLState `22003`になります。

| Machbaseの型 | Javaの型 | データ範囲 |
|---------------|-----------|-------------|
| `USHORT` | `Integer` | 0~65534 |
| `UINTEGER` | `Long` | 0~4294967294 |
| `ULONG` | `BigInteger` | 0~18446744073709551614 |

NULLを入力する場合はセンチネル値を直接渡さず、`setNull()`を使用します。

## Boolean

`setBoolean()`と`setObject(index, value, JDBCType.BOOLEAN)`は、`true`を1、`false`を0として
渡します。文字列は大文字・小文字を問わず`true`と`false`のみ許可され、それ以外はSQLState `22018`に
なります。

## IPv4とIPv6

IPアドレス列には`MachPreparedStatement`の拡張setterを使用できます。

```java
MachPreparedStatement statement =
    (MachPreparedStatement) connection.prepareStatement(
        "INSERT INTO net_log(ts, src_ip, dst_ip) VALUES (?, ?, ?)");

statement.setLong(1, System.currentTimeMillis() * 1_000_000L);
statement.setIpv4(2, "192.168.1.100");
statement.setIpv6(3, "::1");
statement.executeUpdate();
```

## NULL許容性のメタデータ

`ParameterMetaData.isNullable()`は`parameterNoNulls`、`parameterNullable`、
`parameterNullableUnknown`のいずれかを返します。`parameterNullableUnknown`をNOT NULLと
解釈しないでください。SQL別の判定規則は
[NULL許容性メタデータのサポート範囲](/dbms/development-tools-integration/sdk-support-scope/#support-scope-sdk-nullable-metadata)を
参照してください。
