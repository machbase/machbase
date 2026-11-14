---
type: docs
title: 'TAGデータUPDATEのWHERE/SET制約'
weight: 20
toc: true
---

TAGデータのUPDATEでは、対象範囲を明確にする必要があります。
WHERE句にはタグ選択条件とBASETIME条件が両方必要で、SET句は実際のデータ列だけを対象にします。

<span class="badge-since">Machbase 8.7.0からサポートする機能</span>

## SET句の制約

| 列の役割 | SET可否 | 説明 |
|-----------|:------------:|------|
| データ列 | O | `value`、補助の数値・文字列列など |
| `SUMMARIZED`データ列 | O | 元のTAG行の値が変わる |
| BASETIME列 | X | 時間軸列は変更不可 |
| PRIMARY KEY列（`name`） | X | タグ名は変更不可 |
| メタデータ列 | X | `UPDATE ... METADATA`で別途処理 |
| 隠し列・システム列 | X | 内部列はSET対象外 |

SET式には、定数、バインド変数、既存行の列を参照しない算術式・文字列式・`CASE`、許可された型変換関数、NULLを使用できます。
既存行の列を参照する式、サブクエリ、集計式はSET右辺に使用できません。

## WHERE句の制約

```sql
UPDATE table_name
   SET col = expr
 WHERE name = 'tag-name'
   AND time >= TO_DATE('2026-07-01', 'YYYY-MM-DD');
```

| WHERE条件 | 対応 |
|-----------|:---------:|
| `name = '...'` | O |
| `name = ?`, `name = :tag_name` | O |
| `? = name`, `:tag_name = name` | O |
| `name IN ('...', '...')` | O |
| `name LIKE '...'` | O |
| `time = t1` | O |
| `time = ?`, `time = :base_time` | O |
| `? = time`, `:base_time = time` | O |
| `time BETWEEN t1 AND t2` | O |
| `time >= t1 AND time < t2` | O |
| `time >= ? AND time < ?` | O |
| 片側の時間条件 | O |
| データ列条件 | O |
| タグ選択のない条件 | X |
| 時間条件のない条件 | X |
| `OR`条件 | X |
| `IN (SELECT ...)` | X |
| タグ・軸列を関数・演算式で包んだ式 | X |

バインドパラメーターは、条件の値の位置だけに使用します。
タグ名列とBASETIME列をマーカーに置き換えることはできず、バインドを使ってもタグ選択条件と時間条件は両方必要です。
同じプリペアドステートメントを再実行すると、新しくバインドした値で対象を選択し、一致行がなければ影響行数`0`で成功します。

NAMEとTIMEパラメーターの型情報とSDK別APIは、
[TAGデータUPDATEのバインドパラメーター](../tag-data-update-syntax/#tag-data-update-predicate-bind)および
[Named Bind Parameter](../../named-bind-parameter-syntax/)を参照してください。

## メタデータのUPDATE

```sql
UPDATE table_name METADATA
   SET meta_col = value
 WHERE condition;
```

メタデータUPDATEは、タグ属性領域を変更します。
実際の時系列行のデータ列を変更するTAGデータUPDATEとは、構文と対象が異なります。

## 列の役割の確認

`DESC`コマンドで列属性を確認します。

```sql
DESC sensor_tag;
```

または、システムテーブルから列のFLAGを検索します。

```sql
SELECT NAME, TYPE, FLAG
  FROM M$SYS_COLUMNS
 WHERE TABLE_ID = (
     SELECT ID FROM M$SYS_TABLES WHERE NAME = 'SENSOR_TAG'
 );
```

| FLAG値 | 意味 |
|---------|------|
| 134217728 | Tag Name |
| 16777216 | Base Time / Base Distance |
| 33554432 | Summarized |
| 67108864 | Metadata |

## エラー例

```sql
-- エラー: BASETIME列をSET対象に指定
UPDATE sensor_tag
   SET time = TO_DATE('2026-07-01', 'YYYY-MM-DD')
 WHERE name = 'TEMP-01'
   AND time >= TO_DATE('2026-07-01', 'YYYY-MM-DD');

-- エラー: 時間条件がない
UPDATE sensor_tag
   SET value = 0.0
 WHERE name = 'TEMP-01';

-- エラー: OR条件の使用
UPDATE sensor_tag
   SET value = 0.0
 WHERE name = 'TEMP-01'
    OR name = 'TEMP-02';
```

## 関連文書

- [TAGデータUPDATE構文](../tag-data-update-syntax/)
- [Named Bind Parameter](../../named-bind-parameter-syntax/)
- [ROLLUP_REBUILD構文](../../rollup-rebuild-syntax/)
