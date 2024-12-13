---
type: docs
title : '태그 테이블 VARCHAR 저장옵션'
weight: 80
---

## VARCHAR 저장 옵션
VARCHAR의 size가 설정 값 이하일 경우 fixed 영역에 저장하는 옵션으로 설정 값을 table property로 전달한다.
최소 15 에서 최대 127 bytes까지 설정할 수 있으며 기본 값은 15이다.

```sql
-- 입력되는 VARCHAR DATA중 size가 15이하인 경우 확장파일이 아닌 fixed데이터 파일에 저장된다.
  
CREATE TAG TABLE tag (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE SUMMARIZED, strval VARCHAR(100)) VARCHAR_FIXED_LENGTH_MAX = 15;
```
  
m$sys_table_property에서 VARCHAR 저장옵션 설정정보를 확인할  수 있다.
```sql
SELECT * FROM m$sys_table_property WHERE id={table_id} AND name = 'VARCHAR_FIXED_LENGTH_MAX';
```
