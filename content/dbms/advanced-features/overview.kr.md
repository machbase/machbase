---
title : 백업 개요
type : docs
weight: 10
---

## BACKUP/MOUNT의 개념

데이터베이스의 영속성을 보장하기 위해 메모리에 저장된 데이터를 가능한 빨리 디스크에 저장합니다. 프로세스 실패와 같은 일반적인 장애의 경우 재시작 복구를 통해 데이터베이스의 일관성을 유지합니다. 그러나 정전이나 화재로 인한 하드웨어 손상의 경우 데이터베이스 복구가 불가능합니다. 이러한 문제를 해결하기 위해 데이터베이스 백업 및 복구 기능은 데이터를 주기적으로 다른 영역의 다른 디스크나 하드웨어에 저장하고 비상시 해당 데이터를 사용하여 데이터를 복구합니다.

데이터베이스 백업은 수행 시점에 따라 두 가지 유형으로 나뉩니다.
* 오프라인 백업
* 온라인 백업

첫째, 오프라인 백업 기능은 DBMS를 종료하고 데이터베이스를 복사하기 때문에 콜드 백업이라고 합니다. 매우 간단하지만 사용자의 서비스가 중단된다는 단점이 있습니다. 따라서 운영 중에는 거의 사용되지 않으며 초기 테스트나 데이터 구축 시에만 사용되는 경향이 있습니다.

둘째, 온라인 백업은 DBMS가 실행 중일 때 데이터베이스를 백업하는 기능으로 핫 백업이라고 합니다. 이 기능은 서비스를 중단하지 않고 수행할 수 있어 사용자의 서비스 가용성을 높입니다. 대부분의 DBMS 백업은 온라인 백업을 의미합니다. 시계열 데이터베이스인 Machbase는 다른 데이터베이스 백업과 달리 시간 범위 백업을 제공합니다. 이를 통해 백업 시 백업할 데이터베이스의 시간을 지정하여 원하는 시간의 데이터만 백업할 수 있습니다.

![overview1](/dbms/advanced-features/overview1.png)

```sql
backup database into disk = 'backup';
backup database from to_date('2015-07-14 00:00:00','YYYY-MM-DD HH24:MI:SS') to to_date('2015-07-14 23:59:59 999:999:999','YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn')
                into disk = 'backup_20150714';
```

백업된 데이터베이스는 복구 프로세스를 통해 기존 데이터베이스로 사용할 수 있습니다. 이러한 복구 방법을 복원(Restore)이라고 합니다. 이 복원 기능은 손상된 데이터베이스를 삭제하고 백업된 데이터베이스 이미지를 주 데이터베이스로 복원합니다. 따라서 복구할 때는 기존 데이터베이스를 삭제하고 machadmin -r을 사용하여 복원합니다.

```bash
machadmin -r 'backup'
```

마운트/언마운트 기능은 백업된 데이터베이스를 현재 실행 중인 데이터베이스에 연결하는 온라인 기능입니다.

```sql
mount database 'backup' to mountName;
umount database mountName;
```

## 데이터베이스 백업

Machbase는 데이터 백업을 위한 두 가지 옵션을 제공합니다. 실행 중인 DB의 정보를 백업하는 DATABASE 백업 기능과 필요한 테이블만 선택하여 백업할 수 있는 TABLE 백업 기능을 제공합니다.
DB에서 제공하는 백업 명령은 다음과 같습니다.

```bash
BACKUP [ DATABASE | TABLE table_name ]  [ time_duration ] INTO DISK = 'path/backup_name';
time_duration = FROM start_time TO end_time
path = 'absolute_path' or  'relative_path'
```

```
-- 디렉토리 백업
BACKUP DATABASE INTO DISK = 'backup_dir_name';

-- 시간 범위 백업
BACKUP DATABASE FROM TO_DATE('2015-07-14 00:00:00','YYYY-MM-DD HH24:MI:SS')
                     TO TO_DATE('2015-07-14 23:59:59','YYYY-MM-DD HH24:MI:SS')
                     INTO DISK = '/home/machbase/backup_20150714'
```

DB 백업을 수행할 때 백업 타입, 시간 기간, 경로를 옵션으로 입력해야 합니다. DATABASE 전체를 백업할 때는 백업 타입으로 DATABASE를 입력합니다. 특정 테이블만 백업하려면 TABLE을 입력한 다음 백업할 테이블의 이름을 입력합니다. `time_duration` 절을 설정하여 필요한 기간의 데이터만 백업할 수 있습니다. FROM 필드에는 백업하려는 날짜의 시작 시간을 입력하고 TO 필드에는 마지막 날짜의 시간을 입력합니다. 예제 2에서는 `time_duration`이 FROM은 "2014년 7월 14일 0시 0분 0초"로, TO는 "2015년 7월 14일 23시 59분 59초"로 설정되어 14일간의 데이터만 백업하도록 설정되어 있습니다. `time_duration`을 지정하지 않으면 FROM 항목은 '1970년 1월 1일 9시 0분 0초'로 설정되고 TO 항목은 명령을 실행하는 시간으로 자동 설정됩니다.


마지막으로 백업 결과를 저장할 저장 매체를 구성해야 합니다. 백업을 단일 파일로 생성하려면 생성 타입을 IBFILE로 설정하거나 디렉토리 단위로 생성하려면 DISK를 입력합니다. 제품을 저장할 PATH 정보를 지정할 수 있습니다. 상대 경로를 입력하면 현재 DB 구성의 DB_PATH 항목에 지정된 경로에 생성됩니다. DB_PATH 이외의 위치에 저장하려면 '/'로 시작하는 절대 경로를 입력해야 합니다.


### 증분 백업

증분 백업은 이전 백업 이후 입력된 데이터만 백업하는 기능입니다. 증분 백업의 대상은 로그 및 태그 테이블의 데이터만이며, 룩업 테이블은 항상 모든 데이터를 백업합니다.
증분 백업을 수행하려면 이전에 수행한 증분 백업 디렉토리 또는 전체 백업 디렉토리가 필요합니다.
증분 백업은 다음과 같이 수행됩니다.

```sql
Mach> BACKUP DATABASE INTO DISK = 'backup1'; /* 전체 백업 실행 */
Executed successfully.
Mach> ...

Mach> BACKUP DATABASE AFTER 'backup1' INTO DISK = 'backup2'; /* backup1 이후 삽입된 데이터에 대한 증분 백업 실행 */
Executed successfully.
Mach> ...
```

증분 백업은 전체 데이터베이스(이때 룩업 테이블은 전체 백업이 됨), 로그 테이블, 태그 테이블에 사용할 수 있습니다. RESTORE 기능으로 백업하려면 증분 백업 전에 저장된 백업 데이터가 필요합니다.
현재 데이터를 삭제하지 않고 이전 상태로 돌아가려면 아래에 설명된 MOUNT 기능을 사용할 수 있습니다.


### 증분 백업 시 주의사항

위와 같이 backup1을 기반으로 backup2가 증분 백업으로 생성된 경우 backup1이 손실되면(디스크 장애 등으로 인해) backup2를 사용하여 복원할 수 없습니다.

같은 이유로 증분 백업 후 이전 백업이 손실되면 이후 백업을 사용하여 복원할 수 없습니다.

아래와 같이 백업을 3번 수행하면 backup3의 이전 백업은 backup2가 되고 backup2의 이전 백업은 backup1이 됩니다.

따라서 backup1이 손실되면 backup2와 backup3 모두 사용할 수 없으며, backup2가 손실되면 backup3을 사용하여 복구할 수 없습니다.

```sql
Mach> BACKUP DATABASE INTO DISK = 'backup1'; /* 전체 백업 실행 */
Executed successfully.
Mach> ...

Mach> BACKUP DATABASE AFTER 'backup1' INTO DISK = 'backup2'; /* backup1 이후 삽입된 데이터에 대한 증분 백업 실행 */
Executed successfully.
Mach> ...

Mach> BACKUP DATABASE AFTER 'backup2' INTO DISK = 'backup3'; /* backup2 이후 삽입된 데이터에 대한 증분 백업 실행 */
Executed successfully.
Mach> ...
```


## 데이터베이스 복원

데이터베이스 복원 기능은 구문으로 제공되지 않으며 machadmin -r을 사용하여 오프라인으로 복구할 수 있습니다. 복원 전에 다음을 확인해야 합니다.

* Machbase가 종료되었습니까?
* 이전에 생성된 DB가 삭제되었습니까?

```bash
machadmin -r backup_database_path;
```

```sql
backup database into disk = '/home/machbase/backup';
```

```bash
machadmin -k
machadmin -d
machadmin -r /home/machbase/backup;
```


## 데이터베이스 마운트

대량의 데이터베이스를 주기적으로 백업하고 시스템 장애에 대비하여 데이터를 지속적으로 추가하면 다음과 같은 문제가 발생합니다.

* 데이터 저장을 위한 디스크 비용 증가
* 실행 중인 머신의 물리적 디스크 공간 제한

이러한 문제를 해결하기 위해 현재 서비스에 필요한 데이터만 남기고 주기적으로 삭제를 수행합니다. 그러나 과거 데이터를 참조해야 하는 경우 백업된 데이터베이스를 복원해야 합니다. 매우 큰 백업 이미지의 경우 복구 시간이 오래 걸리고 추가 장비가 필요합니다. 이는 복원 기능이 현재 실행 중인 데이터베이스를 삭제해야만 수행될 수 있기 때문입니다. 이 문제를 해결하기 위해 Machbase는 데이터베이스 마운트 기능을 제공합니다.

데이터베이스 마운트 기능은 백업된 데이터베이스를 현재 실행 중인 데이터베이스에 연결하는 온라인 기능입니다. 여러 백업 데이터베이스를 주 데이터베이스에 연결하면 사용자는 여러 백업 데이터베이스를 마치 하나의 데이터베이스인 것처럼 참조할 수 있습니다. 마운트된 데이터베이스는 읽기 전용입니다.

MOUNT DATABASE 명령은 백업으로 생성된 데이터베이스 또는 테이블 데이터를 현재 실행 중인 데이터베이스에서 볼 수 있는 상태로 준비하는 기능입니다. 따라서 마운트된 DATABASE는 동일한 DB 명령을 사용하여 데이터를 쿼리할 수 있습니다.

현재 데이터베이스 마운트 기능 제한 사항은 다음과 같습니다.

* 백업 정보는 마운트할 데이터베이스, DB 메이저 번호, 메타 메이저 번호와 호환되어야 합니다.
* 백업 데이터를 마운트할 때는 읽기 전용이며 인덱스 생성, 데이터 삽입 또는 삭제를 지원하지 않습니다.
* 현재 마운트된 DATABASE에 대한 정보는 V$STORAGE_MOUNT_DATABASES를 쿼리하여 확인할 수 있습니다.
* 증분 백업 데이터가 마운트되면 백업 데이터에 기록된 증분 데이터만 검색되며 이전에 수행한 증분 데이터를 따라가며 마운트하지 않습니다.


### 마운트

마운트 명령을 실행하려면 Backup_database_path 정보와 DatabaseName이 필요합니다. Backup_database_path는 백업 명령으로 생성된 DB의 위치 정보입니다. DatabaseName은 데이터베이스에 마운트할 때 구별할 수 있는 이름입니다. Backup_database_path는 백업을 수행할 때와 마찬가지로 상대 경로를 입력하면 DB의 환경 변수에 설정된 DB_PATH에 지정된 디렉토리를 기준으로 검색됩니다.

```sql
MOUNT DATABASE 'backup_database_path' TO mount_name;
MOUNT DATABASE '/home/machbase/backup' TO mountdb;
```


### 언마운트

마운트된 데이터베이스를 더 이상 사용하지 않을 경우 언마운트 명령을 사용하여 제거할 수 있습니다.

```sql
UNMOUNT DATABASE mount_name;
UNMOUNT DATABASE mountdb;
```

### MOUNT DB 데이터 조회

백업 DB의 데이터를 쿼리할 때 운영 중인 DB의 데이터를 쿼리할 때와 동일한 SQL 문을 사용하여 조회할 수 있습니다.

마운트된 DB는 운영 중인 DB의 SYS 관리자 사용자만 데이터를 조회할 수 있습니다. 데이터를 조회하려면 쿼리할 TableName 앞에 MountDBName과 UserName을 넣고 각 구분 기호로 '.'를 사용해야 합니다. MountDBName은 현재 마운트된 DB 중 특정 DB를 참조하는 데 사용되며, UserName은 마운트된 DB 테이블을 소유한 사용자의 정보를 참조합니다.

```sql
SELECT column_name FROM mount_name.user_name.table_name;
```

```sql
SELECT * FROM mountdb.sys.backuptable;
```
