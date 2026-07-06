---
type: docs
title: '제약 및 주의사항'
weight: 60
---

## 지원하지 않는 기능

| 기능 | 상태 | 대안 |
|------|------|------|
| UPDATE | 미지원 | — |
| DELETE | 미지원 | — |
| PRIMARY KEY | 미지원 | — |
| UNIQUE 제약 | 미지원 | — |
| 인덱스 생성 | 미지원 | `_arrival_time` 활용 |
| ALTER TABLE (컬럼 삭제/변경) | 미지원 | 테이블 재생성 |

## 주의사항

- **역삽입 불가**: `_arrival_time`은 서버 수신 순서이므로, 과거 데이터를 소급 입력해도 `_arrival_time`은 입력 시점으로 기록됩니다.
- **데이터 보정 불가**: 잘못 입력된 레코드는 수정할 수 없습니다.
- **무한 증가**: 파티션 정책 없이 사용하면 디스크가 계속 증가합니다. 보존 기간 정책을 설정하십시오.
- **컬럼 타입 변경 불가**: `ALTER TABLE ... MODIFY COLUMN`은 지원하지 않습니다.

## 파티션 및 데이터 보존

데이터 보존 기간 관리는 운영 구성에서 설정합니다. 자세한 내용은 [운영 및 구성](/dbms/operations-configuration-recovery/)을 참고하십시오.

---

**다음 읽을 내용**
- [TAG 테이블 설계](/dbms/data-modeling-table-design/table-types-design-type/design-tag/)
