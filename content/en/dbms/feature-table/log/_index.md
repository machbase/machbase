---
title : Log Table
type : docs
weight: 20
---

## Concept

The **log table** is a table capable of storing machine log data in which input data is time series data.

Data is infinitely entered into this table, and the value of each field has a unique meaning. 
You can also retrieve data through text fields (varchar or text) and perform fast statistical calculations.

Generally, a Machbase table refers to the Log Table.

The characteristics of the log table are as follows.


### Existing Hidden Time Columns

Every log table has a hidden column called _arrival_time. 
This column stores the time at which the record was generated, and supports nanosecond precision.

### Reverse Time Search

The general database is output regardless of the input order when retrieving data. 
However, Machbase's log tables always have the most up-to-date data as long as they do not have a sort option through a separate ORDER BY. 
This can also be seen in the _arrival_time column.

This is because the importance of recent data in machine log data is much higher than that of previous data.

### View-Only Post Input

Machbase's log tables do not allow Update operations. In other words, once user log data is stored in Machbase,

By disallowing changes to the data, it is possible to support the stability of the data and the integrity of the log data itself at the engine level.

### Limited Deletion Allowed

Machbase permits the deletion of necessary data in special situations, even if the data can not be changed.
However, you can not delete arbitrary data as in a conventional database, and it is only possible to delete the oldest data sequentially.
With this function, it is possible to conveniently manage data by deleting data periodically from embedded devices that are limited in storage space or devices that are not easy to manage.

### Supports Text Search Function

Machbase goes one step further in the way it handles strings in generic databases, and provides word-based searching.
This function is best suited for the purpose of machine log data, and searching for log data stored at a specific time is a major function frequently used in real business situations.

To do this, Machbase provides a real-time reverse index, which enables real-time text search at the same time as insertion of data.

### Special Data Type Support

Machbase supports IPv4 and IPv6. This is a special type of Internet address, and many machine log data are represented by this type of address system.
This data type makes it easy to search and extract specific addresses.

It also provides the ability to search or extract some address ranges of a particular address scheme, using extended syntax such as select * from t1 where ipaddr = '192.168.0.*'.
You can also use the netmask operator to easily determine whether a particular Internet address is included in a particular address range.

### Large Object (LOB) Data Support

The log table provides text and binary types that can store up to 64MB of bytes.

If the data is required to be retrieved as a text document type, it can be stored as a text type and retrieved.
If the data is a binary data type such as picture or music, it can be saved as a binary type.

### Time-based Partitioning

A log table is a sequence of partition files that maintains a certain number of records and indexes relative to the time axis.
In other words, as the data continues to be entered, a new partition file is created, and if a certain number of records in that partition are full, the next partition will be created.

Partition management mainly reflects the characteristics of log data in which search is performed based on time, and has a great advantage in data input performance.
It is also an easy structure for high-speed data access for statistical analysis.


## Operations

* [Creating and Managing Log Table](./create-drop)
* [Log Data Input](./insert)
* [Log Data Extraction](./extract)
* [Deletion of Log Data](./delete)
* [Index for log table](./log-index)
* [Example of Log Table](./ex)




