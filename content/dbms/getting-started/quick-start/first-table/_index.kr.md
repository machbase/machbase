---
type: docs
title: '첫 테이블 만들기'
weight: 30
toc: true
---

첫 테이블은 가장 단순한 LOG 테이블로 만듭니다. LOG 테이블은 이벤트, 로그, 이력처럼
계속 추가되는 데이터를 저장하는 기본 테이블 유형입니다. 처음부터 복잡한 스키마를 만들
필요는 없습니다. 빈 노트를 펼치고 날짜, 수준, 메시지 칸을 먼저 그어 보는 정도로 시작하면
충분합니다.

시계열 테이블을 설계할 때는 “나중에 어떤 시간 조건으로 조회할 것인가”를 먼저 떠올리면
좋습니다. 이벤트가 발생한 시각, 이벤트의 종류, 장비나 서비스의 식별자, 사람이 읽을 수 있는
메시지가 있으면 첫 로그 테이블로 충분한 출발점이 됩니다.

## 첫 테이블 예제

```sql
CREATE TABLE DBMS_GS_FIRST_TABLE (
  EVENT_TIME DATETIME,
  LEVEL VARCHAR(10),
  MESSAGE VARCHAR(80)
);

SELECT NAME
FROM M$SYS_TABLES
WHERE NAME = 'DBMS_GS_FIRST_TABLE';

DROP TABLE DBMS_GS_FIRST_TABLE;
```

위 SQL이 `/tmp/dbms_gs_first_table.sql` 파일에 저장되어 있다고 가정하고 다음 명령을 실행합니다.

```bash
machsql -s 127.0.0.1 -P 5656 -u SYS -p MANAGER -f /tmp/dbms_gs_first_table.sql
```

`DBMS_GS_FIRST_TABLE`이 출력되면 테이블 생성과 카탈로그 조회가 정상적으로 수행된 것입니다.
카탈로그 조회는 방금 만든 테이블이 데이터베이스의 목록에 등록되었는지 확인하는 절차입니다.
운영 환경에서도 새 객체를 만든 뒤에는 이렇게 목록에서 다시 확인하는 습관이 도움이 됩니다.
재실행 중 `DBMS_GS_FIRST_TABLE`이 이미 존재한다는 오류가 나면
`DROP TABLE DBMS_GS_FIRST_TABLE;`를 실행한 뒤 다시 시작합니다.
