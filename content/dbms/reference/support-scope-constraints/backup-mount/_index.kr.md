---
type: docs
title: '18.6.8 백업/마운트 지원표'
weight: 80
toc: true
---

백업은 데이터를 파일로 저장하고, 마운트는 저장된 백업 파일을 데이터베이스에 연결하여 조회하는 기능입니다.

## Edition별 지원 여부

| 기능 | Standard | Cluster | 비고 |
|------|:--------:|:-------:|------|
| 논리 다중 데이터베이스 | O | X | Standard Edition 전용 |
| BACKUP DATABASE | O | O | 전체 데이터베이스 백업 |
| BACKUP TABLE | O | O | 특정 테이블만 백업 |
| MOUNT DATABASE | O | X | Cluster Edition 미지원 |
| UMOUNT DATABASE | O | X | Cluster Edition 미지원 |
| machadmin -r 복구 | O | X | Cluster Edition 미지원 |

`BACKUP DATABASE database_name INTO DISK`는 하나의 active logical database를 백업합니다.
여러 active database가 포함된 full-instance image는 logical `MOUNT`/`RESTORE DATABASE`의
입력으로 사용할 수 없습니다. mounted database 조회에는 `USAGE`와 table `SELECT`가
필요하며 `USE`와 쓰기는 지원하지 않습니다.

## 테이블 타입별 백업 지원

| 테이블 유형 | BACKUP 지원 | MOUNT 후 조회 | 비고 |
|------------|:-----------:|:------------:|------|
| TAG 테이블 | O | O | |
| LOG 테이블 | O | O | |
| LOOKUP 테이블 | O | O | |
| TRANSACTION 테이블 | O | O | |
| VOLATILE 테이블 | X | X | 메모리 기반으로 백업 불가 |

## BACKUP 문법

```sql
-- 전체 데이터베이스 백업
BACKUP DATABASE INTO DISK = '/data/backup/machbase_backup';

-- 특정 테이블 백업
BACKUP TABLE sensor_data INTO DISK = '/data/backup/sensor_backup';
```

## MOUNT / UMOUNT 문법

```sql
-- 백업 파일 마운트 (읽기 전용 조회 가능)
MOUNT DATABASE '/data/backup/machbase_backup' TO MOUNTDB;

-- 마운트된 DB의 데이터 조회
SELECT * FROM MOUNTDB.SYS.sensor_data LIMIT 10;

-- 마운트 해제
UMOUNT DATABASE MOUNTDB;
```

## machadmin을 통한 복구

Standard Edition에서는 `machadmin` 명령으로 전체 복구를 수행할 수 있습니다.

```bash
# 백업에서 복구
machadmin -r /data/backup/machbase_backup
```

## 운영 권장 사항

- 정기 백업은 `BACKUP DATABASE`를 사용하고 외부 스토리지에 보관하십시오.
- MOUNT는 이전 데이터 조회 또는 마이그레이션 목적으로 활용할 수 있습니다.
- VOLATILE 테이블 데이터는 백업되지 않으므로, 중요 데이터는 다른 테이블 유형을 사용하십시오.
- Cluster Edition의 복구 절차는 Cluster Edition 운영 가이드를 참고하십시오.

## 상세 레퍼런스

[백업/복구/마운트](/dbms/operations-configuration-recovery/backup-restore-mount/) 섹션을 참고하십시오.
