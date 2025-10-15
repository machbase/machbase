---
type: docs
title: '튜토리얼 2: 애플리케이션 로그'
weight: 20
---

Machbase Log 테이블을 사용하여 애플리케이션 로그를 저장하고 검색하는 방법을 학습합니다. 이 튜토리얼은 전문 검색 기능을 활용한 효율적인 로그 관리를 시연합니다.

## 시나리오

다음을 생성하는 웹 애플리케이션을 관리합니다:
- HTTP 액세스 로그
- 애플리케이션 오류 로그
- 사용자 활동 이벤트
- 하루에 수백만 건의 로그 항목

**목표**: 로그를 효율적으로 저장하고, 특정 오류를 검색하며, 시간 경과에 따른 패턴을 분석합니다.

## 학습 내용

- 이벤트 데이터를 위한 Log 테이블 생성
- 대용량 로그 저장
- SEARCH 키워드를 사용한 전문 검색
- DURATION을 사용한 시간 기반 쿼리
- 로그 보존 전략

## 단계 1: Log 테이블 생성

```sql
-- 애플리케이션 오류 로그
CREATE TABLE app_error_logs (
    level VARCHAR(10),
    component VARCHAR(50),
    message VARCHAR(2000),
    user_id INTEGER,
    session_id VARCHAR(50)
);

-- HTTP 액세스 로그
CREATE TABLE access_logs (
    method VARCHAR(10),
    uri VARCHAR(500),
    status_code INTEGER,
    response_time INTEGER,
    ip_addr IPV4,
    user_agent VARCHAR(500)
);
```

**참고**: Log 테이블은 나노초 정밀도의 `_arrival_time` 컬럼을 자동으로 추가합니다!

## 단계 2: 로그 데이터 삽입

```sql
-- 오류 로그
INSERT INTO app_error_logs VALUES (
    'ERROR', 'DatabaseConnection', 'Connection timeout after 30s', 12345, 'sess_abc123'
);
INSERT INTO app_error_logs VALUES (
    'WARN', 'Cache', 'Cache miss ratio exceeded 50%', NULL, NULL
);
INSERT INTO app_error_logs VALUES (
    'ERROR', 'Authentication', 'Invalid credentials for user', 67890, 'sess_def456'
);

-- 액세스 로그
INSERT INTO access_logs VALUES (
    'GET', '/api/users', 200, 45, '192.168.1.100', 'Mozilla/5.0...'
);
INSERT INTO access_logs VALUES (
    'POST', '/api/login', 401, 120, '192.168.1.101', 'curl/7.64.1'
);
INSERT INTO access_logs VALUES (
    'GET', '/api/products', 500, 3000, '192.168.1.102', 'Mozilla/5.0...'
);
```

## 단계 3: 전문 검색

`SEARCH` 키워드를 사용하여 빠른 텍스트 검색:

```sql
-- "timeout"을 포함하는 로그 찾기
SELECT _arrival_time, component, message
FROM app_error_logs
WHERE message SEARCH 'timeout';

-- "connection" 오류 찾기
SELECT * FROM app_error_logs
WHERE level = 'ERROR'
  AND message SEARCH 'connection';

-- "cache" 또는 "memory"가 있는 로그 찾기
SELECT * FROM app_error_logs
WHERE message SEARCH 'cache'
   OR message SEARCH 'memory';

-- "user"와 "invalid"가 모두 있는 로그 찾기
SELECT * FROM app_error_logs
WHERE message SEARCH 'user invalid';
```

## 단계 4: 시간 기반 분석

```sql
-- 최근 10분간의 오류
SELECT * FROM app_error_logs
WHERE level = 'ERROR'
DURATION 10 MINUTE;

-- 최근 1시간 동안의 HTTP 500 오류
SELECT uri, COUNT(*) as error_count
FROM access_logs
WHERE status_code >= 500
DURATION 1 HOUR
GROUP BY uri;

-- 최근 하루 동안의 느린 요청 (>1000ms)
SELECT uri, AVG(response_time) as avg_time
FROM access_logs
WHERE response_time > 1000
DURATION 1 DAY
GROUP BY uri
ORDER BY avg_time DESC;
```

## 단계 5: 패턴 분석

```sql
-- 가장 흔한 오류
SELECT component, message, COUNT(*) as occurrences
FROM app_error_logs
WHERE level = 'ERROR'
DURATION 24 HOUR
GROUP BY component, message
ORDER BY occurrences DESC
LIMIT 10;

-- 시간대별 트래픽
SELECT
    TO_CHAR(_arrival_time, 'YYYY-MM-DD HH24:00:00') as hour,
    COUNT(*) as request_count
FROM access_logs
DURATION 1 DAY
GROUP BY TO_CHAR(_arrival_time, 'YYYY-MM-DD HH24:00:00')
ORDER BY hour;

-- 컴포넌트별 오류율
SELECT
    component,
    COUNT(*) as total_logs,
    SUM(CASE WHEN level = 'ERROR' THEN 1 ELSE 0 END) as error_count
FROM app_error_logs
DURATION 1 HOUR
GROUP BY component;
```

## 단계 6: 데이터 보존

```sql
-- 30일간의 로그만 보관
DELETE FROM app_error_logs EXCEPT 30 DAYS;
DELETE FROM access_logs EXCEPT 30 DAYS;

-- 가장 오래된 백만 행 삭제 (크기 제어용)
DELETE FROM access_logs OLDEST 1000000 ROWS;

-- 최근 100000개의 오류 로그만 보관
DELETE FROM app_error_logs EXCEPT 100000 ROWS;
```

## 직접 해보기

### 연습 1: 보안 로그 생성

보안 이벤트를 위한 테이블을 생성합니다:

<details>
<summary>해답</summary>

```sql
CREATE TABLE security_logs (
    event_type VARCHAR(50),
    user_id INTEGER,
    ip_addr IPV4,
    success CHAR(1),  -- 'Y' or 'N'
    details VARCHAR(500)
);

INSERT INTO security_logs VALUES (
    'LOGIN_ATTEMPT', 12345, '192.168.1.100', 'Y', 'Successful login'
);
INSERT INTO security_logs VALUES (
    'LOGIN_ATTEMPT', 67890, '10.0.0.50', 'N', 'Invalid password'
);
```
</details>

### 연습 2: 실패한 로그인 찾기

최근 1시간 동안 동일한 IP에서 실패한 로그인 시도를 찾는 쿼리를 작성합니다:

<details>
<summary>해답</summary>

```sql
SELECT ip_addr, COUNT(*) as failed_attempts
FROM security_logs
WHERE event_type = 'LOGIN_ATTEMPT'
  AND success = 'N'
DURATION 1 HOUR
GROUP BY ip_addr
HAVING COUNT(*) > 3
ORDER BY failed_attempts DESC;
```
</details>

## 실제 적용

### 자동 로그 수집

```python
# machbase-python을 사용한 Python 예제
import machbase

conn = machbase.connect('127.0.0.1', 5656, 'SYS', 'MANAGER')
cur = conn.cursor()

# 로그 대량 삽입
logs = [
    ('ERROR', 'DB', 'Connection failed', 123, 'sess1'),
    ('WARN', 'Cache', 'High miss rate', None, None),
    # ... 수천 건 이상
]

cur.executemany(
    "INSERT INTO app_error_logs VALUES (?, ?, ?, ?, ?)",
    logs
)
conn.commit()
```

### 로그 모니터링 스크립트

```bash
#!/bin/bash
# monitor_errors.sh - 5분마다 실행

ERRORS=$(machsql -s localhost -u SYS -p MANAGER -i -f - <<EOF
SELECT COUNT(*) FROM app_error_logs
WHERE level = 'ERROR'
DURATION 5 MINUTE;
EOF
)

if [ "$ERRORS" -gt 10 ]; then
    echo "Alert: $ERRORS errors in last 5 minutes" | mail -s "Error Alert" admin@company.com
fi
```

### 대시보드 쿼리

```sql
-- 실시간 모니터링 대시보드
SELECT
    level,
    component,
    COUNT(*) as count,
    MAX(_arrival_time) as last_occurrence
FROM app_error_logs
DURATION 15 MINUTE
GROUP BY level, component
ORDER BY count DESC;
```

## 성능 팁

1. **텍스트 검색에 SEARCH 사용**: LIKE '%pattern%'보다 빠름
2. **항상 시간 범위 제한**: DURATION 또는 _arrival_time에 WHERE 사용
3. **가능한 경우 집계**: 원시 로그를 반환하는 대신 GROUP BY 사용
4. **정기적인 정리**: 매일 보존 삭제 실행

## 달성한 내용

✓ 애플리케이션 이벤트를 위한 Log 테이블 생성
✓ 자동 타임스탬프와 함께 로그 데이터 삽입
✓ SEARCH를 사용한 전문 검색
✓ 시간 기반 쿼리로 패턴 분석
✓ 로그 보존 정책 구현

## 다음 단계

- **튜토리얼 3**: [실시간 분석](../realtime-analytics/) - Volatile 테이블
- **심화 학습**: [Log 테이블 레퍼런스](../../table-types/log-tables/) - 고급 기능
- **일반 작업**: [데이터 쿼리](../../common-tasks/querying/) - 쿼리 최적화

---

[튜토리얼 3: 실시간 분석](../realtime-analytics/)로 계속 진행하세요!
