---
type: docs
title: 'Fluentd plugin'
weight: 10
---

Fluentd는 오픈소스 데이터 수집 미들웨어로, `fluent-plugin-machbase` 출력 플러그인을 사용하면 다양한 소스에서 수집한 로그·이벤트 데이터를 Machbase Neo로 스트리밍할 수 있습니다.

## 사전 요구 사항

- Fluentd(td-agent) 1.x 이상 또는 Fluent Bit 2.x 이상
- Ruby 2.7 이상 (Fluentd 자체 실행 환경)
- Machbase Neo 8.0 이상
- Machbase Neo TCP 포트 접근 가능 (기본값: `5656`)

## 플러그인 설치

### 방법 1: gem으로 설치

```bash
gem install fluent-plugin-machbase
```

### 방법 2: td-agent 환경에서 설치

td-agent(Treasure Agent)를 사용하는 경우 td-agent에 포함된 gem 명령어를 사용합니다.

```bash
# td-agent 4.x
sudo td-agent-gem install fluent-plugin-machbase

# Fluentd 1.x (td-agent 3.x)
sudo /opt/td-agent/embedded/bin/fluent-gem install fluent-plugin-machbase
```

설치 확인:

```bash
td-agent-gem list | grep machbase
# 출력 예: fluent-plugin-machbase (0.9.x)
```

## fluentd.conf 설정

### 기본 설정 예시

애플리케이션 로그를 Machbase `log_table` 테이블에 적재하는 기본 구성입니다.

```conf
# 입력 소스: 애플리케이션 로그 파일 감시
<source>
  @type tail
  path /var/log/app/*.log
  pos_file /var/log/fluentd/app.log.pos
  tag app.log
  <parse>
    @type json
  </parse>
</source>

# Machbase 출력
<match app.log>
  @type machbase
  host 127.0.0.1
  port 5656
  user SYS
  password MANAGER
  table_name log_table

  # 필드 매핑: 로그의 JSON 키 → Machbase 컬럼
  <fields>
    ts      ${time}
    level   ${level}
    message ${message}
    host    ${hostname}
  </fields>

  # 버퍼 설정
  <buffer>
    @type file
    path /var/log/fluentd/machbase.buffer
    flush_interval 5s
    chunk_limit_size 8m
    retry_max_interval 30s
    retry_forever false
    retry_max_times 5
  </buffer>
</match>
```

### 다중 소스 집계 예시

여러 소스(syslog, 애플리케이션, 컨테이너)에서 데이터를 수집하여 Machbase에 통합하는 구성입니다.

```conf
# syslog 수신
<source>
  @type syslog
  port 5140
  bind 0.0.0.0
  tag system.syslog
</source>

# Docker 컨테이너 로그
<source>
  @type forward
  port 24224
  bind 0.0.0.0
  tag docker.container
</source>

# 공통 필드 추가 (레코드 변환)
<filter **>
  @type record_transformer
  <record>
    collected_at ${time}
    fluentd_host "#{Socket.gethostname}"
  </record>
</filter>

# syslog → Machbase
<match system.syslog>
  @type machbase
  host 127.0.0.1
  port 5656
  user SYS
  password MANAGER
  table_name syslog_table
  <buffer>
    @type file
    path /var/log/fluentd/syslog.buffer
    flush_interval 10s
    chunk_limit_size 16m
  </buffer>
</match>

# 컨테이너 로그 → Machbase
<match docker.container>
  @type machbase
  host 127.0.0.1
  port 5656
  user SYS
  password MANAGER
  table_name container_log_table
  <buffer>
    @type memory
    flush_interval 3s
    chunk_limit_size 4m
  </buffer>
</match>
```

## 대상 테이블 생성

Fluentd에서 데이터를 받을 Machbase 테이블을 미리 생성합니다. LOG 테이블 또는 TAG 테이블을 용도에 맞게 선택합니다.

### LOG 테이블 (시계열 로그 데이터)

```sql
CREATE TABLE log_table (
    ts      DATETIME,
    level   VARCHAR(16),
    message VARCHAR(4096),
    host    VARCHAR(256)
);
```

### TAG 테이블 (센서·메트릭 데이터)

```sql
CREATE TAG TABLE metric_table (
    name    VARCHAR(64) PRIMARY KEY,
    time    DATETIME BASETIME,
    value   DOUBLE SUMMARIZED
);
```

## 필드 매핑 설정

`<fields>` 블록에서 Fluentd 레코드의 키를 Machbase 테이블의 컬럼에 매핑합니다.

```conf
<fields>
  # 컬럼명   레코드 키 참조
  ts          ${time}          # Fluentd 이벤트 타임스탬프
  level       ${log_level}     # 레코드의 log_level 키
  message     ${msg}           # 레코드의 msg 키
  ip_address  ${remote_addr}   # 레코드의 remote_addr 키
</fields>
```

> **고정값 설정**: `${...}` 대신 따옴표 없는 리터럴 값을 지정하면 고정값으로 삽입됩니다.

## 버퍼(Buffer) 설정 가이드

버퍼 설정은 안정성과 처리량에 직접적인 영향을 줍니다.

| 파라미터 | 설명 | 권장값 |
|----------|------|--------|
| `@type` | 버퍼 유형 (`file` 또는 `memory`) | 프로덕션: `file` |
| `flush_interval` | 버퍼를 Machbase에 플러시하는 주기 | `5s` ~ `30s` |
| `chunk_limit_size` | 단일 청크 최대 크기 | `8m` ~ `64m` |
| `retry_max_times` | 전송 실패 시 최대 재시도 횟수 | `5` ~ `10` |
| `retry_max_interval` | 재시도 간격 최대값 | `30s` ~ `300s` |
| `overflow_action` | 버퍼 초과 시 처리 | `block` (데이터 손실 방지) |

### 고처리량 환경 설정

초당 수만 건 이상의 이벤트를 처리해야 하는 경우:

```conf
<buffer>
  @type file
  path /var/log/fluentd/machbase.buffer
  flush_interval 2s
  chunk_limit_size 64m
  total_limit_size 10g
  flush_thread_count 4
  overflow_action block
  retry_forever false
  retry_max_times 10
  retry_max_interval 60s
</buffer>
```

## 동작 확인

Fluentd를 실행하고 로그를 확인합니다.

```bash
# 설정 파일 문법 검사
fluentd --dry-run -c /etc/fluentd/fluentd.conf

# 포그라운드 실행 (디버그)
fluentd -c /etc/fluentd/fluentd.conf -v

# 서비스로 실행 (td-agent)
sudo systemctl start td-agent
sudo journalctl -u td-agent -f
```

Machbase에서 데이터 수신 확인:

```sql
SELECT COUNT(*) FROM log_table;
SELECT * FROM log_table ORDER BY ts DESC LIMIT 10;
```

## 문제 해결

| 증상 | 원인 | 해결 방법 |
|------|------|-----------|
| 연결 거부 | 포트 또는 방화벽 문제 | Machbase TCP 포트(5656) 개방 여부 확인 |
| 데이터 누락 | 필드 매핑 오류 | `<fields>` 블록의 키 이름과 실제 레코드 키 일치 여부 확인 |
| 버퍼 overflow | 처리 속도 부족 | `flush_thread_count` 증가, 청크 크기 조정 |
| 타입 오류 | 컬럼 타입 불일치 | 테이블 컬럼 타입과 Fluentd 레코드 값 타입 확인 |
