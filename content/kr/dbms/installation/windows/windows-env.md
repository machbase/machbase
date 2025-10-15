---
type: docs
title : 'Windows 설치 환경 준비'
type : docs
weight: 10
---

## 방화벽 포트 열기

Windows에 Machbase를 설치하는 경우 Windows 방화벽에서 Machbase가 사용하는 포트를 열어야 합니다.

일반적으로 Machbase는 **5656**과 **5001** 두 개의 포트를 사용합니다.

1. 방화벽에 포트를 등록하려면 제어판 - Windows 방화벽 또는 Windows Defender 방화벽을 선택합니다.
    실행 화면에서 "고급 설정" 메뉴를 클릭합니다.

![winenv1](../winenv1.png)

2. 고급 설정에서 **인바운드 규칙 - 새 규칙**을 선택하고 클릭합니다.

![winenv2](../winenv2.png)

![winenv3](../winenv3.png)

3. 새 규칙 설정 마법사 창이 표시되면 아래와 같이 포트 옵션을 선택하고 다음을 클릭합니다.

![winenv4](../winenv4.png)

4. **TCP(T)** 옵션을 선택하고, **특정 로컬 포트** 필드에 **5656,5001**을 입력한 후 다음을 클릭합니다.

![winenv5](../winenv5.png)

5. **연결 허용** 옵션을 선택하고 **다음**을 클릭합니다.

![winenv6](../winenv6.png)

6. **도메인**, **개인** 및 **공용**을 체크하고 **다음**을 클릭합니다.

![winenv7](../winenv7.png)

7. **이름**과 **설명** 필드를 작성한 후 **마침**을 클릭합니다.

![winenv8](../winenv8.png)
    
