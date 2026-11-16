---
type: docs
title: '15.5 데이터 보존 정책'
weight: 150
toc: true
---

Retention Policy는 TAG, KV, LOG 테이블에서 기준 시각보다 오래된 데이터를 주기적으로
삭제합니다. `DURATION`은 보존 기간이고 `INTERVAL`은 삭제 작업의 실행 주기입니다.
DBMS 8.9에서는 테이블에 연결할 때 `START AT`으로 최초 실행 기준 시각도 지정할 수 있습니다.
TRANSACTION, VOLATILE, LOOKUP 테이블에는 적용할 수 없습니다.

```text
정책 생성 → 테이블 적용 → 실행 상태 확인 → 테이블에서 해제 → 정책 삭제
```

<a id="retention-policy"></a>

## Retention Policy

운영 정책을 만들기 전에 법적 보관 의무, 복구 요구사항, 시간당 유입량과 삭제 부하를 함께
검토합니다. 고정 비율로 `INTERVAL`을 정하지 말고 운영 환경에서 측정한 삭제 시간보다 충분히
긴 주기를 사용하십시오.

정책과 적용 상태는 다음 뷰에서 확인합니다.

```sql
SELECT * FROM M$RETENTION;
SELECT USER_NAME, TABLE_NAME, POLICY_NAME, STATE,
       LAST_DELETED_TIME, START_TIME, NEXT_RUN_TIME
  FROM V$RETENTION_JOB;
```

<a id="create-retention-policy"></a>
<a id="retention-policy-create-retention-policy"></a>

### Retention Policy 생성

```sql
CREATE RETENTION policy_name
    DURATION duration_value {MONTH|DAY|HOUR|MIN|SEC}
    INTERVAL interval_value {DAY|HOUR|MIN|SEC};
```

`DURATION`은 월부터 초까지, `INTERVAL`은 `DAY`부터 `SEC`까지 지정할 수 있습니다. `MONTH`는 달력
월이 아니라 고정 30일이므로 법적 보관처럼 달력 경계가 중요한 정책은 `DAY` 단위로 환산하고
실제 삭제 기준을 검증합니다. 정확한 파서 문법과 적용 가능한 테이블 타입은
[RETENTION 문법](/dbms-8.9/reference/sql/syntax/retention-syntax/)을 참고합니다.

예를 들어 30일을 보존하고 하루마다 삭제 대상을 처리하는 정책은 다음과 같습니다.

```sql
CREATE RETENTION policy_30d DURATION 30 DAY INTERVAL 1 DAY;
SELECT * FROM M$RETENTION WHERE POLICY_NAME = 'POLICY_30D';
```

정책 생성과 삭제는 SYS로 실행합니다. 테이블 연결·해제는 대상 테이블의 DDL 권한을
확인합니다. 운영 계정으로 실행하기 전에 권한과 변경 범위를 확인하십시오.

<a id="retention-policy-retention-policy"></a>

### 테이블에 적용

```sql
ALTER TABLE sensor_tag ADD RETENTION policy_30d;

SELECT USER_NAME, TABLE_NAME, POLICY_NAME, STATE
  FROM V$RETENTION_JOB
 WHERE TABLE_NAME = 'SENSOR_TAG';
```

한 테이블에는 하나의 정책만 적용할 수 있습니다. TAG 테이블은 `BASETIME`, LOG 테이블은
`_ARRIVAL_TIME`을 기준으로 오래된 데이터를 판정합니다. 적용 직후 삭제되는 것이 아니라
설정한 주기에 따라 작업이 실행됩니다. `START AT`을 생략하면 기존 최초 대기·반복·오류
재시도 방식을 유지합니다. 아래 시각 지정 예제는 생략 방식과 각각 독립적인 연결 방법입니다.

<a id="retention-start-at"></a>

### 최초 실행 시각 지정

| 설정 | 역할 | 지정 위치 |
|---|---|---|
| DURATION | 데이터를 남길 기간 | CREATE RETENTION |
| INTERVAL | 삭제 작업 실행 간격 | CREATE RETENTION |
| START AT | 해당 테이블 작업의 최초 실행 기준 | ALTER TABLE ... ADD RETENTION |

시작 기준은 공유 정책의 속성이 아니라 **테이블별 Retention 작업의 속성**입니다.
Standard Edition과 Cluster Edition에서 사용하며 기존 테이블 타입·권한 범위는 유지합니다.
START AT을 지정한 작업은 최초 예정 시각 전에는 삭제를 수행하지 않습니다.
한 테이블에는 하나의 정책만 연결하므로 이미 적용했다면 먼저 해제한 뒤 예제를 선택합니다.
이후 삭제 작업은 지정한 보존 기간에 따라 데이터를 제거하므로 전용 실습 테이블에서 확인합니다.

#### 야간 시각부터 시작

기존 테이블 sensor_tag와 아직 연결하지 않은 policy_30d를 가정합니다.

```sql
ALTER TABLE sensor_tag ADD RETENTION policy_30d START AT '02:00';
```

시각은 서버 시간대 기준의 정확한 24시간제 `HH:MI` 다섯 글자입니다.
시작일은 실제 명령 실행 시점을 기준으로 정합니다.

| 명령 실행 시각 | START AT | 최초 실행 기준 |
|---|---|---|
| 오늘 01:00 | '02:00' | 오늘 02:00 |
| 오늘 03:00 | '02:00' | 내일 02:00 |
| 오늘 02:00 | '02:00' | 내일 02:00 |

지정 시각이 현재 시각 이하이면 다음 날로 넘어갑니다. INTERVAL이 1 DAY인 예제는
이 최초 기준에서 24시간씩 반복하며, DST마다 같은 현지 시각을 맞추는 달력 스케줄이 아닙니다.

#### 특정 미래 날짜부터 시작

위 예제와 별개의 적용 방법입니다. 날짜는 실제 운영에서 원하는 미래 날짜로 바꿉니다.

```sql
ALTER TABLE sensor_tag ADD RETENTION policy_30d
    START AT TO_DATE('2099-01-02 02:00:00', 'YYYY-MM-DD HH24:MI:SS');
```

TO_DATE의 날짜·형식에는 문자열 상수만 사용합니다. 현재와 같거나 지난 날짜·시각이면
오류입니다. NULL·bind·NOW·일반 계산식·서브쿼리는 START AT 입력으로 지원하지 않습니다.
형식을 생략한 `TO_DATE('2099-01-02 02:00:00')`는 세션의 DEFAULT_DATE_FORMAT을 사용하므로
날짜를 명확히 지정하려면 형식을 명시합니다.

#### 같은 정책에 테이블별 다른 시작 시각

sensor_tag_a와 sensor_tag_b는 기존 독립 테이블이며 Retention이 연결되지 않은 상태를 가정합니다.

```sql
ALTER TABLE sensor_tag_a ADD RETENTION policy_30d START AT '02:00';
ALTER TABLE sensor_tag_b ADD RETENTION policy_30d START AT '03:00';
```

보존 기간과 실행 간격은 같아도 최초 실행 기준은 테이블마다 다릅니다.

#### 시간대와 prepared statement

START AT은 클라이언트·세션 시간대가 아닌 **서버 시간대**로 해석합니다.
일반 TO_DATE SELECT의 시간대 해석과 혼동하지 않습니다. 날짜 형식 생략 시 세션의 날짜
형식을 사용하는 것과 시작 시각을 서버 시간대로 해석하는 것은 별개의 규칙입니다.
등록한 시작 기준은 절대 시각으로 저장하므로 서버 시간대가 바뀌어도 같은 현지 시각으로
다시 계산하지 않습니다.

PREPARE는 입력의 구문·상수 타입·인자 개수를 검사합니다. 값 형식·범위와 오늘/내일 결정,
미래 여부는 EXECUTE에서 검사합니다. 날짜가 PREPARE 때 미래였더라도 EXECUTE 때 지났으면
오류입니다. 재실행은 지난 실행에서 확정한 시작 기준을 재사용하지 않습니다.

<a id="retention-schedule"></a>

### 실행 주기와 삭제 기준

최초 실행 기준을 T0, INTERVAL을 I라고 하면 일정은 다음과 같습니다.

```text
T0 → T0+I → T0+2I → T0+3I → ...
```

작업이 오래 걸려도 완료 시각을 새 기준으로 삼지 않습니다. 성공한 작업이 끝난 시각보다
뒤에 있는 원래 주기의 첫 예정 시각으로 넘어갑니다. 예를 들어 00:00 기준 1시간 간격에서
01:00 회차가 02:10에 끝나면 다음 예정은 03:00입니다. 지나간 02:00 회차를 추가로 연속
실행하지 않습니다.

**삭제 cutoff는 실제 작업 실행 시각−DURATION**입니다. START AT은 보존 기간이나 TAG의
BASETIME·LOG의 _ARRIVAL_TIME 기준을 바꾸지 않습니다. 예정 시각과 실제 시작·완료 시각,
삭제 cutoff를 같은 값으로 해석하지 않습니다.

오류는 기존 backoff로 재시도하고 성공 전에는 해당 회차를 완료한 것처럼 예정 시각을
전진시키지 않습니다. 시스템 시계가 뒤로 움직여도 완료한 슬롯을 다시 예약하지 않습니다.
기간 환산·슬롯 계산이 표현 범위를 넘으면 오류이며 잘못된 시각으로 순환하지 않습니다.
부하와 재시도 때문에 실제 작업은 예정 시각보다 늦게 시작할 수 있습니다.

<a id="retention-restart"></a>

### 재시작과 지연된 회차

시작 기준과 다음 예정 시각은 영속화되므로 재시작 뒤에도 원래 주기를 유지합니다.

| 재시작 시 상태 | 처리 |
|---|---|
| 다음 예정 시각이 미래 | 해당 시각까지 대기 |
| 다음 예정 시각이 지남 | 한 번 실행하고 원래 주기의 다음 미래 시각으로 복귀 |
| 여러 회차를 놓침 | 놓친 횟수만큼 연속 실행하지 않음 |

00:00 기준·1시간 간격이고 미완료 회차가 01:00인 상태에서 01:20에 재시작하면 한 번
실행합니다. 01:21에 완료하면 다음 예정은 02:00입니다.

DELETE 성공 뒤 다음 예정 시각을 저장하기 전에 장애가 나면 같은 회차의 삭제를 다시
실행할 수 있습니다. 반대로 다음 예정 시각의 저장이 이미 커밋된 뒤 후속 정리에 오류가
났다는 이유로 저장된 회차를 되돌리지는 않습니다. 한 회차를 정확히 한 번 실행한다는
보장은 없습니다.
Cluster에서도 최초 기준은 공통으로 전파하지만, 실행 완료에 따른 다음 예정 시각은
broker별로 관리합니다. 장애 전환과 상태 점검은 [Cluster 운영](../cluster/#retention-schedule-cluster)을 참고합니다.

<a id="retention-change-start"></a>

### 시작 시각 변경

기존 연결을 해제한 뒤 새 시각으로 재등록합니다. 시작 시각만 직접 바꾸는 별도 ALTER 문법은
제공하지 않습니다.

```sql
ALTER TABLE sensor_tag DROP RETENTION;
ALTER TABLE sensor_tag ADD RETENTION policy_30d START AT '03:00';
```

두 명령은 별개이므로 그 사이에는 테이블에 Retention 작업이 연결되어 있지 않습니다.
재등록한 작업은 새 최초 기준으로 일정을 만듭니다. 해제해도 이미 삭제된 데이터는 복구되지 않습니다.

<a id="detach-retention-policy"></a>
<a id="retention-policy-detach-retention-policy"></a>

### 테이블에서 해제

```sql
ALTER TABLE sensor_tag DROP RETENTION;
```

해제하면 자동 삭제가 중단되지만 이미 삭제된 데이터는 복구되지 않습니다. 해제 후
`V$RETENTION_JOB`에서 대상 테이블이 사라졌는지 확인합니다.

<a id="delete-retention-policy"></a>
<a id="retention-policy-delete-retention-policy"></a>

### Retention Policy 삭제

정책을 사용하는 모든 테이블에서 먼저 해제한 뒤 정책 객체를 삭제합니다.

```sql
SELECT USER_NAME, TABLE_NAME
  FROM V$RETENTION_JOB
 WHERE POLICY_NAME = 'POLICY_30D';

-- 조회된 각 테이블에서 정책을 해제한 뒤 실행
DROP RETENTION policy_30d;
```

`ALTER TABLE ... DROP RETENTION`은 테이블과 정책의 연결을 해제하고, `DROP RETENTION`은
정책 객체를 삭제합니다. 적용 중인 정책은 삭제할 수 없습니다.

<a id="applicable-privileges-retention-sys"></a>
<a id="retention-policy-applicable-privileges-retention-sys"></a>

### 적용 범위와 권한

| 테이블 타입 | 적용 가능 |
|---|---|
| TAG, KV, LOG | 예 |
| TRANSACTION, VOLATILE, LOOKUP | 아니요 |

정책을 만들거나 삭제할 계정과 테이블 소유 계정이 다르면 운영 전에 실제 권한 구성을
검증하십시오. 다른 소유자의 테이블을 대상으로 할 때는 명시적으로 필요한 권한만 부여합니다.

<a id="execution-status-check-state-retention"></a>
<a id="retention-policy-execution-status-check-state-retention"></a>

### 실행 상태 확인

```sql
SELECT USER_NAME, TABLE_NAME, POLICY_NAME, STATE,
       LAST_DELETED_TIME, START_TIME, NEXT_RUN_TIME
  FROM V$RETENTION_JOB
 ORDER BY USER_NAME, TABLE_NAME;
```

`STATE`는 작업의 현재 상태이고, `LAST_DELETED_TIME`은 마지막 삭제 작업에 사용한 기준
시각입니다. 벽시계 기준의 작업 완료 시각으로 해석하지 마십시오. 실제 삭제 여부는 대상
테이블의 가장 오래된 시간과 행 수 추세를 함께 확인합니다.


| 상태 컬럼 | 의미 |
|---|---|
| START_TIME | 최초 실행 기준 시각 |
| NEXT_RUN_TIME | 현재 미완료 회차의 예정 시각 |
| LAST_DELETED_TIME | 마지막으로 성공한 DELETE의 cutoff |

START AT을 생략한 작업은 START_TIME과 NEXT_RUN_TIME이 모두 NULL입니다.
NEXT_RUN_TIME은 실행 중·지연·재시도 상태에서는 과거일 수 있습니다. 최초 등록 직후에는
START_TIME과 NEXT_RUN_TIME이 같습니다. 실제 삭제 여부는 대상 데이터와 함께 확인합니다.
[카탈로그의 전체 컬럼 정의](/kr/dbms-8.9/reference/system-catalog/virtual-table-full/#vretention_job)를 참고합니다.

### 업그레이드와 백업

시작 기준과 다음 예정 시각을 저장하는 메타 업그레이드가 필요합니다. 기존 작업은
시작 시각 없이 유지되며, 업그레이드된 메타를 지원하지 않는 구버전 엔진으로 실행할 수 없습니다.
물리 백업·복원은 일정을 보존하고 복원 뒤에도 재시작 규칙을 적용합니다.
MOUNT한 DB에서는 Retention worker가 실행되지 않습니다. Retention이 포함된 이미지에 대한
기존 논리 RESTORE 제한은 유지합니다.

- [백업·복원 시 Retention 일정](../backup-restore-mount/#retention-backup-schedule)
- [메타 업그레이드 호환성](/kr/dbms-8.9/reference/support-scope-constraints/compatibility-version/#retention-start-at-compatibility)
