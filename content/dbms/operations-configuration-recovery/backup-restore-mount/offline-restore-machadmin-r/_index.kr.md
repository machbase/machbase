---
type: docs
title: '13.6.7 Offline restore with machadmin -r'
weight: 70
---

오프라인 복원은 서버를 완전히 중단한 상태에서 백업 데이터를 현재 데이터베이스로 교체하는 작업입니다. `machadmin -r` 명령을 사용합니다.

## 온라인 마운트와의 차이

| 항목 | Offline Restore (`machadmin -r`) | Online Mount (`MOUNT DATABASE`) |
|------|:---------------------------------:|:--------------------------------:|
| 서버 상태 | 중단 필요 | 운영 중 가능 |
| 현재 데이터 | 교체됨 (덮어씀) | 유지됨 |
| 결과 | 현재 DB = 백업 시점 상태 | 백업 DB 읽기 전용 접근 |
| 용도 | 재해 복구, 완전 롤백 | 과거 데이터 조회, 선택적 복구 |

## 복원 절차

```bash
# 1. (권장) 현재 데이터 백업 - 복원 후 현재 데이터는 사라짐
cat > /tmp/backup_before_restore.sql <<'SQL'
BACKUP DATABASE INTO DISK = '/backup/machbase_before_restore';
SQL
machsql -u sys -p manager -s 127.0.0.1 -f /tmp/backup_before_restore.sql

# 2. 서버 종료
machadmin -s

# 3. 기존 데이터베이스 삭제
machadmin -d

# 4. 백업 데이터로 복원
machadmin -r /backup/machbase_20240101

# 5. 서버 시작
machadmin -u
```

> 복원을 실행하면 현재 데이터베이스의 내용이 백업 시점으로 완전히 교체됩니다. 복원 전에 반드시 현재 데이터를 백업하거나 불필요한 데이터임을 확인하세요.

## 증분 백업 복원

증분 백업으로 복원할 때는 복원하려는 최종 증분 백업 디렉터리를 한 번 지정합니다. 증분 백업 디렉터리는 체인 정보를 포함하므로 전체 백업과 각 증분 백업을 `machadmin -r`로 반복 적용하지 않습니다.

```bash
# 서버 종료
machadmin -s

# 기존 데이터베이스 삭제
machadmin -d

# 복원하려는 최종 증분 백업 경로 지정
machadmin -r /backup/machbase_incr_20240103

# 서버 시작
machadmin -u
```

## machadmin 주요 옵션

| 옵션 | 설명 |
|------|------|
| `-s` (`--shutdown`) | 서버 정상 종료 |
| `-k` (`--kill`) | 서버 강제 종료 |
| `-u` (`--startup`) | 서버 시작 |
| `-d` (`--destroydb`) | 현재 데이터베이스 삭제 |
| `-r path` (`--restore`) | 지정한 백업 경로로 복원 |

## 복원 실패 시 확인 사항

복원이 실패하는 주요 원인과 해결 방법입니다.

| 원인 | 해결 방법 |
|------|-----------|
| 서버가 실행 중인 상태 | `machadmin -s`로 서버를 완전히 종료한 뒤 재시도 |
| 백업 경로가 존재하지 않음 | 경로가 정확한지 확인 |
| 백업 버전 불일치 | 동일한 메이저 버전 간에만 복원 가능 |
| 디스크 공간 부족 | `$MACHBASE_HOME/dbs` 경로의 여유 공간 확인 |

## 주의 사항

- `machadmin -r` 명령은 데이터베이스가 없는 상태에서 실행합니다.
- 복원 전 서버를 종료하고 현재 데이터베이스를 `machadmin -d`로 삭제해야 합니다.
- TAG 테이블은 기간 백업 복원이 지원되지 않습니다. 전체 백업 또는 증분 백업으로 복원하세요.
