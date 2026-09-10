---
type: docs
title: '11.10 データの入力とエクスポート'
weight: 100
toc: true
aliases:
  - /dbms/application-integration/data-input-load-export/
---

SQL、Append API、ファイルツールからデータ量と運用方式に合う経路を選択します。このページは選択と
検証のフローを説明します。全オプションは各ツール・SQLリファレンスを参照してください。

<a id="selection-input-method"></a>

## 入力方式の選択

<a id="selection-input-method-table-types-type"></a>

| 方式 | 適している場合 | 主な確認値 |
|------|-------------|-------------|
| 単一行INSERT | 少量入力、エラーの即時確認 | 影響行数、生成ID |
| preparedバッチ | 同じSQLの繰り返し実行 | 項目別の結果と失敗位置 |
| Append API | 継続的なTAG・LOGの大量収集 | サーバー処理応答、成功・失敗件数 |
| `LOAD DATA INFILE` | サーバーが読み取れるファイルのロード | サーバーファイルの権限、入力件数 |
| `machloader`・`csvimport` | クライアントファイルのロード | ログ・エラー行ファイル、入力・失敗件数 |

<a id="machloader-vs-csvimport-csvexport-tagmetaimport"></a>
<a id="load-data-infile-vs-machloader"></a>

### 経路とツールの比較

| 経路・ツール | 実行場所と用途 |
|---|---|
| SDK Append | アプリケーションから継続的に複数のTAG・LOG行を送信 |
| SQL INSERT | 少量入力と通常のSQL連携 |
| `LOAD DATA INFILE` | サーバーが読み取れるファイルをSQLでロード |
| `machloader` | クライアントファイルのマッピング・ログ・エラー行ファイルを細かく制御 |
| `csvimport`・`csvexport` | 単純なCSV入出力のラッパー |
| `tagmetaimport` | TAGメタデータの一括登録・変更 |

`tagmetaimport`はTAG測定値の入力ツールではありません。正確なオプションは
[コマンドラインツール](/dbms/reference/command-line-tools/)を確認してください。

<a id="selection-input-method-selection-input-method-guide"></a>

元データを保持する必要がある時系列・イベントはTAGまたはLOGに入れます。リレーショナルな変更は
TRANSACTION、小さな参照データはLOOKUP、再生成可能なメモリキャッシュはVOLATILEを使用します。
テーブル選択後、予想件数、許容遅延、再試行単位、重複ポリシーに基づいて入力方式を決めます。

<a id="sql"></a>
<a id="insert"></a>
<a id="sql-insert"></a>

## SQL INSERT

次の例は作成から後片付けまで順番に実行できます。

```sql
CREATE LOG TABLE integration_insert_demo (
    event_time DATETIME,
    sensor_id  VARCHAR(32),
    value      DOUBLE
);

INSERT INTO integration_insert_demo
VALUES (TO_DATE('2026-01-01 00:00:00'), 'TEMP-01', 25.3);

SELECT sensor_id, value
FROM integration_insert_demo;

DROP TABLE integration_insert_demo;
```

アプリケーションでは値をpreparedパラメーターでバインドし、返された影響行数を確認します。

<a id="append"></a>
<a id="sql-append"></a>

## Append API

Appendは各SDKの専用APIでテーブルを開き、複数行を送ってからフラッシュ・クローズするフローです。
列順序と型を対象スキーマに合わせ、接続を通常のクエリと分けます。言語別の完全なコードは
本章のSDK別ページを参照してください。

Machbase DBMS 8.7.0では、Append Open時に入力する列や`ARRAY`要素の対象を選択できます。
行ごとに異なるARRAY位置を入力する場合はSDKのスパースARRAYオブジェクトを使用します。
選択基準、API、検証例は[Sparse ARRAYと選択列Append API](array-append/)を参照してください。

<a id="load-data-infile"></a>
<a id="sql-load-data-infile"></a>

## LOAD DATA INFILE

`LOAD DATA INFILE`はサーバーからアクセスできるファイルをSQLでロードします。
ファイルパスはサーバープロセスの視点で解釈されるため、次の点を確認します。

- サーバーホストにファイルが存在するか
- サーバープロセスのアカウントがファイルを読み取れるか
- 区切り文字、引用文字、エンコーディング、日付形式が元データと一致するか
- 失敗行を識別するログ・エラー行ファイルをどこに保存するか

構文とサポートするオプションは
[LOAD DATA INFILE](/dbms/reference/sql/syntax/load-data-infile-syntax/)を参照してください。

<a id="file"></a>
<a id="file-csv"></a>
<a id="file-file-csv"></a>

## CSVファイルの準備

先頭行をヘッダーにするか決め、全行で列数と順序を統一します。NULL、空文字列、区切り文字を含む文字列、
改行、DATETIME形式をサンプルファイルで先に検証します。大きなファイルは全体実行前に小さなサンプルで
テーブルスキーマと変換規則を確認します。

<a id="import-machloader"></a>
<a id="file-import-machloader"></a>

## machloaderでインポート

基本構文は次のとおりです。

```bash
"$MACHBASE_HOME/bin/machloader"   -s 127.0.0.1 -P 5656   -u APP_USER -p "$MACH_SAMPLE_PASSWORD"   -i -t SENSOR_LOG -d /data/sensor.csv   -l /data/sensor.log -b /data/sensor.bad
```

ヘッダーがある場合は`-H`、区切り文字がカンマ以外なら`-D`、日付形式が異なる場合は`-F`を明示します。
全オプションは[machloader](/dbms/reference/command-line-tools/machloader/)を参照してください。

<a id="import-csvimport"></a>
<a id="file-import-csvimport"></a>

## csvimportでインポート

`csvimport`はmachloaderでよく使うCSVオプションを簡略化したツールです。

```bash
"$MACHBASE_HOME/bin/csvimport"   -s 127.0.0.1 -P 5656   -u APP_USER -p "$MACH_SAMPLE_PASSWORD"   -t SENSOR_LOG -d /data/sensor.csv -H   -l /data/sensor.log -b /data/sensor.bad
```

`-C`の自動作成では、すべての列が意図した業務用の型になるとは限りません。本番ロードは
テーブルを明示的に作成し、スキーマを確認してから実行します。

<a id="export"></a>

## エクスポート方式の選択

| 方式 | 適している場合 |
|------|-------------|
| `SAVE DATA INTO` | SQL条件と検索列を選択してサーバーファイルを作成 |
| `machloader -o` | テーブル単位のエクスポートと詳細オプションの使用 |
| `csvexport` | 単純なCSVエクスポート |
| SDK SELECT | アプリケーションで行を変換・送信する必要がある場合 |

<a id="export-ownership"></a>
<a id="export-export-ownership"></a>

## ファイル所有権とパス

`SAVE DATA INTO`のパスとファイル権限はサーバープロセス基準です。machloaderとcsvexportの
出力ファイルは、ツールを実行したOSユーザー基準です。相対パスを避け、既存ファイルの上書きポリシーと
利用可能なディスク容量を先に確認します。

<a id="export-sql-save-data-into"></a>
<a id="export-export-sql-save-data-into"></a>

## SAVE DATA INTO

SQL条件で結果をエクスポートする際に使用します。本番経路で実行する前に、小さな結果と専用の検証パスで
ファイル作成・エンコーディング・ヘッダーを確認します。全構文は
[SAVE DATA INTO](/dbms/reference/sql/syntax/save-data-into-syntax/)を参照してください。

<a id="export-machloader"></a>
<a id="export-export-machloader"></a>

## machloaderでエクスポート

```bash
"$MACHBASE_HOME/bin/machloader"   -s 127.0.0.1 -P 5656   -u APP_USER -p "$MACH_SAMPLE_PASSWORD"   -o -t SENSOR_LOG -d /data/sensor-export.csv -H   -l /data/sensor-export.log
```

<a id="export-csvexport"></a>
<a id="export-export-csvexport"></a>

## csvexportでエクスポート

```bash
"$MACHBASE_HOME/bin/csvexport"   -s 127.0.0.1 -P 5656   -u APP_USER -p "$MACH_SAMPLE_PASSWORD"   -t SENSOR_LOG -d /data/sensor-export.csv -H   -l /data/sensor-export.log
```

<a id="error-handling"></a>
<a id="batch"></a>
<a id="error-handling-batch"></a>

## バッチ処理

- バッチサイズは行サイズと遅延要件に基づいて負荷テストします。
- 各バッチの入力元オフセットと対象の成功件数を記録します。
- 部分失敗時は、全体の再実行より失敗行だけを分離して再処理します。
- 同じ行を再送しても安全になるよう、業務キーと重複ポリシーを定義します。

<a id="error-handling-bulk"></a>
<a id="error-handling-error-handling-bulk"></a>

## 大量入力のエラー処理

1. ツールの終了コードと集計件数を確認します。
2. ログでサーバーのエラーコードと最初の失敗原因を確認します。
3. エラー行ファイルの列数、型、NULL、日付形式、エンコーディングを元データと比較します。
4. 修正した小さなファイルで再検証し、失敗行だけを再入力します。
5. 対象テーブルの最終件数、時間範囲、サンプル行を確認します。

認証情報や機密の生データがログ・エラー行ファイルに残る可能性があるため、アクセス権と保持期間を設定します。
