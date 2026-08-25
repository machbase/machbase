---
type: docs
title: '12.1 성능 문제 접근 순서'
weight: 10
toc: true
aliases:
  - /dbms/performance-tuning/checklist-performance-diagnosis/
---

성능 문제는 재현 조건과 기준값을 확보한 뒤 병목을 좁혀야 합니다. 근거 없이 property나
index를 여러 개 동시에 바꾸면 원인과 효과를 구분할 수 없습니다.

## 1. 재현 조건 기록

- 느려진 SQL 또는 입력 경로
- 시작·종료 시각과 database·사용자
- 대상 table, 시간 범위, row 수와 결과 건수
- 동시 session·query·Appender 수
- 정상 시점과 문제 시점의 지연·처리량
- 직전 배포, schema, property, 데이터 분포 변화

## 2. 자원 병목 확인

```bash
iostat -x 1 5
top -b -n 1
free -h
```

CPU·I/O·memory 수치는 고정 임계값보다 정상 시점 baseline과 비교합니다. 짧은 spike와
지속적인 포화를 구분하고, OS 지표 시각을 server trace·query 시각과 맞춥니다.

## 3. 실행 중 작업 확인

```sql
SELECT sess_id, id AS stmt_id, state, record_size, query
FROM V$STMT
ORDER BY sess_id, id;

SELECT id, user_name, user_ip, login_time, client_type
FROM V$SESSION
ORDER BY login_time DESC;
```

장시간 statement, 비정상적으로 늘어난 session, 같은 query의 동시 실행을 찾습니다. system
view 컬럼은 배포 버전에서 `DESC`로 확인합니다.

## 4. 실행 계획과 범위 확인

느린 SELECT는 `EXPLAIN`으로 table, scan 종류, key range, filter, join을 확인합니다. TAG·LOG
query에 시간 범위가 있는지, 조건이 함수나 형변환 때문에 index range에서 제외되는지
점검합니다.

상세 절차는 [조회와 분석 성능 튜닝](../performance-query-tuning/)을 참고합니다.

## 5. 한 가지 변경 후 재측정

변경 후보는 query, index, batch, 동시성, cache·property 순서로 좁힙니다. 한 번에 하나만
바꾸고 같은 재현 조건에서 다음을 비교합니다.

| 항목 | 비교값 |
|------|--------|
| query | 응답 시간 분포, 결과 row, plan |
| 입력 | rows/s, ack 지연, 실패 건수 |
| server | CPU, I/O, memory, session |
| 부작용 | 다른 query 지연, 입력 저하, restart 영향 |

효과가 없거나 부작용이 크면 기록한 이전 값으로 되돌립니다. schema나 storage 구조 변경은
마지막 수단으로 검토하고, staging과 복구 절차를 먼저 준비합니다.

## 최종 진단 체크리스트

- 현재 작업과 session을 정상 baseline과 비교했는가
- 실제 SQL과 시간 범위로 실행 계획을 확인했는가
- index·ROLLUP 변경이 입력 비용에 미치는 영향을 확인했는가
- OS와 서버 지표의 시각을 같은 작업과 맞췄는가
- property·schema 변경을 한 번에 하나씩 적용했는가
- 원복 값과 재측정 결과를 기록했는가
