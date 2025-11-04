---
title: Node.js / TypeScript
type: docs
weight: 40
---

## 개요

Machbase TypeScript 클라이언트(`@machbase/ts-client`)는 Machbase CMI 프로토콜을 순수 TypeScript로 구현한 라이브러리입니다. Node.js 애플리케이션이 네이티브 바인딩 없이도 Machbase(스탠더드 에디션) 서버에 연결해 SQL 실행, 결과 조회, Prepared Statement 처리, 로그 데이터 Append를 수행할 수 있습니다.

이 문서는 설치 방법, 핵심 API, 실용적인 예제, 주의해야 할 동작 특성을 다룹니다.

## 설치

### 요구 사항

- Node.js 18 이상(LTS 권장)
- 접속 가능한 Machbase 서버(스탠더드 에디션)

### npm에서 설치

패키지 매니저로 설치합니다.

```bash
npm install @machbase/ts-client
# or
yarn add @machbase/ts-client
# or
pnpm add @machbase/ts-client
```

### 오프라인 설치

Machbase에서 `.tgz` 패키지를 전달받은 경우:

```bash
# example file name; your version may differ
npm install ./machbase-ts-client-0.9.0.tgz
```

### 설치 확인

```bash
python3 - <<'PY'
from machbaseAPI.machbaseAPI import machbase
print('machbaseAPI import ok')
cli = machbase()
print('isConnected():', cli.isConnected())
PY
```

> **참고**: 이 클라이언트는 Node.js에서 TCP 소켓을 사용하며, 브라우저용 라이브러리(웹소켓 전송)를 제공하지 않습니다.

## 빠르게 시작하기

아래 예제는 로컬 서버에 연결해 샘플 테이블을 생성하고 데이터를 삽입·조회한 뒤 세션을 종료하는 흐름을 보여줍니다.

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

### CommonJS 예제

```javascript
// quickstart.js (CommonJS, Node 18+)
const { createConnection } = require('@machbase/ts-client');

async function main() {
  const conn = createConnection({
    host: '127.0.0.1',
    user: 'SYS',
    password: 'MANAGER',
    port: 5656
  });
  await conn.connect();

  const [rows] = await conn.query('SELECT * FROM v$tables ORDER BY NAME LIMIT ?', [10]);
  console.table(rows);

  await conn.end();
}

main().catch(err => console.error('Unexpected failure:', err));
```

> **트랜잭션 안내:** Machbase는 모든 명령을 자동 커밋합니다. `BEGIN`, `COMMIT`, `ROLLBACK` 같은 명령은 항상 에러를 반환하므로, 트랜잭션을 지원하지 않음을 확인하는 용도로만 사용하십시오.

## 자주 발생하는 문제

- **ECONNREFUSED** – 서버가 실행 중인지(`machadmin -u`), 호스트와 포트가 맞는지, 방화벽이 리스너 포트(기본 5656)의 TCP 연결을 허용하는지 확인하세요.
- **Authentication failed** – 사용자/비밀번호를 다시 확인하고 대상 데이터베이스가 생성되어 있는지(`machadmin -c`) 점검하세요.

## API 참조

### 연결 관리

#### createConnection(config)

Machbase 리스너에 네트워크 세션을 열고 CMI 핸드셰이크를 완료합니다.

| 매개변수 | 타입 | 기본값 | 설명 |
|-----------|------|---------|-------------|
| `host` | string | `127.0.0.1` | Machbase 서버 IP 또는 호스트명 |
| `port` | number | `5656` | 리스너 포트 |
| `user` | string | – | 데이터베이스 사용자(기본 `SYS`) |
| `password` | string | – | 비밀번호(기본 `MANAGER`) |
| `database` | string | `data` | 데이터베이스 이름 |
| `clientId` | string | `CLI` | 서버 로그에 표시될 클라이언트 ID |
| `showHiddenColumns` | boolean | `false` | 메타데이터에 숨김 컬럼 포함 여부 |
| `timezone` | string | 빈 값 | 선택적 타임존 식별자 |
| `connectTimeout` | number | 5000 | 소켓 연결 타임아웃(ms) |
| `queryTimeout` | number | 60000 | 명령별 타임아웃(ms) |

```javascript
const conn = createConnection({ host: '192.168.1.10', user: 'SYS', password: 'MANAGER' });
await conn.connect();
```

소켓 연결 실패, 인증 오류, 핸드셰이크 응답 이상 시 프로미스가 reject됩니다.

#### connect()

서버와의 연결을 엽니다.

```javascript
await conn.connect();
```

#### end()

소켓 연결을 종료합니다. `end()` 호출 이후 추가 작업을 시도하면 에러가 발생합니다.

```javascript
await conn.end();
```

### SQL 실행

#### execute(sql, values?)

결과 집합을 반환하지 않을 수도 있는 명령을 실행합니다. DDL(`CREATE`, `ALTER`, `DROP`)이나 DML(`INSERT`, `UPDATE`, `DELETE`)에 사용하십시오.

```javascript
const [create] = await conn.execute('CREATE TABLE demo (ID INTEGER, NAME VARCHAR(32))');
console.log('Rows affected:', create.affectedRows); // -> 0 for DDL

const [insert] = await conn.execute("INSERT INTO demo VALUES (1, 'alpha')");
console.log('Rows affected:', insert.affectedRows); // -> 1
```

#### query(sql, values?)

행을 반환하는 쿼리를 실행합니다. 반환값은 `[rows, fields]` 형태의 2요소 튜플입니다.

```javascript
const [rows, fields] = await conn.query('SELECT ID, NAME FROM demo ORDER BY ID');
console.table(rows);
```

### Prepared Statement 사용

#### prepare(sql)

서버에 Prepared Statement를 생성합니다.

```javascript
const stmt = await conn.prepare('SELECT NAME FROM demo WHERE ID = ?');
try {
  const [rows] = await stmt.execute([1]);
  console.log(rows); // -> [ { NAME: 'alpha' } ]
} finally {
  await stmt.close();
}
```

반환된 객체에서 제공하는 메서드는 다음과 같습니다.

- `execute(parameters?)` – 문을 실행하고 `[rowsOrPacket, fields]`를 반환합니다.
- `getColumns()` – 컬럼 메타데이터 캐시를 반환합니다.
- `getLastMessage()` – 최근 서버 메시지를 확인합니다.
- `getStatementId()` – 내부 Statement ID를 조회합니다.
- `close()` – 서버 리소스를 정리합니다. 여러 번 호출해도 안전합니다.

#### Prepared Statement Examples

**Prepared SELECT 재사용:**

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
const upsert = await conn.prepare('INSERT INTO devices VALUES (?, ?, ?) ON DUPLICATE KEY UPDATE');
const [result] = await upsert.execute([deviceId, firstValue, firstValue]);
console.log('Affected rows:', result.affectedRows);
await upsert.close();
```

**타입 지정 인자와 NULL 처리:**

```javascript
await update.execute([
  { value: null, type: 'varchar' },
  { value: new Date(), type: 'varchar' },
  { value: 'sensor-200', type: 'varchar' },
]);
```

### Append Protocol

#### appendBatch(table, columns, rows, options?)

`CMI_APPEND_BATCH_PROTOCOL`을 사용해 **로그 테이블**에 행을 추가합니다. 사용자에게 보이는 컬럼만 전달하면 됩니다(로그 테이블에는 `_arrival_time`, `_rid`가 자동 포함됩니다).

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

지원 컬럼 타입: `int32`, `int64`, `float64`, `varchar`.

반환값은 `{ table, rowsAppended, rowsFailed, message }` 형태입니다.

> **팁**: "column count does not match" 오류는 대상 테이블이 로그 테이블이 아니거나, 컬럼 순서가 스키마와 일치하지 않을 때 발생합니다.

#### appendOpen(table, columns, options?)

경량 Append 세션을 엽니다. 기본적으로 네이티브 APPEND open/data/close 흐름을 사용합니다.

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

#### append(rows) on an append stream

열린 Append 스트림으로 하나 이상의 행을 전송합니다.

```javascript
const frames = await stream.append([
  ['S-001', new Date(), 1.0],
  ['S-002', new Date(Date.now() + 1), 2.0],
]);
console.log('frames sent:', frames);
```

### Helper Methods

#### ping()

`SELECT 1 FROM V$TABLES`로 연결 상태를 점검합니다.

```javascript
await conn.ping();
```

#### promise()

익숙한 `.promise()`와 같은 형태의 래퍼를 제공합니다.

```javascript
const p = conn.promise();
await p.ping();
const [rows] = await p.query('SELECT NAME FROM V$TABLES ORDER BY NAME LIMIT ?', [5]);
```

#### escape, escapeId, format

SQL 문자열을 안전하게 구성하기 위한 유틸리티입니다.

```javascript
const safeName = conn.escapeId('table_name');
const safeValue = conn.escape('user input');
```

## 튜토리얼

### 빠른 시작 (로그 테이블)

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

### Prepared Statement 재사용

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
    } finally { await stmt.close(); }
  } finally {
    await conn.execute(`DROP TABLE "${table}"`);
    await conn.end();
  }
})();
```

### 로그 테이블 배치 Append

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
      [ { name: 'ID', type: 'int32' }, { name: 'NAME', type: 'varchar' }, { name: 'VALUE', type: 'float64' } ],
      [ [1, 'X', 0.5], [2, 'Y', 1.25] ],
    );
    console.log(result);
  } finally {
    await conn.execute(`DROP TABLE "${table}"`);
    await conn.end();
  }
})();
```

### TAG 테이블 스트리밍 Append

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

### Promise 래퍼와 Ping

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

## 동작 특성과 한계

### 트랜잭션

Machbase는 모든 명령을 자동 커밋합니다. `BEGIN`, `COMMIT`, `ROLLBACK` 같은 트랜잭션 키워드는 항상 실패하며, 래퍼도 `QueryError`(`ERR_MACHBASE_NO_TX`)를 통해 동일하게 알립니다.

```javascript
try {
  await conn.execute('COMMIT');
} catch (err) {
  console.log('Expected error:', err.message);
  // Error: Machbase does not support transactions
}
```

### 결과 버퍼링 및 페이지네이션

래퍼의 `query` 메서드는 전체 결과 집합을 버퍼링한 뒤 반환합니다. 대용량 테이블에서는 `ORDER BY … LIMIT` 쿼리나 기본 키 범위를 이용해 직접 페이지를 나누세요.

### 파라미터 바인딩

지원 타입은 `int32`, `int64`, `float64`, `varchar` 등 범용 스칼라 타입입니다. `null`을 전달할 경우 명시적 타입을 함께 지정하세요.

```javascript
{ value: null, type: 'varchar' }
```

### Append 프로토콜

로그 테이블에는 `appendBatch`를, 점진적 유입이 필요한 경우 스트리밍 도우미(`appendOpen`/`append`)를 사용하세요. 특정 테이블 타입(예: TAG 테이블)에서 스트리밍을 지원하지 않으면 준비된 문 반복 방식으로 자동 대체됩니다.

### 오류 처리

오류는 기본 `Error` 객체(래퍼 사용 시 `QueryError`)로 전달됩니다. 문제를 진단하려면 `error.message` 또는 `QueryError`의 `code`, `sql` 필드를 확인하세요.
### 테이블 타입별 SQL 유의사항

- **LOG/TAG 테이블**은 `SELECT`, `INSERT`, `DELETE`를 지원하며 `UPDATE`는 사용할 수 없습니다.
- **VOLATILE/LOOKUP 테이블**은 모든 DML을 지원하지만, 인덱스를 올바르게 사용하려면 `WHERE` 절에 기본 키 조건을 포함해야 합니다.

## 모범 사례

1. **항상 연결을 닫기**: `try...finally` 블록으로 `conn.end()`가 호출되도록 보장하세요.
2. **Prepared Statement 재사용**: 한 번 생성한 후 여러 번 실행하면 성능이 향상됩니다.
3. **배치 입력 활용**: 단건 INSERT 대신 `appendBatch`나 `appendOpen`으로 대량 적재를 수행하세요.
4. **오류 처리**: DB 작업을 `try...catch`로 감싸고 적절히 로깅합니다.
5. **커넥션 풀 사용**: 운영 환경에서는 커넥션 풀을 도입해 동시 요청을 안정적으로 처리하세요.
6. **쿼리 파라미터화**: SQL 인젝션을 방지하려면 문자열 결합 대신 바인딩(`?` 플레이스홀더)을 사용하세요.
