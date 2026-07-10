---
title: '8.7 운영과 데이터 생명주기'
weight: 70
toc: true
---

RDB 테이블의 운영 절차와 데이터 관리 방법을 다룹니다. RDB 테이블은 영속 데이터를 저장하므로 트랜잭션, 잠금, 백업, 복구 절차를 함께 설계해야 합니다.

<a id="operations-rdb-lifecycle"></a>

## 데이터 생명주기

RDB 테이블의 데이터는 생성, 입력, 갱신, 삭제, 백업, 복구의 흐름으로 관리합니다.

```
테이블 생성
  └── INSERT / INSERT SELECT
        └── SELECT / JOIN / 집계
              └── UPDATE / DELETE
                    └── 백업 / 복구 / 마운트
```

원본 수집 데이터는 TAG 또는 LOG 테이블에 저장하고, RDB 테이블에는 업무 상태, 기준 정보, 집계 결과처럼 수정 가능한 데이터를 저장하는 구성이 일반적입니다.

<a id="operations-rdb-transaction"></a>

## 트랜잭션 운영

여러 DML을 하나의 작업 단위로 처리해야 하면 `BEGIN`, `COMMIT`, `ROLLBACK`을 사용합니다.

```sql
BEGIN;
UPDATE inventory SET qty = qty - 3 WHERE item_id = 42;
INSERT INTO dispatch_log VALUES (NOW, 42, 'WH-01', 3, 'ORDER-9999');
DELETE FROM reservations WHERE item_id = 42 AND order_id = 'ORDER-9999';
COMMIT;
```

오류가 발생하면 `ROLLBACK`으로 변경을 취소합니다.

```sql
BEGIN;
UPDATE inventory SET qty = qty - 10 WHERE item_id = 42;
ROLLBACK;
```

장시간 열린 트랜잭션은 잠금 충돌을 유발할 수 있으므로, 배치 작업은 적절한 단위로 나누어 실행합니다.

<a id="operations-rdb-cleanup"></a>

## 데이터 정리

RDB 테이블의 정리는 업무 조건에 맞는 `DELETE` 문으로 수행합니다.

```sql
SELECT COUNT(*)
FROM order_history
WHERE status = 'CANCELLED'
  AND order_time < '2026-01-01 00:00:00';

DELETE FROM order_history
WHERE status = 'CANCELLED'
  AND order_time < '2026-01-01 00:00:00';
```

대량 삭제 전에는 같은 조건으로 대상 건수를 확인하고, 필요하면 배치 단위로 나누어 실행합니다. 보존 정책이 필요한 원본 시계열 데이터는 TAG 또는 LOG 테이블의 보존 정책과 함께 설계합니다.

<a id="operations-rdb-backup-recovery"></a>

## 백업과 복구

RDB 테이블은 데이터베이스 백업 대상에 포함됩니다. RDB 테이블은 내부적으로 sidecar 파일을 사용하므로 백업·복구 절차에서 해당 파일이 함께 처리되는지 확인합니다.

```sql
BACKUP DATABASE INTO DISK = '/backup/machbase_backup_20260101';
```

마운트된 백업 데이터베이스에서도 RDB 테이블을 읽기 전용으로 조회할 수 있습니다.

```sql
MOUNT DATABASE '/backup/machbase_backup_20260101' TO backup_db;

SELECT *
FROM backup_db.order_history
WHERE order_time >= '2026-01-01 00:00:00';

UMOUNT DATABASE backup_db;
```

RDB sidecar 파일의 누락 또는 손상에 대한 대응은 [RDB 백업, 마운트, sidecar](/dbms/rdb-table-usage/backup-mount-sidecar/)에서 다룹니다.

<a id="operations-rdb-checklist"></a>

## 운영 체크리스트

- PRIMARY KEY와 주요 WHERE 조건 컬럼에 인덱스가 있는지 확인합니다.
- 장시간 트랜잭션을 피하고, 배치 작업은 적절한 단위로 나눕니다.
- DDL 작업은 DML이 많은 시간대를 피해서 수행합니다.
- 정기 백업에 RDB 테이블과 sidecar 파일이 포함되는지 확인합니다.
- 복구 절차를 운영 환경과 동일한 버전에서 주기적으로 점검합니다.
