---
type: docs
title: '10.7 運用とデータライフサイクル'
weight: 70
toc: true
aliases:
  - /dbms/volatile-table-usage/memory-lifecycle/
  - /dbms/volatile-table-usage/restart-data-loss/
  - /dbms/volatile-table-usage/memory-monitoring-cache-rebuild/
---

VOLATILEテーブルの作成・ロード・使用・消失・再構築の手順を説明します。

<a id="operations-volatile-lifecycle"></a>
<a id="lifecycle-memory"></a>

## データライフサイクル

1. サーバー起動後にテーブル作成SQLを実行します。
2. 必要に応じて永続的な元データから初期データをロードします。
3. アプリケーションが検索と更新を開始します。
4. 保持が必要な結果を永続テーブルに記録します。
5. サーバーが終了するとデータが消失します。テーブル定義は残ります。

<a id="operations-volatile-session-scope"></a>

## セッション間の共有

VOLATILEテーブルはサーバー全体で共有されます。
あるセッションが入力した行を別のセッションから検索でき、接続を終了しただけではデータは消失しません。

<a id="operations-volatile-flush"></a>

## 永続データとの境界

VOLATILEには、元データから再作成できる最新状態や中間結果だけを格納します。
監査記録、元のイベント、復旧できない結果は、TAG、LOG、LOOKUPまたはTRANSACTIONテーブルに保存します。
コピーSQLは、コピー元とコピー先の列、重複処理、実行周期を含む独立したジョブとして管理します。

<a id="operations-volatile-restart"></a>
<a id="data-loss"></a>

## 再起動の手順

- テーブルの存在を確認します。再起動だけでは定義は消失しないため、通常は再作成しません。
- 永続的な元データがある場合は、定義した基準時点のデータだけをロードします。
- 想定行数と最新時刻を確認します。
- 検証後に、収集クライアントとアプリケーションの書き込みを再開します。
- 再構築に失敗した場合は、空のキャッシュでサービスが安全に動作するか確認します。

<a id="operations-volatile-checklist"></a>

## 運用チェックリスト

- 初期ロードSQLをバージョン管理します。初回構築用の作成SQLも保存します。
- 本番アカウントと実際の接続情報で、スクリプトを事前検証します。
- 行数とメモリ上限を監視します。
- 保持が必要なデータがVOLATILEだけに残っていないか確認します。
- 再起動訓練でロードと検証の順序を確認します。

## メモリ確認とキャッシュの再構築

```sql
SELECT * FROM V$STORAGE_DC_VOLATILE_TABLE;
SELECT * FROM V$SYSMEM;
SELECT * FROM V$SESMEM;

SELECT NAME, VALUE
  FROM V$PROPERTY
 WHERE NAME = 'VOLATILE_TABLESPACE_MEMORY_MAX_SIZE';
```

特定の内部列名に依存せず、導入バージョンのビュー定義を確認してください。
キャッシュの再作成では行数とサンプル値を記録し、利用処理を切り替えてから、テーブル作成・初期ロード・検証の順に進めます。
失敗時には空のキャッシュでも安全に動作する必要があります。
