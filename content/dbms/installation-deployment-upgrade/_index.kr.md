---
type: docs
title: '3. 설치, 배포, 업그레이드'
weight: 30
toc: true
---

Machbase를 운영 환경에 배포하려면 에디션 선택부터 설치 준비, 설치, 검증까지 단계를 순서대로 진행해야 합니다. 이 장은 그 전체 흐름을 다룹니다.

## 설치 경로 선택

Machbase는 두 가지 에디션을 제공합니다.

| 에디션 | 대상 환경 | 특징 |
|--------|-----------|------|
| **Standard Edition** | 단일 노드 | 설치가 간단하며 개발·소규모 운영에 적합 |
| **Cluster Edition** | 다중 노드 | Coordinator·Deployer·Lookup·Broker·Warehouse 노드로 구성, 대규모 데이터 수집에 적합 |

에디션 선택 기준은 [에디션 차이점](/dbms/core-concepts/concepts-edition/differences-standard-edition-cluster/)을 참고하십시오.

## 설치 순서

### Standard Edition

1. [설치 전 요구사항](/kr/dbms/installation-deployment-upgrade/pre-install-preparation/pre-install-requirements/) 확인
2. [패키지 구성 이해](/kr/dbms/installation-deployment-upgrade/pre-install-preparation/package/)
3. OS 환경에 맞는 설치 진행
   - [Linux — Tarball 설치](/kr/dbms/installation-deployment-upgrade/standard-edition/linux/tarball/)
   - [Linux — Docker 설치](/kr/dbms/installation-deployment-upgrade/standard-edition/linux/docker/)
   - [Windows — 패키지 설치](/kr/dbms/installation-deployment-upgrade/standard-edition/windows/package/)
4. [라이선스 설치](/kr/dbms/installation-deployment-upgrade/pre-install-preparation/license/)
5. [설치 검증 체크리스트](/kr/dbms/installation-deployment-upgrade/validation-checklist/)

### Cluster Edition

1. [설치 전 요구사항](/kr/dbms/installation-deployment-upgrade/pre-install-preparation/pre-install-requirements/) 확인
2. [클러스터 환경 준비](/kr/dbms/installation-deployment-upgrade/cluster-edition/preparation-environment-cluster-edition/)
3. 배포 방식 선택
   - [machclusterctl 자동 배포](/kr/dbms/installation-deployment-upgrade/cluster-edition/machclusterctl/) — 권장
   - [수동 설치 (machcoordinatoradmin)](/kr/dbms/installation-deployment-upgrade/cluster-edition/manual-machcoordinatoradmin/)
4. [라이선스 설치](/kr/dbms/installation-deployment-upgrade/pre-install-preparation/license/)
5. [설치 검증 체크리스트](/kr/dbms/installation-deployment-upgrade/validation-checklist/)

## 업그레이드

기존 운영 중인 시스템을 새 버전으로 업그레이드하는 절차는 [업그레이드](/kr/dbms/installation-deployment-upgrade/upgrade/) 섹션을 참고하십시오.

---

**다음 읽을 내용**
- [설치 전 준비](/kr/dbms/installation-deployment-upgrade/pre-install-preparation/)
