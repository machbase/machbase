---
type: docs
title: 'TAGデータのUPDATE'
weight: 10
toc: true
---

TAGテーブルの時系列データは、通常の`UPDATE`文で変更します。
`UPDATE TAG TABLE`という別のキーワードは使用しません。

<span class="badge-since">Machbase 8.7.0からサポートする機能</span>

TAGデータのUPDATEは、Standard Editionの論理TAGテーブルだけでサポートします。

## 構文

```sql
UPDATE table_name
   SET data_column = expression [, data_column = expression ...]
 WHERE tag_selector
   AND time_condition
   [AND data_predicate ...];
```

`tag_selector`には、`name = ...`、`name IN (...)`、`name LIKE ...`条件を使用できます。
`time_condition`には、BASETIME列の等価、`BETWEEN`、両側範囲、片側範囲条件を使用できます。

## 例

### 単一タグと時間範囲

```sql
UPDATE sensor_tag
   SET value = 110,
       status = 1
 WHERE name = 'TEMP-01'
   AND time >= TO_DATE('2026-07-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
   AND time <  TO_DATE('2026-07-02 00:00:00', 'YYYY-MM-DD HH24:MI:SS');
```

### 複数タグ

```sql
UPDATE sensor_tag
   SET note = 'corrected'
 WHERE name IN ('TEMP-01', 'TEMP-02')
   AND time BETWEEN TO_DATE('2026-07-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
                AND TO_DATE('2026-07-01 23:59:59', 'YYYY-MM-DD HH24:MI:SS');
```

### LIKEとデータ列の述語

```sql
UPDATE sensor_tag
   SET status = 7
 WHERE name LIKE 'TEMP-%'
   AND time >= TO_DATE('2026-07-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
   AND value > 100;
```

### CASE式

```sql
UPDATE sensor_tag
   SET grade = CASE
                 WHEN 1 = 1 THEN 'HIGH'
                 ELSE 'LOW'
               END
 WHERE name = 'TEMP-01'
   AND time >= TO_DATE('2026-07-01', 'YYYY-MM-DD');
```

<a id="tag-data-update-predicate-bind"></a>

### NAMEとTIME条件でのバインドパラメーター

`WHERE`句のタグ名とBASETIME条件値には、位置指定マーカー`?`または名前付きマーカー`:name`を使用できます。
1つのSQL文でマーカー方式を混在させないでください。

位置指定マーカーは、SQLの出現順にSET値、タグ名、基準時刻をバインドします。

```sql
UPDATE sensor_tag
   SET value = ?,
       status = ?,
       note = ?
 WHERE name = ?
   AND time = ?;
```

名前付きマーカーは、SDKの名前指定APIでSQLの出現順に関係なく値を渡せます。

```sql
UPDATE sensor_tag
   SET value = :value,
       status = :status,
       note = :note
 WHERE name = :name
   AND time = :time;
```

同じプリペアドステートメントを再実行すると、新しくバインドしたSET、NAME、TIMEの値で対象行を選択します。
NAMEパラメーターは`VARCHAR`、TIMEパラメーターは`DATETIME`の型情報を保持します。
条件に一致する行がなければ、エラーなしで影響行数`0`を返します。

`? = name`、`:name = name`、`? = time`、`:time = time`のように、列が右側にある等価条件もサポートします。
ただし、読みやすさのため列を左側に書く形式を推奨します。
既存の許可されたBASETIME範囲条件の値の位置にも、マーカーを使用できます。

SDK別の名前指定APIと位置番号規則は、[Named Bind Parameter](../../named-bind-parameter-syntax/)を参照してください。

## メタデータのUPDATE

TAGのメタデータ列は、TAGデータUPDATEのSET対象ではありません。
メタデータは`UPDATE ... METADATA`構文で変更します。

```sql
UPDATE sensor_tag METADATA
   SET location = 'zone-2',
       owner = 'ops'
 WHERE name = 'TEMP-01';
```

## 制約

- WHERE句には、1つのタグ選択条件と1つ以上のBASETIME条件が必要です。
  `name =`、`name IN (...)`、`name LIKE ...`と、等価・BETWEEN・両側/片側の時間範囲を使用でき、データ列条件は`AND`で追加できます。
- `OR`、サブクエリ、集計式、タグ・軸の列をそのまま参照しない式は、UPDATE対象条件に使用できません。
- `name`（PRIMARY KEY）、`time`（BASETIME）、メタデータ列、隠し列・システム列は、データUPDATEのSET対象にできません。
- SET右辺は、定数、バインド変数、既存行の列を参照しない関数・演算式・`CASE`・NULLだけを使用できます。
  `value = value + 1`のように既存行の列を参照する式は許可されません。
- バインドパラメーターは値だけを置き換え、タグ選択条件、BASETIME条件、SET対象列の制約を変更しません。
- UPDATEは、すでに具体化されたROLLUP行を自動補正しません。
  ROLLUPの検索前に、影響を受けた区間を`ROLLUP_REBUILD`で再構築します。

## 関連文書

- [TAGデータUPDATEのWHERE/SET制約](../tag-data-update-where-set-constraints/)
- [Named Bind Parameter](../../named-bind-parameter-syntax/)
- [ROLLUP_REBUILD構文](../../rollup-rebuild-syntax/)
