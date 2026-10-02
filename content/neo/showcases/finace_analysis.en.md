---
title: Financial Analysis Report
type: docs
weight: 979
---

This AI report template analyzes price trends, volatility, and trading signals in 68,530 SILVER OHLCV records spanning about two years and five months.

{{< youtube Z_pZ14fb0wY >}}

**Analysis pipeline**

- Candlestick chart (OHLC): Display open, high, low, and close values in each candle. Up candles are green and down candles are red; the body shows open and close, while the wick shows high and low.
- Price trends and moving averages (MA): Overlay the MA5 (short-term), MA20 (medium-term), and MA60 (long-term) simple moving averages (SMA) on the closing-price chart. An upward MA5 crossing of MA20 is treated as a bullish golden cross.
- Bollinger Bands: Calculate bands two population standard deviations from the MA20 center line over a rolling 20-day window. Use band width to identify volatility regimes, and interpret a close outside the bands as an overbought or oversold signal.
- Volume-price relationship: Plot price and volume on dual Y-axes, using colors based on the daily price change to reveal volume-price divergence.
- Technical analysis narrative: Generate a diagnosis across five areas: trend, volatility, volume, technical levels (support and resistance), and risk.
- Trading scenario recommendations: Provide eight price-based recommendation triggers for targets, entries, stops, and breakouts instead of fixed immediate, short-term, or long-term time horizons.

**Interactions**

Scroll to zoom, drag to pan, and double-click to reset. Candlestick charts provide a combined O/H/L/C/Volume tooltip; Bollinger Bands provide a combined close/MA20/upper/lower tooltip.

**Summary**

OHLCV time series → four-value candlestick visualization → moving-average trend analysis → Bollinger Band volatility analysis → volume-price relationship → technical analysis narrative → price-triggered trading scenarios