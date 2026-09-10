---
type: docs
title: '11.5.5 Append API'
weight: 50
toc: true
aliases:
  - /dbms/reference/sdk-api/jdbc/append-api/
---

Machbase Append APIは複数行を連続して入力する大量入力APIです。JDBCでは`MachStatement`の
拡張メソッドを使用します。このページはLOG入力の例を中心に説明します。他のテーブルタイプの
サポート範囲は[SDKサポート表](../../sdk-support-scope/#append-table-type-matrix)も確認してください。

## API

| メソッド | 説明 |
|--------|------|
| `executeAppendOpen(tableName, errorCheckCount)` | Appendセッションを開始し、列メタデータを返します。 |
| `executeAppendOpen(tableName, inputColumns, errorCheckCount)` | Machbase DBMS 8.7.0で選択列またはARRAY要素を対象にAppendセッションを開始します。 |
| `executeAppendData(metadata, data)` | 1行を送信します。 |
| `executeAppendDataByTime(metadata, time, data)` | ナノ秒の時刻を指定して1行を送信します。 |
| `executeAppendFlush()` | 保留中の応答を同期します。 |
| `executeAppendClose()` | Appendセッションを終了します。 |
| `executeSetAppendErrorCallback(callback)` | 行エラーのコールバックを登録します。 |
| `getAppendSuccessCount()` | 成功した行数を返します。 |
| `getAppendFailureCount()` | 失敗した行数を返します。 |

公開メソッド`executeAppendData()`は成功すると`1`を返し、無効な内部結果には`SQLException`を
スローします。最終的な成功・失敗件数とコールバックも確認します。

## 入力例

```sql
CREATE LOG TABLE sensor_data (
    time DATETIME,
    name VARCHAR(40),
    value DOUBLE
);
```

```java
import com.machbase.jdbc.MachStatement;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.util.ArrayList;

try (MachStatement statement =
         (MachStatement) connection.createStatement()) {
    ResultSet appendResult =
        statement.executeAppendOpen("sensor_data", 100);
    ResultSetMetaData metadata = appendResult.getMetaData();

    statement.executeSetAppendErrorCallback(
        (errorNumber, errorMessage, rowMessage) ->
            System.err.printf(
                "Append error [%05d]: %s%n%s%n",
                errorNumber, errorMessage, rowMessage));

    long baseTime = System.currentTimeMillis() * 1_000_000L;

    for (int index = 0; index < 10_000; index++) {
        ArrayList<Object> row = new ArrayList<>();
        row.add(baseTime + index);
        row.add("sensor-" + (index % 10));
        row.add(20.0 + index * 0.001);

        int result = statement.executeAppendData(metadata, row);
        if (result != 1 && result != 2) {
            throw new SQLException(
                "Append failed at row " + index);
        }
    }

    statement.executeAppendFlush();
    statement.executeAppendClose();
    appendResult.close();

    System.out.printf("success=%d failure=%d%n",
        statement.getAppendSuccessCount(),
        statement.getAppendFailureCount());
}
```

## ARRAYと選択列

スパースARRAY入力に列選択は必須ではありません。通常の
`executeAppendOpen(tableName, errorCheckCount)`で開き、返されたメタデータに合わせて
`MachSparseArray`を行のARRAY値として渡します。

```java
ResultSet opened = statement.executeAppendOpen("ARRAY_APPEND_FULL_EXAMPLE", 0);
```

接続・入力・Close・検索を含む[通常Openの例](../../data-input-load-export/array-append/#jdbc-full-open)を
先に確認してください。`ID`とARRAY列を宣言順で渡し、自動の`_arrival_time`は行に追加しません。

Machbase DBMS 8.7.0では、`executeAppendOpen()`のオーバーロードに列名や
`ARRAY_COLUMN[position]`を渡せます。

```java
ResultSet appendResult = statement.executeAppendOpen(
    "sensor_array",
    new String[] {"ID", "CHANNELS[0]", "CHANNELS[3]"},
    0);
```

行ごとに異なるARRAY位置を入力する場合は、`MachConnection.createSparseArrayOf()`で
`MachSparseArray`を作成します。mapキーは0から始まり、空のmapは全要素がNULLのARRAYです。
Javaの`null`は配列全体のNULLです。

```java
Map<Integer, Object> entries = new HashMap<Integer, Object>();
entries.put(Integer.valueOf(1), Integer.valueOf(200));
entries.put(Integer.valueOf(3), Integer.valueOf(400));

MachSparseArray sparse = connection.createSparseArrayOf(
    "INT32", 4, entries);
```

密なARRAYの検索とprepared入力には、`java.sql.Array`、`Connection.createArrayOf()`、
`PreparedStatement.setArray()`を使用します。全体例と対象の衝突規則は
[Sparse ARRAYと選択列Append API](../../data-input-load-export/array-append/)を参照してください。

SQLのARRAY要素対象と`MachSparseArray`の位置は0始まりです。JDBC標準のパラメーター番号と
`java.sql.Array.getArray(index, count)`のスライスインデックスは従来どおり1始まりのため、
混同しないでください。

## DATETIME

AppendのDATETIME値はエポックナノ秒単位の`long`で渡します。

```java
long epochNanoseconds =
    System.currentTimeMillis() * 1_000_000L;
```

`executeAppendDataByTime()`は別の時刻値を受け取るテーブル入力経路で使用します。
入力列の順序とJavaの型は、`executeAppendOpen()`が返したResultSetMetaDataに合わせます。

## フラッシュとクローズ

1. `executeAppendOpen()`でセッションを開始します。
2. `executeAppendData()`を繰り返し呼び出します。
3. 途中の確認が必要な場合は`executeAppendFlush()`を呼び出します。
4. 全入力を送った後、`executeAppendClose()`を呼び出します。
5. 成功・失敗件数とコールバックの結果を確認します。

例外時にもAppendセッションとStatementが閉じるよう、try-with-resourcesと`finally`を使用します。
コールバックでは失敗行を別途保存またはログ記録し、無条件の再試行で重複入力を作らないよう業務キーを
使用します。

## サイズと使用範囲

ordered appendはプロトコルのパケット上限を共有するため、1行全体のエンコード後サイズを64KiB未満に
保ちます。BLOB/CLOBなど大きな値を入力する場合は、行サイズとクライアントのメモリ使用量を合わせて
確認します。

TRANSACTIONテーブルのAppendバッチはSQLトランザクションに含まれず、独立して反映されます。
ロールバックが必要な複数のDMLには[JDBCトランザクション](../transaction-pooling/)を使用します。
