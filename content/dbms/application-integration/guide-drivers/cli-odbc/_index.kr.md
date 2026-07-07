---
type: docs
title: 'CLI/ODBC'
weight: 10
---

CLI(Call Level Interface)는 [ISO](https://en.wikipedia.org/wiki/International_Organization_for_Standardization)/[IEC](https://en.wikipedia.org/wiki/International_Electrotechnical_Commission) 9075-3:2003에 정의된 데이터베이스 접속 표준입니다. Machbase는 이 표준을 구현한 네이티브 C 라이브러리를 제공하며, 이를 통해 C/C++ 애플리케이션에서 직접 Machbase에 연결하고 데이터를 처리할 수 있습니다.

## 이 섹션의 구성

| 페이지 | 내용 |
|--------|------|
| [CLI/ODBC 개요](./cli-odbc/) | 헤더 파일, 라이브러리, 주요 API 함수, 연결 파라미터, Append API 상세 설명 |
| [CLI/ODBC 예제](./examples-cli-odbc/) | 접속/해제, INSERT/SELECT, Append 고속 삽입 등 실용적인 예제 코드 |

## CLI/ODBC의 특징

- **네이티브 성능**: 별도의 미들웨어 없이 Machbase 서버와 직접 통신
- **Append API**: 초당 수십만 건의 시계열 데이터를 고속으로 삽입하는 전용 프로토콜
- **표준 호환**: ODBC 3.52 표준을 기반으로 설계되어 익숙한 SQL CLI 패턴 적용 가능
- **C/C++ 지원**: `machbase_sqlcli.h` 헤더와 `libmachbasecli.so` 라이브러리 제공

## 빠른 시작

Machbase가 설치된 환경에서는 다음 경로에 CLI 개발에 필요한 파일이 포함되어 있습니다.

```bash
$MACHBASE_HOME/include/machbase_sqlcli.h   # 헤더 파일
$MACHBASE_HOME/lib/libmachbasecli.so       # 공유 라이브러리 (Linux)
$MACHBASE_HOME/lib/libmachbasecli.a        # 정적 라이브러리
```

컴파일 시 다음과 같이 라이브러리를 링크합니다.

```bash
gcc -o myapp myapp.c \
    -I$MACHBASE_HOME/include \
    -L$MACHBASE_HOME/lib \
    -lmachbasecli -lm -lpthread -ldl -lrt -rdynamic
```
