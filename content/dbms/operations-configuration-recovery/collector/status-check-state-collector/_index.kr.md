---
type: docs
title: 'Collector 상태 확인'
weight: 30
---

Collector 상태를 정기적으로 확인하여 수집이 정상적으로 진행되고 있는지 점검합니다.

## 전체 Collector 목록 조회

```bash
machcollectoradmin --list
```

등록된 모든 Collector 인스턴스와 상태를 출력합니다.

```
Name           Status    Config File
-----------    --------  -----------------------------------
my_collector   RUNNING   /home/mach/conf/collector_a.xml
log_collector  STOPPED   /home/mach/conf/collector_b.xml
err_collector  ERROR     /home/mach/conf/collector_c.xml
```

## 특정 Collector 상태 조회

```bash
machcollectoradmin --status=my_collector
```

특정 Collector의 상세 상태를 출력합니다.

```
Name        : my_collector
Status      : RUNNING
Config File : /home/mach/conf/collector_a.xml
Collected   : 1,234,567 rows
Error Count : 0
Last Active : 2026-07-07 10:32:15
```

## Collector 상태 값

| 상태 | 의미 |
|------|------|
| `RUNNING` | 정상적으로 데이터를 수집 중 |
| `STOPPED` | 중지 상태. 시작 명령 대기 중 |
| `ERROR` | 수집 오류 발생. 로그 확인 필요 |
| `STARTING` | 시작 처리 중 (일시적 상태) |
| `STOPPING` | 종료 처리 중 (일시적 상태) |

## 로그 파일 위치

Collector 인스턴스별 로그는 `$MACHBASE_COLLECTOR_HOME/trc/` 디렉터리에 저장됩니다.

```bash
# 전체 Collector 로그 파일 목록
ls $MACHBASE_COLLECTOR_HOME/trc/machcollector*.trc

# 특정 Collector 로그 실시간 확인
tail -f $MACHBASE_COLLECTOR_HOME/trc/my_collector.trc
```

## 오류 확인 방법

ERROR 상태인 Collector가 있으면 다음 순서로 원인을 파악합니다.

1. **상태 조회**: `machcollectoradmin --status=<이름>`으로 오류 개수와 마지막 활동 시간 확인
2. **로그 확인**: `$MACHBASE_COLLECTOR_HOME/trc/<이름>.trc` 또는 `$MACHBASE_COLLECTOR_HOME/trc/machcollector.trc`에서 오류 메시지 확인
3. **Machbase 연결 확인**: Machbase 서버가 정상 실행 중인지 `machadmin -e`로 확인
4. **소스 연결 확인**: 데이터 소스(파일 경로, 소켓 포트, MQ 서버 등)가 유효한지 확인

오류 원인을 제거한 후 [장애 복구](../recovery-failure-collector/) 절차에 따라 복구합니다.

## 수집 지연 감지

수집이 지연되고 있는지 확인하려면 일정 시간 간격으로 `status` 명령을 실행하여 수집 행 수가 증가하는지 확인합니다.

```bash
# 10초 간격으로 수집 상태 확인
watch -n 10 "machcollectoradmin --status=my_collector"
```

수집 행 수가 증가하지 않거나 `Last Active` 시간이 오래된 경우 수집 지연 또는 중단 상태입니다.
