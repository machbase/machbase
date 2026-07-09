---
type: docs
title: '13.4.1 진단과 로그'
weight: 10
---

Machbase는 서버 동작 전반과 각 도구의 실행 이력을 로그 파일에 기록합니다. 문제가 발생했을 때 가장 먼저 확인해야 할 정보의 출처입니다.

## 로그 파일 종류

| 로그 파일 | 기본 위치 | 생성 주체 |
|---------|---------|---------|
| `machbase.trc` | `$MACHBASE_HOME/trc/` | Machbase 서버 |
| machsql 이력 | `$MACHBASE_HOME/trc/machsql.history` | machsql 클라이언트 |
| `machloader.log` | 실행 디렉터리 | machloader |
| `machloader.err` | 실행 디렉터리 | machloader |
| Collector 로그 | `$MACHBASE_COLLECTOR_HOME/trc/` | Collector 프로세스 |

## 로그 디렉터리

Machbase 서버가 생성하는 로그는 모두 아래 디렉터리에 저장됩니다.

```
$MACHBASE_HOME/trc/
```

이 디렉터리에 기록되는 주요 파일:

- `machbase.trc` — 서버 메인 로그. 시작/종료, 오류, 경고, 진단 정보
- `machbase.trc.<날짜>` — 날짜별로 롤오버된 이전 로그 파일

로그 파일이 과도하게 커지면 디스크 공간을 소진할 수 있습니다. `TRACE_LOG_LEVEL` 설정으로 로깅 수준을 조정하고, 운영 환경에서는 불필요하게 상세한 레벨을 사용하지 않도록 합니다.

## 이 섹션의 구성

- [Trace Log 설정](./configuration-trace-log/) — `TRACE_LOG_LEVEL` 파라미터로 로깅 수준 제어
- [서버 로그](./log-server-logs/) — `machbase.trc` 분석과 주요 오류 패턴
- [machsql 로그](./log-logs-machsql/) — machsql 실행 이력 확인
- [machloader 로그](./log-logs-machloader/) — 데이터 적재 오류와 통계 확인
- [Collector 로그](./log-logs-collector/) — Collector 수집 상태 진단
