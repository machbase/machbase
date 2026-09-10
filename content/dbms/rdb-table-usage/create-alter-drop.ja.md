---
type: docs
title: '8.3 作成、変更、削除'
weight: 30
toc: true
---

スキーマ変更では、コマンドの成否と同じくらい、既存データと取り込みプログラムの状態が重要です。
名前を変更した後に古いSQLを実行したり、インデックスが参照する列を先に削除したりするとエラーになります。
この節ではサンプルを入力した状態で、変更前後を確認します。

<a id="create-rdb-table"></a>

<a id="테이블을-만들고-한-행을-준비합니다"></a>

## テーブルの作成

```sql
CREATE TRANSACTION TABLE ch8_ddl (
    id   LONG,
    code VARCHAR(32),
    qty  INTEGER
);
INSERT INTO ch8_ddl VALUES (1, 'P-01', 10);
```

<a id="create-rdb-primary-key-index"></a>

<a id="기존-데이터에-키와-인덱스를-추가합니다"></a>

## キーとインデックスの作成

```sql
CREATE PRIMARY KEY INDEX ch8_ddl_pk ON ch8_ddl(id);
CREATE UNIQUE INDEX ch8_ddl_code ON ch8_ddl(code);
CREATE INDEX ch8_ddl_qty ON ch8_ddl(qty);
SHOW INDEX ch8_ddl_code;
```

idは単一のPRIMARY KEY、codeは別の業務キーです。
既存データに重複やPRIMARY KEYのNULLがある場合は、作成に失敗することがあります。
複合的な一意性はCREATE UNIQUE INDEXで設定します。CREATE TABLE内のUNIQUE制約構文は未サポートです。

<a id="create-rdb-auto-increment"></a>

自動採番が必要な場合は、作成時に`LONG PRIMARY KEY AUTO_INCREMENT`を指定します。
この節のidは直接入力した値で、自動採番列ではありません。
2つの作成方式を同じオブジェクトに重複して実行しないでください。
[AUTO_INCREMENT](/dbms/reference/sql/syntax/auto-increment-syntax/)に別の実習があります。

<a id="alter-rdb-table"></a>

<a id="새-컬럼이-기존-행에-어떻게-보이는지-확인합니다"></a>

## 列の追加とデフォルト値

```sql
ALTER TABLE ch8_ddl ADD COLUMN (label VARCHAR(64));
ALTER TABLE ch8_ddl ADD COLUMN (status VARCHAR(16) DEFAULT 'NEW');
ALTER TABLE ch8_ddl ADD COLUMN (limits DECIMAL(12)[2] DEFAULT [10, 20]);

SELECT id, label, status, limits FROM ch8_ddl ORDER BY id;
```

行1のlabelはNULL、statusはNEW、limitsは[10, 20]です。
DEFAULTのないARRAY列を追加すると、既存行では配列全体がNULLになります。

`ADD COLUMN`の`DEFAULT`と`CREATE TABLE`の`DEFAULT`は許可範囲が異なります。
上記のように`ADD COLUMN`では型に合う値を指定できますが、`CREATE TABLE`の列定義では、
`DATETIME`列の`DEFAULT SYSDATE`だけを使用できます。
他の型や値を指定すると、それぞれ`ERR-02346`、`ERR-02347`で拒否されます。
作成時にデフォルト値が必要なら、先に列を作成してから`ADD COLUMN`で追加するか、入力文で値を指定してください。
配列内の一部の要素がNULLの場合とは区別してください。

列定義は括弧で囲みます。他のDBMSのALTER TABLE形式と混同しないでください。
TRANSACTIONはMODIFY COLUMNによる長さ・型の変更をサポートしていません。
必要なら、新しいスキーマへの移行手順を別途用意してください。

<a id="인덱스와-의존-객체를-먼저-정리합니다"></a>

## 列の変更と依存オブジェクト

```sql
DROP INDEX ch8_ddl_qty;
ALTER TABLE ch8_ddl DROP COLUMN (qty);
ALTER TABLE ch8_ddl DROP COLUMN (label);
ALTER TABLE ch8_ddl DROP COLUMN (limits);
ALTER TABLE ch8_ddl RENAME COLUMN code TO product_code;

SELECT id, product_code, status FROM ch8_ddl;
SHOW INDEX ch8_ddl_code;
```

既存の行1のP-01・NEWという値と業務キーのインデックスは保持されます。
PRIMARY KEY・UNIQUE・一般・JSONパスインデックスが参照する列では、該当するインデックスを先に確認する必要があります。
最後のユーザー列は削除できません。

VIEWがテーブルや列を参照している場合、関連する名前変更・削除が拒否される場合があります。
VIEWだけでなくアプリケーションSQLとプリペアドステートメントも変更の影響を受けます。
DDL後に既存のプリペアドステートメントを無条件に再使用せず、再準備の必要性を確認してください。

```sql
ALTER TABLE ch8_ddl RENAME TO ch8_product;
SELECT id, product_code, status FROM ch8_product;
```

テーブル名の変更後は、ch8_productで検索します。

<a id="drop-rdb-table"></a>

<a id="전체-삭제와-정의-삭제를-구분합니다"></a>

## 全件削除とテーブル削除

```sql
BEGIN;
TRUNCATE TABLE ch8_product;
SELECT COUNT(*) AS during_delete FROM ch8_product;
ROLLBACK;
SELECT COUNT(*) AS after_rollback FROM ch8_product;
DROP TABLE ch8_product;
```

件数はそれぞれ0と1です。現在のTRANSACTIONのTRUNCATEは全行削除として処理され、明示的なトランザクション内でロールバックできます。
この動作をLOG・TAGのTRUNCATEに拡大して適用しないでください。
最後のDROPは、データ・定義・関連インデックスを削除します。

<a id="rdb-ddl-operation-notes"></a>

<a id="ddl은-업무-트랜잭션-밖에서-수행하세요"></a>

## DDL運用上の注意事項

上記のTRUNCATEの動作と、CREATE・ALTER・DROPなどのスキーマ操作を区別する必要があります。
スキーマ変更をBEGIN内に置けば後でROLLBACKできるとは考えないでください。
同じテーブルのアクティブなトランザクションや開いているカーソルはDDLを妨げる場合があるため、先に結果セットと業務トランザクションを終了します。

ADD・DROP COLUMNはカタログと別の保存ファイルを併せて変更します。
処理中にサーバーが停止した場合は、再起動時の復旧が完了する前に同じDDLを繰り返さないでください。
復旧後にDESC、代表的なSELECT・INSERT、インデックス・VIEWを確認し、サーバーログも点検します。
内部保存ファイルを直接移動・変更・削除して復旧しようとしないでください。

予想と異なるスキーマが表示される場合は、変更前のDDL、実行順序、最初のエラーを併せて確認してください。
最後のエラーだけを見るより原因を特定しやすくなります。
