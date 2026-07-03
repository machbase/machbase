---
type: docs
title: '다음에 읽을 문서 선택하기'
weight: 40
toc: true
---

빠른 시작을 마쳤다면 이제 갈림길에 섰다고 볼 수 있습니다. 같은 Machbase DBMS를 사용해도
산업 IoT 센서 값을 저장하려는 사용자, 금융 틱 데이터를 적재하려는 사용자, 로그를 분석하려는
사용자, 애플리케이션을 연결하려는 사용자가 읽어야 할 다음 문서는 서로 다릅니다. Machbase
DBMS 매뉴얼은 기능 이름보다 사용자의 설계 질문을 기준으로 읽는 것이 효과적입니다.

다음 문서를 고를 때는 네 가지 질문을 먼저 던져 보십시오. 데이터가 얼마나 자주 들어오는지,
시간 범위로 얼마나 자주 조회하는지, 원본을 얼마나 오래 보관해야 하는지, 집계나 롤업이
필요한지입니다. 이 질문에 답하면 어떤 테이블과 어떤 기능을 먼저 공부해야 하는지 분명해집니다.

## 다음 경로

| 해야 할 일 | 다음 문서 |
| --- | --- |
| 산업 IoT 센서, 설비, 계측값 저장 | [TAG 테이블 설계](/dbms/data-modeling-table-design/table-types-design-type/design-tag/) |
| 로그, 이벤트, 금융 틱 수신 이력 저장 | [LOG 테이블 설계](/dbms/data-modeling-table-design/table-types-design-type/design-log/) |
| 장비명, 코드, 매핑 정보 관리 | [LOOKUP 설계](/dbms/data-modeling-table-design/table-types-design-type/design-lookup/), [RDB 설계](/dbms/data-modeling-table-design/table-types-design-type/design-rdb-dbms-nfx/), [LOOKUP과 RDB 비교](/dbms/data-modeling-table-design/table-types-selection-type/comparison-rdb-vs-lookup/) |
| SQL 문법 확인 | [SQL 레퍼런스](/dbms/reference/sql/), [SQL 입력](/dbms/data-input-load-export/sql/) |
| 애플리케이션 연결 | [애플리케이션 연동](/dbms/application-integration/), [드라이버 가이드](/dbms/application-integration/guide-drivers/) |
| 운영 설정 변경 | [운영, 설정, 복구](/dbms/operations-configuration-recovery/) |

## TAG 테이블 맛보기 예제

TAG 테이블은 센서나 설비의 값을 시간축에 맞추어 정리하는 데 사용합니다. 이름표가 붙은
계측 노트라고 생각하면 이해하기 쉽습니다. `sensor01`이라는 이름표 아래에 특정 시각의
값을 기록하고, 필요할 때 그 이름표와 시간축으로 다시 찾아봅니다.

TAG 테이블에서 입력한 데이터를 즉시 조회하려면 `TABLE_FLUSH`를 실행합니다. 이 동작을
처음에 확인해 두면 이후 TAG 문서를 읽을 때 혼동을 줄일 수 있습니다.

```sql
CREATE TAG TABLE DBMS_GS_TAG (
  NAME VARCHAR(128) PRIMARY KEY,
  TIME DATETIME BASETIME,
  VALUE DOUBLE
);

INSERT INTO DBMS_GS_TAG
VALUES ('sensor01', TO_DATE('2026-07-02 00:00:00', 'YYYY-MM-DD HH24:MI:SS'), 21.5);

EXEC TABLE_FLUSH(DBMS_GS_TAG);

SELECT NAME, TIME, VALUE
FROM DBMS_GS_TAG
WHERE NAME = 'sensor01';

DROP TABLE DBMS_GS_TAG;
```

위 SQL이 `/tmp/dbms_gs_tag_preview.sql` 파일에 저장되어 있다고 가정하고 다음 명령을 실행합니다.

```bash
machsql -s 127.0.0.1 -P 5656 -u SYS -p MANAGER -f /tmp/dbms_gs_tag_preview.sql
```

`sensor01`이 출력되면 TAG 테이블의 기본 입력과 조회가 정상적으로 동작한 것입니다. LOG
예제가 “어떤 일이 일어났는가”를 기록했다면, TAG 예제는 “어느 대상의 값이 언제 얼마였는가”를
기록합니다. 이 차이를 기억하면 다음 장의 테이블 설계 문서를 훨씬 수월하게 읽을 수 있습니다.
재실행 중 `DBMS_GS_TAG`가 이미 존재한다는 오류가 나면
`DROP TABLE DBMS_GS_TAG;`를 실행한 뒤 다시 시작합니다.
