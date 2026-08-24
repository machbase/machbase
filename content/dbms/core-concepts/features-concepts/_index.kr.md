---
type: docs
title: '2.3 주요 기능 개념'
weight: 30
toc: true
---
Machbase DBMS의 핵심 기능들이 어떤 역할을 하고 언제 사용하는지를 개념 수준에서 다룹니다. SQL 문법이나 설정 파라미터는 각 기능의 상세 문서를 참고하십시오.

- **[ROLLUP 통계의 역할](/dbms/core-concepts/features-concepts/#role-statistics-rollup)** -- 원시 데이터를 SEC/MIN/HOUR 단위로 자동 집계해 조회 성능을 높이는 메커니즘
- **[Retention Policy의 역할](/dbms/core-concepts/features-concepts/#role-retention-policy)** -- 오래된 데이터를 기간 기반으로 자동 삭제해 저장 공간을 관리하는 정책
- **[Backup / Restore / Mount 개념](/dbms/core-concepts/features-concepts/#concepts-backup-restore-mount)** -- 데이터 복사, 복원, 읽기 전용 연결의 세 가지 데이터 보호 수단


<a id="role-statistics-rollup"></a>

## ROLLUP 통계의 역할

TAG 테이블에서 장기간의 시간별 평균을 반복 조회하면 매번 원시 데이터를 집계하는 비용이
발생합니다. ROLLUP은 이 문제를 해결하는 자동 사전 집계 기능입니다.

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

`rollup()` 함수는 미리 계산된 집계를 읽어 반환하므로 원시 데이터를 매번 집계하는 비용을
줄입니다. 개선 폭은 조회 기간, 원시 데이터 양과 집계 구간에 따라 달라집니다.

### ROLLUP이 필요한 경우와 불필요한 경우

**ROLLUP이 유용한 경우**

- 장기간의 TAG 계측값에서 시간 단위 집계 조회가 반복되는 경우
- 대시보드나 모니터링 화면에서 분·시간 단위 트렌드를 실시간 표시해야 하는 경우
- 최근 데이터뿐 아니라 장기 이력(수개월~수년)의 집계도 빠르게 조회해야 하는 경우

**ROLLUP 없이도 충분한 경우**

- 원시 데이터 집계만으로 목표 응답 시간을 충족하는 경우
- 집계 조회보다 개별 값 조회(포인트 쿼리)가 주된 패턴인 경우
- 집계 주기가 SEC/MIN/HOUR와 맞지 않아 사용자 정의 구간을 애플리케이션에서 계산하는 경우

### 다음 읽을 내용

- [TAG 테이블 설계](/dbms/tag-table-usage/) -- ROLLUP 활성화를 포함한 TAG 테이블 상세 설계

<a id="role-retention-policy"></a>

## Retention Policy의 역할

시계열 데이터는 수집을 멈추지 않는 한 계속 쌓입니다. 모든 데이터를 영구 보관할 수 없다면 일정 기간이 지난 데이터를 자동으로 제거하는 정책이 필요합니다. Retention Policy가 바로 이 자동 데이터 수명 관리 기능입니다.

### Retention Policy란

테이블에 설정한 보관 기간보다 오래된 데이터를 배경 스레드가 자동으로 삭제하는 정책입니다. 운영자가 주기적으로 DELETE를 실행하지 않아도 설정된 기간이 지나면 자동으로 제거됩니다.

LOG 테이블과 TAG 테이블에 적용합니다. LOOKUP, VOLATILE, TRANSACTION 테이블의
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
| 주요 목적 | 장기 보관 정책 자동화 | 특정 구간 이상 데이터 즉시 제거 | LOG/TRANSACTION 테이블 초기화 |

**선택 기준**

- 30일, 90일 등 고정 기간 후 자동 삭제가 필요하면 **Retention Policy**를 사용합니다.
- 특정 이벤트나 배포 전후 특정 시간 구간의 데이터를 선택적으로 제거하려면 **DELETE**를 사용합니다.
- LOG 테이블이나 TRANSACTION 테이블 내용 전체를 즉시 비워야 하면 **TRUNCATE**를 사용합니다.

### 다음 읽을 내용

- [Backup / Restore / Mount 개념](/dbms/core-concepts/features-concepts/#concepts-backup-restore-mount) -- 데이터 보호와 복원 수단
- [Retention vs DELETE / TRUNCATE](/dbms/core-concepts/terminology-distinction/#retention-vs-delete-truncate) -- 세 가지 삭제 방법의 상세 비교

<a id="concepts-backup-restore-mount"></a>

## Backup / Restore / Mount 개념

Backup, Restore, Mount는 데이터 보호와 복구를 담당하는 세 가지 수단입니다. 이름이 비슷해 혼동하기 쉽지만, 각각 목적과 사용 시점이 명확히 구분됩니다.

### Backup: 운영 중 데이터 복사본 생성

운영 중인 데이터베이스를 멈추지 않고 데이터 파일을 지정한 디렉터리에 복사하는 작업입니다. 서버가 계속 데이터를 수신하는 동안에도 실행할 수 있습니다.

Backup 작업은 `LAUNCHED` -> `PROGRESS` -> `FINISHED` (실패 시 `ERROR`) 순으로 진행됩니다.

TRANSACTION 테이블도 데이터베이스 백업에 자동으로 포함됩니다. 데이터베이스 디렉터리를 수동으로
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

인스턴스 전체 복원은 서버를 중지한 상태에서 `machadmin -r`로 실행합니다. Machbase
8.7.0 Standard Edition에서는 단일 active logical database를 named
`RESTORE DATABASE`로 새 catalog에 복원하거나 READ ONLY target을 교체할 수 있습니다.

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
SELECT * FROM MOUNTDB.SYS.sensor_values LIMIT 10;

-- 마운트 해제
UMOUNT DATABASE MOUNTDB;
```

Restore와 달리 데이터를 원래 위치에 복사하지 않습니다. 백업본 디렉터리를 그대로 참조하므로, 과거 특정 시점의 데이터를 조회하거나 검증하는 데 적합합니다.

Mount된 database는 읽기 전용이며 `USE`할 수 없습니다. 조회에는 mounted database의
`USAGE`와 대상 table `SELECT`가 모두 필요합니다. 다른 active database와 함께 조회할
때는 `MOUNTDB.SYS.sensor_values`처럼 세 부분 이름을 사용합니다. mounted TRANSACTION
table에 대한 INSERT/UPDATE/DELETE와 `MOUNT TABLE` 방식의 단독 mount는 지원하지 않습니다.

논리 database의 백업·복원, `DATABASE_ID` 상태 확인과 client catalog 선택은
[다중 데이터베이스 운영 가이드](/dbms/operations-configuration-recovery/multi-database/)를
참조하십시오.

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
