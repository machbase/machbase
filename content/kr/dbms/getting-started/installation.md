---
type: docs
title: '설치 가이드'
weight: 20
---

이 가이드는 Linux 및 Windows에 Machbase Standard Edition 설치를 다룹니다. 클러스터 설치는 [클러스터 에디션 설치](../../installation/cluster/)를 참조하세요.

## 설치 방법 선택

**Linux 사용자:**
- **Tarball** (권장) - 최대 유연성, 모든 배포판에서 작동
- **Docker** - 빠른 설정, 격리된 환경

**Windows 사용자:**
- **MSI 설치 프로그램** - GUI 마법사가 있는 가장 쉬운 옵션

## Linux 설치

### 방법 1: Tarball 설치 (권장)

#### 1. 사용자 생성 (선택 사항이지만 권장)

```bash
sudo useradd machbase
sudo passwd machbase
su - machbase
```

#### 2. 다운로드 및 압축 해제

```bash
# 패키지 다운로드
wget http://machbase.com/dist/machbase-fog-x.x.x.official-LINUX-X86-64-release.tgz

# 디렉토리 생성
mkdir machbase_home
mv machbase-fog-x.x.x.official-LINUX-X86-64-release.tgz machbase_home/
cd machbase_home/

# 압축 해제
tar zxf machbase-fog-x.x.x.official-LINUX-X86-64-release.tgz
```

#### 3. 환경 변수 설정

`~/.bashrc`에 추가:

```bash
export MACHBASE_HOME=/home/machbase/machbase_home
export PATH=$MACHBASE_HOME/bin:$PATH
export LD_LIBRARY_PATH=$MACHBASE_HOME/lib:$LD_LIBRARY_PATH
```

변경 사항 적용:

```bash
source ~/.bashrc
```

#### 4. 설치 확인

```bash
machadmin --help
```

Machbase Administration Tool 도움말 출력이 표시되어야 합니다.

### 방법 2: Docker 설치

```bash
# 이미지 가져오기
docker pull machbase/machbase

# 컨테이너 실행
docker run -d --name machbase \
  -p 5656:5656 \
  -v machbase_data:/data \
  machbase/machbase

# 컨테이너에 연결
docker exec -it machbase machsql
```

자세한 Docker 지침은 [Docker 설치](../../installation/docker/)를 참조하세요.

## Windows 설치

### MSI 설치 프로그램

#### 1. 다운로드

Machbase 웹사이트에서 Windows 설치 프로그램(.msi 파일)을 다운로드합니다.

#### 2. 설치 프로그램 실행

- .msi 파일을 더블 클릭
- 설치 마법사를 따릅니다
- 설치 디렉토리 선택 (기본값: `C:\machbase`)
- 설치 프로그램이 자동으로 PATH 변수를 설정합니다

#### 3. 설치 확인

명령 프롬프트를 열고 실행:

```cmd
machadmin --help
```

자세한 Windows 지침은 [Windows 설치](../../installation/windows/)를 참조하세요.

## 설치 후 단계

### 1. 데이터베이스 생성

```bash
machadmin -c
```

예상 출력:
```
Database created successfully.
```

### 2. 서버 시작

```bash
machadmin -u
```

예상 출력:
```
Machbase server started successfully.
```

### 3. 서버가 실행 중인지 확인

```bash
machadmin -e
```

또는 프로세스 확인:

```bash
# Linux
ps -ef | grep machbased

# Windows
tasklist | findstr machbased
```

### 4. 데이터베이스에 연결

```bash
machsql
```

기본 자격 증명:
- **Username**: SYS
- **Password**: MANAGER

## 디렉토리 구조

설치 후 다음 디렉토리를 찾을 수 있습니다:

```
machbase_home/
├── bin/           # 실행 파일 (machadmin, machsql 등)
├── conf/          # 구성 파일
├── dbs/           # 데이터베이스 파일 (machadmin -c 후 생성)
├── lib/           # 공유 라이브러리
├── trc/           # 로그 파일
├── sample/        # 예제 파일
└── doc/           # 문서
```

## 구성 (선택 사항)

### 서버 포트 변경

기본적으로 Machbase는 포트 5656을 사용합니다. 변경하려면:

**옵션 1: 환경 변수**

```bash
export MACHBASE_PORT_NO=7878
```

**옵션 2: 구성 파일**

`$MACHBASE_HOME/conf/machbase.conf` 편집:

```ini
PORT_NO = 7878
```

모든 구성 옵션은 [구성 가이드](../../configuration/)를 참조하세요.

## 필수 명령어

```bash
# 데이터베이스 생성
machadmin -c

# 서버 시작
machadmin -u

# 서버 중지
machadmin -s

# 상태 확인
machadmin -e

# 데이터베이스 삭제 (주의!)
machadmin -d

# SQL을 통해 연결
machsql
```

## 라이선스 설치

프로덕션 사용을 위해 라이선스를 설치해야 합니다:

```bash
machadmin -t /path/to/license.dat
```

라이선스 확인:

```bash
machadmin -f
```

또는 machsql에서:

```sql
SHOW LICENSE;
```

평가판 라이선스는 Machbase 웹사이트를 방문하세요. 자세한 라이선스 관리는 [라이선스 관리](../../installation/license/)를 참조하세요.

## 시스템 요구 사항

### 최소 요구 사항

- **CPU**: x86-64 호환 프로세서
- **RAM**: 1GB
- **Disk**: 소프트웨어용 100MB + 데이터 저장소
- **OS**:
  - Linux: 커널 2.6 이상
  - Windows: Windows 7 이상

### 프로덕션 권장 사항

- **CPU**: 4개 이상의 코어
- **RAM**: 8GB 이상
- **Disk**: 더 나은 성능을 위한 SSD
- **OS**:
  - Linux: RHEL 7+, Ubuntu 16.04+, CentOS 7+
  - Windows: Windows Server 2012+

## 문제 해결

### 설치 문제

**"Permission denied" 오류 (Linux)**

```bash
chmod +x $MACHBASE_HOME/bin/*
```

**"Library not found" 오류 (Linux)**

```bash
ldd $MACHBASE_HOME/bin/machbased
# 누락된 라이브러리 설치
```

### 서버 시작 문제

**포트가 이미 사용 중**

```bash
# 포트 5656을 사용 중인 항목 확인
netstat -an | grep 5656

# 다른 포트 사용
export MACHBASE_PORT_NO=7878
```

**메모리 부족**

`$MACHBASE_HOME/conf/machbase.conf`에서 확인 및 조정:

```ini
MEM_MAX_DB = 2G
```

더 많은 솔루션은 [문제 해결 가이드](../../troubleshooting/)를 참조하세요.

## 다음 단계

이제 Machbase가 설치되었습니다:

1. [**빠른 시작**](../quick-start/) - 첫 번째 데이터베이스 및 테이블 생성
2. [**첫 단계**](../first-steps/) - 기본 machsql 명령어 학습
3. [**기본 개념**](../concepts/) - Machbase 아키텍처 이해

## 고급 설치

고급 설정의 경우:

- [클러스터 에디션 설치](../../installation/cluster/)
- [고가용성 설정](../../installation/cluster/)
- [업그레이드 절차](../../installation/cluster/upgrade/)
