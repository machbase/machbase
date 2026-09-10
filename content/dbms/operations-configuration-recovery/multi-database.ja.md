---
type: docs
title: '13.2 複数データベース'
weight: 20
toc: true
---

Standard Edition では、1つのサーバー内に複数の論理データベースを作成し、オブジェクトとアクセス権限を
分離できます。このページでは導入と運用の流れを説明します。SQL 構文、権限、SDK オプション、
バックアップ手順は、リンク先の詳細文書を参照してください。

## 適用範囲

- 複数データベースは Standard Edition の機能です。
- 論理データベースは、独立したサーバープロセスやリソース割り当て枠を作りません。
- オブジェクト名は `object`、`owner.object`、`database.owner.object` の最大3部分です。
- 別データベースを指定する場合、所有者を省略しないでください。
- マウントされたデータベースは、アクティブなデータベースとは別の、読み取り専用バックアップ参照経路です。

## 導入前の決定事項

1. データベースごとの所有者とアプリケーションユーザーを決めます。
2. `CONNECT` とオブジェクト単位の最小権限を定義します。
3. 接続プールによる現在のデータベースの初期化・復元方法を確認します。
4. バックアップ単位、復旧順序、マウント名の規則を決めます。
5. データベース別の使用量と障害を区別する監視基準を用意します。

## 簡単な検証

次の例では、2つのデータベースが分離されることを確認し、最後に両方を削除します。

```sql
CREATE DATABASE IF NOT EXISTS manual_multidb_a;
CREATE DATABASE IF NOT EXISTS manual_multidb_b;

USE manual_multidb_a;
CREATE LOG TABLE sensor_event (
    event_time DATETIME,
    message    VARCHAR(100)
);
INSERT INTO sensor_event VALUES (SYSDATE, 'from-a');

USE manual_multidb_b;
CREATE LOG TABLE sensor_event (
    event_time DATETIME,
    message    VARCHAR(100)
);
INSERT INTO sensor_event VALUES (SYSDATE, 'from-b');

SELECT message FROM manual_multidb_a.SYS.sensor_event;
SELECT message FROM manual_multidb_b.SYS.sensor_event;

USE MACHBASEDB;
DROP DATABASE manual_multidb_a CASCADE FORCE;
DROP DATABASE manual_multidb_b CASCADE FORCE;
```

`USE database_name` は現在の接続のデータベースを変更します。トランザクション、開いたカーソル、
プリペアドステートメント（*prepared statement*）、Appender がある状態では切り替えないでください。
別のデータベースのオブジェクトは `database.owner.object` で指定します。

## 権限の境界

ユーザーには、対象データベースの `CONNECT` と、実際のオブジェクト操作に必要な権限の両方が必要です。
データベースの作成・削除・権限管理 SQL は[アカウントと権限](/dbms/security-access-control/privileges/)
を参照してください。運用アカウントへ管理者権限を一括付与しないでください。

## アプリケーションの接続

<a id="94-python"></a>
<a id="95-nodejs"></a>
<a id="97-net"></a>

初期データベースのオプション名と接続プールの初期化動作は SDK ごとに異なります。各 SDK の
接続文書でサポートを確認し、接続を借りた直後に次の値を検証します。

```sql
SELECT CURRENT_DATABASE();
```

言語別設定は[開発とアプリケーション連携](/dbms/development-tools-integration/)、
サーバー・SDK の互換性は[サーバーと SDK の互換性](/dbms/reference/support-scope-constraints/compatibility-xma-protocol/)
を参照してください。

## バックアップと復旧

バックアップ前に、含めるアクティブデータベースと復旧順序を記録します。マウントされたデータベースにも
`USE` は可能ですが、読み取り専用（*read-only*）で `SELECT` だけを実行できます。
正確なコマンドと検証手順は[バックアップ・リストア・マウント](../backup-restore-mount/)を参照してください。

## 運用チェックリスト

- 接続直後と接続プールの再利用直後に `CURRENT_DATABASE()` が期待値を返すか。
- SQL と監視が、異なるデータベースの同名オブジェクトを混同していないか。
- ユーザーには対象データベースとオブジェクトの必要最小限の権限だけを付与したか。
- バックアップ・復旧訓練で全対象データベースを確認したか。
- データベース削除前に、開いた接続、オブジェクト、バックアップの保持条件を確認したか。

正確な `CREATE/DROP/USE DATABASE` 構文は
[DATABASE 構文](/dbms/reference/sql/syntax/database-syntax/)を参照してください。
