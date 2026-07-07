---
type: docs
title: '장애 징후 확인'
weight: 60
---

장애가 발생하기 전에 징후를 발견하여 선제적으로 대응하는 것이 중요합니다. 아래 패턴들을 정기적으로 확인하거나, 이상 증상이 보일 때 단계적으로 점검합니다.

## 디스크 풀 징후

### 징후

- 데이터 적재가 갑자기 중단됨
- machbase.trc에 디스크 관련 오류가 반복됨
- Machbase 오류: "Disk full" 또는 "errno=28"

### 확인 방법

```bash
# OS 레벨 디스크 확인
df -h

# Machbase 데이터 디렉터리 특정 확인
df -h $MACHBASE_HOME/dbs/
```

```sql
-- 스토리지 사용률과 한계 확인
SELECT used_ratio, ratio_cap
  FROM v$storage_usage;
```

```bash
# 서버 로그에서 디스크 관련 오류 확인
grep -i 'disk full\|errno=28\|No space left' $MACHBASE_HOME/trc/machbase.trc | tail -20
```

### 즉각 조치

1. 오래된 트레이스 로그 삭제: `find $MACHBASE_HOME/trc/ -name "*.trc.*" -mtime +30 -delete`
2. 오래된 데이터 삭제: `DELETE FROM <table> BEFORE TO_DATE('...', 'YYYY-MM-DD');`
3. `DISK_FULL_RATIO` 설정 검토 (실제 공간 확보 병행 필수)

---

## 메모리 과다 사용 징후

### 징후

- 서버 프로세스가 갑자기 종료됨
- 쿼리 실행 시 메모리 부족 오류 발생
- 시스템 응답이 매우 느려짐

### 확인 방법

```bash
# 시스템 전체 메모리 확인
free -h

# Machbase 프로세스 메모리 사용량
ps aux | grep machbased | grep -v grep

# OOM Killer 발동 여부 확인
grep 'Out of memory\|oom_kill' /var/log/syslog 2>/dev/null | tail -10
dmesg | grep -i 'oom\|killed process' | tail -10
```

```sql
-- 메모리 매니저별 사용량
SELECT name, round(usage/1048576.0, 1) AS mb, round(max_usage/1048576.0, 1) AS peak_mb
  FROM v$sysmem
 ORDER BY usage DESC;

-- 메모리 과다 사용 세션 확인
SELECT sm.sid, s.user_name, round(sum(sm.usage)/1048576.0, 1) AS mb
  FROM v$sesmem sm
  JOIN v$session s ON sm.sid = s.id
 WHERE s.closed = 0
 GROUP BY sm.sid, s.user_name
 ORDER BY mb DESC;
```

### 즉각 조치

1. 메모리 과다 세션 강제 종료: `ALTER SYSTEM KILL SESSION <id>;`
2. `MAX_QPX_MEM` 설정으로 세션당 쿼리 메모리 제한
3. Volatile 테이블 또는 Result Cache 메모리 설정 검토

---

## 세션 과다 징후

### 징후

- 새로운 연결이 거부됨
- machbase.trc에 "Max session count reached" 오류 발생

### 확인 방법

```sql
-- 현재 세션 수와 최대 세션 수 비교
SELECT (SELECT value FROM v$property WHERE name = 'MAX_SESSION_COUNT') AS max_sessions,
       (SELECT count(*) FROM v$session WHERE closed = 0)               AS current_sessions;

-- 오래 접속된 세션 확인 (오늘보다 하루 이상 이전)
SELECT id, user_name, user_ip, login_time
  FROM v$session
 WHERE closed = 0
 ORDER BY login_time ASC
 LIMIT 20;
```

### 즉각 조치

1. 불필요한 세션 정리: `ALTER SYSTEM KILL SESSION <id>;`
2. `MAX_SESSION_COUNT` 값 검토 및 상향
3. 클라이언트 애플리케이션의 커넥션 풀 설정 점검

---

## 느린 쿼리 징후

### 징후

- 평소보다 쿼리 응답이 느림
- 애플리케이션 타임아웃 오류 발생
- 서버 CPU 사용률이 지속적으로 높음

### 확인 방법

```sql
-- 현재 실행 중인 쿼리 확인
SELECT id, sess_id, state, query
  FROM v$stmt
 WHERE state LIKE 'Execute in progress%'
    OR state LIKE 'Fetch in progress%'
    OR state LIKE 'Append in progress%';

-- 세션별 누적 실행 시간 확인 (큰 순서)
SELECT st.sid, s.user_name,
       st.accum_msec, st.max_msec
  FROM v$sestime st
  JOIN v$session s ON st.sid = s.id
 WHERE s.closed = 0
 ORDER BY st.accum_msec DESC
 LIMIT 10;
```

```sql
-- 시스템 전반 통계 확인
SELECT name, value
  FROM v$sysstat
 ORDER BY name;
```

### 즉각 조치

1. 오래 실행 중인 쿼리의 세션 강제 종료
2. 쿼리 실행 계획 확인 (인덱스 누락 여부)
3. 필요한 모듈 비트를 추가해 `TRACE_LOG_LEVEL`을 일시적으로 높여 상세 로그 수집

---

## Rollup/Stream 이상 징후

### 확인 방법

```sql
-- Rollup 비활성화 또는 오류 확인
SELECT rollup_table, source_table, enabled, run_state, last_elapsed_msec
  FROM v$rollup
 WHERE enabled = 0 OR run_state != 'S';

-- Stream 오류 확인
SELECT name, state, error_msg
  FROM v$streams
 WHERE error_msg IS NOT NULL AND error_msg != '';
```

---

## 장애 발생 시 즉각 조치 체크리스트

장애 또는 이상 증상 발생 시 아래 순서로 점검합니다.

| 단계 | 확인 항목 | 명령/쿼리 |
|------|---------|---------|
| 1 | 서버 프로세스 실행 여부 | `machadmin -e` |
| 2 | 서버 로그 오류 확인 | `tail -100 $MACHBASE_HOME/trc/machbase.trc` |
| 3 | 디스크 사용률 | `df -h` 및 `SELECT used_ratio FROM v$storage_usage` |
| 4 | 메모리 여유 | `free -h` |
| 5 | OOM 발생 여부 | `dmesg \| grep -i oom` |
| 6 | 세션 과다 여부 | `SELECT count(*) FROM v$session WHERE closed = 0` |
| 7 | 실행 중인 쿼리 | `SELECT * FROM v$stmt WHERE state LIKE 'Execute in progress%'` |
| 8 | 라이선스 위반 | `SELECT violate_status FROM v$license_info` |

체크리스트 점검 후 원인이 파악되면 해당 섹션의 조치 지침을 따릅니다. 원인이 불명확하면 `TRACE_LOG_LEVEL`을 높여 상세 로그를 수집한 뒤 Machbase 지원팀에 로그를 제공하십시오.
