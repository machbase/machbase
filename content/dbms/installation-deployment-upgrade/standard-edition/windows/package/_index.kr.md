---
type: docs
title: 'Windows 패키지 설치'
weight: 20
toc: true
---

Machbase Windows 버전은 ZIP 패키지 또는 설치 실행 파일로 제공됩니다. ZIP 패키지는 압축 파일
루트에 `bin\`, `conf\`, `dbs\`, `trc\` 등을 포함하며, 설치 실행 파일은 설치 경로 아래에
`machbase_home\`을 만들고 환경 변수와 실행 바로가기를 생성합니다.

## 설치 절차

1. Machbase Windows 배포 패키지를 다운로드합니다.

2. ZIP 패키지를 사용하는 경우 원하는 설치 디렉터리에 압축을 해제합니다.

   ```cmd
   mkdir C:\machbase
   tar -xf machbase-8.6.0.official-WINDOWS-X86-64-release.zip -C C:\machbase
   ```

3. 설치 실행 파일이 제공된 경우 파일을 실행합니다. 설치 시작 화면이 표시되면 **Next**를 클릭합니다.

4. 설치 경로를 선택합니다. 기본값은 `C:\machbase-<short_version>\` 형식입니다. 변경이 필요하면
   경로를 수정한 후 **Next**를 클릭합니다.

5. 설치가 진행됩니다. 완료되면 **Next** → **Close**를 클릭합니다.

## 서버 시작과 종료

설치 실행 파일을 사용한 경우 바탕화면과 시작 메뉴에 Machbase 바로가기가 생성됩니다.

- **start Machbase**: `machadmin.exe -u`를 실행해 서버를 시작합니다.
- **stop Machbase**: `machadmin.exe -s`를 실행해 서버를 종료합니다.
- **machsql**: SQL 콘솔을 실행합니다.

## 명령줄 접속

설치 후 명령 프롬프트에서 `machsql`을 실행하여 서버에 접속할 수 있습니다. 설치 실행 파일을
사용한 경우 `<설치 경로>\machbase_home\bin`이 시스템 `PATH`에 추가됩니다. ZIP 패키지를 사용한
경우 압축을 해제한 디렉터리의 `bin\`을 `PATH`에 추가하거나 전체 경로로 실행합니다.

```cmd
machsql -s 127.0.0.1 -u SYS -p MANAGER
```

기본 관리자 계정: `SYS` / `MANAGER`

## 설치 경로 구조

ZIP 패키지는 압축 해제 경로 바로 아래에 `bin\`, `conf\`, `dbs\`, `trc\` 등을 배치합니다.
설치 실행 파일은 설치 경로 아래의 `machbase_home\`에 같은 구성을 생성합니다.
[패키지 구성](/kr/dbms/installation-deployment-upgrade/pre-install-preparation/package/) 참고.

---

**다음 읽을 내용**
- [라이선스 설치](/kr/dbms/installation-deployment-upgrade/pre-install-preparation/license/)
- [설치 검증 체크리스트](/kr/dbms/installation-deployment-upgrade/validation-checklist/)
