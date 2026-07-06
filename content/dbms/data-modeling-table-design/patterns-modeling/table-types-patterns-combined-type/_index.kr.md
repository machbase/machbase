---
type: docs
title: '복합 타입 조합 패턴'
weight: 90
---

실제 운영 시스템에서 여러 테이블 타입을 조합하는 대표적인 설계 패턴을 소개합니다.

## 제조 설비 모니터링 시스템

```
┌─────────────────────────────────────────────────┐
│           설비 모니터링 시스템                     │
├──────────────┬──────────────┬───────────────────┤
│ TAG 테이블   │ LOG 테이블   │ LOOKUP 테이블      │
│ sensor_data  │ alarm_event  │ equipment_master   │
│ (계측값 이력) │ (알람 이벤트) │ (설비 기준 정보)   │
├──────────────┴──────────────┴───────────────────┤
│             VOLATILE 테이블                      │
│             sensor_latest (최신값 캐시)           │
└─────────────────────────────────────────────────┘
```

## 물류·주문 관리 시스템 (Standard Edition)

```
┌─────────────────────────────────────────────────┐
│              물류 관리 시스템                     │
├──────────────┬──────────────┬───────────────────┤
│ RDB 테이블   │ LOG 테이블   │ LOOKUP 테이블      │
│ orders       │ delivery_log │ product_master     │
│ (주문 관리)  │ (배송 이벤트) │ (제품 기준 정보)   │
│ UPDATE/DELETE│              │                   │
├──────────────┴──────────────┴───────────────────┤
│             VOLATILE 테이블                      │
│             order_status_cache (현재 상태 캐시)  │
└─────────────────────────────────────────────────┘
```

```sql
-- RDB: 주문 상태 UPDATE 가능
UPDATE orders SET status = 'SHIPPED', shipped_at = NOW WHERE order_id = 1001;

-- LOG: 배송 이벤트 추가 전용
INSERT INTO delivery_log VALUES (NOW, 1001, 'DEPARTED', 'HUB-SEOUL');

-- LOOKUP: 제품 가격 갱신
UPDATE product_master SET price = 19900 WHERE product_id = 42;
```

## 패턴 요약

| 역할 | 권장 타입 | 이유 |
|------|---------|------|
| 고빈도 계측값 이력 | TAG | Append API 고속 버퍼, 시계열 최적화 |
| 이벤트·알람 로그 | LOG | 추가 전용, 도착 시각 자동 |
| 관계형 업무 (UPDATE/DELETE) | RDB | SELECT/INSERT/UPDATE/DELETE 모두 지원 |
| 기준·코드 정보 (소규모) | LOOKUP | PK 기반 UPDATE/DELETE, 영속 |
| 실시간 상태 캐시 | VOLATILE | 메모리 속도, UPSERT |

---

**이 장을 완료했습니다.**

다음으로 읽을 내용:
- [쿼리와 집계](/dbms/query-aggregation/)
- [운영 및 구성](/dbms/operations-configuration-recovery/)
