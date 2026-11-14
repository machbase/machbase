---
type: docs
title: '12.7 SQL 결과를 입력으로 조회'
weight: 70
toc: true
---

파일 대신 SELECT가 반환하는 TEXT/BINARY 셀을 READ의 입력으로 사용할 수 있습니다.
각 셀은 독립 입력이며 셀 문자열을 서로 이어 붙이지 않습니다.

## 작은 CSV 셀로 시작

전용 실습 DB에 같은 이름의 객체가 없을 때 한 번 실행합니다.

```sql
CREATE TRANSACTION TABLE DFQ_PAYLOAD(ID INTEGER PRIMARY KEY,PAYLOAD TEXT);
INSERT INTO DFQ_PAYLOAD VALUES(1,'id,v
1,10
2,20');
SELECT id,v FROM READ('SELECT PAYLOAD FROM DFQ_PAYLOAD WHERE ID=1',
 'format=csv','header=true','type.id=LONG','type.v=LONG') ORDER BY id;
```

결과는 (1,10)·(2,20)입니다. 내부 SELECT가 원래 ID를 자동으로 출력하지는 않습니다.
파일 데이터가 이미 BINARY/BLOB에 있으면 그 바이트를 입력으로 사용하며 HEX/Base64 문자열을
자동으로 복원하지 않습니다. 파일로 내보내 다시 읽는 과정은 필요하지 않습니다.

## BINARY에 저장한 Parquet 읽기

다음은 제공한 작은 Parquet 파일을 셀 하나로 저장해 다시 조회하는 독립 실습입니다.
파일이 청크 크기 1 MiB보다 작을 때만 이 INSERT를 그대로 사용합니다. 큰 파일의 여러
청크를 각각 독립 Parquet 파일처럼 읽으면 안 되며 원래 파일 바이트를 셀 단위로 보존해야 합니다.

```sql
CREATE TRANSACTION TABLE DFQ_BINARY(ID LONG PRIMARY KEY,PAYLOAD BINARY);
INSERT INTO DFQ_BINARY SELECT 1,_CONTENT
FROM READ('/srv/dfq/sensor.parquet','mode=raw','raw.chunk_bytes=1048576');
SELECT COUNT(*) AS N,SUM(v) AS TOTAL
FROM READ('SELECT PAYLOAD FROM DFQ_BINARY WHERE ID=1','format=parquet');
DROP TABLE DFQ_BINARY;
```

결과는 N=5, TOTAL=150입니다. BINARY의 원래 바이트를 사용하며 화면의 HEX 문자열로
변환하거나 임시 Parquet 파일을 만들지 않습니다. NPY·NPZ·MCAP·HDF5도 지원되는 원본
바이트와 해당 format을 사용하며, LeRobot의 디렉터리 root는 이 입력 방식으로 대체하지 않습니다.

## 추론 범위와 재실행

```sql
SELECT /*+ READ_INFER(r,FULL) */ *
FROM READ('SELECT PAYLOAD FROM DFQ_PAYLOAD ORDER BY ID','format=csv') r;
SELECT /*+ READ_INFER(r,SAMPLE,100,50000) */ *
FROM READ('SELECT PAYLOAD FROM DFQ_PAYLOAD ORDER BY ID','format=csv') r;
```

기본 추론은 입력 최대 32행·논리 레코드 합계 최대 20,480개입니다. NULL 셀도 입력 행 한도에
포함합니다. FULL은 내부 SELECT 전체를 스키마 추론에 사용하며 모든 payload의 무결성 검사를
보장하는 옵션은 아닙니다. 바깥 WHERE/LIMIT은 추론 범위를 줄이지 않으므로 입력 필터를
내부 SELECT에 넣습니다. execute에서는 SELECT를 다시 실행하고 준비한 스키마와 비교합니다.

## 허용 입력과 제약

- 내부 SELECT는 VARCHAR/TEXT/CLOB/JSON/BINARY/BLOB 중 컬럼 하나를 반환합니다.
- 단일 SELECT 또는 WITH SELECT만 허용합니다. DML·DDL·다중 문장·bind·외부 상관 참조·
  재귀 SQL source·SELECT FOR UPDATE는 거부합니다.
- NULL 셀은 건너뜁니다. 길이 0인 셀은 해당 포맷의 빈 입력 규칙을 적용합니다.
- CSV/TSV·JSON/JSONL·Parquet·NPY/NPZ·MCAP·HDF5 reader를 사용하며 LeRobot 디렉터리는 제외합니다.
- CSV/TSV의 SQL 입력은 auto에서 순차 실행하고 parallel=true를 거부합니다.
- 파일 snapshot/revision/filename·파일 전용 inspect·영구 token 재조회는 제공하지 않습니다.
- 호출 사용자의 SELECT 권한과 catalog를 사용합니다. 내부 파일 READ가 있으면 파일 권한도 그대로 적용합니다.

빈 결과에서는 자동 추론이 불가능합니다. CSV/TSV는 names와 모든 type을 지정한 명시
스키마 및 header 설정을 사용합니다. 오류의 SQL source row=N은 NULL을 포함한 내부 SELECT
결과 셀의 1부터 시작하는 번호이며 원래 ID나 셀 안 레코드 번호가 아닙니다.
재현 가능한 순서를 원하면 내부 SELECT에 안정적인 ORDER BY를 지정합니다.

실습을 마친 뒤 직접 만든 `DFQ_PAYLOAD`만 `DROP TABLE DFQ_PAYLOAD`로 정리합니다.
