---
title: '7.3 생성, 변경, 삭제'
weight: 30
toc: true
---

LOG 테이블의 생성과 삭제 방법을 다룹니다.


<a id="original-85-creating-log-tables"></a>

## Log 테이블 생성 및 관리

LOG 테이블은 `CREATE TABLE` 문으로 생성합니다. 별도의 테이블 타입 키워드를 붙이지 않으면 LOG 테이블로 생성되며, 입력 시각을 기록하는 `_arrival_time` 컬럼이 자동으로 관리됩니다.

```sql
Mach> CREATE TABLE sensor_data (id VARCHAR(32), val DOUBLE);
Created successfully.
```

운영 로그나 이벤트 데이터는 조회 조건에 맞게 컬럼 타입을 정합니다.

```sql
CREATE TABLE security_event (
    event_time  DATETIME,
    severity    SHORT,
    category    VARCHAR(32),
    src_ip      IPV4,
    dst_ip      IPV4,
    src_port    USHORT,
    dst_port    USHORT,
    message     TEXT
);
```

`_arrival_time`은 데이터가 Machbase에 도착한 시각입니다. 실제 이벤트 발생 시각이 필요하면 `event_time`처럼 별도 `DATETIME` 컬럼을 둡니다.

<a id="create-log-schema-rules"></a>

## 스키마 설계 기준

LOG 테이블은 append 중심 테이블이므로 입력 후 수정할 수 없다는 전제로 스키마를 정합니다.

| 설계 항목 | 권장 방식 |
|----------|-----------|
| 이벤트 시각 | `_arrival_time`과 별도 `DATETIME` 컬럼을 구분 |
| 긴 메시지 | `TEXT` 컬럼 사용 |
| IP 주소 | `IPV4`, `IPV6` 타입 사용 |
| 상태/등급 | `SHORT` 또는 `INTEGER` 사용 |
| 분석 기준 | 자주 필터링하는 값을 별도 컬럼으로 분리 |

LOG 테이블에는 PRIMARY KEY나 UNIQUE 제약을 지정하지 않습니다. 행 단위 UPDATE가 필요한 데이터는 LOOKUP 또는 RDB 테이블을 검토합니다.

<a id="alter-log-table"></a>

## 컬럼 변경

LOG 테이블은 운영 중 필요한 컬럼을 추가, 삭제, 이름 변경, 일부 속성 변경할 수 있습니다.

```sql
ALTER TABLE security_event ADD COLUMN host_name VARCHAR(128);
```

기존 데이터에는 새 컬럼 값이 없으므로, 새 컬럼을 사용하는 쿼리는 NULL 처리 또는 입력 시점 구분을 고려합니다.

```sql
ALTER TABLE security_event DROP COLUMN (host_name);
ALTER TABLE security_event RENAME COLUMN category TO event_category;
ALTER TABLE security_event MODIFY COLUMN (message VARCHAR(4096));
```

`MODIFY COLUMN`은 VARCHAR 크기 확장, `MINMAX_CACHE_SIZE` 같은 컬럼 속성 변경, NULL/NOT NULL 속성 변경에 사용합니다.

```sql
ALTER TABLE security_event MODIFY COLUMN event_category SET MINMAX_CACHE_SIZE = 1048576;
ALTER TABLE security_event MODIFY COLUMN event_category NOT NULL NOCHECK;
ALTER TABLE security_event MODIFY COLUMN event_category NULL;
```

<a id="alter-log-limitations"></a>

## 컬럼 변경 제약

LOG 테이블의 컬럼 변경에는 다음 제약이 있습니다.

- `_ARRIVAL_TIME`, `_RID` 같은 내부 컬럼은 삭제, 이름 변경, 속성 변경 대상이 아닙니다.
- 인덱스가 걸린 컬럼은 인덱스를 먼저 삭제한 뒤 컬럼을 삭제합니다.
- 테이블에는 최소 하나 이상의 사용자 컬럼이 남아 있어야 합니다.
- VARCHAR 크기 변경은 기존 크기보다 크게 확장하는 용도로 사용합니다.
- 운영 중 append가 계속되는 테이블은 DDL 시점을 분리하고, 변경 후 입력·조회 쿼리를 확인합니다.

<a id="delete-log-table-definition"></a>

## 데이터 삭제와 테이블 삭제

테이블 정의를 유지하고 데이터를 모두 비우려면 `TRUNCATE TABLE`을 사용합니다.

```sql
Mach> TRUNCATE TABLE sensor_data;
Truncated successfully.
```

테이블 정의와 데이터를 모두 삭제하려면 `DROP TABLE`을 사용합니다.

```sql
Mach> DROP TABLE sensor_data;
Dropped successfully.
```

`DROP TABLE`은 복구가 필요한 운영 데이터에 바로 실행하지 않습니다. 삭제 전 백업, 마운트 조회, 내보내기 여부를 확인합니다.

<a id="create-log-checklist"></a>

## 생성 전 체크리스트

- 실제 이벤트 시각과 도착 시각을 구분할지 결정합니다.
- 메시지 전문 검색이 필요하면 `TEXT` 컬럼을 사용합니다.
- 네트워크 주소는 문자열보다 `IPV4`/`IPV6` 타입을 우선 검토합니다.
- 행 단위 수정이 필요한 정보는 LOG 테이블에 넣지 않고 LOOKUP 또는 RDB로 분리합니다.
- 보존 기간과 삭제 정책을 테이블 생성 시 함께 정합니다.
