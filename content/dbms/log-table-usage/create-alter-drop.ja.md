---
type: docs
title: '7.3 作成、変更、削除'
weight: 30
toc: true
---

カラム追加のSQLは短くても、運用では既存行に表示される値と、既存の入力プログラムが引き続き動作するかを確認する必要があります。
この節では、データがある状態でスキーマを変更し、その結果を確認します。

<a id="original-85-creating-log-tables"></a>

<a id="log라고-명시해서-만듭니다"></a>

## LOGテーブルの作成

テーブル型を省略した`CREATE TABLE`はTRANSACTIONテーブルを作成します。
この実習では`CREATE LOG TABLE`を使用してください。

```sql
CREATE LOG TABLE ch7_ddl (
    event_id INTEGER,
    category VARCHAR(32),
    severity SHORT,
    message  VARCHAR(128)
);
INSERT INTO ch7_ddl VALUES (1, 'network', 3, 'connection timeout');
```

<a id="create-log-schema-rules"></a>

自動カラム`_arrival_time`はDDLに再宣言しません。
実際の発生時刻が必要なら、別のDATETIMEカラムを用意してください。
LOGではPRIMARY KEY・UNIQUE制約をサポートしていません。

<a id="alter-log-table"></a>

<a id="기존-행에서-새-컬럼-값을-확인합니다"></a>

## カラム追加とデフォルト値

```sql
ALTER TABLE ch7_ddl ADD COLUMN (host_name VARCHAR(64));
ALTER TABLE ch7_ddl ADD COLUMN (source_kind VARCHAR(16) DEFAULT 'agent');
ALTER TABLE ch7_ddl ADD COLUMN (channels INT32[3] DEFAULT [1, NULL, 3]);

SELECT event_id, host_name, source_kind, channels
  FROM ch7_ddl
 ORDER BY event_id;
```

既存の行1では、`host_name`がNULL、`source_kind`が`agent`、
`channels`が`[1, NULL, 3]`として返されます。
DEFAULTを持つカラムと持たないカラムの違いを確認してください。
ARRAYのDEFAULTは、要素数が宣言した長さと一致する必要があります。

続いて、カラム名を変更し、文字列長を拡張します。

```sql
ALTER TABLE ch7_ddl RENAME COLUMN category TO event_category;
ALTER TABLE ch7_ddl MODIFY COLUMN (message VARCHAR(4096));
ALTER TABLE ch7_ddl MODIFY COLUMN severity SET MINMAX_CACHE_SIZE = 1048576;

SELECT event_id, event_category, severity, message FROM ch7_ddl;
```

既存行の値は保持されます。名前の変更後は、検索SQLでも`event_category`を使用する必要があります。
MINMAXの例は数値カラムに1MiBを指定したもので、すべてのテーブルに推奨する値ではありません。

型変更には注意が必要です。VARCHARの長さの拡張は、TEXTをVARCHARに変換する操作ではありません。
`MINMAX_CACHE_SIZE`もVARCHAR・TEXTなどの可変長カラムには設定できません。

<a id="not-null은-기존-데이터-검사도-포함합니다"></a>

## NOT NULLと既存データ

現在の`event_category`には値があるため、次の変更が可能です。

```sql
ALTER TABLE ch7_ddl MODIFY COLUMN event_category NOT NULL;
ALTER TABLE ch7_ddl MODIFY COLUMN event_category NULL;
```

オプションなしの`NOT NULL`は既存行を検査します。
NULLを含む`host_name`には適用できません。次のSQLは、失敗を確認する場合にのみ個別に実行してください。

```sql
-- 意図的に失敗: 既存行のhost_nameはNULLです。
ALTER TABLE ch7_ddl MODIFY COLUMN host_name NOT NULL;
```

`NOT NULL NOCHECK`は既存のNULL検査を省略します。
既存のNULLを埋めたり、過去のデータも条件を満たすと保証したりするオプションではありません。
この実習の通常の手順では使用しません。

<a id="alter-log-limitations"></a>

<a id="컬럼을-지울-때는-인덱스부터-확인합니다"></a>

## インデックスとカラムの削除

```sql
CREATE INDEX ch7_ddl_host_idx ON ch7_ddl(host_name) INDEX_TYPE LSM;
DROP INDEX ch7_ddl_host_idx;
ALTER TABLE ch7_ddl DROP COLUMN (host_name);
ALTER TABLE ch7_ddl DROP COLUMN (source_kind);
ALTER TABLE ch7_ddl DROP COLUMN (channels);

SELECT event_id, event_category, severity, message FROM ch7_ddl;
```

インデックスが参照するカラムを削除するには、先にインデックスを削除してください。
内部カラム`_ARRIVAL_TIME`・`_RID`は削除・名前変更・属性変更の対象にできず、
ユーザーカラムは少なくとも1つ残す必要があります。
VARCHARの長さは既存より大きくすることだけが可能で、最大32,767バイトの範囲内にする必要があります。

<a id="delete-log-table-definition"></a>

<a id="데이터를-비우는-것과-정의를-없애는-것은-다릅니다"></a>

## データの削除とテーブルの削除

注意: 次のコマンドは実習データを削除します。
LOGデータはTRANSACTIONテーブルの`ROLLBACK`では元に戻せません。

```sql
TRUNCATE TABLE ch7_ddl;
SELECT COUNT(*) AS remaining_rows FROM ch7_ddl;
DROP TABLE ch7_ddl;
```

TRUNCATE後の件数は0になり、定義は残ります。最後のDROPは定義も削除します。
古いデータの一部だけを削除するには、[保持期間に基づく削除](../operations-lifecycle/)を使用してください。

<a id="create-log-checklist"></a>

<a id="운영-적용은-입력-프로그램과-함께-준비하세요"></a>

## DDL運用上の注意事項

変更前に入力処理とDDLの実行時刻を調整し、変更後にSQL・Appender・ファイルマッピングの
カラム名・順序・型を確認します。リソース使用中エラーが発生したら、繰り返し実行する前に、
対象テーブルを使用している処理を確認してください。

どの変更で問題が起きたか不明な場合は、変更前のDDLと失敗したSQLを用意してください。
この2つがあると、原因をより早く絞り込めます。
