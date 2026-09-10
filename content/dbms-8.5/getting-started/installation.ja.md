---
type: docs
title: 'インストールガイド'
weight: 20
toc: true
---

Linux と Windows への Standard Edition の導入を説明します。クラスタは [Cluster Edition のインストール](../../installation/cluster/)を参照してください。

## インストール方法の選択 {#choosing-your-installation-method}

**Linux：**
- **tarball（推奨）**：柔軟で、各ディストリビューションで使用可能
- **Docker**：短時間で独立した環境を構築

**Windows：**
- **MSI**：GUI ウィザードで簡単に導入

## Linux へのインストール {#linux-installation}

### 方法 1：tarball（推奨） {#method-1-tarball-installation-recommended}

#### 1．ユーザーの作成（任意、推奨） {#1-create-user-optional-but-recommended}

```bash
sudo useradd machbase
sudo passwd machbase
su - machbase
```

#### 2．ダウンロードと展開 {#2-download-and-extract}

```bash
# パッケージを取得
wget http://machbase.com/dist/machbase-standard-x.x.x.official-LINUX-X86-64-release.tgz

# ディレクトリを作成
mkdir machbase_home
mv machbase-standard-x.x.x.official-LINUX-X86-64-release.tgz machbase_home/
cd machbase_home/

# 展開
tar zxf machbase-standard-x.x.x.official-LINUX-X86-64-release.tgz
```

#### 3．環境変数の設定 {#3-set-environment-variables}

`~/.bashrc` に追加します。

```bash
export MACHBASE_HOME=/home/machbase/machbase_home
export PATH=$MACHBASE_HOME/bin:$PATH
export LD_LIBRARY_PATH=$MACHBASE_HOME/lib:$LD_LIBRARY_PATH
```

変更を反映します。

```bash
source ~/.bashrc
```

#### 4．インストールの確認 {#4-verify-installation}

```bash
machadmin --help
```

Machbase Administration Tool のヘルプが表示されます。

### 方法 2：Docker {#method-2-docker-installation}

```bash
# イメージを取得
docker pull machbase/machbase

# コンテナーを実行
docker run -d --name machbase \
  -p 5656:5656 \
  -v machbase_data:/data \
  machbase/machbase

# コンテナーに接続
docker exec -it machbase machsql
```

詳細は [Docker へのインストール](../../installation/linux/docker-install/)を参照してください。

## Windows へのインストール {#windows-installation}

### MSI インストーラー {#msi-installer}

#### 1．ダウンロード {#1-download}

Machbase のサイトから .msi を取得します。

#### 2．実行 {#2-run-installer}

- .msi をダブルクリック
- ウィザードに従って操作
- インストール先を選択（既定値：`C:\machbase`）
- PATH は自動設定

#### 3．インストールの確認 {#3-verify-installation}

コマンドプロンプトで実行します。

```cmd
machadmin --help
```

詳細は [Windows へのインストール](../../installation/windows/)を参照してください。

## インストール後の操作 {#post-installation-steps}

### 1．データベースの作成 {#1-create-database}

```bash
machadmin -c
```

期待する出力：
```
Database created successfully.
```

### 2．サーバーの起動 {#2-start-server}

```bash
machadmin -u
```

期待する出力：
```
Machbase server started successfully.
```

### 3．稼働状態の確認 {#3-verify-server-is-running}

```bash
machadmin -e
```

または、プロセスを確認します。

```bash
# Linux
ps -ef | grep machbased

# Windows
tasklist | findstr machbased
```

### 4．データベースへの接続 {#4-connect-to-database}

```bash
machsql
```

既定の認証情報：
- **ユーザー名**：SYS
- **パスワード**：MANAGER

## ディレクトリ構成 {#directory-structure}

次のディレクトリが作成されます。

```
machbase_home/
├── bin/           # 実行ファイル（machadmin、machsql など）
├── conf/          # 設定ファイル
├── dbs/           # DB ファイル（machadmin -c 後に作成）
├── lib/           # 共有ライブラリー
├── trc/           # ログファイル
├── sample/        # サンプルファイル
└── doc/           # ドキュメント
```

## 任意の設定 {#configuration-optional}

### ポートの変更 {#change-server-port}

既定のポートは 5656 です。変更方法：

**方法 1：環境変数**

```bash
export MACHBASE_PORT_NO=7878
```

**方法 2：設定ファイル**

`$MACHBASE_HOME/conf/machbase.conf` を編集します。

```ini
PORT_NO = 7878
```

全項目は[設定ガイド](../../configuration/)を参照してください。

## 基本コマンド {#essential-commands}

```bash
# データベースを作成
machadmin -c

# サーバーを起動
machadmin -u

# サーバーを停止
machadmin -s

# 状態を確認
machadmin -e

# データベースを削除（注意）
machadmin -d

# SQL で接続
machsql
```

## ライセンスの導入 {#license-installation}

本番利用にはライセンスを導入します。

```bash
machadmin -t /path/to/license.dat
```

確認方法：

```bash
machadmin -f
```

machsql で確認する場合：

```sql
SHOW LICENSE;
```

評価ライセンスは Machbase のサイトで取得してください。詳細は[ライセンス管理](../../installation/license/)を参照してください。

## システム要件 {#system-requirements}

### 最小要件 {#minimum-requirements}

- **CPU**：x86-64 互換
- **RAM**：1GB
- **ディスク**：ソフトウェア用 100MB とデータ保存領域
- **OS**：
  - Linux：カーネル 2.6 以降
  - Windows：Windows 7 以降

### 本番向け推奨構成 {#recommended-for-production}

- **CPU**：4 コア以上
- **RAM**：8GB 以上
- **ディスク**：性能向上のため SSD
- **OS**：
  - Linux：RHEL 7 以降、Ubuntu 16.04 以降、CentOS 7 以降
  - Windows：Windows Server 2012 以降

## トラブルシューティング {#troubleshooting}

### インストールの問題 {#installation-issues}

**Permission denied（Linux）**

```bash
chmod +x $MACHBASE_HOME/bin/*
```

**Library not found（Linux）**

```bash
ldd $MACHBASE_HOME/bin/machbased
# 不足するライブラリーを導入
```

### 起動の問題 {#server-start-issues}

**ポートが使用中**

```bash
# ポート 5656 の使用状況を確認
netstat -an | grep 5656

# 別のポートを使用
export MACHBASE_PORT_NO=7878
```

**メモリ不足**

`$MACHBASE_HOME/conf/machbase.conf` を確認して調整します。

```ini
MEM_MAX_DB = 2G
```

その他の対処は[トラブルシューティング](../../troubleshooting/)を参照してください。

## 次のステップ {#next-steps}

導入後は、次を参照してください。

1. [**クイックスタート**](../quick-start/)：DB とテーブルの作成
2. [**最初の操作**](../first-steps/)：machsql の基本
3. [**基本概念**](../concepts/)：アーキテクチャー

## 高度なインストール {#advanced-installation}

応用的な構成：

- [Cluster Edition](../../installation/cluster/)
- [高可用性の設定](../../installation/cluster/)
- [アップグレード](../../installation/upgrade/)
