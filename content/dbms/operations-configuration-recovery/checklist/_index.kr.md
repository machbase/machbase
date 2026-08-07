---
type: docs
title: '14.12 운영 체크리스트'
weight: 120
toc: true
---

정기적으로 수행해야 하는 점검 항목입니다. 일별·주별·월별 루틴 점검과 장애 발생 시 대응 체크리스트로 구성됩니다.

## 일별 점검

매일 업무 시작 전 또는 자동화 스크립트로 수행합니다.

### 서버 상태

```bash
# 서버 실행 여부 확인
machadmin -e

# 서버가 응답하지 않는 경우
pgrep -la machbased   # OS 레벨에서 서버 프로세스 확인
```

### 디스크 사용량

```bash
# OS 레벨 디스크 사용량
df -h

# Machbase 데이터 디렉터리 사용량
du -sh $MACHBASE_HOME/dbs/
```

```sql
-- Machbase SQL로 디스크 사용량 확인
ALTER SYSTEM CHECK DISK_USAGE;
SELECT total_space, used_space, used_ratio, ratio_cap
  FROM v$storage_usage;
```

디스크 사용량이 80% 이상이면 즉시 데이터 정리 또는 용량 증설을 검토합니다.

### 장기 실행 세션 확인

```sql
-- 장시간 실행 중인 SQL 세션 확인
SELECT s.id AS session_id, s.user_name, st.id AS stmt_id, st.state, st.query
  FROM v$session s
  JOIN v$stmt st ON s.id = st.sess_id
 WHERE st.state LIKE 'Execute in progress%'
    OR st.state LIKE 'Fetch in progress%'
    OR st.state LIKE 'Append in progress%';
```

비정상적으로 오래 실행 중인 세션은 원인을 파악하고 필요 시 종료합니다.

### Collector 상태 (Collector 운영 환경)

```bash
# 전체 Collector 상태 확인
machcollectoradmin --list

# ERROR 상태 Collector 로그 확인
tail -50 $MACHBASE_COLLECTOR_HOME/trc/machcollector.trc
```

### Cluster 상태 (Cluster Edition)

```bash
# 클러스터 전체 노드 상태 확인
machcoordinatoradmin --cluster-status
```

비정상 노드(`**unknown**`, `inactive`, `scrapped`)가 있으면 즉시 [Warehouse 상태 복구](/dbms/operations-configuration-recovery/cluster/#recovery-state-status-warehouse) 절차를 진행합니다.

---

## 주별 점검

매주 정해진 요일에 수행합니다.

### 백업 실행 및 검증

```sql
-- 온라인 백업 실행
BACKUP DATABASE INTO DISK = '/backup/machbase_weekly';
```

백업 완료 후 백업 파일이 정상적으로 생성되었는지 확인합니다.

```bash
machadmin -w /backup/machbase_weekly
```

### Result Cache 히트율

```sql
-- Result Cache 통계 확인
SELECT * FROM v$rs_cache_stat;
```

히트율이 낮은 경우 캐시 설정 또는 쿼리 패턴을 검토합니다.

### 라이선스 만료일 확인

```sql
-- 라이선스 정보 확인
SELECT * FROM v$license_info;
```

만료 30일 이내인 경우 갱신 절차를 시작합니다.

### 서버 로그 검토

```bash
# 최근 1주일 경고·오류 로그 확인
grep -E 'WARN|ERROR' $MACHBASE_HOME/trc/machbase.trc | tail -200
```

반복되는 경고나 오류 패턴을 파악하고 원인을 제거합니다.

---

## 월별 점검

매월 초 또는 정기 유지보수 일정에 수행합니다.

### 용량 추세 분석

전월 대비 데이터 증가량을 집계하여 향후 용량 계획에 반영합니다.

```bash
# 데이터 디렉터리 용량 기록
du -sh $MACHBASE_HOME/dbs/ >> /var/log/machbase_capacity.log
```

```sql
-- 테이블별 레코드 수 집계
SELECT mt.name AS table_name,
       st.storage_usage
  FROM v$storage_tables st
  JOIN m$sys_tables mt ON st.id = mt.id
 ORDER BY st.storage_usage DESC;
```

### 인덱스 점검

```sql
-- 전체 인덱스 목록 확인
SHOW INDEXES;
```

사용되지 않거나 중복된 인덱스는 제거하여 쓰기 성능을 개선합니다.

### 권한과 접속 정책 검토

```sql
-- 사용자 목록 확인
SELECT user_id, name, valid_before
  FROM m$sys_users
 ORDER BY user_id;
```

불필요한 계정이나 만료 정책이 없는 계정이 있으면 보안 정책을 강화합니다.

---

## 장애 대응 체크리스트

장애 발생 시 아래 표를 참고하여 신속하게 원인을 파악하고 조치합니다.

| 증상 | 확인 명령 | 조치 |
|------|-----------|------|
| 서버 응답 없음 | `machadmin -e` | 재시작(`machadmin -u`) 또는 강제 종료 후 재시작 |
| 디스크 풀 | `df -h` | 오래된 데이터·로그 정리, 보관 데이터 외부 이동 |
| 메모리 부족 | `free -h` | 캐시 크기 조정, 장기 실행 세션 종료 |
| 수집 중단 | `machcollectoradmin --list` / Collector 로그 | Collector 재시작 |
| 쿼리 느림 | `EXPLAIN <쿼리>` | 인덱스 추가, ROLLUP 활용, 쿼리 튜닝 |
| 클러스터 노드 이탈 | `machcoordinatoradmin --cluster-status` | 노드 재시작 또는 [Warehouse 복구](/dbms/operations-configuration-recovery/cluster/#recovery-state-status-warehouse) |
| 클라이언트 연결 불가 | `machadmin -e` / Broker 상태 | Broker 재시작, 포트·방화벽 확인 |
| 라이선스 만료 | `SELECT * FROM v$license_info` | 라이선스 갱신 후 서버 재시작 |

## 자동화 권장 사항

- 일별 점검 항목은 cron 스크립트로 자동화하고 결과를 이메일 또는 모니터링 시스템으로 전송합니다.
- 디스크 사용량 80% 초과 시 자동 알림을 설정합니다.
- 백업은 `cron`으로 자동 실행하고 성공/실패 여부를 기록합니다.

```bash
# crontab 예시
# 매일 오전 8시 서버 상태 및 디스크 확인
0 8 * * * /opt/scripts/machbase_daily_check.sh >> /var/log/machbase_check.log 2>&1

# 매주 일요일 새벽 2시 백업 실행
0 2 * * 0 /opt/scripts/machbase_weekly_backup.sh >> /var/log/machbase_backup.log 2>&1
```
