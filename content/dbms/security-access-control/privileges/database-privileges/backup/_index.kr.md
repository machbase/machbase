---
type: docs
title: 'BACKUP'
weight: 40
---

`BACKUP` 권한은 `BACKUP DATABASE` 명령을 실행하는 권한입니다.  
신규 사용자 생성 시 기본으로 부여되지 않으므로 필요할 때 명시적으로 GRANT해야 합니다.

## 허용하는 작업

`BACKUP` 권한이 있는 사용자는 다음 명령을 실행할 수 있습니다.

- `BACKUP DATABASE` — 데이터베이스 전체 또는 증분 백업

SYS 계정은 별도 권한 없이 백업을 실행할 수 있습니다.

## 권한 부여 예제

```sql
-- backup_user에게 BACKUP 권한 부여
GRANT BACKUP ON machbasedb TO backup_user;

-- BACKUP 권한 취소
REVOKE BACKUP ON machbasedb FROM backup_user;
```

## BACKUP DATABASE 실행 예

```sql
-- backup_user 세션에서 실행
BACKUP DATABASE INTO DISK = '/backup/machbase_backup';

-- 증분 백업
BACKUP DATABASE LEVEL 1 INTO DISK = '/backup/machbase_inc_backup';
```

## 권한 없을 때의 오류

`BACKUP` 권한이 없는 사용자가 `BACKUP DATABASE`를 실행하면 권한 오류가 발생합니다.

```sql
-- 권한 없는 사용자가 실행할 경우
BACKUP DATABASE INTO DISK = '/backup/test';
-- [ERR-02xxx: Not enough privilege to execute BACKUP DATABASE.]
```

## 운영 지침

- 백업 전용 계정을 별도로 생성하고 `BACKUP` 권한만 부여하는 것을 권장합니다.
- 백업 계정은 필요한 파일 시스템 경로에 대한 OS 수준 쓰기 권한도 함께 필요합니다.
- 정기 백업 스크립트는 전용 백업 계정으로 실행하여 SYS 계정 자격증명 노출을 최소화합니다.
