---
type: docs
title: 'TAG data UPDATE 대상 범위와 대량 정정 성능 고려사항'
weight: 40
---

TAG 테이블은 고속 시계열 데이터 수집에 최적화된 구조로, 현재 버전에서는 UPDATE 문을 직접 지원하지 않습니다. 데이터 정정이 필요한 경우 DELETE와 INSERT를 조합하는 패턴을 사용합니다.

## 현재 제약사항

TAG 테이블에 UPDATE를 시도하면 오류가 발생합니다.

```sql
-- 오류: TAG 테이블은 UPDATE 미지원
UPDATE sensor_tag SET value = 99.5 WHERE name = 'TEMP-01' AND time = '2025-06-01 12:00:00';
-- [ERR-02278: UPDATE statement is not allowed for SENSOR_TAG.]
```

이 제약은 TAG 테이블의 LSM 기반 불변 저장 구조에서 비롯됩니다. 한번 기록된 레코드는 덮어쓰지 않고, 정정 시 삭제 후 재삽입 방식을 사용합니다.

## 기본 정정 패턴: DELETE → INSERT

소량의 데이터를 정정할 때는 대상 레코드를 먼저 삭제하고 수정된 값으로 재삽입합니다.

```sql
-- 1단계: 오류 데이터 삭제
DELETE FROM sensor_tag
WHERE  name = 'TEMP-01'
  AND  time = '2025-06-01 12:00:00';

-- 2단계: 정정된 값으로 재삽입
INSERT INTO sensor_tag VALUES ('TEMP-01', '2025-06-01 12:00:00', 99.5);
```

TAG 테이블의 DELETE는 `name`과 `time` 컬럼을 기준으로 대상 레코드를 식별합니다.

## 대량 정정 시 DELETE BEFORE → 재삽입 패턴

수천~수만 건의 오류 데이터를 정정할 때는 트랜잭션 범위와 순서를 고려한 패턴을 사용합니다.

### 시간 범위 기반 대량 삭제

특정 시간 범위의 데이터 전체가 오류인 경우:

```sql
-- 오류 시간 범위의 데이터 전체 삭제
DELETE FROM sensor_tag
WHERE  name = 'TEMP-01'
  AND  time BETWEEN '2025-06-01 10:00:00' AND '2025-06-01 11:00:00';

-- 삭제 완료 확인
SELECT COUNT(*) FROM sensor_tag
WHERE  name = 'TEMP-01'
  AND  time BETWEEN '2025-06-01 10:00:00' AND '2025-06-01 11:00:00';
-- 결과: 0

-- 정정 데이터 재삽입 (machloader 또는 Append API 사용 권장)
-- machloader -i -t sensor_tag -d corrected_data.csv
```

### 대량 정정 성능 고려사항

| 항목 | 권장 사항 |
|------|-----------|
| 삭제 범위 | 태그 이름과 시간 범위를 모두 명시해 스캔 범위 최소화 |
| 재삽입 방법 | machloader 또는 Append API 사용 (INSERT 반복보다 빠름) |
| ROLLUP 처리 | 재삽입 완료 후 `ALTER ROLLUP ... FORCE`로 집계 재수행 |
| 순서 | 반드시 DELETE 완료 후 INSERT 수행 (중복 방지) |

```sql
-- 대량 정정 후 ROLLUP 재집계
ALTER ROLLUP _tag_ru_1s FORCE;
ALTER ROLLUP _tag_ru_1m FORCE;
ALTER ROLLUP _tag_ru_1h FORCE;
```

> **주의**: ROLLUP은 INSERT 시점부터 새 데이터를 인식합니다. 기존 범위를 삭제하고 재삽입하면 ROLLUP 값도 갱신되지만, FORCE를 실행하지 않으면 다음 wakeup 주기까지 집계가 지연됩니다.

## 임시 대안: STREAM을 이용한 정정 데이터 파이프라인

실시간으로 정정 데이터가 발생하는 환경에서는 STREAM을 활용해 정정 데이터를 원본 테이블에 반영하는 파이프라인을 구성할 수 있습니다.

```sql
-- 정정 데이터를 임시 LOG 테이블로 수신
CREATE TABLE correction_staging (
    tag_name   VARCHAR(64),
    tag_time   DATETIME,
    new_value  DOUBLE
);

-- STREAM: 스테이징 테이블에서 읽어 TAG 테이블을 DELETE + INSERT로 갱신
-- (애플리케이션 레벨에서 처리하거나 외부 ETL 도구 사용)
```

**파이프라인 흐름:**

```
정정 소스 데이터
    → correction_staging (LOG 테이블) 적재
        → 애플리케이션: 스테이징에서 읽어 sensor_tag DELETE + INSERT 수행
            → ROLLUP FORCE 실행
```

이 패턴은 정정 작업을 비동기로 처리해 운영 중인 데이터 수집 파이프라인에 영향을 최소화합니다.

## 정정 작업 체크리스트

- [ ] 정정 대상 태그명과 시간 범위를 사전에 정확히 파악
- [ ] DELETE 전 대상 레코드 수를 `SELECT COUNT(*)`로 확인
- [ ] 삭제 완료 후 `SELECT COUNT(*) = 0` 검증
- [ ] 정정 데이터를 machloader 또는 Append API로 재삽입
- [ ] 재삽입 후 `ALTER ROLLUP ... FORCE`로 집계 재수행
- [ ] 정정 완료 후 대시보드/보고서 결과 검증
