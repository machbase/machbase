---
type: docs
title: '12.9 성능 진단 체크리스트'
weight: 90
toc: true
---

다음 순서로 현재 상태와 정상 baseline의 차이를 좁힙니다.

## 현재 작업

```sql
SELECT sess_id, id AS stmt_id, state, record_size, query
FROM V$STMT
ORDER BY sess_id, id;

SELECT id, user_name, user_ip, login_time, client_type
FROM V$SESSION
ORDER BY login_time DESC;
```

- 오래 남은 execute·fetch가 있는가
- 같은 query가 예상보다 많이 동시 실행되는가
- session 수가 설정 한도에 가까운가
- Appender가 정상적으로 close되는가

## 실행 계획

느린 SQL을 실제 table과 시간 범위로 `EXPLAIN`합니다.

- 의도한 table과 index가 선택되는가
- TAG·LOG 시간 범위가 key range에 반영되는가
- 큰 table scan이 join 안에서 반복되는가
- 함수·형변환이 index 조건을 filter로 바꾸는가
- 결과와 NULL 분포가 원래 SQL과 같은가

## Index와 ROLLUP

- 조회 조건에 맞는 index가 있는가
- 쓰기 비용만 늘리는 미사용 index가 있는가
- 반복 장기 집계가 원본을 매번 읽는가
- ROLLUP 상태와 집계 지연이 허용 범위 안인가

```sql
SHOW ROLLUPGAP;
```

## OS 자원

```bash
iostat -x 1 5
top -b -n 1
free -h
```

고정된 CPU·I/O·memory 비율만으로 병목을 판정하지 않습니다. 문제 시각의 지속 시간,
정상 baseline, queue·latency, swap 변화와 query·입력 지연을 함께 비교합니다.

## 변경 전 확인

- property 현재값과 변경 근거를 기록했는가
- 변경을 하나씩 적용하는가
- 같은 데이터·동시성으로 재측정하는가
- 입력·다른 query에 미치는 부작용을 확인하는가
- 원복 값과 실행 순서를 준비했는가
- restart가 필요한 설정인지 레퍼런스에서 확인했는가

## 진단 결과 기록

재현 SQL·입력, 측정 구간, plan, server·OS 지표, 적용 변경, 전후 결과를 하나의 기록으로
남깁니다. 문제가 재현되지 않으면 추정 설정을 적용하지 말고 관찰 항목과 다음 재현 조건을
정의합니다.
