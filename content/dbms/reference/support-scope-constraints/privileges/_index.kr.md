---
type: docs
title: '권한별 기능 지원표'
weight: 70
---

Machbase 권한은 적용 범위에 따라 **데이터베이스 권한**과 **테이블 권한** 두 가지로 나뉩니다.

## 데이터베이스 권한

데이터베이스 권한은 `MACHBASEDB` 전체 범위에 적용됩니다.

| 권한 | 허용하는 작업 | 기본 보유 |
|------|-------------|:--------:|
| `CREATE` | 테이블, 뷰, 인덱스, 롤업, 테이블스페이스, 리텐션 생성 | O |
| `DROP` | 테이블, 뷰, 인덱스, 롤업, 테이블스페이스, 리텐션 삭제 | O |
| `ALTER` | 테이블 구조 변경, `ALTER SYSTEM` 실행 | X |
| `BACKUP` | `BACKUP DATABASE` 실행 | X |
| `MOUNT` | `MOUNT DATABASE` / `UNMOUNT DATABASE` 실행 | X |
| `DDL` | CREATE + DROP 묶음 (합성 권한) | — |
| `ALL` | 모든 데이터베이스 권한 일괄 부여 | — |

> "기본 보유 O": `CREATE USER`로 생성된 사용자가 별도 GRANT 없이 보유하는 권한

## 테이블 권한

테이블 권한은 특정 테이블에 대한 DML 작업을 제어합니다.

| 권한 | 허용하는 작업 |
|------|-------------|
| `SELECT` | 특정 테이블 SELECT 조회 |
| `INSERT` | 특정 테이블 INSERT |
| `DELETE` | 특정 테이블 DELETE |
| `UPDATE` | 특정 테이블 UPDATE |

## GRANT / REVOKE 문법

```sql
-- 데이터베이스 권한 부여
GRANT CREATE ON machbasedb TO app_user;
GRANT BACKUP ON machbasedb TO backup_user;
GRANT ALL ON machbasedb TO admin_user;

-- 테이블 권한 부여
GRANT SELECT ON sys.sensor_data TO reader_user;
GRANT INSERT ON sys.sensor_data TO writer_user;

-- 권한 취소
REVOKE SELECT ON sys.sensor_data FROM reader_user;
REVOKE BACKUP ON machbasedb FROM backup_user;
```

## 권한이 필요한 주요 작업

| 작업 | 필요 권한 종류 | 필요 권한 |
|------|-------------|---------|
| `CREATE TABLE` | 데이터베이스 | CREATE |
| `DROP TABLE` | 데이터베이스 | DROP |
| `ALTER TABLE` | 데이터베이스 | ALTER |
| `BACKUP DATABASE` | 데이터베이스 | BACKUP |
| `MOUNT DATABASE` | 데이터베이스 | MOUNT |
| 테이블 SELECT | 테이블 | SELECT |
| 테이블 INSERT | 테이블 | INSERT |
| 테이블 UPDATE | 테이블 | UPDATE |
| 테이블 DELETE | 테이블 | DELETE |

## 권한 현황 조회

```sql
-- 사용자 목록
SELECT user_name, user_id FROM m$sys_users;

-- 데이터베이스 권한 조회
SELECT * FROM m$sys_grant_databases WHERE grantee = 'APP_USER';

-- 테이블 권한 조회
SELECT * FROM m$sys_grant_tables WHERE grantee = 'APP_USER';
```

## 상세 레퍼런스

권한 모델 전체 설명과 예제는 [권한 관리](/dbms/security-access-control/privileges/) 섹션을 참고하세요.
