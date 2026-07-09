---
type: docs
title: '14.3 권한 관리'
weight: 30
---

권한 관리는 Machbase에서 각 사용자가 어떤 작업을 수행할 수 있는지 제어하는 핵심 보안 기능입니다.

## 권한의 두 가지 종류

Machbase 권한은 적용 범위에 따라 두 가지로 나뉩니다.

| 종류 | 설명 | 예시 |
|---|---|---|
| 데이터베이스 권한 | DB 전체 범위에서 DDL 및 관리 작업 허용 | 테이블 생성, 백업 실행 |
| 테이블 권한 | 특정 테이블에 대한 DML 작업 허용 | 특정 테이블 조회·삽입 |

데이터베이스 권한은 `GRANT ... ON MACHBASEDB TO user` 구문으로 부여하고,  
테이블 권한은 `GRANT ... ON schema.table TO user` 구문으로 부여합니다.

## GRANT / REVOKE 명령어 개요

```sql
-- 데이터베이스 권한 부여
GRANT CREATE ON machbasedb TO app_user;

-- 테이블 권한 부여
GRANT SELECT ON sys.sensor_log TO reader_user;

-- 권한 취소
REVOKE SELECT ON sys.sensor_log FROM reader_user;
```

자세한 문법과 예제는 다음 하위 섹션을 참고하십시오.

- [권한 모델](./privileges/) — 권한 계층 구조와 전체 권한 목록
- [GRANT / REVOKE](./grant-revoke/) — 권한 부여·취소 구문 상세
- [데이터베이스 권한](./database-privileges/) — 데이터베이스 범위 권한 각각의 설명
- [테이블 권한](./privileges-2/) — 특정 테이블 대상 세밀한 권한 제어
- [기본 부여 권한과 제외 권한](./privileges-grant-exclude/) — 신규 사용자의 초기 권한 범위
- [LOOKUP UPDATE/DELETE 내부 target select 권한 모델](./privileges-lookup-update-delete-target-select/) — 계획 중인 권한 동작
- [권한 진단 체크리스트](./checklist-diagnosis-privileges/) — 권한 현황 조회 및 감사 방법
