---
type: docs
title: '테이블 타입별 백업/마운트 제약'
weight: 130
---

Machbase의 테이블 타입마다 백업과 마운트에 대한 지원 범위가 다릅니다. 백업 계획을 수립하기 전에 해당 테이블 타입의 제약사항을 확인하세요.

## 테이블 타입별 지원 여부

| 테이블 타입 | BACKUP | MOUNT | 기간 복원 | 비고 |
|------------|:------:|:-----:|:---------:|------|
| **TAG** | O | O | X | TAG 테이블은 기간 백업 복원(machadmin -r) 미지원 |
| **LOG** | O | O | O | |
| **LOOKUP** | O | O | O | |
| **VOLATILE** | X | X | X | 메모리 기반, 재시작 시 소멸 |
| **RDB** | △ | △ | △ | Standard Edition 전용, sidecar 처리 필요 |

- **O**: 지원
- **X**: 미지원
- **△**: 조건부 지원 (에디션 또는 추가 처리 필요)

## 각 타입별 상세 설명

### TAG 테이블

TAG 테이블은 전체 백업과 마운트를 모두 지원합니다. 단, `machadmin -r` 명령을 이용한 기간 백업 복원은 지원되지 않습니다.

```sql
-- TAG 테이블 백업 (전체)
BACKUP TABLE tag_table INTO DISK = '/backup/tag_table_20240101';

-- 마운트 후 조회
MOUNT DATABASE '/backup/tag_table_20240101' TO tag_backup;
SELECT * FROM tag_backup.sys.tag_table WHERE name = 'sensor_01';
UNMOUNT DATABASE tag_backup;
```

### LOG 테이블

가장 제약이 적은 테이블 타입입니다. 전체 백업, 기간 백업, 증분 백업, 마운트, 복원 모두 지원합니다.

### LOOKUP 테이블

백업과 마운트를 지원합니다. LOOKUP 테이블은 주로 참조 데이터를 저장하므로 변경 빈도가 낮아 백업 주기를 길게 설정해도 무방합니다.

### VOLATILE 테이블

메모리에만 존재하는 임시 테이블로, 서버가 재시작되면 데이터가 소멸합니다. 백업과 마운트를 모두 지원하지 않습니다. VOLATILE 테이블의 데이터를 영구 보관하려면 LOG 테이블이나 TAG 테이블로 데이터를 이동하거나 `SELECT INTO` 방식으로 내보내야 합니다.

### RDB 테이블

Standard Edition에서만 사용 가능한 테이블 타입입니다. 내부적으로 sidecar 데이터베이스(SQLite 등)에 저장될 수 있으며, 백업과 복원 시 sidecar 파일도 함께 처리해야 합니다. 자세한 내용은 [RDB sidecar 백업/복구 제약](../recovery-backup-rdb-sidecar/)을 참고하세요.

## BACKUP DATABASE 실행 시 포함 범위

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
