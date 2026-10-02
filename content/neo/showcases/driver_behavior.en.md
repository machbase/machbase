---
title: Driver Behavior Analysis Report
type: docs
weight: 989
---

This AI report template analyzes 47,096 records of six-axis vehicle IMU data (three-axis accelerometer and gyroscope), sampled once per second over about 1 hour and 52 minutes, to assess driving behavior.

{{< youtube d11v5EG56eg >}}

**Analysis pipeline**

- Event detection: Detect rapid acceleration (AccX above its upper limit), hard braking (AccX below its lower limit), and sharp turns (GyroZ and AccY above their thresholds). Adaptive thresholds based on the mean ± 2σ statistically identify unusual moments for each driver.
- Safety score: Combine event frequency, risky-driving ratio, and severity into a score from 0 to 100, then assign one of four levels: Safe, Moderate, Risky, or Dangerous.
- Three-axis vector visualization: Show raw waveforms at one-second resolution for each tag alongside a three-axis overlay rolled up by minute. Toggle series from the legend.
- Event timeline: Overlay rapid-acceleration (▲), hard-braking (▼), and sharp-turn (◆) markers on the AccX waveform. Sample up to 200 events to prevent overload when events are numerous.
- Event summary table: Use rollup buckets to aggregate the count and ratio for each event type and identify the time range with the highest concentration.
- Class-label validation: Use the time-based distribution and averages of labels 0/1/2 to compare actual and predicted results from a supervised-learning perspective.
- In-depth LLM reporting: Evaluate the safety score, acceleration patterns, turning stability, and driver-level distribution, then generate a narrative diagnosis and eight recommendations, each with evidence, actions, and expected outcomes.

**Interactions**

Scroll to zoom, drag to pan, double-click to reset, toggle series from the three-axis chart legend, and inspect detailed event-marker tooltips.

**Summary**

Raw IMU waveforms → adaptive event detection using mean ± 2σ thresholds → four-level safety scoring → three-axis vector visualization → event and waveform timeline → automated LLM diagnosis