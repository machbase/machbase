---
type: docs
title: '13.4 데이터 보존 정책'
weight: 30
---
Machbase는 시계열 데이터의 자동 삭제 기능인 **Retention Policy**를 제공합니다. 보존 기간과 삭제 주기를 정의한 정책을 생성한 후, 대상 테이블에 적용하면 지정된 주기마다 자동으로 오래된 데이터를 삭제합니다.

## 주요 개념

- **Duration**: 데이터를 보존할 기간. 이 기간을 초과한 데이터는 삭제 대상이 됩니다.
- **Interval**: 보존 기간 점검 주기. 이 주기마다 삭제 작업이 실행됩니다.

## 지원 테이블 타입

Retention Policy는 **TAG, KV, LOG 테이블**에 사용할 수 있습니다.

| 테이블 타입 | Retention Policy 적용 |
|------------|---------------------|
| TAG | O |
| KV | O |
| LOG | O |
| RDB | X |
| VOLATILE | X |
| LOOKUP | X |

RDB, VOLATILE, LOOKUP 테이블의 주기적 데이터 삭제는 별도의 애플리케이션 배치 로직으로 구현해야 합니다.

## 워크플로우

```
CREATE RETENTION → ALTER TABLE ADD RETENTION → (자동 삭제 운영) → ALTER TABLE DROP RETENTION → DROP RETENTION
```

## 하위 페이지

- [Retention Policy 상세](/dbms/operations-configuration-recovery/policy-data-retention/#retention-policy): 생성·적용·해제·삭제 전체 가이드


<a id="retention-policy"></a>

## Retention Policy

Retention Policy는 TAG, KV, LOG 테이블에 보존 기간을 설정하여 오래된 데이터를 자동으로 삭제하는 기능입니다.

### 전체 흐름

1. **[Retention Policy 생성](/dbms/operations-configuration-recovery/policy-data-retention/#create-retention-policy)**: 보존 기간·삭제 주기 정의
2. **[테이블에 적용](/dbms/operations-configuration-recovery/policy-data-retention/#retention-policy)**: `ALTER TABLE ... ADD RETENTION`
3. **[실행 상태 확인](/dbms/operations-configuration-recovery/policy-data-retention/#execution-status-check-state-retention)**: `V$RETENTION_JOB` 조회
4. **[적용 해제](/dbms/operations-configuration-recovery/policy-data-retention/#detach-retention-policy)**: `ALTER TABLE ... DROP RETENTION`
5. **[정책 삭제](/dbms/operations-configuration-recovery/policy-data-retention/#delete-retention-policy)**: `DROP RETENTION`

### 정책 목록 조회

적용 중인 정책과 테이블 정보는 다음 시스템 뷰로 확인합니다.

```sql
-- 생성된 Retention Policy 목록
SELECT * FROM M$RETENTION;

-- 정책이 적용된 테이블 목록
SELECT * FROM V$RETENTION_JOB;
```

### 권한

Retention Policy 생성·삭제는 **SYS 계정 권한**이 필요합니다. 정책 적용·해제는 테이블 소유자가 자신의 테이블에 대해 수행할 수 있습니다.

> 상세 권한 요건은 [Retention 적용 가능 테이블과 SYS 권한 제약](/dbms/operations-configuration-recovery/policy-data-retention/#applicable-privileges-retention-sys)을 참고하세요.

<a id="retention-policy-create-retention-policy"></a>

### Retention Policy 생성

`CREATE RETENTION` 구문으로 보존 기간과 삭제 주기를 정의한 정책을 생성합니다.

#### 구문

```sql
CREATE RETENTION policy_name
    DURATION duration_value {MONTH|DAY|HOUR|MIN|SEC}
    INTERVAL interval_value {DAY|HOUR|MIN|SEC}
```

- **policy_name**: 정책 이름
- **DURATION**: 데이터 보존 기간. 이 기간을 초과한 데이터는 삭제 대상
- **INTERVAL**: 삭제 작업 실행 주기

#### 예시

```sql
-- 1일 보존, 1시간마다 삭제 실행
CREATE RETENTION policy_1d_1h DURATION 1 DAY INTERVAL 1 HOUR;

-- 30일 보존, 1일마다 삭제 실행
CREATE RETENTION policy_30d DURATION 30 DAY INTERVAL 1 DAY;

-- 1개월 보존, 3일마다 삭제 실행
CREATE RETENTION policy_1m_3d DURATION 1 MONTH INTERVAL 3 DAY;

-- 1시간 보존, 10분마다 삭제 실행 (테스트용)
CREATE RETENTION policy_1h_10m DURATION 1 HOUR INTERVAL 10 MIN;

-- 30초 보존, 3초마다 삭제 (개발·디버깅용)
CREATE RETENTION policy_30s_3s DURATION 30 SEC INTERVAL 3 SEC;
```

#### 정책 목록 확인

```sql
SELECT * FROM M$RETENTION;
```

```
USER_ID     POLICY_NAME       DURATION    INTERVAL
--------------------------------------------------
1           POLICY_1D_1H      86400       3600
1           POLICY_30D        2592000     86400
1           POLICY_1M_3D      2592000     259200
```

DURATION과 INTERVAL 값은 초(second) 단위로 저장됩니다.

#### 설계 가이드

- **DURATION**: 비즈니스 요구사항과 규제 보관 의무(예: 3개월, 1년)를 기준으로 결정
- **INTERVAL**: 데이터 삭제 빈도. 너무 짧으면 시스템 부하 증가, 너무 길면 불필요한 데이터가 오래 남음. 일반적으로 DURATION의 1/10 ~ 1/30 수준 권장
- 동일한 정책을 여러 테이블에 공유 적용 가능

<a id="retention-policy-retention-policy"></a>

### Retention Policy 테이블 적용

생성된 Retention Policy를 TAG, KV, LOG 테이블에 적용합니다. 적용 후에는 지정된 INTERVAL마다 DURATION을 초과한 데이터가 자동으로 삭제됩니다.

#### 구문

```sql
ALTER TABLE table_name ADD RETENTION policy_name;
```

#### 예시

```sql
-- TAG 테이블에 정책 적용
ALTER TABLE sensor_tag ADD RETENTION policy_30d;

-- LOG 테이블에 정책 적용
ALTER TABLE event_log ADD RETENTION policy_7d;

-- KV 테이블에 정책 적용
ALTER TABLE raw_kv ADD RETENTION policy_30d;

-- 이미 생성된 정책을 다른 테이블에도 적용 (정책 공유)
ALTER TABLE raw_data ADD RETENTION policy_30d;
```

#### 적용 상태 확인

```sql
SELECT * FROM V$RETENTION_JOB;
```

```
USER_NAME   TABLE_NAME    POLICY_NAME    STATE     LAST_DELETED_TIME
--------------------------------------------------------------------
SYS         SENSOR_TAG    POLICY_30D     WAITING   NULL
SYS         EVENT_LOG     POLICY_7D      WAITING   NULL
```

- **STATE**: `WAITING`(대기 중), `RUNNING`(실행 중), `STOPPED`(중지)
- **LAST_DELETED_TIME**: 마지막 삭제 작업에 사용한 `DELETE ... BEFORE` 기준 시각 (NULL = 아직 기준 시각이 기록되지 않음)

#### 주의 사항

- 한 테이블에는 하나의 정책만 적용할 수 있습니다.
- 이미 정책이 적용된 테이블에 다른 정책을 적용하려면 먼저 기존 정책을 해제해야 합니다.
- 정책 적용 즉시 삭제가 실행되는 것은 아닙니다. 첫 번째 INTERVAL이 경과한 후부터 실행됩니다.
- TAG 테이블의 경우 BASETIME 컬럼 기준으로 DURATION이 적용됩니다.
- LOG 테이블의 경우 `_ARRIVAL_TIME` 컬럼 기준으로 DURATION이 적용됩니다.

<a id="retention-policy-detach-retention-policy"></a>

### Retention Policy 적용 해제

테이블에 적용된 Retention Policy를 해제합니다. 해제 후에는 데이터가 자동으로 삭제되지 않고 영구 보관됩니다.

#### 구문

```sql
ALTER TABLE table_name DROP RETENTION;
```

#### 예시

```sql
-- TAG 테이블에서 정책 해제
ALTER TABLE sensor_tag DROP RETENTION;

-- LOG 테이블에서 정책 해제
ALTER TABLE event_log DROP RETENTION;
```

#### 해제 후 상태 확인

```sql
-- V$RETENTION_JOB에서 해당 테이블이 사라져야 합니다
SELECT * FROM V$RETENTION_JOB;
```

정책 해제 후에는 `V$RETENTION_JOB`에서 해당 테이블 항목이 제거됩니다.

#### 일시 중지가 필요한 경우

데이터 마이그레이션이나 점검 중에 자동 삭제를 일시적으로 중단해야 할 때 사용합니다. 작업 완료 후 다시 정책을 적용하면 됩니다.

```sql
-- 정책 임시 해제
ALTER TABLE sensor_tag DROP RETENTION;

-- ... 점검 작업 수행 ...

-- 정책 재적용
ALTER TABLE sensor_tag ADD RETENTION policy_30d;
```

#### 주의 사항

- 정책 해제는 이미 삭제된 데이터를 복구하지 않습니다.
- 정책 해제 후 데이터는 `DROP TABLE` 또는 수동 `DELETE ... BEFORE`로만 삭제됩니다.
- 정책 자체(policy 객체)는 `DROP RETENTION`으로 별도 삭제해야 합니다. `DROP RETENTION`과 `ALTER TABLE DROP RETENTION`은 다른 명령입니다.

<a id="retention-policy-delete-retention-policy"></a>

### Retention Policy 삭제

더 이상 사용하지 않는 Retention Policy 객체를 삭제합니다.

#### 구문

```sql
DROP RETENTION policy_name;
```

#### 예시

```sql
DROP RETENTION policy_1d_1h;
DROP RETENTION policy_30d;
```

#### 적용 중인 정책 삭제 시 오류

Retention Policy가 하나 이상의 테이블에 적용 중이면 삭제할 수 없습니다.

```sql
-- 정책이 적용 중인 상태에서 삭제 시도
DROP RETENTION policy_1d_1h;
-- [ERR-02702: Policy (POLICY_1D_1H) is in use.]
```

#### 올바른 삭제 순서

1. 정책을 사용 중인 모든 테이블에서 먼저 해제
2. 정책 삭제

```sql
-- 1단계: 적용된 테이블 확인
SELECT * FROM V$RETENTION_JOB WHERE POLICY_NAME = 'POLICY_1D_1H';

-- 2단계: 각 테이블에서 정책 해제
ALTER TABLE sensor_tag DROP RETENTION;
ALTER TABLE event_log DROP RETENTION;

-- 3단계: 정책 삭제
DROP RETENTION policy_1d_1h;
-- Dropped successfully.
```

#### 삭제 후 확인

```sql
SELECT * FROM M$RETENTION;
-- 해당 정책 이름이 사라져야 합니다
```

#### 주의 사항

- 정책 삭제는 테이블 데이터에는 영향을 주지 않습니다. 이후에는 자동 삭제만 중단됩니다.
- 같은 이름의 정책을 재생성하려면 먼저 기존 정책을 삭제해야 합니다.

<a id="retention-policy-applicable-privileges-retention-sys"></a>

### Retention 적용 가능 테이블과 SYS 권한 제약

#### 적용 가능 테이블

Retention Policy는 **TAG, KV, LOG 테이블**에 적용할 수 있습니다. 소스 코드(`qpvRetention.c`) 기준으로, TAG_TABLE, KEYVALUE_TABLE, LOG_TABLE 이외의 테이블 타입에 Retention Policy를 적용하면 오류가 발생합니다.

| 테이블 타입 | Retention Policy 적용 |
|------------|---------------------|
| TAG | O |
| KV | O |
| LOG | O |
| RDB | X |
| VOLATILE | X |
| LOOKUP | X |

```sql
-- 오류: RDB 테이블에 적용 시
ALTER TABLE orders ADD RETENTION policy_30d;
-- → ERR_QP_RETENTION_INVALID_TABLE_TYPE (또는 유사한 오류)
```

#### 권한 제약

Retention Policy의 생성과 삭제는 **SYS 계정** 또는 SYS 권한을 가진 사용자만 수행할 수 있습니다.
정책 적용과 해제는 테이블 소유자가 자신의 테이블에 대해 수행할 수 있습니다.

```sql
-- SYS 계정으로 접속
machsql -u SYS -p MANAGER

-- Retention Policy 생성
CREATE RETENTION policy_30d DURATION 30 DAY INTERVAL 1 DAY;

-- 테이블에 적용
ALTER TABLE sensor_tag ADD RETENTION policy_30d;
```

일반 사용자(SYS 권한 없음)는 Retention Policy를 생성하거나 삭제할 수 없습니다. 다만 SYS가
생성한 정책을 자신의 테이블에 적용하거나 해제할 수 있습니다. 다른 사용자의 테이블에 정책을
적용하거나 해제하려고 하면 권한 오류가 발생합니다.

#### 정책 정보 확인 뷰

| 뷰 이름 | 설명 |
|--------|------|
| `M$RETENTION` | 생성된 Retention Policy 목록 (이름, DURATION, INTERVAL) |
| `V$RETENTION_JOB` | 정책이 적용된 테이블 목록과 실행 상태 |

```sql
-- 정책 목록
SELECT * FROM M$RETENTION;

-- 적용 상태
SELECT USER_NAME, TABLE_NAME, POLICY_NAME, STATE, LAST_DELETED_TIME
FROM V$RETENTION_JOB;
```

<a id="retention-policy-execution-status-check-state-retention"></a>

### Retention 실행 상태 확인

Retention Policy가 적용된 테이블의 실행 상태를 `V$RETENTION_JOB` 뷰로 모니터링합니다.

#### V$RETENTION_JOB 조회

```sql
SELECT USER_NAME, TABLE_NAME, POLICY_NAME, STATE, LAST_DELETED_TIME
FROM V$RETENTION_JOB;
```

```
USER_NAME   TABLE_NAME    POLICY_NAME    STATE     LAST_DELETED_TIME
--------------------------------------------------------------------
SYS         SENSOR_TAG    POLICY_30D     WAITING   2024-01-15 03:00:00
SYS         EVENT_LOG     POLICY_7D      RUNNING   2024-01-15 02:00:00
SYS         RAW_DATA      POLICY_30D     STOPPED   2024-01-15 01:00:00
```

#### STATE 값 의미

| STATE | 설명 |
|-------|------|
| `WAITING` | 다음 INTERVAL을 기다리는 상태 |
| `RUNNING` | 현재 삭제 작업 실행 중 |
| `STOPPED` | 작업 중지 상태 |

#### LAST_DELETED_TIME

마지막 삭제 작업에 사용한 `DELETE ... BEFORE` 기준 시각입니다. 벽시계 기준의 작업 완료 시각이
아닙니다. `NULL`이면 아직 기준 시각이 기록되지 않은 것입니다.

#### 적용 정책 전체 확인

```sql
-- 생성된 정책 전체 목록 (초 단위 값)
SELECT POLICY_NAME,
       DURATION / 86400 AS duration_days,
       INTERVAL / 3600  AS interval_hours
FROM M$RETENTION;
```

```
POLICY_NAME    DURATION_DAYS   INTERVAL_HOURS
---------------------------------------------
POLICY_30D     30              24
POLICY_7D      7               1
POLICY_1H_10M  0               0
```

#### 모니터링 쿼리 패턴

```sql
-- 현재 실행 중인 정책
SELECT TABLE_NAME, POLICY_NAME
FROM V$RETENTION_JOB
WHERE STATE = 'RUNNING';

-- 중지 상태인 정책 확인
SELECT TABLE_NAME, POLICY_NAME, STATE, LAST_DELETED_TIME
FROM V$RETENTION_JOB
WHERE STATE = 'STOPPED';
```

#### 삭제 실행 여부 확인

정책 적용 후 실제로 삭제가 일어나고 있는지 확인하는 방법:

```sql
-- 1. 적용 전 데이터 수 확인
SELECT COUNT(*) FROM sensor_tag;

-- 2. INTERVAL 경과 후 재확인
SELECT COUNT(*) FROM sensor_tag;
-- DURATION을 초과한 데이터가 감소했으면 정상 동작 중
```
