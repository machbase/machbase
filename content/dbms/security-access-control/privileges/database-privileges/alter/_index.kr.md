---
type: docs
title: '14.3.3.3 ALTER'
weight: 30
---

`ALTER` 권한은 테이블 구조 변경과 시스템 수준의 설정 변경을 허용하는 권한입니다.  
신규 사용자 생성 시 기본으로 부여되지 않으므로 필요할 때 명시적으로 GRANT해야 합니다.

## 허용하는 작업

`ALTER` 권한이 있는 사용자는 다음을 실행할 수 있습니다.

- `ALTER TABLE` — 테이블 구조 변경 (컬럼 추가, 컬럼 삭제, 데이터 타입 변경 등)
- `ALTER SYSTEM` — 시스템 설정 변경 및 관리 명령

## 권한 부여 예제

```sql
-- ops_user에게 ALTER 권한 부여
GRANT ALTER ON machbasedb TO ops_user;

-- ALTER 권한 취소
REVOKE ALTER ON machbasedb FROM ops_user;
```

## ALTER TABLE 사용 예

```sql
-- ops_user 세션에서 컬럼 추가 (ALTER 권한 필요)
ALTER TABLE sensor_log ADD COLUMN location VARCHAR(64);

-- 컬럼 삭제
ALTER TABLE sensor_log DROP COLUMN location;
```

## SYS 전용 작업

다음 작업은 `ALTER` 권한이 있어도 SYS 계정에서만 실행할 수 있습니다.

- `ALTER ROLLUP` — 롤업 정책 변경
- 일부 `ALTER SYSTEM` 하위 명령 중 SYS 전용 항목

운영 환경에서는 `ALTER` 권한을 DBA나 운영 담당자에게만 부여하고, 일반 애플리케이션 계정에는 부여하지 않도록 권장합니다.
