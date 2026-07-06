---
type: docs
title: 'Cluster Edition 설치와 배포'
weight: 30
---

Cluster Edition은 여러 노드에 Machbase를 분산 배포하는 구성입니다. 대용량 시계열 데이터 수집이 필요한 산업 IoT·금융 tick 환경에 적합합니다.

## 노드 역할

| 노드 | 역할 |
|------|------|
| **Coordinator** | 클러스터 메타 정보 관리, 노드 상태 감시 |
| **Deployer** | 패키지 배포 및 노드 초기화 중계 |
| **Broker** | SQL 파싱 및 쿼리 분배, 클라이언트 접점 |
| **Warehouse** | 실제 데이터 저장 및 쿼리 실행 |

최소 구성은 Coordinator 1, Deployer 1, Broker 1, Warehouse 2(그룹당 2노드로 복제) 입니다.

## 배포 방식

| 방식 | 설명 | 적합한 경우 |
|------|------|------------|
| [machclusterctl](/dbms/installation-deployment-upgrade/cluster-edition/machclusterctl/) | cluster.yaml 기반 자동 배포 | 권장. 신규 구축 |
| [수동 (machcoordinatoradmin)](/dbms/installation-deployment-upgrade/cluster-edition/manual-machcoordinatoradmin/) | 각 노드에 직접 패키지 배포 | 세밀한 제어가 필요한 경우 |

## 설치 순서

1. [Cluster Edition 구성 개요](/dbms/installation-deployment-upgrade/cluster-edition/cluster-edition/) 숙지
2. [환경 준비](/dbms/installation-deployment-upgrade/cluster-edition/preparation-environment-cluster-edition/) (SSH 키, 커널 파라미터, NTP)
3. 배포 방식 선택 후 설치 진행
4. [라이선스 설치](/dbms/installation-deployment-upgrade/pre-install-preparation/license/)
5. [설치 검증](/dbms/installation-deployment-upgrade/validation-checklist/)

---

**다음 읽을 내용**
- [Cluster Edition 구성 개요](/dbms/installation-deployment-upgrade/cluster-edition/cluster-edition/)
