---
type: docs
title: '권한 모델'
weight: 10
---

## 권한 계층 구조

Machbase의 권한 모델은 다음과 같은 구조를 가집니다.

```
SYS 계정 (슈퍼유저)
  └─ 모든 권한 보유, 별도 GRANT 불필요
  └─ 다른 사용자에게 권한 부여 가능

일반 사용자
  ├─ 데이터베이스 권한 (DB 전체 범위)
  │    SELECT, INSERT, DELETE, UPDATE, CREATE, DROP, ALTER, BACKUP, MOUNT, DDL, ALL
  └─ 테이블 권한 (특정 테이블 범위)
       SELECT, INSERT, DELETE, UPDATE, ALL
```

SYS 계정은 모든 권한을 기본으로 보유하므로 별도로 GRANT를 실행할 필요가 없습니다.  
일반 사용자는 SYS 계정 또는 충분한 권한을 가진 관리자로부터 권한을 부여받아야 합니다.

## 데이터베이스 권한 목록

`MACHBASEDB`를 대상으로 부여하는 DB 전체 범위 권한입니다.

| 권한 | 허용하는 작업 |
|---|---|
| `CREATE` | 테이블, 뷰, 인덱스, 롤업, 테이블스페이스, 리텐션 생성 |
| `DROP` | 테이블, 뷰, 인덱스, 롤업, 테이블스페이스, 리텐션 삭제 |
| `ALTER` | 테이블 구조 변경, `ALTER SYSTEM` 실행 |
| `BACKUP` | `BACKUP DATABASE` 실행 |
| `MOUNT` | `MOUNT DATABASE` / `UNMOUNT DATABASE` 실행 |
| `DDL` | CREATE + DROP 묶음 (두 권한 동시 부여) |
| `ALL` | SELECT, INSERT, DELETE, UPDATE, CREATE, DROP, ALTER, BACKUP, MOUNT 일괄 부여 |

`GRANT ALL ON MACHBASEDB`는 DML 권한 비트도 함께 부여하지만,
`GRANT SELECT ON MACHBASEDB`처럼 DML 권한만 개별로 DB 대상에 부여하는 구문은
지원되지 않습니다. 다른 사용자 소유 테이블에 접근하려면 테이블 대상 GRANT가 필요합니다.

## 테이블 권한 목록

특정 테이블을 대상으로 부여하는 DML 범위 권한입니다.

| 권한 | 허용하는 작업 | 비고 |
|---|---|---|
| `SELECT` | 해당 테이블 조회 | 모든 테이블 유형 지원 |
| `INSERT` | 해당 테이블에 행 삽입 | 모든 테이블 유형 지원 |
| `DELETE` | 해당 테이블에서 행 삭제 | 모든 테이블 유형 지원 |
| `UPDATE` | 해당 테이블의 행 수정 | TAG는 태그/시간 조건 필요. LOG 미지원 |
| `ALL` | SELECT + INSERT + DELETE + UPDATE 일괄 부여 | |

## ALL의 의미

`ALL`은 대상에 따라 의미가 다릅니다.

```sql
-- 데이터베이스 ALL 권한
GRANT ALL ON machbasedb TO admin_user;

-- 테이블 DML 권한 전체 (SELECT, INSERT, DELETE, UPDATE)
GRANT ALL ON sys.sensor_log TO app_user;
```

대상이 `MACHBASEDB`이면 SELECT, INSERT, DELETE, UPDATE, CREATE, DROP, MOUNT,
BACKUP, ALTER 권한 비트를 일괄 부여하고, 특정 테이블이면 해당 테이블의 DML 권한
전체를 의미합니다.

## 신규 사용자의 기본 권한

`CREATE USER`로 생성된 사용자는 다음 권한을 기본으로 가집니다.

| 기본 보유 | 기본 미보유 (명시적 부여 필요) |
|---|---|
| SELECT, INSERT, DELETE, UPDATE, CREATE, DROP | ALTER, BACKUP, MOUNT |

자신이 생성한 객체(테이블, 뷰 등)에 대해서는 소유자로서 모든 작업이 허용됩니다.  
다른 사용자 소유의 객체에 접근하려면 SYS 계정이 명시적으로 GRANT를 실행해야 합니다.

## 권한과 테이블 유형 제약

권한이 있어도 테이블 유형이 지원하지 않는 DML은 실행할 수 없습니다.

- `LOG` 테이블은 `UPDATE`를 지원하지 않습니다.
- `TAG` 테이블의 data UPDATE는 태그 선택 조건과 BASETIME 조건이 필요합니다.
- `VOLATILE`, `LOOKUP` 테이블의 `DELETE`/`UPDATE`는 기본키 기반 `WHERE` 조건이 필요합니다.

권한을 부여한다고 해서 지원하지 않는 DML이 허용되는 것은 아닙니다.
