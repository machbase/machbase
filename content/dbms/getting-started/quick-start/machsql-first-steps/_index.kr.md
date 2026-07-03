---
type: docs
title: 'machsql 첫 단계'
weight: 20
toc: true
---

`machsql`은 Machbase DBMS에 SQL을 전달하는 기본 명령행 클라이언트입니다. 사용자는
SQL을 작성하고, `machsql`은 그 SQL을 서버로 전달합니다. 우편함에 편지를 넣듯이 SQL
파일을 넘기면, 서버는 그 내용을 실행하고 결과를 돌려줍니다.

대화형으로 접속할 수도 있고, `-f` 옵션으로 SQL 파일을 실행할 수도 있습니다. 이 장의
예제는 반복 검증이 쉬운 파일 실행 방식을 사용합니다.

## 자주 쓰는 옵션

| 옵션 | 의미 |
| --- | --- |
| `-s 127.0.0.1` | 접속할 서버 주소 |
| `-P 5656` | 접속할 포트 |
| `-u SYS` | 사용자 이름 |
| `-p MANAGER` | 암호 |
| `-f file.sql` | 실행할 SQL 파일 |

## machsql 실행 예제

```sql
SHOW TABLES;
```

위 SQL이 `/tmp/dbms_gs_machsql.sql` 파일에 저장되어 있다고 가정하고 다음 명령을 실행합니다.

```bash
machsql -s 127.0.0.1 -P 5656 -u SYS -p MANAGER -f /tmp/dbms_gs_machsql.sql
```

결과의 `TABLE_TYPE` 컬럼을 보면 현재 데이터베이스에 어떤 유형의 테이블이 있는지
확인할 수 있습니다. 처음에는 테이블 이름보다 유형을 함께 보는 습관이 중요합니다. 같은
데이터베이스 안에서도 LOG, TAG, LOOKUP은 서로 다른 역할을 맡기 때문입니다.
