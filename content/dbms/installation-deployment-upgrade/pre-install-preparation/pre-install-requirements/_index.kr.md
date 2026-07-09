---
type: docs
title: '설치 전 요구사항'
weight: 10
toc: true
---

## 지원 운영체제

| OS | 버전 |
|----|------|
| RHEL / CentOS | 7 이상 |
| Ubuntu | 18.04 LTS 이상 |
| Windows | 10, Server 2019 이상 |

운영체제 아키텍처는 설치할 Machbase 패키지의 비트 수와 일치해야 합니다.

## 하드웨어 최소 요구사항

| 항목 | 최솟값 | 권장값 |
|------|--------|--------|
| CPU | 2코어 | 8코어 이상 |
| RAM | 4 GB | 32 GB 이상 |
| 디스크 | 20 GB (설치 공간) | SSD, 데이터 크기의 2배 이상 |
| 네트워크 | 100 Mbps | 1 Gbps 이상 (Cluster Edition) |

시계열 데이터는 지속적으로 적재되므로 디스크 여유 공간을 넉넉하게 확보하십시오. 데이터 보존 정책(Retention Policy)을 함께 설계하면 디스크 관리 부담을 줄일 수 있습니다.

## 기본 포트

| 포트 | 용도 |
|------|------|
| **5656** | SQL 클라이언트 접속 (Native TCP) |
| **5657** | HTTP REST API |

SQL 클라이언트 포트를 변경하려면 `$MACHBASE_HOME/conf/machbase.conf`의 `PORT_NO` 항목을
수정합니다. 환경 변수 `MACHBASE_PORT_NO`를 설정해도 동일하게 적용됩니다. HTTP REST API 포트는
`HTTP_PORT_NO` 또는 환경 변수 `MACHBASE_HTTP_PORT_NO`로 변경합니다.

방화벽이 있는 환경에서는 위 포트를 인바운드 허용으로 열어야 합니다. Cluster Edition은 Coordinator
link/admin 포트와 Broker, Warehouse, Deployer 포트도 추가로 열어야 합니다.

## 시스템 커널 파라미터 (Linux)

Linux에 설치할 경우 아래 항목을 설치 전에 점검합니다.

### 파일 디스크립터 한도

Machbase는 다수의 파일을 동시에 열기 때문에 기본값(1024)으로는 부족합니다.

```bash
# 현재 값 확인
ulimit -Sn
```

값이 65535보다 작으면 `/etc/security/limits.conf`를 수정하고 재부팅합니다.

```
*  hard  nofile  65535
*  soft  nofile  65535
```

재부팅 후 값을 다시 확인합니다.

```bash
ulimit -Sn
# 출력: 65535
```

### 포트 예약

운영체제가 Machbase 포트를 다른 프로세스에 할당하는 것을 방지하려면 포트를 예약합니다.

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

## 시간 동기화

Machbase는 시계열 데이터를 처리하므로 서버의 시간이 정확해야 합니다. NTP 또는 `chrony`로 시스템 시간을 동기화하십시오. Cluster Edition에서는 모든 노드의 시간을 일치시켜야 합니다.

```bash
# 타임존 확인
ls -l /etc/localtime
date
```

---

**다음 읽을 내용**
- [패키지 구성 이해](/kr/dbms/installation-deployment-upgrade/pre-install-preparation/package/)
