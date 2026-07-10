---
type: docs
title: '13.8 스키마 변경 체크리스트'
weight: 50
---

운영 중 스키마 변경 전에 아래 항목을 순서대로 확인합니다.

## 변경 전 점검

### 1. 테이블 타입 확인

```sql
SELECT TABLE_NAME, TABLE_TYPE FROM M$SYS_TABLES WHERE TABLE_NAME = 'TARGET_TABLE';
```

테이블 타입별 ALTER TABLE 지원 범위가 다릅니다. [테이블 타입별 관리 가능 범위](/dbms/data-modeling-table-design/table-types-type-manageable/)를 미리 확인하십시오.

### 2. 현재 스키마 확인

```sql
-- 컬럼 정보 확인
DESC target_table;

-- 인덱스 확인
SELECT * FROM M$SYS_INDEXES WHERE TABLE_NAME = 'TARGET_TABLE';
```

### 3. 데이터 볼륨 확인

```sql
SELECT COUNT(*) FROM target_table;
```

대용량 테이블의 스키마 변경은 시간이 걸릴 수 있습니다. 업무 시간 외 실행을 권장합니다.

### 4. Retention Policy 적용 여부

```sql
SELECT * FROM V$RETENTION_JOB WHERE TABLE_NAME = 'TARGET_TABLE';
```

스키마 변경 전 Retention Policy가 실행 중이라면 완료 후 작업하세요.

---

## 컬럼 추가 체크리스트

- [ ] 추가할 컬럼의 데이터 타입이 해당 테이블 타입에서 지원되는가?
- [ ] LOG/RDB 테이블 컬럼 추가 시 기존 데이터의 새 컬럼 값은 NULL로 채워짐을 인지하고 있는가?
- [ ] 컬럼명 중복 여부 확인

```sql
ALTER TABLE sensor_log ADD COLUMN (new_col DOUBLE);
```

---

## 컬럼 삭제 체크리스트

- [ ] 삭제할 컬럼이 인덱스에 포함되어 있는가? (인덱스 먼저 삭제 필요)
- [ ] 애플리케이션에서 해당 컬럼을 참조하는 쿼리가 있는가?
- [ ] 컬럼 삭제 후 데이터는 복구 불가

```sql
ALTER TABLE sensor_log DROP COLUMN (old_col);
```

---

## 인덱스 변경 체크리스트

- [ ] 인덱스 생성/삭제는 쿼리 성능에 직접 영향
- [ ] 인덱스 생성 작업은 기존 데이터에 대한 인덱싱을 포함하므로, 대용량 테이블에서는 시간이 소요됨
- [ ] 사용하지 않는 인덱스는 INSERT 성능을 저하시키므로 삭제 고려

```sql
-- 인덱스 생성 (대용량 테이블은 야간 실행 권장)
CREATE INDEX idx_new ON sensor_log (sensor_id);

-- 불필요한 인덱스 삭제
DROP INDEX idx_old;
```

---

## Retention Policy 변경 체크리스트

- [ ] 정책 변경 필요 시: 기존 정책 해제 → 새 정책 생성/적용
- [ ] 보존 기간 단축 시: 즉시 삭제가 시작되므로 데이터 손실 가능성 검토

```sql
-- 기존 정책 해제
ALTER TABLE sensor_tag DROP RETENTION;

-- 새 정책 적용
ALTER TABLE sensor_tag ADD RETENTION new_policy;
```

---

## 변경 후 검증

```sql
-- 스키마 변경 확인
DESC target_table;

-- 데이터 정합성 확인
SELECT COUNT(*) FROM target_table;

-- 인덱스 상태 확인
SELECT * FROM M$SYS_INDEXES WHERE TABLE_NAME = 'TARGET_TABLE';
```

---

**다음으로 읽을 내용:**
- [데이터 보존 정책](/dbms/operations-configuration-recovery/policy-data-retention/)
- [운영 및 구성](/dbms/operations-configuration-recovery/)
