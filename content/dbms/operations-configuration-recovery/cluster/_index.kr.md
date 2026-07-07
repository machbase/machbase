---
type: docs
title: 'Cluster 운영'
weight: 70
---

Machbase Cluster Edition은 대규모 시계열 데이터를 여러 노드에 분산 저장·처리하는 아키텍처입니다. 이 섹션에서는 클러스터 구성 요소의 역할과 운영 도구 사용법, 장애 복구 절차를 설명합니다.

## 클러스터 노드 구성

| 노드 유형 | 역할 | 비고 |
|-----------|------|------|
| **Coordinator** | 클러스터 전체 메타데이터·토폴로지 관리, 노드 상태 감시 | 클러스터당 1~2개 (Primary/Secondary) |
| **Deployer** | 패키지 배포, 노드 설치·업그레이드 자동화 | 호스트당 1개 |
| **Broker** | 클라이언트 연결 수신, 쿼리 라우팅 | 1개 이상 (HA 시 복수) |
| **Warehouse** | 실제 데이터 저장·처리 노드 | 그룹 단위로 복수 배치 |
| **Lookup** | 참조 데이터(룩업 테이블) 저장 | 선택적 구성 |

## 주요 운영 도구

| 도구 | 설명 |
|------|------|
| `machclusterctl` | 클러스터 전체를 대상으로 한 통합 시작·종료·상태 확인 CLI |
| `machcoordinatoradmin` | Coordinator 및 개별 노드 세부 관리 CLI |
| `machadmin` | 개별 Warehouse/Broker 노드의 프로세스 관리 |

## 이 섹션의 구성

| 주제 | 내용 |
|------|------|
| [Cluster 상태 확인](./status-check-state-cluster/) | 전체 클러스터 상태 및 노드별 상태 조회 |
| [machclusterctl connect/export](./machclusterctl-connect-export/) | 클러스터 접속 및 설정 내보내기 |
| [Cluster 노드 시작과 종료](./node-start-cluster/) | 개별 노드 기동·종료 절차 |
| [machclusterctl start/stop/destroy](./machclusterctl-start-stop-destroy/) | 클러스터 전체 시작·종료·삭제 |
| [Cluster 노드 추가와 제거](./node-cluster/) | 운영 중 노드 확장·축소 |
| [Cluster 그룹 상태 변경](./state-alter-status-cluster/) | 유지보수 모드 전환, 그룹 상태 변경 |
| [Warehouse 상태 복구](./recovery-state-status-warehouse/) | Warehouse 노드 장애 복구 절차 |
| [Cluster 운영 제한사항](./limitations-cluster/) | 단일 에디션 대비 제한 기능 목록 |

## Cluster Edition 전용 제약사항

Cluster Edition에서는 다음 기능이 지원되지 않습니다.

- **RDB 테이블** 미지원
- **Custom ROLLUP** 미지원
- **ROLLUP_REBUILD** 미지원
- `MOUNT`/`UMOUNT`, Stream/CQL 등 일부 Standard Edition 기능 제한
- 일부 `ALTER TABLE` 기능 제한

자세한 내용은 [Cluster 운영 제한사항](./limitations-cluster/)을 참조하십시오.
