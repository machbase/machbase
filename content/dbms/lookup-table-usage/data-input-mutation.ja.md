---
type: docs
title: '9.4 データ入力と変更'
weight: 40
toc: true
---

LOOKUPテーブルの入力、更新、削除を、一連の実行可能な例で説明します。

<a id="original-85-inserting-data"></a>

## サンプルテーブルの準備

次の例は、最後のクリーンアップ文まで順に実行できます。

<a id="insert-lookup-basic"></a>

```sql
CREATE LOOKUP TABLE ch9_mutation (
    code       VARCHAR(32) PRIMARY KEY,
    label      VARCHAR(64),
    status     VARCHAR(16),
    updated_at DATETIME
);

INSERT INTO ch9_mutation VALUES ('TEMP', 'Temperature', 'ACTIVE', NOW);
INSERT INTO ch9_mutation VALUES ('PRESS', 'Pressure', 'ACTIVE', NOW);
```

SEQUENCEキーが必要なら、[SEQUENCE](/dbms/lookup-table-usage/sequence-column/)を参照してください。

<a id="update-lookup-basic"></a>

## UPDATE

単一行の変更はPRIMARY KEY条件で処理します。

```sql
UPDATE ch9_mutation
SET status = 'INACTIVE',
    updated_at = NOW
WHERE code = 'TEMP';
```

複数行を変更する場合は、先に同じ`WHERE`句で対象を検索します。
単一行の変更には、対象が明確でインデックスを使用できる`PRIMARY KEY`条件を推奨します。

PRIMARY KEY列自体はUPDATEできません。キーを変更する場合は、既存行を削除して新しいキーで再入力します。
この2文を1つのTRANSACTIONトランザクションにまとめることはできないため、途中の失敗と参照データの変更手順も設計してください。

<a id="upsert-lookup"></a>

## 重複キーの処理

SQL INSERTのキー重複時に更新が必要なら、`ON DUPLICATE KEY UPDATE`を使用します。

```sql
INSERT INTO ch9_mutation
VALUES ('TEMP', 'Temperature sensor', 'ACTIVE', NOW)
ON DUPLICATE KEY UPDATE SET label = 'Temperature sensor', status = 'ACTIVE', updated_at = NOW;
```

Appendでデータを挿入するときにPRIMARY KEYが重複すると、`LOOKUP_APPEND_UPDATE_ON_DUPKEY`設定に応じて対象行を更新できます。
この設定はLOOKUPテーブルのAppend処理における重複キーポリシーのため、本番環境では現在の設定値を確認してから使用してください。

```sql
SELECT name, value
FROM v$property
WHERE name = 'LOOKUP_APPEND_UPDATE_ON_DUPKEY';
```

<a id="refresh-lookup-table"></a>

## TABLE_REFRESH

永続保存されたLOOKUPの内容を、実行中のメモリテーブルへ再反映する必要がある場合は、`TABLE_REFRESH`を実行します。

```sql
EXEC TABLE_REFRESH(ch9_mutation);
```

通常のSQL DMLの直後に毎回実行するコマンドではありません。
対象は現在のデータベースのLOOKUPテーブルであり、READ ONLYデータベースでは実行できません。
名前の範囲・権限・エラー仕様は、[EXECプロシージャの正本](/dbms/reference/sql/syntax/execute-procedure-syntax/#table-refresh)、
クラスター運用手順は[運用とライフサイクル](/dbms/lookup-table-usage/operations-lifecycle/)を参照してください。

<a id="original-85-deleting-data"></a>

## LOOKUPデータの削除

単一行の削除にはPRIMARY KEY条件を使用します。

```sql
DELETE FROM ch9_mutation
WHERE code = 'PRESS';
```

一般条件式を使用すると、条件に一致するすべての行を削除します。
全行を削除する場合はWHERE句を省略します。

```sql
DELETE FROM ch9_mutation;
DROP TABLE ch9_mutation;
```

<a id="mutation-lookup-checklist"></a>

## 変更操作のチェックリスト

- 単一行の変更にはPRIMARY KEY条件を使用します。
- 一般条件式で一括変更する前に、同じ条件で対象範囲を検索します。
- 全行の削除前に、バックアップまたは再入力できる元データを確認します。
- PRIMARY KEY値の変更は、DELETE後のINSERTで処理します。
- Appendの重複キー処理では、`LOOKUP_APPEND_UPDATE_ON_DUPKEY`設定を確認します。
- 永続LOOKUPを実行時メモリに再反映する必要がある場合だけ、`EXEC TABLE_REFRESH(table_name)`を使用します。
