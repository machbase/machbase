---
title : '사용자 관리'
type: docs
weight: 60
---

## CREATE USER

**create_user_stmt:**

![create_user_stmt](../user_image/create_user_stmt.png)

```sql
create_user_stmt ::= 'CREATE USER' user_name 'IDENTIFIED BY' password
```

사용자를 생성하는 구문은 다음과 같다.

```sql
--예제
CREATE USER new_user IDENTIFIED BY password
```

## DROP USER

**drop_user_stmt:**

![drop_user_stmt](../user_image/drop_user_stmt.png)

```sql
drop_user_stmt ::= 'DROP USER' user_name
```

사용자를 삭제하는 구문은 다음과 같다. SYS 사용자는 삭제할 수 없으며, 삭제 대상 사용자가 이미 생성한 테이블이 있을 경우에는 에러를 나타낸다.

```sql
--예제
DROP USER old_user
```

## ALTER USER

**alter_user_pwd_stmt:**

![alter_user_pwd_stmt](../user_image/alter_user_pwd_stmt.png)

```sql
alter_user_pwd_stmt ::= 'ALTER USER' user_name 'IDENTIFIED BY' password
```

사용자는 아래의 구문을 통해 비밀번호를 변경할 수 있다.

```sql
--예제
ALTER USER user1 IDENTIFIED BY password
```

## CONNECT

**user_connect_stmt:**

![user_connect_stmt](../user_image/user_connect_stmt.png)

```sql
user_connect_stmt: 'CONNECT' user_name '/' password
```

사용자는 응용 프로그램을 종료하지 않고, 다음의 구문을 통해 다른 사용자로 재접속할 수 있다.

```sql
--예제
CONNECT user1/password;
```


## GRANT/REVOKE

![grant_stmt](../user_image/grant_stmt.png)

![revoke_stmt](../user_image/revoke_stmt.png)

![priv_value](../user_image/priv_value.png)

GRANT 구문을 통하여 사용자에게 테이블에 대한 권한을 부여한다.


```sql
-- user1 에게 mytable 에 대한 SELECT 권한 부여
GRANT SELECT ON mytable TO user1;
 
-- user1 에게 mytable 에 대한 모든 권한 부여
GRANT ALL ON mytable TO user1;
```

REVOKE 구문을 통하여 사용자에게 부여된 권한을 회수한다.

```sql
-- user1 에게 부여된 mytable 에 대한 UPDATE 권한 회수
REVOKE UPDATE ON mytable FROM user1;
 
-- user1 에게 부여된 mytable 에 대한 모든 권한 회수
REVOKE ALL ON mytable FROM user1;
```


## 사용자 관리 예제

위의 쿼리를 수행한 예제와 그 결과를 나타냈다.

```sql
############################################
## Connect SYS : SYS 계정으로 접속함.
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
 
#Error: 자기 자신을 Drop 할 수 없음.
Mach> drop user SYS;
[ERR-02083 : Drop user error. You cannot drop yourself(SYS).]
 
############################################
## Connect DEMO1
############################################
Mach> connect demo1/demo1;
Connected successfully.
 
#Error: 일반 유저는 다른 사용자의 비밀번호를 바꿀 수 없다.
Mach> alter user demo2 identified by 'demo22';
[ERR-02085 : ALTER user error. The user(DEMO2) does not have ALTER privileges.]
 
Mach> alter user demo1 identified by demo11;
Altered successfully.
 
Mach> connect demo2/demo22;
Connected successfully.
 
#Error: wrong password
Mach> connect demo1/demo11234;
 [ERR-02081 : User authentication error. Invalid password (DEMO11234).]
 
## Correct password
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
## Connect SYS again
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
 
#Error: demo1 유저에 속한 테이블이 존재함.
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
