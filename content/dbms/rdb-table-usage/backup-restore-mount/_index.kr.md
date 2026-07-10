---
title: '8.14 RDB 백업, 복원, 마운트'
weight: 140
toc: true
---

RDB 테이블은 Machbase 데이터베이스 백업과 복원 대상에 포함됩니다. 다른 영속 테이블과 같은
백업, 복원, 마운트 명령을 사용합니다.

<a id="support-scope-backup-rdb"></a>

## 지원 범위

| 작업 | 지원 | 설명 |
|------|:----:|------|
| `BACKUP DATABASE` | O | RDB 테이블을 포함한 데이터베이스 전체 백업 |
| `BACKUP TABLE` | O | 지정한 RDB 테이블 백업 |
| 증분 백업 | O | `BACKUP DATABASE AFTER ...` 사용 |
| 오프라인 복원 | O | 서버를 중지하고 `machadmin -r` 실행 |
| `MOUNT DATABASE` | O | 백업본의 RDB 테이블을 읽기 전용으로 조회 |

RDB 테이블은 Standard Edition에서 지원합니다. Cluster Edition에서는 RDB 테이블을 생성하거나
복원할 수 없습니다.

<a id="backup-rdb"></a>

## 백업

### 데이터베이스 전체 백업

`BACKUP DATABASE`는 RDB 테이블을 포함한 데이터베이스 전체를 온라인 상태에서 백업합니다.

```sql
BACKUP DATABASE INTO DISK = '/backup/machbase_20260710';
```

백업 명령이 성공하면 지정한 경로에 백업 이미지가 생성됩니다. 이미 존재하는 디렉터리를
지정하면 오류가 발생하므로 백업마다 고유한 경로를 사용합니다.

### RDB 테이블 백업

특정 RDB 테이블만 백업하려면 `BACKUP TABLE`을 사용합니다.

```sql
BACKUP TABLE order_history
INTO DISK = '/backup/order_history_20260710';
```

테이블 백업에도 데이터베이스 백업과 동일한 경로·권한 정책이 적용됩니다.

### 증분 백업

기준 백업 이후의 변경분을 저장하려면 `AFTER` 절을 사용합니다.

```sql
BACKUP DATABASE
AFTER '/backup/machbase_20260710'
INTO DISK = '/backup/machbase_20260711_inc';
```

운영 환경에서는 정기적인 전체 백업 사이에 증분 백업을 배치하고, 복원 훈련으로 전체 체인이
정상인지 확인합니다.

<a id="verify-backup-rdb"></a>

## 백업 검증

백업 완료 메시지만 확인하지 말고 백업본을 마운트하여 주요 RDB 테이블의 행 수와 핵심 값을
검증합니다.

```sql
MOUNT DATABASE '/backup/machbase_20260710' TO verify_db;

SELECT COUNT(*)
FROM verify_db.sys.order_history;

SELECT order_id, status, amount
FROM verify_db.sys.order_history
ORDER BY order_id
LIMIT 10;

UMOUNT DATABASE verify_db;
```

검증 쿼리 결과와 백업 시점의 운영 점검 기록을 함께 보관하면 복원 시 데이터 일관성을 비교할
수 있습니다.

<a id="restore-rdb"></a>

## 복원

`machadmin -r`은 백업 이미지에 포함된 RDB 테이블을 다른 영속 테이블과 함께 복원합니다.

{{< callout type="warning" >}}
복원은 현재 데이터베이스를 교체하는 작업입니다. 서버 중지 시간과 데이터 손실 범위를 확인하고,
복원 대상 백업을 별도 환경에서 먼저 검증하십시오.
{{< /callout >}}

```bash
# 1. 서버 중지
machadmin -s

# 2. 현재 데이터베이스 제거
machadmin -d

# 3. 백업 이미지 복원
machadmin -r /backup/machbase_20260710

# 4. 서버 시작
machadmin -u
```

복원 후에는 RDB 테이블 목록, 행 수, 주요 제약 조건과 인덱스를 확인합니다.

```sql
SELECT name
FROM m$sys_tables
WHERE type = 8
ORDER BY name;

SELECT COUNT(*) FROM order_history;
```

전체 복원 절차와 권한, 중단 시간 계획은
[백업, 복원, 마운트](/dbms/operations-configuration-recovery/backup-restore-mount/)를
참고합니다.

<a id="mount-rdb"></a>
<a id="design-backup-mount-rdb"></a>

## 마운트

백업 이미지를 현재 서버에 마운트하면 백업 시점의 RDB 테이블을 읽기 전용으로 조회할 수
있습니다.

```sql
MOUNT DATABASE '/backup/machbase_20260710' TO backup_db;

SELECT order_id, status, amount
FROM backup_db.sys.order_history
WHERE order_time >= '2026-07-01 00:00:00';

UMOUNT DATABASE backup_db;
```

마운트된 RDB 테이블에는 `INSERT`, `UPDATE`, `DELETE`와 DDL을 실행할 수 없습니다. 운영
테이블과 백업 테이블을 함께 조회할 때는 `mount_name.user_name.table_name` 형식으로 대상을
명확히 구분합니다.

```sql
SELECT active.order_id,
       active.status AS current_status,
       backup.status AS backup_status
FROM order_history active
JOIN backup_db.sys.order_history backup
  ON active.order_id = backup.order_id;
```

열린 커서가 마운트 DB를 참조하고 있으면 `UMOUNT DATABASE`가 실패할 수 있습니다. 조회를
종료하고 결과 커서를 닫은 뒤 다시 실행합니다.

<a id="troubleshooting-backup-rdb"></a>

## 문제 해결

| 증상 | 확인 사항 | 조치 |
|------|-----------|------|
| 백업 경로 생성 실패 | 상위 디렉터리 권한, 동일 경로 존재 여부 | 쓰기 권한을 부여하고 새 경로 사용 |
| RDB 테이블이 복원되지 않음 | 백업 시점의 테이블 존재 여부, Edition | 올바른 Standard Edition 백업 선택 |
| 마운트 후 테이블을 찾을 수 없음 | 마운트 이름, 사용자 이름, 테이블 이름 | 3단계 이름으로 조회 |
| 마운트 테이블 변경 실패 | 마운트 DB의 읽기 전용 속성 | 운영 테이블에 변경 적용 |
| `UMOUNT DATABASE` 실패 | 열린 결과 커서와 실행 중 쿼리 | 참조 종료 후 다시 실행 |

서버 오류가 발생하면 SQL 오류 코드와 `$MACHBASE_HOME/trc/machbase.trc`를 확인합니다. 백업
이미지의 내부 파일을 직접 수정하거나 일부 파일만 복사해 복구하지 않습니다.

## 운영 체크리스트

- RDB 테이블을 데이터베이스 백업 범위에 포함합니다.
- 전체 백업과 증분 백업의 보존 주기를 정합니다.
- 백업본을 정기적으로 마운트하여 행 수와 주요 데이터를 검증합니다.
- 복원 절차와 예상 중단 시간을 별도 환경에서 점검합니다.
- 테이블 DDL과 인덱스 정의를 형상 관리합니다.
- RDB 테이블 데이터 정리는 Retention Policy 대신 업무 조건에 맞는 `DELETE`로 수행합니다.
