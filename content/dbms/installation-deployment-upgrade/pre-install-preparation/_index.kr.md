---
type: docs
title: '3.1 설치 전 준비'
weight: 10
toc: true
---
설치를 시작하기 전에 시스템 요구사항을 확인하고 필요한 환경을 갖춰야 합니다. 사전 준비가 부족하면 설치 후 예기치 않은 오류나 성능 저하가 발생할 수 있습니다.

## 이 섹션에서 다루는 내용

| 항목 | 설명 |
|------|------|
| [설치 전 요구사항](/kr/dbms/installation-deployment-upgrade/pre-install-preparation/pre-install-requirements/) | OS 버전, 하드웨어 최소 사양, 네트워크 포트 |
| [패키지 구성 이해](/kr/dbms/installation-deployment-upgrade/pre-install-preparation/package/) | 패키지 파일 명명 규칙, 디렉터리 구조, 주요 실행 파일 |
| [라이선스 설치](/kr/dbms/installation-deployment-upgrade/pre-install-preparation/license/) | license.dat 파일 배치 방법, 라이선스 상태 확인 방법 |

---

**다음 읽을 내용**
- [설치 전 요구사항](/kr/dbms/installation-deployment-upgrade/pre-install-preparation/pre-install-requirements/)


<a id="pre-install-requirements"></a>

## 설치 전 요구사항

### 지원 운영체제

| OS | 버전 |
|----|------|
| RHEL / CentOS | 7 이상 |
| Ubuntu | 18.04 LTS 이상 |
| Windows | 10, Server 2019 이상 |

운영체제 아키텍처는 설치할 Machbase 패키지의 비트 수와 일치해야 합니다.

### 하드웨어 최소 요구사항

| 항목 | 최솟값 | 권장값 |
|------|--------|--------|
| CPU | 2코어 | 8코어 이상 |
| RAM | 4 GB | 32 GB 이상 |
| 디스크 | 20 GB (설치 공간) | SSD, 데이터 크기의 2배 이상 |
| 네트워크 | 100 Mbps | 1 Gbps 이상 (Cluster Edition) |

시계열 데이터는 지속적으로 적재되므로 디스크 여유 공간을 넉넉하게 확보하십시오. 데이터 보존 정책(Retention Policy)을 함께 설계하면 디스크 관리 부담을 줄일 수 있습니다.

### 기본 포트

| 포트 | 용도 |
|------|------|
| **5656** | SQL 클라이언트 접속 (Native TCP) |
| **5657** | HTTP REST API |

SQL 클라이언트 포트를 변경하려면 `$MACHBASE_HOME/conf/machbase.conf`의 `PORT_NO` 항목을
수정합니다. 환경 변수 `MACHBASE_PORT_NO`를 설정해도 동일하게 적용됩니다. HTTP REST API 포트는
`HTTP_PORT_NO` 또는 환경 변수 `MACHBASE_HTTP_PORT_NO`로 변경합니다.

방화벽이 있는 환경에서는 위 포트를 인바운드 허용으로 열어야 합니다. Cluster Edition은 Coordinator
link/admin 포트와 Broker, Warehouse, Deployer 포트도 추가로 열어야 합니다.

### 시스템 커널 파라미터 (Linux)

Linux에 설치할 경우 아래 항목을 설치 전에 점검합니다.

#### 파일 디스크립터 한도

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

#### 포트 예약

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

### 시간 동기화

Machbase는 시계열 데이터를 처리하므로 서버의 시간이 정확해야 합니다. NTP 또는 `chrony`로 시스템 시간을 동기화하십시오. Cluster Edition에서는 모든 노드의 시간을 일치시켜야 합니다.

```bash
# 타임존 확인
ls -l /etc/localtime
date
```

---

**다음 읽을 내용**
- [패키지 구성 이해](/kr/dbms/installation-deployment-upgrade/pre-install-preparation/package/)

<a id="package"></a>

## 패키지 구성 이해

### 패키지 파일 명명 규칙

Machbase 패키지 파일 이름은 에디션에 따라 다음 형식을 따릅니다.

```
machbase-EDITION-VERSION-OS-CPU-BIT-MODE.EXT
```

| 항목 | 설명 | 예시 |
|------|------|------|
| EDITION | 에디션 구분 | `SDK`, `cluster` |
| VERSION | 버전 (Major.Minor.Fix.AUX) | `8.6.0.official` |
| OS | 운영체제 | `LINUX`, `WINDOWS` |
| CPU | CPU 아키텍처 | `X86` |
| BIT | 아키텍처 비트 수 | `64` |
| MODE | 빌드 모드 | `release` |
| EXT | 확장자 | `tgz` (Linux), `zip` 또는 설치 실행 파일 (Windows) |

Standard Edition Linux tarball은 `machbase-SDK-...tgz` 이름으로 생성됩니다.

예시:
- Standard Edition: `machbase-SDK-8.6.0.official-LINUX-X86-64-release.tgz`
- Cluster Edition: `machbase-cluster-8.6.0.official-LINUX-X86-64-release.tgz`

버전에서 Minor 버전이 다른 경우 DB 파일 및 프로토콜 호환이 보장되지 않습니다. Fix 버전 변경은 호환성이 유지됩니다.

### 설치 디렉터리 구조

tarball 압축을 해제하면 `$MACHBASE_HOME` 아래에 다음 구조가 생성됩니다.

```
$MACHBASE_HOME/
├── bin/        실행 파일
├── conf/       설정 파일 (machbase.conf 등)
├── dbs/        데이터 저장 공간
├── doc/        라이선스 문서
├── http/       HTTP REST API 및 웹 리소스
├── include/    C/C++ 헤더 파일
├── install/    Makefile용 mk 파일
├── lib/        공유 라이브러리
├── package/    Cluster Edition 추가 패키지 경로
├── sample/     예제 파일
├── trc/        서버 로그 및 트레이스 파일
├── tutorials/  튜토리얼
├── utility/    유틸리티 파일
└── 3rd-party/  Grafana 플러그인 등
```

### 주요 실행 파일

| 실행 파일 | 설명 |
|-----------|------|
| `machbased` | 서버 데몬 |
| `machadmin` | 서버 관리 (시작·종료·DB 생성) |
| `machsql` | CLI 쿼리 도구 |
| `machloader` | 대용량 파일 적재·추출 도구 |
| `csvimport` | CSV 파일 가져오기 |
| `csvexport` | CSV 파일 내보내기 |
| `tagmetaimport` | TAG 메타 데이터 일괄 등록 |

Cluster Edition 패키지에는 `machcoordinatoradmin`, `machdeployeradmin` 등의 관리 도구가 추가됩니다.
`machclusterctl`은 해당 도구를 포함하도록 빌드된 패키지에서 사용할 수 있습니다.

### 설정 파일

`$MACHBASE_HOME/conf/` 아래에 에디션별 샘플 설정 파일이 있습니다.

```bash
ls $MACHBASE_HOME/conf/
# machbase.conf
# machbase.conf.sample.standard
# machbase.conf.sample.edge
# machloader.conf.sample
```

실제 사용 파일은 `machbase.conf`입니다. Standard full 패키지는 빌드 과정에서
`machbase.conf.sample.standard`를 복사해 `machbase.conf`를 포함합니다. 실제 파일이 없는
패키지에서는 에디션에 맞는 샘플 파일을 복사하여 수정합니다.

RDB 테이블 기능이 포함된 빌드의 Standard/Edge 샘플에는 RDB 테이블 sidecar 파일 동작을 제어하는
`RDB_BUSY_TIMEOUT_MS`, `RDB_SYNCHRONOUS`, `RDB_JOURNAL_MODE` 설정이 포함될 수 있습니다. 해당
항목이 없는 패키지에서는 추가하지 말고, RDB 테이블을 사용하는 환경에서만 기본값과 운영 중 busy
timeout 또는 SQLite 동기화 정책 조정 필요성을 검토합니다.

---

**다음 읽을 내용**
- [라이선스 설치](/kr/dbms/installation-deployment-upgrade/pre-install-preparation/license/)

<a id="license"></a>

## 라이선스 설치

라이선스 설치는 Machbase 설치 완료 후 수행합니다. 라이선스 파일이 없어도 서버는 기본
`COMMUNITY` 라이선스 정보로 구동됩니다.

### 라이선스 상태와 제한 확인

라이선스 상태는 다음 기준으로 확인합니다.

1. **태그 수와 저장 용량 제한**: 설치된 라이선스에 설정된 최대 태그 수나 저장 용량을 초과하면
   라이선스 위반 상태가 기록됩니다. `V$LICENSE_INFO`의 `VIOLATE_STATUS`와 `VIOLATE_MSG`로
   현재 상태를 확인합니다.

Append 건수나 테이블스페이스 디스크 경로 개수를 기준으로 한 제한은 8.6.0 소스에서 확인되는
라이선스 위반 조건이 아닙니다.

### 라이선스 파일 구조

발급받은 라이선스는 `license.dat` 텍스트 파일 형식입니다.

```
#License ID: 00000001
#Issue DATE: 20991231
#License Type(Version 3): FOGUNLIMITED
#Company: MACHBASE
#Project(Product): NONE
#Country Code: KR
dXlIm7cdJjV1eUibtx0mNQ...
```

### 설치 방법

#### 방법 1: 파일 복사 (서버 시작 전)

`license.dat` 파일을 `$MACHBASE_HOME/conf/`에 복사합니다. 서버가 시작될 때 자동으로 인식합니다.

```bash
cp license.dat $MACHBASE_HOME/conf/license.dat
```

#### 방법 2: machadmin 명령

`machadmin`으로 라이선스 파일을 검증하고 설치합니다. 서버가 실행 중이면 라이선스 reload 요청을
함께 보냅니다.

```bash
machadmin -t /path/to/license.dat
```

#### 방법 3: SQL 쿼리 (서버 실행 중)

서버가 이미 실행 중인 경우 machsql에서 쿼리로 설치할 수 있습니다.

```sql
ALTER SYSTEM INSTALL LICENSE = '/path/to/license.dat';
```

### 설치 확인

#### 서버 로그 확인

서버 시작 후 `$MACHBASE_HOME/trc/machbase.trc`에서 라이선스 정보가 출력되면 정상 설치된 것입니다.

```
[INFO] LICENSE [License ID] [00000001]
[INFO] LICENSE [Issue DATE] [20991231]
[INFO] LICENSE [License Type(Version 3)] [FOGUNLIMITED]
[INFO] LICENSE [Company] [MACHBASE]
```

#### machadmin 확인

```bash
machadmin -f
```

#### V$LICENSE_INFO 뷰 조회

```sql
SELECT ID, ISSUE_DATE, TYPE, CUSTOMER, VIOLATE_STATUS, VIOLATE_MSG
FROM V$LICENSE_INFO;
```

`VIOLATE_STATUS`가 0이면 정상입니다.

machsql에서는 다음 명령으로도 라이선스 정보를 확인할 수 있습니다.

```sql
SHOW LICENSE;
```

---

**다음 읽을 내용**
- [Standard Edition 설치](/kr/dbms/installation-deployment-upgrade/standard-edition/)
- [Cluster Edition 설치](/kr/dbms/installation-deployment-upgrade/cluster-edition/)
