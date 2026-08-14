---
type: docs
title: '18.10.8 sql-generation-rules'
weight: 80
toc: true
---

이 페이지는 AI 에이전트가 Machbase SQL 및 코드를 생성할 때 따라야 할 규칙을 정의합니다.

## 필수 SQL 규칙

### 규칙 1: TAG 테이블 조회 시 `FROM TAG TABLE` 필수

TAG 테이블을 조회할 때는 반드시 `FROM TAG TABLE` 문법을 사용해야 합니다. 일반 `FROM table_name`만 사용하면 오류가 발생하거나 올바른 결과를 얻지 못합니다.

```sql
-- 올바른 예
SELECT * FROM TAG TABLE sensor_data WHERE name = 'temp_01';

-- 잘못된 예 (오류 발생 가능)
SELECT * FROM sensor_data WHERE name = 'temp_01';
```

### 규칙 2: 최신값 조회 시 `RECENT n` 절 사용

최신 N개 행을 조회할 때는 `RECENT n` 절이 `ORDER BY time DESC LIMIT n`보다 효율적입니다.

```sql
-- 권장: RECENT 절 사용
SELECT * FROM TAG TABLE sensor_data WHERE name = 'temp_01' RECENT 1;

-- 비권장: ORDER BY + LIMIT (성능 낮음)
SELECT * FROM TAG TABLE sensor_data WHERE name = 'temp_01'
ORDER BY time DESC LIMIT 1;
```

### 규칙 3: TAG 테이블 대량 삽입은 Append API 권장

TAG 테이블에 데이터를 삽입할 때 SQL INSERT보다 Append API가 훨씬 빠릅니다. SDK별 Append 방법은 [sdk-api-selection-rules](../sdk-api-selection-rules/)를 참조하십시오.

### 규칙 4: DATETIME 바인딩은 나노초 정수 사용

Machbase의 `datetime` 타입은 내부적으로 나노초 단위 `int64`로 저장됩니다. 파라미터 바인딩 시 나노초 정수를 사용하십시오.

```python
# Python 예시: 나노초 타임스탬프 바인딩
import time
ts_nano = int(time.time() * 1_000_000_000)  # 현재 시각을 나노초로
cursor.execute("INSERT INTO sensor_data VALUES (%s, %s, %s)", ('temp_01', ts_nano, 25.3))
```

### 규칙 5: 상대 시간 계산은 상대 시간 리터럴 또는 `ADD_TIME` 사용

```sql
-- 최근 1시간 데이터 조회
SELECT * FROM TAG TABLE sensor_data
WHERE name = 'temp_01'
  AND time BETWEEN now - 1h AND now;

-- ADD_TIME 사용 예
SELECT * FROM TAG TABLE sensor_data
WHERE time > ADD_TIME(sysdate, '0/0/0 0:-30:0');
```

## SDK별 파라미터 바인딩 스타일

| SDK | 플레이스홀더 | 예시 |
|-----|------------|------|
| Python (machbaseAPI) | `%s`, `?`, `%(name)s`, `:name` | `conn.cursor(prepared=True).execute("SELECT * FROM t WHERE name = ?", ('v1',))` |
| Java JDBC | `?` | `pstmt.setString(1, "v1")` |
| Go (machgo / native) | `?`, `:name` | `conn.Query(ctx, "SELECT ... WHERE name = :name", api.Named("name", "v1"))` |
| Go (database/sql) | `?`, `:name` | `db.Query("SELECT ... WHERE name = :name", sql.Named("name", "v1"))` |
| .NET (MachConnector) | `?` | `cmd.Parameters.Add(new MachParameter { Value = "v1" })` |
| Machbase SQLCLI | `?` | `SQLBindParameter(...)` |
| ODBC | `?` | `SQLBindParameter(...)` |
| REST API | 해당 없음 | URL 파라미터 또는 JSON body로 값 직접 포함 |

> Python에서 `%s`와 `?`에는 sequence를, `%(name)s`와 `:name`에는 mapping을 전달합니다.
> 동일 SQL을 여러 호출에서 재사용할 때는 Python API 2.4의 `cursor(prepared=True)`를
> 사용합니다.

## ROLLUP 조회 규칙

ROLLUP 집계 결과를 조회할 때 집계 함수는 `STAT()` 형식을 사용합니다.

```sql
-- ROLLUP 결과 조회 예시
SELECT
    time,
    STAT(avg) AS avg_value,
    STAT(min) AS min_value,
    STAT(max) AS max_value,
    STAT(count) AS cnt
FROM rollup_sensor_data_hour
WHERE name = 'temp_01'
  AND time BETWEEN '2024-01-01' AND '2024-01-02';
```

## 주의해야 할 패턴

| 패턴 | 문제 | 올바른 방법 |
|------|------|------------|
| TAG 쓰기를 `BEGIN` 안에서 실행 | 활성 TRANSACTION 테이블 트랜잭션에는 TAG 쓰기를 포함할 수 없음 | TAG 쓰기는 트랜잭션 밖에서 실행 |
| Go `database/sql`에서 `db.Begin()` | 기본 isolation level에서 지원 | TRANSACTION 테이블 작업을 `BeginTx`/`Commit`/`Rollback`으로 감쌈 |
| Python에서 `?`에 mapping 전달 | `?`는 positional marker이므로 container 불일치 | sequence를 전달하거나 `:name`과 mapping 사용 |
| ROLLUP 집계에 `AVG()` 직접 사용 | ROLLUP 결과 컬럼 구조와 불일치 | `STAT(avg)` 형식 사용 |
| TAG 테이블에 일반 `FROM table_name` 사용 | 정상 문법 | 태그 선택자와 시간 조건을 WHERE에 작성 |
| LOG 테이블 `UPDATE` | LOG 테이블은 Append-only → 미지원 | 수정 불필요한 설계 권장 |

## 유용한 시스템 뷰 쿼리

```sql
-- 테이블 목록 확인
SELECT name, type FROM m$sys_tables ORDER BY name;

-- 테이블 컬럼 확인
SELECT name, type, length FROM m$sys_columns
WHERE table_name = 'SENSOR_DATA';

-- 현재 세션 확인
SELECT * FROM v$session;

-- 실행 중인 쿼리 확인
SELECT sess_id, id, state, query FROM v$stmt WHERE state != 'IDLE';
```
