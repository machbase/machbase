---
type: docs
title: '17.7 백업과 복구 문제'
weight: 70
toc: true
---
백업 실패, 복원 오류, 마운트 오류의 원인 진단과 해결 방법입니다. 백업·복구 기능의 일반적인 사용법은 [백업, 복원, 마운트](/dbms/operations-configuration-recovery/backup-restore-mount/)를 참고하십시오.

## 이 섹션의 구성

| 페이지 | 내용 |
|--------|------|
| [백업과 복원이 실패할 때](/dbms/troubleshooting/recovery-backup/#failure-backup-restore) | 백업/복원 실패 원인 진단 및 해결 방법 |
| [TRANSACTION 백업·복원·마운트 확인](/dbms/rdb-table-usage/backup-restore-mount/#troubleshooting-backup-rdb) | Standard Edition TRANSACTION 백업과 복원 점검 방법 |
| [마운트가 실패할 때](/dbms/troubleshooting/recovery-backup/#failure-mount) | MOUNT 실패 원인 진단 및 해결 방법 |


<a id="failure-backup-restore"></a>

## 백업과 복원이 실패할 때

백업이나 복원 실패의 원인은 대부분 디렉토리 권한, 디스크 공간, 버전 불일치 중 하나입니다. 오류 메시지와 로그를 단서로 원인을 좁히십시오.

### 백업 실패

#### 주요 실패 원인

| 원인 | 증상 |
|------|------|
| 대상 디렉토리 없음 또는 권한 없음 | "No such file or directory" 또는 "Permission denied" 오류 |
| 디스크 공간 부족 | "No space left on device" 오류, 또는 백업 진행 중 중단 |
| 백업 중 서버 비정상 종료 | 백업 파일이 불완전한 상태로 남음 |

#### 백업 전 확인

```bash
# 백업 디렉토리 존재 여부와 권한 확인
ls -la /backup/

# 예상 백업 크기와 운영 중 증가분을 포함한 디스크 여유 공간 확인
df -h /backup/

# Machbase 데이터 디렉토리 크기 확인 (참고용)
du -sh $MACHBASE_HOME/dbs/
```

백업 대상 디렉토리가 없다면 먼저 생성합니다.

```bash
mkdir -p /backup/machbase_20240101
```

#### 백업 실행

```sql
-- 전체 백업
BACKUP DATABASE INTO DISK = '/backup/machbase_20240101';
```

#### 백업 로그 확인

백업 실패 시 트레이스 로그에서 상세 오류를 확인합니다.

```bash
grep -i "backup\|error" $MACHBASE_HOME/trc/machbase.trc | tail -50
```

---

### 복원 실패

#### 주요 실패 원인

| 원인 | 증상 |
|------|------|
| 백업 파일 손상 | "Invalid backup file" 또는 체크섬 오류 |
| 버전 불일치 | 백업 버전이 현재 설치 버전보다 높을 때 실패 |
| 디스크 공간 부족 | 복원 중 디스크 가득 참 |
| 서버가 실행 중인 상태 | 온라인 상태에서 복원 시도 시 실패 |

#### 복원 전 확인

복원은 반드시 서버가 중지된 **오프라인 상태**에서 실행해야 합니다.

```bash
# 1. 서버 상태 확인
machadmin -e

# 2. 서버 종료
machadmin -s

# 3. 백업 파일 존재 확인
ls -la /backup/machbase_20240101/

# 4. 디스크 공간 확인
df -h $MACHBASE_HOME/dbs/
```

#### 복원 실행

```bash
machadmin -r /backup/machbase_20240101
```

복원 완료 후 서버를 재시작합니다.

```bash
machadmin -u
```

#### 버전 불일치 오류

백업을 생성한 Machbase 버전이 현재 설치된 버전보다 높으면 복원이 실패할 수 있습니다. 이 경우 현재 설치된 Machbase를 백업 버전 이상으로 업그레이드한 후 복원을 재시도합니다.

```bash
# 현재 설치 버전 확인
printf "SELECT * FROM v\\$version;\\n" > version_check.sql
machsql -s 127.0.0.1 -u SYS -p MANAGER -f version_check.sql
```

#### 복원 로그 확인

복원 실패 시 로그에서 상세 원인을 확인합니다.

```bash
grep -i "restore\|error" $MACHBASE_HOME/trc/machbase.trc | tail -50
```

---

### 백업 파일 손상 여부 확인

백업 파일이 손상되었는지 확인하려면 복원 전에 마운트를 시도해 볼 수 있습니다. 마운트가 성공하면 파일이 유효한 것입니다.

```sql
-- 마운트 시도 (서버 실행 중 상태에서 가능)
MOUNT DATABASE '/backup/machbase_20240101' TO backup_check;

-- 조회 성공 여부 확인
SELECT COUNT(*) FROM backup_check.sys.sensor_tag;

-- 확인 후 마운트 해제
UMOUNT DATABASE backup_check;
```

마운트가 실패하면 백업 파일이 손상되었거나 불완전한 것입니다. 이전 백업 파일을 사용하거나 새로 백업을 실행해야 합니다.

<a id="failure-mount"></a>

## 마운트가 실패할 때

`MOUNT DATABASE` 실패의 원인은 백업 경로, 마운트 이름 충돌, 한도 초과, 백업 파일 손상 등입니다.

{{< callout type="warning" >}}
**Cluster Edition 주의**: `MOUNT DATABASE` 명령은 Cluster Edition에서 지원되지 않습니다. Cluster Edition 환경에서 마운트가 필요한 경우 Standard Edition에서 마운트 후 데이터를 추출하는 방법을 검토하십시오.
{{< /callout >}}

### 주요 실패 원인

| 원인 | 오류 메시지 예시 |
|------|----------------|
| 백업 경로 없음 또는 접근 불가 | "No such file or directory" |
| 동일 마운트 이름 이미 존재 | "Mount name already exists" |
| 동시 마운트 한도 초과 | "Too many mounted databases" |
| 백업 파일 손상 | "Invalid database file" |
| 권한 없음 | "Permission denied" |

### 진단

#### 1. 현재 마운트 목록 확인

```sql
-- 현재 마운트된 데이터베이스 목록
SELECT * FROM v$storage_mount_databases;
```

동일한 이름으로 이미 마운트되어 있거나 동시 마운트 수가 한도에 달했는지 확인합니다.

#### 2. 백업 파일 존재 및 접근 확인

```bash
# 백업 디렉토리 존재 및 권한 확인
ls -la /backup/machbase_20240101/

# 백업 파일 내용 확인
ls -la /backup/machbase_20240101/
```

#### 3. 트레이스 로그 확인

```bash
grep -i "mount\|error" $MACHBASE_HOME/trc/machbase.trc | tail -30
```

### 해결 방법

#### 동일 마운트 이름 충돌

이미 같은 이름으로 마운트되어 있다면 먼저 해제하고 재마운트합니다.

```sql
-- 기존 마운트 해제
UMOUNT DATABASE backup_20240101;

-- 재마운트
MOUNT DATABASE '/backup/machbase_20240101' TO backup_20240101;
```

#### 백업 경로 문제

경로에 오타가 없는지 확인하고, 절대 경로를 사용합니다.

```sql
-- 올바른 절대 경로 사용
MOUNT DATABASE '/backup/machbase_20240101' TO backup_20240101;
```

#### 마운트 한도 초과

불필요한 마운트를 해제하여 슬롯을 확보합니다.

```sql
-- 모든 마운트 목록 확인
SELECT name, path FROM v$storage_mount_databases;

-- 불필요한 마운트 해제
UMOUNT DATABASE old_backup_name;

-- 이후 마운트 재시도
MOUNT DATABASE '/backup/machbase_20240101' TO backup_20240101;
```

#### 권한 문제

Machbase 프로세스를 실행하는 OS 사용자가 백업 디렉토리에 대한 읽기 권한을 가지고 있어야 합니다.

```bash
# 백업 디렉토리 권한 확인
ls -la /backup/

# 필요 시 권한 부여 (백업 소유자에 맞게 조정)
chmod -R 755 /backup/machbase_20240101/
```

### 마운트 후 데이터 조회 확인

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
UMOUNT DATABASE backup_20240101;
```

마운트와 관련된 상세 동작(읽기 전용 특성, 동시 마운트 수 제한 등)은 [마운트 DB 동작 특성](/dbms/operations-configuration-recovery/backup-restore-mount/#mounted-db-read-only-refcount-active-same-name)을 참고하십시오.
