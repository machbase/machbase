---
layout : post
title : '백업 및 복구'
type : docs
weight: 20
---

## 데이터베이스 백업

마크베이스의 데이터베이스 백업 종류는 다음과 같이 3가지로 분류할 수 있으며
백업시 모든 dbs를 백업하거나 특정 table을 선택하여 백업할 수 있다.
 - 전체백업: 입력된 전체 데이터를 백업
 - 증분백업: 전체백업에 이어 추가된 데이터를 백업
 - 기간백업: 특정 기간의 데이터를 백업

Syntax:

```sql
-- Full backup
BACKUP [ DATABASE | TABLE table_name ]  INTO [ DISK ] = 'path/backup_name';
time_duration = FROM start_time TO end_time

-- Incremental backup
BACKUP [ DATABASE | TABLE table_name ] AFTER 'previous_backup_dir' INTO [ DISK ] = 'path/backup_name';

-- Duration backup
BACKUP [ DATABASE | TABLE table_name ]  [ time_duration ] INTO [ DISK ] = 'path/backup_name';
```
path는 절대경로 또는 상대경로를 사용할 수 있다.
`time_duration`은 백업할 데이터의 시작시간과 마지막시간을 설정한다.

Example:

```sql
-- Full backup backup
BACKUP DATABASE INTO DISK = 'backup_dir_name';
 
-- Incremental backup
BACKUP DATABASE INTO DISK = 'previous_backup_dir' INTO DISK = 'path/backup_name';

-- Duration backup
BACKUP DATABASE FROM TO_DATE('2015-07-14 00:00:00','YYYY-MM-DD HH24:MI:SS')
                TO TO_DATE('2015-07-14 23:59:59','YYYY-MM-DD HH24:MI:SS')
                INTO DISK = '/home/machbase/backup_20150714'
```

백업 명령을 실행할 때 백업 타입과 백업 대상 경로를 반드시 정의하여야 한다. 전체 데이터베이스를 백업하려면 "DATABASE"를, 특정 테이블을 백업하려면 "TABLE"을 백업 타입에 지정하고, 특정 테이블을 백업할 때에는 테이블 이름을 지정하여야 한다.

DURATION 조건절을 이용하여 백업 대상을 지정할 수 있다.
백업 대상 데이터의 시작 시간과 끝 시간을 FROM 및 TO 절에서 지정한다.
위 예제에서  "2015-07-14 00:00:00" 가 FROM으로 정의되었고, "2015-07-14 23:59:59" 이 TO로 정의되었으므로, 사용자는 2015년 7월 14일의 전체 데이터를 백업하는 것이다.
duration 시간 조건절을 지정하지 않으면 "1970-01-01 00:00:00" 이 FROM으로 설정되고 실행되는 현재 시점이 TO절에 설정된다.

백업 경로를 지정할 때, 상대 경로를 지정하면 "$MACHBASE_HOME/dbs" 아래에 백업 파일들이 생성되므로 주의하여야 한다. 절대 경로를 지정하려면 항상 "/"로 시작하는 경로를 설정하여야 한다.

## 데이터베이스 복구

백업 파일에서 데이터를 복원할 수 있으며 다음과 같은 제약사항이 있다.
 - 질의 명령으로 수행할 수 없음(machadmin 명령 으로만 수행 가능)
 - 데이터베이스가 정지 상태이어야함
 - 현재 데이터가 삭제됨(현재 데이터가 더이상 사용되지 않는지 확인 필요함)
 - 증분백업인 경우 Full백업부터 마지막증분 백업까지 모든 백업 dbs가 필요함
 - TAG Table의 경우 기간백업은 복구할 수 없음

Syntax:

```bash
machadmin -r backup_database_path
```

Example:

```bash
backup database into disk = '/home/machbase/backup';

machadmin -k
machadmin -d
machadmin -r /home/machbase/backup;
```

