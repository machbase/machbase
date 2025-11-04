---
title : 백업과 복원
type : docs
weight: 20
---

## 데이터베이스 백업

Machbase의 데이터베이스 백업은 다음과 같이 분류되며, 전체 데이터베이스 백업 또는 특정 테이블 백업이 가능합니다.
  - 전체 백업: 전체 데이터의 백업
  - 증분 백업: 전체 백업 또는 이전 증분 백업 이후에 추가된 데이터의 백업
  - 기간 백업: 특정 기간 동안의 데이터 백업

구문:

```sql
# 전체 백업
BACKUP [ DATABASE | TABLE table_name ]  INTO [ DISK ] = 'path/backup_name';
time_duration = FROM start_time TO end_time

# 증분 백업
BACKUP [ DATABASE | TABLE table_name ] AFTER 'previous_backup_dir' INTO [ DISK ] = 'path/backup_name';

# 기간 백업
BACKUP [ DATABASE | TABLE table_name ]  [ time_duration ] INTO [ DISK ] = 'path/backup_name';
```
경로는 절대 경로와 상대 경로를 모두 사용할 수 있습니다.
time_duration에는 백업 데이터의 시작 시간과 종료 시간을 설정합니다.

예제:

```sql
-- 전체 백업
BACKUP DATABASE INTO DISK = 'backup_dir_name';

-- 증분 백업
BACKUP DATABASE INTO DISK = 'previous_backup_dir' INTO DISK = 'path/backup_name';

-- 시간 범위 백업
BACKUP DATABASE FROM TO_DATE('2015-07-14 00:00:00','YYYY-MM-DD HH24:MI:SS')
                TO TO_DATE('2015-07-14 23:59:59','YYYY-MM-DD HH24:MI:SS')
                INTO DISK = '/home/machbase/backup_20150714'
```

백업 명령을 실행할 때는 백업 타입과 백업 대상 경로를 정의해야 합니다. 전체 데이터베이스를 백업하려면 "DATABASE"를 지정해야 합니다. 특정 테이블을 백업하려면 백업 타입으로 "TABLE"을 지정합니다. 특정 테이블을 백업할 때는 테이블 이름을 지정해야 합니다.

`time_duration` 절을 사용하여 백업 대상을 지정할 수 있습니다. FROM 및 TO 절에 백업 대상 데이터의 시작 시간과 종료 시간을 지정합니다. 위의 예제에서는 FROM에 "2015-07-14 00:00:00"을, TO에 "2015-07-14 23:59:59"를 정의했으므로, 사용자는 2015년 7월 14일의 모든 데이터를 백업할 수 있습니다. 시간 조건을 지정하지 않으면 FROM은 "1970-01-01 00:00:00"으로 설정되고 TO 절에는 실행 시점의 현재 시간이 설정됩니다.

백업 경로를 지정할 때 상대 경로를 지정하면 "$MACHBASE_HOME/dbs" 아래에 백업 파일이 생성됩니다. 절대 경로를 지정하려면 항상 "/"로 시작하는 경로를 설정해야 합니다.


## 데이터베이스 복원

백업 파일로부터 데이터를 복원할 수 있으며 다음과 같은 제약 사항이 있습니다.
* 쿼리 명령을 통해 실행할 수 없습니다('machadmin' 명령을 사용해서만 수행할 수 있습니다).
* 데이터베이스가 중지된 상태여야 합니다.
* 복원 후 현재 데이터가 삭제됩니다(현재 데이터가 더 이상 사용되지 않는지 확인이 필요합니다).
* 증분 백업의 경우 이전 전체 백업 및 증분 백업 파일이 필요합니다.
* 태그 테이블의 경우 시간 범위 백업의 복원은 지원되지 않습니다.

구문:

```bash
machadmin -r backup_database_path
```

예제:

```bash
backup database into disk = '/home/machbase/backup';

machadmin -k
machadmin -d
machadmin -r /home/machbase/backup;
```
