---
type: docs
title: '13.3.2 CHECK DISK_USAGE'
weight: 20
---

```sql
ALTER SYSTEM CHECK DISK_USAGE;
```

`v$storage`의 `DC_TABLE_FILE_SIZE` 값을 파일 시스템에서 직접 읽어 재계산합니다.

## 동작 설명

Machbase는 LOG 테이블의 디스크 사용량을 내부 메타데이터로 관리합니다. 정상적인 상황에서는 이 값이 자동으로 유지되지만, 프로세스 비정상 종료나 정전 등이 발생하면 메타데이터가 실제 파일 시스템 상태와 달라질 수 있습니다.

`CHECK DISK_USAGE`를 실행하면 Machbase가 실제 파일 시스템을 직접 스캔하여 사용량을 재계산하고 `v$storage`에 반영합니다.

> **주의**: 파일 시스템 스캔이 발생하므로 디스크 I/O 부담이 생깁니다. 일상적인 모니터링보다는 사용량 불일치가 의심될 때 사용하십시오.

## 사용 예시

```sql
-- 실행 전 현재 디스크 사용량 확인
SELECT * FROM v$storage;

-- 디스크 사용량 재계산
ALTER SYSTEM CHECK DISK_USAGE;

-- 재계산 후 결과 확인
SELECT * FROM v$storage;
```

## 사용 시점

- 서버 비정상 종료 후 재시작했을 때 디스크 사용량이 실제와 다르게 표시되는 경우
- 용량 모니터링 수치가 실제 파일 크기와 맞지 않는다고 판단될 때
- 디스크 공간 부족 경고가 발생했는데 실제로 여유가 충분한 경우
