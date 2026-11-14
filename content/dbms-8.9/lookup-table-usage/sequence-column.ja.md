---
type: docs
title: '9.11 SEQUENCE列'
weight: 110
toc: true
---

LOOKUPテーブルのSEQUENCE列の設定と活用を説明します。

<a id="design-column-lookup-sequence"></a>

## LOOKUPのSEQUENCE列の定義

SEQUENCE列は、`NEXTVAL`で入力番号を生成するために使用します。
LOOKUPテーブルは[PRIMARY KEYが必須](../primary-key-policy/)のため、
SEQUENCE列自体をPRIMARY KEYにするか、他の列をPRIMARY KEYにするかも決めます。
この番号を、イベント発生時刻の順序と同じものとして解釈しないでください。

## SEQUENCE列が必要な理由

同時刻に発生したアラームや管理履歴を、別々の行として識別する場合に使用できます。
LOOKUPは全行をメモリに保持するため、この例は小規模な管理履歴を対象とします。
長期間蓄積する大量イベントには、LOGテーブルを検討してください。

## SEQUENCE列の宣言

SEQUENCEは`LONG`または`INT64`型の列に指定できます。
PROPERTY句の`SEQUENCE`パラメーターで開始値を設定します。この属性はLOOKUPテーブルだけで使用できます。

```sql
CREATE LOOKUP TABLE ch9_sequence (
    seq       LONG PROPERTY(SEQUENCE=1) PRIMARY KEY,
    sensor_id VARCHAR(40),
    alarm_type VARCHAR(20),
    occurred_at DATETIME,
    message   VARCHAR(200)
);
```

- `SEQUENCE=1`: seq列が1から自動増分します。
- 開始値は1以上4,294,967,295未満の整数だけを指定できます。
- 上の例のようにSEQUENCE列をPRIMARY KEYにすると、番号の一意性も保証されます。

## SEQUENCE値の挿入: NEXTVAL()

サーバーはSEQUENCE列ごとに次に使用する番号をカウンターで保持し、`NEXTVAL()`はその値を取得して挿入します。
毎回テーブルの最大値を再計算することはありません。

```sql
-- NEXTVAL()で自動増分値を入力
INSERT INTO ch9_sequence (seq, sensor_id, alarm_type, occurred_at, message)
VALUES (NEXTVAL(seq), 'TEMP-01', 'HIGH', NOW, '온도 초과');

INSERT INTO ch9_sequence (seq, sensor_id, alarm_type, occurred_at, message)
VALUES (NEXTVAL(seq), 'PRESS-02', 'LOW', NOW, '압력 저하');

-- 検索
SELECT * FROM ch9_sequence ORDER BY seq;
-- seq=1、seq=2の順にソート
```

## 一般列と同様の直接値指定

SEQUENCE列に値を直接入力することもできます。
入力値が現在のカウンターより大きければ、カウンターは`入力値 + 1`に進みます。
現在のカウンターより小さい値を入力しても、カウンターは減少しません。

```sql
-- 値を直接指定（nextvalは不要）
INSERT INTO ch9_sequence (seq, sensor_id, alarm_type, occurred_at, message)
VALUES (100, 'FLOW-03', 'NORMAL', NOW, '정상 복구');

-- 以後のNEXTVAL()呼び出しは101になります
INSERT INTO ch9_sequence (seq, sensor_id, alarm_type, occurred_at, message)
VALUES (NEXTVAL(seq), 'TEMP-01', 'NORMAL', NOW, '온도 정상');
-- seq = 101
```

## 活用パターン

```sql
-- 最新アラームN件を検索
SELECT * FROM ch9_sequence ORDER BY seq DESC LIMIT 10;

-- 特定のseq以降のアラームを検索
SELECT * FROM ch9_sequence WHERE seq > 500 ORDER BY seq;

-- アラーム確認処理（PKによるUPDATE）
UPDATE ch9_sequence SET alarm_type = 'ACKNOWLEDGED'
WHERE seq = 101;
```

実習テーブルは、次のように削除します。

```sql
DROP TABLE ch9_sequence;
```

## 注意事項

- SEQUENCE列は`LONG`、`INT64`型をサポートします。
- 開始値は正数（`SEQUENCE=1`以上）のみ許可され、4,294,967,295未満である必要があります。
- カウンターはサーバーに保存され、増加方向だけに進みます。最大のseq行をDELETEしても番号は再使用されないため、欠番が生じる場合があります。
- SEQUENCE列をPRIMARY KEYにしない場合、`NEXTVAL()`を使わずに重複値を直接入力できます。
  番号の一意性が必要なら、この列をPRIMARY KEYに指定してください。
