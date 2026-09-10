---
type: docs
title: '10.4 データ入力と変更'
weight: 40
toc: true
aliases:
  - /dbms/volatile-table-usage/on-duplicate-key-update/
---

VOLATILEテーブルの`INSERT`、重複キー更新、`DELETE`を、実行可能な例で説明します。

<a id="original-85-insert-update"></a>
<a id="on-duplicate-key-update"></a>

## データ入力と更新

次の例は、最後のクリーンアップ文まで順に実行できます。
最新状態のように同じキーの値を継続的に更新する場合は、`PRIMARY KEY`を定義し、`ON DUPLICATE KEY UPDATE`を使用します。

```sql
CREATE VOLATILE TABLE ch10_mutation (
    id         INTEGER PRIMARY KEY,
    direction  VARCHAR(10),
    refcnt     INTEGER
);

INSERT INTO ch10_mutation VALUES (1, 'west', 0);
INSERT INTO ch10_mutation VALUES (2, 'east', 0);

INSERT INTO ch10_mutation VALUES (1, 'south', 0)
ON DUPLICATE KEY UPDATE;

INSERT INTO ch10_mutation VALUES (1, 'south', 0)
ON DUPLICATE KEY UPDATE SET refcnt = 1;

SELECT * FROM ch10_mutation ORDER BY id;
```

重複キーがなければ新しい行を挿入します。重複キーがある場合、`SET`句のない構文は入力値で行全体を更新し、
`SET`句のある構文は指定した列だけを更新します。`PRIMARY KEY`自体は更新対象に指定できません。

大量取り込みAPIの初期化・バインド・エラー処理は、言語とドライバーによって異なります。
不完全なコード断片をコピーせず、[SDKと連携](/dbms/development-tools-integration/)の該当ドライバーの例を使用してください。

<a id="volatile-primary-key-update"></a>

## 条件付き更新

既存行の一部の列だけを変更する場合は`UPDATE`を使用します。
`INSERT ... ON DUPLICATE KEY UPDATE`が「なければ挿入し、あれば更新する」のに対し、
`UPDATE`は対象行が存在する場合だけ値を変更します。

VOLATILEテーブルの`UPDATE`には`WHERE`が必要です。
条件は削除と同様に`PRIMARY KEY = 値`の形式のみサポートし、他の列の条件や複合条件は使用できません。
`WHERE`を省略した全件更新もサポートしていません。

```sql
UPDATE ch10_mutation SET refcnt = refcnt + 1 WHERE id = 2;
SELECT * FROM ch10_mutation ORDER BY id;
```

`SET`句に`PRIMARY KEY`列は指定できません。
キーを変更する場合は、既存行を削除して新しいキーで再入力します。

<a id="original-85-deleting-data"></a>

## データの削除

条件付き削除は`PRIMARY KEY = 値`の形式のみサポートします。
他の列の条件や複合条件は使用できません。

```sql
DELETE FROM ch10_mutation WHERE id = 2;
SELECT * FROM ch10_mutation ORDER BY id;
DROP TABLE ch10_mutation;
```

テーブル定義を保持したまま全行を削除するには、`DELETE FROM テーブル名`のようにWHEREを省略します。
スキーマも初期化する場合は、DROP後に再作成します。
サーバーを再起動するとデータだけが消え、テーブル定義は残るため、再作成ではなく再ロードのスクリプトを別途管理します。
