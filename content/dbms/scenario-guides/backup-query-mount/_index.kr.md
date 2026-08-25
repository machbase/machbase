---
type: docs
title: '16.5 백업 데이터 조회'
weight: 50
toc: true
---

백업 이미지를 mounted database로 연결하면 현재 database를 덮어쓰지 않고 과거 데이터를
읽을 수 있습니다. 이 작업은 파일 시스템과 database 전역 상태에 영향을 주므로 격리 환경에서
고유한 경로와 MOUNT 이름으로 검증하십시오.

## 1단계: 검증 데이터와 백업 생성

```sql
CREATE TRANSACTION TABLE sc16_backup_source (
    id    INTEGER,
    value VARCHAR(40)
);
INSERT INTO sc16_backup_source VALUES (1, 'before backup');

BACKUP DATABASE INTO DISK = '/backup/sc16_snapshot';
```

경로가 이미 존재하는지, Machbase 서버 프로세스의 OS 계정이 상위 디렉터리에 쓸 수 있는지,
여유 공간이 충분한지 먼저 확인합니다. 운영 database의 백업 정책을 시험 경로로 덮어쓰지
마십시오.

## 2단계: MOUNT와 조회

```sql
MOUNT DATABASE '/backup/sc16_snapshot' TO sc16_mount;

SELECT id, value
  FROM sc16_mount.sys.sc16_backup_source
 ORDER BY id;
```

mounted database는 읽기 전용 분석에 사용합니다. 현재 database의 값과 비교할 때는 어느 쪽
database의 객체인지 알 수 있도록 세 부분 이름을 명시합니다.

```sql
SELECT 'CURRENT' AS source_name, COUNT(*) AS row_count
  FROM sc16_backup_source
UNION ALL
SELECT 'BACKUP' AS source_name, COUNT(*) AS row_count
  FROM sc16_mount.sys.sc16_backup_source;
```

## 3단계: UMOUNT와 정리

```sql
UMOUNT DATABASE sc16_mount;
DROP TABLE sc16_backup_source;
```

UMOUNT 전에 mounted database를 사용하는 세션과 쿼리가 없는지 확인합니다. MOUNT 조회 성공은
백업 검증의 한 단계일 뿐입니다. 복구 가능성을 보장하려면 별도 환경의 restore 시험과 업무
검증 쿼리까지 수행하십시오.

전체 구문과 안전 제한은
[백업, 복구, 마운트](/dbms/operations-configuration-recovery/backup-restore-mount/)를 참고합니다.
