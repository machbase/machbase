---
type: docs
title: '16.6.8 バックアップ/マウントサポート表'
weight: 80
toc: true
---

バックアップはデータをファイルに保存し、マウントは保存したバックアップファイルをデータベースに接続して参照する機能です。

## Edition別のサポート可否

| 機能 | Standard | Cluster | 備考 |
|------|:--------:|:-------:|------|
| 複数の論理データベース | O | X | Standard Edition専用 |
| BACKUP DATABASE | O | O | データベース全体のバックアップ |
| BACKUP TABLE | O | O | 特定テーブルのみのバックアップ |
| MOUNT DATABASE | O | X | Cluster Editionでは非対応 |
| UMOUNT DATABASE | O | X | Cluster Editionでは非対応 |
| machadmin -rによる復元 | O | X | Cluster Editionでは非対応 |

`BACKUP DATABASE database_name INTO DISK`は、1つのアクティブな論理データベースをバックアップします。
複数のアクティブデータベースを含むインスタンス全体のイメージは、論理`MOUNT`/`RESTORE DATABASE`の
入力には使用できません。マウント済みデータベースの参照には`USAGE`とテーブルの`SELECT`権限が
必要です。`USE`と書き込みはサポートしません。

## テーブルタイプ別のバックアップサポート

| テーブルタイプ | BACKUPのサポート | MOUNT後の参照 | 備考 |
|------------|:-----------:|:------------:|------|
| TAGテーブル | O | O | |
| LOGテーブル | O | O | |
| LOOKUPテーブル | O | O | |
| TRANSACTIONテーブル | O | O | |
| VOLATILEテーブル | X | X | メモリ上のデータのためバックアップ不可 |

## 正式な参照先

- 構文: [BACKUP · RESTORE · MOUNT](../../sql/syntax/backup-restore-mount-syntax/)
- 運用手順: [バックアップ、復元、マウント](../../../operations-configuration-recovery/backup-restore-mount/)
