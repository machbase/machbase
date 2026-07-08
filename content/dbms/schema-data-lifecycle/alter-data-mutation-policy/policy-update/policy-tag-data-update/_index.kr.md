---
type: docs
title: 'TAG data UPDATE 정책'
weight: 10
---

TAG 테이블의 실제 시계열 데이터는 제한된 조건에서 UPDATE할 수 있습니다. UPDATE 대상은
명확한 태그 범위와 시간 범위로 한정해야 하며, 메타데이터 수정과는 구문을 구분합니다.

## 기본 정책

TAG data UPDATE는 다음 원칙을 따릅니다.

1. WHERE 절에 태그 선택 조건(`name =`, `name IN`, `name LIKE`)이 있어야 합니다.
2. WHERE 절에 BASETIME 컬럼 조건이 있어야 합니다.
3. SET 대상은 실제 데이터 컬럼이어야 합니다.
4. `name`(PRIMARY KEY), `time`(BASETIME), 메타데이터 컬럼은 data UPDATE로 수정할 수 없습니다.

```sql
UPDATE tag
   SET value = 25.0
 WHERE name = 'TEMP-01'
   AND time = TO_DATE('2024-01-01 12:00:00', 'YYYY-MM-DD HH24:MI:SS');
```

## 메타데이터와의 구분

TAG 메타데이터 컬럼은 `UPDATE ... METADATA` 구문으로 수정합니다.

```sql
UPDATE tag METADATA
   SET location = 'zone-2'
 WHERE name = 'TEMP-01';
```

메타데이터 변경은 태그 속성을 수정하는 작업이며, 이미 적재된 시계열 row의 `value`나
보조 데이터 컬럼을 변경하지 않습니다.

## 지원되는 조건

```sql
UPDATE tag
   SET value = value * 0.98
 WHERE name IN ('TEMP-01', 'TEMP-02')
   AND time BETWEEN TO_DATE('2024-01-15 10:00:00', 'YYYY-MM-DD HH24:MI:SS')
                AND TO_DATE('2024-01-15 11:00:00', 'YYYY-MM-DD HH24:MI:SS')
   AND value > 0;
```

`OR`, 태그 선택 없는 조건, 시간 조건 없는 조건, 서브쿼리 기반 조건은 허용하지 않습니다.

## 운영 고려사항

- 대량 UPDATE 전 같은 WHERE 조건으로 대상 row 수를 확인합니다.
- UPDATE 직후 원본 row는 변경되지만, 이미 만들어진 롤업은 즉시 갱신되지 않을 수 있습니다.
  필요한 롤업은 `ROLLUP_REBUILD`로 재구성합니다.
- 수집 직후 데이터를 수정해야 한다면 먼저 SELECT로 대상 row가 조회되는지 확인합니다.
