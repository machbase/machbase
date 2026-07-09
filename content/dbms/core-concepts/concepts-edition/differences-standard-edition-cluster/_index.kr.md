---
type: docs
title: 'Standard Edition과 Cluster Edition 차이'
weight: 10
---

Machbase DBMS는 운영 규모와 가용성 요구사항에 따라 두 가지 Edition으로 제공됩니다. Standard Edition은 단일 서버에서 운영하고, Cluster Edition은 여러 노드에 데이터를 분산해 처리합니다.

## Standard Edition

Standard Edition은 하나의 프로세스로 동작하는 단일 노드 구성입니다. 설치와 운영이 간단하고, 소규모에서 중규모 시계열 데이터를 처리하는 데 충분한 성능을 제공합니다.

- 단일 `machbase` 프로세스로 SQL 엔진, 저장 관리자, 프로세스 관리자를 모두 포함
- 별도의 분산 코디네이션 없이 즉시 사용 가능
- ROLLUP, STREAM, Retention Policy, Backup/Mount, RDB 테이블 등 대부분의 기능 지원

초당 수십만 건의 입력과 수 TB 규모의 데이터를 단일 서버에서 처리할 수 있습니다.

## Cluster Edition

Cluster Edition은 여러 서버에 데이터를 분산 저장하고 병렬로 처리합니다. 내부적으로 `EDITION_CLUSTER` 컴파일 플래그로 분리된 별도 빌드이며, 주요 노드는 다음과 같이 구성됩니다.

| 노드 유형 | 역할 |
| --- | --- |
| Coordinator | 클러스터 메타데이터 관리, 노드 상태 감시, 쿼리 라우팅 결정 |
| Deployer | 소프트웨어 배포 및 노드 초기화 담당 |
| Broker | 클라이언트 연결 수신, 쿼리를 Warehouse 노드로 분산 |
| Warehouse | 실제 데이터 저장 및 쿼리 실행 담당 |
| Lookup | 클러스터 환경의 LOOKUP 테이블 처리 담당 |

클라이언트는 항상 Broker 노드에 접속하며, Broker가 쿼리를 분석해 해당 데이터를 보유한 Warehouse 노드에 요청을 전달합니다.

## 기능 지원 차이

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

## 선택 기준

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

## 다음 읽을 내용

- [기존 RDBMS와의 차이](../differences-rdbms/) — Machbase 설계 철학의 전체 맥락
- [Machbase 아키텍처 개요](/dbms/core-concepts/storage-execution-architecture/architecture-machbase/) — Standard/Cluster 구조의 내부 상세
