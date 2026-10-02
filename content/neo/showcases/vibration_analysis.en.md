---
title: Vibration Analysis Report
type: docs
weight: 997
---

Give the AI a vibration table and the request "Create a vibration analysis report" to generate an HTML report with visualizations, in-depth diagnostics, and recommendations.

{{< youtube fVrC9ji5Q5M >}}

This report template uses AI to assess bearing condition from raw vibration-acceleration data stored in the Machbase Neo time-series database: 10 million records from channels C1 and C2, sampled at 25.6 kHz.

**Analysis pipeline**

- Time-domain analysis: Roll up four metrics by second: RMS (energy), P2P (amplitude), Crest Factor (impulsiveness), and mean (DC offset).
- Frequency-domain analysis: Use a 0.2 Hz-resolution FFT (up to 12.8 kHz across 4,096 bins) to provide evidence for identifying fault frequencies, such as rotational harmonics and bearing defects.
- Severity assessment: Automatically assign one of four levels (Good/Warning/Danger/Critical) based on reconstructed ISO 10816-3 criteria and provide the reasons for each decision.
- Trend Ratio analysis: Compare RMS values from the beginning and end of the period to provide early warning of changes.
- In-depth LLM reporting: Generate a narrative covering status, spectrum interpretation, impact analysis, root-cause hypotheses, ISO assessment, and fault-mode diagnosis, along with immediate, short-, and long-term recommendations.

**Interactions**

Scroll to zoom, drag to pan, double-click to reset, and inspect detailed tooltips at millisecond resolution.

**Summary**

Raw waveform → four time-domain metrics → frequency-domain FFT → severity assessment based on ISO 10816 → automated LLM diagnosis