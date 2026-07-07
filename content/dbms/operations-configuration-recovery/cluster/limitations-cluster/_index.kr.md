---
type: docs
title: 'Cluster 운영 제한사항'
weight: 80
---

Machbase Cluster Edition은 단일 노드(Standard/Edge Edition) 대비 일부 기능이 지원되지 않거나 동작 방식이 다릅니다. 클러스터 환경으로 마이그레이션하기 전에 반드시 확인합니다.

## 테이블 유형 제한

| 테이블 유형 | Standard Edition | Cluster Edition |
|-------------|:---:|:---:|
| Log 테이블 | 지원 | 지원 |
| Tag 테이블 | 지원 | 지원 |
| Volatile 테이블 | 지원 | 지원 |
| Lookup 테이블 | 지원 | 지원 (Lookup 노드 필요) |
| **RDB 테이블** | 지원 | **미지원** |

RDB 테이블을 사용하는 애플리케이션은 Cluster Edition으로 이전할 때 대체 방안을 마련해야 합니다.

## ROLLUP 관련 제한

| 기능 | Standard Edition | Cluster Edition |
|------|:---:|:---:|
| 자동 ROLLUP | 지원 | 지원 |
| **Custom ROLLUP** | 지원 | **미지원** |
| **ROLLUP_REBUILD** | 지원 | **미지원** |

Cluster Edition에서는 시스템이 자동으로 관리하는 ROLLUP만 사용할 수 있습니다. 사용자 정의 ROLLUP 함수나 ROLLUP 재구성 명령은 실행 시 오류가 발생합니다.

## DDL 및 ALTER TABLE 제한

Cluster Edition에서는 일부 `ALTER TABLE` 명령이 제한됩니다.

- **파티션 추가/삭제** 일부 제한
- **인덱스 변경** 중 데이터 쓰기 일시 차단 가능
- **컬럼 추가/삭제** 클러스터 전체 동기화 필요

ALTER TABLE 실행 전 반드시 테스트 환경에서 검증합니다.

## 고가용성 제한

### 단일 Broker 구성

Broker가 하나만 있는 경우 해당 Broker에 장애가 발생하면 모든 클라이언트 연결이 차단됩니다. 운영 환경에서는 Broker를 2개 이상 구성하는 HA 구성을 강력히 권장합니다.

### 단일 Coordinator 구성

Primary Coordinator에 장애가 발생하면 클러스터 메타 변경이 불가합니다. Secondary Coordinator를 함께 구성하면 자동 페일오버가 가능합니다.

## 쿼리 실행 제한

| 기능 | 비고 |
|------|------|
| 크로스-그룹 조인 | 그룹 간 대용량 조인 시 성능 저하 가능 |
| 서브쿼리 분산 처리 | 일부 복잡한 서브쿼리는 단일 노드에서 처리 |
| 전체 정렬(ORDER BY) | 대용량 데이터 정렬 시 Broker 메모리 소비 증가 |

## 운영 도구 제한

일부 `machadmin` 옵션은 Cluster Edition에서 직접 사용하지 않습니다. 개별 노드에서 `machadmin`을 직접 실행하는 대신 `machcoordinatoradmin`을 통해 클러스터 전체를 관리합니다.

## 버전 혼재 제한

클러스터 내 모든 노드는 동일한 Machbase 버전을 사용해야 합니다. 버전이 다른 노드가 혼재하면 클러스터가 정상적으로 동작하지 않을 수 있습니다. 업그레이드 시 롤링 업그레이드 절차를 따릅니다.

## 제한사항 요약

| 항목 | 제한 내용 |
|------|-----------|
| RDB 테이블 | 미지원 |
| Custom ROLLUP | 미지원 |
| ROLLUP_REBUILD | 미지원 |
| 일부 ALTER TABLE | 제한 또는 동작 차이 |
| 단일 Broker | HA 미구성 시 단일 장애점(SPOF) |
| 단일 Coordinator | Secondary 미구성 시 단일 장애점(SPOF) |
| 버전 혼재 | 미지원 (동일 버전 필수) |
