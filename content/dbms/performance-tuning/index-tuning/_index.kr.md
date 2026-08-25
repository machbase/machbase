---
type: docs
title: '12.3 인덱스 튜닝'
weight: 30
toc: true
---

인덱스는 실제 predicate와 join key의 읽기 비용을 줄일 때만 추가합니다. 생성 전후의 query
지연, 입력 처리량, memory·storage를 함께 측정합니다.

## Table별 확인

| table type | 기본 key·접근 경로 | 추가 index |
|------------|--------------------|------------|
| TAG | 이름과 BASETIME 기반 접근 | 지원 값·metadata index |
| LOG | `_ARRIVAL_TIME` 범위 | LSM, BITMAP, KEYWORD |
| LOOKUP | PRIMARY KEY | 지원 보조 index |
| VOLATILE | 선택한 PRIMARY KEY | REDBLACK 보조 index |
| TRANSACTION | PRIMARY KEY | 관계형 보조 index |

지원되는 index type과 구문은 table별 장과
[index 구문](/dbms/reference/sql/syntax-dictionary-sql/index-syntax/)을 확인합니다.

## 적용 순서

1. 느린 SQL의 `EXPLAIN`과 결과 건수를 기록합니다.
2. predicate의 선택도와 값 분포를 확인합니다.
3. 이미 같은 선두 컬럼을 가진 index가 있는지 확인합니다.
4. 후보 index 하나를 생성하고 구축 완료를 확인합니다.
5. 같은 조건에서 query와 입력을 다시 측정합니다.
6. 효과가 없거나 쓰기 비용이 큰 index는 제거합니다.

```sql
SHOW INDEXES;
SHOW INDEXGAP;
```

고정된 “index 개수별 처리량 감소율”을 적용하지 않습니다. row 크기, key 분포, 동시성,
storage에 따라 결과가 달라지므로 운영과 유사한 데이터로 측정합니다.

## 주의사항

- 낮은 선택도의 컬럼에 index를 추가하기 전에 scan과 비교합니다.
- 함수·형변환으로 index 컬럼을 감싸 key range를 잃지 않는지 확인합니다.
- 복합 index는 자주 쓰는 predicate 조합과 선두 컬럼을 기준으로 설계합니다.
- index 구축 중 입력·query 부하와 `SHOW INDEXGAP`을 관찰합니다.
- 미사용 index를 제거하기 전 peak·batch 업무에서도 쓰이지 않는지 확인합니다.

table별 상세 내용은 TAG, LOG, LOOKUP, VOLATILE, TRANSACTION 장의 “인덱스와 성능” 페이지를
참고합니다.
