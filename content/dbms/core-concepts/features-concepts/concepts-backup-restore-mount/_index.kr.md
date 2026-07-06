---
type: docs
title: 'Backup / Restore / Mount 개념'
weight: 40
---

Backup, Restore, Mount는 Machbase의 데이터 보호와 복구를 담당하는 세 가지 수단입니다. 이름이 비슷해 혼동하기 쉽지만, 각각 목적과 사용 시점이 명확하게 구분됩니다.

## Backup: 운영 중 데이터 복사본 생성

Backup은 현재 운영 중인 데이터베이스를 멈추지 않고, 데이터 파일을 지정한 디렉터리에 복사하는 작업입니다. 서버가 계속 데이터를 수신하는 동안에도 Backup을 실행할 수 있습니다.

Backup 작업은 세 가지 상태를 거칩니다: `LAUNCHED` → `PROGRESS` → `FINISHED` (실패 시 `ERROR`).

지원하는 Backup 유형은 다음과 같습니다.

| 유형 | 설명 |
| --- | --- |
| 전체 Backup | 데이터베이스 전체를 복사 |
| 증분 Backup | 이전 Backup 이후 변경된 부분만 복사 |
| 기간 Backup | 특정 시간 범위의 데이터만 복사 |
| 테이블 Backup | 특정 테이블만 복사 |

```sql
-- 전체 백업 실행
BACKUP DATABASE INTO DISK = '/data/backup/full_20260703';

-- 특정 테이블 백업
BACKUP TABLE sensor_values INTO DISK = '/data/backup/sensor_20260703';
```

## Restore: 백업본으로 데이터베이스 복원

Restore는 백업본을 사용해 데이터베이스를 원래 위치에 복원하는 작업입니다. Backup과 달리, Restore는 반드시 서버를 중지한 상태에서 `machadmin` 도구로 실행합니다.

```bash
# 서버 중지 후 machadmin으로 복원
machadmin -r /data/backup/full_20260703
```

Restore는 장애로 인한 데이터 손상이나 서버 마이그레이션 시 사용합니다. 복원이 완료되면 서버를 재시작합니다.

## Mount: 백업본을 읽기 전용으로 연결

Mount는 백업본을 현재 운영 중인 서버에 읽기 전용으로 연결하는 기능입니다. 서버를 중지할 필요가 없으며, Mount된 데이터를 현재 운영 데이터와 함께 SELECT로 조회할 수 있습니다.

```sql
-- 백업본 Mount
MOUNT DATABASE '/data/backup/full_20260703' TO MOUNTDB;

-- Mount된 데이터 조회
SELECT * FROM MOUNTDB.sensor_values LIMIT 10;

-- Unmount
UNMOUNT DATABASE MOUNTDB;
```

Mount는 Restore와 달리 데이터를 원래 위치에 복사하지 않습니다. 백업본 디렉터리를 그대로 참조하는 방식이므로, 과거 특정 시점의 데이터를 조회하거나 검증하는 데 적합합니다.

## 세 개념의 관계

```
[운영 중인 서버]
        │
        ▼
   BACKUP 실행  ──────────────────────────────►  [백업 디렉터리]
   (서버 유지)                                          │
                                               ┌────────┴────────┐
                                               ▼                 ▼
                                          RESTORE           MOUNT
                                       (서버 중지 필요)   (서버 유지)
                                               │                 │
                                               ▼                 ▼
                                         원위치 복원      현재 서버에
                                         (장애 복구)    read-only 연결
                                                         (과거 조회)
```

## 각 수단의 선택 기준

| 상황 | 권장 수단 |
| --- | --- |
| 정기적인 데이터 보호 목적 | Backup (전체/증분) |
| 서버 장애, 데이터 손상 복구 | Restore |
| 과거 특정 시점 데이터 조회 및 검증 | Mount |
| 운영 서버 마이그레이션 | Backup → 신규 서버에서 Restore |
| 특정 테이블만 과거 데이터 확인 | Backup (테이블) → Mount |

## 다음 읽을 내용

- [Backup vs Restore vs Mount](/dbms/core-concepts/terminology-distinction/backup-vs-restore-mount/) — 세 개념의 비교 표
- [ROLLUP 통계의 역할](../role-statistics-rollup/) — 장기 데이터 집계 조회 성능 관리
- [Retention Policy의 역할](../role-retention-policy/) — 오래된 데이터 자동 삭제 정책
