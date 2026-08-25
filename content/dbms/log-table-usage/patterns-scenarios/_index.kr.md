---
title: '7.9 활용 패턴과 시나리오'
weight: 90
toc: true
---

<a id="use-cases-log"></a>

## 활용 사례

LOG 테이블은 도착 순서대로 누적하고 시간·텍스트로 검색하는 이벤트 데이터에 적합합니다.

| 적합한 데이터 | 다른 table type을 검토할 조건 |
|---|---|
| 애플리케이션·시스템 로그 | 현재 상태를 키로 자주 수정하면 LOOKUP |
| 보안·네트워크 이벤트 | 센서 시계열 집계가 중심이면 TAG |
| 감사·추적 이벤트 | 관계형 트랜잭션이 필요하면 TRANSACTION |

LOG 테이블에는 `_ARRIVAL_TIME`이 자동으로 추가됩니다. 같은 이름의 사용자 열을 선언하지
마십시오. 원본 발생 시각이 별도로 필요하면 `EVENT_TIME` 같은 열을 추가합니다.

<a id="storage-log-text-search-logs"></a>

## 로그 데이터 저장과 텍스트 검색

### 1단계: 테이블과 키워드 인덱스 생성

```sql
CREATE LOG TABLE sc7_app_log (
    host    VARCHAR(64),
    level   VARCHAR(10),
    message VARCHAR(4096)
);

CREATE INDEX sc7_app_log_message
    ON sc7_app_log(message)
    INDEX_TYPE KEYWORD;
```

### 2단계: 테스트 데이터 입력

```sql
INSERT INTO sc7_app_log VALUES ('web-01', 'INFO', 'login succeeded');
INSERT INTO sc7_app_log VALUES ('web-01', 'WARN', 'response latency warning');
INSERT INTO sc7_app_log VALUES ('web-02', 'ERROR', 'database timeout');

EXEC TABLE_FLUSH(sc7_app_log);
```

대량 수집은 [Append API](/dbms/development-tools-integration/concepts-common/#append-api-batch), 파일
수집은 [Collector](/dbms/log-table-usage/collector-ingestion/)의 정본을 사용합니다. 접속
비밀번호를 예제 소스에 고정하지 않습니다.

### 3단계: 텍스트와 시간 검색

```sql
SELECT _arrival_time, host, level, message
  FROM sc7_app_log
 WHERE message SEARCH 'timeout'
 ORDER BY _arrival_time DESC;
```

```sql
SELECT _arrival_time, host, level, message
  FROM sc7_app_log
 WHERE level IN ('ERROR', 'FATAL')
   AND _arrival_time >= ADD_TIME(SYSDATE, '0/0/0 -1:0:0')
 ORDER BY _arrival_time DESC;
```

### 4단계: 기간 집계

```sql
SELECT TO_CHAR(_arrival_time, 'YYYY-MM-DD HH24') AS hour,
       level,
       COUNT(*) AS event_count
  FROM sc7_app_log
 WHERE _arrival_time >= ADD_TIME(SYSDATE, '0/0/-1 0:0:0')
 GROUP BY TO_CHAR(_arrival_time, 'YYYY-MM-DD HH24'), level
 ORDER BY hour, level;
```

검색 시간 범위는 서비스의 분석 요구에 맞는 최소 구간으로 제한합니다. `NOW()`와 다른 DBMS의
`INTERVAL` 표현을 조합하지 말고 `SYSDATE`, `ADD_TIME`과 Machbase 상대 시간 문법을
사용하십시오.

### 5단계: 보존 정책과 정리

자동 삭제가 필요하면 [데이터 보존 정책](/dbms/operations-configuration-recovery/policy-data-retention/)에서
정책 생성·적용·해제 순서를 확인합니다. 실습 객체는 다음처럼 정리합니다.

```sql
DROP TABLE sc7_app_log;
```
