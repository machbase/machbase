---
type: docs
title: '17.8.7 terminology-disambiguation'
weight: 70
toc: true
---

이 페이지는 Machbase에서 혼동하기 쉬운 용어를 정리합니다. AI 에이전트가 사용자의 질문에서 용어를 올바르게 해석할 때 참조합니다.

## 용어 정의 표

| 용어 | Machbase에서의 의미 | 혼동 위험 |
|------|---------------------|-----------|
| **Append** | Machbase 전용 고속 삽입 API. SQL INSERT와 별개의 이진 프로토콜로 동작하며 훨씬 빠름. | SQL `INSERT`와 혼동 주의. Append는 별도 API 호출 방식(예: `executeAppendOpen`, `machbase().append()`) |
| **Warehouse** | Cluster Edition에서 데이터를 실제 저장하는 노드 유형. | 일반적 "창고" 또는 "데이터 웨어하우스(DW)"와 다름. Machbase에서는 Cluster의 특정 노드 역할을 지칭. |
| **ROLLUP** | 시계열 데이터를 주기적으로 집계하여 결과를 저장하는 Machbase 자동화 기능. | SQL 표준의 `GROUP BY ROLLUP(...)` 집계 연산자와 다름. Machbase ROLLUP은 별도 테이블에 사전 집계 결과를 저장. |
| **AUTH KEY** | 공개키(Public Key) 기반 인증 수단. 비밀번호 대신 사용하거나 병행 사용 가능. | 일반적인 API Key나 비밀번호와 다름. RSA/ECDSA 기반 비대칭 키쌍을 사용. |
| **BASETIME** | TAG 테이블에서 시계열 타임스탬프 역할을 하는 컬럼에 부여하는 속성(attribute). | "기준 시각"이라는 일반 단어와 혼동 가능. Machbase에서 BASETIME은 TAG 테이블 스키마 속성으로, 나노초 단위 `datetime` 타입이어야 함. |
| **SUMMARIZED** | TAG 테이블에서 ROLLUP 집계 대상이 되는 컬럼에 부여하는 속성. | "요약된"이라는 일반 단어와 혼동 가능. SUMMARIZED 속성 컬럼만 ROLLUP 집계에 포함되며, UPDATE SET 대상이 될 수 있음. |
| **LOG 테이블** | 시계열 로그/이벤트 데이터를 저장하는 Append-only 테이블 유형. 텍스트 전문 검색 지원. | 서버 로그 파일(machbase.trc)과 완전히 다름. Machbase의 테이블 타입 중 하나. |
| **LOOKUP 테이블** | 참조 데이터(마스터 데이터)를 저장하는 테이블 유형. UPDATE/DELETE를 지원하지만 TRANSACTION 명시 트랜잭션에는 참여하지 않음. | SQL의 LOOKUP 조인 연산이나 일반적인 "조회"와 다름. Machbase에서는 특정 테이블 타입을 지칭. |
| **Broker** | Cluster Edition에서 클라이언트 연결을 수신하고 Warehouse 노드로 쿼리를 분산하는 노드. | 메시지 브로커(Kafka, RabbitMQ 등)와 다름. Machbase Cluster의 프록시/라우팅 노드 역할. |
| **machbase.trc** | Machbase 서버의 메인 로그 파일. `$MACHBASE_HOME/trc/` 디렉토리에 위치. | `.trc`는 "trace"의 약자. LOG 테이블(데이터 저장)과 다른 서버 운영 로그 파일. |
| **VOLATILE 테이블** | 메모리에만 존재하는 임시 테이블. 서버 재시작 시 데이터 소멸. Standard Edition 전용. | TRANSACTION 테이블의 인메모리 버전과 유사하나, Cluster Edition에서는 미지원. |
| **machgo** | Go 언어용 Machbase native 클라이언트 드라이버. Append, named bind, DECIMAL, NULL 메타데이터와 초기 database 선택을 지원. | Go 표준 `database/sql` 드라이버와 구분. 표준 Append API는 없지만 `machbase.Conn.Appender()`를 `sql.Conn.Raw()`에서 선택적으로 사용할 수 있음. |

## 자주 발생하는 혼동 사례

### "Append"를 INSERT로 혼동하는 경우

사용자가 "Python으로 데이터를 Append하려면?" 질문 시:

- 잘못된 해석: SQL `INSERT INTO ... VALUES ...` 사용
- 올바른 해석: `machbaseAPI`의 `machbase()` 클래스의 `append()` 메서드 또는 `executeAppend` 시리즈 사용

### "ROLLUP"을 SQL 집계로 혼동하는 경우

사용자가 "ROLLUP으로 일별 집계를 보려면?" 질문 시:

- 잘못된 해석: `GROUP BY ROLLUP(date)` SQL 구문
- 올바른 해석: `CREATE ROLLUP` 으로 생성된 집계 결과 테이블을 SELECT, 또는 `ALTER SYSTEM FLUSH ROLLUP`으로 강제 실행
