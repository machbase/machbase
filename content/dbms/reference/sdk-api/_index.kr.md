---
type: docs
title: '17.7 SDK API 레퍼런스'
weight: 70
toc: true
---

이 섹션은 Machbase SDK별 API 레퍼런스를 제공합니다. SDK별 설치, 연결, SQL 실행,
Append, 예제는 각 하위 페이지에서 확인합니다.

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
| [CLI/ODBC](./cli-odbc/) | C/C++ CLI/ODBC API와 예제 |
| [JDBC](./jdbc/) | Java JDBC API와 Append |
| [Python](./python/) | `machbaseapi` Python 클라이언트 |
| [Node.js / TypeScript](./node-js-typescript/) | `@machbase/ts-client` TypeScript 클라이언트 |
| [.NET Connector](./net-connector/) | UniMachNetConnector 및 ADO.NET API |
| [Go](./go/) | `machgo` 네이티브 클라이언트와 `database/sql` 드라이버 |

REST API는 [REST API 레퍼런스](../rest-api/)에서 별도로 확인합니다.
