---
type: docs
title: '14.9 백업, 복원, 마운트'
weight: 100
toc: true
---

백업은 생성 성공뿐 아니라 격리 환경의 mount·restore와 표본 query까지 검증해야 합니다.
경로, 권한, 저장 공간, 보존 기간, 암호화·접근 통제를 함께 운영합니다. 전체 SQL과 option은
[백업·복원·마운트 구문](/dbms/reference/sql/syntax-dictionary-sql/backup-restore-mount-syntax/)을
정본으로 사용합니다.

<a id="backup"></a>

## 백업 선택

| 목적 | 방식 |
|------|------|
| instance의 전체 복구 기준점 | database 전체 backup |
| 특정 table 이동·보존 | table backup |
| 이전 backup 이후 변경분 | incremental backup |
| 특정 시간 범위 archive | period backup |
| 운영 중 backup 조회 | read-only mount |
| instance data 교체 | offline restore |

backup 종류를 선택하기 전에 edition, table type, incremental chain, mount·restore 지원
범위를 현재 release에서 확인합니다.

<a id="backup-full"></a>

## 전체 백업

전체 backup은 독립 복구 기준점으로 보존합니다.

- backup 경로는 server process가 접근합니다.
- 대상 filesystem의 free space와 quota를 확인합니다.
- 실행 시작·종료·오류와 결과 크기를 기록합니다.
- backup과 원본 data를 같은 장애 영역에만 두지 않습니다.
- 정기적으로 격리 server에 restore해 주요 table을 검증합니다.

<a id="backup-table"></a>

## Table 백업

table backup은 지원되는 table type과 index·metadata 포함 범위를 확인합니다. table 한 개를
복구할 때는 새 database 또는 mount에서 검증한 뒤 명시적인 INSERT·export/import 경로로
옮기는 방식을 우선합니다. 존재하는 운영 table을 즉시 교체하지 않습니다.

<a id="backup-incremental-after"></a>

## Incremental backup과 AFTER

incremental backup은 기준 backup과 이후 chain이 모두 필요할 수 있습니다.

- 각 backup의 parent와 생성 순서를 기록합니다.
- 중간 파일 하나가 없을 때 복구 가능한지 점검합니다.
- 마지막 incremental만 따로 보관하지 않습니다.
- chain이 길어지면 새 전체 backup 기준점을 만듭니다.
- restore 훈련은 최종 시점까지 실제 chain을 적용합니다.

<a id="backup-period"></a>

## 기간 백업

기간 backup은 시간 조건의 경계와 timezone을 명시합니다. `BETWEEN`의 양끝 포함 여부를
가정하지 말고 시작 포함·끝 제외 범위를 우선 사용합니다. archive의 최소·최대 시각과 row
수를 원본과 비교합니다.

<a id="sql-backup"></a>

## SQL BACKUP

BACKUP 실행 계정에는 필요한 database·table 권한과 server 경로 접근이 필요합니다. 운영
자동화에서는 비밀번호를 command line에 고정하지 않고, exit code와 operation 상태를 함께
확인합니다.

실행 전후 점검:

1. 대상 database·table과 backup 종류 확인
2. 경로가 비어 있거나 정책상 덮어써도 되는지 확인
3. free space와 예상 증가량 확인
4. backup operation 완료·오류 확인
5. 결과 목록·크기·checksum 또는 storage 검증
6. mount·restore 표본 검증

<a id="offline-restore-machadmin-r"></a>

## Offline restore

offline restore는 현재 instance data를 교체할 수 있는 파괴적 작업입니다. 이 매뉴얼의
일반 예제로 server 중지·database 삭제·`machadmin -r`을 연속 실행하지 않습니다.

- service와 모든 client·Collector를 중지할 계획을 세웁니다.
- 현재 data의 별도 backup과 rollback 경로를 확보합니다.
- restore할 정확한 backup과 chain을 검증합니다.
- 동일 release·edition·설정 호환성을 확인합니다.
- 복구 담당자 두 명이 대상 instance와 경로를 교차 확인합니다.
- 격리 복구 훈련을 통과한 runbook만 운영에 적용합니다.
- restore 뒤 schema, row 수, 시간 범위, application query를 검증합니다.

<a id="database-mount"></a>

## Database mount

mount는 backup을 읽기 전용 database로 연결해 조사·선별 복구할 때 사용합니다.

```text
MOUNT DATABASE mount_name FROM '/absolute/backup/path';
UMOUNT DATABASE mount_name;
```

운영 active database와 겹치지 않는 mount 이름을 사용합니다. mount 경로와 권한은 server
process 기준입니다.

<a id="query-database-mount"></a>

## Mounted database 조회

```text
SELECT *
FROM mount_name.SYS.table_name
WHERE _ARRIVAL_TIME >= TO_DATE('2026-01-01', 'YYYY-MM-DD');
```

먼저 table 목록과 schema를 확인하고, 시간 범위·row 수·표본값을 검증합니다. 필요한 data는
현재 schema와 중복 정책을 확인한 뒤 선별 이동합니다.

<a id="mounted-db-read-only-refcount-active-same-name"></a>

## Read-only와 사용 중 mount

mounted database에는 DDL·DML을 실행하지 않습니다. 열린 cursor나 statement가 있으면
unmount가 거부될 수 있으므로 모든 참조를 닫고 재시도합니다. active database나 다른 mount와
이름이 충돌하지 않는지 먼저 확인합니다.

<a id="unsupported-support-scope-mount-table-umount"></a>

## 지원하지 않는 경로

일부 내부 문법이 성공처럼 보이더라도 공개 운영 API가 아닌 `MOUNT TABLE`·`UMOUNT TABLE`에
의존하지 않습니다. 공개 `MOUNT DATABASE`와 `UMOUNT DATABASE`를 사용합니다.

<a id="table-types-type-backup-mount"></a>

## Table type과 edition 범위

LOG, TAG, TRANSACTION, LOOKUP, VOLATILE의 backup·mount 동작은 동일하지 않습니다.
VOLATILE은 server restart에 유지되지 않는 memory table입니다. table·edition별 범위는
[backup·mount 지원 범위](/dbms/reference/support-scope-constraints/backup-mount/)를
확인합니다.

## 복구 검증표

- database·owner·table 수
- 주요 table schema와 index
- row 수와 최소·최대 시간
- NULL·문자열·숫자 표본
- 사용자·권한과 application connection
- ROLLUP·retention·job 상태
- backup 시점 이후 data의 처리
- rollback 가능 여부와 실제 소요 시간
