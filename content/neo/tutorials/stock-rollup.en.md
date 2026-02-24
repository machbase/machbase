---
title: Build a Go app with rollup query
type: docs
weight: 301
toc: true
---

This tutorial shows how Go developers can collect stock tick data and configure Machbase custom rollups
so 1-minute and 1-hour aggregates are generated automatically. You will also build a query program that
reads a target stock code for a time range using rollup data for historical windows and raw ticks for the
most recent 2 minutes.

## What you will build

- A `stock` user and schema objects for ticks and rollups
- A 1-minute rollup from `stock_tick` to `stock_rollup_1m`
- A 1-hour rollup from `stock_rollup_1m` to `stock_rollup_1h`
- A Go data generator that inserts about 30 ticks per minute for 2 hours
- A Go query app that combines rollup + raw data with `UNION ALL`

## Prerequisites

- Machbase Neo is running
- Go 1.24+
- You can connect as `sys` (for initial user creation)
- Basic familiarity with Machbase Go SDK. See [MachGo SDK](/neo/sdk-go/machgo/).

## 1) Create the `stock` user (as `sys`)

Run this SQL first using the `sys` account:

```sql
-- Create an application account dedicated to stock data ingestion and queries.
create user stock identified by stock;
```

From here, use `stock/stock` for all table, rollup, and application work.

## 2) Create tables

Connect as `stock`, then create the raw tick table and two rollup target tables.

```sql
-- Raw tick table: stores per-trade events per stock code with event time.
create tag table if not exists stock_tick (
    code      varchar(20) primary key,
    time      datetime basetime,
    price     double,
    volume    double,
    bid_price double,
    ask_price double
);

-- 1-minute rollup target table: stores pre-aggregated sums and count from stock_tick.
-- The query app will derive averages from (sum / cnt) instead of scanning raw ticks.
create tag table if not exists stock_rollup_1m (
    code      varchar(20) primary key,
    time      datetime basetime,
    sum_price double,
    sum_volume double,
    sum_bid   double,
    sum_ask   double,
    cnt       integer
);

-- 1-hour rollup target table: re-aggregates 1-minute rollup rows into hourly buckets.
-- This second-level rollup supports longer-range analytics with minimal query cost.
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

## 3) Create rollup jobs

Create `rollup_stock_1m` so `stock_tick` is aggregated every minute.

```sql
-- Roll up raw ticks into 1-minute buckets.
-- Runs every 1 minute and writes into stock_rollup_1m.
create rollup rollup_stock_1m
into (stock_rollup_1m)
as (
    select
        code,
        date_trunc('minute', time) as time,
        sum(price) as sum_price,
        sum(volume) as sum_volume,
        sum(bid_price) as sum_bid,
        sum(ask_price) as sum_ask,
        count(*) as cnt
    from stock_tick
    group by code, time
)
interval 1 min;
```

Create `rollup_stock_1h` so `stock_rollup_1m` is aggregated every hour.

```sql
-- Roll up 1-minute aggregates into 1-hour buckets.
-- Runs every 1 hour and writes into stock_rollup_1h.
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

### Why query-time re-aggregation is required on rollup tables

Do not assume each time bucket (minute/hour) has exactly one row in `stock_rollup_1m` or
`stock_rollup_1h`. Because event time, actual commit time into the database, and the rollup
process read boundary are not always perfectly aligned, late or previously missed records for
the same bucket can be added in a later rollup cycle.

For this reason, your query should always re-aggregate with `group by` on the time bucket.
Even with this extra aggregation step, rollup tables still contain far fewer rows than
`stock_tick` for the same range, so queries remain fast and efficient.

## 4) Go program: generate sample tick data

The following example inserts around 30 rows per minute for the last 2 hours into `stock_tick`.
It uses stock code `MO`, so you can run the query example directly after insertion.

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
        for i := 0; i < 30; i++ {
            ts := baseTime.Add(time.Duration(i*2) * time.Second)

            wave := math.Sin(float64(minuteOffset)/10.0) * 3.0
            noise := (rand.Float64() - 0.5) * 0.8
            price := 100.0 + wave + noise
            volume := 1000.0 + rand.Float64()*200.0
            bid := price - 0.05 - rand.Float64()*0.02
            ask := price + 0.05 + rand.Float64()*0.02

            if err := apd.Append(code, ts, price, volume, bid, ask); err != nil {
                panic(err)
            }
        }
    }

    fmt.Println("insert complete: 120 minutes × 30 ticks = 3600 rows")
}
```

## 5) Go program: query 2-hour average by minute

This query pattern is the key point:

- Use rollup table (`stock_rollup_1m`) from `now-2h` to `now-2m`
- Use raw table (`stock_tick`) for the latest 2 minutes
- Merge both with `UNION ALL`

This avoids scanning all raw ticks for large ranges and keeps query latency low.

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

    db, err := machgo.NewDatabase(&machgo.Config{Host: "127.0.0.1", Port: 5656})
    if err != nil {
        panic(err)
    }

    conn, err := db.Connect(ctx, api.WithPassword("stock", "stock"))
    if err != nil {
        panic(err)
    }
    defer conn.Close()

    sqlText := `
select
    DATE_TRUNC('minute', time) as mtime,
        SUM(sum_price) / SUM(cnt) as avg_price,
        SUM(sum_volume) as total_volume,
        SUM(sum_bid) / SUM(cnt) as avg_bid,
        SUM(sum_ask) / SUM(cnt) as avg_ask
from stock_rollup_1m
where code = ?
    and time >= DATE_TRUNC('minute', SYSDATE) - 2h
    and time < DATE_TRUNC('minute', SYSDATE) - 2m
group by mtime

UNION ALL

select
    DATE_TRUNC('minute', time) as mtime,
    SUM(price)/count(*) as avg_price,
    SUM(volume) as total_volume,
    SUM(bid_price)/count(*) as avg_bid,
    SUM(ask_price)/count(*) as avg_ask
from stock_tick
where code = ?
    and time >= DATE_TRUNC('minute', SYSDATE) - 2m
group by mtime

order by mtime;
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

## 6) Verify behavior

After running the insert app for a few minutes:

1. Check that `stock_tick` is increasing in real time.
2. Check that `stock_rollup_1m` is updated every minute.
3. Check that `stock_rollup_1h` is updated every hour.
4. Run the query app and confirm it returns continuous minute-by-minute rows.

## Why this pattern is effective

- Rollup tables reduce CPU and I/O for historical ranges.
- Raw table keeps the latest data near real-time.
- Same application query covers both requirements with a single SQL statement.

For more Go API details, see [MachGo SDK](/neo/sdk-go/machgo/) and related pages under [Go SDK](/neo/sdk-go/).
