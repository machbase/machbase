---
type: docs
title: '6.10 ROLLUP_REBUILD'
weight: 100
toc: true
aliases:
  - /dbms/tag-rollup-usage/delete-partial-rebuild-rollup/
---

TAG 원본 데이터를 보정한 뒤 영향받은 태그와 시간 범위의 ROLLUP 집계를 다시 계산합니다.
`ROLLUP_REBUILD`는 Standard Edition에서만 지원합니다.

## DROP·재생성과 부분 재구성 선택

| 상황 | 시작점 |
|---|---|
| 소수 태그의 제한된 과거 범위를 보정 | `ROLLUP_REBUILD` |
| ROLLUP 정의 자체를 변경 | 기존 ROLLUP 삭제 후 새 정의로 생성 |
| 대상 범위를 확정할 수 없음 | 원본과 ROLLUP 영향 범위를 먼저 조사 |
| Cluster Edition | 지원되지 않으므로 승인된 복구 절차 확인 |

DROP과 재생성은 전체 집계 상태에 영향을 줄 수 있습니다. 운영 적용 전 ROLLUP 정의, gap,
원본 보정 범위와 조회 영향을 기록합니다.

## 사전 확인

1. 수정한 TAG 이름과 BASETIME 시작·종료 경계를 확정합니다.
2. 같은 범위의 원본 행 수와 대표 값을 확인합니다.
3. `SHOW ROLLUPGAP`과 `V$ROLLUP` 상태를 기록합니다.
4. 실행 중 대시보드와 집계 query의 허용 지연을 정합니다.
5. 종료 시각을 포함할지 여부를 표본 데이터로 확인합니다.

## 실행

```sql
EXEC ROLLUP_REBUILD(
    sensor_tag,
    'sensor-01',
    TO_DATE('2026-01-01 00:00:00'),
    TO_DATE('2026-01-02 00:00:00')
);
```

테이블, 태그와 시간 범위를 문자열 결합으로 만들지 말고 운영 도구에서 검증된 입력만
사용합니다. 큰 범위는 업무상 검증 가능한 구간으로 나눠 실행합니다.

## 결과 검증

```sql
SHOW ROLLUPGAP;

SELECT rollup('hour', 1, time) AS bucket,
       AVG(value), MIN(value), MAX(value), COUNT(value)
  FROM sensor_tag
 WHERE name = 'sensor-01'
   AND time >= TO_DATE('2026-01-01 00:00:00')
   AND time <  TO_DATE('2026-01-02 00:00:00')
 GROUP BY bucket
 ORDER BY bucket;
```

다음 항목을 원본 집계 또는 보정 전 기록과 비교합니다.

- bucket 개수와 시작·종료 시각
- `COUNT`, `MIN`, `MAX`, `AVG`
- 보정한 경계 시각의 첫·마지막 bucket
- ROLLUP gap과 서버 오류 로그

결과가 다르면 반복 실행하기 전에 [ROLLUP 문제 해결](/dbms/troubleshooting/rollup/)의 순서로
시간 경계, 상태와 Edition을 확인합니다.

## ROLLUP 정의 변경

집계 간격, 조건, source 또는 EXTENSION 속성을 바꾸려면 기존 ROLLUP을 삭제하고 새 정의로
생성합니다. 정확한 구문은 [ROLLUP 문법](/dbms/reference/sql/syntax-dictionary-sql/rollup-syntax/)을
사용하고, 삭제 전 의존 query와 재집계 시간을 확인하십시오.
