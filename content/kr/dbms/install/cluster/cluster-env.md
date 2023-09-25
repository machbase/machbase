---
title : "Cluster Edition 설치 준비"
type: docs
weight: 10
---

## 파일 LIMIT 확인 및 변경

열 수 있는 최대 파일 개수를 늘려야 하므로, 아래와 같이 수행한다.

1. /etc/security/limits.conf 파일을 아래와 같이 수정한다.

   ```bash
    sudo vi /etc/security/limits.conf
    *       hard   nofile      65535
    *       soft   nofile      65535
   ```

2. 재부팅 한다.

    ```bash
    sudo reboot
    # 또는
    sudo shutdown -r now
    ```

3. 아래 명령어를 실행하여 결과를 확인한다. 65535 가 출력되면 성공적으로 변경된 것이다.

    ```bash
    ulimit -Sn
    ```
## 서버 시간 동기화

각 Host 간 서버 시간을 동기화해야 한다. 이미 동기화를 하고 있다면 확인 차원에서 점검하도록 하자.

1. 모든 서버의 시간을 time 서버와 동기화한다. 

    ```bash
    # 다음 명령어로 동기화한다.                               
    /usr/bin/rdate -s time.bora.net && /sbin/clock -w
    ```

2. Time 서버를 활용할 수 없는 경우 직접 명령어로 수정한다.

    ```bash
    # 다음 명령어로 수정한다.                                
    date -s "2017-10-31 11:15:30"
    ```

3. 변경된 시간을 확인한다

    ```bash
    # 다음 명령어로 확인한다.                                 
    date
    ```

## 네트워크 커널 파라미터 변경

1. 현재 설정된 값을 확인한다.

    ```bash
    # 다음 명령어로 확인한다.                                 
    sysctl -a | egrep 'mem_(max|default)|tcp_.*mem'
    ```
2. 아래 명령어로 설정값을 변경한다.(64GB Memory 기준)

    ```bash
    sysctl -w net.core.rmem_default = "33554432"     # 32MB
    sysctl -w net.core.wmem_default = "33554432"
    sysctl -w net.core.rmem_max     = "268435456"    # 256MB
    sysctl -w net.core.wmem_max     = "268435456"    # 최소 256KB 기본 32MB 최대 256MB
    sysctl -w net.ipv4.tcp_rmem     = "262144 33554432 268435456"
    sysctl -w net.ipv4.tcp_wmem     = "262144 33554432 268435456"
    
    # 8388608 Page * 4KB = 32GB (가용 메모리에 따라 변경 필요)
    sysctl -w net.ipv4.tcp_mem      = "8388608 8388608 8388608"
    ```

3. 변경값을 유지하려면 /etc/sysctl.conf 파일에 추가하고 호스트 OS 를 재시작한다.

    ```bash
    # /etc/sysctl.conf 파일 수정한다.
    net.core.rmem_default = "33554432"
    net.core.wmem_default = "33554432"
    net.core.rmem_max     = "268435456"
    net.core.wmem_max     = "268435456"
    net.ipv4.tcp_rmem     = "262144 33554432 268435456"
    net.ipv4.tcp_wmem     = "262144 33554432 268435456"
    net.ipv4.tcp_mem      = "8388608 8388608 8388608"
    ```

## 사용자 생성

1. Machbase 설치를 위한 리눅스 OS 사용자 machbase를 생성한다.  
   사용자 계정 디렉토리는 /home/machbase 로 생성되도록 한다.  

    ```bash
    # 다음 명령어로 사용자 "machbase"를 추가한다.
    $ sudo useradd machbase --home-dir "/home/machbase"
    ```

2. 사용자 "machbase"의 비밀번호를 설정한다.  

    ```bash
    sudo passwd machbase
    ```
