---
title: OPC UA Client Derived Tags
type: docs
weight: 959
---

Use derived tags in the Machbase Neo OPC UA Client to calculate and store values that are not provided by the OPC UA server during data collection.

{{< youtube _5FEzqZGD-w >}}

This demo uses derived tags to calculate and store values that are not available from the OPC UA server during collection.

Connect the voltage and current tags being collected to variables and write an expression. The server validates it in real time and creates a new power tag.

Registered derived tags are stored periodically in the Machbase database, just like existing tags. View them alongside the source tags in Data Viewer to check the results.

Define the metrics you need in the web interface and collect them immediately, without developing a separate calculation program or changing the OPC UA server configuration.