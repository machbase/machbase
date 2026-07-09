---
type: docs
title: '14.3.6 권한 진단 체크리스트'
weight: 70
---

권한 현황을 정기적으로 점검하고 불필요한 권한을 제거하는 것이 데이터베이스 보안의 기본입니다.

## 권한 조회 쿼리

### 데이터베이스 권한 확인

```sql
-- 모든 데이터베이스 권한 현황
SELECT * FROM m$sys_privileges;

-- 특정 사용자의 데이터베이스 권한 확인
SELECT * FROM m$sys_privileges WHERE grantee = 'APP_USER';
```

### 테이블 권한 확인

```sql
-- 모든 테이블 권한 현황
SELECT * FROM m$obj_privileges;

-- 특정 테이블의 권한 부여 현황
SELECT * FROM m$obj_privileges WHERE obj_name = 'SENSOR_LOG';

-- 특정 사용자의 테이블 권한 목록
SELECT * FROM m$obj_privileges WHERE grantee = 'APP_USER';
```

### 사용자와 권한 전체 현황

```sql
-- 모든 사용자와 데이터베이스 권한 현황
SELECT u.user_name, p.privilege_type
  FROM m$user u
  LEFT JOIN m$sys_privileges p ON u.user_id = p.grantee_id
 ORDER BY u.user_name, p.privilege_type;

-- 모든 사용자와 테이블 권한 현황
SELECT u.user_name, op.obj_name, op.privilege_type
  FROM m$user u
  LEFT JOIN m$obj_privileges op ON u.user_id = op.grantee_id
 ORDER BY u.user_name, op.obj_name, op.privilege_type;
```

## 진단 체크리스트

### 일상 점검

- [ ] 신규 사용자 생성 후 최소 권한 원칙 적용 여부 확인
- [ ] 애플리케이션 계정에 불필요한 관리 권한(ALTER, BACKUP, MOUNT) 부여 여부 확인
- [ ] 읽기 전용 계정에 INSERT, DELETE, UPDATE 권한이 부여되어 있지 않은지 확인

### 정기 감사 (분기별 권장)

- [ ] 전체 사용자 목록과 권한 현황 검토
- [ ] 퇴직·이직한 직원 계정의 비활성화 또는 삭제 여부 확인
- [ ] 임시로 부여한 권한(테스트, 마이그레이션 등)이 회수되었는지 확인
- [ ] SYS 계정 비밀번호 변경 이력 확인
- [ ] 권한이 과도하게 부여된 계정 식별 및 조정

```sql
-- 분기 감사용: 각 사용자별 보유 권한 요약
SELECT
    u.user_name,
    COUNT(DISTINCT p.privilege_type) AS db_priv_count,
    COUNT(DISTINCT op.obj_name)      AS table_access_count
  FROM m$user u
  LEFT JOIN m$sys_privileges p  ON u.user_id = p.grantee_id
  LEFT JOIN m$obj_privileges op ON u.user_id = op.grantee_id
 GROUP BY u.user_name
 ORDER BY db_priv_count DESC, table_access_count DESC;
```

## 계정 비활성화 처리

퇴직·이직 시 계정을 즉시 처리합니다.

```sql
-- 비밀번호를 알 수 없는 값으로 변경하여 접속 차단
ALTER USER old_employee IDENTIFIED BY '!DISABLED!ACCOUNT!';

-- 테이블 권한 전체 취소
REVOKE ALL ON sys.sensor_log FROM old_employee;

-- 데이터베이스 권한 전체 취소
REVOKE ALL ON machbasedb FROM old_employee;

-- 해당 사용자가 소유한 객체를 다른 사용자에게 이관 후 계정 삭제
-- (소유 테이블이 있는 경우 먼저 DROP TABLE 또는 소유권 이전 필요)
DROP USER old_employee;
```

> **주의**: 사용자가 소유한 테이블이 있으면 `DROP USER`가 실패합니다. 먼저 해당 사용자의 테이블을 삭제하거나 SYS 계정으로 이관한 후 사용자를 삭제하십시오.

## 권장 계정 구성 예시

| 계정 유형 | 필요 권한 | 설명 |
|---|---|---|
| 읽기 전용 | `SELECT ON target_table` | 데이터 조회 전용 |
| 데이터 수집 | `INSERT ON target_table` | 센서·IoT 데이터 적재 |
| 애플리케이션 | `SELECT, INSERT ON target_table` | 일반 CRUD 애플리케이션 |
| 배포 자동화 | `DDL ON machbasedb` | 스키마 변경 자동화 |
| 운영 DBA | `ALL ON machbasedb` | 데이터베이스 전반 관리 |
| 백업 에이전트 | `BACKUP ON machbasedb` | 정기 백업 전용 |

각 계정에는 업무에 필요한 최소한의 권한만 부여하고, 정기적으로 권한 현황을 검토하십시오.
