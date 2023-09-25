---
type: docs
title : '태그 테이블 중복제거 설정'
weight: 70
---

## 중복제거설정
TAG table 생성 시 중복제거 기간을 table property로 전달한다. 중복제거 설정이 가능한 최대 기간은 30일이다.  
  
```sql
-- 기존 입력된 데이터 중 1일 이내의 데이터와 중복된 데이터가 입력될 경우 새로 입력된 데이터를 삭제
  
CREATE TAG TABLE tag (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE SUMMARIZED) TAG_DUPLICATE_CHECK_DURATION=1;
```
  
m$sys_table_property에서 중복제거 설정정보를 확인할  수 있다.
```sql
SELECT * FROM m$sys_table_property WHERE id={table_id} AND name = 'TAG_DUPLICATE_CHECK_DURATION';
```
  
데이터 입.출력 예시(중복제거기간 1일 설정)
```sql
-- 입력된 총 6건의 데이터중 4건의 데이터가 중복 이고 그중 1건은 system시간(1970-01-03 09:00:00 000:000:003)으로 부터
-- 1일전 데이터이며 조회시 새로 입력된 데이터중 설정기간(1일)내의 데이터와 중북인 데이터가 출력이 안됨

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
  
## 중복제거 제약 사항
* 테이블 생성 시 중복제거 정책이 설정되면 이후에 변경할 수 없음  
* 중복제거 설정은 일 단위로 설정할 수 있으며 최대 30일까지 설정이 가능함  
* 기존 입력된 데이터가 이미 삭제된 경우 동일한 데이터가 다시 들어와도 중복제거 대상이 아님  
