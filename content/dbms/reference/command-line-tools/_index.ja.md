---
type: docs
title: '16.4 コマンドラインツールリファレンス'
weight: 40
toc: true
---

Machbaseはサーバー管理、データのインポート/エクスポート、クエリ実行のためのコマンドラインツールを提供します。このセクションでは各ツールのオプションと使用方法を確認できます。

## ツール一覧

| ツール | Edition | 説明 |
|------|--------|------|
| [machadmin](./machadmin/) | Standard / Cluster | サーバーの起動/終了、データベースの作成/削除、ライセンス管理 |
| [machsql](./machsql/) | Standard / Cluster | 対話型SQLターミナル |
| [machloader](./machloader/) | Standard / Cluster | CSVなどのテキストファイルのインポート/エクスポート |
| [csvimport / csvexport](./csvimport-csvexport/) | Standard / Cluster | CSVファイル専用の簡易インポート/エクスポートラッパー |
| [tagmetaimport](./tagmetaimport/) | Standard / Cluster | TAGテーブルのメタデータの一括インポート |
| [machclusterctl](./machclusterctl/) | Cluster | クラスター全体の起動/終了/管理 |
| [machcoordinatoradmin](./machcoordinatoradmin/) | Cluster | Coordinatorノードの管理とクラスター構成 |
| [machdeployeradmin](./machdeployeradmin/) | Cluster | Deployerノードの管理 |

## 共通の接続オプション

次は`machsql`の接続オプションです。オプション名とデフォルト値はツールごとに異なるため、
別のツールではそのオプションリファレンスや`--help`の出力を確認してください。特に、サーバーを
直接管理する`machadmin`のオプションとSQLクライアントの接続オプションを混同しないでください。

| オプション | デフォルト値 | 説明 |
|------|--------|------|
| `-s`, `--server` | 127.0.0.1 | サーバーIPアドレス |
| `-P`, `--port` | 5656 | サーバーポート番号 |
| `-u`, `--user` | SYS | ユーザー名 |
| `-p`, `--password` | MANAGER | ユーザーパスワード |

## ツールの場所

インストールパッケージのツールは`$MACHBASE_HOME/bin/`ディレクトリにあります。
使用できるツールはインストールしたEditionとパッケージによって異なります。

```bash
ls $MACHBASE_HOME/bin/
# machadmin  machsql  machloader  csvimport  csvexport  tagmetaimport  ...
```

PATHに`$MACHBASE_HOME/bin`が登録されていれば、ツール名だけで実行できます。

```bash
export PATH=$MACHBASE_HOME/bin:$PATH
machadmin -e
```
