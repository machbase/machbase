---
type: docs
title: '16.1.1 SQL構文リファレンス'
weight: 10
toc: true
---

SQL構文リファレンスは、MachbaseがサポートするすべてのSQL構文のBNF表記と最小限の例を提供します。

## サポートするSQL構文の一覧

| 構文 | 分類 | 説明 |
|------|------|------|
| [CREATE TABLE](./ddl-syntax/#create-table) | DDL | LOG/TAG/LOOKUP/VOLATILE/TRANSACTIONテーブルの作成 |
| [DROP TABLE](./ddl-syntax/#drop-table) | DDL | テーブルの削除 |
| [ALTER TABLE](./ddl-syntax/#alter-table) | DDL | テーブルスキーマの変更（列の追加・削除・変更・名前変更） |
| [TRUNCATE TABLE](./ddl-syntax/#truncate-table) | DDL | テーブルの全データを削除 |
| [CREATE INDEX](./index-syntax/#create-index) | DDL | 条件付き作成とテーブルタイプ別のインデックス対応 |
| [DROP INDEX](./index-syntax/#drop-index) | DDL | インデックスの削除 |
| [CREATE ROLLUP](./rollup-syntax/#create-rollup) | DDL | TAGテーブルのROLLUP定義を作成 |
| [DROP ROLLUP / ALTER ROLLUP](./rollup-syntax/#drop-rollup) | DDL | ROLLUPの削除と制御 |
| [CREATE RETENTION](./retention-syntax/#create-retention) | DDL | データ保持ポリシーの作成 |
| [CREATE VIEW / DROP VIEW](./view-syntax/) | DDL | 保存ビューの作成と削除 |
| [CREATE TABLESPACE](./ddl-syntax/#create-tablespace) | DDL | テーブルスペースの作成 |
| [INSERT INTO](./dml-syntax/#insert-into) | DML | 単一行・複数行のデータ挿入 |
| [INSERT SELECT](./dml-syntax/#insert-select) | DML | クエリ結果を別のテーブルへ挿入 |
| [UPDATE](./dml-syntax/#update) | DML | TRANSACTION/LOOKUP/VOLATILEの行更新と、条件を制限したTAGデータの補正 |
| [DELETE](./dml-syntax/#delete) | DML | テーブルデータの削除 |
| [LOAD DATA INFILE](./load-data-infile-syntax/) | DML | CSVファイルから直接データを取り込み |
| [SELECT](./select-syntax/) | SELECT | データ検索（JOIN、GROUP BY、ORDER BY、LIMITを含む） |
| [WITH / CTE](./cte-syntax/) | SELECT | Standard Editionの非再帰共通テーブル式 |
| [Named Bind Parameter](./named-bind-parameter-syntax/) | SQL共通 | `:name`形式の値パラメーター |
| [CAST](../functions/functions-full/#cast) | SQL式 | 値を指定したデータ型へ明示的に変換 |
| [SAVE DATA INTO](./save-data-into-syntax/) | SELECT | クエリ結果をCSVファイルに保存 |
| [BACKUP](./backup-restore-mount-syntax/#backup) | 運用 | データベースまたはテーブルのバックアップ |
| [RESTORE](./backup-restore-mount-syntax/#restore) | 運用 | 論理データベースのリストアと、`machadmin -r`によるオフライン復旧 |
| [MOUNT / UMOUNT DATABASE](./backup-restore-mount-syntax/#mount-database) | 運用 | バックアップデータベースのマウント・アンマウント |
| [CREATE USER / DROP USER / ALTER USER](./user-auth-syntax/#create-drop-alter-user) | ユーザー | ユーザーの作成・削除・パスワード変更 |
| [GRANT / REVOKE](./user-auth-syntax/#grant-revoke) | ユーザー | 権限の付与と取り消し |
| [AUTH KEY管理](./user-auth-syntax/#auth-key) | ユーザー | 公開鍵ベースの認証キーの登録・管理 |
| [ALTER SYSTEM](./system-session-alter-syntax/#alter-system) | システム | セッション制御、PVO Cacheのflush、ライセンス導入など |
| [ALTER SESSION](./system-session-alter-syntax/#alter-session) | セッション | セッション別のパラメーター設定 |
| [PIVOT](./pivot-syntax/) | 分析 | 行を列へ変換するピボットクエリ |
| [WINDOW FUNCTION (OVER)](./window-function-over-syntax/) | 分析 | ウィンドウ関数とOVER句 |
| [SERIES BY](./series-syntax/) | 分析 | 連続して条件を満たすレコードのグループ化 |
| [SEARCH / ESEARCH / REGEXP](./search-esearch-regexp-syntax/) | 検索 | キーワードインデックスによるテキスト検索 |
| [ROLLUP REBUILD](./rollup-rebuild-syntax/) | 運用 | ROLLUP結果の再計算 |
| [DATABASE](./database-syntax/) | DDL/セッション | 論理データベースの作成・選択・削除と状態確認 |
| [AUTO_INCREMENT](./auto-increment-syntax/) | DDL | 64ビットPRIMARY KEYの自動値生成 |
| [EXEC procedure / SHOW ROLLUPGAP](./execute-procedure-syntax/) | 制御 | テーブルのflush・refreshとROLLUPの制御・状態確認 |

## BNF表記規則

このリファレンスで使用するBNF（Backus-Naur Form）表記は、次の規則に従います。

| 表記 | 意味 |
|------|------|
| `'keyword'` | SQL予約語（大文字・小文字は区別しない） |
| `name` | ユーザー定義名 |
| `( A \| B )` | AまたはBのどちらか |
| `[ ... ]` | 任意の要素（省略可能） |
| `( ... )*` | 0回以上の繰り返し |
| `( ... )+` | 1回以上の繰り返し |
| `( ... )?` | 0回または1回 |
