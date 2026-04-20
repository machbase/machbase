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

GRANT 문을 통해 사용자에게 권한을 부여하고, REVOKE 문을 통해 이미 부여된 권한을 회수합니다.

기본 예제:

```sql
-- user1에게 mytable에 대한 SELECT 권한 부여
GRANT SELECT ON mytable TO user1;

-- user1에게 mytable에 대한 모든 권한 부여
GRANT ALL ON mytable TO user1;
```

```sql
-- user1에게 부여된 mytable에 대한 UPDATE 권한 취소
REVOKE UPDATE ON mytable FROM user1;

-- user1에게 부여된 mytable에 대한 모든 권한 취소
REVOKE ALL ON mytable FROM user1;
```

### 테이블 권한

테이블에 대한 권한을 부여할 때는 다음과 같이 사용합니다.

- `table`
- `user.table`
- `db.user.table`

권한 종류:

- `SELECT`
- `INSERT`
- `DELETE`
- `UPDATE`
- `ALL`

예제:

```sql
GRANT SELECT ON sensor_log TO reader;
GRANT SELECT, INSERT ON sys.sensor_log TO writer;
REVOKE INSERT ON sys.sensor_log FROM writer;
GRANT ALL ON machbasedb.sys.sensor_log TO app_user;
```

### Machbase 8.5 이상: 데이터베이스 권한

> **참고**: 다음 설명은 Machbase 8.5 이상에서 지원됩니다.

Machbase 8.5 이상에서는 `MACHBASEDB`를 대상으로 데이터베이스 범위 권한을 부여할 수 있습니다.

```sql
GRANT CREATE ON machbasedb TO ddl_user;
GRANT DROP ON machbasedb TO ddl_user;
GRANT ALTER ON machbasedb TO ops_user;
GRANT BACKUP ON machbasedb TO backup_user;
GRANT MOUNT ON machbasedb TO mount_user;
GRANT DDL ON machbasedb TO deploy_user;
GRANT ALL ON machbasedb TO admin_user;
```

데이터베이스 범위에서 사용할 수 있는 권한:

- `CREATE`
- `DROP`
- `ALTER`
- `MOUNT`
- `BACKUP`
- `DDL`
- `ALL`

여기서 `DDL`은 `CREATE + DROP` 묶음입니다.

### `ALL`의 의미

> **참고**: 다음 설명은 Machbase 8.5 이상에서 지원됩니다.

`ALL`은 항상 같은 뜻이 아닙니다. 대상에 따라 의미가 달라집니다.

- `GRANT ALL ON machbasedb TO user1`
  - 데이터베이스 범위 전체 권한을 부여합니다.
- `GRANT ALL ON sys.table1 TO user1`
  - 해당 테이블에 대한 전체 DML 권한을 부여합니다.

즉, `MACHBASEDB`에 대한 `ALL`과 테이블에 대한 `ALL`은 같은 문법이지만 용도가 다릅니다.

### 데이터베이스 이름에 직접 DML 권한을 부여할 수 없는 경우

> **참고**: 다음 설명은 Machbase 8.5 이상에서 지원됩니다.

다음과 같이 데이터베이스 이름 `MACHBASEDB`에 `SELECT`, `INSERT`, `DELETE`, `UPDATE`를 직접 부여하는 방식은 사용할 수 없습니다.

```sql
GRANT SELECT ON machbasedb TO user1;
GRANT INSERT ON machbasedb TO user1;
REVOKE DELETE ON machbasedb FROM user1;
REVOKE UPDATE ON machbasedb FROM user1;
```

이 경우에는 다음과 같은 오류가 발생합니다.

```sql
[ERR-02186: Invalid database name.]
```

조회나 입력 권한을 주려면 반드시 테이블을 지정해야 합니다.

```sql
GRANT SELECT ON sys.sensor_log TO user1;
GRANT INSERT ON sys.sensor_log TO user1;
```

### 데이터베이스 대상 이름은 `MACHBASEDB`를 사용

> **참고**: 다음 설명은 Machbase 8.5 이상에서 지원됩니다.

데이터베이스 범위 권한을 부여할 때는 `MACHBASEDB`를 사용합니다.

```sql
GRANT BACKUP ON machbasedb TO backup_user;
REVOKE BACKUP ON machbasedb FROM backup_user;
```

잘못된 데이터베이스 이름을 지정하면 오류가 발생합니다.

```sql
GRANT BACKUP ON typo TO backup_user;
```

```sql
[ERR-02186: Invalid database name.]
```

### 데이터베이스 권한이 필요한 작업

> **참고**: 다음 설명은 Machbase 8.5 이상에서 지원됩니다.

다음 작업은 테이블 권한이 아니라 `MACHBASEDB`에 대한 데이터베이스 권한이 필요합니다.

- `CREATE TABLE`, `DROP TABLE`
- `CREATE VIEW`, `DROP VIEW`
- `CREATE INDEX`, `DROP INDEX`
- `CREATE ROLLUP`, `DROP ROLLUP`
- `CREATE TABLESPACE`, `DROP TABLESPACE`
- `CREATE RETENTION`, `DROP RETENTION`
- `ALTER SYSTEM`
- `BACKUP DATABASE`
- `MOUNT DATABASE`, `UNMOUNT DATABASE`

예를 들어 일반 사용자가 `CREATE VIEW`를 실행하려면 다음과 같이 `CREATE` 권한을 부여해야 합니다.

```sql
GRANT CREATE ON machbasedb TO user1;
```

### 사용자 생성 시 기본 권한

사용자를 생성하면 기본적으로 다음 권한을 가집니다.

- `SELECT`
- `INSERT`
- `DELETE`
- `UPDATE`
- `CREATE`
- `DROP`

다음 권한은 기본 권한에 포함되지 않으므로 필요할 때 명시적으로 부여해야 합니다.

- `ALTER`
- `MOUNT`
- `BACKUP`

### 권한과 테이블 유형 제약은 별개

권한이 있어도 테이블 유형 자체의 제약은 그대로 적용됩니다.

- `LOG`, `TAG` 테이블은 제품 특성상 `UPDATE`를 사용할 수 없습니다.
- `VOLATILE`, `LOOKUP` 테이블은 모든 DML을 사용할 수 있지만, 조회/수정/삭제 시 `WHERE` 절은 기본키 기반으로 작성해야 합니다.

즉, 권한을 부여한다고 해서 지원하지 않는 DML이 가능해지는 것은 아닙니다.

### 자주 사용하는 권한 부여 예제

```sql
-- 특정 테이블 조회만 허용
GRANT SELECT ON sys.sensor_log TO reader;

-- 특정 테이블 조회와 입력 허용
GRANT SELECT, INSERT ON sys.sensor_log TO writer;

-- 일반 사용자에게 DDL만 허용
GRANT DDL ON machbasedb TO deploy_user;

-- ALTER SYSTEM 허용
GRANT ALTER ON machbasedb TO ops_user;

-- 백업 허용
GRANT BACKUP ON machbasedb TO backup_user;

-- 마운트/언마운트 허용
GRANT MOUNT ON machbasedb TO mount_user;
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
