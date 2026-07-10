---
title: '7.7 운영과 데이터 생명주기'
weight: 70
toc: true
---

LOG 테이블의 데이터 삭제와 보존 정책을 다룬다.


<a id="original-85-deleting-data"></a>

## Log 데이터 삭제

LOG 테이블은 append 중심 테이블이다. 데이터는 시간 순서로 계속 입력되고, 보존 기간이 지난 데이터는 오래된 영역부터 정리한다.

임의 위치의 데이터를 삭제하는 것은 불가능하며, 임의 위치에서 마지막(가장 오래된 로그) 레코드까지 연속적으로 삭제하는 방식만 지원한다. 로그 데이터의 특성을 활용한 정책으로, 공간 확보를 위해 파일을 순서대로 삭제하는 행위를 DB 형식으로 표현한 것이다.

사용할 수 있는 표현식은 다음과 같다.

<a id="delete-log-syntax"></a>

## 삭제 구문

```sql
DELETE FROM table_name;
DELETE FROM table_name OLDEST number ROWS;
DELETE FROM table_name EXCEPT number ROWS;
DELETE FROM table_name EXCEPT number [YEAR | MONTH | WEEK | DAY | HOUR | MINUTE | SECOND];
DELETE FROM table_name BEFORE datetime_expr;
```

<a id="delete-log-examples"></a>

## 삭제 예제

```sql
-- 모든 데이터 삭제
mach>DELETE FROM devices;
10 row(s) deleted.

-- 가장 오래된 5개 삭제
mach>DELETE FROM devices OLDEST 5 ROWS;
5 row(s) deleted.

-- 마지막 5개를 제외한 모든 데이터 삭제
mach>DELETE FROM devices EXCEPT 5 ROWS;
15 row(s) deleted.

-- 2018년 6월 1일 이전 또는 같은 시각의 모든 데이터 삭제
mach>DELETE FROM devices BEFORE TO_DATE('2018-06-01', 'YYYY-MM-DD');
50 row(s) deleted.
```

운영 환경에서는 삭제 전 같은 기준으로 보존 범위를 확인한다.

```sql
SELECT COUNT(*)
FROM devices
WHERE _arrival_time <= TO_DATE('2018-06-01', 'YYYY-MM-DD');
```

<a id="retention-log-policy"></a>

## 보존 정책 설계

LOG 테이블은 보존 기간을 기준으로 운영하는 것이 일반적이다.

| 정책 | 예시 |
|------|------|
| 기간 기준 보존 | 최근 90일만 유지 |
| 건수 기준 보존 | 최근 1억 건만 유지 |
| 원본 보존 후 집계 | 원본은 30일, 집계 결과는 RDB 또는 TAG에 장기 보존 |
| 백업 후 삭제 | 백업 완료 후 오래된 구간 삭제 |

기간 기준 삭제는 `BEFORE` 또는 `EXCEPT ... DAY` 형식으로 표현한다.

```sql
-- 최근 90일을 제외한 오래된 데이터 삭제
DELETE FROM devices EXCEPT 90 DAY;
```

<a id="lifecycle-log-backup"></a>

## 백업과 삭제 순서

장기 보관이 필요한 로그는 삭제 전에 백업한다.

```sql
BACKUP DATABASE INTO DISK = '/backup/machbase_log_20260101';
```

백업을 마운트해 필요한 구간을 조회할 수 있는지 확인한 뒤 삭제 작업을 수행한다.

```sql
MOUNT DATABASE '/backup/machbase_log_20260101' TO old_log;

SELECT COUNT(*)
FROM old_log.devices;

UMOUNT DATABASE old_log;
```

<a id="lifecycle-log-monitoring"></a>

## 운영 점검 항목

- 입력량 증가에 따라 테이블 크기와 보존 기간을 주기적으로 조정한다.
- 삭제 전 대상 건수와 시간 범위를 확인한다.
- 백업이 필요한 데이터는 백업 완료 후 삭제한다.
- 잘못 입력된 특정 행을 수정해야 하는 모델이면 LOG가 아니라 RDB 또는 LOOKUP 사용을 검토한다.
- `_arrival_time` 기준 보존과 실제 이벤트 시각 기준 보존을 혼동하지 않는다.
