---
title: 'LSL/USL によるデータ品質管理'
type: docs
weight: 80
toc: true
---

## 概要 {#overview}

LSL（規格下限）と USL（規格上限）でタグの値を自動検証し、範囲外の測定値の混入を防ぎます。

## LSL/USL とは {#introduction-to-lslusl}

LSL（Lower Specification Limit）は規格下限、USL（Upper Specification Limit）は規格上限です。
Machbase では、Tag テーブルに従属するタグメタデータテーブルでのみ使用できます。
特定のタグ ID に上下限を設定し、想定外の入力を防ぎます。

## 制約 {#constraints}

設定には次の制約があります。

* Cluster Edition は LSL/USL をサポートしません。
* Tag テーブルの第 3 列 Value に SUMMARIZED を指定する必要があります。
* LSL <= USL とし、入力値は両端を含む範囲 LSL <= Value <= USL である必要があります。
* 設定前に入力したデータは検証しません。
* NULL に設定された上限または下限は検証しません。
* 片方だけを使用できます。上限だけが必要なら USL だけを設定します。
* USL だけの場合は、USL 以下のデータに下限チェックを行いません。

### 対応データ型 {#supported-data-types}

Value 列と同じ型にします。SUMMARIZED と同様、数値型だけを使用できます。

| 型 | 説明 | 範囲 | 有効桁数 |
|----|------|-----|----|
|short|16 ビット符号付き整数|-32767 ~ 32767|-|
|ushort|16 ビット符号なし整数|0 ~ 65534|-|
|integer|32 ビット符号付き整数|-2147483647 ~ 2147483647|-|
|uinteger|32 ビット符号なし整数|0 ~ 4294967294|-|
|long|64 ビット符号付き整数|-9223372036854775807 ~ 9223372036854775807|-|
|ulong|64 ビット符号なし整数|0~18446744073709551614|-|
|float|32 ビット浮動小数点|-|6[^1]|
|double|64 ビット浮動小数点|-|15[^1]|

## LSL/USL の設定と使用 {#setting-and-using-lslusl}

タグメタデータ列に、次のキーワードを指定します。

* LSL：`LOWER LIMIT`
* USL：`UPPER LIMIT`

テーブル作成時またはメタデータ列の追加時に設定できます。例を示します。

### CREATE {#craete}

```sql
CREATE TAG TABLE example (
    tag_id  VARCHAR(50) PRIMARY KEY,
    time    DATETIME    BASETIME,
    value   INTEGER     SUMMARIZED)
METADATA (
    lsl     INTEGER LOWER LIMIT,
    usl     INTEGER UPPER LIMIT 
);
```

両方を設定することも、片方だけを設定することもできます。
LSL だけの場合、LSL 以上の値に上限チェックは行いません。USL = NULL と同じです。

```sql
CREATE TAG TABLE example (
    tag_id  VARCHAR(50) PRIMARY KEY,
    time    DATETIME    BASETIME,
    value   INTEGER     SUMMARIZED)
METADATA (
    lsl    INTEGER LOWER LIMIT  
);
```

### `ADD COLUMN` {#add-column}

データ入力後に `ADD COLUMN` で追加した場合、既定値は NULL です。

```sql
CREATE TAG TABLE example (
    tag_id  VARCHAR(50) PRIMARY KEY,
    time    DATETIME    BASETIME,
    value   INTEGER     SUMMARIZED
);
 
ALTER TABLE example METADATA ADD COLUMN (lsl INTEGER LOWER LIMIT);
ALTER TABLE example METADATA ADD COLUMN (usl INTEGER UPPER LIMIT);
```

[CREATE](#craete) と同様、片方だけでも追加できます。

```sql
CREATE TAG TABLE example (
    tag_id  VARCHAR(50) PRIMARY KEY,
    time    DATETIME    BASETIME,
    value   INTEGER     SUMMARIZED
);

ALTER TABLE example METADATA ADD COLUMN (usl INTEGER UPPER LIMIT);
```

### INSERT {#insert}

特定のタグ ID に LSL/USL を設定したら、データを入力できます。

```sql
INSERT INTO example metadata VALUES ('TAG_01', 100, 200);
```

設定後の入力は、次のように動作します。

```sql
Mach> INSERT INTO example VALUES ('TAG_01', NOW, 95);  -- 失敗
[ERR-02342: SUMMARIZED value is less than LOWER LIMIT.]

Mach> INSERT INTO example VALUES ('TAG_01', NOW, 100); -- 成功（境界値を含む）
1 row(s) inserted.
Elapsed time: 0.000

Mach> INSERT INTO example VALUES ('TAG_01', NOW, 150); -- 成功
1 row(s) inserted.
Elapsed time: 0.000

Mach> INSERT INTO example VALUES ('TAG_01', NOW, 200); -- 成功（境界値を含む）
1 row(s) inserted.
Elapsed time: 0.000

Mach> INSERT INTO example VALUES ('TAG_01', NOW, 205); -- 失敗
[ERR-02341: SUMMARIZED value is greater than UPPER LIMIT.]
```

入力後のテーブルを確認すると、検証を通過したデータだけが保存されています。

```sql
Mach> SELECT * FROM example;
TAG_ID                                              TIME                            VALUE       LSL         USL         
------------------------------------------------------------------------------------------------------------------------------
TAG_01                                              2023-09-12 09:31:27 923:289:631 100         100         200         
TAG_01                                              2023-09-12 09:31:27 929:013:232 150         100         200         
TAG_01                                              2023-09-12 09:31:27 939:209:248 200         100         200         
[3] row(s) selected.
Elapsed time: 0.001
```

### UPDATE {#update}

タグメタテーブルに設定した LSL/USL の値は変更できます。
既存の入力済みデータは再検証しないため、注意してください。

```sql
Mach> UPDATE example metadata SET lsl = 10, usl = 100 WHERE tag_id = 'TAG_01';
1 row(s) updated.
Elapsed time: 0.001

Mach> SELECT * FROM _example_meta;
_ID                  TAG_ID                                              LSL         USL         
------------------------------------------------------------------------------------------------------
1                    TAG_01                                              10          100         
[1] row(s) selected.
Elapsed time: 0.001
```

### DELETE {#delete}

メタデータ列は `ALTER TABLE example METADATA DROP COLUMN (lsl)` の形式で削除できます。
列を残したまま上下限による制約を無効にする場合は、次のように値を NULL にします。

```sql
Mach> UPDATE EXAMPLE METADATA SET lsl = NULL, usl = NULL WHERE tag_id = 'TAG_01';
1 row(s) updated.
Elapsed time: 0.001

Mach> SELECT * FROM _example_meta;
_ID                  TAG_ID                                              LSL         USL         
------------------------------------------------------------------------------------------------------
1                    TAG_01                                              NULL        NULL        
[1] row(s) selected.
Elapsed time: 0.001
```

[^1]: [IEEE 754](https://en.wikipedia.org/wiki/IEEE_754)

## TRACE ログで違反を確認 {#checking-lslusl-violations-via-trace-log}
- 保存先：`$MACHBASE_HOME/trc/machbase.trc`
- 絞り込みの例：
  ```bash
  grep LIMIT_DROP $MACHBASE_HOME/trc/machbase.trc | tail -n 20
  ```
- 形式：`LIMIT_DROP (TYPE=<UPPER|LOWER>) TABLE=<table> TAG=<tag name> <column=value ...>`
  - TYPE=LOWER/UPPER が、違反した境界を示します。
  - DATETIME は `YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn` 形式です。
- 実際の例：
  ```
  [2025-11-29 13:50:34 P-151395 T-126343511537344][QP-INFO] LIMIT_DROP (TYPE=LOWER) TABLE=TAG3 TAG=tag-1  TIME=2020-01-01 00:00:00 000:000:000 VALUE=5.55
  [2025-11-29 13:50:34 P-151395 T-126343511537344][QP-INFO] LIMIT_DROP (TYPE=UPPER) TABLE=TAG3 TAG=tag-1  TIME=2020-01-01 00:00:04 000:000:000 VALUE=30.55
  [2025-11-29 13:50:35 P-151395 T-126344475694784][QP-INFO] LIMIT_DROP (TYPE=LOWER) TABLE=TAG3 TAG=tag-2  TIME=1998-12-24 09:00:00 000:000:000 VALUE=0
  [2025-11-29 13:50:35 P-151395 T-126344475694784][QP-INFO] LIMIT_DROP (TYPE=UPPER) TABLE=TAG3 TAG=tag-2  TIME=1998-12-24 09:00:00 000:000:008 VALUE=45
  ```
- 活用方法
  - 違反したタグ、時刻、VALUE を確認します。
  - `TAG=` や `TABLE=` を grep して、対象を絞り込みます。
- 注意：1 行は約 4 KB までです。列数が多いと末尾が切り詰められます。起動直後でメタキャッシュが未準備の場合、テーブル名が ID で表示されることがあります。
