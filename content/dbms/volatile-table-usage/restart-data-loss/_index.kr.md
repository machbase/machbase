---
title: '10.11 재시작과 데이터 소실'
weight: 110
toc: true
---

VOLATILE 테이블의 데이터 소실 특성과 이에 대비한 설계 방법을 정리한다.


<a id="data-loss"></a>

## 데이터 손실 위험

VOLATILE 테이블의 데이터는 서버 종료 시 소멸된다. 이 특성을 반드시 이해하고 설계에 반영해야 한다.

### 데이터 손실 시나리오

| 시나리오 | 데이터 손실 여부 |
|---------|--------------|
| 서버 정상 종료 (machadmin -s) | O (전체 소멸) |
| 서버 비정상 종료 (kill -9, OOM) | O (전체 소멸) |
| 전원 차단 | O (전체 소멸) |
| 클라이언트 연결 끊김 | X (데이터 유지) |
| 세션 종료 | X (데이터 유지) |

### 설계 시 고려사항

#### 재생성 가능한 데이터만 저장

원본 데이터에서 언제든 재계산·재생성할 수 있는 데이터만 VOLATILE 테이블에 저장한다.

```sql
-- 좋은 예: TAG 테이블 집계 캐시 (재계산 가능)
CREATE VOLATILE TABLE sensor_1min_avg (
    sensor_id VARCHAR(64) PRIMARY KEY,
    avg_val   DOUBLE,
    calc_at   DATETIME
);

-- 나쁜 예: 원본 데이터를 VOLATILE에만 저장
-- (서버 재시작 시 복구 불가)
```

#### 정기 플러시 패턴

중요 데이터는 주기적으로 디스크 테이블에 플러시한다.

```sql
-- VOLATILE 캐시 → LOG 테이블 영구 저장 (주기적 실행)
INSERT INTO sensor_agg_log
SELECT sensor_id, avg_val, calc_at FROM sensor_1min_avg;
```

#### 재시작 복구 스크립트

서버 시작 시 VOLATILE 테이블을 재생성하고 초기 데이터를 채우는 스크립트를 준비한다.

```bash
#!/bin/bash
# /etc/machbase/startup.sql
machsql -u SYS -p MANAGER << 'SQL'
CREATE VOLATILE TABLE sensor_latest (
    sensor_id  VARCHAR(64) PRIMARY KEY,
    value      DOUBLE,
    updated_at DATETIME
);
-- 최신 값 초기 로드
INSERT INTO sensor_latest
SELECT name, value, time FROM sensor_data WHERE time = (SELECT MAX(time) FROM sensor_data);
SQL
```

---

**다음 읽을 내용**
- [안티패턴](/dbms/data-modeling-table-design/table-types-patterns-type-anti/)
