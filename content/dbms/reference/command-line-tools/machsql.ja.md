---
type: docs
title: '16.4.2 machsql'
weight: 20
toc: true
---

`machsql`は、ターミナルでSQLクエリを対話的に実行するクライアントツールです。SQLスクリプトの実行、結果のファイル保存、公開鍵認証にも対応します。

## オプション一覧

```bash
machsql -h
```

| 短いオプション | 長いオプション | デフォルト値 | 説明 |
|----------|---------|--------|------|
| `-s` | `--server` | 127.0.0.1 | 接続先サーバーIPアドレス |
| `-P` | `--port` | 5656 | サーバーポート番号 |
| `-u` | `--user` | SYS | ユーザー名 |
| `-p` | `--password` | MANAGER | ユーザーパスワード |
| `-K` | `--auth-key-file` | - | 公開鍵認証用の秘密鍵ファイルのパス（8.5以降） |
| | `--auth-sig-scheme` | - | 認証署名方式。`ECDSA`、`RSA_PKCS1_V15`、`RSA_PSS`（8.5以降） |
| `-f` | `--script` | - | 実行するSQLスクリプトファイル |
| `-o` | `--output` | - | クエリ結果の保存先ファイル名 |
| `-r` | `--format` | csv | 出力ファイル形式（`csv`、`json`など） |
| `-z` | `--timezone` | - | タイムゾーン設定。例: `+0900`、`-1230` |
| `-n` | `--nls` | - | NLS設定 |
| `-c` | `--connstr` | - | 追加の接続パラメーター文字列（6.1以降） |
| `-D` | `--database` | `MACHBASEDB` | 接続直後に使用する論理データベース（8.7.0 Standard） |
| `-i` | `--silent` | - | 著作権バナーを表示せずに実行 |
| `-v` | `--verbose` | - | 詳細出力 |
| `-x` | `--testing` | - | テストモードで実行 |
| `-h` | `--help` | - | オプション一覧を表示 |

## 接続例

基本的な接続:

```bash
machsql -s 127.0.0.1 -u SYS -p MANAGER
machsql --server=localhost --user=SYS --password=MANAGER
```

ポートの指定:

```bash
machsql -s 192.168.1.10 -P 5656 -u SYS -p MANAGER
```

SQLスクリプトの実行:

```bash
machsql -s 127.0.0.1 -u SYS -p MANAGER -f create_tables.sql
```

タイムゾーンの指定:

```bash
machsql -s 127.0.0.1 -u SYS -p MANAGER -z +0900
machsql -s 127.0.0.1 -u SYS -p MANAGER -z -1230
```

結果をファイルに保存:

```bash
machsql -s 127.0.0.1 -u SYS -p MANAGER -o result.csv -f query.sql
```

## 公開鍵認証（Machbase 8.5以降）

パスワードの代わりに公開鍵によるチャレンジ認証を使用できます。

ECDSA鍵で接続:

```bash
machsql -s 127.0.0.1 -u app_user \
    -K /opt/machbase/keys/app_user_ecdsa.pem \
    --auth-sig-scheme=ECDSA
```

RSA-PSS鍵で接続:

```bash
machsql -s 127.0.0.1 -u app_user \
    -K /opt/machbase/keys/app_user_rsa.pem \
    --auth-sig-scheme=RSA_PSS
```

対応する鍵アルゴリズム:

| アルゴリズム | 鍵パラメーター | デフォルトの署名方式 |
|---------|-----------|--------------|
| ECDSA | P-256, P-384, P-521 | `ECDSA` |
| RSA | 2048, 3072, 4096 bits | `RSA_PKCS1_V15` |

## 追加の接続パラメーター（6.1以降）

`-c`オプションで追加の接続パラメーターを指定します。

```bash
machsql -s 127.0.0.1 -u SYS -p MANAGER -P 5656 \
    -c 'ALTERNATIVE_SERVERS=192.168.0.147:9209;CONNECTION_TIMEOUT=10'
```

環境変数でも設定できます。

```bash
export MACHBASE_CONNECTION_STRING="ALTERNATIVE_SERVERS=192.168.0.148:8888;CONNECTION_TIMEOUT=3"
machsql -s 127.0.0.1 -u SYS -p MANAGER
```

`-c`オプションが環境変数より優先されます。

## 論理データベースの選択

Machbase 8.7.0 Standard Editionでは、`-D`または`--database`で接続直後に使用する
論理データベースを指定できます。

```bash
machsql -s 127.0.0.1 -u app_a -p 'AppA#1234' -D factory_a
machsql -s 127.0.0.1 -u app_a -p 'AppA#1234' --database=factory_a
```

`-c`接続文字列では、`DATABASE=factory_a`または互換性のための別名`DBNAME=factory_a`を指定できます。
`-D`と接続文字列でデータベースの値が異なると接続が拒否されるため、一方のみを指定するか同じ値を
使用してください。接続後に次のSQLで実際のサーバーカタログを確認します。

```sql
SELECT CURRENT_DATABASE();
SHOW CURRENT DATABASE;
```

## machsql組み込みコマンド

machsqlプロンプト（`Mach>`）で使用できる組み込みコマンドです。

| コマンド | 説明 |
|------|------|
| `SHOW TABLES` | すべてのテーブル一覧を表示 |
| `SHOW TABLE table_name` | 特定テーブルの列とインデックスの情報を表示 |
| `SHOW INDEXES` | すべてのインデックス一覧を表示 |
| `SHOW INDEX index_name` | 特定インデックスの情報を表示 |
| `SHOW INDEXGAP` | インデックス構築のGAP情報を表示 |
| `SHOW LSM` | LSMインデックスの構築情報を表示 |
| `SHOW TABLESPACES` | すべてのテーブルスペース一覧を表示 |
| `SHOW TABLESPACE name` | 特定テーブルスペースの情報を表示 |
| `SHOW STORAGE` | テーブル別のディスク使用量を表示 |
| `SHOW STATEMENTS` | サーバーに登録されたクエリ一覧を表示 |
| `SHOW USERS` | ユーザー一覧を表示 |
| `SHOW LICENSE` | ライセンス情報を表示 |
| `SHOW DATABASES` | アクティブ/マウント済みデータベース一覧を表示 |
| `SHOW CURRENT DATABASE` | 現在のセッションのデータベースを表示 |
| `SHOW LAST ROWID` | 直近に成功した単一行INSERTのROWIDを表示 |
| `SHOW LASTID` | `SHOW LAST ROWID`と同じコマンド |

### 最後のINSERTのROWID確認

Machbase 8.7.0 Standard Editionでは、単一行の`INSERT ... VALUES`の実行直後に挿入した行の
ROWIDを確認できます。

```sql
INSERT INTO orders(item) VALUES('pump');
SHOW LAST ROWID;
```

```text
Last ROWID : 2048
```

`SHOW LASTID`も同じ値を表示します。返すROWIDがなければ、`0`ではなく`NULL`を表示します。
INSERT失敗、batch・Append・loader、`INSERT ... SELECT`、UPSERT、再接続の後に以前の値を
使用しないでください。SELECTやCOMMITなどINSERT以外のコマンドは最後の値を保持します。

テーブル別のROWID条件とSDKでの確認方法は、
[ROWIDとINSERT結果ID](/dbms/reference/sql/rowid/)を参照してください。

## DESCとPRIMARY KEYメタデータ

`DESC table_name`は、列とインデックスの情報に続いて`[ PRIMARY KEY ]`セクションを表示します。
PRIMARY KEY名、列名、キーの順序を確認できます。TRANSACTION・LOOKUP・VOLATILEで宣言されたPKと
TAGテーブルの`NAME`が対象です。通常のLOGテーブルではPK行を表示しません。

```sql
DESC ACCOUNT;
```

この出力はSELECT結果列のメタデータとは別です。SDKでSELECT結果の列がPKかどうかを確認する方法は、
[PRIMARY KEYメタデータのサポート範囲](/dbms/development-tools-integration/sdk-support-scope/#support-scope-sdk-primary-key-metadata)を
参照してください。

## ARRAYの表示とDESC

Machbase DBMS 8.7.0の`DESC`はARRAY列を`INT32[3]`、`DECIMAL(12,4)[2]`などの正規の宣言形式で
表示します。クエリ結果は`[value,null,value]`形式です。小文字の`null`は要素のNULLを表し、
列の値全体がNULLの場合は通常のSQL `NULL`として表示します。

```sql
SELECT ID, CHANNELS, ARRAY_LENGTH(CHANNELS), CHANNELS[1]
  FROM SENSOR_ARRAY
 ORDER BY ID;
```

ARRAYの宣言、NULLの区別、式は、[数値ARRAY型](/dbms/reference/sql/types/array/)を参照してください。

## Named Bind Parameter

`machsql`の`PREPARE` SQLでは`:name`マーカーを使用できます。値は名前ではなく、
SQL内の出現順に`$1`、`$2`、...の変数へ指定します。

```sql
PREPARE INSERT INTO SENSOR_DATA (ID, NAME, VALUE)
        VALUES (:id, :name, :value);
$1 := 900;
$2 := 'machsql-client';
$3 := 72.125000;
EXECUTE;
PREPARE CLEAN;
```

同じ名前が繰り返される場合も、各出現位置に値を指定します。

```sql
PREPARE SELECT ID, NAME
        FROM SENSOR_DATA
        WHERE ID = :id OR PARENT_ID = :id;
$1 := 900;
$2 := 900;
EXECUTE;
PREPARE CLEAN;
```

名前の構文と出現順序の規則は、[Named Bind Parameter構文](../../sql/syntax/named-bind-parameter-syntax/)を
参照してください。

## 使用例

```bash
# 対話モードで接続
machsql -s 127.0.0.1 -u SYS -p MANAGER

# 接続後にテーブルを確認
Mach> SHOW TABLES;

# テーブル構造の確認
Mach> SHOW TABLE sensor_data;

# SQLスクリプトを実行し結果をCSVで保存
machsql -s 127.0.0.1 -u SYS -p MANAGER \
    -f report.sql -o report_output.csv -i
```
