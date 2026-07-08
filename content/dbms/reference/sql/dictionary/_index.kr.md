---
type: docs
title: '함수 사전'
weight: 30
---

Machbase SQL에서 사용할 수 있는 내장 함수를 카테고리별로 정리합니다.

| 카테고리 | 설명 |
|----------|------|
| [집계 함수](aggregation/) | COUNT, SUM, AVG, MIN, MAX, STDDEV, FIRST, LAST 등 그룹 집계 함수 |
| [윈도우/시리즈 함수](item/) | ROWNUM, SERIESNUM 등 윈도우·시리즈 분석 함수 |
| [날짜/시간 함수](item-2/) | TO_DATE, TO_CHAR, DATE_TRUNC, ADD_TIME 등 날짜·시간 처리 함수 |
| [JSON 함수와 `->` 연산자](operators-json/) | JSON 데이터 추출·조작 함수 및 경로 연산자 |
| [정규식 함수](regex/) | REGEXP_LIKE, REGEXP_SUBSTR 등 정규식 기반 검색·변환 함수 |
| [NEXTVAL 함수](nextval/) | Lookup 테이블 Sequence 컬럼용 자동 증가값 생성 함수 |

## 공통 규칙

- 입력 값이 `NULL`이면 결과도 `NULL`입니다 (별도 명시가 없는 한).
- 인자 타입 불일치 시 `ERR-02036` 또는 `ERR-02037` 오류가 발생합니다.
