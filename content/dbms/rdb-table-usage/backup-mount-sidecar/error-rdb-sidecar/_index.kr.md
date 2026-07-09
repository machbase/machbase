---
type: docs
title: 'RDB sidecar 누락/손상 오류'
weight: 20
---

Machbase Standard Edition에서 RDB 테이블은 내부적으로 SQLite 기반의 sidecar를 통해 관리됩니다. sidecar 파일이 누락되거나 손상되면 RDB 테이블에 접근할 때 오류가 발생합니다.

{{< callout type="info" >}}
**참고**: RDB sidecar 관련 제약 및 백업/복구 동작에 대한 상세 내용은 [RDB sidecar 백업/복구 제약](../../../operations-configuration-recovery/backup-restore-mount/recovery-backup-rdb-sidecar/)을 참고하십시오.
{{< /callout >}}

{{< callout type="warning" >}}
**Cluster Edition 해당 없음**: RDB 테이블은 Standard Edition 전용입니다. Cluster Edition에는 적용되지 않습니다.
{{< /callout >}}

## 증상

- RDB 테이블에 SELECT/INSERT/UPDATE를 실행하면 오류 발생
- 서버 시작은 정상이지만 RDB 쿼리만 실패
- 트레이스 로그에 sidecar 관련 오류 메시지 출력

## 진단

### 1. sidecar 파일 존재 여부 확인

```bash
# sidecar DB 파일 확인
ls -la $MACHBASE_HOME/dbs/__rdbt_*.db
```

파일이 없거나 크기가 0이면 누락 또는 손상된 것입니다.

### 2. 트레이스 로그 확인

```bash
grep -i "rdb\|sidecar\|sqlite\|error" $MACHBASE_HOME/trc/machbase.trc | tail -30
```

### 3. RDB 테이블 목록 확인

복구 후 재생성이 필요한 테이블 목록을 파악합니다.

```sql
-- RDB 테이블 목록 조회 (시스템 테이블 이용)
SELECT name FROM m$sys_tables WHERE type = 8;
```

## 복구 방법

### 방법 1: 백업에서 sidecar 파일 복원

최근 백업이 있는 경우 백업에서 sidecar 파일을 복원합니다.

```bash
# 1. 서버 종료
machadmin -s

# 2. 백업에서 전체 복원 (sidecar 포함)
machadmin -r /backup/machbase_20240101

# 3. 서버 시작
machadmin -u
```

백업에서 복원하면 sidecar 파일도 자동으로 복원됩니다. 단, 백업 시점 이후의 RDB 데이터는 복원되지 않습니다.

### 방법 2: RDB 테이블 재생성

백업이 없거나 백업 복원이 불가능한 경우 RDB 테이블을 재생성합니다. 이 방법은 **기존 RDB 데이터가 손실됩니다.**

**재생성 전에 기존 sidecar 파일을 백업합니다.**

```bash
# 손상된 sidecar 파일 백업 (혹시 복구 가능할 경우를 대비)
mkdir -p /tmp/rdb_backup
cp $MACHBASE_HOME/dbs/__rdbt_*.db /tmp/rdb_backup/
```

애플리케이션의 DDL 스크립트를 이용하거나 직접 CREATE TABLE을 실행하여 RDB 테이블을 재생성합니다.

```sql
-- RDB 테이블 재생성 예시
CREATE RDB TABLE rdb_config (
    config_key   VARCHAR(128) PRIMARY KEY,
    config_value VARCHAR(4096),
    updated_at   DATETIME
);
```

## RDB 테이블 사전 백업 권장

RDB 테이블 구조와 데이터를 주기적으로 별도 백업해 두면 복구 시 활용할 수 있습니다.

```sql
-- RDB 테이블 목록 및 정의 확인
SELECT name FROM m$sys_tables WHERE type = 8;

-- 개별 RDB 테이블 백업
BACKUP TABLE rdb_config INTO DISK = '/backup/rdb_config_20240101';
```

데이터 중요도에 따라 RDB 테이블의 내용을 CSV로 내보내거나 외부 시스템에 복사해 두는 것도 권장합니다.
