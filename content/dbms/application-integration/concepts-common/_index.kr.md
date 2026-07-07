---
type: docs
title: '공통 연동 개념'
weight: 20
---

드라이버나 언어에 관계없이 Machbase에 연동할 때 공통으로 이해해야 할 개념을 설명합니다. 이 섹션의 내용을 먼저 파악하면 각 SDK의 개별 문서를 빠르게 이해할 수 있습니다.

## 이 섹션의 구성

| 문서 | 내용 |
|------|------|
| [연결 문자열과 인증](connection-string-authentication/) | HOST:PORT, SYS/MANAGER 기본 인증, AUTH KEY 방식, connection pool 권장 설정 |
| [타임존 연결 옵션](timezone-connection/) | UTC 내부 저장, 연결 시 timezone 설정, TO_CHAR/TO_DATE와 timezone, SYSDATE vs NOW |
| [Prepared statement](prepared-statement/) | SQL 인젝션 방지, 재사용 성능, TAG/LOG 테이블에서의 사용 |
| [Parameter binding](parameter-binding/) | 위치 바인딩(`?`), DATETIME nanosecond 처리, NULL 값, SDK별 바인딩 방법 |
| [트랜잭션 처리](transaction/) | RDB 테이블: ACID 완전 지원, TAG/LOG 테이블: append-only, autocommit 동작 |
| [Append API와 Batch INSERT](append-api-batch/) | 고속 비트랜잭션 입력 vs 트랜잭션 기반 배치 INSERT, 언제 무엇을 선택할지 |
| [오류 처리와 재시도](error-handling-retry/) | 연결 오류 코드, exponential backoff, Append flush 실패, connection pool 격리 |

## Machbase 연동의 핵심 특성

Machbase는 일반 관계형 데이터베이스와 다른 몇 가지 중요한 특성이 있습니다. 연동 코드를 작성하기 전에 반드시 숙지하세요.

**테이블 타입에 따른 트랜잭션 지원 차이**

TAG 테이블과 LOG 테이블은 트랜잭션을 지원하지 않습니다. RDB(관계형) 테이블만 완전한 ACID 트랜잭션을 지원합니다. 대부분의 시계열 데이터 수집은 TAG/LOG 테이블을 사용하므로, 이 테이블에 대한 쓰기는 commit/rollback이 의미 없습니다.

**시간 데이터는 내부적으로 UTC nanosecond**

Machbase는 모든 시간 데이터를 UTC 기준 nanosecond 정수로 저장합니다. 연결 시 timezone을 설정하지 않으면 조회 결과가 UTC로 표시됩니다. 애플리케이션 배포 지역에 맞는 timezone 설정을 연결 시 지정하는 것을 권장합니다.

**대용량 입력에는 Append API 사용**

일반 INSERT는 행 단위로 처리되어 대용량 입력에 적합하지 않습니다. Machbase는 버퍼에 데이터를 누적한 뒤 한 번에 전송하는 Append API를 제공합니다. 초당 수천 건 이상의 쓰기가 예상된다면 Append API를 사용하세요.
