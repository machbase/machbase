---
title: 'Tag テーブルの作成と削除'
type: docs
weight: 10
toc: true
---

## このガイドで学ぶこと {#what-youll-learn}

Tag テーブルは、軸に沿ったセンサーデータを保存するための基盤です。時間軸と距離軸の Tag テーブルの作成、設定、削除を説明します。

> **バージョン**：距離軸列（`BASE DISTANCE`、`BASEDISTANCE`）は Machbase 8.0.75 以降でサポートされます。

## 軸の規則 {#axis-rules}

Tag テーブルは、同じ `tag_name` の行を 1 つの軸列に沿って保存します。

- 時間軸：`DATETIME BASE TIME` または `DATETIME BASETIME`
- 距離軸：`DOUBLE`、`LONG`、`ULONG` に `BASE DISTANCE` または `BASEDISTANCE` を指定
- `BASE` の後には、必ず `TIME` または `DISTANCE` を指定
- 1 つの Tag テーブルに指定できる軸列は 1 つ
- `SELECT`、`INSERT`、`DELETE` をサポートし、`UPDATE` はサポートしない

## 時間軸の Tag テーブルの作成 {#creating-a-time-axis-tag-table}

一般的な時間軸の Tag テーブルには、次の 3 要素が必要です。
- **タグ名**（PRIMARY KEY）：センサーやデータソースの識別子
- **入力時刻**（BASETIME）：データを記録した時刻
- **センサー値**：実際の測定値

### 時間軸の作成例 {#time-axis-creation-example}

同じテーブル名を使用する作成例は、それぞれ独立した例です。対象名のテーブルが存在しない状態で実行します。

```sql
-- 必須キーワードがないため失敗する
Mach> CREATE TAG TABLE tag (name VARCHAR(20) PRIMARY KEY, time DATETIME, value DOUBLE);
[ERR-02253: Mandatory column definition (PRIMARY KEY / BASE TIME) is missing.]

-- 必須の BASETIME を指定した正しい例
Mach> CREATE TAG TABLE tag (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE);
Executed successfully.

-- 統計情報を取得するために SUMMARIZED を指定する
Mach> CREATE TAG TABLE tag (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE SUMMARIZED);
Executed successfully.

Mach> desc tag;
[ COLUMN ]
----------------------------------------------------------------
NAME      TYPE        LENGTH
----------------------------------------------------------------
NAME      varchar         20
TIME      datetime       31
VALUE     double          17
```

> **ヒント**：SUMMARIZED を指定すると、値列の最小値、最大値、平均値を自動的に追跡でき、分析に役立ちます。

## 距離軸の Tag テーブルの作成 {#creating-a-distance-axis-tag-table}

距離軸の Tag テーブルは、時間ではなく累積距離、走行距離、生産ライン上の位置などを軸にする場合に使用します。

```sql
Mach> CREATE TAG TABLE trip_sensor (
          name        VARCHAR(20) PRIMARY KEY,
          distance_m  DOUBLE BASE DISTANCE,
          value       DOUBLE,
          quality     INTEGER
      );
Executed successfully.

Mach> CREATE TAG TABLE trip_sensor_alias (
          name        VARCHAR(20) PRIMARY KEY,
          distance_m  LONG BASEDISTANCE,
          value       DOUBLE
      ) METADATA (route_id VARCHAR(20), axis_unit VARCHAR(8));
Executed successfully.
```

距離軸列には 8 バイトの型が必要です。

- `DOUBLE`
- `LONG`
- `ULONG`

小数の距離が必要な場合は `DOUBLE`、整数で十分な場合は `LONG` または `ULONG` を使用します。

次の型は、距離軸には使用できません。

- `FLOAT`
- `INTEGER`
- `UINTEGER`
- `SHORT`
- `USHORT`

> **制限**：距離軸の Tag テーブルは `WITH ROLLUP` をサポートしません。詳細は[集計用のロールアップテーブル](../rollup-tables)を参照してください。

## センサーの追加列 {#adding-additional-sensor-columns}

実際のセンサーデータでは、名前、軸、値以外の情報も必要になります。時間軸、距離軸のどちらのテーブルにも、グループ ID や IP アドレスなどの追加列を定義できます。

```sql
Mach> create tag table TAG (name varchar(20) primary key, time datetime basetime, value double, grpid short, myip ipv4);
Executed successfully.

Mach> desc tag;
[ COLUMN ]
----------------------------------------------------------------
NAME             TYPE        LENGTH
----------------------------------------------------------------
NAME             varchar         20
TIME             datetime        31
VALUE            double          17
GRPID            short            6       <=== 追加した列
MYIP             ipv4            15       <=== 追加した列
```

> **注意**：5.6 より前のバージョンでは、追加列に VARCHAR を使用できません。5.6 以降でサポートされます。

## メタデータ列の追加 {#adding-metadata-columns}

メタデータ列は、部屋番号や説明など、タグ名ごとに固有の情報を保存します。測定値の各行に同じ情報を繰り返し保存する必要がありません。

```sql
Mach> create tag table TAG (name varchar(20) primary key, time datetime basetime, value double)
   2  metadata (room_no integer, tag_description varchar(100));
Executed successfully.
```

### メタデータの使用例 {#example-metadata-usage}

|name|room_no|tag_description|
|--|--|--|
|temp_001|1|It reads current temperature as Celsius|
|humid_001|1|It reads current humidity as percentage|

センサーデータとメタデータを一緒に検索します。

```sql
Mach> SELECT name, time, value, tag_description FROM tag LIMIT 1;
name                  time                            value
--------------------------------------------------------------------------------------
tag_description
------------------------------------------------------------------------------------
temp_001              2019-03-01 09:52:17 000:000:000 25.3
It reads current temperature as Celsius
```

## テーブルプロパティの設定 {#configuring-table-properties}

次のプロパティで、メモリと CPU の使用量を制御します。

| プロパティ | 説明 | 既定値 | 範囲 |
|--|--|--|--|
| TAG_PARTITION_COUNT | パーティション数 | 4 | 1-1024 |
| TAG_DATA_PART_SIZE | パーティションごとのデータサイズ | 16MB | 1MB-1GB |
| TAG_STAT_ENABLE | 統計情報の追跡 | 1（有効） | 0-1 |

### プロパティの例 {#property-examples}

```sql
-- 少量のデータには 1 パーティションを使用する
Mach> CREATE TAG TABLE tag (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE)
      TAG_PARTITION_COUNT=1;

-- データパートサイズを指定する
Mach> CREATE TAG TABLE tag (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE)
      TAG_DATA_PART_SIZE=1048576;

-- 複数のプロパティを指定する
Mach> CREATE TAG TABLE tag (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE SUMMARIZED)
      TAG_PARTITION_COUNT=2, TAG_STAT_ENABLE=1;
```

## Tag テーブルの削除 {#dropping-tag-tables}

テーブルを作り直す場合や、ディスク領域を解放する場合は DROP を使用します。

```sql
Mach> DROP TABLE tag;
Dropped successfully.

Mach> DESC tag;
tag does not exist.
```

> **警告**：Tag テーブルを削除すると、関連するすべてのデータとメタデータテーブルが完全に削除されます。元に戻すことはできません。

## 推奨事項 {#best-practices}

1. **SUMMARIZED を使用する**：統計情報が必要な値列に SUMMARIZED を指定します。
2. **パーティションを計画する**：パーティション数を増やすと並列処理能力が向上しますが、メモリ使用量も増えます。
3. **適切な名前を付ける**：有効な識別子を使用できます。名前を TAG にする必要はありません。
4. **メタデータと追加列を使い分ける**：
   - 変更頻度の低いタグ固有の情報はメタデータに保存します。
   - 測定ごとに変化するデータは追加列に保存します。

## 次のステップ {#next-steps}

- [Tag メタデータの管理](../tag-metadata)でタグ名の作成と管理を確認
- [Tag データの挿入](../inserting-data)で入力方法を確認
- [Tag データの検索](../querying-data)で効率的な検索方法を確認
