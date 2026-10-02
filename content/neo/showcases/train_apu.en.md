---
title: Railway APU Condition Diagnostics
type: docs
weight: 975
---

Follow a time-series workflow for railway APU sensor data in Machbase Neo, from ingestion and visualization to condition diagnostics.

{{< icon "github" >}} https://github.com/machbase/neo-train-apu-demo
<p/>

{{< youtube UmttgrKJWwM >}}

This demo stores the MetroPT-3 dataset from the UCI Machine Learning Repository in Machbase Neo and explores the condition of a railway vehicle's Air Production Unit (APU) in an interactive dashboard.

Analyze sensor data over time alongside the dataset's recorded air-leak failure periods and an explainable health score.

**Key features**

- Explore the complete MetroPT-3 dataset (about 1.51 million timestamps)
- Visualize railway APU airflow and equipment condition
- Analyze 15 sensor types, including pressure, temperature, current, valves, and switches
- Mark air-leak failure periods recorded in the dataset
- Display an explainable, rule-based health score and events
- Replay and explore sensor data over time
- English and Korean UI
- Fast time-series queries powered by Machbase Neo JSON Rollup
- Frame, Window, and Signal APIs based on Live Query
- Evidence API for inspecting SQL, execution time, and rollup details

The health score and events in this demo are explainable, project-defined rules, not predictions from a machine-learning model.

Failure periods provided by the dataset are displayed separately from events calculated by the project, making the analysis based on real sensor data transparent.

For Industrial AI and predictive maintenance, it is important not only to predict anomalies but also to analyze sensor readings over time and explain the results.

Machbase Neo stores large time-series datasets and uses JSON Rollup to quickly query the required intervals. The data can then be presented in web-based monitoring and analysis views.

This demo shows how railway APU time-series data can power real-time analysis and an explainable condition-diagnostics interface.