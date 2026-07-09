---
type: docs
title: '6.15.1 TAG data UPDATE와 통계/롤업 영향'
weight: 40
---

TAG data UPDATE는 원본 TAG row를 수정합니다. 원본 row와 통계/인덱스는 UPDATE 대상에 맞게
처리되지만, 이미 만들어진 롤업 데이터는 별도 재구성이 필요할 수 있습니다.

## UPDATE 후 영향을 받는 구조

### 원본 TAG row

`UPDATE tag SET value = ... WHERE name ... AND time ...` 문은 조건에 맞는 원본 TAG row의
데이터 컬럼을 변경합니다.

### 통계 정보와 인덱스

TAG 테이블의 `SUMMARIZED` 컬럼과 데이터 파티션 인덱스는 UPDATE 대상 row에 맞게 갱신됩니다.
다만 대량 UPDATE는 내부 정리 비용이 커질 수 있으므로 대상 범위를 태그와 시간 조건으로
좁게 지정합니다.

### 롤업

`WITH ROLLUP` 또는 롤업 테이블을 사용하는 환경에서는 이미 계산된 롤업 row가 원본 UPDATE를
즉시 반영하지 않을 수 있습니다. 정정 구간의 롤업 조회가 필요하면 `ROLLUP_REBUILD`로
해당 롤업을 재구성합니다.

```sql
EXEC ROLLUP_REBUILD(sensor_tag, 'TEMP-01',
    TO_DATE('2026-07-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'),
    TO_DATE('2026-07-02 00:00:00', 'YYYY-MM-DD HH24:MI:SS'));
```

## 검증 절차

1. UPDATE 전 같은 WHERE 조건으로 대상 row 수와 값 범위를 확인합니다.
2. UPDATE를 실행합니다.
3. 원본 TAG 테이블에서 변경 값을 확인합니다.
4. 롤업 조회가 필요한 경우 `ROLLUP_REBUILD`를 실행한 뒤 집계 값을 확인합니다.

```sql
SELECT COUNT(*), MIN(value), MAX(value)
  FROM sensor_tag
 WHERE name = 'TEMP-01'
   AND time >= TO_DATE('2026-07-01', 'YYYY-MM-DD')
   AND time <  TO_DATE('2026-07-02', 'YYYY-MM-DD');
```
