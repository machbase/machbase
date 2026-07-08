---
type: docs
title: '입력이 실패할 때'
weight: 10
---

Append API를 통한 데이터 입력이 실패하는 경우 원인은 대부분 연결 상태, 테이블 정의, 데이터 형식, 디스크 상태 중 하나입니다. 오류 메시지를 단서로 삼아 해당 원인을 빠르게 좁혀 나가십시오.

## 주요 실패 원인

| 원인 | 증상 | 해당 항목 |
|------|------|-----------|
| 연결 끊김 | Connection reset 오류 반환 | [연결 끊김](#연결-끊김-connection-reset) |
| 대상 테이블 없음 | Table not found 오류 반환 | [테이블 없음](#대상-테이블이-없을-때) |
| 컬럼 타입 불일치 | Type mismatch 오류 반환 | [타입 불일치](#컬럼-타입-불일치) |
| 디스크 공간 부족 | 쓰기 실패, 서버 응답 없음 | [디스크 부족](#디스크-공간-부족) |
| 시간 역순 입력 | 입력은 되나 성능 급격히 저하 | [시간 역순 입력](#시간-역순-입력-log-테이블) |

## 진단 방법

Append 세션이 현재 어떤 상태인지 먼저 확인합니다.

```sql
-- Append 세션 확인
SELECT sess_id, id, state, query FROM v$stmt WHERE query LIKE '%APPEND%';
```

`state`가 `APPEND` 또는 `FETCH`로 고정되어 있다면 해당 세션이 중단된 것입니다. `sess_id`를 기억해 두고 아래 해결 방법을 적용하십시오.

## 오류별 해결 방법

| 오류 | 원인 | 해결 |
|------|------|------|
| `ERR-02097: Table not found` | 테이블명 오류 또는 테이블 미생성 | 테이블 이름 철자 확인, 없으면 `CREATE TABLE` 실행 |
| `ERR-02041: Type mismatch` | 컬럼 타입 불일치 | 데이터 형식과 테이블 스키마 비교 확인 |
| `Connection reset by peer` | 네트워크 단절 또는 서버 과부하 | 재연결 로직 추가, 서버 상태 확인 |
| `ERR-02268: Disk is full` | 디스크 공간 소진 | 불필요한 데이터 삭제 또는 디스크 확장 |

---

## 연결 끊김 (Connection reset)

Append 도중 네트워크가 단절되거나 서버가 과부하 상태에 빠지면 `Connection reset by peer` 오류가 발생합니다.

**확인 방법**

```bash
# 서버 상태 확인
machadmin -c

# 트레이스 로그에서 연결 관련 오류 확인
grep -i "reset\|disconnect\|abort" $MACHBASE_HOME/trc/machbase.trc | tail -20
```

**해결 방법**

- Append 클라이언트에 자동 재연결 로직(retry)을 구현합니다.
- 서버 과부하가 원인이라면 [쿼리가 느릴 때](../../performance/slow/)를 참고하십시오.
- 방화벽의 TCP 유휴 타임아웃 설정이 너무 짧지 않은지 확인합니다.

---

## 대상 테이블이 없을 때

`ERR-02097: Table not found` 오류는 테이블명이 틀렸거나 아직 테이블을 생성하지 않았을 때 발생합니다.

**확인 방법**

```sql
-- 테이블 존재 여부 확인
SELECT name, type FROM v$table WHERE name = 'SENSOR_LOG';
```

결과가 없으면 테이블이 존재하지 않는 것입니다.

**해결 방법**

- 테이블명의 대소문자와 철자를 확인합니다. Machbase의 테이블명은 기본적으로 대문자로 저장됩니다.
- 테이블이 없다면 적절한 `CREATE TABLE` 구문으로 먼저 생성합니다.

---

## 컬럼 타입 불일치

`ERR-02041: Type mismatch` 오류는 입력 데이터의 값 형식이 테이블 컬럼 타입과 맞지 않을 때 발생합니다.

**확인 방법**

```sql
-- 테이블 컬럼 정의 확인
DESC sensor_log;
```

반환된 컬럼 타입과 실제 입력 중인 데이터의 형식을 비교합니다.

**해결 방법**

- 입력 데이터에서 해당 컬럼의 값 형식(정수/실수/문자열/시간)을 확인합니다.
- 타임스탬프 컬럼의 경우 나노초 단위 정수값이어야 합니다. 밀리초나 초 단위로 잘못 입력하지 않았는지 확인합니다.

---

## 디스크 공간 부족

디스크가 가득 찬 경우 Append 쓰기가 실패하고 서버가 응답하지 않을 수 있습니다.

**확인 방법**

```bash
# 데이터 디렉토리의 디스크 사용량 확인
df -h $MACHBASE_HOME/dbs

# 트레이스 로그에서 디스크 관련 오류 확인
grep -i "disk\|space\|full\|write" $MACHBASE_HOME/trc/machbase.trc | tail -20
```

**해결 방법**

- 오래된 데이터를 삭제하거나 별도 파티션으로 데이터 경로를 이동합니다.
- `machbase.conf`에서 `DISK_COLUMNAR_TABLE_CHECKPOINT_INTERVAL_SECS` 설정을 확인해 체크포인트 주기를 조정합니다.
- 근본적인 해결이 어렵다면 데이터 보존 정책을 검토하십시오.

---

## 시간 역순 입력 (LOG 테이블)

LOG 테이블은 `_ARRIVAL_TIME` 컬럼이 단조 증가(monotonically increasing)하도록 설계되어 있습니다. 시간이 역순으로 입력되면 입력 자체는 성공하지만 다음과 같은 문제가 발생합니다.

- 내부 인덱스 재정렬로 인한 입력 성능 저하
- 파티션 경계가 불규칙해져 쿼리 성능 저하

**확인 방법**

```sql
-- 가장 최근 데이터와 가장 오래된 데이터의 시간 확인
SELECT MIN(_ARRIVAL_TIME), MAX(_ARRIVAL_TIME) FROM sensor_log;
```

입력 중인 데이터의 타임스탬프가 현재 테이블에 저장된 최댓값보다 과거 시간이라면 역순 입력이 발생하고 있는 것입니다.

**해결 방법**

- 소스에서 데이터를 수집하는 순서를 시간 순으로 정렬합니다.
- 과거 데이터를 일괄 재적재해야 한다면 별도 테이블에 넣은 뒤 시간 순으로 정렬하여 INSERT SELECT로 이관합니다.
- Collector를 사용한다면 소스 쿼리에 `ORDER BY timestamp ASC`를 명시합니다.
