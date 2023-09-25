---
title: TQL Chart
type: docs
weight: 2
---


# TQL Chart
{:.no_toc}

1. TOC
{:toc}

## Fake

Genrating `fake` data by given method. For now only `oscillator()` is available.

### oscillator

Generating wave data by given frequency and time range. If provide multiple `freq()` arguments, it composites waves.

```js
FAKE( oscillator(freq(1.5, 1.0), freq(1.0, 0.7), range('now', '3s', '10ms')))
CSV()
```

`result`

```
1693442166530011217,-1.091479363236998
1693442166540011217,-1.1038681770016647
1693442166550011217,-1.1073173510851453
1693442166560011217,-1.1020044352839933
1693442166570011217,-1.088180543217658
...
```

## Chart

TQL supports serveral types of chart output.

### Line Chart

```js
FAKE( oscillator(freq(1.5, 1.0), freq(1.0, 0.7), range('now', '3s', '10ms')))
CHART_LINE()
```

![chart-line](/assets/img/chart_line.jpg)

### Bar Chart

```js
FAKE( oscillator(freq(1.5, 1.0), freq(1.0, 0.7), range('now', '3s', '10ms')))
CHART_BAR()
```

![chart-line](/assets/img/chart_bar.jpg)

### Scatter Chart

```js
FAKE( oscillator(freq(1.5, 1.0), freq(1.0, 0.7), range('now', '3s', '10ms')))
CHART_SCATTER()
```

![chart-line](/assets/img/chart_scatter.jpg)
