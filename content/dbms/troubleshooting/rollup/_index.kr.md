---
type: docs
title: '16.7 ROLLUP 문제'
weight: 70
toc: true
aliases:
  - /dbms/tag-rollup-usage/constraints-errors-troubleshooting/rollup-troubleshooting/
---

ROLLUP 결과가 늦거나 원본 집계와 다를 때 상태, gap, 대상 시간 범위와 재구성 필요 여부를
순서대로 확인합니다.

## 1. 상태와 gap 확인

```sql
SHOW ROLLUPGAP;

SELECT ROLLUP_TABLE,
       INTERVAL_TIME,
       WAKEUP_INTERVAL,
       LAST_ELAPSED_MSEC,
       RUN_STATE
  FROM V$ROLLUP
 ORDER BY ROLLUP_TABLE;
```

- gap이 남아 있으면 새 데이터의 집계가 아직 끝나지 않은 상태일 수 있습니다.
- `RUN_STATE`가 계속 비정상이면 서버 로그에서 같은 시각의 최초 오류를 확인합니다.
- WAKEUP 주기보다 짧은 지연만으로 장애라고 판단하지 않습니다.

가상 테이블의 정확한 컬럼은
[V$ROLLUP 사전](/dbms/reference/log-logs-system-catalog/dictionary-vrollup/)을 기준으로 합니다.

## 2. 원본과 같은 범위를 비교

태그, 시작·종료 시각과 bucket을 고정한 뒤 원본 집계와 ROLLUP 조회를 비교합니다. 서로 다른
시간대, 열린 종료 경계와 다른 bucket 크기를 섞지 마십시오.

```sql
SELECT rollup('min', 1, time) AS bucket,
       AVG(value), MIN(value), MAX(value), COUNT(value)
  FROM sensor_tag
 WHERE name = 'sensor-01'
   AND time >= TO_DATE('2026-01-01 12:00:00')
   AND time <  TO_DATE('2026-01-01 12:10:00')
 GROUP BY bucket
 ORDER BY bucket;
```

같은 SQL을 ROLLUP 사용 전후의 실행 계획과 결과로 비교합니다. 존재하지 않는 내부 ROLLUP
테이블이나 미확인 hint를 진단용으로 만들지 마십시오.

## 3. 즉시 집계와 재확인

정상적으로 유입된 새 데이터의 집계를 촉진할 때 다음 명령을 사용할 수 있습니다.

```sql
ALTER SYSTEM FLUSH ROLLUP;
SHOW ROLLUPGAP;
```

반복 실행으로 오류를 숨기지 말고 gap 감소와 서버 로그를 함께 확인합니다.

## 4. 데이터 보정 뒤 재구성

TAG 원본을 수정했거나 과거 범위의 집계가 잘못된 경우에는 Standard Edition의
`ROLLUP_REBUILD` 적용 조건을 확인합니다. Cluster Edition에서는 지원하지 않습니다.

```sql
EXEC ROLLUP_REBUILD(
    sensor_tag,
    'sensor-01',
    TO_DATE('2026-01-01 00:00:00'),
    TO_DATE('2026-01-02 00:00:00')
);
```

정확한 인수, 범위와 검증 절차는
[ROLLUP_REBUILD](/dbms/tag-rollup-usage/rollup-rebuild/)를 참고하십시오.

## 5. 지원 요청 자료

- 서버 build와 Edition
- ROLLUP 정의와 대상 TAG schema
- `SHOW ROLLUPGAP`과 `V$ROLLUP` 결과
- 비교한 태그·시간 범위·SQL
- 최초 서버 오류와 발생 시각
- 최근 TAG 수정, 대량 입력과 ROLLUP 설정 변경 이력
