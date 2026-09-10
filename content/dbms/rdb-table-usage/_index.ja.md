---
type: docs
title: '8. TRANSACTIONテーブルの活用'
weight: 80
toc: true
---

元のログを蓄積する処理と、注文状態・在庫・機器情報を変更する処理では性質が異なります。
状態を変更する業務では、「何行が変わったか」「途中で失敗するとどこまで戻るか」
「別の接続が同時に更新するとどうなるか」も確認する必要があります。

TRANSACTIONテーブルは、このようなリレーショナルなクエリと変更のためのStandard Edition専用テーブルです。
この章では、小さなサンプルで結果を確認しながら、スキーマ、更新、トランザクション、同時アクセス、復旧を説明します。
内部ではSQLiteストレージを使用しますが、公開構文とサポート範囲はMachbase SQLを基準にしてください。
SQLiteや他のRDBMSの全機能をそのまま使用できるわけではありません。

<a id="필요한-작업부터-찾아보세요"></a>

## この章の構成

| 節 | 確認内容 |
|---|---|
| [8.1 概要と選択基準](./overview-use-criteria/) | LOG・TAG・LOOKUPとの役割の区別 |
| [8.2 テーブル構造とスキーマ](./table-structure-schema/) | 識別子・業務キー・型・制約の設計 |
| [8.3 作成、変更、削除](./create-alter-drop/) | DDLの実行と既存データの確認 |
| [8.4 データ入力と変更](./data-input-mutation/) | 条件付き更新・削除・コピー・Append |
| [8.5 クエリと分析](./query-analysis/) | フィルター・ソート・集計・JSON検索 |
| [8.6 インデックスとパフォーマンス](./index-performance/) | PK・UNIQUE・複合・JSONパスインデックス |
| [8.7 運用とデータライフサイクル](./operations-lifecycle/) | バッチ削除と運用確認の基準 |
| [8.8 制約、エラー、トラブルシューティング](./constraints-errors-troubleshooting/) | 症状別の確認と再試行判断 |
| [8.9 トランザクション](./transaction/) | 文の失敗・ROLLBACK・コミットの保証範囲 |
| [8.10 ロック、競合、busy timeout](./locking-conflict-timeout/) | 2接続の競合とスナップショットの再試行 |
| [8.11 JOINとリレーショナルクエリの設計](./join-relational-query/) | 結合で増加・除外される行の確認 |
| [8.12 バックアップ、リストア、マウント](./backup-restore-mount/) | バックアップ時点のデータの実検証 |
| [8.13 INSERT ON DUPLICATE KEY UPDATE](./insert-on-duplicate-key-update/) | 挿入・更新の分岐と重複処理 |

自動採番の共通構文は[AUTO_INCREMENT](/dbms/reference/sql/syntax/auto-increment-syntax/)を参照してください。

<a id="실습-환경과-실행-단위를-먼저-맞춥니다"></a>

## 実習環境と実行単位

SQL実習はDBMS 8.7 Standard Editionの検証環境を対象にします。
各節で`ch8_`接頭辞のオブジェクトを準備・削除するため、他の節の実行結果には依存しません。
テーブル・インデックスの作成権限が必要で、バックアップの実習には別途権限とサーバー上のパスが必要です。

BEGINからCOMMIT・ROLLBACKまでは同じ接続で実行してください。
2セッションの実習では、指定したA・Bの順序に従ってください。
意図的に失敗するSQLは通常の流れと分離しています。
実習を再実行する前に、クリーンアップSQLまで完了したことを確認してください。

注意: テーブル名にTRANSACTIONが含まれていても、すべての操作とすべての障害を一括で戻せるわけではありません。
DDL、他のタイプへの書き込み、障害時の複数テーブルのコミット境界は、[8.9 トランザクション](./transaction/)で先に確認してください。
