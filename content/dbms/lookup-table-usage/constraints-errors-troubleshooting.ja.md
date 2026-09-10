---
type: docs
title: '9.8 制約、エラー、トラブルシューティング'
weight: 80
toc: true
---

LOOKUPテーブルの制約、発生し得るエラー、解決方法を説明します。

<a id="limitations-lookup-summary"></a>

## 制約の概要

| 項目 | 制約 | 代表的なエラー |
|---|---|---|
| PRIMARY KEY | 必須。1つだけ指定 | `ERR-02322`, `ERR-02171` |
| PRIMARY KEY列 | `SET`の対象に指定不可 | `ERR-02176` |
| 列の型 | `TEXT`・`CLOB`・`BLOB`・`BINARY`は使用不可 | `ERR-02173` |
| JSON列 | 一般列として使用可能。PRIMARY KEYには使用不可 | — |
| メモリ | VOLATILEと1つの上限を共有 | `ERR-01344` |
| UPDATE | `WHERE`必須。省略時は実行されない | — |

<a id="error-lookup-primary-key"></a>

## PRIMARY KEYのエラー

LOOKUPはPRIMARY KEYなしでは作成できず、2つ以上指定することもできません。
次の2文は、それぞれ失敗します。

```sql
-- 失敗: PRIMARY KEYがありません。（ERR-02322）
CREATE LOOKUP TABLE ch9_err_nopk (code VARCHAR(16), label VARCHAR(64));

-- 失敗: PRIMARY KEYが2つあります。（ERR-02171）
CREATE LOOKUP TABLE ch9_err_twopk (
    code VARCHAR(16) PRIMARY KEY,
    name VARCHAR(32) PRIMARY KEY
);
```

どちらの文もテーブルを作成しないため、削除するオブジェクトはありません。
複合キーが必要なら、区切り文字で組み合わせた単一のキー列を用意し、
[PRIMARY KEYポリシー](../primary-key-policy/)の設計基準に従ってください。

PRIMARY KEY列の値は変更できません。

```sql
CREATE LOOKUP TABLE ch9_err_pk (code VARCHAR(16) PRIMARY KEY, label VARCHAR(64));
INSERT INTO ch9_err_pk VALUES ('KR', '대한민국');

-- 失敗: PRIMARY KEY列はSETの対象外です。（ERR-02176）
UPDATE ch9_err_pk SET code = 'KO' WHERE code = 'KR';
```

キーを変更する場合は、既存行を削除し、新しいキーで再入力します。

<a id="error-lookup-column-type"></a>

## 未サポートの列型

`TEXT`、`CLOB`、`BLOB`、`BINARY`はLOOKUP列に使用できません。
長い文字列は`VARCHAR`で宣言し、原文の保持が必要ならLOGテーブルに分離します。

```sql
-- 失敗: 未サポートの列型です。（ERR-02173）
ALTER TABLE ch9_err_pk ADD COLUMN (memo TEXT);
```

JSONは一般列として使用できます。
使用範囲は[JSON列とクエリ](../json-column-query/)を参照してください。

```sql
DROP TABLE ch9_err_pk;
```

<a id="error-lookup-memory-limit"></a>

## メモリ上限

LOOKUPはディスクに永続保存されますが、クエリの実行経路はメモリです。
サーバー起動時に全行とインデックスをメモリへロードするため、使用量が上限を超えると`ERR-01344`が発生します。

この上限は**VOLATILEテーブルと共有します。**
設定名は`VOLATILE_`で始まりますが、LOOKUPも同じ上限に含まれるため、両タイプを併用する環境では合計で判断する必要があります。

```sql
SELECT NAME, VALUE FROM V$PROPERTY
 WHERE NAME = 'VOLATILE_TABLESPACE_MEMORY_MAX_SIZE';

SELECT * FROM V$STORAGE_DC_VOLATILE_TABLE;
```

上限に近づいたら、保持範囲の縮小や未使用のセカンダリインデックスの削除を行います。
大規模なマスターデータでは、[インデックスとパフォーマンス](../index-performance/)の基準に従って他のテーブルタイプを検討してください。

<a id="too-many-lookup-predicate-update-delete-row"></a>

## 複数行の変更範囲

一般述語のUPDATE/DELETEは、複数行に適用される場合があります。
実行前に同じ述語で対象数を確認し、[一般述語のUPDATE/DELETE](../predicate-update-delete/)の仕様に従ってください。

<a id="error-lookup-json-path-primary-key"></a>

## LOOKUPのJSON PRIMARY KEYエラー

JSON列は一般列として使用できますが、PRIMARY KEYには宣言できません。
識別子を別のスカラー列に格納し、[JSON列とクエリ](../json-column-query/)の型・パス規則に従ってください。

<a id="limitations-lookup"></a>

## 制約と注意事項

- PRIMARY KEYのポリシーは、[PRIMARY KEYポリシー](../primary-key-policy/)を参照してください。
- メモリ規模とインデックスのコストは、[インデックスとパフォーマンス](../index-performance/)で測定します。
- 時系列の元データにはTAG、再起動後に消えてもよいキャッシュにはVOLATILEを選択します。
- Appendの使用条件は、[SDK Append対応表](/dbms/development-tools-integration/sdk-support-scope/#append-table-type-matrix)に従います。
