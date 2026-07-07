---
type: docs
title: 'Append API와 Batch API'
weight: 60
---

Machbase에 데이터를 입력하는 방법은 크게 세 가지입니다. 각 방법의 특성과 적합한 사용 상황을 설명합니다.

## 세 가지 입력 방법 비교

| 방법 | 트랜잭션 | 처리 방식 | 권장 사용량 |
|------|----------|-----------|-------------|
| **단건 INSERT** | 지원 (RDB) | 행 단위 즉시 처리 | 건별 처리, 낮은 빈도 |
| **Batch INSERT** | 지원 (RDB) | 여러 행을 한 번에 전송 | 수십~수백 건 묶음 처리 |
| **Append API** | 미지원 | 버퍼 누적 후 flush | 초당 수천~수십만 건 |

## Append API

### 동작 원리

Append API는 행을 즉시 서버로 전송하지 않고 클라이언트 버퍼에 누적합니다. 버퍼가 가득 차거나 명시적으로 `flush`를 호출하면 누적된 데이터를 한 번에 서버로 전송합니다.

```
애플리케이션
  ↓ AppendData() × N 번 호출 (버퍼에 누적)
클라이언트 버퍼
  ↓ flush (자동 또는 수동)
Machbase 서버 (버퍼 전체를 한 번에 저장)
```

이 방식은 네트워크 왕복 횟수를 대폭 줄여 일반 INSERT 대비 수십 배의 쓰기 처리량을 제공합니다.

### 주요 특성

- **비트랜잭션**: TAG/LOG 테이블에서만 사용합니다. RDB 테이블의 Append는 지원하지 않습니다.
- **순서 보장 없음**: flush 단위 내에서 행 삽입 순서는 보장되지 않습니다.
- **자동 flush**: 내부 버퍼가 일정 크기에 도달하면 자동으로 flush됩니다. 드라이버마다 기본 버퍼 크기가 다릅니다.
- **명시적 flush 권장**: 애플리케이션 종료 전, 또는 일정 주기마다 반드시 명시적으로 flush를 호출하세요.

### SDK별 Append API 지원 현황

| SDK | 지원 여부 | 비고 |
|-----|-----------|------|
| CLI/ODBC | O | `SQLAppendOpen`, `SQLAppendData`, `SQLAppendFlush` |
| JDBC | O | `appendOpen`, `appendData`, `appendFlush` |
| Python SDK | O | `conn.append(table, rows)` |
| .NET (MachClient) | O | `MachAppendCommand` |
| Go 드라이버 | O | `Appender` 인터페이스 |
| Node.js 드라이버 | - | REST API를 통한 bulk insert로 대체 |
| REST API | - | 단건 또는 배열 형태의 bulk insert |

상세 API는 14장 레퍼런스의 각 드라이버 문서를 참조하세요.

### 언제 Append API를 써야 하는가

아래 조건 중 하나라도 해당하면 Append API를 사용하세요.

- 초당 1,000건 이상의 데이터를 입력해야 하는 경우
- 센서, 장비, IoT 디바이스에서 연속적으로 데이터가 수집되는 경우
- 쓰기 성능이 병목이 되어 애플리케이션 전체 처리량이 저하되는 경우

반대로 다음 경우에는 일반 INSERT를 사용하세요.

- 입력 빈도가 낮고 (초당 수십 건 이하) 데이터 무결성이 중요한 경우
- RDB 테이블에 데이터를 저장하고 rollback이 필요한 경우
- 에러 발생 시 어느 행에서 실패했는지 정확히 추적해야 하는 경우

### Append API 사용 예 (Python)

```python
from machbaseAPI import connect

conn = connect(host='127.0.0.1', port=5656, user='SYS', password='MANAGER')

# rows: 각 요소가 테이블 컬럼 순서에 맞는 리스트
rows = [
    ['sensor_01', 1720000000000000000, 23.5],
    ['sensor_01', 1720000001000000000, 23.7],
    ['sensor_02', 1720000000000000000, 18.2],
]

# append() 호출 시 즉시 flush
conn.append('tag_table', rows)
conn.close()
```

### Append API 사용 예 (Java)

```java
import com.machbase.jdbc.MachConnection;
import com.machbase.jdbc.MachAppendWriter;

MachConnection conn = (MachConnection) DriverManager.getConnection(url, "SYS", "MANAGER");

// Append 세션 열기
MachAppendWriter writer = conn.appendOpen("tag_table");

// 행 단위로 버퍼에 추가
Object[] row = {"sensor_01", 1720000000000000000L, 23.5};
writer.append(row);

// 명시적 flush
writer.flush();

// Append 세션 닫기 (내부적으로 flush 포함)
writer.close();
conn.close();
```

## Batch INSERT

### 동작 원리

Batch INSERT는 Prepared statement를 활용해 여러 행의 파라미터를 한 번의 네트워크 요청으로 전송합니다. 트랜잭션 내에서 동작하므로 전체 성공 또는 전체 실패가 보장됩니다.

### 언제 Batch INSERT를 사용하는가

- RDB 테이블에 여러 행을 원자적으로 삽입해야 할 때
- 데이터 마이그레이션 또는 ETL 처리에서 수십~수백 건을 묶어 처리할 때
- 실패 시 rollback이 필요한 경우

### Batch INSERT 사용 예 (Java)

```java
conn.setAutoCommit(false);

String sql = "INSERT INTO rdb_table (id, value, ts) VALUES (?, ?, ?)";
PreparedStatement pstmt = conn.prepareStatement(sql);

for (DataRow row : dataList) {
    pstmt.setString(1, row.getId());
    pstmt.setDouble(2, row.getValue());
    pstmt.setTimestamp(3, row.getTimestamp());
    pstmt.addBatch();  // 배치에 추가
}

pstmt.executeBatch();  // 한 번에 전송
conn.commit();

pstmt.close();
```

### Batch INSERT 사용 예 (Python)

```python
conn = connect(host='127.0.0.1', port=5656, user='SYS', password='MANAGER')
cur = conn.cursor()

sql = "INSERT INTO rdb_table (id, value, ts) VALUES (?, ?, ?)"

rows = [
    ('sensor_01', 23.5, 1720000000000000000),
    ('sensor_02', 18.2, 1720000001000000000),
]

cur.executemany(sql, rows)  # 배치로 실행
conn.commit()
cur.close()
conn.close()
```

## 요약: 입력 방법 선택 기준

```
초당 1,000건 이상 or TAG/LOG 테이블 대량 입력
  → Append API

트랜잭션 필요 or RDB 테이블 or 수십~수백 건 묶음
  → Batch INSERT (executemany / addBatch)

단건, 낮은 빈도, 간단한 작업
  → 단건 INSERT
```
