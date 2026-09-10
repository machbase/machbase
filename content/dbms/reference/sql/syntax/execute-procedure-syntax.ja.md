---
type: docs
title: 'EXECプロシージャとROLLUPGAP'
weight: 240
toc: true
---

Machbaseが公開するテーブル・ROLLUP制御プロシージャと、machsqlの状態確認コマンドを説明します。

## 共通のEXEC形式

```text
execute_procedure_stmt ::=
    'EXEC' procedure_name [ '(' argument_list ')' ]
```

プロシージャごとの引数の数は固定です。
名前がない場合、引数の数・型が異なる場合、対象オブジェクトが存在しない場合はエラーを返します。

<a id="table-flush"></a>

## TABLE_FLUSH

```sql
EXEC TABLE_FLUSH(table_name);
```

| 項目 | 仕様 |
|---|---|
| 引数 | テーブル名1つ |
| Edition | Standard、Cluster |
| 動作 | テーブルの保留中のストレージ・入力バッファを明示的にflush |
| 戻り値 | ResultSetなしで文の成功またはエラーを返す |
| エラー | テーブルなし、アクセス不可、flush処理失敗 |

検証や運用で明示的なストレージのflushが必要な場合に使用します。
トランザクションのコミットやクエリの可視性を保証する手段ではありません。
入力行ごとに呼ぶとflushコストが増えるため、繰り返し呼び出さないでください。

<a id="index-flush"></a>

## INDEX_FLUSH

```sql
EXEC INDEX_FLUSH(table_name);
EXEC INDEX_FLUSH(table_name, index_name);
```

テーブル名だけを指定すると、そのテーブルのすべてのインデックス構築が終わるまで待機します。
インデックス名も指定すると、そのインデックスだけを対象にします。
指定したインデックスがそのテーブルに属さない場合はエラーです。ResultSetは返しません。

<a id="table-refresh"></a>

## TABLE_REFRESH

```sql
EXEC TABLE_REFRESH(lookup_table_name);
```

| 項目 | 仕様 |
|---|---|
| 引数 | LOOKUPテーブル名1つ |
| Edition | Standard、Cluster |
| 動作 | 永続LOOKUPの内容を実行時メモリテーブルに再反映 |
| 名前の範囲 | 現在のデータベースのテーブル。`owner.table`を許可 |
| 権限 | テーブル所有者または許可された管理ユーザー |
| 書き込み制限 | READ ONLYデータベースでは実行不可 |
| 戻り値 | ResultSetなしで文の成功またはエラーを返す |
| エラー | LOOKUP以外のテーブル、テーブルなし、書き込み許可判定の失敗 |

実行前に進行中のLOOKUP変更とクエリへの影響を確認し、完了後に行数と代表的なキーを再検索します。

<a id="freeze-tag-index"></a>

## FREEZE_TAG_INDEXとUNFREEZE_TAG_INDEX

```sql
EXEC FREEZE_TAG_INDEX(tag_table_name);
EXEC UNFREEZE_TAG_INDEX(tag_table_name);
```

TAGテーブルのタグインデックスを凍結・解除する1引数のプロシージャです。TAG以外のテーブルには使用できません。
インデックス保守の境界を直接制御する運用コマンドのため、通常の取り込み処理で常用せず、
失敗時は必ず`UNFREEZE_TAG_INDEX`の実行を確認してください。
両方ともResultSetなしで文の成功またはエラーを返します。

<a id="rollup-start-stop"></a>

## ROLLUP_STARTとROLLUP_STOP

```sql
EXEC ROLLUP_START;
EXEC ROLLUP_START(rollup_name);

EXEC ROLLUP_STOP;
EXEC ROLLUP_STOP(rollup_name);
```

両方のプロシージャは、0引数とROLLUP名1引数の形式に対応します。
名前を指定するとそのROLLUP、省略すると現在のユーザー範囲のROLLUPを制御します。
SYSの引数なし実行は全ユーザー範囲に適用される場合があるため、対象確認と変更承認が必要です。

存在しないROLLUP、開始済みの対象へのSTART、停止済みの対象へのSTOPはエラーです。
`V$ROLLUP.RUN_STATE`で変更結果を確認します。

<a id="rollup-force"></a>

## ROLLUP_FORCE

```sql
EXEC ROLLUP_FORCE;
EXEC ROLLUP_FORCE(rollup_name);
```

0引数形式は、現在のユーザー範囲の基本SEC→MIN→HOUR階層を処理します。
名前を指定すると、そのROLLUPソースの現在のEND_RIDに追いつくまで待機する同期処理です。
停止したROLLUPは、先にSTART状態であることを確認します。

完了後は`V$ROLLUP`と`SHOW ROLLUPGAP`で、関連するすべてのソース段階のgapを確認します。

<a id="rollup-rebuild"></a>

## ROLLUP_REBUILD

タグと時間範囲を受け取る、4引数のStandard専用プロシージャです。
詳細仕様の正本は[ROLLUP_REBUILD](../rollup-rebuild-syntax/)です。

<a id="show-rollupgap"></a>

## SHOW ROLLUPGAP

```sql
SHOW ROLLUPGAP;
```

`SHOW ROLLUPGAP`はサーバーSQLではなく、**machsql専用のクライアントコマンド**です。
JDBC、ODBC、SDKの通常のSQL実行APIに同じ文字列を送信しないでください。

Standardの出力には、ソース・ROLLUPテーブル、ソースEND_RID、ROLLUP END_RID、`GAP`、状態、起動時刻が含まれます。
Clusterの出力には`HOSTNAME`が加わり、ノード別の状態を表示します。
`GAP = SRC_END_RID - ROLLUP_END_RID`であり、階層内のすべてのソース→ROLLUP行が0であることを確認して初めて、階層全体が追いついたと判断できます。

## 関連文書

- [ROLLUPの運用と状態](/dbms/tag-rollup-usage/ingestion-control-rollup/)
- [V$ROLLUPリファレンス](/dbms/reference/system-catalog/vrollup/)
- [machsqlコマンド](/dbms/reference/command-line-tools/machsql/)
