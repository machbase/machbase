---
type: docs
title: '13.7 スキーマ変更チェックリスト'
weight: 80
toc: true
---

運用中のスキーマを変更する前に、次の項目を順に確認します。

## 変更前の確認

### 1. テーブルタイプを確認

```sql
SELECT NAME AS TABLE_NAME, TYPE AS TABLE_TYPE
  FROM M$SYS_TABLES
 WHERE NAME = 'TARGET_TABLE';
```

ALTER TABLE のサポートはタイプごとに異なります。
[テーブルタイプ別の管理範囲](/dbms/reference/support-scope-constraints/table-types-type/)を先に確認してください。

### 2. 現在のスキーマを確認

```sql
-- 列情報を確認
DESC target_table;

-- インデックスを確認
SELECT i.NAME AS INDEX_NAME, i.TYPE AS INDEX_TYPE
  FROM M$SYS_INDEXES i
  JOIN M$SYS_TABLES t
    ON i.DATABASE_ID = t.DATABASE_ID
   AND i.TABLE_ID = t.ID
 WHERE t.NAME = 'TARGET_TABLE';
```

### 3. データ量を確認

```sql
SELECT COUNT(*) FROM target_table;
```

大規模テーブルのスキーマ変更には時間がかかる場合があります。テスト環境で所要時間とロックの影響を
測定し、サービスのメンテナンス時間に実行してください。

### 4. Retention Policy の実行を確認

```sql
SELECT * FROM V$RETENTION_JOB WHERE TABLE_NAME = 'TARGET_TABLE';
```

Retention Policy が実行中の場合は、完了を待ってからスキーマを変更してください。

### 5. DDL 競合ポリシーを設定

Standard Edition は異なるオブジェクトの DDL を同時実行できます。同じオブジェクトや直接関連する
オブジェクトの DDL は競合するため、運用デプロイセッションで許容する待機時間を先に設定します。

```sql
-- 競合する DDL ロックを最大10秒待機
ALTER SESSION SET DDL_LOCK_TIMEOUT = 10;

-- セッション別の設定値を確認
SELECT id, user_name, ddl_lock_timeout
  FROM v$session
 WHERE closed = 0
 ORDER BY id;
```

| 同時実行対象 | 判定 |
|----------------|------|
| 名前の異なる独立したテーブル | 並列実行可能 |
| 同一オブジェクトまたは同一名 | 競合 |
| テーブル変更・削除 DDL とそのテーブルのインデックス DDL | 競合 |
| ビュー DDL と元テーブルの変更・削除 DDL | 競合 |
| TAG テーブル変更・削除 DDL と関連 Rollup・Retention DDL | 競合 |

Cluster Edition には `DDL_LOCK_TIMEOUT` がなく、従来の DDL 直列化ポリシーを使います。
詳細は [DDL の同時実行とロック](/dbms/reference/sql/syntax/ddl-syntax/#ddl-concurrency)を参照してください。

---

## 列追加チェックリスト

- [ ] 追加する列の型は対象テーブルタイプでサポートされるか。
- [ ] LOG/TRANSACTION で列を追加すると、既存行の新しい列が NULL になることを確認したか。
- [ ] 列名の重複を確認したか。

```sql
ALTER TABLE sensor_log ADD COLUMN (new_col DOUBLE);
```

---

## 列削除チェックリスト

- [ ] 列がインデックスに含まれるか。含まれる場合は先にインデックスを削除する。
- [ ] アプリケーションのクエリが列を参照していないか。
- [ ] 削除した列のデータは復旧できないことを確認したか。

```sql
ALTER TABLE sensor_log DROP COLUMN (old_col);
```

---

## インデックス変更チェックリスト

- [ ] インデックスの作成・削除はクエリ性能に直接影響する。
- [ ] 作成時は既存データも索引化するため、大規模テーブルでは時間がかかる。
- [ ] 未使用インデックスは INSERT 性能を下げるため、削除を検討する。
- [ ] `IF NOT EXISTS` を使う場合、同名の既存インデックス定義を別途確認する。

```sql
-- 再デプロイで条件付き作成
CREATE INDEX IF NOT EXISTS idx_new ON sensor_log (sensor_id);

-- 名前だけの一致で何もしない場合があるため、実際のマッピングを確認
SHOW INDEX idx_new;

-- 不要なインデックスを削除
DROP INDEX idx_old;
```

`IF NOT EXISTS` は、同じデータベース・所有者のインデックス名だけを確認します。既存のテーブル、列、
インデックスタイプ、設定がデプロイの意図と一致するかは、
[INDEX 構文](/dbms/reference/sql/syntax/index-syntax/#create-index-if-not-exists)に従って別途検証します。

---

## Retention Policy 変更チェックリスト

- [ ] 変更が必要な場合: 既存ポリシーを解除 → 新ポリシーを作成・適用。
- [ ] 保持期間を短くする場合: 次の削除対象が増える可能性があるため、データ損失を検討する。

```sql
-- 既存ポリシーを解除
ALTER TABLE sensor_tag DROP RETENTION;

-- 新ポリシーを適用
ALTER TABLE sensor_tag ADD RETENTION new_policy;
```

---

## DDL 競合の処理

デフォルトの `DDL_LOCK_TIMEOUT=0` では、競合時に
`ERR-02031: Resource busy (<object>)` が即座に返ります。

1. `ERR-02031` だけを、回数と待機間隔を制限して再試行します。
2. 再試行前に対象と依存オブジェクトの現在状態を再取得します。
3. 待機後、先行 DDL の結果により `already exists` または `table not found` が返る場合があります。
4. 構文・権限エラー、`already exists`、`table not found` に同じ SQL を繰り返し実行しないでください。
5. `machsql` 自動化では終了コードだけでなく出力内の `ERR-` も確認します。

待機時間の終了や操作のキャンセル後も再実行できますが、先行処理が反映されたかを確認してから再試行します。

---

## 変更後の検証

```sql
-- スキーマ変更を確認
DESC target_table;

-- データ整合性を確認
SELECT COUNT(*) FROM target_table;

-- インデックス状態を確認
SELECT i.NAME AS INDEX_NAME, i.TYPE AS INDEX_TYPE
  FROM M$SYS_INDEXES i
  JOIN M$SYS_TABLES t
    ON i.DATABASE_ID = t.DATABASE_ID
   AND i.TABLE_ID = t.ID
 WHERE t.NAME = 'TARGET_TABLE';
```

---

**次に読む文書:**

- [データ保持ポリシー](/dbms/operations-configuration-recovery/policy-data-retention/)
- [運用と設定](/dbms/operations-configuration-recovery/)
