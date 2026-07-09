---
type: docs
title: 'Cluster Edition 설치 환경 준비'
weight: 20
toc: true
---

Cluster Edition을 배포하기 전에 모든 노드에 다음 환경을 준비해야 합니다.

## 파일 디스크립터 한도

모든 노드에서 아래 설정을 적용합니다.

```bash
sudo vi /etc/security/limits.conf
```

```
*  hard  nofile  65535
*  soft  nofile  65535
```

재부팅 후 확인합니다.

```bash
ulimit -Sn
# 65535
```

## OS 사용자 생성

모든 노드에 `machbase` 계정을 생성합니다.

```bash
sudo useradd machbase --home-dir /home/machbase
sudo passwd machbase
```

## SSH 키 기반 인증

`machclusterctl`을 사용하는 경우, 배포 서버에서 모든 노드로 비밀번호 없이 SSH 접속이 가능해야 합니다.

```bash
# 배포 서버에서 SSH 키 생성 (이미 있으면 생략)
ssh-keygen -t rsa -b 4096

# 각 노드에 공개 키 등록
ssh-copy-id machbase@<node-ip>
```

등록 후 비밀번호 없이 접속이 되는지 확인합니다.

```bash
ssh machbase@<node-ip> 'hostname'
```

## 네트워크 커널 파라미터

대용량 데이터 전송 성능을 위해 네트워크 버퍼를 늘립니다. 64 GB 메모리 기준 권장값입니다.

```bash
sudo sysctl -w net.core.rmem_default=33554432
sudo sysctl -w net.core.wmem_default=33554432
sudo sysctl -w net.core.rmem_max=268435456
sudo sysctl -w net.core.wmem_max=268435456
sudo sysctl -w 'net.ipv4.tcp_rmem=262144 33554432 268435456'
sudo sysctl -w 'net.ipv4.tcp_wmem=262144 33554432 268435456'
sudo sysctl -w 'net.ipv4.tcp_mem=8388608 8388608 8388608'
```

영구 적용은 `/etc/sysctl.conf`에 추가합니다.

## 시간 동기화 (NTP)

모든 노드의 시스템 시간이 일치해야 합니다. NTP 또는 `chrony`로 동기화하십시오.

```bash
# chrony 사용 예
sudo systemctl enable chronyd
sudo systemctl start chronyd
chronyc tracking
```

타임 서버를 사용할 수 없는 경우 직접 설정합니다.

```bash
sudo date -s "2025-01-02 12:34:56"
```

## 포트 예약

각 노드에서 Machbase가 사용할 포트를 예약합니다.

```bash
echo 5101-5110,5656-5657 | sudo tee /proc/sys/net/ipv4/ip_local_reserved_ports
```

클러스터 구성에 따라 포트 범위를 조정하십시오. Coordinator link, admin, 복제 포트 등을 모두 포함해야 합니다.

---

**다음 읽을 내용**
- [machclusterctl 기반 배포](/dbms/installation-deployment-upgrade/cluster-edition/machclusterctl/)
