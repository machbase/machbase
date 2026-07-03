---
type: docs
title: '기본 명령 치트시트'
weight: 30
toc: true
---

처음부터 모든 명령을 외울 필요는 없습니다. 접속, 테이블 확인, SQL 파일 실행이라는 세 가지 흐름을 반복하다 보면 나머지 명령은 자연스럽게 익혀집니다. 아래 명령만 알고 있어도 첫 실습을 마치기에 충분합니다.

| 작업 | 명령 |
| --- | --- |
| 대화형 접속 | `machsql -s 127.0.0.1 -P 5656 -u SYS -p MANAGER` |
| SQL 파일 실행 | `machsql -s 127.0.0.1 -P 5656 -u SYS -p MANAGER -f file.sql` |
| 테이블 목록 | `SHOW TABLES;` |
| 테이블 생성 | `CREATE TABLE table_name (...);` |
| 데이터 입력 | `INSERT INTO table_name VALUES (...);` |
| 데이터 조회 | `SELECT ... FROM table_name;` |
| 테이블 삭제 | `DROP TABLE table_name;` |

## 치트시트 검증 예제

```sql
CREATE TABLE DBMS_GS_CHEATSHEET (
  ID INTEGER,
  MESSAGE VARCHAR(40)
);

INSERT INTO DBMS_GS_CHEATSHEET VALUES (1, 'hello machbase');

SELECT ID, MESSAGE FROM DBMS_GS_CHEATSHEET;

DROP TABLE DBMS_GS_CHEATSHEET;
```

위 SQL이 `/tmp/dbms_gs_cheatsheet.sql` 파일에 저장되어 있다고 가정하고 다음 명령을 실행합니다.

```bash
machsql -s 127.0.0.1 -P 5656 -u SYS -p MANAGER -f /tmp/dbms_gs_cheatsheet.sql
```

`hello machbase`가 출력되면 치트시트의 기본 명령 조합이 정상적으로 동작한 것입니다. 이후 더 긴 SQL을 실행하다 문제가 생기면, 이처럼 간단한 예제로 돌아와 접속과 기본 실행 환경이 정상인지 먼저 점검하십시오. 재실행 중 `DBMS_GS_CHEATSHEET`이 이미 존재한다는 오류가 나면 `DROP TABLE DBMS_GS_CHEATSHEET;`를 실행한 뒤 다시 시작합니다.
