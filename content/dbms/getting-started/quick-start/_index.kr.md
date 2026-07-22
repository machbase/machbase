---
type: docs
title: '1.2 10분 빠른 시작'
weight: 20
toc: true
---

1장에서 유일하게 직접 실행하는 대표 예제입니다. 서버 접속, 테이블 생성, 데이터 입력, 조회, 정리 흐름을 한 번에 확인합니다. 가장 기본 테이블 유형인 LOG 테이블을 사용하며, TAG, LOOKUP, TRANSACTION 같은 다른 유형은 이후 테이블 설계 문서에서 다룹니다.

## 실행 전제

- Machbase DBMS 서버가 `127.0.0.1:5656`에서 실행 중입니다.
- `machsql` 명령을 사용할 수 있습니다.
- `SYS` 계정과 `MANAGER` 비밀번호로 접속합니다.

서버가 아직 준비되지 않았다면 [설치, 배포, 업그레이드](/dbms/installation-deployment-upgrade/)와
[Linux Standard Edition 설치](/dbms/installation-deployment-upgrade/standard-edition/#linux)를 먼저
참고하십시오.

## 대표 실행 예제

서비스 시작 이벤트 한 건을 LOG 테이블에 기록합니다. LOG 테이블은 `CREATE LOG TABLE`로
명시해서 생성하며, `_arrival_time` 컬럼이 자동으로 추가됩니다.

다음 명령으로 SQL 파일을 저장하고 실행합니다.

```bash
cat > /tmp/dbms_gs_quick.sql <<'SQL'
CREATE LOG TABLE DBMS_GS_QUICK (
  EVENT_ID INTEGER,
  EVENT_TIME DATETIME,
  LEVEL VARCHAR(10),
  MESSAGE VARCHAR(40)
);

INSERT INTO DBMS_GS_QUICK
VALUES (
  1,
  TO_DATE('2026-07-02 09:00:00', 'YYYY-MM-DD HH24:MI:SS'),
  'INFO',
  'service started'
);

SELECT _arrival_time, EVENT_ID, EVENT_TIME, LEVEL, MESSAGE
FROM DBMS_GS_QUICK
ORDER BY EVENT_ID;

DROP TABLE DBMS_GS_QUICK;
SQL

machsql -s 127.0.0.1 -P 5656 -u SYS -p MANAGER -f /tmp/dbms_gs_quick.sql
```

`service started`가 출력되면 기본 SQL 흐름이 정상 동작한 것입니다.
`EVENT_TIME`은 애플리케이션이 저장한 실제 이벤트 시각이고, `_arrival_time`은 DBMS가
자동 기록한 서버 수신 시각입니다.

재실행 중 `DBMS_GS_QUICK`이 이미 존재한다는 오류가 나면 이전 실행이 `DROP TABLE`
단계에 도달하지 못한 것입니다. `DROP TABLE DBMS_GS_QUICK;`을 먼저 실행하십시오.

## 이 예제에서 확인한 것

| 항목 | 확인 내용 |
| --- | --- |
| 서버 접속 | `machsql`로 `127.0.0.1:5656`에 접속 |
| 테이블 생성 | `CREATE LOG TABLE`로 LOG 테이블을 명시적으로 생성 |
| 데이터 입력 | `INSERT`와 `TO_DATE`로 이벤트 데이터 저장 |
| 데이터 조회 | `SELECT`와 `ORDER BY`로 입력 결과 확인 |
| 자동 컬럼 | LOG 테이블의 `_arrival_time`은 서버가 자동 기록 |
| 정리 | `DROP TABLE`로 실습 테이블 삭제 |
