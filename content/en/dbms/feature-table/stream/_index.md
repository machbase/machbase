---
title : STREAM
type : docs
weight: 50
---

## Concept

Since Machbase 5, STREAM is a newly supported real-time data processing function based on Continuous Query Language (CQL).
In other words, it is possible to extract the data satisfying a condition of incremental data inputted to the log table and to load it in real-time into another table.
If a conditional search is performed on all the data without using the stream function, the retrieval of the accumulated data is not only slow but also may be a heavy burden imposed on the system.
Stream can be used to retrieve conditions for specific log data entered in real time and respond quickly to events.


## Restrictions

* Currently, Machbase (version 8.0) supports STREAM only in Standard Edition.
    * The Cluster Edition will be support STREAM in a future versions. 
* The data input source is only available with the log table.
    * The ability to use the tag table as a source will be supported in future versions.
* The data output destination is available for log and tag tables.
