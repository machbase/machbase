---
type: docs
title: '3.4 アップグレード'
weight: 40
toc: true
---
アップグレードは実行ファイルの交換だけでなく、既存のデータ、設定、アプリケーションが新バージョンで
同じ意味で動作するかを確認する作業です。まず対応するバージョン間の経路を確認し、復元可能なバックアップと
サービス再開基準を準備します。以下の8.7.0パッケージ名とパスは、提供された実際の配布物に合わせます。

## アップグレード前の確認事項

- 現在と対象のバージョンの互換性を確認します。マイナーバージョンが異なるとDBファイル形式が変わる場合があります。
- アップグレード前にバックアップします。[バックアップ方法](/dbms/operations-configuration-recovery/backup-restore-mount/#backup)を参照してください。
- 実行中のINSERT・APPENDクライアントを確認します。

<a id="upgrade-check-870"></a>

### 8.7.0アップグレードの事前確認

8.5から8.7.0にアップグレードする場合は、バイナリ交換前に次の依存関係を調査し、対応する方式へ移行します。

1. 廃止された`HTTP_AUTH`、`HTTP_ENABLE`、`HTTP_MAX_MEM`、`HTTP_PORT_NO`、`RS_CACHE_*`、
   `STREAM_THREAD_COUNT`、`STREAM_WAIT_MS`設定を現在のファイルで探し、サポート一覧と照合します。
   廃止設定は削除し、継続設定は保持します。特にClusterの`HTTP_ADMIN_PORT`は現行の管理ポートのため、
   `HTTP_*`という理由で一緒に削除しないでください。
2. `/machbase`、`/machiot`を呼ぶアプリケーションは、対応SDKを使用するバックエンドへ移行します。
3. `STREAM_*`プロシージャと`FLUSH RESULT_CACHE`を実行するSQL・運用スクリプトを変更します。
4. `machcli.h`と`MachCLI*()`を使用するC/C++アプリケーションをMachbase SQLCLIまたはODBCに移行します。
   SQLCLIとODBCは異なるAPI集合です。
5. WebAdmin/MWAに依存する運用手順・ダッシュボードは、コマンドラインツールまたは別アプリケーションへ移行します。

全廃止項目と継続機能は
[バージョンと互換性](/dbms/reference/support-scope-constraints/compatibility-version/#removed-features-870)を参照してください。

## アップグレード経路

| Edition | 方式 | リンク |
|--------|------|------|
| Standard Edition | サーバー終了後にパッケージを交換 | [Standard Editionのアップグレード](/dbms/installation-deployment-upgrade/upgrade/#standard-edition) |
| Cluster Edition | Broker/Warehouseを順次アップグレード | [オンラインアップグレード](/dbms/installation-deployment-upgrade/upgrade/#cluster-edition-online) |
| Cluster Edition | 全体停止 | [全体停止アップグレード](/dbms/installation-deployment-upgrade/upgrade/#cluster-edition-full-stop) |

Cluster Editionではデータ可用性の要件に応じてオンライン方式または全体停止方式を選びます。

---

<a id="standard-edition"></a>

## Standard Editionのアップグレード

サーバーを終了し、パッケージを交換して再起動します。物理DBファイルをそのまま開くことがサポートされる
バージョン間経路だけに適用します。データ変換やエクスポート・インポートが必要な経路は、
該当リリースの移行手順を先に実行します。

### アップグレード前の準備

1. **バックアップ**: 対応するBACKUPコマンドでバックアップを作成し、別環境で復元可能か確認します。
   実行中のデータディレクトリを単純にコピーしただけで復旧可能なバックアップを確保したとは判断しません。

2. **クライアント接続の終了**: 実行中のAppendまたはINSERTをすべて完了します。

3. **現在のバージョン確認**:
   ```bash
   machbased -v
   ```

### アップグレード手順

#### 1. サーバーの終了

```bash
machadmin -s
# Machbase server shut down successfully.
```

<a id="2-기존-패키지-백업-선택"></a>

#### 2. 既存パッケージと設定の保管

実行ファイルとライブラリだけでなく、現在の設定とライセンスも別の場所に保管します。
以下のパスに以前のバックアップがないことを確認して実行します。

```bash
cp -a "$MACHBASE_HOME/bin" "$MACHBASE_HOME/bin.bak"
cp -a "$MACHBASE_HOME/lib" "$MACHBASE_HOME/lib.bak"
cp -a "$MACHBASE_HOME/conf" "$MACHBASE_HOME/conf.bak"
```

**データディレクトリ（`dbs/`）と別途指定した`DBS_PATH`は保持します。** 上記のコピーは実行ファイルと
設定の保管であり、DBバックアップの代わりにはなりません。新バージョンがデータを変更した後に旧実行ファイルを
戻すだけで復旧できるとは考えず、検証済みのバックアップ復元経路を使用します。

#### 3. 新パッケージの展開

新パッケージは別の作業ディレクトリに展開し、構成と設定の変更点を先に確認します。

```bash
upgrade_stage=$(mktemp -d)
tar zxf machbase-SDK-8.7.0.official-LINUX-X86-64-release.tgz -C "$upgrade_stage"
```

展開だけでは既存インストールの実行ファイルは変わりません。以下は`bin/`、`lib/`、`include/`を含む
Standard tarballから実行ファイル・ライブラリ・ヘッダーを反映する例です。先にサーバー終了を確認し、
コマンドが失敗した場合は次の起動段階に進まないでください。

```bash
(
  set -e
  test -n "$MACHBASE_HOME"
  test -x "$upgrade_stage/bin/machbased"
  test -d "$upgrade_stage/lib"
  test -d "$upgrade_stage/include"
  test -d "$MACHBASE_HOME/bin"
  test -d "$MACHBASE_HOME/lib"
  test -d "$MACHBASE_HOME/include"
  cp -a "$upgrade_stage/bin/." "$MACHBASE_HOME/bin/"
  cp -a "$upgrade_stage/lib/." "$MACHBASE_HOME/lib/"
  cp -a "$upgrade_stage/include/." "$MACHBASE_HOME/include/"
  "$MACHBASE_HOME/bin/machbased" -v
)
```

既存の`conf/machbase.conf`、ライセンス、実際の`DBS_PATH`のデータは保持し、新設定項目を既存設定に
マージします。コピーは同名の配布ファイルを交換しますが、旧バージョンにしかないファイルは自動削除しません。
SDKやプラグインは新バージョンに合うファイルを明示的に選び、追加の交換対象と削除項目はリリース情報で確認します。
出力されたバイナリバージョンと設定の確認が完了してからサーバーを起動します。

#### 4. サーバーの起動

```bash
machadmin -u
# Machbase server started successfully.
```

#### 5. バージョンの確認

```bash
machbased -v

# サーバーへ接続
machsql -s 127.0.0.1 -P 5656 -u SYS -p MANAGER
```

```sql
SELECT EDITION, BINARY_DB_MAJOR_VERSION, BINARY_DB_MINOR_VERSION FROM V$VERSION;
```

### 注意事項

- `dbs/`ディレクトリを削除・初期化（`machadmin -d`）しないでください。
- マイナーバージョン間のアップグレードではDBファイルの移行が必要な場合があります。必ずリリースノートを確認してください。
- Windowsでは新パッケージまたはインストーラー適用前にMachbaseサービスを停止します。

---

<a id="cluster-edition"></a>

## Cluster Editionのアップグレード

サービス停止の可否に応じて2つの方式から選びます。

| 方式 | サービス停止 | 適している状況 |
|------|-----------|------------|
| [オンラインアップグレード](/dbms/installation-deployment-upgrade/upgrade/#cluster-edition-online) | Broker/Warehouseを順次再起動 | BrokerとWarehouseだけを交換する本番環境 |
| [全体停止アップグレード](/dbms/installation-deployment-upgrade/upgrade/#cluster-edition-full-stop) | あり | メンテナンス時間帯を確保できる場合、メジャーバージョン変更 |

### 共通の事前注意事項

- アップグレード中はDDLまたはDELETEを実行しないでください。
- アップグレード中にノードの追加・起動・終了・削除を並行して行わないでください。
- オンラインアップグレードはBrokerとWarehouseが対象です。Coordinator、Deployer、Lookupも交換する場合は全体停止方式を使用します。
- アップグレード前のバックアップを推奨します。

---

<a id="cluster-edition-online"></a>

### オンラインアップグレード

稼働中のクラスターでBrokerとWarehouseを順次アップグレードします。Coordinator、Deployer、Lookupを
含む全バイナリの交換が必要な場合は
[全体停止アップグレード](/dbms/installation-deployment-upgrade/upgrade/#cluster-edition-full-stop)を使用します。

#### アップグレード手順

##### 1. cluster.yamlのパッケージ変更

`cluster.package.name`と`cluster.package.origin_path`を新パッケージに変更します。
パッケージ内容が変わる場合は、パッケージ名とアーカイブ名も一意な新しい名前に変更します。

```yaml
cluster:
  package:
    name: machbase-v8.7.0
    origin_path: /home/machbase/packages/machbase-cluster-8.7.0.official-LINUX-X86-64-release.tgz
```

`registered_path`は`machclusterctl export`が記録するCoordinatorのパッケージ保存先パスです。
アップグレードするアーカイブの指定には`origin_path`を使用します。

##### 2. 実行計画の確認

```bash
machclusterctl upgrade -f cluster.yaml --online --dry-run --verbose
```

##### 3. オンラインアップグレードの実行

```bash
machclusterctl upgrade -f cluster.yaml --online --yes --verbose
```

`--online`を省略してもオンラインモードになりますが、運用手順を明確にするため明示を推奨します。

##### 4. 全体状態の確認

```bash
machclusterctl status
```

#### 手動アップグレードの補足

`machcoordinatoradmin --upgrade-node`を直接使用する場合は、対象ノードとパッケージ名をともに指定します。

```bash
machcoordinatoradmin --upgrade-node=192.168.1.11:5401 --package-name=machbase-v8.7.0
```

オンラインの対象はBrokerとWarehouseに限定します。Brokerが1台しか残っていないときにそのBrokerを
アップグレードすると、その間クライアント接続が切れる場合があります。

オンラインモードはクラスター全体の停止を省略する方式であり、無停止を保証するHA対応のローリング
アップグレードではありません。Warehouseグループが一時的に読み取り専用になる場合があるため、
アプリケーションの再接続・再試行と書き込み遅延を検証する必要があります。プロトコル互換性が変わる場合や、
全役割のバイナリを合わせる必要がある場合は全体停止方式を使用します。

全対象ノードの役割状態とバージョンを確認してから、代表的な検索・入力とレプリケーション状態まで検証します。

---

<a id="cluster-edition-full-stop"></a>

### 全体停止アップグレード

クラスターを完全に終了し、全ノードを一括アップグレードします。Coordinator、Deployer、Lookupを含む
全バイナリの交換が必要な場合や、DBファイル形式の変更を伴う場合に使用します。

#### アップグレード手順

##### 1. クライアント接続の終了

全INSERT・APPEND・SELECT操作が完了したことを確認します。

##### 2. cluster.yamlのパッケージ変更

`cluster.package.name`と`cluster.package.origin_path`を新パッケージに変更します。
アップグレード前にノード追加・削除・ポート変更などのトポロジー変更を残してはいけません。
変更がある場合は先に`apply`で反映してからアップグレードします。

`machclusterctl upgrade --full-stop`はCoordinatorとDeployerを含む全ノードホームに同じパッケージを
交換反映します。そのため`origin_path`には`machcoordinatoradmin`と`machdeployeradmin`を含む
完全なClusterパッケージを指定します。

##### 3. 実行計画の確認

```bash
machclusterctl upgrade -f cluster.yaml --full-stop --dry-run --verbose
```

##### 4. 全体停止アップグレードの実行

```bash
machclusterctl upgrade -f cluster.yaml --full-stop --yes --verbose
```

`machclusterctl`はクラスター全体の停止を前提に、パッケージを一時準備パスへ展開してから
ノードホームへ交換反映します。

#### 手動デプロイの補足

手動デプロイ環境で直接交換する場合は、Coordinatorに新パッケージを登録します。

```bash
machcoordinatoradmin --add-package=machbase-v8.7.0 \
  --file-name=/home/machbase/packages/machbase-cluster-8.7.0.official-LINUX-X86-64-release.tgz
```

Warehouse → Broker → Lookup → Deployer → Coordinatorの順で終了します。

```bash
machcoordinatoradmin --shutdown-node=192.168.1.13:5501
machcoordinatoradmin --shutdown-node=192.168.1.14:5501
machcoordinatoradmin --shutdown-node=192.168.1.11:5401
machcoordinatoradmin --shutdown-node=192.168.1.10:5301
machdeployeradmin --shutdown
machcoordinatoradmin --shutdown
```

各ノードホームを新パッケージに交換する際は、既存の`conf/machbase.conf`、`dbs/`、`meta/`、`package/`を
保持します。別の作業パスに新パッケージを展開し、保持対象パスを除いて交換します。

Coordinator → Deployer → Lookup → Broker → Warehouseの順で起動します。

```bash
machcoordinatoradmin --startup
machdeployeradmin --startup
machcoordinatoradmin --startup-node=192.168.1.10:5301
machcoordinatoradmin --startup-node=192.168.1.11:5401
machcoordinatoradmin --startup-node=192.168.1.13:5501
machcoordinatoradmin --startup-node=192.168.1.14:5501
```

再起動後、BrokerとWarehouseのパッケージメタデータを新パッケージ名に同期します。

```bash
machcoordinatoradmin --upgrade-node=192.168.1.11:5401 --package-name=machbase-v8.7.0
machcoordinatoradmin --upgrade-node=192.168.1.13:5501 --package-name=machbase-v8.7.0
machcoordinatoradmin --upgrade-node=192.168.1.14:5501 --package-name=machbase-v8.7.0
```

##### 5. 状態の確認

```bash
machclusterctl status
```

ノード状態に加え、Broker接続、代表データの検索・入力、レプリケーション、ライセンス、設定値を確認してから
サービスを再開します。[インストール検証](../validation-checklist/)の結果を変更前の記録と比較し、
検証完了まで旧パッケージ・設定とバックアップを保持します。

#### 注意事項

- メジャーバージョンのアップグレードではDBファイル形式が変わる場合があります。必ずリリースノートを確認し、事前にバックアップしてください。
- `conf/machbase.conf`、`dbs/`、`meta/`、`package/`を削除・初期化しないでください。
