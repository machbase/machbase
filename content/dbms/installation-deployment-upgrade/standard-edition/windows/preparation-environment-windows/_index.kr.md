---
type: docs
title: '3.2.2.1 Windows 환경 준비'
weight: 10
toc: true
---

Windows에 Machbase를 설치하기 전에 방화벽 설정을 확인합니다.

## 방화벽 포트 열기

Machbase가 사용하는 포트를 Windows 방화벽 인바운드 규칙에 추가합니다.

| 포트 | 프로토콜 | 용도 |
|------|---------|------|
| 5656 | TCP | SQL 클라이언트 접속 |
| 5657 | TCP | HTTP REST API |

### 설정 방법

1. **제어판 → Windows Defender 방화벽 → 고급 설정**을 엽니다.

2. 왼쪽 패널에서 **인바운드 규칙**을 선택하고, 오른쪽 패널에서 **새 규칙**을 클릭합니다.

3. 규칙 유형으로 **포트**를 선택하고 **다음**을 클릭합니다.

4. **TCP**를 선택하고, **특정 로컬 포트** 필드에 `5656,5657`을 입력한 후 **다음**을 클릭합니다.

5. **연결 허용**을 선택하고 **다음**을 클릭합니다.

6. **도메인**, **개인**, **공용** 모두 체크하고 **다음**을 클릭합니다.

7. 규칙 이름(예: `Machbase`)을 입력하고 **마침**을 클릭합니다.

### PowerShell로 설정 (관리자 권한)

GUI 대신 PowerShell로 빠르게 설정할 수 있습니다.

```powershell
New-NetFirewallRule -DisplayName "Machbase SQL" -Direction Inbound -Protocol TCP -LocalPort 5656 -Action Allow
New-NetFirewallRule -DisplayName "Machbase HTTP" -Direction Inbound -Protocol TCP -LocalPort 5657 -Action Allow
```

## Visual C++ 재배포 패키지

Machbase 실행에 Visual C++ Redistributable이 필요합니다. 설치 실행 파일을 사용하는 경우 자동으로
처리될 수 있지만, 문제가 발생하면 Microsoft 공식 사이트에서 최신 버전을 수동으로 설치하십시오.

---

**다음 읽을 내용**
- [Windows 패키지 설치](/kr/dbms/installation-deployment-upgrade/standard-edition/windows/package/)
