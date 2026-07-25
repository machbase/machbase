---
type: docs
title: '17.7 SDK API 레퍼런스'
weight: 70
toc: true
---

SDK별 API 레퍼런스입니다. 설치, 연결, SQL 실행, Append, 예제는 각 하위 페이지에서 확인합니다.

SELECT 결과 컬럼의 NULL 가능 여부와 SDK별 반환 형식은
[Nullable 메타데이터 지원 범위](/dbms/application-integration/support-scope-sdk/#support-scope-sdk-nullable-metadata)를
참고합니다.

## 공통 연결 정보

| 항목 | 기본값 | 설명 |
|------|--------|------|
| HOST | `127.0.0.1` | Machbase 서버 호스트명 또는 IP |
| PORT | `5656` | Machbase 서버 포트 (`machbase.conf`의 `PORT_NO`) |
| USER | `SYS` | 사용자 ID |
| PASSWORD | `MANAGER` | 사용자 비밀번호 |

## SDK별 레퍼런스

| SDK | 설명 |
|-----|------|
| [CLI/ODBC](./cli-odbc/) | C/C++ CLI/ODBC API, Append, Nullable 메타데이터 |
| [JDBC](./jdbc/) | Java JDBC API, Append, Nullable 메타데이터 |
| [Python](./python/) | `machbaseapi` Python 클라이언트와 DB-API `null_ok` |
| [Node.js / TypeScript](./node-js-typescript/) | `@machbase/ts-client`와 `ColumnMeta.nullable` |
| [.NET Connector](./net-connector/) | UniMachNetConnector, ADO.NET, `GetSchemaTable()` |
| [Go](./go/) | `machgo` 네이티브 클라이언트, `database/sql` 드라이버와 제한 사항 |

REST API는 [REST API 레퍼런스](../rest-api/)에서 별도로 확인합니다.
