---
type: docs
title: '1.2 10分クイックスタート'
weight: 20
toc: true
---

稼働中のサーバーに接続し、サービス開始イベントを1件保存して読み出します。
追記型のイベントに適した LOG テーブルを使用し、SQL の実行結果と2つの時刻列の意味を確認します。
インストール時間は、この演習の所要時間に含みません。

## 前提条件

- Machbase DBMS サーバーが `127.0.0.1:5656` で稼働していること。
- `machsql` コマンドを使用できること。
- テーブルの作成・入力・検索・削除権限を持つ演習用アカウントで接続できること。
- 以下は初期演習用アカウント `SYS` とパスワード `MANAGER` を使用します。
  変更済みの場合は実際のパスワードに置き換えてください。
- `/tmp` に SQL ファイルを保存でき、演習用の名前 `DBMS_GS_QUICK` を使用できること。

既存の業務テーブルと名前が重ならない演習環境を使用します。最後の `DROP TABLE` は、
演習用テーブルと入力したデータを削除します。

サーバーが未準備の場合は、[インストール・デプロイ・アップグレード](/dbms/installation-deployment-upgrade/)と
[Linux Standard Edition のインストール](/dbms/installation-deployment-upgrade/standard-edition/#linux)を
先に参照してください。

## 実行例

サービス開始イベントを1件 LOG テーブルに記録します。`CREATE LOG TABLE` でタイプを明示して作成すると、
`_arrival_time` 列が自動的に追加されます。

次のコマンドで SQL ファイルを保存し、実行します。

```bash
cat > /tmp/dbms_gs_quick.sql <<'SQL'
CREATE LOG TABLE DBMS_GS_QUICK (
  EVENT_ID INTEGER,
  EVENT_TIME DATETIME,
  LEVEL VARCHAR(10),
  MESSAGE VARCHAR(40)
);

INSERT INTO DBMS_GS_QUICK (EVENT_ID, EVENT_TIME, LEVEL, MESSAGE)
VALUES (
  1,
  TO_DATE('2026-07-02 09:00:00', 'YYYY-MM-DD HH24:MI:SS'),
  'INFO',
  'service started'
);

SELECT _arrival_time, EVENT_ID, EVENT_TIME, LEVEL, MESSAGE
FROM DBMS_GS_QUICK
ORDER BY EVENT_ID;

DROP TABLE DBMS_GS_QUICK;
SQL

machsql -s 127.0.0.1 -P 5656 -u SYS -p MANAGER -f /tmp/dbms_gs_quick.sql
```

### 結果の確認

各 SQL ステップでエラーがないことを確認します。SELECT 結果は1行で、`EVENT_ID` が `1`、
`LEVEL` が `INFO`、`MESSAGE` が `service started` である必要があります。
`EVENT_TIME` はアプリケーションが保存したイベントの実際の発生時刻、`_arrival_time` は
この例で DBMS が自動記録したサーバー受信時刻です。実行のたびに `_arrival_time` は変わり、
`EVENT_TIME` と一致する必要はありません。

`CREATE LOG TABLE` は構造を作成し、`INSERT` は1行を追加します。`SELECT` は読み出す列、
`ORDER BY EVENT_ID` は結果の順序を指定します。最後の `DROP TABLE` まで成功すると、
演習用テーブルは削除されます。データをさらに調べる場合は、実行前に最後の DROP 文を除き、
検索が終わってからその演習用テーブルだけを削除します。

再実行時に `DBMS_GS_QUICK` がすでに存在するエラーが出る場合、前の実行が `DROP TABLE`
まで進まなかった可能性があります。`DESC DBMS_GS_QUICK;` で構造を確認し、前の演習で作成した
テーブルである場合に限り `DROP TABLE DBMS_GS_QUICK;` を実行して再試行します。
接続エラーの場合は、まずサーバーアドレス、ポート、起動状態、アカウント情報を確認します。

## この例で確認したこと

| 項目 | 確認内容 |
| --- | --- |
| サーバー接続 | `machsql` で `127.0.0.1:5656` に接続 |
| テーブル作成 | `CREATE LOG TABLE` で LOG テーブルを明示的に作成 |
| データ入力 | `INSERT` と `TO_DATE` でイベントを保存 |
| データ取得 | `SELECT` と `ORDER BY` で入力結果を確認 |
| 自動列 | LOG テーブルの `_arrival_time` をサーバーが自動記録 |
| 後片付け | `DROP TABLE` で演習用テーブルを削除 |
