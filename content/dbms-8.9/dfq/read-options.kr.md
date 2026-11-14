---
type: docs
title: '12.3 READ 공통 사용법'
weight: 30
toc: true
---

옵션은 각각 `'name=value'` SQL 문자열로 전달합니다. 입력 설정의 JSON 객체와 결과의
DATA·_META·DETAILS JSON 표현을 혼동하지 않습니다. `config={...}` 입력은 허용하지 않습니다.

```text
READ('파일' [, '추가 파일' ...] [, '옵션=값' ...])
READ('source=파일' [, '옵션=값' ...])
READ('sources=파일1,파일2' [, '옵션=값' ...])
```

위 세 파일 지정 방식을 혼합하지 않습니다. 위치형 파일은 첫 옵션보다 앞에만 둡니다.
등호가 들어간 파일명은 source=로 명시합니다. SQL 입력은 [12.7](../sql-source/)의 별도 규칙입니다.

## 공통 옵션

| 옵션 | 기본값·범위 | 적용과 의미 |
|---|---|---|
| source / sources | 입력 필수 | 서버 파일 또는 지원되는 source 주소·순서 있는 파일 목록 |
| contract | 1 | 지원되는 계약 버전만 허용 |
| format | auto | 등록된 reader를 선택. 명시값은 해당 reader로 고정 |
| profile | 미지정 | name@version의 고정 설정. 이미 고정된 설정을 중복 지정하면 충돌 가능 |
| mode | data | data/list/schema/elements/nodes/raw/inspect |
| columns | reader별 native/envelope | data와 설명 결과의 출력 방식 |
| target | reader별 기본 대상 | list에서 반환한 정확한 ID |
| row | 미지정, 0 이상 | 명시 target의 원래 부모 행 하나. WHERE·정렬 후 번호가 아님 |
| field | 미지정 | 선택할 논리 경로. elements에서는 배열 경로 필요 |
| time | 매핑별 값 | reader가 선언한 시각 역할. CSV 등에 임의 적용 금지 |
| axis | 적용 가능한 dense 매핑에서 0 | reader의 축 선택. 임의 reshape 기능이 아님 |
| view | inspect에서 columns | reader가 제공하는 inspect 결과 선택 |
| describe.mode | data | inspect에서 설명할 READ 결과 모드 |
| project.* | 미지정 | 별칭에 선언된 원래 필드 경로를 연결해 출력 구성 |
| column.* | 미지정 | 기존 결과 뒤에 data.경로 또는 지원되는 meta.키 추가 |
| source.consistency | best_effort / strong | 원본 일관성 정책 |
| source.expected_revision | 미지정 | 재조회 시 원본 revision 검사 |
| source.expected_mapping | 미지정 | reader·profile·유효 해석 설정 검사 |
| raw.representation | stored | 원본 또는 포맷별 지원 표현. [추출](../extract/) 참고 |
| raw.chunk_bytes | 65536, 1~1048576 | raw 결과의 청크 바이트 상한 |

## 결과 모드와 적용 조건

| 모드 | 용도 | 주요 조건 |
|---|---|---|
| data | native 컬럼 또는 envelope | 선택한 target의 반환 계약 적용 |
| list | 대상과 capability | 데이터 행 자체의 SELECT와 구분 |
| schema | 선언 구조 | 원본 타입과 native SQL 타입 구분 |
| inspect | 관계형 설명·진단 | view별 입력 조건 적용 |
| elements | 배열 원소 | 명시 target과 배열 field 필요 |
| nodes | 구조의 노드·경로 | scalar/배열/객체와 값 상태 구분 |
| raw | 바이트 청크 | stored와 논리 표현의 허용 조합 구분 |

field 경로는 `pose.x`, `items[0]`, 점이 있는 원래 키는 `"joint.angle"`처럼 지정합니다.
전체 값은 `.`입니다. 숫자 객체 키 `"0"`와 배열 `[0]`은 다릅니다. 기존 `$` 경로는
호환 입력이며 예제에서는 SQL형 경로를 우선합니다.

## 옵션 이름·목록·우선순위

이름은 소문자로 정확히 지정합니다. 일반 옵션은 SQL 문자열을 해석한 뒤 첫 등호에서 나누며
값 안의 뒤쪽 등호·공백은 보존합니다. 중복·미등록 옵션은 오류입니다.
SQL 문자열 안의 작은따옴표는 두 번 씁니다. names/null_values/sources의 목록 항목에
쉼표가 있으면 CSV 큰따옴표를 사용합니다.

명시 타입·고정 profile과 자동 추론의 우선순위는 포맷별로 확인합니다. CSV의 type은 원본 입력
컬럼, JSON의 project 사용 시 type은 출력 별칭을 기준으로 하므로 복사해서 쓰지 않습니다.
날짜·시각 형식의 컬럼별 지정은 공통 지정보다 우선합니다.

## 타입·스키마·값

원래 dtype·논리 타입과 SQL carrier는 다릅니다. 자동 추론은 prepare 단계의 표본으로 고정하며
실행 중 새 값이 나왔다고 메타데이터를 조용히 바꾸지 않습니다. 표본을 늘리거나 타입을
명시하고 새로 prepare합니다. 데이터값 변경, 구조 변경, 원본 revision과 mapping 변경은
서로 다른 개념입니다. SCHEMA_CHANGED면 구조를 다시 확인하고 statement를 새로 준비합니다.

native 정수의 NULL 예약값·JSON 32 KiB·VARCHAR 32 KiB·TEXT/BINARY의 64 MiB 한도와
reader별 레코드·작업 예산을 함께 적용합니다. native에서 표현할 수 없는 원래 값은
지원되는 envelope·원문 경로를 확인하며 오류를 임의의 NULL이나 잘린 값으로 대체하지 않습니다.
