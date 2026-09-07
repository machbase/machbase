---
type: docs
title: '3. 설치, 배포, 업그레이드'
weight: 30
toc: true
---

이 장에서는 Machbase DBMS 8.7.0을 설치하고, 데이터 입력과 조회가 가능한 상태인지
확인합니다. 새 서버를 준비하는 작업과 기존 데이터를 유지하면서 업그레이드하는 작업은
출발점이 다릅니다. 먼저 필요한 기능과 배포 환경을 정하고 자신의 상황에 맞는 절차를 선택합니다.

2장에서 살펴본 데이터 모델과 Edition의 차이는 설치에도 영향을 줍니다. TRANSACTION
테이블이나 Restore·Mount가 필요하다면 Standard Edition의 지원 범위를 확인합니다.
분산 저장과 복제가 필요하다면 Cluster의 노드 역할, 네트워크와 장애 대응을 함께 설계합니다.

## 설치 경로 선택

| 에디션 | 배포 구조 | 선택할 때 확인할 점 |
|---|---|---|
| Standard Edition | 하나의 DBMS 서버가 SQL 처리와 저장 수행 | 필요한 기능과 입력·조회·보관 부하를 서버 자원으로 처리할 수 있는지 확인 |
| Cluster Edition | Coordinator·Deployer·Lookup·Broker·Warehouse 역할 분리 | 분산 그룹, 복제, 통신 경로와 노드 운영 절차를 함께 준비할 수 있는지 확인 |

단일 서버가 소규모 데이터만 처리할 수 있다는 뜻은 아닙니다. 필요한 저장량과 성능을
대표 데이터로 측정한 뒤 판단합니다. 반대로 Cluster도 노드 수만 늘리면 모든 쿼리가
비례해서 빨라지는 것은 아닙니다. 자세한 선택 기준은
[에디션 차이점](/dbms/core-concepts/concepts-edition/#differences-standard-edition-cluster)을
참고하십시오.

### 설치 전에 구분할 대상

| 대상 | 의미 | 확인할 예 |
|---|---|---|
| 배포 패키지 | 실행 파일, 라이브러리와 샘플 설정 | 버전·Edition·OS·CPU 아키텍처 |
| 설치 홈 | 한 서버나 노드가 사용하는 실행·설정 경로 | `MACHBASE_HOME`, `conf/machbase.conf` |
| 데이터 저장 경로 | DBMS가 실제 데이터를 읽고 쓰는 위치 | `DBS_PATH`, 여유 공간과 접근 권한 |
| 서버 인스턴스·노드 | 해당 설정으로 실행되는 DBMS 프로세스 | 기동 상태, 로그와 접속 포트 |
| 논리 데이터베이스 | 접속 후 SQL 객체를 생성하고 사용하는 공간 | 현재 데이터베이스, 사용자·권한·테이블 |

패키지 압축 해제, 새 인스턴스의 데이터베이스 생성, 서버 시작과 테이블 생성은 서로 다른
단계입니다. 기존 데이터가 있는 홈에 신규 설치용 초기화 명령을 실행하지 마십시오.
설치 홈과 실제 데이터 경로도 다를 수 있으므로 백업·업그레이드 전에 둘 다 확인합니다.

SQL에서 사용하는 논리 데이터베이스는 설치 홈과 별개의 개념입니다.
여러 데이터베이스를 운용할 때의 선택·생성·권한은
[다중 데이터베이스 운영](/dbms/operations-configuration-recovery/multi-database/)에서 설명합니다.

## 설치 순서

### Standard Edition

1. [설치 전 준비](./pre-install-preparation/)에서 패키지, 서버 계정, 자원과 포트를 확인합니다.
2. 운영체제에 맞는 설치 절차에서 전용 홈과 환경 변수를 준비합니다.
   - [Linux — Tarball 설치](./standard-edition/#linux-tarball)
   - [Linux — Docker 설치](./standard-edition/#linux-docker)
   - [Windows — 패키지 설치](./standard-edition/#windows-package)
3. 설정과 데이터 경로를 확인하고, 별도 라이선스를 사용할 경우 최초 기동 전에
   [라이선스 설치](./pre-install-preparation/#license)를 수행합니다.
4. 선택한 설치 절차에 따라 새 데이터베이스를 생성하고 서버를 시작합니다.
5. [설치 검증 체크리스트](./validation-checklist/)에서 프로세스·포트·접속·버전·라이선스와
   소량 데이터의 입력·조회를 확인합니다.

컨테이너를 사용하는 경우에도 패키지의 버전, 데이터 볼륨과 실행 계정의 쓰기 권한을
확인해야 합니다. 컨테이너 시작과 DBMS 초기화·시작의 관계는 사용하는 이미지에 따라
다르므로 해당 설치 절차를 따릅니다.

### Cluster Edition

1. [설치 전 준비](./pre-install-preparation/)와
   [클러스터 환경 준비](./cluster-edition/#preparation-environment-cluster-edition)를 확인합니다.
2. 노드별 호스트, 홈, SQL·관리·노드 간 통신 포트와 Warehouse 복제 그룹을 정합니다.
3. 사용할 패키지와 라이선스를 준비하고 배포 방식을 선택합니다.
   - [machclusterctl 배포](./cluster-edition/#machclusterctl): 구성 파일로 배포하고 실행 계획 확인
   - [수동 설치](./cluster-edition/#manual-machcoordinatoradmin): 관리 도구로 단계별 등록·기동
4. 노드 역할에 맞는 상태와 복제 구성을 확인하고 Broker에 SQL로 접속합니다.
5. [설치 검증 체크리스트](./validation-checklist/)에서 데이터 입력·조회와 그룹 내 복제 상태를
   구분해 점검합니다.

SQL 접속이 성공하는 것과 모든 복제본이 정상인 것은 별개의 확인입니다. 서로 다른
Warehouse 그룹이 반드시 같은 데이터를 가지는 것도 아닙니다. 장애 대응은
[Cluster 운영](/dbms/operations-configuration-recovery/cluster/)으로 이어서 확인합니다.

## 업그레이드

기존 시스템은 [업그레이드](./upgrade/)의 절차를 사용합니다. 새 패키지의 실행 가능 여부뿐
아니라 데이터 파일, SQL·SDK, 설정·라이선스와 백업·복구 경로의 호환성을 점검합니다.
운영 설정을 새 패키지의 샘플로 덮어쓰거나, 실행 파일을 바꾼 것만으로 업그레이드가
완료됐다고 판단하지 마십시오.

업그레이드 전의 기준 측정값과 백업을 확보하고, 격리 환경에서 복구에 필요한 시간도
확인합니다. “이전 버전으로 돌아갈 수 있다”는 판단에는 바이너리뿐 아니라 이전 버전이
읽을 수 있는 데이터와 설정이 필요합니다.

## 다음 단계

설치 검증은 운영 준비의 시작입니다. 먼저 [빠른 시작](/dbms/getting-started/quick-start/)으로
SQL 흐름을 익히고, [테이블 타입 선택과 스키마 설계](../data-modeling-table-design/)에서
실제 데이터를 모델링합니다. 운영 투입 전에는 전용 계정, 수집 오류 처리, 보관·백업,
대표 부하 시험과 관측 지표를 준비합니다.

[운영 체크리스트](/dbms/operations-configuration-recovery/checklist/)와
[성능 튜닝 접근법](/dbms/performance-tuning/performance-approach/)에서 그 과정을 안내합니다.
