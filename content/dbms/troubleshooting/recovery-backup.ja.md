---
type: docs
title: '15.5 バックアップと復旧の問題'
weight: 50
toc: true
---

<a id="failure-backup-restore"></a>

## バックアップ・リストアが失敗する場合

バックアップ失敗時は、サーバープロセスの OS アカウントのパス権限、空き容量、
同じパスの既存バックアップ、サーバーログを確認します。

```sql
SELECT * FROM V$STORAGE_USAGE;
```

```bash
machadmin -e
tail -100 "$MACHBASE_HOME/trc/machbase.trc"
```

リストアは既存の物理データベースを置き換える破壊的操作です。サーバーを停止するだけでは不十分で、
既存データベースがあると拒否されます。次は概念的な点検手順であり、そのまま運用コマンドとしてコピーしないでください。

```text
1. 復旧対象・バックアップパス・バージョン・チェックサムを確認する。
2. 現在のデータベースの保護方法とロールバック条件の承認を得る。
3. サーバーを正常停止する。
4. 承認済み手順で現在の物理データベースを削除する。
5. machadmin restore を実行する。
6. サーバーを起動し、業務検証クエリを実行する。
```

`machadmin -d` は現在のデータベースを破棄するため、バックアップと明示的な承認なしに実行してはいけません。
正確な構文と制約は[BACKUP/RESTORE/MOUNT 構文](/dbms/reference/sql/syntax/backup-restore-mount-syntax/)
を参照してください。

バックアップイメージ確認や MOUNT 成功は初期検証にすぎず、完全な復旧可能性を保証しません。
別環境でのリストアとアプリケーション検証まで定期的に実施します。

<a id="failure-mount"></a>

## マウントが失敗する場合

現在の MOUNT 一覧、一意な別名、バックアップパス、サーバープロセスの読み取り権限を確認します。

```sql
SELECT * FROM V$STORAGE_MOUNT_DATABASES;
```

現行構文ではバックアップパスの後に別名を指定します。

```sql
MOUNT DATABASE '/backup/sc15_snapshot' TO backup_check;
SELECT COUNT(*) FROM backup_check.sys.target_table;
UMOUNT DATABASE backup_check;
```

別名の衝突、非対応 Edition、非互換バックアップ、使用中のマウントを区別して対応します。
ファイルを強制削除したり、サーバーメタデータを編集したりしないでください。
