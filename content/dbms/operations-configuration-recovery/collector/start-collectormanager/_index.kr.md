---
type: docs
title: 'collectormanager 시작과 종료'
weight: 10
---

collectormanager는 Collector 인스턴스를 관리하는 데몬 프로세스입니다. Machbase 서버와 독립된 별도 프로세스이므로 Machbase 서버 기동 후에 별도로 시작해야 합니다.

## 시작

```bash
collectormanager start
```

정상적으로 시작되면 아래와 같이 출력됩니다.

```
Collector Manager started successfully.
```

collectormanager가 실행되면 설정 파일(`$MACHBASE_HOME/conf/collector_manager.conf`)에 정의된 포트를 통해 machcollectoradmin의 요청을 수신합니다.

## 상태 확인

```bash
collectormanager status
```

실행 중일 때 출력 예:

```
Collector Manager is running (pid: 12345).
```

중지 상태일 때 출력 예:

```
Collector Manager is not running.
```

## 종료

```bash
collectormanager stop
```

종료 시 실행 중인 모든 Collector 인스턴스가 먼저 안전하게 중지된 후 collectormanager 프로세스가 종료됩니다.

## 시작 순서

collectormanager는 반드시 Machbase 서버가 기동된 상태에서 시작해야 합니다. Machbase 서버가 실행되지 않은 상태에서 collectormanager를 시작하면 Collector 인스턴스가 Machbase에 연결하지 못해 수집이 실패합니다.

```
1. machadmin -u               # Machbase 서버 시작
2. collectormanager start     # collectormanager 시작
3. machcollectoradmin -a start -n <이름>  # 개별 Collector 시작
```

## 자동 시작 설정

시스템 재부팅 시 자동으로 시작되도록 systemd 서비스로 등록하거나, 운영 환경의 init 스크립트에 Machbase 서버 기동 직후 `collectormanager start`를 추가하는 것을 권장합니다.

## 로그

collectormanager 자체 로그는 `$MACHBASE_HOME/trc/` 디렉터리에 저장됩니다. 시작·종료 오류가 발생하면 해당 로그 파일을 먼저 확인합니다.

```bash
ls $MACHBASE_HOME/trc/collector*.trc
```
