---
title : "Linux 환경 설치 준비"
type : docs
weight: 10
---


## 파일 최대 개수 확인 및 설정

1. 리눅스 파일 최대 개수를 아래 명령어로 확인한다.

```bash
[machbase@localhost ~] ulimit -Sn
1024
```

2. 결과값이 65535보다 작다면, limit.conf 와 user.conf 를 아래와 같이 수정하고 서버를 재시작 한다.

```bash
[machbase@localhost ~] sudo vi /etc/security/limits.conf
 
 
#<domain>      <type>  <item>         <value>
#
 
*               hard    nofile          65535
*               soft    nofile          65535
 
 
[machbase@localhost ~] sudo vi /etc/systemd/user.conf
 
DefaultLimitNOFILE=65535
```

3. 서버를 재시작하고 다시 값을 확인한다.

```bash
[machbase@localhost ~] ulimit -Sn
65535
```


## 서버의 시간 확인 및 설정

Machbase는 시계열 데이터를 다루는 데이터베이스이므로 Machbase가 설치될 서버의 시간 값을 정확하게 설정해야 한다.

### 타임존 설정하기

Machbase는 모든 데이터를 해당 서버가 위치한 곳의 지역 시간을 이용하기 때문에 현재 서버의 시간과 Timezone이 맞는지 꼭 확인해야 한다.

아래 명령어로 자신이 위치한 Timezone과 맞는지 확인한다. 만약 다르다면, /usr/share/zoneinfo 에서 맞는 지역을 선택하여 링크한다.

```bash
[machbase@localhost ~] ls -l /etc/localtime
lrwxrwxrwx 1 root root 32 Sep 27 14:08 /etc/localtime -> ../usr/share/zoneinfo/Asia/Seoul
 
 
## date 명령어를 통해 설정된 Timezone을 확인할 수 있다.
[machbase@localhost ~] date
Wed Jan  2 11:12:44 KST 2019
```

### 시간 설정하기

만약 현재의 지역 시간이 맞지 않다면 다음 명령을 통해 시간을 재설정한다.

```bash
[machbase@localhost ~] sudo date -s '2018/12/25 12:34:56'
```


## 포트 설정

Machbase가 사용할 운영체제 포트는 다른 프로그램에서 사용이 안되도록 포트 예약을 사용해야 한다.

아래 명령어로 예약 포트를 설정하면 운영체제가 다른 프로그램에 해당 포트를 할당하지 않게 되어 포트 충돌 문제를 피할 수 있다.

```bash
[machbase@localhost ~] sudo echo 예약포트범위~에약포트범위 > /proc/sys/net/ipv4/ip_local_reserved_ports
```

위 방법은 일시적인 방법으로 영구적으로 설정하려면 /etc/sysctl.conf 파일을 수정해야 한다.

```bash
[machbase@localhost ~] sudo vim /etc/sysctl.conf

## 해당 내용 추가
net.ipv4.ip_local_reserved_ports = 예약포트범위-예약포트범위```
```
