---
type: docs
title: '13.6 監視と診断'
weight: 60
toc: true
---

運用診断では再現時刻と症状を記録し、サーバー状態、セッション・文、ストレージ・メモリ、
関連ログを同じ時間軸で確認します。`M$` メタデータテーブルはスキーマ、`V$` 仮想テーブルは現在状態を提供します。

<a id="log-diagnosis-logs"></a>

## 診断とログ

1. 問題の開始・終了時刻とクライアント情報を記録します。
2. `machadmin -e` でサーバー応答を確認します。
3. `V$SESSION` と `V$STMT` から関連処理を探します。
4. 症状に応じてストレージ・メモリ・ROLLUP などの仮想テーブルを確認します。
5. 同じ時刻のサーバー・クライアント・loader ログを比較します。
6. 変更前に現在の設定と基準値を保存します。

<a id="configuration-trace-log"></a>
<a id="log-diagnosis-logs-configuration-trace-log"></a>

<a id="trace-log-설정"></a>

## トレースログ設定

トレースレベル、ファイルサイズ、保持設定は、障害分析に必要な範囲だけを調整します。
[設定リファレンス](/dbms/reference/configuration/configuration/)で、現行リリースのプロパティ名、
許容値、再起動の要否を確認します。機密 SQL やデータが記録され得るため、ログのアクセス権限と保持期間を設定します。

<a id="log-server-logs"></a>
<a id="log-diagnosis-logs-log-server-logs"></a>

<a id="server-log"></a>

## サーバーログ

デフォルトのトレースディレクトリは `$MACHBASE_HOME/trc` です。ファイル名が固定とは考えず、
実際のディレクトリと設定値を確認します。

```bash
ls -lh "$MACHBASE_HOME/trc"
tail -n 200 "$MACHBASE_HOME/trc/machbase.trc"
```

エラー文字列を数えるだけでなく、最初のエラー、直前の警告、起動・停止、チェックポイント・
ストレージのイベントを時系列で確認します。手動コマンドでログを一括削除しないでください。

<a id="log-logs-machsql"></a>
<a id="log-diagnosis-logs-log-logs-machsql"></a>

<a id="machsql-log"></a>

## machsql ログ

`machsql.history` には認証情報や機密 SQL が残ることがあります。運用アカウントの履歴ファイル権限を
制限し、共有前に内容を確認します。再現 SQL は、対象データベース、実行時刻、結果・エラーとともに保存します。

<a id="log-logs-machloader"></a>
<a id="log-diagnosis-logs-log-logs-machloader"></a>

<a id="machloader-log"></a>

## machloader ログ

大量ロードでは、終了コード、サマリー、ログ、失敗行ファイルをまとめて確認します。

- スキーマと入力列数・順序
- 区切り文字、引用符、エンコーディング
- NULL と DATETIME の形式
- 最初の失敗行と繰り返すエラーコード
- 最終的な成功・失敗件数

失敗行ファイル全体をそのまま再実行しないでください。原因を修正したサンプルで検証し、失敗行だけを再処理します。

<a id="item"></a>

<a id="metadata-table"></a>

## メタデータテーブル

`M$SYS_TABLES`、`M$SYS_COLUMNS`、`M$SYS_INDEXES` などで現在のデータベースのスキーマを確認します。
名前だけで結合せず、データベース ID、所有者 ID、オブジェクト ID を含めます。予約オブジェクト名や
内部テーブル構造にアプリケーションが依存しないようにします。

<a id="item-2"></a>

<a id="virtual-table"></a>

## 仮想テーブル

まず現行リリースの実際の列を確認します。

```sql
SELECT * FROM V$SESSION LIMIT 1;
SELECT * FROM V$STMT LIMIT 1;
SELECT * FROM V$PROPERTY LIMIT 1;
SELECT * FROM V$STORAGE_USAGE LIMIT 1;
SELECT * FROM V$SYSMEM LIMIT 1;
SELECT * FROM V$ROLLUP LIMIT 1;
SELECT * FROM V$LICENSE_INFO LIMIT 1;
```

全一覧と列の意味は[システムカタログ](/dbms/reference/system-catalog/virtual-table-full/)を参照してください。

<a id="monitoring-capacity"></a>

## 監視と容量管理

アラートは固定しきい値よりも、正常時の基準値、増加率、業務ピーク負荷、復旧の余裕を基準に設定します。
ファイルシステムとデータベースの使用量を併せて確認し、バックアップ・エクスポートの別領域も含めます。

<a id="status-check-state-server"></a>
<a id="monitoring-capacity-status-check-state-server"></a>

<a id="server-상태"></a>

## サーバー状態

```bash
"$MACHBASE_HOME/bin/machadmin" -e
```

プロセスが存在するだけで正常とは判断しません。ネイティブ接続、軽量 SQL、直近のサーバーログも確認します。

<a id="execution-session"></a>
<a id="monitoring-capacity-execution-session"></a>

<a id="session과-실행-sql"></a>

## セッションと実行 SQL

```sql
SELECT id, user_name, user_ip, login_time, client_type
FROM V$SESSION
ORDER BY login_time DESC;

SELECT sess_id, id AS stmt_id, state, record_size, query
FROM V$STMT
ORDER BY sess_id, id;
```

長時間実行が必ずしもエラーとは限りません。処理内容、処理行数、クライアントのタイムアウト、
I/O・CPU 状態を併せて確認し、cancel・kill の必要性を判断します。

<a id="capacity-disk"></a>
<a id="monitoring-capacity-capacity-disk"></a>

<a id="disk-용량"></a>

## ディスク容量

```bash
df -h "$MACHBASE_HOME"
du -sh "$MACHBASE_HOME/dbs"
```

別の `DBS_PATH` を使用する場合は実際のパスを確認します。内部パーティションファイルを
直接編集・削除しないでください。

<a id="memory-capacity"></a>
<a id="monitoring-capacity-memory-capacity"></a>

<a id="memory"></a>

## メモリ

OS の利用可能メモリとスワップ、`V$SYSMEM`、キャッシュ、同時クエリ数を併せて比較します。
内部の manager 名を自動化の固定基準にしないでください。

<a id="validation-backup"></a>
<a id="monitoring-capacity-validation-backup"></a>

<a id="backup-검증"></a>

## バックアップ検証

コマンド成功だけでなく、パス・サイズ・完了状態を記録し、隔離環境でマウントまたはリストアして、
主要テーブル、行数、時間範囲、サンプルクエリを検証します。

<a id="failure"></a>
<a id="monitoring-capacity-failure"></a>

## 障害資料の収集

- リリースと Edition
- 発生時刻とタイムゾーン
- 再現コマンドとデータベース・ユーザー
- サーバー・クライアント・loader ログ
- 関連仮想テーブルの結果
- OS の CPU・I/O・メモリ・ディスク
- 直近のスキーマ・設定・デプロイ変更
- 試行済みの対策と結果

認証情報、AUTH KEY、個人情報、機密の元データはサポート資料から除去します。
