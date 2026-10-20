---
title: 새소식
type: docs
weight: 5
toc: false
---

Machbase Neo의 최신 소식과 주요 릴리스 변경 사항을 최신순으로 소개합니다.

## 2026-10-20 — Machbase Neo v8.7.2 릴리스

ARRAY 데이터를 더 편리하게 탐색할 수 있으며, 시작 페이지를 나만의 작업 공간으로 구성하는
실험적 기능이 추가되었습니다.
차트와 파일 작업의 사용성이 개선되었으며, 인증 기본값 강화와 서버·데이터베이스 안정성 개선이
함께 반영되었습니다.

- **시작 페이지 맞춤 설정(실험적 기능)**: 서버 시작 시 `--experiment true` 옵션을 지정해야
  활성화됩니다. 사용자 설정, 그룹 구성, 보기 방식을 지원합니다.
  새 탭의 레이아웃과 저장, 그룹 및 대화 상자 관련 문제도 수정되었습니다.
- **ARRAY 데이터 탐색**: Data Viewer에서 숫자 ARRAY의 요소를 선택하고 상세 차트와 표로
  확인할 수 있습니다. 선택한 요소를 Tag Analyzer로 보내 분석하고 저장할 수 있습니다.
- **차트와 분석 화면 개선**: ECharts 6 지원과 v5 호환 처리가 추가되고,
  차트 실행 환경이 통합되었습니다. Tag Analyzer의 편집 내용 유실과 팝오버 동작,
  대시보드 관련 오류도 수정되었습니다.
- **파일 작업과 오류 처리 개선**: 파일 덮어쓰기 경고, 인코딩, 오류 안내가 개선되었습니다.
  저장 단축키는 macOS에서 `Cmd+S`, 그 외 환경에서 `Ctrl+S`로 동작합니다.
  깊게 중첩된 JSON은 화면 오류 대신 텍스트로 표시하며,
  화면 일부의 오류가 앱 전체에 영향을 주지 않도록 오류 처리를 보강했습니다.
- **인증과 서버 안정성 강화**: JWT 서명 키를 안전하게 생성·저장하도록 개선했습니다.
  TQL 요청의 동시 실행과 취소 처리, 셸 실행 시 출력과 오류 처리,
  서버 운영 메트릭의 동시 접근과 일괄 저장 안정성도 개선되었습니다.
- **데이터베이스 엔진 개선**: DBMS 8.7.2에서 구버전 서버에 대한 `SQLColumns` 호환성을
  수정하고, 일부 쿼리의 CPU 비용을 줄였습니다. ARM64 환경의 비트맵 인덱스 메모리 가시성
  오류도 수정되었습니다.

**업그레이드 시 확인하세요:** HTTP·MQTT 토큰 인증이 기본으로 활성화됩니다.
기존에 토큰 없이 HTTP API나 MQTT를 사용했다면, 업그레이드 전에 클라이언트의 인증 설정을
확인하세요. 명령줄 옵션으로 인증을 끄려면 `--http-enable-token-auth false`와
`--mqtt-enable-token-auth false`를 명시해야 합니다.

[v8.7.2 릴리스 노트](https://github.com/machbase/neo-server/releases/tag/v8.7.2)
· [전체 변경 내역](https://github.com/machbase/neo-server/compare/v8.7.1...v8.7.2)

---

## 2026-10-05 — 쇼케이스 메뉴 추가

상단 메뉴의 **Apps** 오른쪽에 **쇼케이스** 링크가 추가되었습니다.
파란색 배경과 작은 재생 아이콘으로 강조된 링크를 통해 Machbase Neo의 활용 사례와
데모를 쉽게 찾아볼 수 있습니다. 현재 문서 언어에 맞는 쇼케이스 페이지로 이동합니다.

[쇼케이스 살펴보기]({{< relref "/neo/showcases" >}})

---

## 2026-09-23 — Machbase Neo v8.7.1 릴리스

SSH와 TQL API에 API 토큰 인증이 추가되고, 시그널 처리와 서비스 종료 동작이 개선되었습니다.
중첩 파일 시스템 마운트와 충돌 처리, 파일 처리 엔드포인트, JSH와 Neo-shell 도움말이
개선되었으며, TQL 버퍼 제한 문제가 수정되었습니다.

[v8.7.1 릴리스 노트](https://github.com/machbase/neo-server/releases/tag/v8.7.1)
· [전체 변경 내역](https://github.com/machbase/neo-server/compare/v8.7.0...v8.7.1)

---

## 2026-09-17 — Machbase Neo v8.5.12 릴리스

Machbase Neo v8.5.12가 발표되었습니다. 릴리스 페이지에 상세 설명이 없으므로,
v8.5.11과 v8.5.12 사이의 변경 사항은 전체 변경 내역에서 확인할 수 있습니다.

[v8.5.12 릴리스 페이지](https://github.com/machbase/neo-server/releases/tag/v8.5.12)
· [전체 변경 내역](https://github.com/machbase/neo-server/compare/v8.5.11...v8.5.12)

---

## 2026-09-09 — Machbase Neo v8.7.0 릴리스

엔진 v8.7과 클라이언트 v2, 다중 데이터베이스 지원, 이름 기반 쿼리 매개변수가 도입되었습니다.
CSV 가져오기 성능, SQL 호환성과 트랜잭션 처리, 인증과 세션 관리,
데이터베이스 백업 요청과 검증 기능이 개선되었습니다.

[v8.7.0 릴리스 노트](https://github.com/machbase/neo-server/releases/tag/v8.7.0)
· [전체 변경 내역](https://github.com/machbase/neo-server/compare/v8.5.10...v8.7.0)
