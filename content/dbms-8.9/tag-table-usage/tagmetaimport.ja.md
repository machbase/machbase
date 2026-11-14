---
type: docs
title: '5.12 tagmetaimportとメタデータの一括登録'
weight: 120
toc: true
---

<a id="metadata-import-tagmetaimport-tag"></a>

## tagmetaimportによるメタデータの登録

`tagmetaimport`はCSVのタグ名とユーザーメタデータをインポートするツールです。
通常のSQLの論理TAG名と`-t`の入力先を区別する必要があります。現在のラッパーは`-t`を
machloaderに渡します。以下の論理テーブル`ch5_meta_import`のメタデータ入力先は
`_CH5_META_IMPORT_META`です。`-t ch5_meta_import`が自動的にMETADATAを選択すると
考えないでください。

この名前はツールの対象指定に使用します。SQLの検索・変更には`ch5_meta_import METADATA`を
使用し、ストレージオブジェクトを直接変更する手順に拡張しないでください。デフォルトの対象に
依存せず、`-t`を明示します。

## 1. テーブルの準備

既存オブジェクトのない実習用データベースで次のSQLを実行します。

```sql
CREATE TAG TABLE ch5_meta_import (
    name VARCHAR(40) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE
) METADATA (
    location VARCHAR(40),
    status VARCHAR(20)
);
```

## 2. CSVの準備

次の内容をクライアントの`ch5_metadata.csv`に保存します。

```csv
name,location,status
TEMP_001,Building-A/F1,READY
TEMP_002,Building-A/F2,STOP
TEMP_003,Building-B/F3,READY
```

ファイルにはタグ名に続いてMETADATAの宣言順で値を記載します。DATAのtime・valueと
システム列`_ID`・`_LAST_UPDATE_TIME`は含めません。ヘッダーがある場合は`-H`を指定します。
ヘッダーが任意の列順序を自動的に対応付けるとは考えないでください。

## 3. 入力と結果の確認

アドレス・アカウントを実際の実習用サーバーに合わせ、使用する8.7.0パッケージの`MACHBASE_HOME`と
ライブラリ環境で実行します。

```bash
tagmetaimport -s 127.0.0.1 -P 5656 -u SYS -p MANAGER \
  -t _CH5_META_IMPORT_META -d ch5_metadata.csv -H \
  -l ch5_import.log -b ch5_import.bad
```

初回実行の期待結果は成功3件・失敗0件です。以下のMETADATA検索は3行を返し、DATAのCOUNTは0です。
メタデータ登録と測定値の入力は異なります。

```sql
SELECT name, location, status, _last_update_time
  FROM ch5_meta_import METADATA ORDER BY name;
SELECT COUNT(*) FROM ch5_meta_import;
```

## 4. 既存タグと再実行

同じファイルを再入力しても既存タグは自動更新されません。現在の経路は通常のMETADATA INSERTのため、
重複タグはエラー行として集計されます。2回目の実行の期待結果は成功0件・失敗3件で、既存属性は
維持されます。終了ステータスだけでなく、成功・失敗件数とbad/logファイルをまとめて確認します。

新しい行と不正な行が混在するファイルでも、全体が1つのトランザクションになるとは考えません。
反映済みのタグを確認し、失敗行だけを修正して再処理します。既存属性は明示的なUPDATEまたは
サポートされるUPSERTで変更します。

```sql
UPDATE ch5_meta_import METADATA SET status = 'DONE' WHERE name = 'TEMP_001';
INSERT INTO ch5_meta_import METADATA VALUES ('TEMP_002', 'Building-C/F2', 'READY')
ON DUPLICATE KEY UPDATE;
SELECT name, location, status FROM ch5_meta_import METADATA ORDER BY name;
```

TEMP_001はDONEに、TEMP_002はBuilding-C/F2・READYに変わります。
実際に値が変わると変更時刻が更新され、同じ値のno-opでは維持されます。
`tagmetaimport`に自動UPSERTオプションがあると解釈しないでください。

## 後片付けと関連ドキュメント

結果の確認後、`DROP TABLE ch5_meta_import;`で今回の実習テーブルだけを削除します。
CSV・ログ・badファイルは、再処理に不要であることを確認してから削除します。

詳細なオプションは[tagmetaimportコマンドリファレンス](../../reference/command-line-tools/tagmetaimport/)、
SQLでの登録・変更規則は[TAGメタデータ](../tag-metadata/)を参照してください。
