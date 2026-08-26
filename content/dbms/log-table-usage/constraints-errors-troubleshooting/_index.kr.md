---
title: '7.8 제약, 오류, 문제 해결'
weight: 80
toc: true
---

LOG 테이블의 제약 사항과 운영 시 주의할 점을 정리합니다.


<a id="limitations-log"></a>

## 제약 및 주의사항

### 지원하지 않는 기능

| 기능 | 상태 | 대안 |
|------|------|------|
| UPDATE | 미지원 | — |
| 일반 조건 DELETE | 미지원 | `BEFORE`/`OLDEST`/`EXCEPT` DELETE |
| PRIMARY KEY | 미지원 | — |
| UNIQUE 제약 | 미지원 | — |
| 일반 인덱스 생성 | 제한적 지원 | BITMAP/KEYWORD 인덱스 활용 |

### 주의사항

- **역삽입 불가**: `_arrival_time`은 서버 수신 순서이므로, 과거 데이터를 소급 입력해도 `_arrival_time`은 입력 시점으로 기록됩니다.
- **데이터 보정 불가**: 잘못 입력된 레코드는 수정할 수 없습니다.
- **삭제 범위 제한**: 임의 조건으로 행을 삭제하는 것은 불가능합니다. 보존/정리 목적의 `BEFORE`, `OLDEST`, `EXCEPT` DELETE를 사용합니다.
- **무한 증가**: 파티션 정책 없이 사용하면 디스크가 계속 증가합니다. 보존 기간 정책을 설정해야 합니다.
- **DDL 확인 필요**: LOG 컬럼의 ADD, DROP, RENAME과 지원되는 `MODIFY COLUMN` 범위는
  [생성, 변경, 삭제](../create-alter-drop/)를 정본으로 사용합니다. 인덱스가 참조하는 컬럼과
  허용되지 않는 타입·길이 변경은 거부될 수 있습니다.

### 파티션 및 데이터 보존

데이터 보존 기간 관리는 운영 구성에서 설정합니다. 자세한 내용은 [운영 및 구성](/dbms/operations-configuration-recovery/)을 참고합니다.

---

**다음 읽을 내용**
- [TAG 테이블 설계](/dbms/tag-table-usage/)
