---
type: docs
title: '16.6.3 TRANSACTION機能サポート表'
weight: 30
toc: true
---

MachbaseのTRANSACTIONテーブルは、トランザクションが必要な一般的なリレーショナルデータを保存します。
Machbase SQLとJDBC/ODBCなどの対応ドライバーでアクセスします。

> **注意**: TRANSACTIONテーブルは**Standard Editionでのみサポート**します。Cluster Editionでは作成・使用できません。

修飾のない`CREATE TABLE`、`CREATE TRANSACTION TABLE`、`CREATE TXN TABLE`はすべてTRANSACTION
テーブルを作成します。このためCluster Editionでは3つの構文がすべて拒否されます。
Cluster EditionでLOGテーブルを作成する場合は`CREATE LOG TABLE`を使用します。

## SQL機能のサポート可否

| 機能 | サポート | 備考 |
|------|:---------:|------|
| **基本DML** | | |
| SELECT | O | |
| INSERT | O | |
| UPDATE | O | |
| DELETE | O | |
| INSERT ... ON DUPLICATE KEY UPDATE | O | PRIMARY KEY・UNIQUE INDEXの競合時に既存行を更新 |
| **トランザクション** | | |
| Transaction (COMMIT/ROLLBACK) | O | 単独の`BEGIN`、`COMMIT`、`ROLLBACK` |
| TRANSACTION TRUNCATEのROLLBACK | O | 明示的トランザクション内の全行削除として処理 |
| Savepoint | X | 非対応 |
| **クエリ機能** | | |
| Prepared Statement | O | |
| パラメーターバインド | O | |
| JOIN | O | 他のテーブルタイプとの結合が可能 |
| Subquery | O | |
| VIEW | O | |
| **オブジェクト** | | |
| SEQUENCE | O | `CREATE SEQUENCE` |
| PRIMARY KEY / UNIQUE INDEX | O | 単一列のPRIMARY KEYと単一・複合列のUNIQUE INDEX |
| セカンダリINDEX | O | 単一・複合列のBTREEインデックス |
| JSON path INDEX | O | `json_column->'$.path'` |
| AUTO_INCREMENT | O | `LONG`/`INT64`列単位のPRIMARY KEY |
| ALTER ADD/DROP COLUMN | O | 列定義に括弧を使用 |
| ALTER RENAME COLUMN / RENAME TO | O | 列名・テーブル名の変更 |
| ALTER MODIFY COLUMN | X | 非対応 |
| Trigger | X | 非対応 |
| Stored Procedure | X | 非対応 |
| Foreign Key | X | 非対応 |

`AUTO_INCREMENT`の使用方法は[AUTO_INCREMENT](/dbms/reference/sql/syntax/auto-increment-syntax/)を、
upsertは[INSERT ON DUPLICATE KEY UPDATE](/dbms/rdb-table-usage/insert-on-duplicate-key-update/)を参照してください。
Appendはクライアント別に経路が異なるため、[SDK Append matrix](/dbms/development-tools-integration/sdk-support-scope/#append-table-type-matrix)を
正式な参照先とします。

## トランザクションと同時アクセスの境界

アクティブなトランザクションでも、他のテーブルタイプのSELECTと、タイプが混在するJOINを許可します。
ただし、LOG・TAG・LOOKUP・VOLATILEへの書き込みを同じTRANSACTIONトランザクションに含めることはできません。
許可されたクエリも、全タイプに共通のスナップショット時点を保証するものではありません。

一般的な制約エラーでは、失敗した文とトランザクション全体を区別します。先に成功した変更を取り消すには
ROLLBACKが必要です。ロールバック専用状態では後続処理を続けず、終了してください。
開いているTRANSACTIONカーソルはCOMMIT・ROLLBACKを妨げる場合があります。

現在、複数のTRANSACTIONテーブルのコミットは、テーブルごとのストレージハンドルに順次適用されます。
通常の複数テーブルCOMMIT・ROLLBACKのサポートは、コミット中の障害を含めた複数テーブルの原子性保証とは
異なります。エラーや応答消失の後は、業務キーで反映状態を確認してください。

WALの古い読み取りスナップショットを書き込みに切り替える際の競合は、
TRANSACTION_BUSY_TIMEOUT_MS=-1でも待機では解消しません。
[トランザクション演習](../../../rdb-table-usage/transaction/)と
[2つの接続による競合演習](../../../rdb-table-usage/locking-conflict-timeout/)を参照してください。

## 関連ドキュメント

- [TRANSACTIONテーブルの利用](../../../rdb-table-usage/)
- [TRANSACTIONのDDLとDML](../../sql/syntax/)
- [SDK機能のサポート範囲](../../../development-tools-integration/sdk-support-scope/)
