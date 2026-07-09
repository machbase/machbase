---
type: docs
title: '16.1.1 증상 확인'
weight: 10
---

문제가 발생했을 때 아래 표에서 증상을 찾아 먼저 확인할 항목과 이동할 섹션을 파악합니다.

## 증상별 빠른 진단 표

| 증상 | 먼저 확인할 항목 | 이동할 섹션 |
|------|----------------|------------|
| 서버 접속 불가 (Connection refused) | 프로세스 실행 여부 확인 | [서버가 시작되지 않을 때](../../server-connection/start-server/) |
| 서버 시작 실패 | `machbase.trc` 최근 오류 확인 | [서버가 시작되지 않을 때](../../server-connection/start-server/) |
| 원격 접속 불가 (로컬은 정상) | `GRANT_REMOTE_ACCESS` 설정, 방화벽 | [연결할 수 없을 때](../../server-connection/connection/) |
| 비밀번호/인증 오류 | 대소문자, AUTH KEY 등록 여부 | [인증이 실패할 때](../../server-connection/failure-authentication/) |
| 쿼리 결과 없음 | 데이터 존재 여부, 시간 범위 조건 | [검색 결과 문제](../../performance/search-results/) |
| 입력 속도 저하 | `v$stmt`로 실행 중인 쿼리 확인 | [쿼리 성능 문제](../../performance/slow/) |
| 메모리 부족 오류 | `v$sysmem`으로 메모리 현황 확인 | [메모리 부족](../../performance/memory-out-of/) |
| 데이터 입력 실패 | 오류 코드, 테이블 스키마 확인 | [데이터 입력 실패](../../item/failure/) |
| CSV 임포트 오류 | `machloader -b`로 지정한 bad file 확인 | [CSV 임포트 실패](../../item/failure-csv-import/) |
| UPDATE/DELETE 오류 | 테이블 타입, WHERE 조건 확인 | [UPDATE/DELETE 문제](../../update-delete/) |
| ROLLUP 결과 이상 | `v$rollup`으로 ROLLUP 상태 확인 | [ROLLUP 문제](../../automation/rollup/) |
| STREAM 쿼리 미실행 | `v$streams`으로 STREAM 상태 확인 | [STREAM 문제](../../automation/execution-stream/) |
| 백업 실패 | 디스크 공간, 백업 경로 권한 확인 | [백업과 복구 문제](../../recovery-backup/failure-backup-restore/) |
| MOUNT 실패 | 백업 파일 존재 여부, 버전 확인 | [MOUNT 실패](../../recovery-backup/failure-mount/) |
| Cluster 노드 이상 | 노드 간 네트워크 연결 확인 | [Cluster 문제](../../cluster/) |

## 서버 상태 즉시 확인

문제가 발생하면 가장 먼저 서버 프로세스 상태를 확인합니다.

```bash
# 서버 프로세스 상태 확인
machadmin -e
```

정상 상태에서는 아래와 같이 출력됩니다.

```
Machbase server is running.
```

서버가 실행 중이 아니면 다음을 확인합니다.

```bash
# 서버 프로세스 직접 확인
ps aux | grep machbase

# 포트 사용 여부 확인 (기본 포트: 5656)
netstat -tlnp | grep 5656
```

## 현재 연결 상태 확인

서버에 접속할 수 있다면 현재 세션 수와 상태를 확인합니다.

```sql
-- 현재 세션 수
SELECT COUNT(*) FROM v$session;

-- 세션 목록
SELECT id, login_time, user_name, user_ip, closed FROM v$session;
```

세션 수가 비정상적으로 많으면 연결 풀 설정이나 최대 연결 수를 확인합니다. 실행 중인 쿼리가 있으면 다음으로 확인합니다.

```sql
-- 실행 중인 쿼리 확인
SELECT sess_id, id, state, record_size, query FROM v$stmt;
```
