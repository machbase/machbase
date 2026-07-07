---
type: docs
title: 'FLUSH AGER'
weight: 60
---

```sql
ALTER SYSTEM FLUSH AGER;
```

Ager 백그라운드 스레드를 즉시 실행하여 만료된 데이터와 삭제 마크된 파티션을 정리합니다.

## Ager란

Ager는 Machbase의 백그라운드 스레드로, 다음 작업을 주기적으로 수행합니다.

- `DELETE` 또는 보존 정책으로 삭제 마크된 파티션 제거
- 만료 기간이 지난 데이터 파티션 물리적 삭제
- 삭제된 데이터가 차지하던 디스크 공간 해제

Ager는 자동으로 실행되지만, `ALTER SYSTEM FLUSH AGER`를 사용하면 예약된 실행 주기를 기다리지 않고 즉시 정리 작업을 실행합니다.

## 사용 시점

| 상황 | 설명 |
|---|---|
| 대량 DELETE 후 즉시 공간 회수 | DELETE 후 디스크가 즉시 해제되지 않을 때 수동으로 Ager 실행 |
| 보존 기간 정책 적용 후 즉시 반영 | 오래된 데이터 파티션을 즉시 제거하고 싶을 때 |
| 디스크 부족 상황에서 긴급 공간 확보 | 여유 공간이 부족할 때 우선 정리 작업 실행 |

## 사용 예시

```sql
-- 대량 삭제 후 Ager 즉시 실행
DELETE FROM log_table BEFORE TO_DATE('2025-01-01', 'YYYY-MM-DD');
ALTER SYSTEM FLUSH AGER;

-- 디스크 사용량 변화 확인
ALTER SYSTEM CHECK DISK_USAGE;
SELECT * FROM v$storage;
```

> **참고**: Ager 실행은 비동기적으로 시작됩니다. 명령이 반환된 직후 모든 정리가 완료된 것은 아니며, 파티션 수와 크기에 따라 시간이 걸릴 수 있습니다.
