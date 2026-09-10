---
type: docs
title: '5.8 制約、エラー、トラブルシューティング'
weight: 80
toc: true
aliases:
  - /dbms/troubleshooting/update-delete/
---


このページのUPDATE実習はStandard Editionを前提とします。まず次のテーブルを作成し、
正常なSQLと意図的に失敗するSQLを区別して実行します。失敗例を正常なスクリプトにまとめて
入れないでください。同名の既存オブジェクトは削除しません。

```sql
CREATE TAG TABLE ch5_error_time (
    name VARCHAR(64) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE,
    status INTEGER
) METADATA (location VARCHAR(64));
INSERT INTO ch5_error_time METADATA VALUES ('sensor-01', 'zone-1');
INSERT INTO ch5_error_time METADATA VALUES ('sensor-02', 'zone-2');
INSERT INTO ch5_error_time VALUES
    ('sensor-01', TO_DATE('2026-07-01 12:00:00', 'YYYY-MM-DD HH24:MI:SS'), 10.0, 0);
INSERT INTO ch5_error_time VALUES
    ('sensor-02', TO_DATE('2026-07-01 12:00:00', 'YYYY-MM-DD HH24:MI:SS'), 20.0, 0);
CREATE TAG TABLE ch5_error_distance (
    name VARCHAR(64) PRIMARY KEY,
    distance DOUBLE BASEDISTANCE,
    value DOUBLE SUMMARIZED
);
```

<a id="rejected-condition-tag-data-update-where"></a>

## TAG data UPDATEのWHERE条件エラー

WHERE句にはタグの選択条件とBASETIME条件の両方が必要です。
条件が曖昧な場合や許可されていない形式の場合、UPDATEは拒否されます。

{{< callout type="warning" >}}
**必須条件**

`WHERE name ...`形式のタグ選択条件と`time ...`形式のBASETIME条件をともに指定します。
条件なしの全件UPDATE、タグ条件だけのUPDATE、時間条件だけのUPDATEは許可されません。
{{< /callout >}}

### 症状

次のようなUPDATEがエラーとして拒否されます。

```sql
-- 時間条件なし
UPDATE ch5_error_time SET value = 99.9
WHERE name = 'sensor-01';

-- タグ選択条件なし
UPDATE ch5_error_time SET value = 99.9
WHERE time >= TO_DATE('2026-07-01', 'YYYY-MM-DD');

-- OR条件を使用
UPDATE ch5_error_time SET value = 99.9
WHERE name = 'sensor-01'
   OR name = 'sensor-02';
```

### 原因

対象タグと時間範囲を明確に制限できない条件は拒否されます。

| 条件の形式 | サポート |
|-----------|:--------:|
| `name = 'sensor-01' AND time >= ...` | O |
| `name IN ('sensor-01', 'sensor-02') AND time BETWEEN ...` | O |
| `name LIKE 'sensor-%' AND time < ...` | O |
| `value > 10`のみ | X |
| `name = 'sensor-01'`のみ | X |
| `time >= ...`のみ | X |
| `OR`、サブクエリ、集計条件 | X |

### 解決方法

タグ選択条件と時間条件をともに明示します。

```sql
UPDATE ch5_error_time
   SET value = 99.9
 WHERE name = 'sensor-01'
   AND time = TO_DATE('2026-07-01 12:00:00', 'YYYY-MM-DD HH24:MI:SS');

UPDATE ch5_error_time
   SET status = 1
 WHERE name IN ('sensor-01', 'sensor-02')
   AND time >= TO_DATE('2026-07-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
   AND time <  TO_DATE('2026-07-02 00:00:00', 'YYYY-MM-DD HH24:MI:SS');
```

### NAMEまたはTIMEのバインドが`ERR-02190`で拒否される場合

Machbase 8.7.0以降のStandard Editionでは、次のようにNAMEとBASETIMEの条件値に
バインドパラメーターを使用できます。

```sql
UPDATE ch5_error_time
   SET value = ?
 WHERE name = ?
   AND time = ?;
```

タグ選択条件とBASETIME条件の両方があるにもかかわらず、この文が
`ERR-02190: Invalid UPDATE/DELETE condition. Specify it as (primary key column) = (value)`で
拒否される場合は、サーバーバージョンを確認します。旧バージョンのサーバーはTAG data UPDATEの
NAME/TIMEバインドをサポートしていません。サーバーを8.7.0以降にアップグレードし、名前付きマーカーを
使用する場合は該当する名前付きAPIをサポートする8.7.0 SDKも使用します。

`?`の例はSDKで準備・バインドするSQLであり、machsqlで値を指定せずそのまま実行する文ではありません。
同じプリペアドステートメントを再利用する際は、SET、NAME、TIMEの値をすべて再バインドします。
マーカーの詳細な規則は
[TAG data UPDATEのバインド](/dbms/reference/sql/syntax/dml-syntax/tag-data-update-syntax/#tag-data-update-predicate-bind)を
参照してください。

大量のUPDATEの前には、同じWHERE条件で`SELECT COUNT(*)`を実行し、変更対象の行数を確認します。

<a id="column-error-tag-data-update-set"></a>

## TAG data UPDATEのSET対象列エラー

SET句は実際のデータ列だけを対象とします。PRIMARY KEY、BASETIME、メタデータ列を
SETの対象に指定するとエラーになります。

{{< callout type="warning" >}}
**SETの対象**

`value`とユーザーデータ列はUPDATEできます。`name`、`time`、METADATAブロックの列は
TAG data UPDATEのSET対象ではありません。
{{< /callout >}}

### 症状

```sql
-- エラー: PRIMARY KEY列(name)の更新を試行
UPDATE ch5_error_time
   SET name = 'new-sensor'
 WHERE name = 'old-sensor'
   AND time >= TO_DATE('2026-07-01', 'YYYY-MM-DD');

-- エラー: BASETIME列(time)の更新を試行
UPDATE ch5_error_time
   SET time = NOW
 WHERE name = 'sensor-01'
   AND time >= TO_DATE('2026-07-01', 'YYYY-MM-DD');

-- エラー: メタデータ列をdata UPDATEで変更
UPDATE ch5_error_time
   SET location = 'zone-2'
 WHERE name = 'sensor-01'
   AND time >= TO_DATE('2026-07-01', 'YYYY-MM-DD');
```

### 列の種類別のUPDATE可否

| 列の種類 | 説明 | data UPDATE |
|-----------|------|:-----------:|
| PRIMARY KEY (`name`) | TAGを識別する一意キー | X |
| BASETIME (`time`) | 時系列データのタイムスタンプ | X |
| データ列（`value`、補助列） | 実際の行の値 | O |
| `SUMMARIZED`データ列 | 統計対象のデータ列 | O |
| メタデータ列 | METADATAブロックのタグ属性 | X |

### 解決方法

データ値は通常のUPDATEで変更します。

```sql
UPDATE ch5_error_time
   SET value = 99.9,
       status = 1
 WHERE name = 'sensor-01'
   AND time = TO_DATE('2026-07-01 12:00:00', 'YYYY-MM-DD HH24:MI:SS');
```

メタデータには別の構文を使用します。

```sql
UPDATE ch5_error_time METADATA
   SET location = 'zone-2'
 WHERE name = 'sensor-01';
```

タグ名や時間軸を変更する必要がある場合は、新しい`name`/`time`値でデータを挿入してから、
運用ポリシーに従って既存データを削除します。

<a id="tag-stat-distance-schema-error"></a>

## BASE DISTANCE TAG STATの列エラー

Machbase 8.7.0はBASE DISTANCE TAGの`V$<TABLE>_STAT`の軸列を距離の名前と数値型で
提供します。アップグレード前のSQLが`MIN_TIME`、`MAX_TIME`、`RECENT_ROW_TIME`などを検索すると、
列が見つからないエラーになる場合があります。

### 症状

- アップグレード後、BASE DISTANCE統計ビューの従来の`*_TIME`列を検索できません。
- 旧バージョンのサーバーでは、距離値が`DATETIME`として解釈され、意味のない日付に見える場合があります。
- Cluster EditionでStandardと同じ位置ベースの結果マッピングを使用すると、先頭の`HOSTNAME`に
  より後続列の対応がずれる場合があります。

### 診断

対象テーブルの軸と実際の統計ビュースキーマをともに確認します。

```sql
DESC ch5_error_distance;
DESC V$CH5_ERROR_DISTANCE_STAT;
```

BASE DISTANCEテーブルの場合、`MIN_DISTANCE`、`MAX_DISTANCE`、`MIN_VALUE_DISTANCE`、
`MAX_VALUE_DISTANCE`、`RECENT_ROW_DISTANCE`が元の距離軸の型で表示される必要があります。
Cluster Editionでは`HOSTNAME VARCHAR(64)`が先頭列に追加されます。

### 解決方法

1. SQLの従来の`*_TIME`名を、対応する`*_DISTANCE`名に変更します。
2. SDKの結果マッピングを`DATETIME`から元の`DOUBLE`、`LONG`、`ULONG`型に変更します。
3. Clusterの結果は列名で読み取るか、`HOSTNAME`を含めた位置番号を再確認します。
4. BASE TIME TAGのクエリは従来の`*_TIME DATETIME`マッピングを維持します。

全変換表とCluster集計の注意事項は
[タグ別統計ビュー](../query-analysis/#tag-stat-axis-schema)を参照してください。

<a id="limitations-tag"></a>

## 制約と注意事項

<a id="지원하지-않는-기능"></a>

### 機能のサポート範囲

| 機能 | 状態 |
|------|------|
| 実際の時系列データのUPDATE | Standard Editionでサポート（タグ/BASETIME条件が必要） |
| メタデータのUPDATE | サポート（`UPDATE ... METADATA`） |
| DELETE | サポート（`BEFORE`、タグ/軸条件、または全削除） |
| 複数のPRIMARY KEY | 非サポート（単一列のみ） |
| BASETIMEとBASEDISTANCEの同時使用 | 非サポート |
| TAG DATAの通常列のALTER ADD/DROP | 非サポート |
| TAG METADATA列のALTER ADD/DROP | サポート（Standard Edition） |

### タグ数の制限

- 単一のTAGテーブルに作成できるタグ数はシステム設定によって制限されます。
- タグ数が増えるとタグインデックスとメタデータのメモリ使用量も増えるため、本番規模のデータで
  検索・入力性能を測定します。
- タグ名がレコードごとに一意になる設計は避けてください（アンチパターン：[センサーごとのテーブル作成](/dbms/data-modeling-table-design/table-types-patterns-type-anti/#per-sensor-create)を参照）。

<a id="시간-역삽입-제한"></a>

### 遅延到着データ

- BASETIME列には任意の過去時刻を挿入できます。
- 遅延到着データが多いワークロードでは、実際の入力レートと検索性能を別途測定します。

### Cluster Editionのサポート

TAGテーブルはCluster Editionでサポートされています。

ただしTAG data UPDATEはStandard Edition専用で、Cluster Editionではサポートされません。

### まとめ

```
TAGテーブル = センサー名 (PK) + 時間/距離軸 + 計測値
- INSERT/APPEND: O
- UPDATE: 実際のDATAはStandard Editionのタグ/BASETIME条件、METADATAは別のSQL
- DELETE: O (BEFOREまたはタグ/軸条件)
- METADATA: O (別途属性を保存、UPDATE可能)
```

---

**次に読む内容**

- [TRANSACTIONテーブルの設計](/dbms/rdb-table-usage/)

## 実習の後片付け

正常な変更結果をSELECTで確認し、今回の実習テーブルのみ削除します。

```sql
SELECT name, time, value, status FROM ch5_error_time ORDER BY name, time;
DROP TABLE ch5_error_time;
DROP TABLE ch5_error_distance;
```
