---
type: docs
title: '8.14.3 RDB sidecar 백업/복구 제약'
weight: 110
---

RDB 테이블은 Machbase Standard Edition에서만 사용 가능한 관계형 테이블 타입입니다. 내부 구현 방식이 LOG/TAG 테이블과 다르기 때문에 백업과 복구 시 추가적인 고려가 필요합니다.

> **참고**: RDB 테이블 백업/복구는 Standard Edition에서만 해당됩니다. Cluster Edition에는 적용되지 않습니다.

## RDB 테이블의 저장 구조

RDB 테이블은 Machbase 엔진 내부에서 별도의 sidecar 데이터베이스(SQLite 등)를 통해 관리됩니다. 이 때문에 데이터 파일이 Machbase의 일반 데이터 파일과 별도로 존재할 수 있습니다.

```
$MACHBASE_HOME/dbs/
├── ...                    # Machbase 일반 데이터 파일
└── __rdbt_<table_id>.db   # RDB sidecar 데이터 파일
```

## 백업 시 동작

`BACKUP DATABASE` 명령을 실행하면 RDB 테이블의 sidecar 파일도 백업에 포함됩니다.

```sql
-- 전체 백업 (RDB 테이블 포함)
BACKUP DATABASE INTO DISK = '/backup/machbase_20240101';
```

RDB 테이블만 개별 백업(`BACKUP TABLE`)하는 경우에도 sidecar 파일이 함께 복사됩니다.

```sql
-- RDB 테이블 단위 백업
BACKUP TABLE rdb_table_name INTO DISK = '/backup/rdb_table_20240101';
```

## 복원 시 주의사항

`machadmin -r` 명령으로 복원할 때 백업 이미지의 `rdb/__rdbt_*.db` 파일이 현재 `$MACHBASE_HOME/dbs/`로 복사됩니다. 단, 다음 사항을 확인해야 합니다.

1. **기존 DB 삭제**: 복원 전에 서버를 종료하고 현재 데이터베이스를 삭제해야 합니다.
2. **sidecar 버전 호환성**: RDB sidecar DB의 버전이 현재 Machbase와 호환되어야 합니다.
3. **잠금 상태 확인**: 복원 전에 sidecar DB 파일이 다른 프로세스에 의해 잠겨 있지 않아야 합니다.

```bash
# 복원 절차 (RDB 포함)
machadmin -s                                    # 서버 종료
machadmin -d                                    # 현재 DB 삭제
machadmin -r /backup/machbase_20240101          # 복원 (RDB sidecar 포함)
machadmin -u                                    # 서버 시작
```

## 마운트 시 동작

RDB 테이블이 포함된 백업을 마운트할 때도 sidecar 파일이 함께 참조됩니다. 마운트 DB에서 RDB 테이블을 조회하는 방법은 일반 테이블과 동일합니다.

```sql
MOUNT DATABASE '/backup/machbase_20240101' TO backup_db;

-- RDB 테이블 조회
SELECT * FROM backup_db.sys.rdb_table_name;

UNMOUNT DATABASE backup_db;
```

## 제약사항 요약

| 항목 | 내용 |
|------|------|
| 지원 에디션 | Standard Edition 전용 |
| 백업 방식 | DISK 방식 기준 |
| sidecar 자동 포함 | BACKUP DATABASE 실행 시 자동 포함 |
| 복원 | machadmin -r 명령으로 sidecar 포함 복원 |
| 마운트 조회 | 읽기 전용으로 지원 |
| 기간 백업 복원 | 제한적 (테이블 타입에 따라 다름) |
