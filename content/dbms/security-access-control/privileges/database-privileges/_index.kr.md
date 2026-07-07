---
type: docs
title: '데이터베이스 권한'
weight: 30
---

데이터베이스 권한은 `MACHBASEDB` 전체 범위에 적용되는 권한으로, 주로 DDL(데이터 정의 언어)과 관리 작업을 제어합니다.

## 데이터베이스 권한 목록

| 권한 | 허용하는 작업 | 기본 보유 |
|---|---|---|
| `CREATE` | 테이블, 뷰, 인덱스, 롤업, 테이블스페이스, 리텐션 생성 | 예 |
| `DROP` | 테이블, 뷰, 인덱스, 롤업, 테이블스페이스, 리텐션 삭제 | 예 |
| `ALTER` | 테이블 구조 변경, `ALTER SYSTEM` 실행 | 아니오 |
| `BACKUP` | `BACKUP DATABASE` 실행 | 아니오 |
| `MOUNT` | `MOUNT DATABASE` / `UNMOUNT DATABASE` 실행 | 아니오 |
| `DDL` | CREATE + DROP 묶음 | — |
| `ALL` | 모든 데이터베이스 권한 일괄 부여 | — |

"기본 보유"가 "예"인 권한은 `CREATE USER`로 생성된 사용자가 별도 GRANT 없이 보유합니다.  
나머지 권한은 SYS 계정이 명시적으로 부여해야 합니다.

## 권한이 필요한 주요 작업

다음 작업은 테이블 권한이 아닌 데이터베이스 권한이 필요합니다.

| 작업 | 필요한 권한 |
|---|---|
| `CREATE TABLE` / `DROP TABLE` | CREATE / DROP |
| `CREATE VIEW` / `DROP VIEW` | CREATE / DROP |
| `CREATE INDEX` / `DROP INDEX` | CREATE / DROP |
| `CREATE ROLLUP` / `DROP ROLLUP` | CREATE / DROP |
| `CREATE TABLESPACE` / `DROP TABLESPACE` | CREATE / DROP |
| `CREATE RETENTION` / `DROP RETENTION` | CREATE / DROP |
| `ALTER TABLE` (컬럼 추가/삭제 등) | ALTER |
| `ALTER SYSTEM` | ALTER |
| `BACKUP DATABASE` | BACKUP |
| `MOUNT DATABASE` / `UNMOUNT DATABASE` | MOUNT |

## 부여 예제

```sql
-- deploy_user에게 DDL 권한 부여
GRANT DDL ON machbasedb TO deploy_user;

-- ops_user에게 ALTER 권한 부여
GRANT ALTER ON machbasedb TO ops_user;

-- backup_user에게 BACKUP 권한 부여
GRANT BACKUP ON machbasedb TO backup_user;

-- admin_user에게 모든 데이터베이스 권한 부여
GRANT ALL ON machbasedb TO admin_user;
```

## 하위 섹션

각 권한의 상세 설명과 사용 예제는 다음 페이지를 참고하십시오.

- [SELECT / INSERT / DELETE / UPDATE](./select-insert-delete-update/)
- [CREATE / DROP](./create-drop/)
- [ALTER](./alter/)
- [BACKUP](./backup/)
- [MOUNT](./mount/)
- [DDL / ALL 합성 권한](./privileges-ddl-all/)
