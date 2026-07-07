---
type: docs
title: '증분 백업과 AFTER 기준 경로'
weight: 40
---

증분 백업은 이전 백업(전체 백업 또는 이전 증분 백업) 이후에 추가된 데이터만 백업합니다. 전체 백업보다 빠르고 저장 공간을 절약할 수 있습니다.

## 문법

```sql
BACKUP DATABASE AFTER 'previous_backup_path'
  INTO DISK = 'incremental_backup_path';
```

- `previous_backup_path`: 기준이 되는 이전 백업 경로 (전체 백업 또는 이전 증분 백업)
- `incremental_backup_path`: 이번 증분 백업을 저장할 새로운 경로

## 예제

```sql
-- 1단계: 기준 전체 백업 (예: 매주 일요일)
BACKUP DATABASE INTO DISK = '/backup/machbase_base_20240101';

-- 2단계: 증분 백업 (예: 매일)
BACKUP DATABASE AFTER '/backup/machbase_base_20240101'
  INTO DISK = '/backup/machbase_incr_20240102';

-- 3단계: 전날 증분 백업을 기준으로 다시 증분 백업
BACKUP DATABASE AFTER '/backup/machbase_incr_20240102'
  INTO DISK = '/backup/machbase_incr_20240103';
```

## 증분 백업 체인 구성

증분 백업은 체인 형태로 연결됩니다. 복구 시에는 복원하려는 최종 증분 백업 디렉터리를 `machadmin -r`에 지정합니다.

```
[전체 백업]            [증분 1]             [증분 2]             [증분 3]
machbase_base   ──▶  machbase_incr_0102  ──▶  machbase_incr_0103  ──▶  machbase_incr_0104
(1/1)               (1/2 이후 데이터)         (1/3 이후 데이터)         (1/4 이후 데이터)
```

## 증분 백업 복구 절차

증분 백업으로 복구할 때는 `machadmin -r` 명령을 최종 증분 백업 경로에 대해 한 번 실행합니다.

```bash
# 서버 종료
machadmin -s

# 기존 데이터베이스 삭제
machadmin -d

# 복원하려는 최종 증분 백업 지정
machadmin -r /backup/machbase_incr_20240103

# 서버 시작
machadmin -u
```

> `AFTER` 체인이 끊기지 않도록 전체 백업과 각 증분 백업 디렉터리를 함께 보관해야 합니다.

## 증분 백업 자동화 예제

```bash
#!/bin/bash
DATE=$(date +%Y%m%d)
PREV_DATE=$(date -d "yesterday" +%Y%m%d)

BASE_DIR="/backup/machbase_base"
PREV_INCR="/backup/machbase_incr_${PREV_DATE}"
CURR_INCR="/backup/machbase_incr_${DATE}"

# 이전 증분 백업이 있으면 그것을 기준으로, 없으면 전체 백업을 기준으로
if [ -d "${PREV_INCR}" ]; then
    AFTER_PATH="${PREV_INCR}"
else
    AFTER_PATH="${BASE_DIR}"
fi

machsql -u sys -p manager -e \
  "BACKUP DATABASE AFTER '${AFTER_PATH}' INTO DISK = '${CURR_INCR}';"
```

## 주의 사항

- `AFTER` 절에 지정하는 경로는 반드시 존재하는 유효한 백업 디렉터리여야 합니다.
- 현재 빌드에서는 직전 백업 경로를 기준으로 증분 백업을 생성합니다.
- 증분 백업 체인이 길어질수록 복구 시간이 늘어납니다. 주기적으로 새로운 전체 백업을 기준으로 재설정하는 것을 권장합니다.
