---
type: docs
title: 'MSI 설치'
weight: 20
toc: true
---

Machbase Windows 버전은 MSI 설치 패키지로 제공됩니다. 설치 마법사를 통해 진행하며 서비스 등록까지 자동으로 처리됩니다.

## 설치 절차

1. Machbase 공식 배포 사이트에서 MSI 파일을 다운로드합니다.

2. MSI 파일을 실행합니다. 설치 시작 화면이 표시되면 **Next**를 클릭합니다.

3. 설치 경로를 선택합니다. 기본값은 `C:\Machbase\`입니다. 변경이 필요하면 경로를 수정한 후 **Next**를 클릭합니다.

4. 설치가 진행됩니다. 완료되면 **Next** → **Close**를 클릭합니다.

## 서버 시작

설치 완료 후 바탕화면에 Machbase 바로가기 아이콘이 생성됩니다. 더블클릭하면 Machbase 관리 창이 열립니다.

관리 창에서:
- **Start Server**: Machbase 서버 시작
- **Stop Server**: 서버 종료
- **Start REST**: HTTP REST 서비스 시작

서버가 시작되면 시스템 트레이에 Machbase 아이콘이 표시됩니다.

## 명령줄 접속

설치 후 명령 프롬프트에서 `machsql`을 실행하여 서버에 접속할 수 있습니다. 설치 경로가 시스템 PATH에 자동 추가됩니다.

```cmd
machsql -s 127.0.0.1 -u SYS -p MANAGER
```

기본 관리자 계정: `SYS` / `MANAGER`

## 서비스 등록 확인

MSI 설치 시 Machbase가 Windows 서비스로 등록됩니다. 서비스 관리자(`services.msc`)에서 `Machbase` 서비스를 확인하고 시작 유형을 조정할 수 있습니다.

## 설치 경로 구조

기본 설치 경로 `C:\Machbase\` 아래에 `bin\`, `conf\`, `dbs\`, `trc\` 등이 생성됩니다. [패키지 구성](/dbms/installation-deployment-upgrade/pre-install-preparation/package/) 참고.

---

**다음 읽을 내용**
- [라이선스 설치](/dbms/installation-deployment-upgrade/pre-install-preparation/license/)
- [설치 검증 체크리스트](/dbms/installation-deployment-upgrade/validation-checklist/)
