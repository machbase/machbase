---
type: docs
title: '14.3.3.2 CREATE / DROP'
weight: 20
---

`CREATE` 권한과 `DROP` 권한은 데이터베이스 객체(테이블, 뷰, 인덱스 등)를 생성하고 삭제하는 권한입니다.  
`CREATE USER`로 생성된 사용자는 이 두 권한을 기본으로 보유합니다.

## CREATE 권한

`CREATE` 권한이 있는 사용자는 다음 객체를 생성할 수 있습니다.

- 테이블 (`CREATE TABLE`)
- 뷰 (`CREATE VIEW`)
- 인덱스 (`CREATE INDEX`)
- 롤업 (`CREATE ROLLUP`)
- 테이블스페이스 (`CREATE TABLESPACE`)
- 리텐션 (`CREATE RETENTION`)

```sql
-- app_user에게 CREATE 권한 부여
GRANT CREATE ON machbasedb TO app_user;

-- CREATE 권한 취소
REVOKE CREATE ON machbasedb FROM app_user;
```

## DROP 권한

`DROP` 권한이 있는 사용자는 다음 객체를 삭제할 수 있습니다.

- 테이블 (`DROP TABLE`)
- 뷰 (`DROP VIEW`)
- 인덱스 (`DROP INDEX`)
- 롤업 (`DROP ROLLUP`)
- 테이블스페이스 (`DROP TABLESPACE`)
- 리텐션 (`DROP RETENTION`)

```sql
-- app_user에게 DROP 권한 부여
GRANT DROP ON machbasedb TO app_user;

-- DROP 권한 취소
REVOKE DROP ON machbasedb FROM app_user;
```

## 소유자의 DROP 권한

자신이 생성한 객체는 별도의 `DROP` 권한 없이도 삭제할 수 있습니다.  
단, 다른 사용자가 소유한 객체를 삭제하려면 반드시 `DROP` 권한이 필요합니다.

```sql
-- app_user가 자신의 테이블을 삭제하는 경우 (DROP 권한 불필요)
-- app_user 세션에서 실행
DROP TABLE my_table;

-- ops_user가 다른 사용자 소유 테이블을 삭제하려면 DROP 권한 필요
-- SYS 계정에서 권한 부여
GRANT DROP ON machbasedb TO ops_user;
```

## CREATE + DROP 동시 부여

두 권한을 함께 부여하려면 `DDL` 권한을 사용합니다.

```sql
-- CREATE + DROP을 한 번에 부여
GRANT DDL ON machbasedb TO deploy_user;

-- 개별 부여와 동일한 효과
GRANT CREATE ON machbasedb TO deploy_user;
GRANT DROP ON machbasedb TO deploy_user;
```

`DDL` 합성 권한에 대한 자세한 내용은 [DDL / ALL 합성 권한](../privileges-ddl-all/)을 참고하십시오.
