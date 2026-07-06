---
type: docs
title: '데이터 변경 정책'
weight: 20
---

Machbase는 테이블 타입에 따라 UPDATE, DELETE, TRUNCATE 지원 범위가 명확하게 구분됩니다. 시계열 특성상 대부분의 테이블은 삽입 후 변경을 제한하며, 일부 테이블만 수정·삭제를 허용합니다.

## 테이블 타입별 데이터 변경 지원 범위

| 테이블 타입 | UPDATE | DELETE | TRUNCATE |
|------------|--------|--------|---------|
| TAG | X (계획 중: #3733) | O (BEFORE 조건 필수) | X |
| LOG | X | O (BEFORE 조건 필수) | O |
| RDB | O (WHERE 유무 모두) | O | O |
| VOLATILE | O (by PK) | O | X |
| LOOKUP | O (by PK) | O (by PK) | X |

> TRUNCATE는 LOG와 RDB 테이블에서만 지원됩니다. TAG, VOLATILE, LOOKUP 테이블에 TRUNCATE를 실행하면 오류가 발생합니다.

## 변경이 제한되는 이유

TAG와 LOG 테이블은 시계열 데이터의 **불변성(immutability)** 원칙을 따릅니다. 수집된 센서 데이터나 이벤트 로그는 원칙적으로 사후에 수정하지 않으며, 이를 통해 저장 구조 최적화와 높은 삽입 처리량을 달성합니다. 수정이 필요한 상태 정보·설정 값은 VOLATILE 또는 LOOKUP 테이블에 저장하는 것이 권장됩니다.

## 각 정책 상세

- [UPDATE 정책](./policy-update/): 테이블 타입별 UPDATE 허용 조건과 구문
- [DELETE 정책](./policy-delete/): 테이블 타입별 DELETE 허용 조건
- [TRUNCATE 정책](./policy-truncate/): TRUNCATE 지원 테이블과 동작 차이
- [TAG/KV DELETE 조건](./condition-tag-kv-delete-before/): BEFORE 조건 필수 규칙
