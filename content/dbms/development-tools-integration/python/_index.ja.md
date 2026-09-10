---
type: docs
title: '11.6 Python'
weight: 60
toc: true
aliases:
  - /dbms/reference/sdk-api/python/
---

## 概要

パッケージ2.4を基準とします。PyPIのパッケージ名は`machbaseapi`（小文字）です。
純粋なPython実装のため、ネイティブバイナリ（`.so/.dll/.dylib`）は不要です。
既存の`machbase`の使用フローは維持されます。

- インストールするパッケージ名: `machbaseapi`
- 従来どおり`import machbaseAPI`を使用
- DB-API形式の`connect()`、`cursor()`をサポート
- 2.4から`cursor(prepared=True)`でサーバーの文を複数の呼び出しで再利用
- `append*`には`on_ack`コールバックを追加でき、ACKを観測可能
- `append()`、`appendByTime()`、`appendData()`、`appendDataByTime()`は型リストを省略しても動作し、サーバーメタデータから型を自動推論
- 2.3からAppend行の末尾の一部の列を省略すると、AppendのNULLビットにより`NULL`として保存
- TAGテーブルは`value`列までが必須で、後続の追加列とメタデータ列は省略時に`NULL`として保存可能
- 接続プールオプション（`pool_name`、`pool_size`、`pool_reset_session`）は非サポート

## マルチデータベース

`connect(database=...)`で初期データベースを指定できます。現在のカタログのgetter/setterはないため、
接続後に`SELECT CURRENT_DATABASE()`で確認し、SQLの`USE`で変更します。

```python
conn = connect(
    host='127.0.0.1', port=5656,
    user='APP_A', password='secret', database='FACTORY_A',
)
cur = conn.cursor()
cur.execute('SELECT CURRENT_DATABASE()')
print(cur.fetchone())
cur.execute('USE FACTORY_B')
```

既存互換の`machbase.open()`にはデータベース引数がありません。マルチデータベース操作には最新の
`connect()`を使用してください。接続プールと文のバインディング規則の詳細は
[マルチデータベース運用ガイド](/dbms/operations-configuration-recovery/multi-database/#94-python)を
参照してください。

## インストール

### 要件

- `pip`を使用できるPython 3.6以降
- 接続可能なMachbaseサーバーとアカウント情報（デフォルトアカウント`SYS/MANAGER`、ポート`5656`）
- 2.4にはネイティブライブラリの依存関係なし

### PyPIからインストール

```bash
pip3 install machbaseapi
```

`pip3`がPATHにない場合は`python3 -m pip install machbaseapi`を使用します。

### インストールパッケージからオフラインでインストール

インターネットに接続できない環境では、Machbaseインストールパッケージに含まれるwheelをインストールします。

```bash
python3 -m pip install \
  $MACHBASE_HOME/3rd-party/python3-module/machbaseapi-2.4-py3-none-any.whl
```

同じディレクトリのソース配布ファイル`machbaseapi-2.4.tar.gz`も使用できます。
インストール前にPython 3.6以降であることを確認します。

### モジュールの確認

```bash
python3 - <<'PY'
from machbaseAPI import machbase, connect
print('machbaseクラスのインポート:', bool(machbase))
print('connect関数の存在:', callable(connect))
print('module import:', __import__('machbaseAPI'))
PY
```

このコマンドが成功すれば、パッケージを正常にインポートできます。

## クイックスタート

次のDB-API例はサンプルLOGテーブルを作成して入力・検索し、テーブルと接続を片付けます。
パスワードは環境変数で渡します。

```python
import os
from machbaseAPI import connect

conn = connect(
    host=os.getenv('MACH_HOST', '127.0.0.1'),
    port=int(os.getenv('MACH_PORT', '5656')),
    user=os.getenv('MACH_USER', 'SYS'),
    password=os.environ['MACHBASE_PASSWORD'],
)
cur = conn.cursor()

try:
    cur.execute(
        'CREATE LOG TABLE py_sample '
        '(ts DATETIME, device VARCHAR(40), value DOUBLE)'
    )
    cur.execute(
        "INSERT INTO py_sample VALUES ("
        "TO_DATE('2026-01-01','YYYY-MM-DD'), 'sensor-1', 20.5)"
    )
    cur.execute('SELECT device, value FROM py_sample')
    print(cur.fetchall())
finally:
    cur.execute('DROP TABLE py_sample')
    cur.close()
    conn.close()
```

## 結果の処理

DB-APIカーソルは`execute()`、`fetchone()`、`fetchall()`を提供します。作業後にカーソルと接続を閉じ、
サンプルオブジェクトが本番データベースに残らないよう削除します。

### INSERT結果のROWID

Standard EditionでDB-APIカーソルを使って単一の`INSERT ... VALUES`を実行した後、
`cursor.lastrowid`で入力行のROWIDを確認できます。

```python
cursor.execute(
    "INSERT INTO orders(item) VALUES(%s)",
    ("pump",),
)
row_id = cursor.lastrowid
```

値は任意精度のPython `int`で、符号なし64ビットROWIDを正の値として保持します。
ROWIDのない実行では`None`です。`executemany()`、Append、`INSERT ... SELECT`、UPSERTは
ROWIDを返しません。実行失敗後も前の値を再利用しないでください。詳細な条件は
[ROWIDとINSERT結果ID](/dbms/reference/sql/rowid/)を参照してください。

### DB-API結果のNULL許容性メタデータ

DB-APIカーソルでは`cursor.description[i][6]`の`null_ok`値で、SELECT結果列のNULL許容性を
確認します。

```python
cursor.execute(sql)

for column in cursor.description:
    name = column[0]
    null_ok = column[6]
    print(name, null_ok)
```

| `null_ok` | 意味 |
|-----------|------|
| `False` | NULLにならない |
| `True` | NULLになり得る |
| `None` | 判定不能 |

`None`は`NOT NULL`を意味しないため、NULLが発生し得るものとして処理します。
SQL結果の判定規則は
[NULL許容性メタデータのサポート範囲](/dbms/development-tools-integration/sdk-support-scope/#support-scope-sdk-nullable-metadata)を
参照してください。

Machbase SQLでは`''`はSQLの`NULL`のため、`null_ok`は`True`です。ただしPythonコネクターは、
互換性のため文字列型のSQL `NULL`をPythonの空文字列`""`として返す場合があります。
`null_ok`は列のNULL許容性を示すもので、個々の行がNULLかは示しません。行ごとの区別が必要な場合は、
SQLの`IS NULL`条件またはそれを使用したCASE結果も検索してください。

### SELECT結果のPRIMARY KEYメタデータ

Machbase 8.7.0サーバーと対応SDKを使用すると、`cursor.column_metadata`の`is_primary_key`で
SELECT結果の直接の列がPRIMARY KEYか確認できます。

```python
cursor.execute("SELECT ID, VALUE, ID + 1 AS ID_EXPR FROM T_PK")
for column in cursor.column_metadata:
    print(column.name, column.is_primary_key)
```

`cursor.description`のDB-API標準の7番目の値（`null_ok`）は従来どおりNULL許容性のみを示します。
式・集計式・外部結合のNULL補完側の列はPKではないため、`is_primary_key`は`False`です。
旧バージョンのサーバーまたはSDKではPKフラグが提供されない場合があります。

### Named Bind Parameter

Python DB-APIモジュールの`paramstyle`は`"named"`です。`cursor.execute()`と
`cursor.executemany()`にマッピングを渡すと、`:name`のSQLをサーバーのprepare/bind経路で実行します。

```python
from decimal import Decimal
from machbaseAPI import connect

conn = connect(host="127.0.0.1", port=5656,
               user="SYS", password="MANAGER")
cur = conn.cursor(dictionary=False)

cur.execute(
    """INSERT INTO SENSOR_DATA (ID, NAME, VALUE)
       VALUES (:id, :name, :value)""",
    {
        "id": 600,
        "name": "python-client",
        "value": Decimal("52.125000"),
    },
)

cur.execute(
    """SELECT ID, NAME FROM SENSOR_DATA
       WHERE ID = :id OR PARENT_ID = :id""",
    {"id": 600},
)
```

`executemany()`では各行をマッピングとして渡します。

```python
cur.executemany(
    "INSERT INTO SENSOR_DATA (ID, NAME, VALUE) "
    "VALUES (:id, :name, :value)",
    [
        {"id": 601, "name": "batch-a", "value": Decimal("1.5")},
        {"id": 602, "name": "batch-b", "value": None},
    ],
)
```

サーバーのプリペアドステートメントの寿命は、カーソルの種類と呼び出し方式によって異なります。

| カーソル | 呼び出し | サーバーの文の再利用範囲 |
|--------|------|----------------------------|
| 通常カーソル | `execute(sql, params)` | その呼び出しのみ |
| 通常カーソル | `executemany(sql, rows)` | その呼び出し内 |
| プリペアドカーソル | `execute()` / `executemany()` | 同じ元SQLを使用する後続の呼び出し |

通常カーソルの`:name`とマッピングはサーバーprepare/bindを使用しますが、呼び出しの完了時に文を閉じます。
複数の呼び出しで同じ文を再利用する場合は`cursor(prepared=True)`を使用します。

マッピングのキーは先頭のコロンなしで指定し、大文字・小文字を区別します。同名が繰り返されると1つの値を
全位置に適用します。名前の欠落、余分なキー、名前付きと位置指定の混用は`ProgrammingError`を返します。
旧サーバーで名前付きAPIを使用すると、SQLSTATE `0A000`の`NotSupportedError`を返します。

互換性のため`%s`と`%(name)s`も維持します。この2形式はクライアントでSQLリテラルを生成する通常カーソルの
既存経路です。プリペアドカーソルでは`%s`を`?`、`%(name)s`を`:name`へ変換し、サーバーの
prepare/bind経路で実行します。

共通の名前構文は
[Named Bind Parameter syntax](../../reference/sql/syntax/named-bind-parameter-syntax/)を参照してください。

## プリペアドカーソル（2.4）

`connection.cursor(prepared=True)`はサーバーのプリペアドステートメントを1つ保持し、同じSQLを
複数回実行する際に再利用します。繰り返しINSERT、条件検索、同じSQLのバッチ実行に使用します。

```python
from machbaseAPI import connect

conn = connect(
    host="127.0.0.1",
    port=5656,
    user="SYS",
    password="MANAGER",
)
cur = conn.cursor(dictionary=False, raw=False, prepared=True)

sql = "INSERT INTO SENSOR_DATA (ID, NAME, VALUE) VALUES (%s, %s, %s)"
cur.execute(sql, (700, "sensor-a", 21.5))
cur.execute(sql, (701, "sensor-b", 22.1))
cur.executemany(
    sql,
    [
        (702, "sensor-c", 23.0),
        (703, "sensor-d", None),
    ],
)

cur.close()
conn.close()
```

`cursor()`の関連引数は次のとおりです。

- `dictionary=True`: 検索結果を列名ベースの辞書として返します。
- `dictionary=False`: 検索結果をタプルとして返します。
- `raw=True`: 既存のraw結果の仕様を維持します。
- `prepared=True`: 公開型`MachbasePreparedCursor`を返します。
- `prepared=False`: 既存の通常カーソルを返すデフォルト値です。

### パラメーターマーカー

プリペアドカーソルはPython DB-API形式とMachbaseネイティブ形式の両方をサポートします。

| 公開プレースホルダー | サーバーのプレースホルダー | パラメーター形式 |
|---------------|-------------|----------------|
| `%s` | `?` | tuple、listなどのシーケンス |
| `?` | `?` | tuple、listなどのシーケンス |
| `%(name)s` | `:name` | dictionaryなどのマッピング |
| `:name` | `:name` | dictionaryなどのマッピング |

文字列リテラル、引用符で囲まれた識別子、`--`コメント、`/* ... */`コメント内のプレースホルダー状の
文字は変換しません。1つのSQLで位置指定と名前付きプレースホルダーを混用できません。
名前付きプレースホルダーの名前は英字、`_`、`$`で始まり、以降は数字も使用できます。
名前付きプレースホルダーはMachbase 8.7.0サーバーと対応SDKでサポートします。

```python
sql = (
    "SELECT ID, NAME FROM SENSOR_DATA "
    "WHERE ID = %(target)s OR PARENT_ID = %(target)s"
)
cur.execute(sql, {"target": 700})
rows = cur.fetchall()
```

### 文の再利用

プリペアドカーソルは、元のSQL文字列が前の呼び出しと完全に同じ場合にキャッシュしたサーバーの文を
再利用します。空白やコメントも含めて文字列が異なると、既存の文を解放して新しい文を準備します。

```python
insert_cur = conn.cursor(prepared=True)
select_cur = conn.cursor(prepared=True)
```

1つのカーソルが保持するサーバーの文は1つです。複数のSQLをそれぞれ継続して再利用する場合は、
上記のようにSQLごとにプリペアドカーソルを作成します。`executemany()`終了後も文は保持され、
同じSQLの後続の`execute()`または`executemany()`で再利用されます。
空のパラメーターリストを渡すと、文を準備・実行せず`0`を返します。

### エラーと終了

次の入力は`ProgrammingError`になります。

- プレースホルダーがあるのにパラメーターを渡さない場合
- 位置指定プレースホルダーにマッピング、名前付きプレースホルダーにシーケンスを渡す場合
- 位置指定と名前付きプレースホルダーを混用する場合
- 名前付きパラメーターのキーが欠ける、または不要なキーが追加される場合
- プレースホルダーのないSQLに空でないパラメーターを渡す場合

プレースホルダーのないSQLには、パラメーターなしとして`None`、空のシーケンス、空のマッピングを
渡せます。空のマッピングは内部で`None`に正規化されるため、プロトコルバージョンに関係なく同じ意味で
処理されます。

パラメーターエラーが発生してもキャッシュした文は保持されるため、正しいパラメーターで同じSQLを
再実行できます。旧サーバーで名前付きパラメーターを使用すると、サーバーのPREPARE前に
`NotSupportedError`とSQLSTATE `0A000`が発生します。このエラーは現在のキャッシュ文を解放・置換しません。
旧サーバーでは位置指定プレースホルダーを使用します。

`cursor.close()`はキャッシュしたサーバーの文を解放します。同じカーソルを2回閉じても安全で、
接続が先に閉じられた場合はネットワーク要求なしでローカル状態だけを解放します。
閉じたプリペアドカーソルで`execute()`、`executemany()`、フェッチAPIを呼ぶと`InterfaceError`になります。

プリペアドカーソルはSQLの許容範囲やPython APIのauto-commit動作を変更しません。
テーブル別のDML範囲は[サポート範囲と制約](../../reference/support-scope-constraints/)を参照してください。

## サポートAPIマトリクス

| クラス | API | 説明 | 戻り値 |
| -- | -- | -- | -- |
| `machbase` | `open(host, user, password, port)` | 基本アカウントとポートでMachbaseサーバーに接続します。 | 成功時`1`、失敗時`0` |
| `machbase` | `openEx(host, user, password, port, conn_str)` | 追加の接続文字列プロパティで拡張接続します。 | `1`または`0` |
| `machbase` | `close()` | 現在のセッションを終了します。 | `1`または`0` |
| `machbase` | `isOpened()` | ハンドルが開いているか確認します。 | `1`または`0` |
| `machbase` | `isConnected()` | サーバーとの接続状態を確認します。 | `1`または`0` |
| `machbase` | `execute(sql)` | SQLを直接実行します。`SELECT`、`WITH`、`DESC`、`DESCRIBE`、`SHOW`は`select()`、それ以外は`exec_direct()`で実行します。 | `1`または`0` |
| `machbase` | `schema(sql)` | スキーマ関連コマンドを実行します。 | `1`または`0` |
| `machbase` | `tables()` | 全テーブルのメタデータを検索します。 | `1`または`0` |
| `machbase` | `columns(table_name)` | 特定テーブルの列メタデータを検索します。 | `1`または`0` |
| `machbase` | `column(table_name)` | 低レベルのカタログ呼び出しで列レイアウトを取得します。 | `1`または`0` |
| `machbase` | `statistics(table_name, user='SYS')` | CLI経由でテーブル統計を要求します。 | `1`または`0` |
| `machbase` | `select(sql)` | ストリーミング`SELECT`または`DESC`を実行します。 | `1`または`0` |
| `machbase` | `fetch()` | `select()`の後に次の行を取得します。 | `(rc, json_str)` |
| `machbase` | `selectClose()` | 開いた結果セットのカーソルを閉じます。 | `1`または`0` |
| `machbase` | `result()` | 最新のJSONペイロードを返します。 | JSON文字列 |
| `machbase` | `appendOpen(table_name, types=None)` | 列の型コードを指定してAppendプロトコルを開始します。省略時はサーバーメタデータの型を使用できます。 | `1`または`0` |
| `machbase` | `appendOpenColumns(table_name, columns, types=None)` | Machbase DBMS 8.7.0で選択列またはARRAY要素を対象にAppendを開始します。 | `1`または`0` |
| `machbase` | `appendData(table_name, rows_or_types, values=None, format='YYYY-MM-DD HH24:MI:SS', on_ack=None)` | 有効なAppendセッションに行を追加します。型リストを省略する場合は第2引数に行を渡します。呼び出し時にデータパケットを直ちに送信します。 | `1`または`0` |
| `machbase` | `appendDataByTime(table_name, rows_or_types, values=None, format='YYYY-MM-DD HH24:MI:SS', aTimes=None, on_ack=None)` | 明示的なタイムスタンプで行を追加します。型リストを省略する場合は第2引数に行を渡し、`aTimes`でタイムスタンプを指定します。呼び出し時にデータパケットを直ちに送信します。 | `1`または`0` |
| `machbase` | `appendFlush()` | 送信済みAppendデータの未受信サーバー応答を確認する同期点です。送信を遅延したバッファを空にするAPIではありません。 | `1`または`0` |
| `machbase` | `appendClose()` | Appendセッションを終了します。 | `1`または`0` |
| `machbase` | `append(table_name, rows_or_types, aValues=None, format='YYYY-MM-DD HH24:MI:SS')` | オープン・追加・クローズをまとめて処理する便利関数です。型リストを省略する場合は第2引数に行を渡します。 | `1`または`0` |
| `machbase` | `appendByTime(table_name, rows_or_types, aValues=None, format='YYYY-MM-DD HH24:MI:SS', aTimes=None)` | タイムスタンプを指定するAppendの便利関数です。型リストを省略する場合は第2引数に行を渡し、`aTimes`でタイムスタンプを指定します。 | `1`または`0` |

## DB-API形式のAPI（2.4）

| API | 説明 | 戻り値 |
| -- | -- | -- |
| `connect(**kwargs)` | DB-API接続を作成。`host`、`port`、`user`、`password`などはキーワード引数で渡します。 | `MachbaseConnection` |
| `cursor(dictionary=True, raw=False, prepared=False)` | 通常またはプリペアドカーソルを作成 | `MachbaseCursor`または`MachbasePreparedCursor` |
| `cursor.execute(sql, params=None)` | SQLを実行 | `cursor` |
| `cursor.executemany(sql, seq_of_params)` | 同じSQLを複数のマッピングまたはシーケンスで実行 | 実行回数 |
| `cursor.fetchone()` | 1件取得 | `tuple | dict | None` |
| `cursor.fetchmany(size)` | 最大`size`件取得 | `list` |
| `cursor.fetchall()` | 全件取得 | `list` |
| `cursor.description` | 結果列メタデータ。7番目の値は`null_ok`です。 | `tuple | None` |
| `cursor.lastrowid` | 成功した単一INSERTのROWID。非サポートの入力方式または失敗後は`None`です。 | `int | None` |
| `cursor.close()` | カーソルを終了 | `None` |
| `cursor.rowcount` | 影響行数 | `int` |
| `connection.append(table, rows, *, types=None, times=None, date_format=..., strict=False, columns=None)` | Appendで行を追加。`columns`は選択列またはARRAY要素対象を指定します。 | 入力行数 |

## 2.3 Appendの型省略と末尾NULLパディング（推奨）

`append()`と`appendByTime()`は型リストを省略して呼び出せます。第2引数に行の集合をそのまま渡すと、
サーバーメタデータに基づいて処理します。2.3以降は入力行の末尾の一部の列を省略でき、省略した列は
AppendのNULLビットにより`NULL`として保存されます。

```python
#!/usr/bin/env python3
from machbaseAPI.machbaseAPI import machbase

def main():
    db = machbase()
    if db.open('127.0.0.1', 'SYS', 'MANAGER', 5656) == 0:
        raise SystemExit(db.result())

    try:
        db.execute('drop table py_append_auto')
        db.result()
        ddl = 'create table py_append_auto(ts datetime, tag varchar(16), reading double)'
        if db.execute(ddl) == 0:
            raise SystemExit(db.result())
        db.result()

        rows = [
            ['2024-01-01 10:00:00', 'node-1', 30.0],
            ['2024-01-01 10:01:00', 'node-1', 30.5],
        ]
        if db.append('PY_APPEND_AUTO', rows) == 0:
            raise SystemExit(db.result())
        print('append without types result:', db.result())
    finally:
        if db.close() == 0:
            raise SystemExit(db.result())

if __name__ == '__main__':
    main()
```

### DB-API Appendの末尾NULLの例

`connect().append()`も同じ末尾`NULL`パディング規則を使用します。途中の列を飛ばす位置指定入力は
サポートしないため、途中の値を`NULL`にする場合は、その位置に`None`を明示します。

```python
from machbaseAPI import connect

conn = connect(host='127.0.0.1', port=5656, user='SYS', password='MANAGER')
cur = conn.cursor()

try:
    cur.execute('drop table py_append_null')
except Exception:
    pass
cur.execute('create table py_append_null(ts datetime, name varchar(20), value double, note varchar(40))')

conn.append('PY_APPEND_NULL', [
    ['2024-01-01 10:00:00', 'sensor-1', 12.3],
    ['2024-01-01 10:00:01', 'sensor-2', None, 'manual null'],
])

cur.execute('select ts, name, value, note from py_append_null order by ts')
print(cur.fetchall())
conn.close()
```

1行目は`note`列を省略しているため`NULL`として保存されます。
2行目は`value`位置に`None`を明示しているため、`value`が`NULL`として保存されます。

### TAGテーブルのAppendとメタデータNULLの例

TAGテーブルは`name`、`time`、`value`に対応する値まで必須です。`value`の後に定義した追加列や
メタデータ列は省略でき、省略した列は`NULL`として保存されます。

```python
from machbaseAPI import connect

conn = connect(host='127.0.0.1', port=5656, user='SYS', password='MANAGER')
cur = conn.cursor()

try:
    cur.execute('drop table py_tag_append_null')
except Exception:
    pass
cur.execute('''
    create tag table py_tag_append_null (
        name varchar(40) primary key,
        time datetime basetime,
        value double summarized,
        status varchar(20)
    ) metadata (
        site varchar(20),
        line integer
    )
''')

conn.append('PY_TAG_APPEND_NULL', [
    ['tag-1', '2024-01-01 10:00:00', 12.3],
])

cur.execute('select name, time, value, status, site, line from py_tag_append_null')
print(cur.fetchall())
conn.close()
```

この例の`status`、`site`、`line`はすべて`NULL`で保存されます。一方、`value`を省略したTAGの
Appendはエラーになります。

## `machbase`クラスの互換API

既存アプリケーションとの互換性のため維持される`machbase`クラスを説明します。
新規コードには前述のDB-API `connect()`方式を推奨します。
`getSessionId()`、`count()`、`checkBit()`などは旧ネイティブパッケージにはありましたが、
現在の純粋なPython実装にはありません。必要に応じて2.4のDB-API例を参照してください。

各スクリプトのホスト・ポート・アカウントを環境に合わせて変更してください。
すべての例は独立実行でき、`python3 script.py`形式で実行できます。

### 接続管理

#### machbase.open(), machbase.isOpened(), machbase.isConnected(), machbase.close()

```python
#!/usr/bin/env python3
from machbaseAPI.machbaseAPI import machbase

def main():
    db = machbase()
    print('isOpened before open:', db.isOpened())
    print('isConnected before open:', db.isConnected())

    if db.open('127.0.0.1', 'SYS', 'MANAGER', 5656) == 0:
        raise SystemExit(db.result())

    print('isOpened after open:', db.isOpened())
    print('isConnected after open:', db.isConnected())

    if db.close() == 0:
        raise SystemExit(db.result())

    print('isOpened after close:', db.isOpened())
    print('isConnected after close:', db.isConnected())

if __name__ == '__main__':
    main()
```

#### machbase.openEx()

```python
#!/usr/bin/env python3
from machbaseAPI.machbaseAPI import machbase

def main():
    db = machbase()
    conn_str = 'APP_NAME=python-demo'
    if db.openEx('127.0.0.1', 'SYS', 'MANAGER', 5656, conn_str) == 0:
        raise SystemExit(db.result())
    print('connected with openEx:', db.isConnected())
    if db.close() == 0:
        raise SystemExit(db.result())

if __name__ == '__main__':
    main()
```

### DMLと結果バッファ

#### machbase.execute(), machbase.result()

```python
#!/usr/bin/env python3
import json
from machbaseAPI.machbaseAPI import machbase

def main():
    db = machbase()
    if db.open('127.0.0.1', 'SYS', 'MANAGER', 5656) == 0:
        raise SystemExit(db.result())

    try:
        rc = db.execute('drop table py_exec_demo')
        print('drop table rc:', rc)
        print('drop table result:', db.result())

        ddl = 'create table py_exec_demo(id integer, note varchar(32))'
        if db.execute(ddl) == 0:
            raise SystemExit(db.result())
        print('create table result:', db.result())

        for idx in range(2):
            sql = f"insert into py_exec_demo values ({idx}, 'row-{idx}')"
            if db.execute(sql) == 0:
                raise SystemExit(db.result())
            print('insert result:', db.result())

        if db.execute('select * from py_exec_demo order by id') == 0:
            raise SystemExit(db.result())
        payload = db.result()
        print('select payload:', payload)
        rows = json.loads(payload)
        print('decoded rows:', rows)
        print('row count:', len(rows))
    finally:
        if db.close() == 0:
            raise SystemExit(db.result())

if __name__ == '__main__':
    main()
```

### ストリーミングSELECTヘルパー

#### machbase.select(), machbase.fetch(), machbase.selectClose()

```python
#!/usr/bin/env python3
import json
from machbaseAPI.machbaseAPI import machbase

def main():
    db = machbase()
    if db.open('127.0.0.1', 'SYS', 'MANAGER', 5656) == 0:
        raise SystemExit(db.result())

    try:
        rc = db.execute('drop table py_select_demo')
        print('drop table rc:', rc)
        print('drop table result:', db.result())

        ddl = 'create table py_select_demo(id integer, value double)'
        if db.execute(ddl) == 0:
            raise SystemExit(db.result())
        print('create table result:', db.result())

        for idx in range(5):
            sql = f"insert into py_select_demo values ({idx}, {idx * 1.5})"
            if db.execute(sql) == 0:
                raise SystemExit(db.result())
            print('insert result:', db.result())

        if db.select('select id, value from py_select_demo order by id') == 0:
            raise SystemExit(db.result())

        fetched = 0
        while True:
            rc, payload = db.fetch()
            if rc == 0:
                break
            print('fetched row:', json.loads(payload))
            fetched += 1
        print('fetched rows:', fetched)

        db.selectClose()
    finally:
        if db.close() == 0:
            raise SystemExit(db.result())

if __name__ == '__main__':
    main()
```

### スキーマヘルパー

#### machbase.schema()

```python
#!/usr/bin/env python3
from machbaseAPI.machbaseAPI import machbase

def main():
    db = machbase()
    if db.open('127.0.0.1', 'SYS', 'MANAGER', 5656) == 0:
        raise SystemExit(db.result())

    try:
        rc = db.schema('drop table py_schema_demo')
        print('schema drop rc:', rc)
        print('schema drop result:', db.result())

        ddl = 'create table py_schema_demo(name varchar(20), created datetime)'
        if db.schema(ddl) == 0:
            raise SystemExit(db.result())
        print('schema create result:', db.result())
    finally:
        if db.close() == 0:
            raise SystemExit(db.result())

if __name__ == '__main__':
    main()
```

### メタデータと統計

#### machbase.tables(), machbase.columns(), machbase.column(), machbase.statistics()

```python
#!/usr/bin/env python3
from machbaseAPI.machbaseAPI import machbase

def main():
    db = machbase()
    if db.open('127.0.0.1', 'SYS', 'MANAGER', 5656) == 0:
        raise SystemExit(db.result())

    try:
        if db.tables() == 0:
            raise SystemExit(db.result())
        print('tables metadata:', db.result())

        if db.columns('PY_EXEC_DEMO') == 0:
            raise SystemExit(db.result())
        print('columns metadata:', db.result())

        if db.column('PY_EXEC_DEMO') == 0:
            raise SystemExit(db.result())
        print('column metadata:', db.result())

        if db.statistics('PY_EXEC_DEMO') == 0:
            raise SystemExit(db.result())
        print('statistics output:', db.result())
    finally:
        if db.close() == 0:
            raise SystemExit(db.result())

if __name__ == '__main__':
    main()
```

### Appendプロトコルの基本

`appendOpen()`、`appendData()`、`appendFlush()`、`appendClose()`を組み合わせると、行を効率的に
ストリーミングできます。2.1以降は型を省略して`appendOpen()`で開始できます。
`appendData()`と`appendDataByTime()`は呼び出し時にデータパケットを直ちに送信します。
`appendFlush()`は、送信済みAppendデータの未受信サーバー応答を確認する同期点です。

```python
#!/usr/bin/env python3
from machbaseAPI.machbaseAPI import machbase

def main():
    db = machbase()
    if db.open('127.0.0.1', 'SYS', 'MANAGER', 5656) == 0:
        raise SystemExit(db.result())

    try:
        rc = db.execute('drop table py_append_demo')
        print('drop table rc:', rc)
        print('drop table result:', db.result())

        ddl = 'create table py_append_demo(ts datetime, device varchar(32), value double)'
        if db.execute(ddl) == 0:
            raise SystemExit(db.result())
        print('create table result:', db.result())

        if db.appendOpen('PY_APPEND_DEMO') == 0:
            raise SystemExit(db.result())

        rows = [
            ['2024-01-01 09:00:00', 'sensor-a', 21.5],
            ['2024-01-01 09:05:00', 'sensor-b', 22.1],
        ]
        if db.appendData('PY_APPEND_DEMO', rows) == 0:
            raise SystemExit(db.result())
        print('appendData result:', db.result())

        if db.appendFlush() == 0:
            raise SystemExit(db.result())
        print('appendFlush result:', db.result())

        if db.appendClose() == 0:
            raise SystemExit(db.result())
        print('appendClose result:', db.result())
    finally:
        if db.close() == 0:
            raise SystemExit(db.result())

if __name__ == '__main__':
    main()
```

### Appendの便利関数

#### machbase.append()

```python
#!/usr/bin/env python3
from machbaseAPI.machbaseAPI import machbase

def main():
    db = machbase()
    if db.open('127.0.0.1', 'SYS', 'MANAGER', 5656) == 0:
        raise SystemExit(db.result())

    try:
        db.execute('drop table py_append_auto')
        db.result()
        ddl = 'create table py_append_auto(ts datetime, tag varchar(16), reading double)'
        if db.execute(ddl) == 0:
            raise SystemExit(db.result())
        db.result()

        values = [
            ['2024-01-01 10:00:00', 'node-1', 30.0],
            ['2024-01-01 10:01:00', 'node-1', 30.5],
        ]
        if db.append('PY_APPEND_AUTO', values) == 0:
            raise SystemExit(db.result())
        print('append() result:', db.result())
    finally:
        if db.close() == 0:
            raise SystemExit(db.result())

if __name__ == '__main__':
    main()
```

#### machbase.appendDataByTime(), machbase.appendByTime()

```python
#!/usr/bin/env python3
from machbaseAPI.machbaseAPI import machbase

def main():
    db = machbase()
    if db.open('127.0.0.1', 'SYS', 'MANAGER', 5656) == 0:
        raise SystemExit(db.result())

    try:
        db.execute('drop table py_append_time')
        db.result()
        ddl = 'create table py_append_time(ts datetime, tag varchar(16), reading double)'
        if db.execute(ddl) == 0:
            raise SystemExit(db.result())
        db.result()

        rows = [
            ['2024-01-01 11:00:00', 'node-2', 40.1],
            ['2024-01-01 11:01:00', 'node-2', 40.7],
        ]
        epoch_times = [
            1704106800 * 1_000_000_000,
            1704106860 * 1_000_000_000,
        ]

        if db.appendOpen('PY_APPEND_TIME') == 0:
            raise SystemExit(db.result())
        if db.appendDataByTime('PY_APPEND_TIME', rows, aTimes=epoch_times) == 0:
            raise SystemExit(db.result())
        print('appendDataByTime result:', db.result())
        db.appendClose()

        if db.appendByTime('PY_APPEND_TIME', rows, aTimes=epoch_times) == 0:
            raise SystemExit(db.result())
        print('appendByTime result:', db.result())
    finally:
        if db.close() == 0:
            raise SystemExit(db.result())

if __name__ == '__main__':
    main()
```

`aTimes`は行と同じ順序のエポックナノ秒のシーケンスです。
秒単位のUnixタイムスタンプをそのまま渡さないでください。

## ARRAYと選択列Append

Machbase DBMS 8.7.0はARRAYをPythonの`list`で返し、prepared入力には`list`または`tuple`を
使用できます。要素NULLはコレクション内の`None`、配列全体のNULLは列自体の`None`です。

列リストなしの`connection.append(table, rows)`に`SparseArray`を渡すこともできます。

```python
from machbaseAPI import SparseArray

sparse = SparseArray(4).set(1, 200).set(3, 400)
connection.append("ARRAY_APPEND_FULL_EXAMPLE", [[2, sparse]])
```

このコードは`ID LONG, A INT32[4]`テーブルと開いた接続を前提とします。全体NULL・空のスパース配列・
結果確認を含む[通常入力の例](../data-input-load-export/array-append/#python-full-open)を参照してください。
legacyラッパーには[`appendOpen(table)`の例](../data-input-load-export/array-append/#python-legacy-full-open)が
あります。

選択対象は`connection.append(..., columns=...)`で指定します。行ごとに異なるARRAY位置を入力する
場合は`SparseArray`を使用します。要素位置を指定した対象と`SparseArray.set()`の位置は0始まりです。

```python
from machbaseAPI import SparseArray, connect

connection = connect(
    host="127.0.0.1",
    port=5656,
    user="SYS",
    password="MANAGER",
)
try:
    connection.append(
        "ARRAY_APPEND_EXAMPLE",
        [[1, 10, 40]],
        columns=["ID", "A[0]", "A[3]"],
    )

    sparse = SparseArray(4).set(1, 200).set(3, 400)
    connection.append(
        "ARRAY_APPEND_EXAMPLE",
        [[2, sparse]],
        columns=["ID", "A"],
    )
finally:
    connection.close()
```

`SparseArray.clear()`は要素数を維持して全要素をNULLに戻します。NULLの区別、検証、既存互換APIの
詳細例は[Sparse ARRAYと選択列Append API](../data-input-load-export/array-append/)を参照してください。
