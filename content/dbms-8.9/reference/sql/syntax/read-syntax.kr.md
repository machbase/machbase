---
type: docs
title: 'READ / DFQ'
weight: 230
toc: true
---

READ는 파일·데이터셋 또는 지원되는 SELECT 결과의 한 컬럼을 관계로 조회하는 테이블 함수입니다.
Standard Edition에서 사용하며 scalar 함수로 호출하지 않습니다.

```text
SELECT ... FROM READ('path' [, 'path' ...] [, 'name=value' ...]) [alias];
SELECT ... FROM READ('source=path' [, 'name=value' ...]) [alias];
SELECT ... FROM READ('sources=path1,path2' [, 'name=value' ...]) [alias];
SELECT ... FROM READ('SELECT ...' [, 'name=value' ...]) [alias];
```

모든 READ 인자는 SQL 문자열 리터럴입니다. 위치형 파일·source·sources를 혼합하지 않습니다.
첫 name=value 뒤에는 위치형 파일을 놓지 않습니다. 일반 옵션은 첫 등호로 나누며
뒤의 등호·공백은 값의 일부입니다. 입력 config JSON은 지원하지 않습니다.
내부 SELECT 문자열의 분류·제약은 아래 SQL 입력 절을 따릅니다.

## 반환 모드와 옵션

반환 컬럼은 reader·target·mode·columns·project·column 설정에 따라 달라집니다.
여러 파일도 같은 reader의 호환 조건을 충족해야 합니다. 실행 중 타입을 자동 확장하지 않습니다.

- [전체 공통 옵션과 모드](/kr/dbms-8.9/dfq/read-options/)
- [포맷별 전체 옵션·조합·반환 예](/kr/dbms-8.9/dfq/formats/)
- [타입·필드와 원문 표현](/kr/dbms-8.9/dfq/extract/)

## SQL 결과 입력과 READ_INFER

내부 SELECT는 VARCHAR/TEXT/CLOB/JSON/BINARY/BLOB 컬럼 하나를 반환해야 합니다.
각 셀을 독립 입력으로 해석합니다. NULL은 건너뛰며 원래 ID를 자동 반환하지 않습니다.
단일 SELECT 또는 WITH SELECT만 허용하고 DML·DDL·다중 문장·bind·외부 상관 참조·
재귀 SQL source·SELECT FOR UPDATE는 거부합니다. 호출 사용자의 권한을 적용합니다.

```text
SELECT /*+ READ_INFER(alias,FULL) */ ... FROM READ('SELECT ...', ...) alias;
SELECT /*+ READ_INFER(alias,SAMPLE,input_rows,logical_records) */ ...
FROM READ('SELECT ...', ...) alias;
```

힌트는 바깥 query block의 정확한 READ alias를 지정합니다. 기본 추론은 입력 최대 32행과
논리 레코드 합계 20,480개입니다. FULL은 전체 내부 SELECT 결과를 추론에 사용합니다.
SAMPLE 한도는 양의 값이며 잘못된 alias·중복·0·음수 한도는 오류입니다.
바깥 WHERE/LIMIT은 내부 추론 범위를 제한하지 않습니다. execute에서는 내부 SELECT를
다시 실행합니다. 파일 전용 snapshot·revision·filename·영구 token 기능은 사용할 수 없습니다.

[실행 예제와 빈 입력 처리](/kr/dbms-8.9/dfq/sql-source/)를 참고합니다.

## 권한과 파일 수명

일반 사용자에게는 디렉터리 READ 권한과 서버 OS 파일 읽기 권한이 필요합니다.
VIEW를 통하더라도 파일은 실행 사용자 기준으로 검사합니다. 열린 cursor와 새 실행의
권한·원본 검사 시점은 [권한과 운영](/kr/dbms-8.9/dfq/operations/)을 참고합니다.
