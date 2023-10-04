---
title: Get started with Docker
type: docs
weight: 11
---

## Prepare

Docker any version. (latest version recommended)

## Docker Pull

Copy the command below and enter it in the terminal to install the latest version of machbase-neo in Docker.

```sh
$ docker pull machbase/machbase-neo
```

If you want to get a specific version, add a tag to the command.

```sh
$ docker pull machbase/machbase-neo:{{ site.latest_version }}
```

If you want to find a different version of the Docker image, look it up [here](https://hub.docker.com/r/machbase/machbase-neo/).

## Docker Run

### Foreground

```sh
$ docker run -it machbase/machbase-neo
```

- `-i`, `--interactive`: Keep STDIN open even if not attached
- `-t`, `--tty`: Allocate a pseudo-TTY

If you run with foreground, you can exit directly with `Ctrl + c` signal.

### Background

```sh
$ docker run -d machbase/machbase-neo
```

- `-d`, `--detach`: Run container in background and print container ID

If you run with background, you can exit indirectly with below command.

```sh
$ docker stop $(docker ps | grep machbase-neo | awk '{print $1}')
```

If you are using multiple machbase-neo images, it is recommended that you stop by entering the Container ID directly instead of the above command.

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

For more docker commands, see [Docker docs](https://docs.docker.com/).

## Docker Configuration

### Volume

You can bind to machbase-neo home path in docker from host directory. 

```sh
docker run -d
           -v /path/to/host/data:/data 
           -v /path/to/host/file:/file
           machbase/machbase-neo
```

- `/data`: machbase-neo home path in docker
- `/file`: machbase-neo tql path in docker
- `-v`, `--volume`: Bind mount a volume.

Even if Docker stops, the host directory of the mounted volume remains.

### Port

Machbase-neo exposes several ports in Docker.

|Port|Description|
|:-|:-----|
|5652|sshd|
|5653|mqtt|
|5654|http|
|5655|grpc|
|5656|database engine|

### Port mapping (forwarding)

```sh
$ docker run -d -p <host port>:<container port>/<protocol> machbase/machbase-neo
```

- `-p`, `--publish`: Publish a container’s port(s) to the host
- `<host port>`: The port of host machine.
- `<container port>`: The port of container.
- `<protocol>`: specify tcp, udp, sctp

When run machbase-neo container, you can map host port to container port like this.

__For example__

```sh
$ docker run -d                           \
             -p 5652-5652:5652-5656/tcp   \
             --name machbase-neo          \
             machbase/machbase-neo
```

With this configuration, all requests made to the host port will be forwarded to the container port.

### Remote access to machbase-neo shell using ssh-key

Before connecting to machbase-neo shell, you need to generate an SSH key.

```sh
$ ssh-keygen -t rsa
```

After you create the ssh key, run machbase-neo in a different environment.

```sh
$ docker pull machbase/machbase-neo
$ docker run -d
             -p 5652-5656:5652-5656/tcp
             --name machbase-neo
             machbase/machbase-neo
```

By default, you will be prompted to enter your password every time you connect via SSH. However, by registering with the machbase-neo shell, you can set it up to enter your password just once.

```sh
$ ssh -l sys -p 5652 192.168.0.116 ssh-key add `cat ~/.ssh/id_rsa.pub`
sys@192.168.0.116's password? manager
Add sshkey success
```

This will allow you to access without having to enter your password every time.

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

### via Docker compose

Save the contents below in `docker-compose.yml` and place them in your project's root directory.

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

Then copy below and execute in your project's root direcotry.

```sh
$ docker compose up -d
```

Or:

```sh
$ docker compose -f docker-compose.yml up -d
```

If you want to shut down docker compose, use this.

```sh
$ docker compose down
```

Then all of the services shut down gracefully.