---
type: docs
title: '19.1.3 함수 사전'
weight: 30
toc: true
---

내장 함수를 카테고리별로 정리합니다.

| 카테고리 | 설명 |
|----------|------|
| [집계 함수](aggregation/) | COUNT·SUM·AVG, FIRST_NOT_NULL·LAST_NOT_NULL·ARG_MIN·ARG_MAX, KSUM·NSUM |
| [선택 윈도 함수 / SUBSAMPLE](subsample/) | LTTB·MINMAX·M4·UNIFORM·CADENCE·SDT의 BOOL 선택 결과 |
| [윈도우/시리즈 함수](series/) | ROWNUM·SERIESNUM, OVER·ROWS와 선택 윈도 함수 문법 연결 |
| [날짜/시간 함수](datetime/) | TO_DATE, TO_CHAR, DATE_TRUNC, ADD_TIME 등 날짜·시간 처리 함수 |
| [JSON 함수와 JSON dot 표기법](operators-json/) | JSON 데이터 추출·조작 함수 및 멤버 접근 문법 |
| [정규식 함수](regex/) | REGEXP_LIKE, REGEXP_SUBSTR 등 정규식 기반 검색·변환 함수 |
| [NEXTVAL 함수](nextval/) | Lookup 테이블 Sequence 컬럼용 자동 증가값 생성 함수 |
| [사용자 컨텍스트 함수](functions-full/#current-session-user) | CURRENT_USER, SESSION_USER와 내부 사용자 ID 조회 |
| [전체 함수 레퍼런스](functions-full/) | 기존 함수 항목과 CAST를 포함한 전체 함수 레퍼런스 |

## 공통 규칙

- 입력 값이 `NULL`이면 결과도 `NULL`입니다 (별도 명시가 없는 한).
- 인자 타입 불일치 시 `ERR-02036` 또는 `ERR-02037` 오류가 발생합니다.

## 문자·바이너리 변환

- [CAST](./functions-full/#cast): UTF-8 문자 경계·타입·길이와 호환성
- [BLOB_TO_TEXT](./functions-full/#blob_to_text): 지정 문자셋의 바이트를 TEXT로 디코딩
- [TEXT_TO_BLOB](./functions-full/#text_to_blob): UTF-8 문자를 지정 문자셋의 BLOB으로 인코딩
- [TO_HEX](./functions-full/#to_hex): 작은 값의 명시적인 HEX 표현

## 집계와 선택 윈도 문법

- [집계 OVER·ROWS 전체 BNF](../syntax/window-function-over-syntax/#rows-bnf)
- [선택 집계의 타입·NULL·동률](./aggregation/#arg_min)
- [보정 합계 KSUM](./aggregation/#ksum)와 [NSUM](./aggregation/#nsum)
- [SUBSAMPLE 절과 BOOL 윈도 형태](../syntax/subsample-syntax/)
