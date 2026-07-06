---
type: docs
title: '6. 데이터 입력, 적재, 반출'
weight: 60
---

Machbase에 데이터를 입력하는 방법은 여러 가지입니다. SQL INSERT, Append API, 파일 적재(machloader, csvimport), SQL 기반 파일 직접 로드까지 상황에 따라 선택할 수 있습니다. 반출도 동일한 도구를 내보내기 방향으로 사용합니다.

## 이 장에서 다루는 내용

- **[입력 방식 선택](./selection-input-method/)**: 테이블 타입·데이터 볼륨에 따른 입력 방법 선택 기준
- **[SQL 입력](./sql/)**: INSERT 구문, Append API, LOAD DATA INFILE
- **[파일 적재](./file/)**: machloader, csvimport, tagmetaimport를 이용한 파일 기반 입력
- **[데이터 반출](./export/)**: SAVE DATA INTO, machloader, csvexport를 이용한 데이터 내보내기
- **[배치와 오류 처리](./error-handling/)**: 대량 입력 시 오류 처리와 배치 전략
- **[입력 성능과 연동 경로](./performance/)**: 입력 경로별 성능 원칙과 권장 구성
