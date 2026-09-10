---
type: docs
title: '11.10.1 Sparse ARRAYと選択列Append API'
weight: 10
toc: true
---

Machbase DBMS 8.7.0では、固定長`ARRAY`の一部の位置だけを入力できます。入力位置が行ごとに異なる
場合はスパースARRAYを使用し、複数のAppend行で同じ位置を入力する場合はAppend Open時に選択列を
指定します。

スパースARRAYは**1つの列に入れる値の表現方法**であり、選択列は**1行で入力する列や要素を選ぶ方法**です。
通常のOpenで全行を入力する場合も、ARRAY列にスパースオブジェクトを渡せます。Node.jsは
`appendOpen()`の列定義引数が必須のため、全列を列挙して同じ入力を行います。

`ARRAY`型の宣言、通常の入力、検索、SDK別の密なARRAY処理は
[数値ARRAY型](/dbms/reference/sql/types/array/)を参照してください。

## 入力方式の選択

| 要件 | 推奨方式 |
|---|---|
| SQLの1行で値のある位置だけを指定 | `ARRAY_SPARSE(position => value, ...)` |
| 複数のAppend行が常に同じ位置を入力 | Append Openの`A[0]`、`A[3]`対象 |
| 通常Openで全行を入力し、ARRAY位置が変わる | 全行のARRAY値にSDKのスパースオブジェクトを渡す |
| 一部の列のみ入力し、ARRAY位置も変わる | 選択リストの全体`A`対象とSDKのスパースオブジェクト |
| 全要素がNULLで、配列自体は非NULLのARRAY | 空のスパースオブジェクト |
| ARRAY自体がNULL | SQLの`NULL`またはSDKの配列全体NULL値 |

位置はSQLとすべてのMachbase専用SDK APIで0から始まります。

## SQLのスパース入力

### ARRAY_SPARSE

対象列があるINSERTまたはUPDATEの文脈では、位置と値だけを指定します。

```sql
CREATE LOG TABLE ARRAY_APPEND_EXAMPLE
(
    ID LONG,
    A  INT32[4]
);

INSERT INTO ARRAY_APPEND_EXAMPLE (ID, A)
VALUES (1, ARRAY_SPARSE(0 => 10, 3 => 40));
```

SELECTのように対象型を推論できない文脈では、要素型と要素数を先に指定します。

```sql
SELECT ARRAY_SPARSE(INT32[4], 0 => 10, 3 => 40);
SELECT ARRAY_SPARSE(DECIMAL(12,4)[4], 1 => 1.2500);
```

- 位置は`0..cardinality-1`の範囲の整数リテラルである必要があります。
- ペアの順序は任意ですが、同じ位置を重複指定できません。
- 省略した位置と`position => NULL`は要素NULLになります。
- `ARRAY_SPARSE()`または`ARRAY_SPARSE(INT32[4])`は、全要素がNULLのARRAYです。
- 配列全体のNULLは`ARRAY_SPARSE()`ではなくSQLの`NULL`で入力します。
- 不正な位置や要素変換は文全体を失敗させます。

### スパースの直接短縮表記

`ARRAY_SPARSE`ラッパーなしで、角括弧内に位置と値のペアを直接記述できます。

```sql
INSERT INTO ARRAY_APPEND_EXAMPLE (ID, A)
VALUES (2, [0 => 10, 3 => 40]);

SELECT [1 => 12, 33 => 23];
```

対象ARRAYがある場合は、その型と要素数を使用します。単独の式では密なARRAYと同じ数値の共通型を推論し、
要素数を`最大のposition + 1`で決定します。そのため2番目の例は`INT32[34]`です。

単独の全NULLスパース式は要素型を判定できないためエラーです。この場合は
`ARRAY_SPARSE(TYPE[N], ...)`形式を使用します。`[]`は従来の密な空コンストラクターとして維持され、
`ARRAY[0 => 1]`はサポートしません。

### INSERT対象への位置指定

複数行が同じ位置を入力する場合は、列リストに要素対象を直接指定します。

```sql
INSERT INTO ARRAY_APPEND_EXAMPLE (ID, A[0], A[3])
VALUES (2, 10, 40);

-- Aは存在しますが全要素がNULLです。
INSERT INTO ARRAY_APPEND_EXAMPLE (ID, A[0], A[3])
VALUES (3, NULL, NULL);

-- A自体がNULLです。
INSERT INTO ARRAY_APPEND_EXAMPLE (ID)
VALUES (4);
```

同じ文で`A`と`A[0]`を併記したり、同じ要素を2回指定したりすることはできません。
スカラー列や範囲外の位置を要素対象にするとエラーです。

要素位置を指定した対象は`INSERT ... VALUES`とAppendの選択対象でサポートします。
`INSERT ... SELECT`と`UPDATE ... SET A[0] = ...`ではサポートしません。

## Appendの共通規則

### 全行入力と選択入力

通常Openはテーブルの入力列順序を使用し、選択Openは指定した対象リストの順序を使用します。
以下の実習の通常Openでは`ID`、`A`の順に2つの値を渡し、`_arrival_time`値は別途入れません。
この例の各APIがLOGの自動時刻を処理します。受信時刻を明示する場合は、該当SDKの時刻指定APIを使用します。

Node.jsは通常Openと選択Openが別メソッドに分かれていません。全体入力にも`name`と`type`のある
列定義が必要で、この実習では`ID`と`A`をテーブル順に列挙します。
`appendOpen(table)`だけを呼び出す方式や、空の列リストを渡す方式はサポートしません。

### 実習の準備と再実行

通常の例と選択の例を分けて実行できるよう、別々のテーブルを使用します。
各例を実行する前に、接続先データベースで次の準備SQLを実行します。

```sql
CREATE LOG TABLE ARRAY_APPEND_FULL_EXAMPLE (ID LONG, A INT32[4]);
```

通常の例のファイル名には`full`を付けます。選択の例は前に作成した`ARRAY_APPEND_EXAMPLE`を使用します。
Cの選択例はこのテーブルを直接再作成するため、実習専用の名前であることを確認してください。
他SDKの選択例でも同じ構造の空の`ARRAY_APPEND_EXAMPLE`を準備します。

各SDKの例は**独立して実行**します。異なるSDKを同じテーブルに連続して実行するとIDが重複します。
再実行時は結果を確認して[実習の後片付け](#sparse-append-cleanup)を行い、該当テーブルを再作成します。
サーバーアドレス・ポート・アカウントは実際の実習環境に合わせます。

### 共通の結果

どちらの入力方式も次の4行を作成します。通常の例はID=1もスパースオブジェクトで入力し、
選択の例はID=1に固定要素対象を使用します。

```text
ID=1  A=[10,null,null,40]       スパースオブジェクトまたは固定要素対象
ID=2  A=[null,200,null,400]     ARRAY列にスパースオブジェクト
ID=3  A=[null,null,null,null]   空のスパースオブジェクト
ID=4  A=NULL                    全体NULL
```

スパースオブジェクトで省略したARRAY要素は要素NULLになります。`entry_count == 0`や空の
スパースオブジェクトは、長さ0の配列ではなく、宣言された長さのすべての要素がNULLの配列です。
全体NULLは配列値自体がないことを意味し、`ARRAY_LENGTH`の結果もNULLです。

### 選択Openの規則

次の規則は**選択Openの対象リスト**に適用されます。通常Openで列引数を省略することと
「空の選択リスト」を混同しないでください。

選択リストにない通常の列は既存のAppend規則に従って処理されます。

- NULL許容列はNULLを使用します。
- DEFAULTがある列はDEFAULTを使用します。
- 値が必須の列が欠けると、Append Openまたは行入力が失敗します。

選択対象リストは空にできず、大文字・小文字を無視して重複してはいけません。
ARRAY全体の対象と、同じARRAYの要素対象を同時に開くことはできません。
Append Open後は、各行の値の数と順序が対象リストと完全に一致する必要があります。

行入力中にエラーが発生しても開いたAppendハンドルは閉じる必要があります。
Append Open自体が失敗した場合はSDKが内部状態を解放するため、同じ接続を再使用できます。

## C SQLCLI

ARRAYの入力と検索には次の公開型を使用します。

| 型または定数 | 用途 |
|---|---|
| `SQL_MACHBASE_ARRAY` | SQL ARRAY型の識別 |
| `SQL_C_MACHBASE_ARRAY` | 密なARRAYの検索・バインド用ディスクリプター |
| `SQL_C_MACHBASE_SPARSE_ARRAY` | preparedのスパースARRAY入力 |
| `SQL_APPEND_SPARSE_ARRAY_DESC_LENGTH` | Appendスパースディスクリプターの識別 |

<a id="c-full-open"></a>

### 通常OpenでスパースARRAYを入力

`SQLAppendOpen()`で開き、`SQL_APPEND_PARAM`配列に`ID`と`A`を渡します。
`A`の`mVar.mData`には`SQL_MACHBASE_SPARSE_ARRAY_DESC`のアドレス、`mVar.mLength`には
`SQL_APPEND_SPARSE_ARRAY_DESC_LENGTH`を指定します。列選択は行わず、値の数を明示する
`SQLAppendDataV3(..., row, 2)`を使用します。
旧式の`SQLAppendData(void *[])`にこのディスクリプターをそのまま渡す例ではありません。

前の準備SQLで作成した空の`ARRAY_APPEND_FULL_EXAMPLE`を使用します。ディスクリプターと位置・値・
インジケーターバッファはAppend呼び出しが終わるまで有効である必要があります。同じ開いたハンドルで
1行目と2行目の入力位置を変え、空のスパース配列と全体NULLも入力します。

```c
/* sparse_append_full.c */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <machbase_sqlcli.h>

static int ok(SQLRETURN rc)
{
    return rc == SQL_SUCCESS || rc == SQL_SUCCESS_WITH_INFO;
}

static void fail(SQLHENV env, SQLHDBC dbc, SQLHSTMT stmt, const char *where)
{
    SQLCHAR state[6] = {0};
    SQLCHAR message[1024] = {0};
    SQLINTEGER native = 0;
    SQLSMALLINT length = 0;
    SQLError(env, dbc, stmt, state, &native, message,
             (SQLSMALLINT)sizeof(message), &length);
    fprintf(stderr, "%s: %s %d %s\n", where, state, (int)native, message);
    exit(EXIT_FAILURE);
}

int main(void)
{
    SQLHENV env = SQL_NULL_HENV;
    SQLHDBC dbc = SQL_NULL_HDBC;
    SQLHSTMT sql = SQL_NULL_HSTMT;
    SQLHSTMT append = SQL_NULL_HSTMT;
    SQLCHAR conn[] =
        "SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD=MANAGER;CONNTYPE=1";
    SQL_APPEND_PARAM row[2];
    SQLUSMALLINT positions[2] = {0, 3};
    SQLINTEGER values[2] = {10, 40};
    SQLLEN indicators[2] = {0, 0};
    SQL_MACHBASE_SPARSE_ARRAY_DESC sparse;
    SQLBIGINT success = 0;
    SQLBIGINT failure = 0;
    SQLINTEGER id;
    SQLLEN idInd;
    SQLLEN textInd;
    SQLCHAR text[128];

    if (!ok(SQLAllocEnv(&env)) || !ok(SQLAllocConnect(env, &dbc)) ||
        !ok(SQLDriverConnect(dbc, NULL, conn, SQL_NTS, NULL, 0, NULL,
                             SQL_DRIVER_NOPROMPT)) ||
        !ok(SQLAllocStmt(dbc, &sql)) || !ok(SQLAllocStmt(dbc, &append)))
        fail(env, dbc, SQL_NULL_HSTMT, "connect");

    memset(&sparse, 0, sizeof(sparse));
    sparse.struct_size = sizeof(sparse);
    sparse.element_c_type = SQL_C_SLONG;
    sparse.cardinality = 4;
    sparse.entry_count = 2;
    sparse.positions = positions;
    sparse.values = values;
    sparse.value_stride = sizeof(values[0]);
    sparse.element_indicators = indicators;

    memset(row, 0, sizeof(row));
    if (!ok(SQLAppendOpen(append,
            (SQLCHAR*)"ARRAY_APPEND_FULL_EXAMPLE", 0)))
        fail(env, dbc, append, "sparse open");

    row[0].mLong = 1;
    row[1].mVar.mData = &sparse;
    row[1].mVar.mLength = SQL_APPEND_SPARSE_ARRAY_DESC_LENGTH;
    if (!ok(SQLAppendDataV3(append, row, 2))) {
        SQLAppendClose(append, &success, &failure);
        fail(env, dbc, append, "first sparse row");
    }

    positions[0] = 1;
    values[0] = 200;
    values[1] = 400;
    row[0].mLong = 2;
    if (!ok(SQLAppendDataV3(append, row, 2))) {
        SQLAppendClose(append, &success, &failure);
        fail(env, dbc, append, "sparse row");
    }

    row[0].mLong = 3;
    sparse.entry_count = 0;
    if (!ok(SQLAppendDataV3(append, row, 2))) {
        SQLAppendClose(append, &success, &failure);
        fail(env, dbc, append, "empty sparse row");
    }

    row[0].mLong = 4;
    row[1].mVar.mData = NULL;
    row[1].mVar.mLength = 0;
    if (!ok(SQLAppendDataV3(append, row, 2))) {
        SQLAppendClose(append, &success, &failure);
        fail(env, dbc, append, "whole NULL row");
    }
    success = 0;
    failure = 0;
    if (!ok(SQLAppendClose(append, &success, &failure)) ||
        success != 4 || failure != 0)
        fail(env, dbc, append, "sparse close");

    if (!ok(SQLExecDirect(sql,
        (SQLCHAR*)"SELECT ID,A FROM ARRAY_APPEND_FULL_EXAMPLE ORDER BY ID", SQL_NTS)))
        fail(env, dbc, sql, "select");
    if (!ok(SQLBindCol(sql, 1, SQL_C_SLONG, &id, sizeof(id), &idInd)) ||
        !ok(SQLBindCol(sql, 2, SQL_C_CHAR, text, sizeof(text), &textInd)))
        fail(env, dbc, sql, "bind verify");
    for (;;) {
        SQLRETURN fetch = SQLFetch(sql);
        if (fetch == SQL_NO_DATA)
            break;
        if (!ok(fetch))
            fail(env, dbc, sql, "fetch verify");
        printf("%d %s\n", (int)id,
               textInd == SQL_NULL_DATA ? "NULL" : (char*)text);
    }

    SQLFreeStmt(append, SQL_DROP);
    SQLFreeStmt(sql, SQL_DROP);
    SQLDisconnect(dbc);
    SQLFreeConnect(dbc);
    SQLFreeEnv(env);
    return EXIT_SUCCESS;
}
```

```bash
cc -I"$MACHBASE_HOME/include" sparse_append_full.c \
  -L"$MACHBASE_HOME/lib" -lmachbasecli -lm -ldl -lrt -pthread \
  -o sparse_append_full
LD_LIBRARY_PATH="$MACHBASE_HOME/lib" ./sparse_append_full
```

プログラムはCloseの成功4件・失敗0件を確認し、検索したIDと配列を出力します。
詳細な期待値は[結果の確認](#結果の確認)と比較します。入力エラー時はAppendを閉じてからプロセスを
終了します。再試行前に、テーブルに実際に反映された行を確認します。

<a id="c-selected-open"></a>

### 選択列Openで入力

`SQLAppendOpenColumns()`とワイド文字版は、最後の要素が`NULL`の列名ポインター配列を受け取ります。
列数を指定する別の引数はありません。

```c
SQLRETURN SQL_API SQLAppendOpenColumns(
    SQLHSTMT     aStmtHandle,
    SQLCHAR     *aTableName,
    SQLCHAR    **aColumnNames,
    SQLINTEGER   aErrorCheckCount);

SQLRETURN SQL_API SQLAppendOpenColumnsW(
    SQLHSTMT     aStmtHandle,
    SQLWCHAR    *aTableName,
    SQLWCHAR   **aColumnNames,
    SQLINTEGER   aErrorCheckCount);
```

`aColumnNames == NULL`または最初の要素が`NULL`の場合はエラーです。Cポインターには配列長の情報が
ないため、呼び出し側は必ず最後の`NULL`まで有効な配列を渡す必要があります。終端の`NULL`を忘れると
配列境界外を読み取る可能性があるため、安全に診断されるとは考えないでください。

次の`sparse_append.c`はテーブルを作成して4行をAppendし、結果を出力します。

```c
/* sparse_append.c */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <machbase_sqlcli.h>

static int ok(SQLRETURN rc)
{
    return rc == SQL_SUCCESS || rc == SQL_SUCCESS_WITH_INFO;
}

static void fail(SQLHENV env, SQLHDBC dbc, SQLHSTMT stmt, const char *where)
{
    SQLCHAR state[6] = {0};
    SQLCHAR message[1024] = {0};
    SQLINTEGER native = 0;
    SQLSMALLINT length = 0;
    SQLError(env, dbc, stmt, state, &native, message,
             (SQLSMALLINT)sizeof(message), &length);
    fprintf(stderr, "%s: %s %d %s\n", where, state, (int)native, message);
    exit(EXIT_FAILURE);
}

int main(void)
{
    SQLHENV env = SQL_NULL_HENV;
    SQLHDBC dbc = SQL_NULL_HDBC;
    SQLHSTMT sql = SQL_NULL_HSTMT;
    SQLHSTMT append = SQL_NULL_HSTMT;
    SQLCHAR conn[] =
        "SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD=MANAGER;CONNTYPE=1";
    SQLCHAR *fixed[] = {(SQLCHAR*)"ID", (SQLCHAR*)"A[0]",
                        (SQLCHAR*)"A[3]", NULL};
    SQLCHAR *whole[] = {(SQLCHAR*)"ID", (SQLCHAR*)"A", NULL};
    SQL_APPEND_PARAM row[3];
    SQLUSMALLINT positions[2] = {1, 3};
    SQLINTEGER values[2] = {200, 400};
    SQLLEN indicators[2] = {0, 0};
    SQL_MACHBASE_SPARSE_ARRAY_DESC sparse;
    SQLBIGINT success = 0;
    SQLBIGINT failure = 0;
    SQLINTEGER id;
    SQLLEN idInd;
    SQLLEN textInd;
    SQLCHAR text[128];

    if (!ok(SQLAllocEnv(&env)) || !ok(SQLAllocConnect(env, &dbc)) ||
        !ok(SQLDriverConnect(dbc, NULL, conn, SQL_NTS, NULL, 0, NULL,
                             SQL_DRIVER_NOPROMPT)) ||
        !ok(SQLAllocStmt(dbc, &sql)) || !ok(SQLAllocStmt(dbc, &append)))
        fail(env, dbc, SQL_NULL_HSTMT, "connect");

    SQLExecDirect(sql, (SQLCHAR*)"DROP TABLE ARRAY_APPEND_EXAMPLE", SQL_NTS);
    if (!ok(SQLExecDirect(sql,
        (SQLCHAR*)"CREATE LOG TABLE ARRAY_APPEND_EXAMPLE(ID LONG,A INT32[4])",
        SQL_NTS)))
        fail(env, dbc, sql, "create");

    memset(row, 0, sizeof(row));
    row[0].mLong = 1;
    row[1].mInteger = 10;
    row[2].mInteger = 40;
    if (!ok(SQLAppendOpenColumns(append,
            (SQLCHAR*)"ARRAY_APPEND_EXAMPLE", fixed, 0)))
        fail(env, dbc, append, "fixed open");
    if (!ok(SQLAppendDataV3(append, row, 3))) {
        SQLAppendClose(append, &success, &failure);
        fail(env, dbc, append, "fixed row");
    }
    if (!ok(SQLAppendClose(append, &success, &failure)) ||
        success != 1 || failure != 0)
        fail(env, dbc, append, "fixed close");

    memset(&sparse, 0, sizeof(sparse));
    sparse.struct_size = sizeof(sparse);
    sparse.element_c_type = SQL_C_SLONG;
    sparse.cardinality = 4;
    sparse.entry_count = 2;
    sparse.positions = positions;
    sparse.values = values;
    sparse.value_stride = sizeof(values[0]);
    sparse.element_indicators = indicators;

    memset(row, 0, sizeof(row));
    if (!ok(SQLAppendOpenColumns(append,
            (SQLCHAR*)"ARRAY_APPEND_EXAMPLE", whole, 0)))
        fail(env, dbc, append, "sparse open");

    row[0].mLong = 2;
    row[1].mVar.mData = &sparse;
    row[1].mVar.mLength = SQL_APPEND_SPARSE_ARRAY_DESC_LENGTH;
    if (!ok(SQLAppendDataV3(append, row, 2))) {
        SQLAppendClose(append, &success, &failure);
        fail(env, dbc, append, "sparse row");
    }

    row[0].mLong = 3;
    sparse.entry_count = 0;
    if (!ok(SQLAppendDataV3(append, row, 2))) {
        SQLAppendClose(append, &success, &failure);
        fail(env, dbc, append, "empty sparse row");
    }

    row[0].mLong = 4;
    row[1].mVar.mData = NULL;
    row[1].mVar.mLength = 0;
    if (!ok(SQLAppendDataV3(append, row, 2))) {
        SQLAppendClose(append, &success, &failure);
        fail(env, dbc, append, "whole NULL row");
    }
    success = 0;
    failure = 0;
    if (!ok(SQLAppendClose(append, &success, &failure)) ||
        success != 3 || failure != 0)
        fail(env, dbc, append, "sparse close");

    if (!ok(SQLExecDirect(sql,
        (SQLCHAR*)"SELECT ID,A FROM ARRAY_APPEND_EXAMPLE ORDER BY ID", SQL_NTS)))
        fail(env, dbc, sql, "select");
    if (!ok(SQLBindCol(sql, 1, SQL_C_SLONG, &id, sizeof(id), &idInd)) ||
        !ok(SQLBindCol(sql, 2, SQL_C_CHAR, text, sizeof(text), &textInd)))
        fail(env, dbc, sql, "bind verify");
    for (;;) {
        SQLRETURN fetch = SQLFetch(sql);
        if (fetch == SQL_NO_DATA)
            break;
        if (!ok(fetch))
            fail(env, dbc, sql, "fetch verify");
        printf("%d %s\n", (int)id,
               textInd == SQL_NULL_DATA ? "NULL" : (char*)text);
    }

    SQLFreeStmt(append, SQL_DROP);
    SQLFreeStmt(sql, SQL_DROP);
    SQLDisconnect(dbc);
    SQLFreeConnect(dbc);
    SQLFreeEnv(env);
    return EXIT_SUCCESS;
}
```

次のようにビルドして実行します。

```bash
cc -I"$MACHBASE_HOME/include" sparse_append.c \
  -L"$MACHBASE_HOME/lib" -lmachbasecli -lm -ldl -lrt -pthread \
  -o sparse_append
LD_LIBRARY_PATH="$MACHBASE_HOME/lib" ./sparse_append
```

ディスクリプターの位置は0始まりです。ソートは不要ですが重複できません。
エントリーのインジケーターが`SQL_NULL_DATA`の場合、その位置は要素NULLです。
`entry_count == 0`は空のスパースARRAYで、配列全体のNULLは`mVar.mData = NULL`、
`mVar.mLength = 0`で指定します。

## C++ SQLCLI

<a id="cpp-full-open"></a>

### 通常OpenでスパースARRAYを入力

Cと同じディスクリプターと`SQLAppendOpen()`を使用します。位置・値バッファは`std::array`で保持し、
成功・例外の両経路でAppendを閉じます。通常の実習テーブルを先に準備します。

```cpp
/* sparse_append_full.cpp */
#include <array>
#include <iostream>
#include <stdexcept>
#include <machbase_sqlcli.h>

static bool ok(SQLRETURN rc) {
    return rc == SQL_SUCCESS || rc == SQL_SUCCESS_WITH_INFO;
}

struct Handles {
    SQLHENV env{SQL_NULL_HENV};
    SQLHDBC dbc{SQL_NULL_HDBC};
    SQLHSTMT stmt{SQL_NULL_HSTMT};
    ~Handles() {
        if (stmt != SQL_NULL_HSTMT) SQLFreeStmt(stmt, SQL_DROP);
        if (dbc != SQL_NULL_HDBC) { SQLDisconnect(dbc); SQLFreeConnect(dbc); }
        if (env != SQL_NULL_HENV) SQLFreeEnv(env);
    }
};

int main() {
    Handles h;
    SQLCHAR conn[] =
        "SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD=MANAGER;CONNTYPE=1";
    if (!ok(SQLAllocEnv(&h.env)) || !ok(SQLAllocConnect(h.env, &h.dbc)) ||
        !ok(SQLDriverConnect(h.dbc, nullptr, conn, SQL_NTS, nullptr, 0,
                             nullptr, SQL_DRIVER_NOPROMPT)) ||
        !ok(SQLAllocStmt(h.dbc, &h.stmt)))
        throw std::runtime_error("connect");

    std::array<SQLUSMALLINT, 2> positions{0, 3};
    std::array<SQLINTEGER, 2> values{10, 40};
    std::array<SQLLEN, 2> indicators{0, 0};
    SQL_MACHBASE_SPARSE_ARRAY_DESC sparse{};
    sparse.struct_size = sizeof(sparse);
    sparse.element_c_type = SQL_C_SLONG;
    sparse.cardinality = 4;
    sparse.entry_count = 2;
    sparse.positions = positions.data();
    sparse.values = values.data();
    sparse.value_stride = sizeof(values[0]);
    sparse.element_indicators = indicators.data();
    std::array<SQL_APPEND_PARAM, 2> row{};
    row[1].mVar.mData = &sparse;
    row[1].mVar.mLength = SQL_APPEND_SPARSE_ARRAY_DESC_LENGTH;

    SQLBIGINT success = 0, failure = 0;
    if (!ok(SQLAppendOpen(h.stmt, (SQLCHAR*)"ARRAY_APPEND_FULL_EXAMPLE", 0)))
        throw std::runtime_error("SQLAppendOpen");
    try {
        for (int id = 1; id <= 4; ++id) {
            row[0].mLong = id;
            if (id == 2) {
                positions[0] = 1;
                values[0] = 200;
                values[1] = 400;
            } else if (id == 3) {
                sparse.entry_count = 0;
            } else if (id == 4) {
                row[1].mVar.mData = nullptr;
                row[1].mVar.mLength = 0;
            }
            if (!ok(SQLAppendDataV3(h.stmt, row.data(), 2)))
                throw std::runtime_error("SQLAppendDataV3");
        }
    } catch (...) {
        SQLAppendClose(h.stmt, &success, &failure);
        throw;
    }
    if (!ok(SQLAppendClose(h.stmt, &success, &failure)) ||
        success != 4 || failure != 0)
        throw std::runtime_error("SQLAppendClose");

    if (!ok(SQLExecDirect(h.stmt,
        (SQLCHAR*)"SELECT ID,A FROM ARRAY_APPEND_FULL_EXAMPLE ORDER BY ID", SQL_NTS)))
        throw std::runtime_error("verify query");
    SQLINTEGER id{}; SQLLEN idInd{}, arrayInd{}; SQLCHAR value[128]{};
    if (!ok(SQLBindCol(h.stmt, 1, SQL_C_SLONG,
                       &id, sizeof(id), &idInd)) ||
        !ok(SQLBindCol(h.stmt, 2, SQL_C_CHAR,
                       value, sizeof(value), &arrayInd)))
        throw std::runtime_error("bind verify");
    for (;;) {
        SQLRETURN fetch = SQLFetch(h.stmt);
        if (fetch == SQL_NO_DATA) break;
        if (!ok(fetch)) throw std::runtime_error("fetch verify");
        std::cout << id << ' ' <<
            (arrayInd == SQL_NULL_DATA ? "NULL" : (char*)value) << '\n';
    }
}
```

```bash
c++ -std=c++11 -I"$MACHBASE_HOME/include" sparse_append_full.cpp \
  -L"$MACHBASE_HOME/lib" -lmachbasecli -lm -ldl -lrt -pthread \
  -o sparse_append_full_cpp
LD_LIBRARY_PATH="$MACHBASE_HOME/lib" ./sparse_append_full_cpp
```

### 選択列Openで入力

C++専用の転送オブジェクトを新設せず、SQLCLIディスクリプターを使用します。次の例はRAIIラッパーで
closeを保証し、C++コンテナーの存続中にディスクリプターを送信します。

```cpp
/* sparse_append.cpp */
#include <array>
#include <iostream>
#include <stdexcept>
#include <machbase_sqlcli.h>

static bool ok(SQLRETURN rc) {
    return rc == SQL_SUCCESS || rc == SQL_SUCCESS_WITH_INFO;
}

struct Handles {
    SQLHENV env{SQL_NULL_HENV};
    SQLHDBC dbc{SQL_NULL_HDBC};
    SQLHSTMT stmt{SQL_NULL_HSTMT};
    ~Handles() {
        if (stmt != SQL_NULL_HSTMT) SQLFreeStmt(stmt, SQL_DROP);
        if (dbc != SQL_NULL_HDBC) { SQLDisconnect(dbc); SQLFreeConnect(dbc); }
        if (env != SQL_NULL_HENV) SQLFreeEnv(env);
    }
};

static void append(Handles& h, SQLCHAR **columns,
                   SQL_APPEND_PARAM *row, SQLINTEGER count) {
    SQLBIGINT success = 0, failure = 0;
    if (!ok(SQLAppendOpenColumns(h.stmt,
            (SQLCHAR*)"ARRAY_APPEND_EXAMPLE", columns, 0)))
        throw std::runtime_error("SQLAppendOpenColumns");
    try {
        if (!ok(SQLAppendDataV3(h.stmt, row, count)))
            throw std::runtime_error("SQLAppendDataV3");
    } catch (...) {
        SQLAppendClose(h.stmt, &success, &failure);
        throw;
    }
    if (!ok(SQLAppendClose(h.stmt, &success, &failure)) || failure != 0)
        throw std::runtime_error("SQLAppendClose");
}

int main() {
    Handles h;
    SQLCHAR conn[] =
        "SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD=MANAGER;CONNTYPE=1";
    if (!ok(SQLAllocEnv(&h.env)) || !ok(SQLAllocConnect(h.env, &h.dbc)) ||
        !ok(SQLDriverConnect(h.dbc, nullptr, conn, SQL_NTS, nullptr, 0,
                             nullptr, SQL_DRIVER_NOPROMPT)) ||
        !ok(SQLAllocStmt(h.dbc, &h.stmt)))
        throw std::runtime_error("connect");

    SQLCHAR *fixed[] = {(SQLCHAR*)"ID", (SQLCHAR*)"A[0]",
                        (SQLCHAR*)"A[3]", nullptr};
    std::array<SQL_APPEND_PARAM, 3> row{};
    row[0].mLong = 1; row[1].mInteger = 10; row[2].mInteger = 40;
    append(h, fixed, row.data(), 3);

    std::array<SQLUSMALLINT, 2> pos{1, 3};
    std::array<SQLINTEGER, 2> val{200, 400};
    std::array<SQLLEN, 2> ind{0, 0};
    SQL_MACHBASE_SPARSE_ARRAY_DESC sparse{};
    sparse.struct_size = sizeof(sparse);
    sparse.element_c_type = SQL_C_SLONG;
    sparse.cardinality = 4;
    sparse.entry_count = 2;
    sparse.positions = pos.data();
    sparse.values = val.data();
    sparse.value_stride = sizeof(val[0]);
    sparse.element_indicators = ind.data();

    SQLCHAR *whole[] = {(SQLCHAR*)"ID", (SQLCHAR*)"A", nullptr};
    std::array<SQL_APPEND_PARAM, 2> sparseRow{};
    sparseRow[0].mLong = 2;
    sparseRow[1].mVar.mData = &sparse;
    sparseRow[1].mVar.mLength = SQL_APPEND_SPARSE_ARRAY_DESC_LENGTH;
    append(h, whole, sparseRow.data(), 2);

    sparse.entry_count = 0;
    sparseRow[0].mLong = 3;
    append(h, whole, sparseRow.data(), 2);

    sparseRow[0].mLong = 4;
    sparseRow[1].mVar.mData = nullptr;
    sparseRow[1].mVar.mLength = 0;
    append(h, whole, sparseRow.data(), 2);

    if (!ok(SQLExecDirect(h.stmt,
        (SQLCHAR*)"SELECT ID,A FROM ARRAY_APPEND_EXAMPLE ORDER BY ID", SQL_NTS)))
        throw std::runtime_error("verify query");
    SQLINTEGER id{}; SQLLEN idInd{}, arrayInd{}; SQLCHAR value[128]{};
    if (!ok(SQLBindCol(h.stmt, 1, SQL_C_SLONG,
                       &id, sizeof(id), &idInd)) ||
        !ok(SQLBindCol(h.stmt, 2, SQL_C_CHAR,
                       value, sizeof(value), &arrayInd)))
        throw std::runtime_error("bind verify");
    for (;;) {
        SQLRETURN fetch = SQLFetch(h.stmt);
        if (fetch == SQL_NO_DATA) break;
        if (!ok(fetch)) throw std::runtime_error("fetch verify");
        std::cout << id << ' ' <<
            (arrayInd == SQL_NULL_DATA ? "NULL" : (char*)value) << '\n';
    }
}
```

```bash
c++ -std=c++11 -I"$MACHBASE_HOME/include" sparse_append.cpp \
  -L"$MACHBASE_HOME/lib" -lmachbasecli -lm -ldl -lrt -pthread \
  -o sparse_append_cpp
```

## Machbase ODBC拡張

<a id="odbc-full-open"></a>

### 通常OpenでスパースARRAYを入力

Machbaseドライバーを直接リンクするCプログラムは、[Cの通常Open例](#c-full-open)の
`sparse_append_full.c`をそのまま使用します。このソースも`SQLAppendOpen()`の後に
`SQLAppendDataV3()`でスパースディスクリプターを渡し、`OpenColumns`は呼び出しません。
同じバージョンのヘッダーとODBC拡張ライブラリでビルドします。

```bash
cc -I"$MACHBASE_HOME/include" sparse_append_full.c \
  -L"$MACHBASE_HOME/lib" -lmachbasecli_dll -lm -ldl -lrt -pthread \
  -o sparse_append_full_odbc
LD_LIBRARY_PATH="$MACHBASE_HOME/lib" ./sparse_append_full_odbc
```

実行前に通常の実習テーブルを準備します。この例のハンドルはMachbaseドライバーが直接生成するもので、
汎用ODBC Driver Managerのハンドルと混用しません。

### 選択列Openで入力

Machbaseドライバーライブラリを直接リンクし、`machbase_sqlcli.h`を使用するODBC Cアプリケーションは
同じ拡張関数を使用できます。次の例は直接のMachbaseドライバーAPIで4行を入力します。
テーブルは前節のDDLで事前に作成します。

```c
/* sparse_odbc.c */
#include <stdio.h>
#include <string.h>
#include <machbase_sqlcli.h>

static int ok(SQLRETURN rc) {
    return rc == SQL_SUCCESS || rc == SQL_SUCCESS_WITH_INFO;
}

int main(void) {
    SQLHENV env = SQL_NULL_HENV;
    SQLHDBC dbc = SQL_NULL_HDBC;
    SQLHSTMT stmt = SQL_NULL_HSTMT;
    SQLBIGINT success = 0, failure = 0;
    SQLCHAR connection[] =
        "SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD=MANAGER;CONNTYPE=1";

    if (!ok(SQLAllocEnv(&env)) ||
        !ok(SQLAllocConnect(env, &dbc)) ||
        !ok(SQLDriverConnect(dbc, NULL, connection, SQL_NTS,
                             NULL, 0, NULL, SQL_DRIVER_NOPROMPT)) ||
        !ok(SQLAllocStmt(dbc, &stmt)))
        return 1;

    SQLCHAR *fixed[] = {(SQLCHAR*)"ID", (SQLCHAR*)"A[0]",
                        (SQLCHAR*)"A[3]", NULL};
    SQL_APPEND_PARAM row[3] = {0};
    row[0].mLong = 1; row[1].mInteger = 10; row[2].mInteger = 40;
    if (!ok(SQLAppendOpenColumns(stmt,
            (SQLCHAR*)"ARRAY_APPEND_EXAMPLE", fixed, 0))) return 2;
    if (!ok(SQLAppendDataV3(stmt, row, 3))) {
        SQLAppendClose(stmt, &success, &failure);
        return 2;
    }
    if (!ok(SQLAppendClose(stmt, &success, &failure)) ||
        success != 1 || failure != 0) return 2;

    SQLUSMALLINT positions[2] = {1, 3};
    SQLINTEGER values[2] = {200, 400};
    SQLLEN indicators[2] = {0, 0};
    SQL_MACHBASE_SPARSE_ARRAY_DESC sparse = {0};
    sparse.struct_size = sizeof(sparse);
    sparse.element_c_type = SQL_C_SLONG;
    sparse.cardinality = 4;
    sparse.entry_count = 2;
    sparse.positions = positions;
    sparse.values = values;
    sparse.value_stride = sizeof(values[0]);
    sparse.element_indicators = indicators;
    SQLCHAR *whole[] = {(SQLCHAR*)"ID", (SQLCHAR*)"A", NULL};
    memset(row, 0, sizeof(row));
    row[0].mLong = 2;
    row[1].mVar.mData = &sparse;
    row[1].mVar.mLength = SQL_APPEND_SPARSE_ARRAY_DESC_LENGTH;
    if (!ok(SQLAppendOpenColumns(stmt,
            (SQLCHAR*)"ARRAY_APPEND_EXAMPLE", whole, 0))) return 3;
    if (!ok(SQLAppendDataV3(stmt, row, 2))) {
        SQLAppendClose(stmt, &success, &failure);
        return 3;
    }
    sparse.entry_count = 0;
    row[0].mLong = 3;
    if (!ok(SQLAppendDataV3(stmt, row, 2))) {
        SQLAppendClose(stmt, &success, &failure);
        return 3;
    }
    row[0].mLong = 4;
    row[1].mVar.mData = NULL;
    row[1].mVar.mLength = 0;
    if (!ok(SQLAppendDataV3(stmt, row, 2))) {
        SQLAppendClose(stmt, &success, &failure);
        return 3;
    }
    success = 0;
    failure = 0;
    if (!ok(SQLAppendClose(stmt, &success, &failure)) ||
        success != 3 || failure != 0) return 3;

    SQLFreeStmt(stmt, SQL_DROP);
    SQLDisconnect(dbc);
    SQLFreeConnect(dbc);
    SQLFreeEnv(env);
    puts("ODBC sparse append OK");
    return 0;
}
```

```bash
cc sparse_odbc.c -I/opt/machbase/include -L/opt/machbase/lib \
  -lmachbasecli_dll -lm -ldl -lrt -pthread -o sparse_odbc
LD_LIBRARY_PATH=/opt/machbase/lib ./sparse_odbc
```

{{< callout type="warning" >}}
汎用ODBC Driver Managerが作成した文ハンドルと直接のSQLCLI拡張ではハンドルABIが異なるため、
混用しないでください。選択列AppendにはMachbaseドライバー拡張と直接のドライバーハンドルを使用する
必要があります。汎用ODBC APIにはAppend Openの選択対象はありません。
{{< /callout >}}

## JDBC

<a id="jdbc-full-open"></a>

### 通常OpenでスパースARRAYを入力

`executeAppendOpen(table, errorCheckCount)`オーバーロードを使用します。返されたメタデータに合わせて
`ID`と`MachSparseArray`を渡し、通常の実習テーブルの自動時刻は直接入力しません。
`null`は全体NULL、空の`MachSparseArray`は全要素がNULLの配列です。

`SparseAppendFull.java`として保存し、ARRAY機能を含むJDBC JARで実行します。

```java
import com.machbase.jdbc.MachConnection;
import com.machbase.jdbc.MachSparseArray;
import com.machbase.jdbc.MachStatement;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

public class SparseAppendFull {
    public static void main(String[] args) throws Exception {
        try (MachConnection con = (MachConnection)DriverManager.getConnection(
                 "jdbc:machbase://127.0.0.1:5656/machbasedb", "SYS", "MANAGER");
             MachStatement st = (MachStatement)con.createStatement()) {
            Map<Integer, Object> entries = new HashMap<Integer, Object>();
            entries.put(0, 10);
            entries.put(3, 40);
            MachSparseArray sparse = con.createSparseArrayOf("INT32", 4, entries);

            try (ResultSet opened = st.executeAppendOpen("ARRAY_APPEND_FULL_EXAMPLE", 0)) {
                try {
                    ResultSetMetaData meta = opened.getMetaData();
                    for (int id = 1; id <= 4; id++) {
                        if (id == 2) sparse.clear().set(1, 200).set(3, 400);
                        if (id == 3) sparse.clear();
                        ArrayList<Object> row = new ArrayList<Object>();
                        row.add(Long.valueOf(id));
                        row.add(id == 4 ? null : sparse);
                        st.executeAppendData(meta, row);
                    }
                } finally {
                    st.executeAppendClose();
                }
            }

            try (ResultSet rs = st.executeQuery(
                     "SELECT ID,A,ARRAY_LENGTH(A) " +
                     "FROM ARRAY_APPEND_FULL_EXAMPLE ORDER BY ID")) {
                int count = 0;
                while (rs.next()) {
                    System.out.println(rs.getLong(1) + " " + rs.getString(2));
                    count++;
                }
                if (count != 4) throw new IllegalStateException("Expected 4 rows");
            }
        }
    }
}
```

```bash
javac -cp "$MACHBASE_JDBC_JAR" SparseAppendFull.java
java -cp ".:$MACHBASE_JDBC_JAR" SparseAppendFull
```

`MACHBASE_JDBC_JAR`には使用するJDBC JARの実際のパスを設定します。上記のクラスパス区切り文字は
Linux用です。エラーなく4行が検索されることを確認し、[共通の期待値](#結果の確認)と比較します。

### 選択列Openで入力

既存の`executeAppendOpen(String, int)`は全行APIとして維持されます。
次のオーバーロードで選択対象を指定します。

```java
ResultSet executeAppendOpen(String tableName,
                            String[] inputColumns,
                            int errorCheckCount)
```

```java
import com.machbase.jdbc.MachConnection;
import com.machbase.jdbc.MachSparseArray;
import com.machbase.jdbc.MachStatement;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

public class SparseAppend {
    static void append(MachStatement st, String[] columns, Object[][] values)
        throws Exception {
        try (ResultSet metaResult = st.executeAppendOpen(
                 "ARRAY_APPEND_EXAMPLE", columns, 0)) {
            ResultSetMetaData meta = metaResult.getMetaData();
            try {
                for (Object[] value : values) {
                    ArrayList<Object> row = new ArrayList<Object>();
                    for (Object item : value) row.add(item);
                    st.executeAppendData(meta, row);
                }
            } finally {
                st.executeAppendClose();
            }
        }
    }

    public static void main(String[] args) throws Exception {
        Class.forName("com.machbase.jdbc.MachDriver");
        MachConnection con = (MachConnection)DriverManager.getConnection(
            "jdbc:machbase://127.0.0.1:5656/machbasedb", "SYS", "MANAGER");
        try {
            try (MachStatement st = (MachStatement)con.createStatement()) {
                append(st, new String[] {"ID", "A[0]", "A[3]"},
                       new Object[][] {{1L, 10, 40}});

                Map<Integer,Object> entries = new HashMap<Integer,Object>();
                entries.put(1, 200);
                entries.put(3, 400);
                MachSparseArray sparse = con.createSparseArrayOf(
                    "INT32", 4, entries);
                MachSparseArray empty = con.createSparseArrayOf(
                    "INT32", 4, new HashMap<Integer,Object>());
                append(st, new String[] {"ID", "A"}, new Object[][] {
                    {2L, sparse}, {3L, empty}, {4L, null}
                });

                try (ResultSet rs = st.executeQuery(
                    "SELECT ID,A,ARRAY_LENGTH(A) " +
                    "FROM ARRAY_APPEND_EXAMPLE ORDER BY ID")) {
                    while (rs.next())
                        System.out.println(
                            rs.getLong(1) + " " + rs.getString(2));
                }
            }
        } finally {
            con.close();
        }
    }
}
```

`createSparseArrayOf()`に渡すmapのキーは0始まりの要素位置です。`MachSparseArray.clear()`と
`set()`で同じオブジェクトを再利用できます。空のmapは全要素がNULLのARRAY、Javaの`null`は
配列全体のNULLです。

## Python DB-API

<a id="python-full-open"></a>

### 列リストなしでスパースARRAYを入力

DB-APIの`append()`は内部でOpen・入力・Closeを処理します。`columns=`を省略し、各行に`ID`と
`SparseArray`を渡します。通常の実習テーブルを先に準備し、次のコードを`sparse_append_full.py`として
保存して実行します。

```python
from machbaseAPI import SparseArray, connect

conn = connect(host="127.0.0.1", port=5656, user="SYS", password="MANAGER")
try:
    first = SparseArray(4).set(0, 10).set(3, 40)
    second = SparseArray(4).set(1, 200).set(3, 400)
    empty = SparseArray(4)
    conn.append("ARRAY_APPEND_FULL_EXAMPLE", [
        [1, first], [2, second], [3, empty], [4, None],
    ])
    rows = conn.cursor(dictionary=False).execute(
        "SELECT ID,A,ARRAY_LENGTH(A) "
        "FROM ARRAY_APPEND_FULL_EXAMPLE ORDER BY ID"
    ).fetchall()
    expected = [
        (1, [10, None, None, 40], 4),
        (2, [None, 200, None, 400], 4),
        (3, [None, None, None, None], 4),
        (4, None, None),
    ]
    assert rows == expected, rows
    print("Python full-row sparse append OK")
finally:
    conn.close()
```

```bash
python3 sparse_append_full.py
```

検索結果が期待値と一致すると`Python full-row sparse append OK`を出力します。

### 選択列を指定して入力

既存の`append(table, rows)`は維持され、`columns=`キーワードで選択対象を指定します。

```python
from machbaseAPI import SparseArray, connect


def main():
    conn = connect(host="127.0.0.1", port=5656,
                   user="SYS", password="MANAGER",
                   database="MACHBASEDB")
    try:
        conn.append(
            "ARRAY_APPEND_EXAMPLE",
            [[1, 10, 40]],
            columns=["ID", "A[0]", "A[3]"],
        )

        sparse = SparseArray(4).set(1, 200).set(3, 400)
        empty = SparseArray(4)
        conn.append(
            "ARRAY_APPEND_EXAMPLE",
            [[2, sparse], [3, empty], [4, None]],
            columns=["ID", "A"],
        )

        rows = conn.cursor(dictionary=False).execute(
            "SELECT ID,A,ARRAY_LENGTH(A) "
            "FROM ARRAY_APPEND_EXAMPLE ORDER BY ID"
        ).fetchall()
        expected = [
            (1, [10, None, None, 40], 4),
            (2, [None, 200, None, 400], 4),
            (3, [None, None, None, None], 4),
            (4, None, None),
        ]
        assert rows == expected, rows
        print("Python sparse append OK")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
```

`SparseArray.clear()`は要素数を維持したまま全要素をNULLに戻します。

### Python legacyラッパー

<a id="python-legacy-full-open"></a>

#### 通常のappendOpenで入力

`appendOpen(table)`で開いて`appendData()`を使用します。スパース配列の作成に
`appendOpenColumns()`の呼び出しは不要です。通常の実習テーブルを準備し、
`sparse_append_full_legacy.py`として保存して実行します。

```python
from machbaseAPI import SparseArray, machbase

db = machbase()
if db.open("127.0.0.1", "SYS", "MANAGER", 5656) != 1:
    raise RuntimeError(db.result())
try:
    if db.appendOpen("ARRAY_APPEND_FULL_EXAMPLE") != 1:
        raise RuntimeError(db.result())
    try:
        sparse = SparseArray(4).set(0, 10).set(3, 40)
        for row_id in range(1, 5):
            if row_id == 2:
                sparse.clear().set(1, 200).set(3, 400)
            if row_id == 3:
                sparse.clear()
            row = [row_id, None if row_id == 4 else sparse]
            if db.appendData("ARRAY_APPEND_FULL_EXAMPLE", None, row) != 1:
                raise RuntimeError(db.result())
    finally:
        if db.appendClose() != 1:
            raise RuntimeError(db.result())
    if db.select(
        "SELECT ID,A,ARRAY_LENGTH(A) "
        "FROM ARRAY_APPEND_FULL_EXAMPLE ORDER BY ID"
    ) != 1:
        raise RuntimeError(db.result())
    print(db.result())
finally:
    db.close()
```

```bash
python3 sparse_append_full_legacy.py
```

`db.result()`の検索結果を[共通の期待値](#結果の確認)と比較します。

#### 選択列Openで入力

既存の`appendOpen(table, types=None)`は全行APIとして維持されます。選択対象には
`appendOpenColumns(table, columns, types=None)`を使用します。

```python
from machbaseAPI import SparseArray, machbase

db = machbase()
if db.open("127.0.0.1", "SYS", "MANAGER", 5656) != 1:
    raise RuntimeError(db.result())
try:
    if db.appendOpenColumns(
        "ARRAY_APPEND_EXAMPLE", ["ID", "A[0]", "A[3]"]
    ) != 1:
        raise RuntimeError(db.result())
    try:
        if db.appendData(
            "ARRAY_APPEND_EXAMPLE", None, [1, 10, 40]
        ) != 1:
            raise RuntimeError(db.result())
    finally:
        if db.appendClose() != 1:
            raise RuntimeError(db.result())

    sparse = SparseArray(4).set(1, 200).set(3, 400)
    empty = SparseArray(4)
    if db.appendOpenColumns(
        "ARRAY_APPEND_EXAMPLE", ["ID", "A"]
    ) != 1:
        raise RuntimeError(db.result())
    try:
        for row in ([2, sparse], [3, empty], [4, None]):
            if db.appendData("ARRAY_APPEND_EXAMPLE", None, row) != 1:
                raise RuntimeError(db.result())
    finally:
        if db.appendClose() != 1:
            raise RuntimeError(db.result())
finally:
    db.close()
```

`appendData()`の値の数と順序は、開いた対象リストに従います。
新規コードでは、より簡潔なDB-APIの`append(..., columns=...)`を推奨します。

## Node.js

<a id="node-full-columns"></a>

### 全列の定義でスパースARRAYを入力

Node.jsも`appendOpen()`でスパース配列を入力します。ただし現在の`@machbase/ts-client`では
`appendOpen(table, columns, options?)`の`columns`は必須です。別の`OpenColumns`メソッドはなく、
全体入力と選択入力を同じメソッドで表します。

次の例は通常の実習テーブルの2つの入力列`ID`、`A`を順に定義します。`A[0]`などの要素対象をOpenに
指定せず、各行の`SparseArray`が位置を決めます。`sparse_append_full.js`として保存し、
ARRAY機能を含むパッケージを使用するプロジェクトで実行します。

```javascript
'use strict';
const { createConnection, SparseArray } = require('@machbase/ts-client');

(async () => {
  const conn = createConnection({
    host: '127.0.0.1', port: 5656, user: 'SYS', password: 'MANAGER',
  });
  await conn.connect();
  try {
    const stream = await conn.appendOpen('ARRAY_APPEND_FULL_EXAMPLE', [
      { name: 'ID', type: 'int64' },
      { name: 'A', type: 'int32-array' },
    ]);
    try {
      await stream.append([
        [1n, new SparseArray(4).set(0, 10).set(3, 40)],
        [2n, new SparseArray(4).set(1, 200).set(3, 400)],
        [3n, new SparseArray(4)],
        [4n, null],
      ]);
    } finally {
      await stream.close();
    }
    const [rows] = await conn.query(
      'SELECT ID,A,ARRAY_LENGTH(A) LEN ' +
      'FROM ARRAY_APPEND_FULL_EXAMPLE ORDER BY ID',
    );
    if (rows.length !== 4) throw new Error('Expected 4 rows');
    console.log(rows);
  } finally {
    await conn.end();
  }
})().catch(error => {
  console.error(error);
  process.exitCode = 1;
});
```

```bash
node sparse_append_full.js
```

4行が検索されることを確認して[共通の期待値](#結果の確認)と比較します。
列定義なしの`appendOpen(table)`や`[]`を渡して自動推論する方式はサポートしません。

### 選択列・要素を定義して入力

`AppendColumnDefinition.name`に、列全体または要素位置を指定した対象を設定します。

```javascript
'use strict';
const { createConnection, SparseArray } = require('@machbase/ts-client');

async function appendRows(connection, columns, rows) {
  const appender = await connection.appendOpen('ARRAY_APPEND_EXAMPLE', columns);
  try {
    await appender.append(rows);
  } finally {
    await appender.close();
  }
}

(async () => {
  const connection = createConnection({
    host: '127.0.0.1', port: 5656, user: 'SYS', password: 'MANAGER',
  });
  await connection.connect();
  try {
    await appendRows(connection, [
      { name: 'ID', type: 'int64' },
      { name: 'A[0]', type: 'int32' },
      { name: 'A[3]', type: 'int32' },
    ], [[1n, 10, 40]]);

    const sparse = new SparseArray(4).set(1, 200).set(3, 400);
    const empty = new SparseArray(4);
    await appendRows(connection, [
      { name: 'ID', type: 'int64' },
      { name: 'A', type: 'int32-array' },
    ], [[2n, sparse], [3n, empty], [4n, null]]);

    const [rows] = await connection.query(
      'SELECT ID,A,ARRAY_LENGTH(A) LEN ' +
      'FROM ARRAY_APPEND_EXAMPLE ORDER BY ID',
    );
    console.log(rows);
  } finally {
    await connection.end();
  }
})().catch((error) => {
  console.error(error.stack || error);
  process.exitCode = 1;
});
```

`MACHBASE_NATIVE_APPEND=0`でprepared代替経路を選択した場合も、`SparseArray`をARRAY互換値として
処理します。

## .NET full/legacyプロバイダー

<a id="dotnet-full-open"></a>

### 通常のAppendOpenでスパースARRAYを入力

`AppendOpen(table)`で開き、`AppendData()`に`MachSparseArray`を渡します。
通常の実習テーブルを先に準備します。次のコードは、ARRAY機能を含むfull/legacyプロバイダーを参照する
C#プロジェクトの`Program.cs`として使用します。

```csharp
using System;
using System.Collections.Generic;
using Mach.Data.MachClient;

public class SparseAppendFull
{
    public static void Main()
    {
        using var conn = new MachConnection(
            "SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD=MANAGER");
        conn.Open();
        using var command = new MachCommand(conn);
        var writer = command.AppendOpen("ARRAY_APPEND_FULL_EXAMPLE");
        try
        {
            var first = new MachSparseArray(MachDBType.INT32_ARRAY, 4)
                .Set(0, 10).Set(3, 40);
            var second = new MachSparseArray(MachDBType.INT32_ARRAY, 4)
                .Set(1, 200).Set(3, 400);
            var empty = new MachSparseArray(MachDBType.INT32_ARRAY, 4);
            var rows = new List<List<object>> {
                new List<object> { 1L, first },
                new List<object> { 2L, second },
                new List<object> { 3L, empty },
                new List<object> { 4L, DBNull.Value },
            };
            foreach (var row in rows) command.AppendData(writer, row);
        }
        finally
        {
            if (command.IsAppendOpened) command.AppendClose(writer);
        }
        if (writer.FailureCount != 0)
            throw new InvalidOperationException("APPEND row failure");

        using var verify = new MachCommand(
            "SELECT ID,A,ARRAY_LENGTH(A) FROM ARRAY_APPEND_FULL_EXAMPLE ORDER BY ID",
            conn);
        using var reader = verify.ExecuteReader();
        int count = 0;
        while (reader.Read())
        {
            Console.WriteLine(reader.IsDBNull(1)
                ? $"{reader.GetInt64(0)} NULL"
                : $"{reader.GetInt64(0)} " +
                  string.Join(",", (object[])reader.GetValue(1)));
            count++;
        }
        if (count != 4) throw new InvalidOperationException("Expected 4 rows");
    }
}
```

次のプロジェクトファイルを`Program.cs`と同じディレクトリに`SparseAppendFull.csproj`として保存します。
この例は.NET 8用プロバイダーを使用します。

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <OutputType>Exe</OutputType>
    <TargetFramework>net8.0</TargetFramework>
    <EnableDefaultCompileItems>false</EnableDefaultCompileItems>
  </PropertyGroup>
  <ItemGroup>
    <Compile Include="Program.cs" />
    <Reference Include="MachbaseProvider">
      <HintPath>$(MachbaseProviderDll)</HintPath>
    </Reference>
  </ItemGroup>
</Project>
```

以下のパスを、ARRAY機能を含む.NET 8プロバイダーDLLの実際のパスに置き換えます。

```bash
dotnet build SparseAppendFull.csproj -p:MachbaseProviderDll=/absolute/path/to/provider.dll
dotnet bin/Debug/net8.0/SparseAppendFull.dll
```

Closeの失敗件数が0で検索結果が4行であることを確認し、[共通の期待値](#結果の確認)と比較します。

### 選択列Openで入力

full APIと既存互換のMachConnector40は、選択対象を受け取るオーバーロードを提供します。
既存の`AppendOpen(string)`とerror-checkオーバーロードは維持されます。

```csharp
MachAppendWriter AppendOpen(string tableName,
                            IList<string> inputColumns);
MachAppendWriter AppendOpen(string tableName,
                            IList<string> inputColumns,
                            int errorCheckCount,
                            MachAppendOption option);
```

```csharp
using System;
using System.Collections.Generic;
using Mach.Data.MachClient;

static void Append(MachConnection connection,
                   IList<string> columns,
                   IList<List<object>> rows)
{
    using var command = new MachCommand(connection);
    var writer = command.AppendOpen("ARRAY_APPEND_EXAMPLE", columns);
    try
    {
        foreach (var row in rows)
            command.AppendData(writer, row);
    }
    finally
    {
        if (command.IsAppendOpened)
            command.AppendClose(writer);
    }
    if (writer.FailureCount != 0)
        throw new InvalidOperationException("APPEND row failure");
}

using var connection = new MachConnection(
    "SERVER=127.0.0.1;PORT_NO=5656;UID=SYS;PWD=MANAGER");
connection.Open();

Append(connection,
    new List<string> { "ID", "A[0]", "A[3]" },
    new List<List<object>> {
        new List<object> { 1L, 10, 40 }
    });

var sparse = new MachSparseArray(MachDBType.INT32_ARRAY, 4)
    .Set(1, 200).Set(3, 400);
var empty = new MachSparseArray(MachDBType.INT32_ARRAY, 4);
Append(connection,
    new List<string> { "ID", "A" },
    new List<List<object>> {
        new List<object> { 2L, sparse },
        new List<object> { 3L, empty },
        new List<object> { 4L, DBNull.Value },
    });

using var verify = new MachCommand(
    "SELECT ID,A,ARRAY_LENGTH(A) FROM ARRAY_APPEND_EXAMPLE ORDER BY ID",
    connection);
using var reader = verify.ExecuteReader();
while (reader.Read())
    Console.WriteLine(reader.IsDBNull(1)
        ? $"{reader.GetInt64(0)} NULL"
        : $"{reader.GetInt64(0)} " +
          string.Join(",", (object[])reader.GetValue(1)));
```

`MachSparseArray.Clear()`はオブジェクトを、全要素がNULLで再利用可能な状態に戻します。
配列全体のNULLは`DBNull.Value`です。Append Open成功後にメタデータ処理が失敗した場合は、
プロバイダーが開いたハンドルを解放し、接続は再利用できます。

## Go neo-client

<a id="go-full-open"></a>

### 列引数なしのConnectで入力

`Appender.Connect(ctx, dsn, table)`の列引数を省略し、`Append(id, sparse)`で入力します。
この例のLOG入力では`_arrival_time`は直接渡しません。`*api.Array`のnilは全体NULLであり、
空のスパースオブジェクトとは区別します。

以下のコードには、要素位置が0始まりのARRAY機能を含む`neo-client/v2`ソースが必要です。
そのソースを`go.work`または`replace`で接続したGoモジュールに`sparse_append_full.go`として保存します。
接続するソースは以下の選択例と同じバージョン条件に従います。

```go
package main

import (
    "context"
    "database/sql"
    "errors"
    "fmt"

    client "github.com/machbase/neo-client/v2"
    "github.com/machbase/neo-client/v2/api"
)

func appendFull(ctx context.Context, dsn string) error {
    first, err := api.NewSparseArray(api.SqlTypeInt32, 4)
    if err != nil { return err }
    if err = first.Set(0, int32(10)); err != nil { return err }
    if err = first.Set(3, int32(40)); err != nil { return err }
    second, err := api.NewSparseArray(api.SqlTypeInt32, 4)
    if err != nil { return err }
    if err = second.Set(1, int32(200)); err != nil { return err }
    if err = second.Set(3, int32(400)); err != nil { return err }
    empty, err := api.NewSparseArray(api.SqlTypeInt32, 4)
    if err != nil { return err }
    var wholeNull *api.Array

    appender := &client.Appender{}
    if err = appender.Connect(ctx, dsn, "ARRAY_APPEND_FULL_EXAMPLE"); err != nil {
        return err
    }
    for _, row := range [][]any{
        {int64(1), first}, {int64(2), second},
        {int64(3), empty}, {int64(4), wholeNull},
    } {
        if err = appender.Append(row...); err != nil {
            _, _, closeErr := appender.Close()
            return errors.Join(err, closeErr)
        }
    }
    success, failure, err := appender.Close()
    if err != nil { return err }
    if success != 4 || failure != 0 {
        return fmt.Errorf("success=%d failure=%d", success, failure)
    }
    return nil
}

func main() {
    ctx := context.Background()
    dsn := "server=tcp://sys:manager@127.0.0.1:5656"
    if err := appendFull(ctx, dsn); err != nil { panic(err) }
    db, err := sql.Open(client.DefaultDriverName, dsn)
    if err != nil { panic(err) }
    defer db.Close()
    rows, err := db.QueryContext(ctx,
        "SELECT ID,A,ARRAY_LENGTH(A) FROM ARRAY_APPEND_FULL_EXAMPLE ORDER BY ID")
    if err != nil { panic(err) }
    defer rows.Close()
    count := 0
    for rows.Next() {
        var id int64
        var value sql.NullString
        var length sql.NullInt64
        if err = rows.Scan(&id, &value, &length); err != nil { panic(err) }
        if value.Valid { fmt.Println(id, value.String, length.Int64) } else {
            fmt.Println(id, "NULL")
        }
        count++
    }
    if err = rows.Err(); err != nil { panic(err) }
    if count != 4 { panic("Expected 4 rows") }
}
```

```bash
go run sparse_append_full.go
```

Closeの成功4件・失敗0件と検索結果を確認します。

### 選択列Connectで入力

この例はMachbase Neoサーバー経由ではなく、`neo-client`がMachbase DBMSに直接接続する経路です。
要素位置が0始まりのARRAYと選択列Append APIは
[`neo-client` PR #17](https://github.com/machbase/neo-client/pull/17)以降のv2モジュールのソースに
含まれます。公開v2リリースが指定されるまでは、公開モジュールのバージョンに同じ機能が含まれると
考えないでください。

```go
package main

import (
    "context"
    "database/sql"
    "errors"
    "fmt"

    client "github.com/machbase/neo-client/v2"
    "github.com/machbase/neo-client/v2/api"
)

func appendRows(ctx context.Context, dsn, table string,
    columns []string, rows [][]any) error {
    appender := &client.Appender{}
    if err := appender.Connect(ctx, dsn, table, columns...); err != nil {
        return err
    }
    for _, row := range rows {
        if err := appender.Append(row...); err != nil {
            _, _, closeErr := appender.Close()
            return errors.Join(err, closeErr)
        }
    }
    success, failure, err := appender.Close()
    if err != nil { return err }
    if failure != 0 {
        return fmt.Errorf("append success=%d failure=%d", success, failure)
    }
    return nil
}

func main() {
    ctx := context.Background()
    dsn := "server=tcp://sys:manager@127.0.0.1:5656"
    db, err := sql.Open(client.DefaultDriverName, dsn)
    if err != nil { panic(err) }
    defer db.Close()
    if err := db.PingContext(ctx); err != nil { panic(err) }

    if err := appendRows(ctx, dsn, "ARRAY_APPEND_EXAMPLE",
        []string{"ID", "A[0]", "A[3]"},
        [][]any{{int64(1), int32(10), int32(40)}}); err != nil {
        panic(err)
    }

    sparse, err := api.NewSparseArray(api.SqlTypeInt32, 4)
    if err != nil { panic(err) }
    if err := sparse.Set(1, int32(200)); err != nil { panic(err) }
    if err := sparse.Set(3, int32(400)); err != nil { panic(err) }
    empty, err := api.NewSparseArray(api.SqlTypeInt32, 4)
    if err != nil { panic(err) }
    var wholeNull *api.Array
    if err := appendRows(ctx, dsn, "ARRAY_APPEND_EXAMPLE",
        []string{"ID", "A"}, [][]any{
            {int64(2), sparse}, {int64(3), empty}, {int64(4), wholeNull},
        }); err != nil {
        panic(err)
    }

    rows, err := db.QueryContext(ctx,
        "SELECT ID,A,ARRAY_LENGTH(A) FROM ARRAY_APPEND_EXAMPLE ORDER BY ID")
    if err != nil { panic(err) }
    defer rows.Close()
    for rows.Next() {
        var id int64
        var value sql.NullString
        var length sql.NullInt64
        if err := rows.Scan(&id, &value, &length); err != nil { panic(err) }
        if !value.Valid { fmt.Println(id, "NULL"); continue }
        fmt.Println(id, value.String, length.Int64)
    }
    if err := rows.Err(); err != nil { panic(err) }
}
```

`Appender.Connect(ctx, dsn, table, columns...)`の可変長引数が選択対象です。
`WithInputColumns(columns...)`を使用する場合は`Connect()`より前に適用します。
1つの`Appender`で`Append`、`Flush`、`Close`を同時に呼び出さないでください。

## 結果の確認

通常の例の実行後、次のクエリで値、全体NULL、要素NULLを確認します。

```sql
SELECT ID, A, ARRAY_LENGTH(A), A[0], A[1], A[2], A[3]
  FROM ARRAY_APPEND_FULL_EXAMPLE
 ORDER BY ID;
```

選択の例の実行後は次のクエリを使用します。両テーブルの期待値は同じです。

```sql
SELECT ID, A, ARRAY_LENGTH(A), A[0], A[1], A[2], A[3]
  FROM ARRAY_APPEND_EXAMPLE
 ORDER BY ID;
```

| ID | A | `ARRAY_LENGTH(A)` |
|---:|---|---:|
| 1 | `[10,null,null,40]` | 4 |
| 2 | `[null,200,null,400]` | 4 |
| 3 | `[null,null,null,null]` | 4 |
| 4 | `NULL` | `NULL` |

各SDKの例を同じテーブルに連続して実行するとIDが重複します。実際の検証では例ごとにテーブルを
空にするか、異なるID範囲を使用します。

<a id="sparse-append-cleanup"></a>

## 実習の後片付け

検索結果の確認後、今回作成した実習テーブルだけを削除します。両方の例を実行した場合は次の2文を使用し、
片方だけなら該当テーブルだけを削除します。

```sql
DROP TABLE ARRAY_APPEND_FULL_EXAMPLE;
DROP TABLE ARRAY_APPEND_EXAMPLE;
```

各文はテーブルとデータをまとめて削除します。同名の既存業務テーブルには適用しないでください。
再実行時は準備SQLから進めます。

## バージョンと制限事項

- `ARRAY`と選択列AppendはMachbase DBMS 8.7.0の機能です。
- ARRAYの公開要素位置は0から始まります。以前の開発バージョンで位置を1から指定していたスパースARRAYと
  選択対象の呼び出しは、位置を1ずつ減らす必要があります。JDBCのパラメーター番号など、別途1始まりの
  標準APIまで変更しないでください。
- Machbase DBMS 8.7.0サーバーとARRAY機能を含むSDKビルドを合わせて使用します。
- 既存の全行Append Open関数・メソッドのシグネチャーと意味は維持されます。
- C APIの列名リストはNULL終端配列であり、件数は別途受け取りません。
- 不正な要素数、重複・範囲外の位置、重複対象、全体・要素対象の衝突、値の数の不一致はエラーです。
- Go ARRAY APIは正式なモジュールリリースまで、機能を含む開発ソースを接続する必要があります。
- SDKは失敗行を成功件数に含めてはいけません。
