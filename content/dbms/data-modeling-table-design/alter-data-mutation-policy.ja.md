---
type: docs
title: '4.3 データ変更ポリシー'
weight: 30
toc: true
---

`UPDATE`、`DELETE`、`TRUNCATE` のサポートはタイプごとに異なります。このページではモデル選択に
必要な方針をまとめます。正確な構文と制約はリンク先の SQL リファレンスを基準にしてください。

変更ポリシーは、更新できるかだけでなく、誰がどの範囲を変え、失敗時にどこまで戻せるかを定めます。
現在状態の更新、元の計測値の補正、スキーマ変更、保持期限による削除を別々の処理として区別します。

## テーブルタイプ別の変更サポート

| テーブルタイプ | UPDATE | DELETE | TRUNCATE |
|------------|--------|--------|----------|
| TAG | Standard の DATA 補正: タグ選択と BASETIME の条件が必要 | `BEFORE`、タグ/軸条件、または全削除 | X |
| LOG | X | `BEFORE`、`OLDEST`、`EXCEPT`、全削除 | O |
| TRANSACTION | O | O | O |
| VOLATILE | 主キー条件 | 主キー条件または全削除 | X |
| LOOKUP | 一般条件式、PK 変更不可 | 一般条件式または全削除 | X |

LOG は入力したイベントを更新しない構造です。頻繁に変更する状態や設定は VOLATILE、LOOKUP、
TRANSACTION に保存してください。

## 変更単位と失敗処理

| 操作 | モデルで決める事項 |
|---|---|
| 現在の設定値の更新 | キー、許容値、同時更新者の処理 |
| 誤った計測値の補正 | タグ・時間範囲、補正理由、ROLLUP 再計算 |
| LOG イベントの訂正 | 原文を残して補正イベントを関連付けるか |
| 参照キーの置き換え | 参照データの切り替え順序と途中失敗の処理 |
| 期間削除 | 保持基準時刻、削除範囲、必要なバックアップ |

複数の TRANSACTION DML は明示的トランザクションにまとめられます。LOOKUP・VOLATILE の変更や
LOG・TAG 入力も同じトランザクションに参加すると考えないでください。TAG 履歴の保存後に VOLATILE
キャッシュ更新が失敗しても履歴は残る場合があり、再構築や再試行が必要です。Append の参加範囲は
API と対象タイプで異なるため、[SDK サポート範囲](/dbms/development-tools-integration/sdk-support-scope/)で確認します。

複数行を変更する前に、同じ条件で件数と代表行を確認します。この事前検索は行をロックせず、
後の変更範囲を固定するものでもありません。同時入力・更新がある場合は作業時間と対象範囲も制御し、
結果の影響行数と変更後の値を確認します。

<a id="policy-update"></a>

## UPDATE ポリシー

### TRANSACTION, VOLATILE, LOOKUP

- TRANSACTION は一般的なリレーショナル `UPDATE` とトランザクションをサポートします。
- VOLATILE は主キーの一致条件で対象を指定します。
- LOOKUP は一般条件式を使えますが、主キー列そのものは変更できません。

LOOKUP UPDATE には WHERE が必要です。LOOKUP・VOLATILE の主キー変更は削除と新キー入力を
別々の文で行うため、元データの保護と参照の切り替え順序を先に定めます。
両方をまとめてロールバックする必要がある場合は TRANSACTION を検討します。

LOOKUP の対応述語と式は
[LOOKUP 述語 UPDATE](/dbms/reference/sql/syntax/dml-syntax/lookup-predicate-update-syntax/)を参照してください。

<a id="policy-update-policy-tag-data-update"></a>
<a id="policy-update-distinction-tag-data-update-metadata"></a>
<a id="policy-update-tag-data-update-where-set-standard-only"></a>

### TAG data UPDATE

TAG の実際の時系列データとメタデータは、異なる構文で更新します。

| 対象 | 構文 | 主な制約 |
|------|------|-----------|
| 時系列データ | `UPDATE tag_table SET ... WHERE ...` | タグ選択と BASETIME の両条件が必要 |
| メタデータ | `UPDATE tag_table METADATA SET ...` | TAG メタデータ専用構文 |

TAG data UPDATE は Standard Edition の論理 TAG テーブルでサポートされます。タグ名、BASETIME、
メタデータ列は `SET` の対象にできません。修正範囲にマテリアライズ済みの集計があれば
`ROLLUP_REBUILD` で再構築してください。

TAG DATA の SET 右辺は既存行の列を参照できません。`SET value = value + 1` のような一括加算では
補正しません。計算済み補正値を定数またはパラメーターで渡し、必要範囲に限定します。
補正履歴が必要なら上書きだけでなく、変更前後の値と理由を別の履歴に保存します。

構文と許容式は次のリファレンスを正本とします。

- [TAG data UPDATE](/dbms/reference/sql/syntax/dml-syntax/tag-data-update-syntax/)
- [TAG data UPDATE の WHERE/SET 制約](/dbms/reference/sql/syntax/dml-syntax/tag-data-update-where-set-constraints/)
- [TAG メタデータ](/dbms/tag-table-usage/tag-metadata/)

LOG は `UPDATE` をサポートしません。

<a id="policy-delete"></a>

## DELETE ポリシー

### TRANSACTION, VOLATILE, LOOKUP

- TRANSACTION は一般的な `WHERE` 条件で削除できます。
- VOLATILE は主キー条件で削除するか、条件なしで全行を削除できます。
- LOOKUP は一般条件式で削除するか、`WHERE` なしで全行を削除できます。

LOOKUP の対応述語は
[LOOKUP 述語 DELETE](/dbms/reference/sql/syntax/dml-syntax/lookup-predicate-delete-syntax/)を参照してください。

### LOG

LOG は任意の一般的な `WHERE` ではなく、ログ保持用の削除構文を使います。`OLDEST`、`EXCEPT`、
`BEFORE`、全削除から目的に合う形式を選びます。正確な構文と実行例は
[LOG データライフサイクル](/dbms/log-table-usage/operations-lifecycle/)を参照してください。

<a id="condition-tag-kv-delete-before"></a>

### TAG/KV

TAG/KV は `BEFORE` で古いデータを削除するか、タグ名と軸条件で対象を選択します。
`BEFORE` の時刻は現在より過去である必要があります。構文は
[TAG データ変更](/dbms/tag-table-usage/data-input-mutation/)を参照してください。

保持目的の手動削除を繰り返す場合は
[Retention Policy](/dbms/operations-configuration-recovery/policy-data-retention/)を使用します。

<a id="delete-tag-metadata"></a>
<a id="policy-delete-delete-tag-metadata"></a>

### TAG メタデータ

`DELETE FROM table_name METADATA` で削除します。対象のタグに実データが1つでも残っていれば、
文全体が失敗します。

詳細は [TAG メタデータ](/dbms/tag-table-usage/tag-metadata/)を参照してください。

<a id="policy-truncate"></a>

## TRUNCATE ポリシー

`TRUNCATE TABLE` は LOG と TRANSACTION だけでサポートされます。スキーマとインデックス定義を
保持し、すべての行を削除します。

| 項目 | TRUNCATE | DELETE |
|------|----------|--------|
| 対象 | テーブル全体 | タイプにより全体または条件指定 |
| `WHERE` | 不可 | 対応範囲で可能 |
| TRANSACTION のロールバック | 明示的トランザクションで可能 | 明示的トランザクションで可能 |

削除前にバックアップと再入力経路を確認します。TAG は対応する `BEFORE` またはタグ/軸条件、
VOLATILE・LOOKUP の全削除は条件なしの `DELETE` を使用します。

TRANSACTION のロールバック可否を LOG の削除へ適用しないでください。確定済みの変更は後の
ROLLBACK で戻せません。また、削除と物理ディスク領域の返却は同時とは限らないため、
使用容量と対象テーブルの領域回収状態を確認します。
