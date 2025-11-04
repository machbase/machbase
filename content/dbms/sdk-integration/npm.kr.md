---
layout : post
title : 'NPM modules'
type : docs
weight: 40
---

# Machbase TypeScript 클라이언트 (npm)

Machbase TypeScript 클라이언트(`@machbase/ts-client`)는 Machbase CMI 프로토콜을 순수 TypeScript로 구현한 라이브러리입니다. Node.js 애플리케이션이 Machbase(standard edition) 서버에 연결하여 SQL을 실행하고, 결과를 조회하고, 준비된 문을 사용하며, 네이티브 바인딩 없이도 로그 데이터 대량 append를 수행할 수 있습니다.

이 문서는 해당 npm 패키지의 한국어 제품 매뉴얼입니다. 설치, 핵심 API, 실용 예제, 동작상의 유의사항을 다루며 처음 사용하는 분도 빠르게 생산성을 낼 수 있도록 구성했습니다.

---

## 0. 일반 사용자 설치(웹에서 다운로드)

대부분의 사용자는 소스에서 빌드하지 않고 npm 레지스트리에서 패키지를 설치하면 됩니다.

사전 요구사항:

- Node.js 18 이상(LTS 권장)
- 접근 가능한 Machbase(standard edition) 서버

패키지 설치:

```bash
npm install @machbase/ts-client
# 또는
yarn add @machbase/ts-client
# 또는
pnpm add @machbase/ts-client
```

오프라인/망분리 환경(사내에서 제공한 `.tgz` 파일이 있는 경우):

```bash
# 파일명은 버전에 따라 달라질 수 있습니다.
npm install ./machbase-ts-client-0.9.0.tgz
```

사용 예시(ESM/TypeScript):

```ts
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

주의사항:

- 본 클라이언트는 Node.js용이며 TCP 소켓을 사용합니다. 브라우저 환경(웹 번들러/웹소켓 전용)에서는 동작하지 않습니다.
- 기본 자격 증명(`SYS`/`MANAGER`)은 로컬 테스트용 예시입니다. 운영 환경에서는 전용 계정/비밀번호를 사용하세요.

자주 발생하는 문제:

- ECONNREFUSED – 서버가 기동되어 있는지(`machadmin -u`), 호스트/포트가 맞는지, 방화벽에서 리스너 포트(기본 5656)가 허용되는지 확인하세요.
- 인증 실패 – 사용자/비밀번호를 확인하고, 대상 데이터베이스가 생성되어 있는지(`machadmin -c`) 확인하세요.

—

## 1. 설치 및 프로젝트 구조

```bash
cd npm/machbase-client
npm install       # 로컬 의존성 설치
npm run build     # TypeScript 소스 컴파일 → dist/
```

주요 디렉터리:

```
npm/machbase-client/
├─ package.json            # scripts: build / lint / test / smoke
├─ src/
│   ├─ connection.ts       # 코어 프로토콜 엔진(내부)
│   ├─ machbase.ts         # createConnection 페이사드
│   ├─ constants.ts        # 프로토콜 상수 및 헬퍼
│   ├─ marshal.ts          # 마샬 인코더/디코더 유틸리티
│   ├─ example-js/         # CommonJS 실행 예제(Node)
│   ├─ examples-ts/        # TypeScript 예제(dist/examples-ts로 컴파일)
│   └─ tests/
│       └─ integration.ts  # 종단 간 검증 스위트
└─ dist/                   # 컴파일된 JS + 타입 선언(.d.ts)
```

---

## 2. 빠른 시작(Quick Start)

```js
// quickstart.js (CommonJS, Node 18+)
const { createConnection } = require('@machbase/ts-client');

async function main() {
  const conn = createConnection({ host: '127.0.0.1', user: 'SYS', password: 'MANAGER', port: 5656 });
  await conn.connect();

  const [rows] = await conn.query('SELECT * FROM system_databases ORDER BY NAME LIMIT ?', [10]);
  console.table(rows);

  await conn.end();
}

main().catch(err => console.error('Unexpected failure:', err));
```

> 트랜잭션 알림: Machbase는 모든 문장을 자동 커밋합니다. `BEGIN`, `COMMIT`, `ROLLBACK` 같은 명령은 항상 오류를 반환하며, 트랜잭션 미지원 여부를 감지하는 용도로만 사용하십시오.

### 2.1 Machbase 페이사드

mysql2와 유사한 개발 경험을 선호한다면 `createConnection`으로 제공되는 페이사드를 사용할 수 있습니다.

```js
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

페이사드는 콜백과 프로미스 흐름(`.promise()`)을 모두 지원하며, 실패 시 `QueryError`를 발생시키고 서버 메시지를 전달합니다.

> 참고: `beginTransaction`, `commit`, `rollback`은 Machbase가 SQL 트랜잭션을 지원하지 않으므로 즉시 `QueryError`를 반환합니다. LOG/TAG 테이블을 대상으로 하는 `UPDATE`도 서버의 명시적 오류로 빠르게 실패합니다.

---

## 3. API 레퍼런스

공개 API는 `createConnection`이 반환하는 연결 페이사드와 몇 가지 헬퍼 타입으로 노출됩니다. 아래 각 함수는 매개변수, 동작상의 주의, 예제 코드와 함께 설명합니다.

### 3.1 `createConnection(config)` 및 `connect()`

Machbase 리스너에 네트워크 세션을 맺고 CMI 핸드셰이크를 완료합니다.

| 매개변수 | 타입 | 기본값 | 설명 |
|---------|------|--------|------|
| `host` | string | `127.0.0.1` | Machbase 서버의 호스트명 또는 IP |
| `port` | number | `5656` | 리스너 포트 |
| `user` | string | – | 데이터베이스 사용자(일반적으로 `SYS`) |
| `password` | string | – | 비밀번호(일반적으로 `MANAGER`) |
| `database` | string | `data` | 데이터베이스 이름 |
| `clientId` | string | `CLI` | 서버 로그에 표시될 클라이언트 식별자 |
| `showHiddenColumns` | boolean | `false` | 숨김 컬럼 메타데이터 포함 여부 |
| `timezone` | string | 빈 문자열 | 타임존 식별자(선택) |
| `connectTimeout` | number | 5000 | 소켓 연결 타임아웃(ms) |
| `queryTimeout` | number | 60000 | 명령별 타임아웃(ms) |

```js
const conn = createConnection({ host: '192.168.1.10', user: 'SYS', password: 'MANAGER' });
await conn.connect();
```

### 3.2 `execute(sql, values?)`

반환 행이 없는 문장을 실행합니다. DDL(`CREATE`, `ALTER`, `DROP`)이나 DML(`INSERT`, `UPDATE`, `DELETE`)에 사용합니다.

```js
const [create] = await conn.execute('CREATE TABLE demo (ID INTEGER, NAME VARCHAR(32))');
console.log('Rows affected:', create.affectedRows); // DDL은 보통 0

const [insert] = await conn.execute("INSERT INTO demo VALUES (1, 'alpha')");
console.log('Rows affected:', insert.affectedRows); // -> 1

await expectTransactionUnsupported(conn, 'COMMIT'); // 트랜잭션 미지원 동작 확인
```

통합 테스트에서 사용하는 보조 함수:

```js
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

### 3.3 `query(sql, values?)`

행을 반환하는 문장을 실행합니다. 페이사드는 `[rows, fields]` 형태의 2원 배열로 결과를 반환합니다(구조는 mysql2 기본값과 유사).

```js
const [rows, fields] = await conn.query('SELECT ID, NAME FROM demo ORDER BY ID');
console.table(rows);
```

### 3.4 `prepare(sql)` / `PreparedStatementInfo`

서버 측 준비문을 생성합니다.

```js
const stmt = await conn.prepare('SELECT NAME FROM demo WHERE ID = ?');
try {
  const [rows2] = await stmt.execute([1]);
  console.log(rows2); // -> [ { NAME: 'alpha' } ]
} finally {
  await stmt.close();
}
```

반환 객체의 주요 메서드:

- `execute(parameters?: MachbaseBindInput[])` – 문장을 실행하고 `[rowsOrPacket, fields]`를 반환합니다.
- `getColumns()` – 캐시된 컬럼 메타데이터를 돌려줍니다.
- `getLastMessage()` – 해당 준비문에서 마지막으로 받은 서버 메시지.
- `getStatementId()` – 내부 스테이트먼트 ID.
- `close()` – 서버 자원 해제(여러 번 호출해도 안전).

바인딩 값은 원시값 혹은 타입 지정 객체(`{ value, type }`)로 전달할 수 있습니다. 예: `[{ value: null, type: 'varchar' }]`.

#### 준비문 예제 모음

`npm run build` 후 `dist/examples/`에서 실행 가능한 스크립트를 제공합니다.

- `prepared-select-reuse.ts`: VOLATILE 테이블을 채우고 `SELECT ... WHERE DEVICE_ID = ?` 준비문을 여러 번 재사용하는 예제.
- `prepared-upsert.ts`: `INSERT ... ON DUPLICATE KEY UPDATE` 흐름을 보여주며 `affectedRows`를 점검.
- `prepared-nullable.ts`: 타입 지정 바인딩(예: `Date`)과 명시적 `NULL` 처리.

예) 준비문 재사용

```
npm run build
node dist/examples/prepared-select-reuse.js
```

예) `INSERT ... ON DUPLICATE KEY UPDATE`

```
npm run build
node dist/examples/prepared-upsert.js
```

예) 타입 지정 파라미터 및 명시적 `NULL`

```
npm run build
node dist/examples/prepared-nullable.js
```

### 3.5 Machbase 페이사드 헬퍼

`src/machbase.ts`에 페이사드 계층이 있습니다. 주요 진입점:

- **`createConnection(config)`** – Machbase 페이사드 연결을 생성합니다(설정 키: `host`, `port`, `user`, `password`, `database`, `timezone` 등).
- **`QueryError`** – 실패한 연산에 대해 발생하는 오류 클래스(코드/SQL 포함).
- **`connection.promise()`** – 프로미스 우선 래퍼를 돌려줍니다.
- **`PreparedStatementInfo.execute(values)`** – 서버 준비문을 콜백 또는 프로미스로 실행.

추가 헬퍼:

- **`ping()`** – `SELECT 1 FROM V$TABLES` 기반의 경량 헬스체크.
- **`escape`, `escapeId`, `format`** – SQL 문자열/식별자 이스케이프 및 단순 포맷팅.
- **`beginTransaction` / `commit` / `rollback`** – 항상 `ERR_MACHBASE_NO_TX` 오류(자동 커밋만 지원).

제약(페이사드가 노출):

- 트랜잭션 미구현 → 위 API는 즉시 `QueryError(ERR_MACHBASE_NO_TX)`를 콜백에 전달.
- Named parameter 바인딩(`{ id: 1 }`) 미지원 → `?` 자리 순서대로 배열 전달.
- LOG/TAG 테이블의 `UPDATE` 미지원 → 서버 오류를 그대로 전달.

### 3.6 `appendBatch(table, columns, rows, options?)`

`CMI_APPEND_BATCH_PROTOCOL`을 사용해 **로그 테이블**에 행을 append합니다. 사용자 가시 컬럼만 제공하면 되며(로그 테이블은 `_arrival_time`, `_rid`를 내포), 대상 테이블 유형에서 배치 프로토콜을 지원하지 않으면(TAG 등) 페이사드가 준비문 루프로 자동 폴백합니다.

```js
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

- 지원 타입: `int32`, `int64`, `float64`, `varchar`
- `rows`는 값 배열 또는 `{ values, arrivalTime }` 객체 배열을 받습니다. `null`은 Machbase 센티널 값으로 자동 인코딩됩니다.
- `options`는 `arrivalTime`(단일 기본값) 또는 `arrivalTimes`(행별 배열)를 지정할 수 있습니다.

### 3.7 `appendOpen(table, columns, options?)`

경량 append 세션을 엽니다. 기본값은 네이티브 APPEND(open/data/close) 사용이며(성공 경로는 청크별 응답 없음), 네이티브를 비활성화하고 준비문 기반으로 강제하려면 `MACHBASE_NATIVE_APPEND=0`을 설정하세요. 서버가 네이티브를 거부하거나 문제가 발생하면 자동으로 준비문 방식으로 폴백합니다.

```js
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

TAG 테이블은 `DATETIME` 컬럼을 노출합니다. `Date` 객체 또는 `bigint` 에폭 값을 전달하십시오. 전체 예제는 `src/examples/tagdata-append-stream.ts`를 참고하세요(기본적으로 준비문 폴백 사용).

### 3.8 append 스트림의 `append(rows)`

열려 있는 append 스트림에 한 번 이상 행을 전송합니다. 값 배열의 배열 또는 `values`와 선택적 `arrivalTime`을 가진 객체 배열을 허용합니다. 전송한 프레임 개수를 반환합니다. 네이티브 모드에서는 최대 성능을 위해 성공 응답이 생략되며, 오류는 실패 응답으로 전달됩니다.

```js
const frames = await stream.append([
  ['S-001', new Date(), 1.0],
  ['S-002', new Date(Date.now() + 1), 2.0],
]);
console.log('frames sent:', frames);
```

### 3.9 `close()`

기저 소켓을 닫습니다. `close` 이후의 모든 호출은 오류가 발생합니다.

```js
await conn.end();
```

---

## 5. 동작상의 유의사항 & 제한

### 5.1 트랜잭션

Machbase는 모든 문장을 자동 커밋합니다. `BEGIN`/`COMMIT`/`ROLLBACK`은 항상 실패하며, 페이사드도 동일하게 `QueryError`를 반환합니다.

### 5.2 결과 버퍼링 & 페이지네이션

`query`는 결과를 모두 수집한 뒤 반환합니다. 대용량 테이블은 `ORDER BY … LIMIT` 또는 기본키 범위를 사용해 페이지 단위로 조회하세요.

### 5.3 파라미터 바인딩

스칼라 타입(`int32`, `int64`, `float64`, `varchar`)을 지원합니다. `null`을 전달할 때는 `{ value: null, type: 'varchar' }`처럼 타입을 명시하세요.

### 5.4 Append 프로토콜

로그 테이블에는 `appendBatch`, 점진적 적재가 필요하면 `appendOpen`/`append`를 사용하세요. 서버가 해당 테이블 타입에서 네이티브 스트리밍을 지원하지 않으면 준비문 루프로 자동 폴백합니다.

### 5.5 에러 처리

오류는 표준 `Error`(또는 페이사드 사용 시 `QueryError`)로 전달됩니다. `error.message` 또는 `QueryError.code/sql`을 참고해 원인을 파악하세요.

### 5.6 Machbase SQL 특성(테이블 타입)

- LOG/TAG 테이블은 `SELECT`, `INSERT`, `DELETE`를 지원하고 `UPDATE`는 지원하지 않습니다.
- VOLATILE/LOOKUP 테이블은 모든 DML을 지원하지만, 성능 및 정확한 인덱스 접근을 위해 `WHERE` 절에 기본키가 반드시 포함되어야 합니다.

---

## 7. 변경 이력

### 2025‑10‑08

- 웹(레지스트리) 기반 일반 사용자 설치 방법과 오프라인(`.tgz`) 설치 방법을 추가했습니다.
- Node.js 전용(브라우저 비지원) 주의와 연결 문제 해결 팁을 보강했습니다.
- Machbase 테이블 타입별 SQL 제약 사항을 한눈에 볼 수 있도록 정리했습니다.


## 4. 테스트 & 진단

### 4.1 스크립트

- `npm run build` – TypeScript 컴파일
- `npm run lint` – `src/`에 ESLint 수행
- `npm run smoke` – 선택적 스모크 테스트(환경변수 없으면 생략)
- `npm test` – 통합 스위트(실서버 필요)
  1) 로그 테이블 생성
  2) 샘플 데이터 INSERT/SELECT
  3) 자리기반 바인딩 준비문 시연
  4) append 부하 테스트(기본: 5배치 × 200행) 및 건수 검증
  5) 각 단계에서 `COMMIT`을 호출하여 트랜잭션 미지원 동작 확인
  6) 페이사드(callback, promise, prepared) 시연 및 LOG/TAG 테이블 `UPDATE` 시 즉시 `QueryError` 확인

샘플 출력(발췌):

```
COMMIT expected failure: Expected COMMIT to fail because Machbase does not support transactions.
machbase-facade-basic callback query returned 3 rows.
machbase-facade-update-log-fails message: UPDATE is not supported for LOG tables.
append-batch progress: batch 4/5 { table: 'TS_CLIENT_IT_...', rowsAppended: 200, rowsFailed: 0 }
append-batch final count: 1004
```

### 4.2 트랜잭션 검증 헬퍼

통합 스위트는 아래 헬퍼로 `COMMIT`이 예상대로 실패하는지 확인합니다.

```js
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

---

## 5. 동작상의 메모 & 제한 사항

### 5.1 트랜잭션

Machbase는 모든 문장을 자동 커밋합니다. `BEGIN`, `COMMIT`, `ROLLBACK`은 항상 실패하며, 페이사드는 `ERR_MACHBASE_NO_TX`를 반환합니다. 통합 테스트(`npm test`)의 `direct-exec-*` 및 `machbase-facade-basic`에서 이 계약을 검증합니다.

### 5.2 결과 버퍼링 & 페이지네이션

페이사드의 `query`는 전체 결과를 메모리에 적재합니다. 대량 데이터는 `ORDER BY … LIMIT` 또는 PK 범위로 직접 페이지를 나누십시오.

### 5.3 파라미터 바인딩

지원 스칼라 타입은 `int32`, `int64`, `float64`, `varchar`입니다. `null`을 보낼 때는 `{ value: null, type: 'varchar' }`처럼 타입을 명시하여 올바른 Machbase 센티널이 전송되도록 하십시오.

### 5.4 Append 프로토콜

로그 테이블에는 `appendBatch`를, 점진적 적재가 필요하면 스트리밍 헬퍼(`appendOpen`/`append`)를 사용하십시오. 서버가 특정 테이블 유형에 대해 스트리밍을 지원하지 않으면(TAG 등) 페이사드가 자동으로 준비문 루프로 폴백하므로, 데이터를 청크로 나누고 `rowsFailed`를 확인하는 패턴을 권장합니다.

### 5.5 오류 처리

표준 API는 `Error`, 페이사드는 `QueryError`로 오류를 전달합니다. `error.message` 또는 `QueryError`의 `code`, `sql`을 확인하세요. 통합 스위트는 일부러 존재하지 않는 테이블 조회, 로그 테이블 `UPDATE` 등을 유발해 설명적인 오류가 유지되는지 검증합니다.

---

## 6. Tutorials

아래 예제는 파일로 저장 후 바로 실행할 수 있는 완결형 스니펫입니다. 각 스니펫은 자체적으로 테이블을 생성하고 정리(drop)합니다.

### 6.1 Quickstart (log table)

```js
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

### 6.2 Prepared statements (reuse)

```js
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

### 6.3 Batch append to a log table

```js
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

### 6.4 Streaming append to a TAG table

```js
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

> 네이티브 모드는 기본 활성화입니다. 비활성화하려면 `MACHBASE_NATIVE_APPEND=0`을 설정하세요. 성공 경로는 응답 패킷이 생략되어 최대 성능을 보장하며, 오류는 실패 응답으로 돌아옵니다.

### 6.5 Promise wrapper + ping

```js
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

---

## 7. 리비전 기록(Revision History)

### 2025‑10‑03

- TAG 예제(초보자용, 자체 정리 포함) 추가.
- `MACHBASE_NATIVE_APPEND` 동작과 네이티브 스트리밍이 불안정할 때의 TAG 자동 폴백 문서화.
- 네이티브 인코더 메모 보강(도착시간 기본값, 시간 단위—마이크로초).

### 2025‑10‑02

- Machbase 페이사드 도입(`createConnection`, `QueryError`, `.promise()`, 페이사드 준비문).
- 통합 테스트 확장(콜백/프로미스 커버리지, LOG/TAG `UPDATE` 거부 검증).
- 페이사드 예제 스크립트 추가 및 문서 갱신(트랜잭션/업데이트 제한 강조).

### 2025‑09‑30

- 자리기반 준비문 구현.
- 로그 테이블용 `appendBatch` 추가(null 처리, 성공 집계 포함).
- 가변 길이 필드 디코딩 정규화.
- DDL/DML/Prepared/Batch append를 포괄하는 통합 스위트 추가 및 트랜잭션 오류 로깅.
- 준비문 예제 스크립트(`prepared-select-reuse.ts`, `prepared-upsert.ts`, `prepared-nullable.ts`) 공개 및 문서에 참조 추가.
- 동작 중심 샘플(트랜잭션, 페이지네이션, 파라미터 바인딩, append 청크, 오류 처리) 보강 및 각 제한 사항을 실행 가능한 코드와 연결.

---
