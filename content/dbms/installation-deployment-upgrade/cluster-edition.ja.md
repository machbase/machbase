---
type: docs
title: '3.3 Cluster Editionのインストールとデプロイ'
weight: 30
toc: true
---
Cluster EditionはSQL接続、データ保存、レプリケーション、ノード管理を複数の役割に分けます。
インストール前に各役割をどのホストへ配置するか、どのポートと保存パスを使うかを決めます。
通常のSQL接続はBrokerへ、運用コマンドは該当する管理ノードへ送る必要があります。

## ノードの役割

| ノード | 役割 |
|------|------|
| **Coordinator** | クラスターメタ情報の管理、ノード状態の監視 |
| **Deployer** | パッケージの配布とノード初期化の中継 |
| **Lookup** | 参照データと検索処理 |
| **Broker** | SQLの解析とクエリの分配、クライアントの接続先 |
| **Warehouse** | 実データの保存とクエリ実行 |

以下のYAML例は、3ホストにCoordinator 2台、Deployer 3台、Lookup 2台（master 1台、monitor 1台）、
Broker 2台、Warehouse 2台（1つのレプリケーショングループ）を配置します。
実際のノード数と配置は、可用性、スループット、障害時に残す必要がある容量に基づいて決めます。

## デプロイ方式

| 方式 | 説明 | 適している場合 |
|------|------|------------|
| [machclusterctl](/dbms/installation-deployment-upgrade/cluster-edition/#machclusterctl) | cluster.yamlによる自動デプロイ | 推奨。新規構築 |
| [手動（machcoordinatoradmin）](/dbms/installation-deployment-upgrade/cluster-edition/#manual-machcoordinatoradmin) | Coordinatorコマンドによるノード登録・デプロイ | 細かい制御が必要な場合 |

## インストール手順

1. [Cluster Editionの構成概要](/dbms/installation-deployment-upgrade/cluster-edition/#overview)を理解
2. [環境の準備](/dbms/installation-deployment-upgrade/cluster-edition/#preparation-environment-cluster-edition)（SSH鍵、カーネルパラメーター、NTP）
3. パッケージ・パスと[ライセンス](../pre-install-preparation/#license)の適用方式を準備
4. デプロイ方式を選択してインストール・起動し、ライセンスを確認
5. [インストール検証](/dbms/installation-deployment-upgrade/validation-checklist/)

---

<a id="overview"></a>

## Cluster Editionの構成概要

役割を分離したCoordinator、Deployer、Lookup、Broker、Warehouseノードで構成されます。
各ノードの役割と相互関係を理解してからデプロイ計画を立ててください。

### ノードの役割の詳細

#### Coordinator

クラスターメタデータ、ノード登録、状態監視を担当します。Primary/Secondaryによる冗長化を検討してください。
稼働中のデータ処理経路と管理経路は分かれていますが、Coordinator障害時に全SQLの継続動作が保証される
わけではありません。他ノードの状態とクライアントへの影響も確認し、検証済みの障害対応手順を使用します。

- 設定ファイル: `$MACHBASE_COORDINATOR_HOME/conf/machbase.conf`
- 管理ツール: `machcoordinatoradmin`
- 主なポート: `CLUSTER_LINK_PORT_NO`、`HTTP_ADMIN_PORT`

デフォルトは`CLUSTER_LINK_PORT_NO=3868`、`HTTP_ADMIN_PORT=5779`です。本章の例では運用中の
ポート競合を避けるため、Coordinatorのlink/adminポートに`5101`/`5102`を明示します。

#### Deployer

Coordinatorの指示に従い、各ノードへパッケージを配布して初期化を中継します。
各ノードホストに1台ずつ配置するか、専用のデプロイサーバーで運用します。

- 管理ツール: `machdeployeradmin`

#### Lookup

参照データと検索処理のためのノードです。構成に応じて`master`、`monitor`、`slave`の役割を指定します。

#### Broker

クライアントのSQL要求を受け取り、解析して適切なWarehouseへ分配します。通常のアプリケーションは
Brokerのアドレスに接続します。Warehouseへの直接接続はレプリケーション状態の比較など管理診断手順だけで
使用し、アプリケーションの接続経路と区別します。Brokerの冗長化を推奨します。

- クライアント接続ポート: デフォルト5656

#### Warehouse

実データを保存してクエリを実行します。同じグループのWarehouse間でデータを複製し、高可用性を提供します。
グループごとに2台以上を推奨します。

### 構成例

```
[クライアント]
     │ (SQL, 5656)
     ▼
[Broker ×2]  ──────────────────────────────────────────
     │ (クエリ分配)
     ├─► [Warehouse group1-node1] ◄──レプリケーション──► [Warehouse group1-node2]
     └─► [Warehouse group2-node1] ◄──レプリケーション──► [Warehouse group2-node2]

[Coordinator Primary] ◄──HA──► [Coordinator Secondary]
     │ (メタ情報管理、ノード監視)
[Deployer]
     │
[Lookup master / monitor]
```

### Editionの比較

Standard Editionとの詳細比較は
[Editionの違い](/dbms/core-concepts/concepts-edition/#differences-standard-edition-cluster)を参照してください。

---

<a id="preparation-environment-cluster-edition"></a>

## Cluster Editionのインストール環境の準備

デプロイ前に全ノードで次の環境を準備します。

### ファイルディスクリプターの上限

全ノードに次の設定を適用します。

```bash
sudo vi /etc/security/limits.conf
```

```
*  hard  nofile  65535
*  soft  nofile  65535
```

サーバー実行アカウントで新しいログインセッションを開き、確認します。サービスマネージャーから起動する場合は、
サービス自体のファイルディスクリプター上限も確認します。

```bash
ulimit -Sn
# 65535
```

### OSユーザーの作成

全ノードに`machbase`アカウントを作成します。

```bash
sudo useradd -m machbase --home-dir /home/machbase
sudo passwd machbase
```

### SSH鍵認証

`machclusterctl`を使用する場合は、デプロイサーバーから全ノードへパスワードなしでSSH接続できる必要があります。

```bash
# デプロイサーバーでSSH鍵を生成（既存なら省略）
ssh-keygen -t rsa -b 4096

# 各ノードに公開鍵を登録
ssh-copy-id machbase@192.168.1.11
```

登録後、パスワードなしで接続できるか確認します。

```bash
ssh machbase@192.168.1.11 'hostname'
```

### ネットワークのカーネルパラメーター

以下はネットワークバッファの調整例であり、全サーバーに適用する必須値ではありません。
現在のカーネル設定、メモリ使用量、ネットワークのボトルネックを先に測定します。値を増やした後は
スループットだけでなくメモリと遅延も比較し、効果を確認した項目だけを永続化します。

```bash
sudo sysctl -w net.core.rmem_default=33554432
sudo sysctl -w net.core.wmem_default=33554432
sudo sysctl -w net.core.rmem_max=268435456
sudo sysctl -w net.core.wmem_max=268435456
sudo sysctl -w 'net.ipv4.tcp_rmem=262144 33554432 268435456'
sudo sysctl -w 'net.ipv4.tcp_wmem=262144 33554432 268435456'
sudo sysctl -w 'net.ipv4.tcp_mem=8388608 8388608 8388608'
```

永続化するには`/etc/sysctl.conf`に追加します。

### 時刻同期（NTP）

全ノードのシステム時刻が一致する必要があります。NTPまたは`chrony`で同期してください。

```bash
# chronyの使用例
sudo systemctl enable chronyd
sudo systemctl start chronyd
chronyc tracking
```

タイムサーバーを使用できない隔離されたインストール環境では、初期時刻を直接設定できます。
次の値は書式例なので実際の現在時刻に置き換えてください。手動設定だけではノード間の時刻差を継続的に
補正できないため、本番投入前に時刻同期経路を用意します。

```bash
sudo date -s "2025-01-02 12:34:56"
```

### ポートの予約

各ノードでMachbaseが使用するポートを予約します。

```bash
current=$(cat /proc/sys/net/ipv4/ip_local_reserved_ports)
ports=5101-5110,5201-5202,5301-5302,5401,5500-5503,5656
sudo sysctl -w net.ipv4.ip_local_reserved_ports="${current:+$current,}$ports"
```

既存の予約ポートは上書きせず、カンマで区切って統合します。クラスター構成に応じてポート範囲を調整してください。
Cluster link、Coordinator/Deployerの管理、サービス、Warehouseのレプリケーション管理ポートなどを
すべて含める必要があります。

---

<a id="machclusterctl"></a>

## machclusterctlによるデプロイ

`machclusterctl`は1つの`cluster.yaml`でクラスター全体を自動デプロイ・管理するツールです。
SSHで各ノードにリモート接続し、パッケージ配布、初期化、起動・終了を一括処理します。

### 前提条件

- Primary Coordinatorをインストールするホストでコマンドを実行し、そのホストからパッケージと
  SSH秘密鍵を読み取れる必要があります。
- Primaryホストから全対象ホストへSSH鍵認証が設定されている必要があります。
- 各ノードの`home_path`と`dbs_path`の親パスに作成・書き込み権限が必要です。
- 別のライセンスが必要な場合は、自動起動前に配布パッケージとライセンス適用手順を準備します。
  YAMLに任意のライセンスプロパティは追加しません。
- [Cluster Editionのインストール環境の準備](/dbms/installation-deployment-upgrade/cluster-edition/#preparation-environment-cluster-edition)の完了

### 作業手順

| 段階 | ドキュメント |
|------|------|
| 1. cluster.yamlの作成 | [cluster.yamlの作成](/dbms/installation-deployment-upgrade/cluster-edition/#machclusterctl-cluster-yaml) |
| 2. YAMLの妥当性検査 | [YAMLの検証](/dbms/installation-deployment-upgrade/cluster-edition/#machclusterctl-validation-yaml) |
| 3. 初回インストールと起動 | [初回インストール](/dbms/installation-deployment-upgrade/cluster-edition/#machclusterctl-initial) |
| 4. 状態確認 | [初回インストールと状態確認](/dbms/installation-deployment-upgrade/cluster-edition/#machclusterctl-initial) |
| 5. 以降の構成変更 | [Cluster運用](/dbms/operations-configuration-recovery/cluster/) |
| 6. 障害時の復旧 | [Clusterのトラブルシューティング](/dbms/troubleshooting/cluster/) |

---

<a id="machclusterctl-cluster-yaml"></a>

### cluster.yamlの作成

`cluster.yaml`はインストールするノード構成とパスを宣言します。以下のアドレスは例のため実ホストに
置き換えます。`origin_path`はコマンドを実行するPrimary Coordinatorホストから読み取るアーカイブ、
`home_path`と`dbs_path`は該当ノードホスト上のパスです。`deployer`はそのノードを配置・制御する
Deployerを参照します。

#### ファイル構造の例

```yaml
version: "1"

cluster:
  name: mc-prod

  hosts:
    node1:
      address: machbase@192.168.1.10
    node2:
      address: machbase@192.168.1.11
    node3:
      address: machbase@192.168.1.12

  package:
    name: machbase
    origin_path: /home/machbase/packages/machbase-cluster-8.7.0.official-LINUX-X86-64-release.tgz

  ssh:
    key_file: /home/machbase/.ssh/id_rsa

  defaults:
    coordinator:
      home_path: /home/machbase/coordinator
      cluster_link_port: 5101
      http_admin_port: 5102
    deployer:
      home_path: /home/machbase/deployer
      cluster_link_port: 5201
      http_admin_port: 5202
    lookup:
      home_path: /home/machbase/lookup
      cluster_link_port: 5301
    broker:
      home_path: /home/machbase/broker
      cluster_link_port: 5401
      service_port: 5656
    warehouse:
      home_path: /home/machbase/warehouse
      cluster_link_port: 5501
      service_port: 5500

  coordinators:
    - alias: coord-primary-1
      host: node1
      role: primary

    - alias: coord-secondary-1
      host: node2
      role: secondary

  deployers:
    - alias: deployer-1
      host: node1

    - alias: deployer-2
      host: node2

    - alias: deployer-3
      host: node3

  lookup:
    - alias: lookup-master-1
      host: node1
      deployer: deployer-1
      type: master

    - alias: lookup-monitor-1
      host: node2
      deployer: deployer-2
      type: monitor

  brokers:
    - alias: broker-1
      host: node1
      deployer: deployer-1
      dbs_path: /data/machbase/broker-1/dbs

    - alias: broker-2
      host: node2
      deployer: deployer-2

  warehouse_groups:
    - name: group1
      nodes:
        - alias: warehouse-group1-1
          host: node2
          deployer: deployer-2
          dbs_path: /data/machbase/warehouse-group1-1/dbs

        - alias: warehouse-group1-2
          host: node3
          deployer: deployer-3
          dbs_path: /data/machbase/warehouse-group1-2/dbs
```

#### 主な項目の説明

| 項目 | 説明 |
|------|------|
| `version` | YAMLスキーマバージョン。現在は`"1"`を使用します。 |
| `cluster.name` | クラスター名。`destroy`の確認などで使用します。 |
| `cluster.hosts` | ノードから参照するホスト別名とSSH接続先。`address`は`user@host`形式です。 |
| `cluster.package.name` | Coordinatorへ登録するパッケージ名。 |
| `cluster.package.origin_path` | `install`、`apply`、`upgrade`の入力に使用するパッケージアーカイブのパス。 |
| `cluster.package.registered_path` | `export`が記録するCoordinatorのパッケージ保存先の観測パス。実行入力には使用しません。 |
| `cluster.ssh.key_file` | 対象サーバーへの接続に使用する秘密鍵パス。パスワードフィールドは使用しません。 |
| `cluster.defaults` | ノードタイプ別の`home_path`、`cluster_link_port`、`service_port`のデフォルト値。 |
| `cluster.coordinators` | Coordinatorノード一覧。`role`は`primary`または`secondary`。 |
| `cluster.deployers` | Deployerノード一覧。 |
| `cluster.lookup` | Lookupノード一覧。`type`は`master`、`monitor`、`slave`。 |
| `cluster.brokers` | Brokerノード一覧。クライアントSQL接続ポートは`service_port`。 |
| `cluster.warehouse_groups` | Warehouseグループとグループ別ノード一覧。 |

#### 推奨構成

- Coordinator: 2台（Primary + Secondary HA）
- Deployer: 1台以上
- Lookup: `master` 1台、`monitor` 1台以上
- Broker: 2台以上（負荷分散）
- Warehouseグループ: グループごとに2台（レプリケーションによる高可用性）

同じサーバーに同タイプのノードを2台以上配置する場合は、2台目以降の`home_path`とポートを明示し、
競合を避けます。

CoordinatorとDeployerの管理ポートには`http_admin_port`を使用します。

BrokerとWarehouseには任意で`dbs_path`を指定します。`dbs_path`はノードがインストールされるサーバーの
データファイルパスで、省略時は`machcoordinatoradmin --add-node`のデフォルト`DBS_PATH`動作に従います。

既存の`cluster.package.path`は後方互換入力として使用できますが、新しいYAMLでは`origin_path`を使用します。

`http_admin_port`はCoordinatorとDeployerだけに使用します。Broker、Lookup、Warehouseには
HTTPポートフィールドを指定しません。

作成後に妥当性を検査します。

---

<a id="machclusterctl-validation-yaml"></a>

### YAMLの検証

`cluster.yaml`を実際のインストールに使用する前に妥当性を検査します。`validate`はYAML構文、必須値、
別名、ポート競合、トポロジーの関係を静的に検査します。

#### 検証コマンド

```bash
machclusterctl validate -f cluster.yaml
```

#### 検証項目

| 項目 | 説明 |
|------|------|
| YAML構文 | ファイルの解析エラー |
| 環境変数の置換 | `${VAR}`または`${VAR:-default}`式を解釈できるか |
| 必須フィールド | クラスター名、ホスト、パッケージ、ノード別の必須値の欠落 |
| 別名 | ノード別名の重複 |
| ポート競合 | 同じホスト内の宣言ポートの競合 |
| トポロジー | Primary Coordinator、Lookup master/monitor、Deployerの参照関係 |

#### 出力例

```text
Validation passed.
```

エラーがあれば、メッセージの項目を修正して再検証します。

#### インストール前の実行計画確認

新規インストール前にSSH接続、パッケージの存在、リモートディレクトリ権限まで確認するには、
`install --dry-run --verbose`を使用します。

```bash
machclusterctl install -f cluster.yaml --dry-run --verbose
```

インストール後の構成変更を検証する場合は`apply --dry-run`を使用します。現在のクラスター状態とYAMLの
差を計算して実行計画を表示し、実際のリモート変更は行いません。

```bash
machclusterctl apply -f cluster.yaml --dry-run --verbose
```

#### 一般的なエラーと解決方法

| エラー | 原因 | 解決方法 |
|------|------|------|
| `field ... not found` | 非サポートのYAMLキー | 現行スキーマの`cluster.*`項目に修正 |
| `required field ...` | 必須値の欠落 | メッセージのフィールドを追加 |
| `duplicate alias` | ノード別名の重複 | 全ノードの別名を一意に変更 |
| `port conflict` | 同一ホストで同じポートを使用 | 競合ポートを別に指定。ホームパスだけの変更では解決しない |
| `deployer ... not found` | Lookup/Broker/Warehouseが存在しないDeployerを参照 | `deployer`値をDeployerの別名またはホスト:ポートに修正 |

---

<a id="machclusterctl-initial"></a>

### 初回インストール

`cluster.yaml`の作成と検証が完了したら、インストール計画を確認してクラスターをインストールします。

#### 1. クラスターのインストール

各ノードへのパッケージ配布と初期化の前に、実行計画と事前検査の結果を確認します。

```bash
machclusterctl install -f cluster.yaml --dry-run --verbose
```

問題がなければ実際にインストールします。

```bash
machclusterctl install -f cluster.yaml --yes --verbose
```

このコマンドは次の処理を自動実行します。

1. 各ノードへのパッケージコピーと展開
2. 各ノードの`machbase.conf`作成とポート設定
3. Coordinatorデータベースの初期化
4. ノード登録（Coordinatorに各ノードを追加）

#### 2. クラスターの起動

`install`はCoordinator、Deployer、Lookup、Broker、Warehouseを準備して起動します。
インストール後にクラスター全体を再起動する必要がある場合だけ、次のコマンドを使用します。

```bash
machclusterctl start
```

<a id="machclusterctl-status-check-state"></a>

#### 3. 状態確認

```bash
export MACHBASE_COORDINATOR_HOME=/home/machbase/coordinator
machclusterctl status
```

1台のサーバーで複数のCoordinatorホームを切り替えて確認する場合は、直接指定します。

```bash
machclusterctl status --coordinator /home/machbase/coordinator
```

出力は`machcoordinatoradmin --cluster-status-full --verbose`形式です。以下は出力列を示す一部の行の例で、
YAMLの全ノード一覧ではありません。CoordinatorとBrokerは`primary`、`leader`など役割別の状態を取るため、
全行が`normal`かではなく、登録ノード数と役割別の目標・実際の状態が一致するかを確認します。

```
+-------------+--------------------------------+--------------------------------+--------------------------------+-------------------------------+-------------+-----------------+----------+
|  Node Type  |           Node Name            |           Group Name           |           Group State          |    Desired & Actual State     |  RP State   | Disk(%) (00/00) | Ping(μs) |
+-------------+--------------------------------+--------------------------------+--------------------------------+-------------------------------+-------------+-----------------+----------+
| coordinator | coord-1(192.168.1.10:5101)     | Coordinator                    | normal                         | primary       | primary       | ----------- | --------------- |      214 |
| deployer    | deployer-1(192.168.1.10:5201)  | Deployer                       | normal                         | running       | running       | ----------- | --------------- |      100 |
| broker      | broker-1(192.168.1.11:5401)    | Broker                         | normal                         | leader        | leader        | ----------- | --------------- |      100 |
| warehouse   | wh-g1-1(192.168.1.13:5501)     | group1                         | normal                         | normal        | normal        | running     | 26.9            |      100 |
+-------------+--------------------------------+--------------------------------+--------------------------------+-------------------------------+-------------+-----------------+----------+
```

#### 4. クライアント接続テスト

BrokerノードのIPとポートに接続します。

```bash
machsql -s 192.168.1.11 -P 5656 -u SYS -p MANAGER
# Mach>
```

#### クラスターの終了

```bash
machclusterctl stop
```

---

<a id="cluster-post-install-operations"></a>

<a id="machclusterctl-configuration-change-alter"></a>
<a id="machclusterctl-failure-recovery"></a>

### インストール後の運用

初回インストールと接続検証後のノード構成変更、追加・削除、状態復旧は
[Cluster運用](../../operations-configuration-recovery/cluster/)に従います。障害原因の分類と
復旧判断は[Clusterのトラブルシューティング](../../troubleshooting/cluster/)を参照してください。

<a id="manual-machcoordinatoradmin"></a>

## machcoordinatoradminによる手動デプロイ

`machclusterctl`を使用できない場合はCoordinatorとDeployerを直接準備し、パッケージとノードを登録します。
自動デプロイ済みの環境で以下の作成コマンドを再実行しないでください。手動例はYAMLとは別構成です。
役割別に実行場所を変えてコマンドを実行します。

| ホスト | 役割 |
|---|---|
| `192.168.1.10` | Primary Coordinator、Deployer、Lookup master |
| `192.168.1.11` | Deployer、Lookup monitor、Broker |
| `192.168.1.13` | Deployer、Warehouse group1の最初のノード |
| `192.168.1.14` | Deployer、Warehouse group1のレプリカノード |
| `192.168.1.20` | 任意のSecondary Coordinator |

同一ホストの役割ごとにホームとポートを分けます。Deployerはデータ処理ノードをインストールする各ホストで
準備し、以下の`--deployer`アドレスも対象ホストに合わせます。

### 手動デプロイの手順

1. [パッケージの準備と登録](/dbms/installation-deployment-upgrade/cluster-edition/#manual-machcoordinatoradmin-package) — 完全パッケージのインストールと軽量パッケージの登録準備
2. [Coordinator / Deployerのインストール](/dbms/installation-deployment-upgrade/cluster-edition/#manual-machcoordinatoradmin-coordinator-deployer) — 主要な管理ノードを起動
3. [パッケージ登録](/dbms/installation-deployment-upgrade/cluster-edition/#manual-machcoordinatoradmin-package) — 稼働中のCoordinatorへ軽量パッケージを登録
4. [Lookup / Broker / Warehouseのインストール](/dbms/installation-deployment-upgrade/cluster-edition/#manual-machcoordinatoradmin-lookup-broker-warehouse) — データ処理ノードを登録・起動
5. [全体状態の確認](/dbms/installation-deployment-upgrade/cluster-edition/#manual-machcoordinatoradmin-lookup-broker-warehouse) — 登録・起動後の初回状態検証

### machclusterctlとの違い

| 項目 | machclusterctl | 手動デプロイ |
|------|---------------|----------|
| 設定方式 | cluster.yamlの単一ファイル | 各ノードのmachbase.confを直接編集 |
| パッケージ配布 | 自動リモートコピー | Coordinator/Deployerは直接インストール、Broker/WarehouseはDeployerが配布 |
| ノード登録 | 自動 | `machcoordinatoradmin --add-node`を手動実行 |
| 一括起動・終了 | `machclusterctl start/stop` | ノードごとに個別実行 |

手動デプロイは柔軟ですが、ミスの可能性も高くなります。新規構築には`machclusterctl`を推奨します。

---

<a id="manual-machcoordinatoradmin-package"></a>

### パッケージの準備と登録

Cluster Editionの手動デプロイでのパッケージ準備・登録手順です。CoordinatorとDeployerには完全パッケージを
インストールして環境変数を設定します。BrokerとWarehouse用の軽量パッケージはCoordinatorの起動後に登録します。

#### パッケージの種類

Cluster Editionには2種類のパッケージがあります。

| パッケージ | 対象ノード | 特徴 |
|--------|-----------|------|
| 完全パッケージ | Coordinator、Deployer | 全実行ファイルを含む |
| 軽量パッケージ（lightweight） | Broker、Warehouse | データ処理に必要なファイルだけを含み、小容量 |

ファイル名の例:

- 完全: `machbase-cluster-8.7.0.official-LINUX-X86-64-release.tgz`
- 軽量: `machbase-cluster-8.7.0.official-LINUX-X86-64-release-lightweight.tgz`

#### CoordinatorとDeployerへのパッケージ配布

完全パッケージをCoordinatorとDeployerノードにコピーして展開します。

##### Coordinatorノード

```bash
# Coordinatorノードで実行
mkdir -p /home/machbase/coordinator
scp machbase@package-host:/path/to/machbase-cluster-8.7.0.official-LINUX-X86-64-release.tgz /home/machbase/
tar zxf /home/machbase/machbase-cluster-8.7.0.official-LINUX-X86-64-release.tgz -C /home/machbase/coordinator
```

##### Deployerノード

```bash
mkdir -p /home/machbase/deployer
scp machbase@package-host:/path/to/machbase-cluster-8.7.0.official-LINUX-X86-64-release.tgz /home/machbase/
tar zxf /home/machbase/machbase-cluster-8.7.0.official-LINUX-X86-64-release.tgz -C /home/machbase/deployer
```

この段階ではBrokerとWarehouseへ軽量パッケージを直接展開しません。Coordinatorへ軽量パッケージを登録すると、
後で`--add-node`で指定したDeployerが対象ノードの`--home-path`へパッケージを配布します。

#### Coordinatorへのパッケージ登録

CoordinatorからBrokerとWarehouseを起動するには、Coordinatorへの軽量パッケージ登録が必要です。
CoordinatorとDeployerをインストールし、Coordinatorが稼働中の状態で次のコマンドを実行します。

```bash
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --add-package=machbase \
  --file-name="/home/machbase/machbase-cluster-8.7.0.official-LINUX-X86-64-release-lightweight.tgz"
```

登録したパッケージは、後でBrokerとWarehouseを`--add-node`で登録する際に`--package-name=machbase`で
参照します。

#### 環境変数の設定

`package-host`と`/path/to/`は実際のパッケージ保存場所に置き換えます。CoordinatorとDeployerを同じホストで
管理する場合も、別々のシェルで役割に合う環境を使用します。以下は各シェルに適用する値で、サービスや
ログイン初期化ファイルにも同じ値を反映します。

```bash
# Coordinatorノード
export MACHBASE_COORDINATOR_HOME=/home/machbase/coordinator
export MACHBASE_HOME=$MACHBASE_COORDINATOR_HOME
export PATH=$MACHBASE_HOME/bin:$PATH
export LD_LIBRARY_PATH=$MACHBASE_HOME/lib:$LD_LIBRARY_PATH
```

```bash
# 別のDeployer管理シェル
export MACHBASE_DEPLOYER_HOME=/home/machbase/deployer
export MACHBASE_HOME=$MACHBASE_DEPLOYER_HOME
export PATH="$MACHBASE_HOME/bin:$PATH"
export LD_LIBRARY_PATH="$MACHBASE_HOME/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
```

---

<a id="manual-machcoordinatoradmin-coordinator-deployer"></a>

### Coordinator / Deployerのインストール

パッケージ配布後、Coordinatorを先にインストール・起動してからDeployerを登録します。

#### Coordinatorのインストール

##### 1. machbase.confの設定

`$MACHBASE_COORDINATOR_HOME/conf/machbase.conf`を編集します。

```bash
vi $MACHBASE_COORDINATOR_HOME/conf/machbase.conf
```

主な設定:

```
CLUSTER_LINK_HOST    = 192.168.1.10   # このノードのIP
CLUSTER_LINK_PORT_NO = 5101
HTTP_ADMIN_PORT      = 5102
```

##### 2. メタデータベースの作成とサービス起動

```bash
machcoordinatoradmin -c
machcoordinatoradmin -u
```

##### 3. 自身をCoordinatorノードとして登録

```bash
machcoordinatoradmin --add-node="192.168.1.10:5101" \
  --node-type=coordinator \
  --http-admin-port=5102
```

##### 4. 登録の確認

```bash
machcoordinatoradmin --cluster-status
```

#### Secondary Coordinatorのインストール（任意）

高可用性のためSecondary Coordinatorを追加します。

Secondaryノードにパッケージを配布して`machbase.conf`を設定し、先に**Primary Coordinatorで**ノードを
登録します。

```bash
# Primary Coordinatorで先に登録
machcoordinatoradmin --add-node="192.168.1.20:5101" \
  --node-type=coordinator \
  --http-admin-port=5102

# 次にSecondaryノードで起動（--primaryでPrimaryを指定）
machcoordinatoradmin -u --primary=192.168.1.10:5101
```

Secondaryの起動前に、必ずPrimaryでノード登録を完了する必要があります。

#### Deployerのインストール

手動構成表の各Deployerホストでこの手順を行います。以下の設定の`CLUSTER_LINK_HOST`は、そのホスト自身の
IPに置き換えます。他ホストのアドレスをそのままコピーすると、ノードの通信アドレスと実際の実行場所が
異なってしまいます。

##### 1. machbase.confの設定

```
CLUSTER_LINK_HOST    = 192.168.1.10   # DeployerノードのIP
CLUSTER_LINK_PORT_NO = 5201
HTTP_ADMIN_PORT      = 5202
```

##### 2. 起動

```bash
machdeployeradmin -c
machdeployeradmin -u
```

##### 3. CoordinatorへのDeployerノード登録

全Deployerが起動したら、Primary Coordinatorの管理シェルで登録します。

```bash
machcoordinatoradmin --add-node="192.168.1.10:5201" \
  --node-type=deployer \
  --http-admin-port=5202

machcoordinatoradmin --add-node="192.168.1.11:5201" \
  --node-type=deployer --http-admin-port=5202
machcoordinatoradmin --add-node="192.168.1.13:5201" \
  --node-type=deployer --http-admin-port=5202
machcoordinatoradmin --add-node="192.168.1.14:5201" \
  --node-type=deployer --http-admin-port=5202
```

---

<a id="manual-machcoordinatoradmin-lookup-broker-warehouse"></a>

### Lookup / Broker / Warehouseのインストール

CoordinatorとDeployerの準備後、Lookup、Broker、WarehouseをCoordinatorに登録して起動します。
BrokerとWarehouseの登録前に、軽量パッケージをCoordinatorへ`--add-package`で登録する必要があります。

<a id="lookup-노드-선택"></a>

#### Lookupノード

Lookup masterとmonitorをそれぞれ登録して起動します。次の例はPrimaryホストとBrokerホストへ配置し、
各ホストのDeployerを使用します。同じホームが既存のLookupで使用中でないことを確認します。

```bash
machcoordinatoradmin --add-node="192.168.1.10:5301" \
  --node-type=lookup \
  --lookup-type=master \
  --deployer="192.168.1.10:5201" \
  --home-path="/home/machbase/lookup"

machcoordinatoradmin --add-node="192.168.1.11:5301" \
  --node-type=lookup \
  --lookup-type=monitor \
  --deployer="192.168.1.11:5201" \
  --home-path="/home/machbase/lookup"

machcoordinatoradmin --startup-node="192.168.1.10:5301"
machcoordinatoradmin --startup-node="192.168.1.11:5301"
```


#### Brokerのインストール

##### 1. 登録パラメーターの確認

Broker設定ファイルは`--add-node`時に生成され、Deployer経由で対象ノードへ配布されます。
登録前にクラスター通信ポートとサービスポートを確定します。BrokerにHTTP管理ポートは指定しません。

```
CLUSTER_LINK_HOST    = 192.168.1.11   # BrokerノードのIP
CLUSTER_LINK_PORT_NO = 5401
PORT_NO              = 5656           # クライアント 接続ポート
```

##### 2. Coordinatorへのノード登録

Coordinatorノードで実行します。

```bash
machcoordinatoradmin --add-node="192.168.1.11:5401" \
  --node-type=broker \
  --deployer="192.168.1.11:5201" \
  --package-name=machbase \
  --home-path="/home/machbase/broker" \
  --dbs-path="/data/machbase/broker_dbs" \
  --port-no=5656
```

| パラメーター | 説明 |
|---------|------|
| `--add-node` | 登録するノードのIP:CLUSTER_LINK_PORT_NO |
| `--node-type` | `broker` / `warehouse` / `lookup` |
| `--deployer` | そのノードをインストール・制御するDeployerのIP:CLUSTER_LINK_PORT_NO |
| `--package-name` | Coordinatorに登録したパッケージ名 |
| `--home-path` | ノードのホームディレクトリ |
| `--dbs-path` | Broker/Warehouseのデータファイルパス。省略時はデフォルト`DBS_PATH` |
| `--port-no` | クライアントまたはノードのサービスポート |
| `--replication` | Warehouseのレプリケーション管理アドレス。`host:port`形式 |

##### 3. ノードの起動

Coordinatorで該当ノードを起動します。

```bash
machcoordinatoradmin --startup-node="192.168.1.11:5401"
```

#### Warehouseのインストール

Warehouseノードはグループ単位で構成します。同じグループ内のノード間でデータを複製します。

##### 1. 登録パラメーターの確認

Warehouse設定ファイルは`--add-node`時に生成され、Deployer経由で対象ノードへ配布されます。
登録前にクラスター通信ポート、サービスポート、レプリケーション管理アドレスを確定します。

```
CLUSTER_LINK_HOST    = 192.168.1.13
CLUSTER_LINK_PORT_NO = 5501
PORT_NO              = 5500
```

##### 2. ノードの登録

```bash
machcoordinatoradmin --add-node="192.168.1.13:5501" \
  --node-type=warehouse \
  --deployer="192.168.1.13:5201" \
  --package-name=machbase \
  --home-path="/home/machbase/warehouse_g1_1" \
  --dbs-path="/data/machbase/warehouse_g1_1_dbs" \
  --port-no=5500 \
  --replication=192.168.1.13:5502 \
  --group=group1 \
  --no-replicate

machcoordinatoradmin --add-node="192.168.1.14:5501" \
  --node-type=warehouse \
  --deployer="192.168.1.14:5201" \
  --package-name=machbase \
  --home-path="/home/machbase/warehouse_g1_2" \
  --dbs-path="/data/machbase/warehouse_g1_2_dbs" \
  --port-no=5500 \
  --replication=192.168.1.14:5502 \
  --group=group1
```

別途`--add-group`コマンドは使用しません。Warehouseグループ名は各Warehouseノードの登録時に
`--group`で指定します。

##### 3. ノードの起動

```bash
machcoordinatoradmin --startup-node="192.168.1.13:5501"
machcoordinatoradmin --startup-node="192.168.1.14:5501"
```

<a id="manual-machcoordinatoradmin-status-check-node-state"></a>

#### 全体状態の確認

全ノードの登録後に状態を確認します。

```bash
machcoordinatoradmin --cluster-status
```

Coordinator、Lookup、Broker、Warehouseが各役割に合う正常状態で表示されれば、クラスターは正常に
稼働しています。Coordinatorは`primary`、Brokerは`leader`、Warehouseは`normal`、`sync-active`、
`sync-standby`などで表示されます。


#### 初回接続の確認

Brokerのネイティブポートに接続し、`SELECT CURRENT_DATABASE();`とサンプル検索を実行します。
初回インストール検証後の個別ノードの起動・終了と状態復旧は
[Cluster運用](../../operations-configuration-recovery/cluster/)と
[Clusterのトラブルシューティング](../../troubleshooting/cluster/)を使用してください。
