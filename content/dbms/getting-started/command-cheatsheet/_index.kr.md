---
type: docs
title: '1.3 기본 명령 치트시트'
weight: 30
toc: true
---

처음부터 모든 명령을 외울 필요는 없습니다. 접속, 테이블 확인, SQL 파일 실행 세 가지만 반복하면 나머지는 자연스럽게 익혀집니다.

| 작업 | 명령 |
| --- | --- |
| 대화형 접속 | `machsql -s 127.0.0.1 -P 5656 -u SYS -p MANAGER` |
| SQL 파일 실행 | `machsql -s 127.0.0.1 -P 5656 -u SYS -p MANAGER -f file.sql` |
| 테이블 목록 | `SHOW TABLES;` |
| 테이블 생성 | `CREATE TABLE table_name (...);` |
| 데이터 입력 | `INSERT INTO table_name VALUES (...);` |
| 데이터 조회 | `SELECT ... FROM table_name;` |
| 테이블 삭제 | `DROP TABLE table_name;` |

대표 실행 예제는 위 명령을 한 번씩 조합해 사용합니다.
