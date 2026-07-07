---
type: docs
title: 'Trace Log 설정'
weight: 10
---

Machbase 서버의 로깅 수준은 `TRACE_LOG_LEVEL` 프로퍼티로 제어합니다. 이 값이 높을수록 더 상세한 정보가 `machbase.trc`에 기록됩니다. 그러나 지나치게 높은 레벨은 디스크 I/O를 증가시켜 서버 성능에 영향을 줄 수 있으므로 운영 환경에서는 최소 레벨을 유지하는 것이 좋습니다.

## TRACE_LOG_LEVEL 설정

`$MACHBASE_HOME/conf/machbase.conf` 파일에서 설정합니다.

```
TRACE_LOG_LEVEL = 3
```

각 비트 플래그는 독립적으로 동작하며, 여러 플래그를 합산하여 설정할 수 있습니다.

| 값 | 의미 |
|----|------|
| 0 | 로깅 없음 |
| 1 | 오류 (Error) 메시지 |
| 2 | 경고 (Warning) 메시지 |
| 3 | 오류 + 경고 (권장 운영 설정) |
| 4 | 정보 (Info) 메시지 |
| 7 | 오류 + 경고 + 정보 |
| 32 | DUP_DROP 이벤트 (중복 레코드 삭제) |
| 63 | 전체 로깅 (디버깅 전용) |

운영 환경에서는 `3`(오류 + 경고)으로 설정하고, 문제 진단이 필요한 경우에만 일시적으로 높여 사용합니다.

## 런타임 변경

서버를 재시작하지 않고도 `ALTER SYSTEM` 명령으로 즉시 변경할 수 있습니다.

```sql
-- 현재 TRACE_LOG_LEVEL 확인
SELECT name, value
  FROM v$property
 WHERE name = 'TRACE_LOG_LEVEL';

-- 런타임 변경 (오류 + 경고 + 정보)
ALTER SYSTEM SET TRACE_LOG_LEVEL = 7;

-- 진단 완료 후 운영 수준으로 복원
ALTER SYSTEM SET TRACE_LOG_LEVEL = 3;
```

## 레벨별 로깅 내용

### 레벨 1 — 오류 (Error)

서버 동작에 영향을 주는 심각한 오류를 기록합니다.

- 디스크 쓰기 실패
- 메모리 할당 실패 (OOM)
- 네트워크 연결 오류
- 데이터 파일 손상 감지

### 레벨 2 — 경고 (Warning)

즉시 문제가 되지는 않지만 주의가 필요한 상황을 기록합니다.

- 디스크 사용량이 `RATIO_CAP`의 80% 초과
- 세션 수 한계 근접
- 느린 쿼리 감지

### 레벨 4 — 정보 (Info)

정상 운영 중의 주요 이벤트를 기록합니다.

- 서버 시작/종료
- DDL 실행 이력 (CREATE/DROP/ALTER)
- 백업 시작/완료
- 체크포인트 수행

### 레벨 32 — DUP_DROP 이벤트

Log 테이블에서 중복 타임스탬프 레코드가 삭제될 때 기록합니다. 대량 적재 시 중복 처리 현황을 추적해야 하는 경우에 유용합니다.

```
# machbase.trc에서 DUP_DROP 로그 예시
[2024-01-15 10:23:45] [INFO] DUP_DROP: table=SENSOR_LOG, dropped=1243, reason=duplicate_timestamp
```

`TRACE_LOG_LEVEL`에 `32`를 더해 활성화합니다.

```sql
-- 오류 + 경고 + DUP_DROP 조합 (1 + 2 + 32 = 35)
ALTER SYSTEM SET TRACE_LOG_LEVEL = 35;
```

## 권장 설정

| 환경 | TRACE_LOG_LEVEL | 이유 |
|------|----------------|------|
| 운영 (정상) | 3 | 오류와 경고만 기록. 디스크 I/O 최소화 |
| 운영 (중복 모니터링) | 35 | 오류 + 경고 + DUP_DROP |
| 장애 진단 중 | 7 | 오류 + 경고 + 정보. 일시적 사용 |
| 개발/디버깅 | 63 | 전체 로깅. 운영 환경에 비권장 |

> **주의**: `TRACE_LOG_LEVEL`이 높으면 로그 파일 크기가 빠르게 증가합니다. 디스크 공간을 정기적으로 확인하고, 진단 완료 후에는 반드시 운영 수준으로 복원하십시오.
