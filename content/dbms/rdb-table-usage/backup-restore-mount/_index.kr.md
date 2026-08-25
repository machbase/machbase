---
title: '8.13 TRANSACTION 백업, 복원, 마운트'
weight: 130
toc: true
---

TRANSACTION 테이블은 Standard Edition의 영속 테이블이며 데이터베이스 백업, 복원과
마운트 범위에 포함됩니다. 이 페이지는 TRANSACTION에만 해당하는 범위를 설명합니다.
공통 문법은 [BACKUP / RESTORE / MOUNT syntax](/dbms/reference/sql/syntax-dictionary-sql/backup-restore-mount-syntax/)를,
운영 절차는 [백업, 복원, 마운트](/dbms/operations-configuration-recovery/backup-restore-mount/)를
정본으로 사용하십시오.

<a id="support-scope-backup-rdb"></a>

## 지원 범위

| 작업 | 지원 | TRANSACTION 관련 설명 |
|------|:----:|-----------------------|
| `BACKUP DATABASE` | O | 다른 영속 테이블과 함께 포함 |
| `BACKUP TABLE` | O | 지정한 TRANSACTION 테이블 백업 |
| 증분 백업 | O | 기준 백업 이후 변경분 포함 |
| 오프라인 복원 | O | `machadmin -r`로 다른 영속 테이블과 함께 복원 |
| `MOUNT DATABASE` | O | 백업 시점의 테이블을 읽기 전용으로 조회 |

TRANSACTION은 Cluster Edition에서 지원하지 않습니다. 다른 Edition에서 생성한
TRANSACTION 객체가 포함된 백업을 Cluster에 복원하는 경로로 사용하지 마십시오.

<a id="backup-rdb"></a>


## TRANSACTION 검증 항목

백업 또는 복구 뒤 table 목록·owner, 주요 행 수와 업무 key, PRIMARY KEY·UNIQUE INDEX, 애플리케이션 권한과 명시적 transaction 흐름을 확인합니다. mounted database는 읽기 전용이며 세 부분 이름으로 조회합니다.

공통 명령과 안전 절차는 [백업, 복원, 마운트](../../operations-configuration-recovery/backup-restore-mount/)를 정본으로 사용하십시오.
