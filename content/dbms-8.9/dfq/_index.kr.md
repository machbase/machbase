---
type: docs
title: '12. DFQ(DIRECT FILE QUERY)'
weight: 120
toc: true
---

DFQ(Direct File Query)는 파일을 DB에 적재하지 않고 SQL로 직접 탐색·조회·분석하는 기능입니다.
처음 사용할 때는 작은 CSV로 시작하고, 실제 파일을 다룰 때는 해당 포맷의 옵션표와 조합 예제를 참고합니다.

```text
서버 파일/데이터셋 → DESC·탐색 → target·타입·옵션 선택 → READ → SQL 분석/클라이언트 수신
DB의 TEXT/BINARY → 내부 SELECT → 셀별 READ ──────────────────┘
```

## 읽는 순서

- 첫 조회: 12.1 → 12.2 → 해당 포맷
- 로봇·센서 데이터: 12.2 → MCAP/HDF5/LeRobot → 12.5
- 애플리케이션: 기본 조회 → 12.7 또는 12.8 → 12.9 → 12.10

## 구성

| 절 | 내용 |
|---|---|
| [12.1 시작하기](./getting-started/) | 서버 실습 파일·접속·권한과 첫 SELECT |
| [12.2 파일 구조와 컬럼 확인하기](./inspect/) | DESC·SOURCE MAP·schema·inspect |
| [12.3 READ 공통 사용법](./read-options/) | 입력 구문·공통 옵션·반환 모드·타입 |
| [12.4 포맷별 상세 사용법](./formats/) | 10개 포맷의 전체 옵션·조합 SQL·예상 결과 |
| [12.5 구조화된 값과 원문 추출](./extract/) | 필드·배열·노드·추가 컬럼·원문 청크 |
| [12.6 여러 파일과 압축 파일](./multiple-files/) | 파일 목록·glob·스키마 결합·압축 |
| [12.7 SQL 결과를 입력으로 조회](./sql-source/) | TEXT/BINARY 셀·스키마 추론·READ_INFER |
| [12.8 분석과 테이블 적재](./analysis-load/) | 조건·JOIN·집계·TEXT·INSERT SELECT |
| [12.9 애플리케이션에서 결과 받기](./clients/) | Python 스트리밍·메타데이터·부분 읽기 |
| [12.10 권한과 운영](./operations/) | 디렉터리 권한·일관성·자원·취소 |
| [12.11 문제 해결과 지원 범위](./troubleshooting/) | 오류 원인·해결과 포맷 지원표 |

[실습 파일](/assets/dbms-8.9/dfq/samples.zip)을 서버에 준비한 뒤 시작합니다.
각 포맷에는 목적별 예제와 정상·오류 SQL 다운로드가 있습니다.

[전체 예제 SQL 묶음](/assets/dbms-8.9/dfq/sql-examples.zip)도 제공합니다. 오류 SQL은 각 포맷 폴더의 마지막 두 파일입니다.
