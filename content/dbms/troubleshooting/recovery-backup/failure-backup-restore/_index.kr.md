---
type: docs
title: '백업과 복원이 실패할 때'
weight: 10
---

백업 또는 복원이 실패하는 경우 대부분 디렉토리 권한, 디스크 공간, 버전 불일치 중 하나가 원인입니다. 오류 메시지와 로그를 단서로 원인을 좁혀 나가십시오.

## 백업 실패

### 주요 실패 원인

| 원인 | 증상 |
|------|------|
| 대상 디렉토리 없음 또는 권한 없음 | "No such file or directory" 또는 "Permission denied" 오류 |
| 디스크 공간 부족 | "No space left on device" 오류, 또는 백업 진행 중 중단 |
| 백업 중 서버 비정상 종료 | 백업 파일이 불완전한 상태로 남음 |

### 백업 전 확인

```bash
# 백업 디렉토리 존재 여부와 권한 확인
ls -la /backup/

# 디스크 여유 공간 확인 (현재 데이터 크기의 1.5배 이상 권장)
df -h /backup/

# Machbase 데이터 디렉토리 크기 확인 (참고용)
du -sh $MACHBASE_HOME/dbs/
```

백업 대상 디렉토리가 없다면 먼저 생성합니다.

```bash
mkdir -p /backup/machbase_20240101
```

### 백업 실행

```sql
-- 전체 백업
BACKUP DATABASE INTO DISK = '/backup/machbase_20240101';
```

### 백업 로그 확인

백업 실패 시 트레이스 로그에서 상세 오류를 확인합니다.

```bash
grep -i "backup\|error" $MACHBASE_HOME/trc/machbase.trc | tail -50
```

---

## 복원 실패

### 주요 실패 원인

| 원인 | 증상 |
|------|------|
| 백업 파일 손상 | "Invalid backup file" 또는 체크섬 오류 |
| 버전 불일치 | 백업 버전이 현재 설치 버전보다 높을 때 실패 |
| 디스크 공간 부족 | 복원 중 디스크 가득 참 |
| 서버가 실행 중인 상태 | 온라인 상태에서 복원 시도 시 실패 |

### 복원 전 확인

복원은 반드시 서버가 중지된 **오프라인 상태**에서 실행해야 합니다.

```bash
# 1. 서버 상태 확인
machadmin -c

# 2. 서버 종료
machadmin -s

# 3. 백업 파일 존재 확인
ls -la /backup/machbase_20240101/

# 4. 디스크 공간 확인
df -h $MACHBASE_HOME/dbs/
```

### 복원 실행

```bash
machadmin -r /backup/machbase_20240101
```

복원 완료 후 서버를 재시작합니다.

```bash
machadmin -u
```

### 버전 불일치 오류

백업을 생성한 Machbase 버전이 현재 설치된 버전보다 높으면 복원이 실패할 수 있습니다. 이 경우 현재 설치된 Machbase를 백업 버전 이상으로 업그레이드한 후 복원을 재시도합니다.

```bash
# 현재 설치 버전 확인
machadmin --version
```

### 복원 로그 확인

복원 실패 시 로그에서 상세 원인을 확인합니다.

```bash
grep -i "restore\|error" $MACHBASE_HOME/trc/machbase.trc | tail -50
```

---

## 백업 파일 손상 여부 확인

백업 파일이 손상되었는지 확인하려면 복원 전에 마운트를 시도해 볼 수 있습니다. 마운트가 성공하면 파일이 유효한 것입니다.

```sql
-- 마운트 시도 (서버 실행 중 상태에서 가능)
MOUNT DATABASE '/backup/machbase_20240101' TO backup_check;

-- 조회 성공 여부 확인
SELECT COUNT(*) FROM backup_check.sys.sensor_tag;

-- 확인 후 마운트 해제
UNMOUNT DATABASE backup_check;
```

마운트가 실패하면 백업 파일이 손상되었거나 불완전한 것입니다. 이전 백업 파일을 사용하거나 새로 백업을 실행해야 합니다.
