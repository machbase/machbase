---
type: docs
title: '9.10 PRIMARY KEYポリシー'
weight: 100
toc: true
---

LOOKUPテーブルのPRIMARY KEY設計原則とポリシーを説明します。
SDKがSELECT結果からPKを判定する方法は、
[PRIMARY KEYメタデータのサポート範囲](/dbms/development-tools-integration/sdk-support-scope/#support-scope-sdk-primary-key-metadata)を参照してください。

<a id="design-primary-key"></a>

## PRIMARY KEYの設計

LOOKUPテーブルには`PRIMARY KEY`が必須です。
PRIMARY KEYは行を一意に識別し、重複入力を制御します。
UPDATEとDELETEの`WHERE`句には一般条件式を使用できますが、PRIMARY KEY列自体はUPDATEできません。

### 基本構文

```text
CREATE LOOKUP TABLE table_name (
    pk_col   type    PRIMARY KEY,
    col2     type,
    ...
);
```

### 単一列のPRIMARY KEY

```sql
CREATE LOOKUP TABLE ch9_pk_country_code (
    code     VARCHAR(4)  PRIMARY KEY,
    name     VARCHAR(64),
    region   VARCHAR(32)
);
```

### 複合キーが必要な場合

```sql
CREATE LOOKUP TABLE ch9_pk_price (
    price_key  VARCHAR(64) PRIMARY KEY,
    product_id VARCHAR(32),
    region     VARCHAR(16),
    price      DOUBLE
);

-- 挿入
INSERT INTO ch9_pk_price VALUES ('PROD-01:KR', 'PROD-01', 'KR', 99.0);
INSERT INTO ch9_pk_price VALUES ('PROD-01:US', 'PROD-01', 'US', 79.0);

-- 組み合わせキーによるUPDATE
UPDATE ch9_pk_price SET price = 89.0
WHERE price_key = 'PROD-01:KR';
```

LOOKUPテーブルにはPRIMARY KEY列を1つだけ指定できます。
複数列の組み合わせが業務キーの場合は、組み合わせた文字列または代理キーを別のPRIMARY KEY列に格納します。

### PRIMARY KEYの型の選択

| 型 | 利点 | 欠点 |
|------|------|------|
| `VARCHAR(n)` | 可読性が高く、意味のあるキー | 文字列の比較コスト |
| `INTEGER` / `LONG` | 比較が高速で保存効率がよい | 意味を持たず、別のマッピングが必要 |

### 注意事項

- PRIMARY KEY値は重複できません。
- PRIMARY KEY値は変更できません（変更時はDELETE + INSERT）。
- PRIMARY KEY列にはインデックスが自動作成されます。
- PRIMARY KEY列は1つだけ指定します。

<a id="policy-lookup-primary-key"></a>

## PRIMARY KEYポリシー

PRIMARY KEY設計で考慮するポリシーと推奨方法を説明します。

### 自然キーと代理キー

#### 自然キー（Natural Key）

業務上の意味を持つ値を、そのままPRIMARY KEYに使用します。

```sql
-- 国コード: 標準化された自然キー
CREATE LOOKUP TABLE ch9_pk_country (
    iso_code VARCHAR(4) PRIMARY KEY,  -- ISO 3166-1 alpha-2
    name     VARCHAR(64)
);
```

**利点**: 意味を理解しやすく、別の検索が不要
**欠点**: キー変更時に参照整合性の問題が発生

#### 代理キー（Surrogate Key）

SEQUENCE列やUUIDなど、業務上の意味を持たない値をPRIMARY KEYに使用します。

```sql
-- 設備マスター: 代理キー
CREATE LOOKUP TABLE ch9_pk_equip (
    equip_id  LONG PROPERTY(SEQUENCE=1) PRIMARY KEY,
    code      VARCHAR(32),          -- 業務キー
    name      VARCHAR(128)
);
CREATE INDEX ch9_pk_equip_idx ON ch9_pk_equip(code);
```

**利点**: 不変で、結合が効率的
**欠点**: コードとIDの変換が必要

### PRIMARY KEY不変の原則

PRIMARY KEY値はUPDATEできません。変更が必要ならDELETE + INSERTを使用します。

```sql
-- 誤ったパターン（PK変更はDELETE + INSERTで実行）
-- UPDATEではPKを変更できません

-- 正しいパターン
DELETE FROM ch9_pk_country WHERE iso_code = 'OLD';
INSERT INTO ch9_pk_country VALUES ('NEW', '새 국가명');
```

LOOKUPテーブルのDMLは個々の文単位で実行します。
`BEGIN`/`COMMIT`でまとめるTRANSACTIONトランザクションに、LOOKUPのDMLを含めることはできません。

したがって、2文の間の検索や挿入失敗に備える必要があります。
既存値を保持し、参照キーの切り替え順序を決めてから変更してください。
変更全体のアトミック性が必要なら、TRANSACTIONテーブルを検討します。

このページの実習テーブルは、次のように削除します。

```sql
DROP INDEX ch9_pk_equip_idx;
DROP TABLE ch9_pk_equip;
DROP TABLE ch9_pk_country;
DROP TABLE ch9_pk_price;
DROP TABLE ch9_pk_country_code;
```
