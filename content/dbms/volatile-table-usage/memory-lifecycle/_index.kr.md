---
title: '10.10 메모리 생명주기'
weight: 100
toc: true
---

<a id="lifecycle-memory"></a>

## 메모리 생명주기

VOLATILE 테이블의 데이터는 메모리에 저장되며, 서버가 종료되면 함께 소멸됩니다.

### 생명주기

```
서버 시작
  └── VOLATILE 테이블 생성 (수동 또는 초기화 스크립트)
        └── 데이터 INSERT/UPDATE/DELETE
              └── 서버 종료 → 데이터 소멸
```

### 세션 공유

VOLATILE 테이블은 세션 범위가 아닌 **서버 수준** 공유 테이블입니다. 여러 세션에서 동시에 읽기·쓰기할 수 있습니다.

```sql
-- 세션 A
INSERT INTO sensor_latest VALUES ('TEMP-01', 25.3, NOW);

-- 세션 B (다른 연결)
SELECT * FROM sensor_latest WHERE sensor_id = 'TEMP-01';
-- TEMP-01, 25.3, ... 조회 가능
```

### 메모리 사용량

데이터가 전부 메모리에 있으므로 사용량을 주기적으로 확인합니다.

```sql
-- VOLATILE 테이블 레코드 수 확인
SELECT COUNT(*) FROM sensor_latest;
```

### 서버 시작 시 자동 생성 패턴

```bash
# /etc/machbase/startup.sql (예시)
CREATE VOLATILE TABLE sensor_latest (
    sensor_id  VARCHAR(64) PRIMARY KEY,
    value      DOUBLE,
    updated_at DATETIME
);

# 서버 시작 후 machsql로 실행
machsql -u SYS -p MANAGER -f /etc/machbase/startup.sql
```

### 주의사항

- 대량 데이터를 VOLATILE 테이블에 저장하면 서버 메모리 부족(OOM)이 발생할 수 있습니다.
- 예상 레코드 수 × 행 크기가 가용 메모리의 10% 이내로 유지하는 것을 권장합니다.
