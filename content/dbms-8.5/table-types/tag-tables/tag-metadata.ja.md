---
title: 'Tag メタデータ'
type: docs
weight: 20
toc: true
---

## 概要 {#overview}

タグごとの静的な属性を保存します。センサーの場所、状態、設置情報、外部識別子、`JSON` 形式のプロパティなどを管理できます。

`TAG METADATA` 構文で、次の操作を直接実行できます。

- メタデータだけの検索
- メタデータ条件による `UPDATE` と `DELETE`
- メタデータ行の最終更新時刻の検索
- `JSON` メタデータ列
- `JSON` パスの検索とインデックス
- `JSON` 文書の部分更新

内部のメタテーブルを直接操作する必要はありません。

## メタデータ列の定義 {#define-metadata-columns}

`CREATE TAG TABLE` の `METADATA (...)` で定義します。

```sql
CREATE TAG TABLE sensors (
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

タグ名ごとに 1 行保存されます。

## メタデータの挿入 {#insert-metadata}

`INSERT INTO ... METADATA` を使用します。

```sql
INSERT INTO sensors METADATA VALUES (
    'TEMP_001',
    'Building-A/F1',
    'READY',
    '192.168.0.11'
);
```

列リストも指定できます。

```sql
INSERT INTO sensors METADATA (name, status, srcip, location)
VALUES ('TEMP_002', 'STOP', '192.168.0.12', 'Building-A/F2');
```

注意事項：

- 列リストを省略した `VALUES (...)` の順序は、`NAME`、続いて宣言順のメタデータ列です。
- 未指定のメタデータ列は `NULL` になります。
- メタデータ行の識別子は常に `NAME` です。
- 作成時に、サーバー時刻が `_LAST_UPDATE_TIME` に自動記録されます。

## メタデータの検索 {#query-metadata}

### メタデータだけの検索 {#query-metadata-only}

`FROM TAG METADATA` を使用します。

```sql
SELECT name, location, status, srcip
  FROM sensors METADATA
 ORDER BY name;
```

タグ名ごとに 1 行を返します。

```sql
SELECT *
  FROM sensors METADATA
 ORDER BY name;
```

`SELECT *` と `table_alias.*` は、`NAME` とユーザー定義メタデータ列だけを返します。

`_LAST_UPDATE_TIME` などのシステム管理列は `SELECT *` に含まれません。必要なら列名を明示します。

### 最終更新時刻の検索 {#query-last-update-time}

システム管理列 `_LAST_UPDATE_TIME` は、メタデータ行の最終変更時刻を保存します。

データ行の最終挿入時刻ではありません。メタデータ行の作成時、またはメタデータの値が実際に変わった時刻です。

#### 検索構文 {#query-syntax}

選択リストに `_LAST_UPDATE_TIME` を明示します。

```sql
SELECT name, _last_update_time
  FROM sensors METADATA;
```

ユーザー定義メタデータ列と一緒に取得したり、条件に使ったりできます。

```sql
SELECT name, location, status, _last_update_time
  FROM sensors METADATA
 WHERE name = 'TEMP_001';
```

`SELECT *` と `table_alias.*` には含まれません。

#### 自動記録と更新の規則 {#automatic-recording-and-update-rules}

メタデータ行の作成時に自動記録されます。

```sql
INSERT INTO sensors METADATA(name, location, status)
VALUES('TEMP_003', 'Building-A/F3', 'READY');
```

ユーザー定義メタデータの値が実際に変わると更新されます。

```sql
UPDATE sensors METADATA
   SET status = 'DONE'
 WHERE name = 'TEMP_003';
```

同じ値の再設定など、保存値が変わらない操作は何もしない操作として扱い、`_LAST_UPDATE_TIME` を維持します。

```sql
UPDATE sensors METADATA
   SET status = 'DONE'
 WHERE name = 'TEMP_003';
```

`info` という `JSON` メタデータ列で、存在しないパスを削除して保存値が変わらない場合も同様です。

```sql
UPDATE sensors METADATA
   SET info = JSON_REMOVE(info, '$.missing')
 WHERE name = 'TEMP_003';
```

#### 直接書き込みの制限 {#direct-write-restrictions}

サーバーが管理するため、`_LAST_UPDATE_TIME` を直接挿入、更新できません。

次の文は使用できません。

```sql
INSERT INTO sensors METADATA(name, location, status, _last_update_time)
VALUES('TEMP_004', 'Building-A/F4', 'READY', now);
```

```sql
UPDATE sensors METADATA
   SET _last_update_time = now
 WHERE name = 'TEMP_003';
```

タグ名列、ユーザー定義メタデータ列、`ALTER TABLE ... METADATA ADD COLUMN` の列名にも使用できません。`ALTER TABLE ... METADATA DROP COLUMN` で削除することもできません。

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

`_LAST_UPDATE_TIME2` のように接頭辞だけが共通する名前は、通常のユーザー定義列に使用できます。

#### 時刻条件と自動インデックス {#time-predicate-queries-and-automatic-index}

`_LAST_UPDATE_TIME` の時刻条件用インデックスは自動的に提供されます。

```sql
SELECT name, location, _last_update_time
  FROM sensors METADATA
 WHERE _last_update_time >= TO_DATE('2026-06-08 00:00:00')
 ORDER BY _last_update_time;
```

同じ列にユーザーインデックスを重複して作る必要はありません。

#### machloader / tagmetaimport の注意 {#notes-for-machloader--tagmetaimport}

入力ファイルとフォームファイルには、`NAME` とユーザー定義メタデータ列だけを含めます。`_ID` や `_LAST_UPDATE_TIME` は入力対象ではありません。

メタデータ列が `location` と `status` の場合、次の入力を使用します。

```text
TEMP_001,Building-A/F1,READY
TEMP_002,Building-A/F2,STOP
```

インポート中に、サーバーが `_LAST_UPDATE_TIME` を自動設定します。

通常の LOG、LOOKUP、VOLATILE に `_LAST_UPDATE_TIME` という列を定義した場合は、通常のユーザー列として動作します。予約列としての動作は TAG メタデータのシステム列だけに適用されます。

### メタデータ条件でデータを検索 {#query-data-with-metadata-filters}

時系列の行をメタデータ条件で絞る場合は、通常の `FROM TAG` を使用します。

```sql
SELECT name, status, time, value
  FROM sensors
 WHERE status = 'READY'
 ORDER BY name, time;
```

データ行を返すため、各行に同じタグのメタデータ値が繰り返し表示されます。

注意事項：

- `FROM TAG METADATA` では `TIME`、`VALUE` などのデータ列は使用できません。
- `FROM TAG` はデータ検索、`FROM TAG METADATA` はメタデータ検索です。
- `_ID`、`_RID` などの内部列は `TAG METADATA` で利用できません。

## メタデータの更新 {#update-metadata}

`UPDATE TAG METADATA` を使用します。

```sql
UPDATE sensors METADATA
   SET status = 'DONE',
       srcip = '10.0.0.20'
 WHERE name = 'TEMP_001';
```

メタデータ条件で複数のタグを更新できます。

```sql
UPDATE sensors METADATA
   SET status = 'DONE'
 WHERE status = 'READY';
```

注意事項：

- 更新できるのは `NAME` とメタデータ列だけです。
- `TIME`、`VALUE` などのデータ列は `UPDATE ... METADATA` では更新できません。
- 内部列は更新できません。
- 保存値が実際に変わった場合だけ `_LAST_UPDATE_TIME` が更新されます。

## メタデータの削除 {#delete-metadata}

`DELETE FROM TAG METADATA` を使用します。

特定のタグだけを削除するには、`WHERE` にタグ名を指定します。

```sql
DELETE FROM sensors METADATA
 WHERE name = 'TEMP_002';
```

メタデータ条件で複数のタグも削除できます。

```sql
DELETE FROM sensors METADATA
 WHERE status = 'STOP';
```

`WHERE` を省略すると、すべてのメタデータ行を削除します。

```sql
DELETE FROM sensors METADATA;
```

注意事項：

- 対象タグにデータ行が 1 つでも残っていると、文全体が失敗します。
- 使用中のタグのメタデータは削除できません。
- 全件削除でも同じです。対象に使用中のタグがあれば全体が失敗し、
  一部のメタデータだけを削除することはありません。

使用中のタグを削除するには、先にそのタグのデータ行を削除し、
メタデータの削除を再実行します。

```sql
DELETE FROM sensors
 WHERE name = 'TEMP_001';

DELETE FROM sensors METADATA
 WHERE name = 'TEMP_001';
```

## `JSON` メタデータ列 {#json-metadata-columns}

`JSON` 型のメタデータ列を定義できます。

```sql
CREATE TAG TABLE ships (
    name VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE
)
METADATA (
    status VARCHAR(20),
    info JSON
);
```

挿入例：

```sql
INSERT INTO ships METADATA VALUES (
    'SHIP_001',
    'READY',
    '{"name":"alpha","ship":{"status":"READY"}}'
);
```

注意事項：

- `JSON` メタデータ列に長さは指定しません。
- 無効な `JSON` テキストはエラーになります。
- `JSON` 列そのものには、自動インデックスを作成しません。

## `JSON` パスの検索 {#query-json-paths}

`->` 演算子で `JSON` メタデータを検索します。

```sql
SELECT name,
       info->'$.name',
       info->'$.ship.status'
  FROM ships METADATA
 WHERE info->'$.ship.status' = 'READY'
 ORDER BY name;
```

同じパス式を、通常のタグ検索でも使用できます。

```sql
SELECT name, time, value
  FROM ships
 WHERE info->'$.ship.status' = 'READY'
 ORDER BY name, time;
```

### パスの表記規則 {#path-notation-rules}

検索と変更のパスには、完全な JSONPath を使用します。

- 単純なキー：`$.name`
- 入れ子のキー：`$.ship.status`
- キーに `.` や `-` を含む場合は、角括弧表記を使用

```sql
SELECT info->'$[''ship.owner'']'
  FROM ships METADATA;

SELECT info->'$[''ship-owner'']'
  FROM ships METADATA;
```

## `JSON` パスインデックス {#json-path-indexes}

### テーブル作成時の定義 {#define-indexes-when-creating-the-table}

よく検索するパスは、テーブルの作成時に定義します。

```sql
CREATE TAG TABLE ships (
    name VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE
)
METADATA (
    status VARCHAR(20),
    info JSON INDEX('name', 'ship.status')
);
```

`INDEX(...)` 内の文字列は、次のように解釈されます。

- `'name'` は `$.name`
- `'ship.status'` は `$.ship.status`
- 特殊なキーや複雑なパスには、完全な JSONPath を直接指定

```sql
INFO JSON INDEX('$[''ship.owner'']')
```

### 作成後の追加 {#add-an-index-after-table-creation}

後から `JSON` パスインデックスを追加することもできます。

```sql
CREATE INDEX idx_ship_owner
ON ships METADATA (info->'$.owner');
```

### インデックスの削除 {#drop-an-index}

インデックス名を指定して削除します。

```sql
DROP INDEX idx_ship_owner;
```

`INFO JSON INDEX(...)` で自動作成した場合は、`SHOW INDEXES` で生成された名前を確認します。個別の詳細には `SHOW INDEX index_name` を使用します。

```sql
SHOW INDEXES;
```

### 利用上の注意 {#notes-on-index-usage}

現在の `JSON` パスインデックスは、主に文字列比較で機能します。

```sql
SELECT name
  FROM ships METADATA
 WHERE info->'$.status' = 'READY';
```

文字列リテラルとの比較では使用できます。数値リテラルとの比較では、全表スキャンになる場合があります。

例：

- `info->'$.num' = '10'`：インデックスを利用可能
- `info->'$.num' = 10`：全表スキャンになる場合あり

## `JSON` の部分更新 {#partial-json-updates}

文書全体を書き直さずに、一部分を更新できます。

### `JSON_SET` {#json_set}

SQL のスカラー値を `JSON` のスカラー値として保存します。

```sql
UPDATE ships METADATA
   SET info = JSON_SET(info, '$.ship.status', 'DONE')
 WHERE name = 'SHIP_001';
```

### `JSON_SET_JSON` {#json_set_json}

入力文字列を `JSON` として解析し、オブジェクトまたは配列として保存します。

```sql
UPDATE ships METADATA
   SET info = JSON_SET_JSON(info, '$.owner', '{"name":"machbase","team":"db"}')
 WHERE name = 'SHIP_001';
```

### `JSON_REMOVE` {#json_remove}

メンバーまたはサブツリーを削除します。

```sql
UPDATE ships METADATA
   SET info = JSON_REMOVE(info, '$.owner.team')
 WHERE name = 'SHIP_001';
```

### 部分更新の規則 {#partial-update-rules}

- `JSON_SET(..., path, NULL)` は `JSON` の `null` を保存します。
- `JSON_SET_JSON(..., path, NULL)` は SQL の `NULL` を返します。
- `JSON` 文書の引数が `NULL` なら、結果は SQL の `NULL` です。
- パスが `NULL` または空文字列ならエラーになります。
- 存在しないパスへの `JSON_REMOVE` は何もしません。
- `JSON_REMOVE(..., '$')` は使用できません。
- オブジェクトパスの部分更新をサポートします。
- `$.items[0]` のような配列要素の変更はサポートしません。

## 完全な例 {#full-example}

```sql
CREATE TAG TABLE ships (
    name VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE
)
METADATA (
    status VARCHAR(20),
    srcip IPV4,
    info JSON INDEX('name', 'ship.status')
);

INSERT INTO ships METADATA VALUES (
    'SHIP_001',
    'READY',
    '192.168.0.11',
    '{"name":"alpha","ship":{"status":"READY"}}'
);

INSERT INTO ships VALUES ('SHIP_001', '2026-04-01 00:00:00', 10.5);

SELECT name, status, info
  FROM ships METADATA;

SELECT name, time, value
  FROM ships
 WHERE info->'$.ship.status' = 'READY';

CREATE INDEX idx_ship_owner
ON ships METADATA (info->'$.owner');

UPDATE ships METADATA
   SET info = JSON_SET(info, '$.ship.status', 'DONE')
 WHERE name = 'SHIP_001';

DROP INDEX idx_ship_owner;
```

## 要点 {#summary}

- メタデータだけの検索には `FROM TAG METADATA`
- 時系列データの検索には `FROM TAG`
- メタデータの変更には `UPDATE/DELETE ... METADATA`
- `JSON` メタデータには `INFO JSON`
- `_LAST_UPDATE_TIME` はメタデータ行の最終変更時刻を保存し、明示的に取得可能
- `JSON` パスインデックスには `INFO JSON INDEX(...)` または `CREATE INDEX ... ON TAG METADATA (...)` 
- `JSON` の部分更新には `JSON_SET`、`JSON_SET_JSON`、`JSON_REMOVE`
- `_LAST_UPDATE_TIME` はサーバーが自動管理し、Standard と Cluster で同じ動作
