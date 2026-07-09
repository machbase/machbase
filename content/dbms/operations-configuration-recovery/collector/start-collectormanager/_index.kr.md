---
type: docs
title: '13.5.1 Collector Manager 시작과 종료'
weight: 10
---

Collector Manager는 Collector 인스턴스를 관리하는 데몬 프로세스입니다. Machbase 서버와 독립된 별도 프로세스이므로 Machbase 서버 기동 후에 별도로 시작해야 합니다.

## 시작

```bash
machcollectoradmin --startup
```

정상적으로 시작되면 아래와 같이 출력됩니다.

```
Machbase Collector Manager started successfully.
```

Collector Manager가 실행되면 설정 파일(`$MACHBASE_COLLECTOR_HOME/conf/machcollector.conf`)에 정의된 설정을 사용합니다. `MACHBASE_COLLECTOR_HOME`을 별도로 지정하지 않은 환경에서는 `$MACHBASE_HOME`과 같은 홈을 사용할 수 있습니다.

## 상태 확인

```bash
machcollectoradmin --status-collector=all
```

Collector Manager에는 별도의 `--check` 옵션이 없습니다. 전체 Collector 상태 조회 명령으로 Collector Manager와 Collector 동작 상태를 함께 확인합니다.

## 종료

```bash
machcollectoradmin --shutdown
```

종료 시 실행 중인 모든 Collector 인스턴스가 먼저 안전하게 중지된 후 Collector Manager 프로세스가 종료됩니다.

## 시작 순서

Collector Manager는 반드시 Machbase 서버가 기동된 상태에서 시작해야 합니다. Machbase 서버가 실행되지 않은 상태에서 Collector 인스턴스를 시작하면 Machbase에 연결하지 못해 수집이 실패합니다.

```
1. machadmin -u               # Machbase 서버 시작
2. machcollectoradmin --startup                 # Collector Manager 시작
3. machcollectoradmin --start-collector=<이름>  # 개별 Collector 시작
```

## 자동 시작 설정

시스템 재부팅 시 자동으로 시작되도록 systemd 서비스로 등록하거나, 운영 환경의 init 스크립트에 Machbase 서버 기동 직후 `machcollectoradmin --startup`을 추가하는 것을 권장합니다.

## 로그

Collector Manager 자체 로그는 `$MACHBASE_COLLECTOR_HOME/trc/machcollectormanager.trc`에 저장됩니다. 관리 도구 로그는 `$MACHBASE_COLLECTOR_HOME/trc/machcollectoradmin.trc`에서 확인합니다.

```bash
tail -100 $MACHBASE_COLLECTOR_HOME/trc/machcollectormanager.trc
tail -100 $MACHBASE_COLLECTOR_HOME/trc/machcollectoradmin.trc
```
