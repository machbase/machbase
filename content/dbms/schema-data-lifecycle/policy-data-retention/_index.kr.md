---
type: docs
title: '데이터 보존 정책'
weight: 30
---

Machbase는 시계열 데이터의 자동 삭제 기능인 **Retention Policy**를 제공합니다. 보존 기간과 삭제 주기를 정의한 정책을 생성한 후, 대상 테이블에 적용하면 지정된 주기마다 자동으로 오래된 데이터를 삭제합니다.

## 주요 개념

- **Duration**: 데이터를 보존할 기간. 이 기간을 초과한 데이터는 삭제 대상이 됩니다.
- **Interval**: 보존 기간 점검 주기. 이 주기마다 삭제 작업이 실행됩니다.

## 지원 테이블 타입

Retention Policy는 **TAG와 LOG 테이블에서만** 사용할 수 있습니다.

| 테이블 타입 | Retention Policy 적용 |
|------------|---------------------|
| TAG | O |
| LOG | O |
| RDB | X |
| VOLATILE | X |
| LOOKUP | X |

RDB, VOLATILE, LOOKUP 테이블의 주기적 데이터 삭제는 별도의 애플리케이션 배치 로직으로 구현해야 합니다.

## 워크플로우

```
CREATE RETENTION → ALTER TABLE ADD RETENTION → (자동 삭제 운영) → ALTER TABLE DROP RETENTION → DROP RETENTION
```

## 하위 페이지

- [Retention Policy 상세](./retention-policy/): 생성·적용·해제·삭제 전체 가이드
