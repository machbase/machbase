---
title: 'extension.tc Sample SQL'
type: docs
weight: 62
---

```sql
*- drop table tag cascade;
create tag table tag (name varchar(20) primary key, time datetime basetime, value double summarized, value2 double);

# value1
create rollup _tag_rollup_custom_1 on tag(value) interval 1 sec  extension;
create rollup _tag_rollup_custom_2 from _tag_rollup_custom_1 interval 1 min extension;
create rollup _tag_rollup_custom_3 on tag(value) interval 1 min extension where value2 = 0;

insert into tag values('APPL', '2020-01-01 00:00:00', 100,  0);
insert into tag values('APPL', '2020-01-01 00:00:10', 101,  0);
insert into tag values('APPL', '2020-01-01 00:00:11', 130,  0);
insert into tag values('APPL', '2020-01-01 00:00:20', 120,  0);
insert into tag values('APPL', '2020-01-01 00:00:30', 110,  0);
insert into tag values('APPL', '2020-01-01 00:00:40', 9900,  1);
insert into tag values('APPL', '2020-01-01 00:00:50', 99,  0);

insert into tag values('APPL', '2020-01-01 00:01:00', 98, 0);
insert into tag values('APPL', '2020-01-01 00:01:10', 94, 0);
insert into tag values('APPL', '2020-01-01 00:01:20', 2990, 1);
insert into tag values('APPL', '2020-01-01 00:01:30', 92, 0);
insert into tag values('APPL', '2020-01-01 00:01:40', 99, 0);
insert into tag values('APPL', '2020-01-01 00:01:50', 102, 0);

insert into tag values('APPL', '2020-01-01 00:02:00', 110, 0);
insert into tag values('APPL', '2020-01-01 00:02:10', 120, 0);
insert into tag values('APPL', '2020-01-01 00:02:20', 140, 0);
insert into tag values('APPL', '2020-01-01 00:02:30', 66160, 1);
insert into tag values('APPL', '2020-01-01 00:02:40', 170, 0);
insert into tag values('APPL', '2020-01-01 00:02:50', 180, 0);

exec rollup_force(_tag_rollup_custom_1);
exec rollup_force(_tag_rollup_custom_2);
exec rollup_force(_tag_rollup_custom_3);

select rollup('sec', 10, time) as rt , count(value), min(value), max(value), first(time, value), last(time , value) from tag group by rt order by rt;
select rollup('min', 1, time) as rt , count(value), min(value), max(value), first(time, value), last(time , value)  from tag group by rt order by rt;
select /*+ ROLLUP_TABLE(_tag_rollup_custom_3) */ rollup('min', 1, time) as rt , count(value), min(value), max(value), first(time, value), last(time , value)  from tag group by rt order by rt;
```
