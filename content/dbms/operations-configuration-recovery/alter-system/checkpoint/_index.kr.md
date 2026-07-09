---
type: docs
title: '13.3.1 CHECKPOINT'
weight: 10
---

```sql
ALTER SYSTEM CHECKPOINT;
```

메모리 버퍼에 있는 변경 데이터를 즉시 디스크에 기록합니다.

## 동작 설명

Machbase는 성능을 위해 쓰기 작업을 메모리 버퍼에 먼저 기록하고 주기적으로 디스크에 동기화합니다. 이 주기적인 동기화를 체크포인트(Checkpoint)라고 합니다. 체크포인트 주기는 `DISK_COLUMNAR_TABLE_CHECKPOINT_INTERVAL_SEC`와 `DISK_COLUMNAR_INDEX_CHECKPOINT_INTERVAL_SEC` 파라미터로 제어됩니다.

`ALTER SYSTEM CHECKPOINT`를 실행하면 예약된 주기를 기다리지 않고 즉시 체크포인트를 수행합니다. 체크포인트가 완료되면 명령이 반환됩니다.

체크포인트 관련 파라미터는 [스토리지 및 체크포인트 설정](../../configuration/storage-checkpoint-configuration/)을 참고하십시오.

## 사용 시점

| 상황 | 설명 |
|---|---|
| 백업 전 | 백업 대상 데이터를 디스크에 완전히 내려쓴 후 백업 실행 |
| 계획된 서버 종료 전 | 종료 시 자동 체크포인트가 수행되지만, 미리 실행해 종료 시간을 단축 |
| 장시간 운영 후 데이터 안전성 확인 | 메모리 버퍼가 누적된 상황에서 수동으로 동기화 |

## 사용 예시

```sql
-- 백업 전 체크포인트 수행
ALTER SYSTEM CHECKPOINT;

-- 체크포인트 완료 후 백업 실행
BACKUP DATABASE INTO DISK = '/backup/machbase_20260707';
```

> **참고**: 서버 재시작 없이 즉시 실행됩니다. 체크포인트가 진행되는 동안 INSERT 성능이 일시적으로 저하될 수 있습니다.
