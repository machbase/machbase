---
type: docs
title: '10분 빠른 시작'
weight: 20
toc: true
---

빠른 시작은 짧은 시운전입니다. 새 장비를 받으면 먼저 전원을 켜고 버튼이 동작하는지, 계기판이 반응하는지 확인하듯이, 여기서는 단 한 번의 `machsql` 실행으로 테이블 생성, 데이터 입력, 조회, 정리까지 전체 흐름을 확인합니다. Machbase가 지향하는 산업 IoT와 금융 틱 데이터 처리도 결국 이 기본 흐름 위에서 시작됩니다. 먼저 LOG 테이블로 SQL 동작을 확인한 뒤, TAG 테이블은 다음 문서 선택 페이지에서 맛보기로 확인합니다.

실제 운영에서는 이 흐름이 매우 빠르게 반복됩니다. 수집기가 데이터를 받고 DBMS에 기록하면, 사용자는 방금 들어온 값을 조회하거나 일정 시간 단위로 집계합니다. 빠른 시작 예제는 그 전체 흐름을 가장 작은 크기로 압축한 것입니다.

## 실행 전제

- Machbase DBMS 서버: `127.0.0.1:5656`
- 사용자: `SYS`
- 암호: `MANAGER`
- 클라이언트: `machsql`

## 빠른 시작 예제

이 예제는 서비스 시작 이벤트 한 건을 LOG 테이블에 기록합니다. LOG 테이블은 설비 이벤트, 수집기 상태, 틱 수신 이력처럼 시간 순서로 계속 추가되는 사건을 담는 기본 그릇입니다.

```sql
CREATE TABLE DBMS_GS_QUICK (
  EVENT_ID INTEGER,
  MESSAGE VARCHAR(40)
);

INSERT INTO DBMS_GS_QUICK VALUES (1, 'service started');

SELECT EVENT_ID, MESSAGE FROM DBMS_GS_QUICK;

DROP TABLE DBMS_GS_QUICK;
```

위 SQL이 `/tmp/dbms_gs_quick.sql` 파일에 저장되어 있다고 가정하고 다음 명령을 실행합니다.

```bash
machsql -s 127.0.0.1 -P 5656 -u SYS -p MANAGER -f /tmp/dbms_gs_quick.sql
```

`service started`가 출력되면 기본 SQL 흐름이 정상적으로 동작한 것입니다. 단 한 줄의 결과처럼 보이지만, 그 뒤에는 서버 접속, SQL 파싱, 테이블 생성, 데이터 입력, 조회가 모두 연결되어 동작했다는 의미가 있습니다. 재실행 중 `DBMS_GS_QUICK`이 이미 존재한다는 오류가 나면 `DROP TABLE DBMS_GS_QUICK;`를 실행한 뒤 다시 시작합니다.
