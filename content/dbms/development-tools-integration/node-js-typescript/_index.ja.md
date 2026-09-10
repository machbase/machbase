---
type: docs
title: '11.7 Node.js / TypeScript'
weight: 70
toc: true
aliases:
  - /dbms/reference/sdk-api/node-js-typescript/
---

## 概要

Machbase TypeScriptクライアント（`@machbase/ts-client`）は、ネイティブバインディングなしで
Machbase Standard Editionサーバーに接続するライブラリです。Node.jsアプリケーションでSQLの実行、
結果の取得、プリペアドステートメントの処理、ログデータのAppendを実行できます。

このドキュメントではインストール、主要API、例、テストフロー、動作特性を扱います。

## マルチデータベース

接続設定またはURLの`database`値で初期データベースを指定します。カタログgetterは提供しないため、
SQLの`CURRENT_DATABASE()`と`USE`で確認・変更します。

```typescript
const conn = createConnection({
  host: '127.0.0.1', port: 5656,
  user: 'APP_A', password: 'secret', database: 'FACTORY_A',
});
await conn.connect();
const [rows] = await conn.query('SELECT CURRENT_DATABASE()');
console.table(rows);
```

Appenderとプリペアドステートメントは、open/prepare時点のデータベースに固定されます。詳細は
[マルチデータベース運用ガイド](/dbms/operations-configuration-recovery/multi-database/#95-nodejs)を
参照してください。

## インストール

### 要件

- Node.js 18以降（LTSを推奨）
- 接続可能なMachbaseサーバー（Standard Edition）

### npmからインストール

パッケージマネージャーでインストールします。

```bash
npm install @machbase/ts-client
# または
yarn add @machbase/ts-client
# または
pnpm add @machbase/ts-client
```

### オフラインインストール

Machbaseから`.tgz`パッケージを受け取った場合:

```bash
# ファイル名の例。バージョンは異なる場合があります
npm install ./machbase-ts-client-<version>.tgz
```

### インストールの確認

```bash
node -e "const { createConnection } = require('@machbase/ts-client'); console.log(typeof createConnection === 'function' ? 'ts-client import ok' : 'ts-client import failed')"
```

> **補足**: このクライアントはNode.jsのTCPソケットを使用し、ブラウザー用ライブラリ（WebSocket転送）は提供しません。
> NFX `cce422d2972`ソースツリーの`package.json`は`@machbase/ts-client` 1.0.1です。ただし、
> 名前付きbind・NULL許容性・PK・ROWID・TRANSACTION機能の一部は、公開1.0.1の配布後に同じソースの
> バージョン文字列の下で追加されました。npmのバージョンだけで同じ機能を想定せず、配布成果物の
> コミット出所を確認するか、このNFXソースからビルドしてください。
>
> 本ドキュメントのデフォルトアカウント（`SYS`/`MANAGER`）はローカルテスト用です。
> 本番環境では専用アカウントとパスワードを使用してください。

## クイックスタート

次の例はローカルサーバーに接続してシステムテーブルを検索し、セッションを終了します。

```typescript
// src/example.ts
import { createConnection } from '@machbase/ts-client';

const conn = createConnection({
  host: process.env.MACH_HOST ?? '127.0.0.1',
  port: +(process.env.MACH_PORT ?? 5656),
  user: process.env.MACH_USER ?? 'SYS',
  password: process.env.MACH_PASS ?? 'MANAGER',
});

await conn.connect();
const [rows] = await conn.query('SELECT NAME FROM V$TABLES ORDER BY NAME LIMIT ?', [5]);
console.log(rows);
await conn.end();
```

> **トランザクションについて:** サーバーはTRANSACTIONテーブルに通常の`BEGIN`、`COMMIT`、
> `ROLLBACK` SQLをサポートします。このクライアントの便利メソッド`beginTransaction`、`commit`、
> `rollback`は未実装のため、`execute()`でSQLを直接実行する必要があります。

## よくある問題

- **ECONNREFUSED** – サーバーの状態（`machadmin -e`）、ホストとポート、ファイアウォールでの
  リスナーポートの許可を確認します。デフォルトのSQL接続ポートは5656です。
- **Authentication failed** – ユーザー・パスワードとアカウントの接続権限を確認してください。

## APIリファレンス

### 接続管理

#### createConnection(config)

Machbaseリスナーに接続し、データベースセッションを作成します。

| パラメーター | 型 | デフォルト値 | 説明 |
|-----------|------|---------|-------------|
| `host` | 文字列 | `127.0.0.1` | MachbaseサーバーのIPまたはホスト名 |
| `port` | number | `5656` | リスナーポート |
| `user` | 文字列 | – | データベースユーザー（デフォルト`SYS`） |
| `password` | 文字列 | – | パスワード（デフォルト`MANAGER`） |
| `database` | 文字列 | `data` | データベース名 |
| `clientId` | 文字列 | `NPM` | サーバーログに表示するクライアントID |
| `showHiddenColumns` | boolean | `false` | メタデータに非表示列を含めるか |
| `timezone` | 文字列 | 空 | 任意のタイムゾーン識別子 |
| `connectTimeout` | number | 5000 | ソケット接続タイムアウト（ms） |
| `queryTimeout` | number | 60000 | コマンドごとのタイムアウト（ms） |

```javascript
const conn = createConnection({ host: '192.168.1.10', user: 'SYS', password: 'MANAGER' });
await conn.connect();
```

ソケット接続失敗、認証エラー、ハンドシェイク応答の異常時はPromiseがrejectされます。

#### connect()

サーバーとの接続を開きます。

```javascript
await conn.connect();
```

#### end()

ソケット接続を終了します。`end()`の後に追加操作を試みるとエラーになります。

```javascript
await conn.end();
```

### SQLの実行

#### execute(sql, values?)

結果セットを返さない場合もあるコマンドを実行します。DDL（`CREATE`、`ALTER`、`DROP`）や
DML（`INSERT`、`UPDATE`、`DELETE`）に使用してください。

```javascript
const [create] = await conn.execute('CREATE TRANSACTION TABLE demo (ID INTEGER, NAME VARCHAR(32))');
console.log('Rows affected:', create.affectedRows); // DDLでは0

await conn.execute('BEGIN');
const [insert] = await conn.execute("INSERT INTO demo VALUES (1, 'alpha')");
console.log('Rows affected:', insert.affectedRows); // -> 1
await conn.execute('COMMIT');
```

Standard Editionで単一の`INSERT ... VALUES`が成功すると、実行結果の`rowId`にROWIDが含まれます。
64ビット精度を保持するため、`number`ではなく`bigint`で処理します。

```javascript
const [result] = await conn.execute(
  'INSERT INTO sensor_log(message) VALUES(?)',
  ['started']
);

if (result.rowId !== undefined) {
  const rowId = result.rowId; // bigint
}
```

ROWIDがない実行では`rowId`は`undefined`です。バッチ、Append、`INSERT ... SELECT`、UPSERTの
違いは[ROWIDとINSERT結果ID](/dbms/reference/sql/rowid/)を参照してください。

#### query(sql, values?)

行を返すクエリを実行します。戻り値は`[rows, fields]`形式の2要素タプルです。

```javascript
const [rows, fields] = await conn.query('SELECT ID, NAME FROM demo ORDER BY ID');
console.table(rows);
```

#### Named Bind Parameter

`execute()`、`query()`、プリペアドステートメントの`execute()`では、配列が位置指定入力、
通常のオブジェクトが名前付き入力です。

```typescript
export type MachbaseNamedBindInput =
  Record<string, MachbaseBindInput>;
export type MachbaseExecuteInput =
  MachbaseBindInput[] | MachbaseNamedBindInput;
```

```javascript
await conn.execute(
  'INSERT INTO demo (ID, NAME) VALUES (:id, :name)',
  { id: 1, name: 'node-client' },
);

const [rows] = await conn.query(
  'SELECT ID, NAME FROM demo WHERE ID = :id OR PARENT_ID = :id',
  { id: 1 },
);
```

プリペアドステートメントでもオブジェクトを渡します。

```javascript
const stmt = await conn.prepare(
  'SELECT ID, NAME FROM demo WHERE ID = :id'
);
try {
  const [rows] = await stmt.execute({ id: 1 });
} finally {
  await stmt.close();
}
```

オブジェクトのキーは先頭のコロンなしで指定し、大文字・小文字を区別します。同名の繰り返しには同じ値が
適用されます。オブジェクト入力と`?`の併用、必須キーの欠落、SQLにないキーの指定はエラーになります。

| エラーコード | 状況 |
|---|---|
| `ERR_MACHBASE_BIND_MISSING` | 必須の名前が欠けている |
| `ERR_MACHBASE_BIND_EXTRA` | SQLにない名前を指定した |
| `ERR_MACHBASE_BIND_MIXED` | 名前付きと匿名プレースホルダーを混用した |
| `ERR_MACHBASE_NAMED_BIND_UNSUPPORTED` | サーバーが名前付きバインディングをサポートしない |

`fields`の各`ColumnMeta`オブジェクトは`nullable`プロパティを提供します。

```typescript
import { ColumnNullable } from '@machbase/ts-client';

const [rows, fields] = await conn.query(
  'SELECT ID, NAME, ID + 1 AS EXPR_VALUE FROM demo ORDER BY ID'
);

for (const field of fields) {
  if (field.nullable === ColumnNullable.NoNulls) {
    console.log(field.name, 'NO_NULLS');
  } else {
    console.log(field.name, 'NULL処理が必要');
  }
}
```

| 列挙値 | 数値 | 意味 |
|--------|:------:|------|
| `ColumnNullable.NoNulls` | `0` | NULLにならない |
| `ColumnNullable.Nullable` | `1` | NULLになり得る |
| `ColumnNullable.Unknown` | `2` | 判定不能 |

`ColumnNullable.Unknown`は`NOT NULL`を意味しません。NULLが発生し得るものとして処理します。
SQL結果の判定規則は
[NULL許容性メタデータのサポート範囲](/dbms/development-tools-integration/sdk-support-scope/#support-scope-sdk-nullable-metadata)を
参照してください。

Machbase SQLでは`''`はSQLの`NULL`のため、該当`field.nullable`は`ColumnNullable.Nullable`、
結果行の値はJavaScriptの`null`です。一方、`''''`は単一引用符1文字のため、
`ColumnNullable.NoNulls`と文字列値`'`を返します。

### SELECT結果のPRIMARY KEYメタデータ

Machbase 8.7.0サーバーと対応SDKを使用すると、`query()`または`execute()`が返す`fields`配列の
`isPrimaryKey`で、直接の列がPRIMARY KEYか確認できます。

```ts
const [rows, fields] = await conn.query(
  'SELECT ID, VALUE, ID + 1 AS ID_EXPR FROM T_PK'
);
for (const field of fields) {
  console.log(field.name, field.isPrimaryKey);
}
```

式・集計式・外部結合のNULL補完側の列は`false`です。
旧バージョンのサーバーまたはSDKではPKフラグが提供されない場合があります。

### プリペアドステートメントの使用

#### prepare(sql)

サーバーにプリペアドステートメントを作成します。

```javascript
const stmt = await conn.prepare('SELECT NAME FROM demo WHERE ID = ?');
try {
  const [rows] = await stmt.execute([1]);
  console.log(rows); // -> [ { NAME: 'alpha' } ]
} finally {
  await stmt.close();
}
```

返されたオブジェクトは次のメソッドを提供します。

- `execute(parameters?)` – 文を実行し、`[rowsOrPacket, fields]`を返します。
- `getColumns()` – 列メタデータのキャッシュを返します。
- `getLastMessage()` – 最新のサーバーメッセージを確認します。
- `getStatementId()` – 内部のStatement IDを取得します。
- `close()` – サーバーリソースを解放します。複数回呼び出しても安全です。

`getColumns()`が返す`ColumnMeta`にも同じ`nullable`値が含まれます。

```typescript
const stmt = await conn.prepare('SELECT ID, NAME FROM demo WHERE ID = ?');
for (const column of stmt.getColumns()) {
  console.log(column.name, ColumnNullable[column.nullable]);
}
```

#### プリペアドステートメントの例

**Prepared SELECTの再利用:**

```javascript
const select = await conn.prepare('SELECT DEVICE_ID, SENSOR_VALUE FROM sensors WHERE DEVICE_ID = ?');
for (const { id } of samples) {
  const [rows] = await select.execute([id]);
  console.log(`selected ${id}:`, rows);
}
await select.close();
```

**Prepared Upsert:**

```javascript
const upsert = await conn.prepare(
  'INSERT INTO devices (DEVICE_ID, SENSOR_VALUE) VALUES (?, ?) ' +
  'ON DUPLICATE KEY UPDATE SET SENSOR_VALUE = ?',
);
const [result] = await upsert.execute([deviceId, firstValue, firstValue]);
console.log('Affected rows:', result.affectedRows);
await upsert.close();
```

**型指定引数とNULL処理:**

```javascript
await update.execute([
  { value: null, type: 'varchar' },
  { value: new Date(), type: 'varchar' },
  { value: 'sensor-200', type: 'varchar' },
]);
```

実行サンプルのスクリプトは通常、`npm run build`の後に`dist/examples/`配下に生成されます。
サンプルは一般に`MACHBASE_EXAMPLE_*`、`MACHBASE_SMOKE_*`、最後に`SYS/MANAGER@127.0.0.1`の順で
接続情報を探します。

### Append API

#### appendBatch(table, columns, rows, options?)

`appendBatch()`で**LOGテーブル**に複数行を追加します。ユーザーに見える列だけを渡せます。
LOGテーブルには`_arrival_time`と`_rid`が自動的に含まれます。

```javascript
const appendResult = await conn.appendBatch(
  'sensor_log',
  [
    { name: 'ID', type: 'int32' },
    { name: 'NAME', type: 'varchar' },
    { name: 'VALUE', type: 'float64' },
  ],
  [
    [1, 'alpha', 0.5],
    { values: [2, 'bravo', 1.25], arrivalTime: BigInt(Date.now()) * 1_000_000n },
  ],
);
console.log('Appended rows:', appendResult.rowsAppended);
```

サポートする列の型: `int32`、`int64`、`float64`、`varchar`。

- `rows`は値配列、または`{ values, arrivalTime }`オブジェクトの配列を受け取れます。
  `null`はMachbaseのセンチネル値に自動エンコードされます。
- `options`は`arrivalTime`（デフォルト値1つ）または`arrivalTimes`（行別の配列）を指定できます。
- エポックナノ秒を直接計算する際は、先に`bigint`へ変換します。`number`の乗算は安全な整数範囲を超えます。

戻り値は`{ table, rowsAppended, rowsFailed, message }`形式です。

> **ヒント**: 列数不一致の「does not match」エラーは、対象がLOGテーブルでない場合や、列順序が
> スキーマと一致しない場合に発生します。TAGテーブルには`appendOpen()`を使用してください。

#### appendOpen(table, columns, options?)

軽量なAppendセッションを開きます。デフォルトではネイティブのAPPEND open/data/closeフローを使用し、
成功したネイティブ書き込みはチャンクごとの応答を返しません。

```javascript
const stream = await conn.appendOpen('sensor_log', [
  { name: 'ID', type: 'int32' },
  { name: 'NAME', type: 'varchar' },
  { name: 'VALUE', type: 'float64' },
]);

await stream.append([
  [1, 'alpha', 0.5],
  [2, 'bravo', 1.25],
]);

await stream.append({ values: [3, 'charlie', 2.5] });
await stream.close();
```

ネイティブAppendを無効化し、プリペアドステートメント方式に固定するには`MACHBASE_NATIVE_APPEND=0`を
設定してください。サーバーが特定テーブルタイプやセッションでネイティブAppendをサポートしない場合は、
ファサードが自動的にプリペアドステートメント方式へフォールバックします。

TAGテーブルの`DATETIME`列には`Date`オブジェクトまたは`bigint`のエポック値を渡してください。

スパースARRAYは`appendOpen()`のARRAY値として渡せます。現在の`@machbase/ts-client`は`columns`引数が
必須のため、全行を入力する場合もテーブルの入力列を順番に定義します。`appendOpen(table)`や空の列リストに
よる自動推論はサポートしません。以下の例の`ID`、`A`がテーブルの全入力列なら全行入力です。
ARRAY内の入力位置は各行の`SparseArray`が決めます。

接続から4行の入力・Close・検索までの
[全列定義の例](../data-input-load-export/array-append/#node-full-columns)を参照してください。

Machbase DBMS 8.7.0の選択列Appendでは、`name`に通常の列または`ARRAY_COLUMN[position]`を指定します。
行ごとに異なる位置を入力する場合は、`SparseArray`を配列全体の対象に渡します。
要素位置を指定した対象と`SparseArray.set()`の位置は0始まりです。

```javascript
const { SparseArray } = require('@machbase/ts-client');

const stream = await conn.appendOpen('array_append_example', [
  { name: 'ID', type: 'int64' },
  { name: 'A', type: 'int32-array' },
]);
const sparse = new SparseArray(4).set(1, 200).set(3, 400);
await stream.append([[2n, sparse]]);
await stream.close();
```

`MACHBASE_NATIVE_APPEND=0`でprepared代替経路に固定した場合も、`SparseArray`をARRAY互換値として
処理します。全体例とNULLの区別は
[Sparse ARRAYと選択列Append API](../data-input-load-export/array-append/)を参照してください。

#### Appendストリームのappend(rows)

開いたAppendストリームに1行以上を送信します。

```javascript
const frames = await stream.append([
  ['S-001', new Date(), 1.0],
  ['S-002', new Date(Date.now() + 1), 2.0],
]);
console.log('frames sent:', frames);
```

ネイティブモードではスループットを最大化するため成功応答を省略し、エラー時だけ失敗パケットを返します。

### ヘルパーメソッド

#### ping()

`SELECT 1 FROM V$TABLES`で接続状態を確認します。

```javascript
await conn.ping();
```

#### promise()

使い慣れた`.promise()`形式のラッパーを提供します。

```javascript
const p = conn.promise();
await p.ping();
const [rows] = await p.query('SELECT NAME FROM V$TABLES ORDER BY NAME LIMIT ?', [5]);
```

#### escape, escapeId, format

SQL文字列を安全に組み立てるユーティリティです。

```javascript
const safeName = conn.escapeId('table_name');
const safeValue = conn.escape('user input');
```

## テストと診断

### スクリプト

- `npm run build` – TypeScriptのコンパイル
- `npm run lint` – `src/`にESLintを実行
- `npm run smoke` – 任意のスモークテスト（環境変数がなければ省略）
- `npm test` – 統合テストスイート（実サーバーが必要）
  1. LOGテーブルを作成
  2. サンプルデータのINSERT/SELECT
  3. 位置指定バインディングのプリペアドステートメントを実演
  4. Append負荷テスト（デフォルト: 5バッチ x 200行）と件数検証
  5. TRANSACTIONテーブルで直接SQLの`BEGIN`/`ROLLBACK`/`COMMIT`の動作を確認
  6. Machbaseファサードと`UPDATE`制限の動作を検証

サンプル出力:

```text
TRANSACTION transaction commit returned 1 row.
machbase-facade-basic callback query returned 3 rows.
machbase-facade-update-log-fails message: UPDATE is not supported for LOG tables.
append-batch progress: batch 4/5 { table: 'TS_CLIENT_IT_...', rowsAppended: 200, rowsFailed: 0 }
append-batch final count: 1004
```

## チュートリアル

### クイックスタート（LOGテーブル）

```javascript
// quickstart-log.js
const { createConnection } = require('@machbase/ts-client');

(async () => {
  const conn = createConnection({ host: '127.0.0.1', port: 5656, user: 'SYS', password: 'MANAGER' });
  await conn.connect();
  const table = 'JS_LOG_' + Math.random().toString(36).slice(2, 7).toUpperCase();
  try {
    await conn.execute(`CREATE LOG TABLE "${table}" (ID INTEGER, NAME VARCHAR(64), VALUE DOUBLE)`);
    await conn.execute(`INSERT INTO "${table}" VALUES (1, 'A', 0.5)`);
    const [rows] = await conn.query(`SELECT * FROM "${table}" ORDER BY ID`);
    console.table(rows);
  } finally {
    await conn.execute(`DROP TABLE "${table}"`);
    await conn.end();
  }
})();
```

### プリペアドステートメントの再利用

```javascript
// prepared-reuse.js
const { createConnection } = require('@machbase/ts-client');

(async () => {
  const conn = createConnection({ host: '127.0.0.1', user: 'SYS', password: 'MANAGER' });
  await conn.connect();
  const table = 'JS_VOL_' + Math.random().toString(36).slice(2, 7).toUpperCase();
  try {
    await conn.execute(`CREATE VOLATILE TABLE "${table}" (ID INTEGER PRIMARY KEY, NAME VARCHAR(64))`);
    for (let i = 1; i <= 3; i++) await conn.execute(`INSERT INTO "${table}" VALUES (${i}, 'N${i}')`);
    const stmt = await conn.prepare(`SELECT NAME FROM "${table}" WHERE ID = ?`);
    try {
      for (const id of [1, 2, 3]) {
        const [rows] = await stmt.execute([id]);
        console.log(id, rows[0]?.NAME);
      }
    } finally {
      await stmt.close();
    }
  } finally {
    await conn.execute(`DROP TABLE "${table}"`);
    await conn.end();
  }
})();
```

### LOGテーブルのバッチAppend

```javascript
// append-batch.js
const { createConnection } = require('@machbase/ts-client');

(async () => {
  const conn = createConnection({ host: '127.0.0.1', user: 'SYS', password: 'MANAGER' });
  await conn.connect();
  const table = 'JS_LOGAPP_' + Math.random().toString(36).slice(2, 7).toUpperCase();
  try {
    await conn.execute(`CREATE LOG TABLE "${table}" (ID INTEGER, NAME VARCHAR(64), VALUE DOUBLE)`);
    const result = await conn.appendBatch(
      table,
      [
        { name: 'ID', type: 'int32' },
        { name: 'NAME', type: 'varchar' },
        { name: 'VALUE', type: 'float64' },
      ],
      [[1, 'X', 0.5], [2, 'Y', 1.25]],
    );
    console.log(result);
  } finally {
    await conn.execute(`DROP TABLE "${table}"`);
    await conn.end();
  }
})();
```

### TAGテーブルのストリーミングAppend

```javascript
// append-tag-stream.js
const { createConnection } = require('@machbase/ts-client');

(async () => {
  const conn = createConnection({ host: '127.0.0.1', user: 'SYS', password: 'MANAGER' });
  await conn.connect();
  const table = 'JS_TAG_' + Math.random().toString(36).slice(2, 7).toUpperCase();
  try {
    await conn.execute(`CREATE TAG TABLE "${table}" (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE SUMMARIZED)`);
    const stream = await conn.appendOpen(table, [
      { name: 'NAME', type: 'varchar' },
      { name: 'TIME', type: 'int64' },
      { name: 'VALUE', type: 'float64' },
    ]);
    const now = Date.now();
    await stream.append([
      ['T-0001', new Date(now), 1.0],
      ['T-0002', new Date(now + 1), 2.0],
    ]);
    await stream.close();
    const [rows] = await conn.query(`SELECT COUNT(*) AS CNT FROM "${table}"`);
    console.log('count', rows[0]?.CNT);
  } finally {
    await conn.execute(`DROP TABLE "${table}"`);
    await conn.end();
  }
})();
```

> ネイティブモードはデフォルトで有効です。無効化には`MACHBASE_NATIVE_APPEND=0`を設定してください。
> 成功時のチャンクごとの応答は省略され、エラーだけが失敗応答として通知されます。

### PromiseラッパーとPing

```javascript
// promise-and-ping.js
const { createConnection } = require('@machbase/ts-client');

(async () => {
  const conn = createConnection({ host: '127.0.0.1', user: 'SYS', password: 'MANAGER' });
  await conn.connect();
  try {
    const p = conn.promise();
    await p.ping(); // SELECT 1 FROM V$TABLES
    const [rows] = await p.query('SELECT NAME FROM V$TABLES ORDER BY NAME LIMIT ?', [5]);
    console.log(rows.map(r => r.NAME));
  } finally {
    await conn.end();
  }
})();
```

## 動作特性と制限

### トランザクション

サーバーのSQLトランザクションはTRANSACTIONテーブルで動作しますが、ファサードのトランザクション用
便利メソッドは未実装です。同じ接続でSQLを直接実行します。

```javascript
await conn.execute('BEGIN');
await conn.execute('UPDATE orders SET status = ? WHERE order_id = ?', ['DONE', 1001]);
await conn.execute('COMMIT');
```

### 結果バッファリングとページネーション

ラッパーの`query`は結果セット全体をバッファリングしてから返します。大きなテーブルでは
`ORDER BY … LIMIT`クエリや主キー範囲を使用して、直接ページ分割してください。

### パラメーターバインディング

配列入力は位置指定プレースホルダー`?`に、オブジェクト入力は`:name`にバインドします。
サポートする型は`int32`、`int64`、`float64`、`varchar`などの汎用スカラー型です。
`null`を渡す場合は型も明示してください。

```javascript
{ value: null, type: 'varchar' }
```

名前の規則と最大パラメーター数は
[Named Bind Parameter syntax](../../reference/sql/syntax/named-bind-parameter-syntax/)を参照してください。

### Append API

LOGテーブルには`appendBatch`、段階的な入力には`appendOpen`/`append`を使用します。
特定のテーブルタイプ（例: TAGテーブル）でこの入力方式が非サポートの場合は、プリペアドステートメントの
繰り返し方式に自動置換されます。本番ではデータをチャンクに分け、`rowsFailed`を確認します。

### エラー処理

エラーは標準の`Error`オブジェクト（ラッパー使用時は`QueryError`）で通知されます。診断には
`error.message`または`QueryError`の`code`、`sql`フィールドを確認してください。統合テストでは、
存在しないテーブルの検索と非サポートの`UPDATE`を意図的に実行し、エラーメッセージが十分に説明的か
確認します。

### テーブルタイプ別のSQLの注意事項

- **LOGテーブル**は`UPDATE`をサポートしません。
- **TAGテーブル**のデータUPDATEはStandard Editionのみでサポートします。タグ選択条件とBASETIME条件が
  必要で、タグ名・時間軸・メタデータ列はデータUPDATEのSET対象にできません。
  SETの右辺で既存行の列を参照できません。
- **VOLATILEテーブル**のUPDATE/DELETEは主キー条件を使用します。**LOOKUPテーブル**は主キー条件と
  一般条件式の両方をサポートし、単一行の変更には主キー条件が効率的です。

## ベストプラクティス

1. **必ず接続を閉じる**: `try...finally`で`conn.end()`が呼ばれることを保証してください。
2. **プリペアドステートメントの再利用**: 一度作成して複数回実行すると性能が向上します。
3. **バッチ入力の活用**: 単一行INSERTではなく、`appendBatch`や`appendOpen`で大量ロードを行ってください。
4. **エラー処理**: DB操作を`try...catch`で囲み、適切にログ記録します。
5. **接続プールの使用**: 本番では接続プールを導入し、同時リクエストを安定して処理してください。
6. **クエリのパラメーター化**: SQLインジェクションを防ぐため、文字列連結ではなくバインディング
   （`?`プレースホルダー）を使用してください。
