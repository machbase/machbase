---
title: Goアプリでのロールアップ検索
type: docs
weight: 301
toc: true
---

このチュートリアルは、Goアプリケーションで株式のティックデータを収集し、Machbaseのカスタムロールアップ機能で
1秒・1分・1時間単位の集計データを自動生成してから、特定の銘柄コードの任意の期間のデータを高速に検索する方法を説明します。

過去の期間はロールアップテーブルを使い、直近2分はより細かい粒度のロールアップテーブルを使うことで、リアルタイムに近い結果を保ちながら検索負荷を減らします。

## 構成する内容 {#구성-목표}

- `stock`ユーザーと株式データ用テーブルの構成
- `stock_tick` → `stock_rollup_1s` (1秒ロールアップ)
- `stock_rollup_1s` → `stock_rollup_1m` (1分ロールアップ)
- `stock_rollup_1m` → `stock_rollup_1h` (1時間ロールアップ)
- 2時間の期間に、毎分約120件のデータを取り込むGoの例
- ロールアップの各階層のデータを、`UNION ALL`で結合して検索するGoの例

## 前提条件 {#사전-준비}

- Machbase Neoが実行中
- Go 1.24+
- 初期ユーザーを作成するための`sys`アカウントへのアクセス権限
- Machbase Go SDKの基本的な使用方法は、[MachGo SDK](/neo/tutorials/cli-go/)を参照

## 1) `sys`アカウントでの`stock`ユーザーの作成 {#1-sys-계정으로-stock-사용자-생성}

まず、`sys`アカウントで以下のSQLを実行します。

```sql
-- 株式データの取り込み・検索アプリケーション専用のアカウントを作成します。
create user stock identified by stock;
```

以降のテーブル作成、ロールアップ作成、アプリケーション実行には、すべて`stock/stock`アカウントを使用します。

## 2) テーブルの作成 {#2-테이블-생성}

`stock`ユーザーで接続し、生データテーブルとロールアップ先のテーブルを作成します。

```sql
-- 生データのtickテーブル：銘柄ごとの約定イベントを時刻に基づいて保存します。
create tag table if not exists stock_tick (
    code      varchar(20) primary key,
    time      datetime basetime,
    price     double,
    volume    double,
    bid_price double,
    ask_price double
);

-- 1秒ロールアップ先テーブル：stock_tickから集計した合計sumと件数cntを保存します。
-- 検索時の平均はsum/cntで求め、生データの全スキャンを減らします。
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

-- 1分ロールアップ先テーブル：1秒ロールアップの結果を分単位に再集計します。
-- 1分間に大量のデータが発生する場合、検索時のCPU/I/O負荷を減らす多段階集計です。
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

-- 1時間ロールアップ先テーブル：1分ロールアップの結果を時間単位に再集計します。
-- 長期間の検索でCPU/I/O負荷を減らす多段階集計です。
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

## 3) ロールアップジョブの作成 {#3-rollup-작업-생성}

`stock_tick`から、1秒間に発生したデータの集計を生成する`rollup_stock_1s`を作成します。

```sql
create rollup rollup_stock_1s
into (stock_rollup_1s)
as (
    select 
        code,
        date_trunc('second', time) as time,
        sum(price) as sum_price,
        sum(volume) as sum_volume,
        sum(bid_price) as sum_bid,
        sum(ask_price) as sum_ask,
        count(*) as cnt,
        first(time, price) as open,
        min(time) as open_time,
        last(time, price) as close,
        max(time) as close_time,
        max(price) as high,
        min(price) as low
    from stock_tick
    group by code, time
)
interval 1 sec;
```

`stock_rollup_1s`から1分集計を生成する`rollup_stock_1m`を作成します。

```sql
-- 1秒ロールアップデータを、1分バケットに集計します。
-- 1分間隔で実行し、結果をstock_rollup_1mに保存します。
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
        min(open_time) as open_time,
        last(close_time, close) as close,
        max(close_time) as close_time,
        max(high) as high,
        min(low) as low
    from stock_rollup_1s
    group by code, time
)
interval 1 min;
```

`stock_rollup_1m`から1時間集計を生成する`rollup_stock_1h`を作成します。

```sql
-- 1分ロールアップデータを、1時間バケットに再集計します。
-- 1時間間隔で実行し、結果をstock_rollup_1hに保存します。
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
        min(open_time) as open_time,
        last(close_time, close) as close,
        max(close_time) as close_time,
        max(high) as high,
        min(low) as low
    from stock_rollup_1m
    group by code, time
)
interval 1 hour;
```

### ロールアップテーブルの検索時に再集計が必要な理由 {#롤업-테이블-조회-시-재집계가-필요한-이유}

`stock_rollup_1s`、`stock_rollup_1m`、`stock_rollup_1h`テーブルでは、時間バケット（秒・分・時間）ごとに必ず1行だけが生成されると
仮定しないでください。イベントの発生時刻、DBへの実際の反映時刻、ロールアッププロセスが保存済みデータを
読み取る時刻の境界が一致しない場合、同じバケットの遅延分や欠落分を後の周期で追加集計し、
複数のレコードが作成されることがあります。

そのため、正確な結果を得るには、検索時に必ず`group by`でバケット単位に再集計してください。
それでも、ロールアップテーブルのレコード数は同じ期間の`stock_tick`原本より大幅に少ないため、
再集計を行っても、高速に検索・集計できます。

## 4) Goの例：サンプルのティックデータの取り込み {#4-go-예제-샘플-tick-데이터-적재}

以下のコードは、直近2時間の期間について、毎分約120件ずつ`stock_tick`にデータを挿入します。
銘柄コードは`MO`に固定しているため、次の検索例をそのまま実行できます。

```go
package main

import (
    "context"
    "fmt"
    "math"
    "math/rand"
    "time"

    "github.com/machbase/neo-client/api"
    "github.com/machbase/neo-client/machgo"
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

    // STOCK_TICKテーブルのAppenderを作成
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

            // STOCK_TICKデータの入力
            if err := apd.Append(code, ts, price, volume, bid, ask); err != nil {
                panic(err)
            }
        }
    }
    if flusher, ok := apd.(api.Flusher); ok {
        flusher.Flush()
    }
    fmt.Println("insert complete: 120 minutes × 120 ticks = 14,400 rows")

    // データはリアルタイムではなく、一度にすべて取り込んだため、
    // ロールアップジョブは自動実行されません。
    // テスト用に各ロールアップを強制実行し、集計テーブルを直ちに更新します。
    // （実際の運用では定期的に自動実行されるため、この手順は不要です。）

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

## 5) Goの例：直近2時間のN分単位の平均検索 {#5-go-예제-최근-2시간-n분-단위-평균-조회}

検索方法は以下のとおりです。

- `now-2h ~ now-2m`: `stock_rollup_1m`を使用
- `now-2m ~ now`: `stock_rollup_1s`を使用
- `UNION ALL`で1つの結果に結合

この方式は、検索期間が長くても、生データのSTOCK_TICKテーブルの広範囲スキャンを避け、応答時間とDB負荷を抑えます。

```go
package main

import (
    "context"
    "fmt"
    "time"

    "github.com/machbase/neo-client/api"
    "github.com/machbase/neo-client/machgo"
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

    nMinute := 5
    nFrom := "0/0/0 -2:0:0" // -2 hours
    nGap := fmt.Sprintf("0/0/0 0:-%d:0", nMinute) // now - n minutes
    if nMinute == 1 {
        nGap = "0/0/0 0:-2:0" // 現在時刻の2分前（1分ロールアップの完了前にクエリを実行する場合がある）
    }

    sqlText := `
        SELECT
            DATE_TRUNC('minute', time, ?) as mtime,
            FIRST(open_time, open) as open,
            LAST(close_time, close) as close,
            MAX(high) as high,
            MIN(low) as low,
            SUM(sum_price) / SUM(cnt) as avg_price,
            SUM(sum_volume) as total_volume,
            SUM(sum_bid) / SUM(cnt) as avg_bid,
            SUM(sum_ask) / SUM(cnt) as avg_ask
        FROM stock_rollup_1m
        WHERE code = ?
        AND time >= ADD_TIME(DATE_TRUNC('minute', SYSDATE, ?), ?)
        AND time <  ADD_TIME(DATE_TRUNC('minute', SYSDATE, ?), ?)
        GROUP BY mtime
        ORDER BY mtime

        UNION ALL

        SELECT
            DATE_TRUNC('minute', time, ?) as mtime,
            FIRST(open_time, open) as open,
            LAST(close_time, close) as close,
            MAX(high) as high,
            MIN(low) as low,
            SUM(sum_price) / SUM(cnt) as avg_price,
            SUM(sum_volume) as total_volume,
            SUM(sum_bid) / SUM(cnt) as avg_bid,
            SUM(sum_ask) / SUM(cnt) as avg_ask
        FROM stock_rollup_1s
        WHERE code = ?
        AND time >= ADD_TIME(DATE_TRUNC('minute', SYSDATE, ?), ?)
        GROUP BY mtime
        ORDER BY mtime
    `
    rows, err := conn.Query(ctx, sqlText, 
        nMinute, "MO", nMinute, nFrom, nMinute, nGap,
        nMinute, "MO", nMinute, nGap)
    if err != nil {
        panic(err)
    }
    defer rows.Close()

    var (
        mtime       time.Time
        open        float64
		close       float64
		high        float64
		low         float64
        avgPrice    float64
        totalVolume float64
        avgBid      float64
        avgAsk      float64
    )

    for rows.Next() {
		if err := rows.Scan(&mtime, &open, &close, &high, &low, &avgPrice, &totalVolume, &avgBid, &avgAsk); err != nil {
			panic(err)
		}

		fmt.Printf(
			"%s open=%.4f close=%.4f high=%.4f low=%.4f avg=%.4f volume=%.2f bid=%.4f ask=%.4f\n",
			mtime.In(time.Local).Format("2006-01-02 15:04"),
			open,
			close,
			high,
			low,
			avgPrice,
			totalVolume,
			avgBid,
			avgAsk,
		)
    }
}
```

## 6) 動作の確認 {#6-동작-확인}

取り込みプログラムの実行後、以下を順に確認します。

1. `stock_tick`のデータがリアルタイムに増えていることを確認
2. `stock_rollup_1s`が1秒単位で蓄積されていることを確認
3. `stock_rollup_1m`が1分単位で蓄積されていることを確認
4. `stock_rollup_1h`が1時間単位で蓄積されていることを確認
5. 検索プログラムが分単位の連続した結果を返すことを確認

## まとめ {#정리}

- 多段階のロールアップテーブルを使用
- stock_tickの生データテーブルに取り込むだけで、ロールアップテーブルに自動蓄積

Go APIの詳細は、[MachGo SDK](/neo/tutorials/cli-go/)と[Go SDK](/neo/tutorials/cli-go/)を参照してください。
