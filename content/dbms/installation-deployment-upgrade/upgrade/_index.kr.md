---
type: docs
title: '업그레이드'
weight: 40
toc: true
---

운영 중인 Machbase를 새 버전으로 업그레이드하는 절차를 설명합니다. 에디션과 업그레이드 방식에 따라 절차가 다릅니다.

## 업그레이드 전 확인사항

- 현재 버전과 대상 버전의 호환성을 확인합니다. Minor 버전이 다른 경우 DB 파일 형식이 변경될 수 있습니다.
- 업그레이드 전 백업을 수행합니다. [백업 방법](/dbms/operations-configuration-recovery/backup-restore-mount/backup/) 참고.
- 진행 중인 INSERT·APPEND 클라이언트를 확인합니다.

## 업그레이드 경로

| 에디션 | 방식 | 링크 |
|--------|------|------|
| Standard Edition | 서버 종료 후 패키지 교체 | [Standard Edition 업그레이드](/dbms/installation-deployment-upgrade/upgrade/standard-edition/) |
| Cluster Edition | Broker/Warehouse 순차 업그레이드 | [온라인 업그레이드](/dbms/installation-deployment-upgrade/upgrade/cluster-edition/online/) |
| Cluster Edition | 전체 중지 | [전체 중지 업그레이드](/dbms/installation-deployment-upgrade/upgrade/cluster-edition/full-stop/) |

Cluster Edition의 경우 데이터 가용성 요구사항에 따라 온라인 또는 전체 중지 방식을 선택합니다.

---

**다음 읽을 내용**
- [Standard Edition 업그레이드](/dbms/installation-deployment-upgrade/upgrade/standard-edition/)
