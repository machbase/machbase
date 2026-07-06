---
type: docs
title: 'Edition 제한'
weight: 130
---

RDB 테이블은 Machbase Standard Edition 전용 기능입니다.

## Edition별 지원 현황

| 기능 | Standard Edition | Cluster Edition |
|------|-----------------|-----------------|
| TAG 테이블 | O | O |
| LOG 테이블 | O | O |
| **RDB 테이블** | **O** | **X** |
| VOLATILE 테이블 | O | O |
| LOOKUP 테이블 | O | O |

## Cluster Edition에서의 대안

Cluster Edition 환경에서 RDB 테이블이 필요한 경우:

1. **LOOKUP 테이블**: 소규모 데이터 + UPDATE 필요 시
2. **외부 RDBMS 연동**: 대규모 관계형 데이터는 별도 RDBMS(PostgreSQL 등)에서 관리하고 Machbase와 조합
3. **LOG 테이블**: UPDATE 불필요한 추가 전용 이력 데이터

## 제약 요약

| 항목 | 상태 |
|------|------|
| Cluster Edition 지원 | X |
| UPDATE | X |
| Append API | X |
| METADATA 절 | X (TAG 전용) |
| 최소 컬럼 수 | 4개 |
| PRIMARY KEY 강제 | X (인덱스로 대체) |

---

**다음 읽을 내용**
- [LOOKUP 테이블 설계](/dbms/data-modeling-table-design/table-types-design-type/design-lookup/)
