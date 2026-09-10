---
type: docs
title: '16.6.9 サーバーとSDKの互換性'
weight: 90
toc: true
---

MachbaseサーバーとSDKのバージョンが異なる場合、基本的な接続は可能でも、最新の認証、メタデータ、
名前付きバインドパラメーターの機能が制限される場合があります。この節では、サーバーとSDKの
バージョンの組み合わせ別のサポート範囲とアップグレード順序を説明します。

## サーバーとSDKのバージョン互換表

| サーバーバージョン | 8.5クライアントドライバー | 8.7.0クライアントドライバー |
|-----------|:---------------------:|:---------------------:|
| **8.7.0サーバー** | 限定的な互換性 | 完全互換 |
| **8.5サーバー** | 完全互換 | 後方互換、8.7.0の名前指定APIは非対応 |

- **完全互換**: 同じバージョンの組み合わせです。実際に使用できる機能はEdition、テーブルタイプ、SDKのサポート範囲によって異なり、その機能を含むビルドを使用する必要があります。
- **限定的な互換性**: 基本的な接続は可能ですが、AUTH KEYの拡張など8.7.0の新機能が動作しない場合があります。
- **後方互換**: 8.5サーバーの範囲内の機能のみ使用できます。

## Machbase 8.7.0 SDKの主な変更点

### AUTH KEY認証の拡張

8.7.0ではAUTH KEYのチャレンジ認証方式を拡張しました。

- 対応する署名方式: `ECDSA`、`RSA_PKCS1_V15`、`RSA_PSS`
- 8.5以前のドライバーでは、新しい署名方式`RSA_PSS`をサポートしない場合があります。
- AUTH KEY認証を使用する場合は、ドライバーを8.7.0に更新してください。

```text
-- AUTH KEYを登録（サーバー）
ALTER USER app_user ADD AUTH KEY (
    KEY='-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----\n',
    VALID_BEFORE='2047-12-31'
);
```

### 接続文字列の互換性

Machbase SQLCLIとODBCのAUTH KEY関連パラメーター:

```ini
AUTH_MODE=CHALLENGE;
AUTH_KEY_FILE=./private_key.pem;
AUTH_SIG_SCHEME=ECDSA;
```

8.5ドライバーでは`AUTH_SIG_SCHEME`パラメーターを無視する場合があります。

### Nullableメタデータ

結果列がNULLを許容するか確認するAPIと、サーバー・SDKの組み合わせ別の制約は
[Nullableメタデータのサポート範囲](/dbms/development-tools-integration/sdk-support-scope/#support-scope-sdk-nullable-metadata)を
参照してください。互換性を確認するときは、サーバーとクライアントの両方のバージョンを記録します。

### Named Bind Parameter

名前付きパラメーターをサーバーのプリペアドステートメントへ渡すか、位置順にバインドするか、
クライアントでSQL文字列へ変換するかはSDKによって異なります。
[SDK機能のサポート範囲](/dbms/development-tools-integration/sdk-support-scope/#support-scope-sdk-transaction-prepare-bind)で
使用するクライアントの動作を確認してください。

### ARRAYと選択列Append

固定長の数値ARRAYと選択列AppendはMachbase DBMS 8.7.0でサポートします。DBMS 8.7.0サーバーと
ARRAY機能を含むSDKビルドを併用してください。旧バージョンのサーバーや対応していないSDKは、
ARRAYのメタデータや値を従来のスカラー型で代用せず、該当リクエストをエラーとして処理します。

ARRAYのSQL要素位置とMachbase専用SDKのpositionは0始まりです。従来の1始まりのSQL、
疎なオブジェクト、添字付きAppendターゲットでは、各位置を1減らしてください。保存データと
密なARRAYの要素順序は変わりません。JDBCのパラメーター序数や`java.sql.Array`のスライスなど、
標準APIが定義する1始まりの位置は変更対象ではありません。

Cluster Editionでは、coordinator、broker、warehouseをすべてARRAYに対応した同じDBMS 8.7.0ビルドに
そろえます。バージョンが混在する状態では、ARRAY DDLやARRAYデータを使用する操作を開始しないでください。

SQLとSDK別の要件は、[数値ARRAY型](/dbms/reference/sql/types/array/)と
[Sparse ARRAYと選択列Append API](/dbms/development-tools-integration/data-input-load-export/array-append/)を参照してください。

## SDKバージョンの確認

JDBC:

```java
Connection conn = DriverManager.getConnection(url, props);
DatabaseMetaData meta = conn.getMetaData();
System.out.println("Driver: " + meta.getDriverVersion());
```

Machbase SQLCLI:

```c
SQLGetInfo(conn, SQL_DRIVER_VER, buf, sizeof(buf), NULL);
```

ODBC:

```c
SQLGetInfo(conn, SQL_DRIVER_VER, buf, sizeof(buf), NULL);
```

## アップグレードの推奨事項

1. サーバーとSDKを同じバージョン（8.7.0）へ一緒にアップグレードしてください。
2. SDKを段階的にアップグレードする場合、その期間中の8.5 SDKから8.7.0サーバーへの接続は限定的な互換性となります。
3. AUTH KEY認証を使用する場合は、最初にSDKをアップグレードしてください。
4. Nullableメタデータをアプリケーションのロジックで使用する場合は、サーバーとSDKの両方を8.7.0へアップグレードしてください。
5. Named Bind Parameterの名前指定SDK APIを使用する場合は、サーバーとSDKの両方を8.7.0へアップグレードしてください。
6. ARRAYまたは選択列Appendを使用する場合は、サーバーをMachbase DBMS 8.7.0に、クライアントを対応機能を含むSDKビルドにアップグレードしてください。Cluster Editionでは全ノードをそろえます。
