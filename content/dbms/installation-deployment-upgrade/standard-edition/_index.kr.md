---
type: docs
title: '3.2 Standard Edition 설치'
weight: 20
toc: true
---
Standard Edition은 단일 노드에 설치하는 구성으로, 개발 환경, 소규모 운영, 엣지 디바이스 등에 적합합니다.

## 설치 경로

운영체제에 따라 아래 경로 중 하나를 선택합니다.

| OS | 설치 방식 | 링크 |
|----|-----------|------|
| Linux | Tarball (.tgz) | [Tarball 설치](/dbms/installation-deployment-upgrade/standard-edition/#linux-tarball) |
| Linux | Docker 컨테이너 | [Docker 설치](/dbms/installation-deployment-upgrade/standard-edition/#linux-docker) |
| Windows | ZIP 또는 설치 실행 파일 | [Windows 패키지 설치](/dbms/installation-deployment-upgrade/standard-edition/#windows-package) |

설치 전에 [Linux 환경 준비](/dbms/installation-deployment-upgrade/standard-edition/#linux-preparation-environment-linux) 또는 [Windows 환경 준비](/dbms/installation-deployment-upgrade/standard-edition/#windows-preparation-environment-windows)를 먼저 확인하십시오.

---

<a id="linux"></a>

## Linux 설치

Linux에서 Standard Edition을 설치하는 방법은 두 가지입니다.

| 방식 | 적합한 상황 |
|------|------------|
| [Tarball 설치](/dbms/installation-deployment-upgrade/standard-edition/#linux-tarball) | 실제 서버 환경, 데이터 디렉터리를 직접 관리해야 하는 경우 |
| [Docker 설치](/dbms/installation-deployment-upgrade/standard-edition/#linux-docker) | 개발·테스트 환경, 빠른 구동이 필요한 경우 |

Tarball 설치는 [설치 전 준비](../pre-install-preparation/)를 먼저 완료해야 합니다. Docker
설치는 Docker Engine과 볼륨·포트 권한을 준비하십시오.

---

<a id="linux-preparation-environment-linux"></a>

### Linux 환경 준비

파일 디스크립터 한도, 시간 동기화, 포트 예약과 방화벽 설정은 Edition 공통 작업입니다.
중복된 설정을 이 페이지에서 반복하지 않고 [설치 전 준비](../pre-install-preparation/)를
기준으로 안내합니다.

---

<a id="linux-tarball"></a>

### Tarball 설치

Linux 환경에 tarball(.tgz)을 압축 해제하여 Standard Edition을 설치하는 절차입니다.

#### 1. 사용자 생성

Machbase 전용 OS 사용자를 생성합니다.

```bash
sudo useradd machbase
sudo passwd machbase
```

이후 `machbase` 계정으로 로그인하여 작업합니다.

#### 2. 패키지 다운로드 및 압축 해제

설치 디렉터리를 만들고 패키지를 압축 해제합니다.

```bash
mkdir ~/machbase_home
cd ~/machbase_home

# 다운로드한 패키지 파일 압축 해제
tar zxf machbase-SDK-8.7.0.official-LINUX-X86-64-release.tgz
```

압축 해제 후 디렉터리 구조를 확인합니다.

```bash
ls -l
# bin/  conf/  dbs/  doc/  include/  lib/  trc/  ...
```

#### 3. 환경 변수 설정

`~/.bashrc`에 환경 변수를 추가합니다.

```bash
export MACHBASE_HOME=~/machbase_home
export PATH=$MACHBASE_HOME/bin:$PATH
export LD_LIBRARY_PATH=$MACHBASE_HOME/lib:$LD_LIBRARY_PATH
```

적용합니다.

```bash
source ~/.bashrc
```

#### 4. 데이터베이스 생성

`machadmin -c`로 데이터베이스 파일을 초기화합니다.

```bash
machadmin -c
# Database created successfully.
```

#### 5. 서버 시작

```bash
machadmin -u
# Machbase server started successfully.
```

프로세스 확인:

```bash
ps -ef | grep machbased
# machbase  1234  1  2 11:25 ? 00:00:01 .../machbased -s --recovery=simple
```

#### 6. 접속 테스트

`machsql`로 서버에 접속합니다. 기본 관리자 계정은 `SYS / MANAGER`입니다.

```bash
machsql
# Machbase server address (Default:127.0.0.1) :
# Machbase user ID  (Default:SYS)
# Machbase User Password :
# MACHBASE_CONNECT_MODE=INET, PORT=5656 EDITION=STANDARD
# Mach>
```

간단한 테스트를 수행합니다.

```sql
CREATE LOG TABLE test (id INTEGER, val DOUBLE);
INSERT INTO test VALUES (1, 3.14);
SELECT * FROM test;
```

#### 서버 종료

설치 확인이 끝난 뒤 서버를 중지해야 할 때만 실행합니다.

```bash
machadmin -s
# Machbase server shut down successfully.
```

#### 포트 변경

기본 포트(5656)를 변경하려면 `$MACHBASE_HOME/conf/machbase.conf`의 `PORT_NO`를 수정하거나 환경 변수를 설정합니다.

```bash
export MACHBASE_PORT_NO=7878
```

---

<a id="linux-docker"></a>

### Docker 설치

Docker 이미지를 사용하면 별도의 환경 준비 없이 빠르게 구동할 수 있습니다. 개발·테스트 환경에 적합합니다.

Docker가 사전에 설치되어 있어야 합니다. 배포 튜토리얼은 `machbase/machbase` 이미지를 사용합니다. 소스에서 Docker 이미지를 직접 빌드한 경우에는 로컬 이미지 이름(`machbase:latest` 등)으로 바꾸십시오.

#### 이미지 확인

```bash
docker pull machbase/machbase
docker image ls machbase/machbase
```

#### 컨테이너 실행

```bash
docker run -d \
  --name machbase \
  --ulimit nofile=65535 \
  -p 5656:5656 \
  -v /data/machbase:/home/machbase/machbase/dbs \
  machbase/machbase
```

| 옵션 | 설명 |
|------|------|
| `-p 5656:5656` | SQL 클라이언트 포트 매핑 |
| `--ulimit nofile=65535` | 컨테이너 안에서 서버가 사용할 파일 디스크립터 한도 |
| `-v /data/machbase:...` | 데이터 디렉터리 볼륨 마운트 (데이터 영속성 보장) |

볼륨 마운트를 생략하면 컨테이너 삭제 시 데이터가 함께 제거됩니다.

#### 컨테이너 상태 확인

```bash
docker ps
docker logs machbase
```

#### 접속 테스트

##### machsql (컨테이너 내부)

```bash
docker exec -it machbase machsql
# Mach>
```

##### 호스트에서 접속

호스트에 machsql이 설치된 경우:

```bash
machsql -s 127.0.0.1 -P 5656 -u SYS -p MANAGER
```

#### 컨테이너 종료 및 재시작

```bash
docker stop machbase
docker start machbase
```

#### 라이선스 설치

컨테이너 실행 후 라이선스를 설치하려면 파일을 컨테이너 내부로 복사합니다.

```bash
docker cp license.dat machbase:/home/machbase/machbase/conf/license.dat
docker restart machbase
```

---

<a id="windows"></a>

## Windows 설치

### 설치 전 확인

- **지원 OS**: Windows 10, Windows Server 2019 이상
- **아키텍처**: 배포 패키지의 비트 수와 운영체제 아키텍처가 일치해야 합니다.

설치 전에 [Windows 환경 준비](/dbms/installation-deployment-upgrade/standard-edition/#windows-preparation-environment-windows)를 먼저 완료하십시오.

### 설치 방식

| 방식 | 설명 |
|------|------|
| [Windows 패키지 설치](/dbms/installation-deployment-upgrade/standard-edition/#windows-package) | 설치 마법사를 통한 설치. 환경 변수와 바로가기 생성 |

---

<a id="windows-preparation-environment-windows"></a>

### Windows 환경 준비

Windows에 설치하기 전에 방화벽 설정을 확인합니다.

#### 방화벽 포트 열기

Machbase가 사용하는 포트를 Windows 방화벽 인바운드 규칙에 추가합니다.

| 포트 | 프로토콜 | 용도 |
|------|---------|------|
| 5656 | TCP | SQL 클라이언트 접속 |

##### 설정 방법

1. **제어판 → Windows Defender 방화벽 → 고급 설정**을 엽니다.

2. 왼쪽 패널에서 **인바운드 규칙**을 선택하고, 오른쪽 패널에서 **새 규칙**을 클릭합니다.

3. 규칙 유형으로 **포트**를 선택하고 **다음**을 클릭합니다.

4. **TCP**를 선택하고, **특정 로컬 포트** 필드에 `5656`을 입력한 후 **다음**을 클릭합니다.

5. **연결 허용**을 선택하고 **다음**을 클릭합니다.

6. **도메인**, **개인**, **공용** 모두 체크하고 **다음**을 클릭합니다.

7. 규칙 이름(예: `Machbase`)을 입력하고 **마침**을 클릭합니다.

##### PowerShell로 설정 (관리자 권한)

GUI 대신 PowerShell로 빠르게 설정합니다.

```powershell
New-NetFirewallRule -DisplayName "Machbase SQL" -Direction Inbound -Protocol TCP -LocalPort 5656 -Action Allow
```

#### Visual C++ 재배포 패키지

실행에 Visual C++ Redistributable이 필요합니다. 설치 실행 파일을 사용하는 경우 자동으로 처리될 수 있지만, 문제가 발생하면 Microsoft 공식 사이트에서 최신 버전을 수동으로 설치하십시오.

---

<a id="windows-package"></a>

### Windows 패키지 설치

Windows 버전은 ZIP 패키지 또는 설치 실행 파일로 제공됩니다. ZIP 패키지는 압축 파일 루트에 `bin\`, `conf\`, `dbs\`, `trc\` 등을 포함하며, 설치 실행 파일은 설치 경로 아래에 `machbase_home\`을 만들고 환경 변수와 실행 바로가기를 생성합니다.

#### 설치 절차

1. Windows 배포 패키지를 다운로드합니다.

2. ZIP 패키지를 사용하는 경우 원하는 설치 디렉터리에 압축을 해제합니다.

   ```cmd
   mkdir C:\machbase
   tar -xf machbase-SDK-8.7.0.official-WINDOWS-X86-64-release.zip -C C:\machbase
   ```

3. 설치 실행 파일이 제공된 경우 파일을 실행합니다. 설치 시작 화면이 표시되면 **Next**를 클릭합니다.

4. 설치 경로를 선택합니다. 기본값은 `C:\machbase-<short_version>\` 형식입니다. 변경이 필요하면 경로를 수정한 후 **Next**를 클릭합니다.

5. 설치가 진행됩니다. 완료되면 **Next** → **Close**를 클릭합니다.

#### 서버 시작과 종료

설치 실행 파일을 사용한 경우 바탕화면과 시작 메뉴에 바로가기가 생성됩니다.

- **start Machbase**: `machadmin.exe -u`를 실행해 서버를 시작합니다.
- **stop Machbase**: `machadmin.exe -s`를 실행해 서버를 종료합니다.
- **machsql**: SQL 콘솔을 실행합니다.

#### 명령줄 접속

설치 후 명령 프롬프트에서 `machsql`을 실행하여 서버에 접속합니다. 설치 실행 파일을 사용한 경우 `<설치 경로>\machbase_home\bin`이 시스템 `PATH`에 추가됩니다. ZIP 패키지를 사용한 경우 압축을 해제한 디렉터리의 `bin\`을 `PATH`에 추가하거나 전체 경로로 실행합니다.

```cmd
machsql -s 127.0.0.1 -P 5656 -u SYS -p MANAGER
```

기본 관리자 계정: `SYS` / `MANAGER`

#### 설치 경로 구조

ZIP 패키지는 압축 해제 경로 바로 아래에 `bin\`, `conf\`, `dbs\`, `trc\` 등을 배치합니다.
설치 실행 파일은 설치 경로 아래의 `machbase_home\`에 같은 구성을 생성합니다.
[패키지 구성](/dbms/installation-deployment-upgrade/pre-install-preparation/#package) 참고.
