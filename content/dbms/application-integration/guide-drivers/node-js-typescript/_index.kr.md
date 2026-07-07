---
type: docs
title: 'Node.js / TypeScript'
weight: 40
---

## 개요

`@machbase/ts-client`는 Machbase CMI 프로토콜을 순수 TypeScript로 구현한 라이브러리입니다. Node.js 애플리케이션이 네이티브 바인딩 없이도 Machbase 서버에 연결해 SQL 실행, Prepared Statement, Append 프로토콜을 사용할 수 있습니다.

- 패키지: `@machbase/ts-client`
- Node.js 18 이상 (LTS 권장)
- 네이티브 바인딩 불필요 (순수 TypeScript)
- CommonJS / ESM / TypeScript 모두 지원
- TCP 소켓 사용 (브라우저 미지원)

## 설치

### npm / yarn / pnpm

```bash
npm install @machbase/ts-client
# 또는
yarn add @machbase/ts-client
# 또는
pnpm add @machbase/ts-client
```

### 오프라인 설치

`.tgz` 파일을 전달받은 경우:

```bash
npm install ./machbase-ts-client-1.0.0.tgz
```

### 설치 확인

```bash
node -e "const { createConnection } = require('@machbase/ts-client'); console.log(typeof createConnection === 'function' ? 'OK' : 'FAIL')"
```

## 빠른 시작

### TypeScript

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

const [rows, fields] = await conn.query(
    'SELECT NAME FROM V$TABLES ORDER BY NAME LIMIT ?', [5]
);
console.log(rows);

await conn.end();
```

### CommonJS (JavaScript)

```javascript
// quickstart.js
const { createConnection } = require('@machbase/ts-client');

async function main() {
    const conn = createConnection({
        host: '127.0.0.1',
        port: 5656,
        user: 'SYS',
        password: 'MANAGER',
    });
    await conn.connect();

    const [rows] = await conn.query(
        'SELECT NAME FROM V$TABLES ORDER BY NAME LIMIT ?', [10]
    );
    console.table(rows);

    await conn.end();
}

main().catch(err => console.error('Error:', err));
```

## 연결 설정

### createConnection(config)

| 매개변수 | 타입 | 기본값 | 설명 |
|----------|------|--------|------|
| `host` | string | `127.0.0.1` | Machbase 서버 IP 또는 호스트명 |
| `port` | number | `5656` | 리스너 포트 |
| `user` | string | – | 데이터베이스 사용자 |
| `password` | string | – | 비밀번호 |
| `database` | string | `data` | 데이터베이스 이름 |
| `clientId` | string | `NPM` | 서버 로그에 표시될 클라이언트 ID |
| `showHiddenColumns` | boolean | `false` | 숨김 컬럼 포함 여부 |
| `timezone` | string | 빈 값 | 타임존 식별자 |
| `connectTimeout` | number | `5000` | 소켓 연결 타임아웃(ms) |
| `queryTimeout` | number | `60000` | 명령별 타임아웃(ms) |

```javascript
const conn = createConnection({
    host: '192.168.1.10',
    port: 5656,
    user: 'SYS',
    password: 'MANAGER',
    timezone: '+09:00',
    connectTimeout: 10_000,
    queryTimeout: 30_000,
});
await conn.connect();
```

### 연결 종료

```javascript
// try...finally 패턴으로 항상 연결 종료를 보장합니다.
await conn.connect();
try {
    // ... 작업 수행 ...
} finally {
    await conn.end();
}
```

## SQL 실행

### execute() - DDL / DML

결과 집합을 반환하지 않는 명령(DDL, INSERT, DELETE)에 사용합니다.

```javascript
const { createConnection } = require('@machbase/ts-client');

(async () => {
    const conn = createConnection({ host: '127.0.0.1', user: 'SYS', password: 'MANAGER' });
    await conn.connect();
    try {
        // 테이블 생성
        const [create] = await conn.execute(
            'CREATE LOG TABLE demo (ID INTEGER, NAME VARCHAR(64), VALUE DOUBLE)'
        );
        console.log('Affected rows:', create.affectedRows); // DDL은 0

        // 데이터 삽입
        const [insert] = await conn.execute(
            "INSERT INTO demo VALUES (1, 'alpha', 0.5)"
        );
        console.log('Inserted rows:', insert.affectedRows); // 1
    } finally {
        await conn.execute('DROP TABLE demo').catch(() => {});
        await conn.end();
    }
})();
```

### query() - SELECT

행을 반환하는 쿼리에 사용합니다. `[rows, fields]` 형태의 2요소 배열을 반환합니다.

```javascript
const [rows, fields] = await conn.query(
    'SELECT ID, NAME, VALUE FROM demo ORDER BY ID'
);
console.table(rows);
console.log('Columns:', fields?.map(f => f.name));
```

## Prepared Statement

반복 실행 쿼리에는 Prepared Statement를 사용하면 성능이 향상됩니다.

```javascript
// prepared-reuse.js
const { createConnection } = require('@machbase/ts-client');

(async () => {
    const conn = createConnection({ host: '127.0.0.1', user: 'SYS', password: 'MANAGER' });
    await conn.connect();
    try {
        await conn.execute(
            'CREATE VOLATILE TABLE vt_demo (ID INTEGER PRIMARY KEY, NAME VARCHAR(64))'
        );
        for (let i = 1; i <= 5; i++) {
            await conn.execute(`INSERT INTO vt_demo VALUES (${i}, 'name-${i}')`);
        }

        // Prepared Statement 준비
        const stmt = await conn.prepare('SELECT NAME FROM vt_demo WHERE ID = ?');
        try {
            for (const id of [1, 3, 5]) {
                const [rows] = await stmt.execute([id]);
                console.log(`ID ${id}:`, rows[0]?.NAME);
            }
        } finally {
            await stmt.close(); // 서버 리소스 해제
        }
    } finally {
        await conn.execute('DROP TABLE vt_demo').catch(() => {});
        await conn.end();
    }
})();
```

### Prepared Statement 메서드

| 메서드 | 설명 |
|--------|------|
| `execute(params?)` | 실행 후 `[rows, fields]` 반환 |
| `getColumns()` | 컬럼 메타데이터 캐시 반환 |
| `getLastMessage()` | 최근 서버 메시지 확인 |
| `getStatementId()` | 내부 Statement ID 조회 |
| `close()` | 서버 리소스 정리 (여러 번 호출해도 안전) |

### NULL 및 타입 지정 바인딩

```javascript
// null을 전달할 때는 타입을 명시합니다.
await stmt.execute([
    { value: null, type: 'varchar' },
    { value: new Date(), type: 'varchar' },
    { value: 42, type: 'int32' },
]);
```

## Append 프로토콜

Append는 대량 데이터를 고속으로 적재할 때 사용합니다. 단건 `INSERT`보다 훨씬 빠른 성능을 제공합니다.

지원 컬럼 타입: `int32`, `int64`, `float64`, `varchar`

### appendBatch() - 로그 테이블 배치 Append

```javascript
// append-batch.js
const { createConnection } = require('@machbase/ts-client');

(async () => {
    const conn = createConnection({ host: '127.0.0.1', user: 'SYS', password: 'MANAGER' });
    await conn.connect();
    try {
        await conn.execute(
            'CREATE LOG TABLE log_demo (ID INTEGER, NAME VARCHAR(64), VALUE DOUBLE)'
        );

        const result = await conn.appendBatch(
            'log_demo',
            [
                { name: 'ID',    type: 'int32'   },
                { name: 'NAME',  type: 'varchar' },
                { name: 'VALUE', type: 'float64' },
            ],
            [
                [1, 'alpha', 0.5],
                [2, 'bravo', 1.25],
                { values: [3, 'charlie', 2.5], arrivalTime: Date.now() * 1_000_000 },
            ],
        );
        console.log('Appended:', result.rowsAppended);
        console.log('Failed:',   result.rowsFailed);
    } finally {
        await conn.execute('DROP TABLE log_demo').catch(() => {});
        await conn.end();
    }
})();
```

`appendBatch()` 반환값: `{ table, rowsAppended, rowsFailed, message }`

### appendOpen() - 스트리밍 Append

점진적으로 데이터를 유입할 때 사용합니다.

```javascript
// append-stream.js
const { createConnection } = require('@machbase/ts-client');

(async () => {
    const conn = createConnection({ host: '127.0.0.1', user: 'SYS', password: 'MANAGER' });
    await conn.connect();
    try {
        await conn.execute(
            'CREATE LOG TABLE stream_demo (ID INTEGER, NAME VARCHAR(64), VALUE DOUBLE)'
        );

        const stream = await conn.appendOpen('stream_demo', [
            { name: 'ID',    type: 'int32'   },
            { name: 'NAME',  type: 'varchar' },
            { name: 'VALUE', type: 'float64' },
        ]);

        // 배열 또는 객체 형태로 행 전송
        await stream.append([
            [1, 'alpha', 0.5],
            [2, 'bravo', 1.25],
        ]);
        await stream.append({ values: [3, 'charlie', 2.5] });

        await stream.close();

        const [rows] = await conn.query('SELECT COUNT(*) AS CNT FROM stream_demo');
        console.log('Count:', rows[0]?.CNT);
    } finally {
        await conn.execute('DROP TABLE stream_demo').catch(() => {});
        await conn.end();
    }
})();
```

### TAG 테이블 스트리밍 Append

```javascript
// append-tag.js
const { createConnection } = require('@machbase/ts-client');

(async () => {
    const conn = createConnection({ host: '127.0.0.1', user: 'SYS', password: 'MANAGER' });
    await conn.connect();
    try {
        await conn.execute(
            'CREATE TAG TABLE tag_demo (' +
            '  name VARCHAR(20) PRIMARY KEY,' +
            '  time DATETIME BASETIME,' +
            '  value DOUBLE SUMMARIZED' +
            ')'
        );

        const stream = await conn.appendOpen('tag_demo', [
            { name: 'NAME',  type: 'varchar' },
            { name: 'TIME',  type: 'int64'   },
            { name: 'VALUE', type: 'float64' },
        ]);

        const now = Date.now();
        await stream.append([
            ['T-0001', new Date(now),     1.0],
            ['T-0002', new Date(now + 1), 2.0],
            ['T-0003', new Date(now + 2), 3.0],
        ]);
        await stream.close();

        const [rows] = await conn.query('SELECT COUNT(*) AS CNT FROM tag_demo');
        console.log('TAG count:', rows[0]?.CNT);
    } finally {
        await conn.execute('DROP TABLE tag_demo').catch(() => {});
        await conn.end();
    }
})();
```

> **팁**: 로그 테이블 Append에는 `appendBatch()`를, TAG 테이블이나 점진적 유입에는 `appendOpen()`을 사용하세요.
> `MACHBASE_NATIVE_APPEND=0` 환경 변수를 설정하면 네이티브 Append를 비활성화하고 Prepared Statement 방식으로 전환합니다.

## 전체 예제: INSERT / SELECT / Append

```javascript
// full-example.js
const { createConnection } = require('@machbase/ts-client');

(async () => {
    const conn = createConnection({
        host: '127.0.0.1',
        port: 5656,
        user: 'SYS',
        password: 'MANAGER',
    });
    await conn.connect();
    console.log('Connected to Machbase.');

    try {
        // 1. 테이블 생성
        await conn.execute('DROP TABLE IF EXISTS ex_sensor');
        await conn.execute(
            'CREATE LOG TABLE ex_sensor (ID INTEGER, DEVICE VARCHAR(40), VALUE DOUBLE)'
        );
        console.log('Table created.');

        // 2. 단건 INSERT
        for (let i = 1; i <= 5; i++) {
            await conn.execute(
                `INSERT INTO ex_sensor VALUES (${i}, 'device-${i}', ${20.0 + i * 0.5})`
            );
        }
        console.log('Inserted 5 rows via INSERT.');

        // 3. SELECT
        const [rows] = await conn.query(
            'SELECT ID, DEVICE, VALUE FROM ex_sensor ORDER BY ID'
        );
        console.table(rows);

        // 4. Append로 추가 적재
        const result = await conn.appendBatch(
            'ex_sensor',
            [
                { name: 'ID',     type: 'int32'   },
                { name: 'DEVICE', type: 'varchar' },
                { name: 'VALUE',  type: 'float64' },
            ],
            [[6, 'device-6', 23.0], [7, 'device-7', 23.5], [8, 'device-8', 24.0]],
        );
        console.log(`Appended ${result.rowsAppended} rows.`);

        // 5. 최종 건수 확인
        const [countRows] = await conn.query('SELECT COUNT(*) AS CNT FROM ex_sensor');
        console.log('Total rows:', countRows[0]?.CNT);
    } finally {
        await conn.execute('DROP TABLE ex_sensor').catch(() => {});
        await conn.end();
        console.log('Connection closed.');
    }
})();
```

## Promise 래퍼와 ping()

```javascript
const { createConnection } = require('@machbase/ts-client');

(async () => {
    const conn = createConnection({ host: '127.0.0.1', user: 'SYS', password: 'MANAGER' });
    await conn.connect();
    try {
        // 연결 상태 확인
        await conn.ping();
        console.log('Ping OK');

        // promise() 래퍼 사용
        const p = conn.promise();
        const [rows] = await p.query('SELECT NAME FROM V$TABLES ORDER BY NAME LIMIT ?', [5]);
        console.log(rows.map(r => r.NAME));
    } finally {
        await conn.end();
    }
})();
```

## 오류 처리

```javascript
const { createConnection } = require('@machbase/ts-client');

(async () => {
    const conn = createConnection({ host: '127.0.0.1', user: 'SYS', password: 'MANAGER' });
    await conn.connect();
    try {
        // 존재하지 않는 테이블 조회
        const [rows] = await conn.query('SELECT * FROM non_existent_table');
    } catch (err) {
        console.error('Query error:', err.message);
        // QueryError의 경우 err.code, err.sql 필드도 확인 가능
    } finally {
        await conn.end();
    }
})();
```

### 자주 발생하는 오류

| 오류 | 원인 | 해결 방법 |
|------|------|-----------|
| `ECONNREFUSED` | 서버 미실행 또는 포트 불일치 | `machadmin -u`로 서버 상태 확인, 포트 및 방화벽 점검 |
| `Authentication failed` | 사용자/비밀번호 오류 | 계정 정보 확인, `machadmin -c`로 DB 생성 여부 확인 |
| `column count does not match` | Append 컬럼 수 불일치 | 대상 테이블 스키마와 컬럼 정의 확인 |

## 동작 특성과 한계

### 트랜잭션 미지원

Machbase는 모든 명령을 자동 커밋합니다. `BEGIN`, `COMMIT`, `ROLLBACK`은 항상 오류를 반환합니다.

```javascript
try {
    await conn.execute('COMMIT');
} catch (err) {
    console.log('Expected:', err.message);
    // Error: Machbase does not support transactions
}
```

### 테이블 타입별 SQL 제약

| 테이블 타입 | SELECT | INSERT | UPDATE | DELETE |
|-------------|--------|--------|--------|--------|
| LOG | 지원 | 지원 | 미지원 | 지원 |
| TAG | 지원 | 지원 | 미지원 | 지원 |
| VOLATILE | 지원 | 지원 | 지원 | 지원 |
| LOOKUP | 지원 | 지원 | 지원 | 지원 |

### 결과 버퍼링

`query()` 메서드는 전체 결과를 메모리에 버퍼링합니다. 대용량 테이블에서는 `LIMIT`나 키 범위를 이용해 페이지를 나누세요.

```javascript
// 페이지 단위로 조회
const pageSize = 1000;
let offset = 0;
while (true) {
    const [rows] = await conn.query(
        `SELECT * FROM big_table ORDER BY ID LIMIT ? OFFSET ?`,
        [pageSize, offset]
    );
    if (rows.length === 0) break;
    // 처리...
    offset += pageSize;
}
```

## 모범 사례

1. **항상 연결 닫기**: `try...finally` 블록으로 `conn.end()`가 반드시 호출되도록 합니다.
2. **Prepared Statement 재사용**: 동일 쿼리를 반복 실행할 때는 `prepare()`로 한 번 준비하고 재사용합니다.
3. **배치 입력 활용**: 단건 `INSERT` 대신 `appendBatch()`나 `appendOpen()`으로 대량 적재를 수행합니다.
4. **파라미터 바인딩 사용**: SQL 인젝션 방지를 위해 문자열 결합 대신 `?` 플레이스홀더를 사용합니다.
5. **오류 처리**: 모든 DB 작업을 `try...catch`로 감쌉니다.
6. **rowsFailed 확인**: Append 후에는 `rowsFailed`를 확인해 오류 여부를 점검합니다.
