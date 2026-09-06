---
title: '7.8 제약, 오류, 문제 해결'
weight: 80
toc: true
---

LOG 테이블의 제약 사항과 운영 시 주의할 점을 정리합니다.


<a id="limitations-log"></a>

## 제약 및 주의사항

<a id="지원하지-않는-기능"></a>

### 기능 지원 범위

| 기능 | 상태 | 대안 |
|------|------|------|
| UPDATE | 미지원 | — |
| 일반 조건 DELETE | 미지원 | `BEFORE`/`OLDEST`/`EXCEPT` DELETE |
| PRIMARY KEY | 미지원 | — |
| UNIQUE 제약 | 미지원 | — |
| 일반 인덱스 생성 | 제한적 지원 | BITMAP/KEYWORD 인덱스 활용 |

### 주의사항

- **시간 의미 구분**: `_arrival_time`을 생략하면 입력 시점의 서버 시각을 사용합니다.
  시각을 명시하는 입력 경로와 실제 이벤트 시각의 설계는
  [_arrival_time 시간 모델](../arrival-time-model/)을 참고하십시오.
- **데이터 보정 불가**: 잘못 입력된 레코드는 수정할 수 없습니다.
- **삭제 범위 제한**: 임의 조건으로 행을 삭제하는 것은 불가능합니다. 보존/정리 목적의 `BEFORE`, `OLDEST`, `EXCEPT` DELETE를 사용합니다.
- **용량 증가**: 삭제나 보존 정책 없이 계속 입력하면 디스크 사용량이 증가합니다.
  데이터 보관 기간과 정리 주기를 함께 설정합니다.
- **DDL 확인 필요**: LOG 컬럼의 ADD, DROP, RENAME과 지원되는 `MODIFY COLUMN` 범위는
  [생성, 변경, 삭제](../create-alter-drop/)를 정본으로 사용합니다. 인덱스가 참조하는 컬럼과
  허용되지 않는 타입·길이 변경은 거부될 수 있습니다.

### 파티션 및 데이터 보존

데이터 보존 기간 관리는 운영 구성에서 설정합니다. 자세한 내용은 [운영 및 구성](/dbms/operations-configuration-recovery/)을 참고합니다.

---

**다음 읽을 내용**
- [TAG 테이블 설계](/dbms/tag-table-usage/)
