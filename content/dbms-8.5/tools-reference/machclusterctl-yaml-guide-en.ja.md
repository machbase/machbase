---
title: machclusterctl YAML 記述ガイド
weight: 0
toc: true
---

# machclusterctl YAML 記述ガイド

`machclusterctl` が使用する `cluster.yaml` の記述方法を説明します。コマンドの実行手順は [machclusterctl-user-guide-en](../machclusterctl-user-guide-en/) を参照してください。

YAML にはクラスタの目標状態を記述します。`machclusterctl` は YAML を読み込み、`cluster.defaults`、`cluster.hosts`、環境変数の置換を適用して最終的な設定値を生成します。

## 1. 最小構成

共通の値は `cluster.defaults` と `cluster.hosts` にまとめ、各ノードには `alias`、`host`、役割のフィールドを記述します。同じタイプのノードを別々のサーバーに 1 台ずつ配置する一般的な構成では、ポートをノードごとに繰り返し記述する必要はありません。同一ホストに同じタイプのノードを 2 台以上配置する場合も、最初のノードはタイプ別の `defaults` を使用し、2 台目以降で競合するポートと通常は `home_path` だけを上書きします。

次の例は、2 台のサーバーに Coordinator 2 台、Deployer 2 台、Lookup の Master/Monitor、Broker 1 台、Warehouse グループ 1 個を構成します。

```yaml
version: "1"

cluster:
  name: mc-minimal

  hosts:
    node1:
      address: machbase@192.168.0.11
    node2:
      address: machbase@192.168.0.12

  package:
    name: machbase
    path: /machbase/packages/machbase-ent-release-lightweight.tgz

  ssh:
    key_file: /home/machbase/.ssh/id_rsa

  defaults:
    coordinator:
      home_path: /machbase/coordinator
      cluster_link_port: 5101
      http_admin_port: 5102
    deployer:
      home_path: /machbase/deployer
      cluster_link_port: 5201
      http_admin_port: 5202
    lookup:
      home_path: /machbase/lookup
      cluster_link_port: 5301
      http_admin_port: 5302
    broker:
      home_path: /machbase/broker
      cluster_link_port: 5401
      http_admin_port: 5402
      service_port: 5656
    warehouse:
      home_path: /machbase/warehouse
      cluster_link_port: 5501
      http_admin_port: 5502
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

  warehouse_groups:
    - name: group1
      nodes:
        - alias: warehouse-group1-1
          host: node1
          deployer: deployer-1

        - alias: warehouse-group1-2
          host: node2
          deployer: deployer-2
```

設定を解決した結果:

- `node1` と `node2` は、`cluster.hosts` で実際の `machbase@IP` に解決します。
- SSH ユーザーは `address: machbase@...` から取得し、SSH キーは共通の `cluster.ssh.key_file` を使用します。
- `home_path`、`cluster_link_port`、`http_admin_port`、`service_port` は、ノードタイプ別の `defaults` から継承します。
- 異なるホストでは同じデフォルトポートを使用しても競合しません。
- 同一ホストに同じタイプのノードを 2 台以上配置する場合、最初のノードはデフォルトポートを使用し、2 台目以降でポートと通常は `home_path` を明示的に上書きします。

同一ホストに Warehouse を 2 台配置する例:

```yaml
defaults:
  warehouse:
    home_path: /machbase/warehouse
    cluster_link_port: 5501
    http_admin_port: 5502
    service_port: 5500

warehouse_groups:
  - name: group1
    nodes:
      - alias: warehouse-group1-1
        host: node1
        deployer: deployer-1

  - name: group2
    nodes:
      - alias: warehouse-group2-1
        host: node1
        deployer: deployer-1
        home_path: /machbase/warehouse-group2
        cluster_link_port: 5511
        http_admin_port: 5512
        service_port: 5510
```

## 2. 環境変数と共通・個別設定の組み合わせ

環境ごとに変わる値は `${VAR}` または `${VAR:-default}` で記述できます。共通値は `defaults` に置き、必要なノードだけでポート、ホームパス、`dbs_path` を上書きします。

使用できる環境変数の構文:

- `${VAR}`: 環境変数が存在しない場合はエラー。
- `${VAR:-default}`: 環境変数が存在しないか空文字列の場合は `default` を使用。

環境変数の例:

```bash
export MC_PACKAGE_PATH=/machbase/packages/machbase-ent-release-lightweight.tgz
export MC_SSH_KEY=/home/machbase/.ssh/id_rsa
export MC_NODE1=machbase@192.168.0.11
export MC_NODE2=machbase@192.168.0.12
export MC_NODE3=machbase@192.168.0.13
export MC_HOME_BASE=/machbase
```

YAML の例:

```yaml
version: "1"

cluster:
  name: "${MC_CLUSTER_NAME:-mc-mixed}"

  hosts:
    node1:
      address: "${MC_NODE1}"
    node2:
      address: "${MC_NODE2}"
    node3:
      address: "${MC_NODE3:-machbase@192.168.0.13}"

  package:
    name: "${MC_PACKAGE_NAME:-machbase}"
    path: "${MC_PACKAGE_PATH}"

  ssh:
    key_file: "${MC_SSH_KEY}"

  defaults:
    coordinator:
      home_path: "${MC_HOME_BASE:-/machbase}/coordinator"
      cluster_link_port: "${MC_COORD_PORT:-5101}"
      http_admin_port: "${MC_COORD_HTTP_PORT:-5102}"
    deployer:
      home_path: "${MC_HOME_BASE:-/machbase}/deployer"
      cluster_link_port: "${MC_DEPLOYER_PORT:-5201}"
      http_admin_port: "${MC_DEPLOYER_HTTP_PORT:-5202}"
    lookup:
      home_path: "${MC_HOME_BASE:-/machbase}/lookup"
      cluster_link_port: "${MC_LOOKUP_PORT:-5301}"
      http_admin_port: "${MC_LOOKUP_HTTP_PORT:-5302}"
    broker:
      home_path: "${MC_HOME_BASE:-/machbase}/broker"
      cluster_link_port: "${MC_BROKER_PORT:-5401}"
      http_admin_port: "${MC_BROKER_HTTP_PORT:-5402}"
      service_port: "${MC_BROKER_SERVICE_PORT:-5656}"
    warehouse:
      home_path: "${MC_HOME_BASE:-/machbase}/warehouse"
      cluster_link_port: "${MC_WAREHOUSE_PORT:-5501}"
      http_admin_port: "${MC_WAREHOUSE_HTTP_PORT:-5502}"
      service_port: "${MC_WAREHOUSE_SERVICE_PORT:-5500}"

  coordinators:
    - alias: coord-primary-1
      host: node1
      role: primary

    - alias: coord-secondary-1
      host: node2
      role: secondary
      # node2 の Coordinator だけに別のホームパスを指定。
      home_path: "${MC_HOME_BASE:-/machbase}/coordinator-secondary"

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

    - alias: lookup-slave-1
      host: node3
      deployer: deployer-3
      type: slave
      # node3 に Lookup を追加する場合に備え、slave のポートだけを上書き。
      cluster_link_port: "${MC_LOOKUP_SLAVE_PORT:-5311}"
      http_admin_port: "${MC_LOOKUP_SLAVE_HTTP_PORT:-5312}"

  brokers:
    - alias: broker-1
      host: node1
      deployer: deployer-1

    - alias: broker-2
      host: node2
      deployer: deployer-2
      # broker-2 のサービスポート・データパスだけを明示的に上書き。
      service_port: "${MC_BROKER2_SERVICE_PORT:-5666}"
      dbs_path: "${MC_HOME_BASE:-/machbase}/dbs/broker-2"

  warehouse_groups:
    - name: group1
      nodes:
        - alias: warehouse-group1-1
          host: node1
          deployer: deployer-1

        - alias: warehouse-group1-2
          host: node2
          deployer: deployer-2
          dbs_path: "${MC_HOME_BASE:-/machbase}/dbs/warehouse-group1-2"

    - name: group2
      nodes:
        - alias: warehouse-group2-1
          host: node2
          deployer: deployer-2
          # node2 に 2 台目の Warehouse を配置するため、ポートと home_path を上書き。
          home_path: "${MC_HOME_BASE:-/machbase}/warehouse-group2"
          cluster_link_port: "${MC_WAREHOUSE_G2_PORT:-5511}"
          http_admin_port: "${MC_WAREHOUSE_G2_HTTP_PORT:-5512}"
          service_port: "${MC_WAREHOUSE_G2_SERVICE_PORT:-5510}"

        - alias: warehouse-group2-2
          host: node3
          deployer: deployer-3
```

運用上の規則:

- 環境変数の置換は YAML のデコード前に行います。数値フィールドの値は、置換後に整数へ変換できる必要があります。
- `cluster.hosts` の `address` に `user@host` を指定すると、SSH ユーザーを繰り返し記述せずに済みます。
- `cluster.ssh.key_file` は共通のキーを 1 か所で指定します。ホストごとにキーが異なる場合は `cluster.hosts.<alias>.ssh.key_file` で上書きします。
- `deployer` は Lookup/Broker/Warehouse が使用する Deployer の別名です。同一ホストに Deployer が 1 台だけなら省略できますが、明示を推奨します。
- `dbs_path` は Broker/Warehouse ノードだけで使用できます。defaults には指定できません。

## 3. 設定可能な全フィールド

### 3-1. 最上位の構造

| YAML パス | 型 | 必須 | 説明 |
|-----------|------|------|------|
| `version` | string | はい | YAML スキーマのバージョン。現在は `"1"` を使用します。 |
| `cluster` | object | はい | クラスタ全体の定義。 |
| `cluster.name` | string | はい | クラスタ名。`validate`、`install`、`apply`、`destroy` の確認メッセージと、運用者によるクラスタの識別に使用します。 |

### 3-2. `cluster.hosts`

`cluster.hosts` は IP・ホスト名を一元管理し、ノード設定でホストの別名だけを使用するためのセクションです。

| YAML パス | 型 | 必須 | 省略時の値 | 説明 |
|-----------|------|------|----------|------|
| `cluster.hosts` | map | いいえ | なし | ホストの別名の定義一覧。 |
| `cluster.hosts.<alias>.address` | string | ホストの別名を使用する場合は必須 | なし | 実際の IP/DNS、または `user@ip`、`user@hostname` のエンドポイント。 |
| `cluster.hosts.<alias>.ssh` | object | いいえ | `cluster.ssh` | このホストの別名を使用するノードに適用する SSH の上書き設定。 |
| `cluster.hosts.<alias>.ssh.user` | string | いいえ | `address` のユーザーまたは共通 SSH ユーザー | 互換性・例外用途の SSH ユーザー。新しい YAML では `address: user@host` を推奨します。 |
| `cluster.hosts.<alias>.ssh.port` | int | いいえ | `cluster.ssh.port` または 22 | SSH 接続ポート。 |
| `cluster.hosts.<alias>.ssh.key_file` | string | いいえ | `cluster.ssh.key_file` | このホスト専用の SSH 秘密鍵のパス。 |

`host` が `cluster.hosts` に存在しない単純な文字列で、IP/DNS 名の形式でもない場合は `undefined host alias` エラーになります。`localhost`、IP、`.` または `:` を含むホスト名は、直接ホスト値として扱います。

### 3-3. `cluster.defaults`

`defaults` は、ノードタイプ別の共通値の記述を減らす machclusterctl の機能です。

| YAML パス | 型 | 必須 | 説明 |
|-----------|------|------|------|
| `cluster.defaults.common.ssh_user` | string | いいえ | 互換性のための共通 SSH ユーザー。新しい YAML では `user@host` を推奨します。 |
| `cluster.defaults.coordinator` | object | いいえ | Coordinator のデフォルト値。 |
| `cluster.defaults.deployer` | object | いいえ | Deployer のデフォルト値。 |
| `cluster.defaults.lookup` | object | いいえ | Lookup のデフォルト値。 |
| `cluster.defaults.broker` | object | いいえ | Broker のデフォルト値。 |
| `cluster.defaults.warehouse` | object | いいえ | Warehouse のデフォルト値。 |

各ノードタイプの defaults に指定できるフィールド:

| フィールド | 適用対象 | 説明 |
|------|-----------|------|
| `home_path` | すべてのノードタイプ | ノードのホームパス。絶対パスのみ指定できます。 |
| `cluster_link_port` | すべてのノードタイプ | クラスタリンクの通信ポート。 |
| `http_admin_port` | すべてのノードタイプ | HTTP 管理ポート。Coordinator/Deployer では必須です。Lookup/Broker/Warehouse でも設定でき、デフォルトまたはノード別の値を推奨します。 |
| `service_port` | broker, warehouse | Broker クライアントの接続ポート、または Warehouse のサービスポート。 |

ノード自身に値がある場合はその値を優先し、ない場合はそのノードタイプの `defaults` を使用します。

### 3-4. `cluster.package`

| YAML パス | 型 | 必須 | 説明 |
|-----------|------|------|------|
| `cluster.package.name` | string | はい | Coordinator に登録するパッケージ名。アップグレード時は新しい名前を推奨します。 |
| `cluster.package.path` | string | 条件付き | 運用者が記述する入力アーカイブのパス。`origin_path` がない場合に使用します。 |
| `cluster.package.origin_path` | string | 条件付き | 入力アーカイブのパス。`path` より優先します。エクスポートする YAML はこのフィールドを出力します。 |
| `cluster.package.registered_path` | string | いいえ | Coordinator のパッケージリポジトリに保存されたパス。エクスポート時の現在のメタデータの値であり、インストール・アップグレードの入力には使用しません。 |

`path` と `origin_path` のどちらか一方は必須です。`install`、`upgrade`、新規ノードの `apply` ではアーカイブが実際に存在し、Machbase の実行バイナリーと `bin/`、`lib/`、`conf/` の構成要素を含む必要があります。

稼働中の Broker/Warehouse の現在のパッケージ名と、YAML の `cluster.package.name` を比較して変更を判定します。同じ名前のまま内容や `cluster.package.path`/`cluster.package.origin_path` だけを変えても、既存の Broker/Warehouse はアップグレード対象として検出されません。異なる内容のアーカイブを適用する場合は、新しい `cluster.package.name` と一意のアーカイブファイル名を指定します。

#### パッケージの入力パスと Coordinator のパッケージリポジトリ

目標状態を記述する YAML の `cluster.package.path` または `cluster.package.origin_path` には、原則として Coordinator のホーム外に保存した **元のアーカイブパス** を指定します。

推奨例:

```yaml
cluster:
  package:
    name: machbase-v2
    path: /machbase/packages/machbase-v2.tgz
```

非推奨例:

```yaml
cluster:
  package:
    name: machbase-v2
    path: /machbase/coordinator/package/machbase-v2.tgz
```

Coordinator の `package/` ディレクトリは、`machcoordinatoradmin --add-package` がパッケージ登録時に内部で使用するリポジトリです。このファイルを新しいパッケージの登録元に再使用すると、次の状況が発生する場合があります。

- 同じ `package.name` とファイル名が既に登録されている場合は、冪等性を保つために処理をスキップする場合があります。
- 別の `package.name` で同じファイル名を登録すると、Coordinator がファイル名重複として拒否する場合があります。
- `destroy` で Coordinator のホームとパッケージリポジトリが削除される場合があります。エクスポートした YAML のパスだけを頼りに再インストールすると、アーカイブが存在しない可能性があります。

アップグレード用の新しいアーカイブは、次の規則で管理します。

- 内容を変更したら `cluster.package.name` を新しい値にします。
- アーカイブファイル名も新しいパッケージ名に合わせて一意にします。例: `machbase-v2.tgz`、`machbase-v3.tgz`。
- `cluster.package.path` または `cluster.package.origin_path` には、`/machbase/packages/...` のように Coordinator のホーム外で保持できる元のパスを指定します。
- `machclusterctl export` が出力した `registered_path` を再インストールや新しいアップグレードの入力にしないでください。必要に応じて `origin_path` を元のアーカイブパスに修正するか、`path` を指定します。

YAML に未定義のフィールドがある場合は、読み込み時にエラーになります。誤記したフィールドは無視されないため、エラーメッセージのフィールド名を確認して修正してください。

### 3-5. SSH 設定

SSH 設定は、`install`、新規ノードの追加、`destroy`、`upgrade --full-stop` など、リモートサーバーに直接アクセスするコマンドで使用します。

適用順序（後の設定が優先）:

```text
cluster.defaults.common.ssh_user
  → cluster.ssh
  → user@host または hosts.<alias>.address のユーザー
  → cluster.hosts.<alias>.ssh
  → node.ssh
```

| YAML パス | 型 | 必須 | 説明 |
|-----------|------|------|------|
| `cluster.ssh.user` | string | 条件付き | 共通 SSH ユーザー。新しい YAML では `address: user@host` を推奨します。 |
| `cluster.ssh.port` | int | いいえ | 共通 SSH ポート。省略時はデフォルトの 22 を使用します。 |
| `cluster.ssh.key_file` | string | リモート操作時は必須 | 共通の SSH 秘密鍵のパス。 |
| `node.ssh.user` | string | いいえ | 特定ノードの SSH ユーザーの上書き。 |
| `node.ssh.port` | int | いいえ | 特定ノードの SSH ポートの上書き。 |
| `node.ssh.key_file` | string | いいえ | 特定ノードの SSH キーの上書き。 |

YAML スキーマには SSH password フィールドがありません。`ssh.password` を記述すると、設定の読み込み時にエラーになります。

### 3-6. 共通のノードフィールド

次のフィールドは Coordinator、Deployer、Lookup、Broker、Warehouse に共通です。ただし、`deployer`、`service_port`、`dbs_path` の適用対象は限定されます。

| フィールド | 型 | 必須 | 省略時の値 | 説明 |
|------|------|------|----------|------|
| `alias` | string | いいえ | 自動生成 | ノードの論理名。運用では明示を推奨します。コマンドの `--node` はこの別名を使用します。 |
| `host` | string | はい | なし | 実際のホスト、`user@host`、または `cluster.hosts` に定義したホストの別名。 |
| `cluster_link_port` | int | defaults がない場合は必須 | `defaults.<type>.cluster_link_port` | ノードのクラスタリンクポート。実際の識別子は `host:cluster_link_port` です。 |
| `http_admin_port` | int | Coordinator/Deployer では defaults がない場合は必須 | `defaults.<type>.http_admin_port` | HTTP 管理ポート。 |
| `home_path` | string | defaults がない場合は必須 | `defaults.<type>.home_path` | ノードのホームパス。絶対パスのみ指定できます。 |
| `deployer` | string | Lookup/Broker/Warehouse では推奨 | 同一ホストの Deployer | 使用する Deployer の別名または `host:cluster_link_port`。同一ホストに複数の Deployer がある場合は明示が必要です。 |
| `service_port` | int | Broker/Warehouse では defaults がない場合は必須 | `defaults.broker.service_port`, `defaults.warehouse.service_port` | Broker クライアントの接続ポート、または Warehouse のサービスポート。 |
| `dbs_path` | string | いいえ | なし | Broker/Warehouse のデータパス。絶対パスまたは `?` で始まるパスのみ指定できます。 |
| `dbs-path` | string | いいえ | なし | `dbs_path` と同じ意味の互換用の別名。Broker/Warehouse ノードでのみ使用できます。 |
| `ssh` | object | いいえ | ホスト別・共通の SSH 設定 | ノード別の SSH 上書き設定。 |

注意:

- 同一ホスト内で `cluster_link_port`、`http_admin_port`、`service_port` と内部の派生ポートが重複すると、検証エラーになります。
- Coordinator/Deployer は `cluster_link_port + 1` を内部の `PORT_NO` に使用します。他のノードのポートと重複しないようにしてください。
- Warehouse は `service_port + 2` をレプリケーションマネージャーのポートに使用します。他のノードの `cluster_link_port`、`http_admin_port`、`service_port` と重複しないようにしてください。
- Broker/Warehouse 以外に `dbs_path` を指定するとエラーになります。
- `dbs_path` は defaults には指定できません。

### 3-7. coordinator

パス: `cluster.coordinators[]`

| フィールド | 型 | 必須 | 説明 |
|------|------|------|------|
| `alias` | string | いいえ | Coordinator の別名。 |
| `host` | string | はい | ホストの別名または実際のホスト。 |
| `role` | string | はい | `primary` または `secondary`。primary は正確に 1 台必要です。 |
| `cluster_link_port` | int | defaults がない場合は必須 | クラスタリンクポート。 |
| `http_admin_port` | int | defaults がない場合は必須 | HTTP 管理ポート。 |
| `home_path` | string | defaults がない場合は必須 | Coordinator のホームパス。 |
| `ssh` | object | いいえ | ノード別の SSH 上書き設定。 |

### 3-8. deployer

パス: `cluster.deployers[]`

| フィールド | 型 | 必須 | 説明 |
|------|------|------|------|
| `alias` | string | いいえ | Deployer の別名。 |
| `host` | string | はい | ホストの別名または実際のホスト。 |
| `cluster_link_port` | int | defaults がない場合は必須 | クラスタリンクポート。 |
| `http_admin_port` | int | defaults がない場合は必須 | HTTP 管理ポート。 |
| `home_path` | string | defaults がない場合は必須 | Deployer のホームパス。 |
| `ssh` | object | いいえ | ノード別の SSH 上書き設定。 |

Lookup/Broker/Warehouse の `deployer` フィールドは、Deployer の `alias` または `host:cluster_link_port` を参照します。

### 3-9. lookup

パス: `cluster.lookup[]`

| フィールド | 型 | 必須 | 説明 |
|------|------|------|------|
| `alias` | string | いいえ | Lookup の別名。 |
| `host` | string | はい | ホストの別名または実際のホスト。 |
| `deployer` | string | 推奨 | インストールに使用する Deployer の別名または `host:cluster_link_port`。 |
| `type` | string | はい | `master`、`monitor`、`slave` のいずれか。master は正確に 1 台、monitor は少なくとも 1 台必要です。 |
| `cluster_link_port` | int | defaults がない場合は必須 | クラスタリンクポート。 |
| `http_admin_port` | int | いいえ | HTTP 管理ポート。 |
| `home_path` | string | defaults がない場合は必須 | Lookup のホームパス。 |
| `ssh` | object | いいえ | ノード別の SSH 上書き設定。 |

### 3-10. broker

パス: `cluster.brokers[]`

| フィールド | 型 | 必須 | 説明 |
|------|------|------|------|
| `alias` | string | いいえ | Broker の別名。 |
| `host` | string | はい | ホストの別名または実際のホスト。 |
| `deployer` | string | 推奨 | インストールに使用する Deployer の別名または `host:cluster_link_port`。 |
| `cluster_link_port` | int | defaults がない場合は必須 | クラスタリンクポート。 |
| `http_admin_port` | int | いいえ | HTTP 管理ポート。 |
| `service_port` | int | defaults がない場合は必須 | クライアント・machsql の接続ポート。 |
| `home_path` | string | defaults がない場合は必須 | Broker のホームパス。 |
| `dbs_path` または `dbs-path` | string | いいえ | Broker の DBS_PATH の上書き。 |
| `ssh` | object | いいえ | ノード別の SSH 上書き設定。 |

### 3-11. warehouse group / warehouse node

パス:

- `cluster.warehouse_groups[]`
- `cluster.warehouse_groups[].nodes[]`

| フィールド | 型 | 必須 | 説明 |
|------|------|------|------|
| `warehouse_groups[].name` | string | はい | Warehouse グループ名。レプリケーションの単位です。 |
| `warehouse_groups[].nodes[].alias` | string | いいえ | Warehouse の別名。 |
| `warehouse_groups[].nodes[].host` | string | はい | ホストの別名または実際のホスト。 |
| `warehouse_groups[].nodes[].deployer` | string | 推奨 | インストールに使用する Deployer の別名または `host:cluster_link_port`。 |
| `warehouse_groups[].nodes[].cluster_link_port` | int | defaults がない場合は必須 | クラスタリンクポート。 |
| `warehouse_groups[].nodes[].http_admin_port` | int | いいえ | HTTP 管理ポート。 |
| `warehouse_groups[].nodes[].service_port` | int | defaults がない場合は必須 | Warehouse のサービスポート。 |
| `warehouse_groups[].nodes[].home_path` | string | defaults がない場合は必須 | Warehouse のホームパス。 |
| `warehouse_groups[].nodes[].dbs_path` または `dbs-path` | string | いいえ | Warehouse の DBS_PATH の上書き。 |
| `warehouse_groups[].nodes[].ssh` | object | いいえ | ノード別の SSH 上書き設定。 |

Warehouse の追加時、`machclusterctl` はその Warehouse 自身の `host:service_port+2` をレプリケーションマネージャーのアドレスとして計算します。これはピアのアドレスではなく、生成する Warehouse 設定の `REPLICATION_MANAGER_PORT_NO` に対応します。グループの最初の Warehouse など `--no-replicate` が必要な場合は、`--replication` を同時に渡しません。

### 3-12. フラットなエクスポート YAML との関係

`machclusterctl export` が生成する YAML は、稼働中のクラスタの最終値を保存したり、差分を比較したりするための出力です。`export` は追加オプションなしで常にフラットな YAML を出力します。

フラットな YAML の特徴:

- `cluster.hosts` を使用しません。
- `cluster.defaults` を使用しません。
- 環境変数式を使用しません。
- 各ノードに実際の `host`、`cluster_link_port`、`http_admin_port`、`service_port`、`home_path`、`dbs_path` などを可能な限り明示します。
- 安定した差分比較ができるように、出力順序を並べ替えます。

手作業で記述する YAML は第 1 章・第 2 章の形式で簡潔に記述し、稼働中のクラスタ状態の保存や変更履歴の比較にはフラットなエクスポートを使用することを推奨します。

注意事項:

- エクスポートした YAML の `cluster.package.origin_path` は、Coordinator が保持する元のアーカイブパスです。メタデータに元のパスがない場合は、`registered_path` の値が入る場合があります。
- `cluster.package.registered_path` は、Coordinator に現在登録・保存されているパッケージファイルのパスです。元のアーカイブの保管場所ではなく、現在のメタデータのスナップショットに相当します。
- パッケージ一覧の取得に失敗した場合や、現在のパッケージ名に対応する登録済みパスを絶対パスとして取得できない場合は、エクスポートに失敗します。
- 同じ稼働中のクラスタへの `validate`、`apply --dry-run`、構造の差分比較には使用できます。
- `destroy` 後の再インストールや、新しいパッケージへのアップグレードの入力に使用する場合は、`cluster.package.origin_path` または `cluster.package.path` を Coordinator のホーム外にある元のアーカイブパスに修正します。
- 新規ノードの追加や再インストールに必要な SSH 設定は Coordinator のメタデータから復元できないため、YAML に追加します。