---
type: docs
title: '8.13 TRANSACTION INSERT ON DUPLICATE KEY UPDATE'
weight: 130
toc: true
---

「なければ追加し、あれば更新する」操作は単純に見えますが、何を重複と見なすかによって更新される行が変わります。
特にカウンター増加を再送すると、同じイベントが2回反映される場合があります。
キー、更新対象、再試行ポリシーを併せて確認してください。

TRANSACTIONの`INSERT ... ON DUPLICATE KEY UPDATE`は、PRIMARY KEYまたは一般のUNIQUE INDEXの競合時に既存行を更新します。
次の実習は、このページ内で必要なオブジェクトを準備します。
エラー確認SQLは通常の流れと分離し、最後のクリーンアップまで実行してから再実行してください。

## サポートする構文

TRANSACTIONテーブルでは、`INSERT ... VALUES ...`形式のUPSERTをサポートします。

```text
INSERT INTO table_name VALUES (...)
    ON DUPLICATE KEY UPDATE;

INSERT INTO table_name VALUES (...)
    ON DUPLICATE KEY UPDATE SET column_name = expression [, ...];

INSERT INTO table_name(column_name, ...)
VALUES (...)
    ON DUPLICATE KEY UPDATE;

INSERT INTO table_name(column_name, ...)
VALUES (...)
    ON DUPLICATE KEY UPDATE SET column_name = expression [, ...];
```

競合判定キーとして認められる対象は次のとおりです。

- TRANSACTION PRIMARY KEY
- TRANSACTION UNIQUE INDEX
- TRANSACTION複合UNIQUE INDEX

## 基本動作

重複がなければ、通常のINSERTと同様に新しい行を追加します。

```sql
CREATE TRANSACTION TABLE ch8_up_device_state (
    device_id INTEGER PRIMARY KEY,
    status VARCHAR(16),
    alarm_count INTEGER,
    updated_at DATETIME
);

INSERT INTO ch8_up_device_state
VALUES (1, 'NORMAL', 0, TO_DATE('2026-07-10 09:00:00', 'YYYY-MM-DD HH24:MI:SS'))
    ON DUPLICATE KEY UPDATE SET
        status = 'NORMAL',
        updated_at = TO_DATE('2026-07-10 09:00:00', 'YYYY-MM-DD HH24:MI:SS');
```

PRIMARY KEYが重複すると、既存行をUPDATEします。

```sql
INSERT INTO ch8_up_device_state
VALUES (1, 'ALARM', 1, TO_DATE('2026-07-10 09:05:00', 'YYYY-MM-DD HH24:MI:SS'))
    ON DUPLICATE KEY UPDATE SET
        status = 'ALARM',
        alarm_count = alarm_count + 1,
        updated_at = TO_DATE('2026-07-10 09:05:00', 'YYYY-MM-DD HH24:MI:SS');
```

`SET`句ではPRIMARY KEYを変更できません。右辺の式は競合した既存行を基準に評価します。
したがって、`alarm_count = alarm_count + 1`は挿入しようとした値ではなく、既存行のalarm_countに1を加算します。

```sql
SELECT device_id, status, alarm_count, updated_at
FROM ch8_up_device_state
WHERE device_id = 1;
```

想定する結果形式は次のとおりです。

```text
DEVICE_ID  STATUS  ALARM_COUNT  UPDATED_AT
---------  ------  -----------  -----------------------------
1          ALARM   1            2026-07-10 09:05:00 000:000:000
```

`ON DUPLICATE KEY UPDATE`の後の`SET`句は省略できます。

```sql
CREATE TRANSACTION TABLE ch8_up_asset_cache (
    asset_id INTEGER PRIMARY KEY,
    asset_name VARCHAR(80),
    location VARCHAR(80),
    keep_value INTEGER
);

INSERT INTO ch8_up_asset_cache VALUES (1, 'compressor-a', 'plant-1', 100);

INSERT INTO ch8_up_asset_cache(asset_id, asset_name, location)
VALUES (1, 'compressor-a-renamed', 'plant-2')
    ON DUPLICATE KEY UPDATE;
```

`SET`句がない場合は、INSERT対象列のうちPRIMARY KEY以外の列だけを既存行に反映します。
上の例では`asset_name`、`location`が更新され、列リストにない`keep_value`は既存値を保持します。

```sql
SELECT asset_id, asset_name, location, keep_value
FROM ch8_up_asset_cache
ORDER BY asset_id;
```

想定する結果形式は次のとおりです。

```text
ASSET_ID  ASSET_NAME            LOCATION  KEEP_VALUE
--------  --------------------  --------  ----------
1         compressor-a-renamed  plant-2   100
```

PRIMARY KEY列だけのテーブルで、重複行に`SET`なしのUPSERTを実行すると、更新対象列がないため行は変更されません。

## UNIQUE INDEXの重複処理

PRIMARY KEYだけでなく、UNIQUE INDEXの競合でも更新処理が実行されます。

```sql
CREATE TRANSACTION TABLE ch8_up_account_profile (
    id INTEGER PRIMARY KEY,
    email VARCHAR(120),
    display_name VARCHAR(80),
    login_count INTEGER
);

CREATE UNIQUE INDEX ch8_up_uidx_account_profile_email
ON ch8_up_account_profile(email);

INSERT INTO ch8_up_account_profile
VALUES (1, 'ops@example.com', 'ops-user', 1);

INSERT INTO ch8_up_account_profile
VALUES (2, 'ops@example.com', 'ops-renamed', 1)
    ON DUPLICATE KEY UPDATE SET
        display_name = 'ops-renamed',
        login_count = login_count + 1;

SELECT id, email, display_name, login_count
FROM ch8_up_account_profile
ORDER BY id;
```

`email`のUNIQUE INDEXが重複するため、`id = 1`の行がUPDATEされます。
挿入しようとした`id = 2`の行は新規追加されません。

複合UNIQUE INDEXは、キーの組み合わせ全体が同じ場合に重複として処理します。

```sql
CREATE TRANSACTION TABLE ch8_up_daily_device_summary (
    id INTEGER PRIMARY KEY,
    device_id INTEGER,
    summary_day VARCHAR(10),
    event_count INTEGER,
    last_status VARCHAR(16)
);

CREATE UNIQUE INDEX ch8_up_uidx_daily_device_summary
ON ch8_up_daily_device_summary(device_id, summary_day);

INSERT INTO ch8_up_daily_device_summary
VALUES (1, 101, '2026-07-10', 3, 'NORMAL');

INSERT INTO ch8_up_daily_device_summary
VALUES (2, 101, '2026-07-10', 1, 'ALARM')
    ON DUPLICATE KEY UPDATE SET
        event_count = event_count + 1,
        last_status = 'ALARM';

INSERT INTO ch8_up_daily_device_summary
VALUES (3, 101, '2026-07-11', 1, 'NORMAL')
    ON DUPLICATE KEY UPDATE SET
        event_count = event_count + 1;
```

最初のUPSERTは`(device_id, summary_day) = (101, '2026-07-10')`の行をUPDATEします。
2番目のUPSERTは日付が異なるため、新しい行をINSERTします。

UNIQUE KEYにNULLを含む行同士は、重複として処理しません。
次の2つの入力は互いを上書きせず、それぞれ新しい行になります。

```sql
INSERT INTO ch8_up_daily_device_summary VALUES (4, NULL, '2026-07-10', 1, 'NORMAL')
    ON DUPLICATE KEY UPDATE;
INSERT INTO ch8_up_daily_device_summary VALUES (5, NULL, '2026-07-10', 2, 'ALARM')
    ON DUPLICATE KEY UPDATE;
SELECT id, device_id, summary_day, event_count
  FROM ch8_up_daily_device_summary ORDER BY id;
```

結果のidは1・3・4・5、event_countはそれぞれ4・1・1・2です。
必須の業務キーでは、UNIQUE INDEXに加えて構成列のNOT NULLも必要です。

## 活用例

TAGテーブルに時系列の測定値を継続的に蓄積し、TRANSACTIONテーブルに機器別の最新状態だけを維持できます。

```sql
CREATE TRANSACTION TABLE ch8_up_latest_device_status (
    device_name VARCHAR(80) PRIMARY KEY,
    last_value DOUBLE,
    last_state VARCHAR(16),
    event_count LONG,
    updated_at DATETIME
);

INSERT INTO ch8_up_latest_device_status
VALUES ('compressor-a', 72.5, 'NORMAL', 1, TO_DATE('2026-07-10 09:00:00', 'YYYY-MM-DD HH24:MI:SS'))
    ON DUPLICATE KEY UPDATE SET
        last_value = 72.5,
        last_state = 'NORMAL',
        event_count = event_count + 1,
        updated_at = TO_DATE('2026-07-10 09:00:00', 'YYYY-MM-DD HH24:MI:SS');

INSERT INTO ch8_up_latest_device_status
VALUES ('compressor-a', 91.2, 'ALARM', 1, TO_DATE('2026-07-10 09:05:00', 'YYYY-MM-DD HH24:MI:SS'))
    ON DUPLICATE KEY UPDATE SET
        last_value = 91.2,
        last_state = 'ALARM',
        event_count = event_count + 1,
        updated_at = TO_DATE('2026-07-10 09:05:00', 'YYYY-MM-DD HH24:MI:SS');
```

このパターンは、ダッシュボードが最新状態だけを高速に検索する場合に使用できます。

外部システムが同じ業務キーでマスターデータを繰り返し送信する場合は、UNIQUE INDEXを基準にUPSERTできます。

```sql
CREATE TRANSACTION TABLE ch8_up_customer_device (
    id LONG PRIMARY KEY AUTO_INCREMENT,
    external_device_id VARCHAR(64),
    device_name VARCHAR(80),
    owner_name VARCHAR(80),
    enabled INTEGER
);

CREATE UNIQUE INDEX ch8_up_uidx_customer_device_external_id
ON ch8_up_customer_device(external_device_id);

INSERT INTO ch8_up_customer_device(external_device_id, device_name, owner_name, enabled)
VALUES ('ERP-DEV-10001', 'compressor-a', 'line-1', 1)
    ON DUPLICATE KEY UPDATE SET
        device_name = 'compressor-a',
        owner_name = 'line-1',
        enabled = 1;

INSERT INTO ch8_up_customer_device(external_device_id, device_name, owner_name, enabled)
VALUES ('ERP-DEV-10001', 'compressor-a-renamed', 'line-2', 1)
    ON DUPLICATE KEY UPDATE SET
        device_name = 'compressor-a-renamed',
        owner_name = 'line-2',
        enabled = 1;
```

最初のINSERTは新しい行を作成し、2番目のINSERTは`external_device_id`のUNIQUE INDEX競合によって既存行をUPDATEします。
内部の`id`は保持されます。

ソースデータの列値をそのまま最新キャッシュに反映する場合は、`SET`句なしのUPSERTを使用できます。

```sql
CREATE TRANSACTION TABLE ch8_up_tag_alias_cache (
    alias_name VARCHAR(80) PRIMARY KEY,
    tag_name VARCHAR(80),
    unit VARCHAR(16),
    description VARCHAR(160),
    manually_checked INTEGER
);

INSERT INTO ch8_up_tag_alias_cache
VALUES ('compressor-a-temp', 'comp_a.temp', 'celsius', 'main compressor temp', 1);

INSERT INTO ch8_up_tag_alias_cache(alias_name, tag_name, unit, description)
VALUES ('compressor-a-temp', 'comp_a.temperature', 'celsius', 'renamed tag')
    ON DUPLICATE KEY UPDATE;
```

上の文は`tag_name`、`unit`、`description`だけを更新します。
列リストにない`manually_checked`は既存値を保持します。

集計テーブルでキーごとの発生回数を累積できます。

```sql
CREATE TRANSACTION TABLE ch8_up_alarm_counter (
    alarm_code VARCHAR(32) PRIMARY KEY,
    first_seen DATETIME,
    last_seen DATETIME,
    hit_count LONG
);

INSERT INTO ch8_up_alarm_counter
VALUES (
    'OVER_TEMP',
    TO_DATE('2026-07-10 09:00:00', 'YYYY-MM-DD HH24:MI:SS'),
    TO_DATE('2026-07-10 09:00:00', 'YYYY-MM-DD HH24:MI:SS'),
    1
)
ON DUPLICATE KEY UPDATE SET
    last_seen = TO_DATE('2026-07-10 09:00:00', 'YYYY-MM-DD HH24:MI:SS'),
    hit_count = hit_count + 1;

INSERT INTO ch8_up_alarm_counter
VALUES (
    'OVER_TEMP',
    TO_DATE('2026-07-10 09:05:00', 'YYYY-MM-DD HH24:MI:SS'),
    TO_DATE('2026-07-10 09:05:00', 'YYYY-MM-DD HH24:MI:SS'),
    1
)
ON DUPLICATE KEY UPDATE SET
    last_seen = TO_DATE('2026-07-10 09:05:00', 'YYYY-MM-DD HH24:MI:SS'),
    hit_count = hit_count + 1;
```

`hit_count = hit_count + 1`は既存行を基準に計算するため、累積カウンターに使用できます。

JSON列も更新対象列として使用できます。

```sql
CREATE TRANSACTION TABLE ch8_up_device_json_state (
    device_id INTEGER PRIMARY KEY,
    state JSON,
    updated_at DATETIME
);

INSERT INTO ch8_up_device_json_state
VALUES (
    1,
    '{"status":"NORMAL","score":10}',
    TO_DATE('2026-07-10 09:00:00', 'YYYY-MM-DD HH24:MI:SS')
)
ON DUPLICATE KEY UPDATE SET
    state = '{"status":"NORMAL","score":10}',
    updated_at = TO_DATE('2026-07-10 09:00:00', 'YYYY-MM-DD HH24:MI:SS');

INSERT INTO ch8_up_device_json_state
VALUES (
    1,
    '{"status":"ALARM","score":90}',
    TO_DATE('2026-07-10 09:05:00', 'YYYY-MM-DD HH24:MI:SS')
)
ON DUPLICATE KEY UPDATE SET
    state = '{"status":"ALARM","score":90}',
    updated_at = TO_DATE('2026-07-10 09:05:00', 'YYYY-MM-DD HH24:MI:SS');

SELECT JSON_EXTRACT_STRING(state, '$.status') AS status,
       JSON_EXTRACT_INTEGER(state, '$.score') AS score
FROM ch8_up_device_json_state
WHERE device_id = 1;
```

制限: JSONパスのUNIQUE INDEXは、競合判定キー候補から除外されます。
JSONパスのUNIQUE INDEX競合はUPSERTの更新処理に切り替わらず、一意性制約エラーとして処理されます。

## トランザクションと権限

TRANSACTIONのUPSERTは、通常のINSERT/UPDATEと同様にトランザクション内でCOMMITまたはROLLBACKされます。

```sql
CREATE TRANSACTION TABLE ch8_up_tx_device_state (
    id INTEGER PRIMARY KEY,
    status VARCHAR(16),
    count_value INTEGER
);

INSERT INTO ch8_up_tx_device_state VALUES (1, 'NORMAL', 10);

BEGIN;

INSERT INTO ch8_up_tx_device_state VALUES (2, 'NORMAL', 1)
    ON DUPLICATE KEY UPDATE SET count_value = count_value + 1;

INSERT INTO ch8_up_tx_device_state VALUES (1, 'ALARM', 1)
    ON DUPLICATE KEY UPDATE SET
        status = 'ALARM',
        count_value = count_value + 1;

ROLLBACK;

SELECT id, status, count_value
FROM ch8_up_tx_device_state
ORDER BY id;
```

上の例では、挿入処理と更新処理の両方がROLLBACKされます。

通常の制約違反で重複更新文が失敗しても、明示的トランザクション内で先に成功した変更は残る場合があります。
アプリケーションはエラーを確認して後続処理を決めるか、ROLLBACKで業務変更を取り消す必要があります。

TRANSACTIONのUPSERT文には、`INSERT`権限と`UPDATE`権限の両方が必要です。
実行結果が挿入処理であっても、文に更新処理が含まれるため両方の権限を付与する必要があります。

次は権限の形式だけを示す例です。
実際の所有者・テーブル・既存アプリケーションアカウントに合わせ、別の管理作業として適用してください。

```text
GRANT INSERT ON owner.table_name TO app_user;
GRANT UPDATE ON owner.table_name TO app_user;
```

`SELECT`権限は、TRANSACTIONのUPSERT文の実行自体には不要です。
ただし、アプリケーションが結果確認のために`SELECT`を実行する場合は、別途`SELECT`権限が必要です。

<a id="타입과-지원하지-않는-구문"></a>

## サポートする型と制約

`SET`句で更新できる列の型は、通常のTRANSACTION `UPDATE`と同じ公開型のサポート範囲に従います。

| 分類 | 型 |
| --- | --- |
| 整数 | `SHORT`, `INT16`, `USHORT`, `UINT16`, `INT`, `INTEGER`, `INT32`, `UINTEGER`, `UINT32`, `LONG`, `INT64`, `ULONG`, `UINT64` |
| 浮動小数点 | `FLOAT`, `DOUBLE` |
| 固定小数点 | `DECIMAL`, `NUMERIC`, `DEC`, `FIXED`, `NUMBER` |
| 文字列/LOB | `VARCHAR`, `TEXT`, `CLOB`, `BINARY`, `BLOB` |
| その他 | `DATETIME`, `IPV4`, `IPV6`, `JSON` |

上の表は、TRANSACTIONで使用するスカラー型をまとめたものです。
数値ARRAYのサポート範囲は、[データ型リファレンス](/dbms/reference/sql/types/)を参照してください。

競合判定キーとなるキー・インデックスの型は、TRANSACTION PRIMARY KEYとUNIQUE INDEXの型ポリシーに従います。
この機能はキー型のサポート範囲を拡張しません。

次の構文はサポートしていません。

```text
-- 未サポートの構文を示す説明用のブロックです。
-- INSERT SELECTとON DUPLICATE KEY UPDATEの組み合わせは未サポートです。
INSERT INTO ch8_up_device_state(device_id, status, alarm_count, updated_at)
SELECT device_id, status, alarm_count, updated_at
FROM staging_device_state
ON DUPLICATE KEY UPDATE SET status = 'UPDATED';

-- MySQLのVALUES(col)関数は未サポートです。
INSERT INTO ch8_up_device_state VALUES (1, 'ALARM', 1, TO_DATE('2026-07-10 09:00:00', 'YYYY-MM-DD HH24:MI:SS'))
ON DUPLICATE KEY UPDATE SET status = VALUES(status);

-- EXCLUDED別名は未サポートです。
INSERT INTO ch8_up_device_state VALUES (1, 'ALARM', 1, TO_DATE('2026-07-10 09:00:00', 'YYYY-MM-DD HH24:MI:SS'))
ON DUPLICATE KEY UPDATE SET status = EXCLUDED.status;

-- conflict target構文は未サポートです。
INSERT INTO ch8_up_device_state VALUES (1, 'ALARM', 1, TO_DATE('2026-07-10 09:00:00', 'YYYY-MM-DD HH24:MI:SS'))
ON CONFLICT (device_id) DO UPDATE SET status = 'ALARM';
```

対象テーブルの制限は次のとおりです。

- このページは、TRANSACTIONのPRIMARY KEY・UNIQUE競合時の動作だけを説明します。
  同じSQL形式はLOOKUPとVOLATILEのPRIMARY KEY競合にも対応します。
  共通構文の正本は[DMLリファレンス](/dbms/reference/sql/syntax/dml-syntax/#on-duplicate-key-update)です。
- LOGとTAG DATA行ではサポートしていません。TAG METADATAのタグ名競合処理は、
  [DMLリファレンス](/dbms/reference/sql/syntax/dml-syntax/#on-duplicate-key-update)を参照してください。
- TRANSACTIONテーブルでも、PRIMARY KEYまたはUNIQUE INDEXがなければ使用できません。
- JSONパスのUNIQUE INDEXは競合判定キーに使用しません。

## 競合とエラー処理

複数のUNIQUE INDEXが同じ既存行を指す場合、その行を一度だけUPDATEします。
一方、異なる既存行と競合すると、更新すべき行を決定できず文が失敗します。

次は、2つの業務キーがそれぞれ異なる行と競合するサンプルです。

```sql
CREATE TRANSACTION TABLE ch8_up_user_contact (
    id INTEGER PRIMARY KEY,
    email VARCHAR(120),
    phone VARCHAR(40),
    note VARCHAR(80)
);

CREATE UNIQUE INDEX ch8_up_uidx_user_contact_email ON ch8_up_user_contact(email);
CREATE UNIQUE INDEX ch8_up_uidx_user_contact_phone ON ch8_up_user_contact(phone);

INSERT INTO ch8_up_user_contact VALUES (1, 'a@example.com', '010-0000-0001', 'user-a');
INSERT INTO ch8_up_user_contact VALUES (2, 'b@example.com', '010-0000-0002', 'user-b');

```

次のINSERTだけを意図的に失敗させる任意の実習です。

```sql
-- emailはid=1、phoneはid=2と競合します。
-- 異なる行と競合するため、更新処理を選択せず失敗します。
INSERT INTO ch8_up_user_contact VALUES (3, 'a@example.com', '010-0000-0002', 'ambiguous')
ON DUPLICATE KEY UPDATE SET note = 'updated';
```

`SET`の結果が別のUNIQUE制約や`NOT NULL`制約に違反した場合も、文は失敗して既存行が保持されます。

<a id="재전송과-최신-상태의-의미를-확인하세요"></a>

## 再送と最新状態

カウンター増加のUPSERTは自動的な重複排除ではありません。
同じイベントを再実行すると、既存のカウンターが再び増加します。
COMMIT応答を失った場合は、業務キー・イベント処理記録で先に結果を確認してください。

また、「最新状態」は、入力順序とイベント発生順序が一致する場合にのみ単純な上書きで維持できます。
遅れて到着した過去のイベントが最新値を上書きしないよう、元の時刻の比較と収集ポリシーを別途定めてください。
複数テーブルをまとめて変更する処理では、[障害時のトランザクションのコミット範囲](../transaction/)も確認する必要があります。

## 運用上の推奨事項

- 業務キーが明確なら、PRIMARY KEYまたはUNIQUE INDEXを先に定義します。
- カウンターの累積には、`SET count_col = count_col + 1`形式を使用します。
- ソース行の値をそのまま反映するには、`SET`なしのUPSERTを使用できます。この場合、列リストで省略した列は保持されます。
- 複数のUNIQUE INDEXを持つテーブルでは、異なる行と同時に競合する可能性がある入力を事前に整理します。
- MySQL互換SQLを移植する場合は、`VALUES(col)`、`EXCLUDED`、`ON CONFLICT`をMachbaseのサポート構文に変更します。
- JSONパスのUNIQUE INDEXをUPSERTキーにする設計は避けます。必要なら別の通常列にキー値を保存してUNIQUE INDEXを作成します。

<a id="실습-결과-확인과-정리"></a>

## 結果確認とクリーンアップ

通常の実習を終えたら、代表値と件数を再確認します。
次の想定値は、意図的なエラー以外の正常なSQLをそれぞれ一度実行した場合です。

```sql
SELECT id, email, display_name, login_count
  FROM ch8_up_account_profile ORDER BY id;
SELECT device_name, last_state, event_count
  FROM ch8_up_latest_device_status;
SELECT external_device_id, device_name, owner_name
  FROM ch8_up_customer_device;
SELECT alias_name, tag_name, manually_checked FROM ch8_up_tag_alias_cache;
SELECT alarm_code, hit_count FROM ch8_up_alarm_counter;
SELECT id, status, count_value FROM ch8_up_tx_device_state ORDER BY id;
SELECT id, note FROM ch8_up_user_contact ORDER BY id;
```

| サンプル | 確認する結果 |
|---|---|
| account_profile | id=1を保持、display_name=ops-renamed、login_count=2 |
| latest_device_status | ALARM、event_count=2 |
| customer_device | 外部キーの1行、名前compressor-a-renamed、所有line-2 |
| tag_alias_cache | tag_name=comp_a.temperature、manually_checked=1を保持 |
| alarm_counter | OVER_TEMPのhit_count=2 |
| tx_device_state | ROLLBACK後は既存のid=1、NORMAL、count_value=10だけが存在 |
| user_contact | id=1・2のuser-a・user-bをそのまま保持 |

```sql
DROP TABLE ch8_up_user_contact;
DROP TABLE ch8_up_tx_device_state;
DROP TABLE ch8_up_device_json_state;
DROP TABLE ch8_up_alarm_counter;
DROP TABLE ch8_up_tag_alias_cache;
DROP TABLE ch8_up_customer_device;
DROP TABLE ch8_up_latest_device_status;
DROP TABLE ch8_up_daily_device_summary;
DROP TABLE ch8_up_account_profile;
DROP TABLE ch8_up_asset_cache;
DROP TABLE ch8_up_device_state;
```

DROPはこのページの実習オブジェクトだけを対象にします。
キーが複雑な場合ほど、新しい入力値と競合する既存行を並べて比較してください。
更新しようとした行が明確になれば、エラーの原因も特定しやすくなります。
