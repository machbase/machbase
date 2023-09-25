---
title : "Docker 설치"
type : docs
weight: 30
---


마크베이스는 Docker 이미지를 제공한다.  Docker가 이미 설치되어 있다고 가정하고 마크베이스를 Docker로 설치하는 과정을 설명한다.

Docker 설치는 [Docker 설치 페이지](https://docs.docker.com/compose/install)를 참조하여 진행한다. 마크베이스의 Docker Hub는 [이 페이지](https://hub.docker.com/r/machbase/machbase)를 참고한다.

```bash
$ docker pull machbase/machbase
Using default tag: latest
latest: Pulling from machbase/machbase
3a291d7fe8d1: Pull complete
f1e7bd0ef2d1: Pull complete
78632f9cbb53: Pull complete
f4f6c5358244: Pull complete
a3e04b27f9cd: Pull complete
a3ed95caeb02: Pull complete
e03e135c0eda: Pull complete
26612cd7ebc1: Pull complete
b61e71cf4bc2: Pull complete
09c9c411b936: Pull complete
2b1cdec8c664: Pull complete
fd9a9a288691: Pull complete
d8852dedc8a1: Pull complete
cba7e30dbb6f: Pull complete
c7ead0fa7c49: Pull complete
6af02fe4c01f: Pull complete
d18db958464f: Pull complete
1fb93627ec0f: Pull complete
265b8b73294a: Pull complete
f122e6396b46: Pull complete
3b2f248fb414: Pull complete
07ed5a8f0935: Pull complete
44ec57c5ed31: Pull complete
59383e5f4c61: Pull complete
542101ec7002: Pull complete
```

```bash
# 설치된 마크베이스 이미지를 확인한다.
$ docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
machbase/machbase   latest              dfb90844e7da        2 months ago        1.09 GB
Digest: sha256:aa6a982d35946b3fb33930de91cad61bfe7d3e9a559080526ed8e9a511c82c2b
Status: Downloaded newer image for machbase/machbase:latest
```

```bash
# 마크베이스 이미지를 실행한다.
$ docker run -it machbase/machbase
-----------------------------------------------------------------
     Machbase Administration Tool
     Release Version - x.x.x.community
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-----------------------------------------------------------------
Database created successfully.
-----------------------------------------------------------------
     Machbase Administration Tool
     Release Version - x.x.x.community
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-----------------------------------------------------------------
Waiting for Machbase server start.
Machbase server started successfully.
SERVER HAS BEEN RESET
SERVER STARTED, PID : 56
     Connection URL : http://172.17.0.2:5001
machbase@5ba45a22d140:~$
```
