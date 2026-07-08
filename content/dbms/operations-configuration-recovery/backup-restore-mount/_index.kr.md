---
type: docs
title: '백업, 복원, 마운트'
weight: 60
---

이 섹션에서는 Machbase 데이터베이스의 백업, 복원, 마운트 기능을 설명합니다.

운영 환경에서 데이터를 안전하게 보호하고 필요 시 복구하기 위한 세 가지 핵심 기능을 다룹니다.

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
| [백업 개요](./backup/) | 백업 방식 비교, 선택 기준, 주기 권장 |
| [전체 백업](./backup-full/) | `BACKUP DATABASE INTO DISK` 전체 백업 |
| [테이블 백업](./backup-table/) | `BACKUP TABLE` 특정 테이블 백업 |
| [증분 백업과 AFTER 기준 경로](./backup-incremental-after/) | 마지막 백업 이후 변경분만 백업 |
| [기간 백업](./backup-period/) | 특정 시간 범위 데이터 백업 |
| [SQL BACKUP 범위](./sql-backup/) | 지원 테이블 타입, 에디션별 차이 |
| [테이블 타입별 백업/마운트 제약](./table-types-type-backup-mount/) | 타입별 지원 여부 |
| [Offline restore with machadmin -r](./offline-restore-machadmin-r/) | 오프라인 복원 절차 |
| [데이터베이스 마운트](./database-mount/) | MOUNT / UNMOUNT 사용법 |
| [마운트된 데이터베이스 조회](./query-database-mount/) | 마운트 DB에서 SELECT |
| [마운트 DB 동작 특성](./mounted-db-read-only-refcount-active-same-name/) | 읽기 전용, 활성 참조, 이름 충돌 |
| [RDB sidecar 백업/복구 제약](./recovery-backup-rdb-sidecar/) | Standard Edition RDB 처리 |
| [MOUNT TABLE 미지원 범위](./unsupported-support-scope-mount-table-umount/) | 테이블 단위 마운트 제약 |

## 권한 요구 사항

Machbase 8.5 이상에서는 일반 사용자가 백업과 마운트를 실행하려면 별도 권한이 필요합니다.

```sql
-- 백업 권한 부여
GRANT BACKUP ON machbasedb TO user_name;

-- 마운트 권한 부여
GRANT MOUNT ON machbasedb TO user_name;
```
