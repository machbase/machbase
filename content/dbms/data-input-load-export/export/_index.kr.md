---
type: docs
title: '데이터 반출'
weight: 50
---

Machbase 테이블의 데이터를 파일로 내보내는 방법을 정리합니다.

## 반출 방법 개요

| 방법 | 특징 |
|------|------|
| `SAVE DATA INTO` | SQL 구문으로 SELECT 결과를 서버 측 파일로 직접 저장 |
| `machloader -o` | CLI 도구. 스키마 파일 지원. 클라이언트 파일시스템에 저장 |
| `csvexport` | machloader 내보내기 래퍼. 간편 CSV 반출 |

## 이 절에서 다루는 내용

- **[반출 작업 소유권](./export-ownership/)**: 반출 파일 권한 관리
- **[SAVE DATA INTO](./export-sql-save-data-into/)**: SQL 기반 서버 측 파일 저장
- **[machloader로 내보내기](./export-machloader/)**: CLI 기반 반출
- **[csvexport로 내보내기](./export-csvexport/)**: 간편 CSV 반출
