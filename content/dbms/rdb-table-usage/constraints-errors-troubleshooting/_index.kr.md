---
title: '8.8 제약, 오류, 문제 해결'
weight: 80
toc: true
---

RDB 테이블의 Edition 제한과 기능 제약 사항을 정리한다.


<a id="limitations-rdb-edition"></a>

## Edition 제한

RDB 테이블은 Standard Edition 전용 기능이다.

### Edition별 지원 현황

| 기능 | Standard Edition | Cluster Edition |
|------|-----------------|-----------------|
| TAG 테이블 | O | O |
| LOG 테이블 | O | O |
| **RDB 테이블** | **O** | **X** |
| VOLATILE 테이블 | O | O |
| LOOKUP 테이블 | O | O |

### Cluster Edition에서의 대안

Cluster Edition 환경에서 RDB 테이블과 유사한 기능이 필요한 경우 다음을 고려한다.

1. **LOOKUP 테이블**: 소규모 데이터 + PRIMARY KEY 기반 UPDATE/DELETE 시
2. **LOG 테이블**: UPDATE 불필요한 추가 전용 이력 데이터
3. **외부 RDBMS 연동**: 대규모 관계형 데이터는 별도 RDBMS(PostgreSQL 등)에서 관리

### 기능 요약

| 항목 | 상태 |
|------|------|
| Cluster Edition 지원 | X |
| SELECT | O |
| INSERT | O |
| UPDATE (WHERE 포함) | O |
| UPDATE (WHERE 없음, 전체 행) | O |
| DELETE | O |
| Append API | O (트랜잭션 기반) |
| PRIMARY KEY 인덱스 | O (BTREE) |
| 보조 인덱스 | O |
| METADATA 절 | X (TAG 전용) |
| 최소 컬럼 수 | 1개 |

---

**다음 읽을 내용**
- [LOOKUP 테이블 설계](/dbms/lookup-table-usage/)
