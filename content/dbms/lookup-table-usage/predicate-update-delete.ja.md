---
type: docs
title: '9.13 一般述語のUPDATE/DELETE'
weight: 130
toc: true
aliases:
  - /dbms/lookup-table-usage/privilege-predicate-performance/
---

LOOKUPテーブルは、主キーだけでなく一般条件式で複数行を更新・削除できます。
変更前に同じ条件で対象行数を確認してください。

このページの実習は、次の1つのテーブルで進め、最後に削除します。

```sql
CREATE LOOKUP TABLE ch9_predicate (
    equip_id VARCHAR(32) PRIMARY KEY,
    site     VARCHAR(16),
    status   VARCHAR(16),
    score    INTEGER
);

INSERT INTO ch9_predicate VALUES ('EQ-01', 'SEOUL', 'READY',   10);
INSERT INTO ch9_predicate VALUES ('EQ-02', 'SEOUL', 'READY',   20);
INSERT INTO ch9_predicate VALUES ('EQ-03', 'SEOUL', 'RETIRED', 30);
INSERT INTO ch9_predicate VALUES ('EQ-04', 'BUSAN', 'READY',   40);
```

<a id="condition-lookup-update"></a>

## UPDATE

条件に一致するすべての行を更新します。
`SET`式は現在の行値を参照できますが、主キー列自体は変更できません。

LOOKUP UPDATEには`WHERE`条件が必要です。
全行を更新する場合でも、サポートされる条件式を明示してください。
`WHERE`なしで全件削除できるDELETEとは区別してください。

```sql
-- 変更前に影響範囲を数えます。
SELECT COUNT(*) FROM ch9_predicate
 WHERE site = 'SEOUL' AND status = 'READY';

UPDATE ch9_predicate
   SET status = 'ACTIVE', score = score + 10
 WHERE site = 'SEOUL' AND status = 'READY';

SELECT equip_id, site, status, score FROM ch9_predicate ORDER BY equip_id;
```

COUNTは2で、EQ-01とEQ-02だけが`ACTIVE`に変わり、scoreは20・30になります。
同じSEOULでもstatusが異なるEQ-03、同じREADYでもsiteが異なるEQ-04は変わりません。

<a id="condition-lookup-delete"></a>

## DELETE

条件に一致するすべての行を削除します。
`WHERE`を省略すると、テーブルの全行が削除されます。

```sql
SELECT COUNT(*) FROM ch9_predicate WHERE status = 'RETIRED';

DELETE FROM ch9_predicate WHERE status = 'RETIRED';

SELECT equip_id, status FROM ch9_predicate ORDER BY equip_id;
```

COUNTは1で、EQ-03が削除されて3行が残ります。

<a id="design-condition-lookup-update-delete"></a>

## 条件の設計指針

1. 単一行の変更には主キー条件を使用します。
2. 一括変更前に、同じ条件の`SELECT COUNT(*)`で影響範囲を確認します。
3. 頻繁にフィルタリングするJSON値は、一般列に分離してインデックスを適用する方法を検討します。
4. 主キーを変更する場合は、既存行を削除して新しいキーで挿入します。

サポートされる演算子とJSON条件の正確な範囲は、SQLリファレンスで確認してください。

- [LOOKUPの述語UPDATE](/dbms/reference/sql/syntax/dml-syntax/lookup-predicate-update-syntax/)
- [LOOKUPの述語DELETE](/dbms/reference/sql/syntax/dml-syntax/lookup-predicate-delete-syntax/)

## 権限とパフォーマンス

UPDATEとDELETEには、それぞれ対象テーブルの`UPDATE`、`DELETE`権限が必要です。
アプリケーションが変更前後の値を直接検索する場合だけ、`SELECT`も付与します。
権限SQLの正本は[権限管理](/dbms/security-access-control/privileges/)です。

主キーの等価条件は単一行を直接検索し、一般条件式は条件を評価して変更対象を収集します。
繰り返す単一行の変更には、プリペアドステートメントとバインドを使用します。
大量変更は、同じ条件の行数と実行時間を検証環境で測定してください。

```sql
DROP TABLE ch9_predicate;
```
