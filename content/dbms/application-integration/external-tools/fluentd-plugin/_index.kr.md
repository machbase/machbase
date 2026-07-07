---
type: docs
title: 'Fluentd plugin'
weight: 10
---

Fluentd는 오픈소스 데이터 수집 미들웨어로, `fluent-plugin-machbase` 출력
플러그인을 사용하면 다양한 소스에서 수집한 로그·이벤트 데이터를 Machbase로
스트리밍할 수 있습니다.

## 사전 요구 사항

- Fluentd(td-agent) 0.10.54 호환 환경
- `machbase` Ruby gem
- Machbase TCP 포트 접근 가능 (기본값: `5656`)

## 플러그인 설치

### 방법 1: gem으로 설치

```bash
gem install fluent-plugin-machbase
```

### 방법 2: td-agent 환경에서 설치

td-agent(Treasure Agent)를 사용하는 경우 td-agent에 포함된 gem 명령어를 사용합니다.

```bash
# td-agent에 포함된 gem 사용
sudo /opt/td-agent/embedded/bin/fluent-gem install fluent-plugin-machbase
```

설치 확인:

```bash
fluent-gem list | grep machbase
# 출력 예: fluent-plugin-machbase (...)
```

## fluentd.conf 설정

### 기본 설정 예시

애플리케이션 로그를 Machbase `log_table` 테이블에 적재하는 기본 구성입니다.

```conf
# 입력 소스: JSON 애플리케이션 로그 파일 감시
<source>
  type tail
  path /var/log/app/*.log
  pos_file /var/log/fluentd/app.log.pos
  tag app.log
  format json
</source>

# Machbase 출력
<match app.log>
  type machbase
  host 127.0.0.1
  port 5656
  uid SYS
  pwd MANAGER
  tablename log_table

  buffersize 64
  bufferflush false
  arrivaltime true

  include_time_key true
  localtime true
  time_format %Y-%m-%d %H:%M:%S
</match>
```

### Apache access log 예시

Apache access log를 수집하여 Machbase에 적재하는 구성입니다.

```conf
# Apache access log → Machbase
<source>
  type tail
  format apache2
  path /var/log/httpd/access_log
  pos_file /var/log/td-agent/access.pos
  tag machbase.apache.access
</source>

<match machbase.apache.access>
  type machbase
  host 127.0.0.1
  port 5656
  uid SYS
  pwd MANAGER
  tablename apache_access_log
  hostname webserver
  buffersize 64
  bufferflush false
  arrivaltime true
  include_time_key true
  localtime true
  time_format %Y-%m-%d %H:%M:%S
</match>
```

## 대상 테이블 생성

Fluentd에서 데이터를 받을 Machbase LOG 테이블을 미리 생성합니다. 플러그인은
Append 프로토콜을 사용하며, `<fields>` 매핑 블록을 지원하지 않습니다. Fluentd
레코드의 값은 레코드 순서대로 테이블 컬럼에 들어가므로 입력 파서가 생성하는 필드
순서와 테이블 컬럼 순서를 맞춥니다.

### LOG 테이블 (시계열 로그 데이터)

```sql
CREATE TABLE log_table (
    level   VARCHAR(16),
    message VARCHAR(4096),
    source  VARCHAR(256)
);
```

`hostname` 옵션을 지정하면 레코드 값보다 앞에 호스트 이름 컬럼을 하나 더 전송합니다.
이 경우 테이블의 첫 번째 사용자 컬럼을 호스트 이름 컬럼으로 둡니다.

```sql
CREATE TABLE apache_access_log (
    hostname VARCHAR(256),
    host     VARCHAR(64),
    remote_user VARCHAR(64),
    method   VARCHAR(16),
    path     VARCHAR(1024),
    code     INTEGER,
    size     LONG
);
```

## 플러그인 설정

주요 설정 키는 실제 플러그인 소스의 `config_param`에 정의되어 있습니다.

| 파라미터 | 설명 | 기본값 |
|----------|------|--------|
| `host` | Machbase 서버 호스트 | 없음 |
| `port` | Machbase TCP 포트 | `5656` |
| `uid` | 접속 사용자 | `SYS` |
| `pwd` | 접속 비밀번호 | `MANAGER` |
| `tablename` | Append 대상 테이블 | 없음 |
| `hostname` | 각 행 앞에 추가할 호스트 이름 값 | 없음 |
| `buffersize` | 플러그인 내부 전송 버퍼 크기 | `32` |
| `bufferflush` | 이벤트마다 즉시 전송할지 여부 | `false` |
| `arrivaltime` | Fluentd 이벤트 시간을 `_arrival_time`으로 사용할지 여부 | `false` |

## 버퍼(Buffer) 설정 가이드

플러그인 내부 버퍼 설정은 안정성과 처리량에 직접적인 영향을 줍니다.

| 파라미터 | 설명 | 권장값 |
|----------|------|--------|
| `buffersize` | 내부 버퍼 크기 | `64` 이상 |
| `bufferflush` | `true`이면 이벤트마다 즉시 전송 | 고처리량: `false` |
| `arrivaltime` | Fluentd 이벤트 시간을 `_arrival_time`으로 사용 | 로그 수집: `true` |

### 고처리량 환경 설정

초당 수만 건 이상의 이벤트를 처리해야 하는 경우:

```conf
<match app.log>
  type machbase
  host 127.0.0.1
  port 5656
  uid SYS
  pwd MANAGER
  tablename log_table

  buffer_queue_limit 64
  buffer_chunk_limit 8m
  flush_interval 2s

  buffersize 128
  bufferflush false
  arrivaltime true
</match>
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
SELECT * FROM log_table LIMIT 10;
```

## 문제 해결

| 증상 | 원인 | 해결 방법 |
|------|------|-----------|
| 연결 거부 | 포트 또는 방화벽 문제 | Machbase TCP 포트(5656) 개방 여부 확인 |
| 데이터 누락 | 테이블 컬럼 순서와 레코드 값 순서 불일치 | 입력 파서의 레코드 필드 순서와 테이블 컬럼 순서 확인 |
| 버퍼 overflow | 처리 속도 부족 | `flush_thread_count` 증가, 청크 크기 조정 |
| 타입 오류 | 컬럼 타입 불일치 | 테이블 컬럼 타입과 Fluentd 레코드 값 타입 확인 |
