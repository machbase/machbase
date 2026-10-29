---
type: docs
title: Apps
weight: 30
---

Machbase Neo packages extend the platform with data collection, replication, video monitoring,
and AI-assisted analysis. You can install the packages you need from the package list in the web UI,
then configure and manage them in your browser.

------

{{< cards >}}

  <!-- Representative image: neo-pkg-replication/docs/images/dashboard-main.png. Replace as needed. -->
  {{< card link="https://machbase.github.io/neo-pkg-replication/en/"
    image="/images/package/replication.png" icon="gift"
    title="Replication"
    subtitle="The Replication package (`neo-pkg-replication`) copies Machbase table data to another Machbase server. You can configure replication conditions and column mappings, monitor progress, and review logs through the web UI. If replication is interrupted by a network issue or server shutdown, it can resume from where it stopped once the connection is restored, helping prevent data gaps.">}}

  <!-- Representative image: neo-pkg-opcua-client/docs/images/opcua-dashboard-main.png. Replace as needed. -->
  {{< card link="https://machbase.github.io/neo-pkg-opcua-client/en/"
    image="/images/package/opcua-client.png" icon="gift"
    title="OPC UA Client"
    subtitle="The OPC UA Client package (`neo-pkg-opcua-client`) collects equipment and sensor data from OPC UA servers and stores it in Machbase Neo. You can browse server nodes, select data to collect, and configure column mappings and value transformations. You can also start or stop collection jobs and review their status and logs through the web UI. The Data Viewer lets you explore collected data in tables and charts.">}}

  <!-- Representative image: neo-pkg-blackbox/docs/images/blackbox-dashboard-video-sync.png. Replace as needed. -->
  {{< card link="https://machbase.github.io/neo-pkg-blackbox/en/"
    image="/images/package/blackbox.png" icon="gift"
    title="Blackbox"
    subtitle="The Blackbox package (`neo-pkg-blackbox`) provides video monitoring for managing camera feeds and detection events. You can register Blackbox servers and cameras, configure object detection and event rules, and review event history. The Video panel in Neo dashboards lets you view live or recorded footage and align recorded video with time-series charts for comparison.">}}

  <!-- Representative image: neo-pkg-llm-chat/docs/images/llm-chat-main.png. Replace as needed. -->
  {{< card link="https://machbase.github.io/neo-pkg-llm-chat/en/"
    image="/images/package/llm-chat.png" icon="gift"
    title="LLM Chat"
    subtitle="The LLM Chat package (`neo-pkg-llm-chat`) provides an AI chat interface for querying and analyzing Machbase Neo data in natural language. You can explore tables and tags, and create dashboards and analysis reports through conversation. It supports a variety of large language models (LLMs), with model selection and connection settings managed through the web UI.">}}

  <!-- Representative image: neo-pkg-bearing-analytics/docs/static/images/monitoring.png. Replace as needed. -->
  {{< card link="https://machbase.github.io/neo-pkg-bearing-analytics/en/"
    image="/images/package/bearing-analytics.png" icon="gift"
    title="Bearing Analytics"
    subtitle="The Bearing Analytics package (`neo-pkg-bearing-analytics`) diagnoses bearing faults from the vibration sensor data stored in Machbase Neo. With no queries or code, just enter the RPM and bearing model for each machine, and it grades the bearing condition of every machine in real time based on bearing defect frequencies. The Detail Analysis screen and HTML reports show the evidence behind each verdict and the actions to take, and server monitoring with messenger notifications keeps watch even after the app is closed.">}}
    
{{< /cards >}}
