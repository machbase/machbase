---
type: docs
title: '5.9 活用パターンとシナリオ'
weight: 90
toc: true
---

各例は独立した実習です。テーブルの作成前に同名のオブジェクトがないことを確認します。
タグ名、1回の観測の意味、値の単位、欠損ポリシーを先に決めてからDDLを適用します。

<a id="use-cases-tag"></a>

## 活用例

### IoTセンサーデータ

工場、ビル、インフラに設置された各種センサーのデータを1つのTAGテーブルで管理します。

```sql
CREATE TAG TABLE factory_sensor (
    name        VARCHAR(128) PRIMARY KEY,
    time        DATETIME     BASETIME,
    temperature DOUBLE,
    vibration   DOUBLE,
    current     DOUBLE
);

-- 同じ設備の同じ観測による測定値を1行にまとめます。
INSERT INTO factory_sensor VALUES (
    'F01/LINE-A/MOTOR-01',
    NOW,
    75.3, 0.15, 2.4
);
```

このモデルは、1台の装置の同時刻の観測を複数列に保存します。項目別のタグ
`.../TEMP`、`.../VIBRATION`を使用する場合は、`name, time, value`形式の単一値モデルを
検討します。項目ごとに測定時刻が異なる場合は、NULLと品質状態でその違いを表現してください。

### エネルギー監視

電力、ガス、水道メーターのデータを時間ごとに収集します。

```sql
CREATE TAG TABLE energy_meter (
    meter_id  VARCHAR(64) PRIMARY KEY,
    time      DATETIME    BASETIME,
    kwh       DOUBLE,
    voltage   DOUBLE,
    current   DOUBLE
);
```

`kwh`が累積計量値の場合、AVG(kwh)は指示値の平均であり、区間使用量ではありません。
消費量は区間境界値の差にリセット・交換・欠損の処理規則を適用して計算します。
電力kWと電力量kWhを区別し、メタデータや収集仕様に単位を明記します。

### 車両・移動体の追跡

GPS座標と速度を時系列で記録します。

```sql
CREATE TAG TABLE vehicle_track (
    vehicle_id VARCHAR(32) PRIMARY KEY,
    time       DATETIME    BASETIME,
    lat        DOUBLE,
    lon        DOUBLE,
    speed      DOUBLE,
    heading    DOUBLE
);
```

座標系、緯度・経度、速度の単位を収集仕様に明記します。位置の欠損を数値0で置き換えると、
実際の座標と区別できません。このテーブルの作成によって空間インデックスや経路マッチングが
自動提供されるわけではありません。まず車両・時間区間で検索し、必要な分析を実行します。

### 適していない場合

- レコードごとにタグ名が変わる場合（タグ数の急増）
- タグ・時間範囲を指定せず、全データを頻繁にUPDATEする必要がある場合
- 単純なイベントログ（LOGテーブルを推奨）


## 結果の確認と後片付け

IoTの例では、次の検索で3つの測定値が同じ1行として返ることを確認します。

```sql
SELECT name, time, temperature, vibration, current FROM factory_sensor;
DROP TABLE factory_sensor;
DROP TABLE energy_meter;
DROP TABLE vehicle_track;
```

後片付けは、このページで実際に作成したテーブルだけに適用します。
