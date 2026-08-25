---
title: '7.6 인덱스와 성능'
weight: 60
toc: true
---

LOG 테이블은 조회 조건에 따라 LSM, KEYWORD, BITMAP 인덱스를 사용할 수 있습니다. 인덱스는
입력과 저장 비용을 늘리므로 대표 쿼리의 실행 계획을 측정한 뒤 추가합니다.

<a id="index-tuning-log"></a>

## 인덱스 선택

| 조회 조건 | 시작점 |
|---|---|
| DATETIME·숫자 범위 | LSM |
| VARCHAR/TEXT 단어 검색 | KEYWORD와 `SEARCH`/`ESEARCH` |
| 반복 값의 분석 조건 | 지원 타입의 BITMAP |

`_ARRIVAL_TIME` 범위는 LOG 테이블의 기본 시간 접근 경로를 먼저 사용합니다. 같은 목적의
인덱스를 관성적으로 추가하지 말고 `EXPLAIN`과 실제 실행 시간을 비교하십시오.

## 검증 예제

```sql
CREATE LOG TABLE sc7_index_log (
    event_time DATETIME,
    level      SHORT,
    message    VARCHAR(256)
);

CREATE INDEX sc7_idx_event_time
    ON sc7_index_log(event_time);
CREATE INDEX sc7_idx_message
    ON sc7_index_log(message) INDEX_TYPE KEYWORD;
CREATE INDEX sc7_idx_level
    ON sc7_index_log(level)
    INDEX_TYPE BITMAP BITMAP_ENCODE = RANGE;

INSERT INTO sc7_index_log VALUES (SYSDATE, 1, 'service started');
INSERT INTO sc7_index_log VALUES (SYSDATE, 3, 'database timeout');
EXEC TABLE_FLUSH(sc7_index_log);

EXPLAIN SELECT _arrival_time, event_time, level, message
  FROM sc7_index_log
 WHERE message SEARCH 'timeout';

SHOW INDEXES;

DROP INDEX sc7_idx_level;
DROP INDEX sc7_idx_message;
DROP INDEX sc7_idx_event_time;
DROP TABLE sc7_index_log;
```

인덱스 생성 전후에는 동일한 데이터량, 바인드 값과 동시 부하로 비교합니다. 쓰기 처리량,
인덱스 저장 공간과 flush 시간도 함께 기록하십시오. 정확한 속성과 table type 지원 범위는
[INDEX 문법](/dbms/reference/sql/syntax-dictionary-sql/index-syntax/)을, 진단 절차는
[인덱스 튜닝](/dbms/performance-tuning/index-tuning/)을 참고하십시오.
