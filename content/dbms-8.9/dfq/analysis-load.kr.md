---
type: docs
title: '12.8 분석과 테이블 적재'
weight: 80
toc: true
---

READ 결과에 WHERE·집계·JOIN·정렬을 적용합니다. 파일 내용을 확인하고 필요할 때만
테이블에 저장합니다. 파일 조회 자체는 DB 테이블을 생성하지 않습니다.

```sql
SELECT COUNT(*) AS N,SUM(v) AS TOTAL FROM READ('/srv/dfq/sensor.csv',
 'type.id=LONG','type.v=LONG') WHERE id>=3;
SELECT A.id,A.v,B.label FROM READ('/srv/dfq/sensor.csv') A
 JOIN READ('/srv/dfq/sensor.json') B ON A.id=B.id ORDER BY A.id;
```

첫 집계는 N=3, TOTAL=120입니다. JOIN은 id로 연결된 5행입니다. 큰 두 파일의 JOIN이
각 파일의 모든 데이터를 메모리 없이 처리한다는 의미는 아닙니다. 범위를 먼저 줄이고
계획과 자원을 확인합니다.

## 필요한 데이터만 저장

전용 실습 DB에서 같은 이름의 객체가 없을 때 실행합니다.

```sql
CREATE TRANSACTION TABLE DFQ_SENSOR(ID LONG PRIMARY KEY,V LONG);
INSERT INTO DFQ_SENSOR SELECT id,v FROM READ('/srv/dfq/sensor.csv',
 'type.id=LONG','type.v=LONG');
SELECT COUNT(*),SUM(v) FROM DFQ_SENSOR;
DROP TABLE DFQ_SENSOR;
```

집계는 5·150입니다. 대상 테이블의 타입·키·DML·트랜잭션 규칙을 따르며 파일을 읽는 것과
대상 DB에 커밋하는 것은 별개입니다. 기존 업무 테이블에는 검증 없이 반복 적재하지 않습니다.

## 긴 TEXT 분석

```sql
SELECT id,LENGTH(label),SUBSTR(label,1,6),UPPER(label)
FROM READ('/srv/dfq/sensor.csv','type.label=TEXT') ORDER BY id;
```

지원하는 TEXT 문자열 연산은 LENGTH·LOWER/UPPER·SUBSTR·SUBSTRING_INDEX·INSTR·
TRIM/LTRIM/RTRIM·REPLACE·LPAD/RPAD·연결입니다. TEXT 전체 값의 정렬·그룹·DISTINCT를
지원하지만 모든 함수·Cluster 지원으로 확대하지 않습니다. 기존 바이트 위치와 NULL 규칙을
유지합니다. 실제 빈 TEXT와 SQL NULL은 COUNT·LENGTH에서도 구분합니다.
TEXT 결과 상한은 64 MiB이며 CSV의 레코드 전체 예산은 별도로 적용합니다.

TEXT Top-N은 LIMIT+OFFSET개의 후보를 보관하지만 전체 입력의 비교 비용이 남습니다. 메모리 예산에 따라 임시 디스크를
사용하며 작은 LIMIT이 파일 읽기·스키마 추론·전체 정렬 비용을 모두 없애지는 않습니다.
