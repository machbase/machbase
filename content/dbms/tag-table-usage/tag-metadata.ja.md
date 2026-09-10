---
type: docs
title: '5.10 TAGメタデータ'
weight: 100
toc: true
---


<a id="original-85-tag-metadata"></a>

## Tagメタデータ


### 概要

METADATAはタグごとに1行の現在の属性です。通常のTAG検索では、同じ属性が各DATA行とともに
表示されます。現在の属性を変えると過去のDATAの検索結果にも新しい属性が表示される場合があるため、
発生時点の属性が必要な場合はDATAまたは別の属性履歴に保存します。

以下では基本メタデータ、JSONメタデータ、全体例を別々のテーブルに分けます。
タグの静的属性を保存する領域として使用し、センサー位置、装置状態、設置情報、外部識別子、
JSONドキュメント形式の属性を格納できます。

メタデータ専用SQLで次の操作を実行できます。以下の例の`TAG`はテーブル名であり、
使用時には実際のTAGテーブル名に置き換えます。

- メタデータ専用の検索
- メタデータ条件による`UPDATE` / `DELETE`
- メタデータ行の最終変更時刻の検索
- ARRAYメタデータ列のADD/DROPと既存行へのDEFAULT適用
- `JSON`型メタデータ列の宣言
- JSONパスの検索とJSONパスインデックス
- JSONドキュメントの一部だけを変更する部分更新

ユーザーは内部ストレージテーブルを直接操作せず、`TAG METADATA`構文だけを使用できます。

### メタデータ列の定義

メタデータ列は`CREATE TAG TABLE`の`METADATA (...)`句で定義します。

```sql
CREATE TAG TABLE ch5_meta (
    name VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE
)
METADATA (
    location VARCHAR(100),
    status VARCHAR(20),
    srcip IPV4
);
```

メタデータ列はタグ名ごとに1行だけ保存されます。

### ARRAYメタデータ列の追加と削除

Standard Editionでは、既存TAGテーブルのMETADATA領域に固定長の数値ARRAY列を
追加・削除できます。

```sql
INSERT INTO ch5_meta (name, time, value)
VALUES ('TEMP_OLD', TO_DATE('2026-09-05 00:00:00'), 10.0);

ALTER TABLE ch5_meta METADATA
    ADD COLUMN (limits DECIMAL(12,4)[2] DEFAULT [0.0000, NULL]);

INSERT INTO ch5_meta (name, time, value)
VALUES ('TEMP_NEW', TO_DATE('2026-09-05 00:00:01'), 20.0);

SELECT name, limits
  FROM ch5_meta METADATA
 ORDER BY name;
```

ALTER前から存在する`TEMP_OLD`のメタデータ行には`[0.0000, NULL]`が補充されます。
ALTER後にTAG DATAの入力で自動登録された`TEMP_NEW`のメタデータ行にはADD COLUMNのDEFAULTが
再適用されず、`limits`全体がNULLになります。DEFAULTがない場合はALTER前の行も全体がNULLです。

追加したARRAYメタデータ列は、通常のTAG検索の明示的な射影と`SELECT *`にも含まれます。
ARRAYメタデータ列にはインデックスが自動作成されず、以下のような明示的なインデックスも
サポートされません。

```sql
-- サポートされず、エラーを返します。
CREATE INDEX idx_sensor_limits ON ch5_meta METADATA(limits);
```

列を削除する場合も`METADATA`を指定します。

```sql
ALTER TABLE ch5_meta METADATA DROP COLUMN (limits);
```

TAG DATAの通常のARRAY列は`CREATE TAG TABLE`で宣言できますが、ALTERでは追加できません。
サポートされる要素型、要素数、DEFAULTの規則は
[数値ARRAY型](/dbms/reference/sql/types/array/)を参照してください。

### メタデータの入力

メタデータは`INSERT INTO ... METADATA`で入力します。

```sql
INSERT INTO ch5_meta METADATA VALUES (
    'TEMP_001',
    'Building-A/F1',
    'READY',
    '192.168.0.11'
);
```

列一覧も指定できます。

```sql
INSERT INTO ch5_meta METADATA (name, status, srcip, location)
VALUES ('TEMP_002', 'STOP', '192.168.0.12', 'Building-A/F2');
```

注意事項:

- 列一覧を省略したVALUESは、タグ名に続いてメタデータの宣言順に従います。
- 列一覧を指定した場合は、その一覧の順に値を渡します。
- 省略した入力のNULL・DEFAULT処理は、該当DDLと入力経路の規則に従います。
- 識別子はTAGのタグ名列です。この例では`name`という名前で宣言しています。
- メタデータ行の作成時に`_LAST_UPDATE_TIME`がサーバー時刻で自動記録されます。

<a id="metadata-query-tag"></a>

### メタデータの検索

#### メタデータのみ検索

メタデータ専用検索は`FROM TAG METADATA`を使用します。

```sql
SELECT name, location, status, srcip
  FROM ch5_meta METADATA
 ORDER BY name;
```

この検索はタグ名ごとに1行を返します。

```sql
SELECT *
  FROM ch5_meta METADATA
 ORDER BY name;
```

`SELECT *`と`table_alias.*`は`NAME`とメタデータ列のみを返します。

`_LAST_UPDATE_TIME`などのシステム管理列は`SELECT *`の結果に表示されません。
必要な場合は列名を明示します。

#### 最終変更時刻の検索

TAGメタデータには、各メタデータ行の最終変更時刻を示すシステム管理列
`_LAST_UPDATE_TIME`があります。

`_LAST_UPDATE_TIME`はTagデータ行の最終入力時刻ではなく、Tagメタデータ行が作成された時刻、
または実際にメタデータ値が変更された時刻です。

##### 検索方法

`_LAST_UPDATE_TIME`は列名を明示して検索します。

```sql
SELECT name, _last_update_time
  FROM ch5_meta METADATA;
```

他のメタデータ列とともに検索したり、条件に使用したりできます。

```sql
SELECT name, location, status, _last_update_time
  FROM ch5_meta METADATA
 WHERE name = 'TEMP_001';
```

`SELECT *`と`table_alias.*`の結果には`_LAST_UPDATE_TIME`は表示されません。

##### 自動記録・更新の規則

メタデータ行が新しく作成されると`_LAST_UPDATE_TIME`が自動記録されます。

```sql
INSERT INTO ch5_meta METADATA(name, location, status)
VALUES('TEMP_003', 'Building-A/F3', 'READY');
```

ユーザーメタデータ値が実際に変わると`_LAST_UPDATE_TIME`が更新されます。

```sql
UPDATE ch5_meta METADATA
   SET status = 'DONE'
 WHERE name = 'TEMP_003';
```

同じ値への更新やJSONの存在しないパスの削除など、保存結果が変わらない更新は実際の変更と
みなしません。この場合、`_LAST_UPDATE_TIME`は維持されます。

```sql
UPDATE ch5_meta METADATA
   SET status = 'DONE'
 WHERE name = 'TEMP_003';
```

JSONの存在しないパスの削除も、保存値が変わらなければno-opです。
実行例は以下のJSONテーブルを作成してから確認します。

##### 直接入力・変更の制限

`_LAST_UPDATE_TIME`はシステム管理列のため、ユーザーが直接値を入力・変更できません。

次の文は許可されません。

```sql
INSERT INTO ch5_meta METADATA(name, location, status, _last_update_time)
VALUES('TEMP_004', 'Building-A/F4', 'READY', now);
```

```sql
UPDATE ch5_meta METADATA
   SET _last_update_time = now
 WHERE name = 'TEMP_003';
```

また、TAGの名前列名、TAGメタデータ列名、`ALTER TABLE ... METADATA ADD COLUMN`の
対象列名に`_LAST_UPDATE_TIME`は使用できません。
`ALTER TABLE ... METADATA DROP COLUMN`で`_LAST_UPDATE_TIME`を削除することもできません。

```sql
CREATE TAG TABLE invalid_sensor (
    _last_update_time VARCHAR(128) PRIMARY KEY,
    time              DATETIME BASETIME,
    value             DOUBLE
);
```

```sql
CREATE TAG TABLE invalid_sensor_meta (
    name  VARCHAR(128) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE
)
METADATA (
    _last_update_time DATETIME
);
```

`_LAST_UPDATE_TIME2`のように接頭辞だけが同じ名前は、別のユーザー列として使用できます。

##### 時間条件による検索と自動インデックス

`_LAST_UPDATE_TIME`には時間条件検索用のインデックスが自動提供されます。

```sql
SELECT name, location, _last_update_time
  FROM ch5_meta METADATA
 WHERE _last_update_time >= TO_DATE('2026-06-08 00:00:00')
 ORDER BY _last_update_time;
```

そのため、ユーザーが同じ列に別のインデックスを重複作成する必要はありません。

##### machloader / tagmetaimportの使用時の注意事項

TAGメタデータのインポートでは、入力ファイルやformファイルには`NAME`とユーザーメタデータ列のみを
含めます。内部列`_ID`とシステム管理列`_LAST_UPDATE_TIME`は入力対象ではありません。

メタデータが`location`、`status`の場合、入力データは次の形式です。

```text
TEMP_001,Building-A/F1,READY
TEMP_002,Building-A/F2,STOP
```

`_LAST_UPDATE_TIME`はインポート時にサーバーが自動設定します。

通常のLOG、LOOKUP、VOLATILEテーブルでユーザーが`_LAST_UPDATE_TIME`という列を定義した場合は、
通常のユーザー列として動作します。予約された動作はTAGメタデータのシステム列だけに適用されます。

#### データとともに検索

メタデータ条件で時系列データを検索する場合は、通常の`FROM TAG`を使用します。

```sql
SELECT name, status, time, value
  FROM ch5_meta
 WHERE status = 'READY'
 ORDER BY name, time;
```

この検索はデータ行単位で返すため、同じタグのメタデータ値が各データ行で繰り返されます。

注意事項:

- `FROM TAG METADATA`では`TIME`、`VALUE`などのデータ列は検索できません。
- `FROM TAG`はデータ検索モード、`FROM TAG METADATA`はメタデータ検索モードです。
- `TAG METADATA`では内部列`_ID`、`_RID`を使用できません。

### メタデータの更新

メタデータの更新は`UPDATE TAG METADATA`を使用します。

```sql
UPDATE ch5_meta METADATA
   SET status = 'DONE',
       srcip = '10.0.0.20'
 WHERE name = 'TEMP_001';
```

メタデータ条件で複数タグを一度に更新することもできます。

```sql
UPDATE ch5_meta METADATA
   SET status = 'DONE'
 WHERE status = 'READY';
```

注意事項:

- 更新対象は`NAME`とメタデータ列です。
- `TIME`、`VALUE`などのデータ列は`UPDATE ... METADATA`で変更できません。
- 内部列は変更できません。
- 実際にメタデータ値が変わった場合だけ`_LAST_UPDATE_TIME`が更新されます。

### メタデータの削除

メタデータの削除は`DELETE FROM TAG METADATA`を使用します。

特定タグのメタデータを削除する場合は、`WHERE`句でタグ名条件を指定します。

```sql
DELETE FROM ch5_meta METADATA
 WHERE name = 'TEMP_002';
```

メタデータ条件で複数タグを一度に削除することもできます。

```sql
DELETE FROM ch5_meta METADATA
 WHERE status = 'STOP';
```

`WHERE`句を省略すると全メタデータが対象です。この実習には前に入力したTEMP_OLD・TEMP_NEWの
DATAが残っているため、以下の全削除は意図的に失敗します。

```sql
DELETE FROM ch5_meta METADATA;
```

注意事項:

- 削除対象のいずれかに実データ行がある場合、文全体が失敗します。
- つまり、使用中のタグのメタデータは削除できません。
- 全削除でも使用中のタグが1つでもあると、一部だけを削除せず文全体が失敗します。

使用中のタグのメタデータを削除する場合は、先にそのタグのデータ行を削除してから
メタデータ削除を再実行します。

```sql
DELETE FROM ch5_meta
 WHERE name = 'TEMP_001';

DELETE FROM ch5_meta METADATA
 WHERE name = 'TEMP_001';
```

<a id="metadata-design-json"></a>

### JSONメタデータ列

メタデータに`JSON`列を宣言できます。

```sql
CREATE TAG TABLE ch5_meta_json (
    name VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE
)
METADATA (
    status VARCHAR(20),
    info JSON
);
```

JSONメタデータの入力例:

```sql
INSERT INTO ch5_meta_json METADATA VALUES (
    'SHIP_001',
    'READY',
    '{"name":"alpha","ship":{"status":"READY"}}'
);
```

注意事項:

- `JSON`メタデータ列には長さを指定しません。
- 無効なJSON文字列はエラーになります。
- 生のJSON列自体にはインデックスが自動作成されません。

### JSONの値が変わらない場合

```sql
SELECT name, _last_update_time FROM ch5_meta_json METADATA;
UPDATE ch5_meta_json METADATA
   SET info = JSON_REMOVE(info, '$.missing')
 WHERE name = 'SHIP_001';
SELECT name, _last_update_time FROM ch5_meta_json METADATA;
```

パスが存在せず保存値が変わらない場合、変更時刻も維持されます。

### JSONパスの検索

JSONメタデータは`->`演算子で検索できます。

```sql
SELECT name,
       info->'$.name',
       info->'$.ship.status'
  FROM ch5_meta_json METADATA
 WHERE info->'$.ship.status' = 'READY'
 ORDER BY name;
```

データ検索でも同じ方法を使用できます。

```sql
SELECT name, time, value
  FROM ch5_meta_json
 WHERE info->'$.ship.status' = 'READY'
 ORDER BY name, time;
```

#### パスの表記規則

検索と部分更新のパスは完全なJSONPathを使用します。

- 通常のキー: `$.name`
- ネストしたキー: `$.ship.status`
- キー名に`.`または`-`が含まれる場合は角括弧表記を使用

```sql
SELECT info->'$[''ship.owner'']'
  FROM ch5_meta_json METADATA;

SELECT info->'$[''ship-owner'']'
  FROM ch5_meta_json METADATA;
```

### JSONパスインデックス

#### テーブル作成時に宣言

頻繁に検索するJSONパスは、メタデータ定義時にインデックスを作成できます。

```sql
CREATE TAG TABLE ch5_meta_json_indexed (
    name VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE
)
METADATA (
    status VARCHAR(20),
    info JSON INDEX('name', 'ship.status')
);
```

`INDEX(...)`内の文字列は次の規則で解釈されます。

- `'name'`は`$.name`
- `'ship.status'`は`$.ship.status`
- 特殊文字のあるキーや複雑なパスは完全なJSONPathを直接使用

```sql
INFO JSON INDEX('$[''ship.owner'']')
```

#### 作成後にインデックスを追加

テーブル作成後もJSONパスインデックスを追加できます。

```sql
CREATE INDEX idx_ship_owner
ON ch5_meta_json METADATA (info->'$.owner');
```

#### インデックスの削除

インデックス名だけで削除します。

```sql
SHOW INDEX idx_ship_owner;
DROP INDEX idx_ship_owner;
```

明示的に作成したインデックスは、作成時に指定した名前で管理します。`SHOW INDEX idx_ship_owner;`は
DROP前に実行します。削除後に同名を検索すると、存在しないオブジェクトになります。

#### インデックス使用時の注意事項

現在のJSONパスインデックスは、主に文字列比較で動作します。

```sql
SELECT name
  FROM ch5_meta_json METADATA
 WHERE info->'$.status' = 'READY';
```

文字列リテラルとの比較はインデックスを使用できます。一方、数値リテラルとの比較は
フルスキャンになる場合があります。

例:

- `info->'$.num' = '10'`: インデックスを使用可能
- `info->'$.num' = 10`: フルスキャンの可能性あり

### JSONの部分更新

JSON関数は、指定パスを変更した新しいドキュメント値を返します。UPDATEはその結果を列に保存します。
これはパス単位の論理更新であり、保存ファイルの一部だけをその場で変更するという性能保証ではありません。

#### JSON_SET

SQLのスカラー値をJSONのスカラーとして保存します。

```sql
UPDATE ch5_meta_json METADATA
   SET info = JSON_SET(info, '$.ship.status', 'DONE')
 WHERE name = 'SHIP_001';
```

#### JSON_SET_JSON

入力文字列をJSONとして解釈し、オブジェクトまたは配列を保存します。

```sql
UPDATE ch5_meta_json METADATA
   SET info = JSON_SET_JSON(info, '$.owner', '{"name":"machbase","team":"db"}')
 WHERE name = 'SHIP_001';
```

#### JSON_REMOVE

指定したメンバーまたは下位パスを削除します。

```sql
UPDATE ch5_meta_json METADATA
   SET info = JSON_REMOVE(info, '$.owner.team')
 WHERE name = 'SHIP_001';
```

#### 部分更新の規則

- `JSON_SET(..., path, NULL)`はJSONの`null`を保存します。
- `JSON_SET_JSON(..., path, NULL)`の結果はSQLの`NULL`です。
- JSONドキュメント引数が`NULL`の場合、関数の結果はSQLの`NULL`です。
- パスが`NULL`または空文字列の場合はエラーになります。
- 存在しないパスへの`JSON_REMOVE`はエラーではなくno-opです。
- `JSON_REMOVE(..., '$')`は許可されません。
- 部分更新は主にオブジェクトのパスをサポートします。
- 配列要素のパス更新（例: `$.items[0]`）はサポートしません。

### 全体例

```sql
CREATE TAG TABLE ch5_meta_complete (
    name VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE
)
METADATA (
    status VARCHAR(20),
    srcip IPV4,
    info JSON INDEX('name', 'ship.status')
);

INSERT INTO ch5_meta_complete METADATA VALUES (
    'SHIP_001',
    'READY',
    '192.168.0.11',
    '{"name":"alpha","ship":{"status":"READY"}}'
);

INSERT INTO ch5_meta_complete VALUES ('SHIP_001', '2026-04-01 00:00:00', 10.5);

SELECT name, status, info
  FROM ch5_meta_complete METADATA;

SELECT name, time, value
  FROM ch5_meta_complete
 WHERE info->'$.ship.status' = 'READY';

CREATE INDEX idx_ship_owner
ON ch5_meta_complete METADATA (info->'$.owner');

UPDATE ch5_meta_complete METADATA
   SET info = JSON_SET(info, '$.ship.status', 'DONE')
 WHERE name = 'SHIP_001';

DROP INDEX idx_ship_owner;
```

### まとめ

- メタデータ専用検索は`FROM TAG METADATA`
- データ検索は`FROM TAG`
- メタデータの更新・削除は`UPDATE/DELETE ... METADATA`
- ARRAYメタデータ列の変更は`ALTER TABLE ... METADATA ADD/DROP COLUMN`
- JSONメタデータは`INFO JSON`
- `_LAST_UPDATE_TIME`はメタデータ行の最終変更時刻で、明示的に検索可能
- JSONパスインデックスは`INFO JSON INDEX(...)`または`CREATE INDEX ... ON TAG METADATA (...)`
- JSONの部分更新は`JSON_SET`、`JSON_SET_JSON`、`JSON_REMOVE`
- `_LAST_UPDATE_TIME`はサーバーが自動管理し、StandardとClusterで同じ動作

<a id="metadata-design-tag"></a>

## 実習の後片付け

全削除の失敗例とは異なり、DROPはテーブルとDATA・METADATAをすべて削除します。
以下の名前が今回の実習で作成したオブジェクトであることを確認して実行します。

```sql
DROP TABLE ch5_meta;
DROP TABLE ch5_meta_json;
DROP TABLE ch5_meta_json_indexed;
DROP TABLE ch5_meta_complete;
```
