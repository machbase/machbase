---
type: docs
title: '15.1 問題解決へのアプローチ'
weight: 10
toc: true
---

再現する前に状態と証拠を保存し、最小範囲から原因を絞り込みます。

## 5段階の問題解決手順

1. 失敗時刻、実行コマンド、エラーメッセージ全文、`ERR-` コードを記録します。
2. `machadmin -e` と接続試験で、サーバー・ネットワーク・認証のどの段階で失敗したかを区別します。
3. 同時刻のサーバーログとセッション・文の状態を確認します。
4. 原因を1つずつ修正し、同じ入力で再検証します。
5. 原因、対策、検証結果、再発防止策を記録します。

<a id="symptom"></a>

## 症状の確認

| 症状 | 最初に確認 |
|---|---|
| サーバーが応答しない | `machadmin -e`、プロセス・ポート、サーバーログ |
| 接続拒否 | サーバー状態、待ち受けアドレス、ファイアウォール、ポート |
| 認証失敗 | ユーザー、認証方式、有効期限、AUTH KEY 状態 |
| SQL 失敗 | SQL 全文、対象データベース・オブジェクト、正確なコード |
| 遅いクエリ | 実行計画、時間範囲、スキャン行数、同時負荷 |
| ロード停止 | 成功・失敗行数、bad/log ファイル、最後の成功位置 |

診断前にサーバーを再起動したり設定を変えたりすると、最初の原因を示す証拠が失われる場合があります。

<a id="diagnosis-commands"></a>

## 診断コマンド

```bash
machadmin -e
tail -100 "$MACHBASE_HOME/trc/machbase.trc"
```

```sql
SELECT * FROM V$VERSION;
SELECT ID, USER_NAME, CLOSED FROM V$SESSION ORDER BY ID;
SELECT ID, SESS_ID, STATE, QUERY FROM V$STMT ORDER BY ID;
SELECT * FROM V$STORAGE_USAGE;
SELECT NAME, VALUE FROM V$PROPERTY ORDER BY NAME;
```

運用環境の結果には SQL 本文、ユーザー名、パスなどの機密情報が含まれ得るため、共有前に確認してください。

<a id="log-logs"></a>

## ログの確認

デフォルトのサーバーログは `$MACHBASE_HOME/trc/machbase.trc` です。実際のパスとローテーション設定は、
`V$PROPERTY` とインストール設定で確認します。

```bash
tail -100 "$MACHBASE_HOME/trc/machbase.trc"
rg -n 'ERR-|ERROR|WARN' "$MACHBASE_HOME/trc/machbase.trc"
```

ログレベルやファイル数を変える前に、現在の `TRACE_LOG_LEVEL`、`TRACE_LOGFILE_SIZE`、
`TRACE_LOGFILE_COUNT`、`TRACE_LOGFILE_PATH` を確認します。障害時の過剰な詳細ログはディスクと性能に影響します。

<a id="cause-lookup-error-codes"></a>

## エラーコードによる原因特定

正確なコードを記録し、[エラーコードリファレンス](/dbms/reference/error-codes/)で現行の定義を確認してください。
一覧にない場合は、全文、サーバービルド、再現 SQL、ログ時刻をまとめて収集します。
