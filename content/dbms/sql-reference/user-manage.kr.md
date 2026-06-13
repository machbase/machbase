---
title : '사용자 관리'
type: docs
weight: 60
---

# Index

* [CREATE USER](#create-user)
* [DROP USER](#drop-user)
* [ALTER USER](#alter-user)
* [PASSWORD POLICY](#password-policy)
* [AUTH KEY 파일 생성](#auth-key-파일-생성)
* [AUTH KEY를 포함한 사용자 생성](#auth-key를-포함한-사용자-생성)
* [AUTH KEY 관리](#auth-key-관리)
* [AUTH KEY 메타 조회](#auth-key-메타-조회)
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

비밀번호 정책을 함께 지정하려면 다음 확장 구문을 사용합니다.

```sql
CREATE USER user_name IDENTIFIED BY password PASSWORD POLICY { NONE | LOW | HIGH }
```

예제:

```sql
CREATE USER app_user IDENTIFIED BY "Aa!StrongPwd1" PASSWORD POLICY LOW;
CREATE USER ops_user IDENTIFIED BY "Bb@StrongPwd2" PASSWORD POLICY HIGH;
```
사용자명은 생성 시 대문자로 변환되어 저장됩니다. 예를 들어 `CREATE USER app_user ...`로 생성하면
메타 테이블과 `V$` 뷰에서는 `APP_USER`로 조회됩니다. 이후 접속이나 권한 부여 구문에서도 같은 사용자명으로
처리됩니다.


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

비밀번호를 변경하면서 정책도 함께 변경할 수 있습니다.

```sql
ALTER USER user_name IDENTIFIED BY password PASSWORD POLICY { NONE | LOW | HIGH }
```

정책을 변경할 때는 새 비밀번호를 함께 지정해야 합니다. `ALTER USER user_name PASSWORD POLICY HIGH`처럼 정책만 단독으로 변경하는 구문은 허용되지 않습니다.


## PASSWORD POLICY

비밀번호 정책은 `CREATE USER`와 `ALTER USER ... IDENTIFIED BY ...`에서 비밀번호 강도를 검증하는 기능입니다. 정책을 지정하지 않으면 기존 호환성을 위해 `NONE`이 적용됩니다.

정책 종류:

- `NONE`
  - 비밀번호 강도 제약이 없습니다.
  - 비밀번호 만료 시각(`VALID_BEFORE`)은 `NULL`입니다.
- `LOW`
  - 최소 길이 10자 이상이어야 합니다.
  - 대문자, 소문자, 특수문자를 포함해야 합니다.
  - 5자리 이상 연속 숫자, 증가/감소 숫자 연번, 키보드 연속 문자열은 사용할 수 없습니다.
  - 비밀번호 만료 시각(`VALID_BEFORE`)은 `NULL`입니다.
- `HIGH`
  - `LOW` 규칙을 모두 적용합니다.
  - 현재 비밀번호와 최근 24개 이내의 과거 비밀번호를 재사용할 수 없습니다.
  - 비밀번호 설정 시점부터 90일 후로 만료 시각(`VALID_BEFORE`)이 자동 설정됩니다.

정책 적용 예:

```sql
CREATE USER user1 IDENTIFIED BY "Aa!StrongPwd1";
CREATE USER user2 IDENTIFIED BY "Bb@StrongPwd2" PASSWORD POLICY LOW;
CREATE USER user3 IDENTIFIED BY "Cc#StrongPwd3" PASSWORD POLICY HIGH;

ALTER USER user2 IDENTIFIED BY "Dd$NewPwd44";
ALTER USER user2 IDENTIFIED BY "Ee%NewPwd55" PASSWORD POLICY LOW;
ALTER USER user3 IDENTIFIED BY "Ff#NewPwd66" PASSWORD POLICY NONE;
```

주의 사항:

- `ALTER USER ... IDENTIFIED BY ...`는 해당 사용자에 저장된 정책으로 새 비밀번호를 검증합니다.
- `ALTER USER ... IDENTIFIED BY ... PASSWORD POLICY ...`는 새 정책으로 새 비밀번호를 검증합니다.
- 정책을 `HIGH`로 설정하거나 `HIGH` 사용자의 비밀번호를 변경하면 `VALID_BEFORE`가 현재 시각 기준 90일 뒤로 갱신됩니다.
- 정책을 `LOW` 또는 `NONE`으로 설정하면 `VALID_BEFORE`는 `NULL`로 갱신됩니다.
- 만료된 계정은 로그인할 수 없으므로 본인 계정으로 비밀번호를 변경할 수 없습니다. 관리자 계정에서 새 비밀번호로 리셋해야 합니다.

정책과 만료 시각은 `M$SYS_USERS`에서 확인할 수 있습니다.

```sql
SELECT USER_ID, NAME, PWD_POLICY_LEVEL, VALID_BEFORE
FROM M$SYS_USERS;
```

`PWD_POLICY_LEVEL` 값은 `0 = NONE`, `1 = LOW`, `2 = HIGH`를 의미합니다. `VALID_BEFORE`는 값이 있을 때 `YYYY-MM-DD` 형식으로 표시됩니다.
## AUTH KEY 파일 생성

> **참고**: 다음 설명은 Machbase 8.5 이상에서 지원됩니다.

AUTH KEY 인증은 클라이언트 측 개인키 파일과 Machbase 사용자에 등록된 공개키를 사용합니다.
일반적으로 `openssl`로 키 쌍을 생성하고, 개인키는 클라이언트 호스트에 보관하며, 공개키만
Machbase에 등록합니다.

지원되는 알고리즘과 키 크기는 다음과 같습니다.

| 공개키 알고리즘 | 지원 키 파라미터 | 지원 서명 스킴 | 해시 |
| --- | --- | --- | --- |
| ECDSA | P-256, P-384, P-521 | `ECDSA` | SHA-256 |
| RSA | 2048, 3072, 4096 bits | `RSA_PKCS1_V15` | SHA-256 |
| RSA | 2048, 3072, 4096 bits | `RSA_PSS` | SHA-256 |

`AUTH_SIG_SCHEME`를 생략하면 키 알고리즘에 따라 기본 스킴을 사용합니다.

- ECDSA 키: `ECDSA`
- RSA 키: `RSA_PKCS1_V15`

RSA-PSS를 사용하려면 클라이언트 접속 옵션에서 `AUTH_SIG_SCHEME=RSA_PSS`를 명시합니다.
등록된 공개키 타입과 클라이언트가 요청한 서명 스킴이 맞지 않으면 인증이 실패합니다.

ECDSA P-256 키 생성 예:

```bash
openssl ecparam -name prime256v1 -genkey -noout -out app_user_ecdsa.key
openssl ec -in app_user_ecdsa.key -pubout -out app_user_ecdsa.pub
chmod 600 app_user_ecdsa.key
```

ECDSA P-384, P-521 키 생성 예:

```bash
openssl ecparam -name secp384r1 -genkey -noout -out app_user_ecdsa_p384.key
openssl ec -in app_user_ecdsa_p384.key -pubout -out app_user_ecdsa_p384.pub

openssl ecparam -name secp521r1 -genkey -noout -out app_user_ecdsa_p521.key
openssl ec -in app_user_ecdsa_p521.key -pubout -out app_user_ecdsa_p521.pub
```

RSA 2048-bit 키 생성 예:

```bash
openssl genrsa -out app_user_rsa.key 2048
openssl rsa -in app_user_rsa.key -pubout -out app_user_rsa.pub
chmod 600 app_user_rsa.key
```

RSA 3072-bit, 4096-bit 키를 사용하려면 `openssl genrsa`의 마지막 인자를 각각 `3072`, `4096`으로 지정합니다.

공개키를 SQL에 넣을 때는 PEM 파일을 줄바꿈이 `\n`으로 이스케이프된 한 줄 문자열로
변환합니다.

```bash
awk '{printf "%s\\n", $0}' app_user_ecdsa.pub
```

명령 출력 결과를 `CREATE USER ... WITH AUTH KEY` 또는 `ALTER USER ... ADD AUTH KEY`의
`key` 값으로 사용합니다.

다음 예는 생성한 공개키로 등록 SQL 파일을 만드는 방법입니다.

```bash
KEY_ESCAPED=$(awk '{printf "%s\\n", $0}' app_user_ecdsa.pub)

cat > add_app_user_key.sql <<EOF
ALTER USER app_user ADD AUTH KEY (
    key='${KEY_ESCAPED}',
    valid_before='2047-12-31',
    comment='openssl generated ecdsa key'
);
EOF
```

## AUTH KEY를 포함한 사용자 생성

> **참고**: 다음 설명은 Machbase 8.5 이상에서 지원됩니다.

Machbase는 비밀번호 인증과 함께 공개키 기반 challenge 인증용 AUTH KEY를 사용자에 등록할 수 있습니다.

```sql
CREATE USER app_user IDENTIFIED BY 'App#1234'
WITH AUTH KEY (
    key='-----BEGIN PUBLIC KEY-----\nMFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEshxcrSmtosaqWjhRkOoAw4v3QWqL\ns3OFN2jbJrustEc12uAn/IdtTG94KK69bY7DWl80pzQ48dNL+ENXe8PT3g==\n-----END PUBLIC KEY-----\n',
    valid_before='2047-12-31',
    comment='initial key'
);
```

설명:

- `key`에는 PEM 형식 공개키를 넣습니다.
- SQL 문장 안에서는 PEM 줄바꿈을 `\n`으로 입력할 수 있습니다.
- `valid_before`는 `YYYY-MM-DD` 형식을 사용합니다.
- `valid_before`에는 시각이 포함된 datetime 형식(`YYYY-MM-DD HH24:MI:SS`)을 사용할 수 없습니다.
- `comment`는 현재 AUTH KEY 문법에서 필수입니다.
- `CREATE USER ... WITH AUTH KEY`로 생성한 첫 키는 즉시 활성 상태(`ACTIVATED=1`)로 등록됩니다.
- 사용자는 비밀번호와 AUTH KEY를 동시에 보유할 수 있습니다. 실제 인증은 클라이언트의 `AUTH_MODE` 선택에 따라 비밀번호 또는 challenge 중 하나만 수행되며, 실패 시 다른 방식으로 자동 fallback하지 않습니다.

## AUTH KEY 관리

### AUTH KEY 추가

```sql
ALTER USER app_user ADD AUTH KEY (
    key='-----BEGIN RSA PUBLIC KEY-----\nMIIBCgKCAQEAqO+tddiAQzsT8iajPy5QJPamIlyq2zB01wgHSTs3OOrvw0uKoFQD\ncqKaDzRya73LETXIEev3nwhGCnG4SjedMHj3EH9/rRJphFtv/dzw0OHum/UhVulR\nIXUYzrTbKPTQ+qyjS8UXTteMncf9OOh4AQyS4+iJW+U344fxymR8USRgZ25N9jhf\n2gkKnn5YSPZHf8ZHQGeA7OXANBwPmH5dQwfqghXRa7Nk1hmkIAnQQXCBJW/Lin+x\nwQfqv8DVwNaiziz77voPwaeD5akq1JYWvcPlOnh+NN3tpu5gudke/t/In4NFJ3W9\n4unVcYIfxcdDSoht3AMObGmuDazOjQJFGQIDAQAB\n-----END RSA PUBLIC KEY-----\n',
    valid_before='2048-01-31',
    comment='rollover candidate'
);
```

추가된 키는 즉시 활성 상태(`ACTIVATED=1`)로 생성됩니다. 롤오버 기간에는 한 사용자에 여러 활성 AUTH KEY를 둘 수 있습니다.

### AUTH KEY 활성화 / 비활성화

```sql
ALTER USER app_user DEACTIVATE AUTH KEY ID 3;
ALTER USER app_user ACTIVATE AUTH KEY ID 3;
```

- 비활성화된 키는 challenge 인증에 사용할 수 없습니다.
- 한 사용자에 여러 AUTH KEY를 보유할 수 있습니다.

### AUTH KEY 유효기간 변경

```sql
ALTER USER app_user ALTER AUTH KEY ID 3 VALID_BEFORE='2048-06-30';
```

- `VALID_BEFORE`가 지난 키는 인증에 사용할 수 없습니다.
- 입력 형식은 `YYYY-MM-DD`이며, 시각이 포함된 datetime 형식은 허용되지 않습니다.

### AUTH KEY 삭제

```sql
ALTER USER app_user DROP AUTH KEY ID 3;
```

- 삭제된 키는 즉시 인증에 사용할 수 없습니다.
- 사용자 삭제 시 해당 사용자의 AUTH KEY 메타도 함께 정리됩니다.

## AUTH KEY 메타 조회

등록된 AUTH KEY 메타는 `V$USER_AUTH_KEYS`에서 조회할 수 있습니다.

주요 컬럼:

- `KEY_ID`: AUTH KEY 식별자
- `USER_NAME`: AUTH KEY 소유 사용자
- `KEY_ALGO`: 키 알고리즘 (`RSA`, `ECDSA`)
- `KEY_PARAM`: 키 파라미터
  - RSA 키: 비트 길이 예) `2048`
  - EC 키: 곡선 이름 예) `P-256`, `P-384`, `P-521`
- `ACTIVATED`: 활성화 여부
- `VALID_AFTER`, `VALID_BEFORE`: 유효 기간
- `COMMENT`: 사용자 메모
- `PUBKEY`: PEM 형식 공개키 본문

```sql
SELECT key_id, user_name, key_algo, key_param, activated, valid_before, comment
  FROM V$USER_AUTH_KEYS
 WHERE user_name='APP_USER'
 ORDER BY key_id;
```

공개키 본문까지 확인하려면 `PUBKEY` 컬럼을 조회합니다.

```sql
SELECT key_id, user_name, pubkey
  FROM V$USER_AUTH_KEYS
 WHERE user_name='APP_USER'
 ORDER BY key_id;
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
