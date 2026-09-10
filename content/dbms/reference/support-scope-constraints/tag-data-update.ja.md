---
type: docs
title: '16.6.4 TAGデータUPDATEサポート表'
weight: 40
toc: true
---

TAGテーブルの実際の時系列データは、`UPDATE table_name SET ... WHERE ...`で更新できます。
このページではTAGデータUPDATEで許可するWHERE条件とSET対象をまとめます。
メタデータの更新には別の`UPDATE ... METADATA`構文を使用します。

<span class="badge-since">Machbase 8.7.0以降でサポート</span>

TAGデータUPDATEは、Standard Editionの論理TAGテーブルでのみサポートします。
Cluster Editionと内部のrawコンポーネントテーブルへの直接UPDATEはサポートしません。

## WHERE条件別のサポート状況

TAGデータUPDATEには、1つのタグ選択条件と1つ以上のBASETIME軸条件が必要です。

| WHERE条件 | サポート | 備考 |
|-----------|:---:|------|
| `name = 'tag-01'` | O | 単一タグを選択 |
| `name = ?`, `name = :tag_name` | O | 位置指定/名前付きバインドで単一タグを選択 |
| `? = name`, `:tag_name = name` | O | 左右を逆にした等値条件もサポート。列を左辺に置く形式を推奨 |
| `name IN ('tag-01', 'tag-02')` | O | リテラル/バインド値のリストをサポート。サブクエリの`IN`は非対応 |
| `name LIKE 'tag-%'` | O | パターンに一致するタグを対象に展開 |
| `time = t1` | O | BASETIME列の等値条件 |
| `time = ?`, `time = :base_time` | O | 位置指定/名前付きバインドで基準時刻を指定 |
| `? = time`, `:base_time = time` | O | 左右を逆にした等値条件をサポート |
| `time BETWEEN t1 AND t2` | O | 両端を含む |
| `time >= t1 AND time < t2` | O | `>`、`>=`、`<`、`<=`の組み合わせをサポート |
| `time >= ? AND time < ?` | O | 範囲の境界値にもバインドマーカーを使用可能 |
| 片側のみの時刻条件 | O | 例: `time >= t1` |
| データ列の述語 | O | 例: `value > 100`。タグ/時刻条件と併用 |
| 条件のないUPDATE | X | TAGデータ全体のUPDATEは不可 |
| タグ選択のない時刻条件のみ | X | 対象タグの指定が必要 |
| 時刻条件のないタグ条件のみ | X | BASETIME範囲の指定が必要 |
| `OR`条件 | X | TAGデータUPDATE条件では不可 |
| サブクエリ/集約式 | X | UPDATE対象の決定条件には使用不可 |
| タグ/軸列を関数・演算式で囲む式 | X | タグ選択とBASETIME条件では該当列を直接指定する必要がある |

バインドパラメーターは値のみを置き換えます。必須のタグ選択・BASETIME条件、許容する条件構造、
SET対象は変わりません。プリペアドステートメントを再実行すると最新のバインド値で対象を選び直し、
一致する行がなければ影響行数`0`で成功します。

## SET対象列別のサポート状況

| SET対象 | サポート | 備考 |
|---------|:---:|------|
| データ列 | O | `value`や補助列などのユーザーデータ列 |
| `SUMMARIZED`データ列 | O | 元のTAGデータを更新 |
| 複数のデータ列 | O | 同じUPDATE文でまとめて指定可能 |
| `name` (PRIMARY KEY) | X | タグ名は変更不可 |
| `time` (BASETIME) | X | 時間軸列は変更不可 |
| メタデータ列 | X | `UPDATE table_name METADATA SET ...`を使用 |
| 隠し/システム列 | X | 内部列はUPDATE対象外 |

SET式には、定数、バインド変数、既存行の列を参照しない算術式・関数・`CASE`式・文字列連結、
列制約が許容する場合はNULL値を使用できます。SETの右辺で既存行の列を参照することはできず、
サブクエリと集約式も使用できません。

## 正式な参照先

実行構文とパラメーターのメタデータは[TAGデータUPDATE](../../sql/syntax/dml-syntax/tag-data-update-syntax/#tag-data-update-predicate-bind)を、
SDK別のマーカーAPIは[Named Bind Parameter](../../sql/syntax/named-bind-parameter-syntax/)を、
診断は[TAGの制約とトラブルシューティング](../../../tag-table-usage/constraints-errors-troubleshooting/)を参照してください。
