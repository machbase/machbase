---
title: 外れ値の自動除去
type: docs
weight: 41
toc: true
---

## はじめに

産業・環境センサーから収集する時系列データには、ノイズ、瞬間的なスパイク、振動による干渉など、想定範囲を外れた値が含まれることがあります。こうした外れ値は分析を大きく妨げ、ストレージと処理時間を余分に消費します。

外れ値を手動で、またはアプリケーション側でフィルタリングする方法は複雑で、計算コストもかかります。Machbase は、TAG テーブルのタグメタデータに定義した規格限界を使用して、取り込み時に外れ値を自動的に除去します。センサーごとに有効な範囲を宣言しておくと、その範囲内のデータだけが保存されます。

## 基本概念: 規格限界（LSL/USL）

外れ値の自動除去では、タグ識別子（Tag ID）ごとに有効な値の範囲を定義します。この範囲は、タグメタデータテーブルの次の 2 つの属性で設定します。

* **LSL（Lower Specification Limit、規格下限）**: 指定した Tag ID の測定値の最小許容値。
* **USL（Upper Specification Limit、規格上限）**: 指定した Tag ID の測定値の最大許容値。

TAG テーブルに新しい行を挿入するとき、Machbase は対応する Tag ID のメタデータにある LSL と USL を使用して次の検証を行います。

1. **メタデータの取得**: 入力行の `name`（Tag ID）に対応する LSL と USL を、従属するタグメタデータテーブル（`_TableName_meta`）から取得します。
2. **値の比較**: `SUMMARIZED` を指定した `value` 列の入力値を、LSL および USL と比較します。
3. **検証規則**: 入力値が `LSL <= incoming_value <= USL` を満たす場合だけ挿入を許可します。
   - LSL が `NULL` の場合は下限の検査を省略します（`incoming_value <= USL`）。
   - USL が `NULL` の場合は上限の検査を省略します（`LSL <= incoming_value`）。
   - LSL と USL の両方が `NULL` の場合は検査せずに値を受け入れます。
4. **処理結果**: 検証に成功すると、行を TAG テーブルに挿入します。値が LSL/USL の範囲外の場合はその行の挿入を拒否し、対応するエラーを返します。たとえば LSL 未満では `ERR-02342`、USL 超過では `ERR-02341` を返します。

この仕組みにより、タグごとに事前に定義した許容範囲に基づいて、取り込み時にデータを直接フィルタリングできます。

## 設定

規格限界（LSL/USL）は、`CREATE TAG TABLE` の `METADATA` 句で専用キーワードを付けた列を定義するか、後から `ALTER TABLE` でその列を追加して設定します。

### テーブル作成時の限界値の定義

LSL と USL を格納する列は `METADATA` 句で定義し、LSL の列に `LOWER LIMIT`、USL の列に `UPPER LIMIT` を指定します。

**構文:**

```sql
CREATE TAG TABLE table_name (
    name_column VARCHAR(...) PRIMARY KEY,
    time_column DATETIME BASETIME,
    value_column numeric_datatype SUMMARIZED, -- SUMMARIZED の指定が必要
    ...
)
METADATA (
    lsl_column_name numeric_datatype LOWER LIMIT, -- LSL の列
    usl_column_name numeric_datatype UPPER LIMIT, -- USL の列
    ... -- その他のメタデータ列
);
```

* `value_column`: 数値型で、`SUMMARIZED` キーワードを必ず指定します。外れ値の検証は、この列に入力される値に適用されます。
* `lsl_column_name`、`usl_column_name`: 限界値を格納するメタデータ列の名前で、任意に指定できます。
* `numeric_datatype`: LSL/USL 列のデータ型は、`value_column` のデータ型と互換性がある必要があります。

**例（LSL と USL の両方）:**

```sql
CREATE TAG TABLE sensor_readings (
    tag_id VARCHAR(50) PRIMARY KEY,
    ts DATETIME BASETIME,
    reading DOUBLE SUMMARIZED
)
METADATA (
    min_acceptable DOUBLE LOWER LIMIT,
    max_acceptable DOUBLE UPPER LIMIT,
    location VARCHAR(100) -- 通常のメタデータ列
);
```

* `SUMMARIZED` を指定した `reading` 列に対して外れ値の検証を行います。
* `min_acceptable` と `max_acceptable` は、LSL と USL を格納する列です。

**例（LSL のみ）:**

下限または上限の一方だけを検査すればよい場合は、限界値を片方だけ定義できます。

```sql
CREATE TAG TABLE pressure_monitor (
    tag_id VARCHAR(50) PRIMARY KEY,
    event_time DATETIME BASETIME,
    pressure_kpa INTEGER SUMMARIZED
)
METADATA (
    min_pressure INTEGER LOWER LIMIT -- 圧力の下限だけを検証
);
```

### 既存テーブルへの限界値列の追加

既存の TAG テーブルに LSL/USL 列を追加するには、従属メタデータテーブル（`_TableName_meta`）に対して `ALTER TABLE` を実行します。LSL/USL 列は、同じメタデータテーブルに対する `DROP COLUMN`（または `ALTER TABLE table_name METADATA DROP COLUMN (column_name)`）で削除することもでき、削除した限界値はそれ以降チェックされません。

**構文:**

```sql
-- LSL 列を追加
ALTER TABLE _table_name_meta ADD COLUMN ( lsl_column_name numeric_datatype LOWER LIMIT );

-- USL 列を追加
ALTER TABLE _table_name_meta ADD COLUMN ( usl_column_name numeric_datatype UPPER LIMIT );
```

**例:**

```sql
-- LSL/USL がない sensor_readings テーブルが既に存在するものとする
ALTER TABLE _sensor_readings_meta ADD COLUMN ( min_acceptable DOUBLE LOWER LIMIT );
ALTER TABLE _sensor_readings_meta ADD COLUMN ( max_acceptable DOUBLE UPPER LIMIT );
```

`ALTER TABLE` で追加した列の値は、既存のすべてのメタデータ行で最初は `NULL` になります。

### 限界値の設定

LSL/USL 列を定義したら、従属するタグメタデータテーブル（`_TableName_meta`）に行を挿入または更新して、Tag ID ごとの限界値を設定します。

```sql
-- 新しいタグのメタデータを挿入するときに限界値を設定
INSERT INTO sensor_readings metadata (tag_id, min_acceptable, max_acceptable, location)
VALUES ('TEMP_SENSOR_01', 10.0, 90.0, 'Boiler Room');

-- 既存タグの限界値を更新
UPDATE sensor_readings metadata
SET min_acceptable = 15.0, max_acceptable = 85.0
WHERE tag_id = 'TEMP_SENSOR_01';
```

## 動作と制約

* **`SUMMARIZED` が必要**: 外れ値の自動除去を使うには、TAG テーブル定義で検証対象の `value` 列に `SUMMARIZED` キーワードを必ず指定します。検証は、この列に入力される値だけに適用されます。
* **データ型の互換性**: `LOWER LIMIT` と `UPPER LIMIT` を指定したメタデータ列のデータ型は、TAG テーブルの `SUMMARIZED` 値列のデータ型と数値として互換性がある必要があります。
* **LSL <= USL**: ある Tag ID の LSL と USL が両方とも非 `NULL` の値で定義されている場合、LSL の値は USL の値以下（`LSL <= USL`）である必要があります。
* **検証の範囲**: 検証は、TAG テーブルへの `INSERT` 時にのみ行います。LSL/USL を定義・更新する前に格納されたデータには、遡って適用されません。
* **メタデータの更新**: メタデータテーブルの LSL/USL を更新すると、以降の挿入に適用する検証規則が変わります。新しい範囲を外れることになった既存データの再検証や削除は行いません。
* **NULL の処理**: ある Tag ID の LSL が `NULL` の場合、そのタグの入力データに対する下限の検査を省略します。同様に、USL が `NULL` の場合は上限の検査を省略します。両方が `NULL` の Tag ID では、外れ値の検証を行いません。
* **片方だけの限界値**: LSL 列だけを定義すると最小値の検査（`value >= LSL`）、USL 列だけを定義すると最大値の検査（`value <= USL`）を行います。
* **メタデータテーブルへの依存**: この機能は、従属するタグメタデータテーブル（`_TableName_meta`）の構造と内容に完全に依存します。

## 例

外れ値の自動除去を設定して使用する実践的な例を示します。

**1. LSL/USL を持つスキーマの定義:**

```sql
-- 前の実行で作成済みの場合は削除
DROP TABLE IF EXISTS out_tag CASCADE;

-- LSL/USL のメタデータを持つ TAG テーブルを作成
CREATE TAG TABLE out_tag (
    tag_id VARCHAR(50) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED -- フィルタリング対象の値列
)
METADATA (
    lsl DOUBLE LOWER LIMIT, -- 規格下限の列
    usl DOUBLE UPPER LIMIT  -- 規格上限の列
) TAG_PARTITION_COUNT=1;
```

**2. メタデータへの限界値の設定:**

```sql
-- TAG_01 の動作範囲を設定: 100.0 <= value <= 200.0
INSERT INTO out_tag metadata (tag_id, lsl, usl) VALUES ('TAG_01', 100.0, 200.0);

-- メタデータ行を確認
SELECT * FROM _out_tag_meta WHERE tag_id = 'TAG_01';
/* 想定出力:
_ID | TAG_ID | LSL   | USL
--- | ------ | ----- | -----
1   | TAG_01 | 100.0 | 200.0
*/
```

**3. データ挿入とフィルタリングの確認:**

```sql
-- TAG_01 のデータの挿入を試行

-- LSL 未満の値（拒否）
INSERT INTO out_tag VALUES ('TAG_01', NOW, 95.2);
-- 想定エラー: [ERR-02342: SUMMARIZED value is less than LOWER LIMIT.]

-- LSL と等しい値（許可）
INSERT INTO out_tag VALUES ('TAG_01', NOW, 100.0);
-- 想定出力: 1 row(s) inserted.

-- 範囲内の値（許可）
INSERT INTO out_tag VALUES ('TAG_01', NOW, 150.5);
-- 想定出力: 1 row(s) inserted.

-- USL と等しい値（許可）
INSERT INTO out_tag VALUES ('TAG_01', NOW, 200.0);
-- 想定出力: 1 row(s) inserted.

-- USL を超える値（拒否）
INSERT INTO out_tag VALUES ('TAG_01', NOW, 205.5);
-- 想定エラー: [ERR-02341: SUMMARIZED value is greater than UPPER LIMIT.]

-- 受け入れたデータを確認
SELECT * FROM out_tag WHERE tag_id = 'TAG_01';
/* 想定出力（時刻は実行時によって変わる）:
TAG_ID | TIME                              | VALUE | LSL   | USL
------ | --------------------------------- | ----- | ----- | -----
TAG_01 | 2024-XX-XX XX:XX:XX XXX:XXX:XXX | 100.0 | 100.0 | 200.0
TAG_01 | 2024-XX-XX XX:XX:XX XXX:XXX:XXX | 150.5 | 100.0 | 200.0
TAG_01 | 2024-XX-XX XX:XX:XX XXX:XXX:XXX | 200.0 | 100.0 | 200.0
*/
```

エラーメッセージを見ると、どちらの限界値に違反したかを確認できます。

**4. メタデータの限界値の更新:**

```sql
-- TAG_01 の限界値を 10.0 <= value <= 100.0 に変更
UPDATE out_tag metadata SET lsl = 10.0, usl = 100.0 WHERE tag_id = 'TAG_01';

-- メタデータの変更を確認
SELECT * FROM _out_tag_meta WHERE tag_id = 'TAG_01';
/* 想定出力:
_ID | TAG_ID | LSL  | USL
--- | ------ | ---- | -----
1   | TAG_01 | 10.0 | 100.0
*/

-- 更新後の限界値で新しい挿入を試行

-- 以前許可された 150.5 は、新しい USL を超えるため拒否
INSERT INTO out_tag VALUES ('TAG_01', NOW, 150.5);
-- 想定エラー: [ERR-02341: SUMMARIZED value is greater than UPPER LIMIT.]

-- 以前拒否された 95.2 は、新しい範囲内なので許可
INSERT INTO out_tag VALUES ('TAG_01', NOW, 95.2);
-- 想定出力: 1 row(s) inserted.

-- 以前挿入した値（100.0、150.5、200.0）は out_tag に残る。
-- メタデータの限界値の更新は既存データに影響しない。
```

**5. NULL によるフィルタリングの無効化:**

```sql
-- 限界値を NULL にして TAG_01 の外れ値フィルタリングを無効化
UPDATE out_tag metadata SET lsl = NULL, usl = NULL WHERE tag_id = 'TAG_01';

-- メタデータを確認
SELECT * FROM _out_tag_meta WHERE tag_id = 'TAG_01';
/* 想定出力:
_ID | TAG_ID | LSL  | USL
--- | ------ | ---- | ----
1   | TAG_01 | NULL | NULL
*/

-- 以前拒否された値を挿入（今度は成功する）
INSERT INTO out_tag VALUES ('TAG_01', NOW, 9.0);   -- 以前の LSL 未満
-- 想定出力: 1 row(s) inserted.
INSERT INTO out_tag VALUES ('TAG_01', NOW, 250.0); -- 以前の USL を超える
-- 想定出力: 1 row(s) inserted.
```
