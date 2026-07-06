---
type: docs
title: 'Backup vs Restore vs Mount'
weight: 30
---

Backup, Restore, Mount는 이름이 비슷하지만 목적과 사용 시점이 다릅니다. 간단히 구분하면 Backup은 "복사본 만들기", Restore는 "복사본으로 되돌리기", Mount는 "복사본을 읽기 전용으로 들여다보기"입니다.

## 비교 표

| 항목 | Backup | Restore | Mount |
| --- | --- | --- | --- |
| 목적 | 데이터 복사본 생성 | 복사본으로 데이터베이스 복원 | 복사본을 읽기 전용으로 연결 |
| 서버 상태 | 운영 중 실행 가능 | 서버 중지 필요 | 운영 중 실행 가능 |
| 실행 방법 | SQL (`BACKUP DATABASE`) | `machadmin -r` 명령 | SQL (`MOUNT DATABASE`) |
| 결과 | 별도 디렉터리에 복사본 저장 | 원래 데이터 위치에 복원 | 현재 서버에 read-only 마운트 |
| 데이터 쓰기 | 불가 (Backup 대상은 운영 DB) | 복원 후 운영 DB로 재사용 | 불가 (read-only) |
| 주요 사용 목적 | 정기 백업, 마이그레이션 준비 | 장애 복구 | 과거 시점 데이터 조회/검증 |

## Backup

운영 중인 서버에서 SQL로 실행합니다.

```sql
-- 전체 백업
BACKUP DATABASE INTO DISK = '/data/backup/full_20260703';

-- 특정 테이블만 백업
BACKUP TABLE sensor_values INTO DISK = '/data/backup/sensor_20260703';
```

Backup 작업은 `LAUNCHED` → `PROGRESS` → `FINISHED` (실패 시 `ERROR`) 순서로 진행됩니다. `V$BACKUP_JOB` 뷰에서 진행 상황을 확인할 수 있습니다.

## Restore

서버를 중지한 후 `machadmin` 명령으로 실행합니다. 복원이 완료되면 서버를 재시작합니다.

```bash
# 서버 중지
machadmin -s stop

# 백업본으로 복원
machadmin -r /data/backup/full_20260703

# 서버 재시작
machadmin -s start
```

Restore는 데이터 손상이나 장애 발생 후 마지막 백업 시점으로 데이터베이스를 되돌릴 때 사용합니다.

## Mount

운영 중인 서버에서 SQL로 실행합니다. 백업 디렉터리를 현재 서버에 read-only로 연결해 SELECT 쿼리를 실행할 수 있습니다.

```sql
-- 마운트
MOUNT DATABASE '/data/backup/full_20260703' TO BACKUP_VIEW;

-- 마운트된 데이터 조회
SELECT * FROM BACKUP_VIEW.sensor_values
WHERE time BETWEEN TO_DATE('2026-07-01', 'YYYY-MM-DD')
                AND TO_DATE('2026-07-02', 'YYYY-MM-DD');

-- 마운트 해제
UNMOUNT DATABASE BACKUP_VIEW;
```

Mount는 Restore와 달리 데이터를 원래 위치에 복원하지 않습니다. 백업 디렉터리를 그대로 참조하므로, 디스크 공간을 추가로 사용하지 않고 과거 시점의 데이터를 확인할 수 있습니다.

## 사용 시나리오별 선택 기준

| 시나리오 | 권장 수단 |
| --- | --- |
| 정기적인 데이터 보호 | Backup (전체/증분) |
| 서버 장애, 데이터 손상 복구 | Restore |
| 과거 특정 시점 데이터 조회 및 검증 | Mount |
| 운영 서버 마이그레이션 | Backup → 신규 서버에서 Restore |
| 특정 테이블만 과거 상태 확인 | Backup (테이블) → Mount |
| 데이터 감사나 포렌식 조회 | Mount (운영 서버 영향 없음) |

## 다음 읽을 내용

- [Backup / Restore / Mount 개념](/dbms/core-concepts/features-concepts/concepts-backup-restore-mount/) — 세 개념의 상세 설명
- [Retention vs DELETE / TRUNCATE](../retention-vs-delete-truncate/) — 데이터 삭제 수단 비교
