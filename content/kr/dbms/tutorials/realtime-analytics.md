---
type: docs
title: '튜토리얼 3: 실시간 분석'
weight: 30
---

Machbase Volatile 테이블을 사용하여 실시간 모니터링 대시보드를 구축하는 방법을 학습합니다. 이 튜토리얼은 빈번한 업데이트가 필요한 인메모리 데이터를 처리하는 방법을 보여줍니다.

## 시나리오

다음을 표시하는 실시간 공장 모니터링 시스템을 구축합니다:
- 50개 생산 라인의 현재 상태
- 실시간 장비 상태 메트릭
- 활성 알람 및 경고
- 매초 업데이트되는 대시보드

**과제**: 지속적으로 변경되는 데이터에 대해 빠른 INSERT, UPDATE, DELETE 작업이 필요합니다.

**해결책**: 고속 업데이트에 최적화된 인메모리 테이블인 Volatile 테이블을 사용합니다.

## 학습 내용

- 인메모리 데이터를 위한 Volatile 테이블 생성
- UPDATE 및 DELETE 작업 사용
- 키 기반 고속 조회
- Volatile 테이블과 Log/Tag 테이블 결합
- 실시간 상태 보드 구축

## 사전 요구 사항

- Machbase 설치 및 실행
- machsql 클라이언트 연결
- 튜토리얼 1과 2 완료
- 20분의 시간

## 단계 1: Volatile 테이블 생성

Volatile 테이블은 최대 속도를 위해 완전히 메모리에 상주합니다:

```sql
-- 생산 라인 상태
CREATE VOLATILE TABLE production_status (
    line_id INTEGER PRIMARY KEY,
    line_name VARCHAR(50),
    status VARCHAR(20),
    current_product VARCHAR(100),
    items_produced INTEGER,
    target_rate INTEGER,
    actual_rate INTEGER,
    last_updated DATETIME
);
```

**주요 특징**:
- `PRIMARY KEY`는 line_id로 빠른 UPDATE/DELETE 가능
- 모든 데이터가 메모리에 저장 (매우 빠름)
- 데이터는 지속되지 않음 (재시작 시 손실)

## 단계 2: 초기 상태 삽입

```sql
-- 생산 라인 초기화
INSERT INTO production_status VALUES (
    1, 'Assembly Line A', 'RUNNING', 'Widget-X100', 1250, 100, 98, NOW
);
INSERT INTO production_status VALUES (
    2, 'Assembly Line B', 'RUNNING', 'Widget-X200', 890, 80, 82, NOW
);
INSERT INTO production_status VALUES (
    3, 'Packaging Line 1', 'IDLE', NULL, 0, 120, 0, NOW
);
INSERT INTO production_status VALUES (
    4, 'Assembly Line C', 'WARNING', 'Widget-X100', 450, 100, 75, NOW
);
INSERT INTO production_status VALUES (
    5, 'Quality Check', 'RUNNING', 'Widget-X200', 320, 50, 48, NOW
);
```

## 단계 3: 실시간 상태 업데이트

Log/Tag 테이블과 달리 Volatile 테이블은 UPDATE를 지원합니다:

```sql
-- 생산 라인이 배치 완료
UPDATE production_status
SET items_produced = items_produced + 50,
    actual_rate = 101,
    last_updated = NOW
WHERE line_id = 1;

-- 라인이 유지보수 시작
UPDATE production_status
SET status = 'MAINTENANCE',
    current_product = NULL,
    actual_rate = 0,
    last_updated = NOW
WHERE line_id = 3;

-- 라인이 경고 해결
UPDATE production_status
SET status = 'RUNNING',
    actual_rate = 98,
    last_updated = NOW
WHERE line_id = 4;
```

## 단계 4: 현재 상태 쿼리

실시간 대시보드 데이터 조회:

```sql
-- 모든 생산 라인
SELECT * FROM production_status
ORDER BY line_id;

-- 실행 중인 라인만
SELECT line_id, line_name, actual_rate, target_rate
FROM production_status
WHERE status = 'RUNNING';

-- 문제가 있는 라인
SELECT line_id, line_name, status
FROM production_status
WHERE status IN ('WARNING', 'ERROR', 'MAINTENANCE');

-- 성능 메트릭
SELECT
    line_name,
    actual_rate,
    target_rate,
    ROUND((actual_rate * 100.0 / target_rate), 2) as efficiency_pct
FROM production_status
WHERE status = 'RUNNING';
```

## 단계 5: 알람 테이블 생성

과거 추적을 위해 Log 테이블과 결합:

```sql
-- 모든 상태 변경 로그
CREATE TABLE production_events (
    line_id INTEGER,
    event_type VARCHAR(50),
    old_status VARCHAR(20),
    new_status VARCHAR(20),
    message VARCHAR(500)
);

-- 이벤트 로그 삽입
INSERT INTO production_events VALUES (
    4, 'STATUS_CHANGE', 'WARNING', 'RUNNING', 'Line recovered from warning state'
);
INSERT INTO production_events VALUES (
    3, 'STATUS_CHANGE', 'RUNNING', 'MAINTENANCE', 'Scheduled maintenance started'
);
```

## 단계 6: 활성 알람 추적

활성 알람을 위한 또 다른 Volatile 테이블 생성:

```sql
CREATE VOLATILE TABLE active_alarms (
    alarm_id INTEGER PRIMARY KEY,
    line_id INTEGER,
    alarm_type VARCHAR(50),
    severity VARCHAR(20),
    message VARCHAR(500),
    triggered_at DATETIME
);

-- 알람 추가
INSERT INTO active_alarms VALUES (
    1001, 4, 'LOW_THROUGHPUT', 'WARNING', 'Rate below 80% of target', NOW
);
INSERT INTO active_alarms VALUES (
    1002, 2, 'TEMPERATURE_HIGH', 'WARNING', 'Temperature 5C above normal', NOW
);

-- 해결 시 알람 해제
DELETE FROM active_alarms WHERE alarm_id = 1001;

-- 활성 알람 쿼리
SELECT a.*, p.line_name
FROM active_alarms a
JOIN production_status p ON a.line_id = p.line_id
ORDER BY severity, triggered_at;
```

## 단계 7: 실시간 메트릭 구현

운영자 대시보드를 위한 세션 추적 생성:

```sql
CREATE VOLATILE TABLE operator_sessions (
    session_id VARCHAR(50) PRIMARY KEY,
    operator_name VARCHAR(100),
    login_time DATETIME,
    assigned_lines VARCHAR(200),
    last_activity DATETIME
);

-- 운영자 로그인
INSERT INTO operator_sessions VALUES (
    'sess_12345', 'John Smith', NOW, '1,2,3', NOW
);

-- 활동 업데이트
UPDATE operator_sessions
SET last_activity = NOW
WHERE session_id = 'sess_12345';

-- 비활성 세션 제거 (30분 후 타임아웃)
DELETE FROM operator_sessions
WHERE last_activity < NOW - INTERVAL '30' MINUTE;
```

## 단계 8: 대시보드 뷰 생성

포괄적인 뷰를 위해 여러 테이블 결합:

```sql
-- 현재 생산 요약
SELECT
    COUNT(*) as total_lines,
    SUM(CASE WHEN status = 'RUNNING' THEN 1 ELSE 0 END) as running,
    SUM(CASE WHEN status = 'IDLE' THEN 1 ELSE 0 END) as idle,
    SUM(CASE WHEN status = 'WARNING' THEN 1 ELSE 0 END) as warnings,
    SUM(CASE WHEN status = 'ERROR' THEN 1 ELSE 0 END) as errors,
    SUM(items_produced) as total_produced
FROM production_status;

-- 주의가 필요한 라인
SELECT
    p.line_id,
    p.line_name,
    p.status,
    COUNT(a.alarm_id) as active_alarms
FROM production_status p
LEFT JOIN active_alarms a ON p.line_id = a.line_id
WHERE p.status != 'RUNNING'
   OR a.alarm_id IS NOT NULL
GROUP BY p.line_id, p.line_name, p.status;
```

## 직접 해보기

### 연습 1: 생산 사이클 시뮬레이션

생산 사이클을 시뮬레이션하는 일련의 업데이트를 작성합니다:

<details>
<summary>해답</summary>

```sql
-- 생산 시작
UPDATE production_status
SET status = 'RUNNING',
    current_product = 'Widget-X300',
    items_produced = 0,
    actual_rate = 95
WHERE line_id = 3;

-- 생산 진행 중
UPDATE production_status
SET items_produced = items_produced + 100,
    last_updated = NOW
WHERE line_id = 3;

-- 배치 완료
UPDATE production_status
SET status = 'IDLE',
    current_product = NULL,
    actual_rate = 0,
    last_updated = NOW
WHERE line_id = 3;
```
</details>

### 연습 2: 알람 시스템 구축

즉각적인 주의가 필요한 라인을 찾는 쿼리를 생성합니다:

<details>
<summary>해답</summary>

```sql
-- 중요 문제: ERROR 상태 또는 여러 알람
SELECT
    p.line_id,
    p.line_name,
    p.status,
    COUNT(a.alarm_id) as alarm_count,
    MAX(a.severity) as worst_severity
FROM production_status p
LEFT JOIN active_alarms a ON p.line_id = a.line_id
WHERE p.status = 'ERROR'
   OR EXISTS (
       SELECT 1 FROM active_alarms
       WHERE line_id = p.line_id
       AND severity = 'CRITICAL'
   )
GROUP BY p.line_id, p.line_name, p.status;
```
</details>

### 연습 3: 성능 추적

성능이 저하되는 라인을 추적합니다:

<details>
<summary>해답</summary>

```sql
SELECT
    line_id,
    line_name,
    status,
    target_rate,
    actual_rate,
    target_rate - actual_rate as shortfall,
    ROUND((actual_rate * 100.0 / target_rate), 1) as efficiency
FROM production_status
WHERE status = 'RUNNING'
  AND actual_rate < target_rate * 0.9  -- 90% 효율 미만
ORDER BY efficiency ASC;
```
</details>

## 실제 적용

### 패턴: 하이브리드 스토리지

Volatile(현재 상태)과 Log(과거)를 결합:

```sql
-- Volatile: 현재 장비 상태
CREATE VOLATILE TABLE equipment_status (
    equipment_id INTEGER PRIMARY KEY,
    temperature DOUBLE,
    vibration DOUBLE,
    status VARCHAR(20),
    last_reading DATETIME
);

-- Log: 과거 측정값
CREATE TABLE equipment_history (
    equipment_id INTEGER,
    temperature DOUBLE,
    vibration DOUBLE,
    status VARCHAR(20)
);

-- 현재 상태 업데이트 (빠름)
UPDATE equipment_status
SET temperature = 75.5,
    vibration = 0.2,
    last_reading = NOW
WHERE equipment_id = 101;

-- 매 분마다 과거 데이터로 보관
INSERT INTO equipment_history
SELECT equipment_id, temperature, vibration, status
FROM equipment_status;
```

### 패턴: 키-값 캐시

빠른 조회 캐시로 Volatile 테이블 사용:

```sql
CREATE VOLATILE TABLE config_cache (
    config_key VARCHAR(100) PRIMARY KEY,
    config_value VARCHAR(500),
    updated_at DATETIME
);

-- 설정 저장
INSERT INTO config_cache VALUES ('max_temp_threshold', '80.0', NOW);
INSERT INTO config_cache VALUES ('alert_email', 'ops@company.com', NOW);

-- 빠른 조회
SELECT config_value
FROM config_cache
WHERE config_key = 'max_temp_threshold';

-- 설정 업데이트
UPDATE config_cache
SET config_value = '85.0',
    updated_at = NOW
WHERE config_key = 'max_temp_threshold';
```

### 패턴: 세션 관리

활성 사용자 세션 추적:

```sql
CREATE VOLATILE TABLE web_sessions (
    session_token VARCHAR(100) PRIMARY KEY,
    user_id INTEGER,
    ip_address IPV4,
    created_at DATETIME,
    expires_at DATETIME,
    last_activity DATETIME
);

-- 세션 생성
INSERT INTO web_sessions VALUES (
    'tok_abc123xyz', 12345, '192.168.1.100', NOW, NOW + INTERVAL '2' HOUR, NOW
);

-- 세션 검증
SELECT user_id
FROM web_sessions
WHERE session_token = 'tok_abc123xyz'
  AND expires_at > NOW;

-- 활동 업데이트
UPDATE web_sessions
SET last_activity = NOW
WHERE session_token = 'tok_abc123xyz';

-- 만료된 세션 정리
DELETE FROM web_sessions
WHERE expires_at < NOW;
```

## 중요 고려 사항

### 데이터 지속성

**경고**: Volatile 테이블 데이터는 Machbase 종료 시 손실됩니다!

```sql
-- 종료 전 중요한 데이터 보관
INSERT INTO production_events
SELECT line_id, 'SHUTDOWN', status, 'OFFLINE', 'Server shutdown'
FROM production_status
WHERE status = 'RUNNING';
```

### 메모리 관리

메모리 사용량 모니터링:

```sql
-- volatile 테이블 크기 확인
SHOW TABLE production_status;
SHOW TABLE active_alarms;

-- 정리 정책 구현
DELETE FROM operator_sessions
WHERE last_activity < NOW - INTERVAL '1' HOUR;
```

### Volatile 테이블을 사용하지 않아야 할 경우

다음의 경우 Volatile 테이블을 사용하지 마세요:
- 반드시 지속되어야 하는 데이터
- 대용량 연속 데이터 (Tag/Log 테이블 사용)
- 대규모 데이터셋 (사용 가능한 메모리로 제한됨)

## 성능 팁

1. **PRIMARY KEY 사용**: O(1) 조회 가능
2. **데이터를 작게 유지**: 현재 상태만 저장, 과거 데이터는 저장하지 않음
3. **정기적인 정리**: 오래되거나 만료된 레코드 삭제
4. **Log 테이블로 보관**: 오래된 데이터를 영구 저장소로 이동

## 달성한 내용

✓ 인메모리 데이터를 위한 Volatile 테이블 생성
✓ UPDATE 및 DELETE 작업 사용
✓ 실시간 상태 추적 구축
✓ Volatile과 Log 테이블 결합
✓ 세션 관리 구현
✓ 실시간 모니터링 대시보드 생성

## 다음 단계

- **튜토리얼 4**: [참조 데이터](../reference-data/) - Lookup 테이블
- **심화 학습**: [Volatile 테이블 레퍼런스](../../table-types/volatile-tables/) - 고급 기능
- **통합**: [SDK & 통합](../../sdk-integration/) - 애플리케이션에서 연결

## 핵심 요점

1. **Volatile 테이블**은 실시간으로 자주 업데이트되는 데이터에 완벽함
2. **PRIMARY KEY**는 키별 빠른 UPDATE/DELETE 가능
3. **인메모리 저장**은 최대 속도 제공
4. **데이터는 지속되지 않음** - 종료 시 손실
5. **Log/Tag 테이블과 결합**하여 하이브리드 스토리지 패턴 구현
6. **현재 상태**에 사용하고, **과거 데이터**는 Log 테이블에 저장

---

**훌륭합니다!** 이제 실시간 모니터링 시스템을 구축하는 방법을 이해했습니다. [튜토리얼 4: 참조 데이터](../reference-data/)로 계속 진행하세요!
