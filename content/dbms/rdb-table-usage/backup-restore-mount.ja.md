---
type: docs
title: '8.12 TRANSACTIONのバックアップ、リストア、マウント'
weight: 120
toc: true
---

バックアップコマンドに成功しても、復旧の準備が完了したとは限りません。
特に本番テーブルとバックアップテーブルが同名だと、誤った方を検索して検証完了と考えがちです。
バックアップ後に本番の値を変更し、両方の結果が異なることを確認する方法で検証します。

<a id="support-scope-backup-rdb"></a>

<a id="백업-범위와-복원-경로를-구분합니다"></a>

## バックアップ・リストアのサポート範囲

| 操作 | TRANSACTIONに関する基準 |
|---|---|
| BACKUP DATABASE | 対象範囲の永続的なTRANSACTIONデータを含む |
| BACKUP TABLE | 指定テーブルと必要なメタデータをバックアップ |
| 増分バックアップ | TRANSACTIONストレージは、その時点の全体スナップショットとして含まれる |
| MOUNT DATABASE | バックアップを読み取り専用で検索 |
| オフラインインスタンス復旧 | サーバーを停止しmachadmin -rを使用 |
| オンライン論理データベース復旧 | サポートされる論理バックアップをRESTORE DATABASEで復元 |

増分バックアップのTRANSACTIONデータを、変更行だけの差分として見積もらないでください。
内部ファイルの直接コピーではなく、サポートされるバックアップコマンドを使用する必要があります。
TRANSACTIONを含むバックアップを、Clusterで使用するための迂回手段にすることもできません。

<a id="backup-rdb"></a>
<a id="design-backup-mount-rdb"></a>

<a id="운영-값과-백업-값을-다르게-만들어-확인합니다"></a>

## バックアップとマウントの検証

この実習は、検証用Standard環境のSYSアカウントを対象にします。
バックアップ・マウント権限と、サーバーファイルへのアクセス権限が必要です。
パスはサーバー上の例であり、実行するたびに存在しない新しいパスに変更してください。
親ディレクトリと空き容量を確認し、パスを再使用するために既存のバックアップを削除しないでください。

```sql
CREATE TRANSACTION TABLE ch8_backup (
    id     LONG PRIMARY KEY,
    code   VARCHAR(32) NOT NULL,
    amount DECIMAL(18,2)
);
CREATE UNIQUE INDEX ch8_backup_code ON ch8_backup(code);
INSERT INTO ch8_backup VALUES (1, 'A', 10.25);
INSERT INTO ch8_backup VALUES (2, 'B', 20.50);

BACKUP TABLE ch8_backup INTO DISK = '/backup/ch8_table_20260907_a';

UPDATE ch8_backup SET amount = 99.00 WHERE id = 1;

MOUNT DATABASE '/backup/ch8_table_20260907_a' TO ch8_bak;

SELECT id, code, amount FROM ch8_bak.SYS.ch8_backup ORDER BY id;
SELECT id, code, amount FROM ch8_backup ORDER BY id;
```

バックアップ側は10.25・20.50、本番側は99.00・20.50です。
マウントしたデータの検索には、`マウント名.所有者.テーブル名`の3部構成の名前を使用します。
別の所有アカウントで実習した場合は、SYSも実際の所有者に合わせる必要があります。

`SELECT ... FROM ch8_backup`だけを実行しないよう注意してください。
これはマウントしたバックアップの検証ではなく、現在の接続の本番テーブルを検索します。
バックアップに含めなかった他のテーブルも存在するはずだと期待しないでください。

マウントは読み取り専用であり、UPDATE・DDLを行う復旧環境ではありません。
検証を終え、開いているカーソルを閉じてからマウントを解除します。

```sql
UMOUNT DATABASE ch8_bak;
DROP TABLE ch8_backup;
```

このクリーンアップは、実習テーブルとマウントだけを削除します。
バックアップディレクトリは残るため、以後の保持ポリシーに従って別途管理してください。

<a id="복원-검증에서는-데이터뿐-아니라-제약도-확인합니다"></a>

## リストアの検証項目

隔離した復旧環境では、所有者、行数、業務キー、金額合計、代表的なJSON値を確認してください。
PRIMARY KEY・UNIQUE INDEXが残っているか、必要な権限とアプリケーションのCOMMIT・ROLLBACKの流れが正常かも点検します。
マウント検索だけでは、実際の書き込み復旧の検証まで完了したことにはなりません。

オンラインRESTORE DATABASEは、論理バックアップと対象データベースの条件に従います。
複数のデータベースを含むインスタンス全体のイメージと混同しないでください。
既存インスタンスを削除するオフライン復旧やREPLACEは、この実習には含めません。
[リストア構文](/dbms/reference/sql/syntax/backup-restore-mount-syntax/)と
[運用手順](/dbms/operations-configuration-recovery/backup-restore-mount/)で、
権限・停止・対象置換の条件を確認してから別途実行してください。

複数テーブルの業務整合性まで検証する場合は、バックアップコマンドの成功だけで判断しないでください。
書き込み停止・業務の基準時点と、テーブル間の検証基準を併せて定めることを推奨します。
