---
type: docs
title: '13.6.2 전체 백업'
weight: 20
---

전체 백업은 현재 시점까지의 모든 데이터베이스 데이터를 지정한 경로에 저장합니다. 서버를 중단하지 않고 실행할 수 있는 온라인 백업입니다.

## 문법

```sql
BACKUP DATABASE INTO DISK = 'backup_path';
```

- `backup_path`: 백업 데이터를 저장할 디렉터리 경로
  - 절대 경로: `/`로 시작하는 전체 경로
  - 상대 경로: `$MACHBASE_HOME/dbs` 기준으로 생성

## 예제

```sql
-- 절대 경로로 전체 백업
BACKUP DATABASE INTO DISK = '/backup/machbase_20240101';

-- 상대 경로 (MACHBASE_HOME/dbs/backup_20240101 에 생성됨)
BACKUP DATABASE INTO DISK = 'backup_20240101';
```

## 동작 방식

- 백업 명령 실행 시 지정한 디렉터리가 자동으로 생성됩니다. 디렉터리가 이미 존재하면 오류가 발생하므로 날짜 등을 포함한 고유한 이름을 사용하세요.
- 백업 실행 중에도 데이터 입력, 조회 등 서버 운영이 계속됩니다.
- 백업이 완료될 때까지 백업 명령은 블로킹 상태로 유지됩니다. 장시간 소요될 수 있으므로 별도 세션에서 실행하거나 쉘 스크립트로 자동화하는 것을 권장합니다.

## 백업 디렉터리 구조

백업이 완료되면 지정한 경로에 다음과 같은 구조의 파일들이 생성됩니다.

```
/backup/machbase_20240101/
├── backup.dat
├── backup.trc
├── meta.dbs-0
├── meta.dbs-1
├── ...
└── rdb/                  # RDB 테이블이 포함된 경우
    └── __rdbt_<table_id>.db
```

## 백업 완료 후 검증

백업 완료 후에는 해당 경로를 마운트하여 데이터가 정상적으로 백업되었는지 확인할 수 있습니다.

```sql
-- 백업된 DB를 마운트
MOUNT DATABASE '/backup/machbase_20240101' TO verify_db;

-- 주요 테이블의 레코드 수 확인
SELECT COUNT(*) FROM verify_db.sys.sensor_log;

-- 마운트 해제
UNMOUNT DATABASE verify_db;
```

## 자동화 예제 (쉘 스크립트)

```bash
#!/bin/bash
DATE=$(date +%Y%m%d)
BACKUP_PATH="/backup/machbase_${DATE}"

machsql -u sys -p manager -e "BACKUP DATABASE INTO DISK = '${BACKUP_PATH}';"

if [ $? -eq 0 ]; then
    echo "백업 완료: ${BACKUP_PATH}"
else
    echo "백업 실패" >&2
    exit 1
fi
```

## 주의 사항

- 백업 중 서버에 부하가 증가할 수 있습니다. 트래픽이 적은 시간대에 실행하는 것을 권장합니다.
- 백업 경로에 충분한 디스크 여유 공간이 있는지 사전에 확인하세요.
- 백업 파일은 원본 서버와 다른 물리 디스크 또는 원격 스토리지에 보관하는 것이 안전합니다.
