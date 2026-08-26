---
type: docs
title: '2.4 Edition 개념'
weight: 40
toc: true
---
Machbase DBMS는 PostgreSQL이나 MySQL 같은 범용 RDBMS와 설계 철학부터 다릅니다. 그 차이를 명확히 이해하고 운영 규모에 따라 올바른 Edition을 선택하는 데 필요한 개념을 다룹니다.

- **[Standard Edition과 Cluster Edition 차이](/dbms/core-concepts/concepts-edition/#differences-standard-edition-cluster)** -- 단일 노드 구성과 분산 클러스터 구성의 구조적 차이, 기능 지원 범위, 선택 기준
- **[기존 RDBMS와의 차이](/dbms/core-concepts/concepts/#differences-rdbms)** -- append 중심 시계열 모델과 관계형 workload의 차이


<a id="differences-standard-edition-cluster"></a>

## Standard Edition과 Cluster Edition 차이

운영 규모와 가용성 요구사항에 따라 두 가지 Edition을 제공합니다. Standard Edition은 단일 서버, Cluster Edition은 여러 노드에 데이터를 분산 처리합니다.

### Standard Edition

단일 노드에서 동작하는 구성입니다. 설치와 운영이 단순하며 TRANSACTION, VOLATILE,
Restore/Mount 등 Standard Edition 기능을 함께 사용할 수 있습니다.

- 단일 서버 인스턴스로 SQL 처리와 데이터 저장 기능 제공
- 별도 분산 코디네이션 없이 즉시 사용 가능
- ROLLUP, Retention Policy, Backup/Mount, TRANSACTION 테이블 등 대부분의 기능 지원

### Cluster Edition

여러 서버에 데이터를 분산 저장하고 병렬로 처리합니다. Coordinator, Deployer, Broker,
Warehouse, Lookup 노드로 역할을 분리합니다.

| 노드 유형 | 역할 |
| --- | --- |
| Coordinator | 클러스터 메타데이터 관리, 노드 상태 감시, 쿼리 라우팅 결정 |
| Deployer | 소프트웨어 배포 및 노드 초기화 |
| Broker | 클라이언트 연결 수신, 쿼리를 Warehouse 노드로 분산 |
| Warehouse | 실제 데이터 저장 및 쿼리 실행 |
| Lookup | 클러스터 환경의 LOOKUP 테이블 처리 |

클라이언트는 항상 Broker 노드에 접속하며, Broker가 쿼리를 분석해 해당 데이터를 보유한 Warehouse 노드에 요청을 전달합니다.

### 기능 지원 차이

대부분의 기능은 두 Edition에서 동일하게 동작하지만, 일부 지원 범위가 다릅니다.

| 기능 | Standard Edition | Cluster Edition |
| --- | --- | --- |
| LOG/TAG/LOOKUP 테이블 | 모두 지원 | 모두 지원 |
| VOLATILE 테이블 | 지원 | 지원 |
| TRANSACTION 테이블 | 지원 | 미지원 |
| ROLLUP | 지원 | 지원 |
| Retention Policy | 지원 | 지원 |
| Backup | 지원 | 지원 |
| Restore / Mount | 지원 | 미지원 |
| 수평 확장 (노드 추가) | 불가 | 가능 |
| 자동 장애 조치 | 불가 | Coordinator가 감시 |

TRANSACTION 테이블과 Restore/Mount는 Standard Edition 전용 기능입니다. VOLATILE 테이블은
두 Edition에서 지원하지만 서버·노드 lifecycle에 따른 데이터 소멸 범위는 배포 구성에서
별도로 검증해야 합니다.

### 선택 기준

**Standard Edition이 적합한 경우**

- 단일 서버 또는 온프레미스 소규모 배포
- 단일 서버의 CPU, 메모리, 스토리지 범위에서 처리 가능한 워크로드
- 관리 인력이 적고 운영 단순성이 중요한 경우
- 개발, 테스트, 파일럿 환경

**Cluster Edition이 적합한 경우**

- 단일 서버의 처리량이나 저장 용량을 넘어 수평 확장이 필요한 워크로드
- 저장 용량이 단일 서버의 한계를 넘는 경우
- 노드 장애 시에도 서비스를 유지해야 하는 고가용성 요구사항
- 데이터 볼륨 증가에 따라 노드를 추가해야 하는 탄력적 확장 필요

### 다음 읽을 내용

- [기존 RDBMS와의 차이](/dbms/core-concepts/concepts/#differences-rdbms) -- Machbase 설계 철학의 전체 맥락
- [Machbase 아키텍처 개요](/dbms/core-concepts/storage-execution-architecture/#architecture-machbase) -- Standard/Cluster 구성 개요


## 관련 문서

시계열 데이터와 범용 RDBMS의 모델 차이는 [데이터 모델 개념](../concepts/#differences-rdbms)을 참고하십시오.
