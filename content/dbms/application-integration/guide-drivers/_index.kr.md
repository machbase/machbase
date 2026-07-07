---
type: docs
title: '드라이버별 가이드'
weight: 30
---

이 섹션에서는 Machbase에 연결하기 위한 각 드라이버 및 SDK의 사용 방법을 설명합니다. C/C++ 네이티브 환경부터 Java, Python, Go 등 다양한 언어를 위한 연결 방식을 제공합니다.

## 지원 드라이버 목록

| 드라이버 / SDK | 언어 | 연결 방식 | Append 지원 | 특징 |
|----------------|------|-----------|:-----------:|------|
| [CLI/ODBC](./cli-odbc/) | C / C++ | 네이티브 라이브러리 | 지원 | 가장 낮은 수준의 직접 연결. 최고 성능의 Append API 제공 |
| JDBC | Java | TCP/IP | 미지원 | 표준 JDBC 인터페이스. Java 애플리케이션과 통합 용이 |
| Python | Python | TCP/IP | 지원 | machbasedb 패키지 제공. 데이터 분석 환경에 적합 |
| Go | Go | TCP/IP | 지원 | database/sql 인터페이스 호환. 고성능 서비스 개발에 적합 |
| Node.js | JavaScript | TCP/IP | 미지원 | machbase-neo-client 패키지 제공 |
| RESTful API | 모든 언어 | HTTP | 미지원 | 별도 드라이버 불필요. 간단한 통합에 적합 |

## 드라이버 선택 가이드

### 고성능 시계열 데이터 수집이 목적인 경우

초당 수만 건 이상의 대용량 시계열 데이터를 입력해야 한다면 **CLI/ODBC의 Append API** 사용을 권장합니다. Append 프로토콜은 비동기 버퍼링 방식으로 동작하여 일반 INSERT 대비 수십 배 이상의 입력 성능을 제공합니다.

### 기존 Java 애플리케이션과 통합하는 경우

**JDBC 드라이버**를 사용하면 표준 `java.sql` 인터페이스를 그대로 활용할 수 있습니다. Spring, MyBatis 등 Java 생태계와의 통합이 용이합니다.

### 데이터 분석 및 빠른 개발이 목적인 경우

**Python 패키지** 또는 **RESTful API**를 사용하면 별도의 컴파일 없이 빠르게 프로토타입을 작성하고 분석 결과를 확인할 수 있습니다.

## 공통 연결 정보

모든 드라이버는 다음 정보를 사용하여 Machbase 서버에 연결합니다.

| 항목 | 기본값 | 설명 |
|------|--------|------|
| HOST | 127.0.0.1 | Machbase 서버의 호스트명 또는 IP 주소 |
| PORT | 5656 | Machbase 서버 포트 번호 (machbase.conf의 PORT_NO) |
| USER | SYS | 사용자 아이디 |
| PASSWORD | MANAGER | 사용자 패스워드 |
