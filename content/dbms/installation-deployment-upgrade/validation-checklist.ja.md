---
type: docs
title: '3.5 インストール検証チェックリスト'
weight: 50
toc: true
---

インストール検証はプロセスの生存確認だけでは完了しません。正しいバージョンと設定のサーバーに
実際のクライアントが接続し、権限の範囲内でデータを書き込み・検索できる必要があります。
以下をサーバー状態 → 接続 → バージョン・ライセンス → SQL → Clusterのレプリケーションの順に確認します。

各結果に実行ホスト、インストールホーム、接続先アドレス・ポート、時刻、エラーを記録します。
アップグレードの場合は変更前の記録と比較してください。`SYS`/`MANAGER`は初期実習の接続例であり、
実際のアカウントに置き換えます。実習テーブル名が既存業務オブジェクトと重複しないことも先に確認します。

## Standard Editionのチェックリスト

### 1. サーバープロセスの確認

```bash
machadmin -e
# Machbase server is running with PID(<pid>).
```

プロセスを直接確認することもできますが、別のインストールホームで実行されたサーバーと区別する必要があります。
`MACHBASE_HOME`が検査対象インスタンスを指すことを確認します。

```bash
ps -ef | grep machbased | grep -v grep
```

### 2. ポートのリスニング確認

```bash
ss -tlnp | grep 5656
# LISTEN 0 128 0.0.0.0:5656 ...
```

現在のOSに合うポート確認ツールを使用します。例の`5656`は実際のSQLポートに置き換え、受信アドレスが
意図したインターフェースか確認します。リスナー確認とリモートクライアントの接続成功は別の検査のため、
アプリケーションを実行するホストでも接続を試します。

### 3. machsqlの接続テスト

```bash
machsql -s 127.0.0.1 -P 5656 -u SYS -p MANAGER
# MACHBASE_CONNECT_MODE=INET, PORT=5656 EDITION=STANDARD
# Mach>
```

ローカル接続が成功してリモート接続だけ失敗する場合は、アドレス・ポート、リスナー設定、ファイアウォールを
確認します。認証エラーはユーザー名・認証方式・有効期限を確認し、接続成功後のオブジェクトアクセスエラーは
現在のデータベースとSQL権限を別途確認します。

### 4. バージョンの確認

```sql
SELECT * FROM V$VERSION;
SELECT CURRENT_DATABASE();
```

### 5. ライセンスの確認

```sql
SELECT ID, ISSUE_DATE, TYPE, VIOLATE_STATUS FROM V$LICENSE_INFO;
```

`VIOLATE_STATUS`が0か確認し、インストールしたライセンスの種類・期間が運用計画に合うか確認します。
違反状態の場合は`VIOLATE_MSG`とサーバーログで原因を確認します。

### 6. 基本クエリのテスト

```sql
CREATE LOG TABLE check_test (id INTEGER, ts DATETIME);
INSERT INTO check_test (id, ts) VALUES (1, NOW);
SELECT id, ts FROM check_test;
DROP TABLE check_test;
```

入力した`id=1`の1行と時刻が返り、DROPが成功することを確認します。この検査は基本的なLOG入力経路だけを
確認します。実際のサービスでTAG・TRANSACTION・Appendなどを使用する場合は、該当テーブルとSDKでも
代表的な入力・検索を実行します。

## Cluster Editionの追加チェックリスト

### 7. クラスターノードの状態確認

```bash
machcoordinatoradmin --cluster-status
# デプロイ記録のノード数と役割別状態を比較
```

### 8. Brokerの接続テスト

```bash
machsql -s 192.168.1.11 -P 5656 -u SYS -p MANAGER
```

```sql
SELECT * FROM V$NODE_STATUS;
```

Coordinatorの`primary`、Brokerの`leader`、Warehouseのレプリケーション状態など、正常状態の表示は
役割ごとに異なります。全ノードを単一の文字列と比較せず、目標状態と実際の状態、グループ構成、アドレスが
デプロイ記録と合うか確認します。

### 9. データレプリケーションの確認

まずBroker経由の入力・検索を確認し、次にWarehouseグループのレプリケーション状態を確認します。
Brokerで1行が検索できるだけでは、全レプリカの同期を証明できません。

```sql
-- Broker経由でデータを入力
CREATE LOG TABLE cluster_check_test (id INTEGER, ts DATETIME);
INSERT INTO cluster_check_test (id, ts) VALUES (1, NOW);

-- Brokerで入力結果を確認
SELECT COUNT(*) FROM cluster_check_test;
```

Warehouseへの直接SQL接続は通常のアプリケーション経路ではなく、レプリケーション診断用の管理手順です。
`machcoordinatoradmin --cluster-status`で同じレプリケーショングループのactive・standbyピアを確認し、
必要な場合のみ各ピアのネイティブポートへ管理アカウントで接続して同じ検索結果を比較します。
異なるWarehouseグループの全ノードが同じ行を持つとは考えないでください。

検証後はBroker接続でテーブルを削除します。

```sql
DROP TABLE cluster_check_test;
```

---

<a id="문제-발생-시"></a>

## 完了基準と問題発生時の対応

サーバー・接続・権限・代表SQLと必要なレプリケーション検査がすべて通れば、サービスの引き継ぎを進めます。
永続性の検証が必要な場合は、専用の検証環境にデータを残し、正常な再起動の前後で結果を比較します。
業務データのあるサーバーを、単純なインストール確認のために再初期化しないでください。

失敗時は最初のエラーと関連ログを保持し、失敗した段階から原因を絞り込みます。

- サーバーログ: `$MACHBASE_HOME/trc/machbase.trc`
- [運用・障害診断](/dbms/operations-configuration-recovery/diagnosis-observability/)を参照
