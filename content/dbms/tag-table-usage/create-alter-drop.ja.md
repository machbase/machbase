---
type: docs
title: '5.3 作成、変更、削除'
weight: 30
toc: true
---
TAGテーブルにはタグ識別子と1つの軸列が必須です。このページでは実行可能な基本例を示し、
全オプションについてはSQLリファレンスを案内します。

<a id="original-85-creating-tag-tables"></a>

## TAGテーブルの作成

TAGテーブルでは最初の2つの列の役割が固定されています。名前列と軸列は省略できず、
順序を変えたり別の位置に指定したりすると、作成に失敗します。

| 列の位置 | 用途と特性 |
| --- | --- |
| 1番目 | タグ名です。`VARCHAR`列に`PRIMARY KEY`を指定し、他の型は使用できません。センサー・設備・検査回など繰り返し観測する対象を識別します。同じタグ名で複数のDATA行を入力できるため、リレーショナルテーブルの行ごとの一意キーとは区別します。 |
| 2番目 | 観測値を時間または距離・位置で整列・検索します。時間軸は`DATETIME BASETIME`、距離軸は`DOUBLE`、`LONG`、`ULONG`のいずれかに`BASEDISTANCE`を指定します。1つのTAGテーブルに定義できるのは時間軸または距離軸のいずれか1つです。 |
| 3番目以降 | 温度、圧力、状態、品質コードなど観測ごとに変化するDATA列です。数値型、`VARCHAR`、`DATETIME`、JSON、数値ARRAY、BINARYを使用できます。複数のDATA列からタグを代表する値を1つ選ぶと、タグごとの値の統計と自動ROLLUPの基準にできます。この場合は`SUMMARIZED`を指定します。任意指定であり、3番目の列にのみ指定できます。 |

ARRAYは名前列、軸列、`SUMMARIZED`列には使用できず、それ以外のDATA列で
使用します。LOGテーブルとは異なり、TAGテーブルのDATA列では`TEXT`、`CLOB`、`BLOB`を
使用できないため、長い文字列は`VARCHAR`、バイナリデータは`BINARY`で保存します。型の表記と
値の範囲は[データ型リファレンス](/dbms/reference/sql/types/)を参照してください。

タグごとに1回だけ保存する属性は、上記の列位置ではなく`METADATA`句で別途宣言します。
次の時間軸の例では`location`が該当します。

次の2つのテーブルは、このページ専用の独立した実習用です。既存オブジェクトがないことを
確認して順番に実行します。データの実際の意味に合う時間軸または距離軸を選びます。
距離軸TAGではROLLUPを使用できません。

### 時間軸TAG

```sql
CREATE TAG TABLE ch5_tag_ddl (
    name  VARCHAR(32) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE SUMMARIZED
) METADATA (
    location VARCHAR(64)
);
```

`SUMMARIZED`を指定すると、2つの効果があります。まず、タグごとのSTATビューに`MIN_VALUE`、
`MAX_VALUE`など値自体の統計がこの列を基準として蓄積されます。`SUMMARIZED`列が
ない場合、STATには行数と軸の範囲だけが残り、値の統計は保存されません。次に、`WITH ROLLUP`に
よる自動作成とJSONドキュメント全体のROLLUPがこの列を対象とします。

一方、通常の数値ROLLUPは`CREATE ROLLUP ... ON table(column)`で列を直接指定するため、
`SUMMARIZED`がなくても作成できます。値の統計が不要でROLLUPも手動で作成する場合は指定不要です。
指定できる型はサポート対象の数値型とJSONです。ROLLUPの作成条件は
[第6章](../../tag-rollup-usage/)を参照してください。

位置・単位などタグごとに1回保存する属性は`METADATA`、測定ごとに変化する値は通常の
データ列に定義します。

### 距離軸TAG

```sql
CREATE TAG TABLE ch5_distance_ddl (
    name     VARCHAR(32) PRIMARY KEY,
    distance DOUBLE BASEDISTANCE,
    value    DOUBLE
);
```

小数の距離値には`DOUBLE`、整数の軸には値の範囲に応じて`LONG`または`ULONG`を使用します。

## TAGテーブルの変更

この節のMETADATA ADD/DROP実習はStandard Editionを前提とします。
TAGデータ列の任意の変更には制限があります。スキーマを拡張する場合は、まず新しいテーブルへの
移行を検討してください。メタデータ列はサポートされる構文で追加・削除できます。

```sql
ALTER TABLE ch5_tag_ddl
    METADATA ADD COLUMN (team VARCHAR(32));

ALTER TABLE ch5_tag_ddl METADATA
    ADD COLUMN (limits DECIMAL(12,4)[2] DEFAULT [0.0000, NULL]);

ALTER TABLE ch5_tag_ddl
    METADATA DROP COLUMN (team);

ALTER TABLE ch5_tag_ddl METADATA
    DROP COLUMN (limits);
```

Standard EditionではTAG METADATAに固定長の数値ARRAY列を追加できます。
ALTER前から存在するメタデータ行には指定したARRAY DEFAULTが適用されます。ALTER後にTAG DATAの
入力で自動登録されるメタデータ行にはDEFAULTが再適用されず、新しいARRAY列全体がNULLになります。

TAG DATAの通常のARRAY列は`CREATE TABLE`で宣言できますが、ALTERでは追加できません。
TAG METADATA ARRAYにはインデックスが自動作成されず、明示的なインデックスもサポートされません。
詳細は[TAGメタデータ](../tag-metadata/)と
[数値ARRAY型](/dbms/reference/sql/types/array/)を参照してください。

データのある運用テーブルでは、変更前に依存クエリ、SDKの列順序、再入力経路を確認します。
ALTER後は`DESC ch5_tag_ddl;`とMETADATAの検索で変更結果を確認します。

## TAGテーブルの削除

`DROP TABLE`は生データとメタデータをまとめて削除します。ROLLUPなどの依存オブジェクトがある場合は、
先に依存関係に従って削除する必要があります。TAGの`DROP TABLE ... CASCADE`は関連するROLLUPも
削除できるため、単純な後片付けの標準コマンドにはしません。
Custom ROLLUPの対象テーブルについては、別途依存関係の制約も確認します。

```sql
DROP TABLE ch5_distance_ddl;
DROP TABLE ch5_tag_ddl;
```

正確な属性、許容範囲、DDLは
[DDL構文リファレンス](/dbms/reference/sql/syntax/ddl-syntax/)を参照してください。

次に読む内容:

- [TAGテーブル構造とスキーマ](../table-structure-schema/)
- [TAGデータの入力と変更](../data-input-mutation/)
- [TAGメタデータ](../tag-metadata/)
