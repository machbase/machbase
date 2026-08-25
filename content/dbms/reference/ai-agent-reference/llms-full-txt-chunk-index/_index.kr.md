---
type: docs
title: '17.8.13 RAG chunk index 설계'
weight: 130
toc: true
---

이 페이지는 문서를 RAG용 청크로 내보낼 때 유지해야 할 경계와 메타데이터를 설명합니다.
현재 사이트는 루트 `/llms-full.txt` 파일을 배포하지 않으므로 해당 URL이 존재한다고 가정하지
마십시오.

## 청크 구성 원칙

- 하나의 SQL 문법, SDK 작업 또는 운영 절차를 가능한 한 한 청크에 둡니다.
- 제목 계층, canonical URL, Edition과 최소 버전을 메타데이터로 보존합니다.
- 코드 블록을 설명과 분리하지 않습니다.
- 오류 코드는 [오류 코드 사전](/dbms/reference/error-dictionary-codes/)을 단일 원본으로 둡니다.
- 내부 issue, commit, 소스 경로를 사용자 응답의 공개 근거로 노출하지 않습니다.

## canonical 범주

| 범주 | URL |
|---|---|
| SQL | `/dbms/reference/sql/` |
| SDK | `/dbms/development-tools-integration/` |
| 운영 | `/dbms/operations-configuration-recovery/` |
| 성능 | `/dbms/performance-tuning/` |
| 시나리오 | `/dbms/scenario-guides/` |
| 문제 해결 | `/dbms/troubleshooting/` |

실제 `llms.txt` 또는 전체 본문 파일을 제공하려면 Hugo 출력 생성, URL 검증, 버전 메타데이터와
배포 테스트를 별도 기능으로 구현해야 합니다. 구현 전에는 이 페이지를 파일 접근 경로로
사용하지 않습니다.
