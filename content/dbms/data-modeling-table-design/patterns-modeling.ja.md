---
type: docs
title: '4.5 モデリングパターン'
weight: 50
toc: true
---
運用環境でよく使うデータモデリングパターンを説明します。

各節の SQL は別々のモデルを示します。必要な節を選び、同名テーブルがないことを確認してから
専用の演習環境で実行します。スキーマ作成だけでは収集・集計・キャッシュ更新は自動実行されません。
入力アプリケーションやスケジューラーの処理と失敗対応も設計します。

- **[時間軸モデリング](/dbms/data-modeling-table-design/patterns-modeling/#time-axis-modeling)**
- **[距離軸モデリング](/dbms/data-modeling-table-design/patterns-modeling/#distance-axis-modeling)**
- **[状態・キャッシュ](/dbms/data-modeling-table-design/patterns-modeling/#state-cache-status-modeling)**
- **[イベント・ログ](/dbms/data-modeling-table-design/patterns-modeling/#event-log-modeling-logs)**
- **[参照・マスターデータ](/dbms/data-modeling-table-design/patterns-modeling/#reference-master-modeling)**
- **[永続・一時データの組み合わせ](/dbms/data-modeling-table-design/patterns-modeling/#persistent-temporary)**
- **[INSERT・UPDATE](/dbms/data-modeling-table-design/patterns-modeling/#insert-update)**
- **[JOIN・メタデータ設計](/dbms/data-modeling-table-design/patterns-modeling/#join-metadata-design)**
- **[複数タイプの組み合わせ](/dbms/data-modeling-table-design/patterns-modeling/#table-types-patterns-combined-type)**


<a id="time-axis-modeling"></a>

## 時間軸モデリング

時間を基準軸とするパターンで、センサー計測、エネルギー監視、環境データなどに適しています。

1行は1台のメーターの1回の観測です。`time` は受信時刻ではなく計測時刻とし、`kwh` が累積値か
区間使用量かを収集仕様に記録します。以下は電圧・電流も同じ観測に含む前提です。計測周期や
時刻が異なる場合は、同じ行へ無理に合わせず、別の時系列にするか欠測処理を定めます。

### 基本パターン: TAG テーブル

```sql
CREATE TAG TABLE power_meter (
    meter_id  VARCHAR(32) PRIMARY KEY,
    time      DATETIME    BASETIME,
    kwh       DOUBLE,
    voltage   DOUBLE,
    current   DOUBLE
) METADATA (
    location  VARCHAR(64),
    phase     SHORT,
    rating_kw DOUBLE
);
```

### 時間範囲の集計

```sql
-- 1時間ごとの平均・最大計測値（直近24時間）
SELECT meter_id,
       DATE_TRUNC('hour', time, 1) AS hour,
       AVG(kwh) AS avg_kwh,
       MAX(kwh) AS peak_kwh
FROM power_meter
WHERE time >= NOW - 86400000000000
GROUP BY meter_id, hour
ORDER BY meter_id, hour;
```

`kwh` が累積電力量なら、上の平均はメーター指示値の平均であり、時間当たりの消費量ではありません。
区間消費量は開始・終了値の差に、初期化・交換・上限超過の処理規則を適用して求めます。
電力（kW）と電力量（kWh）も区別して列名と単位を決めます。

### 複数解像度での保存

高解像度の元データと低解像度の集計データを、別テーブルに保存します。

```sql
-- 元データ（秒単位）
CREATE TAG TABLE power_raw (
    meter_id VARCHAR(32) PRIMARY KEY,
    time     DATETIME    BASETIME,
    kwh      DOUBLE
);

-- 1分集計（VOLATILE または別 TAG にキャッシュ）
CREATE VOLATILE TABLE power_1min (
    key_id   VARCHAR(80) PRIMARY KEY,
    meter_id VARCHAR(32),
    ts       DATETIME,
    avg_kwh  DOUBLE,
    max_kwh  DOUBLE
);
```

この DDL は保存領域を作るだけです。アプリケーションが `power_1min` の `key_id` にメーターと区間を
一意に識別する値を設定し、集計値を入力します。VOLATILE の結果は再起動で消えるため、長期集計の
保存先にはしません。元データ削除後も必要な統計は、永続 TAG または対応 ROLLUP に保持し、
それぞれの保持ポリシーを確認します。

### タイムゾーン処理

DATETIME は時点を表し、文字列の入出力は接続のタイムゾーンに影響されます。韓国時間で表示するには
クライアントの設定を合わせます。保存時刻に9時間を加えると、同じ時点を別タイムゾーンで表示するのではなく、
値自体を9時間後へ変えるため、表示変換と区別してください。

```sql
-- クライアントのタイムゾーンを確認し、元の時刻を取得
SELECT meter_id,
       time,
       kwh
FROM power_meter
WHERE meter_id = 'MTR-001'
  AND time >= '2024-01-01 00:00:00';
```

入力のタイムゾーンと接続設定が異なる場合は、入力前に基準を統一します。JDBC の `TIMEZONE` 例は
[JDBC 接続](/dbms/development-tools-integration/jdbc/)を参照してください。

<a id="distance-axis-modeling"></a>

## 距離軸モデリング

距離・位置を基準軸とするパターンで、パイプライン検査、道路センサー、レーザースキャンなどに適しています。

距離軸は時間軸の別表示ではなく、時間軸専用の ROLLUP・Retention をそのまま適用できません。
同じ管を繰り返し検査する場合、`pipe_id` だけで検査回を混在させないよう、検査 ID やテーブル分割基準を
定めます。以下は1本の管の1回の検査を前提とし、距離は m、厚さは mm です。

### 基本パターン

```sql
CREATE TAG TABLE pipeline_thickness (
    pipe_id   VARCHAR(32) PRIMARY KEY,
    distance  DOUBLE      BASEDISTANCE,    -- 単位: メートル
    thickness DOUBLE,
    temp      DOUBLE
);
```

### 範囲データの検索

```sql
-- 管 ID ごとの0～50mを検索
SELECT pipe_id, distance, thickness
FROM pipeline_thickness
WHERE pipe_id = 'PIPE-A'
  AND distance BETWEEN 0.0 AND 50.0
ORDER BY distance;

-- しきい値未満の箇所を検索
SELECT pipe_id, distance, thickness
FROM pipeline_thickness
WHERE pipe_id = 'PIPE-A'
  AND thickness < 8.0   -- 厚さ8mm未満の箇所
ORDER BY distance;
```

### 距離に基づく集計

```sql
-- 10m区間ごとの平均厚さ
SELECT pipe_id,
       FLOOR(distance / 10.0) * 10 AS segment_start,
       AVG(thickness) AS avg_thickness,
       MIN(thickness) AS min_thickness
FROM pipeline_thickness
WHERE pipe_id = 'PIPE-A'
GROUP BY pipe_id, FLOOR(distance / 10.0) * 10
ORDER BY segment_start;
```

### 時間と距離の複合モデル

検査時刻と位置を併せて管理する場合は、時間軸 TAG に距離列を追加します。

```sql
-- 時間軸と位置情報を保存
CREATE TAG TABLE inspection_data (
    inspector  VARCHAR(64) PRIMARY KEY,
    time       DATETIME    BASETIME,
    distance   DOUBLE,      -- 位置列（軸ではない）
    thickness  DOUBLE,
    defect     SHORT
);

-- 特定の日付・距離範囲を検索
SELECT inspector, time, distance, thickness
FROM inspection_data
WHERE inspector = 'INSPECTOR-01'
  AND time BETWEEN '2024-01-01' AND '2024-01-02'
  AND distance BETWEEN 100.0 AND 200.0
ORDER BY time;
```

<a id="state-cache-status-modeling"></a>

## 状態・キャッシュのモデリング

デバイスやセンサーの現在状態をリアルタイムに検索するキャッシュパターンです。

### 最新状態キャッシュ

VOLATILE に各デバイスの現在状態をキャッシュします。

```sql
-- 状態キャッシュ（VOLATILE）
CREATE VOLATILE TABLE device_status (
    device_id  VARCHAR(64) PRIMARY KEY,
    status     VARCHAR(16),
    value      DOUBLE,
    updated_at DATETIME
);

-- 状態履歴（TAG または LOG）
CREATE TAG TABLE device_status_history (
    name   VARCHAR(64) PRIMARY KEY,
    time   DATETIME    BASETIME,
    value  DOUBLE,
    status VARCHAR(16)
);
```

### 状態更新の流れ

以下は履歴とキャッシュを個別に更新します。2つの入力は1トランザクションではなく、別々に評価する
`NOW` も同時刻とは限りません。実際の収集では1回決めた計測時刻を両経路へ渡します。
遅れて届いた過去値が最新キャッシュを上書きしないよう、順序判定と同時更新をアプリケーションで制御します。

```sql
-- 新計測値を受信したとき:
-- 1. TAG に履歴を保存
INSERT INTO device_status_history VALUES ('DEV-01', NOW, 78.5, 'WARNING');

-- 2. VOLATILE キャッシュを更新（ON DUPLICATE KEY UPDATE）
INSERT INTO device_status VALUES ('DEV-01', 'WARNING', 78.5, NOW)
ON DUPLICATE KEY UPDATE SET status = 'WARNING', value = 78.5, updated_at = NOW;
```

### ダッシュボードのクエリ

```sql
-- 現在アラーム状態のすべてのデバイス
SELECT device_id, status, value, updated_at
FROM device_status
WHERE status IN ('ALARM', 'WARNING')
ORDER BY updated_at DESC;

-- 特定デバイスの最新状態
SELECT device_id, status, value, updated_at
FROM device_status
WHERE device_id = 'DEV-01';
```

### 状態定義の参照

状態コードの意味を LOOKUP で管理します。

```sql
CREATE LOOKUP TABLE status_definition (
    code    VARCHAR(16) PRIMARY KEY,
    label   VARCHAR(64),
    color   VARCHAR(16),
    severity SHORT
);

INSERT INTO status_definition VALUES ('NORMAL', '正常', 'green', 0);
INSERT INTO status_definition VALUES ('WARNING', '警告', 'yellow', 1);
INSERT INTO status_definition VALUES ('ALARM', 'アラーム', 'red', 2);

-- JOIN クエリ
SELECT d.device_id, s.label, s.color, d.value
FROM device_status d
JOIN status_definition s ON d.status = s.code
ORDER BY s.severity DESC;
```

<a id="event-log-modeling-logs"></a>

## イベント・ログのモデリング

システムイベント、アラーム、監査ログを LOG テーブルでモデル化します。

### 階層的なイベントモデル

```sql
-- アラームイベントの LOG テーブル
CREATE LOG TABLE alarm_event (
    severity    SHORT,          -- 1=INFO, 2=WARN, 3=ERROR, 4=CRITICAL
    category    VARCHAR(32),    -- カテゴリ
    source      VARCHAR(64),    -- 発生元
    message     VARCHAR(512),
    src_ip      IPV4            -- 発生元 IP（ある場合）
);

-- システム監査用 LOG テーブル
CREATE LOG TABLE audit_log (
    user_id    VARCHAR(64),
    action     VARCHAR(32),    -- INSERT, UPDATE, DELETE, LOGIN など
    target     VARCHAR(128),   -- 対象テーブル/リソース
    detail     TEXT,           -- 詳細（全文検索対象）
    result     VARCHAR(8)      -- SUCCESS, FAILURE
);

CREATE INDEX idx_audit_detail ON audit_log(detail) INDEX_TYPE KEYWORD;
```

### アラームの集計

```sql
-- 直近1時間の重大度別アラーム数
SELECT severity, COUNT(*) AS cnt
FROM alarm_event
WHERE _arrival_time >= NOW - 3600000000000
GROUP BY severity
ORDER BY severity DESC;

-- 発生元別アラーム状況（直近24時間）
SELECT source, COUNT(*) AS total,
       SUM(CASE WHEN severity = 4 THEN 1 ELSE 0 END) AS critical_cnt
FROM alarm_event
WHERE _arrival_time >= NOW - 86400000000000
GROUP BY source
ORDER BY total DESC;
```

### ログレベルのフィルタリング

```sql
-- ERROR 以上を検索（直近10分）
SELECT _arrival_time, source, message
FROM alarm_event
WHERE severity >= 3
  AND _arrival_time >= NOW - 600000000000
ORDER BY _arrival_time DESC
LIMIT 100;
```

### 全文検索

```sql
-- 指定キーワードを含む監査ログを検索
SELECT _arrival_time, user_id, action, target
FROM audit_log
WHERE detail SEARCH 'password'
  AND _arrival_time >= NOW - 86400000000000;
```

<a id="reference-master-modeling"></a>

## 参照・マスターデータのモデリング

コード表、設備マスター、ユーザー情報などの参照データを LOOKUP でモデル化します。

履歴に識別子だけを保存すると、名前や場所の重複保存を減らせます。ただし現在のマスターの場所を
変えると、過去履歴との結合結果も新しい場所になります。発生時に所属したラインが重要なら、有効期間を
持つ変更履歴を設計するか、元の行に当時の属性を保存します。以下の階層の参照関係は外部キーで自動検証
されないため、存在しない工場・ラインコードを入力しないようアプリケーションで確認します。

### 階層的なコード体系

```sql
-- 大分類コード
CREATE LOOKUP TABLE category_main (
    code  VARCHAR(8)  PRIMARY KEY,
    label VARCHAR(64)
);

-- 中分類コード（大分類を参照）
CREATE LOOKUP TABLE category_sub (
    code      VARCHAR(16) PRIMARY KEY,
    main_code VARCHAR(8),
    label     VARCHAR(64)
);

CREATE INDEX idx_sub_main ON category_sub(main_code);
```

### 設備階層マスター

```sql
-- 工場マスター
CREATE LOOKUP TABLE factory (
    factory_id VARCHAR(16) PRIMARY KEY,
    name       VARCHAR(64),
    location   VARCHAR(128)
);

-- ラインマスター（工場を参照）
CREATE LOOKUP TABLE production_line (
    line_id    VARCHAR(16) PRIMARY KEY,
    factory_id VARCHAR(16),
    name       VARCHAR(64)
);

-- 設備マスター（ラインを参照）
CREATE LOOKUP TABLE equipment (
    equip_id   VARCHAR(32) PRIMARY KEY,
    line_id    VARCHAR(16),
    equip_name VARCHAR(128),
    equip_type VARCHAR(32),
    install_dt DATETIME
);

CREATE INDEX idx_equip_line ON equipment(line_id);
CREATE INDEX idx_equip_type ON equipment(equip_type);
```

### マスターの結合クエリ

計測テーブルには設備識別子を、工場・ライン・設備名などの属性は LOOKUP に1回だけ保存します。
クエリでは先に時間範囲を絞り、設備識別子で LOOKUP と結合します。構文と実行計画の確認は
[JOIN・サブクエリ](/dbms/tag-table-usage/query-analysis/)を参照してください。

<a id="persistent-temporary"></a>

## 永続・一時データの組み合わせ

永続テーブル（TAG、LOG、TRANSACTION、LOOKUP）に元データを、VOLATILE にクエリ用キャッシュを
保存します。両経路を1トランザクションと考えず、キャッシュ遅延と失敗後の再構築も設計します。

### 元データと集計キャッシュ

元データは永続テーブル、集計結果は VOLATILE に保存します。

```sql
-- 元データ（TAG、永続）
CREATE TAG TABLE sensor_data (
    name   VARCHAR(64) PRIMARY KEY,
    time   DATETIME    BASETIME,
    value  DOUBLE
);

-- 集計キャッシュ（VOLATILE、一時）
CREATE VOLATILE TABLE sensor_recent_avg (
    key_id    VARCHAR(64) PRIMARY KEY,
    sensor_id VARCHAR(64),
    base_ts   DATETIME,
    avg_val   DOUBLE,
    max_val   DOUBLE,
    cnt       LONG
);
```

### キャッシュ更新

キャッシュの1行は、1センサーの直近2時間の統計です。`base_ts` は集計窓の境界ではなく、含まれる
最新の計測時刻です。同じ範囲定義で計算し、同一時点の結果を比べる場合は実行ごとに基準時刻を1回
決めます。以下は未来の計測値を除外します。比較時には各 SQL の `NOW` を同じ固定基準時刻に置き換え、
下限と上限を計算します。

```sql
-- 定期集計更新（1時間ごと）
DELETE FROM sensor_recent_avg;

INSERT INTO sensor_recent_avg
SELECT name AS key_id,
       name,
       MAX(time) AS base_ts,
       AVG(value),
       MAX(value),
       COUNT(*)
FROM sensor_data
WHERE time >= NOW - 3600000000000 * 2  -- 直近2時間を再計算
  AND time <= NOW
GROUP BY name;
```

`INSERT ... SELECT` に `ON DUPLICATE KEY UPDATE` を付けないでください。再構築時は既存キャッシュを
削除してから再ロードします。

削除と再ロードの間は、他のクエリに空または一部だけのキャッシュが見えることがあります。
更新中の表示、失敗時の再試行、元データへのフォールバックをアプリケーションで定めます。
常に整合した完全な結果が必要なら、対応する切り替え・トランザクションモデルを検討します。

### ダッシュボードクエリの最適化

```sql
-- 保存キャッシュを検索（元データへの切り替えはアプリケーション側）
SELECT sensor_id, base_ts, avg_val, max_val
FROM sensor_recent_avg
WHERE base_ts >= NOW - 3600000000000 * 2
  AND base_ts <= NOW
ORDER BY sensor_id, base_ts;
```

この条件は、最新計測時刻が直近2時間に含まれるキャッシュ行を表示します。保存済み平均を
クエリ時点で再計算するものではないため、集計の鮮度は更新周期で管理します。

### 障害復旧

再起動すると VOLATILE のデータは消失しますが、テーブル定義は残ります。元の TAG から
同じ直近2時間の統計を再計算します。以下の CREATE は、初回構築などでテーブルが存在しない場合だけ作成します。
再計算対象が元データの保持期間内に残っている必要があります。

```sql
-- キャッシュ再構築（サーバー再起動後）
CREATE VOLATILE TABLE IF NOT EXISTS sensor_recent_avg (
    key_id    VARCHAR(64) PRIMARY KEY,
    sensor_id VARCHAR(64),
    base_ts   DATETIME,
    avg_val   DOUBLE,
    max_val   DOUBLE,
    cnt       LONG
);

INSERT INTO sensor_recent_avg
SELECT name,
       name, MAX(time), AVG(value), MAX(value), COUNT(*)
FROM sensor_data
WHERE time >= NOW - 3600000000000 * 2  -- 通常更新と同じ直近2時間
  AND time <= NOW
GROUP BY name;
```

復旧後、センサー別の件数・平均・最新時刻を、同じ基準時刻の元データ集計と比較します。`cnt` は
NULL 計測値も含む行数です。平均に使ったサンプル数が必要なら `COUNT(value)` を別列に保存します。

<a id="insert-update"></a>

## INSERT・UPDATE パターン

モデルでは変更可能なデータを決めますが、ここでは DML 対応表を再定義しません。タイプ別の変更条件は
[データ変更ポリシー](../alter-data-mutation-policy/)、INSERT・Append・ファイル入力の選択は
[データの入力とエクスポート](/dbms/development-tools-integration/data-input-load-export/)を参照してください。

<a id="join-metadata-design"></a>

## JOIN・メタデータ設計

複数タイプを組み合わせるときは次の原則を適用します。

まず結合関係を定義します。センサーコードごとにマスターが正確に1行か、工場間でコードが重複するかを
確認します。元の1行が複数の参照行に一致すると、結果行と SUM などが重複する場合があります。
名前だけでなく識別範囲と型を合わせてください。

1. 元の行数だけでなく、フィルター後の件数と実行計画で結合順序を検討します。
2. JOIN 列の型を合わせ、対応インデックスが使われるか確認します。
3. WHERE に時間範囲と業務条件を明示して結合行数を減らします。
4. TAG 属性を併せて読む目的なら、LOOKUP より METADATA が適切か検討します。

再現可能な結合例は [TAG のクエリと分析](/dbms/tag-table-usage/query-analysis/)と
[LOOKUP のクエリと分析](/dbms/lookup-table-usage/query-analysis/)を参照してください。

<a id="table-types-patterns-combined-type"></a>

## 複数タイプの組み合わせ

運用システムで複数のテーブルタイプを組み合わせる代表的な設計です。

### 製造設備の監視システム

```
┌─────────────────────────────────────────────────────────┐
│                    設備監視システム                     │
├──────────────────┬──────────────────┬───────────────────┤
│ TAG              │ LOG              │ LOOKUP            │
│ sensor_data      │ alarm_event      │ equipment_master  │
│ 計測履歴         │ アラームイベント │ 設備参照データ    │
├──────────────────┴──────────────────┴───────────────────┤
│ VOLATILE: sensor_latest（最新値キャッシュ）              │
└─────────────────────────────────────────────────────────┘
```

### 物流・注文管理システム（Standard Edition）

```
┌─────────────────────────────────────────────────────────┐
│                    物流管理システム                     │
├──────────────────┬──────────────────┬───────────────────┤
│ TRANSACTION      │ LOG              │ LOOKUP            │
│ orders           │ delivery_log     │ product_master    │
│ 注文管理         │ 配送イベント     │ 製品参照データ    │
│ UPDATE/DELETE    │                  │                   │
├──────────────────┴──────────────────┴───────────────────┤
│ VOLATILE: order_status_cache（現在状態キャッシュ）        │
└─────────────────────────────────────────────────────────┘
```

### パターンのまとめ

| 役割 | 推奨タイプ | 理由 |
|------|---------|------|
| 高頻度の計測履歴 | TAG | Append API の高速バッファ、時系列最適化 |
| イベント・アラームログ | LOG | 追記専用、受信時刻の自動記録 |
| リレーショナル業務（UPDATE/DELETE） | TRANSACTION | SELECT/INSERT/UPDATE/DELETE 対応 |
| 参照・コード情報 | LOOKUP | PK 識別、一般条件 UPDATE/DELETE、永続性 |
| リアルタイム状態キャッシュ | VOLATILE | メモリ速度、UPSERT |

---

次に読む文書:

- [SELECT の GROUP BY と集計](/dbms/reference/sql/syntax/select-syntax/)
- [運用と設定](/dbms/operations-configuration-recovery/)
