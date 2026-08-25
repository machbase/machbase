---
type: docs
title: '11.11 외부 도구 연동'
weight: 110
toc: true
aliases:
  - /dbms/application-integration/external-tools/
---

외부 수집·시각화 도구는 Machbase가 제공하는 SQLCLI, JDBC, ODBC 또는 검증된 전용
플러그인을 통해 연결합니다. 플러그인의 설치 가능 여부와 지원 버전은 도구 배포본마다
달라질 수 있으므로 운영 반영 전에 실제 조합을 검증합니다.

## 공통 점검

1. 외부 도구가 실행되는 호스트에서 5656 포트 연결을 확인합니다.
2. 조회·입력 목적에 맞는 최소 권한 계정을 사용합니다.
3. 비밀번호나 AUTH KEY를 설정 파일에 평문으로 남기지 않습니다.
4. 작은 표본으로 timestamp, NULL, 문자열 encoding, 숫자 타입을 왕복 검증합니다.
5. timeout, batch 크기, retry, 실패 row 처리 방식을 정합니다.
6. 외부 도구와 Machbase 양쪽 로그에서 같은 작업을 추적할 식별자를 남깁니다.

<a id="fluentd-plugin"></a>

## Fluentd

로그·이벤트 수집에는 Fluentd output plugin 또는 파일 파이프라인을 사용할 수 있습니다.
플러그인을 선택했다면 다음을 확인합니다.

- 설치한 gem이 현재 Ruby·Fluentd 버전과 호환되는지
- 대상 LOG 테이블의 컬럼 순서와 record mapping이 일치하는지
- buffer의 flush 주기, chunk 한도, retry와 overflow 정책
- 재시작 후 중복 전송과 유실 처리
- 오류 row를 별도 파일이나 dead-letter 경로로 보존하는지

Fluentd 설치·설정 예제를 이 페이지에 중복하지 않습니다. DBMS 수집 흐름은
[Fluentd 파이프라인](fluentd/)을 정본으로 사용하고, 설치한
plugin의 option은 해당 버전의 plugin 문서를 확인합니다.

<a id="grafana-plugin"></a>

## Grafana

Grafana datasource를 구성할 때는 server 주소, database, 전용 조회 계정, timeout을
지정합니다. 연결 테스트 뒤 다음 순서로 panel query를 검증합니다.

1. 고정된 짧은 시간 범위로 row를 조회합니다.
2. dashboard의 time range가 Machbase `DATETIME` 조건으로 변환되는지 확인합니다.
3. series 이름, 시간 컬럼, 값 컬럼의 mapping을 확인합니다.
4. tag 수와 시간 범위를 늘리며 응답 시간과 반환 row 수를 관찰합니다.
5. alert query가 dashboard query와 같은 timezone·필터를 사용하는지 확인합니다.

dashboard에서 전체 기간을 무제한 조회하지 말고 시간 조건과 tag 조건을 먼저 적용합니다.
plugin별 macro와 변수 문법은 설치한 datasource 버전의 문서를 기준으로 합니다.

<a id="tableau-connector"></a>

## Tableau

Tableau는 Machbase JDBC 또는 ODBC 드라이버를 사용해 연결할 수 있습니다.

| 환경 | 연결 방식 | 준비 |
|------|-----------|------|
| JDBC를 지원하는 Tableau 배포 | Machbase JDBC | `machbase.jar` 배치와 driver 등록 |
| DSN 기반 배포 | Machbase ODBC | 동일 bitness의 ODBC driver와 DSN 구성 |

드라이버 설치와 연결 문자열은 [JDBC](/dbms/development-tools-integration/jdbc/)와
[SQLCLI·ODBC](/dbms/development-tools-integration/cli-odbc/)를 참고합니다. Tableau가
실행되는 desktop·server 노드 모두 같은 driver를 사용하도록 배포합니다.

custom SQL은 먼저 `machsql`에서 실행 계획과 결과 건수를 확인합니다. extract를 만들 때는
시간 범위와 증분 기준 컬럼을 명시하고, refresh 중복·실패 복구 절차를 준비합니다.

## 운영 검증

- 연결 테스트만으로 완료하지 않고 실제 query·입력 경로를 수행합니다.
- 외부 도구의 credential 저장 위치와 file permission을 확인합니다.
- plugin·driver 업그레이드는 staging에서 schema와 timestamp 왕복 테스트 후 반영합니다.
- timeout이나 재시도가 장애를 장시간 숨기지 않도록 한도와 경보를 설정합니다.
- 지원 여부가 확인되지 않은 plugin 이름·고정 버전을 운영 표준으로 문서화하지 않습니다.
