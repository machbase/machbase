---
type: docs
title: '8.6 インデックスとパフォーマンス'
weight: 60
toc: true
---

インデックスは検索速度だけでなく、データの一意性も決定する場合があります。
業務キーを保証するインデックスと読み取り量を減らすインデックスを区別し、性能調整中に必要な制約を誤って削除しないようにします。

<a id="index-tuning-rdb"></a>
<a id="index-strategy-rdb-primary-key-unique-normal"></a>

<a id="primary-key-unique-일반-인덱스를-구분합니다"></a>

## インデックスの種類

| 種類 | 用途 | 複合列 | NULL |
|---|---|---|---|
| PRIMARY KEY | 行の識別。テーブルごとに1つ | 未サポート | 不可 |
| UNIQUE INDEX | 業務キーの一意性 | サポート | NULLを含むキー同士は重複ではない |
| 一般インデックス | 条件検索のアクセス経路 | サポート | 一意性検査なし |

TRANSACTIONのインデックスはBTREEと表示されます。
列のPRIMARY KEY、または作成後のCREATE PRIMARY KEY INDEXを使用できます。
LOGのLSM・KEYWORDインデックス構文を、TRANSACTIONにそのまま適用しないでください。

<a id="unique-index-rdb"></a>

<a id="null과-중복을-함께-확인합니다"></a>

## UNIQUE INDEXとNULL

```sql
CREATE TRANSACTION TABLE ch8_index_account (
    id      LONG PRIMARY KEY,
    email   VARCHAR(120),
    tenant  INTEGER NOT NULL,
    login   VARCHAR(64)
);
INSERT INTO ch8_index_account VALUES (1, 'a@example.com', 1, 'alpha');
INSERT INTO ch8_index_account VALUES (2, 'b@example.com', 1, 'beta');
INSERT INTO ch8_index_account VALUES (3, NULL, 2, NULL);
INSERT INTO ch8_index_account VALUES (4, NULL, 2, NULL);

CREATE UNIQUE INDEX ch8_index_email ON ch8_index_account(email);
CREATE UNIQUE INDEX ch8_index_login ON ch8_index_account(tenant, login);

SELECT id FROM ch8_index_account WHERE email IS NULL ORDER BY id;
SHOW INDEX ch8_index_email;
```

行3と4は両方存在し、インデックスも作成されます。
値が必須の業務キーでは、UNIQUEに加えて各列のNOT NULLも必要です。
CREATE TABLE内にUNIQUEを付けず、別のCREATE UNIQUE INDEXを使用してください。

次の2文は、それぞれ一意性違反を確認する任意の実習です。

```sql
-- 意図的に失敗: emailの重複
INSERT INTO ch8_index_account VALUES (5, 'a@example.com', 1, 'gamma');
UPDATE ch8_index_account SET email = 'a@example.com' WHERE id = 2;
```

失敗後も4行と、行2のb@example.comが保持される必要があります。
現在、一般的なUNIQUE違反はERR-01418として報告されます。
エラーメッセージだけでどの業務キーが重複したかを断定せず、インデックスと入力値を併せて確認してください。

<a id="unique-삭제는-제약-제거입니다"></a>

## UNIQUE INDEXの削除

```sql
DROP INDEX ch8_index_email;
INSERT INTO ch8_index_account VALUES (5, 'a@example.com', 1, 'gamma');
SELECT id, email FROM ch8_index_account WHERE email = 'a@example.com' ORDER BY id;
```

これで行1と5が両方保存されます。
重複がある状態でインデックスを再作成すると失敗します。

```sql
-- 意図的に失敗: 既存データに重複があります。
CREATE UNIQUE INDEX ch8_index_email ON ch8_index_account(email);
```

実習で追加した行5を削除してから、再作成します。

```sql
DELETE FROM ch8_index_account WHERE id = 5;
CREATE UNIQUE INDEX ch8_index_email ON ch8_index_account(email);
SELECT COUNT(*) AS remaining_rows FROM ch8_index_account;
```

件数は4です。
運用ではインデックスを削除する前に、性能用か一意性保証用かを確認する必要があります。

<a id="일반복합-인덱스는-실제-조건으로-비교합니다"></a>

## 一般・複合インデックス

```sql
CREATE TRANSACTION TABLE ch8_index_event (
    id      LONG PRIMARY KEY,
    status  VARCHAR(16),
    created DATETIME,
    state   JSON
);
INSERT INTO ch8_index_event VALUES (
    1, 'OPEN', TO_DATE('2026-01-01', 'YYYY-MM-DD'), '{"status":"ALARM","code":500}');
INSERT INTO ch8_index_event VALUES (
    2, 'CLOSED', TO_DATE('2026-01-02', 'YYYY-MM-DD'), '{"status":"NORMAL","code":200}');
INSERT INTO ch8_index_event VALUES (
    3, 'OPEN', TO_DATE('2026-01-03', 'YYYY-MM-DD'), '{"code":500}');

EXPLAIN SELECT id FROM ch8_index_event
 WHERE status = 'OPEN' AND created >= TO_DATE('2026-01-01', 'YYYY-MM-DD');

CREATE INDEX ch8_index_status_time ON ch8_index_event(status, created);

EXPLAIN SELECT id FROM ch8_index_event
 WHERE status = 'OPEN' AND created >= TO_DATE('2026-01-01', 'YYYY-MM-DD');

SELECT id FROM ch8_index_event
 WHERE status = 'OPEN' AND created >= TO_DATE('2026-01-01', 'YYYY-MM-DD')
 ORDER BY id;
```

結果の意味は作成前後で同じである必要があり、最後のクエリは行1と3を返します。
先頭列を条件に合わせますが、すべての複合条件が必ずそのインデックスを使用するとは断定しないでください。
Machbaseの計画選択とサポートされる条件形式をEXPLAINで確認します。
3行の実行時間は性能ベンチマークではありません。

<a id="index-strategy-rdb-json-path"></a>

<a id="json-path도-같은-데이터에서-확인합니다"></a>

## JSONパスインデックス

```sql
CREATE INDEX ch8_index_json_status ON ch8_index_event(state->'$.status');
CREATE INDEX ch8_index_json_code ON ch8_index_event(state->'$.code');

EXPLAIN SELECT id FROM ch8_index_event WHERE state->'$.status' = 'ALARM';
SELECT id FROM ch8_index_event WHERE state->'$.status' = 'ALARM' ORDER BY id;
SELECT id FROM ch8_index_event WHERE state->'$.code' = '500' ORDER BY id;
```

状態検索は行1、code検索は行1と3を返します。
インデックスを作成しても、すべてのJSON関数式がこの経路を使用するわけではありません。
矢印パスと数値抽出関数は、結果型と比較の意味を区別してください。
複雑な条件を頻繁に繰り返す場合は、通常の列に分離する設計も比較できます。

JSONパスのUNIQUE INDEXを作成できる場合でも、TRANSACTION UPSERTの競合選択キーには使用しません。
[UPSERTの制約](../insert-on-duplicate-key-update/)を確認してください。

<a id="읽기와-쓰기-비용을-함께-기록합니다"></a>

## 読み取り・書き込みコスト

インデックス作成前後では、同じデータ量・条件値・同時入力レートを使用してください。
クエリ時間だけでなく、INSERT・UPDATE・DELETEのスループットとインデックス容量も比較します。
LIMITは結果量を減らしますが、返す行を固定するにはORDER BYが必要です。

```sql
DROP TABLE ch8_index_event;
DROP TABLE ch8_index_account;
```

性能のためにUNIQUE INDEXを一般インデックスに変更すると、一意性の保証は失われます。
チューニング前後で結果と制約が同じであることを、先に確認してください。
