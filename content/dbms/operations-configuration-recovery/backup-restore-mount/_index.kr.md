---
type: docs
title: '13.9 백업, 복원, 마운트'
weight: 90
toc: true
---
운영 환경에서 데이터를 보호하고 필요 시 복구하기 위한 세 가지 핵심 기능 -- 백업, 복원, 마운트 -- 을 다룹니다.

## 세 가지 핵심 기능

### 백업 (BACKUP)

운영 중인 서버를 중단하지 않고 데이터를 외부 저장소에 복사합니다. 백업은 저장 방식과 범위에 따라 구분됩니다.

| 방식 | 설명 |
|------|------|
| **DISK 백업** | 백업 대상 데이터를 지정한 디렉터리에 파일로 저장합니다. 가장 일반적인 방식입니다. |
| **테이블 백업** | 전체 데이터베이스가 아닌 특정 테이블만 선택적으로 백업합니다. |

백업 범위로는 **전체 백업**, **기간 백업**, **증분 백업**을 지원합니다.

### 복원 (RESTORE)

백업 데이터를 현재 데이터베이스로 복구합니다. 복원은 오프라인 상태(서버 중단)에서만 수행할 수 있으며, `machadmin -r` 명령을 사용합니다. 복원을 실행하면 현재 데이터베이스의 내용이 백업 시점으로 교체되므로 사전에 현재 데이터를 별도로 백업해 두어야 합니다.

### 마운트 (MOUNT)

서버를 중단하거나 복원 작업 없이, 백업 데이터베이스를 읽기 전용으로 현재 서버에 연결합니다. 마운트된 데이터베이스는 별도의 이름(스키마)으로 접근하며, 기존 운영 데이터와 동시에 조회할 수 있습니다. 특정 시점의 데이터를 확인하거나 아카이브된 데이터에서 일부 레코드를 추출할 때 유용합니다.

## 섹션 구성

| 섹션 | 내용 |
|------|------|
| [백업 개요](/dbms/operations-configuration-recovery/backup-restore-mount/#backup) | 백업 방식 비교, 선택 기준, 주기 권장 |
| [전체 백업](/dbms/operations-configuration-recovery/backup-restore-mount/#backup-full) | `BACKUP DATABASE INTO DISK` 전체 백업 |
| [테이블 백업](/dbms/operations-configuration-recovery/backup-restore-mount/#backup-table) | `BACKUP TABLE` 특정 테이블 백업 |
| [증분 백업과 AFTER 기준 경로](/dbms/operations-configuration-recovery/backup-restore-mount/#backup-incremental-after) | 마지막 백업 이후 변경분만 백업 |
| [기간 백업](/dbms/operations-configuration-recovery/backup-restore-mount/#backup-period) | 특정 시간 범위 데이터 백업 |
| [SQL BACKUP 범위](/dbms/operations-configuration-recovery/backup-restore-mount/#sql-backup) | 지원 테이블 타입, 에디션별 차이 |
| [테이블 타입별 백업/마운트 제약](/dbms/operations-configuration-recovery/backup-restore-mount/#table-types-type-backup-mount) | 타입별 지원 여부 |
| [Offline restore with machadmin -r](/dbms/operations-configuration-recovery/backup-restore-mount/#offline-restore-machadmin-r) | 오프라인 복원 절차 |
| [데이터베이스 마운트](/dbms/operations-configuration-recovery/backup-restore-mount/#database-mount) | MOUNT / UMOUNT 사용법 |
| [마운트된 데이터베이스 조회](/dbms/operations-configuration-recovery/backup-restore-mount/#query-database-mount) | 마운트 DB에서 SELECT |
| [마운트 DB 동작 특성](/dbms/operations-configuration-recovery/backup-restore-mount/#mounted-db-read-only-refcount-active-same-name) | 읽기 전용, 활성 참조, 이름 충돌 |
| [RDB 백업·복원·마운트](/dbms/rdb-table-usage/backup-restore-mount/) | Standard Edition RDB 절차 |
| [MOUNT TABLE 미지원 범위](/dbms/operations-configuration-recovery/backup-restore-mount/#unsupported-support-scope-mount-table-umount) | 테이블 단위 마운트 제약 |

## 권한 요구 사항

Machbase 8.5 이상에서는 일반 사용자가 백업과 마운트를 실행하려면 별도 권한이 필요합니다.

```sql
-- 백업 권한 부여
GRANT BACKUP ON machbasedb TO user_name;

-- 마운트 권한 부여
GRANT MOUNT ON machbasedb TO user_name;
```


<a id="backup"></a>

## 백업 개요

Machbase 백업은 운영 서버를 중단하지 않고 실행할 수 있는 온라인(Online) 백업입니다. 백업 중에도 데이터 입력과 조회가 정상적으로 이루어집니다.

### 저장 방식

검증 대상 빌드에서는 운영 백업과 마운트 검증에 `DISK` 방식을 사용합니다.

> 마운트(`MOUNT DATABASE`) 기능을 사용하려면 DISK 방식으로 백업해야 합니다.

### 백업 범위 비교

| 범위 | 설명 | 사용 시점 |
|------|------|-----------|
| **전체 백업** | 현재 시점까지의 모든 데이터 | 정기 기준 백업 |
| **기간 백업** | FROM ~ TO 범위의 데이터 | 특정 기간 아카이브 |
| **증분 백업** | 이전 백업 이후 추가된 데이터 | 전체 백업과 함께 사용 |
| **테이블 백업** | 지정한 테이블 하나만 | 개별 테이블 복구 준비 |

### 백업 주기 권장

운영 환경에서는 다음과 같은 백업 정책을 권장합니다.

| 주기 | 방식 | 보관 기간 |
|------|------|-----------|
| 매일 | 전체 백업 (DISK) | 7일 |
| 매주 | 전체 백업 (DISK) | 4주 |
| 매월 | 전체 백업 또는 기간 백업 | 12개월 이상 |

증분 백업을 활용하면 전체 백업의 빈도를 줄이면서 복구 지점을 촘촘하게 유지할 수 있습니다. 단, 복구 시에는 전체 백업을 먼저 복원한 뒤 증분 백업을 순서대로 적용해야 합니다.

### 백업 방식 선택 가이드

```
데이터 전체를 안전하게 보관하고 싶다
  └─▶ 전체 백업 (BACKUP DATABASE INTO DISK)

특정 기간의 데이터만 아카이브하고 싶다
  └─▶ 기간 백업 (FROM ... TO ...)

전체 백업 이후 변경분만 빠르게 저장하고 싶다
  └─▶ 증분 백업 (BACKUP ... AFTER 'base_path')

특정 테이블만 별도로 보관하고 싶다
  └─▶ 테이블 백업 (BACKUP TABLE table_name)

마운트해서 과거 데이터를 읽고 싶다
  └─▶ DISK 방식 전체 백업 후 MOUNT DATABASE 사용
```

### 기본 문법 구조

```sql
-- 전체 또는 테이블 백업
BACKUP [ DATABASE | TABLE table_name ]
  [ FROM start_time TO end_time ]
  INTO DISK = 'backup_path';

-- 증분 백업
BACKUP DATABASE AFTER 'previous_backup_path'
  INTO DISK = 'incremental_backup_path';
```

- `DATABASE`: 전체 데이터베이스 백업
- `TABLE table_name`: 특정 테이블만 백업
- `AFTER 'path'`: 지정한 백업 이후의 데이터만 증분 백업
- `FROM ... TO ...`: 시간 범위 지정 (기간 백업)
- `DISK = 'path'`: 디렉터리로 저장 (절대/상대 경로 모두 가능)

상대 경로를 지정하면 `$MACHBASE_HOME/dbs` 하위에 생성됩니다.

<a id="backup-full"></a>

## 전체 백업

전체 백업은 현재 시점까지의 모든 데이터베이스 데이터를 지정한 경로에 저장합니다. 서버를 중단하지 않고 실행할 수 있는 온라인 백업입니다.

### 문법

```sql
BACKUP DATABASE INTO DISK = 'backup_path';
```

- `backup_path`: 백업 데이터를 저장할 디렉터리 경로
  - 절대 경로: `/`로 시작하는 전체 경로
  - 상대 경로: `$MACHBASE_HOME/dbs` 기준으로 생성

### 예제

```sql
-- 절대 경로로 전체 백업
BACKUP DATABASE INTO DISK = '/backup/machbase_20240101';

-- 상대 경로 (MACHBASE_HOME/dbs/backup_20240101 에 생성됨)
BACKUP DATABASE INTO DISK = 'backup_20240101';
```

### 동작 방식

- 백업 명령 실행 시 지정한 디렉터리가 자동으로 생성됩니다. 디렉터리가 이미 존재하면 오류가 발생하므로 날짜 등을 포함한 고유한 이름을 사용하세요.
- 백업 실행 중에도 데이터 입력, 조회 등 서버 운영이 계속됩니다.
- 백업이 완료될 때까지 백업 명령은 블로킹 상태로 유지됩니다. 장시간 소요될 수 있으므로 별도 세션에서 실행하거나 쉘 스크립트로 자동화하는 것을 권장합니다.

### 백업 디렉터리 구조

백업이 완료되면 지정한 경로에 다음과 같은 구조의 파일들이 생성됩니다.

```
/backup/machbase_20240101/
├── backup.dat
├── backup.trc
├── meta.dbs-0
├── meta.dbs-1
└── ...
```

### 백업 완료 후 검증

백업 완료 후에는 해당 경로를 마운트하여 데이터가 정상적으로 백업되었는지 확인할 수 있습니다.

```sql
-- 백업된 DB를 마운트
MOUNT DATABASE '/backup/machbase_20240101' TO verify_db;

-- 주요 테이블의 레코드 수 확인
SELECT COUNT(*) FROM verify_db.sys.sensor_log;

-- 마운트 해제
UMOUNT DATABASE verify_db;
```

### 자동화 예제 (쉘 스크립트)

```bash
#!/bin/bash
DATE=$(date +%Y%m%d)
BACKUP_PATH="/backup/machbase_${DATE}"

machsql -u sys -p manager -e "BACKUP DATABASE INTO DISK = '${BACKUP_PATH}';"

if [ $? -eq 0 ]; then
    echo "백업 완료: ${BACKUP_PATH}"
else
    echo "백업 실패" >&2
    exit 1
fi
```

### 주의 사항

- 백업 중 서버에 부하가 증가할 수 있습니다. 트래픽이 적은 시간대에 실행하는 것을 권장합니다.
- 백업 경로에 충분한 디스크 여유 공간이 있는지 사전에 확인하세요.
- 백업 파일은 원본 서버와 다른 물리 디스크 또는 원격 스토리지에 보관하는 것이 안전합니다.

<a id="backup-table"></a>

## 테이블 백업

테이블 백업은 전체 데이터베이스가 아닌 특정 테이블 하나만 백업합니다. 중요도가 높은 테이블을 더 자주 백업하거나, 특정 테이블만 별도로 이전해야 할 때 사용합니다.

### 문법

```sql
BACKUP TABLE table_name INTO DISK = 'backup_path';
```

기간 조건을 함께 사용할 수 있습니다.

```sql
BACKUP TABLE table_name
  [ FROM start_time TO end_time ]
  INTO DISK = 'backup_path';
```

### 예제

```sql
-- 특정 테이블 전체 백업
BACKUP TABLE sensor_log INTO DISK = '/backup/sensor_log_20240101';

-- 특정 테이블 기간 백업
BACKUP TABLE sensor_log
  FROM TO_DATE('20240101','YYYYMMDD')
  TO   TO_DATE('20240131','YYYYMMDD')
  INTO DISK = '/backup/sensor_log_202401';
```

### 지원 테이블 타입

| 테이블 타입 | BACKUP TABLE 지원 |
|------------|:-----------------:|
| LOG 테이블 | O |
| TAG 테이블 | O |
| LOOKUP 테이블 | O |
| VOLATILE 테이블 | X (메모리 기반) |
| RDB 테이블 | △ (Standard Edition 전용) |

VOLATILE 테이블은 메모리에만 존재하므로 백업이 지원되지 않습니다.

### 마운트를 통한 테이블 복구

테이블 백업 파일을 마운트하여 특정 테이블의 과거 데이터를 조회하거나, 필요한 데이터를 선별하여 현재 데이터베이스에 복사할 수 있습니다.

```sql
-- 테이블 백업 마운트
MOUNT DATABASE '/backup/sensor_log_20240101' TO tbl_backup;

-- 마운트된 테이블에서 데이터 확인
SELECT COUNT(*) FROM tbl_backup.sys.sensor_log;

-- 필요한 데이터만 현재 DB로 복사
INSERT INTO sensor_log
  SELECT * FROM tbl_backup.sys.sensor_log
   WHERE _arrival_time > TO_DATE('20240115','YYYYMMDD');

-- 언마운트
UMOUNT DATABASE tbl_backup;
```

### 주의 사항

- 테이블 백업으로 생성된 디렉터리에는 해당 테이블의 데이터만 포함됩니다.
- 전체 데이터베이스를 복원하는 용도로는 사용할 수 없습니다.
- 백업 경로가 이미 존재하면 오류가 발생합니다. 고유한 디렉터리 이름을 지정하세요.

<a id="backup-incremental-after"></a>

## 증분 백업과 AFTER 기준 경로

증분 백업은 이전 백업(전체 백업 또는 이전 증분 백업) 이후에 추가된 데이터만 백업합니다. 전체 백업보다 빠르고 저장 공간을 절약할 수 있습니다.

### 문법

```sql
BACKUP DATABASE AFTER 'previous_backup_path'
  INTO DISK = 'incremental_backup_path';
```

- `previous_backup_path`: 기준이 되는 이전 백업 경로 (전체 백업 또는 이전 증분 백업)
- `incremental_backup_path`: 이번 증분 백업을 저장할 새로운 경로

### 예제

```sql
-- 1단계: 기준 전체 백업 (예: 매주 일요일)
BACKUP DATABASE INTO DISK = '/backup/machbase_base_20240101';

-- 2단계: 증분 백업 (예: 매일)
BACKUP DATABASE AFTER '/backup/machbase_base_20240101'
  INTO DISK = '/backup/machbase_incr_20240102';

-- 3단계: 전날 증분 백업을 기준으로 다시 증분 백업
BACKUP DATABASE AFTER '/backup/machbase_incr_20240102'
  INTO DISK = '/backup/machbase_incr_20240103';
```

### 증분 백업 체인 구성

증분 백업은 체인 형태로 연결됩니다. 복구 시에는 복원하려는 최종 증분 백업 디렉터리를 `machadmin -r`에 지정합니다.

```
[전체 백업]            [증분 1]             [증분 2]             [증분 3]
machbase_base   ──▶  machbase_incr_0102  ──▶  machbase_incr_0103  ──▶  machbase_incr_0104
(1/1)               (1/2 이후 데이터)         (1/3 이후 데이터)         (1/4 이후 데이터)
```

### 증분 백업 복구 절차

증분 백업으로 복구할 때는 `machadmin -r` 명령을 최종 증분 백업 경로에 대해 한 번 실행합니다.

```bash
# 서버 종료
machadmin -s

# 기존 데이터베이스 삭제
machadmin -d

# 복원하려는 최종 증분 백업 지정
machadmin -r /backup/machbase_incr_20240103

# 서버 시작
machadmin -u
```

> `AFTER` 체인이 끊기지 않도록 전체 백업과 각 증분 백업 디렉터리를 함께 보관해야 합니다.

### 증분 백업 자동화 예제

```bash
#!/bin/bash
DATE=$(date +%Y%m%d)
PREV_DATE=$(date -d "yesterday" +%Y%m%d)

BASE_DIR="/backup/machbase_base"
PREV_INCR="/backup/machbase_incr_${PREV_DATE}"
CURR_INCR="/backup/machbase_incr_${DATE}"

# 이전 증분 백업이 있으면 그것을 기준으로, 없으면 전체 백업을 기준으로
if [ -d "${PREV_INCR}" ]; then
    AFTER_PATH="${PREV_INCR}"
else
    AFTER_PATH="${BASE_DIR}"
fi

machsql -u sys -p manager -e \
  "BACKUP DATABASE AFTER '${AFTER_PATH}' INTO DISK = '${CURR_INCR}';"
```

### 주의 사항

- `AFTER` 절에 지정하는 경로는 반드시 존재하는 유효한 백업 디렉터리여야 합니다.
- 직전 백업 경로를 기준으로 증분 백업을 생성합니다.
- 증분 백업 체인이 길어질수록 복구 시간이 늘어납니다. 주기적으로 새로운 전체 백업을 기준으로 재설정하는 것을 권장합니다.

<a id="backup-period"></a>

## 기간 백업

기간 백업은 특정 시간 범위에 해당하는 데이터만 선택하여 백업합니다. 오래된 데이터를 아카이브하거나 특정 기간의 데이터를 별도로 보관할 때 사용합니다.

### 문법

```sql
BACKUP DATABASE
  FROM start_time
  TO end_time
  INTO DISK = 'backup_path';
```

- `start_time`, `end_time`: `TO_DATE()` 함수로 표현한 시간 범위
- FROM 절을 생략하면 `1970-01-01 00:00:00`부터 적용됩니다.
- TO 절을 생략하면 명령 실행 시점의 현재 시간까지 적용됩니다.

### 예제

```sql
-- 특정 월 데이터 백업 (2024년 1월)
BACKUP DATABASE
  FROM TO_DATE('20240101','YYYYMMDD')
  TO   TO_DATE('20240131','YYYYMMDD')
  INTO DISK = '/backup/machbase_202401';

-- 특정 날짜 하루 데이터 백업
BACKUP DATABASE
  FROM TO_DATE('2024-01-15 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
  TO   TO_DATE('2024-01-15 23:59:59', 'YYYY-MM-DD HH24:MI:SS')
  INTO DISK = '/backup/machbase_20240115';

-- 테이블 단위 기간 백업
BACKUP TABLE sensor_log
  FROM TO_DATE('20240101','YYYYMMDD')
  TO   TO_DATE('20240131','YYYYMMDD')
  INTO DISK = '/backup/sensor_log_202401';
```

### 동작 방식

- 지정한 시간 범위에 속하는 데이터만 백업 파일에 포함됩니다.
- 시간 조건은 각 레코드의 입력 시각(`_arrival_time` 또는 태그 테이블의 타임스탬프 컬럼)을 기준으로 적용됩니다.
- 기간 백업으로 생성된 백업 파일도 마운트(`MOUNT DATABASE`)할 수 있습니다.

### 주요 활용 시나리오

#### 월별 아카이브

디스크 공간을 절약하기 위해 오래된 데이터를 기간 백업으로 아카이브한 뒤 원본 데이터를 삭제하는 방식입니다.

```bash
# 매월 말일에 해당 월 데이터를 아카이브
YEAR_MONTH="202401"
machsql -u sys -p manager -e "
  BACKUP DATABASE
    FROM TO_DATE('${YEAR_MONTH}01','YYYYMMDD')
    TO   TO_DATE('${YEAR_MONTH}31','YYYYMMDD')
    INTO DISK = '/archive/machbase_${YEAR_MONTH}';
"
```

#### 장기 보관 데이터 조회

아카이브된 기간 백업 파일을 마운트하여 과거 데이터를 현재 서버에서 직접 조회합니다.

```sql
-- 2024년 1월 아카이브 마운트
MOUNT DATABASE '/archive/machbase_202401' TO archive_202401;

-- 아카이브에서 조회
SELECT * FROM archive_202401.sys.sensor_log
 WHERE _arrival_time BETWEEN TO_DATE('20240110','YYYYMMDD')
                         AND TO_DATE('20240115','YYYYMMDD');

-- 조회 완료 후 언마운트
UMOUNT DATABASE archive_202401;
```

### 주의 사항

- TAG 테이블의 경우 기간 백업으로 복원(`machadmin -r`)하는 것은 지원되지 않습니다. 기간 백업을 마운트하여 읽기 전용으로 활용하는 방식은 사용 가능합니다.
- FROM과 TO 범위가 정확하게 지정되어야 원하는 데이터가 포함됩니다. 범위 경계값 포함 여부를 확인하세요.

<a id="sql-backup"></a>

## SQL BACKUP 범위

SQL `BACKUP` 문의 지원 범위를 에디션, 저장 방식, 테이블 타입에 따라 정리합니다.

### 에디션별 지원 범위

| 기능 | Standard Edition | Cluster Edition |
|------|:----------------:|:---------------:|
| `BACKUP DATABASE` | O | O |
| `BACKUP TABLE` | O | O |
| `MOUNT DATABASE` | O | 제한적 (거부될 수 있음) |
| `UMOUNT DATABASE` | O | 제한적 (거부될 수 있음) |
| RDB 테이블 백업 | O | X |

> Cluster Edition에서 `MOUNT` 및 `UMOUNT` 문은 거부될 수 있습니다. 클러스터 환경에서는 각 노드의 데이터를 개별적으로 관리하므로 마운트 방식의 조회가 제한됩니다.

### 저장 방식

검증 대상 빌드의 운영 절차는 `DISK` 백업을 기준으로 작성합니다. `DISK` 백업은 디렉터리 형태로 생성되며, `MOUNT DATABASE`로 검증하거나 읽기 전용 조회에 사용할 수 있습니다.

### 테이블 타입별 BACKUP 지원

| 테이블 타입 | BACKUP DATABASE | BACKUP TABLE | 비고 |
|------------|:---------------:|:------------:|------|
| LOG 테이블 | O | O | |
| TAG 테이블 | O | O | 기간 복원(machadmin -r) 제한 |
| LOOKUP 테이블 | O | O | |
| VOLATILE 테이블 | X | X | 메모리 기반, 백업 불가 |
| RDB 테이블 | △ | △ | Standard Edition 전용 |

### BACKUP DATABASE 문법 전체 구조

```sql
BACKUP [ DATABASE | TABLE table_name ]
  [ FROM start_time TO end_time ]
  INTO DISK = 'directory_path';

BACKUP DATABASE AFTER 'previous_backup_path'
  INTO DISK = 'incremental_backup_path';
```

### 백업 권한

일반 사용자가 `BACKUP DATABASE`를 실행하려면 SYS 사용자가 권한을 부여해야 합니다.

```sql
-- 백업 권한 부여
GRANT BACKUP ON machbasedb TO user_name;

-- 권한 회수
REVOKE BACKUP ON machbasedb FROM user_name;
```

권한 관리에 대한 자세한 내용은 [사용자 관리](/dbms/reference/sql/syntax-dictionary-sql/user-auth-syntax/) 섹션을 참고하세요.

### 백업 진행 상태 확인

백업이 실행 중인 동안 별도 세션에서 시스템 뷰를 통해 진행 상태를 확인할 수 있습니다.

```sql
-- 현재 실행 중인 세션 확인
SELECT * FROM v$session WHERE query LIKE '%BACKUP%';
```

<a id="offline-restore-machadmin-r"></a>

## Offline restore with machadmin -r

오프라인 복원은 서버를 완전히 중단한 상태에서 백업 데이터를 현재 데이터베이스로 교체하는 작업입니다. `machadmin -r` 명령을 사용합니다.

### 온라인 마운트와의 차이

| 항목 | Offline Restore (`machadmin -r`) | Online Mount (`MOUNT DATABASE`) |
|------|:---------------------------------:|:--------------------------------:|
| 서버 상태 | 중단 필요 | 운영 중 가능 |
| 현재 데이터 | 교체됨 (덮어씀) | 유지됨 |
| 결과 | 현재 DB = 백업 시점 상태 | 백업 DB 읽기 전용 접근 |
| 용도 | 재해 복구, 완전 롤백 | 과거 데이터 조회, 선택적 복구 |

### 복원 절차

```bash
# 1. (권장) 현재 데이터 백업 - 복원 후 현재 데이터는 사라짐
cat > /tmp/backup_before_restore.sql <<'SQL'
BACKUP DATABASE INTO DISK = '/backup/machbase_before_restore';
SQL
machsql -u sys -p manager -s 127.0.0.1 -f /tmp/backup_before_restore.sql

# 2. 서버 종료
machadmin -s

# 3. 기존 데이터베이스 삭제
machadmin -d

# 4. 백업 데이터로 복원
machadmin -r /backup/machbase_20240101

# 5. 서버 시작
machadmin -u
```

> 복원을 실행하면 현재 데이터베이스의 내용이 백업 시점으로 완전히 교체됩니다. 복원 전에 반드시 현재 데이터를 백업하거나 불필요한 데이터임을 확인하세요.

### 증분 백업 복원

증분 백업으로 복원할 때는 복원하려는 최종 증분 백업 디렉터리를 한 번 지정합니다. 증분 백업 디렉터리는 체인 정보를 포함하므로 전체 백업과 각 증분 백업을 `machadmin -r`로 반복 적용하지 않습니다.

```bash
# 서버 종료
machadmin -s

# 기존 데이터베이스 삭제
machadmin -d

# 복원하려는 최종 증분 백업 경로 지정
machadmin -r /backup/machbase_incr_20240103

# 서버 시작
machadmin -u
```

### machadmin 주요 옵션

| 옵션 | 설명 |
|------|------|
| `-s` (`--shutdown`) | 서버 정상 종료 |
| `-k` (`--kill`) | 서버 강제 종료 |
| `-u` (`--startup`) | 서버 시작 |
| `-d` (`--destroydb`) | 현재 데이터베이스 삭제 |
| `-r path` (`--restore`) | 지정한 백업 경로로 복원 |

### 복원 실패 시 확인 사항

복원이 실패하는 주요 원인과 해결 방법입니다.

| 원인 | 해결 방법 |
|------|-----------|
| 서버가 실행 중인 상태 | `machadmin -s`로 서버를 완전히 종료한 뒤 재시도 |
| 백업 경로가 존재하지 않음 | 경로가 정확한지 확인 |
| 백업 버전 불일치 | 동일한 메이저 버전 간에만 복원 가능 |
| 디스크 공간 부족 | `$MACHBASE_HOME/dbs` 경로의 여유 공간 확인 |

### 주의 사항

- `machadmin -r` 명령은 데이터베이스가 없는 상태에서 실행합니다.
- 복원 전 서버를 종료하고 현재 데이터베이스를 `machadmin -d`로 삭제해야 합니다.
- TAG 테이블은 기간 백업 복원이 지원되지 않습니다. 전체 백업 또는 증분 백업으로 복원하세요.

<a id="database-mount"></a>

## 데이터베이스 마운트

데이터베이스 마운트는 서버를 중단하거나 데이터를 복원하지 않고 백업 데이터베이스를 현재 서버에 연결하여 읽기 전용으로 접근하는 기능입니다.

### 마운트가 필요한 상황

- 운영 서버를 중단하지 않고 특정 시점의 과거 데이터를 확인해야 할 때
- 아카이브된 오래된 데이터에서 일부 레코드를 추출해야 할 때
- 백업 데이터를 복원 없이 빠르게 조회해야 할 때

### MOUNT DATABASE

```sql
MOUNT DATABASE 'backup_database_path' TO mount_name;
```

- `backup_database_path`: DISK 방식으로 생성된 백업 디렉터리 경로 (절대/상대 경로 모두 가능)
- `mount_name`: 마운트된 DB에 접근할 때 사용할 이름

```sql
-- 절대 경로로 마운트
MOUNT DATABASE '/backup/machbase_20240101' TO backup_db;

-- 상대 경로 (MACHBASE_HOME/dbs 기준)
MOUNT DATABASE 'machbase_20240101' TO backup_db;
```

### 마운트된 DB에서 데이터 조회

마운트된 데이터베이스의 테이블에 접근할 때는 `mount_name.user_name.table_name` 형식을 사용합니다.

```sql
-- 마운트 DB의 특정 테이블 조회
SELECT * FROM backup_db.sys.sensor_log
 WHERE _arrival_time > TO_DATE('2024-01-01','YYYY-MM-DD');

-- 집계 쿼리
SELECT name, COUNT(*), MIN(value), MAX(value)
  FROM backup_db.sys.sensor_log
 WHERE _arrival_time BETWEEN TO_DATE('20240101','YYYYMMDD')
                         AND TO_DATE('20240131','YYYYMMDD')
 GROUP BY name;

-- 현재 DB와 마운트 DB를 함께 조회
SELECT a.name, a.value AS current_value, b.value AS backup_value
  FROM sensor_log a
  JOIN backup_db.sys.sensor_log b ON a.name = b.name
 WHERE a._arrival_time > TO_DATE('20240201','YYYYMMDD');
```

### UMOUNT DATABASE

마운트된 데이터베이스가 더 이상 필요 없으면 언마운트합니다.

```sql
UMOUNT DATABASE mount_name;
```

```sql
-- 예제
UMOUNT DATABASE backup_db;
```

언마운트는 해당 마운트 DB를 참조 중인 열린 커서나 실행 중인 문장이 없을 때 즉시 실행됩니다. 마운트 DB를 참조 중이면 언마운트가 실패할 수 있으므로, 해당 문장과 세션을 종료한 뒤 다시 실행합니다.

### 마운트 조건

마운트 명령을 실행하려면 다음 조건을 충족해야 합니다.

- 백업 데이터베이스의 버전과 현재 서버의 메타데이터 버전이 호환되어야 합니다.
- DISK 방식으로 생성된 백업만 마운트할 수 있습니다 (IBFILE 방식 불가).
- 마운트된 DB에서는 테이블 생성, 인덱스 생성/삭제, 데이터 추가/삭제가 불가능합니다 (읽기 전용).

### 마운트 권한

일반 사용자가 `MOUNT DATABASE` 또는 `UMOUNT DATABASE`를 실행하려면 권한이 필요합니다.

```sql
-- SYS 사용자가 권한 부여
GRANT MOUNT ON machbasedb TO user_name;
```

### 에디션 참고

Cluster Edition에서는 `MOUNT` 및 `UMOUNT` 문이 거부될 수 있습니다. 마운트 기능은 주로 Standard Edition 환경에서 사용합니다.

<a id="query-database-mount"></a>

## 마운트된 데이터베이스 조회

마운트된 데이터베이스는 마운트 이름을 스키마처럼 사용하여 기존 SQL 문법으로 데이터를 조회합니다.

### 테이블 접근 방식

마운트된 DB의 테이블을 참조할 때는 마운트 이름과 소유자 이름을 점(`.`)으로 연결합니다.

```sql
SELECT column_name FROM mount_name.user_name.table_name;
```

예제:

```sql
-- SYS 사용자의 테이블 조회
SELECT * FROM backup_db.sys.sensor_log;

-- 조건 필터링
SELECT * FROM backup_db.sys.sensor_log
 WHERE _arrival_time > TO_DATE('2024-01-15','YYYY-MM-DD')
   AND name = 'sensor_01';

-- 집계
SELECT name, AVG(value) AS avg_val
  FROM backup_db.sys.sensor_log
 WHERE _arrival_time BETWEEN TO_DATE('20240101','YYYYMMDD')
                         AND TO_DATE('20240131','YYYYMMDD')
 GROUP BY name
 ORDER BY name;
```

### 마운트 목록 확인

현재 서버에 마운트된 데이터베이스 목록은 `V$STORAGE_MOUNT_DATABASES` 시스템 뷰에서 확인합니다.

```sql
SELECT * FROM v$storage_mount_databases;
```

| 컬럼 | 설명 |
|------|------|
| `NAME` | 백업 데이터베이스 내부 이름 |
| `PATH` | 백업 디렉터리 경로 |
| `BACKUP_TBSID` | 백업 테이블스페이스 ID |
| `BACKUP_SCN` | 백업 SCN |
| `MOUNTDB` | 마운트 이름 |
| `BACKUP_BEGIN_TIME`, `BACKUP_END_TIME` | 백업 수행 시간 |
| `DB_BEGIN_TIME`, `DB_END_TIME` | 백업에 포함된 데이터 시간 범위 |
| `FLAG` | 마운트 상태 플래그 |

### 조회 시 제약사항

마운트된 데이터베이스는 읽기 전용입니다. 다음 작업은 모두 오류가 발생합니다.

| 불가 작업 | 오류 사유 |
|-----------|-----------|
| `INSERT INTO backup_db.sys.t1 ...` | 마운트 DB는 읽기 전용 |
| `UPDATE backup_db.sys.t1 SET ...` | 마운트 DB는 읽기 전용 |
| `DELETE FROM backup_db.sys.t1 ...` | 마운트 DB는 읽기 전용 |
| `CREATE TABLE backup_db.sys.t2 ...` | 마운트 DB는 읽기 전용 |
| `CREATE INDEX ON backup_db.sys.t1 ...` | 마운트 DB는 읽기 전용 |

### 현재 DB로 데이터 복사

마운트 DB에서 선택한 데이터를 현재 운영 DB로 가져올 수 있습니다.

```sql
-- 마운트 DB의 특정 레코드를 현재 DB에 삽입
INSERT INTO sensor_log (name, time, value)
  SELECT name, time, value
    FROM backup_db.sys.sensor_log
   WHERE _arrival_time BETWEEN TO_DATE('20240115','YYYYMMDD')
                           AND TO_DATE('20240116','YYYYMMDD');
```

### 접근 권한

`GRANT MOUNT` 권한은 `MOUNT DATABASE`와 `UMOUNT DATABASE` 실행 권한입니다. 마운트된 테이블을 읽는 일반 사용자에게는 대상 마운트 DB의 테이블에 대한 `SELECT` 권한도 필요합니다.

```sql
-- 마운트/언마운트 실행 권한
GRANT MOUNT ON machbasedb TO analyst_user;

-- 마운트된 테이블 조회 권한
GRANT SELECT ON backup_db.sys.sensor_log TO analyst_user;
```

<a id="mounted-db-read-only-refcount-active-same-name"></a>

## mounted DB read-only/active reference/same-name isolation

마운트된 데이터베이스의 동작 특성인 읽기 전용 속성, 활성 참조, 동일 이름 충돌 방지에 대해 설명합니다.

### 읽기 전용 (Read-Only)

마운트된 데이터베이스는 반드시 읽기 전용으로만 접근할 수 있습니다. 이는 백업 데이터의 무결성을 보장하기 위한 설계입니다.

- 마운트 DB에 `INSERT`, `UPDATE`, `DELETE`를 실행하면 오류가 발생합니다.
- `CREATE TABLE`, `DROP TABLE`, `CREATE INDEX` 등 DDL도 실행할 수 없습니다.
- 마운트 DB의 내용은 마운트된 이후 변경되지 않으므로 특정 시점의 데이터를 신뢰할 수 있습니다.

```sql
-- 읽기 전용 확인 예제
MOUNT DATABASE '/backup/machbase_20240101' TO backup_db;

-- 아래 명령은 오류 발생
INSERT INTO backup_db.sys.sensor_log VALUES (...);  -- 오류: 읽기 전용
UPDATE backup_db.sys.sensor_log SET value = 0;      -- 오류: 읽기 전용
```

### 활성 참조

열린 커서나 실행 중인 문장이 마운트 DB를 참조하면 `UMOUNT DATABASE`가 실패할 수 있습니다.
참조가 종료된 뒤 다시 실행하면 언마운트할 수 있습니다. `V$STORAGE_MOUNT_DATABASES`는 내부
참조 카운트를 컬럼으로 노출하지 않습니다.

```sql
-- 현재 마운트 목록 확인
SELECT name, path, mountdb, backup_tbsid, backup_scn, flag
  FROM v$storage_mount_databases;
```

**활성 참조의 역할:**

- 마운트 DB를 사용 중인 세션이 있을 때 강제 언마운트를 방지합니다.
- `UMOUNT DATABASE` 명령은 열린 커서나 실행 중인 문장이 마운트 DB를 참조하지 않을 때 즉시 실행됩니다.
- 마운트 DB를 참조 중인 상태에서 `UMOUNT DATABASE`를 실행하면 오류가 반환될 수 있습니다.

```sql
-- 활성 쿼리가 완료된 후 언마운트
-- (활성 쿼리가 완료된 후 실행)
UMOUNT DATABASE backup_db;
```

### 동일 이름 충돌 방지 (Same-Name Isolation)

같은 이름으로 두 개의 마운트 데이터베이스를 동시에 생성할 수 없습니다.

```sql
-- 첫 번째 마운트 성공
MOUNT DATABASE '/backup/machbase_20240101' TO archive_db;

-- 동일 이름으로 다시 마운트 시도 - 오류 발생
MOUNT DATABASE '/backup/machbase_20240201' TO archive_db;  -- 오류: 이미 존재하는 이름
```

다른 백업을 같은 이름으로 마운트하려면 기존 마운트를 먼저 해제해야 합니다.

```sql
-- 기존 마운트 해제 후 새 마운트
UMOUNT DATABASE archive_db;
MOUNT DATABASE '/backup/machbase_20240201' TO archive_db;
```

### 동시 마운트

서버 한 대에 여러 개의 백업 데이터베이스를 동시에 마운트할 수 있습니다. 단, 각각 다른 이름을 사용해야 합니다.

```sql
-- 여러 백업을 동시에 마운트
MOUNT DATABASE '/backup/machbase_202401' TO archive_202401;
MOUNT DATABASE '/backup/machbase_202402' TO archive_202402;
MOUNT DATABASE '/backup/machbase_202403' TO archive_202403;

-- 각 마운트 DB에서 독립적으로 조회
SELECT COUNT(*) FROM archive_202401.sys.sensor_log;
SELECT COUNT(*) FROM archive_202402.sys.sensor_log;
SELECT COUNT(*) FROM archive_202403.sys.sensor_log;

-- 정리
UMOUNT DATABASE archive_202401;
UMOUNT DATABASE archive_202402;
UMOUNT DATABASE archive_202403;
```

### 마운트 상태 요약

| 상태 | 설명 |
|------|------|
| 마운트 직후 | 읽기 전용, 언마운트 가능 |
| 쿼리 실행 중 | 활성 참조 존재, 언마운트 실패 가능 |
| 쿼리 완료 후 | 활성 참조 종료, 언마운트 가능 |
| 언마운트 후 | 목록에서 제거됨 |

<a id="unsupported-support-scope-mount-table-umount"></a>

## MOUNT TABLE / UMOUNT TABLE 비공개 또는 미지원 범위

`MOUNT DATABASE`는 데이터베이스 전체를 단위로 마운트하는 공식 지원 기능입니다. 테이블 단위 마운트(`MOUNT TABLE`)는 현재 공개적으로 지원되지 않습니다.

### 테이블 단위 마운트 미지원

Machbase는 테이블 단위의 마운트(`MOUNT TABLE`)를 운영 절차용 공개 API로 제공하지 않습니다. 검증 대상 빌드에서 일부 내부 문법은 성공을 반환할 수 있지만, 활성 테이블을 백업 시점으로 노출하거나 일반적인 테이블 단위 복구 경로로 동작하지 않습니다.

- `MOUNT TABLE table_name IN DATABASE 'path'`는 운영 문서의 권장 경로가 아닙니다.
- `UMOUNT TABLE table_name IN DATABASE 'path'` 역시 일반 운영 절차로 사용하지 않습니다.

### 권장 대안: MOUNT DATABASE

특정 테이블의 데이터에만 접근하더라도 데이터베이스 전체 마운트를 사용하세요. 마운트된 데이터베이스에서 원하는 테이블만 선택적으로 조회하면 됩니다.

```sql
-- 전체 DB 마운트
MOUNT DATABASE '/backup/machbase_20240101' TO backup_db;

-- 특정 테이블만 조회
SELECT * FROM backup_db.sys.sensor_log
 WHERE _arrival_time > TO_DATE('2024-01-15','YYYY-MM-DD');

SELECT * FROM backup_db.sys.device_info
 WHERE device_id = 'DEV_001';

-- 사용 완료 후 언마운트
UMOUNT DATABASE backup_db;
```

### 테이블 백업과의 조합

특정 테이블만 백업한 경우에도 마운트는 `MOUNT DATABASE` 명령으로 수행합니다.

```sql
-- 테이블 단위 백업
BACKUP TABLE sensor_log INTO DISK = '/backup/sensor_log_20240101';

-- 테이블 백업 파일도 MOUNT DATABASE로 마운트
MOUNT DATABASE '/backup/sensor_log_20240101' TO tbl_backup;
SELECT * FROM tbl_backup.sys.sensor_log;
UMOUNT DATABASE tbl_backup;
```

### 요약

| 기능 | 지원 여부 |
|------|:---------:|
| `MOUNT DATABASE` | O (공식 지원) |
| `UMOUNT DATABASE` | O (공식 지원) |
| `MOUNT TABLE` | X (미공개/미지원) |
| `UMOUNT TABLE` | X (미공개/미지원) |

테이블 단위 마운트가 필요한 경우, 데이터베이스 전체를 마운트한 뒤 해당 테이블만 조회하는 방식을 사용하세요. 마운트는 읽기 전용이므로 다른 테이블에 영향을 주지 않습니다.

<a id="table-types-type-backup-mount"></a>

## 테이블 타입별 백업/마운트 제약

Machbase의 테이블 타입마다 백업과 마운트에 대한 지원 범위가 다릅니다. 백업 계획을 수립하기 전에 해당 테이블 타입의 제약사항을 확인하세요.

### 테이블 타입별 지원 여부

| 테이블 타입 | BACKUP | MOUNT | 기간 복원 | 비고 |
|------------|:------:|:-----:|:---------:|------|
| **TAG** | O | O | △ | 기간 백업은 마운트 검증 후 사용 권장 |
| **LOG** | O | O | O | |
| **LOOKUP** | O | O | O | |
| **VOLATILE** | X | X | X | 메모리 기반, 재시작 시 소멸 |
| **RDB** | O | O | △ | Standard Edition 전용 |

- **O**: 지원
- **X**: 미지원
- **△**: 기능별 조건 확인 필요

### 각 타입별 상세 설명

#### TAG 테이블

TAG 테이블은 전체 백업과 마운트를 모두 지원합니다. 단, `machadmin -r` 명령을 이용한 기간 백업 복원은 지원되지 않습니다.

```sql
-- TAG 테이블 백업 (전체)
BACKUP TABLE tag_table INTO DISK = '/backup/tag_table_20240101';

-- 마운트 후 조회
MOUNT DATABASE '/backup/tag_table_20240101' TO tag_backup;
SELECT * FROM tag_backup.sys.tag_table WHERE name = 'sensor_01';
UMOUNT DATABASE tag_backup;
```

#### LOG 테이블

가장 제약이 적은 테이블 타입입니다. 전체 백업, 기간 백업, 증분 백업, 마운트, 복원 모두 지원합니다.

#### LOOKUP 테이블

백업과 마운트를 지원합니다. LOOKUP 테이블은 주로 참조 데이터를 저장하므로 변경 빈도가 낮아 백업 주기를 길게 설정해도 무방합니다.

#### VOLATILE 테이블

메모리에만 존재하는 임시 테이블로, 서버가 재시작되면 데이터가 소멸합니다. 백업과 마운트를 모두 지원하지 않습니다. VOLATILE 테이블의 데이터를 영구 보관하려면 LOG 테이블이나 TAG 테이블로 데이터를 이동하거나 `SELECT INTO` 방식으로 내보내야 합니다.

#### RDB 테이블

Standard Edition에서만 사용 가능한 테이블 타입입니다. `BACKUP DATABASE`와 `BACKUP TABLE`의
대상에 포함되며, 백업본을 마운트하면 읽기 전용으로 조회할 수 있습니다. 자세한 내용은
[RDB 백업·복원·마운트](/dbms/rdb-table-usage/backup-restore-mount/)를 참고하세요.

### BACKUP DATABASE 실행 시 포함 범위

`BACKUP DATABASE` 명령은 VOLATILE 테이블을 제외한 모든 테이블을 백업 대상에 포함합니다. RDB 테이블은 Standard Edition에서만 포함됩니다.

```sql
-- 전체 백업 실행 시 포함 범위
-- - LOG 테이블: 포함
-- - TAG 테이블: 포함
-- - LOOKUP 테이블: 포함
-- - VOLATILE 테이블: 제외 (메모리 기반)
-- - RDB 테이블: Standard Edition에서만 포함
BACKUP DATABASE INTO DISK = '/backup/machbase_20240101';
```
