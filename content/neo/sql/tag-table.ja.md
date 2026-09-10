---
toc: true
title: タグテーブル
type: docs
weight: 01
---

## タグテーブルのデータモデルの概要 {#overview-of-the-tag-table-data-model}

<span id="개요"></span>

このドキュメントでは、Machbase時系列データベースでセンサーの時系列データを保存・検索・管理するために最適化された、タグテーブルの構造を詳しく説明します。

### 概念データモデル {#conceptual-data-model}

従来のセンサーデータモデルは、各行が1つのタイムスタンプを表し、各列が異なるセンサーの測定値（タグ）に対応する、CSVのような横持ち形式です。

**従来のデータモデル（横持ち形式）：**

| timestamp           | temperature | humidity | pressure | vibration |
| :------------------ | :---------- | :------- | :------- | :-------- |
| 2023-04-15 09:34:12 | 23.5        | 78.9     | 11       | 55        |
| 2023-04-15 09:34:13 | 23.7        | 75.6     | 12       | 51        |
| ...                 | ...         | ...      | ...      | ...       |

*   **特徴：**
    *   同時刻の測定値を1つのレコードとして管理します。
    *   元の横持ち形式のままデータを確認できます。
    *   センサーやタグの追加・削除に対するスキーマ変更の柔軟性が低く、テーブルの変更が必要になることがあります。

Machbaseのタグテーブルは、各行が特定のセンサー（タグ）の特定時刻の測定値を表す、縦持ち形式を使用します。

**Machbaseタグテーブルのデータモデル（縦持ち形式）：**

| TAGID         | timestamp           | value |
| :------------ | :------------------ | :---- |
| temperature   | 2023-04-15 09:34:12 | 23.5  |
| humidity      | 2023-04-15 09:34:12 | 78.9  |
| pressure      | 2023-04-15 09:34:12 | 11    |
| vibration     | 2023-04-15 09:34:12 | 55    |
| temperature   | 2023-04-15 09:34:13 | 23.7  |
| humidity      | 2023-04-15 09:34:13 | 75.6  |
| ...           | ...                 | ...   |

*   **特徴：**
    *   各測定値を個別のレコードに変換して保存します。
    *   タグ（センサー）の追加・削除にテーブル構造の変更が不要で、タグの増減に柔軟に対応できます。
    *   タグごとの効率的な集計と統計解析が可能です。
    *   横持ち形式より行数は増えますが、専用のアーキテクチャにより、通常は検索と取り込みの性能が向上します。

### スキーマによるデータモデルの比較 {#schema-based-data-model-comparison}

データモデルの違いは、テーブル作成の構文にも表れます。

**従来のスキーマ（例）：**

```sql
CREATE TABLE Vibration (
    time      DATETIME,
    temp      DOUBLE,
    humidity  DOUBLE,
    pressure  INTEGER,
    rms       LONG,
    tick      DOUBLE
    -- 新しいセンサーの種類ごとに列を追加
);
```
*これは一般的な設計ですが、変化の多いIoT環境ではスキーマの柔軟性が課題になります。*

**Machbaseタグテーブルのスキーマ：**

```sql
CREATE TAG TABLE Vibration (
    name  VARCHAR(80) PRIMARY KEY, -- タグ・センサーの識別子
    time  DATETIME    BASETIME,    -- 測定時刻
    value DOUBLE                   -- 実際の測定値
);
```
*この構造は、時系列データの基本要素である識別子・時刻・値に絞ってスキーマを簡素化します。追加の属性はメタデータで管理します。*

## タグテーブルの基本 {#tag-table-fundamentals}

<span id="기본-구조"></span>

### 構造 {#structure}

タグテーブルは、構造化されたセンサーデータの効率的な取り込み、検索、圧縮のために最適化されたテーブルです。レコードの基本構造は、次の3要素で構成されます。

1.  **識別子（既定では`name`列）**：特定のセンサーやデータソースを識別する一意の文字列です（例：`"sensor-A"`、`"factory1-machine2-temp"`）。関連するメタデータ構造の主キーとして機能します。
2.  **時刻（既定では`time`列）**：データの生成時刻または記録時刻を表すタイムスタンプです。64ビット整数として保存され、ナノ秒精度に対応します。
3.  **値（既定では`value`列）**：指定時刻の識別子に対応する、実際の測定値やイベントデータです。各種データ型に対応しますが、一般的には`DOUBLE`（64ビット浮動小数点数）を使い、多様な分析機能を利用できます。

内部では、タグの属性を表すメタデータと実際の時系列データを分離します。

```
       タグテーブル：Vibration
+--------------------------------------+------------------------------------------+
|        メタ（センサー属性）      |            データ（センサー測定値）        |
| +---------+-----------+------------+ | +----+---------------------------+-----+ |
| | NAME    | Attribute1| Attribute2 | | | ID | TIME（ナノ秒）        |VALUE| |
| +---------+-----------+------------+ | +----+---------------------------+-----+ |
| | Sensor-A| LocationX | TypeY      | | | 0  | 1719292147529850600       |-1.3 | |
| | Sensor-B| LocationZ | TypeW      | | | 1  | 1719292148529850600       |-2.3 | |
| | Sensor-C| LocationX | TypeY      | | | 2  | 1719292149529850600       |-3.3 | |
| | ...     | ...       | ...        | | | 0  | 1719292150000000000       |-4.3 | |
| +---------+-----------+------------+ | | 0  | 1719292167529850600       |-5.3 | |
|                                      | | 2  | 1719292177529850600       |-6.3 | |
| (_Vibration_METAテーブルで管理)   | | 1  | 1719292187529850600       |-7.3 | |
|                                      | | .. | ...                       | ... | |
|                                      | +----+---------------------------+-----+ |
|                                      | (_Vibration_DATA_Nパーティションで管理)|
+--------------------------------------+------------------------------------------+
```

基本的な`CREATE`文は、この構造を反映します。

```sql
CREATE TAG TABLE Vibration (
    name  VARCHAR(80) PRIMARY KEY, -- メタテーブルに関連付ける一意の識別子
    time  DATETIME    BASETIME,    -- インデックスの基準となる時刻列
    value DOUBLE                   -- 基本の値列
    -- 必要に応じてデータ列を追加できます
);
-- メタデータ列はMETADATA句で別途定義します
```

### 対応するデータ型 {#supported-data-types}

<span id="지원-데이터-타입"></span>

Machbaseタグテーブルの`value`列と追加データ列は、以下のデータ型に対応しています。

| 型       | 説明                      | 範囲・表現                                          | NULLの表現           |
| :------- | :------------------------------- | :-------------------------------------------------------------- | :---------------------------- |
| `SHORT`    | 16ビット符号付き整数            | -32767 to 32767                                                 | -32768                        |
| `USHORT`   | 16ビット符号なし整数          | 0 to 65534                                                      | 65535                         |
| `INTEGER`  | 32ビット符号付き整数            | -2147483647 to 2147483647                                       | -2147483648                   |
| `UINTEGER` | 32ビット符号なし整数          | 0 to 4294967294                                                 | 4294967295                    |
| `LONG`     | 64ビット符号付き整数            | -9223372036854775807 to 9223372036854775807                     | -9223372036854775808          |
| `ULONG`    | 64ビット符号なし整数          | 0 to 18446744073709551614                                      | 18446744073709551615          |
| `FLOAT`    | 32ビット浮動小数点数            | ±1.175494e-38 to ±3.402823e+38                                  | 3.402823466e+38               |
| `DOUBLE`   | 64ビット浮動小数点数            | ±2.225074e-308 to ±1.797693e+308                                | 1.7976931348623158e+308       |
| `DATETIME` | 日時（ナノ秒精度）| 1970-01-01 00:00:00 000:000:000 UTC以降                        | N/A                           |
| `VARCHAR`  | 可変長文字列（UTF-8） | 1バイト〜32KB（32767バイト）                                    | NULL                          |
| `IPV4`     | IPv4アドレス                     | "0.0.0.0" to "255.255.255.255"                                  | NULL                          |
| `IPV6`     | IPv6アドレス                     | "::" to "FFFF:FFFF:FFFF:FFFF:FFFF:FFFF:FFFF:FFFF"               | NULL                          |
| `JSON`     | JSONデータ型                   | データ長：1バイト〜32KB。パス長：1〜512文字 | NULL                          |

**注意：** タグテーブルは、`TEXT`と`BINARY`データ型には**対応していません**。

## タグテーブルの作成と内部構造 {#tag-table-creation-and-internal-architecture}

### タグテーブルの作成 {#creating-tag-tables}

タグテーブルを作成する基本構文は以下のとおりです。

```sql
CREATE TAG TABLE table_name (
    name_column VARCHAR(size) PRIMARY KEY, -- タグの識別子列
    time_column DATETIME BASETIME,         -- BASETIME属性を持つ時刻列
    value_column datatype [SUMMARIZED]     -- 値列
    [, additional_data_column datatype ...] -- 省略可能な追加データ列
)
METADATA (
    meta_column1 datatype,                 -- メタデータ列
    meta_column2 datatype
    [, ...]
)
[ table_property = value [, ...] ];        -- 省略可能なテーブル属性
```

**主要な要素：**

| 要素                         | 説明                                                                                                                                 | 領域       |
| :--------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------ | :--------- |
| `name_column` (`PRIMARY KEY`)  | センサー名など、一意のタグ識別子を保存する列。最大長を指定した`VARCHAR`型が必要で、`PRIMARY KEY`として宣言します。 | データ/メタ |
| `time_column` (`BASETIME`)   | 各データのタイムスタンプを保存する列。通常は`DATETIME`型で、主な時刻インデックスを表す`BASETIME`属性が必要です。 | データ     |
| `value_column` [`SUMMARIZED`] | 測定値を保存する列。一般的な型は`DOUBLE`や`LONG`です。`SUMMARIZED`を指定すると、この列の組み込み統計集計が有効になります。 | データ     |
| `additional_data_column`   | 同じタイムスタンプの値に品質フラグやバッチ番号などの補足データを保存する、省略可能な列です。              | データ     |
| `METADATA`句            | `name_column`で識別する各タグの属性（メタデータ）を保存する列を定義します。属性は`name_column`を介して関連付けられます。 | メタ       |
| `table_property`             | パーティションや統計など、テーブルの動作とリソース割り当てを設定する、省略可能なキーと値の組です。                              | テーブル   |

### タグテーブルの属性 {#tag-table-properties}

<span id="주요-속성"></span>

タグテーブルの作成時に以下の属性を設定し、性能とリソース使用量を調整できます。

| 属性                             | 説明                                                                                                                               | 既定値 | 注意                                                                                         |
| :------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------- | :------ | :-------------------------------------------------------------------------------------------- |
| `TAG_PARTITION_COUNT`            | 作成する内部データパーティション（サブテーブル）の数。取り込みと検索の並列度に影響します。                                    | 4       | 値を大きくすると並列度が向上しますが、メモリ使用量も増えます。リソースの少ないエッジデバイスでは、1や2などの小さい値を使用します。 |
| `TAG_DATA_PART_SIZE`             | パーティション内のデータ格納単位の目標サイズ（バイト）。                                                                          | 16MB    | データのバッファリングとインデックスに関するメモリ割り当てに影響します。                          |
| `TAG_STAT_ENABLE`                | タグごとの統計情報（最小値、最大値、件数、合計）の収集を有効・無効にします。`V$tableName_STAT`ビューに必要です。              | 1 (ON)  | 統計が不要な場合は0で無効にでき、オーバーヘッドを抑えられます。           |
| `TAG_DUPLICATE_CHECK_DURATION`   | 取り込み時に、同じnameとtimeを持つ重複レコードを除外する確認期間（分）。            | 0       | データを再送するソースからの重複データの管理に役立ちます。          |
| `VARCHAR_FIXED_LENGTH_MAX`       | 主データ領域にインライン保存する`VARCHAR`データの最大長（バイト）。長い文字列は外部に保存される場合があります。 | 15      | 可変長文字列の保存効率と検索性能に影響します。               |

**属性を指定する例：**

```sql
CREATE TAG TABLE basic (
    name VARCHAR(32) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
)
METADATA (
    factory VARCHAR(32),
    equipment VARCHAR(64)
)
TAG_PARTITION_COUNT=2,
TAG_STAT_ENABLE=0,
TAG_DUPLICATE_CHECK_DURATION=3;
```

### 内部テーブル構造 {#internal-table-structure}

タグテーブル（例：`MYTAG`）を作成すると、内部で以下の関連オブジェクトを作成・管理します。

1.  **`MYTAG`（仮想テーブル）**：データを検索する主なインターフェースです。メタデータと時系列データを統合したビューを提供します。
2.  **`_MYTAG_META`（メタデータテーブル）**：`METADATA`句で定義した属性を保存します。`name`列が主キーとなり、タグごとのメタデータの一意性を保証します。高速検索のため、通常はメモリ上に保持します。
3.  **`_MYTAG_DATA_N`（データパーティションテーブル）**：実際の時系列データ（`time`、`value`、追加データ列）を保存する内部テーブルです。`N`は0〜`TAG_PARTITION_COUNT - 1`で、タグの`name`に基づいてデータを分散します。
4.  **`V$MYTAG_STAT`（統計ビュー）**：`TAG_STAT_ENABLE=1`の場合に、データパーティションから得たタグごとの統計（最小・最大時刻、最小・最大値、件数、合計）を提供するシステムビューです。

```
      << MYTAGの内部構造 >>

+---------------------------------------------------+
|                  MYTAG（仮想テーブル）            |
|  (検索インターフェース)                                |
+---------------------+-----------------------------+
                      |                             |
+---------------------v-----------------------------+ +-----------------------+
|            _MYTAG_META（メタデータテーブル）           | |   V$MYTAG_STAT        |
| +-------+-----------+-----------+-----+           | | (統計ビュー)     |
| | _ID   | NAME      | factory   | equip |         | +-----------------------+
| +-------+-----------+-----------+-----+           |           ^
| | 1     | sensor-A  | fac1      | eq1   | <------lookup-----+
| | 2     | sensor-B  | fac1      | eq2   |         |           |
| | ...   | ...       | ...       | ...   |         |           | (集計元)
+---------+-----------+-----------+-------+         |           |
       (メモリ上の検索)                     |           |
                                                    |           |
                      +-----------------------------+-----------+
                      | (hash(NAME)によるデータの分散)
                      |
        +-------------+-------------+ ... +-------------+
        |             |             |     |             |
+-------v-------+ +---v-----------+ +-----+-------------v---+
| _MYTAG_DATA_0 | | _MYTAG_DATA_1 | | ... | | _MYTAG_DATA_3 |
| +---+ T | V + | | +---+ T | V + | |     | | +---+ T | V + |
| | 0 |...|...| | | | 1 |...|...| | |     | | | 3 |...|...| |
| | 0 |...|...| | | | 1 |...|...| | |     | | |.. |...|...| |
| +---+---+---+ | | +---+---+---+ | |     | | +---+---+---+ |
+---------------+ +---------------+ +-----+ +---------------+
   (データパーティション) (データパーティション)         (データパーティション)
```

## タグテーブルのメタデータ管理 {#metadata-management-in-tag-tables}

<span id="메타데이터-관리"></span>

### メタデータの役割 {#the-role-of-metadata}

メタデータは、生の時系列データに必要な背景情報を与えます。場所、機器の種類、製造元、測定単位などの属性を各タグ（`name`）に関連付けると、以下が可能になります。

*   **属性に基づく検索**：タグ名だけでなく、特徴に基づいてデータを絞り込み、検索します。
*   **階層的な整理**：センサー、機器、場所などの関係を表現します。
*   **分析の拡張**：メタデータで定義したカテゴリごとに、データをグループ化・集計します。

**概念的な階層の例：**

```
企業
├── city1工場
│   ├── 空調機
│   │   ├── タグ（電流センサー）
│   │   ├── タグ（電圧センサー）
│   │   └── ...
│   ├── 冷蔵装置
│   ├── コンプレッサー
│   └── クレーン
├── city2工場
│   ├── ... (同様の構造)
└── city3工場
    └── ... (同様の構造)
```

各タグには、工場や機器などの背景情報があります。

**用途の例：**

*   「蔚山工場のクレーンに関連するすべての電流センサーについて、直近1分間のデータを取得する」。
*   「冷蔵装置に属し、名前がCurrentで始まるセンサーについて、2022年1月31日の11:00〜12:00の全データを取得する」。
*   「全工場の、名前が空調機で始まる機器について、Current-3というタグの先月の最大値を求める」。

### メタデータ列の定義と使用 {#defining-and-utilizing-metadata-columns}

メタデータ列は、`CREATE TAG TABLE`文の`METADATA`句で定義します。

```sql
CREATE TAG TABLE MYTAG (
    name VARCHAR(32) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
)
METADATA ( -- ここでメタデータ列を定義
    factory VARCHAR(32),
    equipment VARCHAR(64)
);
```

内部メタデータテーブル（`_tableName_META`）に`ALTER TABLE`を実行して、既存のタグテーブルにメタデータ列を追加することもできます。

```sql
ALTER TABLE _mytag_meta ADD COLUMN (line VARCHAR(16) DEFAULT 'op01');
```

メタデータは`_tableName_META`に保存され、主な仮想タグテーブルの検索時に効率的に結合できるよう、通常はメモリ上に保持されます。`name`列が、メタデータ属性と時系列データを関連付ける一意のキーです。

```
       メタデータ領域（_mytag_meta）             データ領域（_mytag_data_N）
+---------+----------+------------+----------+   +----+---------------------+-------+
| NAME    | factory  | equipment  | line     |   | ID | TIME                | VALUE |
+---------+----------+------------+----------+   +----+---------------------+-------+
| Sensor-A| Seoul    | drill      | op01     |   | 0  | ...                 | -1.3  | <= Sensor-Aのデータ
| Sensor-B| Seoul    | punch      | op01     |   | 1  | ...                 | -2.3  | <= Sensor-Bのデータ
| Sensor-C| Ulsan    | rolling    | op01     |   | 2  | ...                 | -3.3  | <= Sensor-Cのデータ
+---------+----------+------------+----------+   | ...| ...                 | ...   |
       (NAMEごとに一意のエントリ)                      (時系列測定値)
```

### メタデータの取り込み {#metadata-ingestion}

新しいタグのメタデータは、通常はそのタグの初回のデータ取り込み時に作成されます。append時にタグの`name`が`_tableName_META`に存在しない場合は、その操作で渡された値を使って新しいメタデータレコードを作成します。

**注意**：タグの`name`がメタデータテーブルに存在する場合、その後のappend操作では既存のメタデータ属性を**更新しません**。更新には、`UPDATE ... METADATA`を明示的に実行してください。

### メタデータで絞り込む検索 {#retrieving-data-with-metadata-filters}

仮想タグテーブルへのクエリには、データ列（`time`、`value`など）とメタデータ列（`factory`、`equipment`など）の両方の条件を指定できます。エンジンはタグの`name`に基づき、データパーティションとメタデータテーブルを自動的に結合します。

```sql
-- 特定の工場と機器に属するタグのデータを取得
-- 指定した時間範囲を使用
SELECT name, time, value, factory, equipment
FROM mytag
WHERE factory = 'Seoul'            -- メタデータによる絞り込み
  AND equipment LIKE '%chill%'     -- メタデータによる絞り込み（LIKEに対応）
  AND name = 'tag-1'               -- データ・タグ識別子による絞り込み
  AND time BETWEEN TO_DATE('2022-01-01 00:00:00')
               AND TO_DATE('2022-12-31 23:59:59'); -- 時刻による絞り込み
```

### メタデータエントリの変更 {#modifying-metadata-entries}

特定のタグの既存のメタデータ属性は、`UPDATE ... METADATA SET`構文で変更できます。

```sql
UPDATE mytag METADATA SET equipment = 'chiller_unit_01', factory = 'Busan'
WHERE name = 'tag-existing'; -- 'name = ...'で対象タグを必ず指定
```

**制約：**

*   `WHERE`句には、`name`列の等価条件（`WHERE name = 'specific_tag_name'`）が**必要**です。
*   メタデータの格納構造がキー・値形式のため、メタデータ更新では`WHERE`句に他の条件を指定できません。
*   このコマンドは、メタデータ属性値に基づく一括更新には直接対応していません。将来拡張される可能性があります。

### メタデータエントリの削除 {#deleting-metadata-entries}

メタデータエントリは、`DELETE FROM ... METADATA`構文で削除できます。

```sql
DELETE FROM mytag METADATA WHERE name = 'tag_to_remove';
```

**制約：**

*   データパーティションにそのタグの時系列データが残っている場合、メタデータエントリは**削除できません**。
*   メタデータを削除する前に、`DELETE FROM table_name WHERE name = '...'`で関連する時系列データを削除する必要があります。

### 用途：メタデータによるタグの動的な分類 {#use-case-dynamic-tag-categorization-via-metadata}

メタデータ列を使うと、基本データ構造を変更せずに、タグを動的に分類したり注記を付けたりできます。

**シナリオ**：エラーが頻繁に発生するタグや、特定のレポートで使用するタグを管理します。

1.  **`alias`メタデータ列を追加：**
    ```sql
    ALTER TABLE _basic_meta ADD COLUMN (alias VARCHAR(128) DEFAULT 'normal');
    ```

2.  **特定のタグのメタデータを更新：**
    ```sql
    UPDATE basic METADATA SET alias = 'error' WHERE name = 'tag-2';
    UPDATE basic METADATA SET alias = 'report' WHERE name = 'tag-4';
    ```

3.  **動的なカテゴリに基づいてデータを検索：**
    ```sql
    -- 指定した期間の、'error'を付けたタグのデータを検索
    SELECT * FROM basic
    WHERE alias = 'error'
      AND time BETWEEN '2022-01-01' AND '2022-12-31';

    -- 'report'を付けたタグのデータを検索
    SELECT * FROM basic
    WHERE alias = 'report'
      AND time BETWEEN '2022-01-01' AND '2022-12-31';
    ```

### `name`列の一意性と用途 {#the-uniqueness-and-usage-of-the-name-column}

`name`列（またはタグテーブルで`PRIMARY KEY`に指定した列）は、以下の役割を担います。

*   **メタデータの主キー**：`_tableName_META`内の各タグを一意に識別し、メタデータ属性の作成・取得・更新・削除（CRUD）に使用します。タグ名は一意である必要があります。
*   **検索時の関連付け**：クエリで、メタデータ属性と対応する時系列データを関連付けます。
*   **直接の絞り込み**：特定のタグの生データや集計データを、直接選択・絞り込みできます。

**`name`値の構成方法：**

*   **タグ数が少ない場合（100未満）、メタデータなし**：`'tag_001'`、`'temp_sensor_main'`など、簡単で読みやすい一意の文字列を使います。一般的には、`name`で直接検索します。
*   **タグ数が多い場合（1000を大幅に超える）、豊富なメタデータあり**：完全な`name`で直接検索する頻度は低くなる場合があります。主要なメタデータを連結した名前（例：`'factoryA-equipmentX-sensorTypeZ-instance01'`）で一意性と背景情報を確保し、主な検索では専用のメタデータ列を使って絞り込みます（例：`WHERE factory = 'factoryA' AND equipment = 'equipmentX'`）。大規模で複雑なシステムでは、この方法がタグの探索と絞り込みに適しています。

## タグテーブルの使用 {#tag-table-utilization}

### タグテーブル設計の例 {#example-tag-table-design}

特定の製造ロットに関連する各種センサー測定値を追跡する製造システムを例にします。

```sql
-- タグテーブル定義
CREATE TAG TABLE tag (
    name                   VARCHAR(100) PRIMARY KEY, -- 工場・機器・tag_idなどを組み合わせた一意の識別子
    time                   DATETIME BASETIME,
    value                  DOUBLE SUMMARIZED,
    lot_no                 VARCHAR(32)             -- 各測定に固有の追加データ列
)
METADATA (
    factory_id             VARCHAR(16),             -- メタデータ：工場識別子
    equipment_id           VARCHAR(16),             -- メタデータ：機器識別子
    tag_id                 VARCHAR(32)              -- メタデータ：基本センサー識別子
);

-- 必要に応じて、lot_noの検索を高速化するため追加データ列にインデックスを作成
CREATE INDEX idx_tag_lot_no ON tag (lot_no) INDEX_TYPE TAG;
```

**クエリの例：**

```sql
-- 特定の工場の全タグデータを取得
SELECT * FROM tag WHERE factory_id = 'fac01';

-- 特定の工場の特定の機器のデータを取得
SELECT * FROM tag WHERE factory_id = 'fac01' AND equipment_id = 'equip01';

-- 特定の製造ロットに関連するデータから指定した列を取得
SELECT name, time, value FROM tag WHERE lot_no = 'lot2001'; -- 有効な場合はidx_tag_lot_noを使用

-- 指定した期間の、特定の機器・工場に属する特定タグのデータを取得
SELECT * FROM tag
WHERE factory_id = 'fac01'
  AND equipment_id = 'equip01'
  AND tag_id IN ('tag01', 'tag02', 'tag03') -- メタデータのtag_idで絞り込み
  AND time BETWEEN TO_DATE('2023-08-15 00:00:00') AND TO_DATE('2023-08-15 23:59:59');
```

### 基本的なデータ検索 {#basic-data-retrieval-operations}

標準SQLの`SELECT`文を使い、`name`と`time`の内部インデックスを活用します。

```sql
-- 総レコード数を取得
SELECT count(*) FROM tag;

-- データ全体の時間範囲を取得
SELECT min(time), max(time) FROM tag;

-- 指定した時間範囲の、特定タグの生データを取得（時刻順）
SELECT time, value FROM tag
WHERE name = 'TAG_00001'
  AND time BETWEEN TO_DATE('2023-01-01') AND TO_DATE('2023-01-31');

-- 複数の指定タグの生データを、時刻の逆順で取得
SELECT /*+ SCAN_BACKWARD(tag) */ time, value FROM tag
WHERE name IN ('TAG1', 'TAG2')
  AND time BETWEEN TO_DATE('2023-01-01') AND TO_DATE('2023-01-31');
```

**注意：** `name`列の条件では、通常は等価比較（`=`）と`IN`リストによる比較を効率的に処理できます。

### 複雑な分析のシナリオ {#complex-analytical-scenarios}

タグテーブルは、メタデータやロールアップ機能と組み合わせることで、高度な分析に対応できます。

**シナリオの設定例：**

```sql
CREATE TAG TABLE MYTAG (
    name VARCHAR(32) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
)
METADATA (
    factory VARCHAR(32),
    equipment VARCHAR(64),
    alias VARCHAR(64) -- 動的なタグ分類用
)
WITH ROLLUP; -- 時刻による自動集計を有効化（詳細はロールアップのドキュメントを参照）
```

**クエリの種類：**

1.  **生データの抽出：**
    *   Seoul工場の、2024年2月12日の全タグデータ。
    *   Seoul工場のコンプレッサーの、2024年7月12日12:00〜13:00のデータ。
    *   全工場の冷却装置に関連する、名前がCurrentで始まるタグの、2024年9月13日13:20〜13:30のデータ。
    *   別名CriticalSensorを付けた全タグの、2024年12月23日〜12月29日のデータ。

2.  **統計データの抽出（ロールアップを使用）：**
    *   Seoul工場のクレーンの全タグについて、2024年全体の月別`value`平均。
    *   Cheongju工場の、名前にCurrentを含むタグについて、2024年6月の日別`value`最大値。
    *   全工場の、別名CriticalSensorを付けた全タグについて、2020年〜2024年の月別`value`平均。

3.  **統計データに基づく分析（ロールアップを使用）：**
    *   Powerを含む全センサーについて、過去5年間の最大値が記録された週と、その最大値を求める。
    *   Cheongju工場のTemperatureを含む全センサーについて、過去1年間で日別の最高温度が最も高かった日と、その日の平均温度を求める。
    *   全工場のPressureを含むセンサーについて、過去3か月で日別の平均圧力が最も高かった日と、その平均値を求める。

**クエリ例（時間別平均と最後の値）：**

```sql
-- factory1の全タグについて、12時間の期間の時間別平均と最後の値を取得
SELECT
    name,
    ROLLUP('hour', 1, time) AS rollup_time, -- 時刻を時間単位に集約
    AVG(value) AS avg_value,
    LAST(time, value) AS last_value -- その時間帯の最後の値を取得
FROM mytag
WHERE name IN (SELECT name FROM _mytag_meta WHERE factory = 'factory1') -- メタデータでタグを絞り込み
  AND time BETWEEN TO_DATE('2000-01-01 00:00:00') AND TO_DATE('2000-01-01 11:59:59') -- 時間範囲
GROUP BY name, rollup_time -- タグと集約した時間区間でグループ化
ORDER BY name, rollup_time;
```

### PIVOTによるデータモデルの変換 {#data-model-transformation-using-pivot}

`PIVOT`句を使うと、分析やレポートの要件に合わせ、縦持ちのタグテーブルを従来のモデルに似た横持ち形式に変換できます。

```sql
-- 時刻を基準に、指定したタグの値を列に変換
SELECT *
FROM (
    -- 対象データを選択するサブクエリ
    SELECT time, name, value -- nameがtagid、valueがdvalueに対応する例
    FROM mytag
    WHERE time BETWEEN TO_DATE('2018-12-07 00:00:00') AND TO_DATE('2018-12-08 05:00:00')
      AND name IN ('FRONT_AXIS_TORQUE', 'REAR_AXIS_TORQUE', 'HOIST_AXIS_TORQUE', 'SLIDE_AXIS_TORQUE')
)
PIVOT (
    SUM(value) -- 同じ時刻・タグに複数の値がある場合に適用する集計関数
    FOR name -- 一意の値が新しい列見出しになる列
    IN ('FRONT_AXIS_TORQUE', 'REAR_AXIS_TORQUE', 'HOIST_AXIS_TORQUE', 'SLIDE_AXIS_TORQUE') -- 列に変換するタグ名の一覧
)
WHERE "FRONT_AXIS_TORQUE" >= 40 AND "REAR_AXIS_TORQUE" >= 20; -- 変換後の列への任意の絞り込み
```

**出力例（概念図）：**

```
time                          'FRONT_AXIS_TORQUE' 'REAR_AXIS_TORQUE' 'HOIST_AXIS_TORQUE' 'SLIDE_AXIS_TORQUE'
----------------------------- ------------------- ------------------ ------------------- -------------------
2018-12-07 16:42:29 840:000:000 12158               7244               NULL                NULL
2018-12-07 14:56:26 220:000:000 3308                663                NULL                NULL
...                           ...                 ...                ...                 ...
```
*（注意：変換後の列名がキーワードと一致する場合や特殊文字を含む場合は、引用符が必要になることがあります）。*

### データの削除 {#data-deletion-operations}

タグテーブルの削除は、主に時刻またはタグ単位で行います。appendに最適化した構造のため、通常は個別レコードの更新や個別削除に対応していません。

**削除構文の例：**

```sql
-- 全タグの、指定時刻より前のデータを削除
DELETE FROM table_name BEFORE TO_DATE('2023-01-15 00:00:00');

-- テーブルの全データを削除（慎重に実行してください）
DELETE FROM table_name;

-- 指定タグの全データを削除
DELETE FROM table_name WHERE name = 'TAG01';

-- 指定タグの、指定時刻より前のデータを削除
DELETE FROM table_name WHERE name = 'TAG01' AND time < TO_DATE('2023-02-01 00:00:00');
```

## タグテーブルのインデックス {#indexing-in-tag-tables}

### 内部インデックスと外部インデックス {#internal-versus-external-indexes}

タグテーブルは、`name`と`time`列に自動作成する、最適化された**内部インデックス**を備えます。一般的な時系列クエリの性能を支える構造です。結果を時刻順に並べるには、`ORDER BY time`を指定してください。

*   **`WHERE name = '...'`**：内部インデックスで、指定タグの全データを効率的に検索します。
*   **`WHERE time BETWEEN ... AND ...`**：内部インデックスで、指定期間の全タグのデータをスキャンします。
*   **`WHERE name = '...' AND time BETWEEN ... AND ...`**：内部インデックスで、指定タグの指定期間のデータを効率的に取得します。
*   **`WHERE name = '...' AND time BETWEEN ... AND ... AND value > ...`**：内部インデックスで対象の`name`と`time`のデータブロックを検索し、取得データに`value`の条件を適用します。

**制約**：`name`や`time`の条件がなく、`value`や追加データ列*だけ*で絞り込むクエリは、主な内部インデックスを有効に使えません。

*   **`WHERE name = '...' AND value > ...`（時刻条件なし）**：対象タグに属する*すべて*のデータブロックをスキャンして`value`の条件を適用するため、そのタグのデータ量に比例して性能が低下します。

このような場合には、**外部インデックス**を作成できます。

### 外部インデックスの作成と使用 {#external-index-creation-and-usage}

`value`や追加データ列に外部インデックスを明示的に作成し、主にその列で絞り込むクエリを高速化できます。

**構文：**

```sql
CREATE INDEX index_name ON table_name (column_name) [INDEX_TYPE TAG];
-- INDEX_TYPE TAGは、タグテーブルのデータ列のインデックスを最適化します。
```

**例：**

```sql
CREATE TAG TABLE mytag (
    name VARCHAR(100) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED,
    lot_no VARCHAR(32)
);

-- value列とlot_no列に外部インデックスを作成
CREATE INDEX idx_mytag_value ON mytag(value) INDEX_TYPE TAG;
CREATE INDEX idx_mytag_lotno ON mytag(lot_no) INDEX_TYPE TAG;

-- このクエリでは外部インデックスidx_mytag_valueを使用できる可能性があります
SELECT * FROM mytag WHERE name = 'TAG-2' AND value > 33;

-- このクエリでは外部インデックスidx_mytag_lotnoを使用できる可能性があります
SELECT * FROM mytag WHERE lot_no = 'LOTXYZ' AND time > TO_DATE('2024-01-01');
```

**外部インデックスの特徴：**

*   **非同期**：インデックスの更新は、データ取り込みより少し遅れる場合があります。新しいデータが外部インデックスにまだ反映されていない短い期間が生じます。
*   **ローカルな構造**：通常はデータパーティションに沿って分割されます。データ量が増えると、外部インデックスを使っても検索性能が低下する場合がありますが、インデックスなしの全スキャンより大幅に効率的です。
*   **リソース消費**：追加のストレージ領域を使用し、データ取り込み時のオーバーヘッドが増えます。

## タグテーブルへのデータ取り込み {#data-ingestion-into-tag-tables}

### 取り込み方法の概要 {#ingestion-methods-overview}

Machbase Neoは、性能要件やクライアント環境に応じた複数のタグテーブルへの取り込み方法を提供します。

```
+-------------------+      +-------------------+      +-------------------+
|    ODBC/JDBC/     |      |    MQTT/gRPC/     |      |    Machbase       |
|   .NET Clients    | ---> |   HTTP Clients    | ---> |     Native        | ---> Machbase Neo
+-------------------+      +-------------------+      |  CLI/SDK (C/Py)   |      (Tag Table)
                                                     +-------------------+
 (標準SQL INSERT,      (REST APIのappend,       (高スループット
  またはAppendプロトコル)        MQTT購読)        Appendプロトコル)
```

### 取り込み方法の詳細 {#detailed-ingestion-approaches}

1.  **SQLの`INSERT`文：**
    *   標準の`INSERT INTO table_name VALUES (...)`構文を使用します。
    *   リクエスト・レスポンス方式で動作します。
    *   少量または低頻度の挿入に適しています。
    *   性能上の制約のため、高スループットで大量の時系列データを取り込む用途には**推奨しません**。

2.  **Appendプロトコル：**
    *   一括取り込みに最適化された、Machbase専用の高性能プロトコルです。
    *   ネットワークのオーバーヘッドと、レコードごとのサーバー処理を最小化します。
    *   以下から使用できます。
        *   **Machbase CLI**：ファイルからの一括取り込み用ユーティリティ。
        *   **ODBC/JDBC/.NET**：Machbaseドライバーの拡張APIでAppendを利用できます。
        *   **C/C++/Go SDK**：ネイティブライブラリからAppend APIに直接アクセスし、高い性能を得られます。
        *   **Python（`machbaseAPI`）**：Append機能を提供するラッパーライブラリ。
    *   高スループットが必要な、多くの時系列取り込み用途に**推奨**します。

3.  **REST API：**
    *   Machbase Neoは、データ操作用のHTTPエンドポイントを提供します。
    *   取り込みエンドポイントは、内部で効率的なAppendプロトコルを使用する、`append`メソッドパラメーターに対応します。
    *   WebクライアントやHTTP連携のシステムに適しています。

4.  **その他の言語（Python、Go、R）：**
    *   通常はCLIやODBC・ネイティブSDKのラッパーを使い、効率的なAppendプロトコルを利用します。

**性能に関する注意**：毎秒数十万〜数百万件の挿入が必要な高周波振動データなど、厳しい要件では、最大の取り込み速度を得るためにネイティブC/C++ SDKのAppend APIが必要になる場合があります。

## 運用上の考慮事項 {#operational-considerations}

### 使用上の主な注意 {#key-usage-precautions}

*   **メモリ消費**：各タグテーブルは、パーティション（`TAG_PARTITION_COUNT`）とデータバッファー（`TAG_DATA_PART_SIZE`）に応じた基本メモリを消費します。多数のテーブルを作成するとサーバー全体のメモリ使用量が大きく増えるため、利用可能なリソースに応じて計画してください。
*   **検索性能**：インデックス付きの列（`name`、`time`、外部インデックスの列）に条件がない`SELECT`は、全テーブルまたは大きな範囲のスキャンとなり、データ量に応じて性能が低下します。可能な限り、`name`や`time`の範囲条件を指定してください。
*   **外部インデックス**：時刻条件なしで、データ列や値列だけを頻繁に絞り込む場合に作成を検討してください。ストレージ使用量と取り込みのオーバーヘッドが増えます。
*   **データの不変性**：タグテーブルは追記用に設計されており、既存データの更新には対応しません。削除は主に時刻またはタグ全体を基準に行います。
*   **取り込み方式**：性能要件に応じて選択してください。大量データには、SDK、CLI、ドライバー、REST APIの`append`などを介してAppendプロトコルを使用します。

### メモリ消費の考慮事項 {#memory-consumption-considerations}

タグテーブルのメモリ使用量には、以下の要因が影響します。

*   **取り込みバッファー**：`TAG_DATA_PART_SIZE`（既定値16MB）に比例します。内部で複数のバッファーを使用します。
*   **パーティション数**：`TAG_PARTITION_COUNT`（既定値4）です。各パーティションが独自のバッファーとインデックス構造を保持します。
*   **インデックス領域**：各パーティションのデータ量やカーディナリティに基づいて動的に割り当てます。`TAG_DATA_PART_SIZE`と平均行サイズに関係します。

**テーブルごとのメモリ概算式：**

`Memory ≈ (TAG_DATA_PART_SIZE * BufferFactor) + ((IndexSizeFactor * TAG_DATA_PART_SIZE / AvgRowSize) * IndexOverheadFactor) * TAG_PARTITION_COUNT`

*（内部係数や動的割り当てのため厳密な計算は複雑ですが、この式は主な要因を表します）。*

既定の設定（`TAG_PARTITION_COUNT=4`、`TAG_DATA_PART_SIZE=16MB`）では、負荷によって主にインデックスとバッファー用に、概算で**最大4GB程度**（パーティションごとに約1GB）のメモリを動的に使用する場合があります。この値は負荷に依存する概算であり、必要RAM容量や使用量の保証上限ではありません。

**メモリ使用量の管理：**

*   **`TAG_PARTITION_COUNT`を減らす**：テーブル作成時にパーティション数を1や2にすると、並列度と関連メモリを減らせます。この属性は`ALTER TABLE`で動的に変更できません。リソースの少ない環境に適しますが、並行処理のピーク性能に影響する場合があります。
*   **`TAG_DATA_PART_SIZE`を調整する**：サーバー設定でこの値を小さくすると（例：4MBまたは8MB、最小1MB）、内部バッファーとインデックスセグメントが小さくなり、メモリ負荷を抑えられます。反映にはサーバーの再起動が必要です。

## 基本構成と取り込みの例 {#기본-구성-예}

以下は、タグごとにfactoryとequipmentを持つ`vibration`テーブルの例です。

```sql
CREATE TAG TABLE vibration (
    name  VARCHAR(80) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE SUMMARIZED
)
METADATA (
    factory   VARCHAR(32),
    equipment VARCHAR(64)
)
TAG_PARTITION_COUNT = 2,
TAG_STAT_ENABLE     = 1;
```

### メタデータ列の追加と登録 {#metadata-add-example}

タグごとの属性は、メタテーブル`_vibration_meta`に保存します。
構造の変更には`ALTER TABLE`を使用します。メタデータの`DROP COLUMN`には対応していません。

```sql
ALTER TABLE _vibration_meta ADD COLUMN (location VARCHAR(32));
INSERT INTO vibration METADATA (name, factory, equipment)
VALUES ('sensor-A', 'factory-1', 'machine-1');
```

### データの取り込み {#데이터-적재}

#### importツール {#import-도구}

CSVのフィールドはテーブルの列順に合わせます。次の例では、時刻を秒単位の
Unixエポック時刻として指定します。

```bash
machbase-neo shell import --input data.csv --timeformat s vibration
machbase-neo shell import --format json --timeformat s --input data.json vibration
```

#### REST APIの使用 {#rest-api-사용}

日時文字列を使用する場合は、`timeformat`を明示します。JSONペイロードは、
HTTP書き込みAPIの`data.columns`と`data.rows`で指定します。

```http
POST /db/write/vibration?timeformat=DEFAULT
Content-Type: application/json

{
  "data": {
    "columns": ["name", "time", "value"],
    "rows": [
      ["sensor-A", "2024-03-01 10:00:00", 12.3],
      ["sensor-B", "2024-03-01 10:00:00", 15.7]
    ]
  }
}
```

### ロールアップと統計 {#rollup-및-통계}

- `WITH ROLLUP`を指定すると、秒・分・時間単位の自動集計テーブルが作成され、時間区間ごとの分析を高速化できます。
- `TAG_STAT_ENABLE=1`の場合、`v$<table>_stat`ビューでタグごとの件数、最小・最大値、最新時刻などを確認できます。

### ビューの構成例 {#뷰-구성-예시}

```sql
CREATE VIEW vibration_view AS
SELECT m.name,
       m.factory,
       m.equipment,
       d.time,
       d.value
FROM vibration d
JOIN _vibration_meta m ON d.name = m.name;
```

### 運用のヒント {#운영-팁}

- **重複データの防止**：`TAG_DUPLICATE_CHECK_DURATION`を設定すると、指定期間内の同じ`(name, time)`のデータを自動的に除外します。
- **保存期間の管理**：保持ポリシー（Retention Policy）を追加すると、指定期間を過ぎたデータを自動削除できます。
- **パーティション数の選択**：高性能サーバーでは大きい`TAG_PARTITION_COUNT`、エッジ機器では小さい値をテーブル作成時に選択して、リソース使用量を調整します。

タグテーブルは、簡単なスキーマで大量の時系列データを取り込み、分析するために設計されています。
ロールアップ、統計、保持ポリシーを組み合わせて、時系列データプラットフォームを構成できます。

## まとめ {#summary}

Machbaseタグテーブルは、センサーの時系列データを効率的に管理するための専用データベースオブジェクトです。主な特徴は以下のとおりです。

*   **最適化された構造**：センサー測定に適した縦持ちモデル（識別子、時刻、値）を使用します。
*   **メタデータとデータの分離**：属性と生の時系列測定値を分離し、柔軟なメタデータ管理と効率的なデータ保存を実現します。
*   **メタデータ管理**：一意のタグ`name`（主キー）で関連付け、検索・追加・変更・削除に対応します。削除には先にデータを削除する必要があります。
*   **データ操作**：高速なappendに最適化されています。`name`や`time`で絞り込む検索は効率的です。データ更新は非対応で、削除は主に時間範囲またはタグ単位です。
*   **拡張性**：メタデータ領域とデータ領域に列を追加して、詳しい属性や測定情報を保存できます。
*   **性能**：内部パーティションと専用インデックスにより、高スループットの取り込みと高速な時刻検索を実現します。

タグテーブルは、Machbaseで拡張性の高い時系列アプリケーションを構築するための、堅牢で高性能な基盤を提供します。
