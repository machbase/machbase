---
type: docs
title: 'RDB vs LOOKUP 비교'
weight: 40
---

RDB 테이블과 LOOKUP 테이블은 모두 관계형 데이터를 저장하지만, 사용 목적과 기능에 차이가 있습니다.

## 비교표

| 항목 | RDB 테이블 | LOOKUP 테이블 |
|------|-----------|--------------|
| DDL | `CREATE RDB TABLE` | `CREATE LOOKUP TABLE` |
| PRIMARY KEY | 불필요 | 필수 |
| INSERT | O | O |
| UPDATE | X | O (by PK) |
| DELETE | O | O (by PK) |
| 최소 컬럼 수 | 4개 | 1개 (PK) |
| 인덱스 | KV Secondary | B-Tree |
| 대용량 | 대규모 가능 | 수백만 건 이하 권장 |
| JOIN 대상 | O | O |
| Cluster Edition | X | O |

## 선택 가이드

**RDB 테이블을 선택하는 경우**
- 대량 데이터 (수천만 건 이상)
- UPDATE가 필요 없고 DELETE·조회 위주
- 4개 이상 컬럼이 있는 복잡한 스키마
- Standard Edition 환경

**LOOKUP 테이블을 선택하는 경우**
- 코드 테이블, 기준 정보 (수백만 건 이하)
- PRIMARY KEY 기준 UPDATE/DELETE 빈번
- Cluster Edition 환경에서도 사용해야 하는 경우
- 실시간 기준 정보 갱신이 필요한 경우

## 예시

```sql
-- LOOKUP: 국가 코드 테이블 (소규모, UPDATE 필요)
CREATE LOOKUP TABLE country_code (
    code   VARCHAR(4)   PRIMARY KEY,
    name   VARCHAR(64)
);
UPDATE country_code SET name = 'Korea' WHERE code = 'KR';

-- RDB: 주문 이력 (대규모, DELETE 가능, UPDATE 불필요)
CREATE RDB TABLE order_history (
    order_id  LONG,
    item_id   INTEGER,
    qty       INTEGER,
    amount    DOUBLE
);
DELETE FROM order_history WHERE order_id = 12345;
```
