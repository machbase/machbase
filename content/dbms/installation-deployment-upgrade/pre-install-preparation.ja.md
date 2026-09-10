---
type: docs
title: '3.1 インストール前の準備'
weight: 10
toc: true
---
インストール前の準備では、実行ファイルのコピー先だけでなく、データの保存先、サーバーの実行アカウント、
クライアントの接続経路を確定します。パッケージとOSの互換性を確認してから、ストレージ、ネットワーク、
ライセンスを準備します。サポート範囲は提供されたパッケージのリリース情報と技術サポートポリシーで判断します。

## 先に決めるデプロイ情報

| 項目 | 決定事項 | 必要な理由 |
|---|---|---|
| Editionとバージョン | StandardまたはCluster、サーバー・SDKバージョン | 使用するSQL機能とデプロイ方式の決定 |
| OSアカウント | サーバー実行アカウントとファイル所有者 | 設定・データ・ログのパスのアクセス権を合わせる |
| インストールホーム | 実行ファイルと設定がある絶対パス | 管理コマンドが操作するインスタンスを識別 |
| データパス | 実際の`DBS_PATH`、ファイルシステム、空き容量 | 再起動・アップグレード時に保持するデータを識別 |
| 接続情報 | サーバーアドレス、SQLポート、管理ポート、許可クライアント | ポート競合と誤ったインスタンスへの接続を防止 |
| 復旧とライセンス | バックアップ保存先、復元手順、使用ライセンス | 障害対応と運用範囲の確認 |

OSアカウント`machbase`とDBユーザー`SYS`は異なります。前者はプロセス・ファイルの権限、後者は
SQL接続とデータベース操作の権限を決めます。サーバー起動が成功しても、ファイル権限やSQL権限が
適切でなければロード・バックアップなどが失敗する場合があります。

| 項目 | 説明 |
|------|------|
| [インストール前の要件](/dbms/installation-deployment-upgrade/pre-install-preparation/#pre-install-requirements) | OSバージョン、ハードウェア最小要件、ネットワークポート |
| [パッケージ構成の理解](/dbms/installation-deployment-upgrade/pre-install-preparation/#package) | パッケージファイルの命名規則、ディレクトリ構造、主な実行ファイル |
| [ライセンスのインストール](/dbms/installation-deployment-upgrade/pre-install-preparation/#license) | license.datの配置方法、ライセンス状態の確認方法 |

---

<a id="pre-install-requirements"></a>

## インストール前の要件

### OSとパッケージ

OSの種類とCPUアーキテクチャーはパッケージの表記と一致する必要があります。対応OSと最小バージョンは
リリースごとに変わる場合があるため、固定的なバージョン表ではなく、パッケージ付属のリリース情報で
確認してください。

### システムリソース

CPU、メモリ、ディスク、ネットワークの必要量は、入力レート、保持期間、インデックス、ROLLUP構成により
異なります。インストール領域だけでなく、予想される生データ、バックアップ、運用上の空き容量を含めて
算定し、実際のワークロードで容量とスループットを検証してください。秒間行数と保持期間から元の行数を
予測し、代表データをロードして行サイズ・圧縮・インデックスの実際の保存コストを測定します。
Clusterではレプリカ領域も含めます。同じディスクの別ディレクトリは、別の障害ドメインや独立した
I/Oデバイスではありません。

### デフォルトポート

| ポート | 用途 |
|------|------|
| **5656** | SQLクライアント接続（Native TCP） |

SQLクライアントポートの変更には、`$MACHBASE_HOME/conf/machbase.conf`の`PORT_NO`を設定します。
`MACHBASE_PORT_NO`環境変数も使用するため、サーバーを起動するシェルやサービスの環境変数も確認します。
変更したポートはクライアントにも明示し、実行中のサーバーに新しい環境変数が遡及適用されるとは考えません。

ファイアウォール環境では上記ポートの受信を許可する必要があります。Cluster EditionではCoordinatorの
link/adminポートと、Broker、Warehouse、Deployerのポートも追加で開く必要があります。

### システムカーネルパラメーター（Linux）

Linuxへのインストールでは、事前に以下を確認します。

#### ファイルディスクリプターの上限

多数のファイルを同時に開くワークロードでは、ファイルディスクリプターの上限が低いとボトルネックになる
場合があります。デフォルトの上限はOSとアカウント設定によって異なるため、サーバー実行アカウントで確認します。

```bash
# 現在値を確認
ulimit -Sn
```

このインストール例は65535を使用します。上限がこれより小さい場合は`/etc/security/limits.conf`を
変更し、新しいログインセッションで適用を確認します。

```
*  hard  nofile  65535
*  soft  nofile  65535
```

サーバー実行アカウントで再ログインして値を確認します。サービスマネージャーからサーバーを起動する場合は、
そのサービスのファイルディスクリプター上限も別途確認します。

```bash
ulimit -Sn
# 出力: 65535
```

#### ポートの予約

MachbaseサービスのポートがOSの一時ポートの自動割り当てに使われないよう予約します。
この設定は、別プロセスによる同じポートの明示的な使用までは防止しません。

```bash
current=$(cat /proc/sys/net/ipv4/ip_local_reserved_ports)
ports=5656
sudo sysctl -w net.ipv4.ip_local_reserved_ports="${current:+$current,}$ports"
```

既存の予約ポートがある場合は上書きせず、カンマで区切って統合します。永続化するには
`/etc/sysctl.conf`の`net.ipv4.ip_local_reserved_ports`項目と次の値を統合します。

```
net.ipv4.ip_local_reserved_ports = 5656
```

### 時刻同期

時系列データを処理するため、サーバー時刻は正確である必要があります。NTPまたは`chrony`で
システム時刻を同期してください。Cluster Editionは全ノードの時刻を合わせる必要があります。

```bash
# タイムゾーンを確認
ls -l /etc/localtime
date
```

---

<a id="package"></a>

## パッケージ構成の理解

### パッケージファイルの命名規則

パッケージのファイル名はEditionに応じて次の形式です。

```
machbase-EDITION-VERSION-OS-CPU-BIT-MODE.EXT
```

| 項目 | 説明 | 例 |
|------|------|------|
| EDITION | Editionの区分 | `SDK`、`cluster` |
| VERSION | バージョン（Major.Minor.Fix.AUX） | `8.7.0.official` |
| OS | オペレーティングシステム | `LINUX`、`WINDOWS` |
| CPU | CPUアーキテクチャー | `X86` |
| BIT | アーキテクチャーのビット数 | `64` |
| MODE | ビルドモード | `release` |
| EXT | 拡張子 | `tgz`（Linux）、`zip`またはインストーラー実行ファイル（Windows） |

Standard EditionのLinux tarballは`machbase-SDK-...tgz`という名前で生成されます。

例:

- Standard Edition: `machbase-SDK-8.7.0.official-LINUX-X86-64-release.tgz`
- Cluster Edition: `machbase-cluster-8.7.0.official-LINUX-X86-64-release.tgz`

マイナーバージョンが異なると、DBファイルやプロトコルの互換性が変わる場合があります。
Fixバージョン変更も含む実際のアップグレード経路は、対象リリースの互換性情報と
[アップグレード手順](../upgrade/)で確認します。

### インストールディレクトリの構造

tarballを展開すると、`$MACHBASE_HOME`配下に次の構造が作成されます。

```
$MACHBASE_HOME/
├── bin/        実行ファイル
├── conf/       設定ファイル（machbase.confなど）
├── dbs/        データ保存領域
├── doc/        ライセンス文書
├── include/    C/C++ヘッダーファイル
├── install/    Makefile用mkファイル
├── lib/        共有ライブラリ
├── package/    Cluster Editionの追加パッケージパス
├── sample/     サンプルファイル
├── trc/        サーバーログとトレースファイル
├── tutorials/  チュートリアル
├── utility/    ユーティリティファイル
└── 3rd-party/  Grafanaプラグインなど
```

### 主な実行ファイル

| 実行ファイル | 説明 |
|-----------|------|
| `machbased` | サーバーデーモン |
| `machadmin` | サーバー管理（起動・終了・DB作成） |
| `machsql` | CLIクエリツール |
| `machloader` | 大容量ファイルのロード・抽出ツール |
| `csvimport` | CSVファイルのインポート |
| `csvexport` | CSVファイルのエクスポート |
| `tagmetaimport` | TAGメタデータの一括登録 |

Cluster Editionパッケージには`machcoordinatoradmin`、`machdeployeradmin`などの管理ツールが追加されます。
`machclusterctl`は、そのツールを含めてビルドされたパッケージで使用できます。

### 設定ファイル

`$MACHBASE_HOME/conf/`配下にはEdition別のサンプル設定があります。

```bash
ls $MACHBASE_HOME/conf/
# machbase.conf
# machbase.conf.sample.standard
# machbase.conf.sample.edge
# machloader.conf.sample
```

実際に使用するファイルは`machbase.conf`です。Standard fullパッケージはビルド時に
`machbase.conf.sample.standard`をコピーし、`machbase.conf`を含めます。実ファイルがないパッケージでは、
Editionに合うサンプルをコピーして変更します。

Standard/Edgeのサンプルには、TRANSACTIONの書き込み競合と耐久性ポリシーを制御する
`TRANSACTION_BUSY_TIMEOUT_MS`、`TRANSACTION_SYNCHRONOUS`、`TRANSACTION_JOURNAL_MODE`が含まれます。
TRANSACTIONテーブルを使用する場合はまずデフォルト値を使用し、同時書き込みと耐久性の要件を検討してから
調整します。

---

<a id="license"></a>

## ライセンスのインストール

ライセンスファイルがない場合、サーバーはデフォルトの`COMMUNITY`ライセンス情報を使用します。
インストール前に、この範囲が予定する機能・容量に合うか確認します。別のライセンスが必要な環境では、
初回サーバー起動前にファイルを準備します。起動できるだけで本番に必要なライセンス条件を満たしたと
判断しないでください。

### ライセンス状態の確認

インストールしたライセンスの状態と制限違反の有無は、`V$LICENSE_INFO`の`VIOLATE_STATUS`と
`VIOLATE_MSG`で確認します。ライセンスファイルの本文は変更しないでください。

### インストール方法

#### 方法1: ファイルのコピー（サーバー起動前）

`license.dat`を`$MACHBASE_HOME/conf/`にコピーします。サーバー起動時に自動認識されます。

```bash
cp license.dat $MACHBASE_HOME/conf/license.dat
```

#### 方法2: machadminコマンド

`machadmin`でライセンスファイルを検証してインストールします。サーバーが実行中の場合は、
ライセンス再読み込み要求も送信します。

```bash
machadmin -t /path/to/license.dat
```

#### 方法3: SQLクエリ（サーバー実行中）

サーバーが実行中の場合は、machsqlのクエリでインストールします。

```sql
ALTER SYSTEM INSTALL LICENSE = '/path/to/license.dat';
```

### インストールの確認

#### machadminで確認

```bash
machadmin -f
```

#### V$LICENSE_INFOビューの検索

```sql
SELECT ID, ISSUE_DATE, TYPE, CUSTOMER, VIOLATE_STATUS, VIOLATE_MSG
FROM V$LICENSE_INFO;
```

`VIOLATE_STATUS`が0なら正常です。

machsqlでは次のコマンドでもライセンス情報を確認できます。

```sql
SHOW LICENSE;
```
