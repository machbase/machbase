---
title : '설치를 위한 리눅스 환경 준비'
type : docs
weight: 10
---

## 파일 최대 개수 확인 및 설정
1. 다음 명령으로 현재 리눅스에서 허용하는 최대 파일 오픈 수를 확인합니다.

```bash
[machbase@localhost ~] ulimit -Sn
1024
```

2. 결과 값이 65535보다 작으면 아래 파일을 수정한 뒤 서버를 재부팅합니다.

```bash
[machbase@localhost ~] sudo vi /etc/security/limits.conf


#<domain>      <type>  <item>         <value>
#

*               hard    nofile          65535
*               soft    nofile          65535


[machbase@localhost ~] sudo vi /etc/systemd/user.conf

DefaultLimitNOFILE=65535
```

3. 서버를 재부팅한 뒤 값을 다시 확인합니다.

```bash
[machbase@localhost ~] ulimit -Sn
65535
```

## 서버 시간 확인 및 설정

Machbase는 시계열 데이터를 처리하므로 설치 대상 서버의 시간이 정확해야 합니다.

### 시간대 설정

Machbase는 서버가 위치한 로컬 시간을 그대로 사용하므로, 현재 서버 시간이 실제 지역 시간과 일치하는지 확인해야 합니다. 아래 명령으로 타임존을 확인하고, 다를 경우 `/usr/share/zoneinfo`에서 올바른 지역을 선택해 링크합니다.

```bash

[machbase@localhost ~] ls -l /etc/localtime
lrwxrwxrwx 1 root root 32 Sep 27 14:08 /etc/localtime -> ../usr/share/zoneinfo/Asia/Seoul


# date 명령으로 설정된 타임존을 확인할 수 있습니다.
[machbase@localhost ~] date
Wed Jan  2 11:12:44 KST 2019
```

### 시간 설정

현재 로컬 시간이 맞지 않다면 다음 명령으로 시간을 재설정합니다.

```bash
[machbase@localhost ~] sudo date -s '2018/12/25 12:34:56'
```

## 포트 설정

Machbase가 사용할 운영체제 포트는 다른 프로그램이 사용하지 못하도록 예약해야 합니다.

아래 명령으로 예약 포트를 지정하면 운영체제가 해당 포트를 다른 프로그램에 할당하지 않아 포트 충돌을 예방할 수 있습니다.

```bash
[machbase@localhost ~] sudo echo reserved port range~reserved port range > /proc/sys/net/ipv4/ip_local_reserved_ports
```

위 방법은 일시적인 설정입니다. 영구적으로 적용하려면 `/etc/sysctl.conf` 파일을 수정합니다.

```bash
[machbase@localhost ~] sudo vim /etc/sysctl.conf

# 아래 내용을 추가합니다.
net.ipv4.ip_local_reserved_ports = reserved port range-reserved port range
```
