---
title : 'Cluster Edition 설치 환경 준비'
type: docs
weight: 10
---

## 파일 LIMIT 확인 및 변경

열 수 있는 파일의 최대 개수를 늘리려면 다음과 같이 수행합니다.

1. /etc/security/limits.conf 파일을 수정합니다.

```bash
sudo vi /etc/security/limits.conf
*       hard   nofile      65535
*       soft   nofile      65535
```

2. 재부팅합니다.

```bash
sudo reboot
# 또는
sudo shutdown -r now
```

3. 결과를 확인합니다. 출력값이 65535이면 성공적으로 변경된 것입니다.

```bash
unlimit -Sn
```


## 서버 시간 동기화

각 호스트 간의 서버 시간을 동기화해야 합니다. 이미 동기화된 경우 확인을 위해 점검합니다.

1. 모든 서버의 시간을 타임 서버와 동기화합니다.

```bash
# 다음 명령으로 동기화합니다.
/usr/bin/rdate -s time.bora.net && /sbin/clock -w
```

2. 타임 서버를 사용할 수 없는 경우 직접 명령으로 수정합니다.

```bash
# 다음 명령으로 수정합니다.
date -s "2017-10-31 11:15:30"
```

3. 수정된 시간을 확인합니다.

```bash
# 다음 명령으로 확인합니다.
date
```


## 네트워크 커널 파라미터 변경

1. 현재 설정값을 확인합니다.

```bash
다음 명령으로 확인합니다.
sysctl -a | egrep 'mem_(max|default)|tcp_.*mem'
```

2. 다음 명령으로 설정값을 변경합니다 (64GB 메모리 기준).

```bash
sysctl -w net.core.rmem_default = "33554432"     # 32MB
sysctl -w net.core.wmem_default = "33554432"
sysctl -w net.core.rmem_max     = "268435456"    # 256MB
sysctl -w net.core.wmem_max     = "268435456"
sysctl -w net.ipv4.tcp_rmem     = "262144 33554432 268435456"
sysctl -w net.ipv4.tcp_wmem     = "262144 33554432 268435456"

# 8388608 페이지 * 4KB = 32GB
sysctl -w net.ipv4.tcp_mem      = "8388608 8388608 8388608"
```

3. 변경 사항을 유지하려면 /etc/sysctl.conf 파일에 추가하고 호스트 OS를 재시작합니다.

```bash
# /etc/sysctl.conf 파일을 수정합니다.
net.core.rmem_default = "33554432"
net.core.wmem_default = "33554432"
net.core.rmem_max     = "268435456"
net.core.wmem_max     = "268435456"
net.ipv4.tcp_rmem     = "262144 33554432 268435456"
net.ipv4.tcp_wmem     = "262144 33554432 268435456"
net.ipv4.tcp_mem      = "8388608 8388608 8388608"
```

## 사용자 생성

1. Machbase 설치를 위한 Linux OS 사용자 'machbase'를 생성합니다. 사용자 계정 디렉토리는 /home/machbase로 생성됩니다.

```bash
$ sudo useradd machbase --home-dir "/home/machbase"
```

2. 비밀번호 설정 (machbase)

```bash
sudo passwd machbase
```
