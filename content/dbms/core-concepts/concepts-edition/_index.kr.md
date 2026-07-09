---
type: docs
title: '2.4 Edition 개념'
weight: 40
---
Machbase DBMS는 PostgreSQL이나 MySQL 같은 범용 RDBMS와 설계 철학부터 다릅니다. 이 섹션은 그 차이를 명확히 이해하고, 운영 규모에 따라 올바른 Edition을 선택하는 데 필요한 개념을 다룹니다.

- **[Standard Edition과 Cluster Edition 차이](/dbms/core-concepts/concepts-edition/#differences-standard-edition-cluster)** — 단일 노드 구성과 분산 클러스터 구성의 구조적 차이, 기능 지원 범위, 선택 기준을 설명합니다.
- **[기존 RDBMS와의 차이](/dbms/core-concepts/concepts-edition/#differences-rdbms)** — append-only 모델, 시간 중심 설계, 컬럼형 저장 등 Machbase가 전통적인 RDBMS와 근본적으로 다른 점을 비교합니다.


<a id="differences-standard-edition-cluster"></a>

## Standard Edition과 Cluster Edition 차이

Machbase DBMS는 운영 규모와 가용성 요구사항에 따라 두 가지 Edition으로 제공됩니다. Standard Edition은 단일 서버에서 운영하고, Cluster Edition은 여러 노드에 데이터를 분산해 처리합니다.

### Standard Edition

Standard Edition은 하나의 프로세스로 동작하는 단일 노드 구성입니다. 설치와 운영이 간단하고, 소규모에서 중규모 시계열 데이터를 처리하는 데 충분한 성능을 제공합니다.

- 단일 `machbase` 프로세스로 SQL 엔진, 저장 관리자, 프로세스 관리자를 모두 포함
- 별도의 분산 코디네이션 없이 즉시 사용 가능
- ROLLUP, STREAM, Retention Policy, Backup/Mount, RDB 테이블 등 대부분의 기능 지원

초당 수십만 건의 입력과 수 TB 규모의 데이터를 단일 서버에서 처리할 수 있습니다.

### Cluster Edition

Cluster Edition은 여러 서버에 데이터를 분산 저장하고 병렬로 처리합니다. 내부적으로 `EDITION_CLUSTER` 컴파일 플래그로 분리된 별도 빌드이며, 주요 노드는 다음과 같이 구성됩니다.

| 노드 유형 | 역할 |
| --- | --- |
| Coordinator | 클러스터 메타데이터 관리, 노드 상태 감시, 쿼리 라우팅 결정 |
| Deployer | 소프트웨어 배포 및 노드 초기화 담당 |
| Broker | 클라이언트 연결 수신, 쿼리를 Warehouse 노드로 분산 |
| Warehouse | 실제 데이터 저장 및 쿼리 실행 담당 |
| Lookup | 클러스터 환경의 LOOKUP 테이블 처리 담당 |

클라이언트는 항상 Broker 노드에 접속하며, Broker가 쿼리를 분석해 해당 데이터를 보유한 Warehouse 노드에 요청을 전달합니다.

### 기능 지원 차이

대부분의 기능은 두 Edition에서 동일하게 동작하지만, 일부 기능은 지원 범위가 다릅니다.

| 기능 | Standard Edition | Cluster Edition |
| --- | --- | --- |
| LOG/TAG/LOOKUP/VOLATILE 테이블 | 모두 지원 | 모두 지원 |
| RDB 테이블 | 지원 | 미지원 |
| ROLLUP | 지원 | 지원 |
| STREAM | 지원 | 제한적 지원 (일부 SQL 패턴 제약) |
| Retention Policy | 지원 | 지원 |
| Backup / Restore / Mount | 지원 | 지원 (노드별 독립 실행) |
| 수평 확장 (노드 추가) | 불가 | 가능 |
| 자동 장애 조치 | 불가 | Coordinator가 감시 |

STREAM의 경우 Cluster Edition에서도 생성과 실행은 가능하지만, 복잡한 조인이나 서브쿼리가 포함된 SQL은 동작하지 않을 수 있습니다. 운영 전에 대상 SQL을 Cluster 환경에서 검증하는 것을 권장합니다.

RDB 테이블은 Standard Edition 전용 기능입니다. Cluster Edition에서는 `CREATE RDB TABLE`과 RDB
관련 DDL/DML/SELECT가 검증 단계에서 거부됩니다. Cluster 환경에서 `CREATE TABLE` 또는
`CREATE LOG TABLE`을 사용하면 기존과 같이 LOG 테이블 생성 경로를 따릅니다.

### 선택 기준

**Standard Edition이 적합한 경우**

- 단일 서버 또는 온프레미스 소규모 배포
- 초당 수십만 건 이하의 입력 처리
- 관리 인력이 적고 운영 단순성이 중요한 경우
- 개발, 테스트, 파일럿 환경

**Cluster Edition이 적합한 경우**

- 초당 수백만 건 이상의 대용량 입력
- 저장 용량이 단일 서버의 한계를 넘는 경우
- 노드 장애 시에도 서비스를 유지해야 하는 고가용성 요구사항
- 데이터 볼륨 증가에 따라 노드를 추가해야 하는 탄력적 확장 필요

### 다음 읽을 내용

- [기존 RDBMS와의 차이](/dbms/core-concepts/concepts-edition/#differences-rdbms) — Machbase 설계 철학의 전체 맥락
- [Machbase 아키텍처 개요](/dbms/core-concepts/storage-execution-architecture/#architecture-machbase) — Standard/Cluster 구조의 내부 상세

<a id="differences-rdbms"></a>

## 기존 RDBMS와의 차이

Machbase는 시계열 데이터의 특성에 맞추어 처음부터 설계된 데이터베이스입니다. PostgreSQL, MySQL, Oracle 같은 범용 RDBMS와 구조적으로 다른 점이 많으며, 이를 이해해야 적절한 테이블 설계와 SQL 전략을 세울 수 있습니다. 다만 Standard Edition에는 관계형 기준 데이터를 함께 다루기 위한 RDB 테이블도 제공되므로, "Machbase 전체"와 "LOG/TAG 시계열 테이블"의 특성을 구분해야 합니다.

### 데이터 모델 차이: CRUD vs Append-Only

RDBMS는 행 단위로 데이터를 삽입(Create), 조회(Read), 수정(Update), 삭제(Delete)하는 CRUD 모델을 기반으로 합니다. 주문 정보를 수정하고 재고를 실시간으로 차감하는 업무 애플리케이션에 최적화된 구조입니다.

Machbase의 LOG 테이블과 TAG 테이블은 append 중심 모델을 따릅니다. 데이터는 고속 append에
맞게 저장되며, TAG 테이블은 태그 선택 조건과 시간 조건을 명시한 범위에서 실제 시계열
데이터 UPDATE를 지원합니다. LOG 테이블은 UPDATE를 지원하지 않습니다.

### 시간의 역할

RDBMS에서 날짜/시간은 여러 컬럼 중 하나일 뿐입니다. 시간 범위 조회에는 일반적으로 B-Tree 인덱스를 사용하지만, 시간이 데이터의 주축으로 설계된 것은 아닙니다.

Machbase의 시계열 테이블에서 시간은 구조의 중심입니다. LOG 테이블은 `_arrival_time`을 자동으로 관리하고, TAG 테이블은 BASETIME 컬럼을 시간 축으로 사용합니다. 파티션도 시간 기준으로 나뉘고, ROLLUP 집계도 시간 단위(SEC/MIN/HOUR)로 수행됩니다. 반면 LOOKUP, VOLATILE, RDB 테이블은 업무 기준 정보나 관계형 데이터를 위한 테이블이므로 필수 시간축을 갖지 않습니다.

### 인덱싱 구조

RDBMS의 기본 인덱스는 B-Tree입니다. 특정 키 값을 빠르게 찾는 랜덤 액세스에 강하지만, 대량 순차 삽입에서는 트리 재균형 비용이 발생합니다.

Machbase의 LOG 테이블은 필요할 때 LSM(Log-Structured Merge-tree) 계열 인덱스를 생성해 순차 입력과 검색을 조합합니다. TAG 테이블은 태그명 → 시간 파티션 → 값의 3단계 자동 파티션 인덱스를 사용합니다. LOOKUP/VOLATILE/RDB 테이블은 기준 정보나 관계형 조회를 위해 각각의 키/인덱스 구조를 사용하므로, LOG/TAG와 같은 시계열 인덱스 모델로 설명하지 않습니다.

### 저장 방식: 행 지향 vs 컬럼 지향

| 항목 | RDBMS (행 지향) | Machbase 시계열 테이블 (컬럼 지향) |
| --- | --- | --- |
| 저장 단위 | 행 전체를 연속으로 저장 | 같은 컬럼값들을 연속으로 저장 |
| INSERT 성능 | 빠름 | 매우 빠름 (append) |
| 특정 컬럼 집계 | 불필요한 컬럼도 읽어야 함 | 해당 컬럼만 읽음 |
| 압축률 | 낮음 (2~5배) | 높음 (10~100배) |
| 전형적 사용 사례 | 업무 트랜잭션, 단건 조회 | 시계열 집계, 분석 쿼리 |

시계열 데이터는 같은 센서의 온도값처럼 유사한 값이 반복되는 경향이 있습니다. 컬럼 단위로 저장하면 이런 패턴이 압축에 매우 유리하게 작용합니다.

### UPDATE / DELETE 제한

LOG 테이블은 UPDATE를 지원하지 않습니다. TAG 테이블은 Standard Edition에서 태그 선택자와
시간축 조건으로 대상 범위를 한정한 data UPDATE를 지원하지만, `name`(PRIMARY KEY)과
`time`(BASETIME)은 변경할 수 없습니다. 메타데이터는 `UPDATE ... METADATA` 구문으로 별도
수정합니다.

자주 수정되는 운영 상태 데이터라면 LOOKUP 또는 VOLATILE 테이블을 활용하고, 계측값 정정은
TAG data UPDATE와 롤업 재구성 절차를 함께 계획합니다.

### 사용 사례 비교

| 사용 사례 | 적합한 선택 |
| --- | --- |
| 공장 설비 계측값 수집 및 집계 | Machbase TAG 테이블 |
| 서버 이벤트 로그, 알람 이력 | Machbase LOG 테이블 |
| 고객 주문 정보, 재고 관리 | 범용 RDBMS |
| 제품 마스터, 센서 메타데이터 | Machbase LOOKUP 테이블 |
| 시계열 데이터 + 관계형 기준 정보 혼합 | Machbase TAG/LOG + RDB 테이블 또는 외부 RDBMS 연계 |

### 다음 읽을 내용

- [Standard Edition과 Cluster Edition 차이](/dbms/core-concepts/concepts-edition/#differences-standard-edition-cluster) — 단일 노드 vs 분산 클러스터 선택
- [데이터 모델 개념](/dbms/core-concepts/concepts/) — 시계열 데이터의 본질과 append-only 설계
- [컬럼형 저장과 압축](/dbms/core-concepts/storage-execution-architecture/#storage-columnar-compression-column) — 컬럼 저장 구조의 상세 내용
