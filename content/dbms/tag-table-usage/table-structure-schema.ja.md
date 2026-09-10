---
type: docs
title: '5.2 テーブル構造とスキーマ'
weight: 20
toc: true
aliases:
  - /dbms/tag-table-usage/time-distance-axis/
---


<a id="tag-table-design"></a>

## TAGテーブルの設計

TAGテーブルの設計では、列数だけでなく、何を1つのタグとするか、どの値をどの領域に置くかを決めます。

列の位置によって決まる役割、軸列の型、指定できない型は
[作成、変更、削除](../create-alter-drop/#original-85-creating-tag-tables)を参照してください。
このページでは、その規則の範囲内で決定する項目を扱います。

このページのDDLはモデルごとの独立した例です。作成順序が必要な実習は各節で説明します。
同名の既存オブジェクトがある場合は、別名で実行します。

スキーマを決める際は、次の項目を合わせて検討します。

- [活用例](#tag-schema-use-case-summary)
- [タグ名の列](#tag-name-column-design)
- [時間軸と距離軸の選択](#time-axis-design-tag)
- [値の列の設計](#tag-table-design-design-column)
- [METADATA列の設計](#metadata-column-design-summary)
- [JSON METADATA列の設計](#json-metadata-column-design-summary)
- [バイナリデータ列の設計](#tag-table-design-design-column-binary)
- [VARCHARストレージの最適化](#tag-table-design-storage-varchar)
- [ストレージ戦略](#tag-table-design-strategy)
- [LSL・USLの設計](#tag-table-design-lsl-usl)
- [補正と重複のポリシー](#correction-duplication-policy-summary)
- [制約とサポート範囲](#tag-schema-limitations-summary)

<a id="tag-schema-use-case-summary"></a>

### 活用例

TAGは、同じ構造の観測値が複数の対象から継続して蓄積される業務に適しています。センサー、設備、
移動体、検査回などの反復観測対象を先に決め、対象ごとの履歴を時間軸または距離軸で検索できるか
確認します。ここでは、対象をTAGでモデル化するか、別のテーブルタイプに分けるかを決定します。
業務モデルの例は[活用例](../patterns-scenarios/#use-cases-tag)を参照してください。

<a id="tag-name-column-design"></a>

### タグ名の列

センサー別、設備別、検査回別のどの単位を1つのタグとするかを先に決めます。細かく分けるとタグ数が
増えてメタデータとインデックスの負担が大きくなり、大きくまとめると1つのタグに異なる対象の履歴が
混在します。命名規則は[VARCHARストレージの最適化](#tag-table-design-storage-varchar)でも扱います。

<a id="time-axis-design-tag"></a>

### 時間軸と距離軸の選択

軸は、検索条件で何を範囲指定するかに基づいて選択します。測定時刻で区間を指定する場合は時間軸、
特定経路の累積位置など距離区間で指定する場合は距離軸です。1つのTAGテーブルは両方の軸を同時に
持てないため、後から変更するにはテーブルを作り直す必要があります。

```sql
-- 測定時刻で区間を指定する時間軸TAGです。
CREATE TAG TABLE time_sensor (
    name  VARCHAR(40) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE SUMMARIZED
);
```

<a id="distance-axis-design-tag"></a>
<a id="distance-axis-query-range"></a>

```sql
-- 距離・位置で区間を指定する距離軸TAGです。
CREATE TAG TABLE rail_sensor (
    name     VARCHAR(40) PRIMARY KEY,
    distance DOUBLE BASEDISTANCE,
    value    DOUBLE
);
```

`DURATION`、ROLLUP、時間関数はBASETIMEだけに適用されます。距離範囲の検索は通常の比較と
`BETWEEN`を使用します。実行例は[検索と分析](../query-analysis/)を参照してください。

<a id="tag-table-design-design-column"></a>

### 値の列の設計

TAGテーブルの値の列は、タグ名と軸列を除く通常のデータ列です。
計測値、状態、品質コードなど測定行ごとに変わる値を保存します。

#### サポートされる型

以下はよく使用する型の例です。JSON、BINARY、DECIMAL、数値ARRAYを含む全サポート範囲は
[データ型リファレンス](/dbms/reference/sql/types/)を参照してください。

| 型 | 説明 | 保存サイズ |
|------|------|---------|
| `DOUBLE` | 64ビット浮動小数点 | 8バイト |
| `FLOAT` | 32ビット浮動小数点 | 4バイト |
| `LONG` | 64ビット整数 | 8バイト |
| `INTEGER` (`INT`) | 32ビット整数 | 4バイト |
| `SHORT` | 16ビット整数 | 2バイト |
| `VARCHAR(n)` | 可変長文字列 | 最大nバイト |

#### 推奨する型の選択

| データ | 推奨する型 |
|--------|---------|
| 温度、湿度、圧力などのアナログ値 | `DOUBLE` |
| カウンター、状態コード | `INTEGER` |
| フラグ、二値状態 | `SHORT` |
| エネルギー、流量の累積値 | `DOUBLE`または`LONG` |
| タグの文字列値 | `VARCHAR(n)` |

#### 複数の値の列の設計

1つのテーブルに複数の計測項目を保存すると、NULL値が発生する場合があります。
計測項目が同時に収集される場合に適しています。

```sql
CREATE TAG TABLE weather_station (
    name        VARCHAR(64) PRIMARY KEY,
    time        DATETIME    BASETIME,
    temperature DOUBLE,     -- 常に収集
    humidity    DOUBLE,     -- 常に収集
    wind_speed  DOUBLE,     -- 任意
    rainfall    DOUBLE      -- 任意
);
```

#### NULLを許容する設計

TAGテーブルの値の列はデフォルトでNULLを許可します。特定タグが一部の項目だけを収集する場合は、
残りの列にNULLを挿入します。

```sql
-- wind_speedとrainfallがない場合
INSERT INTO weather_station VALUES ('WS-01', NOW, 22.5, 65.0, NULL, NULL);
```

<a id="metadata-column-design-summary"></a>

### METADATA列の設計

METADATA列はDATA行ごとに繰り返す値ではなく、タグごとの現在の属性を保存するために使用します。
設置場所、単位、装置設定、管理状態など、タグ名に付随する属性が該当します。DATAとMETADATAを
分離すると、観測履歴を維持しながらタグの現在の属性だけを検索・変更できます。ここでは各属性を
METADATAに置くかDATA列に残すかを決定します。観測ごとに値が変わる場合はDATA、タグの寿命を通して
おおむね固定ならMETADATAです。入力・検索・更新の例は
[METADATAの使用](../tag-metadata/#original-85-tag-metadata)を参照してください。

<a id="json-metadata-column-design-summary"></a>

### JSON METADATA列の設計

タグ別の属性が階層構造を持つ場合や属性の集合が頻繁に変わる場合は、JSON METADATA列を検討します。
たとえば設備の場所、メーカー情報、設置オプションを1つのJSONドキュメントに保存し、必要なパスだけを
検索できます。ここではMETADATAを個別列にするか1つのJSONドキュメントにするかを決定します。
属性の集合が固定で条件検索が多い場合は個別列、タグごとに属性構成が異なる場合はJSONが適しています。
頻繁に条件として使用するパスは、インデックス設計も検討します。詳しい構文と例は
[JSON METADATA](../tag-metadata/#metadata-design-json)を参照してください。

<a id="tag-table-design-design-column-binary"></a>

### バイナリデータ列の設計

TAGテーブルの`BINARY(n)`は、1～32767バイトのセンサーフレームの保存に使用します。
入力リテラル、長さの制約、ドライバーの動作は[Binary列](#original-85-binary-columns)を
参照してください。大きな画像や波形は外部ストレージに置き、参照キーだけを保存する設計も検討してください。

<a id="tag-table-design-storage-varchar"></a>

### VARCHARストレージの最適化

`VARCHAR`は実際の最大長に合わせて宣言します。保存オプションの正確な構文は
[DDLリファレンス](/dbms/reference/sql/syntax/ddl-syntax/)を参照してください。タグ名はサイト、
設備、センサーの識別子を一貫した区切り文字で組み合わせ、範囲検索できるように設計します。

<a id="tag-table-design-strategy"></a>

### ストレージ戦略

データはタグごとに分離された列指向ストレージに保存されます。データ量と検索パターンに応じて
適切な戦略を選択します。

#### 単一テーブルと複数テーブル

##### 単一TAGテーブル（推奨）

同種のセンサーは1つのTAGテーブルにまとめて管理します。

```sql
-- 推奨: 全温度センサーを1つのテーブルにまとめる
CREATE TAG TABLE temperature_sensor (
    name  VARCHAR(64) PRIMARY KEY,
    time  DATETIME    BASETIME,
    value DOUBLE
);
```

**利点**

- 管理箇所を最小化
- タグを横断する集計が容易
- 運用を簡素化

##### 複数TAGテーブル

列構成が異なる場合や保持期間・アクセス権・運用周期を分けて管理する必要がある場合は、
テーブルの分割を検討します。センサー数が増えたという理由だけでセンサー別テーブルを作成しません。

```sql
-- 温度・湿度センサー（DOUBLE値）
CREATE TAG TABLE thermo_sensor (
    name  VARCHAR(64) PRIMARY KEY,
    time  DATETIME    BASETIME,
    temp  DOUBLE,
    humid DOUBLE
);

-- 振動センサー（DOUBLE + BINARY波形）
CREATE TAG TABLE vibration_sensor (
    name     VARCHAR(64) PRIMARY KEY,
    time     DATETIME    BASETIME,
    rms      DOUBLE,
    waveform BINARY(4096)
);
```

#### タグ数の管理

- タグ数の増加に伴うタグインデックスとメタデータのメモリ使用量を、本番規模のデータで測定します。
- センサーの階層構造をタグ名に符号化して管理します。
- タグ名がレコードごとに一意になる設計は避けます（アンチパターン）。

#### パーティション戦略

時間軸TAGは`BASETIME`に基づいて範囲を絞って検索します。システムのストレージオブジェクトや
パーティション名に依存せず、保持期間は
[データ保持ポリシー](/dbms/operations-configuration-recovery/policy-data-retention/)で管理してください。

<a id="tag-table-design-lsl-usl"></a>
<a id="original-85-lsl-usl-limits"></a>

### LSL・USLの設計

LSL（Lower Specification Limit）は下側規格限界、USL（Upper Specification Limit）は
上側規格限界です。TAGテーブルのMETADATA列にタグごとの許容範囲を設定すると、範囲外のDATA入力を
拒否できるため、タグごとに異なる入力品質基準を適用できます。

値を補正する機能ではなく、入力を拒否する機能です。範囲外の入力は収集エラーポリシーに従って
記録・再処理する必要があります。

#### 制約条件

次の制約が適用されます。

* LSL/USLをCluster全体で非サポートとは扱いません。テーブル作成時の限界定義、メタデータ値の設定、
  DATA INSERT・Appendの限界検査は共通の経路です。既存METADATAに限界列をALTERで追加する
  以下の実習はStandard Editionで行います。
* LSL/USLを設定するには、Tagテーブルの3番目の列__Value__に__SUMMARIZED__を指定する必要があります。
* LSLはUSL以下であり、__Value__列の入力値はLSL以上USL以下である必要があります。__(LSL <= Value <= USL)__
* LSL/USL設定前に入力されたデータは検証されません。
* LSL/USL列をNULLにすると入力データを検証しません。
* LSL/USLは個別に使用できます。上限だけを適用する場合はUSLだけを設定できます。
* USLだけを設定すると上限超過のみ、LSLだけを設定すると下限未満のみを検査します。

#### サポートされるデータ型

限界列は対象の__Value__列と同じ型である必要があります。以下では基本数値型の規格範囲設定を
説明します。SUMMARIZED自体がサポートする型にはJSONも含まれるため、SUMMARIZEDを宣言できる条件と
数値限界の設定条件は区別します。

|型|説明|範囲|有効桁数|
|----|------|-----|----|
|short|16ビット符号付き整数型|-32767 ~ 32767|-|
|ushort|16ビット符号なし整数型|0 ~ 65534|-|
|integer|32ビット符号付き整数型|-2147483647 ~ 2147483647|-|
|uinteger|32ビット符号なし整数型|0 ~ 4294967294|-|
|long|64ビット符号付き整数型|-9223372036854775807 ~ 9223372036854775807|-|
|ulong|64ビット符号なし整数型|0~18446744073709551614|-|
|float|32ビット浮動小数点データ|-|6[^1]|
|double|64ビット浮動小数点データ|-|15[^1]|

#### LSL/USLの設定と使用

次のCREATE例は異なる選択肢を示します。以降のINSERT・UPDATE実習では基本の`example`だけを使用し、
代替テーブルは別途作成します。

タグメタデータテーブルの列に`LOWER LIMIT`（LSL）または`UPPER LIMIT`（USL）キーワードを指定します。
Tagテーブルの作成時またはメタデータ列の追加時に設定できます。

##### CREATE

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

2つの列を併用することも、片方だけ使用することもできます。
LSLだけを設定すると`Value >= LSL`を検査し、上限は制限しません。USL値を`NULL`にした場合と
同じ意味です。

```sql
CREATE TAG TABLE example_lower_only (
    tag_id  VARCHAR(50) PRIMARY KEY,
    time    DATETIME    BASETIME,
    value   INTEGER     SUMMARIZED)
METADATA (
    lsl    INTEGER LOWER LIMIT
);
```

##### ADD COLUMN

データ入力後に`ADD COLUMN`で追加する場合、デフォルト値は__NULL__です。

```sql
CREATE TAG TABLE example_alter_limits (
    tag_id  VARCHAR(50) PRIMARY KEY,
    time    DATETIME    BASETIME,
    value   INTEGER     SUMMARIZED
);

ALTER TABLE example_alter_limits METADATA ADD COLUMN (lsl INTEGER LOWER LIMIT);
ALTER TABLE example_alter_limits METADATA ADD COLUMN (usl INTEGER UPPER LIMIT);
```

[CREATE](#create)と同様、片方の属性だけを追加することもできます。

```sql
CREATE TAG TABLE example_alter_upper (
    tag_id  VARCHAR(50) PRIMARY KEY,
    time    DATETIME    BASETIME,
    value   INTEGER     SUMMARIZED
);

ALTER TABLE example_alter_upper METADATA ADD COLUMN (usl INTEGER UPPER LIMIT);
```

##### INSERT

特定のTAG IDのLSL/USL値を設定します。

```sql
INSERT INTO example metadata VALUES ('TAG_01', 100, 200);
```

設定後にタグデータを入力すると、次のように動作します。

```sql
INSERT INTO example VALUES ('TAG_01', NOW, 95);  -- 失敗
```

```text
[ERR-02342: SUMMARIZED value is less than LOWER LIMIT.]
```

```sql
INSERT INTO example VALUES ('TAG_01', NOW, 100); -- 成功（境界を含む）
```

```text
1 row(s) inserted.
Elapsed time: 0.000
```

```sql
INSERT INTO example VALUES ('TAG_01', NOW, 150); -- 成功
```

```text
1 row(s) inserted.
Elapsed time: 0.000
```

```sql
INSERT INTO example VALUES ('TAG_01', NOW, 200); -- 成功（境界を含む）
```

```text
1 row(s) inserted.
Elapsed time: 0.000
```

```sql
INSERT INTO example VALUES ('TAG_01', NOW, 205); -- 失敗
```

```text
[ERR-02341: SUMMARIZED value is greater than UPPER LIMIT.]
```

Tagテーブルを検索すると、規格範囲内のデータだけが入力されたことを確認できます。

```sql
SELECT * FROM example;
```

```text
TAG_ID                                              TIME                            VALUE       LSL         USL
------------------------------------------------------------------------------------------------------------------------------
TAG_01                                              2023-09-12 09:31:27 923:289:631 100         100         200
TAG_01                                              2023-09-12 09:31:27 929:013:232 150         100         200
TAG_01                                              2023-09-12 09:31:27 939:209:248 200         100         200
[3] row(s) selected.
Elapsed time: 0.001
```

##### UPDATE

LSL/USL列の値を変更します。入力済みのデータには遡及適用されない点に注意してください。

```sql
UPDATE example metadata SET lsl = 10, usl = 100 WHERE tag_id = 'TAG_01';
```

```text
1 row(s) updated.
Elapsed time: 0.001
```

```sql
SELECT tag_id, lsl, usl FROM example METADATA;
```

```text
TAG_ID                                              LSL         USL
----------------------------------------------------------------------------------------
TAG_01                                              10          100
[1] row(s) selected.
Elapsed time: 0.001
```

##### DELETE

LSL/USL列は`DROP COLUMN`で削除せず、値をNULLに設定して制約を解除します。

```sql
UPDATE EXAMPLE METADATA SET lsl = NULL, usl = NULL WHERE tag_id = 'TAG_01';
```

```text
1 row(s) updated.
Elapsed time: 0.001
```

```sql
SELECT tag_id, lsl, usl FROM example METADATA;
```

```text
TAG_ID                                              LSL         USL
----------------------------------------------------------------------------------------
TAG_01                                              NULL        NULL
[1] row(s) selected.
Elapsed time: 0.001
```

#### TRACEログでLSL/USL違反を確認

- 場所: `$MACHBASE_HOME/trc/machbase.trc`
- 簡易フィルター:
  ```bash
  grep LIMIT_DROP $MACHBASE_HOME/trc/machbase.trc | tail -n 20
  ```
- ログ形式: `LIMIT_DROP (TYPE=<UPPER|LOWER>) TABLE=<テーブル名> TAG=<tag name> <列名=値 ...>`
  - TYPE=LOWER/UPPERで違反した限界を区別します。
  - DATETIMEは`YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn`形式です。
- 実際の例:
  ```
  [2025-11-29 13:50:34 P-151395 T-126343511537344][QP-INFO] LIMIT_DROP (TYPE=LOWER) TABLE=TAG3 TAG=tag-1  TIME=2020-01-01 00:00:00 000:000:000 VALUE=5.55
  [2025-11-29 13:50:34 P-151395 T-126343511537344][QP-INFO] LIMIT_DROP (TYPE=UPPER) TABLE=TAG3 TAG=tag-1  TIME=2020-01-01 00:00:04 000:000:000 VALUE=30.55
  [2025-11-29 13:50:35 P-151395 T-126344475694784][QP-INFO] LIMIT_DROP (TYPE=LOWER) TABLE=TAG3 TAG=tag-2  TIME=1998-12-24 09:00:00 000:000:000 VALUE=0
  [2025-11-29 13:50:35 P-151395 T-126344475694784][QP-INFO] LIMIT_DROP (TYPE=UPPER) TABLE=TAG3 TAG=tag-2  TIME=1998-12-24 09:00:00 000:000:008 VALUE=45
  ```
- 活用のポイント
  - TAGごとのLOWER/UPPER違反時刻と値を一覧できます。
  - grepでTAG名・テーブル名を追加フィルターすると、特定対象だけを追跡できます。
- 注意: 1行は最大約4KBのため、列が多いと末尾が切れる場合があります。起動直後、メタキャッシュの
  準備前はテーブル名がIDで表示される場合があります。

[^1]: [IEEE 754](https://en.wikipedia.org/wiki/IEEE_754)

<a id="correction-duplication-policy-summary"></a>
<a id="tag-table-design-duplication-removal"></a>

### 補正と重複のポリシー

値の補正と重複排除は列定義だけで完結しませんが、スキーマ設計時に事前に決める必要があります。
補正が必要な場合は、変更可能な値の列、元データを別列または別テーブルに保持するか、補正後のROLLUPを
どう再構築するかを決めます。DATAのUPDATEはStandard Edition専用のため、Cluster Editionでは
補正の代わりに再入力と再集計の手順を設計します。詳細は
[データ補正](../tag-data-update-correction/#design-correction-tag)を参照してください。

同じタグと同じ軸値が繰り返し入力される可能性がある場合は、重複を許可するか、収集段階で排除するか、
Machbaseの自動重複排除を使用するかを決めます。設定変更と運用検証の手順は
[自動重複排除](../operations-lifecycle/#original-85-duplication-removal)を参照してください。

<a id="tag-schema-limitations-summary"></a>

### 制約とサポート範囲

TAGテーブルは反復観測の履歴に合わせた構造のため、すべてのSQL機能を一般的なリレーショナルテーブルと
同様にサポートするわけではありません。軸列、METADATA、値の補正、ROLLUP、Editionごとのサポート範囲を
設計前に確認します。ここでは設計案がサポート範囲内かを確認し、範囲外なら該当項目に戻ってスキーマを
調整します。非サポート機能と代表的なエラーは
[制約と注意事項](../constraints-errors-troubleshooting/#limitations-tag)を参照してください。

<a id="original-85-binary-columns"></a>

## Binary列


`BINARY(n)`はTagテーブルでセンサーフレーム用の固定長バイナリ値を保存します。
TAGで長さを省略した`BINARY`は32767バイトとして扱われます。必要なフレームサイズを明示すると、
保存・転送サイズを把握しやすくなります。TAG以外のテーブルでは長さ指定形式の`BINARY(n)`を
宣言できません。有効な長さは1～32K-1（1～32767）バイトで、インデックスは作成できません。

明示的なバイナリリテラルで`BINARY`値を入力します。

### DDLの規則

```sql
CREATE TAG TABLE t1(
  name VARCHAR(32) PRIMARY KEY,
  time DATETIME BASETIME,
  frame BINARY(4)
);
```

- 有効な長さ: `1 <= n <= 32767`（32K-1）。
- 範囲外の場合は作成時にエラーになります（`BINARY(0)`など）。
- `DESC`とテーブルメタデータは宣言されたバイト長を表示します（16進数の幅ではありません）。
  SQLの`LENGTH(binary_col)`は、短い入力値の末尾に付く0パディングを除いた表示値の長さを返します。

### サポートされる入力形式

```sql
X'hex_digits'
x'hex_digits'
B'bit_digits'
b'bit_digits'
O'octal_digits'
o'octal_digits'
```

| 形式 | 意味 | 単位 |
| --- | --- | --- |
| `X'...'`, `x'...'` | 16進数リテラル | 16進数2桁 = 1バイト |
| `B'...'`, `b'...'` | 2進数リテラル | 8ビット = 1バイト |
| `O'...'`, `o'...'` | 8進数リテラル | 8進数3桁 = 1バイト |

接頭辞は大文字・小文字のどちらも使用できます。

```sql
CREATE TAG TABLE t_bin (
    name  VARCHAR(20) PRIMARY KEY,
    time  DATETIME BASETIME,
    value BINARY(4)
);

INSERT INTO t_bin VALUES('hex1', '2024-01-01 00:00:00', X'0A');
INSERT INTO t_bin VALUES('hex2', '2024-01-01 00:00:01', x'00010203');
INSERT INTO t_bin VALUES('bit1', '2024-01-01 00:00:02', B'00001010');
INSERT INTO t_bin VALUES('oct1', '2024-01-01 00:00:03', O'012');
```

`X'0A'`、`B'00001010'`、`O'012'`はいずれも1バイトの値`0x0A`を表します。

### バイナリリテラルの規則

#### 16進数リテラル

`X'...'`と`x'...'`には`0-9`、`A-F`、`a-f`を使用できます。

```sql
X'00'
X'0AFF'
x'abcdef'
```

16進数の文字数は必ず偶数である必要があります。2桁が1バイトに相当します。

#### 2進数リテラル

`B'...'`と`b'...'`には`0`と`1`だけを使用できます。

```sql
B'00000000'  -- 0x00
B'00001010'  -- 0x0A
b'11111111'  -- 0xFF
```

ビット数は必ず8の倍数である必要があります。8桁が1バイトに相当します。

#### 8進数リテラル

`O'...'`と`o'...'`には`0-7`だけを使用できます。

```sql
O'000'  -- 0x00
O'012'  -- 0x0A
o'377'  -- 0xFF
```

8進数の文字数は必ず3桁単位である必要があります。各3桁の値は`000`から`377`までの
1バイトの範囲内である必要があります。

#### 空の値

単一引用符の中を空にして、長さ0のバイナリ値を表します。

```sql
X''
B''
O''
```

### 長さの制限

`BINARY(n)`列には最大`n`バイトまで入力できます。

```sql
CREATE TAG TABLE t_limit (
    name  VARCHAR(20) PRIMARY KEY,
    time  DATETIME BASETIME,
    value BINARY(2)
);

INSERT INTO t_limit VALUES('ok_hex', '2024-01-01 00:00:00', X'0AFF');
INSERT INTO t_limit VALUES('ok_bit', '2024-01-01 00:00:01', B'0000101011111111');
INSERT INTO t_limit VALUES('ok_oct', '2024-01-01 00:00:02', O'012377');

INSERT INTO t_limit VALUES('bad_hex', '2024-01-01 00:00:03', X'000102'); -- 失敗: 3バイト
```

入力元の種類に関係なく、最終的なバイナリ値が対象の`BINARY(n)`の長さを超えると入力は失敗します。
この規則はバイナリリテラルだけでなく、通常の文字列、従来の`'0x...'`文字列入力、他の`BINARY`列の
値を`INSERT ... SELECT`でコピーする場合にも同じように適用されます。

```sql
CREATE TAG TABLE t_src (
    name  VARCHAR(20) PRIMARY KEY,
    time  DATETIME BASETIME,
    value BINARY(8)
);

CREATE TAG TABLE t_dst (
    name  VARCHAR(20) PRIMARY KEY,
    time  DATETIME BASETIME,
    value BINARY(4)
);

INSERT INTO t_src VALUES('k1', '2024-01-01 00:00:00', X'0102030405060708');
INSERT INTO t_dst SELECT name, time, value FROM t_src; -- 失敗: 8バイトの値をBINARY(4)に入力
```

`CASE`、`INSERT ... SELECT`、ビューなどのSQL式で使用する場合も、最終的なバイナリ値が対象の
`BINARY(n)`の長さを超えると入力は失敗します。

### 無効な入力

次の入力は無効です。

```sql
X'0'        -- 16進数の文字数が奇数
X'0G'       -- Gは16進数の文字ではない
B'0101'     -- ビット数が8の倍数ではない
B'00000002' -- 2は2進数の文字ではない
O'12'       -- 8進数の文字数が3桁単位ではない
O'400'      -- 1バイトの範囲を超過
X'0102      -- 閉じる単一引用符がない
```

不正な値または長さ超過の入力は、次のエラーで失敗します。

```text
[ERR-02233: Error occurred at column (n): (Invalid insert value.)]
```

### 従来の文字列入力との違い

互換性のため、文字列形式の`'0x...'`入力も使用できます。`'0x...'`は文字列から`BINARY`列への
変換方式であり、`X'...'`、`B'...'`、`O'...'`はSQLでバイナリ値であることを明示する
バイナリリテラルです。

通常の文字列を`BINARY(n)`列に入力することもできますが、文字列のバイト長が`n`を超えると失敗します。
新しくSQLを記述する場合は、意味が明確なバイナリリテラル形式を推奨します。

`'0b...'`、`'0o...'`、引用符のない`0x...`、`0b...`、`0o...`形式はバイナリリテラルとして
サポートされません。

### 出力とツールの補足

- machsqlは`0x`のない大文字の16進数で出力します。短い入力値の末尾に付く0パディングは
  テキスト出力に表示されません。
- machloader: スキーマに`BINARY(n)`を宣言します。不正な値や長さ超過は失敗します。
- Machbase SQLCLI、ODBC、Java、C#、Node.jsドライバーは固定長バッファで送受信し、メタデータの
  `LENGTH`はバイト長です。

## 例の後片付け

このページで実際に作成したテーブルのみ削除します。代替DDLを実行していない場合は、
そのテーブルのDROP文も実行しません。

```sql
DROP TABLE time_sensor;
DROP TABLE rail_sensor;
DROP TABLE weather_station;
DROP TABLE temperature_sensor;
DROP TABLE thermo_sensor;
DROP TABLE vibration_sensor;
DROP TABLE example;
DROP TABLE example_lower_only;
DROP TABLE example_alter_limits;
DROP TABLE example_alter_upper;
DROP TABLE t1;
DROP TABLE t_bin;
DROP TABLE t_limit;
DROP TABLE t_dst;
DROP TABLE t_src;
```
