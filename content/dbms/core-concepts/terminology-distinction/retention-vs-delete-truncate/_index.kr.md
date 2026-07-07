---
type: docs
title: 'Retention vs DELETE / TRUNCATE'
weight: 20
---

Machbase에서 데이터를 삭제하는 방법은 세 가지입니다. 각각 목적과 동작 방식이 다르므로, 상황에 맞는 방법을 선택하는 것이 중요합니다.

## 비교 표

| 항목 | Retention Policy | DELETE | TRUNCATE |
| --- | --- | --- | --- |
| 실행 방식 | 자동 (배경 스레드) | 수동 (SQL 실행 시) | 수동 (SQL 실행 시) |
| 삭제 범위 | 보관 기간 초과 데이터 자동 판단 | 테이블 타입별 DELETE 조건 기반 | 테이블 전체 데이터 |
| 지속성 | 지속적 (설정 후 계속 자동 실행) | 일회성 | 일회성 |
| 대상 테이블 | LOG, TAG | LOG, TAG (시간 범위), LOOKUP, VOLATILE | 모든 테이블 |
| 운영 중 실행 | 가능 (무중단) | 가능 | 가능 |
| 설정 방법 | `CREATE RETENTION` + `ALTER TABLE` | `DELETE FROM ...` | `TRUNCATE TABLE` |

## Retention Policy: 자동 기간 기반 삭제

Retention Policy는 보관 기간을 정책으로 설정하면 이후 자동으로 기간이 지난 데이터를 삭제합니다. 운영 중에도 중단 없이 배경에서 실행됩니다.

```sql
-- 60일 보관 정책 생성 및 적용
CREATE RETENTION keep_60days DURATION 60 DAY INTERVAL 1 DAY;
ALTER TABLE device_log ADD RETENTION keep_60days;

-- 정책 해제
ALTER TABLE device_log DROP RETENTION;

-- 정책 삭제
DROP RETENTION keep_60days;
```

데이터가 계속 쌓이는 운영 시스템에서 저장 공간을 자동으로 관리하고 싶을 때 사용합니다.

## DELETE: 조건 기반 수동 삭제

DELETE는 SQL 문장을 직접 실행해 특정 조건에 맞는 데이터를 즉시 삭제합니다. LOG 테이블은 `BEFORE`, `OLDEST`, `EXCEPT` 같은 로그 보존형 DELETE를 사용하고, TAG 테이블은 태그 이름과 축 조건 또는 `BEFORE` 조건을 사용할 수 있습니다.

```sql
-- LOG 테이블에서 특정 시각 이전 삭제
DELETE FROM device_log BEFORE TO_DATE('2026-01-01', 'YYYY-MM-DD');

-- TAG 테이블에서 특정 태그의 특정 시간 범위 삭제
DELETE FROM sensor_values
WHERE name = 'temp_sensor_01'
  AND time >= TO_DATE('2026-01-01', 'YYYY-MM-DD')
  AND time <  TO_DATE('2026-02-01', 'YYYY-MM-DD');
```

잘못 입력된 데이터 구간을 제거하거나, 특정 이유로 오래된 데이터의 일부를 즉시 제거해야 할 때 사용합니다.

## TRUNCATE: 테이블 전체 즉시 삭제

TRUNCATE는 테이블의 모든 데이터를 즉시 삭제합니다. WHERE 조건이 없으므로 단 한 줄로 모든 데이터가 제거됩니다.

```sql
TRUNCATE TABLE device_log;
```

개발이나 테스트 환경에서 테이블을 초기 상태로 되돌리거나, 운영 데이터를 전량 폐기해야 할 때 사용합니다. 운영 테이블에서는 실수로 실행하지 않도록 주의해야 합니다.

## 선택 기준 요약

| 상황 | 권장 방법 |
| --- | --- |
| 장기 보관 정책 자동화 (30일, 90일 등) | Retention Policy |
| 특정 시간 구간 데이터 즉시 제거 | DELETE |
| 잘못 입력된 데이터 구간 재입력을 위한 삭제 | DELETE |
| 테이블 전체 초기화 (개발/테스트) | TRUNCATE |
| 테이블 전체 즉시 폐기 | TRUNCATE |

## 다음 읽을 내용

- [Retention Policy의 역할](/dbms/core-concepts/features-concepts/role-retention-policy/) — Retention Policy 상세 개념
- [Backup vs Restore vs Mount](../backup-vs-restore-mount/) — 데이터 보호 수단 비교
