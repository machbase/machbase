---
type: docs
title: 'YAML 검증'
weight: 20
toc: true
---

`cluster.yaml`을 실제 설치에 사용하기 전에 유효성 검사를 수행합니다. `validate`는 YAML 문법과
필수 값, 별칭, 포트 충돌, 토폴로지 관계를 정적으로 검사합니다.

## 검증 명령

```bash
machclusterctl validate -f cluster.yaml
```

## 검증 항목

| 항목 | 설명 |
|------|------|
| YAML 문법 | 파일 파싱 오류 여부 |
| 환경변수 치환 | `${VAR}` 또는 `${VAR:-default}` 표현식 해석 가능 여부 |
| 필수 필드 | 클러스터 이름, 호스트, 패키지, 노드별 필수 값 누락 여부 |
| 별칭 | 노드 alias 중복 여부 |
| 포트 충돌 | 같은 host 안에서 선언된 포트 충돌 여부 |
| 토폴로지 | Primary Coordinator, Lookup master/monitor, Deployer 참조 관계 |

## 출력 예시

```text
Validation passed.
```

오류가 있으면 메시지에 표시된 항목을 수정한 뒤 재검증합니다.

## 설치 전 실행 계획 확인

SSH 접속, 패키지 파일 존재 여부, 원격 디렉터리 권한 같은 실행 전 점검은 `install` 또는 `apply`의
`--dry-run --verbose` 단계에서 확인합니다.

```bash
machclusterctl install -f cluster.yaml --dry-run --verbose
```

설치 후 구성 변경을 검증할 때는 다음 명령을 사용합니다.

```bash
machclusterctl apply -f cluster.yaml --dry-run --verbose
```

## 일반적인 오류와 해결

| 오류 | 원인 | 해결 |
|------|------|------|
| `field ... not found` | 지원하지 않는 YAML 키 사용 | 현행 스키마의 `cluster.*` 항목으로 수정 |
| `required field ...` | 필수 값 누락 | 메시지에 표시된 필드를 추가 |
| `duplicate alias` | 노드 alias 중복 | 모든 노드 alias를 고유하게 변경 |
| `port conflict` | 같은 host에서 동일 포트 사용 | 해당 노드의 포트 또는 `home_path`를 명시적으로 분리 |
| `deployer ... not found` | Lookup/Broker/Warehouse가 존재하지 않는 Deployer를 참조 | `deployer` 값을 Deployer alias 또는 host:port로 수정 |

---

**다음 읽을 내용**
- [최초 설치](/dbms/installation-deployment-upgrade/cluster-edition/machclusterctl/initial/)
