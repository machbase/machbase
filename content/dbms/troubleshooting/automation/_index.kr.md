---
type: docs
title: '16.6 자동 처리 문제'
weight: 60
---
ROLLUP(TAG 데이터 자동 집계)과 STREAM(쿼리 결과 자동 적재) 기능이 정상 동작하지 않을 때 원인을 진단하고 복구하는 방법을 다룹니다.

## 이 섹션의 구성

| 페이지 | 내용 |
|--------|------|
| [ROLLUP 결과가 예상과 다를 때](/dbms/troubleshooting/automation/#rollup) | ROLLUP 상태 확인, 즉시 실행, 재계산 방법 |
| [STREAM이 실행되지 않을 때](/dbms/troubleshooting/automation/#execution-stream) | STREAM 중지 원인 진단 및 재시작 절차 |


<a id="execution-stream"></a>

## STREAM이 실행되지 않을 때

STREAM이 중지되거나 데이터가 적재되지 않을 때의 진단 및 복구 방법입니다.

{{< callout type="info" >}}
**참고**: 서버를 재시작해도 STREAM은 자동으로 재시작되지 않습니다. 서버 재시작 후에는 수동으로 STREAM을 시작해야 합니다.
{{< /callout >}}

### STREAM 상태 확인

현재 STREAM의 상태를 확인합니다.

```sql
SELECT * FROM v$streams;
```

| 컬럼 | 설명 |
|------|------|
| `name` | STREAM 이름 |
| `state` | 현재 상태 (`RUNNING`, `STOPPED`, `ERROR` 등) |
| `table_name` | 대상 테이블 이름 |
| `query_txt` | STREAM에 등록된 쿼리 |
| `last_ex_time` | 마지막 실행 시각 |
| `error_msg` | 최근 오류 메시지 |

### 원인별 진단

#### 1. STREAM이 STOPPED 상태

STREAM이 수동으로 중지되었거나 서버 재시작 후 자동 시작되지 않은 경우입니다.

**해결 방법**

```sql
-- STREAM 재시작
EXEC STREAM_START(stream_name);
```

상태가 `RUNNING`으로 바뀌었는지 확인합니다.

```sql
SELECT name, state FROM v$streams WHERE name = 'stream_name';
```

#### 2. 소스 또는 대상 테이블이 없음

STREAM 쿼리에서 참조하는 테이블이 삭제되었거나 이름이 변경된 경우입니다.

**확인 방법**

```sql
-- STREAM 쿼리 확인
SELECT name, table_name, query_txt, error_msg FROM v$streams;

-- 쿼리에서 참조하는 테이블 존재 여부 확인
SELECT name, type FROM m$sys_tables WHERE name IN ('SOURCE_LOG', 'DEST_TAG');
```

테이블이 없다면 테이블을 먼저 생성하고 STREAM을 재시작합니다.

#### 3. STREAM 쿼리 오류

STREAM 등록 쿼리에 문법 오류나 논리 오류가 있어 실행 중 실패하는 경우입니다.

**확인 방법**

```bash
# STREAM 관련 오류 로그 확인
grep -i "stream\|error" $MACHBASE_HOME/trc/machbase.trc | tail -30
```

**해결 방법**

STREAM을 삭제하고 올바른 쿼리로 재생성합니다.

```sql
-- 기존 STREAM 중지 및 삭제
EXEC STREAM_STOP(stream_name);
EXEC STREAM_DROP(stream_name);

-- 올바른 쿼리로 재생성
EXEC STREAM_CREATE(stream_name,
    'INSERT INTO dest_tag SELECT name, time, value FROM source_log;');

-- 재시작
EXEC STREAM_START(stream_name);
```

#### 4. 서버 재시작 후 STREAM이 실행되지 않음

STREAM은 서버 재시작 시 자동으로 재시작되지 않습니다. 서버가 재시작될 때마다 수동으로 시작해야 합니다.

**해결 방법**

서버 재시작 후 아래 명령으로 모든 STREAM을 확인하고 수동으로 시작합니다.

```sql
-- 중지된 STREAM 목록 확인
SELECT name FROM v$streams WHERE state <> 'RUNNING';

-- 각 STREAM 시작
EXEC STREAM_START(stream_name);
```

서버 시작 시 STREAM을 자동으로 시작하려면 초기화 스크립트에 `STREAM_START` 명령을 포함합니다.

### STREAM 재생성 전체 절차

STREAM에 문제가 있어 완전히 재생성해야 하는 경우 다음 순서를 따릅니다.

```sql
-- 1. STREAM 중지
EXEC STREAM_STOP(stream_name);

-- 2. STREAM 삭제
EXEC STREAM_DROP(stream_name);

-- 3. 새 쿼리로 STREAM 재생성
EXEC STREAM_CREATE(stream_name,
    'INSERT INTO dest_tag SELECT name, time, value FROM source_log;');

-- 4. STREAM 시작
EXEC STREAM_START(stream_name);

-- 5. 상태 확인
SELECT name, state FROM v$streams WHERE name = 'stream_name';
```

### STREAM 동작 확인

STREAM이 데이터를 정상 적재하는지 확인합니다.

```sql
-- 대상 테이블에 데이터가 들어오는지 확인
SELECT COUNT(*) FROM dest_tag;

-- 잠시 후 다시 확인하여 건수 증가 여부 확인
SELECT COUNT(*) FROM dest_tag;
```

건수가 증가하고 있다면 STREAM이 정상적으로 동작하는 것입니다.
