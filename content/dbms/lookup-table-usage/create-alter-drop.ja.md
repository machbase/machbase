---
type: docs
title: '9.3 作成、変更、削除'
weight: 30
toc: true
---

LOOKUPテーブルの作成、変更、削除方法を説明します。

<a id="original-85-creating-lookup-tables"></a>

## LOOKUPテーブルの作成と管理

参照テーブルの作成方法は次のとおりです。LOOKUPテーブルには必ず`PRIMARY KEY`を指定します。

<a id="create-lookup-table"></a>

## LOOKUPテーブルの作成

```sql
CREATE LOOKUP TABLE ch9_ddl (id INTEGER PRIMARY KEY, name VARCHAR(20));
```

運用で使用するマスターデータには、意味の明確な列名を定義します。

```sql
CREATE LOOKUP TABLE ch9_ddl_equip (
    equip_id   LONG PRIMARY KEY,
    equip_name VARCHAR(128),
    location   VARCHAR(64),
    status     VARCHAR(16),
    updated_at DATETIME
);
```

`PRIMARY KEY`は行を一意に識別し、UPDATE、DELETE、JOINの基準になります。
複数列の組み合わせが業務キーの場合は、結合した文字列を別のキー列にするか、SEQUENCEによる代理キーを使用します。

```sql
CREATE LOOKUP TABLE ch9_ddl_price (
    price_key  VARCHAR(64) PRIMARY KEY,
    product_id VARCHAR(32),
    region     VARCHAR(16),
    price      DOUBLE
);
```

<a id="create-lookup-auto-increment"></a>

## AUTO_INCREMENT PRIMARY KEY

サーバーが数値PRIMARY KEYを生成する場合は、単一の`LONG`または`INT64`列に`AUTO_INCREMENT`を指定します。

```sql
CREATE LOOKUP TABLE ch9_ddl_registry (
    equip_id   LONG PRIMARY KEY AUTO_INCREMENT,
    equip_name VARCHAR(128),
    location   VARCHAR(64)
);

INSERT INTO ch9_ddl_registry(equip_name, location)
VALUES ('compressor-01', 'SEOUL-A');
```

PK列を省略するかNULLを指定すると、サーバーが値を生成します。
単一の`INSERT ... VALUES`では、`0..INT64_MAX`範囲のPK値を直接指定することもできます。
指定値が現在の次の自動値以上なら、次の自動値は`指定値 + 1`に進み、小さい値を指定しても戻りません。
データと次の自動値は、正常な再起動後も保持されます。

AUTO_INCREMENTを使用するLOOKUPテーブルでは、`INSERT ... SELECT`と`ON DUPLICATE KEY UPDATE`は使用できません。
SDKでINSERT結果のIDを取得する方法は、[ROWIDとINSERT結果ID](/dbms/reference/sql/rowid/)を参照してください。

<a id="create-lookup-sequence"></a>

## SEQUENCE列の使用

自動増分番号が必要なら、`LONG PROPERTY(SEQUENCE=1)`列を使用します。
入力時は`NEXTVAL()`関数で次の値を取得します。

```sql
CREATE LOOKUP TABLE ch9_ddl_alarm (
    seq         LONG PROPERTY(SEQUENCE=1) PRIMARY KEY,
    sensor_id   VARCHAR(64),
    alarm_type  VARCHAR(32),
    occurred_at DATETIME,
    message     VARCHAR(256)
);

INSERT INTO ch9_ddl_alarm
VALUES (NEXTVAL(seq), 'TEMP-01', 'HIGH', NOW, '온도 초과');
```

SEQUENCE列の詳細なポリシーは、[SEQUENCE列](/dbms/lookup-table-usage/sequence-column/)で説明します。
`PROPERTY(SEQUENCE)`と`AUTO_INCREMENT`は別の機能であり、同じ列に併用しません。

<a id="alter-lookup-column"></a>

## 列の追加と削除

Standard Editionでは、LOOKUPテーブルに固定長の数値ARRAY列を追加・削除できます。

```sql
ALTER TABLE ch9_ddl_equip
    ADD COLUMN (limits DECIMAL(12,4)[2] DEFAULT [0.0000, NULL]);

ALTER TABLE ch9_ddl_equip
    DROP COLUMN (limits);
```

DEFAULTがなければ、既存行の新しいARRAY列は列全体がNULLになります。
DEFAULTを指定すると、既存行にもその値を適用します。
ARRAY DEFAULTの要素数は、宣言した要素数と正確に一致する必要があります。
ARRAY列はPRIMARY KEYやインデックスキーには使用できません。

サポート型と制約は、[数値ARRAY型](/dbms/reference/sql/types/array/)を参照してください。

<a id="alter-lookup-index"></a>

## インデックスの追加

頻繁に検索する列やJOIN条件に使用する列には、インデックスを追加します。

```sql
CREATE INDEX ch9_ddl_loc_idx ON ch9_ddl_equip(location);
CREATE INDEX ch9_ddl_status_idx   ON ch9_ddl_equip(status);
```

PRIMARY KEY列には標準のインデックスが作成されるため、同じ列に別のインデックスを重複作成しません。
インデックスが多いと入力と更新のコストが増えるため、検索条件が明確な列だけに追加します。

<a id="delete-lookup-data"></a>

## データ削除とテーブル削除

行を削除するには`DELETE`文を使用します。単一行の削除には、PK条件を使用する方法が最も明確です。

```sql
DELETE FROM ch9_ddl_equip
WHERE equip_id = 1001;
```

一括削除では一般条件式を使用できます。
本番データでは、先に同じ条件で対象件数を確認してください。

```sql
SELECT COUNT(*)
FROM ch9_ddl_equip
WHERE status = 'RETIRED';

DELETE FROM ch9_ddl_equip
WHERE status = 'RETIRED';
```

テーブル自体を削除するには、`DROP TABLE`を使用します。

```sql
DROP TABLE ch9_ddl_alarm;
DROP TABLE ch9_ddl_registry;
DROP TABLE ch9_ddl_price;
DROP TABLE ch9_ddl_equip;
DROP TABLE ch9_ddl;
```

`DROP TABLE`はテーブル定義とデータを両方削除します。
必要に応じて、削除前にバックアップまたはエクスポートを行ってください。

<a id="create-lookup-limitations"></a>

## 注意事項

- LOOKUPテーブルには`PRIMARY KEY`が必須です。
- `PRIMARY KEY`列は1つだけ指定します。
- `PRIMARY KEY`値を変更する場合は、既存行を削除してから新しいキーで挿入します。
- マスターデータが大きくなり、検索・更新パターンが複雑になったら、TRANSACTIONテーブルを検討します。
