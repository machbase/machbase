---
type: docs
title: '11.5 외부 도구 연동'
weight: 50
toc: true
---
Machbase Neo는 다양한 외부 도구와 연동하여 데이터 수집, 시각화, 분석 워크플로우를 구성할 수 있습니다. 현장에서 자주 쓰이는 외부 도구별 연동 방법을 다룹니다.


<a id="fluentd-plugin"></a>

## Fluentd plugin

Fluentd는 오픈소스 데이터 수집 미들웨어입니다. `fluent-plugin-machbase` 출력
플러그인으로 다양한 소스의 로그·이벤트 데이터를 Machbase로 스트리밍합니다.

### 사전 요구 사항

- Fluentd(td-agent) 0.10.54 호환 환경
- `machbase` Ruby gem
- Machbase TCP 포트 접근 가능 (기본값: `5656`)

### 플러그인 설치

#### 방법 1: gem으로 설치

```bash
gem install fluent-plugin-machbase
```

#### 방법 2: td-agent 환경에서 설치

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

### fluentd.conf 설정

#### 기본 설정 예시

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

#### Apache access log 예시

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

### 대상 테이블 생성

Fluentd에서 데이터를 받을 Machbase LOG 테이블을 미리 생성합니다. 플러그인은
Append 프로토콜을 사용하며 `<fields>` 매핑 블록을 지원하지 않습니다. Fluentd
레코드 값이 순서대로 테이블 컬럼에 들어가므로 입력 파서의 필드 순서와 테이블 컬럼
순서를 맞추어야 합니다.

#### LOG 테이블 (시계열 로그 데이터)

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

### 플러그인 설정

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

### 버퍼(Buffer) 설정 가이드

내부 버퍼 설정은 안정성과 처리량에 직접 영향을 줍니다.

| 파라미터 | 설명 | 권장값 |
|----------|------|--------|
| `buffersize` | 내부 버퍼 크기 | `64` 이상 |
| `bufferflush` | `true`이면 이벤트마다 즉시 전송 | 고처리량: `false` |
| `arrivaltime` | Fluentd 이벤트 시간을 `_arrival_time`으로 사용 | 로그 수집: `true` |

#### 고처리량 환경 설정

이벤트가 지속적으로 유입되고 flush 비용을 줄여야 하는 경우:

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

### 동작 확인

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

### 문제 해결

| 증상 | 원인 | 해결 방법 |
|------|------|-----------|
| 연결 거부 | 포트 또는 방화벽 문제 | Machbase TCP 포트(5656) 개방 여부 확인 |
| 데이터 누락 | 테이블 컬럼 순서와 레코드 값 순서 불일치 | 입력 파서의 레코드 필드 순서와 테이블 컬럼 순서 확인 |
| 버퍼 overflow | 처리 속도 부족 | `flush_thread_count` 증가, 청크 크기 조정 |
| 타입 오류 | 컬럼 타입 불일치 | 테이블 컬럼 타입과 Fluentd 레코드 값 타입 확인 |

<a id="grafana-plugin"></a>

## Grafana plugin

Grafana는 오픈소스 관측성 플랫폼입니다. Machbase 데이터소스 플러그인을 통해
MWA(Machbase Web Admin)의 Grafana용 REST 엔드포인트를 호출하여 시계열
데이터를 시각화합니다.

### 사전 요구 사항

- Grafana 4.5.x 호환 환경
- Machbase Web Admin(MWA) 실행
- MWA HTTP 포트 접근 가능 (기본값: `5001`)
- Machbase 배포 디렉터리의 Grafana 플러그인 패키지
  (`$MACHBASE_HOME/3rd-party/grafana/machbase.tgz`)

### 플러그인 설치

Machbase 배포 패키지에 포함된 플러그인을 Grafana 플러그인 디렉터리에 압축 해제합니다:

```bash
sudo mkdir -p /var/lib/grafana/plugins/machbase
sudo tar -xzf $MACHBASE_HOME/3rd-party/grafana/machbase.tgz \
    -C /var/lib/grafana/plugins/machbase
sudo systemctl restart grafana-server
```

#### 서명되지 않은 플러그인 허용 (개발/테스트 환경)

`grafana.ini` 또는 환경 변수를 통해 서명 검사를 우회할 수 있습니다.

```ini
# /etc/grafana/grafana.ini
[plugins]
allow_loading_unsigned_plugins = machbase
```

### 데이터소스 연결 설정

1. Grafana 사이드바에서 **Configuration → Data Sources** 로 이동합니다.
2. **Add data source** 를 클릭하고 `Machbase` 를 검색하여 선택합니다.
3. 아래 항목을 입력합니다.

| 항목 | 값 | 설명 |
|------|----|------|
| **URL** | `http://MWA_HOST:5001/machbase` | MWA의 Grafana REST 엔드포인트 |

4. **Save & Test** 를 클릭하여 연결을 확인합니다.

> **주의**: Grafana가 도커 컨테이너에서 실행 중이고 MWA가 호스트에서 실행 중이라면
> `MWA_HOST` 를 `host.docker.internal` (macOS/Windows) 또는 호스트 IP로 설정합니다.

### 패널 설정 및 쿼리 작성

#### 시계열 패널 기본 구성

1. 대시보드에서 **Add panel → Time series** 를 선택합니다.
2. 데이터소스로 `Machbase` 를 선택합니다.
3. 쿼리 편집기에 SQL을 입력합니다.

#### SQL 쿼리 작성 팁

쿼리 편집기에서 시간 범위 조건을 명시해 조회 범위를 제한합니다.

**기본 시계열 쿼리:**

```sql
SELECT
    time AS time,
    value
FROM sensor_data
WHERE name = 'temperature'
  AND time BETWEEN TO_DATE('2024-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
               AND TO_DATE('2024-01-02 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
ORDER BY time ASC
```

**다중 센서 비교 쿼리:**

```sql
SELECT
    time AS time,
    name,
    value
FROM sensor_data
WHERE time BETWEEN TO_DATE('2024-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
               AND TO_DATE('2024-01-02 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
ORDER BY time ASC
```

**집계 쿼리 (시간 버킷 사용):**

```sql
SELECT
    DATE_TRUNC('min', time, 1) AS time,
    name,
    AVG(value) AS avg_value,
    MAX(value) AS max_value,
    MIN(value) AS min_value
FROM sensor_data
WHERE time BETWEEN TO_DATE('2024-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
               AND TO_DATE('2024-01-02 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
GROUP BY time, name
ORDER BY time ASC
```

**최근 1시간 조회:**

```sql
SELECT time AS time, value
FROM sensor_data
WHERE name = 'pressure'
  AND time >= SYSDATE - 3600000000000
ORDER BY time ASC
```

> **time 컬럼 규칙**: Grafana 시계열 패널은 결과의 첫 번째 컬럼이 `time` 이라는 이름의 타임스탬프여야 합니다. TAG 테이블의 `DATETIME BASETIME` 컬럼은 `time AS time`처럼 그대로 별칭을 지정합니다.

#### 변수(Variable) 활용

대시보드 변수를 활용하면 동적으로 필터링할 수 있습니다.

1. **Dashboard Settings → Variables → Add variable** 로 이동합니다.
2. 다음과 같이 설정합니다.

| 항목 | 값 |
|------|----|
| **Type** | Query |
| **Data source** | Machbase |
| **Query** | `SELECT DISTINCT name FROM sensor_data` |

3. 패널 쿼리에서 변수를 사용합니다.

```sql
SELECT time AS time, value
FROM sensor_data
WHERE name = '$sensor_name'
  AND time BETWEEN TO_DATE('2024-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
               AND TO_DATE('2024-01-02 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
ORDER BY time ASC
```

### 권장 대시보드 구성

실시간 IoT 모니터링 대시보드의 권장 패널 구성입니다.

| 패널 | 타입 | 용도 |
|------|------|------|
| 실시간 센서값 | Time series | 다중 센서 시계열 추이 |
| 현재 최신값 | Stat | 각 센서의 최신 측정값 |
| 이상값 감지 | Alert list | 임계값 초과 알림 |
| 일별 평균 추이 | Bar chart | 일별 집계 비교 |
| 데이터 수신 현황 | Table | 센서별 마지막 수신 시각 |

### 알림(Alert) 설정

Grafana Alerting을 사용하여 임계값 초과 시 알림을 받을 수 있습니다.

1. 패널 편집 → **Alert** 탭으로 이동합니다.
2. **Create alert rule** 을 클릭합니다.
3. 조건을 설정합니다.

```sql
-- 온도가 80도를 초과할 때 알림
SELECT time AS time, value
FROM sensor_data
WHERE name = 'temperature'
  AND time BETWEEN TO_DATE('2024-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
               AND TO_DATE('2024-01-02 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
ORDER BY time ASC
```

### 문제 해결

| 증상 | 원인 | 해결 방법 |
|------|------|-----------|
| `Data source connection failed` | URL 또는 포트 오류 | MWA 포트(기본 5001)와 `/machbase` 경로 접근 가능 여부 확인 |
| 데이터가 표시되지 않음 | 시간 범위 또는 쿼리 오류 | `time` 별칭과 시간 필터 조건 확인 |
| 플러그인이 목록에 없음 | 설치 또는 서명 오류 | `grafana.ini` 에서 unsigned plugin 허용 설정 확인 |
| 쿼리가 느림 | 인덱스 미사용 | TAG 테이블 사용, `name` 조건과 시간 범위 필터 명시 |

<a id="tableau-connector"></a>

## Tableau connector

Tableau는 대표적인 BI 도구입니다. Machbase Neo 전용 Tableau Connector가 없는 경우 JDBC 또는 ODBC 드라이버로 연결합니다. 두 가지 연결 방법과 유의 사항을 다룹니다.

### 사전 요구 사항

- Tableau Desktop 2021.4 이상 또는 Tableau Server
- Machbase Neo 8.0 이상
- Machbase JDBC 드라이버 (`machbase.jar`) 또는 ODBC 드라이버
- Java Runtime Environment 11 이상 (JDBC 방식 사용 시)

### 방법 1: JDBC 드라이버 연결 (권장)

#### 1단계: JDBC 드라이버 설치

Machbase 설치 디렉터리의 `lib/machbase.jar` 파일을 사용합니다.

드라이버를 Tableau의 JDBC 드라이버 디렉터리에 복사합니다.

| 운영체제 | 경로 |
|----------|------|
| macOS | `~/Library/Tableau/Drivers/` |
| Windows | `C:\Program Files\Tableau\Drivers\` |
| Linux | `/opt/tableau/tableau_driver/jdbc/` |

```bash
# macOS 예시
cp $MACHBASE_HOME/lib/machbase.jar ~/Library/Tableau/Drivers/
```

#### 2단계: Tableau Desktop에서 연결

1. Tableau Desktop을 실행합니다.
2. 왼쪽 패널 **Connect** 섹션에서 **More...** 를 클릭합니다.
3. 검색창에 `JDBC` 를 입력하고 **Other Databases (JDBC)** 를 선택합니다.
4. 아래와 같이 연결 정보를 입력합니다.

| 항목 | 값 |
|------|----|
| **URL** | `jdbc:machbase://MACHBASE_HOST:5656/machbasedb` |
| **Dialect** | SQL92 |
| **Username** | `SYS` |
| **Password** | `MANAGER` |

5. **Sign In** 을 클릭합니다.

#### JDBC URL 형식

```
jdbc:machbase://<호스트>:<포트>/<데이터베이스>
```

**연결 옵션 예시:**

```
# 기본 연결
jdbc:machbase://127.0.0.1:5656/machbasedb

# AUTH KEY 인증 사용
jdbc:machbase://127.0.0.1:5656/machbasedb?AUTH_MODE=CHALLENGE&AUTH_SIG_SCHEME=ECDSA&AUTH_KEY_FILE=/opt/machbase/keys/app_user_ecdsa.pem

# 타임아웃 설정
jdbc:machbase://127.0.0.1:5656/machbasedb?CONNECTION_TIMEOUT=10&SOCKET_TIMEOUT=60
```

### 방법 2: ODBC 드라이버 연결

ODBC는 Windows 환경에서 주로 사용합니다.

#### 1단계: ODBC 드라이버 설치

Machbase Neo ODBC 드라이버를 설치하고 **ODBC 데이터 원본 관리자**에서 DSN을 구성합니다.

```
시작 → 검색 → "ODBC 데이터 원본 관리자 (64비트)"
→ 시스템 DSN → 추가 → Machbase ODBC Driver 선택
```

| DSN 항목 | 값 |
|----------|----|
| **Data Source Name** | `Machbase` |
| **Host** | `127.0.0.1` |
| **Port** | `5656` |
| **Database** | `machbasedb` |
| **UID** | `SYS` |
| **PWD** | `MANAGER` |

#### 2단계: Tableau에서 ODBC 연결

1. **Connect → More... → Other Databases (ODBC)** 를 선택합니다.
2. **DSN** 목록에서 앞서 만든 `Machbase` DSN을 선택합니다.
3. **Connect** 를 클릭합니다.

### 데이터 분석 설정

#### 테이블 선택 및 조인

연결 후 **Data Source** 탭에서 스키마를 탐색합니다.

- 왼쪽 패널에서 **Database** → **Schema** 를 선택합니다.
- 분석할 테이블을 캔버스로 드래그합니다.
- 필요에 따라 **Custom SQL** 탭에서 직접 SQL을 작성할 수 있습니다.

**Custom SQL 예시 (시계열 집계):**

```sql
SELECT
    DATE_TRUNC('hour', time, 1) AS hour_bucket,
    name AS sensor_name,
    AVG(value) AS avg_value,
    MAX(value) AS max_value,
    MIN(value) AS min_value,
    COUNT(*) AS sample_count
FROM sensor_data
WHERE time >= SYSDATE - 7 * 24 * 3600 * 1000000000
GROUP BY hour_bucket, sensor_name
ORDER BY hour_bucket ASC
```

#### 날짜/시간 필드 설정

`DATETIME` 타입은 Tableau에서 날짜 타입으로 바로 사용할 수 있습니다. TAG 테이블의 `DATETIME BASETIME` 컬럼은 그대로 조회하고, 나노초 BIGINT 컬럼을 별도로 저장한 경우에만 계산 필드에서 변환합니다.

### Tableau Server 배포

Tableau Server에서 Machbase 데이터를 사용하려면 서버 노드 각각에 드라이버를 설치합니다.

```bash
# Tableau Server (Linux)
sudo cp $MACHBASE_HOME/lib/machbase.jar /opt/tableau/tableau_driver/jdbc/

# 드라이버 적용을 위해 Tableau Server 재시작
tsm restart
```

#### Extract vs Live Connection

| 방식 | 설명 | 권장 상황 |
|------|------|-----------|
| **Live** | 쿼리마다 Machbase에 실시간 접속 | 최신 데이터 필요, 데이터량이 적을 때 |
| **Extract** | 데이터를 Tableau Hyper 파일로 추출·캐싱 | 대용량 데이터, 네트워크 부하 감소 필요 |

시계열 데이터의 특성상 **Live Connection** 사용 시 쿼리 성능을 위해 시간 필터를 반드시 적용하는 것을 권장합니다.

### 제한 사항

전용 Tableau Connector(`.taco` 파일)가 없으면 아래 제한이 있습니다.

| 항목 | 제한 내용 |
|------|-----------|
| **SQL 방언** | Tableau가 생성하는 SQL이 Machbase 문법과 다를 수 있음 |
| **함수 매핑** | 일부 Tableau 내장 함수가 Machbase에서 지원되지 않을 수 있음 |
| **데이터 타입** | BINARY 등 일부 타입이 Tableau에서 표시되지 않을 수 있음 |
| **Metadata** | 테이블·컬럼 자동 탐색이 일부 제한될 수 있음 |
| **초기 SQL** | 지원하나 Machbase 고유 문법 사용 권장 |

> **팁**: 제한을 우회하려면 **Custom SQL** 을 사용하거나, Machbase에서 뷰(View)를 미리 생성하여 Tableau에 노출합니다.

### 문제 해결

| 증상 | 원인 | 해결 방법 |
|------|------|-----------|
| 드라이버를 찾을 수 없음 | JAR 파일 경로 오류 | Tableau Drivers 디렉터리에 JAR 복사 후 재시작 |
| 연결 시간 초과 | 방화벽 또는 포트 차단 | 5656 포트 TCP 접근 허용 여부 확인 |
| SQL 오류 | Tableau 자동 생성 SQL 문법 문제 | Custom SQL 사용 또는 뷰 활용 |
| 데이터가 느리게 로드됨 | 인덱스 미사용 또는 전체 스캔 | 시간 범위 필터 추가, Extract 방식 고려 |
