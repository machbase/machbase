---
type: docs
title: '16.8.4 support-matrix'
weight: 40
toc: true
---

このページではサポート表を複製せず、質問の観点を確認して現行の正式な参照先へ案内します。

## 確認順序

1. [Edition別サポート表](/dbms/reference/support-scope-constraints/edition/)でStandardとClusterの範囲を確認します。
2. [テーブルタイプ別サポート表](/dbms/reference/support-scope-constraints/table-types-type/)で対象テーブルのSQL・APIの範囲を確認します。
3. [SDKのサポート範囲](/dbms/development-tools-integration/sdk-support-scope/)でクライアントAPIと最低限の根拠を確認します。
4. 機能別の詳細サポート表で条件と例外を確認します。

| 機能群 | 正式な参照先 |
|--------|------|
| TAGデータのUPDATE | [TAG UPDATEサポート表](/dbms/reference/support-scope-constraints/tag-data-update/) |
| ROLLUP | [ROLLUPのサポート範囲](/dbms/reference/support-scope-constraints/rollup/) |
| TRANSACTION | [TRANSACTIONのサポート範囲](/dbms/reference/support-scope-constraints/rdb/) |
| バックアップ・MOUNT | [バックアップ/MOUNTサポート表](/dbms/reference/support-scope-constraints/backup-mount/) |
| 権限 | [権限サポート表](/dbms/reference/support-scope-constraints/privileges/) |

サポート可否を回答するときは、`O/△/X`だけでなくEdition、テーブルタイプ、サーバーとSDKの
バージョン、必須条件も併せて示します。
