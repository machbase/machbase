---
type: docs
title: '기본 명령 치트시트'
weight: 30
toc: true
---

처음부터 많은 명령을 외울 필요는 없습니다. 초보 운전자가 모든 도로 표지판을 한 번에
외우지 않아도 출발, 정지, 방향 전환부터 익히면 되는 것처럼, 처음에는 아래 명령만 알고
있어도 충분합니다. 접속하고, 테이블을 확인하고, SQL 파일을 실행하는 흐름을 반복하면서
나머지 명령을 자연스럽게 익히면 됩니다.

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

`hello machbase`가 출력되면 치트시트의 기본 명령 조합이 정상적으로 동작한 것입니다.
이 예제는 작지만 유용한 기준점입니다. 이후 더 긴 SQL을 실행하다가 문제가 생기면, 이처럼
짧은 예제로 접속과 기본 실행 환경이 정상인지 다시 확인할 수 있습니다.
재실행 중 `DBMS_GS_CHEATSHEET`이 이미 존재한다는 오류가 나면
`DROP TABLE DBMS_GS_CHEATSHEET;`를 실행한 뒤 다시 시작합니다.
