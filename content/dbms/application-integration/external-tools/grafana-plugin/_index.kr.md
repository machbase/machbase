---
type: docs
title: 'Grafana plugin'
weight: 20
---

Grafana는 오픈소스 관측성 플랫폼으로, Machbase Neo 전용 데이터소스 플러그인을 통해 시계열 데이터를 실시간으로 시각화하고 대시보드를 구성할 수 있습니다.

## 사전 요구 사항

- Grafana 9.0 이상 (Grafana 10.x 권장)
- Machbase Neo 8.0 이상
- Machbase Neo HTTP 포트 접근 가능 (기본값: `5657`)

## 플러그인 설치

### 방법 1: Grafana CLI (권장)

```bash
grafana-cli plugins install machbase-neo-datasource
```

설치 후 Grafana를 재시작합니다.

```bash
# Linux (systemd)
sudo systemctl restart grafana-server

# macOS (Homebrew)
brew services restart grafana
```

### 방법 2: 수동 설치

1. [Grafana 플러그인 마켓플레이스](https://grafana.com/grafana/plugins/machbase-neo-datasource/)에서 플러그인 ZIP 파일을 내려받습니다.
2. 압축을 해제하여 Grafana 플러그인 디렉터리에 복사합니다.

```bash
unzip machbase-neo-datasource-*.zip -d /var/lib/grafana/plugins/
sudo systemctl restart grafana-server
```

### 서명되지 않은 플러그인 허용 (개발/테스트 환경)

`grafana.ini` 또는 환경 변수를 통해 서명 검사를 우회할 수 있습니다.

```ini
# /etc/grafana/grafana.ini
[plugins]
allow_loading_unsigned_plugins = machbase-neo-datasource
```

## 데이터소스 연결 설정

1. Grafana 사이드바에서 **Configuration → Data Sources** 로 이동합니다.
2. **Add data source** 를 클릭하고 `Machbase Neo` 를 검색하여 선택합니다.
3. 아래 항목을 입력합니다.

| 항목 | 값 | 설명 |
|------|----|------|
| **URL** | `http://MACHBASE_HOST:5657` | Machbase Neo HTTP 서버 주소 |
| **User** | `SYS` | 접속 계정 (기본값) |
| **Password** | `MANAGER` | 접속 비밀번호 (기본값) |

4. **Save & Test** 를 클릭하여 연결을 확인합니다.

> **주의**: Grafana가 도커 컨테이너에서 실행 중이고 Machbase가 호스트에서 실행 중이라면 `MACHBASE_HOST` 를 `host.docker.internal` (macOS/Windows) 또는 호스트 IP로 설정합니다.

## 패널 설정 및 쿼리 작성

### 시계열 패널 기본 구성

1. 대시보드에서 **Add panel → Time series** 를 선택합니다.
2. 데이터소스로 `Machbase Neo` 를 선택합니다.
3. 쿼리 편집기에 SQL을 입력합니다.

### SQL 쿼리 작성 팁

Machbase Neo는 Grafana의 시간 범위 변수(`$__timeFrom()`, `$__timeTo()`)를 지원합니다.

**기본 시계열 쿼리:**

```sql
SELECT
    time AS time,
    value
FROM sensor_data
WHERE name = 'temperature'
  AND time BETWEEN $__timeFrom() AND $__timeTo()
ORDER BY time ASC
```

**다중 센서 비교 쿼리:**

```sql
SELECT
    time AS time,
    name,
    value
FROM sensor_data
WHERE time BETWEEN $__timeFrom() AND $__timeTo()
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
WHERE time BETWEEN $__timeFrom() AND $__timeTo()
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

### 변수(Variable) 활용

대시보드 변수를 활용하면 동적으로 필터링할 수 있습니다.

1. **Dashboard Settings → Variables → Add variable** 로 이동합니다.
2. 다음과 같이 설정합니다.

| 항목 | 값 |
|------|----|
| **Type** | Query |
| **Data source** | Machbase Neo |
| **Query** | `SELECT DISTINCT name FROM sensor_data` |

3. 패널 쿼리에서 변수를 사용합니다.

```sql
SELECT time AS time, value
FROM sensor_data
WHERE name = '$sensor_name'
  AND time BETWEEN $__timeFrom() AND $__timeTo()
ORDER BY time ASC
```

## 권장 대시보드 구성

실시간 IoT 모니터링 대시보드의 권장 패널 구성입니다.

| 패널 | 타입 | 용도 |
|------|------|------|
| 실시간 센서값 | Time series | 다중 센서 시계열 추이 |
| 현재 최신값 | Stat | 각 센서의 최신 측정값 |
| 이상값 감지 | Alert list | 임계값 초과 알림 |
| 일별 평균 추이 | Bar chart | 일별 집계 비교 |
| 데이터 수신 현황 | Table | 센서별 마지막 수신 시각 |

## 알림(Alert) 설정

Grafana Alerting을 사용하여 임계값 초과 시 알림을 받을 수 있습니다.

1. 패널 편집 → **Alert** 탭으로 이동합니다.
2. **Create alert rule** 을 클릭합니다.
3. 조건을 설정합니다.

```sql
-- 온도가 80도를 초과할 때 알림
SELECT time AS time, value
FROM sensor_data
WHERE name = 'temperature'
  AND time BETWEEN $__timeFrom() AND $__timeTo()
ORDER BY time ASC
```

## 문제 해결

| 증상 | 원인 | 해결 방법 |
|------|------|-----------|
| `Data source connection failed` | URL 또는 포트 오류 | Machbase Neo HTTP 포트(5657) 접근 가능 여부 확인 |
| 데이터가 표시되지 않음 | 시간 범위 또는 쿼리 오류 | `time` 별칭과 시간 필터 조건 확인 |
| 플러그인이 목록에 없음 | 설치 또는 서명 오류 | `grafana.ini` 에서 unsigned plugin 허용 설정 확인 |
| 쿼리가 느림 | 인덱스 미사용 | TAG 테이블 사용, `name` 조건과 시간 범위 필터 명시 |
