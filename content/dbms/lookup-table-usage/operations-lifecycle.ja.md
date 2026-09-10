---
type: docs
title: '9.7 運用とデータライフサイクル'
weight: 70
toc: true
---

LOOKUPテーブルのバックアップ・復旧とデータの永続性を説明します。

LOOKUPテーブルは、ディスクに永続保存される参照データテーブルです。
運用中に値が変わる場合があるため、変更手順、バックアップ、復旧、クエリへの反映時点を併せて管理します。

永続保存と検索時のデータの場所は区別する必要があります。
サーバー起動時に永続保存されたLOOKUPの全行をメモリテーブルへ復元し、`PRIMARY KEY`とセカンダリインデックスを構築します。
稼働中のSQLクエリはこのメモリ構造を使用します。

<a id="lifecycle-lookup-data"></a>

## データライフサイクル

LOOKUPデータは、作成、入力、更新、参照、バックアップ、復旧の流れで管理します。

```
テーブル作成
  └── マスターデータの入力
        └── TAG/LOG/TRANSACTIONクエリでJOINまたは参照
              └── 運用中のUPDATE/DELETE
                    └── バックアップ / 復旧 / マウント
```

マスターデータは元のイベントより小規模ですが、クエリ結果の解釈に直接影響します。
そのため、変更前後の値と適用時点を記録する運用手順を設けます。

<a id="operate-lookup-change"></a>

## マスターデータの変更手順

運用中にLOOKUPデータを変更する場合は、次の順序で進めます。

1. 変更対象行を検索します。
2. 影響範囲を確認します。
3. UPDATEまたはDELETEを実行します。
4. 必要に応じて`EXEC TABLE_REFRESH(table_name)`を実行します。
5. 代表的なクエリで反映を確認します。

`TABLE_REFRESH`は、通常のSQL DMLの直後に毎回実行するコマンドではありません。
永続LOOKUPの内容を実行時のメモリテーブルに再反映する必要があるときに使用します。
名前の範囲・権限・エラー仕様は、[EXECプロシージャの正本](/dbms/reference/sql/syntax/execute-procedure-syntax/#table-refresh)を参照してください。

次は、この手順をそのまま実行する実習です。

```sql
CREATE LOOKUP TABLE ch9_ops_sensor (
    sensor_id  VARCHAR(32) PRIMARY KEY,
    site       VARCHAR(16),
    status     VARCHAR(16),
    updated_at DATETIME
);

INSERT INTO ch9_ops_sensor VALUES ('TEMP-01', 'SEOUL', 'READY', NOW);
INSERT INTO ch9_ops_sensor VALUES ('TEMP-02', 'SEOUL', 'READY', NOW);
INSERT INTO ch9_ops_sensor VALUES ('TEMP-03', 'BUSAN', 'READY', NOW);

-- 変更対象を検索します。
SELECT sensor_id, site, status FROM ch9_ops_sensor WHERE sensor_id = 'TEMP-01';

-- 変更します。
UPDATE ch9_ops_sensor
   SET status = 'INACTIVE', updated_at = NOW
 WHERE sensor_id = 'TEMP-01';

-- 必要ならメモリテーブルに再反映します。
EXEC TABLE_REFRESH(ch9_ops_sensor);

-- 代表的なクエリで確認します。
SELECT sensor_id, status FROM ch9_ops_sensor ORDER BY sensor_id;
```

TEMP-01だけが`INACTIVE`になり、残りの2行は`READY`のままです。

一括変更では、必ず先に対象件数を確認します。

```sql
SELECT COUNT(*) FROM ch9_ops_sensor
 WHERE site = 'SEOUL' AND status = 'READY';
```

TEMP-01は変更済みのためCOUNTは1です。変更前に数えなければ、対象が変わります。

```sql
DROP TABLE ch9_ops_sensor;
```

<a id="recovery-support-scope-backup-lookup"></a>

## バックアップ・復旧のサポート範囲

LOOKUPはディスクに永続保存され、データベースのバックアップに含まれます。
リストア後は行をメモリテーブルとインデックスに再構築します。
共通のBACKUP・RESTORE・MOUNTコマンドとEditionの範囲は、
[バックアップ・リストア・マウント](/dbms/operations-configuration-recovery/backup-restore-mount/)を正本とします。
復旧後に代表的なキーとJOIN結果を検証してください。

<a id="lifecycle-lookup-monitoring"></a>

## 運用点検項目

- マスターデータの変更履歴を、別のログや運用手順で残します。
- 大量のUPDATE/DELETE前に対象件数を確認します。
- 頻繁にJOINする列にはインデックスを検討します。
- 実際のデータ規模で、サーバー起動時間とLOOKUPの行・インデックスのメモリ使用量を点検します。
- Appendの重複キー処理を使用する場合は、`LOOKUP_APPEND_UPDATE_ON_DUPKEY`設定を確認します。
- バックアップからの復旧後は、代表的なJOINクエリで参照結果を確認します。
