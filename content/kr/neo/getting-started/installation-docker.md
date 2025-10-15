---
title: Docker로 시작하기
type: docs
weight: 11
---

## 준비 사항

Docker는 어떤 버전이든 사용할 수 있지만 최신 버전을 권장합니다.

## Docker Pull

아래 명령을 터미널에 입력하면 Docker에서 machbase-neo 최신 버전을 내려받습니다.

```sh
$ docker pull machbase/machbase-neo
```

특정 버전을 설치하려면 명령에 태그를 추가해 주십시오.

```sh
$ docker pull machbase/machbase-neo:{{< neo_latestver >}}
```

다른 버전의 Docker 이미지를 찾고 싶으시면 [Docker Hub](https://hub.docker.com/r/machbase/machbase-neo/)에서 확인하실 수 있습니다.

## Docker Run

### 포그라운드 실행

```sh
$ docker run -it machbase/machbase-neo
```

- `-i`, `--interactive`: Keep STDIN open even if not attached
- `-t`, `--tty`: Allocate a pseudo-TTY

포그라운드로 실행하면 `Ctrl + c` 신호로 바로 종료하실 수 있습니다.

### 백그라운드 실행

```sh
$ docker run -d machbase/machbase-neo
```

- `-d`, `--detach`: Run container in background and print container ID

백그라운드로 실행한 경우 아래 명령으로 종료하실 수 있습니다.

```sh
$ docker stop $(docker ps | grep machbase-neo | awk '{print $1}')
```

machbase-neo 이미지를 여러 개 사용 중이라면 위 명령 대신 컨테이너 ID를 직접 지정하여 종료하시기를 권장드립니다.

__For example__

```sh
$ docker ps
CONTAINER ID   IMAGE                   COMMAND                   CREATED         STATUS        PORTS           NAMES
92382cf7b738   machbase/machbase-neo   "/bin/sh -c '/opt/ma…"   2 seconds ago   Up 1 second   5652-5656/tcp   exciting_volhard

$ docker stop 92382cf7b738

$ docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
# Container stopped.
```

기타 Docker 명령은 [Docker 문서](https://docs.docker.com/)를 참고해 주십시오.

## Docker 구성

### 볼륨

호스트 디렉터리를 Docker 컨테이너의 machbase-neo 홈 경로에 바인딩할 수 있습니다.

```sh
docker run -d
           -v /path/to/host/data:/data 
           -v /path/to/host/file:/file
           machbase/machbase-neo
```

- `/data`: Docker 컨테이너 내 machbase-neo 홈 경로입니다.
- `/file`: Docker 컨테이너 내 machbase-neo TQL 경로입니다.
- `-v`, `--volume`: 볼륨을 바인드 마운트합니다.

Docker가 중지되더라도 마운트된 호스트 디렉터리는 그대로 유지됩니다.

### 포트

machbase-neo는 Docker 내에서 여러 포트를 노출합니다.

|Port|Description|
|:-|:-----|
|5652|sshd|
|5653|mqtt|
|5654|http|
|5655|grpc|
|5656|database engine|

### 포트 매핑(포워딩)

```sh
$ docker run -d -p <host port>:<container port>/<protocol> machbase/machbase-neo
```

- `-p`, `--publish`: 컨테이너 포트를 호스트에 공개합니다.
- `<host port>`: 호스트 머신 포트입니다.
- `<container port>`: 컨테이너 포트입니다.
- `<protocol>`: tcp, udp, sctp 등을 지정합니다.

machbase-neo 컨테이너를 실행할 때 아래와 같이 호스트 포트를 컨테이너 포트에 매핑하실 수 있습니다.

__For example__

```sh
$ docker run -d                           \
             -p 5652-5652:5652-5656/tcp   \
             --name machbase-neo          \
             machbase/machbase-neo
```

이렇게 구성하면 호스트 포트로 들어온 모든 요청이 컨테이너 포트로 전달됩니다.

### SSH 키를 이용한 machbase-neo 셸 원격 접속

machbase-neo 셸에 접속하기 전에 SSH 키를 생성해야 합니다.

```sh
$ ssh-keygen -t rsa
```

SSH 키를 만들었다면 다른 환경에서 machbase-neo를 실행해 주십시오.

```sh
$ docker pull machbase/machbase-neo
$ docker run -d
             -p 5652-5656:5652-5656/tcp
             --name machbase-neo
             machbase/machbase-neo
```

기본적으로 SSH로 접속할 때마다 비밀번호 입력이 필요합니다. 하지만 machbase-neo 셸에 키를 등록하면 한 번만 비밀번호를 입력하도록 설정할 수 있습니다.

```sh
$ ssh -l sys -p 5652 192.168.0.116 ssh-key add `cat ~/.ssh/id_rsa.pub`
sys@192.168.0.116's password? manager
Add sshkey success
```

이렇게 설정하면 매번 비밀번호를 입력하지 않고 접속하실 수 있습니다.

__For Example__

```sh
$ ssh -l sys -p 5652 192.168.0.116 'create table example (v1 int)';
executed.

$ ssh -l sys -p 5652 192.168.0.116 'show tables';
┌──────────────────────────────────────────────────┐
│ ROWNUM │ DB         │ USER │ NAME    │ TYPE      │
├──────────────────────────────────────────────────┤
│      1 │ MACHBASEDB │ SYS  │ EXAMPLE │ Log Table │
└──────────────────────────────────────────────────┘
```

### Docker Compose 사용

아래 내용을 `docker-compose.yml` 파일로 저장한 뒤 프로젝트 루트 디렉터리에 배치해 주십시오.

```yml
# docker-compose.yml
version: '3'
services:
  machbase-neo:
    image: machbase/machbase-neo
    container_name: machbase-neo
    hostname: machbase
    volumes:
      - /data:/data
      - /file:/file
    ports:
      - "5652:5652" # sshd
      - "5653:5653" # mqtt
      - "5654:5654" # http
      - "5655:5655" # grpc
      - "5656:5656" # database engine
```

그다음 아래 명령을 프로젝트 루트 디렉터리에서 실행해 주십시오.

```sh
$ docker compose up -d
```

또는 아래와 같이 실행하셔도 됩니다.

```sh
$ docker compose -f docker-compose.yml up -d
```

Docker Compose를 중지하려면 다음 명령을 사용하십시오.

```sh
$ docker compose down
```

그러면 모든 서비스가 정상적으로 종료됩니다.
