---
type: docs
title: 'FREEZE / UNFREEZE'
weight: 50
---

일관된 스냅샷 백업을 위해 서버의 모든 DML(데이터 변경 작업)을 일시 중단하거나 재개합니다.

## FREEZE

```sql
ALTER SYSTEM FREEZE;
```

서버에 대한 모든 DML 작업을 일시 중단합니다. FREEZE 상태에서는 데이터가 변경되지 않으므로, 데이터 파일을 복사하여 일관된 스냅샷 백업을 만들 수 있습니다.

**FREEZE 상태에서 불가능한 작업**

- `INSERT` / Append 입력
- `DELETE`
- `UPDATE`

**FREEZE 상태에서 가능한 작업**

- `SELECT` 조회
- DDL(`CREATE`, `DROP`, `ALTER TABLE` 등)
- `ALTER SYSTEM` 명령어

> **주의**: FREEZE 상태를 유지하면 데이터 입력이 모두 차단됩니다. 최대한 짧은 시간 동안만 FREEZE 상태를 유지하고, 백업 완료 즉시 UNFREEZE를 실행하십시오.

## UNFREEZE

```sql
ALTER SYSTEM UNFREEZE;
```

FREEZE로 중단된 DML 작업을 재개합니다. UNFREEZE 이후에는 INSERT, DELETE 등 모든 데이터 변경 작업이 다시 허용됩니다.

## 사용 시나리오: 파일 시스템 수준 백업

`BACKUP DATABASE` 명령을 사용하지 않고 데이터 파일을 직접 복사하는 경우, FREEZE/UNFREEZE를 사용하여 일관성을 보장합니다.

```sql
-- 1. DML 중단
ALTER SYSTEM FREEZE;

-- 2. 데이터 파일 복사 (운영체제 명령 또는 스냅샷)
--    $MACHBASE_HOME/dbs/ 디렉터리를 백업 경로로 복사

-- 3. DML 재개
ALTER SYSTEM UNFREEZE;
```

## FREEZE vs BACKUP DATABASE

| 항목 | FREEZE + 파일 복사 | BACKUP DATABASE |
|---|---|---|
| 일관성 보장 | 수동으로 보장 (FREEZE 중 복사) | 자동 보장 |
| DML 차단 | FREEZE 동안 완전 차단 | 내부적으로 처리 |
| 사용 편의성 | 낮음 (직접 파일 관리 필요) | 높음 |
| 권장 상황 | 스토리지 스냅샷과 연동할 때 | 일반적인 데이터베이스 백업 |

일반적인 백업은 [데이터베이스 백업 및 복구](../../backup-restore-mount/)를 참고하십시오.
