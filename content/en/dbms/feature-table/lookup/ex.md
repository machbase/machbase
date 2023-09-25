---
title : Lookup Table Utilization Example
type: docs
weight: 60
---

The lookup table can be updated and is used to add data that is not in the original log data through a join. The following example shows an example of creating a log table and a lookup table.

```sql
-- Create log table.
create table weblog (addr ipv4, msg varchar(100));
-- Input sample data.
insert into weblog values ('127.0.0.1', 'a test msessage');
-- Create lookup table.
create lookup table dnslookup (addr ipv4 primary key, hostname varchar (100));
```

Let's insert or update the data in the lookup table.

```sql
insert into dnslookup values ('127.0.0.1', 'localhost') on duplicate key update set hostname = '127.0.0.1'
```

You can retrieve data from lookup tables and log tables through join.

```sql
select msg, hostname from weblog, dnslookup where weblog.addr = dnslookup.addr;
```