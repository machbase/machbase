---
type: docs
title: '온라인 업그레이드'
weight: 10
toc: true
---

온라인 업그레이드는 실행 중인 클러스터에서 Broker와 Warehouse를 순차적으로 업그레이드하는
방식입니다. Coordinator, Deployer, Lookup까지 포함한 전체 바이너리 교체가 필요하면
[전체 중지 업그레이드](/kr/dbms/installation-deployment-upgrade/upgrade/cluster-edition/full-stop/)를 사용합니다.

## 업그레이드 절차

### 1. cluster.yaml의 패키지 변경

`cluster.package.name`과 `cluster.package.origin_path`를 새 패키지로 변경합니다. 패키지 내용이 바뀌면
패키지 이름과 archive 파일 이름도 함께 고유하게 바꿉니다.

```yaml
cluster:
  package:
    name: machbase-v8.6.0
    origin_path: /home/machbase/packages/machbase-cluster-8.6.0.official-LINUX-X86-64-release.tgz
```

`registered_path`는 `machclusterctl export`가 기록하는 Coordinator package repository 경로입니다.
업그레이드 입력 archive를 지정할 때는 `origin_path`를 사용합니다.

### 2. 실행 계획 확인

```bash
machclusterctl upgrade -f cluster.yaml --online --dry-run --verbose
```

### 3. 온라인 업그레이드 실행

```bash
machclusterctl upgrade -f cluster.yaml --online --yes --verbose
```

`--online`을 생략하면 online 모드로 처리되지만, 운영 절차를 명확히 하기 위해 옵션을 명시하는
것을 권장합니다.

### 4. 전체 상태 확인

```bash
machclusterctl status
```

## 수동 업그레이드 참고

`machcoordinatoradmin --upgrade-node`를 직접 사용하는 경우에는 대상 노드와 패키지 이름을 함께
지정합니다.

```bash
machcoordinatoradmin --upgrade-node=192.168.1.11:5401 --package-name=machbase-v8.6.0
```

온라인 대상은 Broker와 Warehouse로 제한합니다. Broker가 하나만 남아 있을 때 해당 Broker를
업그레이드하면 그 시간 동안 클라이언트 접속이 끊길 수 있습니다.

모든 대상 노드가 각 역할에 맞는 정상 상태이고 새 패키지로 동작하면 업그레이드 완료입니다.

---

**다음 읽을 내용**
- [설치 검증 체크리스트](/kr/dbms/installation-deployment-upgrade/validation-checklist/)
