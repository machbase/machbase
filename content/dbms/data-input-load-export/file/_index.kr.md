---
type: docs
title: '파일 적재'
weight: 30
---

Machbase는 CSV 파일을 클라이언트에서 서버로 전송하여 적재하는 CLI 도구를 제공합니다.

## 파일 적재 도구

| 도구 | 특징 | 주요 사용처 |
|------|------|-----------|
| `machloader` | 범용 적재/반출 도구. 스키마 파일로 유연한 매핑 | 배치 적재, 마이그레이션, 반출 |
| `csvimport` | machloader의 CSV 전용 래퍼. 옵션 단순화 | 빠른 CSV 적재 |
| `csvexport` | CSV 반출 전용 래퍼 | 빠른 CSV 반출 |
| `tagmetaimport` | TAG 메타데이터 전용 적재 | TAG 메타데이터 초기 로드·업데이트 |

## 이 절에서 다루는 내용

- **[CSV 파일 형식](./file-csv/)**: Machbase가 인식하는 CSV 규격
- **[machloader로 가져오기](./import-machloader/)**: 스키마 파일과 다양한 옵션 활용
- **[csvimport로 가져오기](./import-csvimport/)**: 간편한 CSV 적재
- **[tagmetaimport](./metadata-import-tagmetaimport-tag/)**: TAG 메타데이터 전용 임포트
