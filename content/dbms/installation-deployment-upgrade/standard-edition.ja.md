---
type: docs
title: '3.2 Standard Editionのインストール'
weight: 20
toc: true
---
Standard Editionは1台のサーバーでSQL処理とデータ保存を実行します。インストールは、パッケージの準備、
サーバー実行環境の設定、データベース作成、ライセンス確認、起動、SQL検証の順に進めます。
単一サーバーでも少量データだけを扱うわけではなく、スループットと保持期間に必要なリソースを
実際のワークロードで確認する必要があります。

## インストール経路

OSに応じて次の経路から選択します。

| OS | インストール方式 | リンク |
|----|-----------|------|
| Linux | Tarball (.tgz) | [Tarballインストール](/dbms/installation-deployment-upgrade/standard-edition/#linux-tarball) |
| Linux | Dockerコンテナー | [Dockerインストール](/dbms/installation-deployment-upgrade/standard-edition/#linux-docker) |
| Windows | ZIPまたはインストーラー実行ファイル | [Windowsパッケージインストール](/dbms/installation-deployment-upgrade/standard-edition/#windows-package) |

事前に[Linux環境の準備](/dbms/installation-deployment-upgrade/standard-edition/#linux-preparation-environment-linux)または
[Windows環境の準備](/dbms/installation-deployment-upgrade/standard-edition/#windows-preparation-environment-windows)を確認してください。

---

<a id="linux"></a>

## Linuxへのインストール

LinuxでStandard Editionをインストールする方法は2つあります。

| 方式 | 適している状況 |
|------|------------|
| [Tarballインストール](/dbms/installation-deployment-upgrade/standard-edition/#linux-tarball) | 実サーバー環境、データディレクトリを直接管理する場合 |
| [Dockerインストール](/dbms/installation-deployment-upgrade/standard-edition/#linux-docker) | 開発・テスト環境、すぐに起動する必要がある場合 |

Tarballのインストールは[インストール前の準備](../pre-install-preparation/)を先に完了します。
DockerではDocker Engineとボリューム・ポートの権限を準備してください。

---

<a id="linux-preparation-environment-linux"></a>

### Linux環境の準備

ファイルディスクリプター上限、時刻同期、ポート予約、ファイアウォール設定はEdition共通です。
[インストール前の準備](../pre-install-preparation/)でサーバー実行アカウントと運用環境に合わせて
設定してから、次の手順に進みます。

---

<a id="linux-tarball"></a>

### Tarballインストール

Linux環境にtarball（.tgz）を展開してStandard Editionをインストールする手順です。

#### 1. ユーザーの作成

Machbase専用のOSユーザーを作成します。

```bash
sudo useradd -m -d /home/machbase machbase
sudo passwd machbase
```

以降は`machbase`アカウントでログインして作業します。

#### 2. パッケージのダウンロードと展開

例ではパッケージを`/home/machbase/packages/`にダウンロード済みとします。以下のパッケージ名を
実際の配布物に置き換え、インスタンスがまだない新しいインストールディレクトリに展開します。
既存インストールの更新は[アップグレード](../upgrade/)手順を使用します。

```bash
machbase_package=/home/machbase/packages/machbase-SDK-8.7.0.official-LINUX-X86-64-release.tgz
test -r "$machbase_package" &&
mkdir /home/machbase/machbase_home &&
tar zxf "$machbase_package" -C /home/machbase/machbase_home &&
cd /home/machbase/machbase_home
```

展開後にディレクトリ構造を確認します。

```bash
ls -l
# bin/  conf/  dbs/  doc/  include/  lib/  trc/  ...
```

#### 3. 環境変数の設定

`~/.bashrc`に環境変数を追加します。

```bash
export MACHBASE_HOME=/home/machbase/machbase_home
export PATH="$MACHBASE_HOME/bin:$PATH"
export LD_LIBRARY_PATH="$MACHBASE_HOME/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
```

適用します。

```bash
source ~/.bashrc
```

#### 4. データベースの作成

`machadmin -c`は物理インスタンスのデータベースファイルを作成します。SQLの`CREATE DATABASE`で
論理データベースを追加する操作とは区別してください。実行前に`MACHBASE_HOME`、`conf/machbase.conf`、
実際の`DBS_PATH`が新規インストールの対象か確認します。既存データベースがあるというエラーの場合は、
削除・再作成せず、まず対象パスを確認します。

```bash
machadmin -c
# Database created successfully.
```

#### サーバー起動前の設定とライセンス確認

`conf/machbase.conf`の`PORT_NO`と`DBS_PATH`を確認します。別途ライセンスを使用する場合は、
[ライセンスのインストール](../pre-install-preparation/#license)のファイルコピーまたは`machadmin -t`で
インストールし、`machadmin -f`で確認してから起動します。

#### 5. サーバーの起動

```bash
machadmin -u
# Machbase server started successfully.
```

プロセスの確認:

```bash
machadmin -e
```

#### 6. 接続テスト

`machsql`でサーバーに接続します。デフォルトの管理者アカウントは`SYS / MANAGER`です。

```bash
machsql
# Machbase server address (Default:127.0.0.1) :
# Machbase user ID  (Default:SYS)
# Machbase User Password :
# MACHBASE_CONNECT_MODE=INET, PORT=5656 EDITION=STANDARD
# Mach>
```

簡単なテストを行います。

```sql
CREATE LOG TABLE install_check (id INTEGER, val DOUBLE);
INSERT INTO install_check (id, val) VALUES (1, 3.14);
SELECT id, val FROM install_check;
DROP TABLE install_check;
```

`id=1`、`val=3.14`の1行が返り、最後のDROPが成功することを確認します。
`install_check`がすでに存在する場合は削除せず、未使用の実習用名に置き換えます。

#### サーバーの終了

インストール確認後、サーバーを停止する必要がある場合のみ実行します。

```bash
machadmin -s
# Machbase server shut down successfully.
```

#### ポートの変更

デフォルトポート（5656）を変更するには、`$MACHBASE_HOME/conf/machbase.conf`の`PORT_NO`を変更するか、
環境変数を設定します。

```bash
export MACHBASE_PORT_NO=7878
```

サーバーを終了した状態で設定を適用し、再起動します。この環境変数は現在のシェルだけに適用されるため、
サービスとして起動する場合はサービスの環境にも反映します。接続には
`machsql -s 127.0.0.1 -P 7878 -u SYS`のように変更したポートを指定します。

---

<a id="linux-docker"></a>

### Dockerインストール

Dockerイメージではサーバーと実行環境をコンテナーとしてデプロイできます。開発・テスト環境でも、
ホストのDocker Engine、保存ボリューム、ポート、ファイルディスクリプター上限を準備する必要があります。

Dockerを事前にインストールしてください。デプロイチュートリアルは`machbase/machbase`イメージを使用します。
ソースからDockerイメージを直接ビルドした場合は、ローカルイメージ名（`machbase:latest`など）に置き換えます。

#### イメージの確認

```bash
docker pull machbase/machbase
docker image ls machbase/machbase
```

#### コンテナーの実行

```bash
docker create \
  --name machbase \
  --ulimit nofile=65535 \
  -p 5656:5656 \
  -v /data/machbase:/home/machbase/machbase/dbs \
  machbase/machbase
```

| オプション | 説明 |
|------|------|
| `-p 5656:5656` | ホストSQLポート:コンテナーSQLポートのマッピング |
| `--ulimit nofile=65535` | コンテナー内のサーバーのファイルディスクリプター上限 |
| `-v /data/machbase:...` | データディレクトリをホストに保持するボリュームマウント |

データがコンテナーの書き込み層だけにあると、コンテナー削除時に一緒に削除されます。
実際のデータパスがボリュームに接続されているか確認し、ボリューム自体の削除やディスク障害に備えて
バックアップも準備します。

`docker create`はまだサーバーを起動しません。`/data/machbase`にはコンテナーのサーバー実行アカウントが
書き込める必要があります。既存DBファイルがある場合は、バージョンとインスタンスが合うか確認します。
イメージの実バージョンと`MACHBASE_HOME`パスを確認し、本番では検証済みのイメージタグまたはダイジェストを
固定します。タグなしの公開イメージが常に8.7.0とは考えないでください。

別途ライセンスを使用する場合は、起動前に準備したファイルを次のようにコピーします。

```bash
docker cp /path/to/license.dat machbase:/home/machbase/machbase/conf/license.dat
```

準備ができたらコンテナーを起動します。

```bash
docker start machbase
```

#### コンテナー状態の確認

```bash
docker ps
docker logs machbase
```

#### 接続テスト

##### machsql（コンテナー内部）

```bash
docker exec -it machbase machsql
# Mach>
```

##### ホストからの接続

ホストにmachsqlがインストールされている場合:

```bash
machsql -s 127.0.0.1 -P 5656 -u SYS -p MANAGER
```

#### コンテナーの終了と再起動

```bash
docker stop machbase
docker start machbase
```

#### ライセンスのインストール

実行中にライセンスを更新する場合は、コンテナーにファイルをコピーしてからライセンスインストールコマンドを
実行します。コンテナーの設定ファイルとライセンスはデータボリュームとは別のため、コンテナー再作成時にも
再適用できるよう元のファイルを保持します。

```bash
docker cp /path/to/license.dat machbase:/tmp/license.dat
docker exec machbase machadmin -t /tmp/license.dat
docker exec machbase machadmin -f
```

---

<a id="windows"></a>

## Windowsへのインストール

### インストール前の確認

- **対応OS**: 提供されたWindowsパッケージのリリース情報で対応バージョンを確認します。
- **アーキテクチャー**: パッケージのビット数とOSのアーキテクチャーが一致する必要があります。

先に[Windows環境の準備](/dbms/installation-deployment-upgrade/standard-edition/#windows-preparation-environment-windows)を
完了してください。

### インストール方式

| 方式 | 説明 |
|------|------|
| [Windowsパッケージインストール](/dbms/installation-deployment-upgrade/standard-edition/#windows-package) | インストールウィザードで環境変数とショートカットを作成 |

---

<a id="windows-preparation-environment-windows"></a>

### Windows環境の準備

Windowsにインストールする前にファイアウォール設定を確認します。

#### ファイアウォールのポートを開く

Machbaseが使用するポートを、Windowsファイアウォールの受信規則に追加します。

| ポート | プロトコル | 用途 |
|------|---------|------|
| 5656 | TCP | SQLクライアント接続 |

##### 設定方法

1. **コントロールパネル → Windows Defenderファイアウォール → 詳細設定**を開きます。

2. 左ペインの**受信の規則**を選び、右ペインで**新しい規則**をクリックします。

3. 規則の種類に**ポート**を選び、**次へ**をクリックします。

4. **TCP**を選び、**特定のローカルポート**に`5656`を入力して**次へ**をクリックします。

5. **接続を許可する**を選び、**次へ**をクリックします。

6. 接続を許可するネットワークプロファイル（**ドメイン**、**プライベート**、**パブリック**）だけを選び、**次へ**をクリックします。

7. 規則名（例: `Machbase`）を入力し、**完了**をクリックします。

規則の作成後、プロパティのリモートアドレス範囲も実際のクライアントアドレスに制限します。
リモート接続を使用しない環境では、受信許可規則は不要です。

##### PowerShellで設定（管理者権限）

GUIの代わりにPowerShellですばやく設定します。

```powershell
New-NetFirewallRule -DisplayName "Machbase SQL" -Direction Inbound -Protocol TCP -LocalPort 5656 -Action Allow
```

#### Visual C++再頒布可能パッケージ

実行にはVisual C++ Redistributableが必要です。インストーラーでは自動処理される場合がありますが、
問題が発生した場合はMicrosoft公式サイトから最新バージョンを手動インストールしてください。

---

<a id="windows-package"></a>

### Windowsパッケージインストール

Windows版はZIPパッケージまたはインストーラー実行ファイルで提供されます。ZIPはアーカイブルートに
`bin\`、`conf\`、`dbs\`、`trc\`などを含み、インストーラーはインストールパス配下に`machbase_home\`を
作成して環境変数と実行ショートカットを生成します。

#### インストール手順

1. Windows配布パッケージをダウンロードします。

2. ZIPパッケージの場合は、目的のインストールディレクトリに展開します。

   ```cmd
   mkdir C:\machbase
   tar -xf machbase-SDK-8.7.0.official-WINDOWS-X86-64-release.zip -C C:\machbase
   ```

3. インストーラーが提供された場合は実行します。開始画面が表示されたら**Next**をクリックします。

4. インストールパスを選びます。デフォルトは`C:\machbase-<short_version>\`形式です。
   変更が必要ならパスを修正して**Next**をクリックします。

5. インストールが進み、完了したら**Next** → **Close**をクリックします。

#### ZIPパッケージの初期化

ZIPを展開した場合は、コマンドプロンプトでそのディレクトリをインストールホームに指定します。
以下は`C:\machbase`へ新規インストールした例です。実際の設定ファイルとライセンスを先に確認し、
既存DBのない新規インスタンスだけで`-c`を実行します。

```cmd
set "MACHBASE_HOME=C:\machbase"
set "PATH=%MACHBASE_HOME%\bin;%PATH%"
machadmin.exe -c
machadmin.exe -f
machadmin.exe -u
machadmin.exe -e
```

上記の`set`は現在のウィンドウに適用されます。他のウィンドウやサービスから実行する場合も、
同じインストールホームと実行ファイルパスを使用する必要があります。インストーラーがすでにデータベースを
作成した場合は、ZIP用の作成コマンドを繰り返さないでください。

#### サーバーの起動と終了

インストーラーを使用すると、デスクトップとスタートメニューにショートカットが作成されます。

- **start Machbase**: `machadmin.exe -u`でサーバーを起動します。
- **stop Machbase**: `machadmin.exe -s`でサーバーを終了します。
- **machsql**: SQLコンソールを起動します。

#### コマンドライン接続

インストール後、コマンドプロンプトで`machsql`を実行してサーバーに接続します。インストーラーを使用した
場合は`<インストールパス>\machbase_home\bin`がシステムの`PATH`に追加されます。ZIPの場合は展開先の
`bin\`を`PATH`に追加するか、フルパスで実行します。

```cmd
machsql -s 127.0.0.1 -P 5656 -u SYS -p MANAGER
```

デフォルトの管理者アカウント: `SYS` / `MANAGER`

#### インストールパスの構造

ZIPパッケージは展開先直下に`bin\`、`conf\`、`dbs\`、`trc\`などを配置します。
インストーラーはインストールパス配下の`machbase_home\`に同じ構成を作成します。
[パッケージ構成](/dbms/installation-deployment-upgrade/pre-install-preparation/#package)を参照してください。
