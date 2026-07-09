---
title: '7.14 Fluentd 입력 파이프라인'
weight: 140
toc: true
---
Fluentd 입력 파이프라인에 해당하는 세부 문서를 모았습니다.


<a id="pipeline-fluentd"></a>

## Fluentd 입력 파이프라인 안내

Fluentd는 오픈소스 데이터 수집 에이전트로, 다양한 소스에서 데이터를 수집하여 Machbase로 전달하는 파이프라인을 구성할 수 있습니다.

### Fluentd + Machbase 구성 개요

```
[로그 소스] → [Fluentd Agent] → [Machbase Fluentd Output Plugin]
  - 애플리케이션 로그
  - 시스템 메트릭
  - 네트워크 장비 로그
```

Fluentd는 Machbase Output Plugin을 통해 Machbase 서버에 접속하고 append 세션으로 데이터를 전송합니다.

### 주요 사용 사례

- 서버 로그를 Machbase LOG 테이블로 수집
- Prometheus/StatsD 메트릭을 TAG 테이블로 저장
- Kafka, AWS S3 등 외부 소스에서 Machbase로 ETL

### 기본 설정 예시

```xml
<!-- Fluentd Machbase Output Plugin -->
<match machbase.**>
  type machbase

  host 127.0.0.1
  port 5656
  uid SYS
  pwd MANAGER

  tablename apache_access_log
  hostname webserver
  arrivaltime true
</match>
```

### 성능 고려사항

- Fluentd의 buffer 설정을 통해 배치 전송으로 성능을 높일 수 있습니다
- `flush_interval`을 낮출수록 실시간성이 높아지지만 처리량이 감소할 수 있습니다
- 고처리량이 필요하다면 여러 Fluentd worker를 병렬로 구성하세요

### 상세 문서

Fluentd Output Plugin 설치, 설정, 튜닝 방법은 다음 문서를 참고하세요.

> **[8장 애플리케이션 연동 → Fluentd](/dbms/application-integration/)** 에서 상세 내용을 다룹니다.

<a id="log-logs-pipeline-connection-fluentd"></a>

## Fluentd로 로그 파이프라인 연결하기

### 시나리오 개요

Fluentd(또는 Fluent Bit)를 Machbase output plugin과 연결하여 애플리케이션 로그, 시스템 로그, 컨테이너 로그를 수집·저장하는 파이프라인을 구성합니다. Machbase의 LOG 테이블은 비정형 텍스트 로그를 시계열로 저장하고 전문 검색(Full-Text Search)을 지원하므로, Fluentd와 결합하면 강력한 중앙 집중식 로그 관리 시스템을 구축할 수 있습니다.

---

### 1단계: 아키텍처 다이어그램

```
┌─────────────────────────────────────────────────────────────────┐
│                        데이터 소스                               │
│  [애플리케이션 로그]  [시스템 저널]  [컨테이너 stdout]            │
└──────────────┬─────────────────┬──────────────┬─────────────────┘
               │                 │              │
               ▼                 ▼              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Fluentd / Fluent Bit                          │
│  ┌──────────────┐   ┌─────────────────┐   ┌──────────────────┐ │
│  │   Source     │ → │  Filter/Parser  │ → │  Output Plugin   │ │
│  │ (tail, tcp,  │   │  (정제·변환·     │   │ (machbase output │ │
│  │  systemd...) │   │   필드 추가)     │   │  plugin)         │ │
│  └──────────────┘   └─────────────────┘   └──────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Machbase LOG 테이블                            │
│  system_log (host, service, level, tag, message, time)          │
└─────────────────────────────────────────────────────────────────┘
```

---

### 2단계: fluent-plugin-machbase 플러그인 설치

Fluentd용 Machbase output plugin을 설치합니다.

```bash
# RubyGems를 통한 설치
gem install fluent-plugin-machbase

# td-agent(Treasure Data Fluentd 패키지)를 사용하는 경우
td-agent-gem install fluent-plugin-machbase

# 설치 확인
gem list | grep machbase
```

Fluent Bit를 사용하는 경우, Machbase HTTP output을 통해 연동합니다(별도 플러그인 불필요).

---

### 3단계: Machbase LOG 테이블 스키마 설계

로그 수집 목적에 맞는 LOG 테이블을 설계합니다.

```sql
-- 범용 시스템 로그 테이블
CREATE TABLE system_log (
    _arrival_time DATETIME,
    host          VARCHAR(128),
    service       VARCHAR(64),
    level         VARCHAR(16),
    tag           VARCHAR(256),
    message       TEXT
);

-- 인덱스 설정 (전문 검색용)
CREATE INDEX idx_syslog_msg ON system_log (message) INDEX_TYPE KEYWORD;
CREATE INDEX idx_syslog_host    ON system_log (host);
CREATE INDEX idx_syslog_service ON system_log (service);
CREATE INDEX idx_syslog_level   ON system_log (level);
```

컬럼별 역할:

| 컬럼 | 타입 | 설명 |
|------|------|------|
| `_arrival_time` | DATETIME | 수집 시각 (자동 설정) |
| `host` | VARCHAR(128) | 로그를 생성한 서버 호스트명 |
| `service` | VARCHAR(64) | 서비스·애플리케이션 이름 |
| `level` | VARCHAR(16) | 로그 레벨 (INFO, WARN, ERROR 등) |
| `tag` | VARCHAR(256) | Fluentd 태그 |
| `message` | TEXT | 실제 로그 메시지 (전문 검색 대상) |

---

### 4단계: fluentd.conf 설정 예시

#### 시스템 로그 파일 수집

```xml
# /etc/fluentd/fluentd.conf (또는 /etc/td-agent/td-agent.conf)

##############################################
# 1. Source: 로그 파일 감시 (tail)
##############################################
<source>
  @type tail
  path /var/log/app/*.log
  pos_file /var/log/fluentd/app.log.pos
  tag app.log
  read_from_head false

  <parse>
    @type regexp
    expression /^(?<time>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}) (?<level>[A-Z]+) (?<message>.+)$/
    time_key   time
    time_format %Y-%m-%dT%H:%M:%S
  </parse>
</source>

<source>
  @type systemd
  tag host.systemd
  path /var/log/journal
  <storage>
    @type local
    persistent true
    path /var/log/fluentd/systemd.pos
  </storage>
  <entry>
    fields_strip_underscores true
    field_map {"MESSAGE": "message", "_HOSTNAME": "host", "SYSLOG_IDENTIFIER": "service", "PRIORITY": "level"}
  </entry>
</source>

##############################################
# 2. Filter: 레코드 정제·변환
##############################################

# 호스트명 자동 추가
<filter app.**>
  @type record_transformer
  <record>
    host "#{Socket.gethostname}"
    service ${tag_parts[0]}
  </record>
</filter>

# 빈 메시지 제거
<filter **>
  @type grep
  <exclude>
    key     message
    pattern /^\s*$/
  </exclude>
</filter>

# 레벨 필드가 없는 경우 기본값 설정
<filter **>
  @type record_transformer
  enable_ruby true
  <record>
    level ${record["level"] || "INFO"}
    tag   ${tag}
  </record>
</filter>

##############################################
# 3. Output: Machbase로 전송
##############################################
<match **>
  type machbase
  host     localhost
  port     5656
  uid      SYS
  pwd      MANAGER
  tablename system_log
  arrivaltime true
  include_time_key true
  localtime true
  time_format %Y-%m-%d %H:%M:%S

  # 컬럼 매핑 (로그 레코드 필드 → 테이블 컬럼)
  columns host, service, level, tag, message

  # 버퍼 설정
  <buffer>
    @type file
    path /var/log/fluentd/buffer/machbase.buf

    # 버퍼 청크 크기 (이 크기가 되면 flush)
    chunk_limit_size 8m

    # flush 주기 (초)
    flush_interval   5s

    # 재전송 설정
    retry_type        exponential_backoff
    retry_wait        1s
    retry_max_interval 60s
    retry_forever     true
  </buffer>
</match>
```

#### TCP 소켓으로 로그 수신

```xml
# TCP 포트로 JSON 로그를 수신하는 소스 추가
<source>
  @type tcp
  tag   tcp.json.log
  port  5170
  <parse>
    @type json
  </parse>
</source>
```

---

### 5단계: 필터링·변환 규칙

#### 특정 레벨 이하 필터링 (DEBUG 제외)

```xml
<filter **>
  @type grep
  <exclude>
    key     level
    pattern /^DEBUG$/
  </exclude>
</filter>
```

#### 민감 정보 마스킹

```xml
<filter **>
  @type record_transformer
  enable_ruby true
  <record>
    # 이메일 주소 마스킹
    message ${record["message"].gsub(/[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/, "***@***.***")}
  </record>
</filter>
```

#### 파싱 실패 레코드 격리

```xml
# 파싱에 실패한 레코드를 별도 태그로 분리
<filter **>
  @type parser
  key_name message
  reserve_data true
  emit_invalid_record_to_error true
  <parse>
    @type json
  </parse>
</filter>

# 파싱 실패 레코드는 파일로 저장
<match fluent.{warn,error}>
  @type file
  path /var/log/fluentd/parse_error
</match>
```

---

### 6단계: 전송 보장 - 버퍼 및 재전송 설정

Machbase 서버가 일시적으로 불가용 상태가 되어도 데이터 유실 없이 재전송할 수 있도록 파일 버퍼를 설정합니다.

```xml
<match **>
  @type machbase
  # ... 연결 설정 ...

  <buffer>
    # 파일 버퍼 사용 (메모리 버퍼는 재시작 시 소실)
    @type file
    path /var/log/fluentd/buffer/machbase.buf

    # 청크 최대 크기 (8MB)
    chunk_limit_size    8m

    # 전체 버퍼 최대 크기 (16GB)
    total_limit_size    16g

    # flush 주기
    flush_interval      5s

    # 청크 행 수 제한 (이 수에 도달하면 즉시 flush)
    chunk_limit_records 10000

    # 재전송: 지수 백오프
    retry_type          exponential_backoff
    retry_wait          1s
    retry_max_interval  60s

    # 무한 재시도 (데이터 유실 방지)
    retry_forever       true
  </buffer>
</match>
```

버퍼 디렉터리 용량을 모니터링합니다.

```bash
# 버퍼 사용량 확인
du -sh /var/log/fluentd/buffer/

# 버퍼 파일 개수 확인 (많으면 Machbase 연결 문제 의심)
ls -1 /var/log/fluentd/buffer/ | wc -l
```

---

### 7단계: 수집 검증 쿼리 및 모니터링

#### 적재 데이터 검증

```sql
-- 최근 수집된 로그 확인 (최신 10건)
SELECT _arrival_time, host, service, level, message
  FROM system_log
 LIMIT 10;

-- 시간대별 로그 건수 추이 확인
SELECT TO_CHAR(_arrival_time, 'YYYY-MM-DD HH24') AS hour_slot,
       level,
       COUNT(*)                                   AS log_count
  FROM system_log
 WHERE _arrival_time >= TO_DATE('2024-01-15', 'YYYY-MM-DD')
 GROUP BY TO_CHAR(_arrival_time, 'YYYY-MM-DD HH24'), level
 ORDER BY hour_slot DESC, level
 LIMIT 50;

-- 서비스별 ERROR 건수
SELECT service,
       COUNT(*) AS error_count
  FROM system_log
 WHERE level = 'ERROR'
   AND _arrival_time >= TO_DATE('2024-01-15', 'YYYY-MM-DD')
 GROUP BY service
 ORDER BY error_count DESC
 LIMIT 20;

-- 전문 검색: 특정 키워드 포함 로그
SELECT _arrival_time, host, service, message
  FROM system_log
 WHERE (message SEARCH 'OutOfMemory'
        OR message SEARCH 'connection refused')
   AND _arrival_time >= TO_DATE('2024-01-15', 'YYYY-MM-DD')
 LIMIT 100;
```

#### Fluentd 자체 모니터링

```bash
# Fluentd 상태 확인
systemctl status td-agent

# 실시간 로그 모니터링
tail -f /var/log/td-agent/td-agent.log

# Fluentd 내장 HTTP 모니터링 (포트 24220)
curl http://localhost:24220/api/plugins.json | python3 -m json.tool
```

Fluentd 설정에 모니터링 에이전트를 추가합니다.

```xml
# Fluentd HTTP 모니터링 에이전트 활성화
<source>
  @type monitor_agent
  bind  0.0.0.0
  port  24220
</source>
```

---

### 8단계: Fluent Bit vs Fluentd 선택 기준

| 항목 | Fluent Bit | Fluentd |
|------|-----------|---------|
| **메모리 사용량** | 매우 낮음 (~1MB) | 보통 (~40MB+) |
| **처리 성능** | 높음 (C 기반) | 보통 (Ruby 기반) |
| **플러그인 생태계** | 기본 플러그인 중심 | 매우 풍부 (600+ 플러그인) |
| **설정 복잡도** | 단순 | 유연하고 복잡 |
| **Machbase 연동** | HTTP output 활용 | fluent-plugin-machbase 사용 |
| **적합 환경** | 엣지 디바이스, 컨테이너 | 서버, 복잡한 파이프라인 |

**Fluent Bit 선택을 권장하는 경우:**
- IoT 게이트웨이, 임베디드 환경
- 쿠버네티스 DaemonSet으로 노드별 로그 수집
- 리소스가 제한된 환경

**Fluentd 선택을 권장하는 경우:**
- 다양한 소스·목적지 연동이 필요한 경우
- 복잡한 필터링·변환 로직이 필요한 경우
- 안정적인 버퍼 관리와 재전송 보장이 중요한 경우

#### Fluent Bit에서 Machbase HTTP API로 전송

fluent-plugin-machbase가 없는 Fluent Bit 환경에서는 HTTP output을 사용합니다.

```ini
# /etc/fluent-bit/fluent-bit.conf

[INPUT]
    Name              tail
    Path              /var/log/app/*.log
    Tag               app.log
    Parser            json
    DB                /var/log/fluent-bit/app.db

[FILTER]
    Name    record_modifier
    Match   *
    Record  host ${HOSTNAME}

[OUTPUT]
    Name            http
    Match           *
    Host            localhost
    Port            5657
    URI             /machbase
    Format          json
    Header          Content-Type application/json
    Retry_Limit     5
```

REST API로 LOG 테이블에 INSERT하는 방식:

```bash
# Fluent Bit HTTP output이 전송하는 데이터를 처리하는
# 중간 서버(예: Python Flask) 또는 직접 REST API 사용 예시

curl -G "http://localhost:5657/machbase" \
     --data-urlencode "q=INSERT INTO system_log (host, service, level, message) VALUES ('web-01', 'nginx', 'ERROR', 'connection refused')"
```

---

### 참고

- Machbase LOG 테이블 전문 검색: [전문 검색 조건](/dbms/performance-tuning/query-analysis/#condition-conditional-search)
- Collector를 이용한 파일 수집: [/dbms/scenario-guides/file-ingestion-collector/](/dbms/scenario-guides/file-ingestion-collector/)
- 대량 적재 파이프라인: [/dbms/scenario-guides/bulk-pipeline/](/dbms/scenario-guides/bulk-pipeline/)
- Fluentd 공식 문서: https://docs.fluentd.org
- Fluent Bit 공식 문서: https://docs.fluentbit.io
