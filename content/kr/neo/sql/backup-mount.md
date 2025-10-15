---
title: 백업과 마운트
type: docs
weight: 61
---

## 소개

산업 현장의 센서 데이터는 “산업용 빅데이터”, “Smart-X”와 같은 이름으로 불릴 만큼 기하급수적으로 증가하고 있습니다. 방대한 시계열 데이터를 지속적으로 저장하려면 데이터 보관, 재해 복구, 과거 데이터 분석을 위한 견고한 메커니즘이 필수입니다. 그러나 전통적인 백업/복구 방식은 백업 범위를 유연하게 조절하기 어렵고, 복구에 시간이 많이 걸리며, 전체 복구를 수행하기 전에는 백업 데이터를 조회할 수 없다는 한계가 있습니다.

Machbase는 이러한 문제를 해결하기 위해 시계열 워크로드에 특화된 **백업(Backup)** 과 **마운트(Mount)** 기능을 제공합니다. 전체·증분·시간 범위·테이블 단위 백업을 지원하며, 특히 시간 소모가 큰 복구 과정 없이 백업 데이터를 즉시 읽기 전용으로 부착할 수 있는 마운트 기능이 핵심입니다.

## 핵심 개념

* **Backup**: 데이터베이스 전체 혹은 특정 테이블/시간 범위를 외부 스토리지에 물리적으로 복사합니다. Machbase 백업은 데이터와 메타데이터 파일이 포함된 디렉터리 구조로 저장됩니다.
* **Restore**: 백업 데이터를 다시 실행 중인 Machbase 인스턴스로 복사합니다. 기존 데이터를 덮어쓰므로 주로 재해 복구나 복제 환경 구축에 사용합니다.
* **Mount**: 백업 디렉터리를 실행 중인 Machbase 인스턴스에 읽기 전용 데이터베이스로 연결합니다. 복구 없이도 백업 시점의 “화석화된” 데이터를 즉시 조회할 수 있습니다.
* **Unmount**: 마운트된 백업 데이터를 분리합니다. 백업 파일 자체는 삭제하지 않습니다.
* **Live Data**: 현재 운영 중인 Machbase 인스턴스의 실시간 데이터입니다.
* **Fossilized Data**: 백업에 포함된 특정 시점(또는 기간)의 불변 데이터입니다. 마운트하면 읽기 전용으로 접근할 수 있습니다.

## 백업 작업

Machbase는 다양한 백업 범위와 유형을 제공하여 요구 사항에 맞게 세밀하게 제어할 수 있습니다.

### 전체 백업 (데이터베이스 또는 테이블)

실행 시점의 전체 데이터베이스 또는 지정 테이블을 통째로 복사합니다.

```sql
BACKUP DATABASE INTO DISK = 'path/to/backup_directory_name';

BACKUP TABLE table_name INTO DISK = 'path/to/backup_directory_name';
```

- `DATABASE`: 데이터베이스 전체를 백업합니다.
- `TABLE table_name`: 지정한 테이블만 백업합니다.
- `INTO DISK = '경로'`: 백업 파일이 생성될 대상 디렉터리를 지정합니다. 절대 경로 또는 `$MACHBASE_HOME/dbs` 기준 상대 경로를 사용할 수 있으며, 존재하지 않으면 자동 생성됩니다.

**참고 사항**
- 백업 실행 시점의 데이터를 캡처합니다.
- 결과물은 다수의 파일과 하위 디렉터리로 구성된 디렉터리입니다.

### 증분 백업 (데이터베이스 또는 테이블)

이전 백업(보통 전체 백업 또는 직전 증분 백업) 이후 변경된 데이터만 캡처합니다. 이후 백업의 시간과 저장 공간을 크게 줄일 수 있습니다.

```sql
BACKUP DATABASE AFTER 'path/to/previous_backup' INTO DISK = 'path/to/incremental_backup_dir';

BACKUP TABLE table_name AFTER 'path/to/previous_backup' INTO DISK = 'path/to/incremental_backup_dir';
```

- `AFTER '경로'`: 백업 체인의 *직전* 백업(전체 또는 증분) 디렉터리 경로를 지정합니다. 반드시 존재해야 합니다.
- `INTO DISK = '경로'`: 새 증분 백업이 저장될 대상 디렉터리를 지정합니다.

**참고 사항**
- 주로 로그(Log) 테이블과 태그(Tag) 테이블처럼 append 작업이 많은 경우에 적합합니다.
- Lookup 테이블은 변경 방식이 다양하므로 증분 백업이라도 항상 전체 백업 방식으로 처리됩니다.
- 직전 백업 디렉터리가 온전하게 존재해야 합니다.

### 시간 범위 백업 (데이터베이스 또는 테이블)

특정 기간의 데이터를 백업할 수 있습니다. 시계열 데이터의 기간별 아카이빙에 유용합니다.

```sql
BACKUP DATABASE
    FROM time_expression_start
    TO time_expression_end
    INTO DISK = 'path/to/backup_directory_name';

BACKUP TABLE table_name
    FROM time_expression_start
    TO time_expression_end
    INTO DISK = 'path/to/backup_directory_name';
```

- `FROM time_expression_start`: 백업 시작 시각(포함)을 지정합니다. 예: `TO_DATE('YYYY-MM-DD HH24:MI:SS', ...)`
- `TO time_expression_end`: 백업 종료 시각(포함)을 지정합니다.

### 테이블을 디스크로 백업할 때의 파일 구조

| 경로/파일명             | 설명                                                          |
|:------------------------|:--------------------------------------------------------------|
| `<path>/backup.mbf`     | 백업 파일 매니페스트(제목/설명 파일)                          |
| `<path>/backup.sql`     | 테이블 구조(DDL) 및 메타데이터 정보                          |
| `<path>/data/`          | 테이블 데이터 파일                                             |
| `<path>/index/`         | 인덱스 파일 (Tag 테이블의 경우 시계열 인덱스 포함)            |

## 마운트(Mount) 작업

마운트 작업을 통해 백업 디렉터리를 읽기 전용 데이터베이스로 연결합니다. 복구 없이도 즉시 조회가 가능합니다.

### 백업 마운트

```sql
MOUNT DATABASE '/path/to/backup_directory' TO mount_name;
```

- `'/path/to/backup_directory'`: 마운트할 백업 디렉터리 경로입니다.
- `mount_name`: 마운트 시 사용할 별칭입니다. 마운트된 데이터는 `mount_name.스키마.테이블` 형식으로 조회합니다.

### 마운트 예시

```sql
MOUNT DATABASE '/backup/jan_data' TO backup_jan;

-- 마운트한 데이터 조회
SELECT COUNT(*) FROM backup_jan.sys.sensor_data;
SELECT * FROM backup_jan.sys.sensor_data
 WHERE time BETWEEN TO_DATE('2024-01-05') AND TO_DATE('2024-01-06');
```

### 마운트 해제

```sql
UNMOUNT DATABASE mount_name;
```

마운트를 해제하면 더 이상 해당 백업 데이터를 조회할 수 없습니다. 백업 파일 자체는 삭제되지 않습니다.

## 복구(Restoration) 작업

복구는 백업된 데이터를 실행 중인 데이터베이스로 되돌려놓는 과정입니다. 기존 데이터를 덮어쓰므로 주의가 필요합니다.

```bash
machbase-neo restore --data <machbase_home_dir> <path/to/backup_directory>
```

- `--data <machbase_home_dir>`: 복구 대상으로 사용할 `$MACHBASE_HOME` 디렉터리를 지정합니다.
- `<path/to/backup_directory>`: 복구할 백업 디렉터리 경로입니다.
  - 전체 복구일 경우 전체 백업 디렉터리 경로를 지정합니다.
  - 증분 백업을 포함해 복구할 경우 **마지막 증분 백업** 디렉터리를 지정하면 이전 백업을 자동으로 찾아 처리합니다.

**주의 사항**
- 복구는 기존 데이터를 덮어쓰므로 운영 중인 인스턴스에 적용할 때는 주의해야 합니다.
- 백업 데이터를 수정하려면 반드시 복구가 필요합니다. 마운트는 읽기 전용입니다.

## 마운트의 장점과 유의사항

### 장점

- **빠른 접근성**: 복구 없이도 백업 데이터에 즉시 접근할 수 있어 TB 단위 데이터도 빠르게 확인할 수 있습니다.
- **인덱스 보존**: 백업에 포함된 시계열 인덱스를 그대로 활용하므로 마운트한 데이터도 빠르게 조회할 수 있습니다.
- **롤업(Rollup) 구조 유지**: 백업 시점의 롤업 테이블도 함께 보존되어 라이브 데이터와 동일한 방식으로 통계 분석이 가능합니다.
- **온라인 작업**: 마운트/언마운트는 운영 데이터베이스를 중단하지 않고 수행할 수 있습니다.
- **자원 효율성**: 단순 조회를 위해 전체 복구에 필요한 디스크 I/O, CPU 자원을 소비하지 않아도 됩니다.

### 유의사항

- **읽기 전용**: 마운트된 데이터베이스는 읽기 전용입니다. 변경하려면 `RESTORE`가 필요합니다.
- **통계 뷰 제공 여부**: 실시간 통계 뷰(`v$...`)는 마운트된 정적 데이터에 적용되지 않을 수 있습니다. 필요한 정보는 직접 질의하십시오.
- **파일 시스템 권한**: 마운트하려면 Machbase 서버 프로세스가 백업 디렉터리에 읽기 권한을 가져야 합니다.

## 활용 예시

태그 테이블 `EQPT_A`, `EQPT_B`가 있고 2024-01-01부터 2024-06-30까지 데이터가 저장되어 있다고 가정합니다.

```sql
CREATE TAG TABLE IF NOT EXISTS EQPT_A (
    name VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
) tag_partition_count=1;

CREATE TAG TABLE IF NOT EXISTS EQPT_B (
    name VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
) tag_partition_count=1;

SELECT TO_CHAR(MIN(time)), TO_CHAR(MAX(time)) FROM EQPT_A;
SELECT COUNT(*) FROM EQPT_A;
```

### 예제 1: 전체 데이터베이스 백업 및 마운트

```sql
BACKUP DATABASE INTO DISK = '/backup/full_db_20240630';
MOUNT DATABASE '/backup/full_db_20240630' TO mount_fulldb;

SELECT TO_CHAR(MIN(time)), TO_CHAR(MAX(time)) FROM mount_fulldb.sys.EQPT_A;
SELECT COUNT(*) FROM mount_fulldb.sys.EQPT_A;
SELECT name, TO_CHAR(time), value FROM mount_fulldb.sys.EQPT_B LIMIT 5;

UNMOUNT DATABASE mount_fulldb;
```

### 예제 2: 기간별 데이터베이스 백업 및 마운트

```sql
BACKUP DATABASE
    FROM TO_DATE('2024-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
    TO TO_DATE('2024-03-31 23:59:59', 'YYYY-MM-DD HH24:MI:SS')
    INTO DISK = '/backup/db_2024Q1';

DELETE FROM EQPT_A BEFORE TO_DATE('2024-03-31 23:59:59', 'YYYY-MM-DD HH24:MI:SS');
DELETE FROM EQPT_B BEFORE TO_DATE('2024-03-31 23:59:59', 'YYYY-MM-DD HH24:MI:SS');
SELECT COUNT(*) FROM EQPT_A;

MOUNT DATABASE '/backup/db_2024Q1' TO mount_q1;

SELECT COUNT(*) FROM mount_q1.sys.EQPT_A;
SELECT TO_CHAR(MIN(time)), TO_CHAR(MAX(time)) FROM mount_q1.sys.EQPT_A;

SELECT COUNT(*) AS live_count FROM EQPT_A;
SELECT COUNT(*) AS mounted_q1_count FROM mount_q1.sys.EQPT_A;

UNMOUNT DATABASE mount_q1;
```

### 예제 3: 테이블 단위 기간 백업 및 마운트

```sql
BACKUP TABLE EQPT_A
    FROM TO_DATE('2024-04-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
    TO TO_DATE('2024-05-15 23:59:59', 'YYYY-MM-DD HH24:MI:SS')
    INTO DISK = '/backup/eqpta_20240401_20240515';

MOUNT DATABASE '/backup/eqpta_20240401_20240515' TO mount_eqpta_partial;

SELECT TO_CHAR(MIN(time)), TO_CHAR(MAX(time)) FROM mount_eqpta_partial.sys.EQPT_A;
SELECT COUNT(*) FROM mount_eqpta_partial.sys.EQPT_A;
SELECT name, TO_CHAR(time), value FROM mount_eqpta_partial.sys.EQPT_A LIMIT 5;

UNMOUNT DATABASE mount_eqpta_partial;
```

### 예제 4: 여러 백업을 동시에 마운트

```sql
MOUNT DATABASE '/backup/db_2024Q1' TO mount_q1;
MOUNT DATABASE '/backup/full_db_20240630' TO mount_jun30;
MOUNT DATABASE '/backup/eqpta_20240401_20240515' TO mount_eqpta_partial;

SELECT COUNT(*) FROM mount_q1.sys.EQPT_A;
SELECT COUNT(*) FROM mount_jun30.sys.EQPT_B;
SELECT COUNT(*) FROM mount_eqpta_partial.sys.EQPT_A;

UNMOUNT DATABASE mount_q1;
UNMOUNT DATABASE mount_jun30;
UNMOUNT DATABASE mount_eqpta_partial;
```

이와 같이 Machbase의 백업·마운트 기능을 활용하면 라이브 데이터는 가볍게 유지하면서도 과거 데이터를 즉시 조회하거나 비교 분석할 수 있습니다. 필요에 따라 전체 복구를 수행하거나, 마운트를 활용해 과거 데이터를 읽기 전용으로 빠르게 참조하십시오.
