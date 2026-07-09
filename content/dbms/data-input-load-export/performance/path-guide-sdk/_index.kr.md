---
type: docs
title: 'SDK 입력 경로 안내'
weight: 30
---

Machbase SDK(Go, Python, C 등)를 사용하면 애플리케이션에서 직접 고속으로 데이터를 입력할 수 있습니다.

## SDK 입력 방식

### Append API (고속 대량 입력)

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

### SQL INSERT (소량·범용)

소량 입력, 행 단위 오류 확인, 명시적 트랜잭션이 필요한 작업에는 SQL INSERT를 사용합니다. RDB 대량 입력은 지원되는 client API의 appendBatch 또는 append stream 경로를 사용할 수 있습니다.

```go
// Go SDK SQL INSERT
db.ExecContext(ctx, "INSERT INTO orders VALUES (?, ?, ?)",
    1001, "Widget", 10)
```

## SDK 선택 기준

| SDK | 주요 사용 환경 |
|-----|-------------|
| Go | 고성능 서버, 마이크로서비스 |
| Python | 데이터 분석, 스크립트 자동화 |
| C/C++ | 임베디드, 하드웨어 통합 |
| JDBC | Java 애플리케이션, Spring Boot |
| ODBC | C/C++ 범용, 다양한 언어 바인딩 |

## 상세 문서

SDK 설치, 연결 설정, Append API 사용법, 샘플 코드는 다음 문서를 참고하세요.

> **[8장 애플리케이션 연동 → SDK](/dbms/application-integration/)** 에서 상세 내용을 다룹니다.
