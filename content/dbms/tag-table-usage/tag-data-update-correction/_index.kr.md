---
title: '5.11 TAG data UPDATE와 데이터 보정'
weight: 110
toc: true
---


<a id="correction-performance-bulk-considerations-tag-data-update"></a>

## TAG data UPDATE 대상 범위와 대량 정정 성능 고려사항

잘못 적재된 시계열 값을 직접 정정하려면 태그 선택 조건과 시간 조건으로 대상 범위를 명확히 제한해야 합니다.

<span class="badge-since">Machbase 8.7.0부터 지원되는 기능</span>

TAG data UPDATE는 Standard Edition의 논리 TAG 테이블에서만 지원합니다. SET 우변에서는
기존 행의 컬럼을 참조할 수 없으므로 보정값을 상수 또는 bind 변수로 계산해 전달합니다.

### 기본 정정 패턴

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

INSERT 직후 UPDATE를 이어서 실행하는 수집 경로에서는 대상 행이 조회되는지 먼저 확인합니다.

### 대량 정정 성능 고려사항

| 항목 | 권장 사항 |
|------|-----------|
| 태그 조건 | `name =`, `name IN`, `name LIKE` 중 필요한 최소 범위 사용 |
| 시간 조건 | 가능한 좁은 시간 구간으로 분할 |
| 대상 확인 | UPDATE 전 동일 WHERE 조건으로 `SELECT COUNT(*)` 실행 |
| 추가 predicate | `value > ...` 같은 데이터 조건은 대상 row를 줄이는 데 사용 |
| 롤업 처리 | 롤업 조회가 필요하면 UPDATE 후 `ROLLUP_REBUILD` 실행 |
| 배치 크기 | 긴 구간은 시간 단위로 나누어 실행하고 각 배치 결과를 확인 |

### 여러 태그 정정

```sql
UPDATE sensor_tag
   SET value = 99.5
 WHERE name IN ('TEMP-01', 'TEMP-02')
   AND time BETWEEN TO_DATE('2025-06-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
                AND TO_DATE('2025-06-01 23:59:59', 'YYYY-MM-DD HH24:MI:SS');
```

`LIKE` 조건은 태그 메타 영역에서 패턴에 맞는 태그를 확장한 뒤 UPDATE 대상이 됩니다. 패턴이
넓으면 예상보다 많은 태그가 수정될 수 있으므로 사전 COUNT를 반드시 수행합니다.

`IN`과 `LIKE`로 여러 태그를 수정하는 작업은 태그별로 순차 처리될 수 있습니다. 한 태그 처리
후 오류가 반환될 수 있으므로 문장 전체 원자성을 가정하지 않습니다. 오류 후에는 결과를
조회하고 처리되지 않은 태그로 조건을 좁혀 다시 실행합니다. 같은 문장을 그대로 다시 실행하는
방법은 상수 대입처럼 반복 실행 결과가 동일한 멱등 UPDATE에만 사용합니다.

```sql
SELECT COUNT(*)
  FROM sensor_tag
 WHERE name LIKE 'TEMP-%'
   AND time >= TO_DATE('2025-06-01', 'YYYY-MM-DD')
   AND time <  TO_DATE('2025-06-02', 'YYYY-MM-DD');
```

### 롤업 재구성

원본 row를 UPDATE해도 이미 구체화된 롤업 row는 자동으로 갱신되지 않습니다. 정정 구간을
롤업 기반 조회에 사용하기 전에 필요한 롤업을 재구성합니다.

```sql
EXEC ROLLUP_REBUILD(sensor_tag, 'TEMP-01',
    TO_DATE('2025-06-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'),
    TO_DATE('2025-06-02 00:00:00', 'YYYY-MM-DD HH24:MI:SS'));
```

### 정정 작업 체크리스트

- [ ] 대상 태그 조건과 시간 범위를 확정
- [ ] UPDATE 전 `SELECT COUNT(*)`와 값 범위 확인
- [ ] 긴 구간은 배치로 분할
- [ ] UPDATE 후 원본 TAG 테이블에서 변경 값 검증
- [ ] 롤업 조회가 필요하면 `ROLLUP_REBUILD` 실행
- [ ] 대시보드/보고서 결과 검증

<a id="design-correction-tag"></a>

## 데이터 보정 설계

실제 시계열 데이터를 `UPDATE`로 정정할 때, 보정 이력을 남기거나
조회 시점에 보정 로직이 필요한 업무에서는 별도 보정 컬럼/이력 테이블 패턴을 함께 사용합니다.

### 직접 UPDATE 패턴

잘못 적재된 값을 원본 TAG row에서 직접 수정합니다.

```sql
UPDATE sensor_data
   SET raw_value = 25.3,
       is_corrected = 1
 WHERE name = 'sensor-01'
   AND time = TO_DATE('2026-07-01 12:00:00', 'YYYY-MM-DD HH24:MI:SS');
```

UPDATE에는 태그 선택 조건과 BASETIME 조건이 필요합니다. `name`과 `time` 자체는 변경할 수
없습니다.

### 보정 플래그 패턴

원본 값과 보정 값을 별도 컬럼에 저장하고, 조회 시 보정 값을 우선 사용하는 패턴입니다.
최초 원본과 현재 보정값을 함께 유지할 때 적합합니다. 여러 차례 보정한 변경 이력까지
보존하려면 아래의 별도 이력 테이블도 사용합니다.

```sql
CREATE TAG TABLE sensor_data (
    name          VARCHAR(64) PRIMARY KEY,
    time          DATETIME    BASETIME,
    raw_value     DOUBLE,
    corrected     DOUBLE,
    is_corrected  SHORT
);

SELECT name, time,
       CASE WHEN corrected IS NOT NULL THEN corrected ELSE raw_value END AS value
FROM sensor_data
WHERE name = 'sensor-01'
  AND time >= NOW - 3600000000000;
```

### 보정 이력 테이블 패턴

감사 추적이 필요하면 보정 내용을 별도 LOG/TRANSACTION 테이블에 기록합니다.

```sql
CREATE LOG TABLE correction_log (
    sensor_name  VARCHAR(64),
    target_time  DATETIME,
    old_value    DOUBLE,
    new_value    DOUBLE,
    reason       VARCHAR(256),
    corrected_by VARCHAR(64)
);
```

### 주의사항

- 대량 UPDATE 전 동일 WHERE 조건으로 대상 row 수를 확인합니다.
- 이미 계산된 롤업을 사용하는 경우 UPDATE 후 `ROLLUP_REBUILD`를 실행합니다.
- 보정이 매우 빈번하고 이력 보존이 필수라면 보정 컬럼 또는 보정 이력 테이블을 함께 설계합니다.
