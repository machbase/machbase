---
title : '휘발성 테이블 활용 샘플 예제'
type : docs
weight: 60
---

## 센서 데이터의 현재 값을 저장

휘발성 테이블의 데이터는 메모리 상에만 존재하여 기본 키에 의한 갱신 연산이 매우 빠른 특징이 있다. 이 특징을 이용하여, 매우 빠르게 변화하는 센서의 현재 값을 저장하는 테이블을 만든다. 테이블 생성 스크립트의 예는 아래와 같다.

```sql
create volatile table sensor_current (sensor_id varchar(40) primary key, value double);
```

## 휘발성 데이터의 입력 및 갱신

테이블을 생성하였으므로, 데이터 입력과 갱신 연산을 통하여 센서의 현재 값을 반영할 수 있다. 입력되는 센서값은 기본 키 sensor_id 컬럼을 기준으로 입력 혹은 갱신을 수행할 것인지가 결정된다. 입력 혹은 갱신은 다음의 질의문으로 수행할 수 있다.

```sql
insert into sensor_current values('SENSOR_001',100.0) on duplicate key update set value=100.0;
```

위 질의문에서 입력되는 데이터는 기본 키에 해당하는 컬럼인 sensor_id 값이 'SENSOR_001'인 데이터가 있으면 그 레코드의 value 컬럼 값을 100.0으로 갱신하고, 없으면 Insert문의 문법 대로 새로운 레코드를 삽입한다.

## 휘발성 데이터의 검색

특정 센서 데이터의 현재 값을 알려면 다음의 질의를 이용하여 검색한다. 일반적인 SQL질의문과 동일한 문법을 사용하여 검색을 수행할 수 있다.

```sql
SELECT value FROM sensor_current WHERE sensor_id = 'SENSOR_001'
```
