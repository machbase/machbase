---
type: docs
title: '14.4 ALTER SYSTEM 운영'
weight: 40
toc: true
---
`ALTER SYSTEM`은 서버의 전역 자원을 관리하는 SQL 구문입니다. 세션 제어, 라이선스 설치, 캐시 정리, 체크포인트, I/O 동결 등 서버 운영에 필요한 작업을 수행합니다.

> **권한**: `ALTER SYSTEM` 명령은 `SYS` 계정 또는 `GRANT ALTER ON MACHBASEDB TO user_name;`으로 권한을 부여받은 사용자만 실행할 수 있습니다.

## 명령어 목록

| 명령어 | 기능 | 서버 재시작 필요 |
|---|---|:---:|
| [`ALTER SYSTEM KILL SESSION`](/dbms/operations-configuration-recovery/alter-system/#kill-cancel-session) | 지정한 세션을 강제 종료 | 아니요 |
| [`ALTER SYSTEM CANCEL SESSION`](/dbms/operations-configuration-recovery/alter-system/#kill-cancel-session) | 세션의 현재 실행 중인 쿼리만 취소 (세션 유지) | 아니요 |
| [`ALTER SYSTEM CHECK DISK_USAGE`](/dbms/operations-configuration-recovery/alter-system/#check-disk-usage) | 디스크 사용량 정보를 파일 시스템에서 재계산 | 아니요 |
| [`ALTER SYSTEM INSTALL LICENSE`](/dbms/operations-configuration-recovery/alter-system/#install-license) | 라이선스 파일 설치 (기본 경로 또는 지정 경로) | 아니요 |
| [`ALTER SYSTEM CHECKPOINT`](/dbms/operations-configuration-recovery/alter-system/#checkpoint) | 메모리 버퍼를 디스크에 즉시 동기화 | 아니요 |
| [`ALTER SYSTEM FREEZE`](/dbms/operations-configuration-recovery/alter-system/#freeze-unfreeze) | 모든 DML을 일시 중단 (백업 준비용) | 아니요 |
| [`ALTER SYSTEM UNFREEZE`](/dbms/operations-configuration-recovery/alter-system/#freeze-unfreeze) | FREEZE로 중단된 DML을 재개 | 아니요 |
| [`ALTER SYSTEM FLUSH AGER`](/dbms/operations-configuration-recovery/alter-system/#flush-ager) | Ager 스레드를 즉시 실행하여 만료 데이터 정리 | 아니요 |
| [`ALTER SYSTEM FLUSH RESULT_CACHE`](/dbms/operations-configuration-recovery/alter-system/#flush-result-cache) | 쿼리 결과 캐시 전체 초기화 | 아니요 |
| [`ALTER SYSTEM FLUSH SYS_STAT`](/dbms/operations-configuration-recovery/alter-system/#flush-sys-stat) | 쿼리 최적화기용 시스템 통계 정보 갱신 | 아니요 |
| [`ALTER SYSTEM FLUSH PVO_CACHE`](/dbms/operations-configuration-recovery/alter-system/#flush-pvo-cache) | PVO(Partition Value Object) Statement 캐시 초기화 | 아니요 |
| [`ALTER SYSTEM FLUSH PAGE_CACHE`](/dbms/operations-configuration-recovery/alter-system/#flush-page-cache) | OS 페이지 캐시를 Machbase 레벨에서 강제 해제 | 아니요 |
| [`ALTER SYSTEM FLUSH TAG_CACHE`](/dbms/tag-table-usage/tag-cache-operations/#flush-tag-cache) | TAG 테이블 메타데이터 캐시 초기화 | 아니요 |

## 관련 뷰

| 뷰 | 설명 |
|---|---|
| `v$session` | 현재 접속 세션 목록 및 실행 중인 쿼리 확인 |
| `v$storage` | 디스크 사용량 정보 (`DC_TABLE_FILE_SIZE` 등) |
| `v$license_info` | 설치된 라이선스 정보 확인 |
| `v$property` | 시스템 속성 및 현재 값 확인 |


<a id="checkpoint"></a>

## CHECKPOINT

```sql
ALTER SYSTEM CHECKPOINT;
```

메모리 버퍼에 있는 변경 데이터를 즉시 디스크에 기록합니다.

### 동작 설명

Machbase는 성능을 위해 쓰기 작업을 메모리 버퍼에 먼저 기록하고 주기적으로 디스크에 동기화합니다. 이 주기적인 동기화를 체크포인트(Checkpoint)라고 합니다. 체크포인트 주기는 `DISK_COLUMNAR_TABLE_CHECKPOINT_INTERVAL_SEC`와 `DISK_COLUMNAR_INDEX_CHECKPOINT_INTERVAL_SEC` 파라미터로 제어됩니다.

`ALTER SYSTEM CHECKPOINT`를 실행하면 예약된 주기를 기다리지 않고 즉시 체크포인트를 수행합니다. 체크포인트가 완료되면 명령이 반환됩니다.

체크포인트 관련 파라미터는 [스토리지 및 체크포인트 설정](/dbms/operations-configuration-recovery/configuration/#storage-checkpoint-configuration)을 참고하십시오.

### 사용 시점

| 상황 | 설명 |
|---|---|
| 백업 전 | 백업 대상 데이터를 디스크에 완전히 내려쓴 후 백업 실행 |
| 계획된 서버 종료 전 | 종료 시 자동 체크포인트가 수행되지만, 미리 실행해 종료 시간을 단축 |
| 장시간 운영 후 데이터 안전성 확인 | 메모리 버퍼가 누적된 상황에서 수동으로 동기화 |

### 사용 예시

```sql
-- 백업 전 체크포인트 수행
ALTER SYSTEM CHECKPOINT;

-- 체크포인트 완료 후 백업 실행
BACKUP DATABASE INTO DISK = '/backup/machbase_20260707';
```

> **참고**: 서버 재시작 없이 즉시 실행됩니다. 체크포인트가 진행되는 동안 INSERT 성능이 일시적으로 저하될 수 있습니다.

<a id="check-disk-usage"></a>

## CHECK DISK_USAGE

```sql
ALTER SYSTEM CHECK DISK_USAGE;
```

`v$storage`의 `DC_TABLE_FILE_SIZE` 값을 파일 시스템에서 직접 읽어 재계산합니다.

### 동작 설명

Machbase는 LOG 테이블의 디스크 사용량을 내부 메타데이터로 관리합니다. 정상적인 상황에서는 이 값이 자동으로 유지되지만, 프로세스 비정상 종료나 정전 등이 발생하면 메타데이터가 실제 파일 시스템 상태와 달라질 수 있습니다.

`CHECK DISK_USAGE`를 실행하면 Machbase가 실제 파일 시스템을 직접 스캔하여 사용량을 재계산하고 `v$storage`에 반영합니다.

> **주의**: 파일 시스템 스캔이 발생하므로 디스크 I/O 부담이 생깁니다. 일상적인 모니터링보다는 사용량 불일치가 의심될 때 사용하십시오.

### 사용 예시

```sql
-- 실행 전 현재 디스크 사용량 확인
SELECT * FROM v$storage;

-- 디스크 사용량 재계산
ALTER SYSTEM CHECK DISK_USAGE;

-- 재계산 후 결과 확인
SELECT * FROM v$storage;
```

### 사용 시점

- 서버 비정상 종료 후 재시작했을 때 디스크 사용량이 실제와 다르게 표시되는 경우
- 용량 모니터링 수치가 실제 파일 크기와 맞지 않는다고 판단될 때
- 디스크 공간 부족 경고가 발생했는데 실제로 여유가 충분한 경우

<a id="install-license"></a>

## INSTALL LICENSE

서버를 재시작하지 않고 라이선스 파일을 설치합니다.

### 구문

#### 기본 경로 설치

```sql
ALTER SYSTEM INSTALL LICENSE;
```

`$MACHBASE_HOME/conf/license.dat` 경로에 있는 라이선스 파일을 설치합니다. 설치 전 라이선스의 유효성을 검증하며, 검증에 성공하면 즉시 적용됩니다.

#### 지정 경로 설치

```sql
ALTER SYSTEM INSTALL LICENSE = '/경로/license.dat';
```

지정한 경로의 라이선스 파일을 설치합니다. 운영 절차에서는 현재 작업 디렉터리에 의존하지 않도록 절대 경로 사용을 권장하며, 설치 전 라이선스 유효성을 검증합니다.

**오류 상황**

- 지정한 경로에 파일이 없는 경우
- 라이선스 파일이 손상된 경우
- 현재 서버 환경에 맞지 않는 라이선스 파일인 경우

### 사용 예시

```sql
-- 기본 경로($MACHBASE_HOME/conf/license.dat)에서 설치
ALTER SYSTEM INSTALL LICENSE;

-- 지정 경로에서 설치
ALTER SYSTEM INSTALL LICENSE = '/tmp/new_license.dat';

-- 설치된 라이선스 정보 확인
SELECT * FROM v$license_info;
```

### 라이선스 정보 확인

```sql
SELECT * FROM v$license_info;
```

`v$license_info`에서 확인할 수 있는 주요 항목:

| 컬럼 | 설명 |
|---|---|
| `EDITION` | 에디션 (Standard, Cluster 등) |
| `EXPIRY_DATE` | 라이선스 만료일 |
| `MAX_NODE` | 최대 허용 노드 수 |
| `MAX_SENSORS` | 최대 허용 센서(태그) 수 |
| `MAX_STORAGE_SIZE` | 최대 스토리지 크기 |

### 참고

- 라이선스 파일은 Machbase 공식 채널을 통해 발급받습니다.
- 라이선스 만료 전 갱신을 권장합니다.
- 서버 시작 시 라이선스를 확인하며, 라이선스가 없거나 만료된 경우 제한된 모드로 동작할 수 있습니다.
- 라이선스 관련 상세 내용은 [라이선스 관리](/dbms/operations-configuration-recovery/server-database/#license)를 참고하십시오.

<a id="kill-cancel-session"></a>

## KILL / CANCEL SESSION

실행 중인 세션을 제어하는 두 가지 명령어입니다. `KILL SESSION`은 세션 자체를 강제 종료하고, `CANCEL SESSION`은 세션은 유지하면서 현재 실행 중인 쿼리만 중단합니다.

### KILL SESSION

```sql
ALTER SYSTEM KILL SESSION <session_id>;
```

지정한 세션 ID의 연결을 즉시 끊습니다.

- 대상 세션의 접속이 종료되고, 진행 중이던 트랜잭션은 롤백됩니다.
- `SYS` 계정만 실행할 수 있습니다.
- 자신의 세션이나 권한 없는 세션을 대상으로 하면 오류가 발생합니다.

**오류 코드**

| 상황 | 오류 |
|---|---|
| 세션 ID가 존재하지 않음 | `ERR_MM_SESSION_ID_NOT_FOUND` |
| 권한 없음 (자신 또는 다른 사용자) | `ERR-03025: Not enough privileges to manipulate the session.` |

**예시**

```sql
-- 현재 세션 목록 확인
SELECT id, user_id, client_type, query FROM v$session;

-- 세션 ID 12를 강제 종료
ALTER SYSTEM KILL SESSION 12;
```

### CANCEL SESSION

```sql
ALTER SYSTEM CANCEL SESSION <session_id>;
```

지정한 세션에서 현재 실행 중인 SQL만 중단합니다. 세션 연결 자체는 유지됩니다.

- 대상 세션에서는 `ERR-03027: This statement has been canceled.` 오류가 반환됩니다.
- 같은 사용자 또는 `SYS` 계정만 취소할 수 있습니다.
- 자신의 세션을 취소하려 하면 `ERR-03025` 오류가 발생합니다.

**오류 코드**

| 상황 | 오류 |
|---|---|
| 세션 ID가 존재하지 않음 | `ERR_MM_SESSION_ID_NOT_FOUND` |
| 다른 사용자 세션 취소 시도 | `ERR-03026: You should log in with the same user name in the target session.` |
| 자신의 세션 취소 시도 | `ERR-03025: Not enough privileges to manipulate the session.` |

**예시**

```sql
-- 세션 A: 실행 중인 세션 ID 확인
SELECT id, user_id, query FROM v$session;

-- 세션 B (같은 사용자 또는 SYS): 세션 6의 현재 쿼리만 취소
ALTER SYSTEM CANCEL SESSION 6;
```

### KILL vs CANCEL 비교

| 항목 | KILL SESSION | CANCEL SESSION |
|---|---|---|
| 세션 연결 | 종료 | 유지 |
| 실행 중인 쿼리 | 중단 | 중단 |
| 트랜잭션 롤백 | 예 | 예 |
| 실행 권한 | SYS만 가능 | 동일 사용자 또는 SYS |
| 사용 상황 | 응답 없는 세션을 완전히 제거 | 장시간 실행 쿼리만 취소하고 연결 유지 |

### 세션 ID 확인

```sql
-- 전체 세션 목록 조회
SELECT id, user_id, client_type, login_time FROM v$session;

-- 특정 쿼리를 실행 중인 세션 찾기
SELECT id, user_id, query FROM v$session WHERE query IS NOT NULL;
```

<a id="freeze-unfreeze"></a>

## FREEZE / UNFREEZE

일관된 스냅샷 백업을 위해 서버의 모든 DML(데이터 변경 작업)을 일시 중단하거나 재개합니다.

### FREEZE

```sql
ALTER SYSTEM FREEZE;
```

서버에 대한 모든 DML 작업을 일시 중단합니다. FREEZE 상태에서는 데이터가 변경되지 않으므로, 데이터 파일을 복사하여 일관된 스냅샷 백업을 만들 수 있습니다.

**FREEZE 상태에서 불가능한 작업**

- `INSERT` / Append 입력
- `DELETE`
- `UPDATE`

**FREEZE 상태에서 가능한 작업**

- `SELECT` 조회
- DDL(`CREATE`, `DROP`, `ALTER TABLE` 등)
- `ALTER SYSTEM` 명령어

> **주의**: FREEZE 상태를 유지하면 데이터 입력이 모두 차단됩니다. 최대한 짧은 시간 동안만 FREEZE 상태를 유지하고, 백업 완료 즉시 UNFREEZE를 실행하십시오.

### UNFREEZE

```sql
ALTER SYSTEM UNFREEZE;
```

FREEZE로 중단된 DML 작업을 재개합니다. UNFREEZE 이후에는 INSERT, DELETE 등 모든 데이터 변경 작업이 다시 허용됩니다.

### 사용 시나리오: 파일 시스템 수준 백업

`BACKUP DATABASE` 명령을 사용하지 않고 데이터 파일을 직접 복사하는 경우, FREEZE/UNFREEZE를 사용하여 일관성을 보장합니다.

```sql
-- 1. DML 중단
ALTER SYSTEM FREEZE;

-- 2. 데이터 파일 복사 (운영체제 명령 또는 스냅샷)
--    $MACHBASE_HOME/dbs/ 디렉터리를 백업 경로로 복사

-- 3. DML 재개
ALTER SYSTEM UNFREEZE;
```

### FREEZE vs BACKUP DATABASE

| 항목 | FREEZE + 파일 복사 | BACKUP DATABASE |
|---|---|---|
| 일관성 보장 | 수동으로 보장 (FREEZE 중 복사) | 자동 보장 |
| DML 차단 | FREEZE 동안 완전 차단 | 내부적으로 처리 |
| 사용 편의성 | 낮음 (직접 파일 관리 필요) | 높음 |
| 권장 상황 | 스토리지 스냅샷과 연동할 때 | 일반적인 데이터베이스 백업 |

일반적인 백업은 [데이터베이스 백업 및 복구](/dbms/core-concepts/features-concepts/#concepts-backup-restore-mount)를 참고하십시오.

<a id="flush-ager"></a>

## FLUSH AGER

```sql
ALTER SYSTEM FLUSH AGER;
```

Ager 백그라운드 스레드를 즉시 실행하여 만료된 데이터와 삭제 마크된 파티션을 정리합니다.

### Ager란

Ager는 Machbase의 백그라운드 스레드로, 다음 작업을 주기적으로 수행합니다.

- `DELETE` 또는 보존 정책으로 삭제 마크된 파티션 제거
- 만료 기간이 지난 데이터 파티션 물리적 삭제
- 삭제된 데이터가 차지하던 디스크 공간 해제

Ager는 자동으로 실행되지만, `ALTER SYSTEM FLUSH AGER`를 사용하면 예약된 실행 주기를 기다리지 않고 즉시 정리 작업을 실행합니다.

### 사용 시점

| 상황 | 설명 |
|---|---|
| 대량 DELETE 후 즉시 공간 회수 | DELETE 후 디스크가 즉시 해제되지 않을 때 수동으로 Ager 실행 |
| 보존 기간 정책 적용 후 즉시 반영 | 오래된 데이터 파티션을 즉시 제거하고 싶을 때 |
| 디스크 부족 상황에서 긴급 공간 확보 | 여유 공간이 부족할 때 우선 정리 작업 실행 |

### 사용 예시

```sql
-- 대량 삭제 후 Ager 즉시 실행
DELETE FROM log_table BEFORE TO_DATE('2025-01-01', 'YYYY-MM-DD');
ALTER SYSTEM FLUSH AGER;

-- 디스크 사용량 변화 확인
ALTER SYSTEM CHECK DISK_USAGE;
SELECT * FROM v$storage;
```

> **참고**: Ager 실행은 비동기적으로 시작됩니다. 명령이 반환된 직후 모든 정리가 완료된 것은 아니며, 파티션 수와 크기에 따라 시간이 걸릴 수 있습니다.

<a id="flush-result-cache"></a>

## FLUSH RESULT_CACHE

```sql
ALTER SYSTEM FLUSH RESULT_CACHE;
```

Result Cache(쿼리 결과 캐시)에 저장된 모든 캐시 항목을 초기화합니다.

### Result Cache란

Machbase의 Result Cache는 자주 실행되는 SELECT 쿼리의 결과를 메모리에 저장하여, 동일한 쿼리가 다시 요청될 때 실제 연산 없이 캐시된 결과를 반환하는 기능입니다. Result Cache 사용 여부는 세션 단위(`ALTER SESSION SET RS_CACHE_ENABLE`)로 제어할 수 있습니다.

`FLUSH RESULT_CACHE`를 실행하면 모든 세션에 걸쳐 캐시된 결과가 즉시 삭제됩니다.

### 사용 시점

| 상황 | 설명 |
|---|---|
| 데이터 변경 후 캐시 불일치 | 대량 INSERT/DELETE 후 캐시된 결과가 최신 데이터를 반영하지 않을 때 |
| 메모리 확보 | Result Cache가 차지하는 메모리를 즉시 해제해야 할 때 |
| 캐시 동작 테스트 | 캐시를 초기화하고 히트율 등 동작을 새로 측정할 때 |

### 사용 예시

```sql
-- Result Cache 전체 초기화
ALTER SYSTEM FLUSH RESULT_CACHE;

-- 세션별 Result Cache 제어 (비활성화)
ALTER SESSION SET RS_CACHE_ENABLE = 0;

-- 캐시 상태 확인
SELECT name, value FROM v$property WHERE name LIKE '%CACHE%';
```

### 관련 세션 설정

| 속성 | 설명 |
|---|---|
| `RS_CACHE_ENABLE` | 세션의 Result Cache 사용 여부 (0=비활성, 1=활성) |
| `RS_CACHE_TIME_BOUND_MSEC` | 캐시 저장 기준 실행 시간 (밀리초, 0이면 모든 쿼리 결과 저장 대상) |
| `RS_CACHE_MAX_MEMORY_PER_QUERY` | 쿼리당 최대 캐시 메모리 |
| `RS_CACHE_MAX_RECORD_PER_QUERY` | 쿼리당 최대 캐시 레코드 수 |

<a id="flush-pvo-cache"></a>

## FLUSH PVO_CACHE

```sql
ALTER SYSTEM FLUSH PVO_CACHE;
```

PVO(Partition Value Object) Statement Cache를 초기화합니다.

### PVO 캐시란

PVO Statement Cache는 Machbase Standard 에디션에서 사용하는 글로벌 SQL 실행 계획 캐시입니다. 동일한 SQL 문에 대한 파싱, 검증, 최적화 결과를 캐시하여 반복 실행 시 처리 비용을 줄입니다.

`FLUSH PVO_CACHE`를 실행하면 캐시된 모든 SQL 실행 계획이 제거됩니다. DDL이 성공적으로 실행될 때도 내부적으로 PVO 캐시가 자동으로 플러시됩니다.

> **참고**: PVO 캐시는 Result Cache(`FLUSH RESULT_CACHE`)와 독립적으로 동작합니다.

### PVO 캐시 설정

PVO 캐시 관련 속성은 `ALTER SYSTEM SET`으로 런타임에 조정할 수 있습니다.

| 속성 | 설명 | 재시작 필요 |
|---|---|:---:|
| `PVO_CACHE_ENABLE` | 캐시 활성화 여부 (0/1) | 아니요 |
| `PVO_CACHE_MAX_MEMORY_SIZE` | 캐시 최대 메모리 크기 (바이트) | 아니요 |
| `PVO_CACHE_MAX_PLANS_PER_SQL` | SQL당 최대 저장 실행 계획 수 | 아니요 |
| `PVO_CACHE_MAX_SQL_ENTRIES` | 최대 SQL 엔트리 수 (0=무제한) | 아니요 |
| `PVO_CACHE_SHARD_COUNT` | 캐시 샤드 수 | 예 |

### 사용 예시

```sql
-- PVO 캐시 즉시 초기화
ALTER SYSTEM FLUSH PVO_CACHE;

-- 캐시 비활성화 후 초기화
ALTER SYSTEM SET PVO_CACHE_ENABLE = 0;
ALTER SYSTEM FLUSH PVO_CACHE;

-- 캐시 크기 변경
ALTER SYSTEM SET PVO_CACHE_MAX_MEMORY_SIZE = 268435456;

-- 현재 설정 확인
SELECT name, value FROM v$property WHERE name LIKE 'PVO_CACHE%';
```

### 사용 시점

| 상황 | 설명 |
|---|---|
| 캐시된 실행 계획이 잘못되었을 때 | 테이블 구조 변경 후 오래된 실행 계획을 강제 제거 |
| 메모리 사용량 절감이 필요할 때 | 캐시가 차지하는 메모리를 즉시 해제 |
| 성능 문제 진단 시 | 캐시를 비운 후 재빌드되는 과정에서 실행 계획 문제 확인 |

<a id="flush-sys-stat"></a>

## FLUSH SYS_STAT

```sql
ALTER SYSTEM FLUSH SYS_STAT;
```

쿼리 최적화기(Query Optimizer)가 사용하는 시스템 통계 정보를 최신 상태로 갱신합니다.

### 동작 설명

Machbase의 쿼리 최적화기는 테이블 크기, 컬럼 분포, 인덱스 선택도 등의 통계 정보를 바탕으로 효율적인 실행 계획을 수립합니다. 이 통계 정보는 주기적으로 자동 갱신되지만, 대량의 데이터 변경이 있는 경우 통계가 현재 상태를 반영하지 못할 수 있습니다.

`FLUSH SYS_STAT`를 실행하면 현재 데이터 상태를 기반으로 통계 정보를 즉시 갱신합니다.

### 사용 시점

| 상황 | 설명 |
|---|---|
| 대량 데이터 적재 후 | 많은 양의 데이터가 추가된 직후 통계를 최신 상태로 갱신 |
| 쿼리 실행 계획이 비효율적일 때 | 최적화기가 오래된 통계를 기반으로 잘못된 계획을 선택할 때 |
| 성능 테스트 전 | 통계 기반의 일관된 실행 계획을 보장하기 위해 |

### 사용 예시

```sql
-- 대량 데이터 적재 후 통계 갱신
INSERT INTO sensor_log SELECT * FROM sensor_log_stage;
ALTER SYSTEM FLUSH SYS_STAT;

-- 갱신 후 실행 계획 확인
EXPLAIN SELECT * FROM sensor_log WHERE sensor_id = 'TAG_001';
```

> **참고**: 갱신 작업은 테이블 크기에 따라 수 초에서 수십 초가 걸릴 수 있습니다. 통계 갱신 중에도 서버는 정상적으로 쿼리를 처리합니다.

<a id="flush-page-cache"></a>

## FLUSH PAGE_CACHE

```sql
ALTER SYSTEM FLUSH PAGE_CACHE;
```

Machbase가 관리하는 페이지 캐시를 강제로 비웁니다.

### 동작 설명

Machbase는 자주 접근하는 데이터 페이지를 메모리에 캐시하여 디스크 I/O를 줄입니다. 이 페이지 캐시는 서버 성능 향상을 위해 자동으로 관리되지만, 다음과 같은 상황에서 수동으로 비워야 할 때 `FLUSH PAGE_CACHE`를 사용합니다.

- 메모리 사용량이 급격히 증가했을 때 캐시를 해제하여 메모리 여유 확보
- 성능 벤치마크나 테스트에서 캐시 효과를 배제한 순수 디스크 I/O 성능 측정
- 캐시 관련 동작을 진단하기 위해 초기 상태로 리셋

> **주의**: 캐시를 비운 직후에는 데이터 페이지를 다시 디스크에서 읽어야 하므로, 잠시 쿼리 응답 시간이 느려질 수 있습니다.

### 사용 예시

```sql
-- 페이지 캐시 강제 초기화
ALTER SYSTEM FLUSH PAGE_CACHE;

-- 이후 쿼리는 캐시 없이 디스크에서 직접 읽음
SELECT COUNT(*) FROM log_table;
```

### 관련 설정

페이지 캐시 크기는 `DISK_COLUMNAR_PAGE_CACHE_MAX_SIZE` 파라미터로 제어합니다.

```sql
-- 현재 설정 확인
SELECT name, value FROM v$property WHERE name = 'DISK_COLUMNAR_PAGE_CACHE_MAX_SIZE';

-- 런타임에 크기 변경 (재시작 불필요)
ALTER SYSTEM SET DISK_COLUMNAR_PAGE_CACHE_MAX_SIZE = 536870912;
```
