---
type: docs
title: 'Retention Policy의 역할'
weight: 30
---

시계열 데이터는 수집을 멈추지 않는 한 데이터베이스에 계속 쌓입니다. 모든 데이터를 영구 보관할 수 없다면, 일정 기간이 지난 데이터를 자동으로 제거하는 정책이 필요합니다. Retention Policy는 이 요구를 충족하는 Machbase의 자동 데이터 수명 관리 기능입니다.

## Retention Policy란

Retention Policy는 테이블에 설정한 보관 기간보다 오래된 데이터를 배경 스레드가 자동으로 삭제하는 정책입니다. 운영자가 주기적으로 직접 DELETE를 실행하지 않아도, 설정된 기간이 지나면 데이터가 자동으로 제거됩니다.

Retention Policy는 LOG 테이블과 TAG 테이블에 적용할 수 있습니다. LOOKUP, VOLATILE, RDB 테이블의
수명 관리는 Retention Policy가 아니라 DELETE 또는 TRUNCATE 같은 명시적 DML로 처리합니다.

## 적용 방법

Retention Policy를 생성하고 테이블에 연결하는 방법은 두 단계로 이루어집니다.

```sql
-- 1. Retention Policy 생성 (30일 보관)
CREATE RETENTION keep_30days DURATION 30 DAY INTERVAL 1 DAY;

-- 2. 테이블에 적용
ALTER TABLE device_log ADD RETENTION keep_30days;
```

이후 `device_log` 테이블에서 30일이 지난 데이터는 배경에서 자동으로 삭제됩니다. 정책을 해제하려면 다음을 실행합니다.

```sql
ALTER TABLE device_log DROP RETENTION;
```

## DELETE, TRUNCATE와의 차이

세 가지 방법 모두 데이터를 삭제하지만, 적용 방식과 목적이 다릅니다.

| 항목 | Retention Policy | DELETE | TRUNCATE |
| --- | --- | --- | --- |
| 실행 방식 | 자동 (배경 스레드) | 수동 (SQL 실행) | 수동 (SQL 실행) |
| 삭제 범위 | 기간 기준 자동 판단 | 테이블 타입별 DELETE 조건 기반 | 테이블 전체 |
| 지속성 | 지속적 (한 번 설정 후 자동) | 일회성 | 일회성 |
| 운영 중 실행 | 가능 (무중단) | 가능 (시간 범위 제약) | 가능 |
| 주요 목적 | 장기 보관 정책 자동화 | 특정 구간 이상 데이터 즉시 제거 | LOG/RDB 테이블 초기화 |

**언제 어떤 방법을 선택하는가**

- 30일, 90일 등 고정된 기간 후 자동 삭제가 필요하면 **Retention Policy** 를 사용합니다.
- 특정 이벤트나 배포 전후 특정 시간 구간의 데이터를 선택적으로 제거하려면 **DELETE** 를 사용합니다.
- LOG 테이블이나 RDB 테이블을 지원하는 버전에서 테이블 내용 전체를 즉시 비워야 하면 **TRUNCATE** 를 사용합니다.

## 다음 읽을 내용

- [Backup / Restore / Mount 개념](../concepts-backup-restore-mount/) — 데이터 보호와 복원 수단
- [Retention vs DELETE / TRUNCATE](/dbms/core-concepts/terminology-distinction/retention-vs-delete-truncate/) — 세 가지 삭제 방법의 상세 비교
