---
type: docs
title: 'AUTO_INCREMENT'
weight: 230
toc: true
aliases:
  - /dbms/rdb-table-usage/auto-increment/
---

`AUTO_INCREMENT`は、単一の64ビット整数PRIMARY KEY値をサーバーが自動生成するための列属性です。

<span class="badge-since">Machbase 8.7.0からLOOKUPとVOLATILEでもサポート</span>

## サポート範囲

| 項目 | サポート範囲 |
|---|---|
| Edition | Standard Edition |
| テーブル | TRANSACTION、LOOKUP、VOLATILE |
| 列の型 | `LONG`、`INT64` |
| キー | 列単位の単一`PRIMARY KEY` |

テーブルレベル・複合PRIMARY KEYには使用できません。
LOOKUPの同じ列に`PROPERTY(SEQUENCE)`を併用したり、`NEXTVAL()`を使用したりしないでください。

```sql
CREATE TRANSACTION TABLE device_master (
    id          LONG PRIMARY KEY AUTO_INCREMENT,
    device_name VARCHAR(80),
    site_code   VARCHAR(32)
);

CREATE LOOKUP TABLE lookup_order (
    id   INT64 PRIMARY KEY AUTO_INCREMENT,
    item VARCHAR(100)
);

CREATE VOLATILE TABLE volatile_order (
    id   LONG PRIMARY KEY AUTO_INCREMENT,
    item VARCHAR(100)
);
```

明示的なトランザクションの進行中は、TRANSACTIONテーブルのDDLを実行できません。
先に`COMMIT`または`ROLLBACK`してからテーブルを作成します。

## 自動値の生成

自動生成列を省略するか`NULL`を入力すると、サーバーが値を生成します。

```sql
INSERT INTO device_master(device_name, site_code)
VALUES ('compressor-01', 'SEOUL-A');

INSERT INTO device_master(id, device_name, site_code)
VALUES (NULL, 'pump-02', 'SEOUL-A');
```

`NULL`以外の値を直接指定することもできます。
指定値が現在の次の値以上なら、次の自動値はそれより大きい値から進み、小さい値を指定しても番号は戻りません。
`0`は有効です。`INT64_MAX`の後は生成できる値がないため、自動INSERTは失敗します。

重複キーや失敗したINSERTの後で番号が再使用されるかどうかに依存しないでください。
この値は行識別子であり、欠番のない業務連番ではありません。

## テーブル別の違い

| 動作 | TRANSACTION | LOOKUP | VOLATILE |
|---|:---:|:---:|:---:|
| 再起動後の行と次の自動値の保持 | O | O | X |
| 明示的トランザクション | O | X | X |
| `INSERT ... SELECT`による自動値生成 | O | X | X |
| 単一INSERT結果のROWID | O | O | O |

VOLATILEテーブルは、サーバー再起動時にデータが消失し、次の自動値は1に戻ります。
テーブル定義は保持されるため、再作成は不要です。
自動列を省略した`INSERT ... SELECT`は、TRANSACTIONのデータ移行でのみ使用できます。

```sql
INSERT INTO device_master(device_name, site_code)
SELECT device_name, site_code
  FROM staging_device
 ORDER BY device_name;
```

## INSERT結果の確認

対応するSDKは、成功した単一の`INSERT ... VALUES`の実行結果から、生成された識別子を提供できます。
batch、Append、loader、`INSERT ... SELECT`、UPSERTでは単一値を返しません。
詳細条件は[ROWID](../../rowid/)、言語別APIは
[SDK機能のサポート範囲](/dbms/development-tools-integration/sdk-support-scope/)を参照してください。

## 関連文書

- [TRANSACTIONテーブルの構造](/dbms/rdb-table-usage/table-structure-schema/)
- [LOOKUPテーブルの構造](/dbms/lookup-table-usage/table-structure-schema/)
- [VOLATILEテーブルの構造](/dbms/volatile-table-usage/table-structure-schema/)
- [LOOKUP SEQUENCE](/dbms/lookup-table-usage/sequence-column/)
