---
title: '8.9 활용 패턴과 시나리오'
weight: 90
toc: true
---
활용 패턴과 시나리오에 해당하는 세부 문서를 모았습니다.


<a id="use-cases-rdb"></a>

## 활용 사례

RDB 테이블은 INSERT·UPDATE·DELETE·SELECT가 모두 필요한 일반 관계형 업무 데이터에 적합합니다.

### 적합한 데이터 유형

| 유형 | 설명 |
|------|------|
| 주문·거래 이력 | 상태 변경(UPDATE) + 조회(SELECT) + 삭제(DELETE) |
| 설비 이력 데이터 | 점검 결과 수정, 조회 |
| 재고 관리 | 재고 수량 UPDATE, 내역 DELETE |
| 대용량 참조 이력 | 수백만 건 이상 참조 데이터 (LOOKUP 테이블로 부족한 경우) |
| 이벤트 상태 관리 | 상태 컬럼 UPDATE가 필요한 업무 |

### 예시 스키마

#### 주문 관리

```sql
CREATE RDB TABLE orders (
    order_id   LONG,
    customer   VARCHAR(64),
    item_id    INTEGER,
    qty        INTEGER,
    amount     DOUBLE,
    status     VARCHAR(16)
);

CREATE INDEX idx_order_customer ON orders(customer);
CREATE INDEX idx_order_status   ON orders(status);

-- 상태 변경
UPDATE orders SET status = 'SHIPPED' WHERE order_id = 1001;

-- 취소 처리
DELETE FROM orders WHERE order_id = 1001;
```

#### 재고 관리

```sql
CREATE RDB TABLE inventory (
    item_id    INTEGER,
    warehouse  VARCHAR(32),
    qty        INTEGER,
    updated_at DATETIME
);

-- 재고 차감
UPDATE inventory SET qty = qty - 5, updated_at = NOW
WHERE item_id = 42 AND warehouse = 'WH-01';
```

#### 설비 점검 이력

```sql
CREATE RDB TABLE maintenance_log (
    equip_id    VARCHAR(32),
    check_date  DATETIME,
    technician  VARCHAR(64),
    result      VARCHAR(16),
    note        VARCHAR(512)
);

-- 점검 결과 수정
UPDATE maintenance_log SET result = 'PASS', note = '재확인 완료'
WHERE equip_id = 'MOTOR-01' AND check_date = '2024-01-15 09:00:00';
```

### 부적합한 경우

- **Cluster Edition**: RDB 테이블은 Standard Edition 전용입니다.
- **센서 계측값**: 시계열 패턴이면 TAG 테이블을 권장합니다.
- **소규모 코드 테이블**: PRIMARY KEY 기반 UPDATE 위주면 LOOKUP 테이블이 더 적합합니다.
