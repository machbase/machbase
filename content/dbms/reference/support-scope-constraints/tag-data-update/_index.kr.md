---
type: docs
title: '18.8.4 TAG data UPDATE 지원표'
weight: 40
toc: true
---

TAG 테이블의 실제 시계열 데이터는 `UPDATE table_name SET ... WHERE ...` 구문으로
수정할 수 있습니다. 이 페이지는 TAG data UPDATE에서 허용되는 WHERE 조건과 SET 대상을
정리합니다. 메타데이터 수정은 별도의 `UPDATE ... METADATA` 구문을 사용합니다.

## WHERE 조건별 지원 현황

TAG data UPDATE에는 태그 선택 조건과 시간 축 조건이 모두 필요합니다.

| WHERE 조건 | 지원 | 비고 |
|-----------|:---:|------|
| `name = 'tag-01'` | O | 단일 태그 선택 |
| `name IN ('tag-01', 'tag-02')` | O | 리터럴/바인드 값 목록 지원, 서브쿼리 `IN`은 미지원 |
| `name LIKE 'tag-%'` | O | 패턴에 맞는 태그를 대상으로 확장 |
| `time = t1` | O | BASETIME 컬럼 등치 조건 |
| `time BETWEEN t1 AND t2` | O | 양 끝 포함 |
| `time >= t1 AND time < t2` | O | `>`, `>=`, `<`, `<=` 조합 지원 |
| 한쪽 시간 조건 | O | 예: `time >= t1` |
| 데이터 컬럼 predicate | O | 예: `value > 100`, 태그/시간 조건과 함께 사용 |
| 조건 없는 UPDATE | X | 전체 TAG data UPDATE는 허용하지 않음 |
| 태그 선택 없는 시간 조건만 사용 | X | 대상 태그를 지정해야 함 |
| 시간 조건 없는 태그 조건만 사용 | X | BASETIME 범위를 지정해야 함 |
| `OR` 조건 | X | TAG data UPDATE 조건에서는 허용하지 않음 |
| 서브쿼리/집계/비결정 predicate | X | UPDATE 대상 결정 조건으로 사용할 수 없음 |

## SET 대상 컬럼별 지원 현황

| SET 대상 | 지원 | 비고 |
|---------|:---:|------|
| 데이터 컬럼 | O | `value`, 보조 컬럼 등 사용자 데이터 컬럼 |
| `SUMMARIZED` 데이터 컬럼 | O | 원본 TAG 데이터가 갱신됨 |
| 여러 데이터 컬럼 | O | 같은 UPDATE 문에서 함께 지정 가능 |
| `name` (PRIMARY KEY) | X | 태그 이름은 변경할 수 없음 |
| `time` (BASETIME) | X | 시간 축 컬럼은 변경할 수 없음 |
| 메타데이터 컬럼 | X | `UPDATE table_name METADATA SET ...` 사용 |
| 숨김/시스템 컬럼 | X | 내부 컬럼은 UPDATE 대상이 아님 |

SET 표현식에는 상수, 기존 행의 컬럼 참조, 산술식, `CASE` 표현식, 문자열 연결, NULL
값(컬럼 제약이 허용하는 경우)을 사용할 수 있습니다. 같은 UPDATE 문에서 여러 컬럼을
수정할 때 RHS 표현식은 기존 행 값을 기준으로 평가됩니다.

## 지원되는 UPDATE 예시

```sql
UPDATE sensor_data
   SET value = value + 10,
       status = status + 1
 WHERE name = 'TEMP-01'
   AND time >= TO_DATE('2026-07-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
   AND time <  TO_DATE('2026-07-02 00:00:00', 'YYYY-MM-DD HH24:MI:SS');

UPDATE sensor_data
   SET note = 'checked'
 WHERE name IN ('TEMP-01', 'TEMP-02')
   AND time BETWEEN TO_DATE('2026-07-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
                AND TO_DATE('2026-07-01 23:59:59', 'YYYY-MM-DD HH24:MI:SS')
   AND value > 100;

UPDATE sensor_data
   SET status = 7
 WHERE name LIKE 'TEMP-%'
   AND time >= TO_DATE('2026-07-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS');
```

## 거부되는 UPDATE 예시

```sql
-- 태그 선택 조건 없음
UPDATE sensor_data SET value = 0
WHERE time >= TO_DATE('2026-07-01', 'YYYY-MM-DD');

-- 시간 조건 없음
UPDATE sensor_data SET value = 0
WHERE name = 'TEMP-01';

-- PRIMARY KEY/BASETIME/메타데이터 컬럼은 data UPDATE에서 SET 불가
UPDATE sensor_data SET name = 'TEMP-02'
WHERE name = 'TEMP-01' AND time >= TO_DATE('2026-07-01', 'YYYY-MM-DD');

UPDATE sensor_data SET time = NOW
WHERE name = 'TEMP-01' AND time >= TO_DATE('2026-07-01', 'YYYY-MM-DD');
```

## 운영 시 주의사항

- 대량 UPDATE 전에는 같은 WHERE 조건으로 `SELECT COUNT(*)`를 실행해 대상 범위를 확인합니다.
- `LIKE`와 `IN`은 여러 태그로 확장될 수 있으므로 시간 조건을 함께 좁게 지정합니다.
- INSERT 직후의 append 데이터는 내부 반영 지연이 있을 수 있으므로 UPDATE 전 대상 행이
  조회되는지 확인합니다.
- 원본 TAG 데이터가 수정되면 이미 생성된 롤업 데이터는 즉시 재계산되지 않을 수 있습니다.
  정정 구간을 조회에 사용한다면 `ROLLUP_REBUILD`로 필요한 롤업을 재구성합니다.
