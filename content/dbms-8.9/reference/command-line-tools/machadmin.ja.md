---
type: docs
title: '16.4.1 machadmin'
weight: 10
toc: true
---

`machadmin`は、Machbaseサーバーの起動・終了、データベースの作成・削除、実行状態の確認を行う管理ツールです。

## オプション一覧

```bash
machadmin -h
```

| オプション | 説明 |
|------|------|
| `-u`, `--startup` | Machbase サーバーの起動 |
| `--recovery[=simple,complex,reset]` | 起動時の復旧モードの指定（デフォルト値: simple） |
| `-s`, `--shutdown` | Machbaseサーバーの正常終了（graceful） |
| `-k`, `--kill` | Machbaseサーバーの強制終了 |
| `-c`, `--createdb` | Machbase データベースの作成 |
| `-d`, `--destroydb` | Machbase データベースの削除 |
| `-e`, `--check` | サーバーの実行状態確認 |
| `-i`, `--silent` | バナーを表示せずに実行 |
| `-r`, `--restore` | バックアップからデータベースを復元 |
| `-x`, `--extract` | バックアップファイルをバックアップディレクトリに変換 |
| `-w`, `--viewimage` | バックアップイメージファイルの情報を表示 |
| `-t`, `--licinstall` | ライセンスファイルのインストール |
| `-f`, `--licinfo` | インストール済みライセンスの情報を表示 |
| `--home-path=path` | Machbaseホームパスの指定 |

## サーバーの起動

```bash
machadmin -u
```

### 復旧モードの指定

```bash
machadmin -u --recovery=simple    # デフォルトの復旧（正常終了後）
machadmin -u --recovery=complex   # 電源喪失後の再起動時に自動適用
machadmin -u --recovery=reset     # simple/complexによる復旧失敗時に全体を検査
```

| 復旧モード | 説明 |
|----------|------|
| `simple` | 正常終了後の再起動時のデフォルト復旧。実行時間が短い |
| `complex` | 電源喪失などの異常終了後の再起動時に自動適用。`simple`より時間がかかる |
| `reset` | 全テーブルのデータを検査して復旧。一部のデータが失われる可能性がある |

## サーバーの終了

正常終了（実行中の作業が完了してから終了）:

```bash
machadmin -s
```

強制終了（プロセスを即座に終了）:

```bash
machadmin -k
```

## データベースの作成と削除

```bash
# データベースの作成
machadmin -c

# データベースの削除（確認プロンプトを表示）
machadmin -d
```

## サーバーの実行状態確認

```bash
machadmin -e
```

サーバーが実行中の場合はPIDを表示します。

```
Machbase server is already running with PID (14098).
```

サーバーが実行中でなければエラーを表示します。

```
[ERR] Server is not running.
```

## データベースの復元

バックアップディレクトリからデータベースを復元します。

```bash
machadmin -r /path/to/backup
```

例:

```bash
machadmin -r /home/mach/backup/machbase_backup_20240101
```

## ライセンス管理

ライセンスファイルのインストール:

```bash
machadmin -t /path/to/license.dat
```

インストール済みライセンスの情報確認:

```bash
machadmin -f
```

## サイレントモード

バナーと状態メッセージを表示せずに実行します。スクリプトで便利に使用できます。

```bash
machadmin -i -u    # サーバーの起動 (バナーなし)
machadmin -i -s    # サーバーの終了 (バナーなし)
machadmin -i -e    # 状態確認 (バナーなし)
```

## 使用例

```bash
# データベースの初期設定とサーバーの起動
machadmin -c
machadmin -u

# サーバーの状態を確認して終了
machadmin -e
machadmin -s

# ライセンスの更新
machadmin -s
machadmin -t new_license.dat
machadmin -u
```
