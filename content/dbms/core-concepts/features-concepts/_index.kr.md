---
type: docs
title: '2.3 주요 기능 개념'
weight: 30
toc: true
---
Machbase DBMS의 핵심 기능들이 어떤 역할을 하고 언제 사용하는지를 개념 수준에서 다룹니다. SQL 문법이나 설정 파라미터는 각 기능의 상세 문서를 참고하십시오.

- **[ROLLUP 통계의 역할](/dbms/core-concepts/features-concepts/#role-statistics-rollup)** -- 원시 데이터를 SEC/MIN/HOUR 단위로 자동 집계해 조회 성능을 높이는 메커니즘
- **[STREAM 처리 모델](/dbms/core-concepts/features-concepts/#processing-model-stream)** -- 주기적으로 SELECT 결과를 다른 테이블에 INSERT하는 자동 처리 객체와 ROLLUP과의 차이
- **[Retention Policy의 역할](/dbms/core-concepts/features-concepts/#role-retention-policy)** -- 오래된 데이터를 기간 기반으로 자동 삭제해 저장 공간을 관리하는 정책
- **[Backup / Restore / Mount 개념](/dbms/core-concepts/features-concepts/#concepts-backup-restore-mount)** -- 데이터 복사, 복원, 읽기 전용 연결의 세 가지 데이터 보호 수단


<a id="role-statistics-rollup"></a>

## ROLLUP 통계의 역할

TAG 테이블에 수억 건의 계측값이 쌓인 상황에서 "지난 한 달의 시간별 평균 온도"를 조회한다고 가정합니다. 매번 원시 데이터 전체를 스캔해 계산하면 수억 건을 집계하는 오버헤드가 발생합니다. ROLLUP은 이 문제를 해결하는 자동 사전 집계 메커니즘입니다.

### ROLLUP이란

TAG 테이블에 새 데이터가 입력될 때, 배경 스레드가 자동으로 초·분·시간 단위의 집계 통계를 미리 계산해 내부 테이블에 저장하는 기능입니다. 집계가 이미 계산된 상태이므로 조회 시 원시 데이터를 다시 스캔할 필요가 없습니다.

### 3단계 자동 집계

| 단계 | 집계 단위 | 내부 테이블 |
| --- | --- | --- |
| 1단계 | 초(SEC) | `_TAG_ROLLUP_SEC` |
| 2단계 | 분(MIN) | `_TAG_ROLLUP_MIN` |
| 3단계 | 시(HOUR) | `_TAG_ROLLUP_HOUR` |

SEC 집계가 축적되면 MIN으로, MIN이 축적되면 HOUR로 순차 합산됩니다. 각 집계 테이블에는 합계(SUM), 건수(COUNT), 최솟값(MIN), 최댓값(MAX), 첫 번째 값(FIRST), 마지막 값(LAST)이 저장됩니다.

### ROLLUP 테이블 생성

TAG 테이블 생성 시 `WITH ROLLUP` 절을 추가하면 활성화됩니다.

```sql
CREATE TAG TABLE rollup_sensor_values (
    name  VARCHAR(128) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE SUMMARIZED
) WITH ROLLUP (SEC);
```

`SUMMARIZED` 속성이 붙은 컬럼이 집계 대상입니다. `WITH ROLLUP (SEC)`은 SEC -> MIN -> HOUR 세 단계 모두를 활성화합니다. 특정 단계까지만 필요하면 `WITH ROLLUP (MIN)` 또는 `WITH ROLLUP (HOUR)`를 지정합니다.

### rollup() 함수로 조회

ROLLUP 집계 데이터 조회에는 `rollup()` 함수를 사용합니다.

```sql
-- 분 단위 평균값 조회
SELECT rollup('min', 1, time) AS mtime, AVG(value) AS avg_value
FROM rollup_sensor_values
WHERE name = 'temp_sensor_01'
  AND time BETWEEN TO_DATE('2026-07-01', 'YYYY-MM-DD')
               AND TO_DATE('2026-07-03', 'YYYY-MM-DD')
GROUP BY mtime
ORDER BY mtime;
```

`rollup()` 함수는 내부적으로 `_TAG_ROLLUP_MIN` 테이블에서 이미 계산된 집계를 읽어 반환합니다. 원시 데이터를 스캔하지 않으므로 조회 성능이 수십~수백 배 향상됩니다.

### ROLLUP이 필요한 경우와 불필요한 경우

**ROLLUP이 유용한 경우**

- 수억 건 이상의 TAG 계측값에서 시간 단위 집계 조회가 반복적으로 필요한 경우
- 대시보드나 모니터링 화면에서 분·시간 단위 트렌드를 실시간 표시해야 하는 경우
- 최근 데이터뿐 아니라 장기 이력(수개월~수년)의 집계도 빠르게 조회해야 하는 경우

**ROLLUP 없이도 충분한 경우**

- 데이터 건수가 수천만 건 이하로 원시 데이터 집계가 충분히 빠른 경우
- 집계 조회보다 개별 값 조회(포인트 쿼리)가 주된 패턴인 경우
- 집계 주기가 SEC/MIN/HOUR와 맞지 않아 사용자 정의 구간이 필요한 경우 (STREAM 검토)

### 다음 읽을 내용

- [STREAM 처리 모델](/dbms/core-concepts/features-concepts/#processing-model-stream) -- 임의 SQL 기반의 자동 변환/집계 처리
- [ROLLUP vs STREAM](/dbms/core-concepts/terminology-distinction/#rollup-vs-stream) -- 두 기능의 차이와 선택 기준
- [TAG 테이블 설계](/dbms/tag-table-usage/) -- ROLLUP 활성화를 포함한 TAG 테이블 상세 설계

<a id="processing-model-stream"></a>

## STREAM 처리 모델

STREAM은 입력 데이터를 자동으로 변환하거나 집계해 다른 테이블에 저장하는 처리 객체입니다. 사용자가 정의한 `INSERT ... SELECT ...` 쿼리를 서버 내부 스트림으로 등록하고, 시작(START)한 뒤 중지(STOP)하거나 삭제(DROP)할 때까지 동작합니다.

### STREAM이란

"지정한 `INSERT ... SELECT ...` 변환 쿼리를 서버 내부에 등록해 자동 실행하는 객체"입니다. 배경 스레드로 동작하므로 한 번 생성하고 시작하면 중지하거나 삭제할 때까지 계속 실행됩니다.

```sql
-- STREAM 생성 예시: LOG 테이블의 이상 이벤트를 TAG 테이블로 변환
EXEC STREAM_CREATE(alarm_to_tag,
    'INSERT INTO sensor_alerts SELECT ''ALARM_COUNT'', _arrival_time, value FROM device_log WHERE severity = ''CRITICAL''');

-- 시작
EXEC STREAM_START(alarm_to_tag);

-- 중지
EXEC STREAM_STOP(alarm_to_tag);

-- 삭제
EXEC STREAM_DROP(alarm_to_tag);
```

### ROLLUP과의 차이

ROLLUP과 STREAM은 모두 데이터를 가공해 다른 형태로 저장하지만, 역할과 적용 범위가 다릅니다.

| 항목 | ROLLUP | STREAM |
| --- | --- | --- |
| 대상 테이블 | TAG 테이블 전용 | 임의 테이블 (LOG, TAG, LOOKUP 등) |
| 집계 단위 | SEC / MIN / HOUR 고정 | 사용자가 SQL로 자유롭게 정의 |
| 결과 저장 위치 | 내부 ROLLUP 테이블 | 사용자가 지정한 대상 테이블 |
| 변환 로직 | 고정 (SUM, COUNT, MIN, MAX, FIRST, LAST) | 임의 SQL (JOIN, 조건 필터, 문자열 변환 등) |
| 설정 방법 | `WITH ROLLUP` 절로 테이블 생성 시 지정 | `EXEC STREAM_CREATE`로 별도 생성 |

### 주요 사용 사례

**LOG -> TAG 변환**

비정형 이벤트 로그에서 특정 조건을 만족하는 이벤트를 집계해 TAG 테이블의 계측값으로 변환합니다. 예를 들어 10초마다 로그에서 오류 건수를 세어 TAG 테이블에 저장하면, ROLLUP과 결합해 시간별 오류율 트렌드를 빠르게 조회할 수 있습니다.

**파생 집계 테이블 생성**

원시 데이터를 ROLLUP이 지원하지 않는 사용자 정의 시간 구간(예: 15분, 30분)으로 집계해 별도 테이블에 저장합니다.

**데이터 정제 및 필터링**

수집 단계에서 들어온 노이즈 데이터나 이상값을 필터링하고, 정제된 값만 TAG 테이블에 적재합니다.

### Cluster Edition 주의사항

STREAM은 Standard Edition 중심으로 설계되었습니다. Cluster Edition에서도 생성과 실행은 가능하지만, 복잡한 조인이나 서브쿼리를 포함한 SQL은 지원되지 않을 수 있습니다. Cluster Edition에서 STREAM을 사용하려면 대상 SQL을 먼저 검증하십시오.

### 다음 읽을 내용

- [ROLLUP 통계의 역할](/dbms/core-concepts/features-concepts/#role-statistics-rollup) -- 자동 집계 메커니즘의 상세 내용
- [ROLLUP vs STREAM](/dbms/core-concepts/terminology-distinction/#rollup-vs-stream) -- 두 기능의 차이와 선택 기준
- [Retention Policy의 역할](/dbms/core-concepts/features-concepts/#role-retention-policy) -- 자동 데이터 삭제 정책 개념

<a id="role-retention-policy"></a>

## Retention Policy의 역할

시계열 데이터는 수집을 멈추지 않는 한 계속 쌓입니다. 모든 데이터를 영구 보관할 수 없다면 일정 기간이 지난 데이터를 자동으로 제거하는 정책이 필요합니다. Retention Policy가 바로 이 자동 데이터 수명 관리 기능입니다.

### Retention Policy란

테이블에 설정한 보관 기간보다 오래된 데이터를 배경 스레드가 자동으로 삭제하는 정책입니다. 운영자가 주기적으로 DELETE를 실행하지 않아도 설정된 기간이 지나면 자동으로 제거됩니다.

LOG 테이블과 TAG 테이블에 적용합니다. LOOKUP, VOLATILE, RDB 테이블의
수명 관리는 DELETE 또는 TRUNCATE 같은 명시적 DML로 처리합니다.

### 적용 방법

```sql
-- 1. Retention Policy 생성 (30일 보관)
CREATE RETENTION keep_30days DURATION 30 DAY INTERVAL 1 DAY;

-- 2. 테이블에 적용
ALTER TABLE device_log ADD RETENTION keep_30days;
```

이후 `device_log` 테이블에서 30일이 지난 데이터는 배경에서 자동 삭제됩니다. 정책을 해제하려면 다음을 실행합니다.

```sql
ALTER TABLE device_log DROP RETENTION;
```

### DELETE, TRUNCATE와의 차이

| 항목 | Retention Policy | DELETE | TRUNCATE |
| --- | --- | --- | --- |
| 실행 방식 | 자동 (배경 스레드) | 수동 (SQL 실행) | 수동 (SQL 실행) |
| 삭제 범위 | 기간 기준 자동 판단 | 테이블 타입별 DELETE 조건 기반 | 테이블 전체 |
| 지속성 | 지속적 (한 번 설정 후 자동) | 일회성 | 일회성 |
| 운영 중 실행 | 가능 (무중단) | 가능 (시간 범위 제약) | 가능 |
| 주요 목적 | 장기 보관 정책 자동화 | 특정 구간 이상 데이터 즉시 제거 | LOG/RDB 테이블 초기화 |

**선택 기준**

- 30일, 90일 등 고정 기간 후 자동 삭제가 필요하면 **Retention Policy**를 사용합니다.
- 특정 이벤트나 배포 전후 특정 시간 구간의 데이터를 선택적으로 제거하려면 **DELETE**를 사용합니다.
- LOG 테이블이나 RDB 테이블 내용 전체를 즉시 비워야 하면 **TRUNCATE**를 사용합니다.

### 다음 읽을 내용

- [Backup / Restore / Mount 개념](/dbms/core-concepts/features-concepts/#concepts-backup-restore-mount) -- 데이터 보호와 복원 수단
- [Retention vs DELETE / TRUNCATE](/dbms/core-concepts/terminology-distinction/#retention-vs-delete-truncate) -- 세 가지 삭제 방법의 상세 비교

<a id="concepts-backup-restore-mount"></a>

## Backup / Restore / Mount 개념

Backup, Restore, Mount는 데이터 보호와 복구를 담당하는 세 가지 수단입니다. 이름이 비슷해 혼동하기 쉽지만, 각각 목적과 사용 시점이 명확히 구분됩니다.

### Backup: 운영 중 데이터 복사본 생성

운영 중인 데이터베이스를 멈추지 않고 데이터 파일을 지정한 디렉터리에 복사하는 작업입니다. 서버가 계속 데이터를 수신하는 동안에도 실행할 수 있습니다.

Backup 작업은 `LAUNCHED` -> `PROGRESS` -> `FINISHED` (실패 시 `ERROR`) 순으로 진행됩니다.

RDB 테이블도 데이터베이스 백업에 자동으로 포함됩니다. 데이터베이스 디렉터리를 수동으로
복사하지 말고 Machbase가 제공하는 Backup/Restore/Mount 절차를 사용해야 합니다.

| 유형 | 설명 |
| --- | --- |
| 전체 Backup | 데이터베이스 전체를 복사 |
| 증분 Backup | 이전 Backup 이후 변경된 부분만 복사 |
| 기간 Backup | 특정 시간 범위의 데이터만 복사 |
| 테이블 Backup | 특정 테이블만 복사 |

```sql
-- 전체 백업 실행
BACKUP DATABASE INTO DISK = '/data/backup/full_20260703';

-- 특정 테이블 백업
BACKUP TABLE sensor_values INTO DISK = '/data/backup/sensor_20260703';
```

### Restore: 백업본으로 데이터베이스 복원

백업본을 사용해 데이터베이스를 원래 위치에 복원합니다. Backup과 달리 반드시 서버를 중지한 상태에서 `machadmin` 도구로 실행합니다.

```bash
# 서버 중지 후 machadmin으로 복원
machadmin -r /data/backup/full_20260703
```

장애로 인한 데이터 손상이나 서버 마이그레이션 시 사용합니다. 복원이 완료되면 서버를 재시작합니다.

### Mount: 백업본을 읽기 전용으로 연결

백업본을 현재 운영 중인 서버에 읽기 전용으로 연결합니다. 서버를 중지할 필요가 없으며, Mount된 데이터를 현재 운영 데이터와 함께 SELECT로 조회합니다.

```sql
-- 백업본 Mount
MOUNT DATABASE '/data/backup/full_20260703' TO MOUNTDB;

-- Mount된 데이터 조회
SELECT * FROM MOUNTDB.sensor_values LIMIT 10;

-- 마운트 해제
UMOUNT DATABASE MOUNTDB;
```

Restore와 달리 데이터를 원래 위치에 복사하지 않습니다. 백업본 디렉터리를 그대로 참조하므로, 과거 특정 시점의 데이터를 조회하거나 검증하는 데 적합합니다.

Mount된 데이터베이스는 읽기 전용입니다. RDB 테이블도 `MOUNT DATABASE`로 연결한 백업본에서는
SELECT만 허용되며, mounted RDB 테이블에 대한 INSERT/UPDATE/DELETE나 `MOUNT TABLE` 방식의 RDB
테이블 단독 Mount는 지원하지 않습니다.

### 세 개념의 관계

```
[운영 중인 서버]
        │
        ▼
   BACKUP 실행  ──────────────────────────────►  [백업 디렉터리]
   (서버 유지)                                          │
                                               ┌────────┴────────┐
                                               ▼                 ▼
                                          RESTORE           MOUNT
                                       (서버 중지 필요)   (서버 유지)
                                               │                 │
                                               ▼                 ▼
                                         원위치 복원      현재 서버에
                                         (장애 복구)    read-only 연결
                                                         (과거 조회)
```

### 각 수단의 선택 기준

| 상황 | 권장 수단 |
| --- | --- |
| 정기적인 데이터 보호 목적 | Backup (전체/증분) |
| 서버 장애, 데이터 손상 복구 | Restore |
| 과거 특정 시점 데이터 조회 및 검증 | Mount |
| 운영 서버 마이그레이션 | Backup -> 신규 서버에서 Restore |
| 특정 테이블만 과거 데이터 확인 | Backup (테이블) -> Mount |

### 다음 읽을 내용

- [Backup vs Restore vs Mount](/dbms/core-concepts/terminology-distinction/#backup-vs-restore-mount) -- 세 개념의 비교 표
- [ROLLUP 통계의 역할](/dbms/core-concepts/features-concepts/#role-statistics-rollup) -- 장기 데이터 집계 조회 성능 관리
- [Retention Policy의 역할](/dbms/core-concepts/features-concepts/#role-retention-policy) -- 오래된 데이터 자동 삭제 정책
