---
title: Build a Go app with rollup query
type: docs
weight: 301
toc: true
---

This tutorial explains how to collect stock tick data in a Go application, generate automatic
1-second/1-minute/1-hour aggregates with Machbase custom rollups, and quickly query a target stock
code for a specific time range.

The key strategy is to use rollup tables for historical windows and the recent 2 minutes from a
finer-grained table, which reduces query load while keeping near-real-time results.

## What you will build

- A `stock` user and schema objects for stock data
- `stock_tick` → `stock_rollup_1s` (1-second rollup)
- `stock_rollup_1s` → `stock_rollup_1m` (1-minute rollup)
- `stock_rollup_1m` → `stock_rollup_1h` (1-hour rollup)
- A Go data generator that inserts about 120 ticks per minute for 2 hours
- A Go query app that combines rollup layers with `UNION ALL`

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

Connect as `stock`, then create the raw table and rollup target tables.

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

-- 1-second rollup target table: stores sums and count aggregated from stock_tick.
-- At query time, averages are calculated as sum/cnt to reduce full scans of raw data.
create tag table if not exists stock_rollup_1s (
    code       varchar(20) primary key,
    time       datetime basetime,
    sum_price  double,
    sum_volume double,
    sum_bid    double,
    sum_ask    double,
    cnt        integer,
    open       double,
    open_time  datetime,
    close      double,
    close_time datetime,
    high       double,
    low        double
);

-- 1-minute rollup target table: re-aggregates 1-second rollup data per minute.
-- This multi-stage structure helps reduce CPU/IO load when many events arrive between minute boundaries.
create tag table if not exists stock_rollup_1m (
    code       varchar(20) primary key,
    time       datetime basetime,
    sum_price  double,
    sum_volume double,
    sum_bid    double,
    sum_ask    double,
    cnt        integer,
    open       double,
    open_time  datetime,
    close      double,
    close_time datetime,
    high       double,
    low        double
);

-- 1-hour rollup target table: re-aggregates 1-minute rollup rows into hourly buckets.
-- This multi-stage structure helps reduce CPU/IO load for long-range queries.
create tag table if not exists stock_rollup_1h (
    code       varchar(20) primary key,
    time       datetime basetime,
    sum_price  double,
    sum_volume double,
    sum_bid    double,
    sum_ask    double,
    cnt        integer,
    open       double,
    open_time  datetime,
    close      double,
    close_time datetime,
    high       double,
    low        double
);
```

## 3) Create rollup jobs

Create `rollup_stock_1s` to aggregate data that occurs within each second based on `stock_tick`.

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
            count(*) as cnt,
            first(time, price) as open,
            first(time, time) as open_time,
            last(time, price) as close,
            last(time, time) as close_time,
            max(price) as high,
            min(price) as low
        from stock_tick
    group by code, time
)
interval 1 sec;
```

Create `rollup_stock_1m` to generate 1-minute aggregates from `stock_rollup_1s`.

```sql
-- Roll up 1-second rollup data into 1-minute buckets.
-- Runs every 1 minute and writes into stock_rollup_1m.
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
        sum(cnt) as cnt,
        first(open_time, open) as open,
        first(open_time, open_time) as open_time,
        last(close_time, close) as close,
        last(close_time, close_time) as close_time,
        max(high) as high,
        min(low) as low
    from stock_rollup_1s
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
        sum(cnt) as cnt,
        first(open_time, open) as open,
        first(open_time, open_time) as open_time,
        last(close_time, close) as close,
        last(close_time, close_time) as close_time,
        max(high) as high,
        min(low) as low
    from stock_rollup_1m
    group by code, time
)
interval 1 hour;
```

### Why query-time re-aggregation is required on rollup tables

Do not assume each time bucket (second/minute/hour) has exactly one row in `stock_rollup_1s`,
`stock_rollup_1m`, or `stock_rollup_1h`. Because event time, actual commit time into the database, and the rollup
process read boundary are not always perfectly aligned, late or previously missed records for
the same bucket can be added in a later rollup cycle.

For this reason, your query should always re-aggregate with `group by` on the time bucket.
Even with this extra aggregation step, rollup tables still contain far fewer rows than
`stock_tick` for the same range, so queries remain fast and efficient.

## 4) Go program: insert sample tick data

The following code inserts about 120 rows per minute into `stock_tick` for the last 2 hours.
Because the stock code is fixed to `MO`, you can run the query example directly.

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
        for i := 0; i < 120; i++ {
            ts := baseTime.Add(time.Duration(i/2) * time.Second)

            wave := math.Sin(float64(minuteOffset)/10.0) * 3.0
            noise := (rand.Float64() - 0.5) * 0.8
            price := 100.0 + wave + noise
            volume := 1000.0 + rand.Float64()*200.0
            bid := price - 0.05 - rand.Float64()*0.02
            ask := price + 0.05 + rand.Float64()*0.02

            // Insert into STOCK_TICK
            if err := apd.Append(code, ts, price, volume, bid, ask); err != nil {
                panic(err)
            }
        }
    }
    if flusher, ok := apd.(api.Flusher); ok {
        flusher.Flush()
    }
    fmt.Println("insert complete: 120 minutes × 120 ticks = 14,400 rows")

    // Because data was inserted in a single bulk run (not continuously in real time),
    // rollup jobs may not have run yet.
    // For testing, force each rollup so aggregate tables are updated immediately.
    // (In production, this step is usually unnecessary because rollups run periodically.)

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

## 5) Go program: query 2-hour average by minute

The query strategy is as follows:

- `now-2h ~ now-2m`: use `stock_rollup_1m`
- `now-2m ~ now`: use `stock_rollup_1s`
- Merge with `UNION ALL` as a single result

This minimizes response time and DB load by avoiding wide scans of `stock_tick` even for long ranges.

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
        StatementCache: api.StatementCacheAuto,
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
        AND time >= DATE_TRUNC('minute', sysdate) - 2m
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

## 6) Verify behavior

After running the insert program, check the following in order:

1. Confirm `stock_tick` data is increasing in real time
2. Confirm `stock_rollup_1s` is accumulated every second
3. Confirm `stock_rollup_1m` is accumulated every minute
4. Confirm `stock_rollup_1h` is accumulated every hour
5. Confirm the query program returns continuous minute-level results

## Summary

- Use multi-stage rollup tables
- Insert data only into the `stock_tick` raw table, and rollup tables are accumulated automatically

For more Go API details, see [MachGo SDK](/neo/sdk-go/machgo/) and related pages under [Go SDK](/neo/sdk-go/).
