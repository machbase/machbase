---
type: docs
title: '4.3.4 이벤트·로그 모델링'
weight: 40
---

시스템 이벤트, 알람, 감사 로그를 LOG 테이블로 모델링하는 패턴입니다.

## 계층적 이벤트 모델

```sql
-- 알람 이벤트 LOG 테이블
CREATE TABLE alarm_event (
    severity    SHORT,          -- 1=INFO, 2=WARN, 3=ERROR, 4=CRITICAL
    category    VARCHAR(32),    -- 카테고리
    source      VARCHAR(64),    -- 발생 소스
    message     VARCHAR(512),
    src_ip      IPV4            -- 발생 IP (있는 경우)
);

-- 시스템 감사 LOG 테이블
CREATE TABLE audit_log (
    user_id    VARCHAR(64),
    action     VARCHAR(32),    -- INSERT, UPDATE, DELETE, LOGIN 등
    target     VARCHAR(128),   -- 대상 테이블/리소스
    detail     TEXT,           -- 상세 내용 (전문 검색 대상)
    result     VARCHAR(8)      -- SUCCESS, FAILURE
);

CREATE KEYWORD INDEX idx_audit_detail ON audit_log(detail);
```

## 알람 집계 패턴

```sql
-- 최근 1시간 심각도별 알람 수
SELECT severity, COUNT(*) AS cnt
FROM alarm_event
WHERE _arrival_time >= NOW - 3600000000000
GROUP BY severity
ORDER BY severity DESC;

-- 소스별 알람 현황 (최근 24시간)
SELECT source, COUNT(*) AS total,
       SUM(CASE WHEN severity = 4 THEN 1 ELSE 0 END) AS critical_cnt
FROM alarm_event
WHERE _arrival_time >= NOW - 86400000000000
GROUP BY source
ORDER BY total DESC;
```

## 로그 레벨 필터 패턴

```sql
-- ERROR 이상 로그 조회 (최근 10분)
SELECT _arrival_time, source, message
FROM alarm_event
WHERE severity >= 3
  AND _arrival_time >= NOW - 600000000000
ORDER BY _arrival_time DESC
LIMIT 100;
```

## 전문 검색 패턴

```sql
-- 특정 키워드를 포함하는 감사 로그 조회
SELECT _arrival_time, user_id, action, target
FROM audit_log
WHERE detail SEARCH 'password'
  AND _arrival_time >= NOW - 86400000000000;
```
