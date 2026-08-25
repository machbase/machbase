---
title: '7.7 운영과 데이터 생명주기'
weight: 70
toc: true
---
LOG 테이블은 오래된 영역부터 정리하는 보존형 삭제 구문과 Retention Policy를 사용합니다.
특정 업무 행을 임의로 수정·삭제해야 하는 데이터라면 TRANSACTION 또는 LOOKUP 테이블이 더
적합한지 검토하십시오.

<a id="original-85-deleting-data"></a>

## 삭제 방법 선택

<a id="delete-log-syntax"></a>

| 목적 | 방법 |
| --- | --- |
| 오래된 N개 행 삭제 | `OLDEST n ROWS` |
| 최근 N개 행을 남김 | `EXCEPT n ROWS` |
| 최근 기간을 남김 | `EXCEPT n DAY` 등 기간 단위 |
| 기준 시각까지 삭제 | `BEFORE datetime_expr` |
| 전체 데이터 삭제 | 조건 없는 `DELETE` 또는 지원되는 `TRUNCATE` |
| 지속적인 기간 보존 | Retention Policy |

<a id="delete-log-examples"></a>

## 실행 예제

```sql
CREATE LOG TABLE lifecycle_log (
    message VARCHAR(64)
);

INSERT INTO lifecycle_log(_arrival_time, message)
VALUES (TO_DATE('2026-01-01', 'YYYY-MM-DD'), 'first');
INSERT INTO lifecycle_log(_arrival_time, message)
VALUES (TO_DATE('2026-01-02', 'YYYY-MM-DD'), 'second');
INSERT INTO lifecycle_log(_arrival_time, message)
VALUES (TO_DATE('2026-01-03', 'YYYY-MM-DD'), 'third');

DELETE FROM lifecycle_log OLDEST 1 ROWS;
DELETE FROM lifecycle_log EXCEPT 1 ROWS;

SELECT _arrival_time, message FROM lifecycle_log;

DELETE FROM lifecycle_log;
DROP TABLE lifecycle_log;
```

운영 삭제 전에는 같은 시간 기준으로 대상 범위와 건수를 조회하고, `_arrival_time`과 실제
이벤트 시각을 혼동하지 마십시오.

<a id="retention-log-policy"></a>

## 보존 정책 설계

수동 삭제를 정기 작업으로 반복한다면 Retention Policy로 보관 기간과 실행 주기를
명시합니다. 원본 보관 기간, 백업 보존 기간과 집계 데이터의 수명은 각각 정하십시오.

- [데이터 보존 정책](/dbms/operations-configuration-recovery/policy-data-retention/)
- [LOG DELETE 문법](/dbms/reference/sql/syntax-dictionary-sql/dml-syntax/)

<a id="lifecycle-log-backup"></a>

## 백업 후 삭제

장기 보관이 필요한 데이터는 삭제 전에 백업하고, Mount 또는 격리된 Restore로 조회 가능성을
확인합니다. 이 페이지에서 환경 의존적인 백업 경로와 복원 명령을 반복하지 않고
[백업·복원·마운트](/dbms/operations-configuration-recovery/backup-restore-mount/)를
정본으로 사용합니다.

<a id="lifecycle-log-monitoring"></a>

## 운영 점검 항목

- 입력량, 디스크 사용량과 실제 보관 기간을 함께 확인합니다.
- 삭제 전 대상 건수와 시간 범위를 확인합니다.
- 백업이 필요한 데이터는 복구 가능성을 확인한 뒤 삭제합니다.
- 잘못 입력한 임의 행의 수정·삭제가 반복되면 테이블 모델을 재검토합니다.
