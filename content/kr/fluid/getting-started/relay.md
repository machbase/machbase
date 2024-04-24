---
title: Fluid relay
weight: 180
---

## FLUID relay
일반적으로 Relay proxy는 클라이언트와 서버 사이에서 메시지를 전달해 주는 기능을 수행한다.  
FLUID relay proxy는 방화벽 등으로 차단된 환경에서 사용하기 위하여 방화벽 밖에 있는 FLUID 서버의 Broker에 접속하여 relay 기능을 수행한다.  

{{< figure src="../img/fluid-relay.jpg" width="700" >}}

- Reverse proxy 동일 기능 제공

## Command line
```bash
fluid relay --config <path>
```

| 플래그             | 단축 플래그  | 환경변수             | 필수 |    설명               |
|:-------------------|:------------:|:--------------------:|:----:|:----------------------|
| `--config <file>`  | `-c <file>`  | `FLUID_RELAY_CONFIG` | O    |                       |
| `--verbose`        | `-v`         |                      |      | 다양한 log 정보 제공   |
| `--dry-run`        |              |                      |      | 설정 파일의 오류를 확인 |
| `--broker`         |              | `FLUID_RELAY_BROKER` |      | default broker addresses |
| `--topic`          |              | `FLUID_RELAY_TOPIC`  |      | default topic         |

복수의 Broker를 사용하려면 `--broker` 플래그를 여러번 사용하거나 쉼표(,)로 주소를 구분하여 사용한다.

**환경변수 사용**
```sh
FLUID_RELAY_BROKER=secret@192.168.1.10:3000,secret@192.168.1.20:3000 fluid relay -c relay_config.yaml
```
