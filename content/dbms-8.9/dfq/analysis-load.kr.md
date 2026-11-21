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

## 파일 관측을 저장 테이블과 결합하기 {#read-storage-join}

파일의 관측 시각을 기준으로 장치별 직전 저장값을 조회합니다.
[전체 실습 자료](/assets/dbms-8.9/array-read/samples.zip)를 내려받습니다. 전용 실습 DB를 사용하고
[anchors.csv](/assets/dbms-8.9/array-read/anchors.csv)와 [payload.jsonl](/assets/dbms-8.9/array-read/payload.jsonl)을 서버의
`/srv/dfq/array-read/`에 저장합니다. 실행 계정은 이 경로를 읽을 수 있어야 합니다.
다른 경로에 저장했다면 SQL의 경로를 바꿉니다.

[전체 SQL](/assets/dbms-8.9/array-read/read-join.sql)을 `machsql -f read-join.sql`로 실행합니다.

```sql
CREATE LOG TABLE M89_READ_HISTORY(ID LONG, DEVICE VARCHAR(32), TM DATETIME, A DOUBLE[65536]);
INSERT INTO M89_READ_HISTORY VALUES(1,'robot-a',FROM_TIMESTAMP(1704067201000000000),[10.0,NULL,30.0]);
INSERT INTO M89_READ_HISTORY VALUES(2,'robot-b',FROM_TIMESTAMP(1704067201000000000),[]);
EXEC TABLE_FLUSH(M89_READ_HISTORY);
SELECT L.ID, R.ID AS HISTORY_ID, ARRAY_LENGTH(R.A) AS N
FROM READ('/srv/dfq/array-read/anchors.csv','format=csv','auto_detect=false',
          'type.id=LONG','type.tm=DATETIME','timezone=UTC') L
LEFT JOIN M89_READ_HISTORY R ON L.DEVICE=R.DEVICE
ORDER BY L.ID;
SELECT L.ID, R.ID AS HISTORY_ID, ARRAY_LENGTH(R.A) AS N
FROM READ('/srv/dfq/array-read/anchors.csv','format=csv','auto_detect=false',
          'type.id=LONG','type.tm=DATETIME','timezone=UTC','source.consistency=strong') L TIMESTAMP(TM)
ASOF JOIN M89_READ_HISTORY R TIMESTAMP(TM)
ON L.DEVICE=R.DEVICE TIE LAST BY R.ID
WITH PROVENANCE AS P ORDER BY L.ID;
SELECT ID, ARRAY_LENGTH(PAYLOAD) AS N, ARRAY_VALID_MASK(PAYLOAD) AS MASK
FROM READ('/srv/dfq/array-read/payload.jsonl','format=jsonl','project.id=id','type.id=LONG',
          'project.payload=payload','type.payload=DOUBLE[65536]') ORDER BY ID;
DROP TABLE M89_READ_HISTORY;
```

| 파일 관측 ID | 저장 행 ID | 길이 N |
|---|---|---|
| 1 | 1 | 3 |
| 2 | 2 | 0 |
| 3 | NULL | NULL |

LEFT와 ASOF 예제 모두 위 세 행을 반환합니다. 두 번째 행은 일치한 저장값이 빈 배열이며
세 번째 행은 일치하는 장치가 없습니다. ASOF는 같은 장치에서 파일의 기준 시각 이하인
최신 저장 행을 선택합니다. 동일 시각의 후보는 `TIE LAST BY R.ID`로 결정합니다.
JSONL 조회는 3, 0, SQL NULL의 길이를 반환하며 첫 마스크는 16진수 `05`입니다.
[의도적 오류 SQL](/assets/dbms-8.9/array-read/array-errors.sql)과
[잘못된 원소의 JSONL](/assets/dbms-8.9/array-read/bad-payload.jsonl)로 목록 상한 및 변환
진단을 확인합니다.

상대 tick을 읽을 때는 CSV의 `type.tick=LONG`으로 정수 값을 유지합니다. VIEW에서
`FROM_TIMESTAMP(1699999999999999997 + tick * 4) AS TM`으로 원점과 4ns 단위를 적용한
뒤 JOIN 입력에 `TIMESTAMP(TM)`을 지정합니다. 서로 다른 실행의 데이터가 섞이지 않도록
장치와 세션을 함께 결합 조건에 넣습니다. READ와 READ, READ와 LOG/TAG에 같은 시간축
지정 방식을 사용합니다. [시계열 JOIN](../../time-series-sql/joins/)에서 선택 규칙을 확인합니다.

### 상대 tick을 TAG 시간축에 맞추기

[ticks.csv](/assets/dbms-8.9/array-read/ticks.csv)를 같은 서버 경로에 저장하고,
[전체 SQL](/assets/dbms-8.9/array-read/relative-join.sql)을 실행합니다.

```sql
CREATE TAG TABLE M89_READ_TAG(DEVICE VARCHAR(32) PRIMARY KEY, TM DATETIME BASETIME,
                             ID LONG, SESSION_ID VARCHAR(32));
INSERT INTO M89_READ_TAG VALUES('robot-a',FROM_TIMESTAMP(1699999999999999997),101,'run1');
EXEC TABLE_FLUSH(M89_READ_TAG);
CREATE VIEW M89_READ_TICKS AS
SELECT ID,DEVICE,SESSION_ID,FROM_TIMESTAMP(1699999999999999997+TICK*4) AS TM
FROM READ('/srv/dfq/array-read/ticks.csv','format=csv','auto_detect=false',
          'type.id=LONG','type.tick=LONG');
SELECT L.ID, TO_TIMESTAMP(L.TM) AS TARGET_NS, R.ID AS HISTORY_ID
FROM M89_READ_TICKS L TIMESTAMP(TM)
ASOF JOIN M89_READ_TAG R ON L.DEVICE=R.DEVICE AND L.SESSION_ID=R.SESSION_ID
TOLERANCE 4ns ORDER BY L.ID;
DROP VIEW M89_READ_TICKS;
DROP TABLE M89_READ_TAG;
```

두 파일 행의 TARGET_NS는 1700000000000000001입니다. 첫 행은 정확히 4ns 차이인
저장 ID 101을 선택합니다. 두 번째 행은 세션이 다르므로 HISTORY_ID가 NULL입니다.
TAG의 BASETIME은 기본 시간축으로 사용됩니다.

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
