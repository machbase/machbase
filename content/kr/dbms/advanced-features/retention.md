---
type: docs
title : 데이터 보존
type : docs
weight: 70
---

지정한 데이터 보존 기간이 지나면 데이터를 자동으로 삭제하는 기능입니다.

보존 기간과 삭제 주기를 정의한 보존 정책을 생성한 후 ALTER 구문을 통해 테이블에 적용하거나 해제할 수 있습니다.

## Create Retention Policy

보존 기간과 삭제 주기를 지정해 RETENTION POLICY를 생성합니다.

보존 기간은 월 또는 일 단위로 지정하고, 삭제 주기는 일 또는 시간 단위로 지정할 수 있습니다.

정책 정보는 **M$RETENTION** 테이블 조회로 확인할 수 있습니다.

**Syntax:**

```sql
CREATE RETENTION policy_name DURATION duration {MONTH|DAY} INTERVAL interval {DAY|HOUR}
```

* policy_name : 생성할 정책 이름
* duration : 삭제 대상 데이터의 보존 기간(시스템 시간 기준)
* interval : 보존 기간 점검 주기

**Example:**

```sql
-- 하루 이상 지난 데이터는 삭제하고, 갱신 주기는 1시간으로 설정합니다.
Mach> CREATE RETENTION policy_1d_1h DURATION 1 DAY INTERVAL 1 HOUR;
Executed successfully.

-- 한 달 이상 지난 데이터는 삭제하고, 갱신 주기는 3일로 설정합니다.
Mach> CREATE RETENTION policy_1m_3d DURATION 1 MONTH INTERVAL 3 DAY;
Executed successfully.

Mach> SELECT * FROM M$RETENTION;
USER_ID     POLICY_NAME                               DURATION             INTERVAL             
-----------------------------------------------------------------------------------------------------
1           POLICY_1D_1H                              86400                3600                 
1           POLICY_1M_3D                              2592000              259200               
[2] row(s) selected.
```

## Apply Retention Policy

이전에 생성한 RETENTION POLICY를 테이블에 적용합니다.

적용 이후에는 삭제 주기마다 보존 기간을 점검하고 조건에 부합하는 데이터를 삭제합니다.

정책이 적용된 테이블은 **V$RETENTION_JOB** 테이블 조회로 확인할 수 있습니다.

**Syntax:**

```sql
ALTER TABLE table_name ADD RETENTION policy_name
```

* table_name : 정책을 적용할 테이블 이름
* policy_name : 적용할 정책 이름

**Example:**

```sql
Mach> CREATE TAG TABLE tag (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE SUMMARIZED);
Executed successfully.

Mach> ALTER TABLE tag ADD RETENTION policy_1d_1h;
Altered successfully.

Mach> SELECT * FROM V$RETENTION_JOB;
USER_NAME                                                                         TABLE_NAME                                                                        
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
POLICY_NAME                                                                       STATE                                                                             LAST_DELETED_TIME               
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
SYS                                                                               TAG                                                                               
POLICY_1D_1H                                                                      WAITING                                                                           NULL                            
[1] row(s) selected.

```

## Release Retention Policy

테이블에 적용한 RETENTION POLICY를 해제합니다.

해제 이후에는 데이터가 삭제되지 않고 영구 보관됩니다.

**Syntax:**

```sql
ALTER TABLE table_name DROP RETENTION;
```

* table_name : 보존 정책을 해제할 테이블 이름

**Example:**

```sql
Mach> ALTER TABLE tag DROP RETENTION;
Altered successfully.
```

## Drop Retention Policy

RETENTION POLICY가 적용 중인 테이블이 존재하면 해당 정책을 삭제할 수 없습니다.

정책을 삭제하려면 먼저 적용된 테이블에서 보존 정책을 해제해야 합니다.

**Syntax:**

```sql
DROP RETENTION policy_name
```

* policy_name : 삭제할 정책 이름

**Example:**

```sql
Mach> ALTER TABLE tag ADD RETENTION policy_1d_1h;
Altered successfully.

-- ERROR
Mach> DROP RETENTION policy_1d_1h;
[ERR-02702: Policy (POLICY_1D_1H) is in use.]

Mach> ALTER TABLE tag DROP RETENTION;
Altered successfully.

-- SUCCESS
Mach> DROP RETENTION policy_1d_1h;
Dropped successfully.
```
