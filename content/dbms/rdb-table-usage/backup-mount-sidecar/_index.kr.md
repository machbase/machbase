---
title: '8.14 RDB 백업, 마운트, sidecar'
weight: 140
toc: true
---

RDB 테이블의 백업·복원 절차와 sidecar 구조의 특성, 복구 방법을 다룹니다.


<a id="error-rdb-sidecar"></a>

## RDB sidecar 누락/손상 오류

RDB 테이블은 내부적으로 SQLite 기반 sidecar를 통해 관리됩니다. sidecar 파일이 누락되거나 손상되면 RDB 테이블 접근 시 오류가 발생합니다.

{{< callout type="info" >}}
**참고**: RDB sidecar 관련 제약 및 백업/복구 동작에 대한 상세 내용은 [RDB sidecar 백업/복구 제약](/dbms/rdb-table-usage/backup-mount-sidecar/#recovery-backup-rdb-sidecar)을 참고하십시오.
{{< /callout >}}

{{< callout type="warning" >}}
**Cluster Edition 해당 없음**: RDB 테이블은 Standard Edition 전용입니다. Cluster Edition에는 적용되지 않습니다.
{{< /callout >}}

### 증상

- RDB 테이블에 SELECT/INSERT/UPDATE를 실행하면 오류 발생
- 서버 시작은 정상이지만 RDB 쿼리만 실패
- 트레이스 로그에 sidecar 관련 오류 메시지 출력

### 진단

#### 1. sidecar 파일 존재 여부 확인

```bash
# sidecar DB 파일 확인
ls -la $MACHBASE_HOME/dbs/__rdbt_*.db
```

파일이 없거나 크기가 0이면 누락 또는 손상된 것입니다.

#### 2. 트레이스 로그 확인

```bash
grep -i "rdb\|sidecar\|sqlite\|error" $MACHBASE_HOME/trc/machbase.trc | tail -30
```

#### 3. RDB 테이블 목록 확인

복구 후 재생성이 필요한 테이블 목록을 파악합니다.

```sql
-- RDB 테이블 목록 조회 (시스템 테이블 이용)
SELECT name FROM m$sys_tables WHERE type = 8;
```

### 복구 방법

#### 방법 1: 백업에서 sidecar 파일 복원

최근 백업이 있다면 백업에서 sidecar 파일을 복원합니다.

```bash
# 1. 서버 종료
machadmin -s

# 2. 백업에서 전체 복원 (sidecar 포함)
machadmin -r /backup/machbase_20240101

# 3. 서버 시작
machadmin -u
```

백업에서 복원하면 sidecar 파일도 함께 복원됩니다. 단, 백업 시점 이후의 RDB 데이터는 복구되지 않습니다.

#### 방법 2: RDB 테이블 재생성

백업이 없거나 복원이 불가능한 경우 RDB 테이블을 재생성합니다. **기존 RDB 데이터는 손실됩니다.**

재생성 전에 손상된 sidecar 파일을 별도로 백업해 둡니다.

```bash
# 손상된 sidecar 파일 백업 (혹시 복구 가능할 경우를 대비)
mkdir -p /tmp/rdb_backup
cp $MACHBASE_HOME/dbs/__rdbt_*.db /tmp/rdb_backup/
```

애플리케이션의 DDL 스크립트를 이용하거나 직접 CREATE TABLE을 실행하여 재생성합니다.

```sql
-- RDB 테이블 재생성 예시
CREATE RDB TABLE rdb_config (
    config_key   VARCHAR(128) PRIMARY KEY,
    config_value VARCHAR(4096),
    updated_at   DATETIME
);
```

### RDB 테이블 사전 백업 권장

RDB 테이블 구조와 데이터를 주기적으로 별도 백업해 두면 복구 시 활용할 수 있습니다.

```sql
-- RDB 테이블 목록 및 정의 확인
SELECT name FROM m$sys_tables WHERE type = 8;

-- 개별 RDB 테이블 백업
BACKUP TABLE rdb_config INTO DISK = '/backup/rdb_config_20240101';
```

데이터 중요도에 따라 CSV 내보내기나 외부 시스템 복사도 고려합니다.

<a id="design-backup-mount-rdb"></a>

## 백업·마운트

RDB 테이블은 Machbase 백업 및 마운트 기능으로 데이터를 보호하고 복원할 수 있습니다.

### 백업

RDB 테이블은 다른 테이블과 함께 데이터베이스 백업에 포함됩니다.

```sql
-- 전체 데이터베이스 백업
BACKUP DATABASE INTO DISK = '/backup/machbase_backup_20240101';

-- 증분 백업
BACKUP DATABASE AFTER '/backup/machbase_backup_20240101' INTO DISK = '/backup/machbase_backup_20240102';
```

### 마운트

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

### 시점 복구

```bash
# 특정 백업으로 복원
machadmin -r '/backup/machbase_backup_20240101'
```

### 주의사항

- 백업 중 DML은 계속 가능하지만, DDL은 제한될 수 있습니다.
- RDB 테이블의 데이터 보존 정책은 운영 설정에서 관리합니다.
- 자세한 백업·복구 절차는 [운영 및 구성](/dbms/operations-configuration-recovery/)을 참고하십시오.

<a id="recovery-backup-rdb-sidecar"></a>

## RDB sidecar 백업/복구 제약

RDB 테이블은 Standard Edition 전용 관계형 테이블입니다. 내부 구현이 LOG/TAG 테이블과 다르므로 백업·복구 시 추가 고려가 필요합니다.

> **참고**: RDB 테이블 백업/복구는 Standard Edition에서만 해당됩니다. Cluster Edition에는 적용되지 않습니다.

### RDB 테이블의 저장 구조

RDB 테이블은 엔진 내부에서 별도의 sidecar 데이터베이스(SQLite 등)로 관리됩니다. 데이터 파일이 Machbase의 일반 데이터 파일과 별도로 존재합니다.

```
$MACHBASE_HOME/dbs/
├── ...                    # Machbase 일반 데이터 파일
└── __rdbt_<table_id>.db   # RDB sidecar 데이터 파일
```

### 백업 시 동작

`BACKUP DATABASE` 실행 시 RDB 테이블의 sidecar 파일도 백업에 포함됩니다.

```sql
-- 전체 백업 (RDB 테이블 포함)
BACKUP DATABASE INTO DISK = '/backup/machbase_20240101';
```

`BACKUP TABLE`로 개별 백업하는 경우에도 sidecar 파일이 함께 복사됩니다.

```sql
-- RDB 테이블 단위 백업
BACKUP TABLE rdb_table_name INTO DISK = '/backup/rdb_table_20240101';
```

### 복원 시 주의사항

`machadmin -r`로 복원할 때 백업 이미지의 `rdb/__rdbt_*.db` 파일이 `$MACHBASE_HOME/dbs/`로 복사됩니다. 다음 사항을 확인해야 합니다.

1. **기존 DB 삭제**: 복원 전에 서버를 종료하고 현재 데이터베이스를 삭제합니다.
2. **sidecar 버전 호환성**: sidecar DB 버전이 현재 Machbase와 호환되어야 합니다.
3. **잠금 상태 확인**: sidecar DB 파일이 다른 프로세스에 의해 잠겨 있지 않아야 합니다.

```bash
# 복원 절차 (RDB 포함)
machadmin -s                                    # 서버 종료
machadmin -d                                    # 현재 DB 삭제
machadmin -r /backup/machbase_20240101          # 복원 (RDB sidecar 포함)
machadmin -u                                    # 서버 시작
```

### 마운트 시 동작

RDB 테이블이 포함된 백업을 마운트할 때도 sidecar 파일이 함께 참조됩니다. 마운트 DB에서 RDB 테이블을 조회하는 방법은 일반 테이블과 동일합니다.

```sql
MOUNT DATABASE '/backup/machbase_20240101' TO backup_db;

-- RDB 테이블 조회
SELECT * FROM backup_db.sys.rdb_table_name;

UNMOUNT DATABASE backup_db;
```

### 제약사항 요약

| 항목 | 내용 |
|------|------|
| 지원 에디션 | Standard Edition 전용 |
| 백업 방식 | DISK 방식 기준 |
| sidecar 자동 포함 | BACKUP DATABASE 실행 시 자동 포함 |
| 복원 | machadmin -r 명령으로 sidecar 포함 복원 |
| 마운트 조회 | 읽기 전용으로 지원 |
| 기간 백업 복원 | 제한적 (테이블 타입에 따라 다름) |
