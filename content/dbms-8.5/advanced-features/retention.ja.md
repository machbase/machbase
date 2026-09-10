---
title : データ保持期間
type : docs
weight: 70
toc: true
---

指定した保持期間を過ぎたデータを自動的に削除します。

保持期間と削除間隔を指定した保持ポリシーを作成し、ALTER 文でテーブルに適用、または適用を解除できます。

## 保持ポリシーの作成 {#create-retention-policy}

保持期間と削除間隔を指定して RETENTION POLICY を作成します。

保持期間の単位には、月、日、時、分、秒を指定できます。
削除間隔の単位には、日、時、分、秒を指定できます。

ポリシー情報は **M$RETENTION** テーブルで確認できます。

**構文：**

```sql
CREATE RETENTION policy_name DURATION duration {MONTH|DAY|HOUR|MIN|SEC} INTERVAL interval {DAY|HOUR|MIN|SEC}
```

* policy_name：作成するポリシー名
* duration：データの保持期間（システム時刻を基準とする）
* interval：保持期間を確認する間隔

**例：**

```sql
-- 1 日より古いデータを 1 時間ごとに削除する。
Mach> CREATE RETENTION policy_1d_1h DURATION 1 DAY INTERVAL 1 HOUR;
Executed successfully.

-- 1 か月より古いデータを 3 日ごとに削除する。
Mach> CREATE RETENTION policy_1m_3d DURATION 1 MONTH INTERVAL 3 DAY;
Executed successfully.

-- 短い間隔も指定できる。
Mach> CREATE RETENTION policy_30s_3s DURATION 30 SEC INTERVAL 3 SEC;
Executed successfully.

Mach> SELECT * FROM M$RETENTION;
USER_ID     POLICY_NAME                               DURATION             INTERVAL
-----------------------------------------------------------------------------------------------------
1           POLICY_1D_1H                              86400                3600
1           POLICY_1M_3D                              2592000              259200
1           POLICY_30S_3S                             30                   3
[3] row(s) selected.
```

## 保持ポリシーの適用 {#apply-retention-policy}

作成済みの RETENTION POLICY をテーブルに適用します。

適用後は、削除間隔ごとに保持期間を確認し、期間を過ぎたデータを削除します。

適用先のテーブル情報は **V$RETENTION_JOB** テーブルで確認できます。

**構文：**

```sql
ALTER TABLE table_name ADD RETENTION policy_name
```

* table_name：適用先のテーブル名
* policy_name：適用するポリシー名

**例：**

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

## 保持ポリシーの適用解除 {#release-retention-policy}

テーブルに適用した RETENTION POLICY を解除します。

解除後は、このポリシーによる自動削除は行われず、データは永続的に保持されます。

**構文：**

```sql
ALTER TABLE table_name DROP RETENTION;
```

* table_name：適用を解除するテーブル名

**例：**

```sql
Mach> ALTER TABLE tag DROP RETENTION;
Altered successfully.
```

## 保持ポリシーの削除 {#drop-retention-policy}

ポリシーを適用中のテーブルがある場合、そのポリシーは削除できません。

先にテーブルへの適用を解除してから、ポリシーを削除してください。

**構文：**

```sql
DROP RETENTION policy_name
```

* policy_name：削除するポリシー名

**例：**

```sql
Mach> ALTER TABLE tag ADD RETENTION policy_1d_1h;
Altered successfully.

-- エラー
Mach> DROP RETENTION policy_1d_1h;
[ERR-02702: Policy (POLICY_1D_1H) is in use.]

Mach> ALTER TABLE tag DROP RETENTION;
Altered successfully.

-- 成功
Mach> DROP RETENTION policy_1d_1h;
Dropped successfully.
```
