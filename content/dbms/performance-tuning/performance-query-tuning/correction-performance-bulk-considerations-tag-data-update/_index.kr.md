---
type: docs
title: 'TAG data UPDATE 대상 범위와 대량 정정 성능 고려사항'
weight: 40
---

TAG data UPDATE는 잘못 적재된 시계열 값을 직접 정정할 수 있는 기능입니다. 성능과 운영
위험을 관리하려면 태그 선택 조건과 시간 조건으로 대상 범위를 명확히 제한해야 합니다.

## 기본 정정 패턴

```sql
-- 1단계: 대상 범위 확인
SELECT COUNT(*), MIN(value), MAX(value)
  FROM sensor_tag
 WHERE name = 'TEMP-01'
   AND time >= TO_DATE('2025-06-01 12:00:00', 'YYYY-MM-DD HH24:MI:SS')
   AND time <  TO_DATE('2025-06-01 13:00:00', 'YYYY-MM-DD HH24:MI:SS');

-- 2단계: 값 정정
UPDATE sensor_tag
   SET value = 99.5,
       corrected = 1
 WHERE name = 'TEMP-01'
   AND time >= TO_DATE('2025-06-01 12:00:00', 'YYYY-MM-DD HH24:MI:SS')
   AND time <  TO_DATE('2025-06-01 13:00:00', 'YYYY-MM-DD HH24:MI:SS');
```

INSERT 직후의 append 데이터는 내부 반영 지연이 있을 수 있으므로, UPDATE 전 대상 row가
조회되는지 확인합니다.

## 대량 정정 성능 고려사항

| 항목 | 권장 사항 |
|------|-----------|
| 태그 조건 | `name =`, `name IN`, `name LIKE` 중 필요한 최소 범위 사용 |
| 시간 조건 | 가능한 좁은 시간 구간으로 분할 |
| 대상 확인 | UPDATE 전 동일 WHERE 조건으로 `SELECT COUNT(*)` 실행 |
| 추가 predicate | `value > ...` 같은 데이터 조건은 대상 row를 줄이는 데 사용 |
| 롤업 처리 | 롤업 조회가 필요하면 UPDATE 후 `ROLLUP_REBUILD` 실행 |
| 배치 크기 | 긴 구간은 시간 단위로 나누어 실행하고 각 배치 결과를 확인 |

## 여러 태그 정정

```sql
UPDATE sensor_tag
   SET value = value * 0.98
 WHERE name IN ('TEMP-01', 'TEMP-02')
   AND time BETWEEN TO_DATE('2025-06-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
                AND TO_DATE('2025-06-01 23:59:59', 'YYYY-MM-DD HH24:MI:SS');
```

`LIKE` 조건은 태그 메타 영역에서 패턴에 맞는 태그를 확장한 뒤 UPDATE 대상이 됩니다. 패턴이
넓으면 예상보다 많은 태그가 수정될 수 있으므로 사전 COUNT를 반드시 수행합니다.

```sql
SELECT COUNT(*)
  FROM sensor_tag
 WHERE name LIKE 'TEMP-%'
   AND time >= TO_DATE('2025-06-01', 'YYYY-MM-DD')
   AND time <  TO_DATE('2025-06-02', 'YYYY-MM-DD');
```

## 롤업 재구성

원본 row UPDATE 후 이미 생성된 롤업 row는 즉시 갱신되지 않을 수 있습니다. 정정 구간을
롤업 기반 조회에 사용한다면 필요한 롤업을 재구성합니다.

```sql
EXEC ROLLUP_REBUILD(sensor_tag, 'TEMP-01',
    TO_DATE('2025-06-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'),
    TO_DATE('2025-06-02 00:00:00', 'YYYY-MM-DD HH24:MI:SS'));
```

## 정정 작업 체크리스트

- [ ] 대상 태그 조건과 시간 범위를 확정
- [ ] UPDATE 전 `SELECT COUNT(*)`와 값 범위 확인
- [ ] 긴 구간은 배치로 분할
- [ ] UPDATE 후 원본 TAG 테이블에서 변경 값 검증
- [ ] 롤업 조회가 필요하면 `ROLLUP_REBUILD` 실행
- [ ] 대시보드/보고서 결과 검증
