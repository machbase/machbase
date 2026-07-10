---
title: '7.9 활용 패턴과 시나리오'
weight: 90
toc: true
---

<a id="use-cases-log"></a>

## 활용 사례

LOG 테이블은 다음과 같은 데이터에 적합합니다.

### 적합한 데이터 유형

| 유형 | 예시 |
|------|------|
| 시스템 이벤트 | syslog, Windows Event Log |
| 애플리케이션 로그 | 웹 서버 액세스 로그, 오류 로그 |
| 네트워크 패킷 | NetFlow, IPFIX, 패킷 메타데이터 |
| 보안 이벤트 | IDS/IPS 경보, 방화벽 로그 |
| 트랜잭션 감사 | 데이터베이스 감사 로그 |

### 예시 스키마

#### 웹 액세스 로그

```sql
CREATE TABLE web_access_log (
    method    VARCHAR(8),
    uri       VARCHAR(1024),
    status    SHORT,
    bytes     INTEGER,
    src_ip    IPV4,
    user_agent VARCHAR(512)
);
```

#### 방화벽 이벤트 로그

```sql
CREATE TABLE fw_event (
    action    VARCHAR(8),
    src_ip    IPV4,
    dst_ip    IPV4,
    src_port  INTEGER,
    dst_port  INTEGER,
    protocol  SHORT
);
```

### 부적합한 경우

- 수정이 필요한 데이터 (UPDATE 불가)
- KEY 기반 조회가 빈번한 소규모 참조 데이터 → LOOKUP 테이블 권장
- 센서 계측값 → TAG 테이블 권장

<a id="storage-log-text-search-logs"></a>

## 로그 데이터 저장과 텍스트 검색

로그 데이터는 이벤트 분석과 장애 진단의 핵심 자원입니다. 여기서는 LOG 테이블에 애플리케이션 로그를 저장하고, 텍스트 검색과 시간 기반 집계로 분석하는 전체 흐름을 단계별로 안내합니다.

**난이도**: 초급
**소요 시간**: 30~45분
**주요 기능**: LOG 테이블, 키워드 인덱스, SEARCH, GROUP BY 시간 집계, Retention Policy

---

### 시나리오 개요

```
애플리케이션 / 서버
   │
   │ (Append API / Fluentd)
   ▼
LOG 테이블 (app_log)        ← 로그 고속 저장 (_arrival_time 자동 기록)
   │
   ├── 텍스트 검색           ← SEARCH 키워드 인덱스
   ├── 기간별 집계           ← GROUP BY 1 HOUR
   └── 보관 정책             ← DURATION 자동 삭제
```

---

### 1단계: LOG 테이블 스키마 설계

`CREATE TABLE` 구문으로 테이블을 생성합니다. `_arrival_time` 컬럼은 자동으로 추가되며, 데이터가 서버에 도착한 시각을 나노초 정밀도로 기록합니다.

```sql
CREATE TABLE app_log (
    host      VARCHAR(64),
    level     VARCHAR(10),
    message   VARCHAR(4096),
    _arrival_time DATETIME DEFAULT SYSDATE
);
```

| 컬럼 | 타입 | 역할 |
|------|------|------|
| `host` | VARCHAR(64) | 로그를 발생시킨 서버 호스트명 |
| `level` | VARCHAR(10) | 로그 레벨 (DEBUG, INFO, WARN, ERROR, FATAL) |
| `message` | VARCHAR(4096) | 로그 메시지 본문 |
| `_arrival_time` | DATETIME | 서버 수신 시각 (자동 기록) |

> **참고**: `_arrival_time`은 명시적으로 선언하지 않아도 LOG 테이블에 자동으로 추가됩니다. 애플리케이션이 발생시킨 시각을 별도로 기록하려면 `log_time DATETIME` 컬럼을 추가합니다.

#### 추가 컬럼이 필요한 경우

더 풍부한 분석을 위해 서비스명, 환경, 요청 ID 등을 추가할 수 있습니다.

```sql
CREATE TABLE app_log_detail (
    host       VARCHAR(64),
    service    VARCHAR(32),
    env        VARCHAR(16),
    level      VARCHAR(10),
    request_id VARCHAR(64),
    message    VARCHAR(4096),
    log_time   DATETIME
);
```

---

### 2단계: 텍스트 검색 인덱스 생성

`message` 컬럼에 키워드 인덱스를 생성하면 `SEARCH` 연산자로 빠른 전문 검색이 가능합니다. 키워드 인덱스는 역인덱스(Inverted Index) 방식으로 동작하며 LIKE 검색보다 훨씬 빠릅니다.

```sql
CREATE INDEX idx_app_log_message
    ON app_log (message)
    INDEX_TYPE KEYWORD;
```

`level` 컬럼도 자주 필터 조건으로 사용되므로 일반 인덱스를 추가합니다.

```sql
CREATE INDEX idx_app_log_level
    ON app_log (level);
```

---

### 3단계: 로그 수집

#### Append API로 직접 삽입 (Python)

```python
import machbasedb
from datetime import datetime

conn = machbasedb.connect(
    host='127.0.0.1',
    port=5656,
    user='SYS',
    password='MANAGER'
)

appender = conn.appender('app_log')

# 로그 데이터 삽입 예시
logs = [
    ('web-01', 'INFO',  'User login succeeded: user_id=1042'),
    ('web-01', 'WARN',  'Response time exceeded 2s: /api/order latency=2341ms'),
    ('web-02', 'ERROR', 'Database connection failed: timeout after 30s'),
    ('web-02', 'ERROR', 'NullPointerException at OrderService.process line 128'),
    ('api-01', 'INFO',  'Order created: order_id=8821 amount=59000'),
    ('api-01', 'FATAL', 'Out of memory: heap space exhausted'),
]

for host, level, message in logs:
    appender.append((host, level, message, datetime.now()))

appender.close()
conn.close()
```

#### SQL INSERT 방식 (테스트용)

```sql
INSERT INTO app_log VALUES ('web-01', 'INFO',  'User login succeeded: user_id=1042', NOW());
INSERT INTO app_log VALUES ('web-01', 'WARN',  'Response time exceeded 2s: /api/order latency=2341ms', NOW());
INSERT INTO app_log VALUES ('web-02', 'ERROR', 'Database connection failed: timeout after 30s', NOW());
INSERT INTO app_log VALUES ('web-02', 'ERROR', 'NullPointerException at OrderService.process line 128', NOW());
INSERT INTO app_log VALUES ('api-01', 'INFO',  'Order created: order_id=8821 amount=59000', NOW());
INSERT INTO app_log VALUES ('api-01', 'FATAL', 'Out of memory: heap space exhausted', NOW());
```

#### Fluentd로 로그 파이프라인 연결

Fluentd machbase 플러그인을 사용하면 애플리케이션 로그를 직접 Machbase에 적재할 수 있습니다. 설정 방법은 [Fluentd로 로그 파이프라인 연결하기](/dbms/log-table-usage/fluentd-pipeline/#log-logs-pipeline-connection-fluentd)를 참고합니다.

---

### 4단계: 텍스트 검색 — SEARCH 연산자 활용

키워드 인덱스를 활용하여 메시지 본문에서 단어를 빠르게 찾을 수 있습니다.

#### 단일 키워드 검색

```sql
-- "timeout"이 포함된 로그 검색
SELECT _arrival_time, host, level, message
FROM app_log
WHERE message SEARCH 'timeout'
ORDER BY _arrival_time DESC;
```

#### 복수 키워드 AND 검색

```sql
-- "Database"와 "failed"가 모두 포함된 로그
SELECT _arrival_time, host, level, message
FROM app_log
WHERE message SEARCH 'Database failed'
ORDER BY _arrival_time DESC;
```

#### OR 검색 — 여러 오류 패턴 동시 탐지

```sql
-- "timeout" 또는 "NullPointerException"이 포함된 로그
SELECT _arrival_time, host, level, message
FROM app_log
WHERE message SEARCH 'timeout'
   OR message SEARCH 'NullPointerException'
ORDER BY _arrival_time DESC;
```

#### 레벨 필터와 텍스트 검색 조합

```sql
-- ERROR 레벨 중 "connection"이 포함된 로그
SELECT _arrival_time, host, message
FROM app_log
WHERE level = 'ERROR'
  AND message SEARCH 'connection'
ORDER BY _arrival_time DESC;
```

#### 특정 시간대 텍스트 검색

```sql
-- 최근 1시간 내 ERROR·FATAL 로그에서 "memory" 검색
SELECT _arrival_time, host, level, message
FROM app_log
WHERE _arrival_time >= NOW() - INTERVAL '1' HOUR
  AND level IN ('ERROR', 'FATAL')
  AND message SEARCH 'memory'
ORDER BY _arrival_time DESC;
```

---

### 5단계: 기간별 집계 분석

#### 1시간 단위 레벨별 로그 건수

```sql
SELECT
    TO_CHAR(_arrival_time, 'YYYY-MM-DD HH24') AS hour,
    level,
    COUNT(*) AS cnt
FROM app_log
WHERE _arrival_time >= NOW() - INTERVAL '24' HOUR
GROUP BY TO_CHAR(_arrival_time, 'YYYY-MM-DD HH24'), level
ORDER BY hour, level;
```

#### 호스트별 ERROR 발생 추이 (10분 단위)

```sql
SELECT
    TRUNC(_arrival_time, 600000000000) AS bucket,  -- 10분 버킷 (나노초 단위)
    host,
    COUNT(*) AS error_cnt
FROM app_log
WHERE level IN ('ERROR', 'FATAL')
  AND _arrival_time >= NOW() - INTERVAL '6' HOUR
GROUP BY TRUNC(_arrival_time, 600000000000), host
ORDER BY bucket, host;
```

#### 오늘 하루 시간대별 로그 볼륨

```sql
SELECT
    TO_CHAR(_arrival_time, 'HH24') AS hour,
    COUNT(*) AS total_cnt,
    SUM(CASE WHEN level = 'ERROR' THEN 1 ELSE 0 END) AS error_cnt,
    SUM(CASE WHEN level = 'WARN'  THEN 1 ELSE 0 END) AS warn_cnt
FROM app_log
WHERE _arrival_time >= TRUNC(NOW(), 'DD')
GROUP BY TO_CHAR(_arrival_time, 'HH24')
ORDER BY hour;
```

---

### 6단계: ERROR 레벨 로그 집중 분석 패턴

#### ERROR 로그 상위 패턴 파악

자주 발생하는 오류 유형을 키워드 검색으로 분류합니다.

```sql
-- "timeout" 관련 오류 건수
SELECT COUNT(*) AS timeout_cnt
FROM app_log
WHERE level = 'ERROR'
  AND message SEARCH 'timeout'
  AND _arrival_time >= NOW() - INTERVAL '1' HOUR;
```

```sql
-- "exception" 관련 오류 건수
SELECT COUNT(*) AS exception_cnt
FROM app_log
WHERE level = 'ERROR'
  AND message SEARCH 'Exception'
  AND _arrival_time >= NOW() - INTERVAL '1' HOUR;
```

#### 호스트별 ERROR 집계

```sql
SELECT
    host,
    COUNT(*) AS error_cnt
FROM app_log
WHERE level = 'ERROR'
  AND _arrival_time >= NOW() - INTERVAL '24' HOUR
GROUP BY host
ORDER BY error_cnt DESC;
```

#### 연속 ERROR 구간 탐지 — 최근 ERROR 로그 타임라인

```sql
-- 최근 ERROR/FATAL 로그 최신 20건
SELECT _arrival_time, host, level, message
FROM app_log
WHERE level IN ('ERROR', 'FATAL')
  AND _arrival_time >= NOW() - INTERVAL '24' HOUR
ORDER BY _arrival_time DESC
LIMIT 20;
```

---

### 7단계: 로그 보관 정책 설정 (DURATION)

오래된 로그를 자동 삭제하여 디스크 공간을 관리합니다. 리텐션 정책을 만들고 테이블에 연결합니다.

```sql
-- 30일 보관 정책 설정
CREATE RETENTION app_log_30d DURATION 30 DAY INTERVAL 1 DAY;
ALTER TABLE app_log ADD RETENTION app_log_30d;
```

```sql
-- 보관 정책 확인
SELECT * FROM m$retention;
SELECT * FROM v$retention_job;
```

```sql
-- 보관 정책 해제 (무기한 보관)
ALTER TABLE app_log DROP RETENTION;
```

> **주의**: DURATION을 설정하면 기간이 지난 데이터는 자동으로 삭제됩니다. 삭제 전 필요한 데이터는 별도 백업을 권장합니다.

---

### 핵심 포인트 요약

| 항목 | 내용 |
|------|------|
| LOG 테이블 생성 | `CREATE TABLE` 구문 사용. `_arrival_time`은 자동 추가 |
| 키워드 인덱스 | `CREATE INDEX ... INDEX_TYPE KEYWORD` 로 전문 검색 인덱스 생성 |
| SEARCH 연산자 | `WHERE message SEARCH '키워드'` 형식으로 역인덱스 검색. AND/OR 복합 가능 |
| 시간 집계 | `TO_CHAR(_arrival_time, 'YYYY-MM-DD HH24')` 또는 `TRUNC` 함수로 버킷 집계 |
| ERROR 분석 | 레벨 필터 + SEARCH 조합으로 오류 패턴 신속 탐지 |
| 보관 정책 | `ALTER TABLE ... SET DURATION = N DAY` 로 자동 삭제 기간 설정 |

---

### 다음 단계

- 센서 데이터와 ROLLUP 분석은 [센서 데이터 저장과 ROLLUP 분석](/dbms/tag-rollup-usage/patterns-scenarios/#storage-sensor-data-rollup)을 참고합니다.
- 장비 마스터와 LOG 테이블을 연계한 알람 관리는 [장비 마스터 데이터와 알람 상태 관리](/dbms/scenario-guides/state-master-status-equipment-alarm/)를 참고합니다.
- STREAM으로 LOG 데이터를 TAG 테이블에 자동 적재하는 방법은 [STREAM으로 LOG를 TAG로 자동 적재](/dbms/log-table-usage/stream-log-processing/#stream-log-tag)를 참고합니다.
