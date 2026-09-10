---
type: docs
title: '11.4 Machbase SQLCLIとODBC'
weight: 40
toc: true
aliases:
  - /dbms/reference/sdk-api/cli-odbc/
---

<a id="machbase-sqlcli"></a>
<a id="odbc"></a>

Machbase SQLCLIはC/C++アプリケーションで使用する呼び出しレベルインターフェース（Call-Level
Interface）です。ODBCドライバーは標準ODBCアプリケーションで使用します。両者は環境・接続・文の
ハンドルを使用する実行フローを共有し、SQLCLIには高速Append用の拡張関数が追加されています。

## 選択基準

| 要件 | インターフェース |
|----------|------------|
| MachbaseインストールパッケージとともにC/C++アプリケーションを開発 | SQLCLI |
| 汎用ODBCツールまたはドライバーマネージャーを使用 | ODBC |
| Append拡張APIによる大量入力 | SQLCLI |
| 標準SQLの実行と結果の取得 | SQLCLIまたはODBC |

## ヘッダーとライブラリ

インストールディレクトリで次のファイルを確認します。

```bash
test -f "$MACHBASE_HOME/include/machbase_sqlcli.h"
test -f "$MACHBASE_HOME/lib/libmachbasecli_dll.so"
```

Linuxでの動的リンクの例です。

```bash
gcc cli_quickstart.c   -I"$MACHBASE_HOME/include"   -L"$MACHBASE_HOME/lib"   -lmachbasecli_dll   -o cli_quickstart

LD_LIBRARY_PATH="$MACHBASE_HOME/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"   MACHBASE_PASSWORD='your-password' ./cli_quickstart
```

本番ビルドは、インストールパッケージの`install/machbase_env.mk`とプラットフォーム別の
リンカー設定に基づいて構成します。

## 接続文字列

SQLCLIの基本的な接続文字列は次のキーを使用します。

```text
SERVER=127.0.0.1;PORT_NO=5656;UID=APP_USER;PWD=secret;CONNTYPE=1
```

ODBCデータソースを使用する場合はDSN、アカウント、パスワードを指定します。

```text
DSN=MACHBASE;UID=APP_USER;PWD=secret
```

マルチデータベースの初期値をサポートするドライバーでは`DATABASE`または`DBNAME`を使用できます。
実際に配布されたドライバーのサポート状況を確認し、接続後に`SELECT CURRENT_DATABASE()`で
選択結果を検証します。

## クイックスタート

次のプログラムは5656ポートに接続してシステムテーブルのクエリを実行し、全ハンドルを解放します。
パスワードは環境変数で渡します。

```c
#include <stdio.h>
#include <stdlib.h>
#include <machbase_sqlcli.h>

int main(void)
{
    SQLHENV env = SQL_NULL_HENV;
    SQLHDBC dbc = SQL_NULL_HDBC;
    SQLHSTMT stmt = SQL_NULL_HSTMT;
    char conn[512];
    const char *password = getenv("MACHBASE_PASSWORD");

    if (password == NULL) {
        fputs("MACHBASE_PASSWORD is required\n", stderr);
        return 2;
    }

    snprintf(conn, sizeof(conn),
        "SERVER=127.0.0.1;PORT_NO=5656;"
        "UID=SYS;PWD=%s;CONNTYPE=1", password);

    if (SQLAllocEnv(&env) != SQL_SUCCESS) {
        return 3;
    }
    if (SQLAllocConnect(env, &dbc) != SQL_SUCCESS) {
        SQLFreeEnv(env);
        return 4;
    }
    if (SQLDriverConnect(
            dbc, NULL, (SQLCHAR *)conn, SQL_NTS,
            NULL, 0, NULL, SQL_DRIVER_NOPROMPT) != SQL_SUCCESS) {
        SQLFreeConnect(dbc);
        SQLFreeEnv(env);
        return 5;
    }
    if (SQLAllocStmt(dbc, &stmt) != SQL_SUCCESS) {
        SQLDisconnect(dbc);
        SQLFreeConnect(dbc);
        SQLFreeEnv(env);
        return 6;
    }
    if (SQLExecDirect(
            stmt, (SQLCHAR *)"SELECT COUNT(*) FROM V$TABLES",
            SQL_NTS) != SQL_SUCCESS) {
        SQLFreeStmt(stmt, SQL_DROP);
        SQLDisconnect(dbc);
        SQLFreeConnect(dbc);
        SQLFreeEnv(env);
        return 7;
    }

    puts("query succeeded");
    SQLFreeStmt(stmt, SQL_DROP);
    SQLDisconnect(dbc);
    SQLFreeConnect(dbc);
    SQLFreeEnv(env);
    return 0;
}
```

失敗原因を出力する必要があるアプリケーションは、`SQLGetDiagRec()`または既存コードの
`SQLError()`でSQLSTATE、ネイティブエラーコード、メッセージを読み取ります。

## 標準的な実行フロー

1. 環境ハンドルと接続ハンドルを割り当てます。
2. `SQLDriverConnect()`または`SQLConnect()`で接続します。
3. 文ハンドルを割り当てます。
4. `SQLPrepare()`と`SQLExecute()`、または`SQLExecDirect()`でSQLを実行します。
5. SELECT結果は`SQLBindCol()`と`SQLFetch()`で読み取ります。
6. 文、接続、環境の順にリソースを解放します。

入力値は文字列として連結せず、`SQLBindParameter()`でバインドします。NULL許容性は
`SQLDescribeCol()`の最後の引数、または`SQLColAttribute(..., SQL_DESC_NULLABLE, ...)`で確認します。

## Named Bind Parameter

サーバーとドライバーが名前付きパラメーターをサポートする場合、`:name`プレースホルダーを使用し、
`SQLBindParameterByName()`でバインドできます。同じ名前が複数回現れると1つの値が全位置に適用されます。
共通の制約と例は
[Named Bind Parameter](/dbms/reference/sql/syntax/named-bind-parameter-syntax/)を参照してください。

サポートを確認できない環境では、標準の`?`プレースホルダーと`SQLBindParameter()`を使用します。

## INSERT結果のROWID

Standard Editionで単一の`INSERT ... VALUES`が成功した後、生成されたROWIDが必要な場合は
次の方法を使用します。

- SQLCLI拡張: `SQLGetGeneratedRowID()`
- 標準ODBC: 生成ROWID専用の標準APIなし

バッチ、Append、`INSERT ... SELECT`、UPSERTで同じ戻り値を想定しないでください。詳細な範囲は
[ROWIDとINSERT結果ID](/dbms/reference/sql/rowid/)を参照してください。

## Append拡張API

高速入力は通常の文と分けたAppendフローを使用します。

| 段階 | 主な関数 |
|------|-----------|
| オープン | `SQLAppendOpen()`、選択列は`SQLAppendOpenColumns()`/`W()` |
| 1行の入力 | `SQLAppendDataV2()`または対応バージョンのAppend関数 |
| バッチ入力 | `SQLAppendBatch()` |
| サーバーへの反映 | `SQLAppendFlush()` |
| エラーコールバック | `SQLAppendSetErrorCallback()` |
| クローズ | `SQLAppendClose()` |

Append行の列順序と型は、対象テーブルのスキーマと完全に一致する必要があります。文字列、バイナリ、
IP、DATETIME、NULLの表現は、インストール済み`machbase_sqlcli.h`の`SQL_APPEND_PARAM`定義に
基づいて記述します。エラーコールバックでは失敗行とサーバーエラーを記録しますが、パスワードや機密の
生データはログに残しません。

有効なAppendハンドルがある接続は通常のクエリと共有せず、close結果の成功・失敗件数を確認します。

## マルチスレッドとリソース管理

- スレッドごとに接続と文を分けます。
- 1つの文またはAppendハンドルを複数スレッドで同時に使用しません。
- すべてのエラー経路でもハンドルを逆順に解放するよう、後処理関数を用意します。
- 再試行前に、前の接続とAppendの状態が完全に閉じているか確認します。
- 大量入力では成功件数と失敗件数の両方を記録します。

## API詳細の確認

関数プロトタイプ、定数、構造体は、インストール済みの
`$MACHBASE_HOME/include/machbase_sqlcli.h`が該当ライブラリと一致する基準です。
サンプルを別バージョンのヘッダーと混用せず、コンパイル・リンク・5656接続のテストを
デプロイパイプラインに含めます。

## DECIMAL Append

`SQLAppendDataV2()`と`SQLAppendBatch()`で`DECIMAL`または`NUMERIC`値を入力する際は、
32バイトの不透明型`SQL_APPEND_NUMERIC`と公開生成関数を使用します。
アプリケーションで内部バイトを直接作成・変更しません。

| 入力 | 関数 |
|---|---|
| UTF-8の数値文字列 | `SQLAppendNumericFromString()` |
| 符号付き・符号なし整数 | `SQLAppendNumericFromInt64()`、`SQLAppendNumericFromUInt64()` |
| `SQL_NUMERIC_STRUCT` | `SQLAppendNumericFromSQLNumeric()` |
| NULL | `SQLAppendNumericSetNull()` |

正確な値を保持するには、文字列または`SQL_NUMERIC_STRUCT`を優先します。型配列には
`SQL_APPEND_TYPE_NUMERIC`または`SQL_APPEND_TYPE_DECIMAL`を指定し、対象列の精度とスケールに
基づいてオーバーフローと丸めを確認してください。

## ARRAYと選択列Append

Machbase DBMS 8.7.0は、`SQL_MACHBASE_ARRAY_DESC`による型付きARRAYの検索・バインドと、
`SQL_MACHBASE_SPARSE_ARRAY_DESC`によるスパース入力をサポートします。通常のOpenでもARRAY列に
スパースディスクリプターを渡せます。

```c
SQLAppendOpen(statement, (SQLCHAR *)"ARRAY_APPEND_FULL_EXAMPLE", 0);
row[0].mLong = 1;
row[1].mVar.mData = &sparse;
row[1].mVar.mLength = SQL_APPEND_SPARSE_ARRAY_DESC_LENGTH;
SQLAppendDataV3(statement, row, 2);
SQLAppendClose(statement, &success, &failure);
```

上記コードは`ID LONG, A INT32[4]`テーブルの入力順序に従います。接続・ディスクリプター・バッファの
準備とエラー処理を含む[通常Openの全体例](../data-input-load-export/array-append/#c-full-open)を
先に確認してください。旧式の`SQLAppendData(void *[])`にディスクリプターを渡す方式とは異なります。

一部の列または固定ARRAY要素だけを選択する場合は、`SQLAppendOpenColumns()`または
`SQLAppendOpenColumnsW()`を使用します。

```c
SQLCHAR *targets[] = {
    (SQLCHAR *)"ID",
    (SQLCHAR *)"CHANNELS[0]",
    (SQLCHAR *)"CHANNELS[3]",
    NULL
};

SQLAppendOpenColumns(statement, (SQLCHAR *)"SENSOR_ARRAY", targets, 0);
```

ARRAY要素の対象とスパースディスクリプターの位置は0始まりのインデックスです。列名リストの最後の要素は
`NULL`である必要があります。`SQLAppendBatch()`はARRAYをサポートしません。
ディスクリプター定義、配列全体のNULLと要素NULLの処理、直接ODBCハンドルの制約は
[Sparse ARRAYと選択列Append API](../data-input-load-export/array-append/)を参照してください。
