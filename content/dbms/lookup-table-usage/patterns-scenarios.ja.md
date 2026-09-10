---
type: docs
title: '9.9 活用パターンとシナリオ'
weight: 90
toc: true
aliases:
  - /dbms/lookup-table-usage/reference-master-modeling/
---

LOOKUPテーブルの活用パターンとシナリオを説明します。

<a id="use-cases-lookup"></a>

## 活用例

LOOKUPテーブルは、次のようなデータの保存に適しています。

<a id="lookup-pattern-data-types"></a>

## 適したデータの種類

| 種類 | 例 |
|------|------|
| コードテーブル | 国コード、言語コード、状態コード |
| マスターデータ | 設備一覧、製品分類、部門情報 |
| リアルタイム更新の参照データ | 為替レートテーブル、しきい値設定 |
| タグメタデータの代替 | センサー情報（小規模） |

<a id="lookup-pattern-code-table"></a>

<a id="patterns-reference-design"></a>

## コードテーブル

```sql
CREATE LOOKUP TABLE ch9_pattern_country (
    code   VARCHAR(4)   PRIMARY KEY,
    name   VARCHAR(64),
    region VARCHAR(32)
);

INSERT INTO ch9_pattern_country VALUES ('KR', '대한민국', 'Asia');
INSERT INTO ch9_pattern_country VALUES ('US', '미국', 'America');
UPDATE ch9_pattern_country SET name = 'United States' WHERE code = 'US';

SELECT code, name FROM ch9_pattern_country ORDER BY code;
```

2行が返され、US行のnameだけが`United States`に変わっています。

状態コードやアラームコードも同じ方法で管理し、元のイベントとJOINして使用します。

```sql
CREATE LOOKUP TABLE ch9_pattern_status (
    code  VARCHAR(16) PRIMARY KEY,
    label VARCHAR(64),
    color VARCHAR(16)
);
INSERT INTO ch9_pattern_status VALUES ('RUN',  '가동', 'green');
INSERT INTO ch9_pattern_status VALUES ('STOP', '정지', 'red');

CREATE LOG TABLE ch9_pattern_event (
    event_time DATETIME,
    device_id  VARCHAR(64),
    status     VARCHAR(16)
);
INSERT INTO ch9_pattern_event
VALUES (TO_DATE('2026-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 'DEV-01', 'RUN');
INSERT INTO ch9_pattern_event
VALUES (TO_DATE('2026-01-01 10:05:00', 'YYYY-MM-DD HH24:MI:SS'), 'DEV-01', 'STOP');
EXEC TABLE_FLUSH(ch9_pattern_event);

SELECT e.event_time, e.device_id, c.label
  FROM ch9_pattern_event e
  JOIN ch9_pattern_status c ON e.status = c.code
 ORDER BY e.event_time;
```

2行がコードの代わりに`가동`（稼働）・`정지`（停止）のラベルで返されます。
コードにない状態がイベントに含まれるとINNER JOINでその行が除外されるため、コードテーブルの欠落も点検します。

<a id="lookup-pattern-equipment-master"></a>

## 設備マスター

```sql
CREATE LOOKUP TABLE ch9_pattern_equip (
    equip_id   VARCHAR(32) PRIMARY KEY,
    equip_name VARCHAR(128),
    location   VARCHAR(64),
    dept       VARCHAR(64),
    install_dt DATETIME
);
INSERT INTO ch9_pattern_equip
VALUES ('TEMP-01', 'Boiler', 'Seoul', 'Production',
        TO_DATE('2025-01-01', 'YYYY-MM-DD'));
INSERT INTO ch9_pattern_equip
VALUES ('TEMP-02', 'Chiller', 'Busan', 'Facility',
        TO_DATE('2025-01-01', 'YYYY-MM-DD'));
```

TAGテーブルのセンサーデータとJOINすると、場所や部門などのマスターデータも検索できます。

```sql
CREATE TAG TABLE ch9_pattern_sensor (
    name  VARCHAR(32) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE SUMMARIZED
);
INSERT INTO ch9_pattern_sensor
VALUES ('TEMP-01', TO_DATE('2026-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 90.0);
INSERT INTO ch9_pattern_sensor
VALUES ('TEMP-02', TO_DATE('2026-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 20.0);
EXEC TABLE_FLUSH(ch9_pattern_sensor);

SELECT d.name, m.location, m.dept, d.value
  FROM ch9_pattern_sensor d
  JOIN ch9_pattern_equip m ON d.name = m.equip_id
 WHERE m.dept = 'Production'
 ORDER BY d.name;
```

TEMP-01の1行だけが返されます。部門条件はLOOKUP側の列に適用されるため、
条件を変更すると、読み取るTAGの元データが同じでも結果集合が変わります。

<a id="lookup-pattern-threshold"></a>

## しきい値設定

```sql
CREATE LOOKUP TABLE ch9_pattern_threshold (
    sensor_name VARCHAR(64) PRIMARY KEY,
    low_limit   DOUBLE,
    high_limit  DOUBLE,
    alert_level SHORT
);
INSERT INTO ch9_pattern_threshold VALUES ('TEMP-01', 0.0, 100.0, 1);
INSERT INTO ch9_pattern_threshold VALUES ('TEMP-02', 0.0, 100.0, 1);

-- リアルタイムのしきい値変更
UPDATE ch9_pattern_threshold SET high_limit = 85.0 WHERE sensor_name = 'TEMP-01';
```

しきい値テーブルは、TAGデータと結合してアラーム条件を判定するために使用します。

```sql
SELECT s.name, s.value, t.high_limit
  FROM ch9_pattern_sensor s
  JOIN ch9_pattern_threshold t ON s.name = t.sensor_name
 WHERE s.value > t.high_limit
 ORDER BY s.name;
```

TEMP-01だけが超過と判定されます。値90は変更前の上限100では正常でした。
同じ元データでもしきい値の変更時点によって判定が変わることを、併せて記録してください。

<a id="lookup-pattern-sequence-master"></a>

## SEQUENCEによる履歴番号

小規模な管理履歴や運用イベントに連番が必要なら、SEQUENCE列を使用できます。

```sql
CREATE LOOKUP TABLE ch9_pattern_note (
    seq        LONG PROPERTY(SEQUENCE=1) PRIMARY KEY,
    target_id  VARCHAR(64),
    note       VARCHAR(512),
    created_at DATETIME
);

INSERT INTO ch9_pattern_note
VALUES (NEXTVAL(seq), 'TEMP-01', 'threshold changed', NOW);
INSERT INTO ch9_pattern_note
VALUES (NEXTVAL(seq), 'TEMP-02', 'inspection done', NOW);

SELECT seq, target_id FROM ch9_pattern_note ORDER BY seq;
```

seqは1と2です。大量の元履歴データは、LOOKUPよりLOGテーブルに保存してください。

このページの実習オブジェクトは、次のように削除します。

```sql
DROP TABLE ch9_pattern_note;
DROP TABLE ch9_pattern_threshold;
DROP TABLE ch9_pattern_sensor;
DROP TABLE ch9_pattern_equip;
DROP TABLE ch9_pattern_event;
DROP TABLE ch9_pattern_status;
DROP TABLE ch9_pattern_country;
```

<a id="lookup-pattern-not-suitable"></a>

## 適さない場合

- 明示的トランザクションと一般的なリレーショナルDMLが必要なデータ → TRANSACTIONテーブルを推奨
- UPDATEが不要な追加専用の履歴 → LOGテーブルを推奨
- センサー計測値 → TAGテーブルを推奨
- 再起動後に消えてもよい最新状態キャッシュ → VOLATILEテーブルを推奨
