---
toc: true
title: Dockerで始める
type: docs
weight: 11
---

## 準備 {#준비-사항}

Dockerはどのバージョンでも使用できますが、最新バージョンを推奨します。

## Dockerイメージの取得 {#docker-pull}

以下のコマンドをターミナルで実行すると、machbase-neoの最新Dockerイメージをダウンロードできます。

```sh
$ docker pull machbase/machbase-neo
```

特定のバージョンをインストールするには、コマンドにタグを追加します。

```sh
$ docker pull machbase/machbase-neo:{{< neo_latestver >}}
```

他のバージョンのDockerイメージは、[Docker Hub](https://hub.docker.com/r/machbase/machbase-neo/)で確認できます。

## Dockerコンテナの実行 {#docker-run}

### フォアグラウンドでの実行 {#포그라운드-실행}

```sh
$ docker run -it machbase/machbase-neo
```

- `-i`, `--interactive`: 接続していない場合も標準入力を開いたままにします。
- `-t`, `--tty`: 疑似TTYを割り当てます。

フォアグラウンドで実行すると、`Ctrl + c`で直接停止できます。

### バックグラウンドでの実行 {#백그라운드-실행}

```sh
$ docker run -d machbase/machbase-neo
```

- `-d`, `--detach`: コンテナをバックグラウンドで実行し、コンテナIDを表示します。

バックグラウンドで実行した場合は、以下のコマンドで停止できます。

```sh
$ docker stop $(docker ps | grep machbase-neo | awk '{print $1}')
```

machbase-neoイメージを複数使用している場合は、上記のコマンドではなくコンテナIDを直接指定して停止することを推奨します。

__例__

```sh
$ docker ps
CONTAINER ID   IMAGE                   COMMAND                   CREATED         STATUS        PORTS           NAMES
92382cf7b738   machbase/machbase-neo   "/bin/sh -c '/opt/ma…"   2 seconds ago   Up 1 second   5652-5656/tcp   exciting_volhard

$ docker stop 92382cf7b738

$ docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
# コンテナは停止しています。
```

その他のDockerコマンドは、[Dockerドキュメント](https://docs.docker.com/)を参照してください。

## Dockerの構成 {#docker-구성}

### ボリューム {#볼륨}

ホストのディレクトリを、Dockerコンテナ内のmachbase-neoのホームパスにバインドできます。

```sh
docker run -d
           -v /path/to/host/data:/data 
           -v /path/to/host/file:/file
           machbase/machbase-neo
```

- `/data`: Dockerコンテナ内のmachbase-neoのホームパスです。
- `/file`: Dockerコンテナ内のmachbase-neoのTQLパスです。
- `-v`, `--volume`: ボリュームをバインドマウントします。

Dockerが停止しても、マウントしたホストのディレクトリは保持されます。

### ポート {#포트}

machbase-neoはDocker内で複数のポートを公開します。

|ポート|説明|
|:-|:-----|
|5652|sshd|
|5653|mqtt|
|5654|http|
|5655|grpc|
|5656|データベースエンジン|

### ポートマッピング（転送） {#포트-매핑포워딩}

```sh
$ docker run -d -p <host port>:<container port>/<protocol> machbase/machbase-neo
```

- `-p`, `--publish`: コンテナのポートをホストに公開します。
- `<host port>`: ホストマシンのポートです。
- `<container port>`: コンテナのポートです。
- `<protocol>`: tcp、udp、sctpなどを指定します。

machbase-neoコンテナを実行するときに、以下のようにホストポートをコンテナポートにマッピングできます。

__例__

```sh
$ docker run -d                           \
             -p 5652-5656:5652-5656/tcp   \
             --name machbase-neo          \
             machbase/machbase-neo
```

この構成では、ホストポートに届いたすべてのリクエストがコンテナポートに転送されます。

### SSHキーによるmachbase-neoシェルへのリモート接続 {#ssh-키를-이용한-machbase-neo-셸-원격-접속}

machbase-neoシェルに接続する前に、SSHキーを生成します。

```sh
$ ssh-keygen -t rsa
```

SSHキーを作成したら、別の環境でmachbase-neoを起動します。

```sh
$ docker pull machbase/machbase-neo
$ docker run -d
             -p 5652-5656:5652-5656/tcp
             --name machbase-neo
             machbase/machbase-neo
```

既定では、SSH接続のたびにパスワードの入力が必要です。machbase-neoシェルにキーを登録すると、パスワードの入力を初回だけにできます。

```sh
$ ssh -l sys -p 5652 192.168.0.116 ssh-key add `cat ~/.ssh/id_rsa.pub`
sys@192.168.0.116's password? manager
Add sshkey success
```

この設定により、接続のたびにパスワードを入力する必要がなくなります。

__例__

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

### Docker Composeの使用 {#docker-compose-사용}

以下の内容を`docker-compose.yml`に保存し、プロジェクトのルートディレクトリに配置します。

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

次に、プロジェクトのルートディレクトリで以下のコマンドを実行します。

```sh
$ docker compose up -d
```

以下のように実行することもできます。

```sh
$ docker compose -f docker-compose.yml up -d
```

Docker Composeを停止するには、次のコマンドを使用します。

```sh
$ docker compose down
```

すべてのサービスが正常に停止します。
