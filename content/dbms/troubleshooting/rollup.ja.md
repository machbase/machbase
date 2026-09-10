---
type: docs
title: '15.7 ROLLUP の問題'
weight: 70
toc: true
aliases:
  - /dbms/tag-rollup-usage/constraints-errors-troubleshooting/rollup-troubleshooting/
---

ROLLUP の結果が遅れたり元データと異なったりする場合は、処理遅延と集計の意味の違いを区別します。
例の名前を実際の対象テーブル・ジョブへ置き換え、最初の対策として削除・再作成を行わないでください。

## 1. 状態と範囲の確認

```sql
SELECT ROLLUP_NAME, ROLLUP_TABLE, ROOT_TABLE, EXT_TYPE,
       INTERVAL_TIME, WAKEUP_INTERVAL, ENABLED, RUN_STATE, LAST_ELAPSED_MSEC
  FROM V$ROLLUP ORDER BY ROLLUP_NAME;
SHOW ROLLUPGAP;
```

SHOW ROLLUPGAP は machsql コマンドであり、SDK の SQL API へ送信しません。gap は RID の処理差で、
時間遅延や元データ補正の完了を直接表す値ではありません。各階層・Cluster ノードの状態、
サーバービルド、データベース、所有者を併せて記録します。

## 2. 同じデータセットを比較

| 症状 | 確認事項 |
|---|---|
| 一部サンプルがない | 条件付き ROLLUP 候補と元データのフィルターが一致するか |
| FIRST/LAST エラー | 選択された候補が EXTENSION か |
| 月・日クエリに候補がない | 保存間隔の選択規則とクエリバケットを混同していないか |
| 平均が異なる | NULL、有効件数、部分平均の再集計、タグ単位が同じか |
| 元データ修正後も値が変わらない | FORCE で過去に戻そうとしていないか、REBUILD の対象か |
| JSON 件数が異なる | 元文書、SQL NULL、パス別件数、文書集計件数を区別したか |

元データは DATE_TRUNC/DATE_BIN と GROUP BY、保存集計は rollup() で取得し、比較します。
タグ、時刻、origin、終了境界、集計関数を固定します。対応 ROLLUP がない場合に、
rollup() が元データのスキャンへ自動で切り替わるとは考えないでください。

## 3. 新しい入力への追従

対象ジョブが有効か確認し、必要なジョブを名前で指定します。

```sql
ALTER ROLLUP rollup_name FORCE;
SHOW ROLLUPGAP;
```

WAKEUP は起床させるだけで、FORCE は処理範囲に追いつくまで待ちます。停止中のジョブは状態を確認して
START し、複数階層は下位から処理します。`ALTER SYSTEM FLUSH ROLLUP` は非サポートなので
診断コマンドとして使用しないでください。

## 4. 過去データの補正と再構築

Standard Edition でも、すべての ROLLUP 構成が REBUILD 対象ではありません。完全な自動階層か、
Custom 間隔・バケットが対応するか、元データが残っているかを先に確認します。時間引数には
対応する定数文字列または TO_DATE を使います。指定時刻を含むバケット全体が再計算されます。

関連ジョブの停止・再起動と部分失敗を考慮します。成功・失敗の後も結果と実際の有効状態を確認し、
[REBUILD 演習](../../tag-rollup-usage/rollup-rebuild/)と
[引数の仕様](../../reference/sql/syntax/rollup-rebuild-syntax/)に従います。

## 5. サポート依頼の資料

- サーバービルド、Edition、クライアント、接続先
- TAG スキーマ、ROLLUP 定義、条件、依存関係
- 状態・gap と観測時刻
- 比較した元データ/ROLLUP SQL、タイムゾーン・origin、期待値・実測値
- 最初のエラーと直近の元データ補正・削除・大量入力・設定変更
