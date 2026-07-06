---
type: docs
title: 'Tarball 설치'
weight: 20
---

Linux 환경에 tarball(.tgz)을 압축 해제하여 Machbase Standard Edition을 설치하는 절차입니다.

## 1. 사용자 생성

Machbase 전용 OS 사용자를 생성합니다.

```bash
sudo useradd machbase
sudo passwd machbase
```

이후 `machbase` 계정으로 로그인하여 작업합니다.

## 2. 패키지 다운로드 및 압축 해제

설치 디렉터리를 만들고 패키지를 압축 해제합니다.

```bash
mkdir ~/machbase_home
cd ~/machbase_home

# 다운로드한 패키지 파일 압축 해제
tar zxf machbase-standard-8.6.0.official-LINUX-X86-64-release.tgz
```

압축 해제 후 디렉터리 구조를 확인합니다.

```bash
ls -l
# bin/  conf/  dbs/  doc/  http/  include/  lib/  trc/  ...
```

## 3. 환경 변수 설정

`~/.bashrc`에 Machbase 환경 변수를 추가합니다.

```bash
export MACHBASE_HOME=~/machbase_home
export PATH=$MACHBASE_HOME/bin:$PATH
export LD_LIBRARY_PATH=$MACHBASE_HOME/lib:$LD_LIBRARY_PATH
```

적용합니다.

```bash
source ~/.bashrc
```

## 4. 데이터베이스 생성

`machadmin -c`로 데이터베이스 파일을 초기화합니다.

```bash
machadmin -c
# Database created successfully.
```

## 5. 서버 시작

```bash
machadmin -u
# Machbase server started successfully.
```

프로세스 확인:

```bash
ps -ef | grep machbased
# machbase  1234  1  2 11:25 ? 00:00:01 .../machbased -s --recovery=simple
```

## 6. 접속 테스트

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
CREATE TABLE test (id INTEGER, val DOUBLE);
INSERT INTO test VALUES (1, 3.14);
SELECT * FROM test;
```

## 7. 서버 종료

```bash
machadmin -s
# Machbase server shut down successfully.
```

## 포트 변경

기본 포트(5656)를 변경하려면 `$MACHBASE_HOME/conf/machbase.conf`의 `PORT_NO`를 수정하거나 환경 변수를 설정합니다.

```bash
export MACHBASE_PORT_NO=7878
```

---

**다음 읽을 내용**
- [라이선스 설치](/dbms/installation-deployment-upgrade/pre-install-preparation/license/)
- [설치 검증 체크리스트](/dbms/installation-deployment-upgrade/validation-checklist/)
