---
title : machsql
type : docs
weight: 40
toc: true
---

`machsql` は、端末から `SQL` クエリーを実行する対話型ツールです。

## 起動オプション {#run-option-description}

```
[mach@localhost]$ machsql -h
```

| 短縮形 | 完全形 | 説明 |
|--|--|--|
|-s | --server | サーバー IP（既定値：127.0.0.1） |
|-u | --user | ユーザー名（既定値：SYS） |
|`-p` | --password | パスワード（既定値：MANAGER） |
|`-K` | `--auth-key-file` | 認証用秘密鍵ファイル（8.5 以降） |
|-P | --port | サーバーポート（既定値：5656） |
|-n | --nls | NLS 設定 |
|-f | --script | 実行する `SQL` スクリプト |
|-z | --timezone=+-HHMM | タイムゾーン。例：+0900、-1230 |
|-o | --output | 結果の保存先ファイル |
|-i | --silent | 著作権表示を省略 |
|-v | --verbose | 詳細出力 |
|-x | --testing | テストモードで実行 |
|-r | --format | 出力形式（既定値：csv） |
|   | `--auth-sig-scheme` | 認証署名方式（`ECDSA`、`RSA_PKCS1_V15`、`RSA_PSS`、8.5 以降） |
|-h | --help | オプション一覧 |
|-c | --connstr | 接続パラメーターを追加（6.1 以降） |

例：

```
machsql -s localhost -u sys -p manager
machsql --server=localhost --user=sys --password=manager
machsql -s localhost -u sys -p manager -f script.sql
machsql -s localhost -u app_user -K /opt/machbase/keys/app_user_ecdsa.pem --auth-sig-scheme=ECDSA -f script.sql
#バージョン 6.1 以降でサポート
machsql -s 127.0.0.1 -u sys -p manager -P 8888 -c "ALTERNATIVE_SERVERS=192.168.0.147:9209;CONNECTION_TIMEOUT=10"
```

## AUTH KEY チャレンジ認証 {#auth-key-challenge-authentication}

> **注意**：Machbase 8.5 以降でサポートされます。

`machsql` は、パスワード認証に加えて公開鍵に基づく
チャレンジ認証をサポートします。

### 専用オプションの使用 {#using-dedicated-options}

```bash
machsql -s 127.0.0.1 -u app_user \
    -K /opt/machbase/keys/app_user_ecdsa.pem \
    --auth-sig-scheme=ECDSA \
    -f script.sql
```

```bash
machsql -s 127.0.0.1 -u app_user \
    -K /opt/machbase/keys/app_user_rsa.pem \
    --auth-sig-scheme=RSA_PSS \
    -f script.sql
```

注意事項：

- `-K` / `--auth-key-file` は、内部で `AUTH_MODE=CHALLENGE` を有効にします。
- `--auth-sig-scheme` を省略すると、鍵アルゴリズムから既定の方式を選びます。
  - `ECDSA` 鍵：`ECDSA`
  - RSA 鍵：`RSA_PKCS1_V15`
- 対応する鍵は `ECDSA` の `P-256`、`P-384`、`P-521` と、RSA の `2048`、`3072`、
  `4096` ビットです。
- RSA-PSS は `--auth-sig-scheme=RSA_PSS` を指定します。
- `AUTH_MODE=CHALLENGE` では `-p` は認証に使用しません。
- AUTH KEY を X.509 証明書の PEM から登録した場合も、認証には
  `-K` または `AUTH_KEY_FILE` で対応する秘密鍵ファイルを指定します。
- POSIX では秘密鍵ファイルの権限を `600` に制限することを推奨します。

### 接続文字列の使用 {#using-a-connection-string}

```bash
machsql -c "SERVER=127.0.0.1;PORT_NO=5656;UID=APP_USER;AUTH_MODE=CHALLENGE;AUTH_SIG_SCHEME=ECDSA;AUTH_KEY_FILE=/opt/machbase/keys/app_user_ecdsa.pem;" -f script.sql
```

接続文字列はプロセス引数やログに鍵ファイルのパスを露出させる可能性があるため、
可能なら `-K` を使用してください。

### 失敗する場合 {#failure-cases}

- 鍵ファイルが存在しない。
- 鍵の型が `AUTH_SIG_SCHEME` と一致しない。
- 有効期限（`VALID_BEFORE`）を過ぎた、または無効化された AUTH KEY は、
  認証に使用できません。

## 環境変数 MACHBASE_CONNECTION_STRING {#environment-variable-machbase_connection_string}

基本の接続パラメーターを指定します。CONNECTION_TIMEOUT や ALTERNATIVE_SERVERS の追加には、次の環境変数を使用できます。

```
export MACHBASE_CONNECTION_STRING="ALTERNATIVE_SERVERS=192.168.0.148:8888;CONNECTION_TIMEOUT=3"
```

-c の接続パラメーターは環境変数より優先されます。このオプションは 6.1 以降でサポートされます。


## ヒアドキュメントによる `SQL` スクリプト {#using-heredoc-for-sql-scripts}

`machsql` は HEREDOC（ヒアドキュメント）をサポートし、別ファイルを作らずシェルから直接 `SQL` を渡せます。自動化や一度だけの実行に便利です。

> **注意**：Machbase 8.0.50 以降でサポートされます。

### 基本構文 {#basic-syntax}

```bash
machsql -s <server> -u <user> -p <password> <<'DELIMITER'
SQL statements here
DELIMITER
```

区切り語は任意です。一般に `EOF`、`SQL`、`SQLBLOCK` を使います。`<<'DELIMITER'` のように引用符を付けると、シェル変数の展開を防げます。

### 例 {#examples}

**単純なクエリー：**

```bash
machsql -s 127.0.0.1 -u sys -p manager <<'SQLBLOCK'
select 'WORKS!!!!' from v$tables limit 2;
SQLBLOCK
```

**複数の文：**

```bash
machsql -s 127.0.0.1 -u sys -p manager <<'EOF'
CREATE TABLE test_table (id INTEGER, name VARCHAR(100));
INSERT INTO test_table VALUES (1, 'First Record');
INSERT INTO test_table VALUES (2, 'Second Record');
SELECT * FROM test_table;
DROP TABLE test_table;
EOF
```

**変数を使用する場合（区切り語の引用符なし）：**

```bash
TABLE_NAME="my_table"
machsql -s 127.0.0.1 -u sys -p manager <<EOF
SELECT COUNT(*) FROM ${TABLE_NAME};
EOF
```

**出力のリダイレクト：**

```bash
machsql -s 127.0.0.1 -u sys -p manager <<'SQL' > output.csv
SELECT name, time, value FROM tag_table
WHERE time >= NOW - INTERVAL 1 HOUR
ORDER BY time DESC;
SQL
```

### ヒアドキュメントの利点 {#benefits-of-heredoc}

1. **一時ファイル不要**：`SQL` を直接実行できます。
2. **インラインのスクリプト**：シェルに `SQL` を埋め込み、読みやすくできます。
3. **自動化**：配置や保守用のスクリプトを簡単にできます。
4. **変数の置換**：引用符を省略すると、`SQL` 内でシェル変数を使用できます。

### 注意事項 {#notes}

- 変数展開を防ぐには `<<'DELIMITER'` を使用します。
- `SQL` 内でシェル変数を使うには `<<DELIMITER` とします。
- 終端の区切り語は、1 行に単独で記述してください。
- すべての `machsql` 起動オプションと併用できます。


## SHOW コマンド {#show-command}

テーブル、テーブルスペース、インデックスなどの情報を表示します。

SHOW コマンド一覧：

* SHOW INDEX
* SHOW INDEXES
* SHOW INDEXGAP
* SHOW LSM
* SHOW LICENSE
* SHOW STATEMENTS
* SHOW STORAGE
* SHOW TABLE
* SHOW TABLES
* SHOW TABLESPACE
* SHOW TABLESPACES
* SHOW USERS

### SHOW INDEX {#show-index}
インデックス情報を表示します。

構文：

```
SHOW INDEX index_name
```

例：

```
Mach> CREATE TABLE t1 (c1 INTEGER, c2 VARCHAR(10));
Created successfully.
Mach> CREATE VOLATILE TABLE t2 (c1 INTEGER, c2 VARCHAR(10));
Created successfully.
Mach> CREATE INDEX t1_idx1 ON t1(c1) INDEX_TYPE LSM;
Created successfully.
Mach> CREATE INDEX t1_idx2 ON t1(c2) INDEX_TYPE BITMAP;
Created successfully.
Mach> CREATE INDEX t2_idx1 ON t2(c1) INDEX_TYPE REDBLACK;
Created successfully.
Mach> CREATE INDEX t2_idx2 ON t2(c2) INDEX_TYPE REDBLACK;
Created successfully.

Mach> SHOW INDEX t1_idx2;
TABLE_NAME                                          COLUMN_NAME                                         INDEX_NAME                                          INDEX_TYPE   KEY_COMPRESS  MAX_LEVEL
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
PART_VALUE_COUNT BITMAP_ENCODE
-----------------------------------
T1                                                  C2                                                  T1_IDX2                                             LSM          COMPRESSED    2
100000           EQUAL
[1] row(s) selected.
```

### SHOW INDEXES {#show-indexes}

すべてのインデックスを表示します。

**構文：**

```
SHOW INDEXES
```

**例：**

```sql
Mach> CREATE TABLE t1 (c1 INTEGER, c2 VARCHAR(10));
Created successfully.
Mach> CREATE VOLATILE TABLE t2 (c1 INTEGER, c2 VARCHAR(10));
Created successfully.
Mach> CREATE INDEX t1_idx1 ON t1(c1) INDEX_TYPE LSM;
Created successfully.
Mach> CREATE INDEX t1_idx2 ON t1(c2) INDEX_TYPE BITMAP;
Created successfully.
Mach> CREATE INDEX t2_idx1 ON t2(c1) INDEX_TYPE REDBLACK;
Created successfully.
Mach> CREATE INDEX t2_idx2 ON t2(c2) INDEX_TYPE REDBLACK;
Created successfully.

Mach> SHOW INDEXES;
USER_NAME             TABLE_NAME                                          COLUMN_NAME                                         INDEX_NAME                                          INDEX_TYPE
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
SYS                   T1                                                  C1                                                  T1_IDX1                                             LSM
SYS                   T1                                                  C2                                                  T1_IDX2                                             LSM
SYS                   T2                                                  C2                                                  T2_IDX2                                             REDBLACK
SYS                   T2                                                  C1                                                  T2_IDX1                                             REDBLACK
[4] row(s) selected.
```

### SHOW INDEXGAP {#show-indexgap}

インデックス作成の GAP 情報を表示します。

例：

```
Mach> SHOW INDEXGAP
TABLE_NAME                                INDEX_NAME                                GAP
-------------------------------------------------------------------------------------------------------------
INDEX_TABLE                               T1_IDX1                                   0
INDEX_TABLE                               T1_IDX2                                   0
```

### SHOW LSM {#show-lsm}

LSM インデックス作成の情報を表示します。

例：

```
Mach> SHOW LSM;
TABLE_NAME                                INDEX_NAME                                LEVEL       COUNT
--------------------------------------------------------------------------------------------------------------------------
T1                                        IDX1                                      0           0
T1                                        IDX1                                      1           100000
T1                                        IDX1                                      2           0
T1                                        IDX1                                      3           0
T1                                        IDX2                                      0           100000
T1                                        IDX2                                      1           0
[6] row(s) selected.
```

### SHOW LICENSE {#show-license}

ライセンス情報を表示します。

例：

```
Mach> SHOW LICENSE
INSTALL_DATE          ISSUE_DATE            EXPIRY_DATE  TYPE        POLICY
---------------------------------------------------------------------------------------
2016-07-01 10:24:37   20160325              20170325    2           0
[1] row(s) selected.
```

### SHOW STATEMENTS {#show-statements}

サーバーに登録されたすべてのクエリー（Prepare、Execute、Fetch）を表示します。

例：

```
Mach> SHOW STATEMENTS
USER_ID     SESSION_ID  QUERY
--------------------------------------------------------------------------------------------------------------
0           2           SELECT ID USER_ID, SESS_ID SESSION_ID, QUERY FROM V$STMT
[1] row(s) selected.
```

### SHOW STORAGE {#show-storage}

ユーザーが作成したテーブルごとのディスク使用量を表示します。

構文：

```
SHOW STORAGE
```

例：

```
Mach> CREATE TAG TABLE TAG (name varchar(20) primary key, time datetime basetime, value double summarized);
Created successfully.

Mach> SHOW STORAGE
TABLE_NAME                                          DATA_SIZE            INDEX_SIZE           TOTAL_SIZE
------------------------------------------------------------------------------------------------------------------------
_TAG_DATA_0                                         50335744             0                    50335744
_TAG_DATA_1                                         50335744             0                    50335744
_TAG_DATA_2                                         50335744             0                    50335744
_TAG_DATA_3                                         50335744             0                    50335744
_TAG_META                                           0                    0                    0
```

### SHOW TABLE {#show-table}

ユーザーが作成したテーブルの情報を表示します。

構文：

```
SHOW TABLE table_name
```

例：

```
Mach> CREATE TABLE t1 (c1 INTEGER, c2 VARCHAR(10));
Created successfully.
Mach> CREATE INDEX t1_idx1 ON t1(c1) INDEX_TYPE LSM;
Created successfully.
Mach> CREATE INDEX t1_idx2 ON t1(c1) INDEX_TYPE BITMAP;
Created successfully.

Mach> SHOW TABLE T1
[ COLUMN ]
----------------------------------------------------------------
NAME                          TYPE                LENGTH
----------------------------------------------------------------
C1                            integer             11
C2                            varchar             10

[ INDEX ]
----------------------------------------------------------------
NAME                          TYPE                COLUMN
----------------------------------------------------------------
T1_IDX1                       LSM                 C1
T1_IDX2                       LSM                 C1
```

### SHOW TABLES {#show-tables}

ユーザーが作成したすべてのテーブルを表示します。

例：

```
Mach> SHOW TABLES
NAME
--------------------------------------------
BONUS
DEPT
EMP
SALGRADE
[4] row(s) selected.
```

### SHOW TABLESPACE {#show-tablespace}

テーブルスペース情報を表示します。

例：

```
Mach> CREATE TABLE t1 (id integer);
Created successfully.
Mach> CREATE INDEX t1_idx_id ON t1(id);
Created successfully.

Mach> SHOW TABLESPACE SYSTEM_TABLESPACE;
[TABLE]
NAME                                      TYPE
-------------------------------------------------------
T1                                        LOG
[1] row(s) selected.

[INDEX]
TABLE_NAME                                COLUMN_NAME                               INDEX_NAME
----------------------------------------------------------------------------------------------------------------------------------
T1                                        ID                                        T1_IDX_ID
[1] row(s) selected.
```

### SHOW TABLESPACES {#show-tablespaces}

すべてのテーブルスペースを表示します。

例：

```
Mach> CREATE TABLESPACE tbs1 DATADISK disk1 (DISK_PATH="tbs1_disk1"), disk2 (DISK_PATH="tbs1_disk2"), disk3 (DISK_PATH="tbs1_disk3");
Created successfully.

-- ここでデータを挿入
...
...


Mach> SHOW TABLESPACES;
NAME                                                                              DISK_COUNT  USAGE
-----------------------------------------------------------------------------------------------------------------------
SYSTEM_TABLESPACE                                                                 1           0
TBS1                                                                              3           25824256
[2] row(s) selected.
```

### SHOW USERS {#show-users}

ユーザー一覧を表示します。

例：

```
Mach> CREATE USER testuser IDENTIFIED BY 'test1234';
Created successfully.

Mach> SHOW USERS;
USER_NAME
--------------------------------------------
SYS
TESTUSER
[2] row(s) selected.
```
