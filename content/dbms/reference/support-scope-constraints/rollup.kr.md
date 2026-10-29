---
type: docs
title: '16.6.6 ROLLUP 지원 범위'
weight: 60
toc: true
aliases:
  - /dbms/tag-rollup-usage/support-scope-rollup/
---

<a id="support-scope-rollup-rebuild-cluster"></a>

## Edition과 테이블 범위

| 기능 | Standard | Cluster |
|---|:---:|:---:|
| 시간축 TAG의 일반·조건·확장 ROLLUP 생성·조회·제어 | O | O |
| WITH ROLLUP 자동 생성 | O | O |
| 지원 JSON 경로·문서 전체 집계 | O | O |
| Custom INTO...AS | O | X |
| ROLLUP_REBUILD | 제한된 대상·인수에서 지원 | X |

거리축 TAG, LOG, TRANSACTION, VOLATILE, LOOKUP에 시간축 ROLLUP을 적용하지 않습니다.
Cluster의 상태는 관련 노드와 계층별로 확인합니다.

## 생성 유형과 컬럼

| 유형 | 필요한 조건 |
|---|---|
| 일반 숫자 | 지원 숫자 DATA 컬럼; 명시 생성 시 SUMMARIZED는 필수가 아님 |
| JSON 경로 | JSON DATA 컬럼과 집계할 숫자 경로 |
| JSON 문서 전체 | JSON SUMMARIZED 컬럼 |
| WITH ROLLUP | 시간축 TAG의 세 번째 SUMMARIZED 컬럼 |
| FROM 계층 | 더 큰 정수배 간격과 동일한 확장·모드 조건 |
| Custom | 소스 시간축 TAG 하나, 사전 생성한 호환 대상 TAG |

## 집계와 선택

일반 숫자 ROLLUP은 MIN/MAX/SUM/COUNT/AVG/SUMSQ, 확장은 FIRST/LAST를 추가로
제공합니다. Custom의 부분 결과는 사용자가 재집계합니다. 평균은 합계와 유효 건수로,
FIRST/LAST는 대응 원본 시각과 사용하는 보조 정렬 키를 함께 유지해 합칩니다.
JSON 문서 전체의 COUNT는 저장된 집계 건수이며 원본 COUNT(value)와 무조건 같지 않습니다.

후보 선택은 조건·컬럼·경로·모드·간격에 따릅니다. 일반/확장만으로 우선순위를 단정하거나,
일 버킷에 24 HOUR ROLLUP이 자동 적용된다고 가정하지 않습니다.
[조회 규칙](../../../tag-rollup-usage/query-syntax-rollup/)을 확인합니다.

## REBUILD는 생성 지원과 다름

완전한 자동 SEC/MIN/HOUR 계층과 지원 Custom 경로를 대상으로 합니다. 임의 수동 이름,
부분 자동 계층, 10 MIN Custom 등 생성 가능한 모든 구성을 재구성할 수 있는 것은 아닙니다.
현재 Custom 시간 경계 처리 간격은 1 SEC·1 MIN·1 HOUR이며 SELECT의 버킷과도 맞아야 합니다.
상수 시각 인수, 버킷 전체 확장, 상태 전환과 오류 후 확인은
[REBUILD 레퍼런스](../../sql/syntax/rollup-rebuild-syntax/)를 따릅니다.

## 권한

작업 계정에는 대상 데이터베이스 접속과 생성·삭제·조회 등 필요한 권한을 부여합니다.
다음은 존재하는 작업 계정에 생성·삭제 권한을 부여하는 예시이며 모든 필요 권한을
한 번에 구성하는 스크립트는 아닙니다.

```sql
GRANT CREATE, DROP ON DATABASE MACHBASEDB TO rollup_user;
```

[권한 관리](../../../security-access-control/privileges/)에서 소유자와 작업 범위를
확인하십시오.

## 복합 키 FIRST/LAST 지원 범위

> 복합 키 FIRST/LAST와 정렬 EXTENSION ROLLUP은 Machbase 8.7.3부터 지원합니다. 에디션별 제약은 아래 설명을 확인하십시오.

복합 키 원본 조회와 숫자 대상의 정렬 EXTENSION ROLLUP은 8.7.3부터 Standard·Cluster에서 지원합니다.
Custom ROLLUP 생성과 worker는 Standard 전용이며 Cluster에서는 `ERR-02837`을 반환합니다.
일반 TAG에 이미 저장된 요약 행을 복합 FIRST/LAST로 재집계하는 SELECT는 Cluster에서도
일반 TAG 분산 조회로 지원합니다. 정렬 ROLLUP 정의의 첫 키는 BASETIME이어야 하지만,
일반 TAG 재집계에서 사용하는 원본 후보 시각에 이 제한을 적용하지는 않습니다.

공개 ROWID 보조 키는 Standard 전용이며 명시적으로 지정합니다. 원본 행 식별자를 보존하되
입력 순서를 뜻하지 않고 기존 ROWID 제한을 유지합니다. Cluster는 지원하지 않습니다.
DECIMAL 정렬 키도 지원합니다. 조회의 키·방향은 저장 정의와 맞아야 합니다.
Cluster의 모든 노드에 같은 지원 빌드를 배포해야 하며 혼합 바이너리는 지원하지 않습니다.

정렬 ROLLUP이 있는 DB를 기능이 없는 이전 바이너리로 열거나 MOUNT하는 운영은
메타 버전 검사를 통과하더라도 지원하지 않습니다. 되돌릴 때는 도입 전 백업을 복원하며,
정렬 객체를 DROP하는 것만으로 역호환성이 보장되지는 않습니다.
[전환·되돌리기 제약](../../../tag-rollup-usage/extension-rollup/#ordered-rollup-compatibility)을 확인하십시오.

[전체 데이터와 정렬 ROLLUP 예제](../../../tag-rollup-usage/extension-rollup/#composite-first-last).
