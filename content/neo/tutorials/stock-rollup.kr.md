---
title: Go 앱에서 롤업 조회 구성하기
type: docs
weight: 301
toc: true
---

이 튜토리얼은 Go 애플리케이션에서 주식 tick 데이터를 수집하고, Machbase custom rollup 기능으로
1분/1시간 집계 데이터를 자동 생성한 뒤, 특정 종목 코드의 원하는 기간 데이터를 빠르게 조회하는 방법을 설명합니다.

핵심은 과거 구간은 rollup 테이블을 사용하고, 최근 2분은 raw 테이블을 사용해 조회 부하를 줄이는 것입니다.

## 구성 목표

- `stock` 사용자와 주식 데이터용 테이블 구성
- `stock_tick` → `stock_rollup_1m` (1분 rollup)
- `stock_rollup_1m` → `stock_rollup_1h` (1시간 rollup)
- 2시간 범위, 분당 약 30건 데이터를 적재하는 Go 예제
- rollup + raw 데이터를 결합 조회하는 Go 예제

## 사전 준비

- Machbase Neo 실행 중
- Go 1.24+
- 초기 사용자 생성을 위한 `sys` 계정 접근 권한
- Machbase Go SDK 기본 사용법은 [MachGo SDK](/kr/neo/sdk-go/machgo/) 참고

## 1) `sys` 계정으로 `stock` 사용자 생성

먼저 `sys` 계정으로 아래 SQL을 실행합니다.

```sql
-- 주식 데이터 적재/조회 애플리케이션 전용 계정을 생성합니다.
create user stock identified by stock;
```

이후 테이블 생성, rollup 생성, 애플리케이션 실행은 모두 `stock/stock` 계정을 사용합니다.

## 2) 테이블 생성

`stock` 사용자로 접속한 뒤 raw 테이블과 rollup 대상 테이블을 생성합니다.

```sql
-- 원본 tick 테이블: 종목별 체결 이벤트를 시각 기준으로 저장합니다.
create tag table if not exists stock_tick (
    code      varchar(20) primary key,
    time      datetime basetime,
    price     double,
    volume    double,
    bid_price double,
    ask_price double
);

-- 1초 rollup 대상 테이블: stock_tick에서 집계한 합계(sum)와 건수(cnt)를 저장합니다.
-- 조회 시 평균은 sum/cnt로 계산하여 원본 전체 스캔을 줄입니다.
create tag table if not exists stock_rollup_1s (
    code      varchar(20) primary key,
    time      datetime basetime,
    sum_price double,
    sum_volume double,
    sum_bid   double,
    sum_ask   double,
    cnt       integer
);

-- 1분 rollup 대상 테이블: 1초 rollup 결과를 다시 분 단위로 재집계합니다.
-- 분사이에 많은 데이터가 발생하는 경우에 조회에서 CPU/IO 부하를 낮추기 위한 다단계 집계 구조입니다.
create tag table if not exists stock_rollup_1m (
    code      varchar(20) primary key,
    time      datetime basetime,
    sum_price double,
    sum_volume double,
    sum_bid   double,
    sum_ask   double,
    cnt       integer
);

-- 1시간 rollup 대상 테이블: 1분 rollup 결과를 다시 시간 단위로 재집계합니다.
-- 장기간 조회에서 CPU/I/O 부하를 낮추기 위한 다단계 집계 구조입니다.
create tag table if not exists stock_rollup_1h (
    code      varchar(20) primary key,
    time      datetime basetime,
    sum_price double,
    sum_volume double,
    sum_bid   double,
    sum_ask   double,
    cnt       integer
);
```

## 3) rollup 작업 생성

`stock_tick` 기준으로 1초 사이에 발생한 데이터에 대한 집계를 생성하는 `rollup_stock_1s`를 만듭니다.

```sql
create rollup rollup_stock_1s
into (stock_rollup_1s)
as (
    select code,
            date_trunc('second', time) as time,
            sum(price) as sum_price,
            sum(volume) as sum_volume,
            sum(bid_price) as sum_bid,
            sum(ask_price) as sum_ask,
            count(*) as cnt
        from stock_tick
    group by code, time
)
interval 1 sec;
```

`stock_rollup_1s` 기준으로 1분 집계를 생성하는 `rollup_stock_1m`를 만듭니다.

```sql
-- 원본 tick 데이터를 1분 버킷으로 집계합니다.
-- 1분 주기로 실행되며 결과는 stock_rollup_1m에 저장됩니다.
create rollup rollup_stock_1m
into (stock_rollup_1m)
as (
    select
        code,
        date_trunc('minute', time) as time,
        sum(sum_price) as sum_price,
        sum(sum_volume) as sum_volume,
        sum(sum_bid) as sum_bid,
        sum(sum_ask) as sum_ask,
        sum(cnt) as cnt
    from stock_rollup_1s
    group by code, time
)
interval 1 min;
```

`stock_rollup_1m` 기준으로 1시간 집계를 생성하는 `rollup_stock_1h`를 만듭니다.

```sql
-- 1분 rollup 데이터를 1시간 버킷으로 재집계합니다.
-- 1시간 주기로 실행되며 결과는 stock_rollup_1h에 저장됩니다.
create rollup rollup_stock_1h
into (stock_rollup_1h)
as (
    select
        code,
        date_trunc('hour', time) as time,
        sum(sum_price) as sum_price,
        sum(sum_volume) as sum_volume,
        sum(sum_bid) as sum_bid,
        sum(sum_ask) as sum_ask,
        sum(cnt) as cnt
    from stock_rollup_1m
    group by code, time
)
interval 1 hour;
```

### 롤업 테이블 조회 시 재집계가 필요한 이유

`stock_rollup_1s`, `stock_rollup_1m`, `stock_rollup_1h` 테이블은 시간 버킷(초/분/시간)마다 항상 1건만 생성된다고
가정하면 안 됩니다. 이벤트 발생 시각, 실제 DB 반영 시점, 그리고 rollup 프로세스가 기존 저장 데이터를
읽는 시점의 경계가 완전히 일치하지 않으면, 같은 버킷에 누락분이 후속 주기에 추가 집계되어
여러 레코드가 생길 수 있습니다.

그래서 조회할 때는 반드시 `group by`로 버킷 단위 재집계를 수행해야 정확한 결과를 얻을 수 있습니다.
그럼에도 rollup 테이블의 레코드 수는 같은 구간의 `stock_tick` 원본보다 훨씬 적기 때문에,
재집계를 하더라도 빠른 조회와 집계가 가능합니다.

## 4) Go 예제: 샘플 tick 데이터 적재

아래 코드는 최근 2시간 구간에 대해 분당 약 30건씩 `stock_tick`에 데이터를 넣습니다.
종목 코드는 `MO`로 고정했기 때문에, 다음 조회 예제를 바로 실행할 수 있습니다.

```go
package main

import (
    "context"
    "fmt"
    "math"
    "math/rand"
    "time"

    "github.com/machbase/neo-server/v8/api"
    "github.com/machbase/neo-server/v8/api/machgo"
)

func main() {
    ctx := context.Background()

    db, err := machgo.NewDatabase(&machgo.Config{Host: "127.0.0.1", Port: 5656})
    if err != nil {
        panic(err)
    }

    conn, err := db.Connect(ctx, api.WithPassword("stock", "stock"))
    if err != nil {
        panic(err)
    }
    defer conn.Close()

    // STOCK_TICK 테이블의 Appender를 생성
    apd, err := conn.Appender(ctx, "stock_tick")
    if err != nil {
        panic(err)
    }
    defer apd.Close()

    code := "MO"
    now := time.Now().Truncate(time.Minute)
    start := now.Add(-2 * time.Hour)

    for minuteOffset := 0; minuteOffset < 120; minuteOffset++ {
        baseTime := start.Add(time.Duration(minuteOffset) * time.Minute)
        for i := 0; i < 120; i++ {
            ts := baseTime.Add(time.Duration(i/2) * time.Second)

            wave := math.Sin(float64(minuteOffset)/10.0) * 3.0
            noise := (rand.Float64() - 0.5) * 0.8
            price := 100.0 + wave + noise
            volume := 1000.0 + rand.Float64()*200.0
            bid := price - 0.05 - rand.Float64()*0.02
            ask := price + 0.05 + rand.Float64()*0.02

            // STOCK_TICK 데이터 입력
            if err := apd.Append(code, ts, price, volume, bid, ask); err != nil {
                panic(err)
            }
        }
    }
    if flusher, ok := apd.(api.Flusher); ok {
        flusher.Flush()
    }
    fmt.Println("insert complete: 120 minutes × 120 ticks = 14,400 rows")

    // 데이터가 실시간으로 들어오지 않고 한 번에 모두 적재되었으므로,
    // rollup 작업이 자동으로 실행되지 않습니다.
    // 테스트를 위해 각 rollup을 강제로 실행하여 집계 테이블을 즉시 업데이트합니다.
    // (실제 운영 환경에서는 정해진 주기마다 자동 실행되므로 이 단계는 불필요합니다.)

    result := conn.Exec(ctx, `exec rollup_force(rollup_stock_1s)`)
	if result.Err() != nil {
		panic(result.Err())
	}
    result = conn.Exec(ctx, `exec rollup_force(rollup_stock_1m)`)
	if result.Err() != nil {
		panic(result.Err())
	}
    result = conn.Exec(ctx, `exec rollup_force(rollup_stock_1h)`)
	if result.Err() != nil {
		panic(result.Err())
	}
}
```

## 5) Go 예제: 최근 2시간 분 단위 평균 조회

조회 전략은 다음과 같습니다.

- `now-2h ~ now-2m`: `stock_rollup_1m` 사용
- `now-2m ~ now`: `stock_rollup_1s` 사용
- `UNION ALL`로 하나의 결과로 결합

이 방식은 조회 대상 기간이 길어져도 raw 데이터인 STOCK_TICK 테이블의 스캔을 회피하여 응답 시간과 DB 부하를 최소화할 수 있습니다.

```go
package main

import (
    "context"
    "fmt"
    "time"

    "github.com/machbase/neo-server/v8/api"
    "github.com/machbase/neo-server/v8/api/machgo"
)

func main() {
    ctx := context.Background()

    db, err := machgo.NewDatabase(&machgo.Config{
        Host: "127.0.0.1",
        Port: 5656,
        MaxOpenConn: -1,
        MaxOpenQuery: -1,
    })
    if err != nil {
        panic(err)
    }

    conn, err := db.Connect(ctx, api.WithPassword("stock", "stock"))
    if err != nil {
        panic(err)
    }
    defer conn.Close()

    sqlText := `
        SELECT
            DATE_TRUNC('minute', time) as mtime,
                SUM(sum_price) / SUM(cnt) as avg_price,
                SUM(sum_volume) as total_volume,
                SUM(sum_bid) / SUM(cnt) as avg_bid,
                SUM(sum_ask) / SUM(cnt) as avg_ask
        FROM stock_rollup_1m
        WHERE code = ?
        AND time >= DATE_TRUNC('minute', SYSDATE) - 2h
        AND time < DATE_TRUNC('minute', SYSDATE) - 2m
        GROUP BY mtime
        ORDER BY mtime

        UNION ALL

        SELECT
            DATE_TRUNC('minute', time) as mtime,
            SUM(sum_price) / SUM(cnt) as avg_price,
            SUM(sum_volume) as total_volume,
            SUM(sum_bid) / SUM(cnt) as avg_bid,
            AVG(sum_ask) / SUM(cnt) as avg_ask
        FROM stock_rollup_1s
        WHERE code = ?
        AND time >= date_trunc('minute', sysdate) - 2m
        GROUP BY mtime
        ORDER BY mtime
    `
    rows, err := conn.Query(ctx, sqlText, "MO", "MO")
    if err != nil {
        panic(err)
    }
    defer rows.Close()

    var (
        mtime       time.Time
        avgPrice    float64
        totalVolume float64
        avgBid      float64
        avgAsk      float64
    )

    for rows.Next() {
        if err := rows.Scan(&mtime, &avgPrice, &totalVolume, &avgBid, &avgAsk); err != nil {
            panic(err)
        }

        fmt.Printf(
            "%s avg=%.4f volume=%.2f bid=%.4f ask=%.4f\n",
            mtime.Format("2006-01-02 15:04"),
            avgPrice,
            totalVolume,
            avgBid,
            avgAsk,
        )
    }
}
```

## 6) 동작 확인

적재 프로그램 실행 후 아래를 순서대로 확인합니다.

1. `stock_tick` 데이터가 실시간으로 증가하는지 확인
2. `stock_rollup_1s`가 1초 단위로 누적되는지 확인
3. `stock_rollup_1m`가 1분 단위로 누적되는지 확인
4. `stock_rollup_1h`가 1시간 단위로 누적되는지 확인
5. 조회 프로그램이 분 단위 연속 결과를 반환하는지 확인

## 정리

- 다단계 rollup 테이블 활용
- 데이터를 stock_tick raw 테이블에만 적재하면 자동으로 rollup 테이블로 누적

Go API 상세 내용은 [MachGo SDK](/kr/neo/sdk-go/machgo/) 및 [Go SDK](/kr/neo/sdk-go/) 문서를 참고하세요.
