---
type: docs
title: '활용 사례'
weight: 10
---

RDB 테이블은 관계형 구조의 대규모 업무 데이터 저장에 적합합니다.

## 적합한 데이터 유형

| 유형 | 설명 |
|------|------|
| 주문·거래 이력 | INSERT·SELECT·DELETE 위주, 건수가 수천만 건 이상 |
| 이벤트 상태 관리 | 상태 변경 이력 (UPDATE 불필요, DELETE + 재삽입 패턴) |
| 설비 이력 데이터 | 점검 이력, 교체 이력 등 |
| 대용량 참조 이력 | 수백만 건 이상 참조 데이터 (LOOKUP 테이블로 부족한 경우) |

## 예시 스키마

### 주문 이력

```sql
CREATE RDB TABLE order_history (
    order_id   LONG,
    customer   VARCHAR(64),
    item_id    INTEGER,
    qty        INTEGER,
    amount     DOUBLE
);
```

### 설비 점검 이력

```sql
CREATE RDB TABLE maintenance_log (
    equip_id    VARCHAR(32),
    check_date  DATETIME,
    technician  VARCHAR(64),
    result      VARCHAR(16)
);
```

### 알람 발생 이력

```sql
CREATE RDB TABLE alarm_history (
    alarm_id   LONG,
    sensor     VARCHAR(64),
    alarm_time DATETIME,
    level      SHORT,
    message    VARCHAR(256)
);
```

## 부적합한 경우

- **UPDATE 필요**: RDB 테이블은 UPDATE를 지원하지 않습니다. 행 수정이 필요하면 DELETE + INSERT 패턴을 사용합니다.
- **Cluster Edition**: RDB 테이블은 Standard Edition 전용입니다.
- **센서 계측값**: 시계열 패턴이면 TAG 테이블을 권장합니다.
- **소규모 코드 테이블 + UPDATE 필요**: LOOKUP 테이블을 권장합니다.
