---
type: docs
title: 'STREAM 상태 확인 (V$STREAMS)'
weight: 50
---

`V$STREAMS` 가상 테이블에서 등록된 모든 STREAM의 현재 상태를 조회할 수 있습니다.

## V$STREAMS 컬럼

| 컬럼 | 설명 |
|------|------|
| NAME | STREAM 이름 |
| STATE | 현재 상태 (RUNNING / STOPPED / ERROR) |
| TABLE_NAME | 소스 테이블 이름 |
| END_RID | 마지막으로 처리한 행의 RID |
| LAST_EX_TIME | 마지막 실행 시각 |
| QUERY_TXT | 등록된 쿼리 원문 |
| FREQUENCY | 실행 주기 (나노초, 0이면 매 행마다 실행) |
| ERROR_MSG | 마지막 오류 메시지 (오류 없으면 NULL) |

## 조회 예시

```sql
-- 전체 STREAM 상태 조회
SELECT NAME, STATE, TABLE_NAME, LAST_EX_TIME, ERROR_MSG
FROM   V$STREAMS
ORDER BY NAME;
```

```sql
-- 실행 중인 STREAM만 조회
SELECT NAME, LAST_EX_TIME, END_RID
FROM   V$STREAMS
WHERE  STATE = 'RUNNING';
```

```sql
-- 오류 발생 STREAM 확인
SELECT NAME, STATE, ERROR_MSG
FROM   V$STREAMS
WHERE  STATE = 'ERROR';
```

```sql
-- 특정 STREAM 쿼리 확인
SELECT QUERY_TXT
FROM   V$STREAMS
WHERE  NAME = 'stream_agg_10s';
```

## 상태별 대응

| STATE | 의미 | 조치 |
|-------|------|------|
| RUNNING | 정상 실행 중 | 없음 |
| STOPPED | 중지됨 | 필요시 STREAM_START 재실행 |
| ERROR | 오류로 중단 | ERROR_MSG 확인 후 원인 해결, 재시작 |

## FREQUENCY 해석

FREQUENCY 값은 나노초(ns) 단위입니다.

| FREQUENCY | 실행 조건 |
|-----------|-----------|
| 0 | 매 행 입력마다 즉시 실행 |
| 1,000,000,000 | 1초마다 실행 |
| 60,000,000,000 | 60초마다 실행 |
| -1 | BY USER (수동 실행) |
