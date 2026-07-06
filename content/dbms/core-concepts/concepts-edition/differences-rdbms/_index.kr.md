---
type: docs
title: '기존 RDBMS와의 차이'
weight: 20
---

Machbase는 시계열 데이터의 특성에 맞추어 처음부터 설계된 데이터베이스입니다. PostgreSQL, MySQL, Oracle 같은 범용 RDBMS와 구조적으로 다른 점이 많으며, 이를 이해해야 적절한 테이블 설계와 SQL 전략을 세울 수 있습니다.

## 데이터 모델 차이: CRUD vs Append-Only

RDBMS는 행 단위로 데이터를 삽입(Create), 조회(Read), 수정(Update), 삭제(Delete)하는 CRUD 모델을 기반으로 합니다. 주문 정보를 수정하고 재고를 실시간으로 차감하는 업무 애플리케이션에 최적화된 구조입니다.

Machbase의 LOG 테이블과 TAG 테이블은 append-only 모델을 따릅니다. 데이터는 오직 추가(append)되며, 이미 기록된 행은 수정할 수 없습니다. 이 단순한 원칙 덕분에 행 단위 잠금을 제거하고 초당 수백만 건 이상의 입력 성능을 달성합니다.

## 시간의 역할

RDBMS에서 날짜/시간은 여러 컬럼 중 하나일 뿐입니다. 시간 범위 조회에는 일반적으로 B-Tree 인덱스를 사용하지만, 시간이 데이터의 주축으로 설계된 것은 아닙니다.

Machbase에서 시간은 모든 구조의 중심입니다. LOG 테이블은 `_arrival_time`을 자동으로 관리하고, TAG 테이블은 BASETIME 컬럼을 시간 축으로 사용합니다. 파티션도 시간 기준으로 나뉘고, ROLLUP 집계도 시간 단위(SEC/MIN/HOUR)로 수행됩니다.

## 인덱싱 구조

RDBMS의 기본 인덱스는 B-Tree입니다. 특정 키 값을 빠르게 찾는 랜덤 액세스에 강하지만, 대량 순차 삽입에서는 트리 재균형 비용이 발생합니다.

Machbase는 LOG/LOOKUP 테이블에 LSM(Log-Structured Merge-tree) 계열 인덱스를 사용합니다. 쓰기는 메모리 내 구조에 먼저 기록되고 이후 배경 스레드가 디스크로 병합합니다. 순차 쓰기가 많은 시계열 환경에서 삽입 성능이 월등합니다. TAG 테이블은 태그명 → 시간 파티션 → 값의 3단계 자동 파티션 인덱스를 사용합니다.

## 저장 방식: 행 지향 vs 컬럼 지향

| 항목 | RDBMS (행 지향) | Machbase (컬럼 지향) |
| --- | --- | --- |
| 저장 단위 | 행 전체를 연속으로 저장 | 같은 컬럼값들을 연속으로 저장 |
| INSERT 성능 | 빠름 | 매우 빠름 (append) |
| 특정 컬럼 집계 | 불필요한 컬럼도 읽어야 함 | 해당 컬럼만 읽음 |
| 압축률 | 낮음 (2~5배) | 높음 (10~100배) |
| 전형적 사용 사례 | 업무 트랜잭션, 단건 조회 | 시계열 집계, 분석 쿼리 |

시계열 데이터는 같은 센서의 온도값처럼 유사한 값이 반복되는 경향이 있습니다. 컬럼 단위로 저장하면 이런 패턴이 압축에 매우 유리하게 작용합니다.

## UPDATE / DELETE 제한

LOG 테이블과 TAG 테이블은 UPDATE를 지원하지 않습니다. DELETE는 시간 범위 기반으로만 가능합니다. 잘못 입력된 데이터를 수정해야 한다면, 해당 시간 구간을 삭제하고 재입력하는 방식을 사용합니다.

이 제약은 설계상의 결함이 아니라 고속 입력 성능을 위한 의도적인 트레이드오프입니다. 운영 데이터를 자주 수정해야 하는 업무라면 LOOKUP 또는 VOLATILE 테이블을 활용합니다.

## 사용 사례 비교

| 사용 사례 | 적합한 선택 |
| --- | --- |
| 공장 설비 계측값 수집 및 집계 | Machbase TAG 테이블 |
| 서버 이벤트 로그, 알람 이력 | Machbase LOG 테이블 |
| 고객 주문 정보, 재고 관리 | 범용 RDBMS |
| 제품 마스터, 센서 메타데이터 | Machbase LOOKUP 테이블 |
| 시계열 데이터 + 관계형 업무 혼합 | Machbase (시계열) + 별도 RDBMS 연계 |

## 다음 읽을 내용

- [Standard Edition과 Cluster Edition 차이](../differences-standard-edition-cluster/) — 단일 노드 vs 분산 클러스터 선택
- [데이터 모델 개념](/dbms/core-concepts/concepts/) — 시계열 데이터의 본질과 append-only 설계
- [컬럼형 저장과 압축](/dbms/core-concepts/storage-execution-architecture/storage-columnar-compression-column/) — 컬럼 저장 구조의 상세 내용
