---
type: docs
title: '5. TAG 테이블 활용'
weight: 50
toc: true
---

TAG 테이블은 반복 관측하는 대상의 이름과 시간 또는 거리 축으로 계측 이력을 저장합니다.
이 장은 Machbase DBMS 8.7.0의 TAG 구조, 입력·조회, 메타데이터와 보정·운영을 설명합니다.
3·4장에서 정한 배포 환경과 데이터 모델을 실제 SQL로 확인하는 단계입니다.

태그는 측정 대상이고 DATA 행은 관측 한 건입니다. METADATA는 태그마다 한 행인 속성이며,
과거 관측마다 별도로 저장되는 속성이 아닙니다. 원본 측정, 현재 속성, 구간 집계와
수집 시각을 구분하면 조회 결과와 정정 범위를 일관되게 해석할 수 있습니다.

## 이 장의 구성

| 절 | 내용 |
|---|---|
| [개요와 사용 기준](./overview-use-criteria/) | 태그 식별자와 관측 행, 시간·거리 축 선택 |
| [테이블 구조와 스키마](./table-structure-schema/) | 컬럼 순서·타입, LSL/USL, BINARY와 저장 설계 |
| [생성, 변경, 삭제](./create-alter-drop/) | 기본 DDL, METADATA 확장과 객체 정리 |
| [데이터 입력과 변경](./data-input-mutation/) | 자동 태그 등록, SQL·Append·파일 입력 구분 |
| [조회와 분석](./query-analysis/) | 구간·최신값·STAT 조회와 결과 해석 |
| [인덱스와 성능](./index-performance/) | 실제 데이터를 이용한 접근 경로 확인 |
| [운영과 데이터 생명주기](./operations-lifecycle/) | 삭제, 보존 정책과 중복 제거 완료 확인 |
| [제약, 오류, 문제 해결](./constraints-errors-troubleshooting/) | 정상 조건과 의도적 실패 예제 |
| [활용 패턴과 시나리오](./patterns-scenarios/) | 관측 단위·단위계·결측에 맞는 모델 |
| [TAG 메타데이터](./tag-metadata/) | 등록·조회·수정·삭제, JSON과 ARRAY |
| [TAG data UPDATE와 데이터 보정](./tag-data-update-correction/) | 직접 정정, NULL 보정과 감사 이력 |
| [tagmetaimport와 메타데이터 일괄 등록](./tagmetaimport/) | CSV 준비, 입력 대상, 재입력 오류 확인 |

## 실습과 지원 범위

각 페이지는 독립 실습입니다. 준비 SQL의 테이블이 이미 있으면 다른 업무 객체인지
확인하고, 임의로 삭제하지 않습니다. 성공 예제와 실패를 확인하는 예제를 분리해 실행하며
정리 SQL은 해당 실습에서 만든 객체에만 적용합니다.

TAG DATA UPDATE는 Standard Edition 전용입니다. 자동 중복 검사 기간, METADATA ALTER와
LSL/USL의 세부 작업도 Edition별 범위를 확인합니다. SQL INSERT, Append의 처리 응답,
저장 버퍼 flush와 인덱스·통계 처리 완료는 같은 의미가 아닙니다.

ROLLUP의 생성·조회·재구성 전체 절차는 [6장](../tag-rollup-usage/)에서 설명합니다.
이 장에서는 TAG 정정과 삭제가 집계에 미치는 관계만 다룹니다.
