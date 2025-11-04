---
title : '사용자 관리'
type: docs
weight: 60
---

# Index

* [CREATE USER](#create-user)
* [DROP USER](#drop-user)
* [ALTER USER](#alter-user)
* [CONNECT](#connect)
* [GRANT/REVOKE](#grantrevoke)
* [Managing User Example](#managing-user-example)


## CREATE USER

**create_user_stmt:**

![create_user_stmt](/images/sql/user/create_user_stmt.png)

```sql
create_user_stmt ::= 'CREATE USER' user_name 'IDENTIFIED BY' password
```

사용자를 생성하는 구문입니다:

```sql
-- Example
CREATE USER new_user IDENTIFIED BY password
```


## DROP USER

**drop_user_stmt:**

![drop_user_stmt](/images/sql/user/drop_user_stmt.png)

```sql
drop_user_stmt ::= 'DROP USER' user_name
```

사용자를 삭제하는 구문은 다음과 같습니다. SYS 사용자는 삭제할 수 없으며, 삭제하려는 사용자가 이미 생성한 테이블이 있으면 오류가 표시됩니다.

```sql
-- Example
DROP USER old_user
```


## ALTER USER

**alter_user_pwd_stmt:**

![alter_user_pwd_stmt](/images/sql/user/alter_user_pwd_stmt.png)

```sql
alter_user_pwd_stmt ::= 'ALTER USER' user_name 'IDENTIFIED BY' password
```

사용자는 다음 구문을 통해 비밀번호를 변경할 수 있습니다.

```sql
-- Example
ALTER USER user1 IDENTIFIED BY password
```


## CONNECT

**user_connect_stmt:**

![user_connect_stmt](/images/sql/user/user_connect_stmt.png)

```sql
user_connect_stmt: 'CONNECT' user_name '/' password
```

사용자는 애플리케이션을 종료하지 않고 다음 구문을 통해 다른 사용자로 재연결할 수 있습니다.

```sql
-- Example
CONNECT user1/password;
```


## GRANT/REVOKE

![grant_stmt](/images/sql/user/grant_stmt.png)

![revoke_stmt](/images/sql/user/revoke_stmt.png)

![priv_value](/images/sql/user/priv_value.png)

GRANT 문을 통해 사용자에게 테이블에 대한 권한을 부여합니다.

```sql
-- user1에게 mytable에 대한 SELECT 권한 부여
GRANT SELECT ON mytable TO user1;

-- user1에게 mytable에 대한 모든 권한 부여
GRANT ALL ON mytable TO user1;
```

REVOKE 문을 통해 사용자에게 부여된 권한을 취소합니다.

```sql
-- user1에게 부여된 mytable에 대한 UPDATE 권한 취소
REVOKE UPDATE ON mytable FROM user1;

-- user1에게 부여된 mytable에 대한 모든 권한 취소
REVOKE ALL ON mytable FROM user1;
```


## Managing User Example

위 쿼리의 예제와 결과입니다.

```
############################################
## SYS 계정으로 연결
############################################
Mach> create user demo identified by 'demo';
Created successfully.

Mach> drop user demo;
Dropped successfully.

Mach> create user demo1 identified by 'demo1';
Created successfully.

Mach> create user demo2 identified by 'demo2';
Created successfully.

Mach> alter user demo2 identified by 'demo22';
Altered successfully.

Mach> create table demo1_table (id integer);
Created successfully.

Mach> create bitmap index demo1_table_index1 on demo1_table(id);
Created successfully.

Mach> insert into demo1_table values(99991);
1 row(s) inserted.

Mach> insert into demo1_table values(99992);
1 row(s) inserted.

Mach> insert into demo1_table values(99993);
1 row(s) inserted.

Mach> select * from demo1_table;
ID
--------------
99993
99992
99991
[3] row(s) selected.

#Error: 연결된 사용자는 삭제할 수 없습니다.
Mach> drop user SYS;
[ERR-02083 : Drop user error. You cannot drop yourself(SYS).]

############################################
## DEMO1 연결
############################################
Mach> connect demo1/demo1;
Connected successfully.

#Error: 다른 사용자의 계정 비밀번호를 변경할 수 없습니다
Mach> alter user demo2 identified by 'demo22';
[ERR-02085 : ALTER user error. The user(DEMO2) does not have ALTER privileges.]

Mach> alter user demo1 identified by demo11;
Altered successfully.

#Error: 잘못된 비밀번호
Mach> connect demo1/demo11234;
[ERR-02081 : User authentication error. Invalid password (DEMO11234).]

## 올바른 비밀번호
Mach> connect demo1/demo11;
Connected successfully.

Mach> create table demo1_table (id integer);
Created successfully.

Mach> create bitmap index demo1_table_index1 on demo1_table(id);
Created successfully.

Mach> insert into demo1_table values(1);
1 row(s) inserted.

Mach> insert into demo1_table values(2);
1 row(s) inserted.

Mach> insert into demo1_table values(3);
1 row(s) inserted.

Mach> select * from demo1_table;
ID
--------------
3
2
1
[3] row(s) selected.

Mach> select * from demo1.demo1_table;
ID
--------------
3
2
1
[3] row(s) selected.

############################################
## SYS로 다시 연결
############################################
Mach> connect SYS/MANAGER;
Connected successfully.

Mach> select * from demo1_table;
ID
--------------
99993
99992
99991
[3] row(s) selected.

Mach> select * from demo1.demo1_table;
ID
--------------
3
2
1
[3] row(s) selected.

Mach> drop user demo1;
[ERR-02084 : DROP user error. The user's tables still exist. Drop those tables first.]

Mach> connect demo1/demo11;
Connected successfully.

Mach> drop table demo1_table;
Dropped successfully.

Mach> connect SYS/MANAGER;
Connected successfully.

Mach> drop user demo1;
Dropped successfully.
```
