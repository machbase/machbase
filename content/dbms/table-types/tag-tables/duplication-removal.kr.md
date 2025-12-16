---
title: '자동 중복 제거'
type: docs
weight: 90
---

## 개요

Machbase는 설정 가능한 시간 창 내에서 중복된 센서 읽기를 자동으로 감지하고 제거하여 수동 개입 없이 데이터 품질을 보장할 수 있습니다.

## 중복 제거 설정

TAG 테이블을 생성할 때 중복 제거 기간을 테이블 속성으로 전달합니다. 중복 제거를 위해 설정 가능한 최대 기간은 43200분(30일)입니다.

```sql
-- 새로 삽입된 데이터가 시스템 시간으로부터 1440분(하루) 이내의 기존 데이터와 중복되면 해당 데이터가 삭제됩니다.

CREATE TAG TABLE tag (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE SUMMARIZED) TAG_DUPLICATE_CHECK_DURATION=1440;
```

중복 제거 속성은 m$sys_table_property 테이블에서 확인할 수 있습니다.
```sql
SELECT * FROM m$sys_table_property WHERE id={table_id} AND name = 'TAG_DUPLICATE_CHECK_DURATION';
```

데이터 삽입/조회 예제 - 중복 제거 기간이 1440분(하루)인 경우
```sql
-- 총 6개의 데이터가 삽입되었고 그 중 4개가 중복이지만, 1개의 중복 레코드는 시스템 시간(1970-01-03 09:00:00 000:000:003)으로부터
-- 1440분(하루) 전에 삽입되었습니다.
-- 설정된 기간 1440분(하루) 이내에 새로 삽입된 중복 데이터는 표시되지 않습니다.

INSERT INTO tag VALUES('tag1', '1970-01-01 09:00:00 000:000:001', 0);
INSERT INTO tag VALUES('tag1', '1970-01-02 09:00:00 000:000:001', 0);
INSERT INTO tag VALUES('tag1', '1970-01-02 09:00:00 000:000:002', 0);
INSERT INTO tag VALUES('tag1', '1970-01-02 09:00:00 000:000:002', 1);
INSERT INTO tag VALUES('tag1', '1970-01-03 09:00:00 000:000:003', 0);
INSERT INTO tag VALUES('tag1', '1970-01-01 09:00:00 000:000:001', 0);

SELECT * FROM tag WHERE name = 'tag1';
NAME                  TIME                            VALUE
--------------------------------------------------------------------------------------
tag1                  1970-01-01 09:00:00 000:000:001 0
tag1                  1970-01-02 09:00:00 000:000:001 0
tag1                  1970-01-02 09:00:00 000:000:002 0
tag1                  1970-01-03 09:00:00 000:000:003 0
tag1                  1970-01-01 09:00:00 000:000:001 0

```
## 설정 변경
TAG_DUPLICATE_CHECK_DURATION은 다음과 같이 수정할 수 있습니다.

```sql
ALTER TABLE {table_name} set TAG_DUPLICATE_CHECK_DURATION={duration in minutes};
```

## 중복 제거 제약 조건

* 중복 제거 설정은 분 단위로 구성할 수 있으며, 최대 43200분(30일)의 제한이 있습니다.
* 기존 입력 데이터가 이미 삭제된 경우, 동일한 데이터의 후속 발생은 중복 제거 목적으로 중복으로 간주되지 않습니다.

## TRACE 로그로 중복 제거 확인
TRACE_LOG_LEVEL에 32(SM_2)를 추가하면 중복제거시 로그로 출력됩니다. 
```sql
 -- 설정방법
alter system set TRACE_LOG_LEVEL={TRACE_LOG_LEVEL};

 -- 설정 확인
select name, value from v$property where name like 'TRACE_LOG_LEVEL';

```
- 설정예시
```sql
 -- 기존 설정값 확인
Mach> select name, value from v$property where name like 'TRACE_LOG_LEVEL';
name                                                          value                                                                             
---------------------------------------------------------------------------------------------------------------------------------------------------
TRACE_LOG_LEVEL                                               277                                                                               
[1] row(s) selected.

 -- 기존 설정값에 32를 더한값인 309(277 + 32)를 설정
alter system set TRACE_LOG_LEVEL=309
```

- 로그파일위치: `$MACHBASE_HOME/trc/machbase.trc`
- 빠른 필터:
  ```bash
  tail -n 50 $MACHBASE_HOME/trc/machbase.trc | grep DUP_DROP
  ```
- 로그 포맷: `DUP_DROP Table=<테이블명> TAG=<tag id> TIME=<시간> COL<n>=<값> ...`
- 실제 예시 (TAG=1의 동일 TIME 중복):
  ```
  [2025-11-29 13:50:27 P-151395 T-126344581076672][SM-INFO] DUP_DROP Table=TAG TAG=1 TIME=1998-12-24 09:00:00 000:000:012  COL3=12.000000
  ...
  [2025-11-29 13:50:27 P-151395 T-126344581076672][SM-INFO] DUP_DROP Table=TAG TAG=1 TIME=1998-12-24 09:00:00 000:000:048  COL3=48.000000
  ```
- 활용 포인트
  - TIME을 기준으로 동일 시각에 중복이 어떻게 제거되는지 확인.
  - `Table=`/`TAG=`를 grep으로 추가 필터링하면 특정 테이블·태그만 빠르게 추적.
- 주의: 한 줄 최대 약 4KB라 컬럼이 매우 많을 때 뒤가 잘릴 수 있으나 크래시는 발생하지 않습니다.
