---
type: docs
title: '마운트가 실패할 때'
weight: 30
---

`MOUNT DATABASE` 명령이 실패하는 경우 백업 경로, 마운트 이름 충돌, 한도 초과, 백업 파일 손상 등이 원인일 수 있습니다.

{{< callout type="warning" >}}
**Cluster Edition 주의**: `MOUNT DATABASE` 명령은 Cluster Edition에서 지원되지 않습니다. Cluster Edition 환경에서 마운트가 필요한 경우 Standard Edition에서 마운트 후 데이터를 추출하는 방법을 검토하십시오.
{{< /callout >}}

## 주요 실패 원인

| 원인 | 오류 메시지 예시 |
|------|----------------|
| 백업 경로 없음 또는 접근 불가 | "No such file or directory" |
| 동일 마운트 이름 이미 존재 | "Mount name already exists" |
| 동시 마운트 한도 초과 | "Too many mounted databases" |
| 백업 파일 손상 | "Invalid database file" |
| 권한 없음 | "Permission denied" |

## 진단

### 1. 현재 마운트 목록 확인

```sql
-- 현재 마운트된 데이터베이스 목록
SELECT * FROM v$mount_databases;
```

동일한 이름으로 이미 마운트되어 있거나 동시 마운트 수가 한도에 달했는지 확인합니다.

### 2. 백업 파일 존재 및 접근 확인

```bash
# 백업 디렉토리 존재 및 권한 확인
ls -la /backup/machbase_20240101/

# 백업 파일 내용 확인
ls -la /backup/machbase_20240101/
```

### 3. 트레이스 로그 확인

```bash
grep -i "mount\|error" $MACHBASE_HOME/trc/machbase.trc | tail -30
```

## 해결 방법

### 동일 마운트 이름 충돌

이미 같은 이름으로 마운트되어 있다면 먼저 해제하고 재마운트합니다.

```sql
-- 기존 마운트 해제
UNMOUNT DATABASE backup_20240101;

-- 재마운트
MOUNT DATABASE '/backup/machbase_20240101' TO backup_20240101;
```

### 백업 경로 문제

경로에 오타가 없는지 확인하고, 절대 경로를 사용합니다.

```sql
-- 올바른 절대 경로 사용
MOUNT DATABASE '/backup/machbase_20240101' TO backup_20240101;
```

### 마운트 한도 초과

불필요한 마운트를 해제하여 슬롯을 확보합니다.

```sql
-- 모든 마운트 목록 확인
SELECT name, path FROM v$mount_databases;

-- 불필요한 마운트 해제
UNMOUNT DATABASE old_backup_name;

-- 이후 마운트 재시도
MOUNT DATABASE '/backup/machbase_20240101' TO backup_20240101;
```

### 권한 문제

Machbase 프로세스를 실행하는 OS 사용자가 백업 디렉토리에 대한 읽기 권한을 가지고 있어야 합니다.

```bash
# 백업 디렉토리 권한 확인
ls -la /backup/

# 필요 시 권한 부여 (백업 소유자에 맞게 조정)
chmod -R 755 /backup/machbase_20240101/
```

## 마운트 후 데이터 조회 확인

마운트가 성공하면 해당 마운트 이름으로 데이터를 조회할 수 있습니다.

```sql
-- 마운트된 DB의 테이블 조회
SELECT * FROM backup_20240101.sys.sensor_tag
WHERE name = 'sensor-01'
  AND time >= TO_DATE('2024-01-01')
  AND time <  TO_DATE('2024-01-02')
LIMIT 10;
```

조회가 완료된 후 마운트를 해제합니다.

```sql
UNMOUNT DATABASE backup_20240101;
```

마운트와 관련된 상세 동작(읽기 전용 특성, 동시 마운트 수 제한 등)은 [마운트 DB 동작 특성](../../../operations-configuration-recovery/backup-restore-mount/mounted-db-read-only-refcount-active-same-name/)을 참고하십시오.
