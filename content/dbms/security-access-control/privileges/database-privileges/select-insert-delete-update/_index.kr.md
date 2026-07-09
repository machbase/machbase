---
type: docs
title: '14.3.3.1 SELECT / INSERT / DELETE / UPDATE'
weight: 10
---

`SELECT`, `INSERT`, `DELETE`, `UPDATE`는 데이터 조작 언어(DML) 권한입니다.  
신규 사용자는 이 네 가지 권한을 기본으로 보유합니다.

## 데이터베이스 권한으로서의 DML

Machbase에서는 DML 권한을 데이터베이스 전체 범위(`MACHBASEDB`)로 부여할 수 없습니다.  
DML 권한은 반드시 특정 테이블을 대상으로 부여해야 합니다.

```sql
-- 올바른 방법: 특정 테이블에 SELECT 부여
GRANT SELECT ON sys.sensor_log TO reader_user;

-- 지원하지 않는 방법: MACHBASEDB에 SELECT 부여 (오류 발생)
GRANT SELECT ON machbasedb TO reader_user;
-- [ERR-02186: Invalid database name.]
```

테이블별로 세밀하게 권한을 제어하려면 [테이블 권한](../../privileges-2/)을 참고하십시오.

## 각 DML 권한 설명

### SELECT

데이터를 조회하는 권한입니다. 모든 테이블 유형에서 지원합니다.

```sql
-- 특정 테이블 조회 권한 부여
GRANT SELECT ON sys.sensor_log TO reader_user;

-- 권한 취소
REVOKE SELECT ON sys.sensor_log FROM reader_user;
```

### INSERT

테이블에 새 행을 삽입하는 권한입니다. 모든 테이블 유형에서 지원합니다.

```sql
-- 특정 테이블 삽입 권한 부여
GRANT INSERT ON sys.sensor_log TO writer_user;

-- 권한 취소
REVOKE INSERT ON sys.sensor_log FROM writer_user;
```

### DELETE

테이블에서 행을 삭제하는 권한입니다. 모든 테이블 유형에서 지원합니다.

```sql
-- 특정 테이블 삭제 권한 부여
GRANT DELETE ON sys.sensor_log TO manager_user;

-- 권한 취소
REVOKE DELETE ON sys.sensor_log FROM manager_user;
```

### UPDATE

테이블의 행을 수정하는 권한입니다.

```sql
-- VOLATILE/LOOKUP 테이블에 UPDATE 권한 부여
GRANT UPDATE ON sys.device_config TO ops_user;

-- 권한 취소
REVOKE UPDATE ON sys.device_config FROM ops_user;
```

**UPDATE 권한과 테이블 유형 제약:**

| 테이블 유형 | UPDATE 지원 여부 |
|---|---|
| LOG | 미지원 |
| TAG | 지원 (태그/시간 조건 필요) |
| VOLATILE | 지원 (기본키 기반 WHERE 조건 필요) |
| LOOKUP | 지원 (기본키 기반 WHERE 조건 필요) |

UPDATE 권한을 부여하더라도 LOG 테이블에서는 UPDATE를 실행할 수 없습니다. TAG 테이블의
data UPDATE는 태그 선택 조건과 시간 조건을 만족해야 하며, `name`, `time`, 메타데이터 컬럼은
data UPDATE의 SET 대상이 아닙니다.

## 복합 DML 권한 부여

여러 DML 권한을 한 번에 부여하려면 테이블 권한을 사용합니다.

```sql
-- 조회와 삽입을 함께 허용
GRANT SELECT, INSERT ON sys.sensor_log TO iot_user;

-- 조회, 삽입, 삭제를 함께 허용
GRANT SELECT, INSERT, DELETE ON sys.sensor_log TO app_user;

-- 해당 테이블의 모든 DML 권한 부여
GRANT ALL ON sys.sensor_log TO app_user;
```
