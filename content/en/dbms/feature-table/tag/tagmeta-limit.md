---
type: docs
title : 'Tag Meta LSL/USL Settings'
weight: 80
---

## Introduction to LSL/USL

`LSL(Lower Specification Limit)` denotes the lower specification limit, while `USL(Upper Specification Limit)` signifies the upper specification limit.  
In Machbase, the LSL/USL feature is supported only in the tag metadata table that is dependent on the tag table.  
The LSL/USL feature sets upper and lower specification limits for a specific TAG ID, serving as a protective measure against unexpected data inputs.  

## Constraints

There are several constraints for the LSL/USL setting.

* The `CLUSTER EDITION` doesn't support LSL/USL feature.
* To set LSL/USL, the third column named __Value__ in the tag table must be set to __SUMMARIZED__.
* It should match the __Value__ column type, and like the __SUMMARIZED__ attribute, can only accept numerical types.
* LSL should be less than or equal to USL, and the input value for the __Value__ column is between LSL and USL, inclusive. __(LSL <= Value <= USL)__
* Data entered before granting the LSL/USL settings is not validated.
* Setting the LSL/USL column to NULL does not validate the input data.
* LSL/USL features can be used separately. you can just set the USL if you only want to match the upper specification.
* If only the USL feature is used, data lower than the USL is not validated.

## Setting and Using LSL/USL

To use the LSL/USL feature, you need to set certain keywords in the columns of the tag metadata table.

* For LSL, use the `LOWER LIMIT` keyword.
* For USL, use the `UPPER LIMIT` keyword.

You can set these when creating the tag table or when adding a metadata column. Here are some examples.

### CRAETE

```sql
CREATE TAG TABLE example (
    tag_id  VARCHAR(50) PRIMARY KEY,
    time    DATETIME    BASETIME,
    value   INTEGER     SUMMARIZED)
METADATA (
    lsl     INTEGER LOWER LIMIT,  -- Set LSL
    usl     INTEGER UPPER LIMIT   -- Set USL
);
```

You can use both columns together, but you can also use just one if you want.  
If you set only the LSL, data higher than the LSL is not validated. It's like setting `USL == NULL`.

```sql
CREATE TAG TABLE example (
    tag_id  VARCHAR(50) PRIMARY KEY,
    time    DATETIME    BASETIME,
    value   INTEGER     SUMMARIZED)
METADATA (
    lsl    INTEGER LOWER LIMIT         -- Set only LSL
);
```

### ADD COLUMN

If you add using `ADD COLUMN` after data is already entered, the default value is __NULL__.
You can set a default value using the `DEFAULT` attribute, but previously entered data is not validated.

```sql
CREATE TAG TABLE example (
    tag_id  VARCHAR(50) PRIMARY KEY,
    time    DATETIME    BASETIME,
    value   INTEGER     SUMMARIZED
);
 
ALTER TABLE _example_meta ADD COLUMN (lsl INTEGER LOWER LIMIT)              -- Set LSL
ALTER TABLE _example_meta ADD COLUMN (usl INTEGER DEFAULT 200 UPPER LIMIT)  -- Set USL and provide default value
```

You can also add just one attribute as with [CREATE](#craete).

```sql
CREATE TAG TABLE example (
    tag_id  VARCHAR(50) PRIMARY KEY,
    time    DATETIME    BASETIME,
    value   INTEGER     SUMMARIZED
);

ALTER TABLE _example_meta ADD COLUMN (usl INTEGER DEFAULT 200 UPPER LIMIT)  -- Set only USL
```

### INSERT

Once the LSL/USL feature is set up and the LSL/USL for a specific TAG ID is set, you are ready to input data.

```sql
INSERT INTO example metadata VALUES ('TAG_01', 100, 200);
```

After setting it up, when entering tag data, it will operate as follows.

```sql
Mach> INSERT INTO example VALUES ('TAG_01', NOW, 95);  -- Failure
[ERR-02342: SUMMARIZED value is less than LOWER LIMIT.]

Mach> INSERT INTO example VALUES ('TAG_01', NOW, 100); -- Success (Inclusive)
1 row(s) inserted.
Elapsed time: 0.000

Mach> INSERT INTO example VALUES ('TAG_01', NOW, 150); -- Success
1 row(s) inserted.
Elapsed time: 0.000

Mach> INSERT INTO example VALUES ('TAG_01', NOW, 200); -- Success (Inclusive)
1 row(s) inserted.
Elapsed time: 0.000

Mach> INSERT INTO example VALUES ('TAG_01', NOW, 205); -- Failure
[ERR-02341: SUMMARIZED value is greater than UPPER LIMIT.]
```

When you view the tag table after entering the values, you can confirm that only the verified data has been entered.

```sql
Mach> SELECT * FROM example;
TAG_ID                                              TIME                            VALUE       LSL         USL         
------------------------------------------------------------------------------------------------------------------------------
TAG_01                                              2023-09-12 09:31:27 923:289:631 100         100         200         
TAG_01                                              2023-09-12 09:31:27 929:013:232 150         100         200         
TAG_01                                              2023-09-12 09:31:27 939:209:248 200         100         200         
[3] row(s) selected.
Elapsed time: 0.001
```

### UPDATE

You can modify the values of the LSL/USL columns set in the tag meta table.  
Since it doesn't verify the data already entered into the tag data table, use it with caution.

```sql
Mach> UPDATE example metadata SET lsl = 10, usl = 100 WHERE tag_id = 'TAG_01';
1 row(s) updated.
Elapsed time: 0.001

Mach> SELECT * FROM _example_meta;
_ID                  TAG_ID                                              LSL         USL         
------------------------------------------------------------------------------------------------------
1                    TAG_01                                              10          100         
[1] row(s) selected.
Elapsed time: 0.001
```

### DELETE

The tag meta table does not support the `DROP COLUMN` feature, so there is no direct way to delete only the LSL/USL columns.  
Although you can't delete columns, if you set the LSL/USL column values to NULL, you can input data without any constraints.

```sql
Mach> UPDATE EXAMPLE METADATA SET lsl = NULL, usl = NULL WHERE tag_id = 'TAG_01';
1 row(s) updated.
Elapsed time: 0.001

Mach> SELECT * FROM _example_meta;
_ID                  TAG_ID                                              LSL         USL         
------------------------------------------------------------------------------------------------------
1                    TAG_01                                              NULL        NULL        
[1] row(s) selected.
Elapsed time: 0.001
```
