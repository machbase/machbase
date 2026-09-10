---
type: docs
title: '13.3 設定の運用'
weight: 30
toc: true
---

設定変更は、現在値、変更理由、適用方法、検証値、ロールバックを記録し、1項目ずつ行います。
設定プロパティの全一覧とデフォルト値は、現行リリースの
[設定リファレンス](/dbms/reference/configuration/configuration/)を参照してください。

<a id="file-config-configuration"></a>

## 設定ファイル

デフォルトの設定ファイルは `$MACHBASE_HOME/conf/machbase.conf` です。パッケージやサービス構成に
よって別ファイルを使う場合があるため、起動コマンドと実環境を確認します。

変更前に次を記録します。

- ファイルパス、所有者、権限
- 変更対象のファイル内の値と `V$PROPERTY` の現在値
- 単位と許容範囲
- 実行時変更の可否と再起動の要否
- 関連ノード・インスタンスの範囲
- ロールバック値と検証 SQL

パスワード、AUTH KEY、ライセンス内容は、通常の設定バックアップや作業記録に含めないでください。

<a id="alter-start-restart-configuration-runtime"></a>

<a id="runtime-변경과-restart"></a>

## 実行中の変更と再起動

`ALTER SYSTEM SET` で実行時に変更できるのは、対応する一部のプロパティだけです。
文書に例があるという理由で、任意のプロパティを変更しないでください。

```sql
SELECT NAME, VALUE FROM V$PROPERTY ORDER BY NAME;
```

1. 設定リファレンスで動的変更の対応を確認します。
2. メンテナンス範囲と影響する接続・クエリを定めます。
3. 現在値を保存します。
4. 検証環境または限定したワークロードで1項目だけ変更します。
5. 応答時間、スループット、メモリ・I/O、エラーを比較します。
6. 採用する値は設定ファイルにも反映し、再起動後に戻らないようにします。
7. 再起動後、`V$PROPERTY` と機能テストで適用を確認します。

<a id="parameters-configuration"></a>

<a id="property-찾기"></a>

## 設定プロパティの検索

```sql
SELECT NAME, VALUE FROM V$PROPERTY
WHERE NAME LIKE 'PVO_CACHE%' ORDER BY NAME;
```

正確な名前が分かる場合は `NAME = '...'` で検索します。似た名前から推測して設定しないでください。

<a id="memory-configuration"></a>

<a id="memory-설정"></a>

## メモリ設定

プロセス上限、テーブル領域・キャッシュ、入力バッファ、クエリ・セッションの一時メモリを
1つの予算として考えます。OS と同一ホスト上の他プロセスに必要なメモリも確保します。

- 通常・ピーク負荷時の常駐メモリと利用可能メモリ
- スワップの有無と増加時刻
- 同時クエリ・Appender・セッション数
- PVO、Min-Max、LOOKUP・VOLATILE などのキャッシュ使用量
- インデックス作成、ソート、集計などの一時処理

固定比率や例のバイト数をそのまま適用しないでください。

<a id="network-session-configuration"></a>

<a id="network와-session"></a>

## ネットワークとセッション

リスナーのアドレス・ポート、最大セッション数、接続・クエリタイムアウトは、アプリケーション接続数と
障害分離要件を基準に決めます。ファイアウォールとバインドは別々に検証し、セッション上限を増やす前に
接続リークとプール設定を確認します。

```sql
SELECT ID, USER_NAME, USER_IP, LOGIN_TIME, CLIENT_TYPE
FROM V$SESSION ORDER BY LOGIN_TIME DESC;
```

<a id="storage-checkpoint-configuration"></a>

<a id="storage와-checkpoint"></a>

## ストレージとチェックポイント

`DBS_PATH`、チェックポイント、direct I/O、I/O スレッドの設定は、データの場所と復旧時間に直接影響します。
運用データファイルを手動で移動したり、別のパスを推測したりしないでください。

- 実際のデータ・バックアップパスとファイルシステムを確認します。
- 同じ期間のチェックポイント時間とデバイス遅延を比較します。
- 再起動が必要な設定には、サービス停止・復旧手順を準備します。
- 変更後に正常な再起動、バックアップ、リストアを検証します。

<a id="timezone"></a>

## タイムゾーン

時刻文字列の入力・表示に使うタイムゾーンを、サーバー、コマンドラインツール、SDK で一貫して設定します。
epoch の単位と `DATETIME` の精度は別に確認し、同じ値を入力して読み出す往復テストを行います。

<a id="timezone-server-configuration"></a>
<a id="timezone-timezone-server-configuration"></a>

<a id="server-timezone"></a>

## サーバーとセッションのタイムゾーン

サーバーのデフォルトタイムゾーンと、クライアントが選択したセッションタイムゾーンを区別します。
アプリケーションの文字列入出力基準は対応する接続オプションで明示し、新しい接続の `SHOW TIMEZONE` と
サンプル `DATETIME` クエリで確認します。設定方法は
[タイムゾーン設定](/dbms/reference/configuration/configuration-timezone/)を参照してください。
既存接続のセッション設定は自動では変わりません。

<a id="machsql-z"></a>
<a id="timezone-machsql-z"></a>

## machsql `-z`

```bash
"$MACHBASE_HOME/bin/machsql"   -s 127.0.0.1 -P 5656   -u APP_USER -p "$MACH_SAMPLE_PASSWORD"   -z +0900
```

入力・出力文字列が指定したオフセットで解釈・表示されることをサンプルで確認します。

<a id="machloader-z"></a>
<a id="timezone-machloader-z"></a>

## machloader `-z`

```bash
"$MACHBASE_HOME/bin/machloader"   -s 127.0.0.1 -P 5656   -u APP_USER -p "$MACH_SAMPLE_PASSWORD"   -z +0900 -i -t SENSOR_LOG -d /data/sensor.csv
```

元の CSV のタイムゾーンと日時形式を併せて文書化します。

<a id="connection-cli-jdbc-net-timezone"></a>
<a id="timezone-connection-cli-jdbc-net-timezone"></a>

<a id="sdk-connection-timezone"></a>

## SDK 接続のタイムゾーン

対応オプション名は SDK によって異なります。[11章 開発とアプリケーション連携](/dbms/development-tools-integration/)
でドライバーの接続オプションを確認し、入力・クエリ・接続プールの再利用後も同じタイムゾーンが
適用されることを検証します。

## 変更記録

| 項目 | 記録 |
|------|------|
| 対象 | ホスト、インスタンス、ノード、データベース |
| 変更 | プロパティと変更前後の値 |
| 根拠 | 基準値と目標 |
| 適用 | 実行時または再起動 |
| 検証 | SQL、ワークロード、OS 指標 |
| ロールバック | 値、実行順序、担当者 |

未確認の推奨値や旧リリースのデフォルト値を、現在の設定として扱わないでください。
