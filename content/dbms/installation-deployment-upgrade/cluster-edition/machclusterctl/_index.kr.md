---
type: docs
title: 'machclusterctl 기반 배포'
weight: 30
toc: true
---

`machclusterctl`은 `cluster.yaml` 파일 하나로 전체 클러스터를 자동으로 배포하고 관리하는 도구입니다. SSH를 통해 각 노드에 원격 접속하여 패키지 배포, 초기화, 시작·종료를 일괄 처리합니다.

## 사전 조건

- 배포 서버에서 모든 노드로 SSH 키 기반 인증이 설정되어 있어야 합니다.
- [Cluster Edition 설치 환경 준비](/kr/dbms/installation-deployment-upgrade/cluster-edition/preparation-environment-cluster-edition/) 완료

## 작업 순서

| 단계 | 문서 |
|------|------|
| 1. cluster.yaml 작성 | [cluster.yaml 작성](/kr/dbms/installation-deployment-upgrade/cluster-edition/machclusterctl/cluster-yaml/) |
| 2. YAML 유효성 검사 | [YAML 검증](/kr/dbms/installation-deployment-upgrade/cluster-edition/machclusterctl/validation-yaml/) |
| 3. 최초 설치 및 시작 | [최초 설치](/kr/dbms/installation-deployment-upgrade/cluster-edition/machclusterctl/initial/) |
| 4. 상태 확인 | [상태 확인](/kr/dbms/installation-deployment-upgrade/cluster-edition/machclusterctl/status-check-state/) |
| 5. (이후) 구성 변경 | [구성 변경 적용](/kr/dbms/installation-deployment-upgrade/cluster-edition/machclusterctl/configuration-change-alter/) |
| 6. (장애 시) 복구 | [배포 실패 시 복구](/kr/dbms/installation-deployment-upgrade/cluster-edition/machclusterctl/failure-recovery/) |

---

**다음 읽을 내용**
- [cluster.yaml 작성](/kr/dbms/installation-deployment-upgrade/cluster-edition/machclusterctl/cluster-yaml/)
