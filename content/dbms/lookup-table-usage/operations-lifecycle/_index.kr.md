---
title: '9.7 운영과 데이터 생명주기'
weight: 70
toc: true
---
운영과 데이터 생명주기에 해당하는 세부 문서를 모았습니다.


<a id="recovery-support-scope-backup-lookup"></a>

## 백업·복구 지원 범위

LOOKUP 테이블은 디스크에 영속 저장되며 데이터베이스 백업에 포함됩니다.

### 백업 포함 여부

| 테이블 타입 | 데이터베이스 백업 포함 |
|-----------|-------------------|
| TAG | O |
| LOG | O |
| RDB | O |
| **LOOKUP** | **O** |
| VOLATILE | X (메모리 전용) |

### 백업

```sql
-- LOOKUP 테이블 데이터는 전체 백업에 자동 포함
BACKUP DATABASE INTO DISK = '/backup/machbase_20240101';
```

### 복구

```bash
# 데이터베이스 복원 시 LOOKUP 테이블 데이터도 함께 복원
machadmin -r '/backup/machbase_20240101'
```

### 마운트를 통한 조회

```sql
-- 백업을 마운트하여 LOOKUP 테이블 데이터 조회
MOUNT DATABASE '/backup/machbase_20240101' TO old_db;

SELECT * FROM old_db.country_code;

UMOUNT DATABASE old_db;
```

### 주의사항

- LOOKUP 테이블은 서버 재시작 후에도 데이터가 유지됩니다.
- VOLATILE 테이블과 달리 데이터 손실 위험이 없습니다.
- 대용량 LOOKUP 테이블은 백업 시간에 영향을 줄 수 있습니다.
