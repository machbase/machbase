# 시계열 분석 SQL 실습 자료

Machbase DBMS 8.9 Standard Edition용입니다. 정상 SQL 163개와 의도적 오류 SQL
51개를 포함합니다. SQL 실행 전에 같은 이름의 TS13_ 테이블이 없는 전용 실습 DB를 준비합니다.

## SQL로 따라 하기

```bash
machsql -s 127.0.0.1 -u SYS -p MANAGER --timezone +0900 -f setup.sql
machsql -s 127.0.0.1 -u SYS -p MANAGER --timezone +0900 -f joins/asof/01.sql
machsql -s 127.0.0.1 -u SYS -p MANAGER --timezone +0900 -f cleanup.sql
```

포트가 기본값과 다르면 -P를, 기본 인증정보와 다르면 -u·-p를 지정합니다.
setup.sql은 한 번만 실행하며 CREATE 오류가 있으면 기존 객체를 확인하고 새 실습 DB에서 시작합니다.
cleanup.sql은 이 자료의 테이블을 DROP합니다. 보존할 데이터가 있는 DB에는 실행하지 않습니다.

새 전용 DB에서는 all-normal.sql 하나로 준비·모든 정상 조회·정리를 실행할 수도 있습니다.
setup.sql을 먼저 실행한 DB에는 all-normal.sql을 중복 실행하지 않습니다.
오류 SQL은 정상 SQL 묶음에 포함하지 않았습니다. examples.json의 error가 있는 항목이 오류 예제입니다.

## 파일 읽기

- setup.sql / cleanup.sql: 전체 스키마·입력·정리
- 주제별 NN.sql: 매뉴얼에 실린 온전한 조회
- 같은 위치 NN.json: 열 이름·전체 결과 또는 의도한 오류 진단
- fixtures.json: 기준 절대 시각·원본 데이터·테이블별 건수
- examples.json: 독립적인 예상값과 검증 조건
- plots/: 원본 신호와 선택점을 비교한 SVG

기준 시각은 2027-01-01 00:00:00 +09:00, 절대 ns는 1798729200000000000입니다.
S·EVENT_S·MOTOR_S는 기준에서 지난 초입니다. DATETIME 표시 시간대는 클라이언트에 따라
달라질 수 있으며 TIME_NS가 같은지 확인합니다. NULL은 관측값 NULL 또는 미매칭일 수 있습니다.
출처 예제는 JSON에서 이 차이를 구분합니다.

## 자동 검증

Python 3와 Machbase Python API 2.4 이상이 필요합니다. 해당 제품용 SDK를 설치합니다.

```bash
python3 -m pip install 'machbaseapi>=2.4'
read -rsp '실습 DB 비밀번호: ' TS_SQL_PASSWORD
export TS_SQL_PASSWORD
python3 verify_samples.py --host 127.0.0.1 --port 5656 --user SYS --output verification-results.json
unset TS_SQL_PASSWORD
```

포트와 계정은 실습 서버에 맞춥니다. 자동 검증은 setup부터 시작하므로 테이블을 수동 생성한
DB에서 중복 실행하지 않습니다. 생성에 성공한 테이블만 추적하고 종료 시 해당 테이블을 정리합니다.
쿼리 결과·원본 ID·절대 시각·보간 endpoint·오류 진단을 검사합니다.
prepared 검증은 허용차·SAMPLE 범위·ROWS 폭의 재바인드와 동적 PIVOT의 열 구성을 확인합니다.
정상 결과는 숫자 허용 오차 안에서 비교하며 오류 예제는 의도한 진단과 일치해야 통과합니다.
