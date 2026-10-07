---
title: Binance Visualization
type: docs
weight: 487
---

Install the coin monitor package from the Machbase Neo console to store real-time trades and order book data for 50 Binance coins, then compare queries against raw data and rollups.

{{< icon "github" >}} https://github.com/machbase/neo-pkg-coin-collector
<p/>

{{< youtube bL17z0viUqQ >}}

Installing the package from the app store registers a collection service and creates its tables, rollups, and retention policies. Collection starts immediately, and the app opens in the browser. Use the side panel to stop or restart collection and change the raw data retention period.

The real-time view continuously updates prices, trading volume, and trade strength across five sections—Majors, Layer 1, DeFi, AI, and Meme—with thousands of trades per second. When trades in one second exceed 30 times the usual volume, a whale alert appears. Select the alert to zoom straight into the raw trades from that second. The same real-time data also powers a 10-minute round of simulated trading; every order is recorded in a LOG table and can be recalculated at any time. In the DB Inside view, run the same query against raw data and rollups side by side to compare execution time and rows read (ETH 7-day, 30-minute candles: 14.91 million raw rows in 23.9 seconds versus 699 rollup rows in 0.057 seconds). You can also inspect the SQL, table layout, and data retention period.

Trades and order book data are stored in a TAG table, while whale alerts and simulated trading records are stored in a LOG table. The example shows how minute- and hour-level rollups and retention policies keep raw data only for a set period while retaining summaries. It demonstrates how to deploy a real-time data app—from collection to visualization—with a single Machbase Neo executable, without a separate collection server or frontend build.
