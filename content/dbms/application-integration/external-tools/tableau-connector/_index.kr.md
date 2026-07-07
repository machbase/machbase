---
type: docs
title: 'Tableau connector'
weight: 30
---

Tableau는 대표적인 비즈니스 인텔리전스(BI) 도구로, Machbase Neo 전용 Tableau Connector가 없는 경우 JDBC 또는 ODBC 드라이버를 통해 연결할 수 있습니다. 이 페이지에서는 두 가지 연결 방법과 유의 사항을 설명합니다.

## 사전 요구 사항

- Tableau Desktop 2021.4 이상 또는 Tableau Server
- Machbase Neo 8.0 이상
- Machbase JDBC 드라이버 (`machbase.jar`) 또는 ODBC 드라이버
- Java Runtime Environment 11 이상 (JDBC 방식 사용 시)

## 방법 1: JDBC 드라이버 연결 (권장)

### 1단계: JDBC 드라이버 설치

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

### 2단계: Tableau Desktop에서 연결

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

### JDBC URL 형식

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

## 방법 2: ODBC 드라이버 연결

ODBC는 Windows 환경에서 주로 사용합니다.

### 1단계: ODBC 드라이버 설치

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

### 2단계: Tableau에서 ODBC 연결

1. **Connect → More... → Other Databases (ODBC)** 를 선택합니다.
2. **DSN** 목록에서 앞서 만든 `Machbase` DSN을 선택합니다.
3. **Connect** 를 클릭합니다.

## 데이터 분석 설정

### 테이블 선택 및 조인

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

### 날짜/시간 필드 설정

Machbase의 `DATETIME` 타입은 Tableau에서 날짜 타입으로 사용할 수 있습니다. TAG 테이블의 `DATETIME BASETIME` 컬럼은 그대로 조회하고, 나노초 BIGINT 컬럼을 별도로 저장한 경우에만 애플리케이션 또는 계산 필드에서 변환합니다.

## Tableau Server 배포

Tableau Server에서 Machbase 데이터를 사용하려면 서버 노드 각각에 드라이버를 설치해야 합니다.

```bash
# Tableau Server (Linux)
sudo cp $MACHBASE_HOME/lib/machbase.jar /opt/tableau/tableau_driver/jdbc/

# 드라이버 적용을 위해 Tableau Server 재시작
tsm restart
```

### Extract vs Live Connection

| 방식 | 설명 | 권장 상황 |
|------|------|-----------|
| **Live** | 쿼리마다 Machbase에 실시간 접속 | 최신 데이터 필요, 데이터량이 적을 때 |
| **Extract** | 데이터를 Tableau Hyper 파일로 추출·캐싱 | 대용량 데이터, 네트워크 부하 감소 필요 |

시계열 데이터의 특성상 **Live Connection** 사용 시 쿼리 성능을 위해 시간 필터를 반드시 적용하는 것을 권장합니다.

## 제한 사항

Machbase Neo 전용 Tableau Connector(`.taco` 파일)가 없는 경우 아래와 같은 제한이 있습니다.

| 항목 | 제한 내용 |
|------|-----------|
| **SQL 방언** | Tableau가 생성하는 SQL이 Machbase 문법과 다를 수 있음 |
| **함수 매핑** | 일부 Tableau 내장 함수가 Machbase에서 지원되지 않을 수 있음 |
| **데이터 타입** | BINARY 등 일부 타입이 Tableau에서 표시되지 않을 수 있음 |
| **Metadata** | 테이블·컬럼 자동 탐색이 일부 제한될 수 있음 |
| **초기 SQL** | 지원하나 Machbase 고유 문법 사용 권장 |

> **팁**: 제한을 우회하려면 **Custom SQL** 을 사용하거나, Machbase에서 뷰(View)를 미리 생성하여 Tableau에 노출합니다.

## 문제 해결

| 증상 | 원인 | 해결 방법 |
|------|------|-----------|
| 드라이버를 찾을 수 없음 | JAR 파일 경로 오류 | Tableau Drivers 디렉터리에 JAR 복사 후 재시작 |
| 연결 시간 초과 | 방화벽 또는 포트 차단 | 5656 포트 TCP 접근 허용 여부 확인 |
| SQL 오류 | Tableau 자동 생성 SQL 문법 문제 | Custom SQL 사용 또는 뷰 활용 |
| 데이터가 느리게 로드됨 | 인덱스 미사용 또는 전체 스캔 | 시간 범위 필터 추가, Extract 방식 고려 |
