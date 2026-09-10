---
type: docs
title: '5.1 概要と使用基準'
weight: 10
toc: true
---

TAGは、センサーや設備など同じ対象を繰り返し観測した履歴の保存に適しています。
まず「1つのタグ」と「1行」を区別します。同じ名前で異なる時刻の行を入力でき、
タグ名が同じという理由だけで重複行が排除されることはありません。

<a id="overview-tag-characteristics"></a>

## TAGテーブルの特性

`PRIMARY KEY`はタグ名を指定します。リレーショナルテーブルで各行を一意に識別するキーとは
役割が異なります。1つのテーブルには時間軸または距離軸を1つ指定します。

```sql
-- 時間に沿って発生した観測値を保存する時間軸TAGです。
CREATE TAG TABLE ch5_overview_time (
    name VARCHAR(64) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
);

-- 距離や位置の区間に基づいて観測値を保存する距離軸TAGです。
-- 距離軸TAGではROLLUPを使用できません。
CREATE TAG TABLE ch5_overview_distance (
    name     VARCHAR(64) PRIMARY KEY,
    distance DOUBLE BASEDISTANCE,
    value    DOUBLE
);
```

どちらの例も、名前が1番目の列、軸が2番目の列です。時間軸は`DATETIME BASETIME`、
距離軸は`DOUBLE`、`LONG`、`ULONG`のいずれかと`BASEDISTANCE`を使用します。
`SUMMARIZED`を使用する場合は3番目の列に指定します。列の順序と指定可能な型は
[作成、変更、削除](../create-alter-drop/)、モデルごとの設計判断は
[テーブル構造とスキーマ](../table-structure-schema/)を参照してください。

`SUMMARIZED`は代表値の統計・集計に使用する列を指定する属性であり、ROLLUPオブジェクトを
自動作成するものではありません。

次の表は例のテーブルの列一覧ではなく、TAGテーブルの使用時に区別するデータの範囲です。
DATAはユーザーが入力する観測行で、METADATAとSTATはタグごとの属性・統計を確認するための
別の範囲です。

| データの範囲 | 意味 |
|---|---|
| タグ名 | センサーや繰り返し観測する対象を識別する最初の列 |
| DATA | ユーザーが入力する観測行。軸の値と複数のデータ列 |
| METADATA | タグごとの位置・単位・設定などの現在の属性。通常のDATA列とは区別 |
| STAT | `V$<TABLE>_STAT`で確認するタグごとの入力統計。例のテーブルの直接の列ではない |

<a id="overview-tag-use-criteria"></a>

## TAGが適している場合

- 同じスキーマで複数の対象の履歴を継続して追加します。
- 特定タグの時間・距離範囲を頻繁に検索します。
- 現在の属性を条件としてタグを選択し、その履歴を分析します。
- 時間軸TAGで繰り返し区間統計を保存・検索する必要があります。この場合、ROLLUPの設計は
  [TAG ROLLUP](../../tag-rollup-usage/)で別途確認します。

単一値モデルは測定項目ごとにタグを分け、複数値モデルは同じ観測で得られた温度・圧力などを
1行にまとめます。測定時刻の異なる値を無理に同じ行に入れず、欠損・品質ポリシーを定めます。
時系列の同時刻のデータも重複収集の可能性があるため、名前・時刻・値の重複処理ポリシーを
別途確認します。

<a id="overview-tag-not-use"></a>

## 他のテーブルを検討する場合

| 要件 | 検討する代替案 |
|---|---|
| 観測対象よりイベント自体が重要なイベント検索 | LOG |
| 永続的なマスターデータの一般条件による検索・変更 | LOOKUP |
| 複数のDMLに対する明示的なトランザクションとリレーショナルな変更 | TRANSACTION（Standard Edition専用） |
| 元データから再構成できる共有状態キャッシュ | VOLATILE |

TAGでもJOINと制限付きの値補正を使用できます。「JOINが必要ならTAGは使えない」
「計測値は必ずTAGに保存する」といった判断は避けます。

ただし、DATAのUPDATEはStandard Edition専用です。Cluster EditionではMETADATA UPDATEのみ
使用できるため、値補正が必要な場合は再入力と再集計の手順も設計します。

<a id="overview-tag-design-flow"></a>

## 設計手順

1. タグがセンサー・装置・検査回のどれを識別するかを決めます。
2. 測定時刻または距離・位置の意味と単位を決めます。
3. 値の型、NULLと品質表示、観測周期を決めます。
4. 観測ごとに保存する属性と現在のMETADATAを区別します。
5. 区間検索・集計・補正・保管の要件をEditionのサポート範囲と照合します。

例のテーブルの確認と削除は次のとおりです。

```sql
-- 例のテーブルのスキーマを確認します。
DESC ch5_overview_time;
DESC ch5_overview_distance;

-- 後の例と名前が重複しないように削除します。
DROP TABLE ch5_overview_distance;
DROP TABLE ch5_overview_time;
```

次は[スキーマ設計](../table-structure-schema/)と
[入力・検索の実習](../data-input-mutation/)です。
