---
type: docs
title: 'NEXTVAL関数'
weight: 60
toc: true
---

`NEXTVAL`は、LOOKUPテーブルのSEQUENCE列の次の自動増分値を`INT64`で返します。
`INSERT`の値の式でのみ使用できます。

## 構文

```sql
NEXTVAL(sequence_column)
```

- `sequence_column`は`PROPERTY(SEQUENCE=...)`プロパティで作成された列である必要があります。
- `INSERT`以外の文脈（SELECT、WHEREなど）では使用できません。
- 引数は正確に1つで、同じINSERT対象テーブルのSEQUENCE列を指定します。

---

## Sequence列の作成

SEQUENCE列は、LOOKUPテーブルの`LONG`または`INT64`列でサポートします。
`PROPERTY(SEQUENCE=1)`は開始値を1に指定します。

```sql
CREATE LOOKUP TABLE seq_lookup (
    id   LONG PROPERTY(SEQUENCE=1) PRIMARY KEY,
    name VARCHAR(64)
);
```

---

## NEXTVALの使用

```sql
-- NEXTVALで自動増分IDを挿入
INSERT INTO seq_lookup (id, name) VALUES (NEXTVAL(id), 'sensor-a');
INSERT INTO seq_lookup (id, name) VALUES (NEXTVAL(id), 'sensor-b');
INSERT INTO seq_lookup (id, name) VALUES (NEXTVAL(id), 'sensor-c');

-- 結果の確認
SELECT * FROM seq_lookup;
id    name
----------
1     sensor-a
2     sensor-b
3     sensor-c

DROP TABLE seq_lookup;
```

---

## 注意事項

- `NEXTVAL`は`INSERT`文でのみ使用できます。
- SEQUENCE列は**LOOKUPテーブル**専用です。TAG、LOG、VOLATILE、TRANSACTIONテーブルでは使用できません。
- `LONG`・`INT64`以外の型、通常の列、`SELECT`・`WHERE`からの呼び出しはエラーです。
- Sequence番号はトランザクションのロールバックやエラー発生後も再利用されない場合があり、欠番が生じることがあります。
- DDLの詳細は[DDL - Sequence Column](../../syntax/)を参照してください。
