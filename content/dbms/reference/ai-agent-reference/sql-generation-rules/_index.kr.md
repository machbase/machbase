---
type: docs
title: '17.8.8 sql-generation-rules'
weight: 80
toc: true
---

AI가 SQL을 생성할 때는 먼저 서버 Edition, table 타입, schema와 실제 문법 정본을 확인합니다.
일반 SQL처럼 보이더라도 다른 DBMS의 함수나 절을 추측해 사용하지 않습니다.

## 필수 SQL 규칙

### TAG 테이블 조회

TAG 테이블도 일반 `FROM table_name` 문법으로 조회합니다.

```sql
SELECT name, time, value
  FROM sensor_data
 WHERE name = 'temp_01'
 ORDER BY time DESC
 LIMIT 1;
```

최신 한 건을 자주 조회할 때는 `SCAN_BACKWARD` 힌트나 TAG 통계 뷰의
`RECENT_ROW_TIME`을 사용합니다. 구현되지 않은 `FROM TAG TABLE`이나 `RECENT n` 절을 만들지
않습니다.

```sql
SELECT /*+ SCAN_BACKWARD(sensor_data) */ name, time, value
  FROM sensor_data
 WHERE name = 'temp_01'
 LIMIT 1;
```

### 시간 표현

현재 시각은 `SYSDATE`, 상대 시간 계산은 `ADD_TIME` 또는 문법 사전의 상대 시간 표현을
사용합니다.

```sql
SELECT name, time, value
  FROM sensor_data
 WHERE time > ADD_TIME(SYSDATE, '0/0/0 -1:0:0');
```

SDK에 DATETIME을 바인드할 때는 해당 SDK가 문서화한 네이티브 시간 타입 또는 정수 단위를
사용합니다. 모든 SDK에 나노초 정수를 강제하지 않습니다.

### ROLLUP 조회

ROLLUP 결과는 생성된 ROLLUP 테이블의 실제 열과 `AVG`, `MIN`, `MAX`, `COUNT` 지원 범위를
정본에서 확인합니다. 구현되지 않은 `STAT(avg)` 형식을 생성하지 않습니다.

### 파라미터 바인딩

| SDK | 시작점 |
|---|---|
| Python | [Python 연동](/dbms/development-tools-integration/python/) |
| JDBC | [JDBC](/dbms/development-tools-integration/jdbc/) |
| Go | [Go 연동](/dbms/development-tools-integration/go/) |
| Node.js / TypeScript | [Node.js / TypeScript](/dbms/development-tools-integration/node-js-typescript/) |
| .NET | [.NET Connector](/dbms/development-tools-integration/net-connector/) |

문자열 결합으로 값을 SQL에 넣지 않고 positional 또는 named marker의 현재 지원 범위를
확인합니다.

## 생성 전 체크리스트

- 대상 database와 owner를 확인했는가
- table 타입이 DML을 지원하는가
- 예제의 모든 객체를 같은 페이지에서 생성했는가
- 현재 서버에 없는 함수·뷰·속성을 추측하지 않았는가
- 파괴적 SQL에 대상, 사전 조회, 백업과 되돌림 조건이 있는가
- SQL 문법은 [SQL 레퍼런스](/dbms/reference/sql/)와 대조했는가
