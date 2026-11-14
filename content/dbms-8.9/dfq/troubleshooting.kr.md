---
type: docs
title: '12.11 문제 해결과 지원 범위'
weight: 110
toc: true
---

오류 이름과 발생 단계, 파일·target·row를 함께 확인합니다. 오류를 무조건 skip하거나
타입을 VARCHAR로 바꿔 성공시키기 전에 원래 데이터 의미를 확인합니다.

| 증상·오류 | 확인과 해결 |
|---|---|
| ACCESS_DENIED | 실행 사용자·catalog의 디렉터리 권한 확인 |
| IO_ERROR | 서버 OS 권한, 서버 경로, 일반 파일 여부 확인 |
| UNSUPPORTED_FORMAT | 실제 형식과 reader 지원 확인. format을 명시해 진단 |
| INVALID_OPTION | 옵션 철자·대소문자·허용 모드·값·중복 확인 |
| OPTION_CONFLICT | 위치형/source/sources 혼합, profile 고정 옵션과 중복 확인 |
| SCHEMA_UNAVAILABLE | 빈 입력·부족한 표본·대상 선택 확인. 명시 스키마 또는 표본 보완 |
| SCHEMA_CHANGED / SCHEMA_MISMATCH | 구조와 여러 파일의 타입·선택 대상을 확인하고 새 prepare |
| NATIVE_VALUE_UNREPRESENTABLE | NULL 예약값·길이·dtype·NUL 등 native 표현 경계 확인 |
| FIELD_NOT_FOUND / MISSING_VALUE | 원래 경로와 출력 별칭, 없는 필드·배열 위치 확인 |
| CORRUPT_DATA | 원본 framing·압축·CRC·포맷 구조 확인. 손상은 정상 빈 결과 아님 |
| LIMIT_EXCEEDED | 레코드·컬럼·해제·작업 예산 확인. 청크·선택 필드 활용 |
| SOURCE_CHANGED / MAPPING_CHANGED | 재조회 token과 실제 원본·해석 설정 확인 |
| SNAPSHOT_UNAVAILABLE | 서버·DB·context와 source 주소의 수명·권한 확인 |

## 지원표

| 포맷 | 주요 대상 | 배열·중첩 | 핵심 제약 |
|---|---|---|---|
| CSV/TSV | rows | 문자열 셀을 자동 구조화하지 않음 | 인코딩·타입·레코드 예산 |
| JSON/JSONL | rows/document | 객체·배열 | records와 물리 줄·부모 행 구분 |
| Parquet | rows | STRUCT/LIST/MAP | 여러 파일은 동일 선언 스키마 |
| NPY/NPZ | rows / 배열 | dtype·shape | 첫 축 행, NPZ member 선택 |
| MCAP | messages/topics/schemas/attachments/metadata | 지원되는 payload 해석 | 모든 메시지 codec·센서 타입을 의미하지 않음 |
| HDF5 | dataset/group | dtype·shape·compound | 외부 링크·VDS·plugin 제외 |
| LeRobot | steps/episodes/tasks/media | 배열과 미디어 참조 | v2.1/v3.0 root 하나, 미디어 디코딩 제외 |

DFQ는 Standard Edition 기능입니다. Cluster의 분산 파일 읽기를 의미하지 않습니다.
지원 reader와 옵션은 해당 서버 빌드의 HELP·inspect·capability 및 포맷별 설명으로 확인합니다.
Arrow 라이브러리가 포함되어 있다고 독립 Arrow 파일 reader가 제공되는 것은 아닙니다.
YAML·ROS bag·Zarr 등 예정·관련 형식을 지원 목록에 추가하지 않습니다.

on_error=skip은 일부 reader의 완전한 레코드 오류 복구에만 사용합니다. Parquet·LeRobot은
skip을 허용하지 않으며 I/O·자원·취소·경계를 복구할 수 없는 손상은 쿼리를 중단합니다.

[포맷별 상세 사용법](../formats/)의 오류 예제를 정상 실행 파일과 분리해 사용합니다.

## 실행 환경

Standard 배포판의 Linux x86-64·ARM64, macOS x86-64·ARM64, Windows UCRT64 환경에서
지원 reader가 포함된 패키지를 사용합니다. Parquet·LeRobot·HDF5는 해당 reader가 활성화된
패키지가 필요합니다. Cluster에서 같은 파일·분산 실행 지원을 가정하지 않습니다.
Windows는 드라이브가 있는 서버 절대 경로를 사용합니다. 포맷별 codec·plugin·미디어
지원 범위는 플랫폼 이름만으로 확대되지 않습니다.

Linux의 Parquet 배포는 glibc 2.17 이상, HDF5 배포는 glibc 2.27 이상을 대상으로 합니다.
macOS의 해당 reader 배포는 11.0 이상을 대상으로 합니다. 실제 설치 패키지의 reader 포함
여부를 확인합니다.
