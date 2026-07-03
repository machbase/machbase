---
type: docs
title: '설치 후 첫 확인'
weight: 10
toc: true
---

가장 먼저 확인할 것은 DBMS 서버가 5656 포트에서 응답하고, `machsql`이 해당 서버에
접속할 수 있는지입니다. 데이터베이스 작업에서 접속 확인은 여행 전 지도를 펴는 것과
같습니다. 길이 맞는지 확인하지 않으면 이후의 SQL이 아무리 정확해도 목적지에 도달할 수
없습니다.

## 접속 명령

대화형 접속이 필요하면 터미널에서 `machsql -s 127.0.0.1 -P 5656 -u SYS -p MANAGER`를
실행합니다. 여러 문장을 직접 입력하며 확인할 때 유용합니다.

파일을 실행할 때는 `-f` 옵션을 사용합니다. 이 장의 모든 예제는 이 방식을 기준으로
검증했습니다. 매번 같은 SQL을 실행해야 하는 매뉴얼 예제에서는 파일 실행 방식이 더
일관적입니다.

## 서버 확인 예제

```sql
SELECT COUNT(*) AS TABLE_COUNT FROM M$SYS_TABLES;
```

위 SQL이 `/tmp/dbms_gs_first_check.sql` 파일에 저장되어 있다고 가정하고 다음 명령을 실행합니다.

```bash
machsql -s 127.0.0.1 -P 5656 -u SYS -p MANAGER -f /tmp/dbms_gs_first_check.sql
```

정상적으로 접속되면 `Machbase Client Query Utility` 배너 뒤에 `TABLE_COUNT` 결과가
출력됩니다. 연결에 실패하면 서버 주소, 포트, 사용자 이름, 암호를 먼저 확인합니다. 이
단계에서 문제가 해결되어야 이후의 테이블 생성과 조회 예제를 안정적으로 따라갈 수 있습니다.
