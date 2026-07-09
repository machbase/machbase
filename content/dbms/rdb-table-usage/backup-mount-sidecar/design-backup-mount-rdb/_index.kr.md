---
type: docs
title: '8.14.2 백업·마운트'
weight: 100
---

RDB 테이블은 Machbase 백업 및 마운트 기능을 통해 데이터를 보호하고 복원할 수 있습니다.

## 백업

RDB 테이블은 다른 테이블과 함께 데이터베이스 백업에 포함됩니다.

```sql
-- 전체 데이터베이스 백업
BACKUP DATABASE INTO DISK = '/backup/machbase_backup_20240101';

-- 증분 백업
BACKUP DATABASE AFTER '/backup/machbase_backup_20240101' INTO DISK = '/backup/machbase_backup_20240102';
```

## 마운트

백업된 데이터베이스를 마운트하여 읽기 전용으로 접근할 수 있습니다.

```sql
-- 백업 마운트
MOUNT DATABASE '/backup/machbase_backup_20240101' TO backup_db;

-- 마운트된 RDB 테이블 조회
SELECT * FROM backup_db.order_history
WHERE order_time >= '2024-01-01';

-- 마운트 해제
UMOUNT DATABASE backup_db;
```

## 시점 복구

```bash
# 특정 백업으로 복원
machadmin -r '/backup/machbase_backup_20240101'
```

## 주의사항

- 백업 중 DML은 계속 가능하지만, DDL은 제한될 수 있습니다.
- RDB 테이블의 데이터 보존 정책은 운영 설정에서 관리합니다.
- 자세한 백업·복구 절차는 [운영 및 구성](/dbms/operations-configuration-recovery/)을 참고하십시오.
