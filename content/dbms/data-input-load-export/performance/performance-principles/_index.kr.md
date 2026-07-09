---
type: docs
title: '입력 성능 기본 원칙'
weight: 10
---

Machbase 데이터 입력 성능을 극대화하기 위한 핵심 원칙을 정리합니다.

## 1. Append API 우선

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

## 2. TAG 테이블은 파티션 분산

TAG 테이블의 `TAG_PARTITION_COUNT` 속성을 서버 CPU 코어 수에 맞게 설정합니다.

```sql
CREATE TAG TABLE sensor_data (
    name  VARCHAR(20) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE SUMMARIZED
) TAG_PARTITION_COUNT = 8;  -- CPU 코어 수 기준
```

## 3. 병렬 입력

단일 연결의 한계를 넘으려면 복수의 클라이언트 또는 goroutine/thread로 병렬 입력합니다.

```bash
# machloader 병렬 실행 (파일 분할)
machloader -i -d part1.csv -t sensor_log -I &
machloader -i -d part2.csv -t sensor_log -I &
machloader -i -d part3.csv -t sensor_log -I &
wait
```

## 4. 배치 크기 최적화

- **Append API**: TAG/LOG 입력에서 너무 자주 Close()를 호출하면 처리량 감소. 최소 10,000건 이상 누적 후 Close 권장
- **SQL INSERT**: 다건 삽입으로 왕복 횟수 최소화

## 5. 네트워크 지연 최소화

- 서버와 클라이언트의 네트워크 지연(RTT)이 낮을수록 처리량 향상
- 가능하면 서버와 같은 네트워크 세그먼트에 클라이언트 배치
- 서버 측 직접 적재(`LOAD DATA INFILE`)는 네트워크 영향 없음

## 6. 인덱스 설계

- 불필요한 인덱스는 삭제. 인덱스 수가 많을수록 INSERT 성능 저하
- LOG 테이블에 과도한 BITMAP 인덱스는 입력 성능에 영향

## 7. 시계열 순서

TAG/LOG 테이블에 **과거→현재 순서**로 데이터를 입력하면 파티션 효율이 높아집니다. 역순 입력은 추가 처리를 유발합니다.

## 성능 점검 쿼리

```sql
-- 테이블 현재 행 수 빠른 확인
SELECT COUNT(*) FROM sensor_log;

-- 인덱스 수 확인
SELECT COUNT(*) FROM M$SYS_INDEXES WHERE TABLE_NAME = 'SENSOR_LOG';
```
