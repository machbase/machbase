---
type: docs
title: '로그 확인'
weight: 30
---

Machbase는 서버 동작과 오류를 `$MACHBASE_HOME/trc/` 디렉터리의 로그 파일에 기록합니다. 문제 발생 시 로그 파일을 분석하면 원인을 신속하게 파악할 수 있습니다.

## 주요 로그 파일

| 파일 | 내용 |
|------|------|
| `$MACHBASE_HOME/trc/machbase.trc` | 서버 메인 로그. 시작/종료, 오류, 경고, 운영 이벤트 기록 |
| `$MACHBASE_HOME/trc/machsql.history` | machsql 대화형 세션의 SQL 실행 이력 |
| `machloader -b`로 지정한 bad file | machloader 적재 실패 레코드 (행 단위) |
| `machloader -l`로 지정한 log file | machloader 처리 건수, 오류 건수 통계 |
| `$MACHBASE_COLLECTOR_HOME/trc/` | Collector 에이전트 수집 상태 로그 |

## 서버 메인 로그 확인 방법

### 최근 오류 빠르게 확인

```bash
# 최근 100줄에서 오류와 경고 필터링
tail -100 $MACHBASE_HOME/trc/machbase.trc | grep -i "error\|warn"

# 최근 50줄 전체 확인
tail -50 $MACHBASE_HOME/trc/machbase.trc
```

### 특정 시점 로그 검색

```bash
# 특정 날짜 로그 검색
grep "2024-01-15" $MACHBASE_HOME/trc/machbase.trc | head -50

# 오류만 추출
grep -i "error" $MACHBASE_HOME/trc/machbase.trc | tail -20
```

## 로그 레벨과 의미

`machbase.trc`에 기록되는 로그 항목은 심각도에 따라 구분됩니다.

| 레벨 | 의미 | 조치 |
|------|------|------|
| `ERROR` | 즉시 조치가 필요한 오류. 서비스에 영향을 미침 | 원인을 파악하고 즉시 해결 |
| `WARN` | 경고. 즉각적인 장애는 없지만 성능 저하 또는 향후 문제 가능성 | 원인 파악 후 계획적으로 해결 |
| `INFO` | 일반 운영 정보. 서버 시작, 세션 연결, 정기 작업 완료 등 | 참고용, 별도 조치 불필요 |

## 로그 상세도 조정 (TRACE_LOG_LEVEL)

운영 중 특정 모듈의 동작을 상세히 추적할 때는 `TRACE_LOG_LEVEL`을 조정합니다.

```sql
-- 현재 로그 레벨 확인
SELECT name, value FROM v$property WHERE name = 'TRACE_LOG_LEVEL';

-- 기본값(277)으로 복원
ALTER SYSTEM SET TRACE_LOG_LEVEL = 277;
```

주요 레벨 값 (더해서 사용):

| 값 | 모듈 |
|----|------|
| 1 | MM_1 (Main Module 레벨 1) |
| 4 | QP_1 (Query Processor 레벨 1) |
| 16 | SM_1 (Storage Manager 레벨 1) |
| 256 | XM_1 (Cluster 쿼리 분산 레벨 1) |

기본값 277 = 1(MM_1) + 4(QP_1) + 16(SM_1) + 256(XM_1)

## 로그 순환 설정

로그 파일이 무한히 커지는 것을 방지하기 위해 두 가지 파라미터를 설정합니다.

```sql
-- 현재 설정 확인
SELECT name, value FROM v$property
WHERE name IN ('TRACE_FLUSH_INTERVAL', 'TRACE_TRUNCATE_THRESHOLD');
```

| 파라미터 | 기본값 | 설명 |
|---------|--------|------|
| `TRACE_FLUSH_INTERVAL` | 3 (초) | 로그 버퍼를 파일에 기록하는 주기 |
| `TRACE_TRUNCATE_THRESHOLD` | 100MB | 이 크기를 초과하면 로그 파일을 순환 |

`machbase.conf`에서 영구 설정:

```properties
TRACE_FLUSH_INTERVAL       = 3
TRACE_TRUNCATE_THRESHOLD   = 104857600
```

## 로그에서 원인 파악하는 방법

로그 항목은 보통 다음 형식으로 기록됩니다.

```
[2024-01-15 10:23:45] [ERROR] [QP] ERR-02058: Table does not exist. (TABLE_NAME)
```

- **시각**: 문제 발생 시점 특정
- **레벨**: ERROR/WARN/INFO
- **모듈**: 어느 내부 모듈에서 발생했는지 (QP=쿼리 처리, SM=스토리지, MM=메인)
- **오류 코드**: `ERR-XXXXX` 형식의 코드로 [오류 코드로 원인 찾기](../cause-lookup-error-codes/) 섹션에서 상세 내용을 조회

서버 시작 실패의 경우 로그 파일 맨 끝부분에 원인이 기록됩니다.

```bash
tail -30 $MACHBASE_HOME/trc/machbase.trc
```
