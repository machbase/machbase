---
type: docs
title: 'Linux 환경 준비'
weight: 10
toc: true
---

Machbase를 Linux에 설치하기 전에 파일 디스크립터 한도, 시간 설정, 포트 예약을 확인하고 조정합니다.

## 파일 디스크립터 한도

Machbase는 내부적으로 많은 수의 파일을 동시에 열기 때문에 OS 기본값(1024)으로는 부족합니다.

```bash
# 현재 soft limit 확인
ulimit -Sn
```

출력값이 65535보다 작으면 다음을 수행합니다.

```bash
sudo vi /etc/security/limits.conf
```

아래 내용을 추가합니다.

```
*  hard  nofile  65535
*  soft  nofile  65535
```

systemd 환경에서는 추가로 아래 파일도 수정합니다.

```bash
sudo vi /etc/systemd/user.conf
# 추가:
DefaultLimitNOFILE=65535
```

수정 후 서버를 재부팅하고 값을 확인합니다.

```bash
ulimit -Sn
# 65535
```

## 서버 시간 확인

Machbase는 시계열 데이터를 처리하므로 서버 시간이 정확해야 합니다.

```bash
# 타임존 확인
ls -l /etc/localtime
# 예: /etc/localtime -> ../usr/share/zoneinfo/Asia/Seoul

date
# Wed Jan  2 11:12:44 KST 2019
```

타임존이 올바르지 않으면 `/usr/share/zoneinfo`에서 적절한 지역을 선택해 심볼릭 링크를 변경합니다.

시간 자체가 맞지 않으면 수동으로 설정합니다.

```bash
sudo date -s '2025/01/02 12:34:56'
```

## 포트 예약

운영체제가 Machbase 포트를 다른 프로세스에 할당하지 못하도록 예약합니다.

```bash
current=$(cat /proc/sys/net/ipv4/ip_local_reserved_ports)
ports=5656-5657
sudo sysctl -w net.ipv4.ip_local_reserved_ports="${current:+$current,}$ports"
```

기존 예약 포트가 있으면 덮어쓰지 말고 쉼표로 구분해 병합합니다. 영구 적용은
`/etc/sysctl.conf`의 `net.ipv4.ip_local_reserved_ports` 항목을 다음 값과 병합합니다.

```
net.ipv4.ip_local_reserved_ports = 5656-5657
```

Cluster Edition의 경우 클러스터 링크 포트, 어드민 포트, 복제 포트도 범위에 포함하십시오.

## 방화벽 포트 오픈

외부에서 접속이 필요한 경우 포트를 허용합니다.

```bash
# firewalld 사용 환경
sudo firewall-cmd --permanent --add-port=5656/tcp
sudo firewall-cmd --permanent --add-port=5657/tcp
sudo firewall-cmd --reload

# iptables 사용 환경
sudo iptables -A INPUT -p tcp --dport 5656 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 5657 -j ACCEPT
```

---

**다음 읽을 내용**
- [Tarball 설치](/dbms/installation-deployment-upgrade/standard-edition/linux/tarball/)
- [Docker 설치](/dbms/installation-deployment-upgrade/standard-edition/linux/docker/)
