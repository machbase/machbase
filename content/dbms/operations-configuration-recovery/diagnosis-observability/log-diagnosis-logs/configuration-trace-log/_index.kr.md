---
type: docs
title: 'Trace Log 설정'
weight: 10
---

Machbase 서버의 로깅 수준은 `TRACE_LOG_LEVEL` 프로퍼티로 제어합니다. 이 값이 높을수록 더 상세한 정보가 `machbase.trc`에 기록됩니다. 그러나 지나치게 높은 레벨은 디스크 I/O를 증가시켜 서버 성능에 영향을 줄 수 있으므로 운영 환경에서는 최소 레벨을 유지하는 것이 좋습니다.

## TRACE_LOG_LEVEL 설정

`$MACHBASE_HOME/conf/machbase.conf` 파일에서 설정합니다.

```
TRACE_LOG_LEVEL = 277
```

각 비트 플래그는 독립적으로 동작하며, 여러 플래그를 합산하여 설정할 수 있습니다. 기본값은 `277`이며, `MM_1 + QP_1 + SM_1 + XM_1` 조합입니다.

| 값 | 모듈 |
|----|------|
| 1 | MM_1 |
| 2 | MM_2 |
| 4 | QP_1 |
| 8 | QP_2 |
| 16 | SM_1 |
| 32 | SM_2 |
| 64 | CC_1 |
| 128 | CC_2 |
| 256 | XM_1 |
| 512 | XM_2 |
| 1024 | LM_1 |
| 2048 | LM_2 |
| 4096 | RP_1 |
| 8192 | RP_2 |
| 65536 | MISC_1 |
| 131072 | MISC_2 |
| 262144 | DEBUG |

운영 환경에서는 기본값을 기준으로 유지하고, 특정 모듈 진단이 필요한 경우에만 해당 비트를 일시적으로 추가합니다.

## 런타임 변경

서버를 재시작하지 않고도 `ALTER SYSTEM` 명령으로 즉시 변경할 수 있습니다.

```sql
-- 현재 TRACE_LOG_LEVEL 확인
SELECT name, value
  FROM v$property
 WHERE name = 'TRACE_LOG_LEVEL';

-- 런타임 변경 (MM_1 + QP_1 + SM_1 + XM_1)
ALTER SYSTEM SET TRACE_LOG_LEVEL = 277;

-- QP_2를 추가한 진단 설정
ALTER SYSTEM SET TRACE_LOG_LEVEL = 285;
```

## 권장 설정

| 환경 | TRACE_LOG_LEVEL | 이유 |
|------|----------------|------|
| 운영 (정상) | 277 | 기본 모듈 1단계 로그 |
| QP 진단 | 285 | 기본값 + QP_2 |
| Storage 진단 | 309 | 기본값 + SM_2 |
| 개발/디버깅 | 262144 포함 | DEBUG 비트 포함. 운영 환경에 비권장 |

> **주의**: `TRACE_LOG_LEVEL`이 높으면 로그 파일 크기가 빠르게 증가합니다. 디스크 공간을 정기적으로 확인하고, 진단 완료 후에는 반드시 운영 수준으로 복원하십시오.
