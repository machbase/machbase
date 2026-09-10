---
type: docs
title: '11.5 JDBC'
weight: 50
toc: true
aliases:
  - /dbms/reference/sdk-api/jdbc/
---

Machbase JDBCドライバーはJava 8を基準にJDBC 4.2の主要APIを提供します。標準JDBC APIで
サーバーに接続し、PreparedStatement、型指定の検索とバインディング、データベースメタデータ、
ローカルトランザクション、接続プールを使用できます。

| 項目 | 値 |
|------|----|
| Javaバイトコード基準 | Java 8 |
| ドライバーが報告するJDBCバージョン | 4.2 |
| ドライバーバージョン | 3.0.0 |
| JDBC URL | `jdbc:machbase://<host-list>/[database]` |
| `Driver.jdbcCompliant()` | `false` |

`jdbcCompliant()`の`false`はJDBC 4.2 APIのサポート状況ではなく、SQL-92 Entry Level全体への
準拠状況を示します。アプリケーションでは必要な任意機能を`DatabaseMetaData`の機能メソッドで確認します。

## マルチデータベース

URLパスまたは`database`接続プロパティで初期データベースを指定できます。

```java
String url = "jdbc:machbase://127.0.0.1:5656/factory_a";
Connection conn = DriverManager.getConnection(url, "APP_A", password);

System.out.println(conn.getCatalog());
conn.setCatalog("FACTORY_A");
```

`getCatalog()`と`setCatalog()`はサーバーの現在のデータベースと同期します。URLパスと設定プロパティを
両方指定する場合は同じ値にする必要があります。JDBCメタデータではカタログはデータベース、スキーマは
所有者です。プールされた接続の返却時に初期カタログへ復元されるか確認し、プリペアドステートメントと
Appendハンドルは作成時のデータベースに固定される点を考慮します。

## ドライバーのインストール

### JARファイルの使用

Machbaseインストールディレクトリの`machbase.jar`をクラスパスに追加します。

```bash
ls -l "$MACHBASE_HOME/lib/machbase.jar"
javac -classpath ".:$MACHBASE_HOME/lib/machbase.jar" MyApp.java
java -classpath ".:$MACHBASE_HOME/lib/machbase.jar" MyApp
```

JARには`META-INF/services/java.sql.Driver`が含まれています。JDBC 4.0以降の環境では
`Class.forName("com.machbase.jdbc.MachDriver")`を呼び出さなくてもドライバーが自動登録されます。
既存アプリケーションの明示的な呼び出しも引き続き使用できます。

### Maven

```xml
<dependency>
    <groupId>com.machbase</groupId>
    <artifactId>machjdbc</artifactId>
    <version>{{< jdbc_version >}}</version>
</dependency>
```

### Gradle

```groovy
dependencies {
    implementation 'com.machbase:machjdbc:{{< jdbc_version >}}'
}
```

配布成果物のバージョンは[Maven Central](https://mvnrepository.com/artifact/com.machbase/machjdbc)で
確認します。ドライバーが実行時メタデータで返す`3.0.0`と配布成果物のバージョンは、別のバージョン体系です。

## サーバーへの接続

ユーザー名とパスワードはソースコードに記録せず、環境変数やシークレット管理システムで渡します。

```java
import java.sql.Connection;
import java.sql.DriverManager;
import java.util.Properties;

String url = "jdbc:machbase://127.0.0.1:5656/machbasedb";

Properties properties = new Properties();
properties.setProperty("user", "SYS");
properties.setProperty("password", System.getenv("MACHBASE_PASSWORD"));

try (Connection connection =
         DriverManager.getConnection(url, properties)) {
    // SQLを実行します。
}
```

### 接続オプション

接続オプションは`Properties`またはURLクエリ文字列で指定します。`randomHost`は`Properties`で
指定するか、複数ホストURLの`^`区切り文字を使用します。

| オプション | 説明 |
|------|------|
| `user`, `password` | パスワード認証情報 |
| `TIMEZONE` | セッションのタイムゾーン。`+0900`形式を使用します。 |
| `randomHost` | ホスト一覧から最初の接続先をランダムに選択します。 |
| `maxStatements` | プールされた接続の最大キャッシュStatement数 |
| `CONNECTION_TIMEOUT` | ソケット接続のタイムアウト（秒）。`0`は無制限です。 |
| `SOCKET_TIMEOUT` | ソケット読み取りのタイムアウト（秒）。`0`は無制限です。 |
| `characterEncoding` | クライアントの文字エンコーディング |
| `AUTH_MODE` | `PASSWORD`または`CHALLENGE` |
| `AUTH_SIG_SCHEME` | `ECDSA`、`RSA_PKCS1_V15`、`RSA_PSS` |
| `AUTH_KEY_FILE` | PEM秘密鍵ファイルのパス |

```java
String url =
    "jdbc:machbase://127.0.0.1:5656/machbasedb?TIMEZONE=+0900";
```

<a id="jdbc-multi-host"></a>

### 複数ホストへの接続

Machbase 8.7.0 JDBCドライバーは、1つのURLに複数ホストを指定できます。

| 選択方式 | 指定方法 | 動作 |
|-----------|-----------|------|
| 順次選択 | ホストを`,`で区切る | URLの記載順に接続を試みます。 |
| ランダム開始 | ホストを`^`で区切る | ホスト一覧から最初の接続先をランダムに選びます。 |
| ランダム開始 | `Properties`で`randomHost=true`を指定 | `,`で区切った一覧から最初の接続先をランダムに選びます。 |

次のURLは`db1`への接続に失敗すると、`db2`への接続を試みます。

```java
String url =
    "jdbc:machbase://db1.example.com:5656,db2.example.com:5656/" +
    "machbasedb?CONNECTION_TIMEOUT=5";
```

`^`区切り文字を使用すると、最初の接続先をランダムに選択します。

```java
String url =
    "jdbc:machbase://db1.example.com:5656^db2.example.com:5656/" +
    "machbasedb?CONNECTION_TIMEOUT=5";
```

`randomHost`設定プロパティを使用する場合は、`,`でホストを区切ります。

```java
Properties properties = new Properties();
properties.setProperty("randomHost", "true");

String url =
    "jdbc:machbase://db1.example.com:5656,db2.example.com:5656/" +
    "machbasedb?CONNECTION_TIMEOUT=5";
```

- 1つのURLで`,`と`^`の区切り文字は併用できません。
- 接続拒否、接続タイムアウト、ソケットエラーなど接続段階のI/Oエラーが発生すると、次のホストへの
  接続を試みます。すべてのホストが失敗すると`DriverManager.getConnection()`は`SQLException`を返します。
- `CONNECTION_TIMEOUT`はホストごとの接続試行に適用されます。そのため全体の接続待機時間は
  ホスト数と各ホストの応答時間によって長くなる場合があります。
- `SOCKET_TIMEOUT`は接続済みソケットの読み取り待機時間を制限し、ホストの選択順序は変更しません。

複数ホストの切り替えは、新規接続または再接続時のソケット接続に適用されます。切断後に自動再接続が
成功しても、以前のStatement、PreparedStatement、ResultSetは再利用しません。実行中のSQLの成功や
安全な再実行は保証されないため、有効なトランザクションで接続エラーが発生した場合は接続を破棄し、
業務の冪等性ポリシーに従ってトランザクション全体を再実行します。

## AUTH KEY認証

公開鍵によるチャレンジ認証では、パスワードの代わりにローカルの秘密鍵でサーバーチャレンジに署名します。

```java
Properties properties = new Properties();
properties.setProperty("user", "app_user");
properties.setProperty("AUTH_MODE", "CHALLENGE");
properties.setProperty("AUTH_SIG_SCHEME", "ECDSA");
properties.setProperty(
    "AUTH_KEY_FILE", "/opt/machbase/keys/app_user_ecdsa.pem");

Connection connection = DriverManager.getConnection(
    "jdbc:machbase://127.0.0.1:5656/machbasedb", properties);
```

- `AUTH_MODE=CHALLENGE`では認証に`password`を使用しません。
- `AUTH_KEY_FILE`は必須です。
- `AUTH_SIG_SCHEME`を省略すると、鍵の種類に合うデフォルト署名方式を選択します。
- POSIX環境では秘密鍵ファイルの権限を`600`に制限します。

## クイックスタート

次の例はLOGテーブルに値を入力し、再検索します。

```java
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.Statement;
import java.util.Properties;

public class JdbcQuickStart {
    public static void main(String[] args) throws Exception {
        Properties properties = new Properties();
        properties.setProperty("user", "SYS");
        properties.setProperty(
            "password", System.getenv("MACHBASE_PASSWORD"));

        try (Connection connection = DriverManager.getConnection(
                 "jdbc:machbase://127.0.0.1:5656/machbasedb",
                 properties);
             Statement statement = connection.createStatement()) {
            statement.execute(
                "CREATE LOG TABLE jdbc_sensor " +
                "(ts DATETIME, name VARCHAR(40), value DOUBLE)");

            try (PreparedStatement insert = connection.prepareStatement(
                     "INSERT INTO jdbc_sensor VALUES (?, ?, ?)")) {
                insert.setLong(1, System.currentTimeMillis() * 1_000_000L);
                insert.setString(2, "sensor-1");
                insert.setDouble(3, 25.3);
                insert.executeUpdate();
            }

            try (ResultSet result = statement.executeQuery(
                     "SELECT name, value FROM jdbc_sensor")) {
                while (result.next()) {
                    System.out.printf("%s %.1f%n",
                        result.getString("NAME"),
                        result.getDouble("VALUE"));
                }
            }
        }
    }
}
```

DATETIMEにエポックナノ秒値を渡す場合は`long`を使用します。例のテーブルがすでに存在する場合は、
`CREATE LOG TABLE`を省略するか別名を使用します。

## INSERT結果のROWID

Standard Editionで単一の`INSERT ... VALUES`が成功すると、JDBC標準の生成キーAPIで入力行の
ROWIDを確認できます。

```java
String sql = "INSERT INTO jdbc_sensor VALUES (?, ?, ?)";
try (PreparedStatement insert = connection.prepareStatement(
         sql, Statement.RETURN_GENERATED_KEYS)) {
    insert.setLong(1, System.currentTimeMillis() * 1_000_000L);
    insert.setString(2, "sensor-2");
    insert.setDouble(3, 26.1);
    insert.executeUpdate();

    try (ResultSet keys = insert.getGeneratedKeys()) {
        if (keys.next()) {
            java.sql.RowId rowId = keys.getRowId("ROWID");
        }
    }
}
```

結果は1つの`ROWID`列と最大1行で構成されます。返すROWIDがない場合は空の`ResultSet`です。
サポート状況は`DatabaseMetaData.supportsGetGeneratedKeys()`で確認します。
バッチ、Append、`INSERT ... SELECT`、UPSERTの違いは
[ROWIDとINSERT結果ID](/dbms/reference/sql/rowid/)を参照してください。

## バージョンの確認

```java
import java.sql.DatabaseMetaData;

DatabaseMetaData metadata = connection.getMetaData();

System.out.println(metadata.getDriverName());
System.out.println(metadata.getDriverVersion());
System.out.println(metadata.getJDBCMajorVersion()); // 4
System.out.println(metadata.getJDBCMinorVersion()); // 2
```

## 関連ドキュメント

| ドキュメント | 内容 |
|------|------|
| [PreparedStatementと型](./prepared-types/) | パラメーターメタデータ、名前付きbind、SQLType、NULL、型変換 |
| [ResultSet、Statement、LOB](./resultset-lob/) | 型指定の検索、ストリーム、LOB、タイムアウト、リソース管理 |
| [トランザクションと接続プール](./transaction-pooling/) | Standardのローカルトランザクション、DataSource、接続プール |
| [DatabaseMetaData](./database-metadata/) | テーブル、列、キー、インデックス、機能の検索 |
| [Append API](./append-api/) | `MachStatement`による高速入力 |
| [移行とトラブルシューティング](./migration-troubleshooting/) | 旧ドライバーからの移行、非サポート機能、エラー処理 |
