---
type: docs
title: '18.6.4 TAG data UPDATE 지원표'
weight: 40
toc: true
---

TAG 테이블의 실제 시계열 데이터는 `UPDATE table_name SET ... WHERE ...` 구문으로
수정할 수 있습니다. 이 페이지는 TAG data UPDATE에서 허용되는 WHERE 조건과 SET 대상을
정리합니다. 메타데이터 수정은 별도의 `UPDATE ... METADATA` 구문을 사용합니다.

<span class="badge-since">Machbase 8.7.0부터 지원되는 기능</span>

TAG data UPDATE는 Standard Edition의 논리 TAG 테이블에서만 지원합니다. Cluster Edition과
내부 raw component table에 대한 직접 UPDATE는 지원하지 않습니다.

## WHERE 조건별 지원 현황

TAG data UPDATE에는 하나의 태그 선택 조건과 하나 이상의 BASETIME 축 조건이 필요합니다.

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
| 서브쿼리/집계식 | X | UPDATE 대상 결정 조건으로 사용할 수 없음 |
| 태그/축 컬럼을 함수·연산식으로 감싼 표현식 | X | 태그 선택자와 BASETIME은 해당 컬럼을 직접 지정해야 함 |

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

SET 표현식에는 상수, bind 변수, 기존 행 컬럼을 참조하지 않는 산술식·함수·`CASE`
표현식·문자열 연결, NULL 값(컬럼 제약이 허용하는 경우)을 사용할 수 있습니다. SET
우변에서 기존 행 컬럼을 참조할 수 없으며, 서브쿼리와 집계식도 사용할 수 없습니다.

## 지원되는 UPDATE 예시

```sql
UPDATE sensor_data
   SET value = 110,
       status = 1
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
- 여러 태그를 대상으로 하는 UPDATE는 태그별로 순차 처리될 수 있으며 문장 전체가 원자적으로
  처리된다고 가정하지 않습니다. 오류 또는 중단 후에는 결과를 조회해 반영 여부를 확인하고,
  처리되지 않은 태그로 선택 조건을 좁혀 다시 실행합니다. 상수 대입처럼 반복 실행 결과가
  동일한 멱등 UPDATE인 경우에만 같은 문장을 그대로 다시 실행합니다.
- 대상 row가 없거나 시간 범위의 시작이 끝보다 뒤인 경우에는 오류가 아니라 영향받은 행 수
  0으로 완료될 수 있습니다. 실제 값이 바뀌지 않는 대상 row도 영향받은 행 수에 포함됩니다.
- 원본 row의 `SUMMARIZED` 통계와 관련 인덱스는 변경값에 맞게 갱신되며, 변경 내용은 flush와
  재시작 후에도 유지됩니다.
- INSERT 직후의 append 데이터는 내부 반영 지연이 있을 수 있으므로 UPDATE 전 대상 행이
  조회되는지 확인합니다.
- 원본 TAG 데이터가 수정되면 이미 생성된 롤업 데이터는 즉시 재계산되지 않을 수 있습니다.
  root, custom, extension rollup 모두 원본 UPDATE 자체는 허용되지만 materialized rollup은
  stale 상태로 남을 수 있으므로 정정 구간을 롤업 조회에 사용하기 전에 `ROLLUP_REBUILD`로
  필요한 롤업을 재구성합니다.
