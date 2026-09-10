---
type: docs
title: 'DML'
weight: 120
toc: true
---

DML（Data Manipulation Language）は、テーブルのデータを挿入・更新・削除する構文です。

## テーブルタイプ別のDML対応

| 構文 | LOG | TAG | LOOKUP | VOLATILE | TRANSACTION |
|------|:---:|:---:|:------:|:--------:|:---:|
| INSERT | O | O | O | O | O |
| INSERT SELECT | O | O | O | O | O |
| UPDATE | - | O（タグ・軸条件またはメタデータ） | O（一般条件式） | O（PK条件） | O |
| DELETE | O（保持条件・全件） | O（時間・名前条件） | O（一般条件式・全件） | O（PK条件） | O |
| DELETE WHERE | - | O（タグ・軸条件） | O（一般条件式） | O（PK等価条件） | O |
| TRUNCATE | O | - | - | - | O |

> LOGテーブルのUPDATEは未サポートです。データ更新が必要なら、LOOKUPまたはVOLATILEを使用するか、TRANSACTIONテーブルを選択してください。

---

## INSERT INTO

```sql
insert_stmt ::=
    'INSERT INTO' table_name
    [ 'METADATA' ]
    [ '(' insert_column_list ')' ]
    'VALUES' '(' value_list ')'
    [ 'ON DUPLICATE KEY UPDATE' [ 'SET' set_list ] ]

insert_column_list ::= insert_target ( ',' insert_target )*
insert_target      ::= column_name | array_column_name '[' position ']'
value_list         ::= value ( ',' value )*
set_list           ::= column_name '=' value ( ',' column_name '=' value )*
```

指定しない列にはNULLが入力されます。`METADATA`は、TAGテーブルのメタデータ列に挿入する場合に使用します。

```sql
-- 基本の挿入
INSERT INTO sensor_log VALUES (1, 'sensor-01', 23.5, 'OK');

-- 列を指定して挿入
INSERT INTO sensor_log (name, value) VALUES ('sensor-01', 23.5);

-- TAGテーブルのメタデータ挿入
INSERT INTO sensors METADATA (name, location, unit)
VALUES ('sensor-01', 'building-A', 'celsius');
```

### ARRAY要素の指定

Machbase DBMS 8.7.0では、`INSERT ... VALUES`の列リストに固定長`ARRAY`の位置を指定できます。
位置は0始まりで、指定しない要素は要素のNULLとして保存されます。

```sql
CREATE LOG TABLE array_input (
    id INTEGER,
    channels INT32[4]
);

INSERT INTO array_input (id, channels[0], channels[3])
VALUES (1, 10, 40);
```

同じ文で配列全体と要素を同時に対象にしたり、同じ位置を2回指定したりすることはできません。
スカラー列や範囲外の位置も、要素の対象として使用できません。
添字付き対象は、`INSERT ... SELECT`と`UPDATE SET`ではサポートしていません。

ARRAY値の生成、疎な入力、Appendの選択対象は、
[数値ARRAY型](/dbms/reference/sql/types/array/)と
[Sparse ARRAYと選択列Append API](/dbms/development-tools-integration/data-input-load-export/array-append/)を参照してください。

### ON DUPLICATE KEY UPDATE

`INSERT ... VALUES`でキーが重複した場合、既存行をUPDATEします。
`INSERT ... SELECT`とは組み合わせられません。

| テーブルタイプ | 重複判定キー | サポート範囲 |
|---|---|---|
| TRANSACTION | PRIMARY KEY、単一・複合UNIQUE INDEX | Standard Edition |
| LOOKUP | PRIMARY KEY | サポート |
| VOLATILE | PRIMARY KEY | サポート |
| TAG METADATA | タグ名PRIMARY KEY | サポート |
| TAG DATA、LOG | - | 未サポート |

`SET`を省略すると、INSERT入力値で既存の非キー列を更新します。
`SET`がある場合は、右辺の式を重複した既存行を基準に評価します。
LOOKUP・VOLATILE・TRANSACTIONではPRIMARY KEY自体を更新できません。
TAG METADATAのタグ名とシステム管理列は、[TAGメタデータ](/dbms/tag-table-usage/tag-metadata/)の変更規則に従います。

```sql
-- キー重複時にvalue列だけを更新
INSERT INTO devices (device_id, ip, status)
VALUES ('dev-001', '192.168.1.1', 'ONLINE')
ON DUPLICATE KEY UPDATE SET status = 'ONLINE';

-- SET句なしでは全列を挿入値で更新
INSERT INTO devices (device_id, ip, status)
VALUES ('dev-001', '192.168.1.2', 'ONLINE')
ON DUPLICATE KEY UPDATE;
```

重複判定キーのないテーブルのUPSERT、キー変更、`VALUES(col)`・`EXCLUDED.col`など他のDBMS専用の式はエラーです。
TRANSACTIONのUNIQUE競合・トランザクションの例は、[TRANSACTIONのUPSERT](/dbms/rdb-table-usage/insert-on-duplicate-key-update/)を参照してください。

---

## INSERT SELECT

```sql
insert_select_stmt ::=
    'INSERT INTO' table_name
    [ '(' insert_column_list ')' ]
    [ with_clause ]
    select_stmt
```

SELECT結果をテーブルに挿入します。
Standard Editionでは、対象テーブルと列リストの後に`WITH`句を置けます。
文頭の`WITH ... INSERT INTO ...`形式はサポートしていません。

```sql
-- クエリ結果を別のテーブルへコピー
INSERT INTO sensor_log_copy SELECT * FROM sensor_log;

-- _arrival_timeを明示して挿入（時間順序の保証が必要）
INSERT INTO sensor_log_copy (_arrival_time, id, name, value)
SELECT _arrival_time, id, name, value FROM sensor_log ORDER BY _arrival_time;

-- CTE結果の挿入
INSERT INTO sensor_log_copy (id, name, value)
WITH filtered AS (
    SELECT id, name, value
    FROM sensor_log
    WHERE value >= 80
)
SELECT id, name, value FROM filtered;
```

注意事項:

- `_ARRIVAL_TIME`を明示しなければ、INSERT実行時点の時刻が自動入力されます。
- LOGの明示時刻のコピーは、空の対象に昇順で入力し、他の入力処理と分離してください。
  対象により新しい時刻があれば、元データをソートしていても時刻逆転になります。
  デフォルトの`DISK_COLUMNAR_TABLE_TIME_INVERSION_MODE=1`では逆転値を直前の保存時刻+1nsに補正し、0では拒否します。
  したがって、明示入力は元の時刻の保持を無条件に保証しません。
- VARCHAR列で挿入値が最大長を超えると、自動的に切り詰めて入力します。
- LOG/TAGへの入力は、TRANSACTIONテーブルのトランザクションのROLLBACK対象ではありません。

---

## UPDATE

```sql
update_stmt ::=
    'UPDATE' table_name [ 'METADATA' ]
    'SET' update_expr_list
    [ 'WHERE' predicate ]

update_expr_list ::= column_name '=' value ( ',' column_name '=' value )*
```

TRANSACTIONテーブルは、WHERE句を省略すると全行を更新します。
LOOKUPは主キーまたは一般条件式、VOLATILEは主キーの一致条件を使用します。
TAGデータUPDATEは、タグ選択子と時間軸条件を併用します。

```sql
-- LOOKUPテーブルのレコード更新
UPDATE devices SET status = 'OFFLINE' WHERE device_id = 'dev-001';

-- 複数列を同時に更新
UPDATE devices SET ip = '10.0.0.1', status = 'ONLINE' WHERE device_id = 'dev-002';

-- LOOKUPの一般条件式で複数行を更新
UPDATE devices SET status = 'OFFLINE' WHERE site = 'SEOUL' AND status = 'READY';

```

### TAGデータのUPDATE

TAGテーブルの実際の時系列データは、タグ選択条件とBASETIME条件を併せて指定して更新します。

```sql
UPDATE sensors
   SET value = 101,
       status = 1
 WHERE name = 'sensor-01'
   AND time >= TO_DATE('2026-07-01', 'YYYY-MM-DD');
```

`name`（PRIMARY KEY）、`time`（BASETIME）、メタデータ列は、データUPDATEのSET対象ではありません。

### UPDATE METADATA（TAGテーブル）

TAGテーブルのメタデータ列は、別の`UPDATE ... METADATA`構文で更新します。

```sql
-- メタデータ条件で複数行を更新
UPDATE sensors METADATA
   SET status = 'DONE'
 WHERE status = 'READY';

-- タグ名を基準に更新
UPDATE sensors METADATA
   SET location = 'building-B'
 WHERE name = 'sensor-01';
```

---

## DELETE

```sql
-- LOGテーブルの削除（時間・行数基準）
delete_stmt ::=
    'DELETE FROM' table_name
    [ 'OLDEST' number 'ROWS'
    | 'EXCEPT' number ( 'ROWS' | time_unit )
    | 'BEFORE' datetime_expression ]
    [ 'NO WAIT' ]

time_unit ::= 'YEAR' | 'MONTH' | 'WEEK' | 'DAY' | 'HOUR' | 'MINUTE' | 'SECOND'
```

LOGテーブルは任意の位置の削除をサポートせず、最も古いデータから連続してだけ削除できます。

現在のLOGの`BEFORE t`は、`_arrival_time <= t`の行を削除します。
名前だけで境界を除外すると考えがちなため、事前検索にも同じ比較条件を使用してください。
`EXCEPT n DAY`などの期間は、最後の入力時刻ではなくサーバーの現在時刻を基準に計算します。
一般のユーザー定義DATETIME列の値は、この削除の基準ではありません。
実際の前後の結果は、[LOGの保持期間に基づく削除](/dbms/log-table-usage/operations-lifecycle/)で確認できます。

```sql
-- 全データの削除
DELETE FROM sensor_log;

-- 最も古いN件を削除
DELETE FROM sensor_log OLDEST 1000 ROWS;

-- 最新のN件以外をすべて削除
DELETE FROM sensor_log EXCEPT 10000 ROWS;

-- 直近N日間のデータ以外をすべて削除
DELETE FROM sensor_log EXCEPT 7 DAY;

-- 特定時刻までのデータを削除（境界時刻を含む）
DELETE FROM sensor_log BEFORE TO_DATE('2024-01-01', 'YYYY-MM-DD');
```

### DELETE WHERE（LOOKUP/VOLATILEテーブル）

```sql
delete_where_stmt ::=
    'DELETE FROM' table_name 'WHERE' predicate
```

LOOKUPは主キーまたは一般条件式、VOLATILEは主キーの一致条件を使用します。
LOOKUPはWHERE句を省略して全行を削除することもできます。

```sql
DELETE FROM devices WHERE device_id = 'dev-001';

-- LOOKUPの一般条件式で複数行を削除
DELETE FROM devices WHERE status = 'EXPIRED' OR site = 'RETIRED';

-- LOOKUPの全件削除
DELETE FROM devices;
```

### DELETE（TAGテーブル）

```sql
-- TAGテーブル: 名前または時間条件で削除
delete_from_tag_where_stmt ::=
    'DELETE FROM' table_name [ 'ROLLUP' ]
    'WHERE' predicate
    -- predicate: tag_name条件、tag_time条件、または両方のAND結合
```

時間条件には、`=`、`<`、`<=`、`BETWEEN`を使用できます。

```sql
-- TAG名を基準に削除
DELETE FROM tag WHERE name = 'sensor-01';

-- TAG名 + 時刻を基準に削除
DELETE FROM tag WHERE name = 'sensor-01' AND time < TO_DATE('2024-01-01', 'YYYY-MM-DD');

-- 時間条件だけで削除
DELETE FROM tag WHERE time <= TO_DATE('2024-01-01', 'YYYY-MM-DD');

-- ROLLUPデータの削除
DELETE FROM tag ROLLUP WHERE name = 'sensor-01';
DELETE FROM tag ROLLUP WHERE time BETWEEN TO_DATE('2024-01-01','YYYY-MM-DD') AND TO_DATE('2024-02-01','YYYY-MM-DD');
```

### DELETE FROM TAG METADATA

```sql
DELETE FROM table_name METADATA [ WHERE predicate ]
```

TAGテーブルのメタデータ行を削除します。
WHEREを省略すると、すべてのメタデータを削除します。
実際のデータが存在するタグのメタデータは削除できません。

```sql
DELETE FROM sensors METADATA WHERE name = 'sensor-01';
DELETE FROM sensors METADATA WHERE status = 'STOP';
DELETE FROM sensors METADATA;  -- 全メタデータを削除（実データがないタグのみ）
```

---

<a id="dml-update-delete-affected-rows"></a>

## UPDATE/DELETEの影響行数

`UPDATE`と`DELETE`を実行したクライアントは、その文の影響行数（affected rows）を確認できます。
直接実行とプリペアドステートメントは、同じ基準を使用します。

`UPDATE`は、実際に値が変わった行数ではなく、`WHERE`条件に一致した行数を返します。
そのため、既存値と同じ値を再設定しても、対象行が条件に一致すれば影響行数に含まれます。
`WHERE`句を省略できるテーブルでは、すべての対象行が一致したものとして数えます。

`DELETE`は、条件に一致して実際に削除された行数を返します。
同じ`DELETE`を繰り返すと、初回に行が削除されているため、次の実行は`0`を返します。

```sql
CREATE LOOKUP TABLE device_state (
    id INTEGER PRIMARY KEY,
    value INTEGER
);

INSERT INTO device_state VALUES (1, 10);
INSERT INTO device_state VALUES (2, 10);

UPDATE device_state SET value = 20 WHERE id >= 1 AND id <= 2;
-- 2 row(s) updated.

UPDATE device_state SET value = 20 WHERE id >= 1 AND id <= 2;
-- 2 row(s) updated. （同じ値で繰り返しUPDATE）

UPDATE device_state SET value = 20 WHERE id = 999;
-- No row updated.

DELETE FROM device_state WHERE id = 1;
-- 1 row(s) deleted.

DELETE FROM device_state WHERE id = 1;
-- No row deleted.
```

`No row updated.`または影響行数`0`は、設定値が既存値と同じという意味ではなく、条件に一致する行がなかったことを意味します。

トランザクション内で返された影響行数は、各文の実行時点の結果です。
後で`ROLLBACK`しても、すでに返された影響行数の意味は変わりません。

---

## 関連文書

- [DDL構文リファレンス](../ddl-syntax/) - テーブルの作成とスキーマ変更
- [SELECT構文リファレンス](../select-syntax/) - データ検索
- [WITH / CTE構文](../cte-syntax/) - CTEを使用するINSERT SELECT
- [LOOKUPの述語UPDATE](./lookup-predicate-update-syntax/) - 一般条件式による更新
- [LOOKUPの述語DELETE](./lookup-predicate-delete-syntax/) - 一般条件式による削除
- [LOAD DATA INFILE](../load-data-infile-syntax/) - CSVファイルの一括取り込み
