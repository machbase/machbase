---
title: machclusterctl ユーザーガイド
weight: 0
toc: true
---

# machclusterctl ユーザーガイド

`machclusterctl` は、YAML ファイルで Machbase Cluster Edition をインストール・運用するコマンドラインツールです。`cluster.yaml` に必要なクラスタ構成を宣言し、`validate`、`install`、`apply`、`upgrade`、`start`、`stop` などのコマンドで管理します。

YAML の記述方法は [machclusterctl-yaml-guide-en](../machclusterctl-yaml-guide-en/) も参照してください。

## 1. 基本概念

`machclusterctl` は次の手順で動作します。

1. `cluster.yaml` を読み込み、クラスタの目標状態を構築します。
2. 現在のクラスタ状態と目標状態を比較します。
3. 必要なインストール、追加、削除、アップグレード、起動・停止だけを実行します。

一般的な操作の流れは次のとおりです。

```bash
machclusterctl validate -f cluster.yaml
machclusterctl install -f cluster.yaml --dry-run
machclusterctl install -f cluster.yaml --yes
machclusterctl status
```

インストール後に YAML を編集してノードを追加・削除する場合は、`install` ではなく `apply` を使用します。

```bash
machclusterctl apply -f cluster.yaml --dry-run
machclusterctl apply -f cluster.yaml --yes
```

## 2. 実行場所と環境

`machclusterctl` は、プライマリ Coordinator をインストールするサーバー、またはプライマリ Coordinator サーバーで実行することを推奨します。

推奨する環境変数:

```bash
export MACHBASE_COORDINATOR_HOME=/home/machbase/coordinator
export MACHBASE_HOME=$MACHBASE_COORDINATOR_HOME
export PATH=$MACHBASE_COORDINATOR_HOME/bin:$PATH
export LD_LIBRARY_PATH=$MACHBASE_COORDINATOR_HOME/lib:$LD_LIBRARY_PATH
```

`MACHBASE_COORDINATOR_HOME` は、`status`、`start`、`stop`、`connect`、`export` など YAML なしで実行するコマンドが、プライマリ Coordinator を特定するために使用します。インストール後の現在のトポロジーは、ローカルの状態ファイルではなく Coordinator のメタデータから取得します。

以降、YAML なしで実行するコマンドは通常オプションを付けずに使用します。

```bash
machclusterctl status
machclusterctl connect broker-1
machclusterctl export -o cluster-export.yaml
```

環境変数を変更しにくい場合や、1 台のサーバーで複数の Coordinator ホームを切り替えて確認する場合に限り、`--coordinator` でプライマリ Coordinator のホームを直接指定します。

```bash
machclusterctl status --coordinator /home/machbase/coordinator
machclusterctl export --coordinator /home/machbase/coordinator -o cluster-export.yaml
```

## 3. インストール前の準備

インストール前に次の項目を準備してください。

| 項目 | 説明 |
|------|------|
| パッケージアーカイブ | プライマリ Coordinator サーバーのローカルにある Machbase Cluster Edition パッケージファイル |
| SSH キー | プライマリ Coordinator サーバーから各対象サーバーに接続する秘密鍵 |
| cluster.yaml | インストールする Coordinator、Deployer、Lookup、Broker、Warehouse の構成 |
| ディレクトリ権限 | 各ノードの `home_path` の親パスを作成・書き込みできる権限 |
| ポート | 各サーバーで YAML に指定したポートが未使用であること |

SSH は鍵ファイルによる非対話接続を使用します。YAML に password フィールドは記述しません。

事前確認の例:

```bash
ssh -i /home/machbase/.ssh/id_rsa machbase@192.168.0.11 'echo ok'
scp -i /home/machbase/.ssh/id_rsa /etc/hosts machbase@192.168.0.11:/home/machbase/hosts.test
```

## 4. コマンド概要

| コマンド | 用途 |
|------|------|
| `validate` | YAML 構文、必須値、ポート競合、トポロジーを検証 |
| `install` | 空の環境に新しいクラスタをインストール |
| `apply` | 稼働中のクラスタに YAML の変更を反映 |
| `upgrade` | パッケージ変更に応じてノードをアップグレード |
| `status` | 現在のクラスタ状態を取得 |
| `connect` | Broker または Warehouse の別名を使って `machsql` で接続 |
| `start` | 全体、タイプ別、または特定ノードを起動 |
| `stop` | 全体、タイプ別、または特定ノードを停止 |
| `export` | 稼働中のクラスタのトポロジーを YAML に出力 |
| `destroy` | クラスタのインストール内容を除去 |

よく使用する共通オプション:

| オプション | 説明 |
|------|------|
| `-f`, `--file` | 使用する YAML ファイル。デフォルトは `./cluster.yaml` |
| `--dry-run` | 実際には変更せず、検証と実行計画だけを出力 |
| `-y`, `--yes` | 確認せずに実行 |
| `-v`, `--verbose` | 互換性のために受け付けます。実行コマンドはデフォルトで進捗ログを出力します。 |
| `-s`, `--silent` | 進捗ログを抑制します。`-v`/`--verbose` より優先します。 |
| `--coordinator` | YAML なしで実行する `status`、`start`、`stop`、`connect`、`export` が使用するプライマリ Coordinator のホーム |

## 5. YAML の検証

インストールや変更の前に、必ず YAML を検証してください。

```bash
machclusterctl validate -f cluster.yaml
```

正常な場合:

```text
Validation passed.
```

主な検証項目:

- 必須フィールドの欠落
- ノードの別名の重複
- 同一ホスト内のポート競合
- プライマリ Coordinator の数
- Lookup の Master/Monitor 構成
- `home_path`、`dbs_path` のパス形式
- `deployer` の参照

## 6. 初回インストール

`install` は、クラスタがまだインストールされていない空の環境でのみ使用します。既存のインストール内容が残っている場合や、クラスタが既に稼働している場合は失敗します。

まず、インストール可能か確認します。

```bash
machclusterctl install -f cluster.yaml --dry-run --verbose
```

問題がなければ、実際にインストールします。

```bash
machclusterctl install -f cluster.yaml --yes --verbose
```

インストール後に状態を確認します。

```bash
machclusterctl status
```

`install` は YAML に基づき、Coordinator、Deployer、パッケージ、Lookup、Broker、Warehouse の順に準備・起動します。インストール後の `status`、`start`、`stop`、`connect`、`export` は、稼働中の Coordinator から現在のメタデータを取得します。

## 7. 運用時の変更の反映

インストール後に YAML を編集してノードを追加・削除・変更する場合は、`apply` を使用します。

推奨手順:

```bash
machclusterctl validate -f cluster.yaml
machclusterctl apply -f cluster.yaml --dry-run --verbose
machclusterctl apply -f cluster.yaml --yes --verbose
machclusterctl status
```

`apply` は稼働中のクラスタでのみ動作します。クラスタが停止している場合は、先に起動してください。

```bash
machclusterctl start
machclusterctl apply -f cluster.yaml --dry-run
machclusterctl apply -f cluster.yaml --yes
```

`apply` で実行できる代表的な操作:

- Lookup、Broker、Warehouse の追加
- Lookup、Broker、Warehouse の削除
- Lookup、Broker、Warehouse の設定変更に伴う再登録
- セカンダリ Coordinator の追加
- Deployer の追加
- YAML のパッケージ変更に伴う Broker/Warehouse のアップグレード

プライマリ Coordinator の置き換えや削除には対応していません。

## 8. 起動・停止・状態確認

全体の状態確認:

```bash
machclusterctl status
```

全体の起動と停止:

```bash
machclusterctl start
machclusterctl stop
```

タイプ別の起動と停止:

```bash
machclusterctl start --type=warehouse
machclusterctl stop --type=warehouse

machclusterctl start --type=broker
machclusterctl stop --type=broker
```

特定ノードの起動と停止:

```bash
machclusterctl start --node=warehouse-group1-1
machclusterctl stop --node=warehouse-group1-1
```

`--node` には `host:port` ではなく、YAML の `alias` を指定します。

Warehouse の停止時には、必要な Warehouse グループの状態遷移も行います。単一 Warehouse の停止後はグループを `normal` に戻します。全 Warehouse の停止など、グループ全体が停止する場合は、停止処理に合わせて状態遷移を要求します。

## 9. SQL 接続

Broker または Warehouse に `machsql` で接続するには、`connect` を使用します。

```bash
machclusterctl connect broker-1
machclusterctl connect warehouse-group1-1
```

`connect` は別名に対応するホストと `service_port` を取得し、次の形式で `machsql` を実行します。

```bash
machsql -s <host_ip> -P <service_port>
```

たとえば `broker-1` のホストが `192.168.0.11`、`service_port` が `5656` の場合、次のコマンドと同じ動作です。

```bash
machsql -s 192.168.0.11 -P 5656
```

デフォルトでは、稼働中の Coordinator のメタデータから別名とサービスポートを取得します。別の YAML ファイルで接続先を決める場合は、`-f` を指定します。

```bash
machclusterctl connect -f cluster.yaml broker-1
```

注意:

- 別名は Broker または Warehouse ノードである必要があります。
- `--node` と同様、`host:port` ではなく YAML の `alias` を使用します。
- 通常は `MACHBASE_COORDINATOR_HOME` でプライマリ Coordinator のホームを指定します。
- 環境変数を使用しにくい場合は、例外的に `--coordinator` で直接指定できます。

## 10. パッケージのアップグレード

YAML の `cluster.package` に指定した入力パッケージを新しいアーカイブに変更してから、アップグレードを実行します。手作業で記述する YAML では、通常 `path` を使用します。

```yaml
cluster:
  package:
    name: machbase-v2
    path: /machbase/packages/machbase-v2.tgz
```

`machclusterctl export` が生成する YAML では、パッケージパスを次のように分けて記録する場合があります。

```yaml
cluster:
  package:
    name: machbase-v2
    origin_path: /machbase/packages/machbase-v2.tgz
    registered_path: /machbase/coordinator/package/machbase-v2.tgz
```

各フィールドの意味:

- `path`: 運用者が指定する入力アーカイブのパス。
- `origin_path`: `path` と同じ用途の入力アーカイブパス。両方ある場合は `origin_path` が優先します。
- `registered_path`: `--add-package` 後に Coordinator の内部パッケージリポジトリに保存されたパス。実行の入力ではなく、現在のメタデータから取得した値です。

稼働中の Broker/Warehouse の現在のパッケージ名と、YAML の `cluster.package.name` を比較して変更を判定します。同じ `package.name` のままアーカイブの内容や `path`/`origin_path` だけを変えても、既存の Broker/Warehouse はアップグレード対象として検出されません。新しいアーカイブを適用する場合は、新しいパッケージ名と一意のアーカイブファイル名を指定してください。

### 10-1. パッケージパスの運用規則

`cluster.package.path` または `cluster.package.origin_path` には、プライマリ Coordinator サーバーのローカルにある **元のパッケージアーカイブのパス** を指定します。`install`、新規ノードの `apply`、`upgrade` は、必要に応じて `machcoordinatoradmin --add-package=<name> --file-name=<archive>` を自動実行します。

コマンドを実行するサーバーからアーカイブを読み取れる必要があります。`--full-stop` の事前検証では、アーカイブ内に `machcoordinatoradmin`、`machdeployeradmin`、`conf/`、`lib/` があるか確認します。

運用 YAML では、次のような Coordinator 管理下のパッケージリポジトリのパスを、新しいパッケージの登録元として使用しないでください。

```yaml
# 推奨: 運用者が保持する元のアーカイブパス
cluster:
  package:
    name: machbase-v2
    path: /machbase/packages/machbase-v2.tgz

# 非推奨: Coordinator が登録後に内部で保持するパス
cluster:
  package:
    name: machbase-v2
    path: /machbase/coordinator/package/machbase-v2.tgz
```

理由は次のとおりです。

- Coordinator のパッケージリポジトリにあるファイルは `--add-package` の出力です。同じファイルを再び登録元にすると、登録済みパッケージか、新規登録時のファイル名競合かによって動作が変わります。
- 同じ `package.name` とファイル名が既に登録されている場合、`machclusterctl` は冪等性を保つために処理をスキップすることがあります。
- 別の `package.name` で同じファイル名を再利用すると、Coordinator がファイル名重複として拒否する場合があります。新しいパッケージは `machbase-v2.tgz`、`machbase-v3.tgz` のようにファイル名も一意にしてください。
- `destroy` は Coordinator のホームとパッケージリポジトリを削除する場合があります。再インストール用のアーカイブは、Coordinator のホーム外の別の場所に保存してください。

運用の基本方針:

- `install`、`apply` による新規ノード追加、`upgrade` の `path` または `origin_path` には、Coordinator のホーム外で保持できる元のアーカイブパスを指定します。
- パッケージの内容を変更したら、`package.name` とアーカイブファイル名も変更します。
- エクスポートした YAML を再インストールやアップグレードに使用する場合は、`origin_path` を元のアーカイブパスに修正するか、`registered_path` の代わりに `path` を指定してから実行します。

### 10-2. オンラインアップグレード

`--online` は Broker と Warehouse にパッケージを適用します。Coordinator、Deployer、Lookup は対象外です。

```bash
machclusterctl upgrade -f cluster.yaml --online --dry-run
machclusterctl upgrade -f cluster.yaml --online --yes --verbose
```

`upgrade` でモードを省略するとオンラインモードになります。手順を明確にするため、`--online` の明示を推奨します。`--online` と `--full-stop` は併用できません。`apply` がパッケージ変更を検出して自動実行するアップグレードも、Broker/Warehouse のオンラインアップグレードと同じ範囲です。

オンラインアップグレードの流れ:

1. クラスタが running 状態であることを確認します。
2. YAML と現在のトポロジーの間に、ノード追加・削除・設定変更がないことを確認します。
3. 新しいアーカイブを Coordinator のパッケージリポジトリに登録します。
4. Broker は `--upgrade-node` の後に起動します。
5. Warehouse はグループを `readonly`、対象ノードを `inactive` にしてから、`--upgrade-node`、起動・アクティブ化、グループの `normal` への復帰を行います。
6. 対象の Broker/Warehouse が running 状態であることを確認します。

オンラインモードはクラスタ全体を停止しませんが、HA を考慮したローリングアップグレードを保証するものではありません。Coordinator/Deployer/Lookup のバイナリー変更、プロトコル互換性に影響し得る変更、全ノードを同じパッケージにそろえる変更には `--full-stop` を使用してください。

### 10-3. 全停止アップグレード

Coordinator、Deployer、Lookup を含む全ノードのバイナリーを置き換えるには、`--full-stop` を使用します。このモードではクラスタ全体を停止します。

```bash
machclusterctl upgrade -f cluster.yaml --full-stop --dry-run
machclusterctl upgrade -f cluster.yaml --full-stop --yes --verbose
```

全停止アップグレードの流れ:

1. クラスタが running 状態であることを確認します。
2. YAML と現在のトポロジーの間に、ノード追加・削除・設定変更がないことを確認します。
3. ローカルの `tar` と、リモートノードがある場合は `ssh`/`scp` を実行できることを確認します。
4. アーカイブの存在と必須項目を確認します。
5. 対象の全ノードの `home_path` が存在し、書き込み可能であることを確認します。
6. 新しいパッケージを Coordinator のパッケージリポジトリに登録します。
7. クラスタ全体を停止します。
8. 各ノードの `home_path` の隣に用意したステージングパスでアーカイブを展開し、ノードのホームに反映します。
9. プライマリ Coordinator を先に起動し、残りのクラスタを起動します。
10. Broker/Warehouse のパッケージメタデータを同期し、全対象ノードが running 状態であることを確認します。

ノードのホームを置き換える際は、`dbs`、`meta`、`package` を保持します。既存の `conf/machbase.conf` もバックアップ後に復元します。置き換え中にエラーが発生した場合は、そのノードの元のホームの内容を可能な範囲で戻します。

アップグレード前にトポロジーの差分を解消してください。ノードの追加・削除・変更がある場合は、先に `apply` で反映してからパッケージをアップグレードします。

アップグレード後の確認:

```bash
machclusterctl status
machclusterctl apply -f cluster.yaml --dry-run
```

## 11. 現在のトポロジーのエクスポート

稼働中のクラスタの状態を YAML に保存するには、`export` を使用します。

```bash
machclusterctl export -o current.yaml
```

標準出力に表示する場合:

```bash
machclusterctl export
```

`export` はフラットな YAML を出力します。`cluster.hosts`、`cluster.defaults`、環境変数式を生成せず、各ノードの最終値を直接記録します。パッケージは Coordinator のメタデータに基づいて `origin_path` と `registered_path` を出力します。

`origin_path` は、Coordinator が保持する元のアーカイブパスです。メタデータに元のパスがない場合は、有効な YAML を生成するため、`registered_path` を `origin_path` にも設定します。`registered_path` は Coordinator に登録・保存されたパッケージのパス（`<coordinator_home>/package/<File-Name>`）です。

このファイルは、現在の運用状態の保存や変更前後の差分比較に便利です。ただし、エクスポートの `registered_path` は、初回インストール時に運用者が使用した元のアーカイブパスを復元するものではありません。
`export` は、パッケージ一覧の取得に失敗した場合や、現在のパッケージ名に対応する登録済みパスを絶対パスとして取得できない場合に失敗します。パッケージ名をパスの代わりに使用して YAML を生成することはありません。

エクスポートした YAML の使用方針:

- 稼働中のクラスタとの比較や、同じクラスタに対する変更なしの `apply --dry-run` には、そのまま使用できます。
- 再インストールに使用する場合は、`destroy` 前に `origin_path` のパッケージファイルを Coordinator のホーム外に保存するか、YAML の `origin_path` または `path` を実際の元のアーカイブパスに修正します。
- 新しいパッケージへアップグレードする場合は、`registered_path` を実行の入力にせず、`package.name` と `origin_path` または `path` を新しい元のアーカイブに合わせて変更します。
- SSH キーやユーザーなどの初期設定情報が必要な場合は、YAML に追加します。

## 12. destroy

クラスタを除去し、未インストールの状態に戻すには、`destroy` を使用します。

```bash
machclusterctl destroy -f cluster.yaml
```

確認を省略して実行する場合:

```bash
machclusterctl destroy -f cluster.yaml --yes --verbose
```

注意:

- 稼働中・停止中のクラスタのインストール内容を除去します。
- Broker/Warehouse のデータが削除される場合があります。
- 本番環境では実行権限を制限してください。

## 13. よくあるエラー

| エラー・状況 | 対処 |
|-----------|------|
| `cluster is already installed` | 既存のインストール内容が残っています。新規インストールなら `destroy` または手動で除去し、`install` を再実行します。 |
| `cluster is not installed` | `install` が必要です。 |
| `cluster is installed but not running` | `machclusterctl start` の後に `apply` または `upgrade` を再実行します。 |
| `port conflict` | 同一ホスト内で重複する `cluster_link_port`、`http_admin_port`、`service_port` または派生ポートを修正します。 |
| `undefined host alias` | YAML の `host` が `cluster.hosts` に定義されているか確認します。 |
| `key_file missing` | SSH キーのパスを確認するか、`cluster.ssh.key_file` を指定します。 |
| `ssh.password ... is not supported` | YAML の password 項目を削除し、鍵ファイルによる SSH 接続を使用します。 |
| `missing cluster.package.origin_path` | `cluster.package.path` または `cluster.package.origin_path` に入力アーカイブのパスを指定します。 |
| `package.path changed but package.name stayed` | 新しいアーカイブには新しい `package.name` を指定します。`origin_path` だけを変更する場合も同じです。 |
| `package already exists` または `File-Name already exists` | 同じアーカイブファイル名が既に登録されています。新しいパッケージなら `package.name` とファイル名を両方変更し、`path` または `origin_path` には Coordinator のパッケージリポジトリではなく元のアーカイブパスを指定します。 |
| `connect target ... must be broker or warehouse alias` | `connect` の対象の別名が Broker または Warehouse か確認します。 |

問題が発生した場合は、まず `--dry-run --verbose` で実行計画と事前検証を確認してください。

```bash
machclusterctl install -f cluster.yaml --dry-run --verbose
machclusterctl apply -f cluster.yaml --dry-run --verbose
machclusterctl upgrade -f cluster.yaml --online --dry-run --verbose
```

## 14. 参考ファイル

- YAML 記述ガイド: [machclusterctl-yaml-guide-en](../machclusterctl-yaml-guide-en/)
- 環境変数を使用するサンプル: [machclusterctl-sample-defaults.yaml](/dbms-8.5/tools-reference/machclusterctl-sample-defaults.yaml)
- 環境変数のサンプル: [machclusterctl-sample-defaults.env.sh](/dbms-8.5/tools-reference/machclusterctl-sample-defaults.env.sh)
- 静的なサンプル: [machclusterctl-sample-defaults-noenv.yaml](/dbms-8.5/tools-reference/machclusterctl-sample-defaults-noenv.yaml)
