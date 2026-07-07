---
type: docs
title: 'Grafana plugin'
weight: 20
---

Grafana는 오픈소스 관측성 플랫폼으로, Machbase 데이터소스 플러그인을 통해
Machbase Web Admin(MWA)이 제공하는 Grafana용 REST 엔드포인트를 호출해 시계열
데이터를 시각화할 수 있습니다.

## 사전 요구 사항

- Grafana 4.5.x 호환 환경
- Machbase Web Admin(MWA) 실행
- MWA HTTP 포트 접근 가능 (기본값: `5001`)
- Machbase 배포 디렉터리의 Grafana 플러그인 패키지
  (`$MACHBASE_HOME/3rd-party/grafana/machbase.tgz`)

## 플러그인 설치

Machbase 배포 패키지에 포함된 플러그인을 Grafana 플러그인 디렉터리에 압축 해제합니다.

```bash
sudo mkdir -p /var/lib/grafana/plugins/machbase
sudo tar -xzf $MACHBASE_HOME/3rd-party/grafana/machbase.tgz \
    -C /var/lib/grafana/plugins/machbase
sudo systemctl restart grafana-server
```

### 서명되지 않은 플러그인 허용 (개발/테스트 환경)

`grafana.ini` 또는 환경 변수를 통해 서명 검사를 우회할 수 있습니다.

```ini
# /etc/grafana/grafana.ini
[plugins]
allow_loading_unsigned_plugins = machbase
```

## 데이터소스 연결 설정

1. Grafana 사이드바에서 **Configuration → Data Sources** 로 이동합니다.
2. **Add data source** 를 클릭하고 `Machbase` 를 검색하여 선택합니다.
3. 아래 항목을 입력합니다.

| 항목 | 값 | 설명 |
|------|----|------|
| **URL** | `http://MWA_HOST:5001/machbase` | MWA의 Grafana REST 엔드포인트 |

4. **Save & Test** 를 클릭하여 연결을 확인합니다.

> **주의**: Grafana가 도커 컨테이너에서 실행 중이고 MWA가 호스트에서 실행 중이라면
> `MWA_HOST` 를 `host.docker.internal` (macOS/Windows) 또는 호스트 IP로 설정합니다.

## 패널 설정 및 쿼리 작성

### 시계열 패널 기본 구성

1. 대시보드에서 **Add panel → Time series** 를 선택합니다.
2. 데이터소스로 `Machbase` 를 선택합니다.
3. 쿼리 편집기에 SQL을 입력합니다.

### SQL 쿼리 작성 팁

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

### 변수(Variable) 활용

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
  AND time BETWEEN TO_DATE('2024-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
               AND TO_DATE('2024-01-02 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
ORDER BY time ASC
```

## 문제 해결

| 증상 | 원인 | 해결 방법 |
|------|------|-----------|
| `Data source connection failed` | URL 또는 포트 오류 | MWA 포트(기본 5001)와 `/machbase` 경로 접근 가능 여부 확인 |
| 데이터가 표시되지 않음 | 시간 범위 또는 쿼리 오류 | `time` 별칭과 시간 필터 조건 확인 |
| 플러그인이 목록에 없음 | 설치 또는 서명 오류 | `grafana.ini` 에서 unsigned plugin 허용 설정 확인 |
| 쿼리가 느림 | 인덱스 미사용 | TAG 테이블 사용, `name` 조건과 시간 범위 필터 명시 |
