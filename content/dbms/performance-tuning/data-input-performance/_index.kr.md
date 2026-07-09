---
type: docs
title: '12.8 입력 성능과 연동 경로'
weight: 70
---
데이터 입력 경로별 성능 특성과 선택 기준을 정리합니다.

## 입력 경로별 성능 비교

| 입력 경로 | 최대 처리량 | 지연 | 주요 특징 |
|----------|-----------|------|---------|
| SDK Append API | TAG/LOG에서 수백만 건/초 | 최소 | 내부 Append 버퍼. RDB는 client appendBatch/stream 경로 |
| REST API (JSON) | 수만~수십만 건/초 | 낮음 | HTTP 오버헤드, 범용성 |
| machloader | 수십만~수백만 건/초 | 파일 기반 | 배치 적재, 병렬 실행 가능 |
| LOAD DATA INFILE | 수십만~수백만 건/초 | 파일 기반 | 서버 직접 읽기, 네트워크 무관 |
| SQL INSERT | 수천~수만 건/초 | 트랜잭션 포함 | 단건/소량, 모든 테이블 타입 |

## 이 절에서 다루는 내용

- **[입력 성능 기본 원칙](/dbms/performance-tuning/data-input-performance/#performance-principles)**: 처리량을 높이는 핵심 원칙
- **[REST 입력 경로 안내](/dbms/performance-tuning/data-input-performance/#path-guide-rest)**: REST API 연동 개요 (상세는 8장)
- **[SDK 입력 경로 안내](/dbms/performance-tuning/data-input-performance/#path-guide-sdk)**: SDK Append/INSERT 개요 (상세는 8장)
- **[Fluentd 파이프라인](/dbms/performance-tuning/data-input-performance/#pipeline-fluentd)**: Fluentd 기반 파이프라인 개요 (상세는 8장)


<a id="performance-principles"></a>

## 입력 성능 기본 원칙

Machbase 데이터 입력 성능을 극대화하기 위한 핵심 원칙을 정리합니다.

### 1. Append API 우선

TAG/LOG 테이블의 대량 입력에는 SQL INSERT 대신 **Append API**를 사용합니다.

- Append API: 내부 버퍼 → 배치 전송 → 수백만 건/초
- SQL INSERT: 건별 처리 → 수천~수만 건/초

```go
// Append API 사용
appender, _ := conn.AppendContext(ctx, "sensor_log")
for _, row := range rows {
    appender.Append(row.Name, row.Time, row.Value)
}
appender.Close()
```

### 2. TAG 테이블은 파티션 분산

TAG 테이블의 `TAG_PARTITION_COUNT` 속성을 서버 CPU 코어 수에 맞게 설정합니다.

```sql
CREATE TAG TABLE sensor_data (
    name  VARCHAR(20) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE SUMMARIZED
) TAG_PARTITION_COUNT = 8;  -- CPU 코어 수 기준
```

### 3. 병렬 입력

단일 연결의 한계를 넘으려면 복수의 클라이언트 또는 goroutine/thread로 병렬 입력합니다.

```bash
# machloader 병렬 실행 (파일 분할)
machloader -i -d part1.csv -t sensor_log -I &
machloader -i -d part2.csv -t sensor_log -I &
machloader -i -d part3.csv -t sensor_log -I &
wait
```

### 4. 배치 크기 최적화

- **Append API**: TAG/LOG 입력에서 너무 자주 Close()를 호출하면 처리량 감소. 최소 10,000건 이상 누적 후 Close 권장
- **SQL INSERT**: 다건 삽입으로 왕복 횟수 최소화

### 5. 네트워크 지연 최소화

- 서버와 클라이언트의 네트워크 지연(RTT)이 낮을수록 처리량 향상
- 가능하면 서버와 같은 네트워크 세그먼트에 클라이언트 배치
- 서버 측 직접 적재(`LOAD DATA INFILE`)는 네트워크 영향 없음

### 6. 인덱스 설계

- 불필요한 인덱스는 삭제. 인덱스 수가 많을수록 INSERT 성능 저하
- LOG 테이블에 과도한 BITMAP 인덱스는 입력 성능에 영향

### 7. 시계열 순서

TAG/LOG 테이블에 **과거→현재 순서**로 데이터를 입력하면 파티션 효율이 높아집니다. 역순 입력은 추가 처리를 유발합니다.

### 성능 점검 쿼리

```sql
-- 테이블 현재 행 수 빠른 확인
SELECT COUNT(*) FROM sensor_log;

-- 인덱스 수 확인
SELECT COUNT(*) FROM M$SYS_INDEXES WHERE TABLE_NAME = 'SENSOR_LOG';
```

<a id="path-guide-rest"></a>

## REST 입력 경로 안내

Machbase는 HTTP REST API를 통해 외부 시스템이나 IoT 디바이스에서 직접 데이터를 입력할 수 있습니다.

### REST API 입력 개요

REST API는 HTTP JSON 기반으로 동작합니다. SDK나 별도 드라이버 없이 `curl` 등 표준 HTTP 클라이언트로 연동할 수 있어 범용성이 높습니다.

```bash
# REST API로 데이터 삽입 예시
curl -X POST http://127.0.0.1:5657/machbase \
    -H "Content-Type: application/json" \
    -d '{"name":"sensor_log","date_format":"YYYY-MM-DD HH24:MI:SS","values":[["TEMP-01","2024-01-15 10:00:00",25.3]]}'
```

### 성능 특성

- SQL INSERT 대비 빠르나, SDK Append API보다는 낮은 처리량
- HTTP 오버헤드가 있으므로 초당 수십만 건 이하의 적재에 적합
- 배치(bulk) 전송으로 처리량 향상 가능

### 주요 사용 사례

- IoT 디바이스, 센서 게이트웨이
- 외부 시스템과의 HTTP 기반 연동
- 언어·플랫폼 무관 데이터 수집

### 상세 문서

REST API의 인증, 엔드포인트, 요청/응답 형식, 배치 전송 방법은 다음 문서를 참고하세요.

> **[8장 애플리케이션 연동 → REST API](/dbms/application-integration/)** 에서 상세 내용을 다룹니다.

<a id="path-guide-sdk"></a>

## SDK 입력 경로 안내

Machbase SDK(Go, Python, C 등)를 사용하면 애플리케이션에서 직접 고속으로 데이터를 입력할 수 있습니다.

### SDK 입력 방식

#### Append API (고속 대량 입력)

Append API는 TAG/LOG 테이블에서 비트랜잭션 버퍼 기반으로 높은 처리량을 달성합니다. 시계열 데이터 수집에 최적입니다.

```go
// Go SDK Append API
appender, _ := conn.AppendContext(ctx, "sensor_log")
for _, row := range rows {
    appender.Append(row.Name, row.Time, row.Value)
}
appender.Close()
```

```python
# Python SDK Append API
with conn.appender("sensor_log") as app:
    for row in rows:
        app.append(row.name, row.time, row.value)
```

#### SQL INSERT (소량·범용)

소량 입력, 행 단위 오류 확인, 명시적 트랜잭션이 필요한 작업에는 SQL INSERT를 사용합니다. RDB 대량 입력은 지원되는 client API의 appendBatch 또는 append stream 경로를 사용할 수 있습니다.

```go
// Go SDK SQL INSERT
db.ExecContext(ctx, "INSERT INTO orders VALUES (?, ?, ?)",
    1001, "Widget", 10)
```

### SDK 선택 기준

| SDK | 주요 사용 환경 |
|-----|-------------|
| Go | 고성능 서버, 마이크로서비스 |
| Python | 데이터 분석, 스크립트 자동화 |
| C/C++ | 임베디드, 하드웨어 통합 |
| JDBC | Java 애플리케이션, Spring Boot |
| ODBC | C/C++ 범용, 다양한 언어 바인딩 |

### 상세 문서

SDK 설치, 연결 설정, Append API 사용법, 샘플 코드는 다음 문서를 참고하세요.

> **[8장 애플리케이션 연동 → SDK](/dbms/application-integration/)** 에서 상세 내용을 다룹니다.
