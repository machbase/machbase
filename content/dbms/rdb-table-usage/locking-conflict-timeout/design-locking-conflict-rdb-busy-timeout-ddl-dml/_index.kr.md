---
type: docs
title: '8.11.2 잠금·충돌·타임아웃 설계'
weight: 70
---

RDB 테이블에 동시에 여러 세션이 접근하면 잠금 충돌이 발생할 수 있습니다.

## 잠금 동작

| 작업 | 잠금 유형 |
|------|---------|
| SELECT | 공유 잠금 (읽기 가능) |
| INSERT | 배타 잠금 (해당 행) |
| DELETE | 배타 잠금 (해당 행) |
| DDL (CREATE INDEX, DROP TABLE 등) | 테이블 잠금 |

## BUSY TIMEOUT 설정

잠금 대기 시간을 설정하여 데드락을 방지합니다.

```sql
-- 세션별 타임아웃 설정 (밀리초 단위)
ALTER SESSION SET RDB_BUSY_TIMEOUT_MS = 5000;  -- 5초 대기 후 오류 반환
```

## DDL 잠금 충돌 방지

인덱스 생성 등 DDL 작업은 테이블 잠금을 걸므로, DML 트래픽이 낮은 시간대에 실행합니다.

```sql
-- 인덱스 생성 (운영 시간 외 권장)
CREATE INDEX idx_order_time ON order_history(order_time);
```

## 동시성 설계 지침

1. **트랜잭션 범위 최소화**: 필요한 DML만 포함하여 잠금 보유 시간을 줄입니다.
2. **배치 작업 분리**: 대량 INSERT/DELETE는 별도 세션이나 오프피크 시간에 실행합니다.
3. **DDL과 DML 분리**: 인덱스 생성, 컬럼 추가 등 DDL은 트래픽이 낮은 시간에 실행합니다.
4. **BUSY_TIMEOUT 설정**: 애플리케이션 로직에 따라 적절한 대기 시간을 설정합니다.

## 오류 처리

잠금 충돌 오류 발생 시 애플리케이션에서 재시도 로직을 구현합니다.

```python
import time

def insert_with_retry(conn, sql, max_retries=3):
    for attempt in range(max_retries):
        try:
            conn.execute(sql)
            conn.commit()
            return True
        except Exception as e:
            if 'BUSY' in str(e) and attempt < max_retries - 1:
                time.sleep(0.1 * (attempt + 1))
                continue
            raise
    return False
```
