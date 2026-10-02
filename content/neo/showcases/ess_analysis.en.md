---
title: Pump Backup Power Diagnostics
type: docs
weight: 945
---

Store ESS data from a water-treatment pump in Machbase Neo and detect anomalies early by analyzing thresholds, rates of change, and patterns.

{{< youtube yHfgGf0OOHA >}}

This demo stores cell- and rack-level temperature and voltage data from a water-treatment plant's pump backup power system (ESS) in Machbase Neo. It detects warning signs that fixed thresholds alone can miss by analyzing rates of change and patterns. Pumps must remain available during power outages, so battery backup systems are always on standby. Monitoring individual cells is essential because thermal runaway in one cell can spread into a rack fire and interrupt the water supply.

The demo collects 98 tags at one-second intervals: temperatures and voltages from four racks and 48 cells, plus pump load. It ingests 8.46 million records representing 24 hours of data in 28 seconds, at about 300,000 records per second. The tag table stores site, rack, cell, and measurement metadata in a `METADATA` clause. This makes it possible to query directly with conditions such as `where rack='R02' and metric='TEMP'`, without parsing tag names as strings. Three levels of rollup (seconds, minutes, and hours) are generated automatically, so aggregates are available immediately while all 8.46 million raw records remain intact.

Eight TQL scripts progressively improve detection, from thresholds to rates of change and anomalous patterns. A simple 55 °C threshold can alert on a one-second sensor spike while missing a cell undergoing thermal runaway. By contrast, the temperature rise rate calculated from a five-minute rollup identifies the same cell as risky at 51.6 °C, before it reaches the absolute threshold, with a rise of 0.27 °C per minute. A degraded cell whose temperature remains normal but whose voltage is falling can be found from voltage deviations among cells in the same rack. Comparing the maximum and average values over one-minute intervals also helps distinguish a momentary sensor false positive from sustained overheating.

Finally, a rule-based health score weights four risk factors: rise rate, temperature, cell deviation, and voltage drop. It ranks all 48 cells in one table. A cell undergoing thermal runaway scores 18.9 (Risk), while a degraded cell with only a voltage drop scores 74.0 (Warning). The main reasons for each deduction are shown alongside the score, explaining why cells with similar overall risk can have different underlying issues.

See how tag tables and TQL can detect equipment anomalies before they cross fixed thresholds and show the reasoning in the web interface, without a separate analytics stack or trained model.