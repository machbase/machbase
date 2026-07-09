---
type: docs
title: '14.3.5 테이블 권한'
weight: 60
---

테이블 권한은 특정 테이블에 대한 DML 작업을 세밀하게 제어하는 권한입니다.  
`GRANT ... ON table TO user` 구문으로 부여하며, 테이블 단위로 개별 관리할 수 있습니다.

## 테이블 권한 종류

| 권한 | 허용하는 작업 | 비고 |
|---|---|---|
| `SELECT` | 해당 테이블 데이터 조회 | 모든 테이블 유형 지원 |
| `INSERT` | 해당 테이블에 행 삽입 | 모든 테이블 유형 지원 |
| `DELETE` | 해당 테이블에서 행 삭제 | 모든 테이블 유형 지원 |
| `UPDATE` | 해당 테이블의 행 수정 | VOLATILE, LOOKUP 전용 |
| `ALL` | SELECT + INSERT + DELETE + UPDATE 일괄 부여 | |

## 테이블 지정 방법

테이블 권한 부여 시 테이블을 지정하는 방법은 세 가지입니다.

| 형식 | 예시 |
|---|---|
| 테이블명만 | `GRANT SELECT ON sensor_log TO user1` |
| 스키마.테이블명 | `GRANT SELECT ON sys.sensor_log TO user1` |
| DB명.스키마명.테이블명 | `GRANT SELECT ON machbasedb.sys.sensor_log TO user1` |

## 권한 부여 예제

```sql
-- 단일 테이블 조회 권한
GRANT SELECT ON sys.sensor_log TO reader_user;

-- 단일 테이블 삽입 권한
GRANT INSERT ON sensor_tag TO writer_user;

-- 여러 DML 권한 동시 부여
GRANT SELECT, INSERT ON sys.sensor_log TO app_user;
GRANT SELECT, INSERT, DELETE ON sys.sensor_log TO manager_user;

-- 테이블의 모든 DML 권한 부여
GRANT ALL ON sys.sensor_log TO admin_user;
```

## 권한 취소 예제

```sql
-- 특정 권한 취소
REVOKE DELETE ON sys.sensor_log FROM manager_user;

-- 모든 테이블 권한 취소
REVOKE ALL ON sys.sensor_log FROM admin_user;
```

## 테이블 권한 조회

```sql
-- 모든 테이블 권한 현황 조회
SELECT * FROM m$obj_privileges;

-- 특정 테이블의 권한 부여 현황
SELECT * FROM m$obj_privileges WHERE obj_name = 'SENSOR_LOG';

-- 특정 사용자의 테이블 권한 목록
SELECT * FROM m$obj_privileges WHERE grantee = 'APP_USER';
```

## 주의 사항

- 테이블 소유자는 별도 GRANT 없이 자신의 테이블에 대한 모든 DML을 실행할 수 있습니다.
- 다른 사용자 소유의 테이블에 접근하려면 반드시 해당 테이블에 대한 권한이 필요합니다.
- LOG, TAG 테이블에 `UPDATE` 권한을 부여하더라도 테이블 유형 제약으로 인해 UPDATE를 실행할 수 없습니다.
- VOLATILE, LOOKUP 테이블의 `DELETE`/`UPDATE`는 기본키 기반 `WHERE` 조건이 필요합니다.
