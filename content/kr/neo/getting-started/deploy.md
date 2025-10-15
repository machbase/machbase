---
title: 배포 모드
type: docs
weight: 13
---


## 헤드 온리 모드

{{< neo_since ver="8.0.45" />}}

아래 예시처럼 `--data` 플래그 값이 다른 Machbase DBMS의 mach 포트(`5656`)를 가리키는 URL이라면 다음과 같이 실행합니다.

```sh
machbase-neo serve --data machbase://sys:manager@192.168.1.100:5656
```

또는 사용자 이름과 비밀번호를 환경 변수로 전달할 수도 있습니다.

```sh
SECRET="sys:manager" \
machbase-neo serve --data machbase://${SECRET}@192.168.1.100:5656
```

이 모드에서는 machbase-neo 프로세스가 자체 데이터베이스 없이 실행되고 대상 데이터베이스를 그대로 사용합니다.
"헤드 온리 machbase-neo"는 5656 포트를 제공하지 않으며, 나머지 API는 모두 대상 DBMS와 연동됩니다.

{{< figure src="../img/head-only-1.png" width="600px" >}}


## 헤드리스 모드

{{< neo_since ver="8.0.45" />}}

`machbase-neo serve-headless`는 Machbase DBMS mach 포트(`5656`)만 사용하는 DBMS 프로세스를 실행합니다. 이 모드는 다른 서비스 포트(HTTP, MQTT, gRPC, SSH)와 관련 기능 없이 DBMS만 구동할 때 유용합니다.

이 실행 모드는 별도로 구동되는 "헤드 온리" 프로세스와 함께 동작하도록 설계되어,
API 서비스와 DBMS 엔진을 분리할 수 있습니다.

{{< figure src="../img/head-only-2.png" width="600px" >}}
