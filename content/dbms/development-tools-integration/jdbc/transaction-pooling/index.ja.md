---
type: docs
title: '11.5.3 トランザクションと接続プール'
weight: 30
toc: true
aliases:
  - /dbms/reference/sdk-api/jdbc/transaction-pooling/
---

Machbase JDBCはStandard EditionのTRANSACTIONテーブルで標準JDBCのローカルトランザクションを
サポートします。Cluster EditionにはTRANSACTIONテーブルがないため、このページのトランザクション
機能は適用しません。

## TRANSACTIONテーブルの作成

```sql
CREATE TRANSACTION TABLE sensor_tx
(
    id         INTEGER PRIMARY KEY,
    parent_id  INTEGER,
    name       VARCHAR(64),
    value      DECIMAL(20, 4),
    created_at DATETIME,
    payload    BINARY
);
```

## コミットとロールバック

`setAutoCommit(false)`、`commit()`、`rollback()`を使用します。
アプリケーションからSQLの`BEGIN`を直接送る必要はありません。

```java
import java.sql.PreparedStatement;
import java.sql.SQLException;

connection.setAutoCommit(false);

try (PreparedStatement statement = connection.prepareStatement(
         "INSERT INTO sensor_tx (id, value) VALUES (?, ?)")) {
    statement.setInt(1, 1);
    statement.setBigDecimal(2, new BigDecimal("10.5000"));
    statement.executeUpdate();
    connection.commit();
} catch (SQLException exception) {
    try {
        connection.rollback();
    } catch (SQLException rollbackException) {
        exception.addSuppressed(rollbackException);
    }
    throw exception;
}
```

`setAutoCommit(false)`は直ちに`BEGIN`を送りません。手動モードで最初のStatementを実行する際に
トランザクションを開始します。コミットまたはロールバック後もauto-commitは`false`のままで、
次のStatementが新しいトランザクションを開始します。

- `setAutoCommit(true)`へ切り替える際、有効なトランザクションがあれば先にコミットします。
- auto-commitが`true`のときに`commit()`または`rollback()`を呼ぶと、SQLState `25000`になります。
- Connectionを閉じる際、未完了のトランザクションはロールバックされます。
- コミットとロールバックは開いたResultSetを閉じますが、Statementは再利用できます。

## 分離レベルとカーソル

サポートする分離レベルは`Connection.TRANSACTION_SERIALIZABLE`です。他の分離レベルを要求すると
`SQLFeatureNotSupportedException`になります。

サポートするカーソル保持設定は`ResultSet.CLOSE_CURSORS_AT_COMMIT`です。
コミット前に必要なResultSetを読み取るか、コミット後にクエリを再実行します。

## テーブルタイプ別の動作

| 操作 | 手動トランザクションでの動作 |
|------|--------------------------|
| TRANSACTIONテーブルのDML/SELECT | トランザクションに参加します。 |
| LOG/TAGテーブルのSELECT | 実行できます。 |
| TRANSACTION変更前の最初のLOG DML | 互換経路でauto-commitとして再実行される場合があります。 |
| 独立したTAG DML | トランザクションに参加し、ロールバックできます。 |
| TRANSACTION変更後のLOG/TAG DMLまたはDDL | エラーになります。 |

互換経路でauto-commit再実行されたLOG DMLは、後続のロールバック対象ではありません。
ロールバックが必要なデータにはTRANSACTIONテーブルを使用します。複数のTRANSACTIONテーブルの
通常のコミットとロールバックはサポートしますが、バックエンドのコミット中に障害が起きた場合の
全体の原子性は保証しません。重要なアトミック操作は1つのTRANSACTIONテーブルの範囲で設計します。

## DataSource

`MachDataSource`は、アプリケーションサーバーやフレームワークに接続プロパティを注入する際に使用します。

```java
import com.machbase.jdbc.MachDataSource;
import java.sql.Connection;

MachDataSource dataSource = new MachDataSource();
dataSource.setUrl("jdbc:machbase://127.0.0.1:5656/machbasedb");
dataSource.setUser("SYS");
dataSource.setPassword(System.getenv("MACHBASE_PASSWORD"));
dataSource.setLoginTimeout(10);

try (Connection connection = dataSource.getConnection()) {
    // SQLを実行します。
}
```

DataSourceはURL、ユーザー、password、ログインタイムアウト、ログwriter、JDBCの`Wrapper`仕様を
サポートします。

## ConnectionPoolDataSource

`MachConnectionPoolDataSource`は物理接続を直接公開せず、論理Connectionを返します。

```java
import com.machbase.jdbc.MachConnectionPoolDataSource;
import java.sql.Connection;
import javax.sql.PooledConnection;

MachConnectionPoolDataSource source =
    new MachConnectionPoolDataSource();
source.setUrl("jdbc:machbase://127.0.0.1:5656/machbasedb");
source.setUser("SYS");
source.setPassword(System.getenv("MACHBASE_PASSWORD"));

PooledConnection pooled = source.getPooledConnection();
try {
    try (Connection logical = pooled.getConnection()) {
        // 論理接続を使用します。
    }
} finally {
    pooled.close();
}
```

1つのPooledConnectionでは論理ハンドルを1つだけ有効にします。論理Connectionを閉じると、
次の状態を初期化してから`connectionClosed`イベントが1回発生します。

- 未完了トランザクションのロールバック
- auto-commitの復元
- URLで決まる初期カタログの復元
- ネットワークタイムアウトの復元

クローズを開始した論理ハンドルの呼び出しが終わる前に、次の貸し出しは行いません。
閉じたConnection、Statement、DatabaseMetaDataは次に接続を借りたリクエストで再利用できず、
SQLState `08003`になります。Statement poolingはサポートしません。

SQLStateクラス`08`の致命的な接続エラーでは物理接続を破棄し、`connectionErrorOccurred`を発生させます。
重複キーなどクラス`23`のエラーは接続破損ではないため、接続エラーイベントを発生させません。

## HikariCP

```java
import com.zaxxer.hikari.HikariConfig;
import com.zaxxer.hikari.HikariDataSource;

HikariConfig config = new HikariConfig();
config.setJdbcUrl("jdbc:machbase://127.0.0.1:5656/machbasedb");
config.setUsername("SYS");
config.setPassword(System.getenv("MACHBASE_PASSWORD"));
config.setMaximumPoolSize(10);
config.setMinimumIdle(2);
config.setConnectionTimeout(30_000);
config.setIdleTimeout(600_000);
config.setMaxLifetime(1_800_000);
config.addDataSourceProperty("TIMEZONE", "+0900");

try (HikariDataSource dataSource = new HikariDataSource(config);
     Connection connection = dataSource.getConnection()) {
    // SQLを実行します。
}
```

論理Connectionはtry-with-resourcesで速やかに返却し、返却済みのハンドルを保持しません。

## ネットワークタイムアウト

`setNetworkTimeout(executor, milliseconds)`はソケット読み取りタイムアウトをミリ秒単位で設定し、
`0`は無制限です。負の値、null executor、またはタスクを拒否するexecutorは`SQLException`になります。

実際にネットワークタイムアウトが発生するとSQLStateクラス`08`の例外が発生し、物理接続は無効になります。
その接続で作成したStatementとResultSetは再利用せず、新しい接続を借り出します。
有効なトランザクションのI/O失敗は自動再実行しません。
