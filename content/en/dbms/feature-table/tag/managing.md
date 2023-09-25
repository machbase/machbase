---
title : 'Managing tag meta (tag name)'
type: docs
weight: 20
---

## Concept of tag meta

The tag meta represents the name and additional information of an arbitrary tag stored in the Machbase.

That is, if there are three tags existing in a specific apparatus, an arbitrary name representing the tag and related additional information are required, which are all referred to as meta information of the tag.

This tag meta should specify at least a name and, if necessary, specify various data types for the device.

## Tag meta with tag name only

### Creation of tag meta

Below is the command to create the TAG table where the most basic tag meta is created.

```sql
create tag table TAG (name varchar(20) primary key, time datetime basetime, value double summarized);
Mach> desc tag;
[ COLUMN ]                             
----------------------------------------------------------------
NAME                          TYPE                LENGTH       
----------------------------------------------------------------
NAME                          varchar             20                 
TIME                          datetime            31             
VALUE                         double              17
```

The above is the basic TAG table creation, and there is no separate information about the tag meta.

In this case, the tag meta has only basic information of VARCHAR (20).

### Input of tag meta

Now, let's insert one piece of tag information named TAG1.

```sql
Mach> insert into tag metadata values ('TAG_0001');
1 row(s) inserted.
```
Through the above query, we created one tag named TAG_0001.

### Output of tag meta

Machbase provides a special table _tag_meta for identifying the information of the input tag meta.

Therefore, the user can confirm the information of all the tags input in the Machbase through the following query.

```sql
Mach> select * from _tag_meta;
ID                   NAME                 
----------------------------------------------
1                    TAG_0001             
[1] row(s) selected.
```

The ID is automatically assigned as an internally managed value.

### Modifying tag meta

Machbase allows you to modify the input tag meta information. The name can be modified as follows.

```sql
Mach> update tag metadata set name = 'NEW_0001' where NAME = 'TAG_0001';
1 row(s) updated.
 
Mach> select * from _tag_meta;
ID                   NAME                 
----------------------------------------------
1                    NEW_0001             
[1] row(s) selected.
```

You can see that the name has been changed from TAG_0001 to NEW_0001 as above.

### Deleting tag meta

You can delete the actual tag meta information as shown below.

```sql
Mach> delete from tag metadata where name = 'NEW_0001';
1 row(s) deleted.
 
Mach> select * from _tag_meta;
ID                   NAME                 
----------------------------------------------
[0] row(s) selected.
```

However, it should be noted that tag meta can be deleted when the actual data of the tag dosen't refer to the corresponding tag meta.


## Tag meta with additional information

### Creation of tag meta

Below, we will add 16 bit integer, time, and IPv4 information to the tag meta information.

Note that once you have created a tag meta, you can modify the value except the structure.

```sql
create tag table TAG (name varchar(20) primary key, time datetime basetime, value double summarized)
metadata (type short, create_date datetime, srcip ipv4) ;
 
Mach> desc tag;
[ COLUMN ]                             
----------------------------------------------------------------
NAME                          TYPE                LENGTH       
----------------------------------------------------------------
NAME                          varchar             20                 
TIME                          datetime            31             
VALUE                         double              17                 
[ META-COLUMN ]                             
----------------------------------------------------------------
NAME                          TYPE                LENGTH       
----------------------------------------------------------------
TYPE                          short               6              
CREATE_DATE                   datetime            31             
SRCIP                         ipv4                15                 
```

### Input of tag meta

You can check the information by typing the following with the additional information other than the name.

```sql
Mach> insert into tag metadata(name) values ('TAG_0001');
1 row(s) inserted.
 
Mach> select * from _tag_meta;
ID                   NAME                  TYPE        CREATE_DATE                     SRCIP          
-------------------------------------------------------------------------------------------------------------
1                    TAG_0001              NULL        NULL                            NULL           
[1] row(s) selected.
```

Like above, NULL is inserted except NAME column.

Now let's add more information as shown below.

```sql
Mach> insert into tag metadata values ('TAG_0002', 99, '2010-01-01', '1.1.1.1');
1 row(s) inserted.
 
Mach> select * from _tag_meta;
ID                   NAME                  TYPE        CREATE_DATE                     SRCIP          
-------------------------------------------------------------------------------------------------------------
1                    TAG_0001              NULL        NULL                            NULL           
2                    TAG_0002              99          2010-01-01 00:00:00 000:000:000 1.1.1.1        
[2] row(s) selected.
```

Additional Information made each tag meta can be given a wealth of information.

### Modifying tag meta

Now let's change the type of TAG_0001 from NULL to 11.

```sql
Mach> update tag metadata set type = 11 where name = 'TAG_0001';
1 row(s) updated.
 
Mach> select * from _tag_meta;
ID                   NAME                  TYPE        CREATE_DATE                     SRCIP          
-------------------------------------------------------------------------------------------------------------
2                    TAG_0002              99          2010-01-01 00:00:00 000:000:000 1.1.1.1        
1                    TAG_0001              11          NULL                            NULL           
[2] row(s) selected.
```

You can modify the values of all fields through the UPDATE statement.

However, it is a common constraint that NAME must be specified in the WHERE clause.


## Tag meta lookup via RESTful API

### Get all tag lists

Below is an example of getting a list of all the tags in Machbase.

```bash
Host:~$ curl  -G  "http://192.168.0.148:5001/machiot-rest-api/tags/list"
{"ErrorCode": 0,
 "ErrorMessage": "",
 "Data": [{"NAME": "TAG_0001"},
          {"NAME": "TAG_0002"}]}
Host:~$
```

### Get the time range of a specific tag

Below is an example of obtaining the minimum and maximum time range of the data that the desired tag has.

This feature is very useful when charting specific tags.

#### Syntax

```bash
{MWA URL}/machiot-rest-api/tags/range/  ## Time Range of whole DB
{MWA URL}/machiot-rest-api/tags/range/{TagName}  ## Time Range of a specific Tag
```

#### Getting time range of all tags

```bash
Host:~$ curl  -G  "http://192.168.0.148:5001/machiot-rest-api/tags/range/"
{"ErrorCode": 0,
 "ErrorMessage": "",
 "Data": [{"MAX": "2018-02-10 10:00:00 000:000:000", "MIN": "2018-01-01 01:00:00 000:000:000"}]}
Getting Time range of a specific tag
Host:~$ curl  -G  "http://192.168.0.148:5001/machiot-rest-api/tags/range/TAG_0001"
{"ErrorCode": 0, "ErrorMessage": "", "Data": [{"MAX": "2018-01-10 10:00:00 000:000:000", "MIN": "2018-01-01 01:00:00 000:000:000"}]}
Host:~$
Host:~$ curl  -G  "http://192.168.0.148:5001/machiot-rest-api/tags/range/TAG_0002"
{"ErrorCode": 0, "ErrorMessage": "", "Data": [{"MAX": "2018-02-10 10:00:00 000:000:000", "MIN": "2018-02-01 01:00:00 000:000:000"}]}
```

#### Getting Time range of a specific tag

```bash
Host:~$ curl  -G  "http://192.168.0.148:5001/machiot-rest-api/tags/range/TAG_0001"
{"ErrorCode": 0, "ErrorMessage": "", "Data": [{"MAX": "2018-01-10 10:00:00 000:000:000", "MIN": "2018-01-01 01:00:00 000:000:000"}]}
Host:~$
Host:~$ curl  -G  "http://192.168.0.148:5001/machiot-rest-api/tags/range/TAG_0002"
{"ErrorCode": 0, "ErrorMessage": "", "Data": [{"MAX": "2018-02-10 10:00:00 000:000:000", "MIN": "2018-02-01 01:00:00 000:000:000"}]}
```
