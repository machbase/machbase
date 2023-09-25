---
title : '데이터 자동 삭제'
type : docs
weight: 70
---

데이터 보존 기간을 지정하여, 해당 기간이 지나면 데이터가 자동으로 삭제되는 기능이다.

보존 기간 및 삭제 주기를 지정한 Retention Policy를 생성하고, ALTER 구문을 통해 테이블에 적용/해제할 수 있다.

# Retention Policy 생성

보존 기간 및 삭제 주기를 지정하여 RETENTION POLICY를 생성한다.

보존 기간은 월(MONTH), 일(DAY) 단위로 지정할 수 있으며, 삭제 주기는 일(DAY), 시간(HOUR) 단위로 지정할 수 있다.

POLICY 정보는 **M$RETENTION** 테이블 조회하여 확인할 수 있다.

**Syntax:**
```sql
CREATE RETENTION policy_name DURATION duration {MONTH|DAY} INTERVAL interval {DAY|HOUR}
```

* policy_name : 생성할 policy 이름
* duration : 삭제할 데이터의 보존 기간(시스템 시간 기준)
* interval : 보존 기간 확인 주기

**Example:**
```sql
-- 1일 이상 지난 데이터를 삭제하고, 갱신 주기를 1시간으로 한다.
Mach> CREATE RETENTION policy_1d_1h DURATION 1 DAY INTERVAL 1 HOUR;
Executed successfully.

-- 1달 이상 지난 데이터를 삭제하고, 갱신 주기를 3일로 한다.
Mach> CREATE RETENTION policy_1m_3d DURATION 1 MONTH INTERVAL 3 DAY;
Executed successfully.

Mach> SELECT * FROM M$RETENTION;
USER_ID     POLICY_NAME                               DURATION             INTERVAL             
-----------------------------------------------------------------------------------------------------
1           POLICY_1D_1H                              86400                3600                 
1           POLICY_1M_3D                              2592000              259200               
[2] row(s) selected.
```

# Retention Policy 적용

사전에 생성된 RETENTION POLICY를 테이블에 적용한다.

적용 이후에는 삭제 주기마다 보존 기간을 확인하여 삭제한다.

RETENTION POLICY가 적용된 테이블 정보는 **V$RETENTION_JOB** 테이블을 조회하여 확인할 수 있다.

**Syntax:**
```sql
ALTER TABLE table_name ADD RETENTION policy_name
```

* table_name : 적용할 table 이름
* policy_name : 적용할 policy 이름

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

# Retention Policy 해제

테이블에 적용된 RETENTION POLICY를 해제한다.

해제 이후에는 데이터가 삭제되지 않고 영구 보존된다.

**Syntax:**
```sql
ALTER TABLE table_name DROP RETENTION;
```

* table_name : 해제할 table 이름

**Example:**
```sql
Mach> ALTER TABLE tag DROP RETENTION;
Altered successfully.
```

# Retention Policy 삭제

해당 RETENTION POLICY가 적용 중인 테이블이 존재하면 삭제할 수 없다.

적용 중인 테이블의 RETENTION을 해제하고 삭제해야 한다.

**Syntax:**
```sql
DROP RETENTION policy_name
```

* policy_name : 삭제할 policy 이름

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