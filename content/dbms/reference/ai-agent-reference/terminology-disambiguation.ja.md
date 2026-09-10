---
type: docs
title: '16.8.7 terminology-disambiguation'
weight: 70
toc: true
---

ユーザーの用語を一般的なデータベースの意味で推測せず、Machbaseの正式なリファレンスで確認します。

| 用語 | 正式な参照先 |
|------|-------------|
| TAG, LOG, LOOKUP, VOLATILE, TRANSACTION | [基本概念](/dbms/core-concepts/)と[テーブルタイプの選択](/dbms/data-modeling-table-design/) |
| AppendとSQL INSERT | [連携の共通概念](/dbms/development-tools-integration/concepts-common/) |
| ROLLUP | [ROLLUPの利用](/dbms/tag-rollup-usage/) |
| BASETIME, BASE DISTANCE, SUMMARIZED | [TAGの構造とスキーマ](/dbms/tag-table-usage/table-structure-schema/) |
| AUTH KEY | [認証とAUTH KEY](/dbms/security-access-control/authentication-auth-key/) |
| Broker, Warehouse | [EditionとClusterの概念](/dbms/core-concepts/concepts-edition/) |
| database, owner, tablespace | [複数データベースの運用](/dbms/operations-configuration-recovery/multi-database/) |

回答では製品のオブジェクト名とSQLキーワードをそのまま保持します。ユーザーが一般的な意味で使う
用語がMachbaseのオブジェクトと異なる場合は、最初に区別します。
