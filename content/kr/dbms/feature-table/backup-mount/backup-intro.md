---
title : '백업 개요'
type : docs
weight: 10
---

# BACKUP/MOUNT
데이터베이스의 영속성을 보장하기 위해서 메모리에 저장된 데이터는 최대한 빨리 Disk에 저장된다. <br/>
그리고 Process Failure와 같은 일반적인 장애상황이 발생할 경우, Restart Recovery를 통해서 데이터베이스를 Consistent한 상태로 만든다. <br/>
하지만 Power Failure나 화재에 의한 Hardware의 피해가 발생할 경우, 데이터베이스의 복구는 불가하다. 이런 문제를 해결하기 위해서 별도의 디스크나 Hardware에 데이터를 주기적으로 다른 영역에 저장하여, 유사시 해당 데이터를 이용하여 데이터를 복구하는 기능이 데이터베이스 백업과 복구 기능이다.

데이터베이스 백업은 언제 수행하느냐에 따라서 크게 두 가지로 나누어 진다.

- Offline Backup
- Online Backup


첫번째, Offline Backup 기능은 DBMS를 Shutdown하고 데이터베이스를 복사하는 기능으로 Cold Backup이라고 부르기도 한다. <br/>
매우 간단하지만, 사용자의 서비스가 중단되는 단점이 있으므로 운영 중에는 사용하는 경우가 거의 없으며 초기 테스트나 데이터 구축 시에만 사용하는 경향이 있다.

두 번째, Online Backup은 DBMS가 동작 중일 때, 데이터베이스를 Backup하는 기능으로 Hot Backup이라고 부르기도 한다. <br/>
이 기능은 서비스를 중단하지 않고 수행될 수 있어 사용자의 Service Availability를 증가시켜 대부분의 DBMS Backup은 Online Backup을 의미한다. <br/>
다른 데이터베이스의 Backup과 달리 시계열 데이터베이스인 Machbase 는 Duration Backup을 제공한다. 이는 Backup시 백업될 Database의 시간을 지정하여 원하는 시간대의 데이터만 Backup할 수 있다.

![Backup](./backup.png)

```sql
backup database into disk = 'backup';
backup database from to_date('2015-07-14 00:00:00','YYYY-MM-DD HH24:MI:SS') to to_date('2015-07-14 23:59:59 999:999:999','YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn')
                into disk = 'backup_20150714';
```
Backup된 데이터베이스는 장애 복구 과정을 거쳐서 기존 데이터베이스처럼 사용될 수 있다. 이 복구 방법을 Restore라고 한다. <br/>
이 Restore 기능은 파손된 데이터베이스를 삭제하고 백업된 데이터베이스 이미지를 Primary Database로 복구한다. 때문에 복구시 기존 데이터베이스를 삭제하고 machadmin -r 기능을 이용하여 복구한다.
```sql
machadmin -r 'backup'
```
Mount/unmount 기능은 Online으로 동작하는 기능으로 Backup된 데이터베이스를 현재 운영 중인 데이터베이스에 Attach하는 기능이다.
```sql
mount database 'backup' to mountName;
umount database mountName;
```

## Database Backup
Machbase 에서는 데이터 백업을 할 때 두 가지 옵션을 제공한다. 운영 중인 DB의 정보를 백업하는 DATABASE 백업과 필요한 Table만 선택하여 백업할 수 있는 TABLE 백업 기능을 제공한다.

DB에서 제공하는 백업 명령은 다음과 같다.

```sql
BACKUP [ DATABASE | TABLE table_name ]  [ time_duration ] INTO DISK = 'path/backup_name';
time_duration = FROM start_time TO end_time
path = 'absolute_path' or  'relative_path'
```
```sql
# Directory backup
       BACKUP DATABASE INTO DISK = 'backup_dir_name';
# Set backup duration
      - Directory backup
       BACKUP DATABASE FROM TO_DATE('2015-07-14 00:00:00','YYYY-MM-DD HH24:MI:SS')
                         TO TO_DATE('2015-07-14 23:59:59','YYYY-MM-DD HH24:MI:SS')
                         INTO DISK = '/home/machbase/backup_20150714'
```
DB 백업을 수행할 때 옵션은 백업 타입, Time duration, 경로를 입력해야 한다. DATABASE 전체를 백업할 때는 백업 타입에 DATABASE를 입력하고, 특정 Table만 백업하려면 TABLE을 입력한 후 백업하려는 Table_Name을 입력한다. <br/>
TIME_DURATION 구문은 필요한 기간의 데이터만 백업하도록 설정할 수 있다. FROM 항목에 백업을 원하는 날짜의 시작 시간을 입력하고 TO 항목에 백업의 마지막 날짜의 시간을 입력하면 그 기간의 데이터만 선택하여 백업할 수 있다. 예제 3번을 보면 TIME_DURATION 항목의 FROM에 '2015년 7월 14일 0시 0분 0초'로 설정하고 TO에 '2015년 7월 14일 23시 59분 59초'로 설정하여 2015년 7월 14일의 데이터만 백업되도록 설정하였다. <br/>
만약 DURATION 항목에 대한 정보를 입력하지 않으면 FROM 항목에는 '1970년 1월 1일 9시 0분 0초'로 설정되고 TO 항목에는 명령을 수행하는 시간으로 자동 설정된다. DURATION 절을 이용한 시간범위 백업은 TAG테이블과 TAG table을 포함한 데이터베이스에서 사용할 수가 없으며, 증분 데이터를 백업하는 기능인 INCREMENTAL BACKUP기능을 이용해야 한다.

마지막으로, 백업 수행의 결과를 저장할 저장 매체에 대한 설정이 필요하다. 디렉터리 단위로 생성하려면 DISK를 입력한다. <br/>
주의할 점은 생성물 저장되는 PATH 정보를 지정할 수 있는데 만약 상대 경로를 입력하면 현재 운영 중인 DB의 환경설정의 DB_PATH 항목에 지정된 경로에 생성된다. 만약 DB_PATH가 아닌 다른 곳에 저장하고 싶다면 '/'로 시작하는 절대 경로를 입력해야 한다.

### Incremental Backup
증분 백업이란 이전에 수행한 백업 이후에 입력된 데이터만을 백업하는 기능이다. 증분 백업이 수행되는 대상은 Log, Tag 테이블의 데이터만 해당하며 lookup 테이블은 항상 모든 데이터를 백업한다. <br/>
증분 백업을 수행하기 위해서는 이전에 수행한 증분 백업 디렉토리나 전체 백업 디렉토리가 필요하다. 증분 백업은 다음과 같이 수행한다.

```sql

Mach> BACKUP DATABASE INTO DISK = 'backup1'; /* full backup 수행 */
Executed successfully.
Mach> ...
  
Mach> BACKUP DATABASE AFTER 'backup1' INTO DISK = 'backup2'; /* backup1 이후에 입력한 데이터만 증분 백업을 수행함 */
Executed successfully.
Mach> ...
```

증분 백업은 데이터베이스 전체(이때 lookup 테이블은 전체 백업이 됨), Log 테이블, Tag table에 대해서 가능하며 RESTORE기능을 이용하여 복구할 경우 증분 백업 이전에 백업한 백업 데이터도 필요하다. 현재 데이터를 삭제하고 이전 상태로 되돌리기 싫은 경우 아래에서 설명하는 MOUNT기능을 이용하면 된다.

#### Incremental Backup 주의 사항
위와 같이 backup1을 기준으로 증분 백업으로 backup2를 만든 경우, backup1이 유실(disk failure 등의 이유)되면, backup2를 사용하여 복구할 수 없다.

같은 이유로, 증분 백업을 하였을 때 이전 백업이 유실되면 이후 백업을 사용해서 복구할 수 없다.

아래와 같이 백업을 3번 진행하면 backup3의 이전 백업은 backup2가 되고 backup2의 이전 백업은 backup1이 된다.

따라서, backup1이 유실되면 backup2 와 backup3 모두 사용할 수 없고, backup2가 유실되면 backup3를 사용하여 복구할 수 없다.

```sql
Mach> BACKUP DATABASE INTO DISK = 'backup1'; /* full backup 수행 */
Executed successfully.
Mach> ...
  
Mach> BACKUP DATABASE AFTER 'backup1' INTO DISK = 'backup2'; /* backup1 이후에 입력한 데이터만 증분 백업을 수행함 */
Executed successfully.
Mach> ...
 
Mach> BACKUP DATABASE AFTER 'backup2' INTO DISK = 'backup3'; /* backup2 이후에 입력한 데이터만 증분 백업을 수행함 */
Executed successfully.
Mach> ...
```

## Database Restore
Database Restore기능은 구문으로 제공되지 않고, Offline으로 machadmin -r 기능을 통해 복구할 수 있다. 복구전에 다음 사항을 체크해야 한다.
- Machbase 가 종료되었는가?
- 이전에 생성한 DB를 삭제하였는가?

```
machadmin -r backup_database_path;
```
```sql
backup database into disk = '/home/machbase/backup';
```
```
machadmin -k
machadmin -d
machadmin -r /home/machbase/backup;
```

## Database Mount
장애상황을 대비하여 대량의 데이터베이스를 주기적으로 Backup 하고 데이터를 계속 추가하는 경우, 다음과 같은 문제점이 발생한다.
- 데이터를 저장하기 위한 디스크 비용 증가
- 운영 중인 Machine의 물리적 Disk공간의 한계

이 문제점을 해결하기 위해서 주기적으로 현재 서비스를 위해 필요한 데이터만을 남기고 삭제를 수행한다. 그러나 과거 데이터에 대한 참조가 필요할 경우에는 Backup 된 데이터베이스를 Restore하여 참조해야 하는데, 대단히 큰 Backup Image일 경우 복구시간이 많이 걸리고 또한 별도의 장비도 필요하다. 왜냐하면 Restore기능은 현재 운영 중인 데이터베이스를 삭제해야 수행할 수 있기 때문이다. 이런 문제를 해결하기 위해서 Machbase 는 Database Mount 기능을 제공한다.

Database Mount기능은 Online으로 동작하는 기능으로 Backup된 데이터베이스를 현재 운영 중인 데이터베이스에 Attach하는 기능이다. 그리고 여러 개의 Backup Database을 운영 중인 Primary Database에 Attach하여 사용자는 여러 개의 Backup Database를 하나의 Database인 것처럼 참조 가능한다. 단 Mount한 Database에 대해서는 Read만 가능하다.

Mount DATABASE 명령은 기존에 Backup으로 생성된 데이터베이스 혹은 테이블 DATA를 현재 운영 중인 데이터베이스에서 조회 가능한 상태로 준비시켜 주는 기능이다. 그래서 Mount 된 DATABASE는 동일한 DB 명령어를 사용하여 데이터를 조회할 수 있다.

현재 Database Mount 기능의 제약 사항은 다음과 같다.
- Backup 정보는 Mount할 Database와 DB의 Major 번호와 Meta의 Major 번호가 호환 가능한 버전이어야 한다.
- Backup Data를 Mount할 경우 읽기만 가능하여 Index 생성, 데이터 입력 및 삭제 등은 지원하지 않는다.
- 현재 Mount된 DATABASE의 정보는 V$STORAGE_MOUNT_DATABASES를 조회하여 확인할 수 있다.
- 증분 백업 데이터를 mount하는 경우, 그 백업데이터에 기록된 증분 데이터만 검색되며 이전에 수행한 증분데이터를 따라가서 mount해 주지는 않는다.

### Mount
Mount 명령을 수행하기 위해서는 Backup_database_path 정보와 DatabaseName이 필요하다. Backup_database_path는 Backup 명령을 통하여 생성된 DB의 위치 정보를 입력해야 하고, DatabaseName에는 Database에 Mount 할 때 구분할 수 있는 이름을 지정한다. Backup_database_path는 Backup 할 때와 동일하게 상대 경로를 입력할 경우 DB의 환경변수에 설정된 DB_PATH에 지정된 디렉터리를 기준으로 검색한다.

```sql
MOUNT DATABASE 'backup_database_path' TO mount_name;
```
```sql
MOUNT DATABASE '/home/machbase/backup' TO mountdb;
```

### Unmount
Mount된 Database를 더 이상 사용하지 않을 경우 Umount 명령을 사용하여 제거할 수 있다.

```sql
UNMOUNT DATABASE mount_name;
```
```sql
UNMOUNT DATABASE mountdb;
```

### MOUNT DB에서 데이터 조회
Backup DB의 DATA를 조회할 때 운영 중인 DB의 DATA를 조회하는 것과 동일한 SQL문을 이용하여 조회할 수 있다.

Mount 된 DB는 운영중인 DB의 SYS 권한의 사용자만 데이터를 조회할 수 있다. 데이터를 조회하기 위해서는 조회할 TableName 앞에 MountDBName과 UserName을 입력하고, 각각의 구분자로 '.'을 붙여서 사용해야 한다. MountDBName은 현재 Mount된 DB들 중 특정 DB를 지칭하기 위해 사용하고, UserName은 Mount된 DB의 Table을 소유한 User의 정보를 지칭하는 것이다.

```sql
SELECT column_name FROM mount_name.user_name.table_name;
```
```sql
SELECT * FROM mountdb.sys.backuptable;
```

