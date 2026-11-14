---
type: docs
title: '1.3 基本コマンド早見表'
weight: 30
toc: true
---

接続コマンドは OS のターミナルで、SQL は接続済みの `machsql` で実行します。
サーバーアドレス、ポート、アカウントは実環境に合わせてください。以下の `MANAGER` は
クイックスタートの初期演習用パスワードです。変更済みの場合は、そのアカウントの現在のパスワードを使います。

## ターミナルで実行するコマンド

| 作業 | コマンド |
|---|---|
| 対話接続 | `machsql -s 127.0.0.1 -P 5656 -u SYS -p MANAGER` |
| SQL ファイルの実行 | `machsql -s 127.0.0.1 -P 5656 -u SYS -p MANAGER -f file.sql` |

## machsql で実行する SQL

| 作業 | コマンド |
|---|---|
| テーブル一覧 | `SHOW TABLES;` |
| 列と型の確認 | `DESC table_name;` |
| TRANSACTION テーブルの作成 | `CREATE TRANSACTION TABLE table_name (...);` |
| LOG テーブルの作成 | `CREATE LOG TABLE table_name (...);` |
| データ入力 | `INSERT INTO table_name VALUES (...);` |
| 条件に一致するデータの検索 | `SELECT ... FROM table_name WHERE ...;` |
| 結果の並べ替え | `SELECT ... FROM table_name ORDER BY ...;` |
| テーブルとデータの削除 | `DROP TABLE table_name;` |

`table_name` と `...` は、実際の名前と定義に置き換えるプレースホルダーです。
そのまま実行できる SQL は[クイックスタート](../quick-start/)にあります。
`DROP TABLE` はデータも削除するため、削除対象が演習用テーブルであることを先に確認します。

Machbase DBMS 8.7.0 の `CREATE TABLE` は、タイプを省略すると TRANSACTION テーブルを作成します。
TRANSACTION は Standard Edition でサポートされます。タイプを明示すると例の意図が明確になります。
コマンドの詳細は [machsql リファレンス](../../reference/command-line-tools/machsql/)を参照してください。
