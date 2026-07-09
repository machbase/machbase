---
type: docs
title: 'Append API'
weight: 20
---

Append API는 Machbase SDK가 제공하는 대량 입력 인터페이스입니다. SQL INSERT와 달리 내부 버퍼에 데이터를 모아 배치 전송하므로, TAG/LOG 테이블의 시계열 데이터 입력에서 높은 처리량을 달성할 수 있습니다.

## Append API 특징

- **고속 입력 경로**: TAG/LOG 테이블에서 비트랜잭션 버퍼 기반으로 동작
- **버퍼 기반**: 내부 버퍼에 데이터를 누적하다가 `Close()` 또는 버퍼 플러시 시 서버로 전송
- **테이블 타입**: TAG, LOG, VOLATILE, LOOKUP에서 사용 가능. RDB는 지원되는 client API의 appendBatch 또는 append stream 경로로 사용
- **열 순서 고정**: 테이블 컬럼 순서대로 값을 전달

## Go SDK 예시

```go
package main

import (
    "context"
    "database/sql"
    _ "github.com/machbase/neo-client/driver"
)

func main() {
    db, _ := sql.Open("machbase", "server=127.0.0.1;port=5656;user=SYS;password=MANAGER")
    conn, _ := db.Conn(context.Background())
    defer conn.Close()

    // Appender 생성
    appender, err := conn.AppendContext(context.Background(), "sensor_log")
    if err != nil {
        panic(err)
    }

    // 대량 데이터 입력
    for i := 0; i < 1_000_000; i++ {
        appender.Append("TEMP-01", time.Now(), float64(i)*0.01)
    }

    // 버퍼 플러시 및 완료
    successCount, failCount, err := appender.Close()
    // successCount: 성공 건수, failCount: 실패 건수
}
```

## Python SDK 예시

```python
import machbasedb

conn = machbasedb.connect(host="127.0.0.1", port=5656, user="SYS", password="MANAGER")

with conn.appender("sensor_log") as app:
    for i in range(1_000_000):
        app.append("TEMP-01", time.time_ns(), i * 0.01)
# with 블록 종료 시 자동 Close (플러시)
```

## C SDK 예시 (개념)

```c
// Appender 열기
MCH_APPENDER *appender;
MCHOpenAppender(hEnv, hConn, "sensor_log", &appender);

// 데이터 추가
MCHAppendData(appender, "TEMP-01", timestamp_ns, 25.3);

// 완료
MCHCloseAppender(appender, &successCnt, &failCnt);
```

## Append API vs SQL INSERT 비교

| 항목 | Append API | SQL INSERT |
|------|-----------|-----------|
| 처리량 | TAG/LOG에서 수백만 건/초 수준 | 수천~수만 건/초 |
| 트랜잭션 | TAG/LOG는 비트랜잭션, RDB는 batch 실행 구간에서 트랜잭션 처리 | O |
| 오류 처리 | 실패 행 건너뜀 | 행별 오류 반환 |
| 사용 테이블 | TAG, LOG, VOLATILE, LOOKUP, RDB(client append API) | 모든 테이블 |
| 사용 방법 | SDK 필요 | SQL 클라이언트 |

## REST API Append

REST API를 통한 Append도 동일한 고속 경로를 사용합니다. 상세는 [8장 애플리케이션 연동](/dbms/application-integration/)을 참고하세요.

## 주의사항

- `Close()` 를 반드시 호출해야 내부 버퍼가 플러시됩니다. 호출하지 않으면 데이터 유실이 발생합니다.
- 대량 Append 중 서버 재시작 등의 이유로 연결이 끊기면 버퍼에 남은 데이터는 손실될 수 있습니다.
- RDB 테이블에는 일반 SQL `APPEND INTO` 문법을 사용하지 않습니다. RDB 대량 입력은 지원되는 client API의 appendBatch 또는 append stream 경로를 사용합니다.
