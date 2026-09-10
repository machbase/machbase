---
title : "JDBC"
type : docs
weight: 20
toc: true
---

## JDBC の概要 {#jdbc-overview}

JDBC（Java DataBase Connectivity）は、Java でデータベースを操作するためのインターフェースです。SQL リクエストを構築するオブジェクト指向のクラスを定義し、さまざまなリレーショナルデータベースに共通の API を提供します。JDBC ドライバーを利用すると、接続先の DB を変更しても共通の処理を再利用できます。


## 標準 JDBC 機能 {#standard-jdbc-functions}

[標準機能の仕様 4.0](https://www.oracle.com/java/technologies/javase/javase-tech-database.html#corespec40)

## JDBC の認証モード {#jdbc-authentication-modes}

> **注意**：AUTH KEY チャレンジ認証は Machbase 8.5 以降でサポートされます。

Machbase JDBC は従来のパスワード認証と、公開鍵に基づく
チャレンジ認証をサポートします。

### パスワード認証 {#password-authentication}

従来どおり `user` と `password` を使用します。

### AUTH KEY チャレンジ認証 {#auth-key-challenge-authentication}

次のプロパティを使用します。

- `AUTH_MODE`
  - `PASSWORD` または `CHALLENGE`
- `AUTH_SIG_SCHEME`
  - `ECDSA`
  - `RSA_PKCS1_V15`
  - `RSA_PSS`
- `AUTH_KEY_FILE`
  - ローカルの PEM 形式秘密鍵ファイルのパス

注意事項：

- `AUTH_MODE=CHALLENGE` では、`password` は認証に使用しません。
- `AUTH_KEY_FILE` は必須です。
- `AUTH_SIG_SCHEME` を省略すると、鍵ファイルから既定の方式を選びます。
  - EC 鍵：`ECDSA`
  - RSA 鍵：`RSA_PKCS1_V15`
- 対応する鍵は `ECDSA` の `P-256`、`P-384`、`P-521` と、RSA の `2048`、`3072`、
  `4096` ビットです。
- RSA-PSS を使用するには `AUTH_SIG_SCHEME=RSA_PSS` を指定します。
- `AUTH_KEY_FILE` があり `AUTH_MODE` が省略されている場合は、
  `CHALLENGE` として扱います。
- 秘密鍵ファイルは絶対パスを推奨します。相対パスは
  JVM の作業ディレクトリを基準に解決します。
- POSIX 環境では、秘密鍵ファイルの権限を `600` に制限することを推奨します。

### `Properties` の例 {#properties-example}

```java
String sURL = "jdbc:machbase://127.0.0.1:5656/machbasedb";

Properties sProps = new Properties();
sProps.put("user", "app_user");
sProps.put("AUTH_MODE", "CHALLENGE");
sProps.put("AUTH_SIG_SCHEME", "ECDSA");
sProps.put("AUTH_KEY_FILE", "/opt/machbase/keys/app_user_ecdsa.pem");

Class.forName("com.machbase.jdbc.MachDriver");
Connection conn = DriverManager.getConnection(sURL, sProps);
```

### URL クエリー文字列の例 {#url-query-string-example}

```text
jdbc:machbase://127.0.0.1:5656/machbasedb?AUTH_MODE=CHALLENGE&AUTH_SIG_SCHEME=ECDSA&AUTH_KEY_FILE=/opt/machbase/keys/app_user_ecdsa.pem
```

URL に鍵ファイルのパスを含めるとログや設定ダンプに露出しやすいため、
`Properties` の使用を推奨します。

### 再接続の動作 {#reconnect-behavior}

- 最初の接続が `AUTH_MODE=CHALLENGE` の場合、再接続でも
  チャレンジ認証を行います。
- 以前の nonce や署名は再利用しません。
- チャレンジ認証が失敗しても、パスワード認証へ
  自動的に切り替わりません。


## JDBC 接続オプション {#jdbc-connection-options}

`Properties` または URL のクエリー文字列で指定できます。
DBMS Standard のソースは、次の公開オプションを処理します。

| オプション | 説明 |
| -- | -- |
| `user` / `password` | パスワード認証の認証情報。 |
| `AUTH_MODE`, `AUTH_SIG_SCHEME`, `AUTH_KEY_FILE` | 前述のチャレンジ認証設定。 |
| `TIMEZONE` | セッションのタイムゾーン。例：`+0900`。不正な文字列では接続に失敗。 |
| `randomHost` | `true` の場合、解析したホスト一覧から接続先をランダムに選択。 |
| `maxStatements` | プール接続でキャッシュするステートメントの上限。 |
| `CONNECTION_TIMEOUT` | ソケット接続タイムアウト（秒）。`0` は無期限。 |
| `SOCKET_TIMEOUT` | ソケット読み取りタイムアウト（秒）。`0` は無期限。 |
| `characterEncoding` | クライアントの文字エンコーディング名。 |


## 拡張 JDBC 機能 {#extension-jdbc-functions}

### setIpv4 {#setipv4}

```java
void setIpv4(int ind, String ipString)
```

PreparedStatement に IPv4 アドレスを設定します。

列インデックスと IPv4 文字列を引数に取ります。

### setIpv6 {#setipv6}

```java
void setIpv6(int ind, String ipString)
```

PreparedStatement に IPv6 アドレスを設定します。

列インデックスと IPv6 文字列を引数に取ります。

### executeAppendOpen {#executeappendopen}

```java
ResultSet executeAppendOpen(String aTableName, int aErrorCheckCount)
```

Statement で Append プロトコルを開始します。

テーブル名とエラーチェック間隔を受け取り、結果を含む ResultSet を返します。

### executeAppendData {#executeappenddata}

```java
int executeAppendData(ResultSetMetaData rsmd, ArrayList aData)
```

Statement の Append プロトコルでデータを入力します。

executeAppendOpen の ResultSet メタデータと入力データを受け取ります。送信バッファーへ格納した場合は 1、バッファーを Machbase へ送信した場合は 2 を返します。1 と 2 はどちらも成功です。

### executeAppendDataByTime {#executeappenddatabytime}

```java
int executeAppendDataByTime(ResultSetMetaData rsmd, long aTime, ArrayList aData)
```

Statement の Append プロトコルで、時刻を指定してデータを入力します。

executeAppendOpen の ResultSet メタデータ、指定するタイムゾーンの時刻値、入力データを受け取ります。送信バッファーに格納した場合は 1 を返します。

### executeAppendFlush {#executeappendflush}

```java
int executeAppendFlush()
```

現在の APPEND ストリームをフラッシュし、保留中の応答を確認します。成功時は 1 を返します。

### executeAppendClose {#executeappendclose}

```java
int executeAppendClose()
```

Statement の Append プロトコルを終了します。

成功時は 1 を返します。

### executeSetAppendErrorCallback {#executesetappenderrorcallback}

```java
int executeSetAppendErrorCallback(MachAppendCallback aCallback)
```

APPEND 中のエラーを通知するコールバックを設定します。

エラーログを出力するコールバック関数を受け取り、成功時は 1 を返します。

### getAppendSuccessCount {#getappendsuccesscount}

```java
long getAppendSuccessCount()
```

Statement の Append プロトコルで成功した件数を取得します。

成功件数を返します。

### getAppendFailureCount {#getappendfailurecount}

```java
long getAppendFailureCount()
```

Statement の Append プロトコルで失敗した件数を取得します。

失敗件数を返します。

### バッチ APPEND の実装に関する注意 {#batch-append-implementation-note}

ソースには、バッチ入力用の内部メソッド `executeAppendAll` と `executeAppendAllByTime` があります。確認対象の DBMS Standard ソースでは、公開 `MachStatement` メソッドではありません。公開ラッパーが提供されるまでは、前述の公開 APPEND メソッドを使用してください。


## アプリケーション開発 {#application-development}

### JDBC ライブラリーの確認 {#jdbc-library-installation-check}
$MACHBASE_HOME/lib に machbase.jar があることを確認します。

```bash
[mach@localhost ~]$ cd $MACHBASE_HOME/lib
[mach@localhost lib]$ ls -l machbase.jar
-rw-rw-r-- 1 mach mach 78599 Jun 18 10:00 machbase.jar
[mach@localhost lib]$
```

### Makefile の作成 {#makefile-creation-guide}

クラスパスに $(MACHBASE_HOME)/lib/machbase.jar を指定します。Makefile の例を示します。

```bash
CLASSPATH=".:$(MACHBASE_HOME)/lib/machbase.jar"

SAMPLE_SRC = MakeData.java Sample1Connect.java Sample2Insert.java Sample3PrepareStmt.java Sample4Append.java

all: build

build:
    -@rm -rf *.class
    javac -classpath $(CLASSPATH) -d . $(SAMPLE_SRC)

create_table:
    machsql -s localhost -u sys -p manager -f createTable.sql

select_table:
    machsql -s localhost -u sys -p manager -f selectTable.sql

make_data_file:
    java -classpath $(CLASSPATH) MakeData

run_sample1:
    java -classpath $(CLASSPATH) Sample1Connect

run_sample2:
    java -classpath $(CLASSPATH) Sample2Insert

run_sample3:
    java -classpath $(CLASSPATH) Sample3PrepareStmt

run_sample4:
    java -classpath $(CLASSPATH) Sample4Append

clean:
    rm -rf *.class
```

### コンパイルとリンク {#compile-and-link}
次のように make を実行します。

```bash
[mach@localhost jdbc]$ make
javac -classpath ".:/home/machbase/machbase_home/lib/machbase.jar" -d . MakeData.java Sample1Connect.java Sample2Insert.java Sample3PrepareStmt.java Sample4Append.java
[mach@localhost jdbc]$
```

## Maven を使用した開発 {#application-development-with-maven}

Maven で Machbase JDBC（machjdbc）をプロジェクトに追加できます。
ドライバーは [Maven Central Repository](https://mvnrepository.com/artifact/com.machbase/machjdbc) で取得できます。

### machjdbc の追加と使用 {#import-and-use-machjdbc}

`pom.xml` の `<dependencies>` に次の定義を追加します。
```
<dependency>
    <groupId>com.machbase</groupId>
    <artifactId>machjdbc</artifactId>
    <version>{{< jdbc_version >}}</version>
</dependency>
```
> {{< jdbc_version >}} は Maven Central の最新バージョンに置き換えられます。
<br>

ソースでは、次の `import` 文で使用できます。
```
import com.machbase.jdbc.*;
```
<br><br>

## JDBC のサンプル {#jdbc-sample}

### 接続の例 {#connection-example}

Machbase JDBC でサーバーに接続する例です。ファイル名は Sample1Connect.java です。


> **ヒント**：_arrival_time は既定では表示されません。<br>
> 表示するには、接続文字列に show_hidden_cols=1 を追加します。<br><br>
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;次の例の接続文字列を変更します。<br>
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;String sURL = "jdbc:machbase://localhost:5656/machbasedb?show_hidden_cols=1";

```java
import java.util.*;
import java.sql.*;
import com.machbase.jdbc.*;

public class Sample1Connect
{
    public static Connection connect()
    {
        Connection conn = null;
        try
        {
            String sURL = "jdbc:machbase://localhost:5656/machbasedb";

            Properties sProps = new Properties();
            sProps.put("user", "sys");
            sProps.put("password", "manager");

            Class.forName("com.machbase.jdbc.MachDriver");
            conn = DriverManager.getConnection(sURL, sProps);
        }
        catch ( ClassNotFoundException ex )
        {
            System.err.println("Exception : unable to load mach jdbc driver class");
        }
        catch ( Exception e )
        {
            System.err.println("Exception : " + e.getMessage());
        }
        return conn;
    }

    public static void main(String[] args) throws Exception
    {
        Connection conn = null;

        try
        {
            conn = connect();
            if( conn != null )
            {
                System.out.println("machbase JDBC connected.");
            }
        }
        catch( Exception e )
        {
            System.err.println("Exception : " + e.getMessage());
        }
        finally
        {
            if( conn != null )
            {
                conn.close();
                conn = null;
            }
        }
    }
}
```

用意した Makefile でコンパイルし、実行します。

```bash
[mach@localhost jdbc]$ make
javac -classpath ".:/home/machbase/machbase_home/lib/machbase.jar" -d . MakeData.java Sample1Connect.java Sample2Insert.java Sample3PrepareStmt.java Sample4Append.java
[mach@localhost jdbc]$ make run_sample1
java -classpath ".:/home/machbase/machbase_home/lib/machbase.jar" Sample1Connect
machbase JDBC connected.
```

### データの挿入と取得（1）直接実行 {#data-input-and-output-example-1-direct-io}

JDBC でデータを挿入し、取得する例です。

ファイル名は Sample2Insert.java です。
まず machsql で必要なテーブルを作成します。
この例は sample_table を事前に作成します。

```bash
[mach@localhost jdbc]$ machsql
=================================================================
     Machbase Client Query Utility
     Release Version 8.5.4.develop
     Copyright 2014, Machbase Inc. or its subsidiaries.
     All Rights Reserved.
=================================================================
Machbase server address (Default:127.0.0.1):
Machbase rser ID  (Default:SYS)
Machbase user password: MANAGER
MACHBASE_CONNECT_MODE=INET, PORT=5656 EDITION=STANDARD
mach> create table sample_table(d1 short, d2 integer, d3 long, f1 float, f2 double, name varchar(20), text text, bin binary, v4 ipv4, v6 ipv6, dt datetime);
Created successfully.
mach> exit
[mach@localhost jdbc]$
```

```java
import java.util.*;
import java.sql.*;
import com.machbase.jdbc.*;

public class Sample2Insert
{
    public static Connection connect()
    {
        Connection conn = null;
        try
        {

            String sURL = "jdbc:machbase://localhost:5656/machbasedb";

            Properties sProps = new Properties();
            sProps.put("user", "sys");
            sProps.put("password", "manager");

            Class.forName("com.machbase.jdbc.MachDriver");

            conn = DriverManager.getConnection(sURL, sProps);

        }
        catch ( ClassNotFoundException ex )
        {
            System.err.println("Exception : unable to load mach jdbc driver class");
        }
        catch ( Exception e )
        {
            System.err.println("Exception : " + e.getMessage());
        }

        return conn;
    }


    public static void main(String[] args) throws Exception
    {
        Connection conn = null;
        Statement stmt = null;
        String sql;

        try
        {
            conn = connect();
            if( conn != null )
            {
                System.out.println("machbase JDBC connected.");

                stmt = conn.createStatement();

                for(int i=1; i<10; i++)
                {
                    sql = "INSERT INTO SAMPLE_TABLE VALUES (";
                    sql += (i - 5) * 6552;//short
                    sql += ","+ ((i - 5) * 429496728);//integer
                    sql += ","+ ((i - 5) * 922337203685477580L);//long
                    sql += ","+ 1.23456789+"e"+((i<=5)?"":"+")+((i-5)*7);//float
                    sql += ","+ 1.23456789+"e"+((i<=5)?"":"+")+((i-5)*61);//double
                    sql += ",'id-"+i+"'";//varchar
                    sql += ",'name-"+i+"'";//text
                    sql += ",'aabbccddeeff'";//binary
                    sql += ",'192.168.0."+i+"'";//ipv4
                    sql += ",'::192.168.0."+i+"'";
                    sql += ",TO_DATE('2014-08-0"+i+"','YYYY-MM-DD')";//dt
                    sql += ")";

                    stmt.execute(sql);

                    System.out.println( i+" record inserted.");
                }

                String query = "SELECT d1, d2, d3, f1, f2, name, text, bin, to_hex(bin), v4, v6, to_char(dt,'YYYY-MM-DD') as dt from SAMPLE_TABLE";
                ResultSet rs = stmt.executeQuery(query);
                while( rs.next () )
                {
                    short d1 = rs.getShort("d1");
                    int d2 = rs.getInt("d2");
                    long d3 = rs.getLong("d3");
                    float f1 = rs.getFloat("f1");
                    double f2 = rs.getDouble("f2");
                    String name = rs.getString("name");
                    String text = rs.getString("text");
                    String bin = rs.getString("bin");
                    String hexbin = rs.getString("to_hex(bin)");
                    String v4 = rs.getString("v4");
                    String v6 = rs.getString("v6");
                    String dt = rs.getString("dt");

                    System.out.print("d1: " + d1);
                    System.out.print(", d2: " + d2);
                    System.out.print(", d3: " + d3);
                    System.out.print(", f1: " + f1);
                    System.out.print(", f2: " + f2);
                    System.out.print(", name: " + name);
                    System.out.print(", text: " + text);
                    System.out.print(", bin: " + bin);
                    System.out.print(", hexbin: "+hexbin);
                    System.out.print(", v4: " + v4);
                    System.out.print(", v6: " + v6);
                    System.out.println(", dt: " + dt);

                }
                rs.close();
            }
        }
        catch( SQLException se )
        {
            System.err.println("SQLException : " + se.getMessage());
        }
        catch( Exception e )
        {
            System.err.println("Exception : " + e.getMessage());
        }
        finally
        {
            if( stmt != null )
            {
                stmt.close();
                stmt = null;
            }
            if( conn != null )
            {
                conn.close();
                conn = null;
            }
        }
    }
}
```

用意した Makefile でコンパイルし、実行します。

```bash
[mach@localhost jdbc]$ make
javac -classpath ".:/home/machbase/machbase_home/lib/machbase.jar" -d . MakeData.java Sample1Connect.java Sample2Insert.java Sample3PrepareStmt.java Sample4Append.java
[mach@localhost jdbc]$ make run_sample2
make run_sample2
java -classpath ".:/home/machbase/machbase_home/lib/machbase.jar" Sample2Insert
machbase JDBC connected.
1 record inserted.
2 record inserted.
3 record inserted.
4 record inserted.
5 record inserted.
6 record inserted.
7 record inserted.
8 record inserted.
9 record inserted.
d1: 26208, d2: 1717986912, d3: 3689348814741910320, f1: 1.2345679E28, f2: 1.23456789E244, name: id-9, text: name-9, bin: aabbccddeeff, hexbin: 616162626363646465656666, v4: 192.168.0.9, v6: 0:0:0:0:0:0:c0a8:9, dt: 2014-08-09
d1: 19656, d2: 1288490184, d3: 2767011611056432740, f1: 1.2345678E21, f2: 1.23456789E183, name: id-8, text: name-8, bin: aabbccddeeff, hexbin: 616162626363646465656666, v4: 192.168.0.8, v6: 0:0:0:0:0:0:c0a8:8, dt: 2014-08-08
d1: 13104, d2: 858993456, d3: 1844674407370955160, f1: 1.23456788E14, f2: 1.23456789E122, name: id-7, text: name-7, bin: aabbccddeeff, hexbin: 616162626363646465656666, v4: 192.168.0.7, v6: 0:0:0:0:0:0:c0a8:7, dt: 2014-08-07
d1: 6552, d2: 429496728, d3: 922337203685477580, f1: 1.2345679E7, f2: 1.23456789E61, name: id-6, text: name-6, bin: aabbccddeeff, hexbin: 616162626363646465656666, v4: 192.168.0.6, v6: 0:0:0:0:0:0:c0a8:6, dt: 2014-08-06
d1: 0, d2: 0, d3: 0, f1: 1.2345679, f2: 1.23456789, name: id-5, text: name-5, bin: aabbccddeeff, hexbin: 616162626363646465656666, v4: 192.168.0.5, v6: 0:0:0:0:0:0:c0a8:5, dt: 2014-08-05
d1: -6552, d2: -429496728, d3: -922337203685477580, f1: 1.2345679E-7, f2: 1.23456789E-61, name: id-4, text: name-4, bin: aabbccddeeff, hexbin: 616162626363646465656666, v4: 192.168.0.4, v6: 0:0:0:0:0:0:c0a8:4, dt: 2014-08-04
d1: -13104, d2: -858993456, d3: -1844674407370955160, f1: 1.2345679E-14, f2: 1.23456789E-122, name: id-3, text: name-3, bin: aabbccddeeff, hexbin: 616162626363646465656666, v4: 192.168.0.3, v6: 0:0:0:0:0:0:c0a8:3, dt: 2014-08-03
d1: -19656, d2: -1288490184, d3: -2767011611056432740, f1: 1.2345679E-21, f2: 1.23456789E-183, name: id-2, text: name-2, bin: aabbccddeeff, hexbin: 616162626363646465656666, v4: 192.168.0.2, v6: 0:0:0:0:0:0:c0a8:2, dt: 2014-08-02
d1: -26208, d2: -1717986912, d3: -3689348814741910320, f1: 1.2345679E-28, f2: 1.23456789E-244, name: id-1, text: name-1, bin: aabbccddeeff, hexbin: 616162626363646465656666, v4: 192.168.0.1, v6: 0:0:0:0:0:0:c0a8:1, dt: 2014-08-01
```

### データの挿入と取得（2）PreparedStatement {#data-input-and-output-example-2-preparedstatement-input-used}

PreparedStatement で入力する例です。

ファイル名は Sample3PrepareStmt.java です。

```java
import java.util.*;
import java.sql.*;
import java.text.SimpleDateFormat;
import com.machbase.jdbc.*;

public class Sample3PrepareStmt
{
    public static Connection connect()
    {
        Connection conn = null;
        try
        {
            String sURL = "jdbc:machbase://localhost:5656/machbasedb";

            Properties sProps = new Properties();
            sProps.put("user", "sys");
            sProps.put("password", "manager");

            Class.forName("com.machbase.jdbc.MachDriver");

            conn = DriverManager.getConnection(sURL, sProps);

        }
        catch ( ClassNotFoundException ex )
        {
            System.err.println("Exception : unable to load mach jdbc driver class");
        }
        catch ( Exception e )
        {
            System.err.println("Exception : " + e.getMessage());
        }
        return conn;
    }

    public static void main(String[] args) throws Exception
    {
        Connection conn = null;
        Statement stmt = null;
        MachPreparedStatement preStmt = null;
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss SSS");

        try
        {
            conn = connect();
            if( conn != null )
            {
                System.out.println("machbase JDBC connected.");

                stmt = conn.createStatement();
                preStmt = (MachPreparedStatement)conn.prepareStatement("INSERT INTO SAMPLE_TABLE VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)");

                String ipStr = null;
                String dateStr = null;
                for(int i=1; i<10; i++)
                {
                    ipStr = String.format("172.16.0.%d",i);
                    dateStr = String.format("2014-08-09 12:23:34 %03d", i);
                    byte[] bin = new byte[20];
                    for(int j=0;j<20;j++){
                        bin[j]=(byte)(Math.random()*255);
                    }
                    java.util.Date day = sdf.parse(dateStr);
                    java.sql.Date sqlDate = new java.sql.Date(day.getTime());

                    preStmt.setShort(1, (i-5) * 3276 );
                    preStmt.setInt(2, (i-5) * 214748364 );
                    preStmt.setLong(3, (i-5) * 922337203685477580L );
                    preStmt.setFloat(4, 1.23456789101112131415*Math.pow(10,i));
                    preStmt.setDouble(5, 1.23456789101112131415*Math.pow(10,i*10));
                    preStmt.setString(6, String.format("varchar-%d",i));
                    preStmt.setString(7, String.format("text-%d",i));
                    preStmt.setBytes(8, bin);
                    preStmt.setIpv4(9, ipStr);
                    preStmt.setIpv6(10, "::"+ipStr);
                    preStmt.setDate(11, sqlDate);
                    preStmt.executeUpdate();

                    System.out.println( i+" record inserted.");
                }

                //日時形式：YYYY-MM-DD HH24:MI:SS mmm:uuu:nnnn
                String query = "SELECT d1, d2, d3, f1, f2, name, text, bin, to_hex(bin), v4, v6, to_char(dt,'YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn') as dt from SAMPLE_TABLE";
                ResultSet rs = stmt.executeQuery(query);
                while( rs.next () )
                {
                    short d1 = rs.getShort("d1");
                    int d2 = rs.getInt("d2");
                    long d3 = rs.getLong("d3");
                    float f1 = rs.getFloat("f1");
                    double f2 = rs.getDouble("f2");
                    String name = rs.getString("name");
                    String text = rs.getString("text");
                    String bin = rs.getString("bin");
                    String hexbin = rs.getString("to_hex(bin)");
                    String v4 = rs.getString("v4");
                    String v6 = rs.getString("v6");
                    String dt = rs.getString("dt");

                    System.out.print("d1: " + d1);
                    System.out.print(", d2: " + d2);
                    System.out.print(", d3: " + d3);
                    System.out.print(", f1: " + f1);
                    System.out.print(", f2: " + f2);
                    System.out.print(", name: " + name);
                    System.out.print(", text: " + text);
                    System.out.print(", bin: " + bin);
                    System.out.print(", hexbin: "+hexbin);
                    System.out.print(", v4: " + v4);
                    System.out.print(", v6: " + v6);
                    System.out.println(", dt: " + dt);
                }
                rs.close();
            }
        }
        catch( SQLException se )
        {
            System.err.println("SQLException : " + se.getMessage());
        }
        catch( Exception e )
        {
            System.err.println("Exception : " + e.getMessage());
        }
        finally
        {
            if( stmt != null )
            {
                stmt.close();
                stmt = null;
            }
            if( conn != null )
            {
                conn.close();
                conn = null;
            }
        }
    }
}
```

用意した Makefile でコンパイルし、実行します。

Sample2Insert.java で入力したデータも一緒に表示されます。

```bash
[mach@localhost jdbc]$ make
javac -classpath ".:/home/machbase/machbase_home/lib/machbase.jar" -d . Sample1Connect.java
MakeData.java Sample2Insert.java Sample3PrepareStmt.java Sample4Append.java
[mach@localhost jdbc]$ make run_sample3
make run_sample3
java -classpath ".:/home/machbase/machbase_home/lib/machbase.jar" Sample3PrepareStmt
machbase JDBC connected.
1 record inserted.
2 record inserted.
3 record inserted.
4 record inserted.
5 record inserted.
6 record inserted.
7 record inserted.
8 record inserted.
9 record inserted.
d1: 13104, d2: 858993456, d3: 3689348814741910320, f1: 754454.6, f2: 453821.380752063, name:
varchar-9, text: text-9, bin: ?+,??r?J?????S)n?, hexbin:
A4C9A8D491D6728B4AACB39EE5FC5300296EFA9F, v4: 172.16.0.9, v6: 0:0:0:0:0:0:ac10:9, dt:
2014-08-09 12:23:34 009:000:000
?h???a?, hexbin: 6C20F09329ABBA3E7DE501C30DA368D6EFC961EF, v4: 172.16.0.8, v6:
0:0:0:0:0:0:ac10:8, dt: 2014-08-09 12:23:34 008:000:000
d1: 6552, d2: 429496728, d3: 1844674407370955160, f1: 2664182.0, f2: 1357910.1926900472, name:
varchar-7, text: text-7, bin: ????Uls?q?H?I?&(?, hexbin:
B5A0A2EFA185556C73BF719448BD49C92628F8C6, v4: 172.16.0.7, v6: 0:0:0:0:0:0:ac10:7, dt:
2014-08-09 12:23:34 007:000:000
d1: 3276, d2: 214748364, d3: 922337203685477580, f1: 443847.1, f2: 9342855.256576871, name:
varchar-6, text: text-6, bin: ??>x??Eu?? ?Iw??+n, hexbin:
BC973E78F5B44575D6CC15F94977DAE62B6E1D0E, v4: 172.16.0.6, v6: 0:0:0:0:0:0:ac10:6, dt:
2014-08-09 12:23:34 006:000:000
d1: 0, d2: 0, d3: 0, f1: 1283723.1, f2: 1771261.2019240903, name: varchar-5, text: text-5,
bin: &== j?j3?? T??y?
??, hexbin: 263D3D1C6AF56A33F79D0C54A5C479A4030AFE8B, v4: 172.16.0.5, v6: 0:0:0:0:0:0:ac10:5,
dt: 2014-08-09 12:23:34 005:000:000
d1: -3276, d2: -214748364, d3: -922337203685477580, f1: 9447498.0, f2: 7529392.937964935,
name: varchar-4, text: text-4, bin: ?Sw ??)? ?h2?E??/?, hexbin:
C653771DD2DF29CDB30ED96832E745D3D7A52FD2, v4: 172.16.0.4, v6: 0:0:0:0:0:0:ac10:4, dt:
2014-08-09 12:23:34 004:000:000
d1: -6552, d2: -429496728, d3: -1844674407370955160, f1: 9589634.0, f2: 5994172.201347323,
name: varchar-3, text: text-3, bin: 9aB,.????L/?=3,?`?f, hexbin:
3961422C2EA39BE6F2964C2FCD3D332C8960A466, v4: 172.16.0.3, v6: 0:0:0:0:0:0:ac10:3, dt:
2014-08-09 12:23:34 003:000:000
d1: -9828, d2: -644245092, d3: -2767011611056432740, f1: 7409537.5, f2: 2313739.6613546023,
name: varchar-2, text: text-2, bin: _? N?3 ?? ??~H ??= 8, hexbin:
5F84144EF63320F3C718B0FD7E4809A4CB3D1838, v4: 172.16.0.2, v6: 0:0:0:0:0:0:ac10:2, dt:
2014-08-09 12:23:34 002:000:000
d1: -13104, d2: -858993456, d3: -3689348814741910320, f1: 596626.75, f2: 2649492.1936065694,
name: varchar-1, text: text-1, bin: ???d??Wu$v? 7m?-, hexbin:
E8D0C564B4EB57E59B08752476FC07376DBF2D14, v4: 172.16.0.1, v6: 0:0:0:0:0:0:ac10:1, dt:
2014-08-09 12:23:34 001:000:000
d1: 26208, d2: 1717986912, d3: 3689348814741910320, f1: 1.2345679E28, f2: 1.23456789E244,
name: id-9, text: name-9, bin: aabbccddeeff, hexbin: 616162626363646465656666, v4:
192.168.0.9, v6: 0:0:0:0:0:0:c0a8:9, dt: 2014-08-09 00:00:00 000:000:000
d1: 19656, d2: 1288490184, d3: 2767011611056432740, f1: 1.2345678E21, f2: 1.23456789E183,
name: id-8, text: name-8, bin: aabbccddeeff, hexbin: 616162626363646465656666, v4:
192.168.0.8, v6: 0:0:0:0:0:0:c0a8:8, dt: 2014-08-08 00:00:00 000:000:000
d1: 13104, d2: 858993456, d3: 1844674407370955160, f1: 1.23456788E14, f2: 1.23456789E122,
name: id-7, text: name-7, bin: aabbccddeeff, hexbin: 616162626363646465656666, v4:
192.168.0.7, v6: 0:0:0:0:0:0:c0a8:7, dt: 2014-08-07 00:00:00 000:000:000
d1: 6552, d2: 429496728, d3: 922337203685477580, f1: 1.2345679E7, f2: 1.23456789E61, name:
id-6, text: name-6, bin: aabbccddeeff, hexbin: 616162626363646465656666, v4: 192.168.0.6, v6:
0:0:0:0:0:0:c0a8:6, dt: 2014-08-06 00:00:00 000:000:000
d1: 0, d2: 0, d3: 0, f1: 1.2345679, f2: 1.23456789, name: id-5, text: name-5, bin:
aabbccddeeff, hexbin: 616162626363646465656666, v4: 192.168.0.5, v6: 0:0:0:0:0:0:c0a8:5, dt:
2014-08-05 00:00:00 000:000:000
d1: -6552, d2: -429496728, d3: -922337203685477580, f1: 1.2345679E-7, f2: 1.23456789E-61,
name: id-4, text: name-4, bin: aabbccddeeff, hexbin: 616162626363646465656666, v4:
192.168.0.4, v6: 0:0:0:0:0:0:c0a8:4, dt: 2014-08-04 00:00:00 000:000:000
d1: -13104, d2: -858993456, d3: -1844674407370955160, f1: 1.2345679E-14, f2: 1.23456789E-122,
name: id-3, text: name-3, bin: aabbccddeeff, hexbin: 616162626363646465656666, v4:
192.168.0.3, v6: 0:0:0:0:0:0:c0a8:3, dt: 2014-08-03 00:00:00 000:000:000
d1: -19656, d2: -1288490184, d3: -2767011611056432740, f1: 1.2345679E-21, f2: 1.23456789E-183,
name: id-2, text: name-2, bin: aabbccddeeff, hexbin: 616162626363646465656666, v4:
192.168.0.2, v6: 0:0:0:0:0:0:c0a8:2, dt: 2014-08-02 00:00:00 000:000:000
d1: -26208, d2: -1717986912, d3: -3689348814741910320, f1: 1.2345679E-28, f2: 1.23456789E-244,
name: id-1, text: name-1, bin: aabbccddeeff, hexbin: 616162626363646465656666, v4:
192.168.0.1, v6: 0:0:0:0:0:0:c0a8:1, dt: 2014-08-01 00:00:00 000:000:000
```

### 拡張機能 APPEND の例 {#extension-function-append-example}

Machbase JDBC は、大量データを高速入力する Append プロトコルをサポートします。

使用例を示します。
前の例の sample_table を使用します。
ファイル名は Sample4Append.java です。
`data.txt` の内容を sample_table に入力します。
実行前に `make_data_file` ターゲットで `data.txt` を作成してください。

```java
import java.util.*;
import java.sql.*;
import java.io.*;
import java.text.SimpleDateFormat;
import java.math.BigDecimal;
import com.machbase.jdbc.*;


public class Sample4Append
{
    protected static final String sTableName = "sample_table";
    protected static final int sErrorCheckCount = 100;

    public static Connection connect()
    {
        Connection conn = null;
        try
        {
            String sURL = "jdbc:machbase://localhost:5656/machbasedb";

            Properties sProps = new Properties();
            sProps.put("user", "sys");
            sProps.put("password", "manager");

            Class.forName("com.machbase.jdbc.MachDriver");

            conn = DriverManager.getConnection(sURL, sProps);

        }
        catch ( ClassNotFoundException ex )
        {
            System.err.println("Exception : unable to load mach jdbc driver class");
        }
        catch ( Exception e )
        {
            System.err.println("Exception : " + e.getMessage());
        }
        return conn;
    }

    public static void main(String[] args) throws Exception
    {
        Connection conn = null;
        MachStatement stmt = null;
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        Calendar cal = Calendar.getInstance();
        String filename = "data.txt";

        try
        {
            conn = connect();
            if( conn != null )
            {
                System.out.println("machbase JDBC connected.");

                stmt = (MachStatement)conn.createStatement();

                ResultSet rs = stmt.executeAppendOpen(sTableName, sErrorCheckCount);
                ResultSetMetaData rsmd = rs.getMetaData();

                System.out.println("append open ok");

                MachAppendCallback cb = new MachAppendCallback() {
                        @Override
                        public void onAppendError(long aErrNo, String aErrMsg, String aRowMsg) {
                             System.out.format("Append Error : [%05d - %s]\n%s\n", aErrNo, aErrMsg, aRowMsg);
                        }
                    };

                stmt.executeSetAppendErrorCallback(cb);

                System.out.println("append data start");
                BufferedReader in = new BufferedReader(new FileReader(filename));
                String buf = null;
                int cnt = 0;
                long dt;

                long startTime = System.nanoTime();

                while( (buf = in.readLine()) != null )
                {
                    ArrayList<Object> sBuf = new ArrayList<Object>();
                    StringTokenizer st = new StringTokenizer(buf,",");
                    for(int i=0; st.hasMoreTokens() ;i++ )
                    {
                        switch(i){
                            case 7://binary case
                                sBuf.add(new ByteArrayInputStream(st.nextToken().getBytes())); break;
                            case 10://date case
                                java.util.Date day = sdf.parse(st.nextToken());
                                cal.setTime(day);
                                dt = cal.getTimeInMillis()*1000000; //make nanotime
                                sBuf.add(dt);
                                break;
                            default:
                                sBuf.add(st.nextToken()); break;
                        }
                    }

                    if( stmt.executeAppendData(rsmd, sBuf) != 1 )
                    {
                        System.err.println("Error : AppendData error");
                        break;
                    }

                    if( (cnt++%10000) == 0 )
                    {
                        System.out.print(".");
                    }
                    sBuf = null;

                }
                System.out.println("\nappend data end");

                long endTime = System.nanoTime();
                stmt.executeAppendClose();
                System.out.println("append close ok");
                System.out.println("Append Result : success = "+stmt.getAppendSuccessCount()+", failure = "+stmt.getAppendFailureCount());
                System.out.println("timegap " + ((endTime - startTime)/1000) + " in microseconds, " + cnt + " records" );

                try {
                    BigDecimal records = new BigDecimal( cnt );
                    BigDecimal gap = new BigDecimal( (double)(endTime - startTime)/1000000000 );
                    BigDecimal rps = records.divide(gap, 2, BigDecimal.ROUND_UP );

                    System.out.println( rps + " records/second" );
                } catch(ArithmeticException ae) {
                    System.out.println( cnt + " records/second");
                }

                rs.close();
            }
        }
        catch( SQLException se )
        {
            System.err.println("SQLException : " + se.getMessage());
        }
        catch( Exception e )
        {
            System.err.println("Exception : " + e.getMessage());
        }
        finally
        {
            if( stmt != null )
            {
                stmt.close();
                stmt = null;
            }
            if( conn != null )
            {
                conn.close();
                conn = null;
            }
        }
    }
}
```

APPEND 時の日時データは、long 型のナノ秒時刻へ変換する必要があります。

```bash
[mach@localhost jdbc]$ make run_sample4
make run_sample4
java -classpath ".:/home/machbase/machbase_home/lib/machbase.jar" Sample4Append;
machbase JDBC connected.
append open ok
append data start
......
append data end
append close ok
Append Result : success = 100000, failure = 0
timegap 6905594 in microseconds, 100000 records
8688.61 records/second
```

1 万件ごとにドット（.）を表示し、入力時間を確認できます。

```bash
#machsql で実際の入力件数を確認
#Sample2Insert と Sample3PrepareStmt を含めて 100018 件を確認


[mach@localhost jdbc]$ machsql
=================================================================
     Machbase Client Query Utility
     Release Version 8.5.4.develop
     Copyright 2014, Machbase Inc. or its subsidiaries.
     All Rights Reserved.
=================================================================
Machbase server address (Default:127.0.0.1):
Machbase user ID  (Default:SYS)
Machbase user password: MANAGER
MACHBASE_CONNECT_MODE=INET, PORT=5656 EDITION=STANDARD
mach> select count(*) from sample_table;
count(*)
-----------------------
100018
[1] row(s) selected.
```
