---
type: docs
title: 'Batch 입력'
weight: 10
---

대량 데이터를 효율적으로 입력하기 위한 배치 전략을 정리합니다.

## 배치 크기 선택

| 방법 | 권장 배치 크기 | 설명 |
|------|--------------|------|
| SQL INSERT (개별) | N/A | 건별 처리 |
| Append API | 10,000~100,000건 버퍼 | 내부 버퍼 자동 관리 |
| LOAD DATA INFILE | 제한 없음 | 파일 단위 처리 |
| machloader | 제한 없음 | 파일 단위 처리 |

## Append API 배치 전략

Append API는 내부 버퍼에 데이터를 누적하다가 `Close()` 시 일괄 전송합니다.

```go
// Go SDK: 100만 건 배치 입력
appender, _ := conn.AppendContext(ctx, "sensor_log")
for i := 0; i < 1_000_000; i++ {
    appender.Append("TEMP-01", time.Now(), float64(i)*0.01)
}
// Close()에서 서버로 일괄 전송
success, fail, _ := appender.Close()
```

### 멀티 Appender 병렬 입력

여러 goroutine/thread에서 각각 별도의 Appender를 사용하여 병렬 입력합니다.

```go
var wg sync.WaitGroup
for workerID := 0; workerID < 4; workerID++ {
    wg.Add(1)
    go func(id int) {
        defer wg.Done()
        appender, _ := conn.AppendContext(ctx, "sensor_log")
        for i := 0; i < 250_000; i++ {
            appender.Append(fmt.Sprintf("TEMP-%02d", id), time.Now(), float64(i))
        }
        appender.Close()
    }(workerID)
}
wg.Wait()
```

## SQL INSERT 배치 전략

SQL INSERT는 행 단위로 실행합니다. 대량 입력에는 Append API나 파일 적재 방식을 사용합니다.

```sql
CREATE VOLATILE TABLE batch_orders (
    order_id INTEGER PRIMARY KEY,
    product  VARCHAR(64),
    qty      INTEGER
);

INSERT INTO batch_orders VALUES (1, 'Widget', 10);
INSERT INTO batch_orders VALUES (2, 'Gadget', 5);
INSERT INTO batch_orders VALUES (3, 'Doohickey', 20);
```

## machloader 배치 파일 분할

매우 큰 CSV 파일은 여러 파일로 분할하여 병렬 실행합니다.

```bash
# 파일 분할 (Linux)
split -l 1000000 large_data.csv chunk_

# 병렬 machloader 실행
for f in chunk_*; do
    machloader -i -d "$f" -t sensor_log -I &
done
wait
```

## 시간대별 분할 로드

시계열 데이터는 시간 범위별로 분할하여 순서대로 적재하면 효율적입니다.

```bash
# 월별 파일 순서대로 적재
for month in 2024-01 2024-02 2024-03; do
    machloader -i -d "sensor_${month}.csv" -t sensor_log
done
```
