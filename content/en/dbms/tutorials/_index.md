---
title: 'Tutorials'
weight: 20
---

Learn Machbase through hands-on tutorials. Each tutorial walks you through a real-world scenario from start to finish.

## Tutorial Overview

| Tutorial | Table Type | Difficulty | Time | What You'll Learn |
|----------|-----------|------------|------|-------------------|
| [IoT Sensor Data](./iot-sensor-data/) | Tag Table | Beginner | 15 min | Collect and analyze sensor data from multiple devices |
| [Application Logs](./application-logs/) | Log Table | Beginner | 15 min | Store and search application logs efficiently |
| [Real-time Analytics](./realtime-analytics/) | Volatile Table | Intermediate | 20 min | Build a real-time monitoring dashboard |
| [Reference Data](./reference-data/) | Lookup Table | Beginner | 10 min | Manage device registry and metadata |

## Before You Start

Make sure you have:

1. Machbase installed and running
2. machsql command-line client available
3. Basic understanding of SQL
4. Completed the [Getting Started](../getting-started/) section

## Tutorial Format

Each tutorial follows this structure:

1. **Scenario** - Real-world problem description
2. **What You'll Build** - Expected outcome
3. **Step-by-Step Instructions** - Detailed walkthrough
4. **Try It Yourself** - Practice exercises
5. **Next Steps** - How to expand on what you learned

## Learning Path

We recommend following the tutorials in order:

```
Tutorial 1: IoT Sensor Data
    ↓
Tutorial 2: Application Logs
    ↓
Tutorial 3: Real-time Analytics
    ↓
Tutorial 4: Reference Data
```

However, feel free to jump to any tutorial that matches your needs!

## Tutorial 1: IoT Sensor Data

**Perfect for**: Anyone working with sensor devices, IoT platforms, or industrial monitoring

**You'll learn**:
- How to use Tag tables for sensor data
- Storing millions of sensor readings
- Querying by sensor ID and time range
- Using automatic rollup statistics
- Implementing data retention policies

[Start Tutorial 1 →](./iot-sensor-data/)

## Tutorial 2: Application Logs

**Perfect for**: Developers managing application logs, system administrators

**You'll learn**:
- How to use Log tables for event data
- Storing high-volume application logs
- Full-text search with SEARCH keyword
- Time-based queries with DURATION
- Log retention and cleanup

[Start Tutorial 2 →](./application-logs/)

## Tutorial 3: Real-time Analytics

**Perfect for**: Building dashboards, real-time monitoring systems

**You'll learn**:
- How to use Volatile tables for in-memory data
- UPDATE and DELETE operations
- Fast key-based lookups
- Building live status boards
- Combining with other table types

[Start Tutorial 3 →](./realtime-analytics/)

## Tutorial 4: Reference Data

**Perfect for**: Managing master data, device registries, configuration

**You'll learn**:
- How to use Lookup tables
- Storing reference/master data
- JOIN operations with time-series data
- Maintaining device metadata

[Start Tutorial 4 →](./reference-data/)

## After Completing Tutorials

Once you've finished, you'll be ready to:

- Choose the right table type for your use case
- Design efficient Machbase schemas
- Write optimized queries
- Implement production-ready solutions

**Continue learning**:
- [Core Concepts](../core-concepts/) - Deeper understanding of Machbase
- [Common Tasks](../common-tasks/) - Everyday operations
- [Table Types Deep Dive](../table-types/) - Advanced features

## Need Help?

- Review [Basic Concepts](../getting-started/concepts/)
- Check [Troubleshooting Guide](../troubleshooting/)
- Refer to [SQL Reference](../sql-reference/)

Ready to start? Begin with [Tutorial 1: IoT Sensor Data](./iot-sensor-data/)!
