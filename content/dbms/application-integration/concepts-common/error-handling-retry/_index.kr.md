---
type: docs
title: '오류 처리와 재시도'
weight: 70
---

애플리케이션의 안정성을 위해 연결 오류, 쿼리 오류, Append 실패를 각각 다르게 처리해야 합니다.

## 오류 유형별 분류

| 유형 | 대표 오류 | 재시도 가능 여부 |
|------|-----------|:---:|
| 연결 실패 | Connection refused, timeout | O |
| 인증 실패 | Wrong password, invalid key | X |
| 쿼리 오류 | Syntax error, column not found | X |
| 리소스 부족 | Out of memory, disk full | 상황에 따라 |
| 네트워크 단절 | Connection reset | O |
| Append flush 실패 | Network error during flush | O |

## 연결 오류와 재시도

연결 실패는 일시적인 네트워크 문제나 서버 재시작으로 발생할 수 있습니다. **지수 백오프(exponential backoff)** 전략으로 재시도합니다.

```python
import time
import machbaseapi

def connect_with_retry(host, port, user, password, max_attempts=5):
    delay = 1.0  # 초기 대기 시간 (초)
    for attempt in range(1, max_attempts + 1):
        try:
            conn = machbaseapi.connect(host, port, user, password)
            return conn
        except Exception as e:
            if attempt == max_attempts:
                raise
            print(f"연결 실패 (시도 {attempt}/{max_attempts}): {e}")
            time.sleep(delay)
            delay = min(delay * 2, 30)  # 최대 30초
    return None
```

```java
// Java JDBC 재시도 예제
int maxAttempts = 5;
long delay = 1000; // ms
for (int i = 1; i <= maxAttempts; i++) {
    try {
        conn = DriverManager.getConnection(url, props);
        break;
    } catch (SQLException e) {
        if (i == maxAttempts) throw e;
        Thread.sleep(delay);
        delay = Math.min(delay * 2, 30000);
    }
}
```

## 쿼리 오류 처리

쿼리 오류는 재시도해도 동일한 결과가 반복되므로, **오류 내용을 로그로 남기고 상위 레이어에 전파**합니다.

```python
cursor = conn.cursor()
try:
    cursor.execute("INSERT INTO sensor_log (name, time, value) VALUES (%s, %s, %s)",
                   ['sensor-01', time_ns, 23.5])
    conn.commit()
except Exception as e:
    # 오류 코드 확인 후 처리
    print(f"쿼리 오류: {e}")
    conn.rollback()  # RDB 테이블인 경우
    raise
finally:
    cursor.close()
```

## Append API 오류 처리

Append API는 버퍼에 누적 후 flush 시점에 오류가 발생합니다. flush 실패 시 재시도 또는 대체 INSERT로 전환합니다.

```python
try:
    appended = conn.append('SENSOR_LOG', data_batch)
    print(f"Append rows: {appended}")
except Exception as e:
    print(f"Append 오류: {e}")
    # flush 실패 시 누적된 데이터를 INSERT로 재시도
    fallback_insert(conn, data_batch)
```

```c
/* C/CLI Append 오류 처리 */
if (SQLAppendFlush(stmt) != SQL_SUCCESS) {
    char err_msg[1024];
    SQLError(env, conn, stmt, NULL, NULL, err_msg, sizeof(err_msg), NULL);
    fprintf(stderr, "Flush 오류: %s\n", err_msg);
    /* 재연결 후 재시도 */
    reconnect_and_retry();
}
```

## Connection Pool 사용 시 오류 격리

Connection pool을 사용할 때 오류가 발생한 연결은 pool에서 제거하고 새 연결로 교체합니다.

```java
// HikariCP 설정 예시
HikariConfig config = new HikariConfig();
config.setConnectionTimeout(5000);      // 연결 획득 대기 최대 5초
config.setValidationTimeout(2000);      // 연결 유효성 검사 최대 2초
config.setConnectionTestQuery("SELECT 1 FROM v$version"); // 연결 상태 확인
config.setMaximumPoolSize(10);
```

## 주의사항

- **TAG/LOG 테이블** INSERT/Append는 트랜잭션이 없으므로 부분 실패 가능성 고려
- **인증 실패**는 재시도 전에 자격 증명을 확인 (재시도 반복 시 계정 잠금 가능성)
- 재시도 횟수에 상한을 두고, 최종 실패 시 알림을 발송하는 구조 권장
