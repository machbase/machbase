---
title: '8.13 TRANSACTION 백업, 복원, 마운트'
weight: 140
toc: true
---

TRANSACTION 테이블은 Standard Edition의 영속 테이블이며 데이터베이스 백업, 복원과
마운트 범위에 포함됩니다. 이 페이지는 TRANSACTION에만 해당하는 범위를 설명합니다.
공통 문법은 [BACKUP / RESTORE / MOUNT syntax](/dbms/reference/sql/syntax-dictionary-sql/backup-restore-mount-syntax/)를,
운영 절차는 [백업, 복원, 마운트](/dbms/operations-configuration-recovery/backup-restore-mount/)를
정본으로 사용하십시오.

<a id="support-scope-backup-rdb"></a>

## 지원 범위

| 작업 | 지원 | TRANSACTION 관련 설명 |
|------|:----:|-----------------------|
| `BACKUP DATABASE` | O | 다른 영속 테이블과 함께 포함 |
| `BACKUP TABLE` | O | 지정한 TRANSACTION 테이블 백업 |
| 증분 백업 | O | 기준 백업 이후 변경분 포함 |
| 오프라인 복원 | O | `machadmin -r`로 다른 영속 테이블과 함께 복원 |
| `MOUNT DATABASE` | O | 백업 시점의 테이블을 읽기 전용으로 조회 |

TRANSACTION은 Cluster Edition에서 지원하지 않습니다. 다른 Edition에서 생성한
TRANSACTION 객체가 포함된 백업을 Cluster에 복원하는 경로로 사용하지 마십시오.

<a id="backup-rdb"></a>

## 백업 시 확인 사항

- 데이터베이스 백업 정책에 TRANSACTION 테이블을 별도로 빠뜨릴 필요가 없습니다.
- 단일 테이블 백업이 필요하면 공통 `BACKUP TABLE` 문법을 사용합니다.
- 전체·증분 백업의 보존 주기와 최종 복구 지점을 함께 기록합니다.
- 백업 경로, 권한과 기존 디렉터리 충돌은 공통 백업 정책을 따릅니다.

<a id="verify-backup-rdb"></a>

## 백업 검증

백업을 마운트한 뒤 주요 TRANSACTION 테이블의 행 수, 키와 제약이 기대한 시점과
일치하는지 확인합니다.

```sql
SELECT COUNT(*) FROM verify_db.sys.order_history;

SELECT order_id, status, amount
  FROM verify_db.sys.order_history
 ORDER BY order_id
 LIMIT 10;
```

<a id="restore-rdb"></a>

## 복원 후 확인 사항

오프라인 인스턴스 복원 후 다음 항목을 확인합니다.

1. TRANSACTION 테이블 목록과 소유자
2. 주요 테이블의 행 수와 업무 기준 값
3. PRIMARY KEY, UNIQUE INDEX와 일반 인덱스
4. 애플리케이션 계정의 권한
5. 명시적 트랜잭션을 사용하는 핵심 업무 흐름

<a id="mount-rdb"></a>
<a id="design-backup-mount-rdb"></a>

## 마운트 조회

mounted database의 TRANSACTION 테이블은 읽기 전용입니다. INSERT, UPDATE, DELETE와 DDL을
실행할 수 없습니다. `mount_name.user_name.table_name` 형식으로 운영 테이블과 명확히
구분하십시오.

```sql
SELECT active.order_id,
       active.status AS current_status,
       backup.status AS backup_status
  FROM order_history active
  JOIN backup_db.sys.order_history backup
    ON active.order_id = backup.order_id;
```

열린 cursor가 mounted database를 참조하면 `UMOUNT DATABASE`가 실패할 수 있습니다.
조회와 cursor를 종료한 뒤 다시 실행하십시오.

<a id="troubleshooting-backup-rdb"></a>

## 문제 해결

| 증상 | 확인 사항 |
|------|-----------|
| 테이블이 복원되지 않음 | 백업 시점의 객체 존재 여부와 Standard Edition 백업인지 확인 |
| 마운트 후 테이블을 찾지 못함 | mount, owner, table의 3단계 이름 확인 |
| mounted 테이블 변경 실패 | 읽기 전용이므로 active database에서 변경 |
| `UMOUNT DATABASE` 실패 | 열린 결과 cursor와 실행 중 query 종료 |

백업 이미지 내부 파일을 직접 수정하거나 일부 파일만 복사해 복구하지 마십시오.
