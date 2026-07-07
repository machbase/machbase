---
type: docs
title: '기본 부여 권한과 제외 권한'
weight: 40
---

`CREATE USER`로 사용자를 생성하면 일부 권한이 자동으로 부여되고, 일부는 명시적으로 부여해야 합니다.

## 기본 보유 권한

신규 생성된 사용자가 별도 GRANT 없이 보유하는 권한입니다.

| 권한 | 허용 작업 |
|---|---|
| `SELECT` | 자신이 소유한 테이블 조회 |
| `INSERT` | 자신이 소유한 테이블 삽입 |
| `DELETE` | 자신이 소유한 테이블 삭제 |
| `UPDATE` | 자신이 소유한 테이블 수정 |
| `CREATE` | 테이블, 뷰, 인덱스 등 객체 생성 |
| `DROP` | 자신이 소유한 객체 삭제 |

## 기본 제외 권한 (명시적 부여 필요)

다음 권한은 기본 보유 권한에 포함되지 않습니다.

| 권한 | 부여 구문 |
|---|---|
| `ALTER` | `GRANT ALTER ON machbasedb TO user;` |
| `BACKUP` | `GRANT BACKUP ON machbasedb TO user;` |
| `MOUNT` | `GRANT MOUNT ON machbasedb TO user;` |

```sql
-- 기본 제외 권한 부여 예시
GRANT ALTER ON machbasedb TO ops_user;
GRANT BACKUP ON machbasedb TO backup_user;
GRANT MOUNT ON machbasedb TO mount_user;
```

## 객체 소유권과 권한

사용자가 직접 생성한 객체에 대해서는 해당 사용자가 소유자가 됩니다.  
소유자는 별도 권한 없이 자신의 객체에 대한 모든 DML 및 DROP을 실행할 수 있습니다.

```sql
-- app_user가 생성한 테이블은 app_user가 소유자
-- app_user 세션에서 아래 작업 모두 가능 (별도 GRANT 불필요)
CREATE TABLE my_data (id INTEGER, val DOUBLE);
INSERT INTO my_data VALUES (1, 3.14);
SELECT * FROM my_data;
DROP TABLE my_data;
```

## 다른 사용자 소유 객체 접근

SYS 계정이 생성한 테이블이나 다른 사용자 소유 테이블에 접근하려면 명시적 GRANT가 필요합니다.

```sql
-- SYS 소유의 sensor_log를 app_user가 조회하려면
-- SYS 계정에서 권한 부여
GRANT SELECT ON sys.sensor_log TO app_user;

-- app_user1 소유의 테이블을 app_user2가 접근하려면
GRANT SELECT ON app_user1.shared_table TO app_user2;
```

권한 부여 없이 다른 사용자 소유 테이블에 접근하면 권한 오류가 발생합니다.

## 최소 권한 원칙 적용

실무에서는 업무에 필요한 최소한의 권한만 부여하는 것을 권장합니다.

```sql
-- 읽기 전용 계정: SELECT만 부여
CREATE USER reader_user IDENTIFIED BY 'Reader!Pass1';
-- CREATE, DROP, INSERT, DELETE, UPDATE 기본 권한은 제거하지 않음에 주의
-- 다른 사용자 테이블에 대한 접근은 별도 GRANT로 제어

-- 데이터 수집 전용 계정: INSERT만 필요한 테이블에 부여
CREATE USER collector_user IDENTIFIED BY 'Collect!Pass1';
GRANT INSERT ON sys.sensor_log TO collector_user;
GRANT INSERT ON sys.sensor_tag TO collector_user;
```

신규 사용자의 기본 권한(SELECT, INSERT, DELETE, UPDATE, CREATE, DROP)은 자신의 소유 객체에만 적용됩니다. 다른 사용자 소유 객체에 대한 접근은 항상 명시적 GRANT가 필요합니다.
