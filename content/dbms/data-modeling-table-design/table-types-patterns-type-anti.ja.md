---
type: docs
title: '4.4 アンチパターン'
weight: 40
toc: true
---
アンチパターンとは、特定のタイプを使うこと自体ではなく、データの意味や要件に合わない使い方です。
各例の前提が業務に当てはまるか確認し、代替案を選びます。同じスキーマでも、現在状態には適し、
履歴の蓄積には適さない場合があります。

- **[LOOKUP に無制限の履歴を蓄積](/dbms/data-modeling-table-design/table-types-patterns-type-anti/#high-frequency-lookup)**
- **[センサー別にテーブルを作成](/dbms/data-modeling-table-design/table-types-patterns-type-anti/#per-sensor-create)**
- **[不適切なタイプ選択](/dbms/data-modeling-table-design/table-types-patterns-type-anti/#table-types-selection-type-wrong)**
- **[VOLATILE を永続保存に使用](/dbms/data-modeling-table-design/table-types-patterns-type-anti/#storage-persistent-volatile)**
- **[時系列に TRANSACTION を誤用](/dbms/data-modeling-table-design/table-types-patterns-type-anti/#time-series-storage-misuse-rdb)**


<a id="high-frequency-lookup"></a>

<a id="고빈도-lookup-조회"></a>

## LOOKUP に無制限の履歴を蓄積

### 問題

問題は検索頻度ではなく、増え続ける計測履歴を LOOKUP に保存する設計です。LOOKUP は全行と
インデックスをメモリに保持するため、長期履歴が増えるほどメモリ負荷も増えます。
小さな参照データをキーで繰り返し検索する用途には適しています。

### アンチパターンの例

```sql
-- 不適切: センサー計測を LOOKUP に保存
CREATE LOOKUP TABLE sensor_data_wrong (
    sensor_id  VARCHAR(64) PRIMARY KEY,
    value      DOUBLE,
    ts         DATETIME
);

-- sensor_id が PK のため、センサーごとに現在の1行しか保存できない
-- 履歴を追加すると同じ PK と競合する
INSERT INTO sensor_data_wrong VALUES ('TEMP-01', 25.3, NOW);
INSERT INTO sensor_data_wrong VALUES ('TEMP-01', 25.5, NOW);  -- PK 重複エラー
```

### 適切なパターン

タグ別の計測履歴の収集・クエリが中心なら TAG を検討します。LOOKUP でも計測ごとに別キーを
付けられますが、全履歴がメモリに常駐するコストは残ります。最新値キャッシュは、性能上必要で
元データから復旧できる場合に VOLATILE で追加します。TAG の最新値クエリで要件を満たすなら
別キャッシュは不要です。

```sql
-- 適切: 履歴は TAG
CREATE TAG TABLE sensor_data (
    name   VARCHAR(64) PRIMARY KEY,
    time   DATETIME    BASETIME,
    value  DOUBLE
);

-- 最新値キャッシュは VOLATILE
CREATE VOLATILE TABLE sensor_latest (
    sensor_id VARCHAR(64) PRIMARY KEY,
    value     DOUBLE,
    updated_at DATETIME
);
```

### 結果

| | アンチパターン（LOOKUP） | 適切な設計（TAG） |
|-|-----------------|-----------------|
| 同じセンサーキーで履歴を蓄積 | X（このキーは行を識別） | O（タグ名の下に複数計測行） |
| 継続入力の経路 | 行識別子中心 | 時系列 Append API を利用可能 |
| 時間範囲クエリ | 一般条件検索 | タグ・時間軸の検索 |

<a id="per-sensor-create"></a>

## センサー別にテーブルを作成

### 問題

センサー（タグ）ごとにテーブルを作ると、センサー数に応じて DDL、権限、クエリ対象が増え、
運用コストが高くなります。

### アンチパターンの例

```sql
-- 不適切: センサーごとにテーブルを作成
CREATE TAG TABLE sensor_temp_01 (
    name VARCHAR(32) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE
);
CREATE TAG TABLE sensor_temp_02 (
    name VARCHAR(32) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE
);
CREATE TAG TABLE sensor_temp_03 (
    name VARCHAR(32) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE
);
-- ... 10,000センサーなら10,000テーブル
```

### 問題点

| 問題 | 説明 |
|------|------|
| 管理の複雑化 | テーブル数だけ DDL を管理 |
| クエリの複雑化 | センサー間集計に複数テーブルの結合が必要 |
| メタデータの増加 | システムカタログの負荷 |
| 新センサー追加 | 毎回 DDL が必要 |

### 適切なパターン

センサー名を PRIMARY KEY とする1つの TAG テーブルに、すべてのセンサーデータを保存します。

これは同じ列構造・権限・保持ポリシーを共有するセンサー群に適用します。単位、スキーマ、
アクセス権限、保持期間を個別管理するなら、テーブルを分けるのが適切な場合もあります。
センサー数そのものを分割基準にしないことが重要です。

```sql
-- 適切: すべての温度センサーを1テーブルに
CREATE TAG TABLE temperature_sensor (
    name   VARCHAR(128) PRIMARY KEY,
    time   DATETIME     BASETIME,
    value  DOUBLE
);

-- すべてのセンサーデータを同じテーブルに入力
INSERT INTO temperature_sensor VALUES ('TEMP-01', NOW, 23.5);
INSERT INTO temperature_sensor VALUES ('TEMP-02', NOW, 24.1);
INSERT INTO temperature_sensor VALUES ('TEMP-10000', NOW, 22.9);
```

### 利点

- 新センサー追加に DDL が不要。新しいタグ名で INSERT するだけ。
- センサー間の集計が容易。
- 運用管理対象を削減。

<a id="table-types-selection-type-wrong"></a>

## 不適切なタイプ選択

データの特性に合わないタイプ選択の代表例です。

### アンチパターン1: イベントログを TAG に保存

```sql
-- 不適切: イベントログを TAG に保存
CREATE TAG TABLE error_log_wrong (
    name   VARCHAR(256) PRIMARY KEY,  -- イベント内容がタグ名になる
    time   DATETIME     BASETIME,
    level  SHORT
);
-- 問題: イベントごとに一意な名前を付けるとタグ数が急増
```

**適切な設計**: LOG テーブルを使用します。

```sql
CREATE LOG TABLE error_log (
    level   SHORT,
    msg     VARCHAR(512),
    src     VARCHAR(128)
);
```

### アンチパターン2: センサー値を LOG に保存

LOG にセンサー値を保存すること自体は誤りではありません。問題は、タグ別の計測時刻集計が必要なのに、
実際の計測時刻を省いて受信時刻だけを残すことです。複数項目の設備イベント検索が中心なら LOG が適する場合もあります。

```sql
-- 計測時刻が必要な要件には不十分なスキーマ
CREATE LOG TABLE sensor_wrong (
    sensor_id VARCHAR(64),
    value     DOUBLE
    -- 計測時刻がなく、サーバー受信時刻だけを自動保存
);
```

**適切な設計**: TAG テーブルを使用します。

```sql
CREATE TAG TABLE sensor_measurements (
    name  VARCHAR(64) PRIMARY KEY,
    time  DATETIME    BASETIME,
    value DOUBLE
);
```

### アンチパターン3: 大量の履歴を LOOKUP に保存

```sql
-- 不適切: リレーショナルトランザクションが必要な注文履歴を LOOKUP に保存
CREATE LOOKUP TABLE order_history_wrong (
    order_id LONG PRIMARY KEY,
    customer VARCHAR(64)
    -- 全行・インデックスのメモリと明示的トランザクション要件を確認
);
```

**適切な設計**: TRANSACTION テーブルを使用します。

```sql
CREATE TRANSACTION TABLE order_history (
    order_id  LONG,
    customer  VARCHAR(64),
    item_id   INTEGER,
    amount    DOUBLE,
    status    VARCHAR(16)
);
-- UPDATE/DELETE/SELECT をすべてサポート
UPDATE order_history SET status = 'SHIPPED' WHERE order_id = 1001;
```

### アンチパターン4: 時系列を TRANSACTION に保存

TRANSACTION も時間列と Append API を使用できますが、TAG 専用の時間軸ストレージや ROLLUP はありません。
リレーショナルな変更より計測履歴の収集・集計が中心なら TAG を検討します。詳細は
[時系列に TRANSACTION を誤用](/dbms/data-modeling-table-design/table-types-patterns-type-anti/#time-series-storage-misuse-rdb)を参照してください。

<a id="storage-persistent-volatile"></a>

## VOLATILE を永続保存に使用

### 問題

永続的に保持する必要があるデータを VOLATILE に保存するパターンです。

### アンチパターンの例

```sql
-- 不適切: 重要な設定を VOLATILE に保存
CREATE VOLATILE TABLE critical_config (
    key_name VARCHAR(64) PRIMARY KEY,
    value    VARCHAR(256)
);

INSERT INTO critical_config VALUES ('license_key', 'XXXX-XXXX-XXXX');
INSERT INTO critical_config VALUES ('max_connections', '1000');
-- 再起動ですべての設定が消失!
```

### 問題点

- サーバー停止・再起動でデータが消失します。テーブル定義は保持されます。
- プロセスが終了する障害でもメモリ内データを復旧できないため、唯一の元データを
  VOLATILE に保存するとデータ損失につながります。

### 適切なパターン

永続的に必要なデータは LOOKUP または TRANSACTION に保存します。

```sql
-- 適切: 設定は LOOKUP
CREATE LOOKUP TABLE app_config (
    key_name VARCHAR(64) PRIMARY KEY,
    value    VARCHAR(256)
);

INSERT INTO app_config VALUES ('max_connections', '1000');
-- 再起動後もデータを保持
```

### VOLATILE の適切な用途

再起動後に再生成または破棄できるデータを保存します。クエリキャッシュだけでなく、寿命が明確な
作業状態も含められます。必ず保持する業務結果をメモリだけに保存しないでください。

| 適切 | 不適切 |
|------|--------|
| センサー最新値キャッシュ | 元のトランザクションデータ |
| リアルタイム集計結果 | 重要な設定値 |
| セッションの一時状態 | 監査ログ |
| ダッシュボードキャッシュ | ユーザー情報 |

<a id="time-series-storage-misuse-rdb"></a>

## 時系列に TRANSACTION を誤用

### 問題

センサー・IoT 計測のような継続的な時系列を TRANSACTION に保存するパターンです。リレーショナルな
更新が不要なら、TAG のタグ・時間軸と ROLLUP を利用できず、必要なクエリ・運用に合わない場合があります。
一方、計測登録と他の業務変更を1トランザクションにまとめるなら TRANSACTION を選ぶ理由があります。

### アンチパターンの例

```sql
-- 不適切: センサー時系列を TRANSACTION に保存
CREATE TRANSACTION TABLE sensor_timeseries (
    sensor_id VARCHAR(64),
    ts        DATETIME,
    value     DOUBLE,
    unit      VARCHAR(16)
);
```

### 問題点

| 問題 | 説明 |
|------|------|
| 入力の意味が不一致 | リレーショナルトランザクション不要の値にもリレーショナル書き込みを使用 |
| 時間軸がない | TAG の BASETIME 検索構造を利用できない |
| 集計機能の違い | TAG 専用 ROLLUP を利用できない |

### 適切なパターン

センサー計測は TAG に保存します。

```sql
-- 適切: TAG を使用
CREATE TAG TABLE sensor_history (
    name   VARCHAR(64) PRIMARY KEY,
    time   DATETIME    BASETIME,
    value  DOUBLE,
    unit   VARCHAR(16)
);

-- Append API の高速バッファで大量入力可能
-- 時間単位集計と TAG 専用最適化を利用可能
SELECT name, DATE_TRUNC('hour', time, 1) AS hour, AVG(value), MAX(value)
FROM sensor_history
WHERE time >= NOW - 86400000000000
GROUP BY name, hour;
```

### TRANSACTION が適する場合

TRANSACTION は注文、在庫、設備履歴などリレーショナルな業務データに使います。時間列があっても
UPDATE/DELETE が必要な業務履歴には TRANSACTION、変更せず蓄積する高頻度計測には TAG を選びます。

## 意味の異なる値を同じ統計で集計

スキーマが同じでも単位や行の意味が異なれば単純集計できません。累積電力量（kWh）の平均は
消費電力（kW）ではなく、区間平均の単純平均は全サンプルの平均と異なる場合があります。
NULL を0で埋めると計測失敗が正常な0になります。

型とともに単位、サンプル数、品質規則を記録します。区間統計の再集計には合計と有効件数などを
保持し、元データを削除する前に将来の分析に必要な解像度を確認します。
