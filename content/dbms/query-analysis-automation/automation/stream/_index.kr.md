---
type: docs
title: 'STREAM'
weight: 10
---

STREAM은 원본 LOG 테이블에 새로 입력된 데이터를 실시간으로 감지해 미리 정의한 `INSERT ... SELECT` 쿼리를 자동 실행하는 기능입니다. CEP(복합 이벤트 처리), 실시간 집계, 데이터 라우팅에 활용합니다.

## 동작 원리

```
원본 테이블 (LOG)
  ↓ 새 데이터 입력 감지
STREAM 실행 엔진
  ↓ INSERT ... SELECT 실행
대상 테이블 (LOG, TAG 등)
```

STREAM은 마지막으로 처리한 행의 RID(Row ID)를 기억합니다. 다음 실행 때는 그 RID 이후의 새 데이터만 처리합니다. 서버 재시작 후에도 이 위치가 유지되어 연속적으로 처리됩니다.

## 실행 주기

| 실행 조건 | 동작 |
|-----------|------|
| 주기 없음 (기본) | 새 행이 입력될 때마다 즉시 실행 |
| `BY n SECOND` | 매 n초마다 누적 데이터를 집계해 실행 |
| `BY USER` | 사용자가 `EXEC STREAM_EXECUTE`를 호출할 때만 실행 |

주기를 설정하면 SUM, AVG 같은 집계 함수를 사용할 수 있습니다. 주기 없이 실행하면 집계 함수를 사용할 수 없습니다.

## 제약사항

- 쿼리는 `INSERT INTO target SELECT ... FROM source` 형태만 허용됩니다.
- 원본 테이블은 LOG 테이블이어야 합니다.
- STREAM은 Standard Edition 전용입니다.

> STREAM 기능은 **Standard Edition**에서만 지원됩니다. Cluster Edition에서 STREAM 생성을 시도하면 오류가 반환됩니다.
