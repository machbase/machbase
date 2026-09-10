---
title: Node.js / TypeScript
type: docs
weight: 40
toc: true
---

## 概要 {#overview}

Machbase TypeScript クライアント（`@machbase/ts-client`）は、CMI プロトコルを TypeScript だけで実装しています。Node.js から Standard Edition に接続し、SQL の実行、結果取得、プリペアードステートメント、Log データのバッチ APPEND を、ネイティブバインディングなしで利用できます。

インストール、主要 API、実用例、テスト手順、動作上の注意事項を説明します。

## インストール {#installation}

### 要件 {#requirements}

- Node.js 18 以降（LTS を推奨）
- 接続可能な Machbase Standard Edition サーバー

### npm からのインストール {#install-from-npm}

パッケージマネージャーでインストールします。

```bash
npm install @machbase/ts-client
# または
yarn add @machbase/ts-client
# または
pnpm add @machbase/ts-client
```

### オフラインインストール {#offline-installation}

Machbase から `.tgz` ファイルを取得した場合：

```bash
# ファイル名の例。バージョンにより異なる
npm install ./machbase-ts-client-1.0.0.tgz
```

### インストールの確認 {#verify-installation}

```bash
node -e "const { createConnection } = require('@machbase/ts-client'); console.log(typeof createConnection === 'function' ? 'ts-client import ok' : 'ts-client import failed')"
```

> **注意**：TCP ソケットを使用する Node.js 向けクライアントです。ブラウザー用ライブラリーではなく、WebSocket トランスポートはありません。
> DBMS Standard のソースパッケージでは、`@machbase/ts-client` のバージョンは 1.0.0 です。
>
> 本ガイドの既定の認証情報 `SYS`/`MANAGER` はローカルテスト用です。本番では専用のユーザーとパスワードを使用してください。

## クイックスタート {#quick-start}

ローカルサーバーに接続し、テーブルを作成して行を挿入し、読み取ってからセッションを閉じる例です。

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

### CommonJS の例 {#commonjs-example}

```javascript
// quickstart.js (CommonJS, Node 18+)
const { createConnection } = require('@machbase/ts-client');

async function main() {
  const conn = createConnection({
    host: '127.0.0.1',
    user: 'SYS',
    password: 'MANAGER',
    port: 5656,
  });
  await conn.connect();

  const [rows] = await conn.query('SELECT * FROM V$TABLES ORDER BY NAME LIMIT ?', [10]);
  console.table(rows);

  await conn.end();
}

main().catch(err => console.error('Unexpected failure:', err));
```

> **トランザクションの注意**：各ステートメントは自動コミットされます。`BEGIN`、`COMMIT`、`ROLLBACK` は常にエラーとなるため、トランザクションが未サポートであることの確認にのみ使用してください。

### Machbase ファサード {#machbase-facade}

他の Node.js SQL クライアントに近いインターフェースとして、`createConnection()` はコールバックと Promise の両方をサポートします。

```javascript
// facade-basic.js (CommonJS)
const { createConnection } = require('@machbase/ts-client');

async function bootstrap() {
  const conn = createConnection({ host: '127.0.0.1', user: 'SYS', password: 'MANAGER' });
  await conn.connect();
  try {
    const [rows, fields] = await conn.query('SELECT NAME FROM V$TABLES ORDER BY NAME LIMIT ?', [3]);
    console.log('rows', rows, 'fields', fields?.map(f => f.name));

    await new Promise((resolve, reject) =>
      conn.query('SELECT VALUE FROM V$SYSSTAT WHERE NAME = ?', ['SERVER_VERSION'], (err, result) => {
        if (err) return reject(err);
        console.log('callback result', result);
        resolve();
      })
    );
  } finally {
    await conn.end();
  }
}

bootstrap().catch(console.error);
```

コールバックと `.promise()` を利用でき、失敗時は `QueryError` を返し、サーバーメッセージも伝達します。

> **ファサードの制限**：SQL トランザクションが未サポートのため、`beginTransaction`、`commit`、`rollback` は直ちに `QueryError` を返します。LOG/TAG テーブルの `UPDATE` も、明示的なサーバーエラーで失敗します。

## よくある問題 {#common-issues}

- **ECONNREFUSED**：サーバーが起動済み（`machadmin -u`）か、ホストとポートが正しいか、ファイアウォールがリスナーポート（既定値 `5656`）への TCP 接続を許可しているか確認します。
- **認証失敗**：ユーザー名とパスワード、およびデータベースが作成済み（`machadmin -c`）か確認します。

## API リファレンス {#api-reference}

### 接続管理 {#connection-management}

#### createConnection(config) {#createconnectionconfig}

リスナーへのネットワークセッションを確立し、CMI ハンドシェイクを完了します。

| パラメーター | 型 | 既定値 | 説明 |
|-----------|------|---------|-------------|
| `host` | string | `127.0.0.1` | サーバーの IP アドレスまたはホスト名 |
| `port` | number | `5656` | リスナーポート |
| `user` | string | – | DB ユーザー（一般に `SYS`） |
| `password` | string | – | パスワード（一般に `MANAGER`） |
| `database` | string | `data` | データベース名 |
| `clientId` | string | `NPM` | サーバーログに表示するクライアント識別子 |
| `showHiddenColumns` | boolean | `false` | メタデータに隠し列を含める |
| `timezone` | string | 空 | 任意のタイムゾーン識別子 |
| `connectTimeout` | number | 5000 | ソケット接続のタイムアウト（ms） |
| `queryTimeout` | number | 60000 | コマンドごとのタイムアウト（ms） |

```javascript
const conn = createConnection({ host: '192.168.1.10', user: 'SYS', password: 'MANAGER' });
await conn.connect();
```

ソケット障害、認証失敗、想定外のハンドシェイク応答がある場合、Promise は reject されます。

#### connect() {#connect}

サーバーへの接続を開きます。

```javascript
await conn.connect();
```

#### `end()` {#end}

ソケットを閉じます。`end()` の呼び出し後に操作すると、エラーが発生します。

```javascript
await conn.end();
```

### SQL の実行 {#executing-sql}

#### execute(`sql`, values?) {#executesql-values}

行を返すとは限らないステートメントを実行します。DDL（`CREATE`、`ALTER`、`DROP`）やデータ変更（`INSERT`、`UPDATE`、`DELETE`）に使用します。

```javascript
const [create] = await conn.execute('CREATE TABLE demo (ID INTEGER, NAME VARCHAR(32))');
console.log('Rows affected:', create.affectedRows); // DDL では 0

const [insert] = await conn.execute("INSERT INTO demo VALUES (1, 'alpha')");
console.log('Rows affected:', insert.affectedRows); // -> 1

await expectTransactionUnsupported(conn, 'COMMIT');
```

統合テストで使用するヘルパー：

```javascript
async function expectTransactionUnsupported(conn, sql) {
  try {
    await conn.execute(sql);
    throw new Error(`Expected ${sql} to fail because Machbase does not support transactions.`);
  } catch (err) {
    const msg = err instanceof Error ? err.message : String(err);
    console.log(`${sql} expected failure:`, msg);
  }
}
```

#### query(sql, values?) {#querysql-values}

行を返すステートメントを実行します。ファサードでは `[rows, fields]` の 2 要素タプルを返します。

```javascript
const [rows, fields] = await conn.query('SELECT ID, NAME FROM demo ORDER BY ID');
console.table(rows);
```

### プリペアードステートメント {#prepared-statements}

#### prepare(`sql`) {#preparesql}

サーバー上にプリペアードステートメントを作成します。

```javascript
const stmt = await conn.prepare('SELECT NAME FROM demo WHERE ID = ?');
try {
  const [rows] = await stmt.execute([1]);
  console.log(rows); // -> [ { NAME: 'alpha' } ]
} finally {
  await stmt.close();
}
```

戻り値のオブジェクトは、次のメソッドを持ちます。

- `execute(parameters?)`：実行し、`[rowsOrPacket, fields]` を返します。
- `getColumns()`：キャッシュした列メタデータを返します。
- `getLastMessage()`：ステートメントの最新のサーバーメッセージを返します。
- `getStatementId()`：内部のステートメント識別子を返します。
- `close()`：サーバーリソースを解放します。複数回呼び出しても安全です。

#### プリペアードステートメントの例 {#prepared-statement-examples}

**プリペアード `SELECT` の再利用：**

```javascript
const select = await conn.prepare('SELECT DEVICE_ID, SENSOR_VALUE FROM sensors WHERE DEVICE_ID = ?');
for (const { id } of samples) {
  const [rows] = await select.execute([id]);
  console.log(`selected ${id}:`, rows);
}
await select.close();
```

**プリペアード upsert：**

```javascript
const upsert = await conn.prepare(
  'INSERT INTO devices (DEVICE_ID, SENSOR_VALUE) VALUES (?, ?) ' +
  'ON DUPLICATE KEY UPDATE SET SENSOR_VALUE = ?',
);
const [result] = await upsert.execute([deviceId, firstValue, firstValue]);
console.log('Affected rows:', result.affectedRows);
await upsert.close();
```

**型付きパラメーターと NULL：**

```javascript
await update.execute([
  { value: null, type: 'varchar' },
  { value: new Date(), type: 'varchar' },
  { value: 'sensor-200', type: 'varchar' },
]);
```

実行用のサンプルは、通常 `npm run build` 後に `dist/examples/` に作成されます。環境変数は通常 `MACHBASE_EXAMPLE_*`、`MACHBASE_SMOKE_*` の順に参照し、どちらもなければ `SYS/MANAGER@127.0.0.1` を使用します。

### Append プロトコル {#append-protocol}

#### appendBatch(table, columns, rows, options?) {#appendbatchtable-columns-rows-options}

`CMI_APPEND_BATCH_PROTOCOL` で **Log テーブル**に行を追加します。ユーザーから見える列だけを指定してください。Log テーブルには `_arrival_time` と `_rid` が暗黙に含まれます。

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
    { values: [2, 'bravo', 1.25], arrivalTime: Date.now() * 1_000_000 },
  ],
);
console.log('Appended rows:', appendResult.rowsAppended);
```

サポートする列型：`int32`、`int64`、`float64`、`varchar`。

- `rows`には、各行の値配列、または`{ values, arrivalTime }`オブジェクトを並べた配列を指定できます。`null`はMachbaseの専用値に自動変換されます。
- `options` には、共通の `arrivalTime` または行ごとの配列 `arrivalTimes` を指定できます。

Promise は `{ table, rowsAppended, rowsFailed, message }` を返します。

> **ヒント**：column count does not match は、対象が Log テーブルでないか、列がスキーマ順になっていない場合に発生します。TAG テーブルでは `appendOpen()` を使用してください。

#### appendOpen(table, columns, options?) {#appendopentable-columns-options}

軽量な APPEND セッションを開きます。既定ではネイティブ APPEND の open/`data`/close を使用し、書き込み成功時にチャンクごとの応答は返しません。

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

ネイティブ APPEND を無効にしてプリペアードステートメントへ切り替えるには、`MACHBASE_NATIVE_APPEND=0` を設定します。テーブル型やセッションに対してサーバーがネイティブ APPEND を拒否した場合も、自動的に切り替わります。

TAG テーブルの `DATETIME` 列には、`Date` オブジェクトまたは `bigint` のエポック値を渡します。

#### APPEND ストリームの append(rows) {#appendrows-on-an-append-stream}

開いている APPEND ストリームに 1 行以上を送信します。

```javascript
const frames = await stream.append([
  ['S-001', new Date(), 1.0],
  ['S-002', new Date(Date.now() + 1), 2.0],
]);
console.log('frames sent:', frames);
```

ネイティブモードではスループット向上のため成功応答を省略します。エラー時は失敗パケットが返ります。

### ヘルパーメソッド {#helper-methods}

#### ping() {#ping}

`SELECT 1 FROM V$TABLES` でヘルスチェックします。

```javascript
await conn.ping();
```

#### promise() {#promise}

`.promise()` と同様の、Promise を中心としたラッパーを返します。

```javascript
const p = conn.promise();
await p.ping();
const [rows] = await p.query('SELECT NAME FROM V$TABLES ORDER BY NAME LIMIT ?', [5]);
```

#### escape, escapeId, format {#escape-escapeid-format}

SQL 文字列を安全に組み立てる補助関数です。

```javascript
const safeName = conn.escapeId('table_name');
const safeValue = conn.escape('user input');
```

## テストと診断 {#testing--diagnostics}

### スクリプト {#scripts}

- `npm run build`：TypeScript をコンパイルします。
- `npm run lint`：`src/` に ESLint を実行します。
- `npm run smoke`：任意のスモークテストです。環境変数がなければスキップします。
- `npm test`：稼働中のサーバーを必要とする統合テストです。
  1. Log テーブルを作成します。
  2. サンプルデータを挿入して検索します。
  3. 位置パラメーターをバインドしたプリペアードステートメントを確認します。
  4. APPEND の負荷テスト（既定：5 バッチ × 200 行）を行い、件数を確認します。
  5. 各段階で `COMMIT` を発行し、想定どおりのトランザクションエラーを確認します。
  6. ファサードを確認し、トランザクションと LOG/TAG の `UPDATE` が直ちに `QueryError` になることを検証します。

コンソール出力の例：

```text
COMMIT expected failure: Expected COMMIT to fail because Machbase does not support transactions.
machbase-facade-basic callback query returned 3 rows.
machbase-facade-update-log-fails message: UPDATE is not supported for LOG tables.
append-batch progress: batch 4/5 { table: 'TS_CLIENT_IT_...', rowsAppended: 200, rowsFailed: 0 }
append-batch final count: 1004
```

## チュートリアル {#tutorials}

### クイックスタート（Log テーブル） {#quickstart-log-table}

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

### プリペアードステートメントの再利用 {#prepared-statements-reuse}

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

### Log テーブルへのバッチ APPEND {#batch-append-to-a-log-table}

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

### TAG テーブルへのストリーミング APPEND {#streaming-append-to-a-tag-table}

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

> ネイティブモードは既定で有効です。`MACHBASE_NATIVE_APPEND=0` で無効にできます。成功時はチャンクごとの応答がなく、エラーは返されます。

### Promise ラッパーと Ping {#promise-wrapper--ping}

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

## 動作上の注意と制限 {#behaviour-notes--limitations}

### トランザクション {#transactions}

各文は自動コミットされます。`BEGIN`、`COMMIT`、`ROLLBACK` は常に失敗し、ファサードは指定したコールバックに `QueryError`（`ERR_MACHBASE_NO_TX`）を渡します。

```javascript
try {
  await conn.execute('COMMIT');
} catch (err) {
  console.log('Expected error:', err.message);
  // エラー：Machbase はトランザクションをサポートしない
}
```

### 結果のバッファリングとページ分割 {#result-buffering--pagination}

ファサード接続の `query` は、全行をバッファーに格納してから結果を返します。大きなテーブルは `ORDER BY … LIMIT` や主キー範囲で手動でページ分割してください。

### パラメーターバインド {#parameter-binding}

型付きバインドは `int32`、`int64`、`float64`、`varchar` をサポートします。`null` を渡すときも具体的な型を指定します。

```javascript
{ value: null, type: 'varchar' }
```

### Append プロトコル {#append-protocol-1}

Log テーブルには `appendBatch`、逐次取り込みには `appendOpen` / `append` を使用します。対象のテーブル型（例：TAG）でサーバーがストリーミングをサポートしない場合、プリペアードステートメントの反復へ自動的に切り替わります。データを分割して `rowsFailed` を確認し、必要に応じて再試行してください。

### エラー処理 {#error-handling}

エラーは標準の `Error`、またはファサードの `QueryError` として伝達されます。`error.message` や `QueryError` の `code`、`sql` を確認して診断します。統合テストでは、存在しないテーブルや未サポートの `UPDATE` も意図的に実行し、メッセージが明確か確認します。

### テーブル型ごとの SQL 動作 {#table-type-sql-semantics}

- **LOG と TAG**：`SELECT`、`INSERT`、`DELETE` をサポートし、`UPDATE` はサポートしません。
- **VOLATILE と LOOKUP**：すべての DML をサポートします。適切なインデックスアクセスと性能のため、`WHERE` 句に主キーを含めてください。

## 推奨事項 {#best-practices}

1. **接続を必ず閉じる**：try-finally で `conn.end()` の実行を保証します。
2. **プリペアードステートメントを再利用する**：1 度作成し、繰り返し実行します。
3. **挿入をまとめる**：大量入力には個別の `INSERT` より `appendBatch` や `appendOpen` を使用します。
4. **エラーを処理する**：DB 操作を try-catch で囲み、適切に記録します。
5. **コネクションプールを使用する**：本番では複数の同時リクエストを管理するプールを実装します。
6. **クエリーをパラメーター化する**：SQL インジェクションを防ぐため、文字列連結ではなく `?` のバインドを使用します。

## 改訂履歴 {#revision-history}

### 2025-10-08 {#2025-10-08}

- npm、yarn、pnpm、オフライン `.tgz` のインストール手順を追加。
- Node.js 専用という要件と、接続時のトラブルシューティングを補足。
- テーブル型ごとの SQL 制約を整理。

### 2025-10-03 {#2025-10-03}

- TAG ストリーミング例と、`MACHBASE_NATIVE_APPEND` の既定動作を追加。
- ストリーミング非対応時の、プリペアードステートメントへの自動切り替えを説明。

### 2025-10-02 {#2025-10-02}

- Machbase ファサード（`createConnection`、`QueryError`、`.promise()`、ファサードのプリペアードステートメント）を導入。
- コールバック、Promise、LOG/TAG の `UPDATE` 拒否のテストを拡充。

### 2025-09-30 {#2025-09-30}

- 位置パラメーターバインド付きのプリペアードステートメントを追加。
- NULL 処理と結果統計を含む、Log テーブル用 `appendBatch` を追加。
- トランザクション、ページ分割、バインド、APPEND 分割、エラー処理のテストと実行例を追加。
